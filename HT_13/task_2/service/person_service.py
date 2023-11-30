from HT_13.task_2.model.model import Person
from HT_13.task_2.repository.person_repository import PersonRepository


class PersonService:
    def __init__(self):
        self.__repository = PersonRepository()

    def get_all(self) -> list[Person]:
        return self.__repository.get_all()

    def get_by_name(self, name: str, lastname: str) -> [Person, None]:
        return self.__repository.get_by_name(name, lastname)

    def save(self, person: Person):
        if self.__repository.get_by_name(person.name, person.lastname):
            self.__repository.update(person)
        else:
            self.__repository.insert(person)
