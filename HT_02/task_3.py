# Write a script which accepts a <number> from user and print out a sum of the first <number> positive integers.
#      e.g. "5" --> 15

print(sum(range(int(input('Enter the number: ')) + 1)))
