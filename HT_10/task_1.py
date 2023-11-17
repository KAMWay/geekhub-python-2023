# Банкомат 2.0
#     - усі дані зберігаються тільки в sqlite3 базі даних. Більше ніяких файлів. Якщо в попередньому завданні
#       ви добре продумали структуру програми то у вас не виникне проблем швидко адаптувати її до нових вимог.
#     - на старті додати можливість залогінитися або створити новго користувача (при створенні новго користувача,
#       перевіряється відповідність логіну і паролю мінімальним вимогам. Для перевірки створіть окремі функції)
#     - в таблиці (базі) з користувачами має бути створений унікальний користувач-інкасатор, який матиме розширені
#       можливості (домовимось, що логін/пароль будуть admin/admin щоб нам було простіше перевіряти)
#     - банкомат має власний баланс
#     - кількість купюр в банкоматі обмежена. Номінали купюр - 10, 20, 50, 100, 200, 500, 1000
#     - змінювати вручну кількість купюр або подивитися їх залишок в банкоматі може лише інкасатор
#     - користувач через банкомат може покласти на рахунок лише сумму кратну мінімальному номіналу що підтримує
#       банкомат. В іншому випадку - повернути "здачу" (наприклад при поклажі 1005 --> повернути 5). Але це не
#       має впливати на баланс/кількість купюр банкомату, лише збільшуєтсья баланс користувача (моделюємо наявність
#       двох незалежних касет в банкоматі - одна на прийом, інша на видачу)
#     - зняти можна лише в межах власного балансу, але не більше ніж є всього в банкоматі.
#     - при неможливості виконання якоїсь операції - вивести повідомлення з причиною (не вірний логін/пароль,
#     недостатньо коштів на раунку, неможливо видати суму наявними купюрами тощо.)
from pathlib import Path
import sqlite3


class ATMException(Exception):
    pass


BASE_DIR = 'db'
BASE_NAME = 'atm.db'


def get_connection():
    return sqlite3.connect(Path(BASE_DIR, BASE_NAME))


def close_connection(con):
    if con:
        con.close()


def db_get_user(username: str, password: str) -> [int, None]:
    con = None
    try:
        con = get_connection()
        cur = con.cursor()

        sql = "SELECT id FROM users WHERE username=? and password=?"
        cur.execute(sql, (username, password))

        data = cur.fetchone()
        return data[0] if data else None
    except sqlite3.Error:
        raise ATMException("can't login")
    finally:
        close_connection(con)


def db_save_user(username: str, password: str) -> int:
    con = None
    try:
        con = get_connection()
        cur = con.cursor()

        cur.execute("INSERT INTO users (username, password) VALUES (?,?) RETURNING id", (username, password))
        data = cur.fetchone()
        con.commit()

        return data[0]
    except sqlite3.Error:
        raise ATMException('save user exception')
    finally:
        close_connection(con)


def db_get_user_balance(user: int) -> float:
    con = None
    try:
        con = get_connection()
        cur = con.cursor()

        sql = "SELECT balance FROM user_balance WHERE user_id=?"
        cur.execute(sql, (user,))

        data = cur.fetchone()
        return data[0] if data else 0
    except sqlite3.Error:
        raise ATMException('get balance exception')
    finally:
        close_connection(con)


def db_save_user_balance(user: int, balance: [int, float]):
    con = None
    try:
        con = get_connection()
        cur = con.cursor()

        sql = "SELECT user_id FROM user_balance WHERE user_id=?"
        cur.execute(sql, (user,))
        if len(cur.fetchall()) > 0:
            sql = "UPDATE user_balance SET balance=? WHERE user_id=?"
        else:
            sql = "INSERT INTO user_balance (balance, user_id) VALUES (?,?)"
        cur.execute(sql, (balance, user))

        con.commit()
    except sqlite3.Error:
        raise ATMException('save balance exception')
    finally:
        close_connection(con)


def db_get_user_transactions(user: int) -> list[dict]:
    con = None
    try:
        con = get_connection()
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        sql = "SELECT user_id, dt, amount, balance FROM user_transactions WHERE user_id=?"
        cur.execute(sql, (user,))

        rows = cur.fetchall()

        return [{'date': row['dt'], 'amount': row['amount'], 'balance': row['balance']} for row in rows]
    except sqlite3.Error:
        raise ATMException("can't get transactions")
    finally:
        close_connection(con)


def db_save_user_transaction(user: int, amount: [int, float], balance: [int, float]):
    from datetime import datetime
    con = None
    try:
        con = get_connection()
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        sql = "INSERT INTO user_transactions (user_id, dt, amount, balance) VALUES (?, ?, ?, ?)"
        cur.execute(sql, (user, datetime.now(), amount, balance))

        con.commit()
    except sqlite3.Error:
        raise ATMException("can't save transactions")
    finally:
        close_connection(con)


def db_get_banknotes(atm: int = 1) -> list[dict[int:int]]:
    con = None
    try:
        con = get_connection()
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        sql = "SELECT atm_id, denomination, amount FROM atm_banknotes WHERE atm_id=?"
        cur.execute(sql, (atm,))

        rows = cur.fetchall()

        return [{'denomination': row['denomination'], 'amount': row['amount']} for row in rows]
    except sqlite3.Error:
        raise ATMException("can't get banknotes")
    finally:
        close_connection(con)


