import re

log = """
Detected nvme0n1 and nvme1n1.
Device nvme12n3 is online.
Invalid entries: nvmeXn1, nvme2, nvme3n1x.
"""

pattern = r"\bnvme\d+n\d+\b"

result = re.findall(pattern, log)

if result:
    print(result)
else:
    print("No match found")
