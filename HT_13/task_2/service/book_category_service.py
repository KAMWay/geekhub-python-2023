from HT_13.task_2.model.model import Book, Category
from HT_13.task_2.repository.book_category_repository import BookCategoryRepository


class BookCategoryService:
    def __init__(self):
        self.__repository = BookCategoryRepository()

    def get_books_with_categories(self) -> dict[Book:list[Category]]:
        books_dict = {}
        for item_dict in self.__repository.get_all():
            for book, category in item_dict.items():
                categories = books_dict.get(book)
                if categories:
                    categories.append(category)
                else:
                    books_dict[book] = [category]
        return books_dict

    def get_categories_with_books(self) -> dict[Category:list[Book]]:
        categories_dict = {}
        for item_dict in self.__repository.get_all():
            for book, category in item_dict.items():
                books = categories_dict.get(category)
                if books:
                    books.append(book)
                else:
                    categories_dict[category] = [book]

        return categories_dict

    def save(self, book_id: int, category_id: int):
        self.__repository.insert(book_id, category_id)

    def delete(self, book_id: int, category_id: int):
        self.__repository.delete(book_id, category_id)
