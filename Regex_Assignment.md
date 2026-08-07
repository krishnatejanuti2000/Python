## 1. What are metacharacters in regex? List five commonly used ones.

## 2. Explain the difference between `*` and `+` quantifiers in regex.

## 3. What does the `.` (dot) character match in a regular expression? Are there any exceptions?

## 4. What is the role of anchors like `^` and `$` in regex?

## 5. What is the difference between greedy and non-greedy quantifiers in regex? Give an example.

## 6. What is the purpose of character classes like `[a-z]`, `[0-9]`, or `\w`?

## 7. How do regular expressions handle Unicode characters?

## 8. Explain the concept of backreferences in regex.

## 9. What is the `re` module used for in Python?

## 10. How do you import the `re` module in a Python script?

## 11. List important functions provided by the `re` module.

## 12. What is the difference between `re.search()` and `re.match()`?

## 13. What is the difference between `re.finditer()` and `re.findall()`?

## 14. What is the difference between `group()` and `groups()`?

## 15. What is the difference between `re.sub()` and `re.subn()`?

## 16. Explain the use of `re.split()`. How is it different from the `split()` method of a string?

## 17. What does the `re.IGNORECASE` flag do? Provide an example of its use.

## 18. Explain all the metacharacters used in `re`.

## 19. What is the use of the following? Explain with an example.

## 20. Write the regex pattern and complete Python code for the following scenarios.

### 20.1 Write a regex to check whether a given string contains digits or not.

### 20.2 Write a regex to check whether a given string contains alphabets.

### 20.3 Write a regex to check whether a given number is in the range **0 to 255**.


### 20.4 Write a regex to validate an email address.
```python
import re

text = input("enter the email : ")

pattern = r"^(?!.*\.\.)(?!.*\+\+)[A-Za-z0-9]([A-Za-z0-9.+_-]*[A-Za-z0-9])?@(gmail|winteck)\.(com|org|in)

result = re.match(pattern, text)

if result:
    print("Valid Email")
else:
    print("Invalid Email")
```
### 20.5 Write a regex to validate an IPv4 address.

```python

import re

text = input("Enter the IP address : ")

octet = r"(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)"

pattern = rf"^{octet}\.{octet}\.{octet}\.{octet}$"

result = re.match(pattern, text)

if result:
    print("Valid IP address")
else:
    print("Invalid IP address")
```
### 20.6 Write a regex to extract all IPv4 addresses from a given text file.
```python
import re

text = input("Enter the IP address : ")

pattern = r"^(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)$"

result = re.match(pattern, text)

if result:
    print(f"full match is : {result.group(0)}")
    print(f"first octet is : {result.group(1)}")
    print(f"second octet is : {result.group(2)}")
    print(f"third octet is : {result.group(3)}")
    print(f"fourth octet is : {result.group(4)}")
else:
    print("Invalid IP address")
```
### 20.7 Write a regex to validate a MAC address.

#for Linux
```python
import re

text = input("enter the MAC address : ")

group = r"([A-Fa-f0-9]{2})"

pattern = rf"^{group}:{group}:{group}:{group}:{group}:{group}$"

result = re.match(pattern, text)

if result:
    print("Valid MAC address")
else:
    print("Invalid MAC address")

```
#for windows
```python
import re

text = input("enter the MAC address : ")

group = r"([A-Fa-f0-9]{2})"

pattern = rf"^{group}-{group}-{group}-{group}-{group}-{group}$"

result = re.match(pattern, text)

if result:
    print("Valid MAC address")
else:
    print("Invalid MAC address")

```
#for cisco
```python
import re

text = input("enter the MAC address : ")

group = r"([A-Fa-f0-9]{4})"

pattern = rf"^{group}\.{group}\.{group}$"

result = re.match(pattern, text)

if result:
    print("Valid MAC address")
else:
    print("Invalid MAC address")
```

### 20.8 Write a regex to validate a password with the following conditions:

- At least 8 characters long.
- Contains at least one uppercase letter.
- Contains at least one lowercase letter.
- Contains at least one digit.
- Contains at least one special character.
- Does not contain spaces.

```python
import re

text = input("enter the password")

pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+=-])(?!.*\s).{8,}$"

result = re.match(pattern, text)

if result:
    print("Valid password")
else:
    print("Invalid password")
```

### 20.9 Write a regex to validate a mobile number.
```python
import re

text = input("enter the mobile number : ")

pattern = r"^(91|\+91)?([6-9]\d{9})$"

result = re.match(pattern, text)

if result:
    print("Valid Mobile number")
else:
    print("Invalid Mobile number")
```
### 20.10 Replace all instances of multiple spaces with a single space in a given string.

**Example:**

```text
"My    name    is    python"
```

```python
import re

text = "My    name    is    python"

result = re.sub(r"\s+", r" ", text)

print(result)
```

### 20.11 Using regex, format a given list of dates from **MM/DD/YYYY** to **YYYY-MM-DD**.

#using capturing groups
```python
import re
n = int(input("enter the size of the list : "))

dates = []

for i in range(n):
    dates.append(input(f"enter the date{i+1} : "))

result = []

for date in dates:
    formatted_date = re.sub(r"(\d{2})/(\d{2})/(\d{4})", r"\3-\1-\2", date)
    result.append(formatted_date)

print(result)
```

#using named capturing groups

```python
import re
n = int(input("enter the size of the list : "))

dates = []

for i in range(n):
    dates.append(input(f"enter the date{i+1} : "))

result = []

for date in dates:
    formatted_date = re.sub(r"(?P<month>\d{2})/(?P<day>\d{2})/(?P<year>\d{4})", r"\g<year>-\g<month>-\g<day>", date)
    result.append(formatted_date)

print(result)
```
### 20.12 Write a regex to validate a date.

**Example:**

```text
24-08-2024
```
```python
import re

text = input("enter the date in (DD/MM/YYYY) format : ")

pattern = r"^(0[1-9]|1[0-9]|2[0-9]|3[0-1])/(0[1-9]|1[0-2])/(19\d{2}|20\d{2})$"

result = re.match(pattern, text)

if result:
    print("Valid Date")
else:
    print("Invalid Date")

```
### 20.13 Extract drive names into a list.

```python
drive_names = "Drive1 /dev/sda , Drive2 /dev/sdb"
```

### 20.14 Extract the PCI address.

```python
str1 = "PCI address is 0a.1.1"
```

### 20.15 Create a dictionary from the following string.

```python
str2 = "Drive name /dev/sda capacity 500GB type HDD"
```

**Expected Output**

```python
{
    "Drive name": "/dev/sda",
    "capacity": "500GB",
    "type": "HDD"
}
```
