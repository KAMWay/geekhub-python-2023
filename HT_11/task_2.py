# Створити клас Person, в якому буде присутнім метод __init__ який буде приймати якісь аргументи,
# які зберігатиме в відповідні змінні.
# - Методи, які повинні бути в класі Person - show_age, print_name, show_all_information.
# - Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть атребут profession (його не має інсувати
# під час ініціалізації).


class Person:
    def __init__(self, age: int, name: str):
        self.__age = age
        self.__name = name

    def show_age(self) -> int:
        return self.__age

    def print_name(self) -> str:
        return self.__name

    def show_all_information(self) -> dict:
        return self.__dict__


if __name__ == '__main__':
    person1 = Person(18, 'Tom')
    person2 = Person(25, 'Jerry')

    person1.profession = 'cat'
    person2.profession = 'mouse'

    print(person1.show_all_information())
    print(person2.show_all_information())
