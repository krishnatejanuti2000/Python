# `10_Directory_Traversal.md`

# Directory Traversal

## 1. Introduction

Directory traversal means **examining the contents of a directory and discovering files and subdirectories inside it**.

In storage test automation, this is extremely important.

A test framework may need to:

* Find all log files
* Find all test-result files
* Search nested directories
* Process every `.log` file
* Locate configuration files
* Count generated reports
* Find failed-test artifacts
* Process files across multiple devices or test runs

Python's `pathlib` provides simple and readable tools for this.

The two most important approaches are:

```python
Path.iterdir()
```

and:

```python
Path.rglob()
```

---

# 2. Directory Traversal Concept

Consider:

```text
storage_tests/
├── logs/
│   ├── device1.log
│   └── device2.log
├── results/
│   ├── test1.txt
│   └── test2.txt
└── reports/
    └── summary.txt
```

Traversal means starting at:

```text
storage_tests/
```

and examining what exists underneath it.

A traversal operation may return:

```text
logs
results
reports
```

and potentially continue into:

```text
logs/device1.log
logs/device2.log
results/test1.txt
...
```

depending on the traversal method used.

---

# 3. `Path.iterdir()`

`iterdir()` returns the **direct children** of a directory.

Syntax:

```python
path.iterdir()
```

Example:

```python
from pathlib import Path

directory = Path("storage_tests")

for item in directory.iterdir():
    print(item)
```

If the directory contains:

```text
storage_tests/
├── logs/
├── results/
└── report.txt
```

the output may be:

```text
storage_tests/logs
storage_tests/results
storage_tests/report.txt
```

---

# 4. `iterdir()` Does Not Traverse Recursively

This is one of the most important points.

Suppose:

```text
storage_tests/
├── logs/
│   ├── device1.log
│   └── device2.log
├── results/
│   └── test.txt
└── report.txt
```

Running:

```python
for item in Path("storage_tests").iterdir():
    print(item)
```

only examines:

```text
logs/
results/
report.txt
```

It does **not** automatically enter `logs/` or `results/`.

So:

```text
storage_tests/
    ↓
logs/
results/
report.txt
```

Only one level is examined.

---

# 5. Checking What Each Entry Is

Because `iterdir()` can return both files and directories, use:

```python
item.is_file()
```

and:

```python
item.is_dir()
```

Example:

```python
from pathlib import Path

directory = Path("storage_tests")

for item in directory.iterdir():

    if item.is_file():
        print("FILE:", item)

    elif item.is_dir():
        print("DIR :", item)
```

Possible output:

```text
DIR : storage_tests/logs
DIR : storage_tests/results
FILE: storage_tests/report.txt
```

---

# 6. Listing Only Files

Example:

```python
from pathlib import Path

directory = Path("storage_tests")

for item in directory.iterdir():
    if item.is_file():
        print(item)
```

This ignores directories.

---

# 7. Listing Only Directories

Example:

```python
from pathlib import Path

directory = Path("storage_tests")

for item in directory.iterdir():
    if item.is_dir():
        print(item)
```

This ignores files.

---

# 8. Using `rglob()`

When we need **recursive traversal**, `rglob()` is extremely useful.

Syntax:

```python
path.rglob(pattern)
```

Example:

```python
from pathlib import Path

directory = Path("storage_tests")

for file in directory.rglob("*"):
    print(file)
```

This recursively examines the directory tree.

---

# 9. `rglob("*")`

Consider:

```text
storage_tests/
├── logs/
│   ├── device1.log
│   └── device2.log
├── results/
│   └── test.txt
└── report.txt
```

Code:

```python
from pathlib import Path

for item in Path("storage_tests").rglob("*"):
    print(item)
```

It can discover entries throughout the tree:

```text
storage_tests/logs
storage_tests/logs/device1.log
storage_tests/logs/device2.log
storage_tests/results
storage_tests/results/test.txt
storage_tests/report.txt
```

The exact ordering should not be relied upon.

---

# 10. Recursive Search for Specific File Types

One of the most useful patterns:

```python
for file in directory.rglob("*.log"):
    print(file)
```

This means:

> Recursively find entries matching `*.log`.

Example tree:

