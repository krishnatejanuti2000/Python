# `11_File_Operations.md`

# File Operations

## 1. Introduction

File handling is not limited to reading and writing files.

Storage automation frequently needs to **manage files**:

* Rename files
* Delete files
* Copy files
* Move files
* Create backups
* Organize test artifacts
* Archive logs
* Clean temporary files
* Prepare files for another test stage

Python provides these capabilities through:

```python
pathlib
shutil
```

For modern Python automation, `pathlib.Path` should generally be the first choice for filesystem operations, while `shutil` is particularly useful for copying and moving files/directories.

---

# 2. File Operations Overview

The major operations are:

| Operation       | Python           |
| --------------- | ---------------- |
| Rename          | `Path.rename()`  |
| Delete file     | `Path.unlink()`  |
| Copy file       | `shutil.copy2()` |
| Move file       | `shutil.move()`  |
| Check existence | `Path.exists()`  |
| Check file      | `Path.is_file()` |
| Check directory | `Path.is_dir()`  |

A typical workflow might be:

```text
Test generates log
       ↓
Rename log
       ↓
Copy backup
       ↓
Move to archive
       ↓
Delete temporary file
```

---

# 3. Renaming a File

Use:

```python
Path.rename()
```

Example:

```python
from pathlib import Path

old_file = Path("test.log")
new_file = Path("test_complete.log")

old_file.rename(new_file)
```

Before:

```text
test.log
```

After:

```text
test_complete.log
```

The file itself is renamed; its contents remain unchanged.

---

# 4. Rename with a New Path

`rename()` can also move a file to another location while changing its name.

Example:

```python
from pathlib import Path

source = Path("test.log")
destination = Path("results/test.log")

source.rename(destination)
```

If the destination directory exists, the file is moved there under the new path.

So `rename()` can perform a filesystem rename/move operation depending on the destination.

---

# 5. Important Rename Requirement

The destination's parent directory must generally already exist.

For example:

```python
source = Path("test.log")
destination = Path("results/test.log")

source.rename(destination)
```

If:

```text
results/
```

does not exist, the operation can fail.

Prepare the directory first:

```python
from pathlib import Path

source = Path("test.log")
destination = Path("results/test.log")

destination.parent.mkdir(parents=True, exist_ok=True)

source.rename(destination)
```

---

# 6. Checking Before Renaming

A safer automation pattern:

```python
from pathlib import Path

source = Path("test.log")
destination = Path("test_complete.log")

if not source.is_file():
    raise FileNotFoundError(
        f"Source file not found: {source}"
    )

source.rename(destination)
```

This provides a meaningful failure if the expected source file does not exist.

---

# 7. Deleting a File with `unlink()`

Use:

```python
Path.unlink()
```

Example:

```python
from pathlib import Path

file = Path("temporary.log")

file.unlink()
```

The file is removed from the filesystem.

---

# 8. `unlink()` Only for Files

`unlink()` is intended for removing a file or symbolic link.

Do not use:

```python
Path("logs").unlink()
```

if `logs` is a directory.

For directories, different operations are required.

A directory can be removed when empty using:

```python
Path("logs").rmdir()
```

But directory deletion is a separate topic from deleting individual files.

---

# 9. Safe File Deletion

Before deleting:

```python
from pathlib import Path

file = Path("temporary.log")

if file.is_file():
    file.unlink()
```

This prevents trying to delete a path that is not a regular file.

However, in automation, it is often better to distinguish between:

```text
file missing
```

and:

```text
file successfully deleted
```

depending on the expected behavior.

---

# 10. `missing_ok=True`

`unlink()` supports:

```python
missing_ok=True
```

Example:

```python
from pathlib import Path

Path("temporary.log").unlink(missing_ok=True)
```

Behavior:

| File State     | Result                 |
| -------------- | ---------------------- |
| Exists         | Deleted                |
| Does not exist | No `FileNotFoundError` |

This is useful for cleanup operations.

Example:

```python
temporary_file.unlink(missing_ok=True)
```

This makes cleanup idempotent.

---

# 11. When Should `missing_ok=True` Be Used?

It depends on the purpose of the operation.

### Required file

If the file is expected to exist:

```python
file.unlink()
```

A missing file may indicate a problem.

### Optional cleanup file

If the file is temporary and may or may not exist:

```python
file.unlink(missing_ok=True)
```

A missing file is acceptable.

This distinction is important in test automation.

---

# 12. Copying Files with `shutil.copy2()`

For copying files, use:

```python
shutil.copy2()
```

Example:

