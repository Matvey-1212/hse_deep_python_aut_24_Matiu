"""
    В файле реализована тесты для дескрипторов
"""

import unittest
from datetime import datetime
from unittest.mock import patch
from descriptor import VKProfile, Name, Email, BFDate, BaseDescriptor


class TestNameDescriptor(unittest.TestCase):
    """
        Класс проверки дескриптора Name
    """

    def setUp(self):
        """
            Создание тестового класса
        """
        class TestClass:  # pylint: disable=too-few-public-methods
            """
                Тестовый класс
            """
            fisrt_name = Name()
            last_name = Name()

            def __init__(self, value1, value2):
                """
                    Инициализация
                """
                self.fisrt_name = value1
                self.last_name = value2

        self.test_instance = TestClass

    def test_valid_name(self):
        """
            Проверка валидности имени
        """
        name_obj = self.test_instance("Test", "Testov")

        self.assertEqual(name_obj.fisrt_name, "Test")
        self.assertEqual(name_obj.last_name, "Testov")

    def test_name_with_kiril(self):
        """
            Проверка валидности имени на кириллице
        """
        name_obj = self.test_instance("Тест", "Тестов")
        self.assertEqual(name_obj.fisrt_name, "Тест")
        self.assertEqual(name_obj.last_name, "Тестов")

    def test_invalid_name_empty(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance("", "Testov")

    def test_invalid_name_only_spaces(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance("   ", "Testov")
        with self.assertRaises(ValueError):
            self.test_instance("---", "Testov")

    def test_invalid_name_special_characters(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance("Test123!", "Testov")

    def test_invalid_name_type(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance(1, 2)


class TestEmailDescriptor(unittest.TestCase):
    """
        Класс проверки дескриптора Email
    """

    def setUp(self):
        """
            Создание тестового класса
        """
        class TestClass:  # pylint: disable=too-few-public-methods
            """
                Тестовый класс
            """
            email = Email()

            def __init__(self, value1):
                """
                    Инициализация
                """
                self.email = value1

        self.test_instance = TestClass

    def test_valid_email(self):
        """
            Проверка валидности email
        """
        email_obj = self.test_instance("Test@example.ru")
        self.assertEqual(email_obj.email, "Test@example.ru")

        email_obj = self.test_instance("Test@example.ru")
        self.assertEqual(email_obj.email, "Test@example.ru")

    def test_invalid_email_no_domain(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance("Test@.ru")

    def test_invalid_email_wrong_format(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance("Testexample.ru")

    def test_invalid_email_non_ru_domain(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance("Test@example.com")

    def test_invalid_email_empty_string(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance("")

    def test_invalid_email_special_characters(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance("Test@exam!ple.ru")

    def test_invalid_email_type(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance(1)


class TestBFDateDescriptor(unittest.TestCase):
    """
        Класс проверки дескриптора BFDate
    """

    def setUp(self):
        """
            Создание тестового класса
        """
        class TestClass:  # pylint: disable=too-few-public-methods
            """
                Тестовый класс
            """
            bf_date = BFDate()

            def __init__(self, value1):
                """
                    Инициализация
                """
                self.bf_date = value1

        self.test_instance = TestClass

    def test_valid_date(self):
        """
            Проверка валидности email
        """
        bf_obj = self.test_instance((10, 10, 2000))
        self.assertEqual(bf_obj.bf_date, (10, 10, 2000))

        bf_obj = self.test_instance((1, 1, 2000))
        self.assertEqual(bf_obj.bf_date, (1, 1, 2000))

    def test_invalid_date_future(self):
        """
            Проверка вызова ошибок
        """
        future_date = (10, 10, datetime.now().year + 1)
        with self.assertRaises(ValueError):
            self.test_instance(future_date)

    def test_invalid_date_too_old(self):
        """
            Проверка вызова ошибок
        """
        old_date = (10, 10, datetime.now().year - 151)
        with self.assertRaises(ValueError):
            self.test_instance(old_date)

    def test_invalid_date_too_young(self):
        """
            Проверка вызова ошибок
        """
        young_date = (10, 10, datetime.now().year - 13)
        with self.assertRaises(ValueError):
            self.test_instance(young_date)

    def test_invalid_date_tuple_length(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance((10, 10))

    def test_invalid_date_non_tuple(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(TypeError):
            self.test_instance("10-10-2000")

    def test_invalid_date_string_elements(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(TypeError):
            self.test_instance(("10", "10", "2000"))

    def test_invalid_date_day(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance((0, 12, 2000))

        with self.assertRaises(ValueError):
            self.test_instance((-1, 12, 2000))

        with self.assertRaises(ValueError):
            self.test_instance((32, 12, 2000))

    def test_invalid_date_month(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance((10, 0, 2000))

        with self.assertRaises(ValueError):
            self.test_instance((10, -1, 2000))

        with self.assertRaises(ValueError):
            self.test_instance((10, 13, 2000))

    def test_invalid_date_year(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance((10, 10, 0))

        with self.assertRaises(ValueError):
            self.test_instance((10, 10, 24))

        with self.assertRaises(ValueError):
            self.test_instance((10, 10, -1))

    def test_invalid_date(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(ValueError):
            self.test_instance((29, 2, 2001))

        with self.assertRaises(ValueError):
            self.test_instance((31, 4, 2001))


class TestBaseDescriptor(unittest.TestCase):
    """
        Класс проверки дескриптора BaseDescriptor
    """

    def setUp(self):
        """
            Создание тестового класса
        """
        class TestClass1:  # pylint: disable=too-few-public-methods
            """
                Тестовый класс
            """
            attr = BaseDescriptor()

        self.test_instance_empty = TestClass1()

    def test_base_descriptor_get(self):
        """
            Проверка пустого дескриптора
        """
        self.assertIsNone(self.test_instance_empty.attr)

    def test_base_descriptor_set_not_implemented(self):
        """
            Проверка вызова ошибок
        """
        with self.assertRaises(NotImplementedError):
            self.test_instance_empty.attr = 10


class TestVKProfile(unittest.TestCase):
    """
        Класс проверки класса VKProfile
    """

    def test_profile_creation_valid(self):
        """
            Проверка создания класса
        """
        vk = VKProfile("Test", "Testov", "Test@example.ru", (10, 10, 2000))
        self.assertEqual(vk.fisrt_name, "Test")
        self.assertEqual(vk.last_name, "Testov")
        self.assertEqual(vk.email, "Test@example.ru")
        self.assertEqual(vk.bfdate, (10, 10, 2000))

    def test_profile_update(self):
        """
            Создание изменения значений дескрипторов
        """
        vk = VKProfile("Test", "Testov", "Test@example.ru", (10, 10, 2000))
        vk.fisrt_name = "Test-new"
        vk.last_name = "Testov-new"
        vk.email = "Test_new@example.ru"
        vk.bfdate = (1, 1, 1990)
        self.assertEqual(vk.fisrt_name, "Test-new")
        self.assertEqual(vk.last_name, "Testov-new")
        self.assertEqual(vk.email, "Test_new@example.ru")
        self.assertEqual(vk.bfdate, (1, 1, 1990))

    def test_profile_double(self):
        """
            Проверка независимости дескрипторов
        """
        vk1 = VKProfile("Test", "Testov", "Test@example.ru", (10, 10, 2000))
        vk2 = VKProfile("Test-new", "Testov-new",
                        "Test_new@example.ru", (1, 1, 1990))

        self.assertEqual(vk1.fisrt_name, "Test")
        self.assertEqual(vk1.last_name, "Testov")
        self.assertEqual(vk1.email, "Test@example.ru")
        self.assertEqual(vk1.bfdate, (10, 10, 2000))

        self.assertEqual(vk2.fisrt_name, "Test-new")
        self.assertEqual(vk2.last_name, "Testov-new")
        self.assertEqual(vk2.email, "Test_new@example.ru")
        self.assertEqual(vk2.bfdate, (1, 1, 1990))

    def test_profile_invalid_update(self):
        """
            Проверка вызова ошибок
        """
        vk = VKProfile("Test", "Testov", "Test@example.ru", (10, 10, 2000))
        with self.assertRaises(ValueError):
            vk.fisrt_name = "1234"
        with self.assertRaises(ValueError):
            vk.email = "wrong-email-format"
        with self.assertRaises(ValueError):
            vk.bfdate = (32, 13, 2100)

    def test_print(self):
        """
            Проверка вывода
        """
        name1 = "Test"
        name2 = "Testov"
        email = "Test@example.ru"
        bf_date = (10, 10, 2000)

        test_str = (f"fisrt_name: {name1}; " +
                    f"last_name: {name2}; " +
                    f"email: {email}; " +
                    f"bfdate: {bf_date};"
                    )

        vk = VKProfile(name1, name2, email, bf_date)

        with patch('builtins.print') as mocked_print:
            vk.print()
            mocked_print.assert_called_with(test_str)


if __name__ == '__main__':
    unittest.main()
