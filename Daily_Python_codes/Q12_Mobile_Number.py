import re

text = input("enter mobile number : ")

pattern = r"(91|\+91)?[6-9]\d{9}"

result = re.fullmatch(pattern, text)

if result:
    print("Valid mobile number")
else:
    print("INvalid mobile number")

