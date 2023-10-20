# Write a script that will run through a list of tuples and replace the last value for each tuple.
# The list of tuples can be hardcoded. The "replacement" value is entered by user. The number of elements
# in the tuples must be different.

list_of_tuples = [(1, 2, 3), ('a', 100, 'c', 'd'), (6, 'b'), ('str',)]
item = input('Enter replacement value: ')
list_of_tuples = [item_tuple[:-1] + (item,) for item_tuple in list_of_tuples]
