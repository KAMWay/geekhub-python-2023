# Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї функції. Тобто щоб її можна було використати у вигляді:
#     for i in my_range(1, 10, 2):
#         print(i)
#     1
#     3
#     5
#     7
#     9
#    P.S. Повинен вертатись генератор.
#    P.P.S. Для повного розуміння цієї функції - можна почитати документацію по ній: https://docs.python.org/3/library/stdtypes.html#range
#    P.P.P.S Не забудьте обробляти невалідні ситуації (аналог range(1, -10, 5)). Подивіться як веде себе стандартний range в таких випадках.

def custom_range(*args) -> iter:
    def is_valid_args(*args) -> bool:
        return 1 <= len(args) <= 3 and all([isinstance(arg, int) for arg in args])

    def inner_range(start: int, stop: int, steep: int = 1) -> iter:
        if start > stop and steep > 0:
            iter(())

        __item = start
        __ind = 1 if steep > 0 else -1
        while __item * __ind < stop * __ind:
            yield __item
            __item += steep

    if is_valid_args(*args):
        if len(args) == 1:
            return inner_range(start=0, stop=args[0])
        elif len(args) == 2:
            return inner_range(start=args[0], stop=args[1])
        elif len(args) == 3:
            return inner_range(start=args[0], stop=args[1], steep=args[2])
    else:
        return iter(())


if __name__ == '__main__':
    for i in custom_range(5, 10, 2):
        print(i)

    print('--------------')
    for i in custom_range(10, 5, -1):
        print(i)

    print('--------------')
    for i in custom_range(10, 5, None):
        print(i)

    print('--------------')
    for i in custom_range(10, 5, 1):
        print(i)

    print('--------------')
    for i in custom_range(10):
        print(i)

    print('--------------')
    for i in custom_range(10, 5, 1):
        print(i)

    for i in custom_range(1, 10, 2):
        print(i)
