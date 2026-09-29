# BLOCK 1.2 — FILESYSTEM AUTOMATION

## Purpose

Filesystem automation allows Python automation to create, inspect, manipulate, preserve, and clean up files and directories.

For Storage Test Automation, filesystem operations are required for:

* Test logs
* Test results
* Diagnostic evidence
* Temporary test artifacts
* Backup/archive of failed runs
* Cleanup of temporary data
* Recursive file discovery

The master syllabus requires:

* `os`
* `pathlib`
* `shutil`
* `tempfile`
* Directory creation
* File existence checks
* File copying / moving
* File cleanup
* Recursive directory traversal
* Temporary test artifacts
* Log and evidence directory handling

---

# 1. `os`

The `os` module provides basic operating-system and filesystem operations.

```python
import os
```

---

## 1.1 Current Working Directory

```python
os.getcwd()
```

Returns the directory from which the Python process is currently running.

Example:

```python
import os

print(os.getcwd())
```

Possible output:

```text
/home/krishnatejanuti/Documents/Automation
```

### Important distinction

`os.getcwd()` does not mean:

> Where is my Python source file?

It means:

> From which directory is the Python process currently running?

For example:

```bash
cd ~/Documents/Automation
python3 tests/test_nvme.py
```

The working directory is:

```text
/home/krishnatejanuti/Documents/Automation
```

even though the Python file is inside:

```text
tests/test_nvme.py
```

This matters because relative paths are interpreted from the current working directory.

---

# 1.2 `os.listdir()`

Lists the contents of a directory.

```python
import os

print(os.listdir("."))
```

`.` represents the current working directory.

For example:

```text
Automation/
├── Storage_Validation/
├── Nvme_Validation/
└── tests/
```

may produce:

```python
['Storage_Validation', 'Nvme_Validation', 'tests']
```

To list the contents of a subdirectory:

```python
print(os.listdir("tests"))
```

Example:

```python
['test_nvme.py']
```

### Important distinction

```python
os.listdir(".")
```

lists the current directory.

```python
os.listdir("tests")
```

lists the `tests` directory.

---

# 1.3 `os.path.exists()`

Checks whether something exists at a specified path.

```python
import os

print(os.path.exists("tests"))
```

Possible result:

```text
True
```

If the path does not exist:

```python
print(os.path.exists("missing_file.txt"))
```

Result:

```text
False
```

`exists()` answers:

> Does something exist at this path?

It does not tell us whether that thing is a file or directory.

---

# 1.4 `os.path.isfile()`

Checks whether a path refers to a file.

```python
os.path.isfile("tests/test_nvme.py")
```

If `test_nvme.py` is a file:

```text
True
```

---

# 1.5 `os.path.isdir()`

Checks whether a path refers to a directory.

```python
os.path.isdir("tests")
```

If `tests` is a directory:

```text
True
```

---

## Important Difference

For a directory:

```text
tests
```

the results are:

```text
exists() → True
isfile() → False
isdir()  → True
```

For a file:

```text
tests/test_nvme.py
```

the results are:

```text
exists() → True
isfile() → True
isdir()  → False
```

For a missing path:

```text
exists() → False
isfile() → False
isdir()  → False
```

Mental model:

```text
exists()
    ↓
Is anything there?

isfile()
    ↓
Is it a file?

isdir()
    ↓
Is it a directory?
```

---

# 1.6 Creating Directories with `os.makedirs()`

```python
os.makedirs("results")
```

Creates a directory if it does not already exist.

If the directory already exists, it normally raises an error.

For automation, we commonly use:

```python
os.makedirs("results", exist_ok=True)
```

Behavior:

```text
Directory does not exist
        ↓
Create it

Directory already exists
        ↓
Continue without error
```

### `exist_ok=True`

This means that an existing directory is not treated as an error.

It does not mean that every filesystem problem is ignored.

If `results` already exists as a file rather than a directory, creation still fails.

---

# 1.7 Relative and Absolute Paths

A relative path:

```text
logs/test.log
```

is interpreted relative to the current working directory.

An absolute path:

```text
/home/krishnatejanuti/Documents/Automation/logs/test.log
```

starts from the filesystem root.

