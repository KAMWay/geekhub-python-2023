# Написати функцію <prime_list>, яка прийматиме 2 аргументи - початок і кінець діапазона, і вертатиме список простих
# чисел всередині цього діапазона. Не забудьте про перевірку на валідність введених даних та у випадку невідповідності -
# виведіть повідомлення.

from math import sqrt


def get_from_console():
    while True:
        try:
            return list(map(int, input("Enter range (e.g 'start' 'end'):").split()[:2]))
        except ValueError:
            print('Not valid input. Try again.')


def is_prime(number: int):
    for i in range(2, int(sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True


def prime_list(start_range: int, end_range: int) -> list:
    if not start_range or not end_range:
        return []

    if start_range > end_range:
        start_range, end_range = end_range, start_range

    return list(filter(lambda number: is_prime(number), range(max(start_range, 2), max(end_range + 1, 2))))


if __name__ == '__main__':
    start, end = get_from_console()
    print(prime_list(start, end))
