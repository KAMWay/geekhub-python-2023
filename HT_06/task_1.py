# 1. Написати функцію <square>, яка прийматиме один аргумент - сторону квадрата, і вертатиме 3 значення
# у вигляді кортежа: периметр квадрата, площа квадрата та його діагональ.
from math import sqrt


def square(side: int or float) -> tuple:
    return 4 * side, side ** 2, side * sqrt(2)


def get_number_from_console() -> int or float:
    while True:
        number = input('Enter the side of the square: ')
        try:
            try:
                return int(number)
            except ValueError:
                return float(number)
        except ValueError:
            print(f"{number} is not number. Try again.")


def get_side_of_square_from_console() -> int or float:
    side = 0
    while side <= 0:
        side = get_number_from_console()
        if side <= 0:
            print(f"The side of the square must be positive. Try again.")
    return side


if __name__ == '__main__':
    side_of_square = get_side_of_square_from_console()
    print(square(side_of_square))