```text
storage_tests/
├── logs/
│   ├── device1.log
│   └── device2.log
├── old/
│   └── old.log
└── results/
    └── result.txt
```

Code:

```python
from pathlib import Path

directory = Path("storage_tests")

for file in directory.rglob("*.log"):
    print(file)
```

Output:

```text
storage_tests/logs/device1.log
storage_tests/logs/device2.log
storage_tests/old/old.log
```

---

# 11. `glob()` vs `rglob()`

`pathlib` provides both:

```python
Path.glob()
```

and:

```python
Path.rglob()
```

### `glob()`

Searches according to the pattern within the path's directory hierarchy as specified by the pattern.

Example:

```python
directory.glob("*.log")
```

This commonly means matching `.log` files directly under that directory.

### `rglob()`

Provides recursive searching.

```python
directory.rglob("*.log")
```

This searches nested directories as well.

For automation, remember:

```text
glob  → pattern-based directory search
rglob → recursive pattern-based search
```

---

# 12. Why `rglob("*.log")` Is Useful in Storage Automation

Storage validation can generate large directory trees:

```text
test_runs/
├── run_001/
│   ├── logs/
│   │   ├── controller.log
│   │   └── kernel.log
│   └── results/
├── run_002/
│   ├── logs/
│   │   └── controller.log
│   └── results/
└── run_003/
    └── logs/
        └── kernel.log
```

A script can find every log:

```python
from pathlib import Path

root = Path("test_runs")

for log_file in root.rglob("*.log"):
    print(log_file)
```

No need to manually know how deeply nested the files are.

---

# 13. Finding All Test Result Files

Suppose result files use:

```text
*.result
```

Use:

```python
from pathlib import Path

root = Path("test_runs")

for result_file in root.rglob("*.result"):
    print(result_file)
```

This can be used to collect results from multiple test runs.

---

# 14. Finding Multiple File Types

You can search for different extensions separately:

```python
from pathlib import Path

root = Path("test_runs")

for log_file in root.rglob("*.log"):
    print("LOG:", log_file)

for result_file in root.rglob("*.result"):
    print("RESULT:", result_file)
```

If more control is required, inspect the suffix:

```python
for item in root.rglob("*"):

    if item.is_file():

        if item.suffix == ".log":
            print("LOG:", item)

        elif item.suffix == ".result":
            print("RESULT:", item)
```

---

# 15. `Path.suffix`

A `Path` object provides:

```python
path.suffix
```

Example:

```python
from pathlib import Path

path = Path("controller.log")

print(path.suffix)
```

Output:

```text
.log
```

Another example:

```python
path = Path("test_result.txt")

print(path.suffix)
```

Output:

```text
.txt
```

This is useful when classification needs to happen after traversal.

---

# 16. Finding Files and Processing Them

Traversal becomes much more useful when combined with file handling.

Example:

```python
from pathlib import Path

root = Path("test_runs")

for log_file in root.rglob("*.log"):

    with log_file.open("r", encoding="utf-8") as file:
        for line in file:
            if "ERROR" in line:
                print(log_file, line.strip())
```

The automation:

1. Searches recursively.
2. Finds `.log` files.
3. Opens each file.
4. Reads it line-by-line.
5. Searches for `ERROR`.
6. Reports matching lines.

This is a realistic storage troubleshooting pattern.

---

# 17. Counting Files

Example:

```python
from pathlib import Path

root = Path("test_runs")

count = 0

for file in root.rglob("*.log"):
    if file.is_file():
        count += 1

print("Log files:", count)
```

This determines how many log files exist in the directory tree.

---

# 18. Collecting Paths into a List

Sometimes the automation needs to process the discovered files later.

```python
from pathlib import Path

root = Path("test_runs")

log_files = []

for file in root.rglob("*.log"):
    if file.is_file():
        log_files.append(file)

print(log_files)
```

Or, more compactly:

```python
log_files = [
    file
    for file in root.rglob("*.log")
    if file.is_file()
]
```

Both are valid.

For learning and debugging, the explicit loop is often easier to understand.

---

# 19. Directory Traversal with `iterdir()`

Use `iterdir()` when you care about the **immediate contents**.

Example:

```python
from pathlib import Path

root = Path("test_runs")

for item in root.iterdir():
    print(item)
```

