# 10 — Pattern Matching

## Module 06 — Regular Expressions

## Purpose

This section focuses on applying Python Regular Expressions to **real Storage Testing and Storage Test Automation scenarios**.

The objective is not simply to memorize:

```text
re.search()
re.match()
re.fullmatch()
re.findall()
re.finditer()
````

The objective is to develop the ability to take a **Storage Testing requirement** and naturally derive:

```text
Requirement
    ↓
Understand exactly what is required
    ↓
Choose the correct regex API
    ↓
Identify what must be matched
    ↓
Identify what must be captured
    ↓
Identify boundaries / restrictions
    ↓
Choose lookarounds if required
    ↓
Choose greedy / lazy matching if required
    ↓
Choose flags if required
    ↓
Build the regex
    ↓
Execute and inspect the result
    ↓
Validate against the requirement
```

---

# 1. Pattern Matching APIs

The primary Python `re` pattern-matching APIs are:

```python
re.search()
re.match()
re.fullmatch()
re.findall()
re.finditer()
```

They should not be treated as interchangeable.

The correct API depends on the actual requirement.

---

# 2. `re.search()`

## Purpose

`re.search()` searches for the **first occurrence** of a pattern anywhere in the string.

Syntax:

```python
re.search(pattern, string)
```

If a match is found:

```text
Match object
```

is returned.

If no match is found:

```text
None
```

is returned.

---

## Storage Testing Example

Captured storage output:

```text
/dev/sda: PASS
/dev/sdb: PASS
/dev/nvme0n1: I/O ERROR
/dev/sdc: PASS
/dev/nvme1n1: I/O ERROR
```

Requirement:

> Find the first occurrence of `I/O ERROR`.

Solution:

```python
import re

text = """/dev/sda: PASS
/dev/sdb: PASS
/dev/nvme0n1: I/O ERROR
/dev/sdc: PASS
/dev/nvme1n1: I/O ERROR
"""

pattern = r"I/O ERROR"

result = re.search(pattern, text)

if result:
    print("I/O ERROR Detected")
else:
    print("I/O ERROR not Detected")
```

Output:

```text
I/O ERROR Detected
```

---

## Why `re.search()`?

The requirement says:

> Find the first occurrence.

Therefore:

```text
Requirement
    ↓
First occurrence anywhere
    ↓
re.search()
```

`re.search()` stops after finding the first match.

---

## Important Difference

`re.search()` does **not** mean:

> Search only at the beginning.

It means:

> Search anywhere and return the first match.

Example:

```python
import re

text = "HDD SSD NVMe"

result = re.search(r"SSD", text)

print(result.group())
```

Output:

```text
SSD
```

Even though `SSD` is not at the beginning.

---

# 3. `re.match()`

## Purpose

`re.match()` checks whether the pattern matches at the **beginning of the string**.

Syntax:

```python
re.match(pattern, string)
```

It does not continue searching later in the string when the beginning does not match.

---

## Example

```python
import re

text = "HDD SSD NVMe"

result = re.match(r"SSD", text)

print(result)
```

Output:

```text
None
```

Why?

The string starts with:

```text
HDD
```

but the pattern is:

```text
SSD
```

`re.match()` checks the starting position and fails.

It does not continue forward to the later `SSD`.

---

## Successful Example

```python
import re

text = "SSD HDD SSD"

result = re.match(r"SSD", text)

print(result.group())
```

Output:

```text
SSD
```

Because the pattern matches the beginning of the string.

---

## Mental Model

```text
re.match()
    ↓
Check position 0
    ↓
Does pattern match?
    ├── Yes → Match object
    └── No  → None
```

---

# 4. `re.fullmatch()`

## Purpose

`re.fullmatch()` requires the **entire string** to match the pattern.

Syntax:

```python
re.fullmatch(pattern, string)
```

---

## Example

```python
import re

text = "SSD"

result = re.fullmatch(r"SSD", text)

print(result.group())
```

Output:

```text
SSD
```

The entire input is:

```text
SSD
```

and the pattern also matches:

```text
SSD
```

Therefore the match succeeds.

---

## Failure Example

```python
import re

text = "SSD-1234"

result = re.fullmatch(r"SSD", text)

print(result)
```

Output:

```text
None
```

Why?

The pattern matches only:

```text
SSD
```

but the complete input is:

```text
SSD-1234
```

The entire input must match for `re.fullmatch()` to succeed.

---

## Mental Model

```text
re.search()
    → Pattern can occur anywhere

re.match()
    → Pattern must start at position 0

re.fullmatch()
    → Pattern must cover the entire input
```

---

## Storage Testing Use Case

`re.fullmatch()` is useful when the requirement is:

> Validate that the complete device identifier or complete storage field follows a required format.

---

# 5. `re.findall()`

## Purpose

`re.findall()` finds **all occurrences** of a pattern.

Syntax:

```python
re.findall(pattern, string)
```

It returns a list.

---

## Example

```python
import re

text = "SSD HDD SSD NVMe SSD"

result = re.findall(r"SSD", text)

print(result)
```

Output:

```python
['SSD', 'SSD', 'SSD']
```

---

## No Match

```python
import re

text = "HDD NVMe"

result = re.findall(r"SSD", text)

print(result)
```

Output:

```python
[]
```

`findall()` returns an empty list when there are no matches.

It does not return `None`.

---

# 6. `findall()` with Capturing Groups

Example:

```python
import re

text = "Drive: SSD, Drive: HDD, Drive: NVMe"

result = re.findall(r"Drive: (\w+)", text)

print(result)
```

Output:

```python
['SSD', 'HDD', 'NVMe']
```

When `findall()` contains a capturing group, it returns the captured values.

---

## Important

`findall()` returns a list.

Therefore:

```python
result.group(1)
```

is not valid for the result of `findall()`.

Instead:

```python
result[0]
result[1]
result[2]
```

can be used.

---

# 7. Capturing Groups and `findall()`

Consider:

```python
import re

text = "Drive: SSD, Drive: HDD, Drive: NVMe"

result = re.findall(r"Drive: (\w+)", text)

print(result)
```

The regex contains:

```regex
(\w+)
```

which is **Group 1**.

There is still only one group even though there are three matches.

Conceptually:

```text
Pattern
    ↓
ONE capturing group

Drive: SSD
    ↓
Group 1 = SSD

Drive: HDD
    ↓
Group 1 = HDD

Drive: NVMe
    ↓
Group 1 = NVMe
```

---

# 8. `re.finditer()`

## Purpose

`re.finditer()` finds all matches and returns an **iterator of Match objects**.

Syntax:

```python
re.finditer(pattern, string)
```

---

## Example

```python
import re

text = "SSD HDD SSD NVMe SSD"

result = re.finditer(r"SSD", text)

for match in result:
    print(match.group())
```

Output:

```text
SSD
SSD
SSD
```

---

## Difference Between `findall()` and `finditer()`

```text
re.findall()
    ↓
List of matched values

re.finditer()
    ↓
