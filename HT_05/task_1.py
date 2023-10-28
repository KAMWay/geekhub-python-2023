# Написати функцiю season, яка приймає один аргумент (номер мiсяця вiд 1 до 12) та яка буде повертати пору року,
# якiй цей мiсяць належить (зима, весна, лiто або осiнь). У випадку некоректного введеного значення - виводити
# відповідне повідомлення.

def season(month_int: int) -> str:
    if 1 > month_int or month_int > 12:
        return 'Month number must be in range [1..12]'
    elif 3 <= month_int <= 5:
        return 'spring'
    elif 6 <= month_int <= 8:
        return 'summer'
    elif 9 <= month_int < 11:
        return 'fall(autumn)'
    else:
        return "winter"


def get_from_console():
    while True:
        number = input('Enter number of month [1-12]: ')
        try:
            return int(number)
        except ValueError:
            print(f"{number} can't be the number of month. Try again.")


if __name__ == '__main__':
    month = get_from_console()
    print(season(month))
