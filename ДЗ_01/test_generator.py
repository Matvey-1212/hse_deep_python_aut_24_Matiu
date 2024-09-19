import unittest
from unittest import mock
from io import StringIO

from generator import file_searche_generator


class TestSearchInFile(unittest.TestCase):
    
    def setUp(self):
        self.test_file = StringIO()
        self.test_file.write("а Роза упала на лапу Азора\n")
        self.test_file.write("тут еще что то\n")
        self.test_file.write("Роза растет в саду\n")
        self.test_file.write("Азора не должна учитыватья\n")
        self.test_file.seek(0)  

    def test_search_word_found(self):
        search_words = ['роза']
        stop_words = ['азора']
        result = list(file_searche_generator(self.test_file, search_words, stop_words))
        self.assertEqual(result, ["Роза растет в саду"])

    def test_stop_word_ignores_line(self):
        search_words = ['роза']
        stop_words = ['азора']
        self.test_file.write("Роза и Азора\n")
        self.test_file.seek(0)  
        result = list(file_searche_generator(self.test_file, search_words, stop_words))
        self.assertEqual(result, ["Роза растет в саду"])

    def test_no_matches(self):
        search_words = ['нечего']
        stop_words = ['азора']
        self.test_file.seek(0) 
        result = list(file_searche_generator(self.test_file, search_words, stop_words))
        self.assertEqual(result, [])

    def tearDown(self):
        self.test_file.close()

if __name__ == '__main__':
    unittest.main()