# Напишіть функцію,яка приймає на вхід рядок та повертає кількість окремих регістро-незалежних букв та цифр, які
# зустрічаються в рядку більше ніж 1 раз. Рядок буде складатися лише з цифр та букв (великих і малих).
# Реалізуйте обчислення за допомогою генератора.

#     Example (input string -> result):
#     "abcde" -> 0            # немає символів, що повторюються
#     "aabbcde" -> 2          # 'a' та 'b'
#     "aabBcde" -> 2          # 'a' присутнє двічі і 'b' двічі (`b` та `B`)
#     "indivisibility" -> 1   # 'i' присутнє 6 разів
#     "Indivisibilities" -> 2 # 'i' присутнє 7 разів та 's' двічі
#     "aA11" -> 2             # 'a' і '1'
#     "ABBA" -> 2             # 'A' і 'B' кожна двічі


def get_repeatable_count(str_value: str) -> int:
    str_value_lower = str_value.lower()

    ch_generator = (ch for ch in set(str_value_lower))
    ch = next(ch_generator, None)
    count = 0
    while ch:
        if str_value_lower.count(ch) > 1:
            count += 1
        ch = next(ch_generator, None)

    return count


if __name__ == '__main__':
    print(get_repeatable_count('abcde'))
    print(get_repeatable_count('aabbcde'))
    print(get_repeatable_count('aabBcde'))
    print(get_repeatable_count('indivisibility'))
    print(get_repeatable_count('Indivisibilities'))
    print(get_repeatable_count('aA11'))
    print(get_repeatable_count('ABBA'))