```python
from pathlib import Path
import shutil

source = Path("test.log")
destination = Path("backup/test.log")

destination.parent.mkdir(parents=True, exist_ok=True)

shutil.copy2(source, destination)
```

The original file remains.

After copying:

```text
test.log
backup/
└── test.log
```

---

# 13. `copy2()` vs `copy()`

Python's `shutil` provides:

```python
shutil.copy()
```

and:

```python
shutil.copy2()
```

Both copy file contents.

`copy2()` additionally attempts to preserve file metadata such as modification time.

For test artifacts and logs, `copy2()` is often a useful choice when preserving metadata matters.

---

# 14. Copying a File Does Not Remove the Original

Example:

```python
shutil.copy2(
    "results.txt",
    "backup/results.txt"
)
```

Before:

```text
results.txt
```

After:

```text
results.txt
backup/
└── results.txt
```

Both files exist.

This is different from moving.

---

# 15. Moving a File with `shutil.move()`

Use:

```python
shutil.move()
```

Example:

```python
from pathlib import Path
import shutil

source = Path("test.log")
destination = Path("archive/test.log")

destination.parent.mkdir(parents=True, exist_ok=True)

shutil.move(source, destination)
```

After the operation:

```text
archive/
└── test.log
```

The source path no longer contains the file.

---

# 16. Copy vs Move

This distinction is fundamental.

### Copy

```python
shutil.copy2(source, destination)
```

Result:

```text
Source exists
Destination exists
```

### Move

```python
shutil.move(source, destination)
```

Result:

```text
Source removed from original location
Destination exists
```

Think:

```text
COPY
A ─────────────→ B
A remains

MOVE
A ─────────────→ B
A no longer remains at original location
```

---

# 17. Rename vs Move

`Path.rename()` can change the name or path of a file.

Example:

```python
source = Path("test.log")
destination = Path("test_final.log")

source.rename(destination)
```

This is primarily useful for renaming or relocating a filesystem entry.

`shutil.move()` is convenient when the intention is explicitly to move files/directories.

Example:

```python
shutil.move(
    "test.log",
    "archive/test.log"
)
```

---

# 18. Creating Backups

A common automation requirement is backing up a generated result.

Example:

```python
from pathlib import Path
import shutil

source = Path("results/test_results.txt")
backup = Path("backup/test_results.txt")

backup.parent.mkdir(parents=True, exist_ok=True)

shutil.copy2(source, backup)
```

Now:

```text
results/
└── test_results.txt

backup/
└── test_results.txt
```

The original remains available.

---

# 19. Archiving Completed Logs

Suppose a test finishes and logs need to be moved:

```text
logs/
└── device_01.log
```

to:

```text
archive/
└── device_01.log
```

Code:

```python
from pathlib import Path
import shutil

source = Path("logs/device_01.log")
archive = Path("archive/device_01.log")

archive.parent.mkdir(parents=True, exist_ok=True)

shutil.move(source, archive)
```

This is useful for separating:

```text
active logs
```

from:

```text
archived logs
```

---

# 20. Cleaning Temporary Files

Storage test automation often creates temporary artifacts:

```text
temp/
├── command_output.txt
├── debug.log
└── intermediate.result
```

After the test:

```python
from pathlib import Path

temp_dir = Path("temp")

for file in temp_dir.iterdir():

    if file.is_file():
        file.unlink()
```

This removes files directly inside `temp`.

It does not recursively delete nested directories.

---

# 21. Safe Cleanup

A safer version:

```python
from pathlib import Path

temp_dir = Path("temp")

if temp_dir.is_dir():

    for file in temp_dir.iterdir():

        if file.is_file():
            file.unlink()
```

This prevents traversal of a path that isn't a directory.

---

# 22. Recursive File Cleanup

Suppose:

```text
temp/
├── device1/
│   └── debug.log
└── device2/
    └── debug.log
```

To find all `.log` files recursively:

```python
from pathlib import Path

temp_dir = Path("temp")

for file in temp_dir.rglob("*.log"):

    if file.is_file():
        file.unlink()
```

This combines:

```text
Directory traversal
        +
File deletion
```

---

# 23. Copying Multiple Files

Suppose:

```text
logs/
├── controller.log
├── kernel.log
└── storage.log
```

We want to copy all logs to:

```text
backup/
```

Code:

```python
from pathlib import Path
import shutil

source_dir = Path("logs")
backup_dir = Path("backup")

backup_dir.mkdir(parents=True, exist_ok=True)

for file in source_dir.glob("*.log"):

    if file.is_file():
        destination = backup_dir / file.name
        shutil.copy2(file, destination)
```

The resulting structure:

```text
backup/
├── controller.log
├── kernel.log
└── storage.log
```

---

