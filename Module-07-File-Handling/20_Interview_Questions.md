# 20 — Interview Questions

````markdown id="j3k8qf"
# File Handling — Interview Questions

## 1. Introduction

File handling is a fundamental Python skill for Storage Test Automation.

Interviewers may evaluate whether you understand:

- File objects
- File modes
- Reading and writing
- Context managers
- `pathlib`
- Directory traversal
- File operations
- Large-file processing
- JSON
- CSV
- YAML
- File comparison
- Error handling
- Automation design
- Troubleshooting

The goal is not only to remember syntax.

You should be able to explain:

> **Why you chose a particular approach and what happens when something goes wrong.**

---

# 2. File Fundamentals

## Q1. What is file handling?

File handling is the process of creating, opening, reading, writing, modifying, and managing files using a program.

Python provides functions and modules for interacting with files and directories.

---

## Q2. What does `open()` do?

`open()` opens a file and returns a file object.

Example:

```python
file = open("results.txt", "r", encoding="utf-8")
````

The file object can then be used to read or write data.

---

## Q3. Why should you specify `encoding`?

It makes the expected text encoding explicit.

Example:

```python
open("results.txt", "r", encoding="utf-8")
```

This avoids relying on platform-dependent defaults and helps prevent encoding-related problems.

---

## Q4. What is the difference between text mode and binary mode?

Text mode:

```python
open("file.txt", "r")
```

works with text and returns strings.

Binary mode:

```python
open("file.bin", "rb")
```

works with raw bytes and returns bytes.

Typical examples:

```text
Text
→ logs
→ configuration
→ reports

Binary
→ disk images
→ binary artifacts
→ raw device data
```

---

# 3. File Modes

## Q5. What is the difference between `r`, `w`, and `a`?

### `r`

Read an existing file.

```python
open("file.txt", "r")
```

The file must normally already exist.

### `w`

Write to a file.

```python
open("file.txt", "w")
```

Creates the file if necessary and truncates an existing file.

### `a`

Append to a file.

```python
open("file.txt", "a")
```

Preserves existing contents and writes new data at the end.

---

## Q6. What is dangerous about using `w`?

`w` truncates an existing file.

Example:

```python
with open("report.txt", "w", encoding="utf-8") as file:
    file.write("New report")
```

Any previous contents are removed.

This is important when handling test results and logs.

---

## Q7. What is the difference between `w` and `a`?

```text
w
→ replace existing contents

a
→ preserve existing contents and add new data
```

---

## Q8. What does `x` mode do?

`x` creates a new file and fails if the file already exists.

Example:

```python
open("report.txt", "x", encoding="utf-8")
```

It is useful when accidental overwriting must be prevented.

---

# 4. Reading Files

## Q9. What is the difference between `read()`, `readline()`, and `readlines()`?

### `read()`

Reads the requested content, or the entire remaining file if no size is specified.

```python
data = file.read()
```

### `readline()`

Reads one line.

```python
line = file.readline()
```

### `readlines()`

Reads remaining lines into a list.

```python
lines = file.readlines()
```

---

## Q10. Which approach is preferred for large files?

Usually:

```python
with open("large.log", "r", encoding="utf-8") as file:
    for line in file:
        process(line)
```

This processes the file incrementally rather than loading the entire file into memory.

---

## Q11. Why is direct file iteration useful?

A file object is iterable.

Example:

```python
for line in file:
    process(line)
```

This is memory-efficient and natural for line-oriented processing.

It is particularly useful for large log files.

---

# 5. `tell()` and `seek()`

## Q12. What does `tell()` do?

`tell()` returns the current file position.

Example:

```python
position = file.tell()
```

---

## Q13. What does `seek()` do?

`seek()` changes the current file position.

Example:

```python
file.seek(0)
```

moves the position to the beginning.

---

## Q14. Is `tell()` the same as file size?

No.

`tell()` reports the current position in the stream.

It does not inherently mean:

> "This is the size of the file."

---

# 6. Writing Files

## Q15. What does `write()` return?

In text mode, `write()` returns the number of characters written.

Example:

```python
count = file.write("PASS\n")
```

---

## Q16. Does `write()` automatically add a newline?

No.

This:

```python
file.write("PASS")
```

does not automatically add:

```text
\n
```

If a newline is required:

```python
file.write("PASS\n")
```

---

## Q17. What is `writelines()`?

`writelines()` writes an iterable of strings.

Example:

```python
lines = [
    "TEST_001 PASS\n",
    "TEST_002 FAIL\n"
]