Iterator of Match objects
```

---

## Why `finditer()` Is Useful

`finditer()` is useful when we need detailed information about each match:

```text
Matched value
Start position
End position
Span
Capturing groups
Named groups
Other Match object information
```

This becomes particularly useful in:

```text
Storage Log Parsing
Storage Test Automation
Error Position Detection
Structured Extraction
Validation
```

---

# 9. Match Objects

The following APIs can return Match objects:

```text
re.search()
re.match()
re.fullmatch()
re.finditer()
```

Important Match-object methods include:

```python
match.group()
match.group(0)
match.group(1)
match.group(2)
match.groups()
match.start()
match.end()
match.span()
match.groupdict()
```

---

# 10. `match.group()`

Returns the complete matched text.

Example:

```python
import re

text = "Drive: SSD"

match = re.search(r"Drive: (\w+)", text)

print(match.group())
```

Output:

```text
Drive: SSD
```

---

# 11. `match.group(0)`

`group(0)` represents the complete match.

Therefore:

```python
match.group()
```

and:

```python
match.group(0)
```

refer to the same complete match.

Example:

```python
import re

text = "Drive: SSD"

match = re.search(r"Drive: (\w+)", text)

print(match.group())
print(match.group(0))
```

Output:

```text
Drive: SSD
Drive: SSD
```

---

# 12. `match.group(1)`

If the pattern contains a capturing group:

```regex
Drive: (\w+)
```

then:

```python
match.group(1)
```

returns the value captured by Group 1.

Example:

```python
print(match.group(1))
```

Output:

```text
SSD
```

---

# 13. Multiple Capturing Groups

Example:

```python
import re

text = "Drive: SSD Capacity: 1TB"

match = re.search(
    r"Drive: (\w+) Capacity: (\d+\w+)",
    text
)

print(match.group())
print(match.group(0))
print(match.group(1))
print(match.group(2))
print(match.groups())
```

Output:

```text
Drive: SSD Capacity: 1TB
Drive: SSD Capacity: 1TB
SSD
1TB
('SSD', '1TB')
```

---

## Mental Model

```text
group(0)
    ↓
Entire match

group(1)
    ↓
First capturing group

group(2)
    ↓
Second capturing group

groups()
    ↓
All capturing groups as a tuple
```

---

# 14. `match.start()`

Returns the starting index of the match.

Example:

```python
import re

text = "HDD Drive: SSD"

match = re.search(r"SSD", text)

print(match.start())
```

Output:

```text
10
```

The first character of `SSD` is at index `10`.

---

# 15. `match.end()`

Returns the index immediately **after** the match.

For:

```text
SSD
```

starting at index `10`:

```text
10 → S
11 → S
12 → D
13 → end
```

Therefore:

```python
match.end()
```

returns:

```text
13
```

---

## Important

`end()` is **exclusive**.

---

# 16. `match.span()`

Returns:

```text
(start, end)
```

Example:

```python
import re

text = "HDD Drive: SSD"

match = re.search(r"SSD", text)

print(match.span())
```

Output:

```text
(10, 13)
```

Therefore:

```text
start() → 10
end()   → 13
span()  → (10, 13)
```

---

# 17. Named Capturing Groups

Numbered groups:

```python
match.group(1)
match.group(2)
```

can become difficult to remember when extracting many fields.

Python supports **named capturing groups**.

Syntax:

```regex
(?P<name>pattern)
```

---

## Example

```python
import re

text = "Drive: SSD Capacity: 1TB"

pattern = r"Drive: (?P<type>\w+) Capacity: (?P<capacity>\d+\w+)"

match = re.search(pattern, text)
```

Now:

```python
match.group("type")
```

returns:

```text
SSD
```

and:

```python
match.group("capacity")
```

returns:

```text
1TB
```

---

# 18. `match.groupdict()`

`groupdict()` converts named capturing groups into a dictionary.

Example:

```python
print(match.groupdict())
```

Output:

```python
{
    "type": "SSD",
    "capacity": "1TB"
}
```

---

## Important

Dictionary keys come from:

```regex
(?P<name>...)
```

For example:

```regex
(?P<type>\w+)
```

creates the key:

```text
type
```

---

# 19. Storage Testing Pattern-Matching Methodology

We now move from learning each API separately to using them in realistic Storage Testing scenarios.

The engineering workflow is:

```text
Storage Testing Requirement
        ↓
Understand exactly what is required
        ↓
First or all?
        ↓
Where is the target?
        ↓
What must be captured?
        ↓
What must only be verified?
        ↓
What separates the required information?
        ↓
Do I need capturing groups?
        ↓
Do I need lookarounds?
        ↓
Do I need lazy matching?
        ↓
Do I need flags?
        ↓
Choose the simplest correct API + regex
```

---

# Level 1 — Find All Failed Devices

## Storage Test Output

```text
/dev/sda: PASS
/dev/sdb: PASS
/dev/nvme0n1: I/O ERROR
/dev/sdc: PASS
/dev/nvme1n1: I/O ERROR
```

## Requirement

> Extract every device that reports `I/O ERROR`.

Expected:

```python
[
    "/dev/nvme0n1",
    "/dev/nvme1n1"
]
```

---

## Solution

```python
import re

text = """/dev/sda: PASS
/dev/sdb: PASS
/dev/nvme0n1: I/O ERROR
/dev/sdc: PASS
/dev/nvme1n1: I/O ERROR
"""

pattern = r"/dev/\w+(?=:\sI/O\sERROR)"

result = re.findall(pattern, text)

print(result)
```

Output:

```python
['/dev/nvme0n1', '/dev/nvme1n1']
```

---

## Thought Process

### Requirement

We need:

```text
ALL failed devices
```

Therefore:

```text
re.findall()
```

---

### Device Pattern

```regex
/dev/\w+
```

matches:

```text
/dev/sda
/dev/sdb
/dev/nvme0n1
/dev/nvme1n1
```

---

### Failure Condition

The device must be followed by:

```text
: I/O ERROR
```

Therefore:

```regex
(?=:\sI/O\sERROR)
```

is used.

This is a **positive lookahead**.

It verifies the condition without consuming the error text.

---

## Engineering Lesson

When the requirement changes from:

```text
Find the first failed device
```

to:

```text
Find ALL failed devices
```

the API changes naturally:

```text
First
 ↓
re.search()

All
 ↓
re.findall()
```

---

# Level 2 — Any Error Type

## Storage Test Output

```text
/dev/sda: PASS
/dev/sdb: READ ERROR
/dev/nvme0n1: I/O ERROR
/dev/sdc: PASS
/dev/nvme1n1: WRITE ERROR
```

## Requirement

> Extract every device that has any error status.

The exact error type is not important.

Expected:

```python
[
    "/dev/sdb",
    "/dev/nvme0n1",
    "/dev/nvme1n1"
]
```

---

## Solution

```python
import re

text = """/dev/sda: PASS
/dev/sdb: READ ERROR
/dev/nvme0n1: I/O ERROR
/dev/sdc: PASS
/dev/nvme1n1: WRITE ERROR
"""

pattern = r"/dev/\w+(?=.*ERROR)"

result = re.findall(pattern, text)

print(result)
```

Output:

```python
['/dev/sdb', '/dev/nvme0n1', '/dev/nvme1n1']
```

---

## Thought Process

We don't want to hard-code:

```text
READ ERROR
I/O ERROR
WRITE ERROR
```

because the exact error type is not part of the requirement.

Instead:

```text
Device
   ↓
