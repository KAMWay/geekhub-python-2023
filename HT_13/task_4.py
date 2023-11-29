# 4. Create 'list'-like object, but index starts from 1 and index of 0 raises error. Тобто це повинен бути клас,
# який буде поводити себе так, як list (маючи основні методи), але індексація повинна починатись із 1

class CustomList(list):
    class _CustomIndex:
        def __getitem__(self, index):
            if isinstance(index, slice):
                new_key = slice(self.__get_index(index.start) if index.start else index.start,
                                self.__get_index(index.stop) if index.stop else index.stop,
                                index.step)
                return new_key

            return self.__get_index(index)

        def __get_index(self, index: int):
            if index == 0:
                raise IndexError("Index can't be 0")

            return index - 1 if index > 0 else index

    def __init__(self):
        super().__init__()
        self._index = CustomList._CustomIndex()

    def __getitem__(self, key):
        return super().__getitem__(self._index[key])

    def __setitem__(self, key, value):
        return super().__setitem__(self._index[key], value)

    def __delitem__(self, key):
        return super().__delitem__(self._index[key])

    def insert(self, index: int, val: any):
        super().insert(self._index[index], val)

    def index(self, value, start=..., stop=...):
        return super().index(value) + 1

    def pop(self, index=None):
        return super().pop(self._index[index]) if index else super().pop()


if __name__ == '__main__':
    cl = CustomList()
    cl.append(1)
    cl.append(2)
    cl.append(3)
    cl.append(4)
    cl.append(9)

    print(cl.index(1))
    cl.insert(1, 0)
    print(cl)
    print(cl.pop(1))
    print(cl.pop())
    print(cl)

    print(cl[1])
    print(cl[1:])
    print(cl[1:3])
    print(cl[::-1])

    try:
        print(cl[0])
    except IndexError as e:
        print(f"{e}")
