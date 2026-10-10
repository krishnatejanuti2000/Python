import re

userinput = input("Enter the IPv4 address: ")

pair = r"(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)"

pattern = rf"{pair}\.{pair}\.{pair}\.{pair}"

result = re.fullmatch(pattern, userinput)

if result:
    print("Valid IPv4 address")
else:
    print("Invalid IPv4 address")


##Write a Python program using regular expressions to accept a valid IPv4 address and reject an invalid IPv4 address.
