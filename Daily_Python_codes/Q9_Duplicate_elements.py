n = int(input("Enter the size of the list : "))
user_list = []
for i in range(n):
    user_list.append(int(input(f"enter the element{i+1} : ")))


seen = []
duplicate_list = []

for i in user_list:
    if i in seen:
        if i not in duplicate_list:
            duplicate_list.append(i)
    else:
        seen.append(i)

if duplicate_list:
    print(f"Duplicate elements : {duplicate_list}")
else:
    print("No duplicate elements found")
    

