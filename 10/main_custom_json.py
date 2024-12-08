"""
В файле реализован вызов custom_json
"""

import time
import json
import custom_json


def main():
    """
    Просто main
    """
    with open('generated_data_1.json', 'r', encoding='utf-8') as generate_file:
        json_str = generate_file.read()

    # json_str = '{"hello": 10, "world": "value"}'

    t = time.time()
    json_doc = json.loads(json_str)
    t2 = time.time() - t
    t = time.time()
    cust_json_doc = custom_json.loads(json_str)  # pylint: disable=I1101
    t3 = time.time() - t
    print(t2, t3)

    assert json_doc == cust_json_doc

    t = time.time()
    json_str_1 = json.dumps(json_doc)
    t2 = time.time() - t
    t = time.time()
    json_str_2 = custom_json.dumps(json_doc)  # pylint: disable=I1101
    t3 = time.time() - t
    print(t2, t3)
    assert json_str_1 == json_str_2
    # print(json_str_1)
    # print(json_str_2)


if __name__ == "__main__":
    main()
