n = int(input("enter the size of the list : "))

numbers = []

for i in range(n):
    numbers.append(int(input(f"enter the element{i+1} : ")))

result = []

zero_count = 0

for i in numbers:
    if i != 0:
        result.append(i)
    else:
        zero_count += 1

for i in range(zero_count):
    result.append(0)


print(result)