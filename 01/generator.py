"""
    В файле реализован генератор для поиска строк в текстовом файле
"""
import os


def find_line(str_file, search_words_list, stop_words_list):
    """Ищет строки в файле, содержащие искомые слова и
        игнорирует строки со стоп-словами.

    Args:
        file (file/str): Путь к файлу или файловый объект.
        search_words_list (list[str]): Список слов, которые необходимо
                                        найти в строках.
        stop_words_list (list[str]): Список слов, которые игнорируют строки.

    Yields:
        str: Строки, содержащие искомые слова.
    """
    for line in str_file:
        words_in_line = line.lower().strip().split()

        if any(word in stop_words_list for word in words_in_line):
            continue

        if any(word in search_words_list for word in words_in_line):
            yield line.strip()


def file_search_generator(file, search_words, stop_words):
    """Генератор, ищет содержащие искомые слова и не содержащие стоп-слова.

    Args:
        file (file/str): Путь к файлу или файловый объект.
        search_words (list[str]): Список слов, которые необходимо
                                    найти в строках.
        stop_words (list[str]): Список слов, которые игнорируют строки.

    Yields:
        str: Строки, содержащие искомые слова.
    """
    if ((not isinstance(search_words, list)) or
            (not all(isinstance(word, str) for word in search_words))):
        raise TypeError("Список слов для поиска должен быть списком строк")

    if ((not isinstance(stop_words, list)) or
            (not all(isinstance(word, str) for word in stop_words))):
        raise TypeError("Список стоп-слов должен быть списком строк")

    search_words = set(word.lower() for word in search_words)
    stop_words = set(word.lower() for word in stop_words)

    if isinstance(file, str):
        if os.path.isfile(file):
            with open(file, 'r', encoding='utf-8') as file_object:
                yield from find_line(file_object, search_words, stop_words)
        else:
            raise TypeError("file не существует по указанному пути")
    elif hasattr(file, 'read') and hasattr(file, 'write'):
        yield from find_line(file, search_words, stop_words)
    else:
        raise TypeError("file должен быть либо путем, либо объектом файла")


if __name__ == '__main__':
    words_to_find = ['роза']
    words_to_stop = ['стопслово']

    for matching_line in file_search_generator(
            "fish_text.txt", words_to_find, words_to_stop):
        print(matching_line)
