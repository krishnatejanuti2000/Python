# Regex Quick Revision

## Module 06 — Regular Expressions

This document is a fast revision guide for the complete Regex module.

Use it for:

- Daily revision
- Before coding practice
- Before Storage Automation work
- Before interviews
- Quick syntax recall
- Last-minute troubleshooting

---

# 1. Regex Fundamentals

Regex = pattern matching.

Used for:

```text
Search
Extract
Validate
Replace
Parse
````

Python:

```python
import re
```

Basic example:

```python
re.findall(r"/dev/\w+", text)
```

---

# 2. Character Classes

```regex
\d      digit
\D      non-digit

\w      word character
\W      non-word character

\s      whitespace
\S      non-whitespace

.       any character except newline
```

Custom classes:

```regex
[abc]       a, b or c
[a-z]       lowercase
[A-Z]       uppercase
[0-9]       digit
[^0-9]      anything except digit
```

---

# 3. Quantifiers

```regex
*       0 or more
+       1 or more
?       0 or 1

{n}     exactly n
{n,}    n or more
{n,m}   n to m
```

Examples:

```regex
\d+
\d{4}
[a-z]+
```

---

# 4. Anchors

```regex
^       beginning
$       end
```

Validation example:

```regex
^PASS$
```

For complete Python validation:

```python
re.fullmatch(pattern, text)
```

---

# 5. Groups

Capturing:

```regex
(...)
```

Named:

```regex
(?P<name>...)
```

Non-capturing:

```regex
(?:...)
```

Alternation:

```regex
|
```

Example:

```regex
(?:PASS|FAIL)
```

---

# 6. Named Groups

Example:

```python
pattern = (
    r"Drive=(?P<drive>/dev/\w+)\s+"
    r"Type=(?P<type>\w+)"
)
```

Access:

```python
match.group("drive")
match.group("type")
```

All groups:

```python
match.groupdict()
```

---

# 7. Lookarounds

## Positive Lookahead

```regex
(?=...)
```

Check what follows without consuming it.

Example:

```regex
/dev/\w+(?=:\sI/O\sERROR)
```

---

## Negative Lookahead

```regex
(?!...)
```

Check that something does NOT follow.

---

## Positive Lookbehind

```regex
(?<=...)
```

Check what precedes.

---

## Negative Lookbehind

```regex
(?<!...)
```

Check that something does NOT precede.

---

# 8. Lookaround Rule

Remember:

```text
Lookaround = Assertion
```

Use it when:

```text
I need context
BUT
I don't want that context in my match.
```

---

# 9. Greedy vs Lazy

Greedy:

```regex
.*
```

Consumes as much as possible.

Lazy:

```regex
.*?
```

Consumes as little as possible.

Use lazy matching when a reliable boundary exists.

---

# 10. Backtracking

Concept:

```text
Try
 ↓
Fail
 ↓
Go backward
 ↓
