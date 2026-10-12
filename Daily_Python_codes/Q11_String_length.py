user_input = input("enter the input string : ")
result = ""

if user_input:
    current_char = user_input[0]
    count = 1

    for char in user_input[1:]:
        if char == current_char:
            current_char = char
            count+=1
        else:
            result += current_char+str(count)
            current_char = char
            count = 1

    result += current_char+str(count)

    print(result)