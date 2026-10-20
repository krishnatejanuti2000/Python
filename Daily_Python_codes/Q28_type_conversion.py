raw_values = ["12", "7", "abc", "", "-3", "8.5", " 20 "]

valid_integers = []
invalid_entries = []
total = 0

for value in raw_values:
    try:
        number = int(value)

        valid_integers.append(number)
        total += number

    except ValueError:
        invalid_entries.append(value)

print("Valid integers:", valid_integers)
print("Sum:", total)
print("Invalid entries:", invalid_entries)