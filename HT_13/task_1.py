# 1. Напишіть програму, де клас «геометричні фігури» (Figure) містить властивість color
# з початковим значенням white і метод для зміни кольору фігури, а його підкласи «овал» (Oval)
# і «квадрат» (Square) містять методи __init__ для завдання початкових розмірів об'єктів при їх створенні.


class Figure:
    def __init__(self):
        self.__color = 'white'

    @property
    def color(self) -> str:
        return self.__color

    @color.setter
    def color(self, color: str):
        self.__color = color


class Oval(Figure):

    def __init__(self, width: [int, float], height: [int, float]):
        super().__init__()
        self.__width = width
        self.__heigth = height

    @property
    def width(self) -> [int, float]:
        return self.__width

    @property
    def heigth(self) -> [int, float]:
        return self.__heigth

    @width.setter
    def width(self, width: [int, float]):
        self.__width = width

    @heigth.setter
    def heigth(self, heigth: [int, float]):
        self.__heigth = heigth


class Square(Figure):

    def __init__(self, side: [int, float]):
        super().__init__()
        self.__side = side

    @property
    def side(self) -> [int, float]:
        return self.__side

    @side.setter
    def side(self, side: [int, float]):
        self.__side = side


if __name__ == '__main__':
    figure = Figure()
    print(figure.color)
    figure.color = "red"
    print(figure.color)

    oval = Oval(10, 20)
    print(f"width:{oval.width} heigth: {oval.heigth} color:{oval.color}")
    oval.width, oval.heigth, oval.color = 25, 35, 'red'
    print(f"width:{oval.width} heigth: {oval.heigth} color:{oval.color}")

    square = Square(10)
    print(f"side:{square.side} color:{oval.color}")
    square.side, oval.color = 25, 'red'
    print(f"side:{square.side} color:{square.color}")

#
#
#
#
#
#
#
#
#
#
#
#
#
#
# 2. Створіть за допомогою класів та продемонструйте свою реалізацію шкільної бібліотеки (включіть фантазію).
# Наприклад вона може містити класи Person, Teacher, Student, Book, Shelf, Author, Category і.т.д.
#
# 3. Створіть клас в якому буде атребут який буде рахувати кількість створених екземплярів класів.
#
# 4. Create 'list'-like object, but index starts from 1 and index of 0 raises error. Тобто це повинен бути клас,
# який буде поводити себе так, як list (маючи основні методи), але індексація повинна починатись із 1
