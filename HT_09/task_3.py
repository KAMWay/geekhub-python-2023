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

class ATMException(Exception):
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
    except Exception:
        raise ATMException(f"can't save {path}")


def read_json(path: str) -> list[dict]:
    import json
    try:
        with open(path) as f:
            for data in json.load(f):
                yield data
    except FileNotFoundError:
        return iter(())


def save_json(path: str, data):
    import json

    file_date = list(read_json(path))
    file_date.append(data)

    data = json.dumps(file_date, indent=2)
    save_txt(path, data)


def save_balance(user: str, balance: [int, float]):
    save_txt(f'{user}_balance.txt', balance)


def get_transactions(user: str) -> list[dict]:
    return list(read_json(f'{user}_transactions.json'))


def save_transaction(user: str, amount: [int, float], balance: [int, float]):
    from datetime import datetime
    data = {'user': user, 'date': str(datetime.now()), 'amount': amount, 'balance': balance}
    save_json(f'{user}_transactions.json', data)


def change_balance(user: str, amount: [int, float]):
    balance = get_balance(user)
    if amount < 0 and balance < -amount:
        raise ATMException('insufficient funds')

    balance += amount
    save_balance(user, balance)
    save_transaction(user, amount, balance)


def get_balance(user: str) -> float:
    try:
        return float(next(read_txt(f'{user}_balance.txt')))
    except TypeError:
        raise ATMException("can't get balance")
    except StopIteration:
        return 0


def is_valid_user(username: str, psw: str) -> bool:
    if not username or not psw:
        raise ATMException("username and password can't be empty")

    return True


def login(username: str, psw: str) -> bool:
    users = read_csv()
    if is_valid_user and users:
        return any(filter(lambda u: u.get('username') == username and u.get('password') == psw, users))
    else:
        return False


def get_user() -> str:
    count = 3
    while True:
        username = input('Enter user name: ')
        password = input('Enter password: ')

        try:
            if is_valid_user(username, password) and login(username, password):
                return username
        except ATMException as e:
            print(f'Login exception: {e}')

        if count > 0:
            count -= 1
            print(f'You have {count} attempts. Try again.')
        else:
            raise ATMException('you could not login')


def get_amount() -> float:
    try:
        amount = float(input('Input amount: '))
        if amount <= 0:
            raise ValueError
        return amount
    except ValueError:
        raise ATMException('incorrect input amount.')


def get_command() -> int:
    while True:
        print('------------------------')
        print('Available ATM commands:')
        print('1. Show total balance')
        print('2. Top-up balance')
        print('3. Deposit money')
        print('4. Transaction history')
        print('5. Exit')
        print('------------------------')
        try:
            number = int(input('Enter command number [1..5]:'))
            if 1 <= number <= 5:
                return number
            raise ValueError()
        except ValueError:
            print('Incorrect input. Try again.')


def get_command_result(user: str, command: int) -> str:
    if command == 5:
        return 'User exit'

    if command == 1:
        return f'Total deposit: {get_balance(user)}'

    if command == 2 or command == 3:
        amount = get_amount()
        change_balance(user, amount if command == 2 else -amount)
        return 'Done'

    if command == 4:
        str_generator = ('Date {} Amount: {}'.format(item.get('date'), item.get('amount')) for item in
                         get_transactions(user))
        return '\n'.join(str_generator)


def start():
    user = None
    try:
        user = get_user()
    except ATMException as e:
        print(f'Login exception: {e}')

    command = None
    while user and (not command or command != 5):
        command = get_command()
        try:
            print(get_command_result(user, command))
        except ATMException as e:
            print(f'Command exception: {e}')

    print('Program complete')


if __name__ == '__main__':
    start()
