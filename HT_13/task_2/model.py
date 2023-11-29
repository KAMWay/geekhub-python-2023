# 2. Створіть за допомогою класів та продемонструйте свою реалізацію шкільної бібліотеки (включіть фантазію).
# Наприклад вона може містити класи Person, Teacher, Student, Book, Shelf, Author, Category і.т.д.

import sqlite3
from pathlib import Path


class CustomException(Exception):
    pass


class Entity:
    def __init__(self, id: [int, None] = None):
        self.__id = id

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, id: int):
        self.__id = id

    def is_new(self) -> bool:
        return self.__id is not None


class Group(Entity):
    def __init__(self, id: [int, None], info: str):
        Entity.__init__(self, id)
        self.__info = info

    @property
    def info(self) -> str:
        return self.__info


class Person(Entity):
    def __init__(self, id: [int, None], name: str, lastname: str):
        super().__init__(id)
        self.__name = name
        self.__lastname = lastname

    @property
    def name(self) -> str:
        return self.__name

    @property
    def lastname(self) -> str:
        return self.__lastname


class Author(Entity):
    def __init__(self, id: [int, None], full_name: str):
        super().__init__(id)
        self.__full_name = full_name

    @property
    def full_name(self) -> str:
        return self.__full_name


class Book(Entity):
    def __init__(self, id: [int, None], author_id: int, title: str, publisher_info: str, number: int,
                 number_available: int):
        super().__init__(id)

        self.__author_id = author_id
        self.__title = title
        self.__publisher_info = publisher_info
        self.__number = number
        self.__number_available = number_available

    @property
    def author_id(self) -> int:
        return self.__author_id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def publisher_info(self) -> str:
        return self.__publisher_info

    @property
    def number(self) -> int:
        return self.__number

    @property
    def number_available(self) -> int:
        return self.__number_available

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.id == other.id and self.author_id == other.author_id

    def __hash__(self):
        return self.id

    def __str__(self):
        return f"id:{self.id} title:{self.title} number:{self.number} available:{self.__number_available}"


class Category(Entity):
    def __init__(self, id: [int, None], info: str):
        super().__init__(id)
        self.__info = info

    @property
    def info(self) -> str:
        return self.__info

    def __str__(self):
        return f"{self.id}:{self.__info}"


class BookCategories:
    def __init__(self, book: Book, categories: [set[Category], None] = None):
        self.__book = book
        self.__categories = [] if not categories else categories

    @property
    def book(self) -> Book:
        return self.__book

    @property
    def categories(self) -> set[int]:
        return self.__categories

    def add_category(self, category_id: int):
        self.__categories.add(category_id)

    def remove_category(self, category_id: int):
        self.__categories.remove(category_id)

    def clear_categories(self):
        self.__categories.clear()


class AuthorBooks:
    def __init__(self, author: Author, books: [set[Book], None] = None):
        self.__author = author
        self.__books = [] if not books else books

    @property
    def author(self) -> Author:
        return self.__author

    @property
    def books(self) -> set[Book]:
        return self.__books

    def add_book(self, book: Book):
        self.__books.add(book)

    def remove_book(self, book: Book):
        self.__books.remove(book)

    def clear_books(self):
        self.__books.clear()


class PersonBooks:
    def __init__(self, person: Person, books: [set[Book], None] = None):
        self.__person = person
        self.__books = [] if not books else books

    @property
    def person(self) -> Person:
        return self.__person

    @property
    def books(self) -> set[Book]:
        return self.__books

    def add_book(self, book: Book):
        self.__books.add(book)

    def remove_book(self, book: Book):
        self.__books.remove(book)

    def clear_books(self):
        self.__books.clear()


class DBConnection:
    def __enter__(self):
        return sqlite3.connect(Path('db', 'library.db'))

    def __exit__(self, con):
        if con:
            con.close()


if __name__ == '__main__':
    ...
