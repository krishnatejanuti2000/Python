# 14 — Regex Interview Questions

## Objective

This module prepares the engineer to answer Regex questions in:

- Python interviews
- QA Automation interviews
- Storage Test Engineering interviews
- Storage Automation interviews
- Linux Automation interviews
- Log Parsing interviews
- Troubleshooting interviews

The focus is not memorizing Regex syntax.

The focus is:

```text
Understand the requirement
        ↓
Identify the pattern
        ↓
Choose the correct Regex construct
        ↓
Write the pattern
        ↓
Explain why it works
        ↓
Handle edge cases
        ↓
Integrate with Python
```

---

# Interview Level Structure

| Level    | Focus                           | Difficulty |
| -------- | ------------------------------- | ---------- |
| Level 1  | Regex Fundamentals              | 🟢         |
| Level 2  | Character Classes & Quantifiers | 🟢         |
| Level 3  | Groups & Capturing              | 🟡         |
| Level 4  | Lookarounds                     | 🟡         |
| Level 5  | Python `re` Module              | 🟠         |
| Level 6  | Greedy / Lazy / Backtracking    | 🟠         |
| Level 7  | Validation                      | 🟠         |
| Level 8  | Log Parsing                     | 🔴         |
| Level 9  | Storage Testing Scenarios       | 🔴         |
| Level 10 | Advanced Troubleshooting        | 🔴🔥       |

---

# Level 1 — Regex Fundamentals

---

## Q1. What is Regex?

### Answer

Regex, or Regular Expression, is a pattern-matching mechanism used to:

* Search text
* Extract information
* Validate input
* Replace text
* Parse logs

Example:

```python
import re

text = "Drive=/dev/sda"

pattern = r"/dev/\w+"

result = re.findall(pattern, text)

print(result)
```

Output:

```text
['/dev/sda']
```

### Key Interview Point

Regex describes a **pattern**, not a specific piece of text.

---

# Q2. What is the difference between literal text and Regex?

### Answer

Literal:

```regex
ERROR
```

matches exactly:

```text
ERROR
```

Regex:

```regex
ERROR\d+
```

matches:

```text
ERROR123
ERROR456
```

because:

```regex
\d+
```

means:

```text
one or more digits
```

---

# Q3. What does `\d` mean?

### Answer

`\d` matches a digit.

Equivalent conceptual form:

```regex
[0-9]
```

Example:

```python
re.findall(r"\d+", "sector=182736")
```

Output:

```python
['182736']
```

---

# Q4. What does `\w` mean?

### Answer

`\w` matches a word character.

Commonly:

```text
a-z
A-Z
0-9
_
```

Example:

```python
re.findall(r"\w+", "Drive=sda_01")
```

Output:

```python
['Drive', 'sda_01']
```

---

# Q5. What does `\s` mean?

### Answer

`\s` matches whitespace.

Examples:

```text
space
tab
newline
```

Example:

```python
pattern = r"Drive=\s+/dev/\w+"
```

---

# Q6. Difference between `*`, `+`, and `?`

### Answer

### `*`

Zero or more.

```regex
a*
```

Matches:

```text
""
"a"
"aa"
"aaa"
```

### `+`

One or more.

```regex
a+
```

Matches:

```text
"a"
"aa"
"aaa"
```

but not:

```text
""
```

### `?`

Zero or one.

```regex
a?
```

Matches:

```text
""
"a"
```

---

# Level 2 — Character Classes & Quantifiers

---

# Q7. What is a character class?

### Answer

A character class specifies allowed characters.

Example:

```regex
[abc]
```

matches one of:

```text
a
b
c
```

Example:

```regex
[0-9]
```

matches a digit.

Example:

```regex
[a-z]
```

matches lowercase letters.

---

# Q8. Difference between `[0-9]` and `\d`?

### Answer

Both are commonly used to match digits.

```regex
[0-9]
```

explicitly describes ASCII digits.

```regex
\d
```

is the digit character class provided by Regex engines and, in Python, has Unicode-aware behavior by default.

For storage log parsing where ASCII digits are expected, `[0-9]` can sometimes make the intent clearer.

---

# Q9. Write a Regex to match a storage device.

### Requirement

Match:

```text
/dev/sda
/dev/sdb
/dev/sdc1
```

### Answer

A simple pattern:

```regex
/dev/sd[a-z]\d*
```

### Breakdown

```text
/dev/
   ↓
sd
   ↓
[a-z]
   ↓
\d*
```

