# Банкомат 2.0: переробіть программу з функціонального підходу програмування на використання класів.
# Додайте шанс 10% отримати бонус на баланс при створенні нового користувача.
import sqlite3


class ATMException(Exception):
    pass


class Connection:
    @staticmethod
    def get_connection():
        from pathlib import Path
        return sqlite3.connect(Path('db', 'atm.db'))

    @staticmethod
    def close_connection(con):
        if con:
            con.close()


class ConsoleReader:
    @staticmethod
    def get_username_and_password() -> [str, str]:
        print('----Please Sign In/Up----')
        username = input('Enter user name: ')
        password = input('Enter password: ')
        return username, password

    @staticmethod
    def get_amount() -> float:
        try:
            amount = float(input('Input amount: '))
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            raise ATMException('incorrect input amount')

    @staticmethod
    def get_banknotes_amount() -> dict[str:int]:
        try:
            banknote = int(input('Input banknotes denomination [10, 20, 50, 100, 200, 500, 1000]: '))
            if banknote not in ATMService.get_available_denomination():
                raise ValueError

            amount = int(input('Input amount: '))
            if amount < 0:
                raise ValueError

            return {'denomination': banknote, 'amount': amount}
        except ValueError:
            raise ATMException('incorrect input banknotes')

    @staticmethod
    def get_command_from_console(is_admin: bool) -> int:
        count_commands = 8 if is_admin else 6
        while True:
            print('----Available ATM commands----')
            print('1. Show total user deposit')
            print('2. Show total ATM deposit')
            print('3. Top-up balance')
            print('4. Deposit money')
            print('5. Transaction history')
            print('6. Exit')

            if is_admin:
                print('7. Administrator: update banknotes')
                print('8. Administrator: available banknotes')

            print('------------------------')
            try:
                number = int(input(f"Enter command number [1..{count_commands}]:"))
                if 1 <= number <= count_commands:
                    return number
                raise ValueError()
            except ValueError:
                print('Incorrect input. Try again.')


class User:
    def __init__(self, id):
        self.id = id


class UserService:
    def __init__(self):
        self.__user_repository = UserRepository()

    @staticmethod
    def __is_valid(username: str, psw: str) -> bool:
        if not username or not psw:
            raise ATMException("username and password can't be empty")
        return True

    def login(self, username: str, password: str) -> User:
        if self.__is_valid(username, password):
            return self.__user_repository.get_by_username_and_password(username, password)

    def sign_up(self, username: str, password: str) -> User:
        if self.__is_valid(username, password):
            return self.__user_repository.create(username, password)


class UserBalanceService:
    def __init__(self):
        self.__user_balance_repository = UserBalanceRepository()

    def get(self, user: int) -> float:
        user_balance = self.__user_balance_repository.get_by_user_id(user)
        return user_balance if user_balance else 0

    def save(self, user: int, amount: [int, float]):
        if self.__user_balance_repository.get_by_user_id(user):
            self.__user_balance_repository.update(user, amount)
        else:
            self.__user_balance_repository.insert(user, amount)


class UserTransactionService:
    def __init__(self):
        self.__user_transaction_repository = UserTransactionRepository()

    def get_all(self, user: int) -> list[dict]:
        return self.__user_transaction_repository.get_all_by_user_id(user)

    def save(self, user: int, amount: [int, float], balance: [int, float]):
        self.__user_transaction_repository.insert(user, amount, balance)


class ATMBanknoteService:
    def __init__(self):
        self.__banknote_repository = ATMBanknoteRepository()

    def save(self, denomination: int, amount: int = 0, atm: int = 1):
        if self.__banknote_repository.get_by_denomination(denomination):
            self.__banknote_repository.update(denomination, amount, atm)
        else:
            self.__banknote_repository.insert(denomination, amount, atm)

    def get_all(self, atm: int = 1) -> list[dict]:
        return self.__banknote_repository.get_all(atm)


