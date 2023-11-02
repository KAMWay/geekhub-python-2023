# Написати функцію <prime_list>, яка прийматиме 2 аргументи - початок і кінець діапазона, і вертатиме список простих
# чисел всередині цього діапазона. Не забудьте про перевірку на валідність введених даних та у випадку невідповідності -
# виведіть повідомлення.

from math import sqrt


def integer(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return None

    return wrapper


def range_args(func):
    def wrapper(*args, **kwargs):
        numbers = func(*args, **kwargs)

        if not numbers or len(numbers) != 2:
            return None

        return numbers if (numbers[0] and numbers[1]) and (numbers[0] < numbers[1]) else None

    return wrapper


@range_args
@integer
def get_range_args(args_str: str):
    return list(map(int, args_str.split(' ')[:2]))


def get_range_args_from_console() -> []:
    str_line = input("Enter range (e.g 'start' 'end'): ")

    range_args = None
    while not range_args and len(str_line.split()) < 3:
        range_args = get_range_args(str_line.strip())

        if len(str_line.split()) < 2:
            str_line += ' ' + input().strip()
        else:
            return range_args

    return range_args


def is_prime(number: int):
    for steep in range(2, int(sqrt(number)) + 1):
        if number % steep == 0:
            return False
    return True


def prime_list(start: int, end: int) -> list:
    return list(filter(lambda number: is_prime(number), range(max(start, 2), max(end + 1, 2))))


if __name__ == '__main__':
    range_args = get_range_args_from_console()

    if range_args:
        print(prime_list(range_args[0], range_args[1]))
    else:
        print("Can't parser range args.")
