
# 08 — `pathlib`

## 1. Introduction

`pathlib` is Python's modern, object-oriented approach to working with filesystem paths.

Instead of treating paths only as strings, `pathlib` provides `Path` objects with methods for:

- Checking paths
- Opening files
- Creating directories
- Traversing directories
- Renaming files
- Deleting files
- Building paths
- Inspecting path components

Import:

```python
from pathlib import Path
```

---

# 2. Creating a `Path` Object

Example:

```python
from pathlib import Path

path = Path("results.txt")
```

This creates a `Path` object representing:

```text
results.txt
```

Important:

> Creating a `Path` object does not create the actual file.

It only represents the filesystem location.

---

# 3. Relative Paths

A relative path is interpreted relative to the process's current working directory.

Example:

```python
path = Path("results.txt")
```

If the current working directory is:

```text
/home/user/Documents/Python
```

then the relative path refers to:

```text
/home/user/Documents/Python/results.txt
```

The path itself remains relative until resolved.

---

# 4. Absolute Paths

An absolute path specifies the complete filesystem location.

Example:

```python
path = Path("/home/user/Documents/Python/results.txt")
```

It does not depend on the current working directory for interpretation.

---

# 5. `Path.cwd()`

`Path.cwd()` returns the process's current working directory.

Example:

```python
from pathlib import Path

current_directory = Path.cwd()

print(current_directory)
```

Example output:

```text
/home/user/Documents/Python
```

Important:

> `cwd()` means the current working directory of the running process.

It does not mean "the directory where the Python file is stored."

---

# 6. `exists()`

`exists()` checks whether something exists at the specified path.

Example:

```python
from pathlib import Path

path = Path("results.txt")

print(path.exists())
```

Possible result:

```text
True
```

or:

```text
False
```

It can refer to either a file or a directory.

---

# 7. `is_file()`

`is_file()` checks whether the path represents a regular file.

Example:

```python
if path.is_file():
    print("This is a file")
```

This is more specific than `exists()`.

---

# 8. `is_dir()`

`is_dir()` checks whether the path represents a directory.

Example:

```python
directory = Path("Practice")

if directory.is_dir():
    print("This is a directory")
```

---

# 9. `exists()` vs `is_file()` vs `is_dir()`

These methods answer different questions:

```text
exists()
    ↓
Does anything exist here?

is_file()
    ↓
Is it a file?

is_dir()
    ↓
Is it a directory?
```

Example:

```python
path.exists()
path.is_file()
path.is_dir()
```

Do not confuse:

```python
path.exists
```

with:

```python
path.exists()
```

The first refers to the method itself.

The second actually calls the method.

---

# 10. `resolve()`

`resolve()` produces a resolved absolute path.

Example:

```python
from pathlib import Path

path = Path("results.txt")

print(path)
print(path.resolve())
```

Possible output:

```text
results.txt
/home/user/Documents/Python/results.txt
```

`resolve()` does not:

* Move the file
* Copy the file
* Rename the file
* Create the file

It only resolves the path representation.

---

# 11. Joining Paths

One of the most useful `pathlib` features is joining paths using `/`.

Example:

```python
from pathlib import Path

results_dir = Path("results")
result_file = results_dir / "results.txt"
```

The resulting path represents:

```text
results/results.txt
```

Another example:

```python
project = Path("Enterprise_Project")
module = "Module7"
report = "final_report.txt"

result = project / module / report
```

Result:

```text
Enterprise_Project/Module7/final_report.txt
```

---

# 12. Why Use `/` Instead of String Concatenation?

Avoid manually constructing filesystem paths like:

```python
path = "results/" + "results.txt"
```

`pathlib` handles path joining appropriately for the operating system.

Preferred:

```python
path = Path("results") / "results.txt"
```

This is cleaner and safer.

---

# 13. Path Components

A `Path` object provides useful information about its components.

Example:

```python
from pathlib import Path

path = Path("Practice/reports/final_report.txt")
```

### `.name`

Returns the final component:

```python
path.name
```

Result:

```text
final_report.txt
```

---

### `.parent`

Returns the containing directory:

```python
path.parent
```

Result:

```text
Practice/reports
```

---

### `.stem`

Returns the filename without its final extension:

```python
path.stem
```

Result:

```text
final_report
```

---

### `.suffix`

Returns the final file extension:

```python
path.suffix
```

Result:

```text
.txt
```

---

# 14. Path Component Example

For:

```text
Practice/reports/final_report.txt
```

