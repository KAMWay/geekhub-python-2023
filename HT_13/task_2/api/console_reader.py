from HT_13.task_2.model.model import Person, Book, Entity


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
    def get_number(msg:str) -> int:
        try:
            number = int(input(msg))
            if 1 <= number:
                return number
            raise ValueError()
        except ValueError:
            print('Incorrect input. Try again.')

    @staticmethod
    def get_command(is_admin: bool = False) -> int:
        count_commands = 12 if is_admin else 7
        while True:
            print()
            print('----Available commands----')
            print('1. Books all')
            print('2. Find books')
            print('3. Books categories')
            print('4. Person books')
            print('5. Return book')
            print('6. Get book')
            print('7. Exit')

            if is_admin:
                print('8. Admin: add person')
                # print('9. Admin: add book')
                # print('10. Admin: add category')
                # print('11. Admin: set book amount')
                # print('12. Admin: set book category')

            print('------------------------')
            try:
                number = int(input(f"Enter command number [1..{count_commands}]:"))
                if 1 <= number <= count_commands:
                    return number
                raise ValueError()
            except ValueError:
                print('Incorrect input. Try again.')
