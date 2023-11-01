# 2. Написати функцію <bank> , яка працює за наступною логікою: користувач робить вклад у розмірі <a> одиниць
# строком на <years> років під <percents> відсотків (кожен рік сума вкладу збільшується на цей відсоток,
# ці гроші додаються до суми вкладу і в наступному році на них також нараховуються відсотки).
# Параметр <percents> є необов'язковим і має значення по замовчуванню <10> (10%). Функція повинна принтануть суму,
# яка буде на рахунку, а також її повернути (але округлену до копійок).

def positive(func):
    def wrapper(*args, **kwargs):
        number = func(*args, **kwargs)

        if not number:
            return None

        if number > 0:
            return number
        else:
            print(f"The number must be positive. Try again.")

    return wrapper


@positive
def get_positive_number(number) -> int or float:
    try:
        try:
            return int(number)
        except ValueError:
            return float(number)
    except ValueError:
        print(f"{number} is not number. Try again.")


def get_positive_number_from_console(msg: str) -> int or float:
    positive_number = None

    while not positive_number:
        positive_number = get_positive_number(input(msg))

    return positive_number


def repeat_bank_decorator(func):
    def wrapper(amount: int or float, years: int or float, percents: int or float):
        while years > 0:
            amount = func(amount, years, (percents if years > 1 else percents * years))
            years -= 1
        return amount

    return wrapper


@repeat_bank_decorator
def bank(amount: int or float, years: int or float, percents: int or float = 10) -> int or float:
    amount = amount + amount * percents / 100

    if years - 1 <= 0:
        print(f'Total amount: {amount}')

    return round(amount, 2)


if __name__ == '__main__':
    amount_deposit = get_positive_number_from_console('Enter amount deposit: ')
    number_years = get_positive_number_from_console('Enter the number of years: ')
    number_percents = get_positive_number_from_console('Enter the number of percents: ')

    print(bank(amount_deposit, number_years, number_percents))
