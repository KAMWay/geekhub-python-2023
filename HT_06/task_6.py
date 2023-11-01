# Написати функцію, яка буде реалізувати логіку циклічного зсуву елементів в списку.
# Тобто функція приймає два аргументи: список і величину зсуву (якщо ця величина додатня - пересуваємо
# з кінця на початок, якщо від'ємна - навпаки - пересуваємо елементи з початку списку в його кінець).
#  Наприклад:
#    fnc([1, 2, 3, 4, 5], shift=1) --> [5, 1, 2, 3, 4]
#    fnc([1, 2, 3, 4, 5], shift=-2) --> [3, 4, 5, 1, 2]


def fnc_shift(items_list: list, shift: int):
    if len(items_list) < 2:
        return items_list

    shift = -shift % len(items_list)
    return items_list[shift:] + items_list[:shift]


if __name__ == '__main__':
    print(fnc_shift([1, 2, 3, 4, 5], 6))
    print(fnc_shift([1, 2, 3, 4, 5], -2))
    print(fnc_shift([], 5))
