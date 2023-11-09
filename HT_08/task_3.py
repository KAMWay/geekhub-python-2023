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


def custom_range(start: int, stop: int, steep: int = 1) -> iter:
    if steep == 0:
        raise ValueError('range steep is zero')

    if start > stop and steep > 0:
        return iter(())

    item = start
    ind = 1 if steep > 0 else -1
    while item * ind < stop * ind:
        yield item
        item += steep


if __name__ == '__main__':
    print(f'Test1: {list(custom_range(5, 10)) == [5, 6, 7, 8, 9]}')
    print(f'Test2: {list(custom_range(10, 5, -1)) == [10, 9, 8, 7, 6]}')

    print(f'Test4: {list(custom_range(0, 10, 50)) == [0]}')
    print(f'Test5: {list(custom_range(10, 5)) == []}')

    print(f'Test6: {list(custom_range(5, 10, 3)) == [5, 8]}')
    print(f'Test7: {list(custom_range(10, 5, -4)) == [10, 6]}')

    try:
        list(custom_range(10, 5, 0))
    except ValueError as e:
        print(f'Test8: ValueError -> {e}')