Examples:

```text
/dev/sda
/dev/sdb
/dev/sdc1
/dev/sdc10
```

---

# Q10. Write a Regex for NVMe devices.

### Requirement

Match:

```text
/dev/nvme0n1
/dev/nvme1n1
/dev/nvme2n5
/dev/nvme0n1p1
/dev/nvme0n1p10
```

### Answer

```regex
/dev/nvme\d+n\d+(?:p\d+)?
```

### Breakdown

```text
/dev/
nvme
\d+
n
\d+
(?:p\d+)?
```

Partition is optional:

```regex
(?:p\d+)?
```

---

# Q11. What is the difference between `.` and `\.`?

### Answer

`.` means:

> Any character except newline by default.

Example:

```regex
a.b
```

can match:

```text
a1b
axb
a-b
```

But:

```regex
a\.b
```

matches the literal:

```text
a.b
```

### Interview Trap

If you want a literal dot, escape it:

```regex
\.
```

---

# Q12. How do you match one or more words?

### Answer

A simple pattern:

```regex
\w+
```

For:

```text
READ ERROR
```

you can use:

```regex
\w+(?:\s+\w+)*
```

This allows:

```text
READ
READ ERROR
WRITE I/O ERROR
```

depending on the exact requirements.

---

# Level 3 — Groups & Capturing

---

# Q13. What is a capturing group?

### Answer

A capturing group stores the part of the match that is enclosed in:

```regex
(...)
```

Example:

```python
import re

text = "Drive=/dev/sda"

pattern = r"Drive=(/dev/\w+)"

match = re.search(pattern, text)

print(match.group(1))
```

Output:

```text
/dev/sda
```

---

# Q14. What is a named capturing group?

### Answer

Instead of:

```regex
(...)
```

we can use:

```regex
(?P<name>...)
```

Example:

```python
pattern = r"Drive=(?P<drive>/dev/\w+)"
```

Then:

```python
match.group("drive")
```

returns:

```text
/dev/sda
```

---

# Q15. Why are named groups useful in automation?

### Answer

They make extracted information self-documenting.

Instead of:

```python
match.group(1)
match.group(2)
match.group(3)
```

we can use:

```python
match.group("drive")
match.group("type")
match.group("capacity")
```

This is much easier to maintain.

---

# Q16. What is a non-capturing group?

### Answer

A non-capturing group is:

```regex
(?:...)
```

It groups Regex components without creating a captured result.

Example:

```regex
\d+(?:GB|TB|MB)
```

This captures:

```text
500GB
2TB
512MB
```

without creating a separate group for:

```text
GB
TB
MB
```

---

# Q17. Capturing group vs non-capturing group?

### Answer

Capturing:

```regex
(...)
```

Use when you need the matched value.

Non-capturing:

```regex
(?:...)
```

Use when you only need grouping for Regex logic.

---

# Q18. What does `groupdict()` do?

### Answer

For named groups:

```python
import re

text = "Drive=/dev/sda Type=HDD"

pattern = (
    r"Drive=(?P<drive>/dev/\w+)\s+"
    r"Type=(?P<type>\w+)"
)

match = re.search(pattern, text)

print(match.groupdict())
```

Output:

```python
{
    'drive': '/dev/sda',
    'type': 'HDD'
}
```

This is extremely useful for log parsing.

---

# Level 4 — Lookarounds

---

# Q19. What is a lookahead?

### Answer

A lookahead checks what comes next without consuming it.

Syntax:

```regex
(?=...)
```

Example:

```python
pattern = r"/dev/\w+(?=:\sI/O\sERROR)"
```

Given:

```text
/dev/sda: PASS
/dev/sdb: I/O ERROR
```

the Regex extracts:

```text
/dev/sdb
```

The lookahead verifies:

```text
: I/O ERROR
```

but does not include it in the result.

---

# Q20. What is negative lookahead?

### Answer

Syntax:

```regex
(?!...)
```

It means:

> The following pattern must NOT exist here.

Example:

```regex
/dev/\w+(?!\d)
```

The exact usefulness depends on the position of the assertion.

---

# Q21. What is positive lookbehind?

### Answer

Syntax:

```regex
(?<=...)
```

It checks what appears immediately before the current position.

Example:

```python
text = "ERROR=READ"

pattern = r"(?<=ERROR=)\w+"

print(re.findall(pattern, text))
```

Output:

```text
['READ']
```

---

# Q22. What is negative lookbehind?

### Answer

