class CustomException(Exception):
    pass


class Entity:
    def __init__(self, _id: [int, None] = None):
        self.__id = _id

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, _id: int):
        self.__id = _id

    def is_new(self) -> bool:
        return self.__id is None


class Person(Entity):
    def __init__(self, _id: [int, None], name: str, lastname: str, role: str = 'STUDENT'):
        super().__init__(_id)
        self.__name = name
        self.__lastname = lastname
        self.__role = role

    @property
    def name(self) -> str:
        return self.__name

    @property
    def lastname(self) -> str:
        return self.__lastname

    @property
    def role(self) -> str:
        return self.__role

    @role.setter
    def role(self, role: str):
        self.__role = role

    def is_admin(self):
        return self.__role == 'ADMIN'

    def __hash__(self):
        return hash(
            (self.id, self.__name, self.__lastname, self.__role))

    def __eq__(self, other):
        if self is other:
            return True
        if other is None or type(self) is not type(other):
            return False

        return (self.id == other.id and self.__name == other.name and self.__lastname == other.lastname
                and self.__role == other.role)


class Book(Entity):
    def __init__(self, _id: [int, None], author: str, title: str, publisher_info: str, number: int,
                 number_available: int):
        super().__init__(_id)

        self.__author = author
        self.__title = title
        self.__publisher_info = publisher_info
        self.__number = number
        self.__number_available = number_available

    @property
    def author(self) -> str:
        return self.__author

    @property
    def title(self) -> str:
        return self.__title

    @property
    def publisher_info(self) -> str:
        return self.__publisher_info

    @property
    def number(self) -> int:
        return self.__number

    @number.setter
    def number(self, number: int):
        self.__number = number

    @property
    def number_available(self) -> int:
        return self.__number_available

    @number_available.setter
    def number_available(self, number: int):
        self.__number_available = number

    def __eq__(self, other):
        if self is other:
            return True
        if other is None or type(self) is not type(other):
            return False

        return (self.id == other.id and self.__author == other.author and self.__title == other.title
                and self.__publisher_info == other.publisher_info and self.__number == other.number
                and self.__number_available == other.number_available)

    def __hash__(self):
        return hash(
            (self.id, self.__author, self.__title, self.__publisher_info, self.__number, self.__number_available))

    def __str__(self):
        return f"id:{self.id} title:{self.title} number:{self.number} available:{self.__number_available}"


class Category(Entity):
    def __init__(self, _id: [int, None], info: str):
        super().__init__(_id)
        self.__info = info

    @property
    def info(self) -> str:
        return self.__info

    @info.setter
    def info(self, info):
        self.__info = info

    def __str__(self):
        return f"{self.id}:{self.__info}"

    def __hash__(self):
        return hash(
            (self.id, self.__info))

    def __eq__(self, other):
        if self is other:
            return True
        if other is None or type(self) is not type(other):
            return False

        return self.id == other.id and self.__info == other.info


if __name__ == '__main__':
    ...
