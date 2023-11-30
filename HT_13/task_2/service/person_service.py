from HT_13.task_2.model.model import Person, CustomException
from HT_13.task_2.repository.person_repository import PersonRepository


class PersonService:
    def __init__(self):
        self.__repository = PersonRepository()

    def get_all(self) -> list[Person]:
        return self.__repository.get_all()

    def get_by_name(self, name: str, lastname: str) -> [Person, None]:
        return self.__repository.get_by_name(name, lastname)

    def save(self, person: Person):
        self.__validate(person)

        person.role = person.role.upper()
        if self.__repository.get_by_name(person.name, person.lastname):
            self.__repository.update(person)
        else:
            self.__repository.insert(person)

    def __validate(self, person: Person):
        if not person.name or len(person.name) == 0:
            raise CustomException("person name can't be empty")

        if not person.lastname or len(person.lastname) == 0:
            raise CustomException("person lastname can't be empty")

        if not person.role or person.role not in self.get_roles():
            raise CustomException(f"not allowed person role {self.get_roles()}")

    @staticmethod
    def get_roles():
        return ['ADMIN', 'STUDENT', 'TEACHER']