file.writelines(lines)
```

It does not automatically insert newlines between elements.

---

# 7. Context Managers

## Q18. Why should you use `with open(...)`?

A context manager ensures that the file is properly closed after the block finishes, including when an exception occurs.

Example:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read()
```

This is safer and cleaner than manually managing `close()`.

---

## Q19. What happens when an exception occurs inside a `with` block?

The context manager performs its cleanup operation before the exception propagates.

For a file, this means the file is properly closed.

---

## Q20. Why is resource lifetime different from object lifetime?

The Python file object may still exist as an object, but the underlying operating-system file resource can already have been released after leaving the context manager.

The important concept is:

```text
Python object lifetime
        ≠
Underlying resource lifetime
```

---

# 8. `pathlib`

## Q21. Why use `pathlib`?

`pathlib` provides an object-oriented way to work with filesystem paths.

Example:

```python
from pathlib import Path

path = Path("results/test_results.txt")
```

It makes path manipulation clearer and more portable.

---

## Q22. How do you check whether a path exists?

```python
path.exists()
```

---

## Q23. How do you determine whether a path is a file or directory?

```python
path.is_file()
path.is_dir()
```

---

## Q24. How do you obtain the absolute path?

```python
path.resolve()
```

Example:

```python
print(path.resolve())
```

This is particularly useful when troubleshooting relative-path problems.

---

## Q25. How do you construct paths using `pathlib`?

Use `/`.

Example:

```python
base = Path("results")
report = base / "run_001" / "report.txt"
```

This is preferred over manually concatenating strings.

---

# 9. Directory Handling

## Q26. How do you create a directory?

```python
path.mkdir()
```

---

## Q27. What does `parents=True` do?

It allows missing parent directories to be created.

Example:

```python
path.mkdir(parents=True)
```

---

## Q28. What does `exist_ok=True` do?

It prevents an error when the directory already exists.

Example:

```python
path.mkdir(
    parents=True,
    exist_ok=True
)
```

This is useful for repeatable automation.

---

# 10. Directory Traversal

## Q29. What is the difference between `iterdir()` and `rglob()`?

### `iterdir()`

Returns entries directly inside a directory.

```python
for path in root.iterdir():
    print(path)
```

### `rglob()`

Recursively searches through subdirectories.

```python
for path in root.rglob("*.log"):
    print(path)
```

---

## Q30. How would you find all log files recursively?

```python
for path in root.rglob("*.log"):
    print(path)
```

This is useful when collecting logs from test-run directories.

---

# 11. File Operations

## Q31. How do you rename a file using `pathlib`?

```python
path.rename(new_path)
```

---

## Q32. How do you delete a file?

```python
path.unlink()
```

Use deletion carefully, especially for test artifacts.

---

## Q33. What is the difference between copying and moving?

Copying:

```text
Source
  ↓
Destination

Source remains
```

Moving:

```text
Source
  ↓
Destination

Source is moved
```

Python commonly uses:

```python
shutil.copy2()
shutil.move()
```

---

## Q34. Why might `copy2()` be preferable to `copy()`?

`copy2()` attempts to preserve additional metadata such as timestamps along with the file contents.

Whether that metadata matters depends on the automation requirement.

---

# 12. Large File Processing

## Q35. Why should you avoid `read()` for very large files?

Because it can load the entire file into memory.

For large logs, prefer:

```python
with path.open("r", encoding="utf-8") as file:
    for line in file:
        process(line)
```

---

## Q36. How can binary files be processed in chunks?

Example:

```python
with path.open("rb") as file:
    while chunk := file.read(1024 * 1024):
        process(chunk)
```

This allows large binary data to be processed incrementally.

---

# 13. File Comparison

## Q37. How do you compare two files for exact equality?

If their contents are already loaded:

```python
if expected == actual:
    print("MATCH")
```

For complete files, another approach is to compare their contents or hashes depending on the requirements.

---

## Q38. What is `difflib` useful for?

`difflib` can produce human-readable differences between sequences.

Example:

```python
import difflib

diff = difflib.unified_diff(
    expected,
    actual,
    fromfile="expected",
    tofile="actual"
)
```

This is useful when a simple PASS/FAIL comparison is not enough.

---

## Q39. What do `-` and `+` mean in a unified diff?

Typically:

