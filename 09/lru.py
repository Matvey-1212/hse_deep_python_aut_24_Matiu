"""
    Файл соддержит реализацию LRUCache вместе с логированием
    через двунаправленный список хранящий элементы
    в порядке их последнего обращения и
    словаря для хранения ссылок на элементы списка
"""
import logging
import argparse
import sys


class Node:
    """
        Класс элемента двусявязного списка
    """

    def __init__(self,
                 key: str,
                 value: any = None
                 ):
        """
            Инициализация элемента
        """
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

    def get(self) -> any:
        """
            Обход pylint
        """
        return self.value

    def __str__(self) -> str:
        """
            Обход pylint
        """
        return str(self.key)


class LRUCache:
    """
        Класс LRUCache на основе двунаправленного
        списка и словаря ссылок на элементы списка
    """

    def __init__(self,
                 max_items: int = 10
                 ):
        """
            Инициализация
        """
        if not isinstance(max_items, int):
            logging.critical("LRU_init:Тип max_items, "
                             "некорректен: %s",
                             type(max_items))
            raise TypeError("max_items должен быть int, "
                            f"сейчас max_items: {type(max_items)}")
        if max_items <= 0:
            logging.critical("LRU_init: Попытка инициализировать, "
                             "LRUCache с некорректной ёмкостью: %s",
                             max_items)
            raise ValueError("max_items должен быть больше 0, "
                             f"сейчас max_items = {max_items}")

        self.max_items = max_items
        self.cache = {}
        self.head = Node(key='head')
        self.tail = Node(key='tail')
        self.head.next = self.tail
        self.tail.prev = self.head
        logging.info("LRU_init: Создан LRUCache с ёмкостью %s",
                     self.max_items)

    def _remove(self, node: Node) -> None:
        """
            Удаление узла из двусвязного списка
        """
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        logging.debug("LRU_remove: Узел %s удалён из списка.",
                      node.key)

    def _add(self, node: Node) -> None:
        """
            Добавление узла в начало
        """
        next_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = next_node
        next_node.prev = node
        logging.debug("LRU_add: Узел %s добавлен в начало списка.",
                      node.key)

    def get(self, key: str) -> any:
        """
            Получение значения из LRUCache
        """
        if key not in self.cache:
            logging.warning(
                "LRU_get: Попытка получить отсутствующий ключ: %s",
                key
            )
            return None
        node = self.cache[key]
        self._remove(node)
        self._add(node)
        logging.info(
            "LRU_get: Получен существующий ключ: %s, "
            "со значением: %s",
            key,
            node.value
        )
        return node.value

    def set(self,
            key: str,
            value: any = None
            ) -> None:
        """
            Задание значения в LRUCache
        """
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add(node)
            logging.info(
                "LRU_set: Обновлён существующий ключ: %s "
                "с новым значением: %s",
                key,
                value
            )
        else:
            if len(self.cache) >= self.max_items:
                node_to_remove = self.tail.prev
                self._remove(node_to_remove)
                del self.cache[node_to_remove.key]
                logging.info(
                    "LRU_set: Достигнута ёмкость. "
                    "Удалён ключ: %s "
                    "со значением: %s",
                    node_to_remove.key,
                    node_to_remove.value
                    )

            new_node = Node(key, value)
            self._add(new_node)
            self.cache[key] = new_node
            logging.info(
                "LRU_set: Установлен новый ключ: %s "
                "со значением: %s",
                key,
                value
                )

        logging.debug("LRU_set: Текущее состояние "
                      "кэша: %s",
                      self._current_cache_state()
                      )

    def __getitem__(self, key: str) -> any:
        """
            Получение значения из LRUCache черех []
        """
        return self.get(key)

    def __setitem__(self,
                    key: str,
                    value: any
                    ) -> None:
        """
            Задание значения в LRUCache через []
        """
        self.set(key, value)

    def _current_cache_state(self) -> str:
        """
        Возвращает текущее состояние кэша для отладки
        """
        keys = []
        current = self.head.next
        while current != self.tail:
            keys.append(str(current.key) + ' : ' + str(current.value))
            current = current.next
        return " -> ".join(keys)


# pylint: disable=too-few-public-methods
class CastomFilter(logging.Filter):
    """
    Кастомный фильтр
    """
    def __init__(self, keywords=None):
        """
        Инициализация
        """
        super().__init__()
        self.keywords = keywords if keywords is not None else []

    def filter(self, record):
        """
        метод фильтрации
        """
        message = record.getMessage()

        if any(keyword.lower() in message.lower() for keyword in self.keywords):
            return True

        return False


def setup_logging(show_stdout=False, apply_filter=False):
    """
    задание параметров логирования
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
        )

    file_handler = logging.FileHandler('cache.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    if apply_filter:
        file_handler.addFilter(CastomFilter(['init']))

    logger.addHandler(file_handler)

    if show_stdout:
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(console_formatter)

        if apply_filter:
            console_handler.addFilter(CastomFilter(['init']))

        logger.addHandler(console_handler)


def parse_arguments():
    """
    Парсер
    """
    parser = argparse.ArgumentParser(description="LRUCache")
    parser.add_argument('-s',
                        action='store_true',
                        help='Логировать в stdout'
                        )
    parser.add_argument('-f',
                        action='store_true',
                        help='Применить кастомный фильтр'
                        )
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_arguments()
    setup_logging(show_stdout=args.s, apply_filter=args.f)

    cache = LRUCache(3)

    cache.set('k1', 'A')  # set отсутствующего ключа
    cache.set('k2', 'B')  # set отсутствующего ключа
    cache.set('k3', 'C')  # set отсутствующего ключа
    cache.set('k4', 'D')  # set отсутствующего ключа, когда достигнута ёмкость
    cache.get('k2')        # get существующего ключа
    cache.get('k5')        # get отсутствующего ключа
    cache.set('k3', 'new_C')  # set существующего ключа

    try:
        cache = LRUCache(0)
    except ValueError:
        pass

    try:
        cache = LRUCache('3')
    except TypeError:
        pass
