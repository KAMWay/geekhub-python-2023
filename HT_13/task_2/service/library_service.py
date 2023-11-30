from HT_13.task_2.api.console_reader import ConsoleReader
from HT_13.task_2.model.model import Person, CustomException, Book, Category
from HT_13.task_2.service.book_category_service import BookCategoryService
from HT_13.task_2.service.book_service import BookService
from HT_13.task_2.service.category_service import CategoryService
from HT_13.task_2.service.person_book_service import PersonBookService
from HT_13.task_2.service.person_service import PersonService


class LibraryService:
    def __init__(self):
        self.__person_service = PersonService()
        self.__book_service = BookService()
        self.__category_service = CategoryService()
        self.__book_category_service = BookCategoryService()
        self.__person_book_service = PersonBookService()

    def get_person(self) -> Person:
        person = ConsoleReader.get_person()
        return self.__person_service.get_by_name(person.name, person.lastname)

    def __create_person(self) -> Person:
        roles = ['ADMIN', 'STUDENT', 'TEACHER']
        roles_str = "\n".join(f"{i}. {roles[i]}" for i in range(len(roles)))

        person = ConsoleReader.get_person()
        number = ConsoleReader.get_number(roles_str + '\nEnter number: ')

        if number < 1 or number > len(roles):
            raise CustomException('Incorrect input role')

        person.role = roles[number - 1]
        return self.__person_service.save(person)

    def __return_book(self, person: Person):
        book_id = ConsoleReader.get_number('Enter book id: ')
        book = self.__book_service.get_by_id(book_id)
        book.number_available += 1
        self.__book_service.save(book)
        self.__person_book_service.delete(person, book)

    def __get_book(self, person: Person):
        book_id = ConsoleReader.get_number('Enter book id: ')
        book = self.__book_service.get_by_id(book_id)
        book.number_available -= 1
        self.__book_service.save(book)
        self.__person_book_service.save(person, book)

    @staticmethod
    def __book_to_str(book: Book) -> str:
        return f"id:{book.id} Title: {book.title} Author: {book.author} Number {book.number} Available {book.number_available}"

    def __category_with_books_to_str(self, category: Category, books: list[Book]) -> str:
        return f"id:{category.id} {category.info}: \n     " + '\n     '.join(self.__book_to_str(i) for i in books)

    def get_command_result(self, person: Person, command: int) -> str:
        if command == 7:
            return 'Exit'

        if command == 1:
            str_generator = (self.__book_to_str(book) for book in self.__book_service.get_all())
            return '\n'.join(str_generator)

        if command == 2:
            book_atr = ConsoleReader.get_book_atr_for_search()
            str_generator = (self.__book_to_str(book) for book in
                             self.__book_service.get_by_author_and_title(book_atr.author, book_atr.title))
            return '\n'.join(str_generator)

        if command == 3:
            categories = self.__book_category_service.get_categories_with_books()
            str_generator = (self.__category_with_books_to_str(k, v) for k, v in categories.items())
            return '\n'.join(str_generator)

        if command == 4:
            str_generator = (self.__book_to_str(book) for book in
                             self.__person_book_service.get_person_with_books(person))
            return '\n'.join(str_generator)

        if command == 5:
            self.__return_book(person)
            return "Done"

        if command == 6:
            self.__get_book(person)
            return "Done"

        if person.is_admin() and command == 8:
            person = self.__create_person()
            return "Done"
