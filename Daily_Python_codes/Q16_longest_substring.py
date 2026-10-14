sample = input("Enter the string : ")

result = {}
sub = ""

max_sub = ""
max_len = 0

for i in sample:
    if i in sub:
        sub = sub[sub.index(i) + 1:]
        sub += i
    else:
        sub += i

    if len(sub) > max_len:
        max_len = len(sub)
        max_sub = sub

result["substring"] = max_sub
result["length"] = max_len

print(result)

#---------------
# def longest_unique_substring(text):
#     last_seen = {}

#     start = 0
#     best_start = 0
#     best_length = 0

#     for index, char in enumerate(text):

#         if char in last_seen and last_seen[char] >= start:
#             start = last_seen[char] + 1

#         last_seen[char] = index

#         current_length = index - start + 1

#         if current_length > best_length:
#             best_length = current_length
#             best_start = start

#     return {
#         "substring": text[best_start:best_start + best_length],
#         "length": best_length
#     }


# text = input("Enter the string: ")
# result = longest_unique_substring(text)
# print(result)

##-----------------