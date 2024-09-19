import os

def find_line(str_file, search_words, stop_words):
    for line in str_file:
        words_in_line = line.lower().strip().split()
        
        if any(word in stop_words for word in words_in_line):
            continue 
        
        if any(word in search_words for word in words_in_line):
            yield line.strip()  

def file_searche_generator(file, search_words, stop_words):
    
    if not isinstance(search_words, list) or not all(isinstance(word, str) for word in search_words):
        raise TypeError("Список слов для поиска должен быть списком строк.")
    if not isinstance(stop_words, list) or not all(isinstance(word, str) for word in stop_words):
        raise TypeError("Список стоп-слов должен быть списком строк.")
    
    search_words = set(word.lower() for word in search_words)
    stop_words = set(word.lower() for word in stop_words)

    if isinstance(file, str) and os.path.isfile(file):
        with open(file, 'r', encoding='utf-8') as file_object:
            yield from find_line(file_object, search_words, stop_words)
    else:
        yield from find_line(file, search_words, stop_words)

if __name__ == '__main__':
    search_words = ['роза']
    stop_words = ['стопслово']

    for matching_line in file_searche_generator("fish_text.txt", search_words, stop_words):
        print(matching_line)
