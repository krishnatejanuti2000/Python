# `09_Directory_Handling.md`

# Directory Handling

## 1. Introduction

In storage test automation, files rarely exist in isolation.

Test automation commonly works with directory structures such as:

```text
test_environment/
├── configs/
├── logs/
├── results/
├── reports/
├── temporary/
└── backups/
```

A Python automation script may need to:

* Create directories
* Check whether a directory exists
* Create nested directory structures
* Detect whether a path is a file or directory
* Avoid errors when a directory already exists
* Build directories dynamically
* Prepare output locations before writing files
* Organize test results and logs

Python's `pathlib` module provides a clean and modern way to perform these operations.

---

# 2. What Is a Directory?

A **directory** is a filesystem container used to organize files and other directories.

For example:

```text
/home/user/storage_tests/
```

may contain:

```text
storage_tests/
├── logs/
├── results/
├── reports/
└── configs/
```

Here:

* `storage_tests` → directory
* `logs` → directory
* `results` → directory
* `reports` → directory
* `configs` → directory

Directories can also contain other directories.

This creates a hierarchy:

```text
Parent Directory
      │
      ├── File
      ├── File
      │
      └── Child Directory
              │
              ├── File
              └── File
```

---

# 3. `pathlib.Path`

Before working with directories, create a `Path` object:

```python
from pathlib import Path

path = Path("logs")
```

The `Path` object represents the filesystem path.

It does **not** automatically create the directory.

For example:

```python
from pathlib import Path

path = Path("logs")

print(path)
```

Output:

```text
logs
```

At this point, `logs` may or may not exist.

---

# 4. Creating a Directory with `mkdir()`

The primary method for creating a directory is:

```python
Path.mkdir()
```

Example:

```python
from pathlib import Path

path = Path("logs")
path.mkdir()
```

If `logs` does not exist, Python creates it.

---

# 5. `mkdir()` and Existing Directories

Consider:

```python
from pathlib import Path

path = Path("logs")
path.mkdir()
```

If `logs` already exists, Python raises:

```text
FileExistsError
```

Example:

```text
FileExistsError: [Errno 17] File exists: 'logs'
```

This is important in automation.

A test script may be executed multiple times.

If the directory already exists, we usually do **not** want the automation to fail simply because the output directory is already present.

---

# 6. `exist_ok=True`

Use:

```python
mkdir(exist_ok=True)
```

Example:

```python
from pathlib import Path

path = Path("logs")

path.mkdir(exist_ok=True)
```

Behavior:

| Directory State | Result            |
| --------------- | ----------------- |
| Does not exist  | Directory created |
| Already exists  | No error          |

This is extremely useful for automation.

Example:

```python
results_dir = Path("results")
results_dir.mkdir(exist_ok=True)
```

The script can safely run multiple times.

---

# 7. `parents=True`

Suppose we want:

```text
storage_tests/
└── results/
    └── daily/
        └── logs/
```

But none of these directories exist.

If we run:

```python
from pathlib import Path

path = Path("storage_tests/results/daily/logs")
path.mkdir()
```

Python will fail because the parent directories do not exist.

Use:

```python
path.mkdir(parents=True)
```

This tells Python to create the required parent directories.

Result:

```text
storage_tests/
└── results/
    └── daily/
        └── logs/
```

---

# 8. `parents=True` + `exist_ok=True`

For automation, this is one of the most useful patterns:

```python
path.mkdir(parents=True, exist_ok=True)
```

Example:

```python
from pathlib import Path

report_dir = Path("test_results/reports/daily")

report_dir.mkdir(
    parents=True,
    exist_ok=True
)
```

This means:

* Create missing parent directories
* Create the target directory
* Do not fail if directories already exist

This pattern is extremely common in automation scripts.

---

# 9. Understanding `parents=True`

Consider:

```python
path = Path("A/B/C")
```

Suppose nothing exists:

```text
.
```

Running:

```python
path.mkdir()
```

fails because:

```text
A
```

does not exist.

But:

```python
path.mkdir(parents=True)
```

creates:

```text
A/
└── B/
    └── C/
```

Python creates the entire missing directory hierarchy.

---

# 10. Combining Both Options

Recommended automation pattern:

```python
path.mkdir(parents=True, exist_ok=True)
```

Example:

```python
from pathlib import Path

log_dir = Path("storage_test/logs/device_01")

log_dir.mkdir(
    parents=True,
    exist_ok=True
)
```

After execution:

```text
storage_test/
└── logs/
    └── device_01/
```

If everything already exists, no error occurs.

---

# 11. Checking Whether a Directory Exists

Use:

```python
Path.exists()
```

Example:

```python
from pathlib import Path

path = Path("logs")

if path.exists():
    print("Path exists")
```

However, `exists()` only tells us that **something** exists at that path.

It does not necessarily mean it is a directory.

---

# 12. Checking Specifically for a Directory

Use:

```python
Path.is_dir()
```

Example:

```python
from pathlib import Path

path = Path("logs")

if path.is_dir():
    print("Directory exists")
```

This is more precise.

---

# 13. Checking for a File

Use:

```python
Path.is_file()
```

Example:

