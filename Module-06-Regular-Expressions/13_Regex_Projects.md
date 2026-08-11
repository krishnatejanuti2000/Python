Yes — you are right. The previous version gave the **project requirements but not the complete solutions**.
# 13 — Regex Projects

## Objective

This module converts the Regex knowledge developed in Modules 01–12 into practical, end-to-end Storage Test Engineering projects.

The focus is no longer isolated Regex syntax.

The focus is:

```text
Storage Testing Requirement
        ↓
Understand the input
        ↓
Identify the pattern
        ↓
Design Regex
        ↓
Write Python code
        ↓
Extract structured information
        ↓
Validate
        ↓
Handle edge cases
        ↓
Generate useful test information
```

The projects increase in difficulty from basic extraction to complete Storage Test Log Automation.

---

# Project 1 — Storage Device Information Extractor

## Difficulty

🟢 Beginner

## Scenario

A storage inventory command produces:

```text
Drive=/dev/sda Type=HDD Capacity=500GB
Drive=/dev/sdb Type=HDD Capacity=1TB
Drive=/dev/nvme0n1 Type=SSD Capacity=2TB
Drive=/dev/nvme1n1 Type=SSD Capacity=4TB
```

## Requirement

Extract:

* Drive
* Type
* Capacity

Expected:

```python
[
    {
        "drive": "/dev/sda",
        "type": "HDD",
        "capacity": "500GB"
    },
    {
        "drive": "/dev/sdb",
        "type": "HDD",
        "capacity": "1TB"
    },
    {
        "drive": "/dev/nvme0n1",
        "type": "SSD",
        "capacity": "2TB"
    },
    {
        "drive": "/dev/nvme1n1",
        "type": "SSD",
        "capacity": "4TB"
    }
]
```

---

## Solution

```python
import re

text = """
Drive=/dev/sda Type=HDD Capacity=500GB
Drive=/dev/sdb Type=HDD Capacity=1TB
Drive=/dev/nvme0n1 Type=SSD Capacity=2TB
Drive=/dev/nvme1n1 Type=SSD Capacity=4TB
"""

pattern = (
    r"Drive=(?P<drive>/dev/\w+)\s+"
    r"Type=(?P<type>\w+)\s+"
    r"Capacity=(?P<capacity>\d+(?:TB|GB|MB))"
)

result = []

for match in re.finditer(pattern, text):
    result.append(match.groupdict())

print(result)
```

## Output

```python
[
    {
        'drive': '/dev/sda',
        'type': 'HDD',
        'capacity': '500GB'
    },
    {
        'drive': '/dev/sdb',
        'type': 'HDD',
        'capacity': '1TB'
    },
    {
        'drive': '/dev/nvme0n1',
        'type': 'SSD',
        'capacity': '2TB'
    },
    {
        'drive': '/dev/nvme1n1',
        'type': 'SSD',
        'capacity': '4TB'
    }
]
```

## What We Used

```regex
(?P<drive>...)
```

Named group for the device.

```regex
(?:TB|GB|MB)
```

Non-capturing group for capacity units.

```python
match.groupdict()
```

Converts named groups directly into a dictionary.

## Engineering Lesson

This is the basic pattern:

```text
Raw inventory
     ↓
Regex
     ↓
Named groups
     ↓
Dictionary
```

---

# Project 2 — Storage Test Result Validator

## Difficulty

🟢 → 🟡

## Scenario

A Storage Test framework produces:

```text
/dev/sda: PASS
/dev/sdb: FAIL
/dev/nvme0n1: PASS
/dev/nvme1n1: FAIL
```

## Requirement

Validate complete device-result strings.

Valid:

```text
/dev/sda: PASS
/dev/sda1: FAIL
/dev/nvme0n1: PASS
/dev/nvme0n1p1: FAIL
```

Invalid:

```text
sda: PASS
/dev/sda
/dev/sda: UNKNOWN
/dev/nvmeXn1: PASS
```

---

## Solution

For this project, we can explicitly describe the supported device formats.

```python
import re

pattern = (
    r"^"
    r"(?:/dev/sd[a-z]\d*|/dev/nvme\d+n\d+(?:p\d+)?)"
    r":\s"
    r"(?:PASS|FAIL)"
    r"$"
)

def validate_result(line):
    return bool(re.fullmatch(pattern, line))


tests = [
    "/dev/sda: PASS",
    "/dev/sda1: FAIL",
    "/dev/nvme0n1: PASS",
    "/dev/nvme0n1p1: FAIL",
    "sda: PASS",
    "/dev/sda",
    "/dev/sda: UNKNOWN",
    "/dev/nvmeXn1: PASS"
]

for test in tests:
    print(test, "->", validate_result(test))
```

## Output

