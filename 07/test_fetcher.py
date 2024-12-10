"""
    В файле реализованы тесты для класса Fetcher
"""

# import time
import unittest
import asyncio
from fetcher import Fetcher


class TestFetcher(unittest.TestCase):
    """
        Тесты для класса Fetcher
    """
    def setUp(self):
        """
        Инициализация перед каждым тестом
        """
        self.valid_urls = [
            'https://httpbin.org/get',
            'https://httpbin.org/status/200',
            'https://httpbin.org/delay/1'
        ]
        self.invalid_urls = [
            'https://httpbin.org/status/404',
            'https://invalid-url',
            'invalid_url'
        ]
        self.concurrency = 2
        self.fetcher = Fetcher(self.concurrency)

    def test_fetch_valid_urls(self):
        """
        Тест успешной обкачки корректных урлов
        """
        async def run_test():
            await self.fetcher.run(self.valid_urls)
            self.assertEqual(len(self.fetcher.results), len(self.valid_urls))
            for url, content, exception in self.fetcher.results:
                self.assertIsNotNone(content)
                self.assertIsNone(exception)
                self.assertIn(url, self.valid_urls)
        asyncio.run(run_test())

    def test_fetch_invalid_urls(self):
        """
        Тест обработки некорректных урлов
        """
        async def run_test():
            await self.fetcher.run(self.invalid_urls)
            self.assertEqual(len(self.fetcher.results), len(self.invalid_urls))
            for url, content, exception in self.fetcher.results:
                self.assertIsNone(content)
                self.assertIsNotNone(exception)
                self.assertIn(url, self.invalid_urls)
        asyncio.run(run_test())

    # def test_concurrency_performance(self):
    #     """
    #     Тест скорости при разных значениях concurrency
    #     """
    #     async def run_test():
    #         urls = ['https://httpbin.org/delay/1'] * 10

    #         fetcher = Fetcher(concurrency=1)
    #         start_time = time.time()
    #         await fetcher.run(urls)
    #         time_concurrency_1 = time.time() - start_time
    #         print("Время выполнения с concurrency=1: " +
    #               f"{time_concurrency_1:.2f} секунд")

    #         fetcher = Fetcher(concurrency=10)
    #         start_time = time.time()
    #         await fetcher.run(urls)
    #         time_concurrency_10 = time.time() - start_time
    #         print("Время выполнения с concurrency=10: " +
    #               f"{time_concurrency_10:.2f} секунд")

    #         self.assertTrue(time_concurrency_10 < time_concurrency_1)
    #         self.assertTrue(time_concurrency_10 < 5)
    #         self.assertTrue(time_concurrency_1 >= 10)

    #     asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()
