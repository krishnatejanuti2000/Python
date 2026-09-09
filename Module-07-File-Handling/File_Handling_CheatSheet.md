# `File_Handling_CheatSheet.md`

````markdown
# File Handling — Cheat Sheet

## 1. File Opening

```python
file = open("file.txt", "r", encoding="utf-8")
````

Preferred:

```python
with open("file.txt", "r", encoding="utf-8") as file:
    data = file.read()
```

Using `with` ensures proper resource cleanup.

---

# 2. File Modes

| Mode | Meaning                         |
| ---- | ------------------------------- |
| `r`  | Read                            |
| `w`  | Write + truncate                |
| `a`  | Append                          |
| `x`  | Create new file; fail if exists |
| `r+` | Read + write                    |
| `w+` | Read + write + truncate         |
| `a+` | Read + append                   |
| `rb` | Binary read                     |
| `wb` | Binary write                    |
| `ab` | Binary append                   |

Important:

```text
w → destroys existing contents
a → preserves existing contents
x → prevents accidental overwrite
```

---

# 3. Reading Files

## Entire file

```python
with open("file.txt", "r", encoding="utf-8") as file:
    data = file.read()
```

## Limited amount

```python
data = file.read(100)
```

## One line

```python
line = file.readline()
```

## All remaining lines

```python
lines = file.readlines()
```

## Recommended for large files

```python
with open("large.log", "r", encoding="utf-8") as file:
    for line in file:
        process(line)
```

---

# 4. Cleaning Lines

```python
line = line.strip()
```

Removes leading/trailing whitespace, including newline characters.

Example:

```python
"TEST_001 PASS\n".strip()
```

becomes:

```text
TEST_001 PASS
```

---

# 5. Writing Files

```python
with open("report.txt", "w", encoding="utf-8") as file:
    file.write("Storage Test Report\n")
```

`write()` expects a string.

```python
file.write("PASS\n")
```

No newline is added automatically.

---

# 6. `write()` vs `writelines()`

### `write()`

```python
file.write("TEST_001 PASS\n")
```

### `writelines()`

```python
lines = [
    "TEST_001 PASS\n",
    "TEST_002 FAIL\n"
]

file.writelines(lines)
```

Important:

> `writelines()` does not automatically insert newlines.

---

# 7. Append

```python
with open("results.txt", "a", encoding="utf-8") as file:
    file.write("TEST_004 PASS\n")
```

Existing contents remain.

Be careful about newline boundaries when appending to files whose last line may not end with `\n`.

---

# 8. File Position

## `tell()`

Returns the current file position.

```python
position = file.tell()
```

## `seek()`

Moves the current position.

```python
file.seek(0)
```

Moves to the beginning.

Remember:

```text
tell() → where am I?
seek() → move there
```

`tell()` is not inherently the file size.

---

# 9. `pathlib`

Preferred for filesystem paths:

```python
from pathlib import Path

path = Path("results/test_results.txt")
```

## Current directory

```python
Path.cwd()
```

## Absolute path

```python
path.resolve()
```

## Existence

```python
path.exists()
```

## File check

```python
path.is_file()
```

## Directory check

```python
path.is_dir()
```

---

# 10. Path Construction

Use `/`:

```python
base = Path("results")