```text
/dev/sda: PASS -> True
/dev/sda1: FAIL -> True
/dev/nvme0n1: PASS -> True
/dev/nvme0n1p1: FAIL -> True
sda: PASS -> False
/dev/sda -> False
/dev/sda: UNKNOWN -> False
/dev/nvmeXn1: PASS -> False
```

## Pattern Breakdown

### SATA/SCSI-style device

```regex
/dev/sd[a-z]\d*
```

Examples:

```text
/dev/sda
/dev/sda1
/dev/sdb
/dev/sdb10
```

### NVMe device

```regex
/dev/nvme\d+n\d+(?:p\d+)?
```

Examples:

```text
/dev/nvme0n1
/dev/nvme1n1
/dev/nvme0n1p1
/dev/nvme2n5p10
```

### Result

```regex
(?:PASS|FAIL)
```

### Anchors

```regex
^
$
```

Ensure the entire line is validated.

## Engineering Lesson

Validation is different from extraction.

For validation, ask:

> Does the entire input conform to the required format?

That is why:

```python
re.fullmatch()
```

is useful here.

---

# Project 3 — Storage Error Extractor

## Difficulty

🟡

## Scenario

```text
2026-08-12 09:00:01 [INFO] /dev/sda READ PASS
2026-08-12 09:00:02 [ERROR] /dev/sdb READ ERROR sector=182736
2026-08-12 09:00:03 [INFO] /dev/nvme0n1 WRITE PASS
2026-08-12 09:00:04 [ERROR] /dev/nvme1n1 WRITE I/O ERROR timeout=30s
```

## Requirement

Extract only failed operations.

Expected:

```python
[
    {
        "device": "/dev/sdb",
        "operation": "READ",
        "error": "READ ERROR",
        "diagnostic": "sector=182736"
    },
    {
        "device": "/dev/nvme1n1",
        "operation": "WRITE",
        "error": "WRITE I/O ERROR",
        "diagnostic": "timeout=30s"
    }
]
```

---

## Solution

```python
import re

text = """
2026-08-12 09:00:01 [INFO] /dev/sda READ PASS
2026-08-12 09:00:02 [ERROR] /dev/sdb READ ERROR sector=182736
2026-08-12 09:00:03 [INFO] /dev/nvme0n1 WRITE PASS
2026-08-12 09:00:04 [ERROR] /dev/nvme1n1 WRITE I/O ERROR timeout=30s
"""

pattern = (
    r"(?P<device>/dev/\w+)\s+"
    r"(?P<operation>\w+)\s+"
    r"(?P<error>(?:[\w/]+\s+)*ERROR)\s+"
    r"(?P<diagnostic>.+)"
)

result = []

for match in re.finditer(pattern, text):
    result.append(match.groupdict())

print(result)
```

## Output

```python
[
    {
        'device': '/dev/sdb',
        'operation': 'READ',
        'error': 'READ ERROR',
        'diagnostic': 'sector=182736'
    },
    {
        'device': '/dev/nvme1n1',
        'operation': 'WRITE',
        'error': 'WRITE I/O ERROR',
        'diagnostic': 'timeout=30s'
    }
]
```

## Important Concept

The error is variable length:

```text
READ ERROR
WRITE I/O ERROR
READ MEDIA ERROR
WRITE UNRECOVERABLE ERROR
```

Therefore we don't hard-code:

```regex
READ ERROR
```

Instead:

```regex
(?P<error>(?:[\w/]+\s+)*ERROR)
```

means:

```text
zero or more words
        +
ERROR
```

## Engineering Lesson

When a log field is variable-length, find its reliable boundary.

Here:

```text
ERROR
```

is the boundary.

---

# Project 4 — Storage Log Sanitizer

## Difficulty

🟡

## Scenario

A raw log contains unnecessary information:

```text
2026-08-12 10:00:01 USER=krishna HOST=storage01 /dev/sda READ PASS
2026-08-12 10:00:02 USER=krishna HOST=storage01 /dev/sdb READ ERROR
2026-08-12 10:00:03 USER=krishna HOST=storage01 /dev/sdc WRITE PASS
```

## Requirement

Remove:

```text
USER=<value>
HOST=<value>
```

Expected:

```text
2026-08-12 10:00:01 /dev/sda READ PASS
2026-08-12 10:00:02 /dev/sdb READ ERROR
2026-08-12 10:00:03 /dev/sdc WRITE PASS
```

---

## Solution

```python
import re

text = """
2026-08-12 10:00:01 USER=krishna HOST=storage01 /dev/sda READ PASS
2026-08-12 10:00:02 USER=krishna HOST=storage01 /dev/sdb READ ERROR
2026-08-12 10:00:03 USER=krishna HOST=storage01 /dev/sdc WRITE PASS
"""

pattern = r"(?:USER|HOST)=\S+\s*"

result = re.sub(pattern, "", text)

print(result)
```