Try another possibility
```

Avoid unnecessary:

```regex
.*
```

Prefer specific patterns when possible.

Example:

```regex
[^,]+
```

when the field ends at a comma.

---

# 11. Python `re` Functions

## `search()`

Find first match anywhere.

```python
re.search(pattern, text)
```

---

## `match()`

Match from beginning.

```python
re.match(pattern, text)
```

---

## `fullmatch()`

Entire input must match.

```python
re.fullmatch(pattern, text)
```

Best choice for many validation tasks.

---

## `findall()`

Return all matches.

```python
re.findall(pattern, text)
```

---

## `finditer()`

Return Match objects.

```python
re.finditer(pattern, text)
```

Use when you need:

```python
group()
groupdict()
start()
end()
```

---

## `sub()`

Replace matches.

```python
re.sub(pattern, replacement, text)
```

---

## `split()`

Split using Regex.

```python
re.split(pattern, text)
```

---

# 12. Match Object

Important methods:

```python
match.group()
match.group(1)
match.group("name")
match.groupdict()
match.start()
match.end()
```

---

# 13. Regex Flags

```python
re.I
re.M
re.S
re.X
```

## `re.I`

Case-insensitive.

```text
error
ERROR
Error
```

all match.

---

## `re.M`

Multiline.

Makes:

```regex
^
$
```

work per line.

Useful for logs.

---

## `re.S`

DOTALL.

Makes:

```regex
.
```

match newline too.

---

## `re.X`

Verbose mode.

Useful for complex readable patterns.

---

# 14. Storage Device Patterns

## SATA/SCSI-style

```regex
/dev/sd[a-z]\d*
```

Examples:

```text
/dev/sda
/dev/sdb
/dev/sda1
/dev/sdb10
```

---

## NVMe

```regex
/dev/nvme\d+n\d+
```

Examples:

```text
/dev/nvme0n1
/dev/nvme1n1
```

---

## NVMe with partition

```regex
/dev/nvme\d+n\d+(?:p\d+)?
```

Examples:

```text
/dev/nvme0n1
/dev/nvme0n1p1
/dev/nvme0n1p10
```

---

## Combined

```regex
/dev/(?:sd[a-z]\d*|nvme\d+n\d+(?:p\d+)?)
```

---

# 15. Storage Capacity

Pattern:

```regex
\d+(?:MB|GB|TB)
```

Examples:

```text
500MB
500GB
1TB
4TB
```

Validation:

```regex
^\d+(?:MB|GB|TB)$
```

---

# 16. Storage Status

```regex
(?:PASS|FAIL)
```

Validation:

```regex
^(?:PASS|FAIL)$
```

---

# 17. Storage Severity

```regex
\[(?:INFO|WARN|ERROR)\]
```

Examples:

```text
[INFO]
[WARN]
[ERROR]
```

---

# 18. Storage Error Patterns

Basic:

```regex
ERROR
```

Read:

```regex
READ ERROR
```

Write:

```regex
WRITE ERROR
```

I/O:

```regex
I/O ERROR
```

Media:

```regex
MEDIA ERROR
```

---

# 19. Extract Failed Devices

Input:

```text
/dev/sda: PASS
/dev/sdb: READ ERROR
/dev/nvme0n1: PASS
/dev/nvme1n1: I/O ERROR
```

Pattern:

```regex
/dev/\w+(?=:\s.*ERROR)
```

For line-oriented logs, safer:

```regex
/dev/\w+(?=[^\n]*ERROR)
```

---

# 20. Extract Error Lines

```regex
^.*ERROR.*$
```

Python:

```python
errors = re.findall(
    r"^.*ERROR.*$",
    text,
    re.M
)
```

---

# 21. Extract Error Device

```regex
(?P<device>/dev/\w+).*ERROR
```

---

# 22. Retry

Input:

```text
retry=3
```

Pattern:

```regex
retry=(\d+)
```

Named:

```regex
retry=(?P<retry>\d+)
```

---

# 23. Sector

Input:

```text
sector=182736
```

Pattern:

```regex
sector=(\d+)
```

Named:

```regex
sector=(?P<sector>\d+)
```

---

# 24. Timeout

Input:

```text
timeout=30s
```

Pattern:

```regex
timeout=(\d+)s
```

---

# 25. Timestamp

Input:

```text
2026-08-11 09:10:04
```

Pattern:

```regex
\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}
```

Named:

```regex
(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})
```

---

# 26. Complete Storage Error Record

Input:

```text
2026-08-11 09:10:04 [ERROR] /dev/sda READ ERROR sector=182736
```

Pattern:

```regex
(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})
\s+
\[(?P<severity>\w+)\]
\s+
(?P<device>/dev/\w+)
\s+
(?P<operation>\w+)
\s+
(?P<error>.+?ERROR)
\s+
(?P<diagnostic>.+)
```

---

# 27. Inventory Record

Input:

```text
Drive=/dev/sda Type=HDD Capacity=500GB Status=PASS
```

Pattern:

```regex
Drive=(?P<drive>/dev/\w+)\s+
Type=(?P<type>\w+)\s+
Capacity=(?P<capacity>\d+(?:TB|GB|MB))\s+
Status=(?P<status>\w+)
```

---

# 28. Inventory Record With Diagnostic

Input:

```text
Drive=/dev/sdb Type=HDD Capacity=2TB Status=READ ERROR - sector=182736 retry=3
```

Pattern:

```regex
Drive=(?P<drive>/dev/\w+)\s+
Type=(?P<type>\w+)\s+
Capacity=(?P<capacity>\d+(?:TB|GB|MB))\s+
Status=(?P<status>.+?)
\s+-\s+
(?P<diagnostic>.+)
```

---

# 29. Validation Quick Reference

## Device

```regex
^/dev/(?:sd[a-z]\d*|nvme\d+n\d+(?:p\d+)?)$
```

## Capacity

```regex
^\d+(?:MB|GB|TB)$
```

## Status

```regex
^(?:PASS|FAIL)$
```

## Severity

```regex
^(?:INFO|WARN|ERROR)$
```

---

# 30. Validation With Python

```python
def validate_device(device):
    pattern = (
        r"/dev/"
        r"(?:sd[a-z]\d*|nvme\d+n\d+(?:p\d+)?)"
    )

    return bool(re.fullmatch(pattern, device))
