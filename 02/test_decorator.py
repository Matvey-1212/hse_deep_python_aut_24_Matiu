"""
    Тесты для декоратора retry_deco

"""

import unittest
from unittest.mock import Mock, patch
from custom_decorator import retry_deco


class TestRetryDeco(unittest.TestCase):
    """
        Тесты для декоратора retry_deco
    """

    def setUp(self):
        """
            Настройка перед каждым тестом
        """
        self.mock_func = Mock()

    def test_retry_deco_successful_run(self):
        """
            Тест успешного выполнения функции без исключений
        """
        @retry_deco(3)
        def add(a, b):
            return a + b

        result = add(2, 3)
        self.assertEqual(result, 5)

    def test_retry_deco_positional_args(self):
        """
            Тест успешного выполнения с позиционными аргументами
        """
        @retry_deco(3)
        def add(a, b):
            return a + b

        result = add(4, 2)
        self.assertEqual(result, 6)

    def test_retry_deco_keyword_args(self):
        """
            Тест успешного выполнения с именованными аргументами
        """
        @retry_deco(3)
        def check_str(value=None):
            if value is None:
                raise ValueError()

            return isinstance(value, str)

        result = check_str(value='str')
        self.assertEqual(result, True)

    def test_retry_deco_with_exception_retry(self):
        """
            Тест с перезапусками при возникновении исключения
        """
        @retry_deco(2)
        def func_with_exception1():
            raise ValueError()

        @retry_deco(3)
        def func_with_exception2():
            raise TypeError()

        @retry_deco(4)
        def func_with_exception3():
            raise RuntimeError("Test error")

        with self.assertRaises(ValueError):
            with patch('builtins.print') as mocked_print:
                func_with_exception1()
                self.assertEqual(mocked_print.call_count, 2)

        with self.assertRaises(TypeError):
            with patch('builtins.print') as mocked_print:
                func_with_exception2()
                self.assertEqual(mocked_print.call_count, 3)

        with self.assertRaises(RuntimeError):
            with patch('builtins.print') as mocked_print:
                func_with_exception3()
                self.assertEqual(mocked_print.call_count, 4)

    def test_retry_deco_with_exception_no_retry(self):
        """
            Тест без перезапусков, если исключение из списка ожидаемых
        """
        @retry_deco(15, [ValueError])
        def check_int(value=None):
            if value is None:
                raise ValueError()
            return isinstance(value, int)

        with self.assertRaises(ValueError):
            with patch('builtins.print') as mocked_print:
                check_int(value=None)
                self.assertEqual(mocked_print.call_count, 1)

    def test_retry_deco_function_return(self):
        """
            Тест функции, которая возвращает значение после трех попыток
        """
        attempt = 0

        @retry_deco(3)
        def occasionally_fails():
            nonlocal attempt
            attempt += 1
            if attempt < 3:
                raise ValueError()
            return True

        with patch('builtins.print') as mocked_print:
            result = occasionally_fails()
            self.assertEqual(result, True)
            self.assertEqual(mocked_print.call_count, 3)

    def test_retry_deco_no_retries_due_to_exception_type(self):
        """
            Тест без повторного запуска из-за
                типа исключения в списке исключений
        """
        @retry_deco(3, [ValueError])
        def func_with_key_error():
            raise ValueError()

        with self.assertRaises(ValueError):
            with patch('builtins.print') as mocked_print:
                result = func_with_key_error()
                self.assertIsNone(result)
                self.assertEqual(mocked_print.call_count, 1)

    def test_print_output_on_success_pos_arg(self):
        """
            Тест корректности вывода print при
                успешном выполнении функции c позиционными аргументами
        """
        @retry_deco(3)
        def add(a, b):
            return a + b

        with patch('builtins.print') as mocked_print:
            add(4, 2)
            mocked_print.assert_called_with(
                'run "add" with positional args = (4, 2), ' +
                'attempt = 1, result = 6',
                end='\n\n'
                )

    def test_print_output_on_success_kwargs(self):
        """
            Тест корректности вывода print при
                успешном выполнении функции с именованными аргументами
        """
        @retry_deco(3)
        def add(a, b):
            return a + b

        with patch('builtins.print') as mocked_print:
            add(a=4, b=2)
            mocked_print.assert_called_with(
                'run "add" with keyword kwargs = {\'a\': 4, \'b\': 2}, ' +
                'attempt = 1, result = 6',
                end='\n\n')

    def test_print_output_on_success_empty_input(self):
        """
            Тест корректности вывода print без аргументов
        """
        @retry_deco(3)
        def check_empty():
            return True

        with patch('builtins.print') as mocked_print:
            check_empty()
            mocked_print.assert_called_with(
                'run "check_empty", attempt = 1, result = True',
                end='\n\n'
                )

    def test_print_output_on_exception_with_retries(self):
        """
            Тест корректности вывода print
                при возникновении исключения и перезапусках
        """
        @retry_deco(3)
        def check_str(value=None):
            if value is None:
                raise ValueError()
            return isinstance(value, str)

        with self.assertRaises(ValueError):
            with patch('builtins.print') as mocked_print:
                check_str(value=None)
                expected_calls = [
                    unittest.mock.call(
                        'run "check_str" with keyword kwargs ' +
                        '= {\'value\': None},' +
                        ' attempt = 1, exception = ValueError',
                        end='\n'
                        ),
                    unittest.mock.call(
                        'run "check_str" with keyword kwargs ' +
                        '= {\'value\': None},' +
                        ' attempt = 2, exception = ValueError',
                        end='\n'
                        ),
                    unittest.mock.call(
                        'run "check_str" with keyword kwargs ' +
                        '= {\'value\': None},' +
                        ' attempt = 3, exception = ValueError',
                        end='\n\n'
                        )
                ]
                mocked_print.assert_has_calls(expected_calls, any_order=False)

    def test_print_output_on_no_retry_due_to_exception(self):
        """
            Тест корректности вывода print при исключении,
                которое не должно запускать повторный вызов
        """
        @retry_deco(2, [ValueError])
        def check_int(value=None):
            if value is None:
                raise ValueError()

        with self.assertRaises(ValueError):
            with patch('builtins.print') as mocked_print:
                check_int(value=None)
                mocked_print.assert_called_once_with(
                    'run "check_int" with keyword kwargs ' +
                    '= {\'value\': None}, ' +
                    'attempt = 1, exception = ValueError',
                    end='\n\n'
                    )


if __name__ == '__main__':
    unittest.main()