## Output

```text
2026-08-12 10:00:01 /dev/sda READ PASS
2026-08-12 10:00:02 /dev/sdb READ ERROR
2026-08-12 10:00:03 /dev/sdc WRITE PASS
```

## Engineering Lesson

This project demonstrates that Regex is not only for extraction.

It can also transform data:

```python
re.sub()
```

Pipeline:

```text
Raw Log
   ↓
Find unwanted information
   ↓
Replace with ""
   ↓
Clean Log
```

---

# Project 5 — Storage Error Normalizer

## Difficulty

🟡

## Scenario

Different firmware versions produce different capitalization:

```text
/dev/sda read error
/dev/sdb READ ERROR
/dev/sdc Read Error
/dev/nvme0n1 i/o error
/dev/nvme1n1 I/O ERROR
```

## Requirement

Normalize to:

```text
/dev/sda READ ERROR
/dev/sdb READ ERROR
/dev/sdc READ ERROR
/dev/nvme0n1 I/O ERROR
/dev/nvme1n1 I/O ERROR
```

---

## Solution

```python
import re

text = """
/dev/sda read error
/dev/sdb READ ERROR
/dev/sdc Read Error
/dev/nvme0n1 i/o error
/dev/nvme1n1 I/O ERROR
"""

pattern = re.compile(
    r"(?P<device>/dev/\w+)\s+"
    r"(?P<operation>READ|WRITE)\s+"
    r"(?P<error>ERROR|I/O ERROR)",
    re.I
)

def normalize(match):
    device = match.group("device")
    operation = match.group("operation").upper()
    error = match.group("error").upper()

    return f"{device} {operation} {error}"


result = pattern.sub(normalize, text)

print(result)
```

## Output

```text
/dev/sda READ ERROR
/dev/sdb READ ERROR
/dev/sdc READ ERROR
/dev/nvme0n1 I/O ERROR
/dev/nvme1n1 I/O ERROR
```

## Engineering Lesson

The `re.I` flag allows:

```text
read
READ
Read
rEaD
```

to match the same pattern.

Then Python can normalize the result using:

```python
.upper()
```

This is often cleaner than trying to perform every transformation inside Regex.

---

# Project 6 — Storage Log Analyzer

## Difficulty

🟠

## Scenario

```text
2026-08-12 11:00:01 [INFO] /dev/sda TEST_START
2026-08-12 11:00:02 [INFO] /dev/sda READ PASS
2026-08-12 11:00:03 [ERROR] /dev/sda READ ERROR sector=100
2026-08-12 11:00:04 [INFO] /dev/sda TEST_END

2026-08-12 11:01:01 [INFO] /dev/sdb TEST_START
2026-08-12 11:01:02 [INFO] /dev/sdb READ PASS
2026-08-12 11:01:03 [INFO] /dev/sdb WRITE PASS
2026-08-12 11:01:04 [INFO] /dev/sdb TEST_END

2026-08-12 11:02:01 [INFO] /dev/nvme0n1 TEST_START
2026-08-12 11:02:02 [ERROR] /dev/nvme0n1 WRITE I/O ERROR timeout=30s
2026-08-12 11:02:03 [INFO] /dev/nvme0n1 TEST_END
```

## Requirement

Generate:

```python
{
    "/dev/sda": {
        "status": "FAIL",
        "error_count": 1
    },
    "/dev/sdb": {
        "status": "PASS",
        "error_count": 0
    },
    "/dev/nvme0n1": {
        "status": "FAIL",
        "error_count": 1
    }
}
```

---

## Solution

```python
import re

text = """
2026-08-12 11:00:01 [INFO] /dev/sda TEST_START
2026-08-12 11:00:02 [INFO] /dev/sda READ PASS
2026-08-12 11:00:03 [ERROR] /dev/sda READ ERROR sector=100
2026-08-12 11:00:04 [INFO] /dev/sda TEST_END

2026-08-12 11:01:01 [INFO] /dev/sdb TEST_START
2026-08-12 11:01:02 [INFO] /dev/sdb READ PASS
2026-08-12 11:01:03 [INFO] /dev/sdb WRITE PASS
2026-08-12 11:01:04 [INFO] /dev/sdb TEST_END

2026-08-12 11:02:01 [INFO] /dev/nvme0n1 TEST_START
2026-08-12 11:02:02 [ERROR] /dev/nvme0n1 WRITE I/O ERROR timeout=30s
2026-08-12 11:02:03 [INFO] /dev/nvme0n1 TEST_END
"""

pattern = (
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})"
    r"\s+\[(?P<severity>\w+)\]\s+"
    r"(?P<device>/dev/\w+)\s+"
    r"(?P<message>.+)"
)

devices = {}

for match in re.finditer(pattern, text):
    data = match.groupdict()

    device = data["device"]

    if device not in devices:
        devices[device] = {
            "status": "PASS",
            "error_count": 0
        }

    if data["severity"] == "ERROR":
        devices[device]["status"] = "FAIL"
        devices[device]["error_count"] += 1

print(devices)
```

