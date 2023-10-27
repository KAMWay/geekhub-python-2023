# Написати функцiю season, яка приймає один аргумент (номер мiсяця вiд 1 до 12) та яка буде повертати пору року,
# якiй цей мiсяць належить (зима, весна, лiто або осiнь). У випадку некоректного введеного значення - виводити
# відповідне повідомлення.

def season(month: int) -> str:
    if 0 > month or month > 12:
        return 'Month value must be in range [1..12]'
    elif 3 <= month <= 5:
        return 'spring'
    elif 6 <= month <= 8:
        return 'summer'
    elif 9 <= month < 11:
        return 'fall(autumn)'
    else:
        return "winter"


season(1)

if __name__ == '__main__':
    print(season(1))
    print(season(10))
    print(season(-1))
    print(season(15))