Syntax:

```regex
(?<!...)
```

It verifies that the specified pattern does not occur immediately before the current position.

Example:

```regex
(?<!ERROR=)\w+
```

---

# Q23. When should you use lookarounds?

### Answer

Use lookarounds when:

```text
You need context
BUT
You don't want that context in the final match.
```

Example:

```regex
/dev/\w+(?=:.*ERROR)
```

This can extract only the device while using the error information as a condition.

---

# Q24. What is the difference between capturing and lookahead?

### Capturing

```regex
(?P<device>/dev/\w+)
```

means:

> Extract this value.

### Lookahead

```regex
(?=.*ERROR)
```

means:

> Verify that ERROR exists later.

Therefore:

```text
Capture → extract
Lookaround → assert
```

---

# Level 5 — Python `re` Module

---

# Q25. Difference between `re.search()` and `re.match()`?

### `re.search()`

Searches anywhere in the string.

```python
re.search(pattern, text)
```

### `re.match()`

Attempts to match from the beginning of the string.

```python
re.match(pattern, text)
```

---

# Q26. Difference between `match()` and `fullmatch()`?

### `match()`

Matches from the beginning but does not necessarily require the entire string.

### `fullmatch()`

Requires the entire string to conform to the pattern.

Example:

```python
pattern = r"/dev/\w+"

re.match(pattern, "/dev/sda EXTRA")
```

can match the beginning.

But:

```python
re.fullmatch(pattern, "/dev/sda EXTRA")
```

fails.

### Interview Rule

For validation, `fullmatch()` is often the clearest choice.

---

# Q27. Difference between `findall()` and `finditer()`?

### `findall()`

Returns matching values.

```python
re.findall(pattern, text)
```

### `finditer()`

Returns Match objects.

```python
re.finditer(pattern, text)
```

Use `finditer()` when you need:

```python
match.group()
match.groupdict()
match.start()
match.end()
```

---

# Q28. When would you prefer `finditer()` for Storage Logs?

### Answer

When extracting multiple structured records.

Example:

```python
for match in re.finditer(pattern, log):
    data = match.groupdict()
    print(data)
```

This is particularly useful for:

```text
Timestamp
Severity
Device
Operation
Error
Diagnostic
```

---

# Q29. What does `re.sub()` do?

### Answer

It replaces matching text.

Example:

```python
text = "USER=krishna /dev/sda"

result = re.sub(r"USER=\S+", "", text)

print(result)
```

Output:

```text
 /dev/sda
```

---

# Q30. What are Regex flags?

### Answer

Flags modify Regex behavior.

Common Python flags:

```python
re.I
re.M
re.S
re.X
```

### `re.I`

Case-insensitive.

### `re.M`

Multiline mode.

### `re.S`

Dot matches newline.

### `re.X`

Verbose mode.

---

# Q31. Why is `re.M` useful for logs?

Suppose:

```text
line1
line2
line3
```

Pattern:

```regex
^ERROR.*$
```

With:

```python
re.M
```

`^` and `$` operate per line.

Example:

```python
re.findall(r"^.*ERROR.*$", text, re.M)
```

This can extract every error line.

---

# Level 6 — Greedy, Lazy & Backtracking

---

# Q32. What does greedy matching mean?

### Answer

Regex quantifiers are greedy by default.

Example:

```regex
.*
```

tries to consume as much as possible while still allowing the rest of the pattern to succeed.

---

# Q33. What is lazy matching?

### Answer

Lazy quantifiers try to consume as little as possible.

Example:

```regex
.*?
```

Instead of:

```regex
.*
```

Example:

```text
Status=READ ERROR - sector=182736
```

A lazy match can help separate:

```text
READ ERROR
```

from:

```text
sector=182736
```

---

# Q34. Why can `.*` be dangerous in log parsing?

### Answer

Because it can consume too much.

Example:

```regex
Status=(.*) - (.*)
```

can behave unexpectedly when multiple separators exist.

A better pattern often uses:

```regex
.*?
```

with a meaningful boundary.

---

# Q35. What is backtracking?

### Answer

Backtracking occurs when Regex tries one possible path, fails to complete the pattern, and goes back to try another path.

Conceptually:

```text
Try match
   ↓
Failure
   ↓
Go backward
   ↓
Try another possibility
```

This is one reason poorly designed Regex can become expensive.

---

# Q36. How do you reduce unnecessary backtracking?

### Answer

Prefer specific patterns over unlimited wildcards.

