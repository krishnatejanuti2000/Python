command_results = [
    {
        "command": "nvme list",
        "returncode": 0,
        "stdout": "/dev/nvme0n1\n/dev/nvme1n1\n",
        "stderr": ""
    },
    {
        "command": "nvme smart-log /dev/nvme0",
        "returncode": 0,
        "stdout": "critical_warning : 0\n",
        "stderr": ""
    },
    {
        "command": "nvme id-ctrl /dev/nvme9",
        "returncode": 2,
        "stdout": "",
        "stderr": "No such device"
    },
    {
        "command": "nvme list-subsys",
        "returncode": 0,
        "stdout": "   ",
        "stderr": ""
    }
]

summary = {
    "SUCCESS": 0,
    "NO_OUTPUT": 0,
    "FAILED": 0
}

failed_commands = []

for item in command_results:
    command = item["command"]
    returncode = item["returncode"]
    stdout = item["stdout"]
    stderr = item["stderr"]

    if returncode != 0:
        status = "FAILED"
        failed_commands.append((command, stderr.strip()))

    elif stdout.strip():
        status = "SUCCESS"

    else:
        status = "NO_OUTPUT"

    summary[status] += 1

print("Command Summary:")
print(f"SUCCESS: {summary['SUCCESS']}")
print(f"NO_OUTPUT: {summary['NO_OUTPUT']}")
print(f"FAILED: {summary['FAILED']}")

print("\nFailed Commands:")
print(failed_commands)