This distinction is important when debugging automation failures involving missing files or incorrect working directories.

---

# 1.8 `os.path.join()`

Builds a path from separate components.

```python
path = os.path.join(
    "test_run",
    "logs",
    "nvme_health.log"
)
```

Result:

```text
test_run/logs/nvme_health.log
```

Important:

> `os.path.join()` only constructs the path. It does not create the directory or file.

For example:

```python
path = os.path.join("abc", "logs", "test.log")
```

creates only a Python path value.

It does not create:

```text
abc/
└── logs/
    └── test.log
```

---

# 1.9 `os.path.abspath()`

Converts a relative path to an absolute path.

```python
path = os.path.abspath("logs/test.log")
```

If the current directory is:

```text
/home/krishnatejanuti/Documents/Automation
```

the result may be:

```text
/home/krishnatejanuti/Documents/Automation/logs/test.log
```

Important:

> `abspath()` does not create the path.

It only represents the same location as an absolute path.

---

# 1.10 `os.path.basename()`

Returns the final component of a path.

```python
path = "/tmp/nvme/results/test_result.json"

print(os.path.basename(path))
```

Output:

```text
test_result.json
```

Mental model:

```text
/tmp/nvme/results/test_result.json
                         └─────────────┘
                            basename
```

The final component does not have to be a file.

For:

```python
os.path.basename("/tmp/nvme/results")
```

the result is:

```text
results
```

So:

> `basename()` means the final component of the path.

---

# 1.11 `os.path.dirname()`

Returns the directory portion of a path.

```python
path = "/tmp/nvme/results/test_result.json"

print(os.path.dirname(path))
```

Output:

```text
/tmp/nvme/results
```

Together:

```text
/tmp/nvme/results/test_result.json
└──────────────────┘ └───────────────┘
      dirname             basename
```

---

# 1.12 File Opening Modes

Python's `open()` can work with different file modes.

## `"r"` — Read

```python
with open("nvme.log", "r") as file:
    data = file.read()
```

The file must already exist.

If it does not exist:

```text
FileNotFoundError
```

---

## `"w"` — Write

```python
with open("nvme.log", "w") as file:
    file.write("NVMe Health: PASS\n")
```

Behavior:

```text
File doesn't exist
    ↓
Create it

File already exists
    ↓
Existing contents are truncated
    ↓
New contents are written
```

Example:

Before:

```text
OLD LOG DATA
```

After:

```python
with open("nvme.log", "w") as file:
    file.write("NEW LOG DATA")
```

the file contains:

```text
NEW LOG DATA
```

---

## `"a"` — Append

```python
with open("nvme.log", "a") as file:
    file.write("Temperature: 45C\n")
```

Behavior:

```text
File doesn't exist
    ↓
Create it

File already exists
    ↓
Preserve existing contents
    ↓
Append new data
```

For example:

```text
HEALTH OK
TEMPERATURE 45C
```

This is useful for repeatedly adding diagnostic information to a log.

---

## `"x"` — Exclusive Creation

```python
with open("test_result.json", "x") as file:
    file.write("PASS")
```

Behavior:

```text
File doesn't exist
    ↓
Create it

File already exists
    ↓
FileExistsError
```

`"x"` is useful when an existing file must never be silently overwritten.

---

# 1.13 Context Manager and `open()`

Consider:

```python
with open("nvme.log", "w") as file:
    file.write("NVMe test log\n")
```

There are two separate concepts here.

### `open(..., "w")`

Controls how the file is opened.

In `"w"` mode, it creates the file if necessary and overwrites existing contents.

### `with`

Manages the lifetime of the file resource.

Conceptually:

```text
open file
   ↓
use file
   ↓
leave with block
   ↓
file is closed automatically
```

Therefore:

> The `with` statement does not create the file. The file-opening operation does.

---

# 1.14 `os.remove()`

Removes a file.

```python
os.remove("test.log")
```

It is intended for files.

It does not remove a directory.

Trying to use it on a directory results in an error.

---

# 1.15 `os.rmdir()`

Removes an empty directory.

```python
os.rmdir("logs")
```

If the directory contains files:

```text
logs/
├── test1.log
└── test2.log
```

`os.rmdir()` cannot remove it.

Mental model:

```text
os.remove()
    ↓
file

os.rmdir()
    ↓
empty directory
```

---

# 1.16 `os.walk()`

`os.walk()` recursively traverses a directory tree.

Example:

```text
test_run/
├── logs/
│   ├── nvme.log
│   └── dmesg.log
└── results/
    └── result.json
```

Code:

```python
import os

for root, directories, files in os.walk("test_run"):
    print("ROOT:", root)
    print("DIRS:", directories)
    print("FILES:", files)
```

Conceptually:

```text
Iteration 1
root        → test_run
directories → logs, results
files       → []

Iteration 2
root        → test_run/logs
directories → []
files       → nvme.log, dmesg.log

Iteration 3
root        → test_run/results
directories → []
files       → result.json
```

`os.walk()` performs the recursion for us.

---

# 1.17 Getting Full File Paths from `os.walk()`

`os.walk()` gives us a directory (`root`) and filenames.

We can construct the full path:

```python
import os

for root, directories, files in os.walk("test_run"):
    for file_name in files:
        full_path = os.path.join(root, file_name)
        print(full_path)
```

Example output:

```text
test_run/logs/nvme.log
test_run/logs/dmesg.log
test_run/results/result.json
```

This is useful for later:

```text
Read
Parse
Copy
Archive
Validate
```

---

# 1.18 Environment Variables

Python can access environment variables through `os`.

```python
import os

print(os.environ.get("HOME"))
```

Possible output:

```text
/home/krishnatejanuti
```

Environment variables are useful when automation should avoid unnecessarily hardcoding environment-specific values.

---

# 2. `pathlib`

`pathlib` provides an object-oriented way to work with filesystem paths.

```python
from pathlib import Path
```

The central idea is:

```text
os approach
    ↓
Path represented mainly as a string
    ↓
os.path functions

pathlib approach
    ↓
Path object
    ↓
operations on the Path object
```

---

# 2.1 Creating a `Path`

```python
from pathlib import Path

path = Path("test_run/logs/nvme.log")
```

This creates a `Path` object representing that location.

It does not create the filesystem object.

---

# 2.2 Building Paths with `/`

Instead of:

```python
os.path.join(
    "test_run",
    "logs",
    "nvme.log"
)
```

we can use:

```python
Path("test_run") / "logs" / "nvme.log"
```

Example:

```python
run_dir = Path("test_run")
log_dir = run_dir / "logs"
log_file = log_dir / "nvme.log"
```

Result:

```text
test_run/logs/nvme.log
```

---

# 2.3 Current Directory

```python
Path.cwd()
```

returns the current working directory as a `Path` object.

Comparison:

```text
os.getcwd()
    → string

Path.cwd()
    → Path object
```

---

# 2.4 Existence and Type Checks

```python
path.exists()
path.is_file()
path.is_dir()
```

Equivalent concepts:

```text
os.path.exists()  → path.exists()
os.path.isfile()  → path.is_file()
os.path.isdir()   → path.is_dir()
```

---

# 2.5 Parent and Name

For:

```python
path = Path("/tmp/nvme/results/test_result.json")
```

we can use:

```python
path.parent
path.name
```

Results:

```text
/tmp/nvme/results
test_result.json
```

---

# 2.6 Stem and Suffix

For:

```python
path = Path("nvme_health.log")
```

we have:

```python
path.name
path.stem
path.suffix
```

Results:

```text
nvme_health.log
nvme_health
.log
```

Meaning:

```text
name   → complete final component
stem   → name without extension
suffix → extension
```

---

# 2.7 Creating Directories

```python
from pathlib import Path

log_dir = Path("test_run/logs")

log_dir.mkdir(
    parents=True,
    exist_ok=True
)
```

`parents=True` allows missing parent directories to be created.

`exist_ok=True` prevents an already-existing directory from being treated as an error.

---

# 2.8 Creating Files with `touch()`

```python
file_path = Path("test_run/logs/nvme.log")

file_path.touch()
```

This actually creates the file if necessary.

Remember:

```python
Path("test_run/logs/nvme.log")
```

only represents the path.

```python
file_path.touch()
```

creates the file.

---

# 2.9 Writing Text

