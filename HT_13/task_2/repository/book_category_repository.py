import sqlite3

from HT_13.task_2.connect import DBConnection
from HT_13.task_2.model.model import CustomException, Book, Category


class BookCategoryRepository:
    def get_all(self) -> list[dict[Book:Category]]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = '''
                        SELECT bc.book_id         as book_id,
                               b.author           as book_author,
                               b.title            as book_title,
                               b.publisher_info   as book_publisher_info,
                               b.number           as book_number,
                               b.number_available as book_number_available,
                               bc.category_id     as category_id,
                               c.info             as category_info
                        FROM books_categories bc
                                 JOIN books b on b.id = bc.book_id
                                 JOIN categories c on c.id = bc.category_id
                '''
                cur.execute(sql)
                rows = cur.fetchall()

                return [{self.__book_mapping(row): self.__category_mapping(row)} for row in rows]
            except sqlite3.Error:
                raise CustomException("can't get persons books from database")

    def get_by_book_id(self, book_id: int) -> list[dict[Book:Category]]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = '''
                        SELECT bc.book_id         as book_id,
                               b.author           as book_author,
                               b.title            as book_title,
                               b.publisher_info   as book_publisher_info,
                               b.number           as book_number,
                               b.number_available as book_number_available,
                               bc.category_id     as category_id,
                               c.info             as category_info
                        FROM books_categories bc
                                 JOIN books b on b.id = bc.book_id
                                 JOIN categories c on c.id = bc.category_id
                        WHERE bc.book_id  = 1
                '''
                cur.execute(sql, (book_id,))
                rows = cur.fetchall()
                return [{self.__book_mapping(row): self.__category_mapping(row)} for row in rows]
            except sqlite3.Error:
                raise CustomException("can't get person books from database")

    def insert(self, book_id: int, category_id: int):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO books_categories (book_id, category_id) VALUES (?,?)", (book_id, category_id))
                con.commit()
            except sqlite3.Error:
                raise CustomException("can't person book to database")

    def delete(self, book_id: int, category_id: int):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute("DELETE FROM books_categories WHERE book_id=? AND category_id=?", (book_id, category_id))
                con.commit()
            except sqlite3.Error:
                raise CustomException("can't update group to database")

    @staticmethod
    def __category_mapping(row: dict) -> Category:
        return Category(row['category_id'], row['category_info'])

    @staticmethod
    def __book_mapping(row: dict) -> Book:
        return Book(row['book_id'], row['book_author'], row['book_title'],
                    row['book_publisher_info'], row['book_number'], row['book_number_available'])
