from HT_13.task_2.model.model import Book, Category, CustomException
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

    def get_categories_by_book(self, book: Book) -> list[Category]:
        return self.__repository.get_by_book_id(book.id)

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

    def save(self, book: Book, category: Category):
        if any(i.id == category.id for i in self.get_categories_by_book(book)):
            raise CustomException("book have this category")

        self.__repository.insert(book.id, category.id)

    def delete(self, book: Book, category: Category):
        if not any(i.id == category.id for i in self.get_categories_by_book(book)):
            raise CustomException("book have not this category")

        self.__repository.delete(book.id, category.id)
