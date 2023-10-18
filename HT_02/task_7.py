# Write a script to concatenate all elements in a list into a string and print it. List must be include both strings
# and integers and must be hardcoded.
#      e.g. [1, 2, '3', 4, '567', 890] --> '1234567890'

print(''.join(map(str, [1, 2, '3', 4, '567', 890])))
