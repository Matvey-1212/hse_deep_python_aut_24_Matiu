"""
файл сервера
"""

import socket
import threading
import json
import argparse
from collections import Counter
from queue import Queue, Empty
from urllib.request import urlopen
from urllib.error import URLError


class Worker(threading.Thread):
    """
    Воркер, который обрабатывает урлы из
    очереди заданий и отправляет ответ клиенту

    Аргументы:
        task_queue (Queue): Общая очередь заданий
        top_k (int): Количество наиболее частых слов для возврата клиенту
        counter (Counter): Счетчик обработанных урлов
        lock (Lock): Блокировка для безопасного увеличения счетчика
    """
    # pylint: disable=too-many-arguments
    def __init__(self, task_queue, top_k, counter, lock, worker_id):
        super().__init__()
        self.task_queue = task_queue
        self.top_k = top_k
        self.counter = counter
        self.lock = lock
        self.worker_id = worker_id
        self.stop_event = threading.Event()

    def run(self):
        """
        Постоянно обрабатывает задания из очереди,
        если они есть, и отправляет результат клиенту
        """
        while not self.stop_event.is_set():
            try:
                client_socket, url = self.task_queue.get(timeout=1)

                try:
                    with urlopen(url) as response:
                        html = response.read().decode('utf-8')
                        words = html.split()
                        common_words = Counter(words).most_common(self.top_k)
                        result = dict(common_words)
                        client_socket.sendall(json.dumps(result).encode())
                except (URLError, UnicodeDecodeError) as e:
                    error_message = json.dumps({"error": str(e)}).encode()
                    client_socket.sendall(error_message)
                finally:
                    client_socket.close()
                    self.task_queue.task_done()

                    with self.lock:
                        self.counter[0] += 1
                        print(f"Обработано URL суммарно: {self.counter[0]}")

            except Empty:
                continue

    def stop(self):
        """
        Устанавливает флаг остановки для воркера
        """
        self.stop_event.set()


class MasterServer:  # pylint: disable=too-many-instance-attributes
    """
    Мастер-сервер для приема запросов и раздаче их ворккерам
    Аргументы:
        host (str): Хост сервера
        port (int): Порт сервера
        num_workers (int): Количество воркеров для обработки запросов
        top_k (int): Количество наиболее частых слов для возврата клиенту
    """
    def __init__(self, host="localhost", port=8080, num_workers=10, top_k=5):
        self.host = host
        self.port = port
        self.top_k = top_k
        self.num_workers = num_workers
        self.task_queue = Queue()
        self.counter = [0]
        self.lock = threading.Lock()
        self._stop_event = threading.Event()
        self.workers = [
            Worker(self.task_queue, self.top_k, self.counter, self.lock, i)
            for i in range(num_workers)
        ]

    def start_workers(self):
        """
        Запускает все воркеры для постоянного ожидания задач
        """
        for worker in self.workers:
            worker.start()

    def handle_client(self, client_socket):
        """
        Обрабатывает запрос от клиента, добавляя его в очередь задач
        """
        url = client_socket.recv(4096).decode()
        self.task_queue.put((client_socket, url))

    def start(self):
        """
        Запускает сервер, слушает порт и распределяет запросы по воркерам
        """
        self.start_workers()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Сервер слушает порт {self.host}:{self.port}")

            while not self._stop_event.is_set():
                client_socket, _ = server_socket.accept()
                self.handle_client(client_socket)

    def stop(self):
        """
        Останавливает сервер и завершает работу воркеров
        """
        self._stop_event.set()
        for worker in self.workers:
            worker.stop()
        for worker in self.workers:
            worker.join()
        print("Сервер остановлен")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workers", type=int, required=True)
    parser.add_argument("-k", "--top_k", type=int, required=True)

    args = parser.parse_args()

    server = MasterServer(num_workers=args.workers, top_k=args.top_k)
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nОстановка сервера")
    finally:
        server.stop()