Instead of:

```regex
.*
```

consider:

```regex
[^,]+
```

when the boundary is a comma.

Or:

```regex
\d+
```

when the field is numeric.

### Engineering Principle

Use the structure of the data.

Do not use:

```regex
.*
```

everywhere.

---

# Level 7 — Validation

---

# Q37. How would you validate a storage device name?

### Answer

For SATA/SCSI-style devices:

```regex
^/dev/sd[a-z]\d*$
```

For NVMe:

```regex
^/dev/nvme\d+n\d+(?:p\d+)?$
```

Combined:

```regex
^/(?:dev/sd[a-z]\d*|dev/nvme\d+n\d+(?:p\d+)?)$
```

A Python implementation:

```python
pattern = (
    r"^/dev/(?:sd[a-z]\d*|nvme\d+n\d+(?:p\d+)?)$"
)

def validate_device(device):
    return bool(re.fullmatch(pattern, device))
```

---

# Q38. How would you validate a storage capacity?

### Requirement

Accept:

```text
500MB
1GB
500GB
2TB
```

### Answer

```regex
^\d+(?:MB|GB|TB)$
```

---

# Q39. How would you validate a test result?

### Requirement

Accept:

```text
PASS
FAIL
```

### Answer

```regex
^(?:PASS|FAIL)$
```

Python:

```python
def validate_status(status):
    return bool(re.fullmatch(r"(?:PASS|FAIL)", status))
```

---

# Q40. Why are anchors important in validation?

Without anchors:

```regex
PASS
```

can match:

```text
TEST_PASS_EXTRA
```

With:

```regex
^PASS$
```

only:

```text
PASS
```

is accepted.

---

# Level 8 — Log Parsing

---

# Q41. Parse this storage log line.

Input:

```text
2026-08-11 09:10:04 [ERROR] /dev/sda READ ERROR sector=182736
```

Extract:

```text
Timestamp
Severity
Device
Operation
Error
Diagnostic
```

### Answer

```python
pattern = (
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})"
    r"\s+\[(?P<severity>\w+)\]\s+"
    r"(?P<device>/dev/\w+)\s+"
    r"(?P<operation>\w+)\s+"
    r"(?P<error>.+?ERROR)"
    r"\s+"
    r"(?P<diagnostic>.+)"
)
```

---

# Q42. Extract only failed devices.

Input:

```text
/dev/sda: PASS
/dev/sdb: READ ERROR
/dev/nvme0n1: PASS
/dev/nvme1n1: I/O ERROR
```

### Answer

```python
pattern = r"/dev/\w+(?=:\s.*ERROR)"
```

Result:

```python
[
    "/dev/sdb",
    "/dev/nvme1n1"
]
```

---

# Q43. Extract the entire error line.

### Answer

```python
pattern = r"^.*ERROR.*$"

result = re.findall(pattern, text, re.M)
```

This returns every line containing:

```text
ERROR
```

---

# Q44. Why is this pattern wrong?

```regex
^/dev/\w+(?=.*ERROR.*)$
```

for a log line such as:

```text
2026-08-11 09:10:04 [ERROR] /dev/sda READ ERROR
```

### Answer

Because the line does not start with:

```text
/dev/
```

It starts with:

```text
2026-08-11
```

Correct approach:

```regex
/dev/\w+(?=.*ERROR.*$)
```

with multiline mode if processing multiple lines.

---

# Q45. Extract device and error using named groups.

Input:

```text
/dev/sdb: READ ERROR
```

### Answer

```python
pattern = (
    r"(?P<device>/dev/\w+):\s+"
    r"(?P<error>.+ERROR)"
)
```

Output:

```python
{
    "device": "/dev/sdb",
    "error": "READ ERROR"
}
```

---

# Level 9 — Storage Testing Scenarios

---

# Q46. How would you extract all failed storage operations from a log?

### Answer

First identify the stable structure.

Example:

```text
2026-08-12 10:00:01 [ERROR] /dev/sda READ ERROR sector=100
```

Then:

```python
pattern = (
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})"
    r"\s+\[ERROR\]\s+"
    r"(?P<device>/dev/\w+)\s+"
    r"(?P<operation>\w+)\s+"
    r"(?P<error>.+?ERROR)\s+"
    r"(?P<diagnostic>.+)"
)
```

Then:

```python
for match in re.finditer(pattern, text):
    print(match.groupdict())
```

---

# Q47. How would you find drives with I/O errors only?

### Answer

