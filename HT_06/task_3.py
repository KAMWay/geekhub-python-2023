# 3. Написати функцию <is_prime>, яка прийматиме 1 аргумент - число від 0 до 1000, и яка вертатиме True,
# якщо це число просте і False - якщо ні.
from math import sqrt
from math import sqrt


def in_range(__obj=None, *, accesses_range=(0, 1000)):
    def in_range_decorator(func):
        def wrapper(*args, **kwargs):
            number = func(*args, **kwargs)

            if not number:
                return None

            min_range = min(accesses_range)
            max_range = max(accesses_range)
            if min_range <= number <= max_range:
                return number
            else:
                print(f'The number must be in range {accesses_range}. Try again.')

        return wrapper

    if callable(__obj):
        return in_range_decorator(__obj)

    return in_range_decorator


def integer(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print("Enter number is not integer. Try again.")

    return wrapper


@integer
@in_range(accesses_range=[0, 1000])
def get_integer_in_range(number) -> int:
    return int(number)


def get_integer_number_from_console(msg: str) -> int:
    integer_number = None
    while not integer_number:
        integer_number = get_integer_in_range(input(msg))
    return integer_number


def is_prime(number: int):
    for steep in range(2, int(sqrt(number)) + 1):
        if number % steep == 0:
            return False
    return True


if __name__ == '__main__':
    number = get_integer_number_from_console('Enter number: ')
    print(is_prime(number))
