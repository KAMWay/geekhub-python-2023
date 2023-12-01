import sqlite3
from pathlib import Path


class Connection:
    @staticmethod
    def get_connection():
        return sqlite3.connect(Path('db', 'atm.db'))

    @staticmethod
    def close_connection(con):
        if con:
            con.close()