```python
pattern = r"/dev/\w+(?=:\sI/O ERROR)"
```

For a log where the device and status are separated by arbitrary content:

```python
pattern = r"/dev/\w+(?=.*\bI/O ERROR\b)"
```

The exact pattern depends on the log structure.

### Engineering Principle

Do not use the same Regex blindly for different log formats.

---

# Q48. How would you count errors per device?

### Answer

Regex extracts the device.

Python performs counting.

```python
import re

pattern = r"(?P<device>/dev/\w+).*ERROR"

error_count = {}

for match in re.finditer(pattern, text):
    device = match.group("device")

    error_count[device] = error_count.get(device, 0) + 1

print(error_count)
```

Example:

```python
{
    "/dev/sda": 2,
    "/dev/sdb": 1
}
```

---

# Q49. How would you identify a device that started testing but never completed?

### Answer

This is not purely a Regex problem.

Regex can extract:

```text
TEST_START
TEST_END
```

Python should track state.

Conceptually:

```python
devices = {}

for event in events:

    if event == "TEST_START":
        devices[device]["started"] = True

    elif event == "TEST_END":
        devices[device]["completed"] = True
```

Then:

```python
if started and not completed:
    print("Incomplete test")
```

### Interview Point

Do not force Regex to solve state management.

---

# Q50. How would you find drives with errors and retries?

### Answer

Extract both events.

Error:

```regex
(?P<device>/dev/\w+).*ERROR
```

Retry:

```regex
(?P<device>/dev/\w+).*RETRY
```

Then correlate them in Python.

```text
Regex → extraction
Python → correlation
```

---

# Q51. How would you extract a diagnostic field?

Input:

```text
/dev/sda READ ERROR sector=182736 retry=3
```

### Answer

```regex
(?P<diagnostic>sector=\d+\s+retry=\d+)
```

More generally:

```regex
(?P<diagnostic>.+)
```

if the diagnostic field extends to the end of the line.

---

# Q52. How would you parse this?

```text
Drive=/dev/sda Type=HDD Capacity=500GB Status=PASS
```

### Answer

```python
pattern = (
    r"Drive=(?P<drive>/dev/\w+)\s+"
    r"Type=(?P<type>\w+)\s+"
    r"Capacity=(?P<capacity>\d+(?:TB|GB|MB))\s+"
    r"Status=(?P<status>\w+)"
)
```

Output:

```python
{
    "drive": "/dev/sda",
    "type": "HDD",
    "capacity": "500GB",
    "status": "PASS"
}
```

---

# Level 10 — Advanced Troubleshooting

---

# Q53. Your Regex works for one log line but fails for multiple lines. Why?

Possible reasons:

### Reason 1 — Missing multiline handling

You may need:

```python
re.M
```

especially when using:

```regex
^
$
```

### Reason 2 — Dot does not match newline

If you intentionally need `.` to cross newline boundaries:

```python
re.S
```

may be required.

### Reason 3 — Pattern was designed for one record

A Regex should normally be designed around the actual record structure.

---

# Q54. Your Regex returns too much text. What do you investigate?

Check:

```text
1. Greedy quantifiers
2. Lazy quantifiers
3. Missing boundaries
4. Missing anchors
5. Incorrect character classes
6. Incorrect lookarounds
```

Example:

```regex
Status=(.*)
```

may consume too much.

Try:

```regex
Status=(.*?)(?=\s+-\s+|$)
```

when `-` is the known boundary.

---

# Q55. Your Regex returns too little text. What do you investigate?

Check:

```text
1. Quantifiers
2. Character classes
3. Anchors
4. Lookarounds
5. Optional groups
6. Greedy/lazy behavior
```

Example:

```regex
/dev/sd[a-z]
```

will not match:

```text
/dev/sda1
```

because the partition number was not included.

Possible improvement:

```regex
/dev/sd[a-z]\d*
```

---

# Q56. How would you debug a complex Regex?

Use progressive construction.

Do NOT write the final pattern immediately.

Start:

```regex
/dev/
```

Then:

```regex
/dev/\w+
```

Then:

```regex
/dev/\w+\s+
```

Then:

```regex
/dev/\w+\s+(?P<operation>\w+)
```

Then continue.

Test after every step.

### Engineering Method

```text
Small pattern
    ↓
Test
    ↓
Expand
    ↓
Test
    ↓
Expand
    ↓
Final pattern
```

---

# Q57. How would you explain a complex Regex in an interview?