```python
from pathlib import Path

path = Path("results.txt")

if path.is_file():
    print("File exists")
```

This allows automation code to distinguish between files and directories.

---

# 14. `exists()` vs `is_dir()` vs `is_file()`

These methods answer different questions.

### `exists()`

```python
path.exists()
```

Question:

> Does something exist at this path?

---

### `is_dir()`

```python
path.is_dir()
```

Question:

> Is this path a directory?

---

### `is_file()`

```python
path.is_file()
```

Question:

> Is this path a file?

---

Example:

```python
from pathlib import Path

path = Path("logs")

print(path.exists())
print(path.is_dir())
print(path.is_file())
```

If `logs` is a directory:

```text
True
True
False
```

---

# 15. Important Edge Case: Same Path Is a File

Consider:

```text
results
```

Suppose `results` is actually a file:

```text
results
```

Then:

```python
path = Path("results")
```

and:

```python
path.exists()
```

returns:

```text
True
```

But:

```python
path.is_dir()
```

returns:

```text
False
```

Therefore:

```python
path.exists()
```

does not guarantee that the path is usable as a directory.

---

# 16. Safe Directory Creation

A robust pattern is:

```python
from pathlib import Path

path = Path("results")

if path.exists() and not path.is_dir():
    raise RuntimeError(f"{path} exists but is not a directory")

path.mkdir(parents=True, exist_ok=True)
```

This protects against an important failure:

```text
results
```

already exists, but it is a **file**, not a directory.

The automation should not silently ignore this.

---

# 17. Example: Preparing Test Directories

Storage test automation may need several directories:

```text
storage_test/
├── logs/
├── results/
├── reports/
└── temp/
```

Python:

```python
from pathlib import Path

base_dir = Path("storage_test")

(base_dir / "logs").mkdir(parents=True, exist_ok=True)
(base_dir / "results").mkdir(parents=True, exist_ok=True)
(base_dir / "reports").mkdir(parents=True, exist_ok=True)
(base_dir / "temp").mkdir(parents=True, exist_ok=True)
```

This creates the required test environment.

---

# 18. Dynamic Directory Creation

Directories can be created dynamically based on test information.

Example:

```python
from pathlib import Path

device = "device_01"

log_dir = Path("logs") / device

log_dir.mkdir(parents=True, exist_ok=True)
```

Result:

```text
logs/
└── device_01/
```

For another device:

```python
device = "device_02"

log_dir = Path("logs") / device
log_dir.mkdir(parents=True, exist_ok=True)
```

Result:

```text
logs/
├── device_01/
└── device_02/
```

This is useful when testing multiple storage devices.

---

# 19. Dynamic Directories Based on Test Runs

Suppose each test run should have its own directory:

```text
results/
├── run_001/
├── run_002/
└── run_003/
```

Python:

```python
from pathlib import Path

run_id = "run_001"

run_dir = Path("results") / run_id

run_dir.mkdir(parents=True, exist_ok=True)
```

This creates:

```text
results/run_001/
```

The same pattern can be used for:

* Device IDs
* Test IDs
* Build numbers
* Firmware versions
* Dates
* Execution IDs

---

# 20. Directory Creation with Date-Based Organization

A test framework may organize results like:

```text
results/
└── 2026-09-09/
    ├── logs/
    ├── reports/
    └── failures/
```

Example:

```python
from pathlib import Path
from datetime import date

today = date.today()

base_dir = Path("results") / str(today)

(base_dir / "logs").mkdir(parents=True, exist_ok=True)
(base_dir / "reports").mkdir(parents=True, exist_ok=True)
(base_dir / "failures").mkdir(parents=True, exist_ok=True)
```

This creates a structured test-result environment.

---

# 21. Directory Permissions

`mkdir()` also supports a `mode` argument:

```python
path.mkdir(mode=0o755)
```

Example:

```python
from pathlib import Path

path = Path("logs")
path.mkdir(mode=0o755, exist_ok=True)
```

The mode represents filesystem permission bits.

Common example:

```text
755
```

means, conceptually:

```text
Owner  → read/write/execute
Group  → read/execute
Others → read/execute
```

However, the final permissions can also be affected by the system's `umask`.

For most automation scripts, use the default permissions unless there is a specific requirement.

---

# 22. `mkdir()` vs Shell `mkdir`

Python:

```python
from pathlib import Path

Path("logs").mkdir(parents=True, exist_ok=True)
```

Shell:

```bash
mkdir -p logs
```

Both can create directories.

For Python automation, prefer `pathlib` when the operation is part of a Python workflow.

Advantages:

* Cross-platform path handling
* No unnecessary shell invocation
* Easier exception handling
* Easier integration with other `Path` operations
* Cleaner Python code

---

# 23. Common Mistake — Forgetting `parents=True`

Incorrect:

```python
Path("a/b/c").mkdir()
```

when `a` and `b` do not exist.

Correct:

```python
Path("a/b/c").mkdir(parents=True)
```

---

# 24. Common Mistake — Forgetting `exist_ok=True`

This:

```python
Path("logs").mkdir()
```

can fail if `logs` already exists.

For reusable automation:

```python
Path("logs").mkdir(exist_ok=True)
```

---

# 25. Common Mistake — Assuming `exists()` Means Directory

Incorrect assumption:

```python
if path.exists():
    # definitely a directory
```

This is wrong.

The path could be:

* File
* Directory
* Other filesystem object

Use:

```python
if path.is_dir():
    ...
```

when a directory is specifically required.

---

# 26. Common Mistake — Ignoring File/Directory Conflicts

Suppose the automation expects:

```text
results/
```

but the filesystem contains:

```text
results
```

as a file.

Blindly doing:

```python
Path("results").mkdir(exist_ok=True)
```

does not make the situation valid.

The automation should detect the conflict and report it.

Example:

```python
from pathlib import Path

path = Path("results")

if path.exists() and not path.is_dir():
    raise RuntimeError(
        f"{path} exists but is not a directory"
    )

path.mkdir(parents=True, exist_ok=True)
```

---

# 27. Storage Automation Example

Imagine a storage validation framework that needs:

```text
storage_validation/
├── logs/
├── results/
├── reports/
└── temp/
```

Initialization code:

```python
from pathlib import Path

base_dir = Path("storage_validation")

directories = [
    "logs",
    "results",
    "reports",
    "temp"
]

for directory in directories:
    path = base_dir / directory
    path.mkdir(parents=True, exist_ok=True)

print("Test environment initialized.")
```

This is much better than manually creating directories outside the script.

The automation prepares its own required environment.

---

# 28. Directory Handling and Idempotency

A very important automation concept is **idempotency**.

An operation is idempotent when running it repeatedly produces the same intended state.

For example:

```python
path.mkdir(parents=True, exist_ok=True)
```

Running it once:

```text
logs/
```

Running it again:

```text
logs/
```

The result remains valid.

This is desirable in automation because scripts may be:

* Re-run after failures
* Executed repeatedly
* Started by CI systems
* Used by multiple test runs

---

# 29. Directory Creation as Part of Automation Initialization

A good automation structure might be:

```text
Initialize
   ↓
Validate environment
   ↓
Create required directories
   ↓
Run tests
   ↓
Write logs
   ↓
Generate results
   ↓
Generate report
```

Directory handling therefore happens before file-writing operations.

For example:

```python
from pathlib import Path

base_dir = Path("test_run")

logs_dir = base_dir / "logs"
results_dir = base_dir / "results"
reports_dir = base_dir / "reports"

for directory in (logs_dir, results_dir, reports_dir):
    directory.mkdir(parents=True, exist_ok=True)
```

After this, the rest of the automation can safely create files inside those directories.

---

# 30. Recommended Pattern

For most automation directory creation:

```python
from pathlib import Path

directory = Path("results")

directory.mkdir(
    parents=True,
    exist_ok=True
)
```

For a required directory where a file conflict must be detected explicitly:

```python
from pathlib import Path

directory = Path("results")

if directory.exists() and not directory.is_dir():
    raise RuntimeError(
        f"{directory} exists but is not a directory"
    )

directory.mkdir(parents=True, exist_ok=True)
```

---

# 31. Key Takeaways

Remember these methods:

| Method           | Purpose                                |
| ---------------- | -------------------------------------- |
| `Path.mkdir()`   | Create a directory                     |
| `parents=True`   | Create missing parent directories      |
| `exist_ok=True`  | Don't fail if directory already exists |
| `Path.exists()`  | Check whether path exists              |
| `Path.is_dir()`  | Check whether path is a directory      |
| `Path.is_file()` | Check whether path is a file           |

Most common automation pattern:

```python
Path("results").mkdir(
    parents=True,
    exist_ok=True
)
```

---

# 32. Interview Points

### Q1. How do you create a directory in Python?

```python
from pathlib import Path

Path("logs").mkdir()
```

### Q2. How do you create nested directories?

```python
Path("a/b/c").mkdir(parents=True)
```

### Q3. How do you avoid an error if the directory already exists?

```python
Path("logs").mkdir(exist_ok=True)
```

### Q4. What does `parents=True` do?

It creates missing parent directories in the specified path.

### Q5. What does `exist_ok=True` do?

It prevents `FileExistsError` when the target directory already exists.

### Q6. How do you check whether a path is a directory?

```python
path.is_dir()
```

### Q7. What is the difference between `exists()` and `is_dir()`?

```python
exists()
```

checks whether something exists at the path.

```python
is_dir()
```

checks specifically whether the path represents a directory.

### Q8. What happens if a file already exists where you want to create a directory?

The directory cannot be created there. Robust automation should detect the conflict and report it rather than assuming the path is usable.

---

# 33. Automation Principle

> **A reliable automation script should prepare and validate its filesystem environment before performing test operations.**

Instead of assuming:

```text
logs/
results/
reports/
```

already exist, the automation should establish the required directory structure itself.

The core pattern to remember is:

```python
from pathlib import Path

directory = Path("test_results/logs")

directory.mkdir(
    parents=True,
    exist_ok=True
)
```

This is the foundation for the next topics, where we will work with **directory traversal and discovering files inside directory trees**.

**Next file:** `10_Directory_Traversal.md`

