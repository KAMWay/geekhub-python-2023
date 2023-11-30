from HT_13.task_2.model.model import Category
from HT_13.task_2.repository.category_repository import CategoryRepository


class CategoryService:
    def __init__(self):
        self.__repository = CategoryRepository()

    def get_all(self) -> list[Category]:
        return self.__repository.get_all()

    def get_by_id(self, _id: int) -> [Category, None]:
        return self.__repository.get_by_id(_id)

    def save(self, category: Category):
        if category.is_new():
            self.__repository.insert(category)
        else:
            self.__repository.update(category)

