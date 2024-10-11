"""
    В файле реализовано использование дескрипторов.
"""

import re
from datetime import datetime


class BaseDescriptor:
    """
        Базовый дескриптор для проверки и установки значений.
    """
    def __init__(self):
        """
        Инициализирует дескриптор.
        """
        self.name = None

    def __set_name__(self, owner, name):
        """
            Устанавливает имя атрибута.

            Параметры:
                owner: Класс, которому принадлежит дескриптор.
                name: Имя атрибута.
        """
        self.name = f"_{name}"

    def __get__(self, obj, objtype):
        """
            Получает значение атрибута.
        """
        if obj is None:
            return None

        return getattr(obj, self.name, None)

    def __set__(self, obj, value):
        """
            Устанавливает значение атрибута после проверки.
        """
        self.check_value(value)
        setattr(obj, self.name, value)

    def check_value(self, value):
        """
            Абстрактный метод для проверки значения.
        """
        raise NotImplementedError()


class Name(BaseDescriptor):  # pylint: disable=too-few-public-methods
    """
        Дескриптор хранящий имя/фамилию пользователя.
    """
    def check_value(self, value):
        """
            Проверка корректности полученных данных.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Username must be a non-empty string.")

        if not re.match(r"^[A-Za-zА-Яа-яЁё\s-]+$", value):
            raise ValueError(
                "The username must contain only letters, spaces, or hyphens."
            )

        if value.strip() == "" or all(char in " -" for char in value):
            raise ValueError("The username cannot ",
                             "consist only of spaces or hyphens.")


class Email(BaseDescriptor):  # pylint: disable=too-few-public-methods
    """
        Дескриптор хранящий email пользователя.
    """
    def check_value(self, value):
        """
            Проверка корректности полученных данных.
        """
        email_r = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\."
        if (
            not isinstance(value, str)
            or not re.match(email_r, value)
            or not value.endswith(".ru")
        ):
            raise ValueError("Email must be in correct format.")


class BFDate(BaseDescriptor):  # pylint: disable=too-few-public-methods
    """
        Дескриптор хранящий дату рождения пользователя.
    """
    def check_value(self, value):
        """
            Проверка корректности полученных данных.
        """
        if not isinstance(value, tuple):
            raise TypeError(f"bf should be a tuple. Cur type is {type(value)};")
        if not len(value) == 3:
            raise ValueError(
                "bf should containt day, month, year. ",
                f"Now lenght of bf is {len(value)};"
            )

        day = value[0]
        month = value[1]
        year = value[2]

        if (
            not isinstance(day, int)
            or not isinstance(month, int)
            or not isinstance(year, int)
        ):
            raise TypeError(
                "Day, month, year. should be an int. ",
                f"Cur type is day: {type(value)}, ",
                f"month: {type(value)}, year: {type(value)};"
            )

        try:
            parsed_date = datetime.strptime(f"{day} {month} {year}", "%d %m %Y")
            current_date = datetime.now()
        except ValueError as e:
            raise ValueError("date format is invalid") from e

        if parsed_date > current_date:
            raise ValueError("you couldn't have been born now")
        if (current_date.year - parsed_date.year) > 150:
            raise ValueError("you can't be that old")
        if (current_date.year - parsed_date.year) < 14:
            raise ValueError("you can't be that young")


class VKProfile:  # pylint: disable=too-few-public-methods
    """
        Класс профиля ВК, реализующий использование дескрипторов.
    """
    fisrt_name = Name()
    last_name = Name()
    email = Email()
    bfdate = BFDate()

    def __init__(self, fisrt_name, last_name, email, bfdate):
        """
            Инициализация объекта класса.
        """
        self.fisrt_name = fisrt_name
        self.last_name = last_name
        self.email = email
        self.bfdate = bfdate

    def print(self):
        """
            Вывод данных для проверки.
        """
        print(
            f"fisrt_name: {self.fisrt_name}; " +
            f"last_name: {self.last_name}; " +
            f"email: {self.email}; " +
            f"bfdate: {self.bfdate};"
        )


if __name__ == "__main__":
    user = VKProfile(
        "Matvey",
        "Antonov",
        "mtv@mail.ru",
        (11, 11, 1911)
        )
    user1 = VKProfile(
        "Gennadij",
        "Kandaurov",
        "test_email@mail.ru",
        (12, 12, 1912)
        )
    user.print()
    user1.print()

    user.fisrt_name = "laev"
    user.print()
    user1.print()
    # print(VKProfile.fisrt_name.check_str())
