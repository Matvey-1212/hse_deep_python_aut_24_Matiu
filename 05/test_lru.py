"""
    В файле реализовано тестирование класса LRUCache
"""

import time
import unittest
from lru import LRUCache


class TestLRUCache(unittest.TestCase):
    """
        Класс тестирования LRUCache
    """

    def setUp(self):
        """
            Инициализация кэша перед каждым тестом
        """
        self.cache = LRUCache(2)

    def test_set_and_get(self):
        """
            Тест установки и получения значений
        """
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")

        self.assertEqual(self.cache.get("k1"), "val1")
        self.assertEqual(self.cache.get("k2"), "val2")

    def test_getitem_and_setitem(self):
        """
            Тест установки и получения значений через []
        """
        self.cache["k1"] = "val1"
        self.cache["k2"] = "val2"

        self.assertEqual(self.cache["k1"], "val1")
        self.assertEqual(self.cache["k2"], "val2")

    def test_cache_eviction_via_getitem_and_setite(self):
        """
            Тест на удаление старого элемента через getitem и setite
        """
        self.cache["k1"] = "val1"
        self.cache["k2"] = "val2"
        self.cache["k3"] = "val3"

        self.assertIsNone(self.cache["k1"])
        self.assertEqual(self.cache["k2"], "val2")
        self.assertEqual(self.cache["k3"], "val3")

    def test_cache_eviction_via_get_and_set(self):
        """
            Тест на удаление старого элемента через get и set
        """
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.cache.set("k3", "val3")

        self.assertIsNone(self.cache.get("k1"))
        self.assertEqual(self.cache.get("k2"), "val2")
        self.assertEqual(self.cache.get("k3"), "val3")

    def test_update_value_via_getitem_and_setite(self):
        """
            Тест обновления значения в элементе через getitem и setite
        """
        self.cache["k1"] = "val1"
        self.cache["k2"] = "val2"

        self.cache["k1"] = "new_val1"
        self.assertEqual(self.cache["k1"], "new_val1")

    def test_update_value_via_get_and_set(self):
        """
            Тест обновления значения в элементе через get и set
        """
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")

        self.cache.set("k1", "new_val1")
        self.assertEqual(self.cache.get("k1"), "new_val1")

    def test_access_updates_priority_via_getitem_and_setite(self):
        """
            Тест на обновление порядка доступа через getitem и setite
        """
        self.cache["k1"] = "val1"
        self.cache["k2"] = "val2"
        self.cache["k1"] = "val1"
        self.cache["k3"] = "val3"

        self.assertEqual(self.cache["k1"], "val1")
        self.assertIsNone(self.cache["k2"])
        self.assertEqual(self.cache["k3"], "val3")

    def test_access_updates_priority_via_get_and_set(self):
        """
            Тест на обновление порядка доступа через get и set
        """
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.cache.set("k1", "val1")
        self.cache.set("k3", "val3")

        self.assertEqual(self.cache.get("k1"), "val1")
        self.assertIsNone(self.cache.get("k2"))
        self.assertEqual(self.cache.get("k3"), "val3")

    def test_cache_capacity_via_getitem_and_setite(self):
        """
            Тест вместимости через getitem и setite
        """
        cache = LRUCache(2)
        cache["k1"] = "val1"
        cache["k2"] = "val2"
        self.assertIsNone(cache["k3"])
        self.assertEqual(cache["k2"], "val2")
        self.assertEqual(cache["k1"], "val1")

        cache["k3"] = "val3"
        self.assertEqual(cache["k3"], "val3")
        self.assertIsNone(cache["k2"])
        self.assertEqual(cache["k1"], "val1")

    def test_cache_capacity_via_get_and_set(self):
        """
            Тест вместимости через get и set
        """
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        self.assertIsNone(cache.get("k3"))
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k1"), "val1")

    def test_invalid_input(self):
        """
            Тест корректности входных данных
        """
        with self.assertRaises(ValueError):
            _ = LRUCache(0)

        with self.assertRaises(TypeError):
            _ = LRUCache('2')

    def time_operation(self, operation, *args, **kwargs):
        """
            Функция для измерения времени выполнения операции
        """
        start_time = time.perf_counter()
        operation(*args, **kwargs)
        end_time = time.perf_counter()
        return end_time - start_time

    def test_get_performance(self):
        """
            Тест на O(1)
        """
        cache_small = LRUCache(1000)
        cache_medium = LRUCache(10000)
        cache_large = LRUCache(100000)

        for i in range(1000):
            cache_small.set(f"k{i}", f"val{i}")

        for i in range(10000):
            cache_small.set(f"k{i}", f"val{i}")

        for i in range(100000):
            cache_large.set(f"k{i}", f"val{i}")

        get_time_small = self.time_operation(cache_small.get, "k1")
        get_time_medium = self.time_operation(cache_medium.get, "k1")
        get_time_large = self.time_operation(cache_large.get, "k1")

        self.assertAlmostEqual(get_time_small, get_time_large, delta=0.0001)
        self.assertAlmostEqual(get_time_small, get_time_medium, delta=0.0001)
        self.assertAlmostEqual(get_time_medium, get_time_large, delta=0.0001)


if __name__ == "__main__":
    unittest.main()
