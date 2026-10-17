import re

logs = [
    "ERROR controller=nvme0 code=E101 message=Command timeout",
    "INFO controller=nvme1 message=Health check passed",
    "ERROR controller=nvme1 code=E205 message=Namespace failure",
    "ERROR controller=nvme0 code=E102 message=I/O failure"
]

result = []
pattern = r"\bE\d+\b"

for log in logs:
    if log.startswith("ERROR"):
        res = re.findall(pattern, log)
        result.extend(res)

print(result)