class UserRepository:

    def get_by_username_and_password(self, username: str, password: str) -> [User, None]:
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()

            sql = "SELECT id FROM users WHERE username=? and password=?"
            cur.execute(sql, (username, password))

            data = cur.fetchone()
            if data:
                return User(data[0])
        except sqlite3.Error:
            raise ATMException("can't login")
        finally:
            Connection.close_connection(con)

    def create(self, username: str, password: str) -> User:
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()

            cur.execute("INSERT INTO users (username, password) VALUES (?,?) RETURNING id", (username, password))
            data = cur.fetchone()
            con.commit()

            return User(data[0])
        except sqlite3.Error:
            raise ATMException('save user exception')
        finally:
            Connection.close_connection(con)


class UserBalanceRepository:
    def get_by_user_id(self, user: int) -> float:
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()

            sql = "SELECT balance FROM user_balance WHERE user_id=?"
            cur.execute(sql, (user,))

            data = cur.fetchone()
            if data:
                return data[0]
        except sqlite3.Error:
            raise ATMException('get balance exception')
        finally:
            Connection.close_connection(con)

    def update(self, user: int, balance: [int, float]):
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()
            cur.execute("UPDATE user_balance SET balance=? WHERE user_id=?",
                        (balance, user))
            con.commit()
        except sqlite3.Error:
            raise ATMException('save balance exception')
        finally:
            Connection.close_connection(con)

    def insert(self, user: int, balance: [int, float]):
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()
            cur.execute("INSERT INTO user_balance (balance, user_id) VALUES (?,?)",
                        (balance, user))
            con.commit()
        except sqlite3.Error:
            raise ATMException('save balance exception')

        finally:
            Connection.close_connection(con)


class UserTransactionRepository:
    def get_all_by_user_id(self, user: int) -> list[dict]:
        con = None
        try:
            con = Connection.get_connection()
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            sql = "SELECT user_id, dt, amount, balance FROM user_transactions WHERE user_id=?"
            cur.execute(sql, (user,))

            rows = cur.fetchall()

            return [{'date': row['dt'], 'amount': row['amount'], 'balance': row['balance']} for row in rows]
        except sqlite3.Error:
            raise ATMException("can't get transactions")
        finally:
            Connection.close_connection(con)

    def insert(self, user: int, amount: [int, float], balance: [int, float]):
        from datetime import datetime
        con = None
        try:
            con = Connection.get_connection()
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            sql = "INSERT INTO user_transactions (user_id, dt, amount, balance) VALUES (?, ?, ?, ?)"
            cur.execute(sql, (user, datetime.now(), amount, balance))

            con.commit()
        except sqlite3.Error:
            raise ATMException("can't save transactions")
        finally:
            Connection.close_connection(con)


class ATMBanknoteRepository:
    def get_all(self, atm: int = 1) -> list[dict]:
        con = None
        try:
            con = Connection.get_connection()
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            sql = "SELECT atm_id, denomination, amount FROM atm_banknotes WHERE atm_id=?"
            cur.execute(sql, (atm,))

            rows = cur.fetchall()

            return [{'denomination': row['denomination'], 'amount': row['amount']} for row in rows]
        except sqlite3.Error:
            raise ATMException("can't get banknotes")
        finally:
            Connection.close_connection(con)

    def get_by_denomination(self, denomination: int, atm: int = 1) -> dict:
        con = None
        try:
            con = Connection.get_connection()
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            sql = "SELECT atm_id, denomination, amount FROM atm_banknotes WHERE denomination=? AND atm_id=?"
            cur.execute(sql, (denomination, atm))

            row = cur.fetchone()

            if row:
                return {'denomination': row['denomination'], 'amount': row['amount']}
        except sqlite3.Error:
            raise ATMException('save banknotes exception')
        finally:
            Connection.close_connection(con)

    def update(self, denomination: int, amount: int = 0, atm: int = 1):
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()

            cur.execute("UPDATE atm_banknotes SET amount=? WHERE denomination=? AND atm_id=?",
                        (amount, denomination, atm))

            con.commit()
        except sqlite3.Error:
            raise ATMException('save banknotes exception')
        finally:
            Connection.close_connection(con)

    def insert(self, denomination: int, amount: int = 0, atm: int = 1):
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()

            cur.execute("INSERT INTO atm_banknotes (amount, denomination, atm_id) VALUES (?, ?, ?)",
                        (amount, denomination, atm))

            con.commit()
        except sqlite3.Error:
            raise ATMException('save banknotes exception')
        finally:
            Connection.close_connection(con)


