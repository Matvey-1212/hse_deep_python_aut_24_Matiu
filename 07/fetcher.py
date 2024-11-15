"""
В файле реализована асинхронная обкачка урлов
"""

import sys
import argparse
import asyncio
import aiohttp


class Fetcher:
    """
        Класс для асинхронной обкачки списка URL-адресов.
    """
    def __init__(self, concurrency):
        """
            Инициализация

            Аргументы:
                concurrency (int): Максимальное количество
                                    одновременных запросов
        """
        self.concurrency = concurrency
        self.results = []

    async def fetch(self, session, url, semaphore):
        """
            Асинхронно получает содержимое указанного урла

            Аргументы:
                session (aiohttp.ClientSession): Сессия aiohttp для
                                        выполнения запросов
                url (str): урлы для обкачки
                semaphore (asyncio.Semaphore): Семафор для ограничения
                                        количества одновременных запросов
        """
        async with semaphore:
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise aiohttp.ClientResponseError(
                            status=response.status,
                            request_info=response.request_info,
                            history=response.history,
                            message=f"Status code {response.status}"
                        )
                    content = await response.text()
                    print(
                        f"Успешно получен URL: {url}, " +
                        f"кол-во буковок {len(content)}"
                        )
                    return (url, content, None)
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f"Ошибка при загрузке URL {url}: {e}")
                return (url, None, e)

    async def run(self, urls):
        """
            Запускает асинхронную обкачку списка урлов

            Аргументы:
                urls (list): Список урлов для обкачки
        """
        semaphore = asyncio.Semaphore(self.concurrency)
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(
                self.fetch(session, url, semaphore)
                ) for url in urls]
            self.results = await asyncio.gather(*tasks)


def parse_args():
    """
        Парсит входные аргументы
    """
    parser = argparse.ArgumentParser(
        description="Асинхронный фетчер URL-адресов"
        )
    parser.add_argument("-c", "--concurrency", type=int, default=10,
                        help="Количество одновременных запросов")
    parser.add_argument("file", type=str, help="Путь к файлу с URL-адресами")
    return parser.parse_args()


def read_urls(file_path):
    """
        Читает файл урлов

        Аргументы:
            file_path (str): Путь к файлу с урлами
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        sys.exit(1)


def main():
    """
        Основная функция программы
    """
    args = parse_args()
    urls = read_urls(args.file)
    fetcher = Fetcher(args.concurrency)

    asyncio.run(fetcher.run(urls))


if __name__ == "__main__":
    main()