```text
- → removed / expected-side content
+ → added / actual-side content
```

Unchanged lines may appear with a leading space depending on the diff output.

---

# 14. JSON

## Q40. What is JSON?

JSON is a structured data interchange format commonly used for:

* APIs
* Metadata
* Configuration
* Machine-readable data

---

## Q41. What is the difference between `load()` and `loads()`?

```python
json.load(file)
```

reads JSON from a file object.

```python
json.loads(string)
```

reads JSON from a string.

---

## Q42. What is the difference between `dump()` and `dumps()`?

```python
json.dump(data, file)
```

writes JSON to a file.

```python
json.dumps(data)
```

returns JSON as a string.

---

## Q43. What exception is raised for invalid JSON?

Typically:

```python
json.JSONDecodeError
```

---

# 15. CSV

## Q44. Why is CSV useful in automation?

CSV is useful when data is naturally tabular.

Examples:

```text
Test ID
Status
Duration
Device
Performance
```

---

## Q45. What is `csv.DictReader`?

It reads CSV rows as dictionaries using the header names as keys.

Example:

```python
with open(
    "results.csv",
    "r",
    newline="",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for row in reader:
        print(row["test_id"])
```

---

## Q46. Why use `newline=""` with Python's CSV module?

It allows the CSV module to handle newline processing correctly and helps avoid unwanted blank-line behavior, particularly across platforms.

---

## Q47. What types do CSV values initially have?

CSV data is read as strings.

For example:

```csv
test_id,duration
TEST_001,30
```

The value:

```python
row["duration"]
```

is initially a string.

If numeric processing is required:

```python
duration = int(row["duration"])
```

---

# 16. YAML

## Q48. What is YAML commonly used for?

YAML is commonly used for human-readable configuration.

Example:

```yaml
execution:
  timeout: 60
  retries: 2
```

---

## Q49. How do you read YAML in Python?

Using PyYAML:

```python
import yaml

with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
```

---

## Q50. Why use `safe_load()`?

It is the preferred approach for loading normal configuration/data because it avoids unnecessary arbitrary Python object construction.

---

## Q51. What exception can malformed YAML produce?

Typically:

```python
yaml.YAMLError
```

---

# 17. Choosing File Formats

## Q52. When would you use TXT?

For:

* Logs
* Simple text
* Human-readable reports
* Command output

---

## Q53. When would you use CSV?

For:

* Tabular test results
* Performance measurements
* Device inventories
* Spreadsheet-compatible reports

---

## Q54. When would you use JSON?

For:

* APIs
* Structured metadata
* Nested machine-readable data

---

## Q55. When would you use YAML?

For:

* Automation configuration
* Test configuration
* Environment configuration
* Human-maintained settings

---

# 18. File Automation Architecture

## Q56. What is a common file-processing automation pattern?

```text
Input
 ↓
Read
 ↓
Parse
 ↓
Validate
 ↓
Process
 ↓
Output
 ↓
Report
```

This is one of the most important patterns in file-based automation.

---

## Q57. Why separate parsing and validation?

Because they answer different questions.

Parsing:

> Can I understand the structure?

Validation:

> Does the data satisfy my requirements?

---

## Q58. Why separate configuration from automation logic?

It allows the same automation to operate with different:

* Devices
* Test selections
* Timeouts
* Retry counts
* Environments

without changing the core Python implementation.

---

# 19. Troubleshooting

## Q59. What would you check if a file cannot be opened?

A systematic approach:

```text
Path
 ↓
Existence
 ↓
File/directory type
 ↓
Permissions
 ↓
Encoding
 ↓
Content
 ↓
Format
 ↓
Concurrent modification
```

---

## Q60. Does `exists()` guarantee that a subsequent operation will succeed?

No.

The filesystem can change between the existence check and the later operation.

This is related to:

> TOCTOU — Time Of Check To Time Of Use.

---

## Q61. What is the difference between a symptom and a root cause?

Example:

```text
Symptom:
Unable to read results.csv

Possible root cause:
Permission denied
```

Other possible root causes could include:

* File missing
* Wrong path
* Directory instead of file
* Filesystem full
* Concurrent file operation

Good troubleshooting goes beyond the immediate error message.

---

# 20. Exception Handling

## Q62. Which exceptions commonly occur during file handling?

Examples:

```python
FileNotFoundError
PermissionError
IsADirectoryError
NotADirectoryError
UnicodeDecodeError
ValueError
```