def db_save_banknotes(denomination: int, amount: int = 0, atm: int = 1):
    con = None
    try:
        con = get_connection()
        cur = con.cursor()

        sql = "SELECT denomination FROM atm_banknotes WHERE denomination=? AND atm_id=?"
        cur.execute(sql, (denomination, atm))
        if len(cur.fetchall()) > 0:
            sql = "UPDATE atm_banknotes SET amount=? WHERE denomination=? AND atm_id=?"
        else:
            sql = "INSERT INTO atm_banknotes (amount, denomination, atm_id) VALUES (?, ?, ?)"
        cur.execute(sql, (amount, denomination, atm))

        con.commit()
    except sqlite3.Error:
        raise ATMException('save banknotes exception')
    finally:
        close_connection(con)


def get_atm_balance(atm: int = 1) -> int:
    return sum(i.get('denomination') * i.get('amount') for i in db_get_banknotes(atm))


def change_user_balance(user: int, amount: [int, float]) -> float:
    user_balance = db_get_user_balance(user)
    if amount < 0 and user_balance < -amount:
        raise ATMException('insufficient user funds')

    atm_balance = get_atm_balance()
    if amount < 0 and atm_balance < -amount:
        raise ATMException('insufficient ATM funds')

    min_banknote = min(get_available_banknotes_denomination())
    back_amount = abs(amount % (min_banknote if amount > 0 else -min_banknote))
    amount = amount - (back_amount if amount > 0 else - back_amount)

    if amount == 0:
        return back_amount

    user_balance += amount
    db_save_user_balance(user, user_balance)
    db_save_user_transaction(user, amount, user_balance)

    return back_amount if amount > 0 else -amount


def is_valid_user(username: str, psw: str) -> bool:
    if not username or not psw:
        raise ATMException("username and password can't be empty")

    return True


def login(username: str, psw: str) -> int:
    return db_get_user(username, psw)


def sign_up(username: str, psw: str) -> int:
    return db_save_user(username, psw)


def get_user() -> int:
    count = 3
    user = None
    while not user:
        print('----Please Sign In/Up----')
        username = input('Enter user name: ')
        password = input('Enter password: ')

        if is_valid_user:
            user = login(username, password)
            if not user and input('User not found. To create this user enter 1:') == '1':
                user = sign_up(username, password)

        if not user and count > 0:
            count -= 1
            print(f'You have {count} attempts. Try again.')
        elif count <= 0:
            raise ATMException("you could not login")

    return user


def get_amount() -> float:
    try:
        amount = float(input('Input amount: '))
        if amount <= 0:
            raise ValueError
        return amount
    except ValueError:
        raise ATMException('incorrect input amount')


def get_available_banknotes_denomination() -> tuple:
    return 10, 20, 50, 100, 200, 500, 1000


def get_banknotes_amount() -> dict[str:int]:
    try:
        banknote = int(input('Input banknotes denomination [10, 20, 50, 100, 200, 500, 1000]: '))
        if banknote not in get_available_banknotes_denomination():
            raise ValueError

        amount = int(input('Input amount: '))
        if amount <= 0:
            raise ValueError

        return {'denomination': banknote, 'amount': int(input('Input amount: '))}
    except ValueError:
        raise ATMException('incorrect input banknotes')


def get_command(user: int) -> int:
    count_commands = 7 if user == 1 else 5
    while True:
        print('----Available ATM commands----')
        print('1. Show total balance')
        print('2. Top-up balance')
        print('3. Deposit money')
        print('4. Transaction history')
        print('5. Exit')

        if (user == 1):
            print('6. Administrator: update banknotes')
            print('7. Administrator: available banknotes')

        print('------------------------')
        try:
            number = int(input(f"Enter command number [1..{count_commands}]:"))
            if 1 <= number <= count_commands:
                return number
            raise ValueError()
        except ValueError:
            print('Incorrect input. Try again.')


def get_command_result(user: int, command: int) -> str:
    if command == 5:
        return 'User exit'

    if command == 1:
        return f'Total deposit: {db_get_user_balance(user)}'

    if command == 2 or command == 3:
        amount = get_amount()
        back_amount = change_user_balance(user, amount if command == 2 else -amount)
        return 'Done' if back_amount == 0 else f'Return {round(back_amount, 2)}'

    if command == 4:
        str_generator = ('Date {} Amount: {}'.format(item.get('date'), item.get('amount'))
                         for item in db_get_user_transactions(user))
        return '\n'.join(str_generator)

    if user == 1 and command == 6:
        banknote = get_banknotes_amount()
        db_save_banknotes(banknote.get('denomination'), banknote.get('amount'))
        return 'Done'

    if user == 1 and command == 7:
        str_generator = (f"Denomination {item.get('denomination')} Amount: {item.get('amount')}"
                         for item in db_get_banknotes())
        return '\n'.join(str_generator)


def start():
    user = None

    try:
        user = get_user()
    except ATMException as e:
        print(f'Login exception: {e}')

    command = None
    while user and (not command or command != 5):
        command = get_command(user)
        try:
            print('- - - - - - - - - - - -')
            print(get_command_result(user, command))
            print('- - - - - - - - - - - -')
            print()
        except ATMException as e:
            print(f'Command exception: {e}')

    print('Program complete')


if __name__ == '__main__':
    start()
