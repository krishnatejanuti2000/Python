# 12 — Log Parsing

## Objective

Use Python Regular Expressions and Python data structures to parse real-world Storage Test logs.

The focus of this document is not to relearn Regex syntax.

The focus is to apply the Regex knowledge already learned to Storage Testing scenarios.

The overall flow is:

Raw Storage Log
        ↓
Identify relevant records
        ↓
Extract required fields
        ↓
Filter events
        ↓
Correlate events
        ↓
Analyze failures
        ↓
Generate structured test results


---

# Q1 — Basic Storage Log Field Extraction

## Scenario

A Storage Test Automation framework produces the following log:

```text
2026-08-11 09:10:01 [INFO] /dev/sda TEST_START
2026-08-11 09:10:02 [INFO] /dev/sda READ PASS
2026-08-11 09:10:03 [INFO] /dev/sda WRITE PASS
2026-08-11 09:10:04 [ERROR] /dev/sda READ ERROR sector=182736
2026-08-11 09:10:05 [INFO] /dev/sda TEST_END
2026-08-11 09:11:01 [INFO] /dev/sdb TEST_START
2026-08-11 09:11:02 [INFO] /dev/sdb READ PASS
2026-08-11 09:11:03 [ERROR] /dev/sdb WRITE ERROR timeout=30s
2026-08-11 09:11:04 [INFO] /dev/sdb TEST_END
````

## Requirement

Extract only failed events.

Expected structure:

```python
[
    {
        "timestamp": "...",
        "device": "...",
        "operation": "...",
        "error": "...",
        "diagnostic": "..."
    }
]
```

Expected output:

```python
[
    {
        "timestamp": "2026-08-11 09:10:04",
        "device": "/dev/sda",
        "operation": "READ",
        "error": "READ ERROR",
        "diagnostic": "sector=182736"
    },
    {
        "timestamp": "2026-08-11 09:11:03",
        "device": "/dev/sdb",
        "operation": "WRITE",
        "error": "WRITE ERROR",
        "diagnostic": "timeout=30s"
    }
]
```

## Structure

A failed record contains:

```text
TIMESTAMP
    ↓
[ERROR]
    ↓
DEVICE
    ↓
OPERATION
    ↓
ERROR
    ↓
