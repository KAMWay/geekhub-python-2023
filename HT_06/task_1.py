# 1. Написати функцію <square>, яка прийматиме один аргумент - сторону квадрата, і вертатиме 3 значення
# у вигляді кортежа: периметр квадрата, площа квадрата та його діагональ.
from math import sqrt


def to_number(value):
    try:
        try:
            return int(value)
        except ValueError:
            return float(value)
    except ValueError:
        return None


def get_from_console() -> int or float:
    while True:
        _values = to_number(input('Enter the side of the square: '))
        if _values and _values >= 0:
            return _values
        else:
            print('Not valid input. Try again.')


def square(side: int or float) -> tuple:
    return 4 * side, side ** 2, side * sqrt(2)


if __name__ == '__main__':
    side_of_square = get_from_console()
    print(square(side_of_square))
