# Написати функцію, яка приймає на вхід список (через кому), підраховує кількість однакових елементів у ньомy
# і виводить результат. Елементами списку можуть бути дані будь-яких типів.
#     Наприклад:
#     1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2] ----> "1 -> 3, foo -> 2, [1, 2] -> 2, True -> 1"


def dict_key(func):
    def wrapper(key, value):
        try:
            return func(str(key) if isinstance(key, bool) else item, value)
        except TypeError:
            return {str(key): value}

    return wrapper


@dict_key
def get_dict(key, value):
    return {key: value}


if __name__ == '__main__':

    some_list = [None, 1, 1, (1, 'a'), None, 'foo', [1, 2], (1, 'a'), True, None, 'foo', 1, [1, 2]]

    str_values = list(map(str, some_list))
    some_dict = {}
    for item in some_list:
        some_dict.update(get_dict(item, str_values.count(str(item))))

    print(some_dict)