```

---

# 31. Line-Based Log Parsing

Use:

```python
re.M
```

with:

```regex
^
$
```

Example:

```python
pattern = r"^.*ERROR.*$"

errors = re.findall(
    pattern,
    text,
    re.M
)
```

---

# 32. Same-Line Lookahead

Use:

```regex
/dev/\w+(?=[^\n]*ERROR)
```

Meaning:

```text
Find /dev/<device>
AND
ERROR must occur later on the SAME line.
```

This is safer than:

```regex
/dev/\w+(?=.*ERROR)
```

for multi-line logs.

---

# 33. `re.sub()` Quick Reference

Remove:

```text
USER=krishna
```

Pattern:

```regex
USER=\S+\s*
```

Remove:

```text
HOST=storage01
```

Pattern:

```regex
HOST=\S+\s*
```

Remove either:

```regex
(?:USER|HOST)=\S+\s*
```

Python:

```python
cleaned = re.sub(
    r"(?:USER|HOST)=\S+\s*",
    "",
    text
)
```

---

# 34. Regex Design Process

Always think:

```text
1. What do I need?
        ↓
2. What is fixed?
        ↓
3. What is variable?
        ↓
4. What is the boundary?
        ↓
5. What is optional?
        ↓
6. What should NOT be included?
```

Then build the Regex.

---

# 35. Debugging Process

If the Regex fails:

```text
1. Inspect exact input
2. Build the smallest pattern
3. Test
4. Add one component
5. Test again
6. Add groups
7. Add boundaries
8. Add lookaround if needed
9. Check flags
10. Test edge cases
```

Never jump directly to a huge Regex.

---

# 36. Common Mistakes

## Mistake

```regex
.*
```

everywhere.

### Problem

Can overmatch.

### Better

Use precise boundaries.

---

## Mistake

Using:

```regex
PASS
```

for strict validation.

### Better

```regex
^PASS$
```

or:

```python
re.fullmatch()
```

---

## Mistake

Using:

```regex
(...)
```

when you don't need the captured value.

### Better

```regex
(?:...)
```

---

## Mistake

Using broad:

```regex
/dev/\w+
```

for strict device validation.

### Better

Use a device-specific pattern.

---

## Mistake

Using:

```regex
.*
```

inside a multi-line lookahead without considering boundaries.

### Better

For line-oriented logs:

```regex
[^\n]*
```

---

# 37. Regex vs Python

## Regex should handle

```text
Pattern matching
Extraction
Validation
Replacement
```

## Python should handle

```text
Counting
Aggregation
State
Correlation
Business logic
Reporting
```

Remember:

```text
Regex extracts.
Python analyzes.
```

---

# 38. Storage Test Automation Flow

```text
RAW LOG
   ↓
Regex
   ↓
Timestamp
Severity
Device
Operation
Error
Diagnostic
   ↓
Python
   ↓
Error Count
Retry Count
Device Grouping
State Tracking
Failure Correlation
   ↓
PASS / FAIL / INCOMPLETE
   ↓
REPORT
```

---

# 39. Essential Python Template

```python
import re

pattern = re.compile(
    r"..."
)

result = []

for match in pattern.finditer(text):
    result.append(match.groupdict())

print(result)
```

---

# 40. Essential Storage Error Template

```python
pattern = re.compile(
    r"(?P<device>/dev/\w+)\s+"
    r"(?P<operation>\w+)\s+"
    r"(?P<error>.+?ERROR)\s+"
    r"(?P<diagnostic>.+)"
)

for match in pattern.finditer(text):
    print(match.groupdict())
```

---

# 41. Essential Validation Template

```python
pattern = (
    r"^/dev/"
    r"(?:sd[a-z]\d*|nvme\d+n\d+(?:p\d+)?)"
    r"$"
)

if re.fullmatch(pattern, device):
    print("Valid")
else:
    print("Invalid")
```

---

# 42. Essential Failure Extraction Template

```python
pattern = r"/dev/\w+(?=[^\n]*ERROR)"

failed_devices = re.findall(
    pattern,
    text
)
```

---

# 43. Interview Rapid Recall

```text
\d       → digit
\w       → word character
\s       → whitespace
.        → any character except newline

*        → 0 or more
+        → 1 or more
?        → 0 or 1

^        → beginning
$        → end

(...)    → capturing group
(?:...)  → non-capturing group
(?P<>)   → named group

(?=...)  → positive lookahead
(?!...)  → negative lookahead
(?<=...) → positive lookbehind
(?<!...) → negative lookbehind

.*       → greedy
.*?      → lazy