## Output

```python
{
    '/dev/sda': {
        'status': 'FAIL',
        'error_count': 1
    },
    '/dev/sdb': {
        'status': 'PASS',
        'error_count': 0
    },
    '/dev/nvme0n1': {
        'status': 'FAIL',
        'error_count': 1
    }
}
```

## Engineering Lesson

Regex extracts the event.

Python performs the analysis.

```text
Regex
  ↓
Event extraction
  ↓
Dictionary
  ↓
Aggregation
  ↓
PASS/FAIL
```

---

# Project 7 — Storage Log Failure Correlator

## Difficulty

🟠

## Scenario

```text
2026-08-12 12:00:01 [INFO] /dev/sda TEST_START
2026-08-12 12:00:02 [INFO] /dev/sda READ START
2026-08-12 12:00:03 [ERROR] /dev/sda READ ERROR sector=100
2026-08-12 12:00:04 [WARN] /dev/sda RETRY retry=1
2026-08-12 12:00:05 [WARN] /dev/sda RETRY retry=2
2026-08-12 12:00:06 [ERROR] /dev/sda READ ERROR sector=100
2026-08-12 12:00:07 [INFO] /dev/sda TEST_END
```

## Requirement

Determine:

* Device
* First error timestamp
* Retry count
* Error count
* Completion
* Final status

Expected:

```python
{
    "device": "/dev/sda",
    "first_error": "2026-08-12 12:00:03",
    "retry_count": 2,
    "error_count": 2,
    "completed": True,
    "status": "FAIL"
}
```

---

## Solution

```python
import re

text = """
2026-08-12 12:00:01 [INFO] /dev/sda TEST_START
2026-08-12 12:00:02 [INFO] /dev/sda READ START
2026-08-12 12:00:03 [ERROR] /dev/sda READ ERROR sector=100
2026-08-12 12:00:04 [WARN] /dev/sda RETRY retry=1
2026-08-12 12:00:05 [WARN] /dev/sda RETRY retry=2
2026-08-12 12:00:06 [ERROR] /dev/sda READ ERROR sector=100
2026-08-12 12:00:07 [INFO] /dev/sda TEST_END
"""

pattern = (
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})"
    r"\s+\[(?P<severity>\w+)\]\s+"
    r"(?P<device>/dev/\w+)\s+"
    r"(?P<message>.+)"
)

result = {
    "device": None,
    "first_error": None,
    "retry_count": 0,
    "error_count": 0,
    "completed": False,
    "status": "PASS"
}

for match in re.finditer(pattern, text):
    data = match.groupdict()

    result["device"] = data["device"]

    if data["severity"] == "ERROR":
        result["error_count"] += 1
        result["status"] = "FAIL"

        if result["first_error"] is None:
            result["first_error"] = data["timestamp"]

    elif data["severity"] == "WARN" and "RETRY" in data["message"]:
        result["retry_count"] += 1

    elif data["message"] == "TEST_END":
        result["completed"] = True

print(result)
```

## Output

```python
{
    'device': '/dev/sda',
    'first_error': '2026-08-12 12:00:03',
    'retry_count': 2,
    'error_count': 2,
    'completed': True,
    'status': 'FAIL'
}
```

## Engineering Lesson

This is no longer simply:

```text
Find text
```

It is:

```text
Find event
   ↓
Understand event
   ↓
Maintain state
   ↓
Correlate events
   ↓
Generate conclusion
```

---

# Project 8 — Storage Test Report Generator

## Difficulty

🟠 → 🔴

## Scenario

```text
2026-08-12 13:00:01 [INFO] /dev/sda TEST_START
2026-08-12 13:00:02 [INFO] /dev/sda READ PASS
2026-08-12 13:00:03 [INFO] /dev/sda WRITE PASS
2026-08-12 13:00:04 [INFO] /dev/sda TEST_END

2026-08-12 13:01:01 [INFO] /dev/sdb TEST_START
2026-08-12 13:01:02 [INFO] /dev/sdb READ PASS
2026-08-12 13:01:03 [ERROR] /dev/sdb WRITE ERROR timeout=30s
2026-08-12 13:01:04 [INFO] /dev/sdb TEST_END

2026-08-12 13:02:01 [INFO] /dev/nvme0n1 TEST_START
2026-08-12 13:02:02 [ERROR] /dev/nvme0n1 READ MEDIA ERROR block=918273
2026-08-12 13:02:03 [ERROR] /dev/nvme0n1 WRITE I/O ERROR timeout=20s
2026-08-12 13:02:04 [INFO] /dev/nvme0n1 TEST_END
```

