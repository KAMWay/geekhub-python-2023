# Write a script which accepts two sequences of comma-separated colors from user. Then print out a set containing all
# the colors from color_list_1 which are not present in color_list_2.
#      e.g. red,magenta,blue --> red,green,blue --> {'magenta'}

color_list_1 = input('Enter the 1st sequence of comma-separated colors: ').split(',')
color_list_2 = input('Enter the 2nd sequence of comma-separated colors: ').split(',')
print(set(color_list_1).difference(color_list_2))
