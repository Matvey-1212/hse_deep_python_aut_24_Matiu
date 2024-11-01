"""
файл тестирования клиента
"""

import unittest
from unittest.mock import patch
import socket
import json
from client import Client, process_urls


class TestClient(unittest.TestCase):
    """
    тестирование клиента
    """
    @patch("socket.socket")
    def test_send_url_success(self, mock_socket):
        """
        Тестирование успешной отправки URL на сервер и получения ответа.
        """
        mock_socket_instance = mock_socket.return_value.__enter__.return_value
        mock_socket_instance.recv.return_value = json.dumps(
            {"word1": 10, "word2": 5}
            ).encode()

        client = Client()
        response = client.send_url("http://example.com")

        self.assertEqual(response, {"word1": 10, "word2": 5})
        mock_socket_instance.sendall.assert_called_once_with(
            "http://example.com".encode()
        )
        mock_socket_instance.connect.assert_called_once_with(
            ("localhost", 8080)
        )

    @patch("socket.socket")
    def test_send_url_connection_error(self, mock_socket):
        """
        Тестирование обработки ошибки соединения.
        """

        (mock_socket.
         return_value.
         __enter__.
         return_value.
         connect.
         side_effect) = socket.error("Connection failed")

        client = Client()
        with self.assertRaises(socket.error):
            client.send_url("http://example.com")

    @patch("builtins.open", create=True)
    @patch("client.Client.send_url")
    def test_process_urls_with_error(self, mock_send_url, mock_open):
        """
        Тестирование process_urls: обработка ошибки при отправке URL.
        """
        mock_send_url.side_effect = ConnectionError("Ошибка подключения")

        mock_open.return_value.__enter__.return_value = ["http://example.com"]

        with patch("sys.stdout") as mock_stdout:
            process_urls("url.txt")
            self.assertIn("Ошибка на http://example.com:" +
                          " Ошибка подключения",
                          mock_stdout.write.call_args_list[0][0][0])

    def test_client_initialization(self):
        """
        Тестирование инициализации клиента с различными хостами и портами.
        """
        client = Client(server_host="127.0.0.1", server_port=9090)
        self.assertEqual(client.server_host, "127.0.0.1")
        self.assertEqual(client.server_port, 9090)

    def test_valid_initialization(self):
        """
        Тестирование корректной инициализации с правильными значениями.
        """
        client = Client(server_host="localhost", server_port=8080)
        self.assertEqual(client.server_host, "localhost")
        self.assertEqual(client.server_port, 8080)

    def test_invalid_server_host_type(self):
        """
        Тестирование инициализации с некорректным типом server_host.
        """
        with self.assertRaises(ValueError) as context:
            Client(server_host=123, server_port=8080)
        self.assertEqual(str(context.exception), "server_host" +
                         " должен быть непустой строкой.")

    def test_empty_server_host(self):
        """
        Тестирование инициализации с пустым значением server_host.
        """
        with self.assertRaises(ValueError) as context:
            Client(server_host="", server_port=8080)
        self.assertEqual(str(context.exception), "server_host" +
                         " должен быть непустой строкой.")

    def test_invalid_server_port_type(self):
        """
        Тестирование инициализации с некорректным типом server_port.
        """
        with self.assertRaises(ValueError) as context:
            Client(server_host="localhost", server_port="not_a_number")
        self.assertEqual(str(context.exception), "server_port должен быть" +
                         " целым числом в диапазоне от 1 до 65535.")

    def test_server_port_out_of_range_low(self):
        """
        Тестирование инициализации с server_port ниже допустимого диапазона.
        """
        with self.assertRaises(ValueError) as context:
            Client(server_host="localhost", server_port=0)
        self.assertEqual(str(context.exception), "server_port должен быть" +
                         " целым числом в диапазоне от 1 до 65535.")

    def test_server_port_out_of_range_high(self):
        """
        Тестирование инициализации с server_port выше допустимого диапазона.
        """
        with self.assertRaises(ValueError) as context:
            Client(server_host="localhost", server_port=70000)
        self.assertEqual(str(context.exception), "server_port должен быть" +
                         " целым числом в диапазоне от 1 до 65535.")


if __name__ == "__main__":
    unittest.main()
