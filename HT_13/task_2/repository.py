import sqlite3

from HT_13.task_2.connect import DBConnection
from HT_13.task_2.model import Person, CustomException, Author, Book, Category


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

                sql = "SELECT id, name, lastname FROM persons WHERE name=? and lastname=?"
                cur.execute(sql, (name, lastname))

                data = cur.fetchone()
                if data:
                    return Person(data[0], data[1], data[2])
            except sqlite3.Error:
                raise CustomException("can't get person from database")

    def insert(self, person: Person):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO persons (name, lastname) VALUES (?, ?) RETURNING id",
                            (person.name, person.lastname))
                data = cur.fetchone()
                con.commit()

                person.id = data[0]
            except sqlite3.Error:
                raise CustomException("can't insert person to database")

    def update(self, person: Person):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute("UPDATE persons SET name=?, lastname=? WHERE id=?",
                            (person.name, person.lastname, person.id))
                con.commit()
            except sqlite3.Error:
                raise CustomException("can't update person to database")


class AuthorRepository:
    def get_all(self) -> list[Author]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = "SELECT id, full_name FROM authors"
                cur.execute(sql)
                rows = cur.fetchall()
                return [Author(row['id'], row['full_name']) for row in rows]
            except sqlite3.Error:
                raise CustomException("can't get authors from database")

    def get_by_full_name(self, full_name: str) -> [Author, None]:
        with DBConnection() as con:
            try:
                cur = con.cursor()

                sql = "SELECT id, full_name FROM authors WHERE full_name=? "
                cur.execute(sql, (full_name,))

                data = cur.fetchone()
                if data:
                    return Author(data[0], data[1])
            except sqlite3.Error:
                raise CustomException("can't get author from database")

    def insert(self, author: Author):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO authors (full_name) VALUES (?) RETURNING id", (author.full_name,))
                data = cur.fetchone()
                con.commit()

                author.id = data[0]
            except sqlite3.Error:
                raise CustomException("can't insert author to database")

    def update(self, author: Author):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute("UPDATE authors SET full_name=? WHERE id=?", (author.full_name,))
                con.commit()
            except sqlite3.Error:
                raise CustomException("can't update author to database")


class BookRepository:
    def get_all(self) -> list[Book]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = "SELECT id, author_id, title, publisher_info, number, number_available FROM books"
                cur.execute(sql)
                rows = cur.fetchall()
                return [Book(row['id'], row['author_id'], row['title'], row['publisher_info'], row['number'],
                             row['number_available']) for row in rows]
            except sqlite3.Error:
                raise CustomException("can't get books from database")

    def get_by_id(self, book_id: int) -> [Book, None]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = '''SELECT id, author_id, title, publisher_info, number, number_available FROM books WHERE id=? '''
                cur.execute(sql, (book_id,))

                row = cur.fetchone()
                if row:
                    return Book(row['id'], row['author_id'], row['title'], row['publisher_info'], row['number'],
                                row['number_available'])
            except sqlite3.Error:
                raise CustomException("can't get book from database")

    def insert(self, book: Book):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute(''' INSERT INTO books (author_id, title, publisher_info, number, number_available) 
                                VALUES (?, ?, ?, ?, ?) RETURNING id''',
                            (book.author_id, book.title, book.publisher_info, book.number, book.number_available))
                data = cur.fetchone()
                con.commit()

                book.id = data[0]
            except sqlite3.Error:
                raise CustomException("can't insert boof to database")

    def update(self, book: Book):
        with DBConnection() as con:
            try:
                cur = con.cursor()
                cur.execute(''' UPDATE books SET author_id=?, title=?, publisher_info=?, number=?, number_available = ?
                                WHERE id=?''',
                            (book.author_id, book.title, book.publisher_info, book.number, book.number_available,
                             book.id))
                con.commit()
            except sqlite3.Error:
                raise CustomException("can't update author to database")


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

    def get_by_id(self, id: int) -> [Category, None]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = "SELECT id, info FROM categories WHERE id=? "
                cur.execute(sql, (id,))

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


class PersonBooksRepository:
    def get_all(self) -> dict[Person:list[Book]]:
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
                       b.author_id          as book_author_id,
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

                persons_dict = {}
                for row in rows:
                    person = Person(row['person_id'], row['person_name'], row['person_lastname'])
                    book = Book(row['book_id'], row['book_author_id'], row['book_title'],
                                row['book_publisher_info'], row['book_number'], row['book_number_available'])
                    books = persons_dict.get(person)
                    if books:
                        books.append(book)
                    else:
                        persons_dict[person] = [book]

                return persons_dict
            except sqlite3.Error:
                raise CustomException("can't get persons books from database")

    def get_by_person_id(self, persons_id: int) -> dict[Person:list[Book]]:
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
                       b.author_id          as book_author_id,
                       b.title              as book_title,
                       b.publisher_info     as book_publisher_info,
                       b.number             as book_number,
                       b.number_available   as book_number_available
                FROM persons_books pb
                        JOIN persons p on p.id = pb.person_id
                        JOIN books b on b.id = pb.book_id
                WHERE pb.person_id = ?
                '''
                cur.execute(sql, (persons_id,))
                rows = cur.fetchall()
                person = None
                books = []
                for row in rows:
                    if not person:
                        person = Person(row['person_id'], row['person_name'], row['person_lastname'])
                    book = Book(row['book_id'], row['book_author_id'], row['book_title'],
                                row['book_publisher_info'], row['book_number'], row['book_number_available'])
                    books.append(book)

                return {person: books}
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


class BookCategoriesRepository:
    def get_all(self) -> dict[Book:list[Category]]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = '''
                        SELECT bc.book_id         as book_id,
                               b.author_id        as book_author_id,
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

                books_dict = {}
                for row in rows:
                    book = Book(row['book_id'], row['book_author_id'], row['book_title'],
                                row['book_publisher_info'], row['book_number'], row['book_number_available'])
                    category = Category(row['category_id'], row['category_info'])
                    categories = books_dict.get(book)
                    if categories:
                        categories.append(category)
                    else:
                        books_dict[book] = [category]

                return books_dict
            except sqlite3.Error:
                raise CustomException("can't get persons books from database")

    def get_by_book_id(self, book_id: int) -> dict[Book:list[Category]]:
        with DBConnection() as con:
            try:
                con.row_factory = sqlite3.Row
                cur = con.cursor()

                sql = '''
                        SELECT bc.book_id         as book_id,
                               b.author_id        as book_author_id,
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
                book = None
                categories = []
                for row in rows:
                    if not book:
                        book = Book(row['book_id'], row['book_author_id'], row['book_title'],
                                    row['book_publisher_info'], row['book_number'], row['book_number_available'])

                    category = Category(row['category_id'], row['category_info'])
                    categories.append(category)

                return {book: categories}
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


if __name__ == '__main__':
    s = BookCategoriesRepository()
    for k, v in s.get_all().items():
        print(k, end=' | ')
        [print(i, end=' ') for i in v]
        print()