DIAGNOSTIC
```

## Pattern

```regex
(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[ERROR\]\s(?P<device>/dev/\w+)\s(?P<error>(?P<operation>\w+)\s\w+)\s(?P<diagnostic>.+)
```

## Solution

```python
import re

text = """
2026-08-11 09:10:01 [INFO] /dev/sda TEST_START
2026-08-11 09:10:02 [INFO] /dev/sda READ PASS
2026-08-11 09:10:03 [INFO] /dev/sda WRITE PASS
2026-08-11 09:10:04 [ERROR] /dev/sda READ ERROR sector=182736
2026-08-11 09:10:05 [INFO] /dev/sda TEST_END
2026-08-11 09:11:01 [INFO] /dev/sdb TEST_START
2026-08-11 09:11:02 [INFO] /dev/sdb READ PASS
2026-08-11 09:11:03 [ERROR] /dev/sdb WRITE ERROR timeout=30s
2026-08-11 09:11:04 [INFO] /dev/sdb TEST_END
"""

pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[ERROR\]\s(?P<device>/dev/\w+)\s(?P<error>(?P<operation>\w+)\s\w+)\s(?P<diagnostic>.+)"

result = []

for match in re.finditer(pattern, text):
    result.append(match.groupdict())

print(result)
```

## Engineering Lesson

The important step is identifying the structure of the failure record and extracting only the information required by the automation.

---

# Q2 — Variable Error Formats

## Scenario

Storage errors are not always exactly two words.

```text
2026-08-11 09:20:01 [ERROR] /dev/sda READ ERROR sector=182736
2026-08-11 09:20:02 [ERROR] /dev/sdb WRITE I/O ERROR timeout=30s
2026-08-11 09:20:03 [ERROR] /dev/nvme0n1 READ MEDIA ERROR block=918273
2026-08-11 09:20:04 [ERROR] /dev/nvme1n1 WRITE UNRECOVERABLE ERROR retry=5
```

## Requirement

Extract:

```python
[
    {
        "timestamp": "...",
        "device": "...",
        "operation": "...",
        "error": "...",
        "diagnostic": "..."
    }
]
```

Do not hard-code:

```text
READ ERROR
WRITE I/O ERROR
READ MEDIA ERROR
WRITE UNRECOVERABLE ERROR
```

The error portion may contain a variable number of words.

The diagnostic starts with a `key=value` field.

## Derivation

The first word after the device is the operation:

```regex
(?P<operation>\w+)
```

The error continues until `ERROR`:

```regex
(?P<error>(?P<operation>\w+)\s+(?:[\w/]+\s+)*ERROR)
```

The diagnostic begins with a key/value field:

```regex
(?P<diagnostic>\w+=.+)
```

## Pattern

```regex
(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[ERROR\]\s(?P<device>/dev/\w+)\s(?P<error>(?P<operation>\w+)\s+(?:[\w/]+\s+)*ERROR)\s+(?P<diagnostic>\w+=.+)
```

## Solution

```python
import re

text = """
2026-08-11 09:20:01 [ERROR] /dev/sda READ ERROR sector=182736
2026-08-11 09:20:02 [ERROR] /dev/sdb WRITE I/O ERROR timeout=30s
2026-08-11 09:20:03 [ERROR] /dev/nvme0n1 READ MEDIA ERROR block=918273
2026-08-11 09:20:04 [ERROR] /dev/nvme1n1 WRITE UNRECOVERABLE ERROR retry=5
"""

pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[ERROR\]\s(?P<device>/dev/\w+)\s(?P<error>(?P<operation>\w+)\s+(?:[\w/]+\s+)*ERROR)\s+(?P<diagnostic>\w+=.+)"

result = []

for match in re.finditer(pattern, text):
    result.append(match.groupdict())

print(result)
```

## Engineering Lesson

Never assume that a field is fixed-length merely because the first example is fixed-length.

Always identify the structural boundary.

---

# Q3 — Multiple Devices and Error Filtering

## Scenario

```text
2026-08-11 10:00:01 [INFO] /dev/sda READ PASS
2026-08-11 10:00:02 [ERROR] /dev/sdb READ ERROR sector=12345
2026-08-11 10:00:03 [INFO] /dev/nvme0n1 WRITE PASS
2026-08-11 10:00:04 [WARN] /dev/sdc READ RETRY retry=2
2026-08-11 10:00:05 [ERROR] /dev/nvme1n1 WRITE I/O ERROR timeout=30s
2026-08-11 10:00:06 [INFO] /dev/sda WRITE PASS
2026-08-11 10:00:07 [ERROR] /dev/sdb WRITE MEDIA ERROR block=777
```

## Requirement

Extract only `[ERROR]` records.

Ignore:

```text
PASS
RETRY
WARN
```

## Pattern

```regex
(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[ERROR\]\s(?P<device>/dev/\w+)\s(?P<error>(?P<operation>\w+)\s+(?:[\w/]+\s+)*ERROR)\s+(?P<diagnostic>\w+=.+)
```

## Solution

```python
import re

text = """
2026-08-11 10:00:01 [INFO] /dev/sda READ PASS
2026-08-11 10:00:02 [ERROR] /dev/sdb READ ERROR sector=12345
2026-08-11 10:00:03 [INFO] /dev/nvme0n1 WRITE PASS
2026-08-11 10:00:04 [WARN] /dev/sdc READ RETRY retry=2
2026-08-11 10:00:05 [ERROR] /dev/nvme1n1 WRITE I/O ERROR timeout=30s
2026-08-11 10:00:06 [INFO] /dev/sda WRITE PASS
2026-08-11 10:00:07 [ERROR] /dev/sdb WRITE MEDIA ERROR block=777
"""

pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[ERROR\]\s(?P<device>/dev/\w+)\s(?P<error>(?P<operation>\w+)\s+(?:[\w/]+\s+)*ERROR)\s+(?P<diagnostic>\w+=.+)"

result = []

for match in re.finditer(pattern, text):
    result.append(match.groupdict())

print(result)
```

## Engineering Lesson

A useful parser often follows:

```text
Large Log
   ↓
Filter relevant records
   ↓
Extract useful fields
```

---

# Q4 — Event Classification

## Scenario

```text
2026-08-11 11:00:01 [INFO] /dev/sda READ PASS
2026-08-11 11:00:02 [WARN] /dev/sda READ RETRY retry=1
2026-08-11 11:00:03 [ERROR] /dev/sda READ ERROR sector=123
2026-08-11 11:00:04 [INFO] /dev/sdb WRITE PASS
2026-08-11 11:00:05 [WARN] /dev/sdb WRITE RETRY retry=2
2026-08-11 11:00:06 [ERROR] /dev/sdb WRITE I/O ERROR timeout=30s
```

## Requirement

Extract:

```python
{
    "timestamp": "...",
    "severity": "...",
    "device": "...",
    "operation": "...",
    "message": "..."
}
```

## Pattern

```regex
(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[(?P<severity>\w+)\]\s(?P<device>/dev/\w+)\s(?P<message>.+)
```

## Solution

```python
import re

text = """
2026-08-11 11:00:01 [INFO] /dev/sda READ PASS
2026-08-11 11:00:02 [WARN] /dev/sda READ RETRY retry=1
2026-08-11 11:00:03 [ERROR] /dev/sda READ ERROR sector=123
2026-08-11 11:00:04 [INFO] /dev/sdb WRITE PASS
2026-08-11 11:00:05 [WARN] /dev/sdb WRITE RETRY retry=2
2026-08-11 11:00:06 [ERROR] /dev/sdb WRITE I/O ERROR timeout=30s
"""

pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[(?P<severity>\w+)\]\s(?P<device>/dev/\w+)\s(?P<message>.+)"

result = []

for match in re.finditer(pattern, text):
    data = match.groupdict()
    data["operation"] = data["message"].split()[0]
    result.append(data)

print(result)
```

## Engineering Lesson

Regex should extract stable structure.

Python can then interpret the message semantics.

---

# Q5 — Device-wise Error Analysis

## Scenario

```text
2026-08-11 12:00:01 [ERROR] /dev/sda READ ERROR sector=100
2026-08-11 12:00:02 [ERROR] /dev/sdb WRITE ERROR timeout=20s
2026-08-11 12:00:03 [ERROR] /dev/sda WRITE MEDIA ERROR block=200
2026-08-11 12:00:04 [INFO] /dev/sdc READ PASS
2026-08-11 12:00:05 [ERROR] /dev/sdb READ I/O ERROR timeout=30s
2026-08-11 12:00:06 [ERROR] /dev/sda READ ERROR sector=300
```

## Requirement

Group errors by device.

Expected:

```python
{
    "/dev/sda": [
        "READ ERROR",
        "WRITE MEDIA ERROR",
        "READ ERROR"
    ],
    "/dev/sdb": [
        "WRITE ERROR",
        "READ I/O ERROR"
    ]
}
```

## Solution

```python
import re

text = """
2026-08-11 12:00:01 [ERROR] /dev/sda READ ERROR sector=100
2026-08-11 12:00:02 [ERROR] /dev/sdb WRITE ERROR timeout=20s
2026-08-11 12:00:03 [ERROR] /dev/sda WRITE MEDIA ERROR block=200
2026-08-11 12:00:04 [INFO] /dev/sdc READ PASS
2026-08-11 12:00:05 [ERROR] /dev/sdb READ I/O ERROR timeout=30s
2026-08-11 12:00:06 [ERROR] /dev/sda READ ERROR sector=300
"""

pattern = r"(?P<device>/dev/\w+)\s(?P<error>(?P<operation>\w+)\s+(?:[\w/]+\s+)*ERROR)\s+(?P<diagnostic>\w+=.+)"

errors_by_device = {}

for match in re.finditer(pattern, text):
    data = match.groupdict()

    device = data["device"]
    error = data["error"]

    errors_by_device.setdefault(device, []).append(error)

print(errors_by_device)
```

## Engineering Lesson

Regex performs extraction.

Python data structures perform aggregation.

```text
Regex
  ↓
Extraction
  ↓
Dictionary/List
  ↓
Aggregation
```

---

# Q6 — Multi-line Diagnostic Parsing

## Scenario

Storage controller logs may contain multi-line diagnostics:

```text
2026-08-11 13:00:01 [ERROR] /dev/sda READ ERROR
sector=182736
sense=0x03
retry=5
2026-08-11 13:00:05 [INFO] /dev/sda TEST_END

2026-08-11 13:01:01 [ERROR] /dev/nvme0n1 WRITE I/O ERROR
opcode=0x01
status=0xC000
timeout=30s
2026-08-11 13:01:05 [INFO] /dev/nvme0n1 TEST_END
```

## Requirement

Associate continuation lines with the preceding ERROR record.

Expected:

```python
{
    "device": "/dev/sda",
    "error": "READ ERROR",
    "diagnostic": [
        "sector=182736",
        "sense=0x03",
        "retry=5"
    ]
}
```

## Key Concept

A new record begins when a line starts with a timestamp.

Therefore:

```text
ERROR record
     ↓
continuation lines
     ↓
next timestamped record
```

## Pattern

```regex
(?P<diagnostic>(?:\n(?!\d{4}-\d{2}-\d{2}).+)*)
```

## Solution

```python
import re

text = """
2026-08-11 13:00:01 [ERROR] /dev/sda READ ERROR
sector=182736
sense=0x03
retry=5
2026-08-11 13:00:05 [INFO] /dev/sda TEST_END
2026-08-11 13:01:01 [ERROR] /dev/nvme0n1 WRITE I/O ERROR
opcode=0x01
status=0xC000
timeout=30s
2026-08-11 13:01:05 [INFO] /dev/nvme0n1 TEST_END
"""

pattern = re.compile(
    r"(?m)^(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})"
    r"\s+\[ERROR\]\s+(?P<device>/dev/\w+)\s+"
    r"(?P<error>(?P<operation>\w+)\s+(?:[\w/]+\s+)*ERROR)"
    r"(?P<diagnostic>(?:\n(?!\d{4}-\d{2}-\d{2}).+)*)"
)

result = []

for match in pattern.finditer(text):
    data = match.groupdict()

    data["diagnostic"] = [
        line.strip()
        for line in data["diagnostic"].splitlines()
        if line.strip()
    ]

    result.append(data)

print(result)
```

## Engineering Lesson

Multi-line logs introduce:

```text
Record start
Record continuation
Record end
```

For complex production logs, a line-by-line state machine may be easier to maintain than one giant regex.

---

# Q7 — Correlating Events Within a Test Run

## Scenario

```text
2026-08-11 14:00:01 [INFO] /dev/sda TEST_START
2026-08-11 14:00:02 [INFO] /dev/sda READ PASS
2026-08-11 14:00:03 [INFO] /dev/sda WRITE PASS
2026-08-11 14:00:04 [ERROR] /dev/sda READ ERROR sector=100
2026-08-11 14:00:05 [INFO] /dev/sda TEST_END

2026-08-11 14:01:01 [INFO] /dev/sdb TEST_START
2026-08-11 14:01:02 [INFO] /dev/sdb READ PASS
2026-08-11 14:01:03 [INFO] /dev/sdb WRITE PASS
2026-08-11 14:01:04 [INFO] /dev/sdb TEST_END
```

## Requirement

Produce:

```python
{
    "device": "...",
    "started": True,
    "completed": True,
    "failed": True/False,
    "errors": [...]
}
```

Expected:

```python
[
    {
        "device": "/dev/sda",
        "started": True,
        "completed": True,
        "failed": True,
        "errors": ["READ ERROR"]
    },
    {
        "device": "/dev/sdb",
        "started": True,
        "completed": True,
        "failed": False,
        "errors": []
    }
]
```

## Engineering Concept

This introduces state.

The parser needs to track:

```text
Which device?
TEST_START?
TEST_END?
ERROR?
```

Regex extracts events.

Python maintains state.

## Solution

```python
import re

text = """
2026-08-11 14:00:01 [INFO] /dev/sda TEST_START
2026-08-11 14:00:02 [INFO] /dev/sda READ PASS
2026-08-11 14:00:03 [INFO] /dev/sda WRITE PASS
2026-08-11 14:00:04 [ERROR] /dev/sda READ ERROR sector=100
2026-08-11 14:00:05 [INFO] /dev/sda TEST_END

2026-08-11 14:01:01 [INFO] /dev/sdb TEST_START
2026-08-11 14:01:02 [INFO] /dev/sdb READ PASS
2026-08-11 14:01:03 [INFO] /dev/sdb WRITE PASS
2026-08-11 14:01:04 [INFO] /dev/sdb TEST_END
"""

pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[(?P<severity>\w+)\]\s(?P<device>/dev/\w+)\s(?P<message>.+)"

tests = {}

for match in re.finditer(pattern, text):
    data = match.groupdict()

    device = data["device"]
    message = data["message"]

    if device not in tests:
        tests[device] = {
            "device": device,
            "started": False,
            "completed": False,
            "failed": False,
            "errors": []
        }

    if message == "TEST_START":
        tests[device]["started"] = True

    elif message == "TEST_END":
        tests[device]["completed"] = True

    elif data["severity"] == "ERROR":
        tests[device]["failed"] = True
        tests[device]["errors"].append(
            message.split(" sector")[0]
        )

result = list(tests.values())

print(result)
```

## Engineering Lesson

This is the transition from a Regex problem to a log-processing automation problem.

```text
Regex
  ↓
Extract events

Python
  ↓
Maintain state

Python
  ↓
Correlate events
```

---

# Q8 — Noisy / Mixed Storage Logs

## Scenario

Real storage logs contain unrelated lines:

```text
Starting storage validation...
2026-08-11 15:00:01 [INFO] /dev/sda TEST_START
DEBUG controller queue initialized
2026-08-11 15:00:02 [INFO] /dev/sda READ PASS
random diagnostic text
2026-08-11 15:00:03 [ERROR] /dev/sda READ ERROR sector=123
WARNING: temperature approaching threshold
2026-08-11 15:00:04 [INFO] /dev/sda TEST_END
```

## Requirement

Extract only valid timestamped storage records.

Ignore:

```text
Starting storage validation...
DEBUG controller queue initialized
random diagnostic text
WARNING: temperature approaching threshold
```

## Valid Record Structure

```text
TIMESTAMP
+
SEVERITY
+
DEVICE
+
MESSAGE
```

## Pattern

```regex
(?m)^(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+\[(?P<severity>\w+)\]\s+(?P<device>/dev/\w+)\s+(?P<message>.+)$
```

## Solution

```python
import re

text = """
Starting storage validation...
2026-08-11 15:00:01 [INFO] /dev/sda TEST_START
DEBUG controller queue initialized
2026-08-11 15:00:02 [INFO] /dev/sda READ PASS
random diagnostic text
2026-08-11 15:00:03 [ERROR] /dev/sda READ ERROR sector=123
WARNING: temperature approaching threshold
2026-08-11 15:00:04 [INFO] /dev/sda TEST_END
"""

pattern = (
    r"(?m)^(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})"
    r"\s+\[(?P<severity>\w+)\]\s+"
    r"(?P<device>/dev/\w+)\s+(?P<message>.+)$"
)

result = []

for match in re.finditer(pattern, text):
    result.append(match.groupdict())

print(result)
```

## Engineering Lesson

Production logs are noisy.

A robust parser should recognize valid records and ignore unrelated lines.

---

# Q9 — Structured Storage Test Results

## Scenario

```text
2026-08-11 16:00:01 [INFO] /dev/sda TEST_START
2026-08-11 16:00:02 [INFO] /dev/sda READ PASS
2026-08-11 16:00:03 [ERROR] /dev/sda WRITE ERROR timeout=30s
2026-08-11 16:00:04 [INFO] /dev/sda TEST_END
2026-08-11 16:01:01 [INFO] /dev/sdb TEST_START
2026-08-11 16:01:02 [INFO] /dev/sdb READ PASS
2026-08-11 16:01:03 [INFO] /dev/sdb WRITE PASS
2026-08-11 16:01:04 [INFO] /dev/sdb TEST_END
```

## Requirement

Produce:

```python
[
    {
        "device": "/dev/sda",
        "status": "FAIL",
        "error_count": 1,
        "errors": [
            {
                "operation": "WRITE",
                "error": "WRITE ERROR",
                "diagnostic": "timeout=30s"
            }
        ]
    },
    {
        "device": "/dev/sdb",
        "status": "PASS",
        "error_count": 0,
        "errors": []
    }
]
```

## Engineering Pipeline

```text
Raw Log
   ↓
Regex Parsing
   ↓
Structured Events
   ↓
Group by Device
   ↓
Detect Errors
   ↓
Calculate Status
   ↓
Generate Report
```

## Solution

```python
import re

text = """
2026-08-11 16:00:01 [INFO] /dev/sda TEST_START
2026-08-11 16:00:02 [INFO] /dev/sda READ PASS
2026-08-11 16:00:03 [ERROR] /dev/sda WRITE ERROR timeout=30s
2026-08-11 16:00:04 [INFO] /dev/sda TEST_END
2026-08-11 16:01:01 [INFO] /dev/sdb TEST_START
2026-08-11 16:01:02 [INFO] /dev/sdb READ PASS
2026-08-11 16:01:03 [INFO] /dev/sdb WRITE PASS
2026-08-11 16:01:04 [INFO] /dev/sdb TEST_END
"""

pattern = (
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})"
    r"\s+\[(?P<severity>\w+)\]\s+"
    r"(?P<device>/dev/\w+)\s+(?P<message>.+)"
)

error_pattern = re.compile(
    r"(?P<operation>\w+)\s+"
    r"(?P<error>(?:[\w/]+\s+)*ERROR)\s+"
    r"(?P<diagnostic>\w+=.+)"
)

devices = {}

for match in re.finditer(pattern, text):
    data = match.groupdict()

    device = data["device"]

    if device not in devices:
        devices[device] = {
            "device": device,
            "errors": []
        }

    error_match = error_pattern.fullmatch(data["message"])

    if data["severity"] == "ERROR" and error_match:
        devices[device]["errors"].append(
            error_match.groupdict()
        )

result = []

for data in devices.values():
    result.append({
        "device": data["device"],
        "status": "FAIL" if data["errors"] else "PASS",
        "error_count": len(data["errors"]),
        "errors": data["errors"]
    })

print(result)
```

## Engineering Lesson

A real parser is usually a pipeline:

```text
Regex
  ↓
Extraction
  ↓
Python Data Structures
  ↓
Aggregation
  ↓
Analysis
  ↓
Report
```

---

# Q10 — Final Enterprise Storage Log Parser

## Scenario

This is the final challenge of `12_Log_Parsing.md`.

The Storage Validation framework produces:

```text
2026-08-11 17:00:01 [INFO] /dev/sda TEST_START
2026-08-11 17:00:02 [INFO] /dev/sda READ PASS
2026-08-11 17:00:03 [INFO] /dev/sda WRITE PASS
2026-08-11 17:00:04 [ERROR] /dev/sda READ ERROR sector=182736 retry=2
2026-08-11 17:00:05 [INFO] /dev/sda TEST_END

2026-08-11 17:01:01 [INFO] /dev/sdb TEST_START
2026-08-11 17:01:02 [INFO] /dev/sdb READ PASS
2026-08-11 17:01:03 [WARN] /dev/sdb WRITE RETRY retry=3
2026-08-11 17:01:04 [ERROR] /dev/sdb WRITE I/O ERROR timeout=30s queue=7
2026-08-11 17:01:05 [INFO] /dev/sdb TEST_END

Controller initialization complete
DEBUG queue depth=32

2026-08-11 17:02:01 [INFO] /dev/nvme0n1 TEST_START
2026-08-11 17:02:02 [INFO] /dev/nvme0n1 READ PASS
2026-08-11 17:02:03 [INFO] /dev/nvme0n1 WRITE PASS
2026-08-11 17:02:04 [INFO] /dev/nvme0n1 TEST_END
```

## Requirement

Produce one structured result per device:

```python
[
    {
        "device": "/dev/sda",
        "started": True,
        "completed": True,
        "status": "FAIL",
        "error_count": 1,
        "errors": [...]
    },
    {
        "device": "/dev/sdb",
        "started": True,
        "completed": True,
        "status": "FAIL",
        "error_count": 1,
        "errors": [...]
    },
    {
        "device": "/dev/nvme0n1",
        "started": True,
        "completed": True,
        "status": "PASS",
        "error_count": 0,
        "errors": []
    }
]
```

Each error must contain:

```python
{
    "timestamp": "...",
    "operation": "...",
    "error": "...",
    "diagnostic": "..."
}
```

## Final Challenge Requirements

The parser must:

* ignore unrelated lines
* recognize storage records
* identify devices
* identify `TEST_START`
* identify `TEST_END`
* identify ERROR records
* handle variable-length error messages
* extract diagnostics
* group events by device
* calculate error count
* determine PASS/FAIL
* produce structured Python data

## Final Engineering Architecture

```text
                    RAW LOG
                       |
                       v
              Record Recognition
                       |
                       v
              Field Extraction
                       |
                       v
              Event Classification
                       |
                       v
               Device Grouping
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

## Final Engineering Lesson

The objective is NOT to create one giant regex.

The objective is to build a reliable parser using the right tool for each task.

```text
Regex
  ↓
Recognize and extract structure

Python
  ↓
Store information

Python
  ↓
Correlate events

Python
  ↓
Analyze failures

Python
  ↓
Generate report
```

A maintainable Storage Test parser is a pipeline rather than one enormous regular expression.

---

# Overall Progression

| Question | Topic                                | Difficulty |
| -------- | ------------------------------------ | ---------- |
| Q1       | Basic Storage Log Field Extraction   | 🟢         |
| Q2       | Variable Error Formats               | 🟢 → 🟡    |
| Q3       | Multiple Devices and Error Filtering | 🟡         |
| Q4       | Event Classification                 | 🟡         |
| Q5       | Device-wise Error Analysis           | 🟡 → 🟠    |
| Q6       | Multi-line Diagnostic Parsing        | 🟠         |
| Q7       | Test-run Event Correlation           | 🟠         |
| Q8       | Noisy / Mixed Storage Logs           | 🟠 → 🔴    |
| Q9       | Structured Storage Test Results      | 🔴         |
| Q10      | Final Enterprise Storage Log Parser  | 🔴🔥       |

---

# Completion Criteria

`12_Log_Parsing.md` is complete when:

```text
Q1  → Completed
Q2  → Completed
Q3  → Completed
Q4  → Completed
Q5  → Completed
Q6  → Completed
Q7  → Completed
Q8  → Completed
Q9  → Completed
Q10 → Completed
```



---

# Final Skill Target

The final target of this module is:

```text
Raw Storage Log
       ↓
Identify record structure
       ↓
Identify record boundaries
       ↓
Extract fields
       ↓
Filter events
       ↓
Classify events
       ↓
Group by device/test
       ↓
Correlate related events
       ↓
Handle noisy/multi-line data
       ↓
Build structured Python objects
       ↓
Analyze failures
       ↓
Generate automated test results
```

---