we can think of:

```text
name   → final_report.txt
parent → Practice/reports
stem   → final_report
suffix → .txt
```

This is useful when automation needs to inspect or generate filenames dynamically.

---

# 15. Opening Files with `Path.open()`

A `Path` object can directly open the file it represents.

Example:

```python
from pathlib import Path

path = Path("results.txt")

with path.open("r", encoding="utf-8") as file:
    content = file.read()

print(content)
```

This is equivalent in purpose to:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    content = file.read()
```

The difference is that the first approach starts with a `Path` object.

---

# 16. Why `pathlib` Is Useful in Automation

Automation frequently constructs paths dynamically.

For example:

```text
Project
 ├── Module7
 │   ├── results
 │   ├── logs
 │   └── reports
```

A program can construct these locations:

```python
project = Path("Project")
module = project / "Module7"

results = module / "results"
logs = module / "logs"
reports = module / "reports"
```

This is much cleaner than manually concatenating strings.

---

# 17. Path Objects vs Strings

A string:

```python
path = "Practice/results.txt"
```

is simply text.

A `Path`:

```python
path = Path("Practice/results.txt")
```

represents a filesystem path and provides filesystem-oriented operations.

For example:

```python
path.exists()
path.is_file()
path.parent
path.name
path.suffix
path.resolve()
```

This is one of the main advantages of `pathlib`.

---

# 18. Dynamic Path Construction

Automation often needs paths based on variables.

Example:

```python
from pathlib import Path

project = Path("Enterprise_Project")
module = "Module7"
report = "final_report.txt"

report_path = project / module / report

print(report_path)
```

This produces:

```text
Enterprise_Project/Module7/final_report.txt
```

The components can come from configuration, command-line arguments, test metadata, or other runtime data.

---

# 19. Common Mistakes

## Mistake 1 — Thinking `Path()` creates a file

```python
path = Path("results.txt")
```

does not create the file.

It only creates a Python representation of the path.

---

## Mistake 2 — Forgetting parentheses

Incorrect:

```python
path.exists
```

Correct:

```python
path.exists()
```

`exists` is a method.

---

## Mistake 3 — Confusing `cwd()` with the script directory

```python
Path.cwd()
```

returns the process's current working directory.

It does not necessarily return the directory containing the Python script.

---

## Mistake 4 — Using string concatenation for paths

Avoid:

```python
path = "Practice/" + "results/" + "test.txt"
```

Prefer:

```python
path = Path("Practice") / "results" / "test.txt"
```

---

# 20. Practical Automation Example

A common pattern:

```python
from pathlib import Path

project_dir = Path("Storage_Project")
results_dir = project_dir / "results"
report_file = results_dir / "final_report.txt"

print("Project:", project_dir)
print("Results directory:", results_dir)
print("Report:", report_file)
print("Report exists:", report_file.exists())
```

The program can construct and inspect the entire path structure without manually manipulating path strings.

---

# 21. Key Takeaways

1. `pathlib` provides an object-oriented way to work with filesystem paths.
2. `Path()` creates a path object, not the actual filesystem object.
3. Relative paths are interpreted relative to the current working directory.
4. Absolute paths specify the complete location.
5. `Path.cwd()` returns the process's current working directory.
6. `exists()` checks whether something exists at a path.
7. `is_file()` checks for a regular file.
8. `is_dir()` checks for a directory.
9. `resolve()` produces a resolved absolute path.
10. `/` is used to join path components.
11. `.name` returns the final filename.
12. `.parent` returns the containing directory.
13. `.stem` returns the filename without its final extension.
14. `.suffix` returns the final extension.
15. `Path.open()` can be used to open files represented by `Path` objects.
16. `pathlib` makes dynamic path construction cleaner and more portable.

---

# Interview Points

### What is `pathlib`?

`pathlib` is Python's object-oriented API for filesystem paths.

### Does `Path("file.txt")` create a file?

No. It creates a `Path` object representing that location.

### What does `Path.cwd()` return?

The current working directory of the running process.

### What is the difference between `exists()` and `is_file()`?

`exists()` checks whether anything exists at the path, while `is_file()` specifically checks whether the path represents a regular file.

### Why use `Path / "filename"`?

It provides a clean and portable way to join filesystem path components.

### What does `resolve()` do?

It resolves a path into an absolute/resolved filesystem path representation. It does not move or copy the file.

---

# Automation Principle

> Treat filesystem paths as structured objects rather than manually constructed strings.



