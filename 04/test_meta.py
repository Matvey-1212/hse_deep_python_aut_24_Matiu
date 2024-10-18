"""
     В файле реализовно тестирование метакласса
"""

import unittest
from meta_class import CustomMeta


class TestCustomMeta(unittest.TestCase):
    """
        Класс тестирования класса CustomMeta
    """

    def setUp(self):
        """
        Инициализация экземпляра.
        """

        class TestClass(metaclass=CustomMeta):
            """
                Тестовый класс
            """
            x = 50
            custom_x2 = 52

            def __init__(self, val=99):
                """
                    Инициализация
                """
                self.val = val
                self.custom_val2 = val+2

            def line(self):
                """
                    Тестовый метод
                """
                return 100

            def custom_line2(self):
                """
                    Тестовый метод
                """
                return 102

            def __str__(self):
                """
                    Тестовый метод
                """
                return "Custom_by_metaclass"

        self.instance = TestClass

    def test_class_attributes(self):
        """
        Тестирование атрибутов класса
        """
        self.assertEqual(self.instance.custom_x, 50)  # pylint: disable=E1101
        with self.assertRaises(AttributeError):
            _ = self.instance.x

    def test_instance_attributes(self):
        """
        Тестирование атрибутов экземпляра
        """
        test_c = self.instance()
        self.assertEqual(test_c.custom_val, 99)  # pylint: disable=E1101

        with self.assertRaises(AttributeError):
            _ = test_c.val

    def test_instance_method(self):
        """
        Тестирование метода экземпляра
        """
        test_c = self.instance()
        self.assertEqual(test_c.custom_line(), 100)  # pylint: disable=E1101

        with self.assertRaises(AttributeError):
            test_c.line()

    def test_str_method(self):
        """
        Тестирование метода __str__.
        """
        test_c = self.instance()
        self.assertEqual(str(test_c), "Custom_by_metaclass")

    def test_dynamic_attributes(self):
        """
        Тестирование динамически добавленных атрибутов экземпляра.
        """
        test_c = self.instance()
        test_c.dynamic = "added later"  # pylint: disable=W0201
        self.assertEqual(
            test_c.custom_dynamic,  # pylint: disable=E1101
            "added later"
            )

        with self.assertRaises(AttributeError):
            _ = test_c.dynamic

    def test_custom_meta_behavior(self):
        """
        Дополнительная проверка наличия
        атрибутов в __dict__ экземпляра и класса.
        """

        test_c = self.instance()

        test_c.dynamic = "added later"  # pylint: disable=W0201

        self.assertNotIn('val', test_c.__dict__)
        self.assertNotIn('dynamic', test_c.__dict__)
        self.assertIn('__str__', self.instance.__dict__)

        self.assertIn('custom_val', test_c.__dict__)
        self.assertIn('custom_dynamic', test_c.__dict__)
        self.assertNotIn('custom___str__', self.instance.__dict__)
        self.assertNotIn('custom__str__', self.instance.__dict__)

        self.assertIn('custom_x', self.instance.__dict__)
        self.assertNotIn('x', self.instance.__dict__)

    def test_absent_attributes(self):
        """
        Проверка отсутствия несуществующих атрибутов.
        """
        test_c = self.instance()
        with self.assertRaises(AttributeError):
            _ = test_c.custom_yyy  # pylint: disable=E1101
        with self.assertRaises(AttributeError):
            _ = test_c.yyy  # pylint: disable=E1101

    def test_doubled_prefics(self):
        """
        Проверка дублирования "custom_"
        """

        test_c = self.instance()

        test_c.custom_dynamic2 = "added later"  # pylint: disable=W0201

        self.assertNotIn('custom_custom_val2', test_c.__dict__)
        self.assertNotIn('custom_custom_dynamic2', test_c.__dict__)
        self.assertNotIn('custom_custom_x2', self.instance.__dict__)

        self.assertIn('custom_val2', test_c.__dict__)
        self.assertIn('custom_dynamic2', test_c.__dict__)
        self.assertIn('custom_x2', self.instance.__dict__)


if __name__ == "__main__":
    unittest.main()
