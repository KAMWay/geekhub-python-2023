# Write a script to get the maximum and minimum value in a dictionary.

# some_dict = {'foo': 10, 'bar': 36, 'dou': 3.8, 'USD': 5, 'AUD': 19.2, 'name': 36}
# print(max(some_dict.values()))
# print(min(some_dict.values()))

# some_dict = {'foo': '10', 'bar': 36, 'dou': 3.8, 'USD': 5, 'AUD': 19.2, 'name': 36}
# print(max(map(str, some_dict.values())))
# print(min(map(str, some_dict.values())))

some_dict = {'foo': [10], 'bar': 36, 'dou': 3.8, 'USD': 5, 'AUD': 19.2, 'name': '36'}

value_list = [item for item in some_dict.values() if isinstance(item, (int, float))]
print(max(value_list))
print(min(value_list))
