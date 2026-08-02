# Python Functions

## 1. What is a function in Python?

A function in Python is a block of reusable code that performs a specific task, Instead of writing the same code again and again, we define it once inside a function and call it whenever required.

## 2. How do you define a function in Python?
syntax:-

def function_name():
    #fucntion body
    return value

ex:-

def greet():
    print("Hello, Python!")

greet()

#Output
Hello, Python!

## 3. How do you call a function in Python?

A function in Python is called by writing its name followed by parentheses `()`. When the function is called, Python transfers control to the function, executes the statements inside it, and then returns to the point where it was called.

ex:-

def greet():
   return "Hello"
#calling
result = greet()
print(result)

#output
Hello

## 4. What is the purpose of the `return` statement in a function?

The `return` statement is used to send a value back to the caller after a function completes its execution. It also terminates the function immediately, meaning any code after the `return` statement inside the function is not executed.

## 5. What are the different types of arguments that a function allows?

Python functions support different types of arguments to provide flexibility while calling a function. The different types of arguments are:

a). Positional Arguments
b). Keyword Arguments
c). Default Arguments
d). Variable-Length Arguments (`*args`)
e). Keyword Variable-Length Arguments (`**kwargs`)

## 6. What is the sequence of arguments that a function accepts?

When defining a function in Python, the parameters must follow a specific order. Following this sequence ensures that the function definition is valid and avoids syntax errors.

### Sequence of Function Arguments

a). Positional Arguments
b). Default Arguments
c). Variable-Length Positional Arguments (`*args`)
d). Keyword-Only Arguments (optional, after `*args`)
e). Variable-Length Keyword Arguments (`**kwargs`)


## 7. Can you explain the difference between positional arguments and keyword arguments?

| Positional Arguments | Keyword Arguments |
|----------------------|-------------------|
| Values are passed based on position. | Values are passed using parameter names. |
| Order of arguments is important. | Order of arguments is not important. |
| Simpler for functions with fewer parameters. | More readable for functions with many parameters. |
| Incorrect order may produce incorrect results. | Parameter names ensure correct assignment. |


## 8. What are default arguments in Python functions? Give an example.

Default arguments are function parameters that are assigned a default value during function definition. If the caller does not provide a value for that parameter, Python automatically uses the default value.

# Example

def add(a, b=10):
    return a + b

print(add(5))
print(add(5, 20))

# Output
15
25

## 9. What is the scope of a variable inside a function? Explain with examples.

The scope of a variable refers to the region of a program where a variable can be accessed. In Python, variables can have Local Scope or Global Scope.
# 1. Local Scope

A variable declared inside a function is called a local variable. It can be accessed only within that function.
# Example

def display():
    message = "Hello Python"
    print(message)

display() #Hello Python

print(message) #NameError: name 'message' is not defined

Reason: `message` is a local variable and exists only inside the function.

# 2. Global Scope

A variable declared outside all functions is called a global variable. It can be accessed from anywhere in the program.

# Example

name = "Revanth"

def display():
    print(name)

display()
print(name)

# Output

Revanth
Revanth


## 10. How can you pass a variable number of arguments to a function?

In Python, a variable number of arguments can be passed to a function using `*args` and `**kwargs`.

- `*args` is used to accept a variable number of positional arguments.
- `**kwargs`is used to accept a variable number of keyword arguments.

---

## 1. Using `*args`

`*args` allows a function to accept any number of positional arguments. The arguments are stored as a tuple.

## 2. Using `**kwargs`

`**kwargs` allows a function to accept any number of keyword arguments. The arguments are stored as a dictionary.


## 11. What is the difference between `*args` and `**kwargs`?

| `*args` | `**kwargs` |
|---------|------------|
| Accepts variable number of positional arguments. | Accepts variable number of keyword arguments. |
| Stores arguments as a tuple. | Stores arguments as a dictionary. |
| Arguments are passed without parameter names. | Arguments are passed with parameter names. |
| Represented using a single asterisk (`*`). | Represented using a double asterisk (`**`). |


## 12. What does the `lambda` keyword do in Python? How does it differ from a regular function?

The `lambda` keyword is used to create an anonymous (unnamed) function in Python. Lambda functions are generally used for small, simple operations where defining a full function using `def` is unnecessary.

Unlike regular functions, a lambda function:
- Does not have a name.
- Can contain only one expression.
- Automatically returns the result of that expression

## Syntax

lambda arguments: expression

| Lambda Function | Regular Function (`def`) |
|-----------------|---------------------------|
| Created using the `lambda` keyword. | Created using the `def` keyword. |
| Anonymous (no function name required). | Has a function name. |
| Contains only one expression. | Can contain multiple statements. |
| Automatically returns the result. | Requires the `return` statement to return a value. |
| Used for short, simple operations. | Used for complex logic and larger programs. |


## 13. How do you define a function that takes another function as an argument?

In Python, functions are first-class objects, which means a function can be:
- Assigned to a variable.
- Passed as an argument to another function.
- Returned from another function.

A function that accepts another function as an argument is called a Higher-Order Function.

## Example

def greet():
    return "Hello"

def display(func):
    print(func())

display(greet)

### Output

Hello

## 14. Write a Python function to find the largest number from a list. *(Argument: list)*

#using sort method

```
def largest_num(list1):
     list1.sort()
     print(list1[-1])
     
n = int(input("enter the size of the list: "))
list1 = []
for i in range(n):
    list1.append(int(input(f"enter the value{i+1} : ")))

largest_num(list1)

```
#using for loop

```
def largest_num(list1):
    max = float('-inf')
    for i in list1:
        if i > max:
            max = i
    return max
n = int(input("enter the size of the list: "))
list1 = []
for i in range(n):
    list1.append(int(input(f"enter the value{i+1} : ")))
    
result = largest_num(list1)
print(result)
```

