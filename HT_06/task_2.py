# 2. Написати функцію <bank> , яка працює за наступною логікою: користувач робить вклад у розмірі <a> одиниць
# строком на <years> років під <percents> відсотків (кожен рік сума вкладу збільшується на цей відсоток,
# ці гроші додаються до суми вкладу і в наступному році на них також нараховуються відсотки).
# Параметр <percents> є необов'язковим і має значення по замовчуванню <10> (10%). Функція повинна принтануть суму,
# яка буде на рахунку, а також її повернути (але округлену до копійок).

def to_number(value):
    try:
        try:
            return int(value)
        except ValueError:
            return float(value)
    except ValueError:
        return None


def get_from_console(msg: str) -> int or float:
    while True:
        _values = to_number(input(msg))
        if _values and _values >= 0:
            return _values
        else:
            print('Not valid input. Try again.')


def bank(amount: int or float, years: int or float, percents: int or float = 10) -> float:
    _total = amount
    for year in range(int(years)):
        _total += _total * percents / 100
    _total += amount * percents * (years % 1) / 100

    print(f'Total amount: {_total}')

    return round(_total, 2)


if __name__ == '__main__':
    amount = get_from_console('Enter amount deposit: ')
    years = get_from_console('Enter the number of years: ')
    percents = get_from_console('Enter the number of percents: ')

    print(bank(amount, years, percents))