# 24. Moving Multiple Files

Similarly:

```python
from pathlib import Path
import shutil

source_dir = Path("logs")
archive_dir = Path("archive")

archive_dir.mkdir(parents=True, exist_ok=True)

for file in source_dir.glob("*.log"):

    if file.is_file():
        destination = archive_dir / file.name
        shutil.move(file, destination)
```

The files are moved from:

```text
logs/
```

to:

```text
archive/
```

---

# 25. Preserving the Filename

A common pattern is:

```python
destination = destination_dir / source.name
```

Example:

```python
source = Path("logs/device_01.log")
destination_dir = Path("archive")

destination = destination_dir / source.name
```

Result:

```text
archive/device_01.log
```

Here:

```python
source.name
```

returns:

```text
device_01.log
```

This is useful when processing many files.

---

# 26. Copying While Changing the Name

You can also construct a different destination name:

```python
source = Path("test.log")

destination = Path("backup/test_backup.log")
```

Then:

```python
shutil.copy2(source, destination)
```

Result:

```text
backup/test_backup.log
```

---

# 27. File Operations and Error Handling

Filesystem operations can fail for many reasons.

Common exceptions include:

```text
FileNotFoundError
PermissionError
FileExistsError
IsADirectoryError
NotADirectoryError
OSError
```

Example:

```python
from pathlib import Path

file = Path("test.log")

try:
    file.unlink()

except FileNotFoundError:
    print("File does not exist")

except PermissionError:
    print("Permission denied")
```

This connects directly with the exception-handling concepts learned earlier.

---

# 28. Don't Hide Filesystem Errors Blindly

Avoid:

```python
try:
    file.unlink()
except:
    pass
```

This is poor automation practice.

It can hide:

* Permission problems
* Filesystem problems
* Unexpected paths
* Programming errors

Instead, catch specific exceptions when you can.

---

# 29. Example: Robust File Move

```python
from pathlib import Path
import shutil

source = Path("test.log")
destination = Path("archive/test.log")

try:

    if not source.is_file():
        raise FileNotFoundError(
            f"Source file not found: {source}"
        )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.move(source, destination)

    print("File moved successfully.")

except PermissionError:
    print("Permission denied.")

except OSError as error:
    print(f"Filesystem error: {error}")
```

This is much closer to production-style automation.

---

# 30. Atomicity and Data Safety

File operations can matter greatly when dealing with test results.

For example, suppose a test generates:

```text
results.txt
```

and the automation immediately deletes or moves it.

If the operation fails halfway through or an unexpected condition occurs, important test evidence could be lost.

Therefore:

> **Do not delete or move important test artifacts until their successful persistence has been verified.**

For critical storage validation results, consider:

```text
Generate
   ↓
Validate
   ↓
Backup
   ↓
Archive
   ↓
Cleanup temporary copy
```

rather than immediately deleting the original.

---

# 31. Example: Backup Before Cleanup

```python
from pathlib import Path
import shutil

result = Path("results/test_result.txt")
backup = Path("backup/test_result.txt")

backup.parent.mkdir(parents=True, exist_ok=True)

shutil.copy2(result, backup)

if backup.is_file():
    result.unlink()
```

The important idea is:

```text
Copy first
   ↓
Verify backup
   ↓
Delete original
```

This is safer than:

```text
Delete first
   ↓
Hope backup existed
```

---

# 32. Working with Directories

`shutil` can also operate on directories.

For example:

```python
shutil.copytree(
    "test_results",
    "test_results_backup"
)
```

This copies an entire directory tree.

Similarly, `shutil.move()` can move a directory:

```python
shutil.move(
    "test_results",
    "archive/test_results"
)
```

Directory-tree operations should be used carefully because they can affect many files at once.

---

# 33. Why `pathlib` + `shutil` Work Well Together

A clean Python automation design often looks like:

```python
from pathlib import Path
import shutil
```

Use `Path` for:

* Building paths
* Checking files/directories
* Traversal
* Renaming
* Deleting
* Opening files

Use `shutil` for:

* Copying
* Moving
* Directory-tree operations

Example:

```python
source = Path("logs/device.log")
backup_dir = Path("backup")

backup_dir.mkdir(parents=True, exist_ok=True)

destination = backup_dir / source.name

shutil.copy2(source, destination)
```

This combination is highly practical.

---

# 34. Common Mistake — Copying Instead of Moving

If the requirement is:

> Archive the log and remove it from the active log directory.

Using:

```python
shutil.copy2(source, destination)
```

leaves the original behind.

You need:

```python
shutil.move(source, destination)
```

---

# 35. Common Mistake — Moving Instead of Copying

