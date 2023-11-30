import sqlite3

from HT_13.task_2.connect import DBConnection
from HT_13.task_2.model.model import Person, CustomException


class PersonRepository:
    def get_all(self) -> list[Person]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = "SELECT id, name, lastname FROM persons"
                cur.execute(sql)
                rows = cur.fetchall()
                return [Person(row['id'], row['name'], row['lastname']) for row in rows]
            except sqlite3.Error:
                raise CustomException("can't get persons from database")

    def get_by_name(self, name: str, lastname: str) -> [Person, None]:
        with DBConnection() as con:
            try:
                cur = con.cursor()

                sql = "SELECT id, name, lastname, role FROM persons WHERE name=? and lastname=?"
                cur.execute(sql, (name, lastname))

                data = cur.fetchone()
                if data:
                    return Person(data[0], data[1], data[2], data[3])
            except sqlite3.Error:
                raise CustomException("can't get person from database")

    def insert(self, person: Person):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO persons (name, lastname, role) VALUES (?, ?, ?) RETURNING id",
                            (person.name, person.lastname, person.role))
                data = cur.fetchone()
                con.commit()

                person.id = data[0]
            except sqlite3.Error:
                raise CustomException("can't insert person to database")

    def update(self, person: Person):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute("UPDATE persons SET name=?, lastname=?, role=? WHERE id=?",
                            (person.name, person.lastname, person.role, person.id))
                con.commit()
            except sqlite3.Error:
                raise CustomException("can't update person to database")
