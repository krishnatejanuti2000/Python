# BLOCK 1.3 — PATTERN-BASED FILE HANDLING

## Purpose

Pattern-based file handling is used when automation needs to **discover or filter files based on filename patterns**.

In Storage Test Automation, this is useful for:

* Finding log files
* Filtering test artifacts
* Recursive file discovery
* Selecting files relevant to diagnostics and validation

The master syllabus defines this section around:

* `glob`
* `fnmatch`
* Finding log files
* Filtering test artifacts
* Recursive file discovery

---

# 1. `glob`

## What is `glob`?

`glob` is used to **find filesystem paths that match a specified pattern**.

```python
import glob
```

Example:

```python
files = glob.glob("run_001/logs/*.log")

print(files)
```

Suppose:

```text
run_001/
└── logs/
    ├── nvme_health.log
    ├── dmesg.log
    ├── fio.log
    └── notes.txt
```

The pattern:

```text
*.log
```

matches the `.log` files.

Possible result:

```python
[
    "run_001/logs/nvme_health.log",
    "run_001/logs/dmesg.log",
    "run_001/logs/fio.log"
]
```

`notes.txt` is not returned because it does not match the pattern.

---

# 2. Understanding `*`

The `*` wildcard means:

> Match any sequence of characters.

For:

```text
*.log
```

think:

```text
anything + .log
```

Therefore:

```text
nvme.log
dmesg.log
fio.log
automation.log
```

can match.

But:

```text
result.json
notes.txt
```

do not match.

---

# 3. `glob.glob()` Returns Matching Paths

Example:

```python
import glob

log_files = glob.glob("run_001/logs/*.log")

for file_path in log_files:
    print(file_path)
```

The result is a list of matching filesystem paths.

Mental model:

```text
Pattern
   ↓
glob
   ↓
Matching paths
   ↓
List
   ↓
Process each file
```

---

# 4. Recursive File Discovery

Consider:

```text
run_001/
├── logs/
│   ├── nvme.log
│   └── dmesg.log
├── diagnostics/
│   └── nvme_error.log
└── performance/
    └── fio.log
```

This:

```python
glob.glob("run_001/*.log")
```

looks for matching files directly under `run_001`.

It does not mean that every nested directory will automatically be searched.

For recursive discovery:

```python
glob.glob(
    "run_001/**/*.log",
    recursive=True
)
```

`**` allows recursive matching when `recursive=True` is used.

This can discover:

```text
run_001/logs/nvme.log
run_001/logs/dmesg.log
run_001/diagnostics/nvme_error.log
run_001/performance/fio.log
```

---

# 5. Useful Patterns

## All log files

```text
*.log
```

Matches files ending in `.log`.

---

## NVMe log files

```text
nvme_*.log
```

Matches names beginning with `nvme_` and ending with `.log`.

Examples:

```text
nvme_health.log
nvme_error.log
nvme_reset.log
```

---

## JSON files

```text
*.json
```

Matches JSON artifacts.

---

## Recursive log discovery

```text
**/*.log
```

with:

```python
recursive=True
```

allows recursive discovery.

---

# 6. `?` Wildcard

`?` represents **one character**.

Example:

```text
test?.log
```

can match:

```text
test1.log
test2.log
testA.log
```

but not:

```text
test10.log
```

because `10` contains two characters.

---

# 7. Character Classes `[ ]`

A pattern can select characters using `[ ]`.

Example:

```text
test[12].log
```

can match:

```text
test1.log
test2.log
```

but not:

```text
test3.log
```

These pattern rules are useful when filenames follow a predictable naming convention.

---

# 8. Storage Automation Example — Finding Logs

Suppose an NVMe validation run creates:

```text
run_001/
├── logs/
│   ├── automation.log
│   ├── nvme_health.log
│   └── dmesg.log
├── diagnostics/
│   └── nvme_error.log
└── results/
    └── result.json
```

To find all logs recursively:

```python
import glob

logs = glob.glob(
    "run_001/**/*.log",
    recursive=True
)

for log_file in logs:
    print(log_file)
```

The discovered files can then be passed to other automation components:

```text
Find logs
   ↓
Read logs
   ↓
Parse logs
   ↓
Search for errors
   ↓
Validate
   ↓
Preserve evidence
```

---

# 9. `fnmatch`

## What is `fnmatch`?

`fnmatch` is used to determine whether an **already available filename matches a pattern**.

```python
import fnmatch
```

Example:

```python
print(
    fnmatch.fnmatch(
        "nvme_health.log",
        "*.log"
    )
)
```

Result:

```text
True
```

Another example:

```python
print(
    fnmatch.fnmatch(
        "result.json",
        "*.log"
    )
)
```

Result:

```text
False
```

---

# 10. `glob` vs `fnmatch`

This is one of the most important distinctions in this section.

## `glob`

```python
glob.glob("run_001/logs/*.log")
```

asks:

> **Which filesystem paths match this pattern?**

It performs discovery.

---

## `fnmatch`

```python
fnmatch.fnmatch(
    "nvme_health.log",
    "*.log"
)
```

asks:

> **Does this particular filename match this pattern?**

It performs pattern matching.

Therefore:

```text
glob
 ↓
Discovery

fnmatch
 ↓
Matching / filtering
```

---

# 11. `os.walk()` + `fnmatch`

We already learned `os.walk()`.

Suppose:

```python
files = [
    "nvme_health.log",
    "dmesg.log",
    "result.json",
    "notes.txt"
]
```

We can filter the files:

```python
import fnmatch

for file_name in files:

    if fnmatch.fnmatch(file_name, "*.log"):
        print(file_name)
```

Result:

```text
nvme_health.log
dmesg.log
```

A complete traversal example:

```python
import os
import fnmatch

for root, directories, files in os.walk("run_001"):

    for file_name in files:

        if fnmatch.fnmatch(file_name, "*.log"):

            full_path = os.path.join(
                root,
                file_name
            )

            print(full_path)
```

The flow is:

```text
os.walk()
    ↓
Traverse filesystem
    ↓
Obtain filenames
    ↓
fnmatch
    ↓
Filter matching names
    ↓
os.path.join()
    ↓
Full path
```

---

# 12. `fnmatch.filter()`

When a list is already available, `fnmatch.filter()` can filter it directly.

Example:

```python
import fnmatch

files = [
    "nvme_health.log",
    "dmesg.log",
    "result.json",
    "notes.txt"
]

logs = fnmatch.filter(
    files,
    "*.log"
)

print(logs)
```

Result:

```python
[
    "nvme_health.log",
    "dmesg.log"
]
```

Mental model:

```text
Existing list
     ↓
fnmatch.filter()
     ↓
Matching names
```

---

# 13. Filtering Storage Artifacts

Suppose we already have:

```python
files = [
    "nvme_health.json",
    "nvme_error.json",
    "dmesg.txt",
    "lspci.txt",
    "fio_result.json",
    "notes.txt"
]
```

Requirement:

> Select NVMe JSON artifacts.

Pattern:

```text
nvme_*.json
```

Code:

```python
import fnmatch

nvme_files = fnmatch.filter(
    files,
    "nvme_*.json"
)

print(nvme_files)
```

Result:

```text
[
    "nvme_health.json",
    "nvme_error.json"
]
```

---

# 14. Matching Does Not Mean Existence

This is an important concept.

Consider:

```python
fnmatch.fnmatch(
    "does_not_exist.log",
    "*.log"
)
```

This can return:

```text
True
```

even though the file does not exist.

Why?

Because `fnmatch` only asks:

> Does this string match the pattern?

It does not ask:

> Does this file exist?

Therefore:

```text
fnmatch
    ↓
Pattern matching

os.path.exists()
    ↓
Filesystem existence
```

These are different questions.

---

# 15. Choosing the Appropriate Tool

## Use `os.walk()` when:

You need to traverse a directory tree and apply custom processing.

```text
Directory tree
      ↓
Visit directories
      ↓
Inspect files
      ↓
Apply custom logic
```

---

## Use `glob()` when:

You know the pattern you want to discover.

Example:

```python
glob.glob(
    "run_001/**/*.log",
    recursive=True
)
```

Meaning:

> Find log files recursively.

---

## Use `fnmatch()` when:

You already have a filename and need to determine whether it matches a pattern.

Example:

```python
fnmatch.fnmatch(
    file_name,
    "*.log"
)
```

---

## Use `fnmatch.filter()` when:

You already have a list of names and want only matching entries.

---

# 16. Real Storage Automation Flow

Suppose an NVMe validation test fails.

The run produces:

```text
run_001/
├── logs/
│   ├── automation.log
│   ├── nvme_health.log
│   └── dmesg.log
├── diagnostics/
│   ├── nvme_error.json
│   └── kernel.log
└── results/
    └── result.json
```

Automation can perform:

```text
Test Failure
     ↓
Discover diagnostic artifacts
     ↓
glob / os.walk()
     ↓
Filter required files
     ↓
fnmatch
     ↓
Read / Parse
     ↓
Identify relevant errors
     ↓
Preserve evidence
```

The purpose is not simply finding files.

The purpose is to make **diagnostic automation efficient and repeatable**.

---

# 17. `glob` and `pathlib`

Since `pathlib` was already learned, the same idea can also be expressed with `Path`.

Example:

```python
from pathlib import Path

run_dir = Path("run_001")

for log_file in run_dir.glob("*.log"):
    print(log_file)
```

For recursive discovery:

```python
for log_file in run_dir.rglob("*.log"):
    print(log_file)
```

These represent the same pattern-based discovery concept.

The important thing is understanding the operation, not memorizing every API variation.

---

# 18. Complete Mental Model

```text
                 FILE DISCOVERY

                 os.walk()
                     ↓
              Traverse the tree


                  glob()
                     ↓
          Find matching filesystem paths


                 fnmatch()
                     ↓
             Match a filename


             fnmatch.filter()
                     ↓
            Filter a filename list
```

Or as a storage workflow:

```text
Filesystem
    ↓
Discover
    ↓
Filter
    ↓
Process
    ↓
Validate
    ↓
Evidence
```

---

# 19. Important Patterns

```text
*.log
```

→ all log files

```text
*.json
```

→ all JSON files

```text
nvme_*.log
```

→ NVMe log files matching the naming convention

```text
**/*.log
```

with:

```python
recursive=True
```

→ recursively discover log files

```text
test?.log
```

→ `test` + one character + `.log`

```text
test[12].log
```

→ `test1.log` or `test2.log`

---

# 20. Key Engineering Principle

Do not choose a tool just because it is available.

First identify the operation:

```text
Need to discover files?
        ↓
glob

Already have filenames and need filtering?
        ↓
fnmatch

Need to traverse the tree and apply custom logic?
        ↓
os.walk()
```

The tool should match the requirement.

---

# 21. Final Summary

```text
glob
├── Pattern-based discovery
├── *
├── ?
├── [ ]
├── Recursive discovery
└── Log/artifact discovery

fnmatch
├── Pattern matching
├── fnmatch()
└── fnmatch.filter()

Integration
├── os.walk() + fnmatch
└── glob + recursive discovery
```

The core distinction is:

```text
os.walk()
    → Traverse

glob()
    → Discover by pattern

fnmatch()
    → Match/filter names
```

# BLOCK 1.3 — COMPLETED

