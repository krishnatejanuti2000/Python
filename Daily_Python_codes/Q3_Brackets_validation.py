userinput = input("Enter brackets: ")

pairs = {')': '(','}': '{',']': '['}

result = []

for i in userinput:

    if i == '(' or i == '{' or i == '[':
        result.append(i)

    elif i == ')' or i == '}' or i == ']':
        if len(result) == 0:
            print("Invalid")
            break

        if result[-1] == pairs[i]:
            result.pop()
        else:
            print("Invalid")
            break

else:
    if len(result) == 0:
        print("Valid")
    else:
        print("Invalid")


"""
Write a Python program to determine whether a given string containing (), {}, and [] has balanced brackets.
A bracket sequence is valid when every closing bracket matches the most recently opened bracket.
Examples
Input:  [{()}]
Output: Valid
Input:  [{(})]
Output: Invalid
Input:  (([]))
Output: Valid
Input:  ([)]
Output: Invalid
"""