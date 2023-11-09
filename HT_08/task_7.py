# Напишіть функцію, яка приймає 2 списки. Результатом має бути новий список, в якому знаходяться елементи
# першого списку, яких немає в другому. Порядок елементів, що залишилися має відповідати порядку
# в першому (оригінальному) списку. Реалізуйте обчислення за допомогою генератора.
#     Приклад:
#     array_diff([1, 2], [1]) --> [2]
#     array_diff([1, 2, 2, 2, 4, 3, 4], [2]) --> [1, 4, 3, 4]


def array_diff(items1: list, items2: list) -> list:
    if len(items2) == 0:
        return items1.copy()
    if len(items1) == 0:
        return []

    items = []
    items1_generator = (item for item in items1)
    while True:
        try:
            item = next(items1_generator)
        except StopIteration:
            return items

        if item not in items2:
            items.append(item)


if __name__ == '__main__':
    print(array_diff([1, 2], []))
    print(array_diff([1, 2], [1]))
    print(array_diff([1, 2, 2, 2, 4, 3, 4], [2]))
