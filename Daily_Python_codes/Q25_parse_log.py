logs = [
    "controller=nvme0 test=read result=PASS",
    "controller=nvme0 test=write result=FAIL",
    "controller=nvme1 test=read result=PASS",
    "controller=nvme0 test=flush result=PASS",
    "controller=nvme1 test=namespace_attach result=FAIL"
]

summary = {}
failed_tests = []

for log in logs:
    parsed = {}

    for item in log.split():
        key, value = item.split("=")
        parsed[key] = value

    controller = parsed["controller"]
    test = parsed["test"]
    status = parsed["result"]

    if controller not in summary:
        summary[controller] = {"PASS": 0, "FAIL": 0}

    summary[controller][status] += 1

    if status == "FAIL":
        failed_tests.append((controller, test))

print("Controller Summary:")

for controller, counts in summary.items():
    print(f"{controller}: PASS={counts['PASS']}, FAIL={counts['FAIL']}")

print("\nFailed Tests:")
print(failed_tests)