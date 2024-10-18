"""
    В файле реализован метакласс, который в начале названий
    всех атрибутов и методов, кроме магических, добавляет префикс "custom_"
"""


class CustomMeta(type):
    """
        Метакласс, который изменяет название атрибутов
    """

    def __new__(mcs, name, bases, class_dict):
        """
            Создает новый класс, добавляя префикс 'custom_' ко всем
            атрибутам и методам класса, кроме магических и
            начинающихся с 'custom_'.
            Также переопределяет метод __setattr__,
            чтобы добавлять префикс к атрибутам экземпляра класса.
        """
        new_class_dict = {}
        for key, value in class_dict.items():  # обработка атрибутов класса
            # учитываем магические атрибуты и методы,
            # а также учитываем дублирование "custom_"
            if not key.startswith('__') and not key.startswith('custom_'):
                new_class_dict[f'custom_{key}'] = value
            else:
                new_class_dict[key] = value

        new_class = super().__new__(mcs, name, bases, new_class_dict)

        original_setattr = new_class.__setattr__

        def custom_setattr(self, name, value):  # обработка атрибутов экземпляра
            """
                Новый __setatt__, добавляющий префикс к экземпляярам класса
            """
            # учитываем магические атрибуты и методы,
            # а также учитываем дублирование "custom_"
            if not name.startswith('custom_') and not name.startswith('__'):
                original_setattr(self, f'custom_{name}', value)
            else:
                original_setattr(self, name, value)

        new_class.__setattr__ = custom_setattr

        return new_class


class CustomClass(metaclass=CustomMeta):
    """
        Тестовый класс
    """
    x = 50

    def __init__(self, val=99):
        """
            Инициализация
        """
        self.val = val

    def line(self):
        """
            Тестовый метода
        """
        return 100

    def __str__(self):
        """
            Тестовый метода
        """
        return "Custom_by_metaclass"


if __name__ == "__main__":
    assert CustomClass.custom_x == 50  # pylint: disable=E1101
    try:
        _ = CustomClass.x
        print('!')
    except AttributeError:
        pass

    inst = CustomClass()

    try:
        _ = inst.x
        print('!')
    except AttributeError:
        pass

    try:
        _ = inst.val
        print('!')
    except AttributeError:
        pass

    assert inst.custom_x == 50  # pylint: disable=E1101
    assert inst.custom_val == 99  # pylint: disable=E1101
    assert inst.custom_line() == 100  # pylint: disable=E1101
    assert str(inst) == "Custom_by_metaclass"

    try:
        _ = inst.x
        print('!')
    except AttributeError:
        pass

    try:
        _ = inst.val
        print('!')
    except AttributeError:
        pass

    try:
        inst.line()
        print('!')
    except AttributeError:
        pass

    try:
        _ = inst.yyy
        print('!')
    except AttributeError:
        pass

    inst.dynamic = "added later"  # pylint: disable=W0201
    assert inst.custom_dynamic == "added later"  # pylint: disable=E1101
    try:
        _ = inst.dynamic
        print('!')
    except AttributeError:
        pass

    print(inst.__dict__, end='\n\n')
    print(CustomClass.__dict__)
