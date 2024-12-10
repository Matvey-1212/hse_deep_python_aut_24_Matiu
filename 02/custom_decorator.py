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
            allowed_exceptions_tuple = tuple(exceptions) if exceptions else ()
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
                except allowed_exceptions_tuple as e:
                    exception_name = type(e).__name__
                    output += (
                        f", attempt = {attempt}, "
                        f"allowed exception = {exception_name}"
                    )
                    print(output)
                    raise
                except Exception as e:  # pylint: disable=broad-exception-caught
                    exception_name = type(e).__name__
                    output += (f", attempt = {attempt}, "
                               f"exception = {exception_name}")
                    print(output)
                    if attempt == retries:
                        raise
                    attempt += 1
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
    try:
        check_str(value=None)
    except Exception:  # pylint: disable=broad-exception-caught
        print('Catch exception')

    check_int(value=1)
    try:
        check_int(value=None)
    except Exception:  # pylint: disable=broad-exception-caught
        print('Catch exception')

    check_empty()
