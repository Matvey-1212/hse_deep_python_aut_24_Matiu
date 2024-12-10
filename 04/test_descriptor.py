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
            Проверка валидности имени дескриптора Name
        """
        name_obj = self.test_instance("Test", "Testov")

        self.assertEqual(name_obj.fisrt_name, "Test")
        self.assertEqual(name_obj.last_name, "Testov")

    def test_valid_name_update_valid_name(self):
        """
            Проверка замены значения на валидное в Name
        """
        initial_first_name = "Test"
        new_valid_first_name = "newTest"
        test_obj = self.test_instance(initial_first_name, "InitialLastName")
        self.assertEqual(test_obj.fisrt_name, initial_first_name)

        test_obj.fisrt_name = new_valid_first_name
        self.assertEqual(test_obj.fisrt_name, new_valid_first_name)

    def test_valid_name_update_inalid_name(self):
        """
            Проверка замены значения на невалидное в Name
        """
        initial_first_name = "Test"
        test_obj = self.test_instance(initial_first_name, "ValidLastName")
        self.assertEqual(test_obj.fisrt_name, initial_first_name)

        with self.assertRaises(ValueError):
            test_obj.fisrt_name = "Invalid123!"

        self.assertEqual(test_obj.fisrt_name, initial_first_name)

    def test_name_with_kiril(self):
        """
            Проверка валидности имени на кириллице дескриптора Name
        """
        name_obj = self.test_instance("Тест", "Тестов")
        self.assertEqual(name_obj.fisrt_name, "Тест")
        self.assertEqual(name_obj.last_name, "Тестов")

    def test_invalid_name_empty(self):
        """
            Проверка вызова ошибок дескриптора Name
        """
        with self.assertRaises(ValueError):
            self.test_instance("", "Testov")

    def test_invalid_name_only_spaces(self):
        """
            Проверка вызова ошибок дескриптора Name
        """
        with self.assertRaises(ValueError):
            self.test_instance("   ", "Testov")
        with self.assertRaises(ValueError):
            self.test_instance("---", "Testov")

    def test_invalid_name_special_characters(self):
        """
            Проверка вызова ошибок дескриптора Name
        """
        with self.assertRaises(ValueError):
            self.test_instance("Test123!", "Testov")

    def test_invalid_name_type(self):
        """
            Проверка вызова ошибок дескриптора Name
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
            Проверка валидности email дескриптора Email
        """
        email_obj = self.test_instance("Test@example.ru")
        self.assertEqual(email_obj.email, "Test@example.ru")

        email_obj = self.test_instance("Test@example.ru")
        self.assertEqual(email_obj.email, "Test@example.ru")

    def test_valid_name_update_valid_name(self):
        """
            Проверка замены значения на валидное в Email
        """
        initial_email = "Test@example.ru"
        new_valid_email = "newTest@example.ru"
        test_obj = self.test_instance(initial_email)
        self.assertEqual(test_obj.email, initial_email)

        test_obj.email = new_valid_email
        self.assertEqual(test_obj.email, new_valid_email)

    def test_valid_name_update_inalid_name(self):
        """
            Проверка замены значения на невалидное в Email
        """
        initial_email = "Test@example.ru"
        test_obj = self.test_instance(initial_email)
        self.assertEqual(test_obj.email, initial_email)

        with self.assertRaises(ValueError):
            test_obj.email = "Test@.ru"

        self.assertEqual(test_obj.email, initial_email)

    def test_invalid_email_no_domain(self):
        """
            Проверка вызова ошибок дескриптора Email
        """
        with self.assertRaises(ValueError):
            self.test_instance("Test@.ru")

    def test_invalid_email_wrong_format(self):
        """
            Проверка вызова ошибок дескриптора Email
        """
        with self.assertRaises(ValueError):
            self.test_instance("Testexample.ru")

    def test_invalid_email_non_ru_domain(self):
        """
            Проверка вызова ошибок дескриптора Email
        """
        with self.assertRaises(ValueError):
            self.test_instance("Test@example.com")

    def test_invalid_email_empty_string(self):
        """
            Проверка вызова ошибок дескриптора Email
        """
        with self.assertRaises(ValueError):
            self.test_instance("")

    def test_invalid_email_special_characters(self):
        """
            Проверка вызова ошибок дескриптора Email
        """
        with self.assertRaises(ValueError):
            self.test_instance("Test@exam!ple.ru")

    def test_invalid_email_type(self):
        """
            Проверка вызова ошибок дескриптора Email
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
            Проверка валидности поля дескриптора BFDate
        """
        bf_obj = self.test_instance((10, 10, 2000))
        self.assertEqual(bf_obj.bf_date, (10, 10, 2000))

        bf_obj = self.test_instance((1, 1, 2000))
        self.assertEqual(bf_obj.bf_date, (1, 1, 2000))

    def test_valid_name_update_valid_name(self):
        """
            Проверка замены значения на валидное в BFDate
        """
        initial_bf_date = (10, 10, 2000)
        new_valid_bf_date = (10, 10, 2010)
        test_obj = self.test_instance(initial_bf_date)
        self.assertEqual(test_obj.bf_date, initial_bf_date)

        test_obj.bf_date = new_valid_bf_date
        self.assertEqual(test_obj.bf_date, new_valid_bf_date)

    def test_valid_name_update_inalid_name(self):
        """
            Проверка замены значения на невалидное в BFDate
        """
        initial_bf_date = (10, 10, 2000)
        test_obj = self.test_instance(initial_bf_date)
        self.assertEqual(test_obj.bf_date, initial_bf_date)

        with self.assertRaises(ValueError):
            test_obj.bf_date = (10, 10, datetime.now().year + 1)

        self.assertEqual(test_obj.bf_date, initial_bf_date)

    def test_invalid_date_future(self):
        """
            Проверка вызова ошибок дескриптора BFDate,
            ненаступившая дата
        """
        future_date = (10, 10, datetime.now().year + 1)
        with self.assertRaises(ValueError):
            self.test_instance(future_date)

    def test_invalid_date_too_old(self):
        """
            Проверка вызова ошибок дескриптора BFDate,
            некорректный возраст (старый)
        """
        old_date = (10, 10, datetime.now().year - 151)
        with self.assertRaises(ValueError):
            self.test_instance(old_date)

    def test_invalid_date_too_young(self):
        """
            Проверка вызова ошибок дескриптора BFDate,
            некорректный возраст (молодой)
        """
        young_date = (10, 10, datetime.now().year - 13)
        with self.assertRaises(ValueError):
            self.test_instance(young_date)

    def test_invalid_date_tuple_length(self):
        """
            Проверка вызова ошибок дескриптора BFDate,
            некорректное колво значений
        """
        with self.assertRaises(ValueError):
            self.test_instance((10, 10))

    def test_invalid_date_non_tuple(self):
        """
            Проверка вызова ошибок дескриптора BFDate,
            некорректный тип данных tuple
        """
        with self.assertRaises(TypeError):
            self.test_instance("10-10-2000")

    def test_invalid_date_string_elements(self):
        """
            Проверка вызова ошибок дескриптора BFDate,
            некорректный тип данных str
        """
        with self.assertRaises(TypeError):
            self.test_instance(("10", "10", "2000"))

    def test_invalid_date_day(self):
        """
            Проверка вызова ошибок дескриптора BFDate, некоректный день
        """
        with self.assertRaises(ValueError):
            self.test_instance((0, 12, 2000))

        with self.assertRaises(ValueError):
            self.test_instance((-1, 12, 2000))

        with self.assertRaises(ValueError):
            self.test_instance((32, 12, 2000))

    def test_invalid_date_month(self):
        """
            Проверка вызова ошибок дескриптора BFDate, некорректный месяц
        """
        with self.assertRaises(ValueError):
            self.test_instance((10, 0, 2000))

        with self.assertRaises(ValueError):
            self.test_instance((10, -1, 2000))

        with self.assertRaises(ValueError):
            self.test_instance((10, 13, 2000))

    def test_invalid_date_year(self):
        """
            Проверка вызова ошибок дескриптора BFDateб некорректный год
        """
        with self.assertRaises(ValueError):
            self.test_instance((10, 10, 0))

        with self.assertRaises(ValueError):
            self.test_instance((10, 10, 24))

        with self.assertRaises(ValueError):
            self.test_instance((10, 10, -1))

    def test_invalid_date(self):
        """
            Проверка вызова ошибок дескриптора BFDate, некорректная дата
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
            Проверка пустого дескриптора BaseDescriptor
        """
        self.assertIsNone(self.test_instance_empty.attr)

    def test_base_descriptor_set_not_implemented(self):
        """
            Проверка вызова ошибок в BaseDescriptor
        """
        with self.assertRaises(NotImplementedError):
            self.test_instance_empty.attr = 10


class TestVKProfile(unittest.TestCase):
    """
        Класс проверки класса VKProfile
    """

    def test_profile_creation_valid(self):
        """
            Проверка создания класса TestVKProfile
        """
        vk = VKProfile("Test", "Testov", "Test@example.ru", (10, 10, 2000))
        self.assertEqual(vk.fisrt_name, "Test")
        self.assertEqual(vk.last_name, "Testov")
        self.assertEqual(vk.email, "Test@example.ru")
        self.assertEqual(vk.bfdate, (10, 10, 2000))

    def test_profile_update(self):
        """
            Создание изменения значений дескрипторов в TestVKProfile
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
            Проверка независимости дескрипторов в TestVKProfile
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
            Проверка вызова ошибок в TestVKProfile
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
            Проверка вывода TestVKProfile
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