## 15. Write a Python function to find the second largest number from a list. *(Argument: list)*

#using sort method

```
def largest_num(list1):
     list1.sort()
     print(list1[-2])
     
n = int(input("enter the size of the list: "))
list1 = []
for i in range(n):
    list1.append(int(input(f"enter the value{i+1} : ")))

largest_num(list1)
```
#using for loop

```
def largest_num(list1):
    max = float('-inf')
    second_max = float('-inf')
    for i in list1:
        if i > max:
            second_max = max
            max = i
        elif i > second_max and i != max :
            second_max = i
        
    return second_max
            
    
n = int(input("enter the size of the list: "))
list1 = []
for i in range(n):
    list1.append(int(input(f"enter the value{i+1} : ")))
    
result = largest_num(list1)
print(result)
```

## 16. Write a Python function to reverse a string. *(Argument: string)*

#using for loop
```
def rev_string(str1):
    rev = ''
    for i in str1:
        rev = i+rev
    return rev

result = rev_string(input("Enter the string: "))

print(result)
```
#reversing the elements in the list(without changing there order
```
def rev_string(list1):
    rev_list = []
    
    for i in list1:
        rev = ''
        for j in i:
            rev = j+rev
        rev_list.append(rev)
    return rev_list

n = int(input("enter the size of the list: "))
list1 = []
for i in range(n):
     list1.append(input(f"enter the element{i+1} : "))
    
result = rev_string(list1)

print(result)
```

## 17. Write a Python function to remove duplicate elements from a list. *(Argument: list)*

## 18. Write a Python function to sort a list and return the sorted list. *(Argument: list)*

## 19. Write a Python function to generate prime numbers in a given range. *(Arguments: \*args)*

## 20. Write a function `factorial(n)` that takes a non-negative integer `n` and returns its factorial.

## 21. Write a function `is_palindrome(s)` that checks whether a given string is a palindrome.

## 22. Write a function `fibonacci(n)` that returns the nth Fibonacci number.

## 23. Write a function `sum_of_digits(n)` that calculates the sum of the digits of a non-negative integer.

## 24. Write a function `count_vowels(s)` that counts the number of vowels in a given string.

## 25. Write a function `sort_dict_by_value(d)` that takes a dictionary and returns a list of tuples sorted by dictionary values.

## 26. Write a function `merge_lists(lst1, lst2)` that merges two lists by alternating elements from each.
```
def merge_list(l1,l2):
    f = []
    
    if len(l1) >= len(l2):
        for i in range(len(l1)):
            if i <= len(l2)-1:
                f.append(l1[i])
                f.append(l2[i])
            else:
                f.append(l1[i])
    else:
        for i in range(len(l2)):
            if i <= len(l1)-1:
                f.append(l1[i])
                f.append(l2[i])
            else:
                f.append(l2[i])
    print(f)
merge_list([0,2,4,6],[1,3,5])
merge_list([0,2,4,6],[1,3,5,7]),
merge_list([0,2,4,6],[1,3,5,7,9])
```

## 27. Write a function `flatten(lst)` that takes a nested list and returns a flat list.

## 28. Write a recursive function to generate the Fibonacci series.

# Lambda Functions

## 29. What is a lambda function?

## 30. How does a lambda function differ from a regular function defined with `def` in Python?

## 31. What is the syntax for creating a lambda function in Python?

## 32. Can a lambda function have multiple arguments? Provide an example.

## 33. Can a lambda function include multiple expressions? Why or why not?

## 34. Write a lambda function that adds two numbers.

## 35. How would you use a lambda function with the `map()` function? Provide an example.

## 36. What is a common use case for lambda functions in combination with the `filter()` function?

## 37. How can you use a lambda function as a key in the `sorted()` function?

## 38. Write a lambda function that returns the square of a number and use it to sort a list of numbers in descending order.

# map(), filter(), and reduce()

## 39. What is the purpose of the `map()` function in Python?

## 40. How does the `filter()` function work and what is it used for?

## 41. What is the role of the `reduce()` function and in which module can it be found?

## 42. What types of arguments do `map()`, `filter()`, and `reduce()` accept?

## 43. Using `filter()`, print only the required numbers from a given list.

## 44. Using `map()`, find the square of all elements in a given list.

---

# File Handling

## 45. What are the different ways of opening a file in Python?

## 46. What are the different access modes used in file handling?

## 47. What is a file handler? Give its syntax and an example.

## 48. How do you open a file for reading and writing in Python?

## 49. What is the purpose of the `with` statement when handling files?

## 50. How do you read the entire content of a file into a string?

## 51. How can you read a file line by line?

## 52. How do you write data to a file?

## 53. What is the syntax to close a file?

## 54. How do you check if a file exists before opening it?

## 55. What is the difference between `file.write()` and `file.writelines()`?

## 56. How do you append data to an existing file?

## 57. Write a Python function to count the number of lines, words, and characters in a file.

## 58. Write a Python script to copy the contents of one file to another.

## 59. Create a function that takes a file path and searches for a specific string within the file, returning the line numbers where the string occurs.

## 60. Write a function to merge multiple text files into a single file.

## 61. Write a Python program to sort the lines in a text file alphabetically and save the sorted lines to a new file.

## 62. Write a Python program to print the number of words, characters, and lines in a given file.

## 63. Open a file and print the number of occurrences of the keyword `"Failed"`.

## 64. What is the use of the `seek()` and `tell()` methods?

## 65. Write a function that finds and replaces all occurrences of a string in a file.

## 66. Create a function that reverses the content of a file.

## 67. Write a Python script that counts the number of occurrences of each word in a file.

## 68. Write a function that reads a file and returns a list of all unique words in the file.
