expected_devices = [
    "nvme0n1",
    "nvme1n1",
    "nvme2n1",
    "nvme3n1"
]

detected_devices = [
    "nvme0n1",
    "nvme2n1",
    "nvme4n1"
]

missing_devices = []
unexpected_devices = []

for i in expected_devices:
    if i not in detected_devices:
        missing_devices.append(i)

for i in detected_devices:
    if i not in expected_devices:
        unexpected_devices.append(i)

print(f"Missing devices : {missing_devices}")
print(f"Unexpected devices : {unexpected_devices}")
print(f"Total detected devices : {len(detected_devices)}")

