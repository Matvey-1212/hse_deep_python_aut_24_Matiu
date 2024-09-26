"""
    В файле реализован обработчик декоратор
        с функциоей повтора при ошибке
"""

from functools import wraps
from typing import Callable, List, Optional, Type


def retry_deco(
    retries: int = 1,
    exceptions: Optional[List[Type[BaseException]]] = None
) -> Callable:
    """
        Декоратор для повторного выполнения функции в случае ошибок

        Args:
            retries: Количество попыток выполнения функции
            exceptions: Список классов исключений,
                при возникновении которых не нужно повторно выполнять функцию
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while attempt <= retries:
                output = ''
                output += f'run "{func.__name__}"'
                if len(args) != 0 or len(kwargs) != 0:
                    output += " with "
                else:
                    output += ", "
                if len(args) != 0:
                    output += f"positional args = {args}, "
                if len(kwargs) != 0:
                    output += f"keyword kwargs = {kwargs}, "
                try:
                    result = func(*args, **kwargs)
                    output += f"attempt = {attempt}, result = {result}"
                    print(output, end='\n\n')
                    return result
                except Exception as e:  # pylint: disable=broad-exception-caught
                    output += f"attempt = {attempt}, "
                    output += f"exception = {type(e).__name__}"
                    if ((exceptions is not None) and
                            (any(isinstance(e, exc) for exc in exceptions))):
                        print(output, end='\n\n')
                        break
                    attempt += 1
                    print(output, end='\n' if attempt <= retries else '\n\n')
            return None
        return wrapper
    return decorator


@retry_deco(3)
def add(a, b):
    """
        Тестовая функция
    """
    return a + b


@retry_deco(3)
def check_str(value=None):
    """
        Тестовая функция
    """
    if value is None:
        raise ValueError()

    return isinstance(value, str)


@retry_deco(2, [ValueError])
def check_int(value=None):
    """
        Тестовая функция
    """
    if value is None:
        raise ValueError()

    return isinstance(value, int)


@retry_deco(2, [ValueError])
def check_empty():
    """
        Тестовая функция
    """
    return True


if __name__ == '__main__':
    add(4, 2)
    add(4, b=3)

    check_str(value="123")
    check_str(value=1)
    check_str(value=None)

    check_int(value=1)
    check_int(value=None)

    check_empty()