```python
file_path.write_text(
    "NVMe Health check started\n"
)
```

This writes text to the file.

Existing contents are replaced.

---

# 2.10 Reading Text

```python
data = file_path.read_text()

print(data)
```

This reads the text from the file.

---

# 2.11 Appending with `Path.open()`

For append behavior:

```python
with file_path.open("a") as file:
    file.write("NVMe Health check completed\n")
```

The `Path` object provides the path while `open("a")` provides the desired file mode.

---

# 2.12 Removing a File

```python
file_path.unlink()
```

This removes the file.

Afterward:

```python
file_path.exists()
```

returns:

```text
False
```

---

# 3. `shutil`

`shutil` provides higher-level filesystem operations, especially copying, moving, and recursive removal.

```python
import shutil
```

---

# 3.1 Copying a File

```python
shutil.copy(
    "run_001/logs/nvme.log",
    "backup/nvme.log"
)
```

Mental model:

```text
source
   ↓
copy
   ↓
destination
```

After copying:

```text
source       → still exists
destination  → new copy exists
```

---

# 3.2 `copy2()`

```python
shutil.copy2(source, destination)
```

`copy2()` copies the file and attempts to preserve additional file metadata compared with `copy()`.

Use it when preserving metadata is desirable.

---

# 3.3 Copying a Directory

```python
shutil.copytree(
    "run_001",
    "failed_runs/run_001"
)
```

This recursively copies the complete directory tree.

Example:

```text
run_001/
├── logs/
├── results/
└── evidence/
```

becomes:

```text
failed_runs/
└── run_001/
    ├── logs/
    ├── results/
    └── evidence/
```

---

# 3.4 Moving Files or Directories

```python
shutil.move(
    "temp/result.json",
    "final_results/result.json"
)
```

Unlike copying, the original is moved to the destination.

Mental model:

```text
copy
    → source remains

move
    → source is relocated
```

---

# 3.5 Recursive Cleanup with `rmtree()`

`os.rmdir()` removes only an empty directory.

For a non-empty directory tree:

```python
shutil.rmtree("temporary_run")
```

This recursively removes the directory and its contents.

Because it is destructive, it must be used carefully.

---

# 3.6 Storage Automation Example

A failed test may produce:

```text
run_001/
├── logs/
├── results/
└── evidence/
```

We may want to preserve it:

```python
shutil.copytree(
    "run_001",
    "failed_runs/run_001"
)
```

This follows an important automation principle:

```text
Failure
   ↓
Preserve evidence
   ↓
Investigate / report
   ↓
Clean disposable data
```

---

# 4. `tempfile`

`tempfile` is used for temporary files and directories.

```python
import tempfile
```

The purpose is to provide temporary workspace for data that is needed during an operation but does not necessarily belong in permanent test artifacts.

---

# 4.1 Temporary File

```python
temp_file = tempfile.NamedTemporaryFile()

print(temp_file.name)
```

Python generates a temporary file with a system-managed name.

Conceptually:

```text
/tmp/tmpXXXXXX
```

The generated name helps avoid collisions when multiple operations or tests run.

---

# 4.2 Temporary Directory

```python
temp_dir = tempfile.TemporaryDirectory()

print(temp_dir.name)
```

A temporary directory is useful when multiple temporary files are needed.

Example:

```text
temporary workspace/
├── raw.txt
├── parsed.json
└── intermediate.log
```

---

# 4.3 Temporary Directory with a Context Manager

```python
import tempfile

with tempfile.TemporaryDirectory() as temp_dir:
    print(temp_dir)

    # temporary test work
```

Conceptual lifecycle:

```text
Enter with
    ↓
Temporary directory exists
    ↓
Perform test work
    ↓
Leave with
    ↓
Temporary workspace is cleaned up
```

This makes the resource lifecycle explicit.

---

# 4.4 Temporary Data vs Permanent Evidence

This distinction is critical for Storage Test Automation.

### Temporary working data

Examples:

```text
Intermediate parser output
Temporary test input
Temporary comparison file
Temporary command output
```

These can normally be cleaned up.

### Permanent evidence

Examples:

```text
dmesg output
NVMe error log
Health information
Failure command output
Test result
```

These may need to be preserved for troubleshooting and RCA.

