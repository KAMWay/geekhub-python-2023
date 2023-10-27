# Наприклад маємо рядок
#    --> "f98neroi4nr0c3n30irn03ien3c0rfe  kdno400wenwkowe00koijn35pijnp46ij7k5j78p3kj546p4 65jnpoj35po6j345"
#    просто потицяв по клавi =)
# Створіть ф-цiю, яка буде отримувати рядки на зразок цього та яка оброблює наступні випадки:
#    -  якщо довжина рядка в діапазонi 30-50 (включно) -> прiнтує довжину рядка, кiлькiсть букв та цифр
#    -  якщо довжина менше 30 -> прiнтує суму всiх чисел та окремо рядок без цифр лише з буквами (без пробілів)
#    -  якщо довжина більше 50 -> щось вигадайте самі, проявіть фантазію =)

from functools import reduce


def print_string_info1(in_str: str):
    print(f'String length  is {len(in_str)}')

    _char_count = sum(ch.isalpha() for ch in in_str)
    print(f'Count of chars: {_char_count}')

    _digit_count = sum(ch.isdigit() for ch in in_str)
    print(f'Count of digit: {_digit_count}')


def print_string_info2(in_str: str):
    _char_string = ''.join(filter(lambda ch: ch.isalpha(), list(in_str)))
    print(f'Chars in string: {_char_string}')

    _digits_sum = sum(map(int, filter(lambda ch: ch.isdigit(), list(in_str))))
    print(f'Digits sum: {_digits_sum}')


def print_string_info3(in_str: str):
    _char_max = max(in_str, key=lambda x: in_str.count(x))
    print(f"Maximum frequency character is ['{_char_max}':{in_str.count(_char_max)}]")

    _digit_min = reduce(lambda d1, d2: d1 if d1 > d2 else d2, map(int, (filter(lambda ch: ch.isdigit(), in_str))))
    print(f'Maximum digit is {_digit_min}')


def get_string_info(in_str: str):
    str_len = len(in_str)
    if str_len < 30:
        print_string_info2(in_str)
    elif str_len > 50:
        print_string_info3(in_str)
    else:
        print_string_info1(in_str)


if __name__ == '__main__':
    string = input("Enter string: ")
    get_string_info(string)
