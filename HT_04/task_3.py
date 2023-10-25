# Create a Python script that takes an age as input. If the age is less than 18 or greater than 120,
# raise a custom exception called InvalidAgeError. Handle the InvalidAgeError by displaying
# an appropriate error message.

class InvalidAgeError(Exception):
    min_age = 18
    max_age = 120

    def __init__(self, age, *args):
        super().__init__(args)
        self.age = age

    def __str__(self):
        return f'The age {self.age} is not in a valid range {self.min_age, self.max_age}'


age = input('Enter integer number: ')
try:
    age = int(age)
    if age < 18 or age > 120:
        raise InvalidAgeError(age)
except ValueError:
    print(f'{age} is not integer number')
except InvalidAgeError as e:
    print(f'Invalid age error: {e}')
