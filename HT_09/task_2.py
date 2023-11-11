# 2. Написати функцію, яка приймає два параметри: ім'я (шлях) файлу та кількість символів. Файл також додайте в
# репозиторій. На екран повинен вивестись список із трьома блоками - символи з початку, із середини та з кінця файлу.
#
# Кількість символів в блоках - та, яка введена в другому параметрі.
#
# Придумайте самі, як обробляти помилку, наприклад, коли кількість символів більша, ніж є в файлі або, наприклад,
# файл із двох символів і треба вивести по одному символу, то що виводити на місці середнього блоку символів?).
#
# Не забудьте додати перевірку чи файл існує.

class ValidateException(Exception):
    pass


def positions_generator(number: int, max_number: int):
    if number <= 0 or max_number <= 0:
        raise ValidateException('number of characters must be positive')

    if number > max_number:
        raise ValidateException('the number is greater than the maximum possible')

    if number * 3 > max_number:
        raise ValidateException('the number of characters is too small')

    yield 0
    yield int((max_number - number) / 2)
    yield max_number - number


def print_file(path: str, count: int):
    try:
        with open(path) as f:
            for position in positions_generator(count, sum((len(l) for l in f))):
                f.seek(position)
                print(f'{f.read(count):<{count}s}', end=' ')
    except FileNotFoundError:
        print('file not found')
    except ValidateException as e:
        print(e)


if __name__ == '__main__':
    print_file('task_2.txt', 1)

# 3. Програма-банкомат.
#    Використувуючи функції створити програму з наступним функціоналом:
#       - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.CSV>);
#       - кожен з користувачів має свій поточний баланс (файл <{username}_balance.TXT>) та історію транзакцій
#         (файл <{username_transactions.JSON>);
#       - є можливість як вносити гроші, так і знімати їх. Обов'язкова перевірка введених даних (введено цифри;
#         знімається не більше, ніж є на рахунку і т.д.).
#    Особливості реалізації:
#       - файл з балансом - оновлюється кожен раз при зміні балансу (містить просто цифру з балансом);
#       - файл - транзакціями - кожна транзакція у вигляді JSON рядка додається в кінець файла;
#       - файл з користувачами: тільки читається. Але якщо захочете реалізувати функціонал додавання нового
#         користувача - не стримуйте себе :)
#    Особливості функціонала:
#       - за кожен функціонал відповідає окрема функція;
#       - основна функція - <start()> - буде в собі містити весь workflow банкомата:
#       - на початку роботи - логін користувача (програма запитує ім'я/пароль). Якщо вони неправильні - вивести
#         повідомлення про це і закінчити роботу (хочете - зробіть 3 спроби, а потім вже закінчити роботу -
#         все на ентузіазмі :))
#       - потім - елементарне меню типн:
#         Введіть дію:
#            1. Продивитись баланс
#            2. Поповнити баланс
#            3. Вихід
#       - далі - фантазія і креатив, можете розширювати функціонал, але основне завдання має бути повністю реалізоване :)
#     P.S. Увага! Файли мають бути саме вказаних форматів (csv, txt, json відповідно)
#     P.S.S. Добре продумайте структуру програми та функцій (edited)