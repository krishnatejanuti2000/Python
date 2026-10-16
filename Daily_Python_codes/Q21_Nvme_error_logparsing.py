import re

logs = [
    "INFO controller=nvme0 message=Controller initialized",
    "ERROR controller=nvme0 code=E101 message=Command timeout",
    "ERROR controller=nvme1 code=E205 message=Namespace failure",
    "ERROR controller=nvme0 code=E102 message=I/O failure",
    "INFO controller=nvme1 message=Health check passed",
    "ERROR controller=nvme1 code=E206 message=Command timeout",
    "ERROR controller=nvme0 code=E103 message=Reset failure"
]

# logs = [
#     "ERROR controller=nvme0 code=E101 message=Command timeout",
#     "ERROR controller=nvme1 code=E102 message=Namespace failure",
#     "ERROR controller=nvme0 code=E103 message=I/O failure",
#     "ERROR controller=nvme1 code=E104 message=Reset failure",
#     "ERROR controller=nvme2 code=E105 message=Command timeout"
# ]

result = []
pattern = r"\bnvme\d+\b"

# Step 1: Extract controller names from ERROR logs
for i in logs:
    if i.startswith("ERROR"):
        res = re.findall(pattern, i)
        result.extend(res)

# Step 2: Count errors for each controller
error_freq = {}

for i in result:
    error_freq[i] = error_freq.get(i, 0) + 1

# Step 3: Find the controller(s) with the highest error count
max_count = 0
max_controller = []

print("Error counts:")

for key, value in error_freq.items():
    print(f"{key}: {value}")

    if value > max_count:
        max_count = value
        max_controller = [key]
    elif value == max_count:
        max_controller.append(key)

# Step 4: Print the summary
print(f"Controller(s) with the highest number of errors: {max_controller}")
print(f"Total error entries: {len(result)}")
