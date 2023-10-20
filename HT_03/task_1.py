# Write a script that will run through a list of tuples and replace the last value for each tuple.
# The list of tuples can be hardcoded. The "replacement" value is entered by user. The number of elements
# in the tuples must be different.
#     e.g. (1, 2, 3), (a, 100, c, d), (6, b), () --> reply
#          --> [('1', '2', 'reply'), ('a', '100', 'c', 'reply'), ('6', 'reply'), ()]

list_of_tuples = []
for item in input('Enter list of tuples split by comma: ').split('), ('):
    item = item.replace('(', '').replace(')', '')
    list_of_tuples.append(() if not item else tuple(item.split(', ')))

item = input('Enter replacement value: ')
list_of_tuples = [item_tuple[:-1] + (item,) if len(item_tuple) > 0 else item_tuple for item_tuple in list_of_tuples]
print(list_of_tuples)