report = base / "run_001" / "report.txt"
```

Avoid manually concatenating path strings.

---

# 11. Path Properties

```python
path.name
path.parent
path.stem
path.suffix
```

Example:

```text
results/test_report.txt
```

| Expression | Result            |
| ---------- | ----------------- |
| `name`     | `test_report.txt` |
| `parent`   | `results`         |
| `stem`     | `test_report`     |
| `suffix`   | `.txt`            |

---

# 12. `Path.open()`

Instead of:

```python
open(path, "r", encoding="utf-8")
```

you can use:

```python
path.open("r", encoding="utf-8")
```

Example:

```python
with path.open("r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

---

# 13. Directory Creation

```python
path.mkdir()
```

Create missing parents:

```python
path.mkdir(parents=True)
```

Avoid failure when directory already exists:

```python
path.mkdir(
    parents=True,
    exist_ok=True
)
```

Common automation pattern:

```python
output_dir.mkdir(
    parents=True,
    exist_ok=True
)
```

---

# 14. Directory Traversal

## Direct children

```python
for path in root.iterdir():
    print(path)
```

`iterdir()` does not recursively search subdirectories.

## Recursive search

```python
for path in root.rglob("*"):
    print(path)
```

## Find logs recursively

```python
for path in root.rglob("*.log"):
    print(path)
```

---

# 15. File Operations

## Rename

```python
path.rename(new_path)
```

## Delete

```python
path.unlink()
```

## Delete without error if missing

```python
path.unlink(missing_ok=True)
```

Use deletion carefully when test artifacts are valuable.

---

# 16. Copy and Move

Import:

```python
import shutil
```

## Copy

```python
shutil.copy2(source, destination)
```

## Move

```python
shutil.move(source, destination)
```

Remember:

```text
copy → source remains

move → source is moved
```

---

# 17. Large File Processing

Avoid unnecessarily doing:

```python
data = file.read()
```

for huge files.

Prefer:

```python
with path.open("r", encoding="utf-8") as file:
    for line in file:
        process(line)
```

For binary data:

```python
with path.open("rb") as file:
    while chunk := file.read(1024 * 1024):
        process(chunk)
```

---

# 18. File Comparison

Simple comparison:

```python
if expected == actual:
    print("MATCH")
```

For detailed differences:

```python
import difflib

diff = difflib.unified_diff(
    expected,
    actual,
    fromfile="expected",
    tofile="actual"
)
```

Common diff symbols:

```text
- → removed / expected-side content
+ → added / actual-side content
```

`difflib` compares sequences; it does not itself read files.

---

# 19. JSON

Import:

```python
import json
```

## JSON file → Python

```python
with open("config.json", "r", encoding="utf-8") as file:
    data = json.load(file)
```

## JSON string → Python

```python
data = json.loads(text)
```

## Python → JSON file

```python
with open("config.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)
```

## Python → JSON string

```python
text = json.dumps(data, indent=4)
```

Invalid JSON:

```python
json.JSONDecodeError
```

---

# 20. CSV

Import:

```python
import csv
```

## Read rows

```python
with open(
    "results.csv",
    "r",
    newline="",
    encoding="utf-8"
) as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)
```

## Dictionary rows

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

## Write CSV

```python
with open(
    "results.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow(["test_id", "status"])
    writer.writerow(["TEST_001", "PASS"])
```

## Dictionary writer

```python
writer = csv.DictWriter(
    file,
    fieldnames=["test_id", "status"]
)

writer.writeheader()
writer.writerow({
    "test_id": "TEST_001",
    "status": "PASS"
})
```

Important:

> CSV values are initially read as strings.

---

# 21. YAML

Install PyYAML:

```bash
pip install pyyaml
```

Import:

```python
import yaml
```

## Read YAML

```python
with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
```

## Write YAML

```python
with open("config.yaml", "w", encoding="utf-8") as file:
    yaml.safe_dump(config, file)
```

Recommended:

```text
safe_load()
safe_dump()
```

Malformed YAML can raise:

```python
yaml.YAMLError
```

---

# 22. Choosing File Formats

| Requirement               | Recommended |
| ------------------------- | ----------- |
| Simple text               | TXT         |
| Logs                      | TXT         |
| Human-readable report     | TXT         |
| Tabular results           | CSV         |
| Device inventory          | CSV         |
| API data                  | JSON        |
| Structured metadata       | JSON        |
| Automation configuration  | YAML        |
| Test configuration        | YAML        |
| Environment configuration | YAML        |

Core rule:

> Choose the format based on the data structure, consumer, interoperability requirements, scale, and maintainability.

---

# 23. Configuration-Driven Automation

Example:

```yaml
execution:
  timeout: 60
  retries: 2

tests:
  - read
  - write
  - verify
```

Python:

```python
import yaml

with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

timeout = config["execution"]["timeout"]
retries = config["execution"]["retries"]
tests = config["tests"]
```

Architecture:

```text
YAML
 ↓
Load
 ↓
Parse
 ↓
Validate
 ↓
Python Automation
 ↓
Execute
 ↓
Results
```

---

# 24. File Automation Pattern

The core pattern:

```text
INPUT
  ↓
READ
  ↓
PARSE
  ↓
VALIDATE
  ↓
PROCESS
  ↓
OUTPUT
  ↓
REPORT
```

For storage automation:

```text
Configuration
      ↓
Test Execution
      ↓
Result Collection
      ↓
Analysis
      ↓
Reporting
      ↓
Artifact Preservation
```

---

# 25. Exception Handling

Common file-related exceptions:

```python
FileNotFoundError
PermissionError
IsADirectoryError
NotADirectoryError
UnicodeDecodeError
ValueError
```

JSON:

```python
json.JSONDecodeError
```

YAML:

```python
yaml.YAMLError
```

Example:

```python
try:
    with path.open("r", encoding="utf-8") as file:
        data = file.read()

except FileNotFoundError:
    print(f"File not found: {path}")

except PermissionError:
    print(f"Permission denied: {path}")
```

Avoid:

```python
try:
    ...
except Exception:
    pass
```

because it can hide real failures.

---

# 26. Troubleshooting Checklist

When a file operation fails:

```text
[ ] Check path
[ ] Check current working directory
[ ] Check resolved path
[ ] Check existence
[ ] Check file vs directory
[ ] Check permissions
[ ] Check ownership
[ ] Check encoding
[ ] Check contents
[ ] Check expected format
[ ] Check data validation
[ ] Check file size
[ ] Check disk space
[ ] Check concurrent access
[ ] Check whether another process modified/deleted it
[ ] Preserve diagnostic artifacts
```

Useful:

```python
print(Path.cwd())
print(path.resolve())
print(path.exists())
print(path.is_file())
print(path.is_dir())
```

---

# 27. TOCTOU

TOCTOU:

> Time Of Check To Time Of Use

Problem:

```python
if path.exists():
    with path.open("r", encoding="utf-8") as file:
        ...
```

The file could disappear between:

```text
exists()
  ↓
open()
```

Therefore, an existence check does not guarantee that the later operation will succeed.

Handle the actual operation appropriately:

```python
try:
    with path.open("r", encoding="utf-8") as file:
        data = file.read()

except FileNotFoundError:
    print("File disappeared before it was opened.")
```

---

# 28. Root Cause vs Symptom

Example:

```text
Symptom:
Unable to read results.csv

Possible root causes:
- File does not exist
- Wrong path
- Permission denied
- Path is a directory
- Filesystem is full
- Another process deleted the file
- File is inaccessible
```

Good troubleshooting asks:

> Why did the expected condition not occur?

rather than stopping at the first error message.

---

# 29. Artifact Preservation

Storage test automation may produce:

```text
run_001/
├── config.yaml
├── kernel.log
├── test_results.csv
├── metadata.json
└── report.txt
```

These artifacts can provide evidence for:

* Debugging
* Failure analysis
* Root-cause analysis
* Reproducibility
* Result verification

Do not automatically delete useful failure artifacts.

---

# 30. Best Practices

```text
1. Use context managers.
2. Specify text encoding explicitly.
3. Prefer pathlib for filesystem paths.
4. Process large files incrementally.
5. Validate input before processing.
6. Handle expected exceptions specifically.
7. Avoid accidental overwrites.
8. Preserve important test artifacts.
9. Avoid unnecessary hard-coded paths.
10. Make output generation repeatable.
11. Separate configuration from automation logic.
12. Troubleshoot root causes, not just symptoms.
```

---

# 31. Storage Automation Mental Model

```text
                STORAGE TEST AUTOMATION
                         |
                  File Handling
                         |
       +-----------------+-----------------+
       |                 |                 |
   Configuration       Results          Artifacts
       |                 |                 |
      YAML              CSV             TXT/JSON
       |                 |                 |
       +-----------------+-----------------+
                         |
                      Python
                         |
              Read → Parse → Validate
                         |
                      Process
                         |
                    Report
                         |
                 Troubleshooting
```

---

# 32. Final Revision

The most important concepts in Module-07 are:

```text
open()
file modes
read()
readline()
readlines()
file iteration
tell()
seek()
write()
writelines()
with
pathlib
mkdir()
iterdir()
rglob()
rename()
unlink()
copy2()
move()
large-file processing
file comparison
JSON
CSV
YAML
file-format selection
configuration-driven automation
exception handling
troubleshooting
TOCTOU
artifact preservation
```

---

# Automation Principle

> **File handling in automation is not just reading and writing files. It is the disciplined management of input, configuration, results, artifacts, resources, errors, and evidence throughout the test lifecycle.**

````
