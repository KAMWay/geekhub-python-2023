import sqlite3
from pathlib import Path


class DBConnection:

    def __init__(self):
        self.__con = None

    def __enter__(self):
        return sqlite3.connect(Path('db', 'library.db'))

    def __exit__(self, exception_type, exception_val, trace):
        if self.__con:
            self.__con.close()
