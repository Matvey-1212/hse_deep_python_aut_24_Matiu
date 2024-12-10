"""
    В файле реализованы тесты для generator.py
"""
import unittest
from io import StringIO
from generator import file_search_generator


class TestSearchInFile(unittest.TestCase):
    """
    Тестовый класс для проверки функции file_search_generator
    """
    def setUp(self):
        """
            Инициализация тестовых данных.

            Создает файловый объект StringIO с несколькими строками текста
        """
        self.test_file = StringIO()
        self.test_file.write("а Роза упала на лапу Азора\n")
        self.test_file.write("тут еще что то\n")
        self.test_file.write("Роза растет в саду\n")
        self.test_file.write("Роза и Азора\n")
        self.test_file.write("Азора не должна учитыватья\n")
        self.test_file.write("роза Роза Роз\n")
        self.test_file.write("конец, точно конец\n")
        self.test_file.write("розан\n")
        self.test_file.write("РоЗА на траве роз\n")
        self.test_file.write("розанА на траве\n")
        self.test_file.write("роза\n")
        self.test_file.write("рОзА\n")
        self.test_file.write("розана\n")
        self.test_file.write("азора\n")
        self.test_file.write("рОз роза\n")
        self.test_file.seek(0)

    def test_search_word_found(self):
        """
        Проверяет, что функция находит строки с искомыми словами
        """
        search_words = ['роза']
        stop_words = []
        self.test_file.seek(0)
        result = list(
            file_search_generator(self.test_file,
                                  search_words, stop_words))
        self.assertEqual(result, ["а Роза упала на лапу Азора",
                                  "Роза растет в саду",
                                  "Роза и Азора",
                                  "роза Роза Роз",
                                  "РоЗА на траве роз",
                                  "роза",
                                  "рОзА",
                                  "рОз роза"])

    def test_stop_word_ignores_line(self):
        """
        Проверяет, что строки со стоп-словами игнорируются
        """
        search_words = ['роза']
        stop_words = ['азора', 'роз']
        self.test_file.seek(0)
        result = list(
            file_search_generator(self.test_file,
                                  search_words, stop_words))
        self.assertEqual(result, ["Роза растет в саду", "роза", "рОзА"])

    def test_no_matches(self):
        """
        Проверяет, что функция возвращает пустой список
        при отсутствии совпадений
        """
        search_words = ['любое']
        stop_words = ['азора']
        self.test_file.seek(0)
        result = list(
            file_search_generator(self.test_file,
                                  search_words, stop_words))
        self.assertEqual(result, [])

    def test_empty_input(self):
        """
        Проверяет, что функция возвращает пустой список
        при пустых входных данных
        """
        search_words = []
        stop_words = []
        self.test_file.seek(0)
        result = list(
            file_search_generator(self.test_file,
                                  search_words, stop_words))
        self.assertEqual(result, [])

    def test_multiple_matches(self):
        """
        Проверяет, что функция корректно находит строки
        с несколькими совпадениями
        """
        search_words = ['конец']
        stop_words = []
        self.test_file.seek(0)
        result = list(
            file_search_generator(self.test_file,
                                  search_words, stop_words))
        self.assertEqual(result, ["конец, точно конец"])

    def test_invalid_input_words_type(self):
        """
        Проверяет, что функция выбрасывает TypeError для
        некорректных типов входных данных
        """
        with self.assertRaises(TypeError):
            list(
                file_search_generator(self.test_file,
                                      [123], ['stop_words']))

        with self.assertRaises(TypeError):
            list(
                file_search_generator(self.test_file,
                                      ['word'], [123]))

        with self.assertRaises(TypeError):
            list(
                file_search_generator(self.test_file,
                                      ['word'], 123))

        with self.assertRaises(TypeError):
            list(
                file_search_generator(self.test_file,
                                      123, ['stop_words']))

    def test_invalid_file_type(self):
        """
        Проверяет, что функция выбрасывает TypeError
        для некорректного типа файла
        """
        with self.assertRaises(TypeError):
            list(
                file_search_generator('User/empty_path/text.txt',
                                      ['word'], ['word']))

        with self.assertRaises(TypeError):

            class FakeFile:
                """
                Класс для имитации файлового объекта
                без методов read и write
                """
                def __init__(self):
                    self.name = 'FakeFile'

                def __str__(self):
                    return self.name

                def get_name(self):
                    """Метод для обхода pylint"""
                    return self.name

            list(
                file_search_generator(FakeFile,
                                      ['word'], ['word']))

    def tearDown(self):
        """
        Закрывает тестовый файловый объект после завершения тестов
        """
        self.test_file.close()


if __name__ == '__main__':
    unittest.main()
