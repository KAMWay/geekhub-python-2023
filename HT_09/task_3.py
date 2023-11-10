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
class ValidateException(Exception):
    pass


class OperationException(Exception):
    pass


def read_csv(path: str = 'user.csv', delimiter: str = ';', fieldnames: list = ('username', 'password')):
    import csv
    try:
        with open(path) as f:
            reader = csv.DictReader(f, delimiter=delimiter, fieldnames=fieldnames)
            next(reader)
            for row in reader:
                yield row
    except FileNotFoundError:
        return iter(())


def read_txt(path: str):
    try:
        with open(path) as f:
            for line in f:
                yield line.strip()
    except FileNotFoundError:
        return iter(())


def save_txt(path: str, data: str):
    try:
        with open(path, 'w') as f:
            f.write(str(data))

    except FileNotFoundError:
        return iter(())


def read_json(path: str):
    import json
    try:
        with open(path) as f:
            for data in json.load(f):
                yield data
    except FileNotFoundError:
        return iter(())


def save_json(path: str, data):
    import json
    file_data = list(read_json(path))
    try:
        with open(path, 'w') as f:
            file_data.append(data)
            data = json.dumps(file_data, indent=2)
            f.write(data)
            # json.dump(file_data, f, indent=2)
    except FileNotFoundError:
        return iter(())


def is_valid_user(username: str, psw: str) -> bool:
    if not username or not psw:
        raise ValidateException("username and password can't be empty")

    return True


def login(username: str, psw: str) -> bool:
    users = read_csv()
    if is_valid_user and users:
        return any(filter(lambda u: u.get('username') == username and u.get('password') == psw, users))
    else:
        return False


def user_balance(user: str) -> float:
    try:
        return float(next(read_txt(f'{user}_balance.txt')))
    except (TypeError, StopIteration):
        return 0


def save_balance(user: str, balance: [int, float]):
    save_txt(f'{user}_balance.txt', balance)


def save_transaction_log(user: str, amount: [int, float], balance: [int, float]):
    from datetime import datetime
    save_json(f'{user}_transactions.json',
              {'user': user, 'date': str(datetime.now()), 'amount': amount, 'balance': balance})


def do_transaction(user: str, amount: [int, float]):
    balance = user_balance(user)
    if amount < 0 and balance < -amount:
        raise OperationException('insufficient funds')

    balance += amount
    save_balance(user, balance)
    save_transaction_log(user, amount, balance)


if __name__ == '__main__':
    print(login('user1', 'paswd1'))
    print(login('user1', 'paswd2'))

    do_transaction('user1', 230)
    do_transaction('user1', -150)

    # users_transaction('user1', 'user2', 50)

    # save_json('aaa.json', {'name': 'bbb', 'pass': 'pass2'})

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
