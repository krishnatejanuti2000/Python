d1 = {
    "a": {"b": 10, "c": 20, "d": 6000},
    "k1": 100,
    "k2": 4000
}

largest = None

for key, value in d1.items():
    if isinstance(value, dict):
        for i in value.values():
            if largest is None or i > largest:
                largest = i
    else:
        if largest is None or value > largest:
            largest = value

print("Maximum value:", largest)