# Реалізуйте генератор, який приймає на вхід будь-яку ітерабельну послідовність (рядок, список, кортеж)
# і повертає генератор, який буде вертати значення з цієї послідовності, при цьому, якщо було повернено
# останній елемент із послідовності - ітерація починається знову.
#    Приклад (якщо запустили його у себе - натисніть Ctrl+C ;) ):
#    for elem in generator([1, 2, 3]):
#        print(elem)
#    1
#    2
#    3
#    1
#    2
#    3
#    1
#    .......
def generator(sequence) -> iter:
    try:
        _it = iter(sequence)
    except TypeError:
        return iter(())

    while True:
        try:
            yield next(_it)
        except StopIteration:
            _it = iter(sequence)


if __name__ == '__main__':
    for elem in generator([1, 2, 3]):
        print(elem)