Therefore:

```text
Temporary data
    ↓
tempfile
    ↓
use
    ↓
cleanup

Important evidence
    ↓
permanent evidence directory
    ↓
preserve
```

---

# 4.5 `delete=True` and `delete=False`

For temporary files:

```python
tempfile.NamedTemporaryFile(delete=True)
```

is intended for automatic cleanup according to the temporary-file object's lifecycle.

With:

```python
tempfile.NamedTemporaryFile(delete=False)
```

the file remains after the temporary-file object is closed, allowing explicit lifecycle management.

The correct choice depends on whether the data is disposable or needs to be preserved.

---

# 5. Filesystem Automation Mental Model

The four main tools have different responsibilities.

```text
os
 ↓
Basic OS/filesystem operations

pathlib
 ↓
Object-oriented path/file handling

shutil
 ↓
Copy, move, recursive filesystem operations

tempfile
 ↓
Temporary working files/directories
```

---

# 6. Complete Storage Automation Example

A storage test may use filesystem automation like this:

```text
Test starts
    ↓
Create run directories
    ↓
Create temporary workspace
    ↓
Execute test
    ↓
Generate temporary/intermediate data
    ↓
Validate result
    ↓
PASS?
    │
    ├── YES → clean temporary data
    │
    └── NO
         ↓
      preserve evidence
         ↓
      collect diagnostics
         ↓
      archive/copy failed run
         ↓
      clean disposable data
```

This is the practical reason we learned these filesystem tools.

---

# 7. Tool Selection Summary

| Requirement            | Appropriate Tool                        |
| ---------------------- | --------------------------------------- |
| Get current directory  | `os.getcwd()` / `Path.cwd()`            |
| List directory         | `os.listdir()`                          |
| Check existence        | `exists()`                              |
| Check file             | `isfile()` / `is_file()`                |
| Check directory        | `isdir()` / `is_dir()`                  |
| Build path             | `os.path.join()` / `Path / ...`         |
| Absolute path          | `os.path.abspath()` / `Path.absolute()` |
| Traverse tree          | `os.walk()`                             |
| Create directory       | `os.makedirs()` / `Path.mkdir()`        |
| Remove file            | `os.remove()` / `Path.unlink()`         |
| Remove empty directory | `os.rmdir()` / `Path.rmdir()`           |
| Copy file              | `shutil.copy()` / `copy2()`             |
| Copy directory         | `shutil.copytree()`                     |
| Move file/directory    | `shutil.move()`                         |
| Remove directory tree  | `shutil.rmtree()`                       |
| Temporary file         | `tempfile.NamedTemporaryFile()`         |
| Temporary workspace    | `tempfile.TemporaryDirectory()`         |

---

# 8. Key Concepts to Remember

## Path representation is not filesystem creation

```python
Path("run_001/logs/nvme.log")
```

does not create anything.

Similarly:

```python
os.path.join("run_001", "logs", "nvme.log")
```

only constructs a path.

Filesystem-changing operations include:

```python
mkdir()
touch()
write_text()
open(..., "w")
os.remove()
unlink()
shutil.copy()
shutil.move()
shutil.rmtree()
```

---

## File mode is separate from the context manager

```python
with open("file.txt", "w") as file:
```

contains:

```text
open(..., "w")
    → file opening/creation behavior

with
    → resource lifecycle management
```

---

## Preserve evidence before destructive cleanup

In failure scenarios:

```text
Failure
  ↓
Preserve diagnostic evidence
  ↓
Investigate
  ↓
Cleanup only disposable data
```

Do not blindly delete the test run simply because the test failed.

---

# 9. Completion Checklist

```text
✓ os
✓ pathlib
✓ shutil
✓ tempfile

✓ Directory creation
✓ File existence checks
✓ File/directory type checks
✓ Path construction
✓ Absolute paths
✓ Path components
✓ File read/write/append/create-only modes
✓ File deletion
✓ Empty-directory deletion
✓ Recursive traversal
✓ File copying
✓ Directory copying
✓ File/directory moving
✓ Recursive cleanup
✓ Temporary files
✓ Temporary directories
✓ Temporary vs permanent evidence
```

## BLOCK 1.2 — COMPLETED

