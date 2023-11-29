# 3. Створіть клас в якому буде атребут який буде рахувати кількість створених екземплярів класів.

class SomeClass:
    __create_count = 0

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        cls.__create_count += 1
        return self

    @property
    def create_count(self):
        return self.__create_count


if __name__ == '__main__':
    SomeClass()
    SomeClass()
    SomeClass()
    print(SomeClass().create_count)
