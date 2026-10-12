import re

userinput = input("Enter a string: ")

pattern = r"\d+"
result = re.findall(pattern, userinput)

if result:
    print(result)
else:
    print("No numbers found")



"""
Write a Python program using regular expressions to extract every sequence of one or more digits from a given string and print the extracted numbers in their original order.
Example 1
Input:
There are 12 errors, 3 warnings, and 45 retries in rack 7.
Expected output:
['12', '3', '45', '7']

"""