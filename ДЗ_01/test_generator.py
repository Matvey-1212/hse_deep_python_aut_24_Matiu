import unittest
from io import StringIO
from generator import file_search_generator


class TestSearchInFile(unittest.TestCase):

    def setUp(self):
        self.test_file = StringIO()
        self.test_file.write("а Роза упала на лапу Азора\n")
        self.test_file.write("тут еще что то\n")
        self.test_file.write("Роза растет в саду\n")
        self.test_file.write("Роза и Азора\n")
        self.test_file.write("Азора не должна учитыватья\n")
        self.test_file.write("роза Роза Роз\n")
        self.test_file.write("конец, точно конец\n")
        self.test_file.seek(0)

    def test_search_word_found(self):
        search_words = ['роза']
        stop_words = []
        self.test_file.seek(0)
        result = list(
            file_search_generator(self.test_file,
                                  search_words, stop_words))
        self.assertEqual(result, ["а Роза упала на лапу Азора",
                                  "Роза растет в саду",
                                  "Роза и Азора",
                                  "роза Роза Роз"])

    def test_stop_word_ignores_line(self):
        search_words = ['роза']
        stop_words = ['азора', 'роз']
        self.test_file.seek(0)
        result = list(
            file_search_generator(self.test_file,
                                  search_words, stop_words))
        self.assertEqual(result, ["Роза растет в саду"])

    def test_no_matches(self):
        search_words = ['любое']
        stop_words = ['азора']
        self.test_file.seek(0)
        result = list(
            file_search_generator(self.test_file,
                                  search_words, stop_words))
        self.assertEqual(result, [])

    def test_empty_input(self):
        search_words = []
        stop_words = []
        self.test_file.seek(0)
        result = list(
            file_search_generator(self.test_file,
                                  search_words, stop_words))
        self.assertEqual(result, [])

    def test_multiple_matches(self):
        search_words = ['конец']
        stop_words = []
        self.test_file.seek(0)
        result = list(
            file_search_generator(self.test_file,
                                  search_words, stop_words))
        self.assertEqual(result, ["конец, точно конец"])

    def test_invalid_input_words_type(self):
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
        with self.assertRaises(TypeError):
            list(
                file_search_generator('User/empty_path/text.txt',
                                      ['word'], ['word']))

        with self.assertRaises(TypeError):

            class FakeFile:
                def __init__(self):
                    self.name = 'FakeFile'

                def __str__(self):
                    return self.name

            list(
                file_search_generator(FakeFile,
                                      ['word'], ['word']))

    def tearDown(self):
        self.test_file.close()


if __name__ == '__main__':
    unittest.main()
