from HT_13.task_2.model.model import Person, Book, CustomException, Category


class ConsoleReader:
    @staticmethod
    def get_person() -> Person:
        print()
        print('------ Please ------')
        name = input('Enter person name: ')
        lastname = input('Enter person lastname: ')
        return Person(None, name, lastname)

    @staticmethod
    def get_book_atr_for_search() -> Book:
        print()
        print('------ Please ------')
        author = input('Enter book author: ')
        title = input('Enter book title: ')
        return Book(None, author, title, "", 0, 0)

    @staticmethod
    def get_category() -> Category:
        print()
        print('------ Please ------')
        info = input('Enter category info: ')
        return Category(None, info)

    @staticmethod
    def get_book() -> Book:
        print()
        print('------ Please ------')
        author = input('Enter book author: ')
        title = input('Enter book title: ')
        publisher_info = input('Enter publisher info: ')
        number = ConsoleReader.get_number('Enter number: ', 0)
        number_available = ConsoleReader.get_number('Enter available number: ', 0)
        return Book(None, author, title, publisher_info, number, number_available)

    @staticmethod
    def get_number(msg: str, min_value: int = 1) -> int:
        try:
            number = int(input(msg))
            if min_value <= number:
                return number
            raise ValueError()
        except ValueError:
            raise CustomException('Incorrect input. Try again.')

    @staticmethod
    def get_command(is_admin: bool = False) -> int:
        count_commands = 12 if is_admin else 7
        while True:
            print()
            print('----Available commands----')
            print('1. Books all')
            print('2. Find books')
            print('3. Books by categories')
            print('4. Person books')
            print('5. Return book')
            print('6. Get book')
            print('7. Exit')

            if is_admin:
                print('8. Admin: add person')
                print('9. Admin: add book')
                print('10. Admin: view categories')
                print('11. Admin: add category')
                # print('12. Admin: set book amount')
                # print('13. Admin: set book category')

            print('------------------------')
            try:
                number = int(input(f"Enter command number [1..{count_commands}]:"))
                if 1 <= number <= count_commands:
                    return number
                raise ValueError()
            except ValueError:
                print('Incorrect input. Try again.')