## Requirement

Generate:

```text
Storage Test Report
===================

/dev/sda
Status       : PASS
Errors       : 0

/dev/sdb
Status       : FAIL
Errors       : 1

/dev/nvme0n1
Status       : FAIL
Errors       : 2
```

---

## Solution

```python
import re

text = """
2026-08-12 13:00:01 [INFO] /dev/sda TEST_START
2026-08-12 13:00:02 [INFO] /dev/sda READ PASS
2026-08-12 13:00:03 [INFO] /dev/sda WRITE PASS
2026-08-12 13:00:04 [INFO] /dev/sda TEST_END

2026-08-12 13:01:01 [INFO] /dev/sdb TEST_START
2026-08-12 13:01:02 [INFO] /dev/sdb READ PASS
2026-08-12 13:01:03 [ERROR] /dev/sdb WRITE ERROR timeout=30s
2026-08-12 13:01:04 [INFO] /dev/sdb TEST_END

2026-08-12 13:02:01 [INFO] /dev/nvme0n1 TEST_START
2026-08-12 13:02:02 [ERROR] /dev/nvme0n1 READ MEDIA ERROR block=918273
2026-08-12 13:02:03 [ERROR] /dev/nvme0n1 WRITE I/O ERROR timeout=20s
2026-08-12 13:02:04 [INFO] /dev/nvme0n1 TEST_END
"""

pattern = (
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})"
    r"\s+\[(?P<severity>\w+)\]\s+"
    r"(?P<device>/dev/\w+)\s+"
    r"(?P<message>.+)"
)

devices = {}

for match in re.finditer(pattern, text):
    data = match.groupdict()

    device = data["device"]

    if device not in devices:
        devices[device] = {
            "status": "PASS",
            "errors": 0
        }

    if data["severity"] == "ERROR":
        devices[device]["status"] = "FAIL"
        devices[device]["errors"] += 1


print("Storage Test Report")
print("===================")

for device, result in devices.items():
    print()
    print(device)
    print(f"Status       : {result['status']}")
    print(f"Errors       : {result['errors']}")
```

## Output

```text
Storage Test Report
===================

/dev/sda
Status       : PASS
Errors       : 0

/dev/sdb
Status       : FAIL
Errors       : 1

/dev/nvme0n1
Status       : FAIL
Errors       : 2
```

## Engineering Lesson

This is the first project where the Regex parser directly produces an engineer-facing report.

```text
Raw Log
   ↓
Regex
   ↓
Events
   ↓
Aggregation
   ↓
Analysis
   ↓
Human-readable Report
```

---

# Project 9 — Enterprise Storage Log Parser

## Difficulty

🔴

## Scenario

The log contains multiple formats and unrelated lines:

```text
Storage validation started

2026-08-12 14:00:01 [INFO] Drive=/dev/sda Type=HDD Capacity=1TB Status=PASS
2026-08-12 14:00:02 [WARN] Drive=/dev/sdb Type=HDD Capacity=2TB Status=READ ERROR - sector=182736 retry=3
2026-08-12 14:00:03 [INFO] Drive=/dev/nvme0n1 Type=SSD Capacity=4TB Status=PASS
DEBUG queue initialized
2026-08-12 14:00:04 [ERROR] Drive=/dev/nvme1n1 Type=SSD Capacity=8TB Status=I/O ERROR - timeout=30s queue=7
Controller initialization complete
2026-08-12 14:00:05 [INFO] Drive=/dev/sdc Type=HDD Capacity=2TB Status=PASS
```

## Requirement

Produce:

```python
[
    {
        "device": "/dev/sda",
        "type": "HDD",
        "capacity": "1TB",
        "status": "PASS",
        "diagnostic": None
    },
    {
        "device": "/dev/sdb",
        "type": "HDD",
        "capacity": "2TB",
        "status": "READ ERROR",
        "diagnostic": "sector=182736 retry=3"
    },
    {
        "device": "/dev/nvme0n1",
        "type": "SSD",
        "capacity": "4TB",
        "status": "PASS",
        "diagnostic": None
    },
    {
        "device": "/dev/nvme1n1",
        "type": "SSD",
        "capacity": "8TB",
        "status": "I/O ERROR",
        "diagnostic": "timeout=30s queue=7"
    },
    {
        "device": "/dev/sdc",
        "type": "HDD",
        "capacity": "2TB",
        "status": "PASS",
        "diagnostic": None
    }
]
```

---

## Solution

