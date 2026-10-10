import re

text = input("Enter the MAC address :")


pair = r"[A-Fa-f0-9]{2}"

pattern = rf"{pair}(?P<sep>[:-]){pair}(?P=sep){pair}(?P=sep){pair}(?P=sep){pair}(?P=sep){pair}"

result = re.fullmatch(pattern, text)

if result:
    print("Valid MAC address")
else:
    print("Invalid MAC address")

"""
Write a Python program using regular expressions to validate whether the input is a valid MAC address.
A MAC address must contain exactly six hexadecimal pairs. The pairs may be separated by colons (:) or hyphens (-), but the same separator must be used throughout.
Examples
Input	Expected result
00:1A:2B:3C:4D:5E	Valid
aa:bb:cc:dd:ee:ff	Valid
00-1A-2B-3C-4D-5E	Valid
00:1A:2B:3C:4D	Invalid
00:1A:2B:3C:4D:5G	Invalid
00:1A-2B:3C:4D:5E	Invalid
001A:2B:3C:4D:5E	Invalid
Constraints
- Use Python's re module.
- Do not use a library that directly validates MAC addresses.
- Accept uppercase and lowercase hexadecimal characters.
- Validate the entire input, not just a matching substring.
- Print Valid MAC address or Invalid MAC address.
"""
