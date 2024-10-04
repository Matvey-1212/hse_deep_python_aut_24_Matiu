"""
    В файле реализован класс CustomList
"""


class CustomList(list):
    """
        Класс CustomList - содержит перегрузку
            некоторых операторов исходного List
    """

    def _custom_getitem(self, index, lst=None):
        """
            Возвращает элемент списка по индексу
                или 0, если индекс выходит за границы
        """
        if lst is None:
            lst = self
        return lst[index] if index < len(lst) else 0

    def __add__(self, other):
        """
            Переопределение сложения CustomList с CustomList, числом или List
        """
        if isinstance(other, list):
            max_length = max(len(self), len(other))
            result = [
                self._custom_getitem(i) + self._custom_getitem(i, other)
                for i in range(max_length)
                ]
            return CustomList(result)
        if isinstance(other, int):
            if len(self) == 0:
                return CustomList([other])
            return CustomList([x + other for x in self])
        raise TypeError(f"CustomList нельзя складывать с {type(other)}")

    def __radd__(self, other):
        """
            Обратное сложение, когда CustomList идет вторым операндом
        """
        return self.__add__(other)

    def __sub__(self, other):
        """
            Переопределение вычитания CustomList
                с другим списком, числом или CustomList
        """
        if isinstance(other, list):
            max_length = max(len(self), len(other))
            result = [
                self._custom_getitem(i) - self._custom_getitem(i, other)
                for i in range(max_length)
                ]
            return CustomList(result)
        if isinstance(other, int):
            if len(self) == 0:
                return CustomList([-other])
            return CustomList([x - other for x in self])
        raise TypeError(f"CustomList нельзя складывать с {type(other)}")

    def __rsub__(self, other):
        """
            Обратное вычитание, когда CustomList идет вторым операндом
        """
        if isinstance(other, list):
            max_length = max(len(self), len(other))
            result = [
                self._custom_getitem(i, other) - self._custom_getitem(i)
                for i in range(max_length)
            ]
            return CustomList(result)
        if isinstance(other, int):
            if len(self) == 0:
                return CustomList([other])
            return CustomList([other - x for x in self])
        raise TypeError(f"CustomList нельзя складывать с {type(other)}")

    def __eq__(self, other):
        """
            Переопределение сравнения на равенство по сумме элементов списка
        """
        if isinstance(other, CustomList):
            return sum(self) == sum(other)
        raise TypeError(f"CustomList нельзя сравнивать с {type(other)}")

    def __ne__(self, other):
        """
            Переопределение != по сумме элементов списка
        """
        if isinstance(other, CustomList):
            return sum(self) != sum(other)
        raise TypeError(f"CustomList нельзя сравнивать с {type(other)}")

    def __lt__(self, other):
        """
            Переопределение оператора < по сумме элементов списка
        """
        if isinstance(other, CustomList):
            return sum(self) < sum(other)
        raise TypeError(f"CustomList нельзя сравнивать с {type(other)}")

    def __le__(self, other):
        """
            Переопределение оператора <= по сумме элементов списка
        """
        if isinstance(other, CustomList):
            return sum(self) <= sum(other)
        raise TypeError(f"CustomList нельзя сравнивать с {type(other)}")

    def __gt__(self, other):
        """
            Переопределение оператора > по сумме элементов списка
        """
        if isinstance(other, CustomList):
            return sum(self) > sum(other)
        raise TypeError(f"CustomList нельзя сравнивать с {type(other)}")

    def __ge__(self, other):
        """
            Переопределение оператора >= по сумме элементов списка
        """
        if isinstance(other, CustomList):
            return sum(self) >= sum(other)
        raise TypeError(f"CustomList нельзя сравнивать с {type(other)}")

    def __str__(self):
        """
            Переопределение метода str для перевода элементов
                списка и их суммы в строку
        """
        return f"{list(self)}, сумма: {sum(self)}"