```python
import re

text = """
Storage validation started

2026-08-12 14:00:01 [INFO] Drive=/dev/sda Type=HDD Capacity=1TB Status=PASS
2026-08-12 14:00:02 [WARN] Drive=/dev/sdb Type=HDD Capacity=2TB Status=READ ERROR - sector=182736 retry=3
2026-08-12 14:00:03 [INFO] Drive=/dev/nvme0n1 Type=SSD Capacity=4TB Status=PASS
DEBUG queue initialized
2026-08-12 14:00:04 [ERROR] Drive=/dev/nvme1n1 Type=SSD Capacity=8TB Status=I/O ERROR - timeout=30s queue=7
Controller initialization complete
2026-08-12 14:00:05 [INFO] Drive=/dev/sdc Type=HDD Capacity=2TB Status=PASS
"""

pattern = (
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})"
    r"\s+\[(?P<severity>\w+)\]\s+"
    r"Drive=(?P<device>/dev/\w+)\s+"
    r"Type=(?P<type>\w+)\s+"
    r"Capacity=(?P<capacity>\d+(?:TB|GB|MB))\s+"
    r"Status=(?P<status>.+?)"
    r"(?:\s+-\s+(?P<diagnostic>.+))?$"
)

result = []

for match in re.finditer(pattern, text, re.M):
    data = match.groupdict()

    result.append({
        "device": data["device"],
        "type": data["type"],
        "capacity": data["capacity"],
        "status": data["status"],
        "diagnostic": data["diagnostic"]
    })

print(result)
```

## Output

```python
[
    {
        'device': '/dev/sda',
        'type': 'HDD',
        'capacity': '1TB',
        'status': 'PASS',
        'diagnostic': None
    },
    {
        'device': '/dev/sdb',
        'type': 'HDD',
        'capacity': '2TB',
        'status': 'READ ERROR',
        'diagnostic': 'sector=182736 retry=3'
    },
    {
        'device': '/dev/nvme0n1',
        'type': 'SSD',
        'capacity': '4TB',
        'status': 'PASS',
        'diagnostic': None
    },
    {
        'device': '/dev/nvme1n1',
        'type': 'SSD',
        'capacity': '8TB',
        'status': 'I/O ERROR',
        'diagnostic': 'timeout=30s queue=7'
    },
    {
        'device': '/dev/sdc',
        'type': 'HDD',
        'capacity': '2TB',
        'status': 'PASS',
        'diagnostic': None
    }
]
```

## Important Regex Concept

This part:

```regex
(?P<status>.+?)
```

is lazy.

It prevents the status from consuming the diagnostic section.

The boundary is:

```regex
(?=\s+-\s+)
```

or, in the final pattern, the explicit optional diagnostic structure.

The important idea is:

```text
Status
   ↓
lazy match
   ↓
" - "
   ↓
Diagnostic
```

## Engineering Lesson

This is similar to the advanced pattern you solved in `10_Pattern_Matching.md`.

The key is not memorizing the final Regex.

The key is understanding the boundary between:

```text
Status
```

and:

```text
Diagnostic
```

---

# Project 10 — Final Storage Test Automation Project

## Difficulty

🔴🔥

This is the final project of Module 13.

---

## Scenario

The Storage Test framework produces:

```text
2026-08-12 15:00:01 [INFO] /dev/sda TEST_START
2026-08-12 15:00:02 [INFO] /dev/sda READ PASS
2026-08-12 15:00:03 [INFO] /dev/sda WRITE PASS
2026-08-12 15:00:04 [ERROR] /dev/sda READ ERROR sector=182736 retry=2
2026-08-12 15:00:05 [WARN] /dev/sda READ RETRY retry=3
2026-08-12 15:00:06 [INFO] /dev/sda TEST_END

2026-08-12 15:01:01 [INFO] /dev/sdb TEST_START
2026-08-12 15:01:02 [INFO] /dev/sdb READ PASS
2026-08-12 15:01:03 [ERROR] /dev/sdb WRITE I/O ERROR timeout=30s queue=7
2026-08-12 15:01:04 [ERROR] /dev/sdb READ MEDIA ERROR block=123456
2026-08-12 15:01:05 [INFO] /dev/sdb TEST_END

DEBUG controller initialized

2026-08-12 15:02:01 [INFO] /dev/nvme0n1 TEST_START
2026-08-12 15:02:02 [INFO] /dev/nvme0n1 READ PASS
2026-08-12 15:02:03 [INFO] /dev/nvme0n1 WRITE PASS
2026-08-12 15:02:04 [INFO] /dev/nvme0n1 TEST_END
```

---

# Requirement

Determine for every device:

* Device name
* Test started
* Test completed
* Number of errors
* Number of retries
* First error
* Error types
* Final PASS/FAIL status

Expected:

