# Написати функцію, яка приймає на вхід список (через кому), підраховує кількість однакових елементів у ньомy
# і виводить результат. Елементами списку можуть бути дані будь-яких типів.
#     Наприклад:
#     1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2] ----> "1 -> 3, foo -> 2, [1, 2] -> 2, True -> 1"
from collections import Counter


def is_hashable(item):
    try:
        hash(item)
        return True
    except TypeError:
        return False


def get_dict_key_value(item):
    if isinstance(item, bool) or not is_hashable(item):
        return str(item)
    else:
        return item


def get_dict(elements_list: list) -> dict:
    _str_values = list(map(str, elements_list))
    _elements_dict = {}
    for item in elements_list:
        _key = get_dict_key_value(item)
        _value = _str_values.count(str(item))
        _elements_dict[_key] = _value
    return _elements_dict


def get_dict_with_counter(elements_list: list) -> dict:
    return dict(Counter(map(str, elements_list)).items())


if __name__ == '__main__':
    some_list = [None, 1, 1, (1, 'a'), None, 'foo', [1, 2], (1, 'a'), True, None, 'foo', 1, [1, 2]]
    print(get_dict(some_list))
    print(get_dict_with_counter(some_list))
