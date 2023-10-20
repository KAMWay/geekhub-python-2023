# Користувачем вводиться початковий і кінцевий рік. Створити цикл, який виведе всі високосні роки в цьому проміжку
# (границі включно). P.S. Рік є високосним, якщо він кратний 4, але не кратний 100, а також якщо він кратний 400.

initial_year = int(input("Input initial year: "))
final_year = int(input("Input final year: "))
for year in range(initial_year, final_year + 1, 4):
    if ((year % 4 == 0) and (year % 100 != 0)) or ((year % 400 == 0) and (year % 100 == 0)):
        print(f'{year} year is leap')