The exact exception depends on the operation and failure.

---

## Q63. Should you catch `Exception` for every file operation?

Generally, no.

Avoid:

```python
try:
    ...
except Exception:
    pass
```

because it can hide real problems.

Prefer handling known failures explicitly.

---

## Q64. Why are useful error messages important?

A good error message should provide useful diagnostic context.

For example:

```python
print(f"Configuration file not found: {path.resolve()}")
```

is much more useful than:

```python
print("Error")
```

---

# 21. Storage Test Automation Questions

## Q65. How would you design file handling for a storage test framework?

A reasonable structure is:

```text
Configuration
      ↓
Input
      ↓
Parsing
      ↓
Validation
      ↓
Test Execution
      ↓
Result Collection
      ↓
Reporting
      ↓
Artifact Preservation
```

---

## Q66. What files might a storage test framework generate?

Examples:

```text
Configuration
Logs
Test results
Performance data
Device metadata
Failure reports
Debug artifacts
```

---

## Q67. Why should storage test artifacts be preserved?

They provide evidence for:

* Failure analysis
* Debugging
* Root-cause analysis
* Test reproducibility
* Result verification

---

## Q68. How would you process a large storage log?

Prefer streaming:

```python
with open("kernel.log", "r", encoding="utf-8") as file:
    for line in file:
        if "error" in line.lower():
            process(line)
```

This avoids unnecessarily loading the entire log into memory.

---

## Q69. How would you make test output directories repeatable?

Example:

```python
output_dir.mkdir(
    parents=True,
    exist_ok=True
)
```

For individual test runs, use separate run directories when artifact preservation is important.

Example:

```text
results/
├── run_001/
├── run_002/
└── run_003/
```

---

# 22. Scenario-Based Interview Questions

## Q70. Your automation says `FileNotFoundError`, but you can see the file on disk. What do you check?

Check:

```text
1. Current working directory
2. Relative vs absolute path
3. Resolved path
4. Filename spelling
5. Case sensitivity
6. Mount/filesystem state
7. Whether the file is visible to the executing process
```

Useful Python:

```python
print(Path.cwd())
print(path.resolve())
print(path.exists())
```

---

## Q71. Your CSV parser fails on one row. What do you investigate?

Check:

```text
Delimiter
Column count
Quoting
Missing fields
Unexpected fields
Encoding
Malformed row
```

Do not immediately assume the Python CSV module is broken.

---

## Q72. A test report is suddenly empty after automation runs. What could have happened?

One possibility is opening the file with:

```python
open("report.txt", "w")
```

which truncates the file.

Other possibilities include:

* Automation failure before writing
* Incorrect output path
* Partial write
* Disk-full condition

---

## Q73. A 20 GB log causes your script to consume too much memory. What would you change?

Instead of:

```python
data = file.read()
```

use incremental processing:

```python
for line in file:
    process(line)
```

or binary chunk processing where appropriate.

---

## Q74. A configuration file parses successfully but the test still fails. What do you investigate?

Do not assume successful parsing means valid configuration.

Check:

```text
Required keys
Data types
Allowed values
Device paths
Timeouts
Retry values
Test selections
Environment settings
```

---

## Q75. A file exists when discovered but disappears before it is opened. Why?

Another process may have modified or deleted the file between the two operations.

This is a race condition and can be related to TOCTOU.

Handle the actual operation with appropriate exception handling rather than relying solely on `exists()`.

---

# 23. Coding Questions

## Q76. Read all failed test IDs from a result file.

Input:

```text
TEST_001 PASS
TEST_002 FAIL
TEST_003 PASS
TEST_004 FAIL
```

Expected:

```python
["TEST_002", "TEST_004"]
```

Possible solution:

```python
from pathlib import Path

failed_tests = []

path = Path("results.txt")

with path.open("r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        test_id, status = line.split()

        if status == "FAIL":
            failed_tests.append(test_id)

print(failed_tests)
```

---

## Q77. Count PASS and FAIL results.

```python
passed = 0
failed = 0

with path.open("r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        _, status = line.split()

        if status == "PASS":
            passed += 1

        elif status == "FAIL":
            failed += 1
```

---

## Q78. Find all `.log` files recursively.

```python
from pathlib import Path

root = Path("logs")

for path in root.rglob("*.log"):
    print(path)
```

---

## Q79. Create a result directory safely.

```python
from pathlib import Path

result_dir = Path("results/run_001")

result_dir.mkdir(
    parents=True,
    exist_ok=True
)
```

