# Write a script which accepts a sequence of comma-separated numbers from user
# and generate a list and a tuple with those numbers.
#      e.g. "1,2 ,3.6,  5, 7." --> (1, 2, 3.6, 5, 7.0)

number_list = []
for number in input().replace(' ', '').split(','):
    number_list.append(float(number) if '.' in number else int(number))
number_tuple = tuple(number_list)
