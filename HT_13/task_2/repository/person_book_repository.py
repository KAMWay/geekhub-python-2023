import sqlite3

from HT_13.task_2.connect import DBConnection
from HT_13.task_2.model.model import Person, CustomException, Book

class PersonBookRepository:
    def get_all(self) -> list[dict[Person:Book]]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = '''
                SELECT pb.person_id         as person_id,
                       p.name               as person_name,
                       p.lastname           as person_lastname,
                       p.role               as person_role,
                       pb.book_id           as book_id,
                       b.author             as book_author,
                       b.title              as book_title,
                       b.publisher_info     as book_publisher_info,
                       b.number             as book_number,
                       b.number_available   as book_number_available
                FROM persons_books pb
                        JOIN persons p on p.id = pb.person_id
                        JOIN books b on b.id = pb.book_id
                '''
                cur.execute(sql)
                rows = cur.fetchall()

                return [{self.__person_mapping(row): self.__book_mapping(row)} for row in rows]
            except sqlite3.Error:
                raise CustomException("can't get persons books from database")

    def get_by_person_id(self, persons_id: int) -> list[Book]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = '''
                SELECT pb.person_id         as person_id,
                       pb.book_id           as book_id,
                       b.author             as book_author,
                       b.title              as book_title,
                       b.publisher_info     as book_publisher_info,
                       b.number             as book_number,
                       b.number_available   as book_number_available
                FROM persons_books pb
                        JOIN books b on b.id = pb.book_id
                WHERE pb.person_id = ?
                '''
                cur.execute(sql, (persons_id,))
                rows = cur.fetchall()

                return [self.__book_mapping(row) for row in rows]
            except sqlite3.Error:
                raise CustomException("can't get person books from database")

    def insert(self, person_id: int, book_id: int):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO persons_books (person_id, book_id) VALUES (?,?)", (person_id, book_id))
                con.commit()
            except sqlite3.Error:
                raise CustomException("can't person book to database")

    def delete(self, person_id: int, book_id: int):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute("DELETE FROM persons_books WHERE person_id=? AND book_id=?", (person_id, book_id))
                con.commit()
            except sqlite3.Error:
                raise CustomException("can't update group to database")

    @staticmethod
    def __person_mapping(row: dict) -> Person:
        return Person(row['person_id'], row['person_name'], row['person_lastname'])

    @staticmethod
    def __book_mapping(row: dict) -> Book:
        return Book(row['book_id'], row['book_author'], row['book_title'],
                    row['book_publisher_info'], row['book_number'], row['book_number_available'])


