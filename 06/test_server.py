"""
файл тестирования сервера
"""

import json
from urllib.error import URLError
import unittest
from unittest.mock import patch, MagicMock
from queue import Queue
from threading import Lock
from server import Worker, MasterServer


class TestWorker(unittest.TestCase):
    """
        тестирование воркера
    """
    @patch("server.urlopen")
    def test_worker_returns_correct_values_to_client(self, mock_urlopen):
        """
        тестирование воркера
        """
        mock_response = MagicMock()
        mock_response.read.return_value = b"hello world world test test test"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        mock_client_socket = MagicMock()

        task_queue = Queue()
        counter = [0]
        lock = Lock()
        task_queue.put((mock_client_socket, "http://example.com"))

        worker = Worker(task_queue,
                        top_k=2,
                        counter=counter,
                        lock=lock,
                        worker_id=1
                        )
        worker.start()

        task_queue.join()

        worker.stop()
        worker.join()

        expected_result = json.dumps({"test": 3, "world": 2}).encode()

        mock_client_socket.sendall.assert_called_once_with(expected_result)
        self.assertEqual(counter[0], 1)

    # pylint: disable=unused-argument
    @patch("server.urlopen", side_effect=URLError("Connection error"))
    def test_worker_process_url_error(self, mock_urlopen):
        """
        тестирование воркера
        """
        mock_socket = MagicMock()

        task_queue = Queue()
        counter = [0]
        lock = Lock()
        task_queue.put((mock_socket, "http://example.com"))

        worker = Worker(task_queue,
                        top_k=2,
                        counter=counter,
                        lock=lock,
                        worker_id=1
                        )
        worker.start()

        task_queue.join()
        worker.stop()
        worker.join(timeout=2)

        expected_error = json.dumps(
            {"error": "<urlopen error Connection error>"}
            ).encode()
        mock_socket.sendall.assert_called_once_with(expected_error)
        self.assertEqual(counter[0], 1)


class TestMasterServer(unittest.TestCase):
    """
        тестирование мастера
    """
    @patch("socket.socket")
    def test_master_server_handle_client(self, mock_socket):
        """
        тестирование создания очереди задач
        """
        server = MasterServer(host="localhost",
                              port=8080,
                              num_workers=3,
                              top_k=2
                              )

        mock_client_socket = MagicMock()
        server_socket_instance = mock_socket.return_value.__enter__.return_value
        server_socket_instance.accept.return_value = (mock_client_socket,
                                                      ('127.0.0.1', 12345))

        server.handle_client(mock_client_socket)

        self.assertTrue(server.task_queue.qsize() > 0)


if __name__ == "__main__":
    unittest.main()
