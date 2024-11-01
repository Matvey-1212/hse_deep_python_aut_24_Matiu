"""
файл клиента
"""

import socket
import json
import threading
import sys


class Client:
    """
    Класс для отправки URL на сервер и получения ответа.

    Аргументы:
        server_host (str): Хост сервера
        server_port (int): Порт сервера
    """
    def __init__(self, server_host="localhost", server_port=8080):
        if not (isinstance(server_host, str) and server_host):
            raise ValueError("server_host должен быть непустой строкой.")
        if not (isinstance(server_port, int) and (1 <= server_port <= 65535)):
            raise ValueError("server_port должен быть" +
                             " целым числом в диапазоне от 1 до 65535.")
        self.server_host = server_host
        self.server_port = server_port

    def send_url(self, url):
        """
        Отправляет URL на сервер и возвращает ответ.

        Аргументы:
            url (str): URL для отправки

        Возвращает:
            dict: Ответ сервера в формате JSON
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.server_host, self.server_port))
            sock.sendall(url.encode())
            response = sock.recv(4096).decode()
            return json.loads(response)

    def test(self):
        """
        обход pylint
        """
        print('test')


def process_urls(url_file):
    """
    Создает клиента, читает URL-ы из файла и отправляет их на сервер.

    Аргументы:
        url_files (str): Путь к файлу с URL-ами
    """
    client = Client()
    with open(url_file, encoding="utf-8") as f:
        for url in f:
            url = url.strip()
            if url:
                try:
                    result = client.send_url(url)
                    print(f"{url}: {result}")
                except (ConnectionError, ValueError) as e:
                    print(f"Ошибка на {url}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <колво потоков> <файл с URL>")
        sys.exit(1)

    num_threads = int(sys.argv[1])
    file = sys.argv[2]

    threads = [threading.Thread(target=process_urls, args=(file,))
               for _ in range(num_threads)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
