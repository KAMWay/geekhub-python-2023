import sqlite3

from HT_14.task_1.model import User, ATMException, Transaction, Banknote
from HT_14.task_1.util import Connection


class UserRepository:
    def get_by_username(self, username: str) -> [User, None]:
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()

            sql = "SELECT id, username, password FROM users WHERE username=?"
            cur.execute(sql, (username,))

            data = cur.fetchone()
            if data:
                return User(data[0], data[1], data[2])
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


class BanknoteRepository:
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

    def update_all(self, banknotes: list[Banknote]):
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()
            cur.executemany("UPDATE atm_banknotes SET amount=? WHERE denomination=? AND atm_id=?",
                            [(banknote.amount, banknote.denomination, banknote.atm_id) for banknote in banknotes])

            con.commit()
        except sqlite3.Error:
            raise ATMException("can't update all banknotes in database")
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

    def insert_all(self, banknotes: list[Banknote]):
        con = None
        try:
            con = Connection.get_connection()
            cur = con.cursor()
            cur.executemany("INSERT INTO atm_banknotes (amount, denomination, atm_id) VALUES (?, ?, ?)",
                            [(banknote.amount, banknote.denomination, banknote.atm_id) for banknote in banknotes])

            con.commit()
        except sqlite3.Error:
            raise ATMException("can't insert all banknotes in database")
        finally:
            Connection.close_connection(con)
