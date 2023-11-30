from HT_13.task_2.model.model import Book, CustomException
from HT_13.task_2.repository.book_repository import BookRepository


class BookService:
    def __init__(self):
        self.__repository = BookRepository()

    def get_all(self) -> list[Book]:
        return self.__repository.get_all()

    def get_by_author_and_title(self, author: str, title: str) -> list[Book]:
        return list(filter(lambda i: author in i.author and title in i.title, self.get_all()))

    def get_by_id(self, _id: int) -> [Book, None]:
        book = self.__repository.get_by_id(_id)

        if not book:
            raise CustomException("book not found")

        return self.__repository.get_by_id(_id)

    def save(self, book: Book):
        if book.number_available > book.number:
            raise CustomException("available book can't be more then total number")

        if book.number_available < 0:
            raise CustomException("available book can't be negative")

        if book.is_new():
            self.__repository.insert(book)
        else:
            self.__repository.update(book)
