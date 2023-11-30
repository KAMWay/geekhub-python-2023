from HT_13.task_2.model.model import Category, CustomException
from HT_13.task_2.repository.category_repository import CategoryRepository


class CategoryService:
    def __init__(self):
        self.__repository = CategoryRepository()

    def get_all(self) -> list[Category]:
        return self.__repository.get_all()

    def get_by_id(self, _id: int) -> [Category, None]:
        return self.__repository.get_by_id(_id)

    def save(self, category: Category):
        self.__validate(category)

        category.info = category.info.lower()
        if category.is_new():
            self.__repository.insert(category)
        else:
            self.__repository.update(category)

    def __validate(self, category: Category):
        if not category.info or len(category.info) == 0:
            raise CustomException("book author can't be empty")

        if category.is_new() and any(i.info.lower() == category.info.lower() for i in self.get_all()):
            raise CustomException("category already exist")