If the requirement is:

> Create a backup while keeping the original.

Do **not** use:

```python
shutil.move(source, destination)
```

Use:

```python
shutil.copy2(source, destination)
```

---

# 36. Common Mistake — Deleting Without Validation

Risky:

```python
Path("results.txt").unlink()
```

when the path may be incorrect or dynamically generated.

For important artifacts, first verify:

```python
if path.is_file():
    path.unlink()
```

For critical cleanup, additional validation may be appropriate.

---

# 37. Common Mistake — Hard-Coded Destination Paths

Instead of:

```python
destination = "backup/device_01.log"
```

prefer:

```python
source = Path("logs/device_01.log")
destination_dir = Path("backup")

destination = destination_dir / source.name
```

This becomes reusable for any source file.

---

# 38. Practical Storage Automation Example

Suppose a storage test produces:

```text
test_run/
├── logs/
│   ├── controller.log
│   └── kernel.log
├── results/
│   └── test_results.txt
└── temp/
    └── debug.txt
```

After the test:

1. Back up results.
2. Archive logs.
3. Remove temporary files.

Example:

```python
from pathlib import Path
import shutil

base = Path("test_run")

logs_dir = base / "logs"
results_dir = base / "results"
backup_dir = base / "backup"
archive_dir = base / "archive"
temp_dir = base / "temp"

backup_dir.mkdir(parents=True, exist_ok=True)
archive_dir.mkdir(parents=True, exist_ok=True)

# Backup results
for file in results_dir.glob("*"):

    if file.is_file():
        shutil.copy2(
            file,
            backup_dir / file.name
        )

# Archive logs
for file in logs_dir.glob("*.log"):

    if file.is_file():
        shutil.move(
            file,
            archive_dir / file.name
        )

# Clean temporary files
for file in temp_dir.iterdir():

    if file.is_file():
        file.unlink()
```

This demonstrates several concepts together:

```text
Path
  ↓
Directory handling
  ↓
Traversal
  ↓
Copy
  ↓
Move
  ↓
Delete
```

---

# 39. File Operation Decision Guide

When you need to perform an operation, ask:

### Do I want another copy?

Use:

```python
shutil.copy2()
```

### Do I want to relocate the file?

Use:

```python
shutil.move()
```

### Do I want to rename the file?

Use:

```python
Path.rename()
```

### Do I want to delete the file?

Use:

```python
Path.unlink()
```

### Do I want to delete an optional cleanup file?

Use:

```python
Path.unlink(missing_ok=True)
```

---

# 40. Interview Questions

### Q1. How do you rename a file using `pathlib`?

```python
Path("old.txt").rename("new.txt")
```

---

### Q2. How do you delete a file?

```python
Path("file.txt").unlink()
```

---

### Q3. How do you delete a file without raising an error if it doesn't exist?

```python
Path("file.txt").unlink(missing_ok=True)
```

---

### Q4. How do you copy a file?

```python
import shutil

shutil.copy2(source, destination)
```

---

### Q5. What is the difference between `copy2()` and `move()`?

`copy2()` creates another copy while retaining the source.

`move()` relocates the source to the destination.

---

### Q6. Why might you use `copy2()` instead of `copy()`?

`copy2()` attempts to preserve additional file metadata such as modification time.

---

### Q7. How do you construct a destination using the source filename?

```python
destination = destination_dir / source.name
```

---

### Q8. Why should important test results be backed up before deletion?

Because test artifacts may be required for:

* Failure analysis
* Debugging
* Reproduction
* Validation evidence
* Reporting

Deleting them prematurely can destroy valuable diagnostic information.

---

# 41. Key Takeaways

### Rename

```python
source.rename(destination)
```

### Delete

```python
file.unlink()
```

### Delete safely when missing is acceptable

```python
file.unlink(missing_ok=True)
```

### Copy

```python
shutil.copy2(source, destination)
```

### Move

```python
shutil.move(source, destination)
```

### Preserve source while creating backup

```python
shutil.copy2(source, backup)
```

### Archive/remove from original location

```python
shutil.move(source, archive)
```

---

# 42. Automation Principle

> **File operations should be intentional, validated, and safe because test artifacts are evidence.**

In storage test automation, logs and results are not merely files—they may be the evidence required to determine **why a storage test failed**.

Therefore, a good automation flow is:

```text
Generate artifact
       ↓
Validate artifact
       ↓
Preserve / backup if required
       ↓
Archive if required
       ↓
Clean temporary data
```

The next topic focuses on an important scalability problem: **processing very large files efficiently without consuming excessive memory.**

**Next file:** `12_Large_File_Processing.md`

