"""
В файле реализованы тесты ддля custom_json
"""
import time
import os
import json
import random
import string
import unittest
import custom_json
import numpy as np


class TestCustomJson(unittest.TestCase):
    """
    Класс тестов
    """
    @classmethod
    def setUpClass(cls):
        """
            Генерация тестовых файлов
        """
        cls.test_files = []
        num_files = 9
        num = 500000

        for i in range(1, num_files + 1):
            filename = f"generated_data_{i}.json"
            cls.test_files.append(filename)

            test_data = {}
            for i in range(num):
                test_data[f"test_string_{i}"] = ''.join(
                    random.choices(string.ascii_letters + string.digits, k=20)
                    )

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(test_data, f, ensure_ascii=False, indent=4)

    @classmethod
    def tearDownClass(cls):
        """
            Удаление тестовых файлов
        """
        for filename in cls.test_files:
            if os.path.exists(filename):
                os.remove(filename)

    def test_custom_json_loads(self):
        """
        Тест loads из custom_json
        """
        json_string = '{"hello": 10, "world": "value"}'
        expected = {'hello': 10, 'world': 'value'}
        result = custom_json.loads(json_string)  # pylint: disable=I1101
        self.assertEqual(result, expected)

        json_string = '{"hello": 10, \t "world": \n"value"}'
        expected = {'hello': 10, 'world': 'value'}
        result = custom_json.loads(json_string)  # pylint: disable=I1101
        self.assertEqual(result, expected)

        json_string = '{"a": 100, "b": 0.5, "c": -42, "d": 0.0001}'
        expected = {'a': 100, 'b': 0.5, 'c': -42, 'd': 1e-4}
        result = custom_json.loads(json_string)  # pylint: disable=I1101
        self.assertEqual(result, expected)

        json_string = '{}'
        expected = {}
        result = custom_json.loads(json_string)  # pylint: disable=I1101
        self.assertEqual(result, expected)

        json_string = '{"key": ""}'
        expected = {'key': ''}
        result = custom_json.loads(json_string)  # pylint: disable=I1101
        self.assertEqual(result, expected)

    def test_custom_json_dumps(self):
        """
        Тест функции dumps из custom_json
        """
        data = {'hello': 10, 'world': 'value'}
        expected = '{"hello": 10, "world": "value"}'
        result = custom_json.dumps(data)  # pylint: disable=I1101
        self.assertEqual(result, expected)

        data = {'a': 100, 'b': 0.5, 'c': -42, 'd': 1e-4, 'e': 0.0}
        expected = '{"a": 100, "b": 0.5, "c": -42, "d": 0.0001, "e": 0.0}'
        result = custom_json.dumps(data)  # pylint: disable=I1101
        self.assertEqual(result, expected)

        data = {}
        expected = '{}'
        result = custom_json.dumps(data)  # pylint: disable=I1101
        self.assertEqual(result, expected)

        data = {'key': ''}
        expected = '{"key": ""}'
        result = custom_json.dumps(data)  # pylint: disable=I1101
        self.assertEqual(result, expected)

    def test_json_comparison(self):
        """
        Сравнение результатов из custom_json и json
        """
        test_files = [f"generated_data_{i}.json" for i in range(1, 10)]

        for test_file in test_files:
            with open(test_file, 'r', encoding='utf-8') as f:
                data = f.read()

            # pylint: disable=I1101
            custom_json_result = custom_json.loads(data)
            json_result = json.loads(data)
            self.assertEqual(custom_json_result, json_result)
            # pylint: disable=I1101
            custom_json_result = custom_json.dumps(custom_json_result)
            json_result = json.dumps(json_result)
            self.assertEqual(custom_json_result, json_result)

    def test_performance(self):
        # непонятно условие дз, нужно чтобы разница выполнения была 100мс
        # не более или именно проверка на
        # каждом файле (то есть критерий размера файлов)
        """
        Сравнение производдительности custom_json и json
        """
        test_files = [f"generated_data_{i}.json"
                      for i in range(1, 10)]

        custom_loads_times = []
        custom_dupm_times = []
        loads_times = []
        dupm_times = []

        for test_file in test_files:
            with open(test_file, 'r', encoding='utf-8') as f:
                large_json = f.read()

            start_time = time.time()
            custom_json.loads(large_json)  # pylint: disable=I1101
            custom_json_duration = time.time() - start_time

            custom_loads_times.append(custom_json_duration)
            self.assertGreater(custom_json_duration, 0.1)

            start_time = time.time()
            # pylint: disable=I1101
            custom_json.dumps(custom_json.loads(large_json))
            custom_json_dumps_duration = time.time() - start_time

            custom_dupm_times.append(custom_json_dumps_duration)
            self.assertGreater(custom_json_dumps_duration, 0.1)

            start_time = time.time()
            json.loads(large_json)
            json_duration = time.time() - start_time

            loads_times.append(json_duration)
            self.assertGreater(json_duration, 0.1)

            start_time = time.time()
            json.dumps(json.loads(large_json))
            json_dumps_duration = time.time() - start_time

            dupm_times.append(json_dumps_duration)
            self.assertGreater(json_dumps_duration, 0.1)

        print("AVG время custom_loads: " +
              f"{np.mean(custom_loads_times):.4f} секунд")
        print("AVG время custom_dumps: " +
              f"{np.mean(custom_dupm_times):.4f} секунд")
        print(f"AVG время loads: {np.mean(loads_times):.4f} секунд")
        print(f"AVG время dumps: {np.mean(dupm_times):.4f} секунд")


if __name__ == "__main__":
    unittest.main()
