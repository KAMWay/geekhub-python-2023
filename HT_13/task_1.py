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
