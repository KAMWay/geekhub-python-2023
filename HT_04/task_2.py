# Create a custom exception class called NegativeValueError. Write a Python program that takes an integer as input and
# raises the NegativeValueError if the input is negative. Handle this custom exception with a try/except block
# and display an error message.

class NegativeValueError(Exception):
    pass


number = input('Enter integer number: ')
try:
    number = int(number)
    if number < 0:
        raise NegativeValueError()
except ValueError:
    print(f'{number} is not integer number')
except NegativeValueError:
    print(f'Enter number {number} is negative')