search()     → search first match
match()      → beginning
fullmatch()  → entire input
findall()    → all matches
finditer()   → Match objects
sub()        → replace
split()      → split

re.I      → ignore case
re.M      → multiline
re.S      → dot matches newline
re.X      → verbose
```

---

# 44. Storage Device Rapid Recall

```text
SATA/SCSI:
    /dev/sd[a-z]\d*

NVMe:
    /dev/nvme\d+n\d+(?:p\d+)?

Combined:
    /dev/(?:sd[a-z]\d*|nvme\d+n\d+(?:p\d+)?)

Capacity:
    \d+(?:MB|GB|TB)

Status:
    (?:PASS|FAIL)

Retry:
    retry=(\d+)

Sector:
    sector=(\d+)

Timeout:
    timeout=(\d+)s
```

---

# 45. Error Extraction Rapid Recall

```text
Any ERROR:
    ERROR

Error line:
    ^.*ERROR.*$

Failed device:
    /dev/\w+(?=[^\n]*ERROR)

Error device:
    (?P<device>/dev/\w+).*ERROR

I/O error device:
    /dev/\w+(?=[^\n]*I/O ERROR)
```

---

# 46. The Most Important Concept

Do not ask:

> "What Regex should I memorize?"

Ask:

> "What is the structure of this input?"

Then:

```text
Structure
   ↓
Pattern
   ↓
Boundary
   ↓
Regex
```

---

# 47. Production Regex Rules

```text
1. Prefer readable Regex.
2. Prefer specific patterns.
3. Avoid unnecessary .*.
4. Use named groups for structured data.
5. Use fullmatch() for validation.
6. Use finditer() for structured parsing.
7. Use lookarounds for assertions.
8. Use lazy matching when appropriate.
9. Respect record boundaries.
10. Let Python handle business logic.
11. Test negative cases.
12. Test edge cases.
```

---

# 48. Final Mental Model

```text
REGEX
│
├── Match
│
├── Extract
│
├── Validate
│
├── Replace
│
└── Parse
```

Python:

```text
PYTHON
│
├── Count
├── Group
├── Track State
├── Correlate
├── Analyze
└── Report
```

Together:

```text
REGEX + PYTHON
       ↓
STORAGE TEST AUTOMATION
```

---

# 49. Complete Module 06 Revision

```text
01 Regex Fundamentals
        ↓
02 Character Classes
        ↓
03 Quantifiers
        ↓
04 Groups & Capturing
        ↓
05 Lookarounds
        ↓
06 Python re Module
        ↓
07 Greedy / Lazy / Backtracking
        ↓
08 Advanced re.sub()
        ↓
09 Flags & Modifiers
        ↓
10 Pattern Matching
        ↓
11 Validation
        ↓
12 Log Parsing
        ↓
13 Regex Projects
        ↓
14 Regex Interview Questions
        ↓
Regex CheatSheet
        ↓
Regex Quick Revision
```

---

# 50. Final Skill Target

You should be able to look at:

```text
2026-08-11 09:10:04 [ERROR] /dev/sda READ ERROR sector=182736
```

and immediately reason:

```text
Timestamp  → fixed date/time structure
Severity   → [ERROR]
Device     → /dev/sda
Operation  → READ
Error      → READ ERROR
Diagnostic → sector=182736
```

Then design:

```regex
(?P<timestamp>...)
(?P<severity>...)
(?P<device>...)
(?P<operation>...)
(?P<error>...)
(?P<diagnostic>...)
```

Then use Python:

```python
match.groupdict()
```

to obtain structured data.

Then use Python logic to determine:

```text
PASS
FAIL
INCOMPLETE
ERROR COUNT
RETRY COUNT
FIRST ERROR
DEVICE STATUS
```

That is the final practical goal of this Regex module.

---

# Module 06 — Final Status

```text
01_Regex_Fundamentals.md        → COMPLETE
02_Character_Classes.md         → COMPLETE
03_Quantifiers.md               → COMPLETE
04_Groups_and_Capturing.md      → COMPLETE
05_Lookarounds.md               → COMPLETE
06_Python_re_Module.md          → COMPLETE
07_Greedy_Lazy_Backtracking.md  → COMPLETE
08_Advanced_re_sub.md           → COMPLETE
09_Flags_and_Modifiers.md       → COMPLETE
10_Pattern_Matching.md          → COMPLETE
11_Validation.md                → COMPLETE
12_Log_Parsing.md               → COMPLETE
13_Regex_Projects.md            → COMPLETE
14_Regex_Interview_Questions.md → COMPLETE
Regex_CheatSheet.md             → COMPLETE
Regex_Quick_Revision.md         → COMPLETE
```

# END

```
```