class ATMService:
    def __init__(self):
        self.__banknote_service = ATMBanknoteService()
        self.__user_balance_service = UserBalanceService()
        self.__user_transaction_service = UserTransactionService()

    def __save_banknote(self, denomination: int, amount: int = 0, atm: int = 1):
        self.__banknote_service.save(denomination, amount, atm)

    def __get_atm_balance(self, atm: int = 1) -> int:
        return sum(i.get('denomination') * i.get('amount') for i in self.__banknote_service.get_all(atm))

    def __get_bonus_percent(self, user: int, bonus_size: int = 10) -> float:
        from random import randrange
        if len(self.__user_transaction_service.get_all(user)) != 0:
            return 0

        return bonus_size / 100 if not randrange(0, 9, 1) else 0

    def __change_user_balance(self, user: int, amount: [int, float], atm: int = 1) -> float:
        user_balance = self.__user_balance_service.get(user)

        if amount < 0 and user_balance < -amount:
            raise ATMException('insufficient user funds')

        atm_balance = self.__get_atm_balance(atm)
        if amount < 0 and atm_balance < -amount:
            raise ATMException('insufficient ATM funds')

        min_banknote = min(self.get_available_denomination())
        back_amount = abs(amount % (min_banknote if amount > 0 else -min_banknote))
        amount = amount - (back_amount if amount > 0 else - back_amount)

        if amount == 0:
            return back_amount

        amount += amount * self.__get_bonus_percent(user) if amount > 0 else 0
        user_balance += amount

        self.__user_balance_service.save(user, user_balance)
        self.__user_transaction_service.save(user, amount, user_balance)

        return back_amount if amount > 0 else -amount

    def __get_user_transactions(self, user: int):
        return self.__user_transaction_service.get_all(user)

    def get_command_result(self, user: User, command: int, atm: int = 1) -> str:
        if command == 6:
            return 'User exit'

        if command == 1:
            return f'Total user deposit: {self.__user_balance_service.get(user.id)}'

        if command == 2:
            return f'Total ATM deposit: {self.__get_atm_balance(atm)}'

        if command == 3 or command == 4:
            amount = ConsoleReader.get_amount()
            back_amount = self.__change_user_balance(user.id, amount if command == 3 else -amount)
            return 'Done' if back_amount == 0 else f'Return {round(back_amount, 2)}'

        if command == 5:
            str_generator = ('Date {} Amount: {}'.format(item.get('date'), item.get('amount'))
                             for item in self.__get_user_transactions(user.id))
            return '\n'.join(str_generator)

        if user.id == 1 and command == 7:
            banknote = ConsoleReader.get_banknotes_amount()
            self.__save_banknote(banknote.get('denomination'), banknote.get('amount'))
            return 'Done'

        if user.id == 1 and command == 8:
            str_generator = (f"Denomination {item.get('denomination')} Amount: {item.get('amount')}"
                             for item in self.__banknote_service.get_all())
            return '\n'.join(str_generator)

    @staticmethod
    def get_available_denomination() -> tuple:
        return 10, 20, 50, 100, 200, 500, 1000


def get_user() -> User:
    count = 3
    user = None
    user_service = UserService()
    while not user:
        username, password = ConsoleReader.get_username_and_password()

        try:
            user = user_service.login(username, password)
            if not user and input('User not found. To create this user enter 1:') == '1':
                user = user_service.sign_up(username, password)
        except ATMException as e:
            print(f"Verification exception: {e}")

        if not user and count > 0:
            count -= 1
            print(f'You have {count} attempts. Try again.')
        elif count <= 0:
            raise ATMException("you could not login")

    return user


def start():
    user = None
    try:
        user = get_user()
    except ATMException as e:
        print(f'Login exception: {e}')

    command = None
    atm_service = ATMService()
    while user and (not command or command != 6):
        command = ConsoleReader.get_command_from_console(user.id == 1)
        try:
            print('- - - - - - - - - - - -')
            print(atm_service.get_command_result(user, command))
            print('- - - - - - - - - - - -')
            print()
        except ATMException as e:
            print(f'Command exception: {e}')

    print('Program complete')


if __name__ == '__main__':
    start()
