"""
    Файл соддержит реализацию LRUCache
    через двунаправленный список хранящий элементы
    в порядке их последнего обращения и
    словаря для хранения ссылок на элементы списка
"""


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
        if max_items <= 0:
            raise ValueError("max_items должен быть больше 0, "
                             f"сейчас max_items = {max_items}")
        if not isinstance(max_items, int):
            raise TypeError("max_items должен быть int, "
                            f"сейчас max_items: {type(max_items)}")

        self.max_items = max_items
        self.cache = {}
        self.head = Node(key='head')
        self.tail = Node(key='tail')
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """
            Удаление узла из двусвязного списка
        """
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node: Node) -> None:
        """
            Добавление узла в начало
        """
        next_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = next_node
        next_node.prev = node

    def get(self, key: str) -> any:
        """
            Получение значения из LRUCache
        """
        if key not in self.cache:
            return None
        node = self.cache[key]
        self._remove(node)
        self._add(node)
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
        else:
            if len(self.cache) >= self.max_items:
                node_to_remove = self.tail.prev
                self._remove(node_to_remove)
                del self.cache[node_to_remove.key]

            new_node = Node(key, value)
            self._add(new_node)
            self.cache[key] = new_node

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


if __name__ == "__main__":

    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"

    cache["k1"] = "val1"
    print(cache["k3"])