Do not read the Regex character by character without structure.

Instead divide it into logical components.

Example:

```regex
(?P<device>/dev/\w+)\s+
(?P<operation>\w+)\s+
(?P<error>.+?ERROR)
```

Explain:

```text
Part 1 → capture device
Part 2 → match whitespace
Part 3 → capture operation
Part 4 → capture error ending in ERROR
```

This demonstrates understanding.

---

# Q58. What is the biggest Regex mistake in production automation?

### Answer

Trying to solve everything with one huge Regex.

Bad design:

```text
One giant Regex
        ↓
Everything
        ↓
Impossible to maintain
```

Better:

```text
Regex
 ↓
Extract fields

Python
 ↓
Business logic

Python
 ↓
State

Python
 ↓
Reporting
```

---

# Q59. When should you NOT use Regex?

### Answer

Do not use Regex when:

* The format already has a reliable parser.
* The data is deeply nested.
* JSON should be parsed with `json`.
* CSV should be parsed with `csv`.
* YAML should be parsed with a YAML parser.
* Complex state logic is required.
* Regex makes the code significantly less maintainable.

Example:

Instead of:

```python
re.findall(...)
```

for JSON, use:

```python
import json

data = json.loads(text)
```

---

# Q60. What makes a Regex production-ready?

A production Regex should be:

```text
Correct
Readable
Tested
Maintainable
Specific enough
Not unnecessarily complicated
```

It should be tested against:

```text
Valid input
Invalid input
Empty input
Unexpected input
Boundary cases
Multiple records
```

---

# Storage Interview Scenario 1

## Question

You receive:

```text
/dev/sda: PASS
/dev/sdb: READ ERROR
/dev/nvme0n1: PASS
/dev/nvme1n1: I/O ERROR
```

The interviewer asks:

> Give me the devices that failed.

### Answer

```python
pattern = r"/dev/\w+(?=:\s.*ERROR)"

result = re.findall(pattern, text)

print(result)
```

Output:

```python
[
    "/dev/sdb",
    "/dev/nvme1n1"
]
```

### Why lookahead?

Because we want:

```text
/dev/sdb
```

but we don't want:

```text
: READ ERROR
```

in the match.

---

# Storage Interview Scenario 2

## Question

Extract:

```text
timestamp
severity
device
operation
error
diagnostic
```

from:

```text
2026-08-11 09:10:04 [ERROR] /dev/sda READ ERROR sector=182736
```

### Answer

```python
pattern = (
    r"(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})"
    r"\s+\[(?P<severity>\w+)\]\s+"
    r"(?P<device>/dev/\w+)\s+"
    r"(?P<operation>\w+)\s+"
    r"(?P<error>.+?ERROR)\s+"
    r"(?P<diagnostic>.+)"
)
```

---

# Storage Interview Scenario 3

## Question

Given:

```text
2026-08-11 09:10:04 [ERROR] /dev/sda READ ERROR sector=182736
2026-08-11 09:10:05 [ERROR] /dev/sdb WRITE ERROR timeout=30s
```

Extract only the device names from ERROR records.

### Answer

```python
pattern = r"\[ERROR\]\s+(?P<device>/dev/\w+)"
```

Then:

```python
for match in re.finditer(pattern, text):
    print(match.group("device"))
```

Output:

```text
/dev/sda
/dev/sdb
```

---

# Storage Interview Scenario 4

## Question

A device test log contains:

```text
/dev/sda TEST_START
/dev/sda READ PASS
/dev/sda READ ERROR
```

There is no:

```text
/dev/sda TEST_END
```

What should the automation report?

### Answer

```text
Started   : YES
Completed : NO
Status    : INCOMPLETE / FAIL
```

### Important

Regex alone should not determine this.

Use Regex to extract events:

```text
TEST_START
TEST_END
```

Then Python state tracking determines completion.

---

# Storage Interview Scenario 5

## Question

Why is this better?

```python
pattern = (
    r"Drive=(?P<drive>/dev/\w+)\s+"
    r"Type=(?P<type>\w+)\s+"
    r"Capacity=(?P<capacity>\d+(?:TB|GB|MB))"
)
```

than:

```python
pattern = r"Drive=(.*) Type=(.*) Capacity=(.*)"
```

### Answer

The first pattern is more specific.

It defines expected formats:

```text
Drive → /dev/...
Type → word
Capacity → number + unit
```

The second pattern accepts almost anything and can overmatch.

### Production principle

Prefer:

