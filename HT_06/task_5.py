# Написати функцію <fibonacci>, яка приймає один аргумент і виводить всі числа Фібоначчі, що не перевищують його.

def positive(func):
    def wrapper(*args, **kwargs):
        number = func(*args, **kwargs)

        if not number:
            return None

        if number > 0:
            return number
        else:
            print(f"The number must be positive. Try again.")

    return wrapper


@positive
def get_positive_integer_number(number) -> int:
    try:
        return int(number)
    except ValueError:
        print(f"{number} is not integer number. Try again.")


def get_positive_integer_number_from_console() -> int:
    positive_number = None
    while not positive_number:
        positive_number = get_positive_integer_number(input('Enter positive integer number: '))

    return positive_number


def fibonacci(max_number: int):
    n1, n2 = 0, 1
    while n1 < max_number:
        print(n1, end=" ")
        n1, n2 = n2, n1 + n2


if __name__ == '__main__':
    max_number = get_positive_integer_number_from_console()
    fibonacci(max_number)
