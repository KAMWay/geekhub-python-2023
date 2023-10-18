# Write a script which accepts a <number> from user and then <number> times asks user for string input.
# At the end script must print out result of concatenating all <number> strings.
#     e.g. "4 123 45 6 7890" --> 1234567890

print(''.join([input() for _ in range(int(input()))]))
