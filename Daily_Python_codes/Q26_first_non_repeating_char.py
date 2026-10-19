text = input("enter the string : ")

frequency = {}

for char in text:
    if char not in frequency:
        frequency[char] = 1
    else:
        frequency[char] += 1

for char in text:
    if frequency[char] == 1:
        print(char)
        break
else:
    print("None")

