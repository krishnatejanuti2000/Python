# `File_Handling_Quick_Revision.md`

````markdown
# File Handling — Quick Revision

## 1. Core File Handling

Python opens files using:

```python
open("file.txt", "r", encoding="utf-8")
````

Preferred pattern:

```python
with open("file.txt", "r", encoding="utf-8") as file:
    data = file.read()
```

Core idea:

```text
open → use → automatic cleanup
```

---

# 2. File Modes

```text
r   → read
w   → write + truncate
a   → append
x   → create new file only

r+  → read + write
w+  → read + write + truncate
a+  → read + append

rb  → binary read
wb  → binary write
ab  → binary append
```

Remember:

```text
w → existing contents are destroyed
a → existing contents are preserved
x → existing file causes failure
```

---

# 3. Reading

```python
file.read()
```

Read content.

```python
file.read(100)
```

Read a limited amount.

```python
file.readline()
```

Read one line.

```python
file.readlines()
```

Read remaining lines into a list.

Preferred for large files:

```python
for line in file:
    process(line)
```

---

# 4. File Position

```python
file.tell()
```

Returns the current position.

```python
file.seek(0)
```

Moves the position.

Remember:

```text
tell → where am I?
seek → move position
```

`tell()` does not inherently mean file size.

---

# 5. Writing

```python
file.write("PASS\n")
```

Writes a string.

`write()` does not automatically add a newline.

```python
file.writelines(lines)
```

Writes multiple strings.

Important:

```text
writelines()
→ does NOT automatically add newlines
```

---

# 6. Context Managers

Preferred:

```python
with path.open("r", encoding="utf-8") as file:
    ...
```

Why?

```text
Resource acquired
      ↓
Use resource
      ↓
Cleanup automatically
```

Even if an exception occurs inside the block, cleanup is performed.

---

# 7. Pathlib

```python
from pathlib import Path
```

Create a path:

```python
path = Path("results/test_results.txt")
```

Current directory:

```python
Path.cwd()
```

Absolute path:

```python
path.resolve()
```

Check existence:

```python
path.exists()
```

Check file:

```python
path.is_file()
```

Check directory:

```python
path.is_dir()
```

Construct paths:

```python
report = Path("results") / "run_001" / "report.txt"
```

Properties:

```python
path.name
path.parent
path.stem
path.suffix
```

---

# 8. Directory Creation

```python
path.mkdir()
```

Create parent directories:

```python
path.mkdir(parents=True)
```

Safe repeatable creation:

```python
path.mkdir(
    parents=True,
    exist_ok=True
)
```

---

# 9. Directory Traversal

Direct children:

```python
for path in root.iterdir():
    print(path)
```

Recursive traversal:

```python
for path in root.rglob("*"):
    print(path)
```

Find logs:

```python
for path in root.rglob("*.log"):
    process(path)
```

Remember:

```text
iterdir → direct children
rglob   → recursive search
```

---

# 10. File Operations

Rename:

```python
path.rename(new_path)
```

Delete:

```python
path.unlink()
```

Delete without error if missing:

```python
path.unlink(missing_ok=True)
```

Copy:

```python
import shutil

shutil.copy2(source, destination)
```

Move:

```python
shutil.move(source, destination)
```

Remember:

```text
copy → source remains
move → source is moved
```

---

# 11. Large Files

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

For binary files:

```python
with path.open("rb") as file:
    while chunk := file.read(1024 * 1024):
        process(chunk)
```

Core principle:

> Process large data incrementally when the entire file does not need to be in memory.

---

# 12. File Comparison

Simple equality:

```python
if expected == actual:
    print("MATCH")
```

Detailed differences:

```python
import difflib

diff = difflib.unified_diff(
    expected,
    actual,
    fromfile="expected",
    tofile="actual"
)
```

Common symbols:

```text
- → removed / expected-side content
+ → added / actual-side content
```

`difflib` compares sequences; it does not itself read files.

---

# 13. JSON

```python
import json
```

File → Python:

```python
json.load(file)
```

String → Python:

```python
json.loads(text)
```

Python → file:

```python
json.dump(data, file)
```

Python → JSON string:

```python
json.dumps(data)
```

Invalid JSON:

```python
json.JSONDecodeError
```

---

# 14. CSV

```python
import csv
```

Read:

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

Dictionary-based reading:

```python
reader = csv.DictReader(file)
```

Writing:

```python
writer = csv.writer(file)
writer.writerow(["test_id", "status"])
```

Dictionary writing:

```python
writer = csv.DictWriter(
    file,
    fieldnames=["test_id", "status"]
)

writer.writeheader()
```

Important:

> CSV values are initially read as strings.

---

# 15. YAML

Using PyYAML:

```python
import yaml
```

Read:

```python
with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
```

Write:

```python
with open("config.yaml", "w", encoding="utf-8") as file:
    yaml.safe_dump(config, file)
