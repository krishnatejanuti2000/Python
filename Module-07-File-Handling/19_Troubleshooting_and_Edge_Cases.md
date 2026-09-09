# 19 — Troubleshooting and Edge Cases

````markdown
# Troubleshooting and Edge Cases

## 1. Introduction

File handling in automation is simple when everything goes as expected.

Real automation environments are different.

Files can be:

- Missing
- Empty
- Corrupted
- Inaccessible
- Unexpectedly modified
- Extremely large
- In the wrong format
- Replaced by a directory
- Encoded differently
- Deleted while the automation is running

A Storage Test Automation engineer must therefore understand not only how to process files, but also how to diagnose and handle filesystem-related failures.

The important principle is:

> **Do not assume the filesystem is always in the state your script expects.**

---

# 2. A Systematic Troubleshooting Approach

When file handling fails, troubleshoot in a fixed sequence:

```text
1. What path is the script using?
          ↓
2. Does the path exist?
          ↓
3. Is it a file or directory?
          ↓
4. Can the process access it?
          ↓
5. Is the file content valid?
          ↓
6. Is the encoding correct?
          ↓
7. Is the file format correct?
          ↓
8. Did the file change during processing?
          ↓
9. Is the file too large for the chosen approach?
````

This prevents random debugging.

---

# 3. FileNotFoundError

One of the most common errors is:

```python
FileNotFoundError
```

Example:

```python
from pathlib import Path

path = Path("results.txt")

with path.open("r", encoding="utf-8") as file:
    data = file.read()
```

If the file does not exist:

```text
FileNotFoundError
```

## Troubleshooting

First check:

```python
print(path)
print(path.exists())
```

Then:

```python
print(path.resolve())
```

This helps determine the actual path Python is using.

---

# 4. Relative Path Problems

Consider:

```python
path = Path("results/test_results.txt")
```

This is a relative path.

Its meaning depends on the current working directory.

Check it:

```python
from pathlib import Path

print(Path.cwd())
```

If the script is executed from a different directory, the same relative path may point somewhere else.

## Better troubleshooting

```python
path = Path("results/test_results.txt")

print("Path:", path)
print("Absolute path:", path.resolve())
print("Exists:", path.exists())
```

This immediately gives useful diagnostic information.

---

# 5. File vs Directory Confusion

Suppose:

```python
path = Path("results")
```

and `results` is actually a directory.

Trying to read it as a normal file can fail.

Check:

```python
if path.is_file():
    print("Path is a file")

elif path.is_dir():
    print("Path is a directory")
```

This distinction is important.

```text
Path
 ├── file
 └── directory
```

A path existing does not mean it is the type your program expects.

---

# 6. Permission Errors

A file may exist but still be inaccessible.

Example:

```python
with path.open("r", encoding="utf-8") as file:
    ...
```

The operating system may deny access.

Python can raise:

```python
PermissionError
```

Example handling:

```python
try:
    with path.open("r", encoding="utf-8") as file:
        data = file.read()

except PermissionError:
    print(f"Permission denied: {path}")
```

## Troubleshooting questions

Check:

* File permissions
* Directory permissions
* User executing the script
* Ownership
* Whether another security mechanism is blocking access

On Linux, filesystem troubleshooting may also involve commands such as:

```bash
ls -l
```

and:

```bash
ls -ld <directory>
```

---

# 7. Empty Files

A file can exist and still contain no useful data.

Example:

```python
with path.open("r", encoding="utf-8") as file:
    data = file.read()
```

Result:

```python
data == ""
```

For configuration files, an empty file may be an error.

Example:

```python
if not data.strip():
    raise ValueError("File is empty")
```

For log files, however, an empty file may be perfectly valid.

Therefore:

> **Whether an empty file is an error depends on the purpose of the file.**

---

# 8. Malformed Data

A file can exist and be readable but contain invalid data.

Example:

```text
TEST_001 PASS
TEST_002
TEST_003 FAIL
```

This code:

```python
test_id, status = line.split()
```

can fail because the second line contains only one field.

Possible exception:

```python
ValueError
```

A robust parser should validate the record.

Example:

```python
parts = line.split()

