# Write a script to remove values duplicates from dictionary. Feel free to hardcode your dictionary.

# some_dict = {'foo': 'bar', 'bar': 36, 'dou': 'bar', 'USD': 36, 'AUD': 19.2, 'name': 36}
some_dict = {'foo': ['bar'], 'bar': 36, 'dou': 'bar', 'USD': 36, 'AUD': 19.2, 'name': 36}

temp_val = []
temp_key = set()
for key, val in some_dict.items():
    temp_val.append(val) if val not in temp_val else temp_key.add(key)

[some_dict.pop(key) for key in temp_key]