```

Preferred APIs:

```text
safe_load()
safe_dump()
```

Malformed YAML:

```python
yaml.YAMLError
```

---

# 16. File Format Selection

```text
TXT
→ logs
→ simple text
→ human-readable reports

CSV
→ rows and columns
→ test results
→ performance data

JSON
→ structured data
→ APIs
→ metadata

YAML
→ configuration
→ test configuration
→ environment configuration
```

Core principle:

> Choose the format according to the data structure and its consumer.

---

# 17. Automation Pattern

The fundamental file automation pattern:

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

Storage automation example:

```text
config.yaml
     ↓
Load configuration
     ↓
Validate
     ↓
Execute tests
     ↓
Collect results
     ↓
Analyze
     ↓
Generate report
     ↓
Preserve artifacts
```

---

# 18. Configuration-Driven Automation

Instead of hard-coding:

```python
timeout = 60
retries = 2
```

configuration can be stored in YAML:

```yaml
execution:
  timeout: 60
  retries: 2
```

Python:

```python
timeout = config["execution"]["timeout"]
retries = config["execution"]["retries"]
```

Core principle:

> Configuration describes what should be executed; Python contains the logic for how it is executed.

---

# 19. Parsing vs Validation

These are different.

### Parsing

```text
Can I understand the structure?
```

### Validation

```text
Is the data acceptable?
```

Example:

```python
test_id, status = line.split()
```

Parsing.

Then:

```python
if status not in {"PASS", "FAIL"}:
    raise ValueError("Invalid status")
```

Validation.

---

# 20. Common Exceptions

File handling:

```text
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

Handle expected failures explicitly.

Avoid:

```python
try:
    ...
except Exception:
    pass
```

because it can hide real failures.

---

# 21. Troubleshooting

When a file operation fails:

```text
Path
 ↓
Current working directory
 ↓
Resolved path
 ↓
Existence
 ↓
File vs directory
 ↓
Permissions
 ↓
Encoding
 ↓
Content
 ↓
Format
 ↓
Validation
 ↓
Concurrency
 ↓
Disk space
```

Useful diagnostics:

```python
print(Path.cwd())
print(path.resolve())
print(path.exists())
print(path.is_file())
print(path.is_dir())
```

---

# 22. TOCTOU

TOCTOU:

> Time Of Check To Time Of Use

Example:

```python
if path.exists():
    path.open()
```

The file may disappear between:

```text
exists()
  ↓
open()
```

Therefore:

> An existence check does not guarantee that a later filesystem operation will succeed.

Handle the actual operation appropriately.

---

# 23. Root Cause Analysis

Do not stop at:

```text
"File read failed"
```

Investigate:

```text
Wrong path?
    ↓
File missing?
    ↓
Permission denied?
    ↓
Directory instead of file?
    ↓
Filesystem full?
    ↓
File deleted?
    ↓
File modified?
```

Remember:

```text
Symptom ≠ Root Cause
```

---

# 24. Artifact Preservation

Storage tests may produce:

```text
run_001/
├── config.yaml
├── kernel.log
├── test_results.csv
├── metadata.json
└── report.txt
```

Preserve useful artifacts because they provide evidence for:

* Debugging
* Failure analysis
* Root-cause analysis
* Reproducibility
* Result verification

---

# 25. Storage Test Automation Mental Model

```text
                 STORAGE TEST
                      |
                Configuration
                      |
                     YAML
                      ↓
                   Python
                      |
              Read / Parse / Validate
                      |
                 Execute Tests
                      |
               Collect Results
                      |
          +-----------+-----------+
          |                       |
         Logs                  Results
          |                       |
         TXT                     CSV
          |                       |
          +-----------+-----------+
                      |
                    JSON
                      |
                 Metadata
                      |
                   Report
```

---

# 26. Interview Rapid Revision

### File modes

```text
r → read
w → write/truncate
a → append
x → create only
```

### Large files

```text
iterate line-by-line
```

### Paths

```text
pathlib.Path
```

### Context management

```text
with
```

### Recursive files

```python
rglob()
```

### JSON

```text
load / loads
dump / dumps
```

### CSV

```text
reader / DictReader
writer / DictWriter
```

### YAML

```text
safe_load / safe_dump
```

### Troubleshooting

```text
Path → Access → Content → Format → Validation
```

### Automation

```text
Input
 ↓
Parse
 ↓
Validate
 ↓
Process
 ↓
Report
```

---

# 27. Final Principles

Remember these ten principles:

```text
1. Use context managers.
2. Prefer pathlib for filesystem paths.
3. Specify encoding explicitly.
4. Process large files incrementally.
5. Validate important input.
6. Choose the appropriate file format.
7. Handle expected exceptions specifically.
8. Preserve valuable test artifacts.
9. Separate configuration from automation logic.
10. Troubleshoot root causes rather than symptoms.
```

---

# Automation Principle

> **Reliable file automation is the disciplined movement of data from input to validated processing to preserved evidence.**