if len(parts) != 2:
    raise ValueError(f"Invalid record: {line}")

test_id, status = parts
```

---

# 9. Unexpected Values

Even correctly structured data may contain invalid values.

Example:

```text
TEST_001 PASS
TEST_002 UNKNOWN
TEST_003 FAIL
```

The structure is correct, but:

```text
UNKNOWN
```

may not be an accepted status.

Validate:

```python
valid_statuses = {"PASS", "FAIL"}

if status not in valid_statuses:
    raise ValueError(
        f"Invalid status for {test_id}: {status}"
    )
```

This is an important distinction:

```text
Parsing
  ↓
Is the structure correct?

Validation
  ↓
Is the data acceptable?
```

---

# 10. Invalid JSON

Consider:

```json
{
    "device": "/dev/nvme0n1",
    "timeout": 60,
}
```

The trailing comma makes this invalid JSON.

Python:

```python
import json

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
```

can raise:

```python
json.JSONDecodeError
```

Handle it explicitly:

```python
try:
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

except json.JSONDecodeError as error:
    print(f"Invalid JSON: {error}")
```

---

# 11. Invalid YAML

Malformed YAML can raise:

```python
yaml.YAMLError
```

Example:

```python
import yaml

try:
    with open("config.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

except yaml.YAMLError as error:
    print(f"Invalid YAML: {error}")
```

The important point is that:

```text
File exists
     ≠
File content is valid
```

---

# 12. Missing Configuration Keys

Suppose:

```yaml
execution:
  timeout: 60
```

but the program expects:

```python
config["execution"]["retries"]
```

This can produce:

```python
KeyError
```

For mandatory values:

```python
retries = config["execution"]["retries"]
```

For optional values:

```python
retries = config["execution"].get("retries", 1)
```

The correct choice depends on whether the setting is required.

---

# 13. Incorrect Data Types

Consider:

```yaml
execution:
  timeout: sixty
```

The YAML may parse successfully.

But the automation expects:

```text
timeout → integer
```

Validate:

```python
timeout = config["execution"]["timeout"]

if not isinstance(timeout, int):
    raise ValueError("timeout must be an integer")
```

This illustrates an important principle:

> **Parsing validates syntax; application validation validates meaning.**

---

# 14. Encoding Problems

Files can use different encodings.

A script may assume:

```python
encoding="utf-8"
```

but the actual file may use another encoding.

This can result in:

```python
UnicodeDecodeError
```

Example:

```python
try:
    with open("results.txt", "r", encoding="utf-8") as file:
        data = file.read()

except UnicodeDecodeError:
    print("Unable to decode file as UTF-8")
```

For automation, explicitly specifying encoding is generally better than relying on platform defaults.

---

# 15. Newline Problems

Text files may originate from different operating systems.

Common newline conventions include:

```text
Linux/macOS → \n
Windows     → \r\n
```

Python's text mode generally handles newline translation appropriately.

For CSV, use:

```python
with open(
    "results.csv",
    "r",
    newline="",
    encoding="utf-8"
) as file:
    ...
```

This is especially important when using Python's `csv` module.

---

# 16. File Modified During Processing

A file may change while the automation is reading it.

Example:

```text
Automation
    ↓
opens log
    ↓
another process writes new entries
    ↓
automation continues reading
```

This can produce inconsistent results depending on the application.

Possible approaches include:

* Process only a stable snapshot
* Coordinate with the producer
* Record file metadata
* Use application-specific synchronization
* Re-read or verify when necessary

The correct approach depends on the system.

---

# 17. File Deleted During Processing

A file may exist when discovered but disappear before it is opened.

Example:

```text
Directory scan
      ↓
file found
      ↓
another process deletes file
      ↓
open() fails
```

Therefore:

```python
path.exists()
```

followed later by:

```python
path.open()
```

does not guarantee success.

The filesystem can change between those operations.

This is an important real-world race condition.

---

# 18. TOCTOU Problem

The previous situation is an example of:

> **Time-of-check to time-of-use (TOCTOU)**

Example:

```python
if path.exists():
    with path.open("r", encoding="utf-8") as file:
        ...
```

The check and use are separate operations.

The file could disappear between them.

Therefore, for many operations, it is better to perform the operation directly and handle the exception.

Example:

```python
try:
    with path.open("r", encoding="utf-8") as file:
        data = file.read()

except FileNotFoundError:
    print("File disappeared before it could be opened.")
```

Use existence checks when they provide useful information, but do not treat them as a guarantee.

---

# 19. Large File Problems

This approach:

```python
data = file.read()
```

may be inappropriate for a very large log.

It can consume significant memory.

Prefer:

```python
with path.open("r", encoding="utf-8") as file:
    for line in file:
        process(line)
```

For binary data, use chunks:

```python
with path.open("rb") as file:
    while chunk := file.read(1024 * 1024):
        process(chunk)
```

This allows processing without loading the entire file into memory.

---

# 20. Very Large Directory Trees

This:

```python
for path in root.rglob("*"):
    ...
```

can discover a very large number of files.

Potential issues include:

* Processing time
* Memory if results are collected
* Permission errors
* Broken links or unusual filesystem entries
* Unexpected directories

Prefer targeted patterns when possible:

```python
for path in root.rglob("*.log"):
    process(path)
```

Filtering early reduces unnecessary work.

---

# 21. Symlinks and Special Files

Not every filesystem entry is a normal regular file.

A path may refer to:

* Regular file
* Directory
* Symbolic link
* Device
* Socket
* Other filesystem object

Basic checks:

```python
path.is_file()
path.is_dir()
```

For automation operating on system files, it is important to understand what type of filesystem object is actually being accessed.

---

# 22. Safe Deletion

Avoid blindly deleting files.

Dangerous pattern:

```python
path.unlink()
```

without understanding what `path` refers to.

A safer workflow:

```python
if path.exists() and path.is_file():
    path.unlink()
```

But remember the TOCTOU limitation: the filesystem can change.

For important artifacts, consider:

```text
Verify
 ↓
Preserve
 ↓
Delete only when appropriate
```

---

# 23. Safe File Moves

Moving files can fail because of:

* Missing source
* Invalid destination
* Permission problems
* Existing destination
* Filesystem restrictions

Example:

```python
import shutil

try:
    shutil.move(source, destination)

except FileNotFoundError:
    print("Source file not found.")

except PermissionError:
    print("Permission denied.")
```

For test artifacts, verify the result after important operations.

---

# 24. Partial Writes

Automation may terminate while writing a file.

Example:

```text
Automation starts writing report
        ↓
System/process failure
        ↓
Report is incomplete
```

This can leave a partially written artifact.

For critical output, a safer pattern can be:

```text
Write temporary file
        ↓
Complete successfully
        ↓
Rename to final filename
```

Example conceptually:

```python
temporary = Path("report.tmp")
final = Path("report.txt")

with temporary.open("w", encoding="utf-8") as file:
    file.write(report)

temporary.replace(final)
```

The exact strategy should depend on the importance and concurrency requirements of the output.

---

# 25. Unexpected File Extensions

Do not always assume an extension guarantees content type.

For example:

```text
results.json
```

could contain invalid JSON.

Likewise:

```text
config.yaml
```

could contain invalid YAML.

Therefore:

```text
Extension
   ↓
Helpful hint

Content parsing
   ↓
Actual validation
```

The parser should determine whether the content is valid for the expected format.

---

# 26. Missing Parent Directories

Suppose:

```python
report_path = Path("results/run_001/report.txt")
```

but the directory does not exist.

Opening the file for writing can fail.

Create the directory first:

```python
report_path.parent.mkdir(
    parents=True,
    exist_ok=True
)
```

Then:

```python
with report_path.open("w", encoding="utf-8") as file:
    file.write("Report")
```

This is a common automation pattern.

---

# 27. Disk Space Problems

File writing can fail when the filesystem has insufficient free space.

For large test artifacts, this can become significant.

Potential symptoms:

```text
Write operation fails
Report incomplete
Log truncated
Test artifact missing
```

When troubleshooting large output failures, check:

* Available disk space
* Filesystem capacity
* Output directory
* Artifact size
* Cleanup policies

On Linux:

```bash
df -h
```

is commonly used to inspect filesystem capacity.

---

# 28. File Locking and Concurrent Access

Multiple processes may attempt to access the same file.

Example:

```text
Process A ──→ writes results.csv
                    ↑
Process B ─────────┘
```

Potential problems include:

* Corrupted output
* Interleaved writes
* Incomplete data
* Access failures
* Race conditions

Possible solutions depend on the application:

* Separate output files
* File locking
* Process synchronization
* Temporary files
* Atomic replacement
* Centralized result collection

Do not assume concurrent file access is automatically safe.

---

# 29. Troubleshooting Checklist

When a file operation fails, use this checklist:

```text
[ ] Confirm the path
[ ] Print/inspect the resolved path
[ ] Check existence
[ ] Check file vs directory
[ ] Check permissions
[ ] Check ownership
[ ] Check encoding
[ ] Check file contents
[ ] Check expected format
[ ] Validate parsed data
[ ] Check file size
[ ] Check disk space
[ ] Check concurrent access
[ ] Check whether another process modified/deleted it
[ ] Preserve diagnostic artifacts
```

This provides a repeatable troubleshooting methodology.

---

# 30. Practical Storage Automation Example

Imagine a storage test framework produces:

```text
run_001/
├── config.yaml
├── test_results.csv
├── kernel.log
└── report.txt
```

The automation expects:

```text
config.yaml
test_results.csv
```

A robust workflow could be:

```text
Start
  ↓
Check configuration path
  ↓
Load YAML
  ↓
Validate configuration
  ↓
Check result file
  ↓
Read CSV
  ↓
Validate records
  ↓
Analyze failures
  ↓
Generate report
  ↓
Preserve logs
```

If something fails:

```text
Failure
   ↓
Identify stage
   ↓
Identify exception
   ↓
Inspect filesystem state
   ↓
Inspect input
   ↓
Determine root cause
   ↓
Report meaningful failure
```

---

# 31. Root Cause vs Symptom

This distinction is critical.

Suppose the script reports:

```text
Failed to read results.csv
```

That is a symptom.

The root cause might be:

```text
results.csv does not exist
```

or:

```text
Permission denied
```

or:

```text
results.csv is actually a directory
```

or:

```text
Filesystem is full
```

or:

```text
The producer never generated the file
```

Good troubleshooting asks:

> **Why did the expected condition not occur?**

rather than stopping at the first error message.

---

# 32. Good Error Messages

Weak:

```python
print("Error")
```

Better:

```python
print(f"Failed to read results file: {path}")
```

Even better:

```python
try:
    with path.open("r", encoding="utf-8") as file:
        data = file.read()

except FileNotFoundError:
    print(f"Results file not found: {path.resolve()}")

except PermissionError:
    print(f"Permission denied: {path.resolve()}")
```

A useful error message should tell the engineer:

```text
What failed?
Where did it fail?
Why did it fail?
```

when that information is available.

---

# 33. Exception Handling Strategy

A useful hierarchy is:

```text
Expected operational failure
        ↓
Handle specifically

Unexpected programming failure
        ↓
Do not silently hide it
```

Avoid:

```python
try:
    ...
except Exception:
    pass
```

This can hide serious bugs.

Instead:

```python
try:
    ...
except FileNotFoundError:
    ...
except PermissionError:
    ...
```

and allow unexpected exceptions to surface during development unless there is a deliberate framework-level strategy for handling them.

---

# 34. Preserve Evidence

When automation fails, the files generated before the failure may be extremely valuable.

For example:

```text
run_001/
├── config.yaml
├── kernel.log
├── command_output.txt
├── partial_results.csv
└── failure_report.txt
```

Do not automatically delete everything after failure.

The artifacts may allow an engineer to determine:

* What configuration was used
* What test ran
* Where execution stopped
* What the operating system reported
* What the device reported
* What result had been collected

This is particularly important in storage validation.

---

# 35. Industry Troubleshooting Pattern

A useful storage automation troubleshooting model is:

```text
                FAILURE
                   |
                   ↓
             Identify Stage
                   |
          +--------+--------+
          |        |        |
        Input    Parse    Output
          |        |        |
          ↓        ↓        ↓
       Path?    Format?   Disk?
       Exists?  Syntax?   Permission?
       Access?  Type?     Space?
          |        |        |
          +--------+--------+
                   |
                   ↓
              Root Cause
                   |
                   ↓
              Evidence
                   |
                   ↓
             Final Report
```

The automation should make the investigation easier, not harder.

---

# 36. Interview Questions

## Basic

**1. What is the first thing you check when a file cannot be opened?**

Verify the path and filesystem state.

**2. What is `FileNotFoundError`?**

An exception raised when the requested file or path cannot be found.

**3. What is `PermissionError`?**

An exception raised when the process does not have the required permission for an operation.

**4. How do you determine whether a path is a file or directory?**

Use:

```python
path.is_file()
path.is_dir()
```

---

## Intermediate

**5. Does `Path.exists()` guarantee that a later file operation will succeed?**

No. The filesystem can change between the check and the operation.

**6. What is TOCTOU?**

Time-of-check to time-of-use: the state of a resource can change between checking it and using it.

**7. Why shouldn't huge files always be read using `read()`?**

Because the entire file is loaded into memory.

**8. What is the difference between parsing and validation?**

Parsing determines whether the input can be converted into a structured representation.

Validation determines whether the resulting data satisfies application requirements.

**9. What exception can invalid JSON produce?**

```python
json.JSONDecodeError
```

**10. What exception can malformed YAML produce?**

```python
yaml.YAMLError
```

---

## Storage Automation

**11. Why is preserving artifacts important when a storage test fails?**

Artifacts provide evidence needed for troubleshooting and root-cause analysis.

**12. What filesystem problems can affect storage test automation?**

Examples:

```text
Missing files
Permission problems
Disk-full conditions
Concurrent access
Partial writes
File deletion
File modification
Incorrect paths
Incorrect file types
```

**13. Why are good error messages important?**

They reduce troubleshooting time by identifying the failed operation, affected path, and available failure details.

**14. What should an automation engineer distinguish between?**

```text
Symptom
   vs
Root Cause
```

---

# 37. Key Takeaways

Remember:

```text
File exists
    ≠
File is usable

File is readable
    ≠
File content is valid

File content is valid
    ≠
Configuration is correct
```

A robust file-processing system performs:

```text
Path Validation
      ↓
Access
      ↓
Parsing
      ↓
Validation
      ↓
Processing
      ↓
Output Verification
      ↓
Artifact Preservation
```

For troubleshooting:

```text
Failure
 ↓
Identify stage
 ↓
Inspect state
 ↓
Inspect exception
 ↓
Determine root cause
 ↓
Preserve evidence
 ↓
Report clearly
```

---

# Automation Principle

> **Never troubleshoot only the exception message. Troubleshoot the entire chain of assumptions that led to the failure.**

For Storage Test Automation, this mindset is essential because the filesystem, operating system, storage device, test framework, and automation script can all contribute to the final failure.

```

**Next:** `20_Interview_Questions.md`
```

