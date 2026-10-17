n = int(input("Enter the size of the list: "))

devices = []

for i in range(n):
    devices.append(input(f"Enter element {i + 1}: "))

unique_devices = []

for device in devices:
    if device not in unique_devices:
        unique_devices.append(device)

print(unique_devices)