Must have ERROR later on the same line
```

Therefore:

```regex
/dev/\w+(?=.*ERROR)
```

The positive lookahead:

```regex
(?=.*ERROR)
```

verifies that `ERROR` appears later on the line.

Because `.` does not match newline by default, the lookahead does not cross into the next line.

---

# Level 3 — Extract Device + Error Type

## Storage Test Output

```text
/dev/sda: PASS
/dev/sdb: READ ERROR
/dev/nvme0n1: I/O ERROR
/dev/sdc: PASS
/dev/nvme1n1: WRITE ERROR
```

## Requirement

Extract:

1. Device name
2. Error type

Expected:

```python
[
    ("/dev/sdb", "READ ERROR"),
    ("/dev/nvme0n1", "I/O ERROR"),
    ("/dev/nvme1n1", "WRITE ERROR")
]
```

---

## Solution

```python
import re

text = """/dev/sda: PASS
/dev/sdb: READ ERROR
/dev/nvme0n1: I/O ERROR
/dev/sdc: PASS
/dev/nvme1n1: WRITE ERROR
"""

pattern = r"(/dev/\w+):\s(.*ERROR)"

result = re.findall(pattern, text)

print(result)
```

Output:

```python
[
    ('/dev/sdb', 'READ ERROR'),
    ('/dev/nvme0n1', 'I/O ERROR'),
    ('/dev/nvme1n1', 'WRITE ERROR')
]
```

---

## Thought Process

Now we need **two pieces of information**.

Therefore we use two capturing groups.

### Group 1 — Device

```regex
(/dev/\w+)
```

### Separator

```regex
:\s
```

### Group 2 — Error

```regex
(.*ERROR)
```

Therefore:

```regex
(/dev/\w+):\s(.*ERROR)
```

Because there are two capturing groups, `findall()` returns:

```text
(group1, group2)
```

for every match.

---

# Level 3 — Lookaround Alternative

If the requirement were only:

> Extract the failed device names.

we could use:

```regex
/dev/\w+(?=:\s.*ERROR)
```

The lookahead verifies that the device's line contains an error.

However, when the requirement is:

```text
Device + Error
```

the capturing-group solution is simpler:

```regex
(/dev/\w+):\s(.*ERROR)
```

---

## Engineering Lesson

Knowing a feature does not mean it should always be used.

Use the simplest regex that clearly satisfies the requirement.

---

# Level 4 — First Complete Error Log Line

## Storage Log

```text
2026-08-10 10:15:01 /dev/sda test started
2026-08-10 10:15:02 /dev/sda read PASS
2026-08-10 10:15:03 /dev/sda I/O ERROR during sequential read
2026-08-10 10:15:04 /dev/sda test completed
2026-08-10 10:16:01 /dev/sdb test started
2026-08-10 10:16:02 /dev/sdb read PASS
```

## Requirement

> Find the first complete log line containing `I/O ERROR`.

Expected:

```text
2026-08-10 10:15:03 /dev/sda I/O ERROR during sequential read
```

---

## Regex

```regex
^.*I/O ERROR.*$
```

---

## Flag

Use:

```python
re.M
```

because the input contains multiple lines and `^` / `$` need to operate on individual lines.

---

## API

The requirement says:

> Find the first matching line.

Therefore the most precise API is:

```python
re.search()
```

Example:

```python
import re

text = """
2026-08-10 10:15:01 /dev/sda test started
2026-08-10 10:15:02 /dev/sda read PASS
2026-08-10 10:15:03 /dev/sda I/O ERROR during sequential read
2026-08-10 10:15:04 /dev/sda test completed
2026-08-10 10:16:01 /dev/sdb test started
2026-08-10 10:16:02 /dev/sdb read PASS
"""

pattern = r"^.*I/O ERROR.*$"

result = re.search(pattern, text, re.M)

if result:
    print(result.group())
```

Output:

```text
2026-08-10 10:15:03 /dev/sda I/O ERROR during sequential read
```

---

## Why `re.M`?

Without `re.M`:

```regex
^
$
```

refer to the beginning and end of the **entire string**.

With:

```python
re.M
```

they operate at the beginning and end of **each line**.

Therefore:

```regex
^.*I/O ERROR.*$
```

means:

```text
Beginning of line
       ↓
Anything
       ↓
I/O ERROR
       ↓
Anything
       ↓
End of line
```

---

## Important API Distinction

If we used:

```python
re.findall(pattern, text, re.M)
```

we would get **all matching lines**.

If we use:

```python
re.search(pattern, text, re.M)
```

we get the **first matching line**.

Therefore:

```text
First
 ↓
search()

All
 ↓
findall()
```

---

# Level 5 — Status + Diagnostic Information

## Storage Test Output

```text
/dev/sda: PASS
/dev/sdb: READ ERROR - sector 182736
/dev/nvme0n1: I/O ERROR - timeout
/dev/sdc: PASS
/dev/nvme1n1: MEDIA ERROR - unrecoverable
/dev/sde: COMMAND ABORTED - timeout
```

## Requirement

Extract every device whose status is **not `PASS`**.

Capture:

1. Device
2. Complete status

Ignore the diagnostic information beginning with:

```text
 -
```

Expected:

```python
[
    ("/dev/sdb", "READ ERROR"),
    ("/dev/nvme0n1", "I/O ERROR"),
    ("/dev/nvme1n1", "MEDIA ERROR"),
    ("/dev/sde", "COMMAND ABORTED")
]
```

---

# Level 5 — Thought Process

This level introduces a new problem:

The error/status names are **not fixed**.

We could have:

```text
READ ERROR
I/O ERROR
MEDIA ERROR
COMMAND ABORTED
```

and potentially many other error types.

Therefore we should not hard-code:

```regex
READ ERROR|WRITE ERROR|I/O ERROR|MEDIA ERROR|...
```

Instead, we should use the **structure of the log**.

The structure is:

```text
/device: STATUS - diagnostic
```

---

## Step 1 — Capture the Device

```regex
(/dev/\w+)
```

---

## Step 2 — Match the Separator

```regex
:\s
```

---

## Step 3 — Capture the Status

We need:

```text
READ ERROR
I/O ERROR
MEDIA ERROR
COMMAND ABORTED
```

but not:

```text
- sector 182736
- timeout
- unrecoverable
- LBA ...
```

The important boundary is:

```text
 -
```

---

## Step 4 — Lazy Matching

Use:

```regex
(.+?)
```

The lazy quantifier means:

> Capture as little as possible while still allowing the rest of the pattern to succeed.

---

## Step 5 — Positive Lookahead

We want to stop immediately before:

```text
 -
```

Therefore:

```regex
(?= -)
```

is used.

It means:

> Assert that ` -` comes next, but do not consume it.

---

## Step 6 — Build the Status Pattern

```regex
(.+?)(?= -)
```

This means:

```text
Capture status lazily
        ↓
Stop when " -" is immediately ahead
```

---

## Step 7 — Complete Pattern

```regex
(/dev/\w+):\s(.+?)(?= -)
```

---

## Complete Solution

```python
import re