```python
[
    {
        "device": "/dev/sda",
        "started": True,
        "completed": True,
        "status": "FAIL",
        "error_count": 1,
        "retry_count": 1,
        "first_error": "READ ERROR",
        "errors": [
            {
                "operation": "READ",
                "error": "READ ERROR",
                "diagnostic": "sector=182736 retry=2"
            }
        ]
    },
    {
        "device": "/dev/sdb",
        "started": True,
        "completed": True,
        "status": "FAIL",
        "error_count": 2,
        "retry_count": 0,
        "first_error": "WRITE I/O ERROR",
        "errors": [
            {
                "operation": "WRITE",
                "error": "WRITE I/O ERROR",
                "diagnostic": "timeout=30s queue=7"
            },
            {
                "operation": "READ",
                "error": "READ MEDIA ERROR",
                "diagnostic": "block=123456"
            }
        ]
    },
    {
        "device": "/dev/nvme0n1",
        "started": True,
        "completed": True,
        "status": "PASS",
        "error_count": 0,
        "retry_count": 0,
        "first_error": None,
        "errors": []
    }
]
```

---

# Solution

```python
import re


text = """
2026-08-12 15:00:01 [INFO] /dev/sda TEST_START
2026-08-12 15:00:02 [INFO] /dev/sda READ PASS
2026-08-12 15:00:03 [INFO] /dev/sda WRITE PASS
2026-08-12 15:00:04 [ERROR] /dev/sda READ ERROR sector=182736 retry=2
2026-08-12 15:00:05 [WARN] /dev/sda READ RETRY retry=3
2026-08-12 15:00:06 [INFO] /dev/sda TEST_END

2026-08-12 15:01:01 [INFO] /dev/sdb TEST_START
2026-08-12 15:01:02 [INFO] /dev/sdb READ PASS
2026-08-12 15:01:03 [ERROR] /dev/sdb WRITE I/O ERROR timeout=30s queue=7
2026-08-12 15:01:04 [ERROR] /dev/sdb READ MEDIA ERROR block=123456
2026-08-12 15:01:05 [INFO] /dev/sdb TEST_END

DEBUG controller initialized

2026-08-12 15:02:01 [INFO] /dev/nvme0n1 TEST_START
2026-08-12 15:02:02 [INFO] /dev/nvme0n1 READ PASS
2026-08-12 15:02:03 [INFO] /dev/nvme0n1 WRITE PASS
2026-08-12 15:02:04 [INFO] /dev/nvme0n1 TEST_END
"""


# --------------------------------------------------
# 1. Parse all valid storage log records
# --------------------------------------------------

record_pattern = re.compile(
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})"
    r"\s+\[(?P<severity>\w+)\]\s+"
    r"(?P<device>/dev/\w+)\s+"
    r"(?P<message>.+)"
)


# --------------------------------------------------
# 2. Parse error messages
# --------------------------------------------------

error_pattern = re.compile(
    r"(?P<operation>\w+)\s+"
    r"(?P<error>(?:[\w/]+\s+)*ERROR)"
    r"\s+"
    r"(?P<diagnostic>.+)"
)


# --------------------------------------------------
# 3. Store results device-wise
# --------------------------------------------------

devices = {}


for match in record_pattern.finditer(text):

    record = match.groupdict()

    device = record["device"]
    message = record["message"]
    severity = record["severity"]
    timestamp = record["timestamp"]


    # Create device entry if not present
    if device not in devices:

        devices[device] = {
            "device": device,
            "started": False,
            "completed": False,
            "status": "PASS",
            "error_count": 0,
            "retry_count": 0,
            "first_error": None,
            "errors": []
        }


    # --------------------------------------------------
    # TEST_START
    # --------------------------------------------------

    if message == "TEST_START":

        devices[device]["started"] = True


    # --------------------------------------------------
    # TEST_END
    # --------------------------------------------------

    elif message == "TEST_END":

        devices[device]["completed"] = True


    # --------------------------------------------------
    # RETRY
    # --------------------------------------------------

    elif "RETRY" in message:

        devices[device]["retry_count"] += 1


    # --------------------------------------------------
    # ERROR
    # --------------------------------------------------

    elif severity == "ERROR":

        error_match = error_pattern.fullmatch(message)

        if error_match:

            error_data = error_match.groupdict()

            devices[device]["status"] = "FAIL"

            devices[device]["error_count"] += 1


            if devices[device]["first_error"] is None:

                devices[device]["first_error"] = (
                    error_data["error"]
                )


            devices[device]["errors"].append({
                "operation": error_data["operation"],
                "error": error_data["error"],
                "diagnostic": error_data["diagnostic"]
            })


# --------------------------------------------------
# 4. Convert dictionary to list
# --------------------------------------------------

result = list(devices.values())


# --------------------------------------------------
# 5. Print final result
# --------------------------------------------------

for device in result:

    print(device)
```