---

## Q80. Read JSON safely.

```python
import json

try:
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

except FileNotFoundError:
    print("Configuration file not found.")

except json.JSONDecodeError as error:
    print(f"Invalid JSON: {error}")
```

---

# 24. Rapid-Fire Revision

Before an interview, remember these:

```text
open()
→ opens a file

r
→ read

w
→ write + truncate

a
→ append

x
→ create only

rb
→ binary read

with
→ automatic cleanup

read()
→ read content

readline()
→ read one line

readlines()
→ list of lines

tell()
→ current position

seek()
→ move position

Path
→ filesystem path abstraction

exists()
→ path exists?

is_file()
→ regular file?

is_dir()
→ directory?

mkdir()
→ create directory

iterdir()
→ direct children

rglob()
→ recursive matching

rename()
→ rename/move within pathlib

unlink()
→ delete file

copy2()
→ copy file + metadata

move()
→ move file/directory

JSON
→ structured/API data

CSV
→ tabular data

YAML
→ configuration

safe_load()
→ YAML → Python

safe_dump()
→ Python → YAML

read line-by-line
→ large-file processing

difflib
→ detailed sequence differences

FileNotFoundError
→ missing path/file

PermissionError
→ access denied

UnicodeDecodeError
→ decoding problem

TOCTOU
→ resource changes between check and use
```

---

# 25. Most Important Interview Principles

Do not memorize only syntax.

Be able to explain these principles:

### Principle 1

> Use context managers for resource-safe file handling.

### Principle 2

> Use `pathlib` for clear filesystem path manipulation.

### Principle 3

> Process large files incrementally when the entire file is unnecessary.

### Principle 4

> Parsing and validation are separate responsibilities.

### Principle 5

> Choose file formats based on data structure and consumer requirements.

### Principle 6

> Do not assume `exists()` guarantees a later filesystem operation.

### Principle 7

> Preserve useful test artifacts for troubleshooting.

### Principle 8

> Error messages should provide actionable diagnostic information.

### Principle 9

> Configuration should generally be separated from automation logic.

### Principle 10

> Troubleshoot the root cause, not merely the visible symptom.

---

# 26. Storage Automation Mental Model

The complete Module-07 picture is:

```text
                         FILE HANDLING
                              |
        +---------------------+---------------------+
        |                     |                     |
      Files               Directories          Formats
        |                     |                     |
     Read/Write          Traverse/Manage       TXT/CSV/JSON/YAML
        |                     |                     |
        +---------------------+---------------------+
                              |
                         Automation
                              |
                    +---------+---------+
                    |                   |
                 Input                Output
                    |                   |
                 Parse                Report
                    |                   |
               Validate             Results
                    |                   |
                 Process             Artifacts
                    |
                Troubleshoot
```

---

# 27. Final Interview Checklist

Before considering File Handling interview preparation complete, you should be able to explain and demonstrate:

```text
[ ] open()
[ ] File modes
[ ] Text vs binary
[ ] read()
[ ] readline()
[ ] readlines()
[ ] File iteration
[ ] tell()
[ ] seek()
[ ] write()
[ ] writelines()
[ ] Context managers
[ ] pathlib
[ ] mkdir()
[ ] Directory traversal
[ ] File rename/delete
[ ] Copy/move
[ ] Large-file processing
[ ] File comparison
[ ] JSON
[ ] CSV
[ ] YAML
[ ] Format selection
[ ] Configuration-driven automation
[ ] Exception handling
[ ] Permission problems
[ ] Missing files
[ ] Invalid data
[ ] Encoding problems
[ ] Disk-space problems
[ ] Concurrent access
[ ] TOCTOU
[ ] Artifact preservation
[ ] Root-cause troubleshooting
```

---

# 28. Key Takeaways

File handling is not just:

```python
open()
read()
write()
```

For a Storage Test Automation Engineer, it becomes:

```text
Filesystem
    ↓
Input
    ↓
Parsing
    ↓
Validation
    ↓
Automation
    ↓
Results
    ↓
Reporting
    ↓
Artifacts
    ↓
Troubleshooting
```

The most important skill is being able to build automation that remains reliable when the filesystem or input data is not perfect.

---

# Automation Principle

> **Production-quality automation assumes that files can be missing, malformed, inaccessible, unexpectedly modified, or very large—and handles those conditions deliberately.**

```


