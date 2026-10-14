words = [
    "listen", "eat", "silent",
    "tea", "enlist", "ate", "hello"
]

groups = {}

for i in words:
    char_counts = [0]*26

    for char in i:
        index = ord(char)-ord('a')
        char_counts[index] += 1

    signature = tuple(char_counts)

    if signature not in groups:
        groups[signature] = []

    groups[signature].append(i)

result = list(groups.values())
print(result)