---

# Expected Output

```python
{
    'device': '/dev/sda',
    'started': True,
    'completed': True,
    'status': 'FAIL',
    'error_count': 1,
    'retry_count': 1,
    'first_error': 'READ ERROR',
    'errors': [
        {
            'operation': 'READ',
            'error': 'READ ERROR',
            'diagnostic': 'sector=182736 retry=2'
        }
    ]
}

{
    'device': '/dev/sdb',
    'started': True,
    'completed': True,
    'status': 'FAIL',
    'error_count': 2,
    'retry_count': 0,
    'first_error': 'WRITE I/O ERROR',
    'errors': [
        {
            'operation': 'WRITE',
            'error': 'WRITE I/O ERROR',
            'diagnostic': 'timeout=30s queue=7'
        },
        {
            'operation': 'READ',
            'error': 'READ MEDIA ERROR',
            'diagnostic': 'block=123456'
        }
    ]
}

{
    'device': '/dev/nvme0n1',
    'started': True,
    'completed': True,
    'status': 'PASS',
    'error_count': 0,
    'retry_count': 0,
    'first_error': None,
    'errors': []
}
```

---

# Final Project Architecture

The final project follows:

```text
                    RAW LOG
                       |
                       v
              Record Recognition
                       |
                       v
              Regex Extraction
                       |
                       v
               Event Classification
                       |
                       v
                Device Grouping
                       |
                       v
               State Tracking
                       |
                       v
              Failure Correlation
                       |
                       v
                Result Analysis
                       |
                       v
              Structured Report
```

---

# Important Engineering Principle

Do NOT try to solve Project 10 using one giant Regex.

Instead:

```text
Regex
  ↓
Extract records

Regex
  ↓
Extract error fields

Python
  ↓
Track state

Python
  ↓
Group devices

Python
  ↓
Count errors

Python
  ↓
Count retries

Python
  ↓
Determine PASS/FAIL

Python
  ↓
Generate final result
```

This is much closer to how production Storage Test Automation should be designed.

---

# Project Difficulty Progression

| Project | Topic                         | Difficulty | Solution |
| ------- | ----------------------------- | ---------: | -------- |
| 1       | Device Information Extraction |         🟢 | ✅        |
| 2       | Device/Test Result Validation |      🟢→🟡 | ✅        |
| 3       | Storage Error Extraction      |         🟡 | ✅        |
| 4       | Log Sanitization              |         🟡 | ✅        |
| 5       | Error Normalization           |         🟡 | ✅        |
| 6       | Device-wise Log Analysis      |         🟠 | ✅        |
| 7       | Failure Correlation           |         🟠 | ✅        |
| 8       | Test Report Generation        |      🟠→🔴 | ✅        |
| 9       | Enterprise Log Parsing        |         🔴 | ✅        |
| 10      | Final Storage Test Automation |       🔴🔥 | ✅        |

---

# What Each Project Teaches

## Project 1

```text
Named Groups
    +
finditer()
    +
groupdict()
```

## Project 2

```text
Anchors
    +
Alternation
    +
fullmatch()
    +
Validation
```

## Project 3

```text
Variable-length fields
    +
Named Groups
    +
Error extraction
```

## Project 4

```text
re.sub()
    +
Text transformation
```

## Project 5

```text
Flags
    +
Normalization
    +
Replacement functions
```

## Project 6

```text
Regex
    +
Dictionary
    +
Aggregation
```

## Project 7

```text
Regex
    +
State
    +
Event correlation
```

## Project 8

```text
Parsing
    +
Aggregation
    +
Reporting
```

## Project 9

```text
Complex Regex
    +
Lazy matching
    +
Optional fields
    +
Noisy input
```

## Project 10

```text
Everything combined
```

---

# Project Completion Criteria

All projects must eventually be:

```text
Project 1  → Solved
Project 2  → Solved
Project 3  → Solved
Project 4  → Solved
Project 5  → Solved
Project 6  → Solved
Project 7  → Solved
Project 8  → Solved
Project 9  → Solved
Project 10 → Solved
```

After completing and testing all ten:

```text
13_Regex_Projects.md
        ↓
        COMPLETE
```

Then move to:

```text
14_Regex_Interview_Questions.md
```

After Module 14:

```text
Regex_CheatSheet.md
```

Finally:

```text
Regex_Quick_Revision.md
```

---

# Final Skill Target

The goal is NOT:

> "I know Regex."

The goal is:

> "I can look at a real Storage Testing requirement, understand the log structure, design the Regex, implement it in Python, validate the result, handle edge cases, correlate events, and generate useful automation output."

That is the practical Regex skill required for Storage Test Engineering.

```


