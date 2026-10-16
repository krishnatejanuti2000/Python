#without using slicing

n = int(input("Enter the size of the list: "))

numbers = []

for i in range(n):
    numbers.append(int(input(f"Enter element {i + 1}: ")))

k = int(input("Enter the value of k to rotate: "))

right_rotate = numbers.copy()
left_rotate = numbers.copy()

if numbers:
    k = k % len(numbers)

    # Right rotation
    for i in range(k):
        right_rotate.insert(0, right_rotate[-1])
        right_rotate.pop()

    # Left rotation
    for i in range(k):
        left_rotate.append(left_rotate[0])
        left_rotate.pop(0)

print("Original list:", numbers)
print("Right rotation:", right_rotate)
print("Left rotation:", left_rotate)


#with slicing:

# n = int(input("Enter the size of the list: "))

# numbers = []

# for i in range(n):
#     numbers.append(int(input(f"Enter element {i + 1}: ")))

# k = int(input("Enter the value of k to rotate: "))

# right_rotate = []
# left_rotate = []

# if numbers:
#     k = k % len(numbers)

#     right_rotate = numbers[-k:] + numbers[:-k]
#     left_rotate = numbers[k:] + numbers[:k]

# print("Right rotation:", right_rotate)
# print("Left rotation:", left_rotate)