```text
Specific patterns
```

over:

```text
Unrestricted wildcards
```

when the input structure is known.

---

# Advanced Interview Question 61

## Question

You wrote:

```regex
/dev/\w+(?=.*ERROR)
```

Why might this be dangerous?

### Answer

The lookahead:

```regex
(?=.*ERROR)
```

can search farther than intended.

If the Regex is applied to a multi-line string without carefully controlling boundaries, an `ERROR` belonging to another record could potentially cause the current device to match.

A safer pattern should respect the record boundary.

For line-based logs:

```python
pattern = r"/dev/\w+(?=[^\n]*ERROR)"
```

This restricts the lookahead to the same line.

### Important Engineering Lesson

Always ask:

> "How far can my lookaround search?"

---

# Advanced Interview Question 62

## Question

What is better?

```regex
/dev/\w+(?=.*ERROR)
```

or:

```regex
/dev/\w+(?=[^\n]*ERROR)
```

### Answer

For line-based logs:

```regex
/dev/\w+(?=[^\n]*ERROR)
```

is safer because the lookahead cannot cross the newline.

This prevents unrelated records from affecting the match.

---

# Advanced Interview Question 63

## Question

How would you extract only ERROR records from a multi-line storage log?

### Answer

```python
pattern = r"^.*\[ERROR\].*$"

result = re.findall(pattern, text, re.M)
```

Or:

```python
for match in re.finditer(pattern, text, re.M):
    print(match.group())
```

---

# Advanced Interview Question 64

## Question

How would you extract only failed NVMe devices?

### Answer

```python
pattern = r"/dev/nvme\d+n\d+(?:p\d+)?(?=[^\n]*ERROR)"
```

This combines:

```text
NVMe device validation
+
same-line error assertion
```

---

# Advanced Interview Question 65

## Question

How would you extract failed SATA/SCSI devices only?

### Answer

```python
pattern = r"/dev/sd[a-z]\d*(?=[^\n]*ERROR)"
```

---

# Advanced Interview Question 66

## Question

How would you extract both SATA/SCSI and NVMe failed devices?

### Answer

```python
pattern = (
    r"/dev/(?:sd[a-z]\d*|nvme\d+n\d+(?:p\d+)?)"
    r"(?=[^\n]*ERROR)"
)
```

---

# Advanced Interview Question 67

## Question

What if the log contains:

```text
/dev/sda PASS
/dev/sdb READ ERROR
DEBUG ERROR
/dev/sdc PASS
```

and you use:

```regex
/dev/\w+(?=[^\n]*ERROR)
```

Will `DEBUG ERROR` cause `/dev/sdc` to match?

### Answer

No.

The lookahead:

```regex
[^\n]*
```

is restricted to the same line.

Therefore:

```text
/dev/sdc PASS
```

does not contain `ERROR` on its own line.

This is an important difference between:

```regex
.*
```

and:

```regex
[^\n]*
```

in line-oriented log parsing.

---

# Advanced Interview Question 68

## Question

How would you extract all `sector=` values from errors?

Input:

```text
/dev/sda READ ERROR sector=182736
/dev/sdb READ ERROR sector=918273
```

### Answer

```python
pattern = r"sector=(\d+)"

result = re.findall(pattern, text)

print(result)
```

Output:

```python
[
    "182736",
    "918273"
]
```

---

# Advanced Interview Question 69

## Question

How would you extract retry counts?

Input:

```text
/dev/sda READ ERROR sector=182736 retry=3
/dev/sdb WRITE ERROR timeout=30s retry=5
```

### Answer

```python
pattern = r"retry=(\d+)"

result = re.findall(pattern, text)
```

Output:

```python
[
    "3",
    "5"
]
```

---

# Advanced Interview Question 70

## Question

How would you determine the device with the highest error count?

### Answer

Regex should extract:

```text
device
error
```

Python should perform aggregation:

```python
error_count = {}

for match in re.finditer(pattern, text):

    device = match.group("device")

    error_count[device] = (
        error_count.get(device, 0) + 1
    )

max_device = max(
    error_count,
    key=error_count.get
)

print(max_device)
```

### Engineering Principle

Regex:

```text
Extraction
```

Python:

```text
Analysis
```

---

# Interview Troubleshooting Checklist

When a Regex does not work, check in this order:

