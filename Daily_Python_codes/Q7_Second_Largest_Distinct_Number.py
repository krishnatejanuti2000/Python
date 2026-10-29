n = int(input("enter the size of the list : "))

input_list = []

for i in range(n):
  input_list.append(int(input(f"enter element{i+1} : ")))

largest = None
second_largest = None

for i in input_list:
  if largest is None:
    largest = i
  elif i > largest:
    second_largest = largest
    largest = i
  elif i < largest:
    if second_largest is None or  i > second_largest:
      second_largest = i

if second_largest is None:
  print(f"largest is {largest}")
  print("No second_largest number exist")
else:
  print(f"largest is {largest}")
  print(f"second largest is {second_largest}")

'''
def find_largest_disctinct(numbers):

    if not numbers or len(numbers)<2:

        return "No second-largest distinct number exists"

    largest = None
    second_largest = None

    for i in numbers:
        if largest is None:
            largest = i
        elif i > largest:
            second_largest = largest
            largest = i
        elif i < largest:
            if second_largest is None or i > second_largest:
                second_largest = i

    if second_largest is None:
        return "No second-largest distinct number exists"

    return f"Second-largest distinct number is : {second_largest}"




num = []
n = int(input("enter the size of list : "))

for i in range(n):
    num.append(int(input(f"enter the element{i+1} : ")))

print(find_largest_disctinct(num))

'''

"""
Write a Python program to find the second-largest distinct number in a list of integers.

Your program must identify the second-largest value that is different from the largest value.

### Example 1

Input:

```
numbers = [12, 45, 7, 45, 32, 18]
```

Expected output:

```
Second-largest distinct number: 32
```

Explanation: The largest number is `45`, and the second-largest distinct number is `32`.

### Example 2

Input:

```
numbers = [10, 10, 8, 8, 5]
```

Expected output:

```
Second-largest distinct number: 8
```

Explanation: Repeated occurrences of `10` do not make `10` the second-largest distinct number. The answer is `8`.

### Example 3

Input:

```
numbers = [5, 5, 5, 5]
```

Expected output:

```
No second-largest distinct number exists
```

### Constraints

1. Do not use `max()`, `min()`, `sort()`, or `sorted()`.
2. Use loops and conditional statements.
3. Handle duplicate values correctly.
4. Support negative numbers.
5. Handle lists containing fewer than two distinct values.
6. Do not hard-code the answer.

"""