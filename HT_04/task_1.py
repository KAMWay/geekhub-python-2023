# Написати скрипт, який приймає від користувача два числа (int або float) і робить наступне:
#   - Кожне введене значення спочатку пробує перевести в int. У разі помилки - пробує перевести в float,
#     а якщо і там ловить помилку - пропонує ввести значення ще раз (зручніше на даному етапі навчання для цього
#     використати цикл while)
#   - Виводить результат ділення першого на друге. Якщо при цьому виникає помилка - оброблює її і виводить відповідне
#     повідомлення

def get_number_from_console(console_msg):
    while True:
        number = input(console_msg)
        try:
            try:
                return int(number)
            except ValueError:
                return float(number)
        except ValueError:
            print(f'{number} is not number')


def get_division(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Can't division by zero")


a = get_number_from_console('Enter number a: ')
b = get_number_from_console('Enter number b: ')
print(f'Result of division: {get_division(a, b)}')
