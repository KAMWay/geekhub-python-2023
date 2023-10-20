# Write a script to get the maximum and minimum value in a dictionary.

some_dict = {'foo': 10, 'bar': 36, 'dou': 3.8, 'USD': 5, 'AUD': 19.2, 'name': 36}

print(max(some_dict.values()))
print(min(some_dict.values()))

# This can be realized by the following code (if values of different type):
#   print(max(map(str, some_dict.values())))
#   print(min(map(str, some_dict.values())))
