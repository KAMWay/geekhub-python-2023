# Написати функцію <fibonacci>, яка приймає один аргумент і виводить всі числа Фібоначчі, що не перевищують його.

def get_from_console():
    while True:
        try:
            return int(input("Enter positive integer number:"))
        except ValueError:
            print('Not valid input. Try again.')


def fibonacci(max_number: int):
    _current_number, _next_number = 0, 1
    while _current_number < max_number:
        print(_current_number, end=" ")
        _current_number, _next_number = _next_number, _current_number + _next_number


if __name__ == '__main__':
    number = get_from_console()
    fibonacci(number)
