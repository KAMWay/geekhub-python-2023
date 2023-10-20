# Write a script which accepts a <number> from user and then <number> times asks user for string input.
# At the end script must print out result of concatenating all <number> strings.
#     e.g. 4 --> 123 --> ab --> 6 --> cd --> 123ab6cd

print(''.join([input(f'Enter the {i + 1} string: ') for i in range(int(input("Input number: ")))]))
