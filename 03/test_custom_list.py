"""
    В файле реализованы тесты для CustomList
"""

import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    """
        Тесты для класса CustomList
    """

    def test_add_custom_lists(self):
        """
            Тест сложения двух CustomList
        """
        cl1 = CustomList([5, 1, 3, 7])
        cl2 = CustomList([1, 2, 7])
        result = cl1 + cl2
        self.assertEqual(list(result), [6, 3, 10, 7])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl1), list(CustomList([5, 1, 3, 7])))
        self.assertEqual(list(cl2), list(CustomList([1, 2, 7])))
        result = cl2 + cl1
        self.assertEqual(list(result), [6, 3, 10, 7])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl1), list(CustomList([5, 1, 3, 7])))
        self.assertEqual(list(cl2), list(CustomList([1, 2, 7])))

        cl1 = CustomList([5, 1, 3, 7])
        cl2 = CustomList([1, 2, 7, 1])
        result = cl1 + cl2
        self.assertEqual(list(result), [6, 3, 10, 8])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl1), list(CustomList([5, 1, 3, 7])))
        self.assertEqual(list(cl2), list(CustomList([1, 2, 7, 1])))
        result = cl2 + cl1
        self.assertEqual(list(result), [6, 3, 10, 8])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl1), list(CustomList([5, 1, 3, 7])))
        self.assertEqual(list(cl2), list(CustomList([1, 2, 7, 1])))

        cl1 = CustomList([5, 1, 3, 7])
        cl2 = CustomList([])
        result = cl1 + cl2
        self.assertEqual(list(result), [5, 1, 3, 7])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl1), list(CustomList([5, 1, 3, 7])))
        self.assertEqual(list(cl2), list(CustomList([])))
        result = cl2 + cl1
        self.assertEqual(list(result), [5, 1, 3, 7])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl1), list(CustomList([5, 1, 3, 7])))
        self.assertEqual(list(cl2), list(CustomList([])))

        cl1 = CustomList([])
        cl2 = CustomList([])
        result = cl1 + cl2
        self.assertEqual(list(result), [])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl1), list(CustomList([])))
        self.assertEqual(list(cl2), list(CustomList([])))
        result = cl2 + cl1
        self.assertEqual(list(result), [])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl1), list(CustomList([])))
        self.assertEqual(list(cl2), list(CustomList([])))

    def test_add_custom_list_with_list(self):
        """
            Тест сложения CustomList с List
        """
        cl = CustomList([10, 11])
        lst = [2, 5]
        result = cl + lst
        self.assertEqual(list(result), [12, 16])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([10, 11])))

        cl = CustomList([])
        lst = [2, 5]
        result = cl + lst
        self.assertEqual(list(result), [2, 5])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

        cl = CustomList([10, 11])
        lst = []
        result = cl + lst
        self.assertEqual(list(result), [10, 11])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([10, 11])))

        cl = CustomList([])
        lst = []
        result = cl + lst
        self.assertEqual(list(result), [])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

        cl = CustomList([1, 2, 3, 4, 5])
        lst = [1]
        result = cl + lst
        self.assertEqual(list(result), [2, 2, 3, 4, 5])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([1, 2, 3, 4, 5])))

    def test_add_list_with_custom_list(self):
        """
            Тест сложения List с CustomList
        """
        cl = CustomList([10, 11])
        lst = [2, 5]
        result = lst + cl
        self.assertEqual(list(result), [12, 16])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([10, 11])))

        cl = CustomList([])
        lst = [2, 5, 6, 7, 8]
        result = lst + cl
        self.assertEqual(list(result), [2, 5, 6, 7, 8])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

        cl = CustomList([10, 11])
        lst = []
        result = lst + cl
        self.assertEqual(list(result), [10, 11])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([10, 11])))

        cl = CustomList([])
        lst = []
        result = lst + cl
        self.assertEqual(list(result), [])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

        cl = CustomList([1, 2, 3, 4, 5])
        lst = [1]
        result = lst + cl
        self.assertEqual(list(result), [2, 2, 3, 4, 5])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([1, 2, 3, 4, 5])))

    def test_add_custom_list_with_int(self):
        """
            Тест сложения CustomList с int
        """
        cl = CustomList([2, 5])
        result = cl + 10
        self.assertEqual(list(result), [12, 15])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([2, 5])))

        cl = CustomList([])
        result = cl + 10
        self.assertEqual(list(result), [10])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

        cl = CustomList([2, 5, 6])
        result = cl + 0
        self.assertEqual(list(result), [2, 5, 6])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([2, 5, 6])))

    def test_add_int_with_custom_list(self):
        """
            Тест сложения int с CustomList
        """
        cl = CustomList([2, 5])
        result = 10 + cl
        self.assertEqual(list(result), [12, 15])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([2, 5])))

        cl = CustomList([])
        result = 10 + cl
        self.assertEqual(list(result), [10])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

        cl = CustomList([2, 5, 6])
        result = 0 + cl
        self.assertEqual(list(result), [2, 5, 6])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([2, 5, 6])))

    def test_sub_custom_lists(self):
        """
            Тест вычитания CustomList из CustomList
        """
        cl1 = CustomList([5, 1, 3, 7])
        cl2 = CustomList([1, 2, 7])
        result = cl1 - cl2
        self.assertEqual(list(result), [4, -1, -4, 7])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl1), list(CustomList([5, 1, 3, 7])))
        self.assertEqual(list(cl2), list(CustomList([1, 2, 7])))

        cl1 = CustomList([5, 1, 3])
        cl2 = CustomList([1, 2, 7, 2])
        result = cl1 - cl2
        self.assertEqual(list(result), [4, -1, -4, -2])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl1), list(CustomList([5, 1, 3])))
        self.assertEqual(list(cl2), list(CustomList([1, 2, 7, 2])))

        cl1 = CustomList([])
        cl2 = CustomList([1, 2, 7, 2])
        result = cl1 - cl2
        self.assertEqual(list(result), [-1, -2, -7, -2])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl1), list(CustomList([])))
        self.assertEqual(list(cl2), list(CustomList([1, 2, 7, 2])))

        cl1 = CustomList([5, 1, 3, 7])
        cl2 = CustomList([])
        result = cl1 - cl2
        self.assertEqual(list(result), [5, 1, 3, 7])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl1), list(CustomList([5, 1, 3, 7])))
        self.assertEqual(list(cl2), list(CustomList([])))

        cl1 = CustomList([])
        cl2 = CustomList([])
        result = cl1 - cl2
        self.assertEqual(list(result), [])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl1), list(CustomList([])))
        self.assertEqual(list(cl2), list(CustomList([])))

    def test_sub_custom_list_with_list(self):
        """
            Тест вычитания List из CustomList
        """
        cl = CustomList([10, 10, 10])
        lst = [2, 5]
        result = cl - lst
        self.assertEqual(list(result), [8, 5, 10])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([10, 10, 10])))

        cl = CustomList([10])
        lst = [2, 5, 10]
        result = cl - lst
        self.assertEqual(list(result), [8, -5, -10])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([10])))

        cl = CustomList([])
        lst = [2, 5, 10]
        result = cl - lst
        self.assertEqual(list(result), [-2, -5, -10])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

        cl = CustomList([10, 10, 10])
        lst = []
        result = cl - lst
        self.assertEqual(list(result), [10, 10, 10])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([10, 10, 10])))

        cl = CustomList([])
        lst = []
        result = cl - lst
        self.assertEqual(list(result), [])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

    def test_sub_list_with_custom_list(self):
        """
            Тест вычитания CustomList из List
        """
        cl = CustomList([10, 10, 10])
        lst = [2, 5]
        result = lst - cl
        self.assertEqual(list(result), [-8, -5, -10])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([10, 10, 10])))

        cl = CustomList([10])
        lst = [2, 5, 10]
        result = lst - cl
        self.assertEqual(list(result), [-8, 5, 10])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([10])))

        cl = CustomList([])
        lst = [2, 5, 10]
        result = lst - cl
        self.assertEqual(list(result), [2, 5, 10])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

        cl = CustomList([10, 10, 10])
        lst = []
        result = lst - cl
        self.assertEqual(list(result), [-10, -10, -10])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([10, 10, 10])))

        cl = CustomList([])
        lst = []
        result = lst - cl
        self.assertEqual(list(result), [])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

    def test_sub_custom_list_with_int(self):
        """
            Тест вычитания int из CustomList
        """
        cl = CustomList([2, 5])
        result = cl - 10
        self.assertEqual(list(result), [-8, -5])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([2, 5])))

        cl = CustomList([2])
        result = cl - 10
        self.assertEqual(list(result), [-8])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([2])))

        cl = CustomList([])
        result = cl - 10
        self.assertEqual(list(result), [-10])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

        cl = CustomList([2, 5])
        result = cl - 0
        self.assertEqual(list(result), [2, 5])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([2, 5])))

        cl = CustomList([2])
        result = cl - 0
        self.assertEqual(list(result), [2])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([2])))

        cl = CustomList([])
        result = cl - 0
        self.assertEqual(list(result), [0])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

    def test_sub_int_with_custom_list(self):
        """
            Тест вычитания CustomList из int
        """
        cl = CustomList([2, 5])
        result = 10 - cl
        self.assertEqual(list(result), [8, 5])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([2, 5])))

        cl = CustomList([2])
        result = 10 - cl
        self.assertEqual(list(result), [8])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([2])))

        cl = CustomList([])
        result = 10 - cl
        self.assertEqual(list(result), [10])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

        cl = CustomList([2, 5])
        result = 0 - cl
        self.assertEqual(list(result), [-2, -5])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([2, 5])))

        cl = CustomList([2])
        result = 0 - cl
        self.assertEqual(list(result), [-2])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([2])))

        cl = CustomList([])
        result = 0 - cl
        self.assertEqual(list(result), [0])
        self.assertIsInstance(result, CustomList)
        self.assertEqual(list(cl), list(CustomList([])))

    def test_eq_custom_lists(self):
        """
            Тест равенства двух CustomList по сумме элементов
        """
        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([3, 3])
        self.assertTrue(cl1 == cl2)

        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([6])
        self.assertTrue(cl1 == cl2)

        cl1 = CustomList([1] * 100)
        cl2 = CustomList([100])
        self.assertTrue(cl1 == cl2)

        cl1 = CustomList([])
        cl2 = CustomList([0])
        self.assertTrue(cl1 == cl2)

        cl1 = CustomList([])
        cl2 = CustomList([])
        self.assertTrue(cl1 == cl2)

        cl1 = CustomList([5, -5])
        cl2 = CustomList([0])
        self.assertTrue(cl1 == cl2)

        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([3, 3])
        self.assertTrue(cl2 == cl1)

        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([6])
        self.assertTrue(cl2 == cl1)

        cl1 = CustomList([1] * 100)
        cl2 = CustomList([100])
        self.assertTrue(cl2 == cl1)

        cl1 = CustomList([])
        cl2 = CustomList([0])
        self.assertTrue(cl2 == cl1)

        cl1 = CustomList([])
        cl2 = CustomList([])
        self.assertTrue(cl2 == cl1)

        cl1 = CustomList([5, -5])
        cl2 = CustomList([0])
        self.assertTrue(cl2 == cl1)

    def test_ne_custom_lists(self):
        """
            Тест неравенства двух CustomList по сумме элементов
        """
        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([3, 4])
        self.assertTrue(cl1 != cl2)

        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([7])
        self.assertTrue(cl1 != cl2)

        cl1 = CustomList([1] * 100)
        cl2 = CustomList([-100])
        self.assertTrue(cl1 != cl2)

        cl1 = CustomList([1])
        cl2 = CustomList([])
        self.assertTrue(cl1 != cl2)

        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([3, 4])
        self.assertTrue(cl2 != cl1)

        cl1 = CustomList([1, 2, 3])
        cl2 = CustomList([7])
        self.assertTrue(cl2 != cl1)

        cl1 = CustomList([1] * 100)
        cl2 = CustomList([-100])
        self.assertTrue(cl2 != cl1)

        cl1 = CustomList([1])
        cl2 = CustomList([])
        self.assertTrue(cl2 != cl1)

    def test_lt_custom_lists(self):
        """
            Тест < по сумме элементов двух CustomList
        """
        cl1 = CustomList([1, 2])
        cl2 = CustomList([4])
        self.assertTrue(cl1 < cl2)

        cl1 = CustomList([])
        cl2 = CustomList([4])
        self.assertTrue(cl1 < cl2)

        cl1 = CustomList([0])
        cl2 = CustomList([4])
        self.assertTrue(cl1 < cl2)

        cl1 = CustomList([-100])
        cl2 = CustomList([])
        self.assertTrue(cl1 < cl2)

    def test_le_custom_lists(self):
        """
            Тест <= по сумме элементов двух CustomList
        """
        cl1 = CustomList([1, 2])
        cl2 = CustomList([3])
        self.assertTrue(cl1 <= cl2)

        cl1 = CustomList([])
        cl2 = CustomList([0])
        self.assertTrue(cl1 <= cl2)

        cl1 = CustomList([1, 2])
        cl2 = CustomList([4])
        self.assertTrue(cl1 <= cl2)

        cl1 = CustomList([])
        cl2 = CustomList([4])
        self.assertTrue(cl1 <= cl2)

        cl1 = CustomList([0])
        cl2 = CustomList([4])
        self.assertTrue(cl1 <= cl2)

        cl1 = CustomList([-100])
        cl2 = CustomList([])
        self.assertTrue(cl1 <= cl2)

    def test_gt_custom_lists(self):
        """
            Тест > по сумме элементов двух CustomList
        """
        cl2 = CustomList([1, 2])
        cl1 = CustomList([4])
        self.assertTrue(cl1 > cl2)

        cl2 = CustomList([])
        cl1 = CustomList([4])
        self.assertTrue(cl1 > cl2)

        cl2 = CustomList([0])
        cl1 = CustomList([4])
        self.assertTrue(cl1 > cl2)

        cl2 = CustomList([-100])
        cl1 = CustomList([])
        self.assertTrue(cl1 > cl2)

    def test_ge_custom_lists(self):
        """
            Тест >= по сумме элементов двух CustomList
        """
        cl2 = CustomList([1, 2])
        cl1 = CustomList([3])
        self.assertTrue(cl1 >= cl2)

        cl2 = CustomList([])
        cl1 = CustomList([0])
        self.assertTrue(cl1 >= cl2)

        cl2 = CustomList([1, 2])
        cl1 = CustomList([4])
        self.assertTrue(cl1 >= cl2)

        cl2 = CustomList([])
        cl1 = CustomList([4])
        self.assertTrue(cl1 >= cl2)

        cl2 = CustomList([0])
        cl1 = CustomList([4])
        self.assertTrue(cl1 >= cl2)

        cl2 = CustomList([-100])
        cl1 = CustomList([])
        self.assertTrue(cl1 >= cl2)

    def test_str_custom_list(self):
        """
            Тест строкового представления CustomList
        """
        cl = CustomList([1, 2, 3])
        self.assertEqual(str(cl), "[1, 2, 3], сумма: 6")

        cl = CustomList([1, -1])
        self.assertEqual(str(cl), "[1, -1], сумма: 0")

        cl = CustomList([0, 0, 0])
        self.assertEqual(str(cl), "[0, 0, 0], сумма: 0")

        cl = CustomList([])
        self.assertEqual(str(cl), "[], сумма: 0")

    def test_invalid_type_int(self):
        """
        Проверяет, что функция выбрасывает TypeError для
            некорректных типов входных данных
        """

        with self.assertRaises(TypeError):
            _ = CustomList([0]) + 1.2
        with self.assertRaises(TypeError):
            _ = 1.2 + CustomList([0])
        with self.assertRaises(TypeError):
            _ = CustomList([0]) - 1.2
        with self.assertRaises(TypeError):
            _ = 1.2 - CustomList([0])
        with self.assertRaises(TypeError):
            _ = CustomList([0]) == 0
        with self.assertRaises(TypeError):
            _ = 0 == CustomList([0])
        with self.assertRaises(TypeError):
            _ = CustomList([0]) < 1
        with self.assertRaises(TypeError):
            _ = 0 < CustomList([1])
        with self.assertRaises(TypeError):
            _ = CustomList([1]) > 0
        with self.assertRaises(TypeError):
            _ = 1 > CustomList([0])
        with self.assertRaises(TypeError):
            _ = CustomList([1]) > 0
        with self.assertRaises(TypeError):
            _ = 1 > CustomList([0])
        with self.assertRaises(TypeError):
            _ = CustomList([0]) <= 1
        with self.assertRaises(TypeError):
            _ = 0 <= CustomList([1])
        with self.assertRaises(TypeError):
            _ = CustomList([1]) >= 0
        with self.assertRaises(TypeError):
            _ = 1 >= CustomList([0])
        with self.assertRaises(TypeError):
            _ = CustomList([1]) >= 0
        with self.assertRaises(TypeError):
            _ = 1 >= CustomList([0])

    def test_invalid_type_list(self):
        """
        Проверяет, что функция выбрасывает TypeError для
            некорректных типов входных данных
        """
        with self.assertRaises(TypeError):
            _ = CustomList([0]) == [0]
        with self.assertRaises(TypeError):
            _ = [0] == CustomList([0])
        with self.assertRaises(TypeError):
            _ = CustomList([0]) < [1]
        with self.assertRaises(TypeError):
            _ = [0] < CustomList([1])
        with self.assertRaises(TypeError):
            _ = CustomList([1]) > [0]
        with self.assertRaises(TypeError):
            _ = [1] > CustomList([0])
        with self.assertRaises(TypeError):
            _ = CustomList([1]) > [0]
        with self.assertRaises(TypeError):
            _ = [1] > CustomList([0])
        with self.assertRaises(TypeError):
            _ = CustomList([0]) <= [1]
        with self.assertRaises(TypeError):
            _ = [0] <= CustomList([1])
        with self.assertRaises(TypeError):
            _ = CustomList([1]) >= [0]
        with self.assertRaises(TypeError):
            _ = [1] >= CustomList([0])
        with self.assertRaises(TypeError):
            _ = CustomList([1]) >= [0]
        with self.assertRaises(TypeError):
            _ = [1] >= CustomList([0])


if __name__ == '__main__':
    unittest.main()
