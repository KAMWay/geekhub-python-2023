import sqlite3

from HT_13.task_2.connect import DBConnection
from HT_13.task_2.model.model import CustomException, Category


class CategoryRepository:
    def get_all(self) -> list[Category]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = "SELECT id, info FROM categories"
                cur.execute(sql)
                rows = cur.fetchall()
                return [Category(row['id'], row['info']) for row in rows]
            except sqlite3.Error:
                raise CustomException("can't get categories from database")

    def get_by_id(self, _id: int) -> [Category, None]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = "SELECT id, info FROM categories WHERE id=? "
                cur.execute(sql, (_id,))

                row = cur.fetchone()
                if row:
                    return Category(row['id'], row['info'])
            except sqlite3.Error:
                raise CustomException("can't get category from database")

    def insert(self, category: Category):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO categories (info) VALUES (?) RETURNING id", (category.info,))
                data = cur.fetchone()
                con.commit()

                category.id = data[0]
            except sqlite3.Error:
                raise CustomException("can't insert category to database")

    def update(self, category: Category):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute("UPDATE categories SET info=? WHERE id=?", (category.info,))
                con.commit()
            except sqlite3.Error:
                raise CustomException("can't update category to database")
