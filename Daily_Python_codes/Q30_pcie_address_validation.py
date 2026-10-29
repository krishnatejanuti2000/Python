import re

logs = """
nvme nvme0: PCI address 0000:5e:00.0 initialized
e1000: PCI address 0000:00:1f.6 initialized
nvme nvme1: PCI address 0000:af:00.0 initialized
nvme nvme2: controller initialization failed
nvme nvme3: PCI address 0000:3b:00.1 initialized
"""

pattern = r"\b[0-9A-Fa-f]{4}:[0-9A-Fa-f]{2}:(?:0[0-9A-Fa-f]|1[0-9A-Fa-f])\.[0-7]\b"

result = []

for line in logs.splitlines():
    if "nvme" in line.lower():
        addresses = re.findall(pattern, line)
        for address in addresses:
            result.append(address)

print(result)