text = """/dev/sda: PASS
/dev/sdb: READ ERROR - sector 182736
/dev/nvme0n1: I/O ERROR - timeout
/dev/sdc: PASS
/dev/nvme1n1: MEDIA ERROR - unrecoverable
/dev/sde: COMMAND ABORTED - timeout
"""

pattern = r"(/dev/\w+):\s(.+?)(?= -)"

result = re.findall(pattern, text)

print(result)
```

Output:

```python
[
    ('/dev/sdb', 'READ ERROR'),
    ('/dev/nvme0n1', 'I/O ERROR'),
    ('/dev/nvme1n1', 'MEDIA ERROR'),
    ('/dev/sde', 'COMMAND ABORTED')
]
```

---

## Level 5 Engineering Thought Process

The important part is not memorizing:

```regex
(.+?)(?= -)
```

The important thought process is:

```text
Requirement
    ↓
Need Device + Status
    ↓
Two capturing groups
    ↓
Where does Status end?
    ↓
Diagnostic boundary = " -"
    ↓
Need to stop BEFORE the boundary
    ↓
Lazy matching
    +
Positive lookahead
    ↓
(.+?)(?= -)
```

---

# Level 6 — Named Capturing Groups

## Storage Validation Output

```text
Drive=/dev/nvme0n1 Type=SSD Capacity=1TB Status=PASS
Drive=/dev/sda Type=HDD Capacity=500GB Status=FAIL
Drive=/dev/sdb Type=SSD Capacity=2TB Status=PASS
```

## Requirement

Extract every record into dictionaries containing:

```text
drive
type
capacity
status
```

Expected:

```python
[
    {
        "drive": "/dev/nvme0n1",
        "type": "SSD",
        "capacity": "1TB",
        "status": "PASS"
    },
    {
        "drive": "/dev/sda",
        "type": "HDD",
        "capacity": "500GB",
        "status": "FAIL"
    },
    {
        "drive": "/dev/sdb",
        "type": "SSD",
        "capacity": "2TB",
        "status": "PASS"
    }
]
```

---

# Level 6 — New Concept

Previously we used numbered capturing groups:

```regex
(group1)
(group2)
```

Now we use **named capturing groups**:

```regex
(?P<name>pattern)
```

This makes extracted fields easier to understand.

---

# Step 1 — Drive

```regex
(?P<drive>/dev/\w+)
```

---

# Step 2 — Type

```regex
(?P<type>\w+)
```

---

# Step 3 — Capacity

```regex
(?P<capacity>\d+(?:TB|GB|MB))
```

---

# Step 4 — Status

```regex
(?P<status>\w+)
```

---

# Complete Pattern

```regex
Drive=(?P<drive>/dev/\w+)\s+Type=(?P<type>\w+)\s+Capacity=(?P<capacity>\d+(?:TB|GB|MB))\s+Status=(?P<status>\w+)
```

---

# Why `(?:TB|GB|MB)`?

This:

```regex
(TB|GB|MB)
```

creates another capturing group.

But we don't need to separately extract:

```text
TB
GB
MB
```

Therefore use:

```regex
(?:TB|GB|MB)
```

This is a **non-capturing group**.

---

## Engineering Principle

> Do not create a capturing group unless you actually need to extract its value.

---

# Step 5 — Find Every Record

There are multiple storage records.

Therefore:

```python
matches = re.finditer(pattern, text)
```

returns an iterator of Match objects.

---

# Step 6 — Convert Match to Dictionary

Because we used named groups:

```python
match.groupdict()
```

returns:

```python
{
    "drive": "/dev/nvme0n1",
    "type": "SSD",
    "capacity": "1TB",
    "status": "PASS"
}
```

---

# Step 7 — Build the List

```python
result = []

for match in matches:
    result.append(match.groupdict())
```

---

# Complete Solution

```python
import re

text = """Drive=/dev/nvme0n1 Type=SSD Capacity=1TB Status=PASS
Drive=/dev/sda Type=HDD Capacity=500GB Status=FAIL
Drive=/dev/sdb Type=SSD Capacity=2TB Status=PASS"""

pattern = r"Drive=(?P<drive>/dev/\w+)\s+Type=(?P<type>\w+)\s+Capacity=(?P<capacity>\d+(?:TB|GB|MB))\s+Status=(?P<status>\w+)"

result = []

matches = re.finditer(pattern, text)

for match in matches:
    result.append(match.groupdict())

print(result)
```

Output:

```python
[
    {
        'drive': '/dev/nvme0n1',
        'type': 'SSD',
        'capacity': '1TB',
        'status': 'PASS'
    },
    {
        'drive': '/dev/sda',
        'type': 'HDD',
        'capacity': '500GB',
        'status': 'FAIL'
    },
    {
        'drive': '/dev/sdb',
        'type': 'SSD',
        'capacity': '2TB',
        'status': 'PASS'
    }
]
```

---

# Level 6 Engineering Thought Process

```text
Multiple storage records
        ↓
Need every record
        ↓
re.finditer()
        ↓
Each record → Match object
        ↓
Named capturing groups
        ↓
groupdict()
        ↓
Dictionary
        ↓
Append dictionaries to list
```

This converts semi-structured storage-test output into structured Python data.

---

# 20. API Selection — Storage Testing

## Requirement: Find First Occurrence

Use:

```python
re.search()
```

Mental model:

```text
Need first
    ↓
search()
```

---

## Requirement: Match Beginning

Use:

```python
re.match()
```

Mental model:

```text
Must start at position 0
    ↓
match()
```

---

## Requirement: Validate Entire Input

Use:

```python
re.fullmatch()
```

Mental model:

```text
Entire input must match
    ↓
fullmatch()
```

---

## Requirement: Find All Values

Use:

```python
re.findall()
```

Mental model:

```text
Need all values
    ↓
findall()
```

---

## Requirement: Find All Detailed Matches

Use:

```python
re.finditer()
```

Mental model:

```text
Need all matches
+
Match object details
    ↓
finditer()
```

---

# 21. Storage Testing Decision Examples

## First I/O Error

Requirement:

> Find the first `I/O ERROR`.

Use:

```python
re.search()
```

---

## Every Failed Device

Requirement:

> Extract every failed device.

Use:

```python
re.findall()
```

---

## Every Failed Device + Error

Requirement:

> Extract device and error for every failed drive.

Use:

```python
re.findall()
```

with capturing groups.

---

## Every Storage Record + Metadata

Requirement:

> Extract multiple structured records and convert them into dictionaries.

Use:

```python
re.finditer()
```

with:

```python
match.groupdict()
```

---

# 22. Engineering Regex Design Process

Do not start by writing random regex syntax.

Start from the requirement.

Ask:

```text
1. What exactly must be found?

2. Do I need the first occurrence or all occurrences?

3. Can the target occur anywhere?

4. Must the target be at the beginning?

5. Must the entire input match?

6. What information must be extracted?

7. Do I need capturing groups?

8. Would named groups make the result clearer?

9. What separates the required information from surrounding data?

10. Do I need a positive lookahead?

11. Do I need a negative lookahead?

12. Do I need lazy matching?

13. Do I need a regex flag?

14. Can the pattern be made simpler?

