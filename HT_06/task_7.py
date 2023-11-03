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


def to_string(items_dict: dict) -> str:
    return ', '.join(f'{key}:{val}' for key, val in items_dict.items())


def print_dict_with_counter(elements_list: list):
    hashable_items = filter(lambda i: is_hashable(i) and not isinstance(i, bool), elements_list)
    hashable_items_dict = dict(Counter(hashable_items).items())

    not_hashable_items = filter(lambda i: not is_hashable(i), elements_list)
    not_hashable_items_dict = dict(Counter(map(str, not_hashable_items)).items())

    boll_items = filter(lambda i: isinstance(i, bool), elements_list)
    boll_items_dict = dict(Counter(boll_items).items())

    print(to_string(hashable_items_dict), end=', ')
    print(to_string(boll_items_dict), end=', ')
    print(to_string(not_hashable_items_dict))


if __name__ == '__main__':
    some_list = [None, 1, 1, (1, 'a'), None, 'foo', False, 'True', [1, 2], (1, 'a'), True, None, 'foo', 1, [1, 2]]
    print_dict_with_counter(some_list)
