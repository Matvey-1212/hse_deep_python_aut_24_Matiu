"""
    Тесты для функции process_json, которая обрабатывает JSON строки
"""

import unittest
from unittest.mock import Mock
from json_parser import process_json


class TestProcessJson(unittest.TestCase):
    """
        Класс тестов для функции process_json
    """

    def setUp(self):
        """
            Настройка для тестов, добавляющая Mock объект для Callback
        """
        self.callback = Mock()

    def test_process_json_with_all_parameters(self):
        """
            Тест с корректными параметрами
        """
        json_str = '{"key1": "word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2", "key3"]
        tokens = ["word1", "word2"]

        process_json(json_str, required_keys, tokens, self.callback)

        self.callback.assert_any_call("key1", "word2")
        self.callback.assert_any_call("key1", "word1")
        self.callback.assert_any_call("key2", "word2")
        self.assertEqual(self.callback.call_count, 3)

    def test_process_json_with_case_sensitive_keys(self):
        """
        Тест регистрозависимости ключей
        """
        json_str = '{"KEY1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = ["word1", "word2"]

        process_json(json_str, required_keys, tokens, self.callback)

        self.callback.assert_any_call("key2", "word2")
        self.assertEqual(self.callback.call_count, 1)

    def test_process_json_without_required_keys(self):
        """
            Тест с отсутствующими ключами
        """
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        tokens = ["WORD1", "word2"]

        process_json(json_str, [], tokens, self.callback)
        self.callback.assert_not_called()

    def test_process_json_without_tokens(self):
        """
            Тест с отсутствующими токенами
        """
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]

        process_json(json_str, required_keys, [], self.callback)
        self.callback.assert_not_called()

    def test_process_json_with_empty_json(self):
        """
            Тест с пустым JSON
        """
        json_str = '{}'
        required_keys = ["key1", "key2"]
        tokens = ["WORD1", "word2"]

        process_json(json_str, required_keys, tokens, self.callback)
        self.callback.assert_not_called()

    def test_process_json_with_case_insensitive_tokens(self):
        """
            Тест регистронезависимости токенов
        """
        json_str = '{"key1": "WORD1 WoRd2", "key2": "wOrd2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = ["word1", "word2", "word3"]

        process_json(json_str, required_keys, tokens, self.callback)

        self.callback.assert_any_call("key1", "WORD1")
        self.callback.assert_any_call("key1", "WoRd2")
        self.callback.assert_any_call("key2", "wOrd2")
        self.callback.assert_any_call("key2", "word3")
        self.assertEqual(self.callback.call_count, 4)

    def test_process_json_without_callback(self):
        """
            Тест без функции-обработчика
        """
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = ["word1", "word2"]

        process_json(json_str, required_keys, tokens)

    def test_process_json_keyword_arguments(self):
        """
            Тест на использование именованных аргументов
        """
        json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
        required_keys = ["key1", "key2"]
        tokens = ["word1", "word2"]

        process_json(
            json_str,
            required_keys=required_keys,
            tokens=tokens
            )

        process_json(
            json_str,
            tokens=tokens
            )

        process_json(
            json_str,
            required_keys=required_keys
            )

    def test_invalid_input_words_type(self):
        """
            Тест некорректных типов входных данных
        """
        with self.assertRaises(TypeError):
            json_str = '{"key1": "WORD1 WoRd2", "key2": "wOrd2 word3"}'
            tokens = ["word1", "word2", "word3"]
            process_json(json_str, 1, tokens, self.callback)

        with self.assertRaises(TypeError):
            json_str = '{"key1": "WORD1 WoRd2", "key2": "wOrd2 word3"}'
            tokens = ["word1", "word2", "word3"]
            process_json(json_str, [1], tokens, self.callback)

        with self.assertRaises(TypeError):
            json_str = '{"key1": "WORD1 WoRd2", "key2": "wOrd2 word3"}'
            required_keys = ["key1", "key2"]
            process_json(json_str, required_keys, 1, self.callback)

        with self.assertRaises(TypeError):
            json_str = '{"key1": "WORD1 WoRd2", "key2": "wOrd2 word3"}'
            required_keys = ["key1", "key2"]
            process_json(json_str, required_keys, [1], self.callback)

        with self.assertRaises(TypeError):
            required_keys = ["key1", "key2"]
            tokens = ["word1", "word2", "word3"]
            process_json(1, required_keys, tokens, self.callback)

    def test_invalid_json_str(self):
        """
            Тест корректности json строки
        """
        with self.assertRaises(ValueError):
            json_str = '{'
            required_keys = ["key1", "key2"]
            tokens = ["word1", "word2", "word3"]
            process_json(json_str, required_keys, tokens, self.callback)


if __name__ == '__main__':
    unittest.main()