15. Does the final output exactly satisfy the requirement?
```

---

# 23. Storage Engineering Applications

The pattern-matching techniques learned here will later be applied to:

```text
Storage Test Automation
Storage Log Parsing
Failure Detection
SMART Output Parsing
dmesg Parsing
fio Output Parsing
Device Discovery
RAID Validation
NVMe Validation
SATA Validation
SAS Validation
Capacity Validation
Firmware Validation
I/O Error Detection
Drive Health Validation
```

---

# 24. Current Progress

```text
Level 1 — Find all failed devices
    ✅

Level 2 — Any error type
    ✅

Level 3 — Device + error type
    ✅

Level 4 — Complete error log line
    ✅

Level 5 — Status + diagnostic boundary
    ✅

Level 6 — Named structured extraction
    ✅
```

---

# 25. What Has Been Learned So Far

The progression so far has been intentional.

## Level 1

Learned to change:

```text
First match
```

into:

```text
All matches
```

by selecting:

```python
re.findall()
```

---

## Level 2

Learned to avoid hard-coding every possible error type.

Instead of:

```text
READ ERROR
I/O ERROR
WRITE ERROR
```

we used the structural condition:

```text
ERROR appears on the line
```

---

## Level 3

Introduced multiple capturing groups:

```regex
(device):(error)
```

and understood that `findall()` returns tuples when multiple capturing groups are present.

---

## Level 4

Introduced realistic multiline storage logs.

Combined:

```text
^
$
re.M
re.search()
```

to identify a complete error line.

---

## Level 5

Introduced a **dynamic status boundary**.

Instead of hard-coding error names, we used:

```text
status
    ↓
diagnostic separator
```

and designed:

```regex
(.+?)(?= -)
```

using:

```text
Lazy matching
+
Positive lookahead
```

---

## Level 6

Introduced:

```text
Named capturing groups
finditer()
groupdict()
Non-capturing groups
```

and converted semi-structured storage output into structured Python dictionaries.

---

# 26. Core Engineering Principle

Regex in Storage Testing is not about writing complicated patterns.

The real skill is:

> **Translate a storage-testing requirement into a precise matching strategy.**

Always ask:

```text
What do I need?

Where is it?

How many do I need?

What identifies it?

What separates it from surrounding data?

What must be captured?

What must only be verified?

Which API gives me exactly the required result?
```

---

# 27. Final Mental Model

```text
                 STORAGE REQUIREMENT
                         │
                         ▼
               What exactly is needed?
                         │
             ┌───────────┴───────────┐
             │                       │
          First                    All
             │                       │
        re.search()        ┌─────────┴─────────┐
                           │                   │
                       Values            Match objects
                           │                   │
                     re.findall()       re.finditer()
                                               
             Beginning?
                 │
            re.match()

             Entire input?
                 │
          re.fullmatch()
```

Then:

```text
Need extraction?
       │
       ▼
Capturing groups
       │
       ├── Numbered groups
       │
       └── Named groups
               │
          groupdict()
```

If the surrounding text must only be checked:

```text
Need verification without consuming?
       │
       ▼
Lookaround
```

If the endpoint is dynamic:

```text
Need to stop at a boundary?
       │
       ▼
Lazy matching + lookaround
```

If the data is multiline:

```text
Need line-based ^ and $?
       │
       ▼
re.M
```

---

# 28. Training Method Going Forward

The remaining pattern-matching training will continue **one scenario at a time**.

The difficulty will increase gradually.

The process will remain:

```text
New scenario
    ↓
Understand requirement
    ↓
Attempt solution
    ↓
Review solution
    ↓
Explain mistakes
    ↓
Introduce only the necessary new concept
    ↓
Increase difficulty
```

We will not jump several levels at once.

The objective is to make regex design **natural and requirement-driven**, especially for Storage Testing and Storage Test Automation.



---


# Level 7 — Multiline Storage Error Extraction

## Objective

This level introduces a more realistic storage-test log where multiple lines may contain errors.

The requirement is:

> Extract every complete log line containing an error.

This builds on the Level 4 concept of multiline matching, but now we need **all matching error lines** rather than the first one.

---

## Storage Test Output

```text
2026-08-10 10:15:01 /dev/sda test started
2026-08-10 10:15:02 /dev/sda read PASS
2026-08-10 10:15:03 /dev/sda I/O ERROR during sequential read
2026-08-10 10:15:04 /dev/sda test completed
2026-08-10 10:16:01 /dev/sdb test started
2026-08-10 10:16:02 /dev/sdb read PASS
2026-08-10 10:16:03 /dev/sdb WRITE ERROR during test
2026-08-10 10:16:04 /dev/sdb test completed
````

## Requirement

Extract every complete log line containing an error.

Expected:

```python
[
    "2026-08-10 10:15:03 /dev/sda I/O ERROR during sequential read",
    "2026-08-10 10:16:03 /dev/sdb WRITE ERROR during test"
]
```

---

# Level 7 — Thought Process

## Step 1 — Understand the Requirement

We need:

```text
ALL error lines
```

Not:

```text
first error line
```

Therefore the API should be:

```python
re.findall()
```

because:

```text
First match
    ↓
re.search()

All matches
    ↓
re.findall()
```

---

## Step 2 — What Should One Match Represent?

We don't just want:

```text
I/O ERROR
```

We want the **complete line**:

```text
2026-08-10 10:15:03 /dev/sda I/O ERROR during sequential read
```

Therefore the regex must match from:

```text
Beginning of line
```

to:

```text
End of line
```

---

## Step 3 — Line Beginning

Use:

```regex
^
```

This represents the beginning of a line when multiline mode is enabled.

---

## Step 4 — Match Anything Before the Error

We don't know exactly what appears before the error.

It can contain:

```text
timestamp
device
operation
```

Therefore:

```regex
.*
```

can represent the content before the error.

---

## Step 5 — Require an Error

The important part is:

```text
ERROR
```

We therefore include:

```regex
ERROR
```

We don't need to hard-code:

```text
I/O ERROR
WRITE ERROR
READ ERROR
```

because the requirement is simply:

> Find lines containing an error.

---

## Step 6 — Match Anything After the Error

The line may contain diagnostic information after the error:

```text
during sequential read
during test
```

Therefore:

```regex
.*
```

can match the remaining part of the line.

---

## Step 7 — End of Line

Use:

```regex
$
```

So the complete pattern becomes:

```regex
^.*ERROR.*$
```

---

## Step 8 — Multiline Flag

Our input contains multiple lines.

We want:

```text
^
```

and:

```text
$
```

to operate on every line.

Therefore:

```python
re.M
```

is required.

---

# Complete Solution

```python
import re

text = """
2026-08-10 10:15:01 /dev/sda test started
2026-08-10 10:15:02 /dev/sda read PASS
2026-08-10 10:15:03 /dev/sda I/O ERROR during sequential read
2026-08-10 10:15:04 /dev/sda test completed
2026-08-10 10:16:01 /dev/sdb test started
2026-08-10 10:16:02 /dev/sdb read PASS
2026-08-10 10:16:03 /dev/sdb WRITE ERROR during test
2026-08-10 10:16:04 /dev/sdb test completed
"""

pattern = r"^.*ERROR.*$"

result = re.findall(pattern, text, re.M)

print(result)
```

