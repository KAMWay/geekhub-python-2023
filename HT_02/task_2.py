# Write a script which accepts two sequences of comma-separated colors from user. Then print out a set containing all
# the colors from color_list_1 which are not present in color_list_2.
#      e.g. "red  blue  red pink, withe  blue    black" --> {'red', 'pink'}

colors = input().split(',')
if len(colors) > 1:
    print(set(colors[0].split()).difference(colors[1].split()))
