# Напишіть функцію,яка прймає рядок з декількох слів і повертає довжину найкоротшого слова.
# Реалізуйте обчислення за допомогою генератора.

def get_min_words_len(str_value: str) -> int:
    if len(str_value) == 0:
        return 0

    words_generator = (word for word in str_value.split(' '))
    word = next(words_generator, None)
    min_len = 0
    while word is not None:
        if len(word) > 0:
            if min_len == 0 or len(word) < min_len:
                min_len = len(word)
        word = next(words_generator, None)

    return min_len


if __name__ == '__main__':
    print(get_min_words_len('fdh hdfhhh  kkdd  sg fff'))
