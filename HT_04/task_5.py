# Create a Python program that repeatedly prompts the user for a number until a valid integer is provided.
# Use a try/except block to handle any ValueError exceptions, and keep asking for input until a valid integer
# is entered. Display the final valid integer.

is_ok = False
while not is_ok:
    number = input('Enter integer number: ')
    try:
        number = int(number)
    except ValueError:
        print(f'{number} is not valid integer number. Try again.')
    else:
        is_ok = True
        print(f'{number} is integer number')
