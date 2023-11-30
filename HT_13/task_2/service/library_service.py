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
        person = ConsoleReader.get_person()

        roles = self.__person_service.get_roles()
        roles_str = "\n".join(f"{i + 1}. {roles[i]}" for i in range(len(roles)))
        number = ConsoleReader.get_number(roles_str + '\nEnter number: ')

        if number < 1 or number > len(roles):
            raise CustomException('Incorrect input role')

        person.role = roles[number - 1]
        return self.__person_service.save(person)

    def __create_book(self) -> Book:
        book = ConsoleReader.get_book()
        return self.__book_service.save(book)

    def __create_category(self) -> Category:
        category = ConsoleReader.get_category()
        return self.__category_service.save(category)

    def __change_book_category(self, is_new: bool = True):

        book_id = ConsoleReader.get_number("Enter book id: ")
        book = self.__book_service.get_by_id(book_id)
        if not book:
            raise CustomException("can't find book")

        if is_new:
            all_categories = set(self.__category_service.get_all())
            exist_categories = set(self.__book_category_service.get_categories_by_book(book))
            categories = all_categories.difference(exist_categories)
        else:
            categories = self.__book_category_service.get_categories_by_book(book)

        if len(categories) == 0:
            raise CustomException("not available categories")

        categories_str = "\n".join(f"id:{i.id} {i.info}" for i in categories)
        number = ConsoleReader.get_number(categories_str + '\nEnter category id: ')

        if not categories or not any(i.id == number for i in categories):
            raise CustomException('Incorrect input category id')

        category = next((i for i in categories if i.id == number))

        if is_new:
            self.__book_category_service.save(book, category)
        else:
            self.__book_category_service.delete(book, category)

    def __update_book_amount(self):
        book_id = ConsoleReader.get_number("Enter book id: ")
        book = self.__book_service.get_by_id(book_id)

        if not book:
            raise CustomException("can't find book")

        book.number = ConsoleReader.get_number("Enter book number: ", 0)
        book.number_available = ConsoleReader.get_number("Enter book number available: ", 0)
        self.__book_service.save(book)

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
        return f"id:{book.id} Title: {book.title} Author: {book.author} [{book.number}:{book.number_available}]"

    def __category_with_books_to_str(self, category: Category, books: list[Book]) -> str:
        return f"id:{category.id} {category.info}: \n     " + '\n     '.join(self.__book_to_str(i) for i in books)

    def get_command_result(self, person: Person, command: int) -> str:
        if command == 7:
            return 'Exit'

        if command == 1:
            return '\n'.join((self.__book_to_str(book) for book in self.__book_service.get_all()))

        if command == 2:
            book_atr = ConsoleReader.get_book_atr_for_search()
            str_generator = (self.__book_to_str(book) for book in
                             self.__book_service.get_by_author_and_title(book_atr.author, book_atr.title))
            return '\n'.join(str_generator)

        if command == 3:
            categories = self.__book_category_service.get_categories_with_books()
            return '\n'.join((self.__category_with_books_to_str(k, v) for k, v in categories.items()))

        if command == 4:
            return '\n'.join(
                (self.__book_to_str(book) for book in self.__person_book_service.get_books_by_person(person)))

        if command == 5:
            self.__return_book(person)
            return "Done"

        if command == 6:
            self.__get_book(person)
            return "Done"

        if person.is_admin() and command == 8:
            self.__create_person()
            return "Done"

        if person.is_admin() and command == 9:
            self.__create_book()
            return "Done"

        if person.is_admin() and command == 10:
            return '\n'.join((f"{category.id}:{category.info}" for category in self.__category_service.get_all()))

        if person.is_admin() and command == 11:
            self.__create_category()
            return "Done"

        if person.is_admin() and (command == 12 or command == 13):
            self.__change_book_category(command == 12)
            return "Done"

        if person.is_admin() and command == 14:
            self.__update_book_amount()
            return "Done"