## Output

```python
[
    "2026-08-10 10:15:03 /dev/sda I/O ERROR during sequential read",
    "2026-08-10 10:16:03 /dev/sdb WRITE ERROR during test"
]
```

---

## Why `re.M` Is Important

Without:

```python
re.M
```

the anchors:

```regex
^
$
```

refer to the beginning and end of the entire string.

With:

```python
re.M
```

they refer to the beginning and end of each line.

Therefore:

```regex
^.*ERROR.*$
```

effectively means:

```text
Beginning of line
       ↓
Anything
       ↓
ERROR
       ↓
Anything
       ↓
End of line
```

for every line.

---

## Level 7 Engineering Lesson

The important decision was:

```text
Requirement
    ↓
Need ALL error lines
    ↓
re.findall()
    ↓
Need complete lines
    ↓
^ ... $
    ↓
Multiline input
    ↓
re.M
```

This is the same pattern-selection process used in real log parsing.

---

# Level 8 — Device + Error + Diagnostic

## Objective

Now we need to extract **three different pieces of information** from every failed storage device:

1. Device
2. Error status
3. Diagnostic information

This is more difficult because the status and diagnostic information are separated by a delimiter.

---

## Storage Test Output

```text
/dev/sda: PASS
/dev/sdb: READ ERROR - sector 182736
/dev/nvme0n1: I/O ERROR - timeout after 30s
/dev/sdc: PASS
/dev/nvme1n1: MEDIA ERROR - unrecoverable block
/dev/sde: COMMAND ABORTED - controller timeout
```

---

## Requirement

Extract:

```text
Device
Error status
Diagnostic information
```

for every failed drive.

Expected:

```python
[
    (
        "/dev/sdb",
        "READ ERROR",
        "sector 182736"
    ),
    (
        "/dev/nvme0n1",
        "I/O ERROR",
        "timeout after 30s"
    ),
    (
        "/dev/nvme1n1",
        "MEDIA ERROR",
        "unrecoverable block"
    ),
    (
        "/dev/sde",
        "COMMAND ABORTED",
        "controller timeout"
    )
]
```

---

# Level 8 — Thought Process

## Step 1 — Identify the Structure

Look at one failed record:

```text
/dev/sdb: READ ERROR - sector 182736
```

The structure is:

```text
DEVICE : STATUS - DIAGNOSTIC
```

So conceptually:

```text
(/device) : (status) - (diagnostic)
```

We need three capturing groups.

---

## Step 2 — Capture the Device

The device format is:

```text
/dev/sdb
/dev/nvme0n1
/dev/nvme1n1
/dev/sde
```

We already know:

```regex
/dev/\w+
```

Therefore:

```regex
(/dev/\w+)
```

is Group 1.

---

## Step 3 — Match the Separator

After the device:

```text
:
```

followed by whitespace.

Therefore:

```regex
:\s
```

---

## Step 4 — Capture the Status

The status can vary:

```text
READ ERROR
I/O ERROR
MEDIA ERROR
COMMAND ABORTED
```

We cannot safely hard-code all possible status names.

Instead, we use the structural boundary:

```text
 -
```

The status ends immediately before that delimiter.

Therefore we use lazy matching:

```regex
(.+?)
```

combined with:

```regex
(?= -)
```

The complete status portion becomes:

```regex
(.+?)(?= -)
```

This means:

> Capture the status lazily until ` -` is immediately ahead.

---

## Step 5 — Match the Diagnostic Separator

After the status we have:

```text
 -
```

We can consume it:

```regex
\s-\s
```

This represents:

```text
space
-
space
```

---

## Step 6 — Capture the Diagnostic

Everything remaining on the line is the diagnostic information.

Therefore:

```regex
(.+)
```

can capture it.

---

## Step 7 — Combine Everything

The structure becomes:

```regex
(/dev/\w+):\s(.+?)(?= -)\s-\s(.+)
```

We now have:

```text
Group 1 → Device
Group 2 → Status
Group 3 → Diagnostic
```

---

# Complete Solution

```python
import re

text = """/dev/sda: PASS
/dev/sdb: READ ERROR - sector 182736
/dev/nvme0n1: I/O ERROR - timeout after 30s
/dev/sdc: PASS
/dev/nvme1n1: MEDIA ERROR - unrecoverable block
/dev/sde: COMMAND ABORTED - controller timeout
"""

pattern = r"(/dev/\w+):\s(.+?)(?= -)\s-\s(.+)"

result = re.findall(pattern, text)

print(result)
```

## Output

```python
[
    ('/dev/sdb', 'READ ERROR', 'sector 182736'),
    ('/dev/nvme0n1', 'I/O ERROR', 'timeout after 30s'),
    ('/dev/nvme1n1', 'MEDIA ERROR', 'unrecoverable block'),
    ('/dev/sde', 'COMMAND ABORTED', 'controller timeout')
]
```

---

## Why Does `PASS` Not Match?

Consider:

```text
/dev/sda: PASS
```

Our regex requires:

```text
status
 -
```

But there is no:

```text
 -
```

after `PASS`.

Therefore the pattern fails.

That naturally filters out successful drives.

---

## Level 8 Engineering Lesson

The important reasoning is:

```text
Need 3 pieces of information
        ↓
3 capturing groups
        ↓
Device boundary
        ↓
Status boundary
        ↓
Diagnostic boundary
        ↓
Lazy matching + lookahead
        ↓
Extract structured result
```

The key concept is:

> When values are dynamic, identify the **structural boundaries** instead of hard-coding every possible value.

---

# Level 9 — Structured Storage Validation Records

## Objective

Now the storage validation output contains several fields.

Instead of returning tuples with numbered groups, we want structured dictionaries.

---

## Storage Test Output

```text
Drive=/dev/nvme0n1 Type=SSD Capacity=1TB Status=PASS Firmware=5B2QGXA7
Drive=/dev/sda Type=HDD Capacity=500GB Status=FAIL Firmware=FW1234
Drive=/dev/sdb Type=SSD Capacity=2TB Status=PASS Firmware=3B2QGXA7
Drive=/dev/nvme1n1 Type=SSD Capacity=4TB Status=FAIL Firmware=7B2QGXA7
```

---

## Requirement

Extract every complete record into:

```python
{
    "drive": "...",
    "type": "...",
    "capacity": "...",
    "status": "...",
    "firmware": "..."
}
```

Expected:

```python
[
    {
        "drive": "/dev/nvme0n1",
        "type": "SSD",
        "capacity": "1TB",
        "status": "PASS",
        "firmware": "5B2QGXA7"
    },
    {
        "drive": "/dev/sda",
        "type": "HDD",
        "capacity": "500GB",
        "status": "FAIL",
        "firmware": "FW1234"
    },
    {
        "drive": "/dev/sdb",
        "type": "SSD",
        "capacity": "2TB",
        "status": "PASS",
        "firmware": "3B2QGXA7"
    },
    {
        "drive": "/dev/nvme1n1",
        "type": "SSD",
        "capacity": "4TB",
        "status": "FAIL",
        "firmware": "7B2QGXA7"
    }
]
```

