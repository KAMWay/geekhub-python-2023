# Користувач вводить змiннi "x" та "y" з довiльними цифровими значеннями. Створiть просту умовну конструкцiю
# (звiсно вона повинна бути в тiлi ф-цiї), пiд час виконання якої буде перевiрятися рiвнiсть змiнних "x" та "y"
# та у випадку нервіності - виводити ще і різницю.
#     Повиннi опрацювати такi умови (x, y, z заміність на відповідні числа):
#     x > y;       вiдповiдь - "х бiльше нiж у на z"
#     x < y;       вiдповiдь - "у бiльше нiж х на z"
#     x == y.      вiдповiдь - "х дорiвнює z"


def to_number(value):
    try:
        try:
            return int(value)
        except ValueError:
            return float(value)
    except ValueError:
        return None


def compare_two_numbers(o1, o2):
    number1 = to_number(o1)
    number2 = to_number(o2)

    if not isinstance(number1, (int, float)) or not isinstance(number2, (int, float)):
        print(f"Can't compare {o1} and {o2}")
    elif number1 == number2:
        print(f'{number1} equal {number2}')
    else:
        print(f'{max(number1, number2)} more then {min(number1, number2)}')


if __name__ == '__main__':
    x, y = input("Enter x and y (separated ' '): ").split()[:2]
    compare_two_numbers(x, y)