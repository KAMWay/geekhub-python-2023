# 2. Створіть за допомогою класів та продемонструйте свою реалізацію шкільної бібліотеки (включіть фантазію).
# Наприклад вона може містити класи Person, Teacher, Student, Book, Shelf, Author, Category і.т.д.
from HT_13.task_2.api.console_reader import ConsoleReader
from HT_13.task_2.model.model import CustomException
from HT_13.task_2.service.library_service import LibraryService


def start():
    library_service = LibraryService()
    person = library_service.get_person()
    # person = PersonService().get_by_name("admin", "admin")

    if not person:
        print('Person not found')

    while person:
        command = ConsoleReader.get_command(person.is_admin())

        try:
            rez = library_service.get_command_result(person, command)
            print('- - -  Result  - - - - -')
            print(rez)
            print('- - - - -  - - - - - - -')
            if rez == 'Exit':
                break
        except CustomException as e:
            print(f'Command exception: {e}')

    print('Program complete')


if __name__ == '__main__':
    start()
