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


class User:
    def __init__(self, user_id: [int, None], username: str, password: str):
        self.id = user_id
        self.username = username
        self.password = password

    def is_new(self):
        return self.id is None

    def is_admin(self):
        return self.id == 1


class ATM:
    def __init__(self, atm_id: int = 1, info: str = ""):
        self.id = atm_id
        self.info = info


class Banknote:
    def __init__(self, denomination: int, amount: int, atm_id: int = 1):
        self.denomination = denomination
        self.amount = amount
        self.atm_id = atm_id


class Transaction:
    from datetime import datetime

    def __init__(self, user_id: int, dt: [datetime, None], amount: [float, int], balance: [float, int]):
        from datetime import datetime
        dt = datetime.now() if not dt else dt

        self.user_id = user_id
        self.dt = dt
        self.amount = amount
        self.balance = balance


class ConsoleReader:
    @staticmethod
    def get_user() -> User:
        print('----Please Sign In/Up----')
        username = input('Enter user name: ')
        password = input('Enter password: ')
        return User(None, username, password)

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
    def get_banknote_amount() -> Banknote:
        try:
            banknote = int(input('Input banknotes denomination [10, 20, 50, 100, 200, 500, 1000]: '))
            if banknote not in ATMService.get_available_denomination():
                raise ValueError

            amount = int(input('Input amount: '))
            if amount < 0:
                raise ValueError

            return Banknote(banknote, amount)
        except ValueError:
            raise ATMException('incorrect input banknotes')

    @staticmethod
    def get_command_from_console(is_admin: bool = False) -> int:
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


class UserService:
    def __init__(self):
        self.__user_repository = UserRepository()

    @staticmethod
    def __is_valid(username: str, password: str) -> bool:
        if not username or not password:
            raise ATMException("username and password can't be empty")
        return True

    def get(self, username: str, password: str) -> User:
        if self.__is_valid(username, password):
            return self.__user_repository.get_by_username_and_password(username, password)

    def save(self, user: User):
        if self.__is_valid(user.username, user.password):
            if user.is_new():
                self.__user_repository.insert(user)


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

    def get_all(self, user: int) -> list[Transaction]:
        return self.__user_transaction_repository.get_all_by_user_id(user)

    def save(self, transaction: Transaction):
        self.__user_transaction_repository.insert(transaction)


class ATMBanknoteService:
    def __init__(self):
        self.__banknote_repository = ATMBanknoteRepository()

    def save(self, banknote: Banknote):
        if self.__banknote_repository.get_by_denomination(banknote.denomination):
            self.__banknote_repository.update(banknote)
        else:
            self.__banknote_repository.insert(banknote)

    def get_all(self, atm_id: int = 1) -> list[Banknote]:
        return self.__banknote_repository.get_all_by_atm_id(atm_id)


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
                return User(data[0], username, password)
        except sqlite3.Error:
            raise ATMException("can't get user from database")
        finally:
            Connection.close_connection(con)

    def insert(self, user: User):
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()

            cur.execute("INSERT INTO users (username, password) VALUES (?,?) RETURNING id",
                        (user.username, user.password))
            data = cur.fetchone()
            con.commit()

            user.id = data[0]
        except sqlite3.Error:
            raise ATMException("can't save user to database")
        finally:
            Connection.close_connection(con)


class UserBalanceRepository:
    def get_by_user_id(self, user_id: int) -> float:
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()

            sql = "SELECT balance FROM user_balance WHERE user_id=?"
            cur.execute(sql, (user_id,))

            data = cur.fetchone()
            if data:
                return data[0]
        except sqlite3.Error:
            raise ATMException("can't get balance from database")
        finally:
            Connection.close_connection(con)

    def update(self, user_id: int, balance: [int, float]):
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()
            cur.execute("UPDATE user_balance SET balance=? WHERE user_id=?",
                        (balance, user_id))
            con.commit()
        except sqlite3.Error:
            raise ATMException("can't update balance in database")
        finally:
            Connection.close_connection(con)

    def insert(self, user_id: int, balance: [int, float]):
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()
            cur.execute("INSERT INTO user_balance (balance, user_id) VALUES (?,?)",
                        (balance, user_id))
            con.commit()
        except sqlite3.Error:
            raise ATMException("can't insert balance to database")

        finally:
            Connection.close_connection(con)


class UserTransactionRepository:
    def get_all_by_user_id(self, user_id: int) -> list[Transaction]:
        con = None
        try:
            con = Connection.get_connection()
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            sql = "SELECT user_id, dt, amount, balance FROM user_transactions WHERE user_id=?"
            cur.execute(sql, (user_id,))

            rows = cur.fetchall()

            return [Transaction(user_id, row['dt'], row['amount'], row['balance']) for row in rows]
        except sqlite3.Error:
            raise ATMException("can't get transactions from database")
        finally:
            Connection.close_connection(con)

    def insert(self, transaction: Transaction):
        con = None
        try:
            con = Connection.get_connection()
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            sql = "INSERT INTO user_transactions (user_id, dt, amount, balance) VALUES (?, ?, ?, ?)"
            cur.execute(sql, (transaction.user_id, transaction.dt, transaction.amount, transaction.balance))

            con.commit()
        except sqlite3.Error:
            raise ATMException("can't save transactions to database")
        finally:
            Connection.close_connection(con)


