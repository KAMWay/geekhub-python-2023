# Write a script which accepts a <number> from user and generates dictionary in range <number> where key is <number>
# and value is <number>*<number>
#     e.g. 3 --> {0: 0, 1: 1, 2: 4, 3: 9}

some_dict = {i: i * i for i in range(int(input("Input number: ")) + 1)}
