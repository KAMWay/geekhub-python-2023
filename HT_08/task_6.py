# Напишіть функцію,яка прймає рядок з декількох слів і повертає довжину найкоротшого слова.
# Реалізуйте обчислення за допомогою генератора.


def words_len_iterator_1(str_value: str) -> iter:
    _count = 0
    _it = iter(str_value)
    _ch = next(_it, None)

    while _ch:
        if _ch == ' ':
            if _count > 0:
                yield _count
            _count = 0
        else:
            _count += 1
        _ch = next(_it, None)

    if _count > 0:
        yield _count


def words_len_iterator_2(str_value: str) -> iter:
    _count = 0
    for ch in str_value:
        if ch == ' ':
            if _count > 0:
                yield _count
            _count = 0
        else:
            _count += 1

    if _count > 0:
        yield _count


def get_min_words_len(str_value: str) -> int:
    def words_len_iterator() -> iter:
        for word in str_value.split(' '):
            if len(word) > 0:
                yield len(word)

    return min(words_len_iterator())


if __name__ == '__main__':
    print(get_min_words_len('fdh hdfhhh  kk  gfff'))
