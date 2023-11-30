import sqlite3
from pathlib import Path


class DBConnection:
    def __init__(self):
        self.__con = None

    def __enter__(self):
        self.__con = sqlite3.connect(Path('db', 'library.db'))
        return self.__con

    def __exit__(self, exception_type, exception_val, trace):
        if self.__con:
            self.__con.close()