Useful for:

* Checking directory structure
* Listing immediate test-run folders
* Validating expected directories
* Inspecting a single directory level

---

# 20. Recursive Traversal with `rglob()`

Use `rglob()` when you need to search **through nested directories**.

Example:

```python
from pathlib import Path

root = Path("test_runs")

for item in root.rglob("*.log"):
    print(item)
```

Useful for:

* Finding logs
* Finding reports
* Finding test results
* Searching artifacts
* Collecting files from multiple test runs

---

# 21. Handling a Missing Directory

Before traversal, consider whether the directory exists.

```python
from pathlib import Path

root = Path("test_runs")

if not root.is_dir():
    raise RuntimeError(
        f"Directory does not exist: {root}"
    )

for file in root.rglob("*.log"):
    print(file)
```

This produces a clearer failure than allowing the problem to propagate unnoticed.

---

# 22. Empty Directory

A directory may exist but contain nothing.

Example:

```python
root = Path("empty_directory")

for item in root.iterdir():
    print(item)
```

If the directory is empty, the loop simply has no iterations.

This is not necessarily an error.

Automation should distinguish:

```text
Directory missing
```

from:

```text
Directory exists but is empty
```

These can have very different meanings.

---

# 23. No Matching Files

Suppose:

```python
for file in root.rglob("*.log"):
    print(file)
```

and there are no `.log` files.

The loop simply produces no output.

That is not automatically an exception.

If logs are mandatory for a test, the automation should explicitly validate that expectation.

Example:

```python
log_files = list(root.rglob("*.log"))

if not log_files:
    raise RuntimeError("No log files found")
```

---

# 24. Traversal + Validation

A useful automation pattern:

```python
from pathlib import Path

root = Path("test_runs")

if not root.is_dir():
    raise RuntimeError(
        f"Test-run directory missing: {root}"
    )

log_files = [
    file
    for file in root.rglob("*.log")
    if file.is_file()
]

if not log_files:
    raise RuntimeError(
        "No log files found"
    )

print(f"Found {len(log_files)} log files")
```

This combines:

```text
Validate
   ↓
Traverse
   ↓
Collect
   ↓
Validate result
```

---

# 25. Traversal and Large Directory Trees

Recursive traversal can potentially encounter many files.

For example:

```text
test_runs/
├── run_001/
├── run_002/
├── run_003/
...
└── run_10000/
```

Avoid unnecessarily creating huge lists if you can process entries directly.

Instead of:

```python
files = list(root.rglob("*.log"))

for file in files:
    process(file)
```

you can often do:

```python
for file in root.rglob("*.log"):
    process(file)
```

This allows processing as entries are produced rather than explicitly constructing a list of every matching path first.

---

# 26. Traversal + Large File Processing

We can combine two important concepts learned earlier:

```text
Directory traversal
        +
Large-file processing
```

Example:

```python
from pathlib import Path

root = Path("test_runs")

for log_file in root.rglob("*.log"):

    with log_file.open("r", encoding="utf-8") as file:

        for line in file:
            if "FAIL" in line:
                print(log_file, line.strip())
```

This is much more scalable than loading every log file completely into memory.

---

# 27. Practical Storage Automation Example

Imagine:

```text
storage_validation/
├── device_01/
│   └── logs/
│       ├── controller.log
│       └── kernel.log
├── device_02/
│   └── logs/
│       └── controller.log
└── device_03/
    └── logs/
        └── kernel.log
```

We want to find all logs containing:

```text
ERROR
```

Code:

```python
from pathlib import Path

root = Path("storage_validation")

for log_file in root.rglob("*.log"):

    with log_file.open("r", encoding="utf-8") as file:

        for line in file:
            if "ERROR" in line:
                print(
                    f"{log_file}: {line.strip()}"
                )
```

This pattern is directly applicable to storage test troubleshooting.

---

# 28. Traversal Does Not Mean Reading

An important distinction:

```python
for file in root.rglob("*.log"):
```

discovers paths.

It does **not** read the contents of those files.

Reading happens separately:

```python
with file.open("r", encoding="utf-8") as f:
    ...
```

Think of the process as:

```text
Filesystem
    ↓
Traversal
    ↓
Path discovered
    ↓
File opened
    ↓
Content processed
```

