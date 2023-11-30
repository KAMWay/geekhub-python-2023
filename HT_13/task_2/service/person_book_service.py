from HT_13.task_2.model.model import Book, Person
from HT_13.task_2.repository.person_book_repository import PersonBookRepository


class PersonBookService:
    def __init__(self):
        self.__repository = PersonBookRepository()

    def get_persons_with_books(self) -> dict[Person:list[Book]]:
        persons_dict = {}
        for item_dict in self.__repository.get_all():
            for person, book in item_dict.items():
                books = persons_dict.get(person)
                if books:
                    books.append(book)
                else:
                    persons_dict[person] = [book]
        return persons_dict

    def get_person_with_books(self, person:Person) -> dict[Person:list[Book]]:
        return self.__repository.get_by_person_id(person.id)

    def get_books_with_persons(self) -> dict[Book:list[Person]]:
        books_dict = {}
        for item_dict in self.__repository.get_all():
            for person, book in item_dict.items():
                persons = books_dict.get(book)
                if persons:
                    persons.append(person)
                else:
                    books_dict[book] = [person]
        return books_dict

    def save(self, person: Person, book: Book):
        self.__repository.insert(person.id, book.id)

    def delete(self, person: Person, book: Book):
        self.__repository.delete(person.id, book.id)
