# Створити клас Calc, який буде мати атребут last_result та 4 методи. Методи повинні виконувати математичні операції
# з 2-ма числами, а саме додавання, віднімання, множення, ділення.
# - Якщо під час створення екземпляру класу звернутися до атребута last_result він повинен повернути пусте значення.
# - Якщо використати один з методів - last_result повенен повернути результат виконання ПОПЕРЕДНЬОГО методу.
#     Example:
#     last_result --> None
#     1 + 1
#     last_result --> None
#     2 * 3
#     last_result --> 2
#     3 * 4
#     last_result --> 6
#     ...
# - Додати документування в клас (можете почитати цю статтю:
# https://realpython.com/documenting-python-code/ )


class Calc:
    """
    A class used to calculate results of mathematical operations addition, subtraction, multiplication, and division.

    Attributes
    ----------
    __result : [int, float]
        result of execution of the current method.
    last_result : [int, float]
        result of execution of the previous method.

    Methods
    -------
    add(a: int, float, b: int, float)
        Calculated the result of the addition arguments a and b
    sub(a: int, float, b: int, float)
        Calculated the result of the subtraction arguments a and b
    mult(a: int, float, b: int, float)
        Calculated the result of the multiplication arguments a and b
    div(a: int, float, b: int, float)
        Calculated the result of the division arguments a and b
    """

    last_result = None

    def __init__(self):
        self.last_result = None
        self.__result = None

    def add(self, a: [int, float], b: [int, float]) -> [int, float]:
        """
        Calculated the result of the addition arguments a and b: a + b

        Parameters
        ----------
        :param a: int, float
        :param b: int, float

        Returns
        -------
        None
        """
        self.last_result, self.__result = self.__result, a + b

    def sub(self, a: [int, float], b: [int, float]) -> [int, float]:
        """
        Calculated the result of the subtraction arguments a and b: a - b

        Parameters
        ----------
        :param a: int, float
        :param b: int, float

        Returns
        -------
        None
        """
        self.last_result, self.__result = self.__result, a - b

    def mult(self, a: [int, float], b: [int, float]) -> [int, float]:
        """
        Calculated the result of the multiplication arguments a and b: a * b

        Parameters
        ----------
        :param a: int, float
        :param b: int, float

        Returns
        -------
        None
        """
        self.last_result, self.__result = self.__result, a * b

    def div(self, a: [int, float], b: [int, float]) -> [int, float]:
        """
        Calculated the result of the division arguments a and b: a / b.
        If b is 0, occur arithmetic exception: ZeroDivisionError.

        Parameters
        ----------
        :param a: int, float
        :param b: int, float

        Returns
        -------
        None
        """
        self.last_result, self.__result = self.__result, a / b


if __name__ == '__main__':
    calc = Calc()

    print(f"{calc.last_result}")
    calc.add(1, 1)
    print(f"{calc.last_result}")
    calc.mult(2, 3)
    print(f"{calc.last_result}")
    calc.mult(3, 4)
    print(f"{calc.last_result}")
