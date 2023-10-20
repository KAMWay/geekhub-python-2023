# Write a script to remove values duplicates from dictionary. Feel free to hardcode your dictionary.

some_dict = {'foo': 'bar', 'bar': 36, 'dou': 'bar', 'USD': 36, 'AUD': 19.2, 'name': 36}

temp_dict = {val: key for key, val in some_dict.items()}
for key in temp_dict.values():
    some_dict.pop(key)

# This can be realized by the following code (rewriting exist dictionary):
#       temp_dict = {val: key for key, val in some_dict.items()}
#       some_dict = {val: key for key, val in temp_dict.items()}