---

# Level 9 — Thought Process

## Step 1 — Multiple Records

There are multiple records.

Therefore we need:

```python
re.finditer()
```

because we want each record as a Match object.

---

## Step 2 — Named Groups

There are five fields:

```text
drive
type
capacity
status
firmware
```

Using numbered groups would require remembering:

```text
group(1)
group(2)
group(3)
group(4)
group(5)
```

That becomes harder to maintain.

Therefore we use named groups:

```regex
(?P<drive>...)
(?P<type>...)
(?P<capacity>...)
(?P<status>...)
(?P<firmware>...)
```

---

## Step 3 — Drive

```regex
(?P<drive>/dev/\w+)
```

---

## Step 4 — Type

```regex
(?P<type>\w+)
```

This captures:

```text
SSD
HDD
```

---

## Step 5 — Capacity

The capacity format is:

```text
1TB
500GB
2TB
4TB
```

Therefore:

```regex
(?P<capacity>\d+(?:TB|GB|MB))
```

The unit alternatives are non-capturing because we don't need them separately.

---

## Step 6 — Status

```regex
(?P<status>\w+)
```

captures:

```text
PASS
FAIL
```

---

## Step 7 — Firmware

Firmware values contain letters and digits:

```text
5B2QGXA7
FW1234
3B2QGXA7
7B2QGXA7
```

Therefore:

```regex
(?P<firmware>\w+)
```

---

## Step 8 — Complete Pattern

```regex
Drive=(?P<drive>/dev/\w+)\s+Type=(?P<type>\w+)\s+Capacity=(?P<capacity>\d+(?:TB|GB|MB))\s+Status=(?P<status>\w+)\s+Firmware=(?P<firmware>\w+)
```

---

# Complete Solution

```python
import re

text = """Drive=/dev/nvme0n1 Type=SSD Capacity=1TB Status=PASS Firmware=5B2QGXA7
Drive=/dev/sda Type=HDD Capacity=500GB Status=FAIL Firmware=FW1234
Drive=/dev/sdb Type=SSD Capacity=2TB Status=PASS Firmware=3B2QGXA7
Drive=/dev/nvme1n1 Type=SSD Capacity=4TB Status=FAIL Firmware=7B2QGXA7
"""

pattern = (
    r"Drive=(?P<drive>/dev/\w+)"
    r"\s+Type=(?P<type>\w+)"
    r"\s+Capacity=(?P<capacity>\d+(?:TB|GB|MB))"
    r"\s+Status=(?P<status>\w+)"
    r"\s+Firmware=(?P<firmware>\w+)"
)

result = []

matches = re.finditer(pattern, text)

for match in matches:
    result.append(match.groupdict())

print(result)
```

## Output

```python
[
    {
        'drive': '/dev/nvme0n1',
        'type': 'SSD',
        'capacity': '1TB',
        'status': 'PASS',
        'firmware': '5B2QGXA7'
    },
    {
        'drive': '/dev/sda',
        'type': 'HDD',
        'capacity': '500GB',
        'status': 'FAIL',
        'firmware': 'FW1234'
    },
    {
        'drive': '/dev/sdb',
        'type': 'SSD',
        'capacity': '2TB',
        'status': 'PASS',
        'firmware': '3B2QGXA7'
    },
    {
        'drive': '/dev/nvme1n1',
        'type': 'SSD',
        'capacity': '4TB',
        'status': 'FAIL',
        'firmware': '7B2QGXA7'
    }
]
```

---

## Why `finditer()` + `groupdict()`?

The requirement is:

```text
Multiple records
+
Multiple named fields
+
Structured dictionaries
```

Therefore:

```text
finditer()
    ↓
Match object for each record
    ↓
groupdict()
    ↓
Dictionary for each record
    ↓
Append to list
```

---

## Level 9 Engineering Lesson

As the number of extracted fields increases, named groups become increasingly useful.

Compare:

```python
match.group(1)
match.group(2)
match.group(3)
match.group(4)
match.group(5)
```

with:

```python
match.group("drive")
match.group("type")
match.group("capacity")
match.group("status")
match.group("firmware")
```

The second approach is much clearer and easier to maintain.

---

# Level 10 — Enterprise Storage Log Analysis

## Objective

This is the final integrated scenario.

The output combines:

```text
Timestamp
Drive
Type
Capacity
Status
Diagnostic information
```

We need to identify only failed records and extract all relevant information.

---

## Storage Test Output

```text
2026-08-10 11:20:01 Drive=/dev/sda Type=HDD Capacity=500GB Status=PASS
2026-08-10 11:20:02 Drive=/dev/sdb Type=HDD Capacity=500GB Status=READ ERROR - sector 182736
2026-08-10 11:20:03 Drive=/dev/nvme0n1 Type=SSD Capacity=1TB Status=PASS
2026-08-10 11:20:04 Drive=/dev/nvme1n1 Type=SSD Capacity=2TB Status=I/O ERROR - timeout after 30s
2026-08-10 11:20:05 Drive=/dev/sdc Type=HDD Capacity=1TB Status=PASS
```

---

## Requirement

Extract only failed drives.

For every failed record, extract:

```text
Timestamp
Drive
Type
Capacity
Status
Diagnostic
```

Expected:

```python
[
    {
        "timestamp": "2026-08-10 11:20:02",
        "drive": "/dev/sdb",
        "type": "HDD",
        "capacity": "500GB",
        "status": "READ ERROR",
        "diagnostic": "sector 182736"
    },
    {
        "timestamp": "2026-08-10 11:20:04",
        "drive": "/dev/nvme1n1",
        "type": "SSD",
        "capacity": "2TB",
        "status": "I/O ERROR",
        "diagnostic": "timeout after 30s"
    }
]
```

---

# Level 10 — Thought Process

This is the most important level because we now need to combine everything learned.

---

## Step 1 — Identify the Record Structure

A record looks like:

```text
TIMESTAMP Drive=DEVICE Type=TYPE Capacity=CAPACITY Status=STATUS
```

For failed records, it becomes:

```text
TIMESTAMP Drive=DEVICE Type=TYPE Capacity=CAPACITY Status=STATUS - DIAGNOSTIC
```

Therefore the structure is:

```text
timestamp
    ↓
drive
    ↓
type
    ↓
capacity
    ↓
status
    ↓
diagnostic
```

---

# Step 2 — Timestamp

The timestamp is:

```text
2026-08-10 11:20:02
```

The structure is:

```text
YYYY-MM-DD HH:MM:SS
```

A precise regex is:

```regex
(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})
```

---

# Step 3 — Drive

We already know:

```regex
(?P<drive>/dev/\w+)
```

---

# Step 4 — Type

```regex
(?P<type>\w+)
```

---

# Step 5 — Capacity

```regex
(?P<capacity>\d+(?:TB|GB|MB))
```

---

# Step 6 — Status

The status is dynamic.

It can be:

```text
READ ERROR
I/O ERROR
MEDIA ERROR
COMMAND ABORTED
```

We should not hard-code all possible status values.

Instead, we know the structural boundary:

```text
 -
```

Therefore:

```regex
(?P<status>.+?)(?= -)
```

means:

