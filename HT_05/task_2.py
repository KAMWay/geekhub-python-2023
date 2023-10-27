# Створiть 3 рiзних функцiї (на ваш вибiр). Кожна з цих функцiй повинна повертати якийсь результат
# (напр. інпут від юзера, результат математичної операції тощо). Також створiть четверту ф-цiю, яка всередині
# викликає 3 попереднi, обробляє їх результат та також повертає результат своєї роботи. Таким чином ми будемо
# викликати одну (четверту) функцiю, а вона в своєму тiлi - ще 3.

def to_number(value):
    try:
        try:
            return int(value)
        except ValueError:
            return float(value)
    except ValueError:
        return None


def is_positive(number):
    return isinstance(number, (float, int)) and number > 0


def get_values_from_console():
    while True:
        _values = input("Enter values (separated ','): ").split(',')
        if len(_values) > 0:
            return _values
        else:
            print('Must be enter not empty values. Try again.')


def get_positive_numbers_sum():
    values = get_values_from_console()
    positive_numbers = list(filter(is_positive, map(to_number, values)))
    print(f'Sum of positive numbers is {sum(positive_numbers)}')


if __name__ == '__main__':
    get_positive_numbers_sum()
