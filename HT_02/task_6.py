# Write a script to check whether a value from user input is contained in a group of values.
#     e.g. [1, 2, 'u', 'a', 4, True] --> 2 --> True
#          [1, 2, 'u', 'a', 4, True] --> 5 --> False

value = input()
print((int(value) if value.isdigit() else value) in [1, 2, 'u', 'a', 4, True])
