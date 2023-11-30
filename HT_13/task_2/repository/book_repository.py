import sqlite3

from HT_13.task_2.connect import DBConnection
from HT_13.task_2.model.model import CustomException, Book


class BookRepository:

    def get_all(self) -> list[Book]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = "SELECT id, author, title, publisher_info, number, number_available FROM books"
                cur.execute(sql)
                rows = cur.fetchall()
                return [Book(row['id'], row['author'], row['title'], row['publisher_info'], row['number'],
                             row['number_available']) for row in rows]
            except sqlite3.Error:
                raise CustomException("can't get books from database")

    def get_by_id(self, _id: int) -> [Book, None]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = '''SELECT id, author, title, publisher_info, number, number_available FROM books WHERE id=? '''
                cur.execute(sql, (_id,))

                row = cur.fetchone()
                if row:
                    return Book(row['id'], row['author'], row['title'], row['publisher_info'], row['number'],
                                row['number_available'])
            except sqlite3.Error:
                raise CustomException("can't get book from database")

    def insert(self, book: Book):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute(''' INSERT INTO books (author, title, publisher_info, number, number_available) 
                                VALUES (?, ?, ?, ?, ?) RETURNING id''',
                            (book.author, book.title, book.publisher_info, book.number, book.number_available))
                data = cur.fetchone()
                con.commit()

                book.id = data[0]
            except sqlite3.Error:
                raise CustomException("can't insert boof to database")

    def update(self, book: Book):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute(''' UPDATE books SET author=?, title=?, publisher_info=?, number=?, number_available = ?
                                WHERE id=?''',
                            (book.author, book.title, book.publisher_info, book.number, book.number_available,
                             book.id))
                con.commit()
            except sqlite3.Error:
                raise CustomException("can't update author to database")