class ATMBanknoteRepository:
    def get_all_by_atm_id(self, atm_id: int = 1) -> list[Banknote]:
        con = None
        try:
            con = Connection.get_connection()
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            sql = "SELECT atm_id, denomination, amount FROM atm_banknotes WHERE atm_id=?"
            cur.execute(sql, (atm_id,))

            rows = cur.fetchall()

            return [Banknote(row['denomination'], row['amount'], atm_id) for row in rows]
        except sqlite3.Error:
            raise ATMException("can't get banknotes from database")
        finally:
            Connection.close_connection(con)

    def get_by_denomination(self, denomination: int, atm_id: int = 1) -> Banknote:
        con = None
        try:
            con = Connection.get_connection()
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            sql = "SELECT atm_id, denomination, amount FROM atm_banknotes WHERE denomination=? AND atm_id=?"
            cur.execute(sql, (denomination, atm_id))

            row = cur.fetchone()

            if row:
                return Banknote(row['denomination'], row['amount'], atm_id)
        except sqlite3.Error:
            raise ATMException("can't get banknote from database")
        finally:
            Connection.close_connection(con)

    def update(self, banknote: Banknote):
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()

            cur.execute("UPDATE atm_banknotes SET amount=? WHERE denomination=? AND atm_id=?",
                        (banknote.amount, banknote.denomination, banknote.atm_id))

            con.commit()
        except sqlite3.Error:
            raise ATMException("can't update banknotes in database")
        finally:
            Connection.close_connection(con)

    def insert(self, banknote: Banknote):
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()

            cur.execute("INSERT INTO atm_banknotes (amount, denomination, atm_id) VALUES (?, ?, ?)",
                        (banknote.amount, banknote.denomination, banknote.atm_id))

            con.commit()
        except sqlite3.Error:
            raise ATMException("can't insert banknotes to database")
        finally:
            Connection.close_connection(con)


class ATMService:
    def __init__(self):
        self.__banknote_service = ATMBanknoteService()
        self.__user_balance_service = UserBalanceService()
        self.__user_transaction_service = UserTransactionService()

    def __save_banknote(self, banknote: Banknote):
        self.__banknote_service.save(banknote)

    def __get_atm_balance(self, atm: ATM) -> int:
        return sum(i.denomination * i.amount for i in self.__banknote_service.get_all(atm.id))

    def __get_bonus_percent(self, user: User, bonus_size: int = 10) -> float:
        from random import randrange
        if len(self.__user_transaction_service.get_all(user.id)) != 0:
            return 0

        return bonus_size / 100 if not randrange(0, 9, 1) else 0

    def __change_user_balance(self, user: User, amount: [int, float], atm: ATM) -> float:
        user_balance = self.__user_balance_service.get(user.id)

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

        self.__user_balance_service.save(user.id, user_balance)
        transaction = Transaction(user.id, None, amount, user_balance)
        self.__user_transaction_service.save(transaction)

        return back_amount if amount > 0 else -amount

    def __get_user_transactions(self, user: User):
        return self.__user_transaction_service.get_all(user.id)

    def get_command_result(self, user: User, command: int, atm: ATM = ATM(1)) -> str:
        if command == 6:
            return 'User exit'

        if command == 1:
            return f'Total user deposit: {self.__user_balance_service.get(user.id)}'

        if command == 2:
            return f'Total ATM deposit: {self.__get_atm_balance(atm)}'

        if command == 3 or command == 4:
            amount = ConsoleReader.get_amount()
            back_amount = self.__change_user_balance(user, (amount if command == 3 else -amount), atm)
            return 'Done' if back_amount == 0 else f'Return {round(back_amount, 2)}'

        if command == 5:
            str_generator = ('Date {} Amount: {}'.format(item.dt, item.amount)
                             for item in self.__get_user_transactions(user))
            return '\n'.join(str_generator)

        if user.is_admin() and command == 7:
            banknote = ConsoleReader.get_banknote_amount()
            banknote.atm_id = atm.id
            self.__save_banknote(banknote)
            return 'Done'

        if user.is_admin() and command == 8:
            str_generator = (f"Denomination {item.denomination} Amount: {item.amount}"
                             for item in self.__banknote_service.get_all())
            return '\n'.join(str_generator)

    @staticmethod
    def get_available_denomination() -> tuple:
        return 10, 20, 50, 100, 200, 500, 1000


def get_user() -> User:
    count = 3
    user_service = UserService()
    user = None
    while not user or user.id is None:
        user = ConsoleReader.get_user()

        try:
            exist_user = user_service.get(user.username, user.password)
            if exist_user:
                return exist_user
            if input('User not found. To create this user enter 1:') == '1':
                user_service.save(user)
        except ATMException as e:
            print(f"Sign In/Up exception: {e}")

        if not user.id and count > 0:
            count -= 1
            print(f'You have {count + 1} attempts. Try again.')
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
        command = ConsoleReader.get_command_from_console(user.is_admin())
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
