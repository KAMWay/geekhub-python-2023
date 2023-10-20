# Write a script to concatenate following dictionaries to create a new one.
#   dict_1 = {'foo': 'bar', 'bar': 'buz'}
#   dict_2 = {'dou': 'jones', 'USD': 36}
#   dict_3 = {'AUD': 19.2, 'name': 'Tom'}

dict_1 = {'foo': 'bar', 'bar': 'buz'}
dict_2 = {'dou': 'jones', 'USD': 36}
dict_3 = {'AUD': 19.2, 'name': 'Tom'}

merged_dict = {}
for dict_item in [dict_1, dict_2, dict_3]:
    for key, value in dict_item.items():
        merged_dict[key] = value

# This can be realized by the following method:
#   merged_dict = {**dict_1, **dict_2, **dict_3}