This separation makes automation code easier to reason about.

---

# 29. Common Mistake — Expecting `iterdir()` to Be Recursive

Incorrect assumption:

```python
for file in root.iterdir():
    ...
```

will find every file underneath the entire tree.

It does not.

For recursive searching, use:

```python
root.rglob("*")
```

or a specific pattern such as:

```python
root.rglob("*.log")
```

---

# 30. Common Mistake — Forgetting to Check File Type

This:

```python
for item in root.rglob("*"):
    with item.open("r") as file:
        ...
```

can fail because `rglob("*")` can return directories as well.

Safer:

```python
for item in root.rglob("*"):

    if item.is_file():
        with item.open("r", encoding="utf-8") as file:
            ...
```

Or, if you specifically want log files:

```python
for item in root.rglob("*.log"):

    if item.is_file():
        ...
```

---

# 31. Common Mistake — Treating "No Results" as an Exception

This:

```python
for file in root.rglob("*.log"):
    ...
```

does not raise an error simply because no files match.

If the automation requires at least one result, explicitly check:

```python
log_files = list(root.rglob("*.log"))

if not log_files:
    raise RuntimeError("No log files found")
```

The expected behavior must be defined by the test requirements.

---

# 32. `iterdir()` vs `rglob()`

| Feature                       | `iterdir()` | `rglob()` |
| ----------------------------- | ----------- | --------- |
| Lists directory contents      | Yes         | Yes       |
| Direct children               | Yes         | Yes       |
| Recursive                     | No          | Yes       |
| Pattern matching              | No          | Yes       |
| Find `.log` files recursively | No          | Yes       |
| Simple directory inspection   | Excellent   | Possible  |
| Deep filesystem search        | No          | Excellent |

The key distinction:

```text
iterdir()
    → immediate children

rglob()
    → recursive pattern-based search
```

---

# 33. Interview Questions

### Q1. What does `Path.iterdir()` do?

It returns the entries immediately contained in a directory.

---

### Q2. Is `iterdir()` recursive?

No.

It only examines the directory's direct children.

---

### Q3. How do you recursively find all `.log` files?

```python
for file in Path("logs").rglob("*.log"):
    print(file)
```

---

### Q4. What is the difference between `glob()` and `rglob()`?

`glob()` performs pattern-based matching according to the specified path pattern, while `rglob()` provides recursive pattern-based searching through descendant directories.

---

### Q5. Does `rglob()` read file contents?

No.

It discovers matching filesystem paths.

---

### Q6. How do you ensure a discovered path is a file?

```python
if path.is_file():
    ...
```

---

### Q7. What happens if no files match an `rglob()` pattern?

The iteration produces no entries; it does not automatically raise an exception.

---

### Q8. Why is directory traversal important in storage automation?

Because storage test environments can generate large and deeply nested collections of:

* Logs
* Results
* Reports
* Dumps
* Configuration files
* Test artifacts

Traversal allows automation to discover and process these files without hard-coding every path.

---

# 34. Key Takeaways

The most important patterns from this topic are:

### Direct directory contents

```python
from pathlib import Path

for item in Path("logs").iterdir():
    print(item)
```

### Only files

```python
for item in Path("logs").iterdir():
    if item.is_file():
        print(item)
```

### Recursive search

```python
for item in Path("logs").rglob("*"):
    print(item)
```

### Recursive `.log` search

```python
for log_file in Path("logs").rglob("*.log"):
    print(log_file)
```

### Recursive processing

```python
for log_file in Path("logs").rglob("*.log"):

    if log_file.is_file():

        with log_file.open("r", encoding="utf-8") as file:
            for line in file:
                if "ERROR" in line:
                    print(log_file, line.strip())
```

---

# 35. Automation Principle

> **Separate filesystem discovery from file processing.**

A strong automation design looks like:

```text
Validate root directory
        ↓
Traverse directory tree
        ↓
Discover relevant files
        ↓
Validate discovered files
        ↓
Open files
        ↓
Process contents
        ↓
Generate results
```

This separation becomes extremely powerful when building storage validation tools.

The next topic builds on this directly: **performing file operations such as rename, delete, copy, and move.**

**Next file:** `11_File_Operations.md`