> Capture the status lazily until ` -` is found.

---

# Step 7 — Diagnostic

After:

```text
 -
```

everything remaining on the line is diagnostic information.

Therefore:

```regex
(?P<diagnostic>.+)
```

captures the diagnostic.

---

# Step 8 — How Do We Select Only Failed Records?

This is critical.

Successful records have:

```text
Status=PASS
```

and do not contain:

```text
 - diagnostic
```

Failed records have:

```text
Status=... - diagnostic
```

Therefore the pattern itself can require:

```text
 -
```

after the status.

This naturally excludes successful records.

We don't need to separately search for `PASS`.

---

# Step 9 — Complete Pattern

The complete pattern is:

```regex
(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+
Drive=(?P<drive>/dev/\w+)\s+
Type=(?P<type>\w+)\s+
Capacity=(?P<capacity>\d+(?:TB|GB|MB))\s+
Status=(?P<status>.+?)(?= -)\s-\s
(?P<diagnostic>.+)
```

---

# Step 10 — API Selection

We need:

```text
All failed records
+
Match objects
+
Named groups
```

Therefore:

```python
re.finditer()
```

is the natural choice.

Then:

```python
match.groupdict()
```

converts every match into a dictionary.

---

# Complete Solution

```python
import re

text = """2026-08-10 11:20:01 Drive=/dev/sda Type=HDD Capacity=500GB Status=PASS
2026-08-10 11:20:02 Drive=/dev/sdb Type=HDD Capacity=500GB Status=READ ERROR - sector 182736
2026-08-10 11:20:03 Drive=/dev/nvme0n1 Type=SSD Capacity=1TB Status=PASS
2026-08-10 11:20:04 Drive=/dev/nvme1n1 Type=SSD Capacity=2TB Status=I/O ERROR - timeout after 30s
2026-08-10 11:20:05 Drive=/dev/sdc Type=HDD Capacity=1TB Status=PASS
"""

pattern = (
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+"
    r"Drive=(?P<drive>/dev/\w+)\s+"
    r"Type=(?P<type>\w+)\s+"
    r"Capacity=(?P<capacity>\d+(?:TB|GB|MB))\s+"
    r"Status=(?P<status>.+?)(?= -)\s-\s"
    r"(?P<diagnostic>.+)"
)

result = []

matches = re.finditer(pattern, text)

for match in matches:
    result.append(match.groupdict())

print(result)
```

---

## Output

```python
[
    {
        'timestamp': '2026-08-10 11:20:02',
        'drive': '/dev/sdb',
        'type': 'HDD',
        'capacity': '500GB',
        'status': 'READ ERROR',
        'diagnostic': 'sector 182736'
    },
    {
        'timestamp': '2026-08-10 11:20:04',
        'drive': '/dev/nvme1n1',
        'type': 'SSD',
        'capacity': '2TB',
        'status': 'I/O ERROR',
        'diagnostic': 'timeout after 30s'
    }
]
```

---

# Why PASS Records Are Excluded

Consider:

```text
2026-08-10 11:20:01 Drive=/dev/sda Type=HDD Capacity=500GB Status=PASS
```

Our pattern eventually requires:

```regex
\s-\s
```

after the status.

But the PASS record ends at:

```text
PASS
```

There is no:

```text
 -
```

Therefore the entire pattern fails for that record.

This naturally filters the successful drives.

---

# Level 10 — Complete Engineering Reasoning

The final pattern was not created randomly.

It was derived field by field:

```text
Enterprise Storage Record
        ↓
Timestamp
        ↓
Drive
        ↓
Type
        ↓
Capacity
        ↓
Status
        ↓
Diagnostic
```

Then each field was assigned a matching strategy:

```text
Timestamp
    ↓
\d{4}-\d{2}-\d{2} ...

Drive
    ↓
/dev/\w+

Type
    ↓
\w+

Capacity
    ↓
\d+(?:TB|GB|MB)

Status
    ↓
.+?(?= -)

Diagnostic
    ↓
.+
```

Then the API was selected:

```text
Multiple records
        ↓
finditer()
        ↓
Named groups
        ↓
groupdict()
        ↓
List of dictionaries
```

---

# Level 10 — Concepts Combined

Level 10 combines the concepts learned throughout the progression:

```text
API Selection
        +
Named Capturing Groups
        +
Non-Capturing Groups
        +
finditer()
        +
groupdict()
        +
Lazy Matching
        +
Positive Lookahead
        +
Field Boundaries
        +
Dynamic Status Matching
        +
Structured Output
```

---

# 33. Complete Pattern-Matching Progression

The complete progression is:

```text
Level 1
    Find all failed devices
        ↓
    re.findall()
    Positive lookahead
        ✅

Level 2
    Match any error type
        ↓
    Structural matching
    Positive lookahead
        ✅

Level 3
    Extract device + error
        ↓
    Multiple capturing groups
        ✅

Level 4
    Extract complete error line
        ↓
    ^ $
    re.M
    re.search()
        ✅

Level 5
    Dynamic status + diagnostic boundary
        ↓
    Lazy matching
    Positive lookahead
        ✅

Level 6
    Structured storage records
        ↓
    Named groups
    finditer()
    groupdict()
    Non-capturing groups
        ✅

Level 7
    All multiline error lines
        ↓
    re.M
    findall()
    Complete line extraction
        ✅

Level 8
    Device + status + diagnostic
        ↓
    Three capturing groups
    Lazy matching
    Lookahead
        ✅

Level 9
    Structured validation records
        ↓
    Multiple named fields
    finditer()
    groupdict()
        ✅

Level 10
    Enterprise storage log analysis
        ↓
    Complete integrated regex design
        ↓
    Named groups
    Lookahead
    Lazy matching
    Structured extraction
        ✅
```

---

# 34. Final Engineering Skill

The objective of these ten levels is not:

> Memorize ten regex patterns.

The objective is:

> **Given a Storage Testing requirement, derive the regex and API from the structure of the problem.**

The mental process should become:

```text
Requirement
    ↓
What exactly do I need?
    ↓
First or all?
    ↓
What defines one record?
    ↓
What fields must be captured?
    ↓
What fields only need to be verified?
    ↓
Where does each field end?
    ↓
What are the structural boundaries?
    ↓
Do I need capturing groups?
    ↓
Do I need named groups?
    ↓
Do I need lookarounds?
    ↓
Do I need lazy matching?
    ↓
Do I need flags?
    ↓
Which API gives the required result?
    ↓
Implement
    ↓
Test
    ↓
Validate against the requirement
```

---

# 35. Final Storage Testing Application

These techniques can now be applied to real storage automation tasks such as:

```text
Storage Validation
        ↓
Device Discovery
        ↓
Device Identification
        ↓
Capacity Validation
        ↓
Firmware Validation
        ↓
SMART Output Parsing
        ↓
dmesg Error Parsing
        ↓
I/O Error Detection
        ↓
fio Output Parsing
        ↓
NVMe Validation
        ↓
SATA/SAS Validation
        ↓
RAID Validation
        ↓
Failure Classification
        ↓
Automated Test Result Extraction
```

The final goal is to transform unstructured or semi-structured storage-test output into reliable structured data that automation can consume.


