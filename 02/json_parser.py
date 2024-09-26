"""
В файле реализован обработчик JSON строки с использованием Callback функции
"""

import json
from typing import Callable, List, Optional


def process_json(
    json_str: str,
    required_keys: Optional[List[str]] = None,
    tokens: Optional[List[str]] = None,
    callback: Optional[Callable[[str, str], None]] = None,
) -> None:
    """
    Обрабатывает JSON строку, вызывая функцию-обработчик для ключей и токенов.

    Args:
        json_str (str): Строка с JSON
        required_keys (Optional[List[str]]): Список ключей для поиска
        tokens (Optional[List[str]]): Список токенов для поиска
        callback (Optional[Callable[[str, str], None]]): Функция-обработчик,
            которая вызывается для каждого найденного ключа и токена
    """
    if not isinstance(json_str, str):
        raise TypeError("JSON должен быть строкой")

    if required_keys is None:
        required_keys = []
    elif ((not isinstance(required_keys, list)) or
            (not all(isinstance(key, str) for key in required_keys))):
        raise TypeError("Список ключей должен быть списком строк")

    if tokens is None:
        tokens = []
    elif ((not isinstance(tokens, list)) or
            (not all(isinstance(token, str) for token in tokens))):
        raise TypeError("Список токенов должен быть списком строк")

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as exc:
        raise ValueError("Некорректная строка JSON") from exc

    tokens_lower = [token.lower() for token in tokens]

    for key, value in data.items():
        if key in required_keys:
            words = value.split(' ')
            for word in words:
                if word.lower() in tokens_lower:
                    if callback:
                        callback(key, word)


if __name__ == '__main__':
    JSON_INPUT = '{"key1": "Word1 word2", "key2": "word2 word3"}'
    keys_input = ["key1", "KEY2"]
    tokens_input = ["WORD1", "word2"]

    process_json(
        JSON_INPUT,
        keys_input,
        tokens_input,
        lambda key, token: print(f"{key=}, {token=}")
    )

    keys_input = ["key2"]

    process_json(
        JSON_INPUT,
        keys_input,
        tokens_input,
        lambda key, token: print(f"{key=}, {token=}")
    )
