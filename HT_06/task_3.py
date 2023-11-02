# 3. Написати функцию <is_prime>, яка прийматиме 1 аргумент - число від 0 до 1000, и яка вертатиме True,
# якщо це число просте і False - якщо ні.
from math import sqrt
from math import sqrt


def to_integer(value):
    try:
        return int(value)
    except ValueError:
        return None


def get_from_console() -> int:
    while True:
        _values = to_integer(input('Enter number [0..1000]: '))
        if _values and 0 <= _values <= 1000:
            return _values
        else:
            print('Not valid input. Try again.')


def is_prime(number: int):
    for i in range(2, int(sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True


if __name__ == '__main__':
    number = get_from_console()
    print(is_prime(number))