```text
1. Is the input exactly what I think it is?
        ↓
2. Am I matching the correct starting point?
        ↓
3. Are my character classes correct?
        ↓
4. Are my quantifiers correct?
        ↓
5. Are my boundaries correct?
        ↓
6. Do I need a capturing group?
        ↓
7. Do I need a non-capturing group?
        ↓
8. Do I need a lookahead/lookbehind?
        ↓
9. Is greedy matching consuming too much?
        ↓
10. Do I need lazy matching?
        ↓
11. Do I need a Regex flag?
        ↓
12. Should Python logic handle this instead?
```

---

# Regex Interview Golden Rules

## Rule 1

Do not memorize patterns blindly.

Understand:

```text
What
Where
How many
Until where
Under what condition
```

---

## Rule 2

Use named groups for structured parsing.

Prefer:

```python
match.group("device")
```

over:

```python
match.group(1)
```

when the Regex is complex.

---

## Rule 3

Use lookarounds when you need context without consuming it.

```text
Lookahead  → check what follows
Lookbehind → check what precedes
```

---

## Rule 4

Use `fullmatch()` for strict validation when appropriate.

---

## Rule 5

Use `finditer()` when processing structured records.

---

## Rule 6

Use lazy matching when a known boundary exists later.

```regex
.*?
```

---

## Rule 7

Avoid unnecessary `.*`.

Prefer precise boundaries.

---

## Rule 8

Regex extracts.

Python analyzes.

---

## Rule 9

Always test negative cases.

A Regex is not finished merely because it matches the positive example.

---

## Rule 10

Production automation prioritizes:

```text
Correctness
+
Maintainability
+
Readability
+
Edge-case handling
```

over:

```text
Shortest Regex
```

---

# Final Interview Skill Matrix

| Skill                                  | Expected Level |
| -------------------------------------- | -------------- |
| Basic Regex syntax                     | Expert         |
| Character classes                      | Expert         |
| Quantifiers                            | Expert         |
| Groups                                 | Expert         |
| Named groups                           | Expert         |
| Lookahead                              | Expert         |
| Lookbehind                             | Strong         |
| Python `re`                            | Expert         |
| `search()` / `match()` / `fullmatch()` | Expert         |
| `findall()` / `finditer()`             | Expert         |
| `sub()`                                | Strong         |
| Flags                                  | Strong         |
| Greedy / Lazy                          | Strong         |
| Backtracking                           | Strong         |
| Validation                             | Expert         |
| Log Parsing                            | Expert         |
| Storage Log Parsing                    | Expert         |
| Error Extraction                       | Expert         |
| Failure Correlation                    | Strong         |
| Troubleshooting Regex                  | Expert         |
| Regex + Python Automation              | Expert         |

---

# Final Interview Standard

The expected answer in an interview should not simply be:

> "Here is the Regex."

Instead:

```text
1. Understand the input format
2. Identify fixed fields
3. Identify variable fields
4. Identify boundaries
5. Design the Regex
6. Explain every important component
7. Test positive cases
8. Test negative cases
9. Consider edge cases
10. Use Python for business logic
```

---

# Final Storage Engineering Mindset

For a Storage Test Engineer, Regex is primarily useful for:

```text
Storage Logs
     ↓
Device Identification
     ↓
Test Result Extraction
     ↓
Error Detection
     ↓
Diagnostic Extraction
     ↓
Retry Detection
     ↓
Failure Correlation
     ↓
Test Result Analysis
     ↓
Automation Report
```

The objective is therefore not:

> "Become a Regex syntax expert."

The objective is:

> "Use Regex as one component of reliable Storage Test Automation."

---

# Module Completion Criteria

`14_Regex_Interview_Questions.md` is complete when the engineer can:

```text
Explain Regex concepts
        ↓
Write patterns independently
        ↓
Explain patterns
        ↓
Debug incorrect patterns
        ↓
Handle edge cases
        ↓
Parse real storage logs
        ↓
Combine Regex with Python
        ↓
Answer Storage Automation interview questions
```

After completing this module:

```text
14_Regex_Interview_Questions.md
                ↓
             COMPLETE
```

Then proceed to:

```text
Regex_CheatSheet.md
```

After that:

```text
Regex_Quick_Revision.md
```

---

# Final Goal

The complete Regex learning path is:

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
Regex Cheat Sheet
        ↓
Regex Quick Revision
```

The final target is:

```text
RAW STORAGE DATA
        ↓
REGEX
        ↓
STRUCTURED DATA
        ↓
PYTHON LOGIC
        ↓
STORAGE TEST ANALYSIS
        ↓
AUTOMATION
```

