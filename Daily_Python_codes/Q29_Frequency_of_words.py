n = int(input("enter the size of the list : "))

input_list = []

for i in range(n):
    input_list.append(input(f"enter the element{i+1} : "))

freq = {}

for i in input_list:
    if i in freq:
        freq[i] += 1
    else:
        freq[i] = 1
        
result = {}

for word,frequency in freq.items():
    if frequency not in result:
        result[frequency] = []

    result[frequency].append(word)

print(result)
