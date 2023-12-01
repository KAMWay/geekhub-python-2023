# 4. Create 'list'-like object, but index starts from 1 and index of 0 raises error. Тобто це повинен бути клас,
# який буде поводити себе так, як list (маючи основні методи), але індексація повинна починатись із 1

class CustomList(list):
    def __init__(self):
        super().__init__()

    def __getitem__(self, key):
        if isinstance(key, slice):
            new_key = slice(self.__get_index(key.start), self.__get_index(key.stop), key.step)
            return super().__getitem__(new_key)
        return super().__getitem__(self.__get_index(key))

    @staticmethod
    def __get_index(index: int):
        if index is None:
            return index
        if index == 0:
            raise IndexError("Index can't be 0")
        return index - 1 if index > 0 else index

    def insert(self, index: int, val: any):
        super().insert(self.__get_index(index), val)

    def pop(self, index=None):
        return super().pop(self.__get_index(index)) if index else super().pop()


if __name__ == '__main__':
    cl = CustomList()
    cl.append(1)
    cl.append(2)
    cl.append(3)
    cl.append(4)
    cl.append(9)

    print(cl)
    print(cl.index(1))
    cl.insert(1, 0)
    print(cl)
    print(cl.pop(1))
    print(cl.pop())
    print(cl)

    print(cl[1])
    print(cl[1:])
    print(cl[1:10])

    print(cl[1:3])
    print(cl[::-1])

    try:
        print(cl[0])
    except IndexError as e:
        print(f"{e}")
