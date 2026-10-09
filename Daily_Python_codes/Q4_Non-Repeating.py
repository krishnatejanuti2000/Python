userinput = input("Enter the string: ")

char_count = {}


for i in userinput:
    char_count[i] = char_count.get(i, 0) + 1


found = False

for i in userinput:
    if char_count[i] == 1:
        print("First non-repeating character:", i)
        found = True
        break

if not found:
    print("No non-repeating character found")