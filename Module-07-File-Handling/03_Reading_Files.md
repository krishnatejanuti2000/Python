## `03_Reading_Files.md`

Copy this into:

# 03 — Reading Files

## 1. Introduction

Python provides several ways to read data from a text file.

The main methods are:

- `read()`
- `readline()`
- `readlines()`
- Iterating directly over the file object

The correct method depends on:

- How much data needs to be processed.
- Whether the entire file is required.
- Whether processing should happen line-by-line.
- How large the file can become.

---

# 2. `read()`

`read()` reads the remaining contents of the file and returns them as a string.

Example:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read()

print(data)
```

If the file contains:

```text
TEST-101 PASS
TEST-102 FAIL
TEST-103 PASS
```

`data` contains the entire remaining file content as one `str`.

Conceptually:

```text
File
 ↓
read()
 ↓
Entire remaining content
 ↓
Python str
```

---

# 3. `read(size)`

`read()` can optionally receive a number specifying how many characters to read.

Example:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read(4)

print(data)
```

If the file begins with:

```text
TEST-101 PASS
```

the result is:

```text
TEST
```

Reading advances the current file position.

The next `read()` continues from that position.

---

# 4. `readline()`

`readline()` reads the next line from the current file position.

Example:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    line = file.readline()

print(line)
```

If the file contains:

```text
TEST-101 PASS
TEST-102 FAIL
```

the first call returns the first line.

A subsequent call:

```python
line = file.readline()
```

returns the next line.

---

# 5. Newline Behavior

A line returned by `readline()` normally includes its trailing newline character if one exists.

For example, the returned string may effectively be:

```python
"TEST-101 PASS\n"
```

Therefore:

```python
print(line)
```

can produce an extra blank line because:

* `line` already contains `\n`
* `print()` adds another newline

To avoid this:

```python
print(line, end="")
```

Alternatively:

```python
print(line.strip())
```

can remove surrounding whitespace.

Be aware that `strip()` removes whitespace from both ends, not just the newline.

---

# 6. `readlines()`

`readlines()` reads all remaining lines and returns them as a list of strings.

Example:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

print(lines)
```

For:

```text
TEST-101 PASS
TEST-102 FAIL
TEST-103 PASS
```

the result is conceptually:

```python
[
    "TEST-101 PASS\n",
    "TEST-102 FAIL\n",
    "TEST-103 PASS\n"
]
```

Each line becomes an element of the list.

---

# 7. Iterating Directly Over the File

A file object can be iterated over directly.

Example:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line, end="")
```

This processes the file sequentially, one line at a time.

This is usually preferred for large text files because it does not first create a complete list of all lines.

---

# 8. `read()` vs `readlines()` vs Iteration

| Method             | Result                 | Memory behavior          | Typical use                         |
| ------------------ | ---------------------- | ------------------------ | ----------------------------------- |
| `read()`           | One string             | Entire remaining content | Small/medium files                  |
| `readline()`       | One line               | Small                    | Controlled line-by-line reads       |
| `readlines()`      | List of lines          | Entire remaining content | When all lines are needed as a list |
| `for line in file` | One line per iteration | Incremental              | Large files/logs                    |

Important principle:

> Use the smallest amount of data you need to keep in memory.

---

# 9. Why Direct Iteration Is Important

Consider a very large log file:

```text
large.log
```

It could contain millions of lines.

Avoid unnecessarily doing:

```python
data = file.read()
```

if the program only needs to inspect each line.

Instead:

```python
with open("large.log", "r", encoding="utf-8") as file:
    for line in file:
        if "FAIL" in line:
            print(line, end="")
```

The program processes the log incrementally.

This is especially useful in test automation and log analysis.

---

# 10. Using `strip()`

Suppose:

```python
line = "TEST-101 PASS\n"
```

Then:

```python
cleaned = line.strip()
```

produces:

```text
TEST-101 PASS
```

This is commonly useful before parsing:

```python
test_id, status = cleaned.split()
```

However, remember that `strip()` removes whitespace from both ends.

It is not specifically a "remove newline" operation.

If only the trailing newline needs to be removed, other approaches can be more precise.

---

# 11. Reading and Parsing

File reading is often only the first step.

Example:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    for line in file:
        cleaned = line.strip()

        if not cleaned:
            continue

        test_id, status = cleaned.split()

        print("Test ID:", test_id)
        print("Status:", status)
```

Workflow:

```text
File
 ↓
Read line
 ↓
Clean line
 ↓
Parse fields
 ↓
Process data
```

This pattern is extremely common in automation.

---

# 12. File Position During Reading

Reading methods advance the current file position.

Example:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    print(file.tell())

    file.read(4)

    print(file.tell())
```

The position changes after reading.

The concepts of `tell()` and `seek()` are covered in:

`04_File_Position_tell_seek.md`

---

# 13. Reading Empty Files

If a file is empty:

```python
with open("empty.txt", "r", encoding="utf-8") as file:
    data = file.read()
```

then:

```python
data == ""
```

For `readline()`:

```python
line = file.readline()
```

at the end of the file returns:

```python
""
```

An empty string therefore indicates that no more data is available when using these reading operations.

---

# 14. End-of-File Concept

When the file position reaches the end:

```python
file.read()
```

returns:

```python
""
```

Similarly:

```python
file.readline()
```

returns:

```python
""
```

when there is no next line.

When iterating:

```python
for line in file:
    ...
```

Python naturally stops iteration at the end of the file.

---

# 15. Common Mistakes

## Mistake 1 — Printing a line with an extra newline

```python
print(line)
```

when `line` already contains `\n`.

Better when preserving the original line ending:

```python
print(line, end="")
```

---

## Mistake 2 — Loading a huge file unnecessarily

```python
data = file.read()
```

For a very large log, this can consume significant memory.

Prefer:

```python
for line in file:
    ...
```

when line-by-line processing is sufficient.

---

## Mistake 3 — Expecting `readlines()` to return strings without newlines

`readlines()` normally preserves the line endings that exist in the file.

For example:

```python
[
    "TEST-101 PASS\n",
    "TEST-102 FAIL\n"
]
```

You can clean individual lines when needed.

---

## Mistake 4 — Forgetting that reading advances the position

After:

```python
file.read()
```

the position is normally at the end of the consumed data.

A subsequent read starts from the new position.

Use `seek()` when you intentionally need to move back or elsewhere.

---

# 16. Automation Example — Count Failures

A simple test-result parser:

```python
from pathlib import Path

path = Path("results.txt")

failed_count = 0

with path.open("r", encoding="utf-8") as file:
    for line in file:
        if "FAIL" in line:
            failed_count += 1

print("Failed tests:", failed_count)
```

This demonstrates incremental processing.

For a controlled format such as:

```text
TEST-101 PASS
TEST-102 FAIL
```

more precise parsing can be used:

```python
test_id, status = line.strip().split()

if status == "FAIL":
    failed_count += 1
```

Exact parsing is generally preferable when the input format is known and structured.

---

# 17. Choosing the Reading Method

Ask what the program actually needs.

### Need the entire file as one string?

Use:

```python
read()
```

### Need one specific next line?

Use:

```python
readline()
```

### Need all lines as a list?

Use:

```python
readlines()
```

### Need to process a potentially large file?

Prefer:

```python
for line in file:
    ...
```

---

# 18. Key Takeaways

1. `read()` returns the remaining file content as a string.
2. `read(size)` reads a specified number of characters.
3. `readline()` reads one line.
4. `readlines()` returns all remaining lines as a list.
5. File objects can be iterated over directly.
6. Reading advances the file position.
7. Lines normally retain their trailing newline.
8. `print(line)` can therefore produce extra blank lines.
9. `strip()` is commonly used when cleaning lines before parsing.
10. Direct iteration is preferred for large files when line-by-line processing is sufficient.
11. Empty reads return an empty string at end-of-file.
12. File reading is commonly followed by parsing and validation.

---

# Interview Points

### What is the difference between `read()` and `readlines()`?

`read()` returns the remaining content as one string, while `readlines()` returns the remaining lines as a list of strings.

### Why is iterating directly over a file preferred for large logs?

It processes lines incrementally rather than loading the entire file or all lines into memory at once.

### Does `readline()` include the newline?

Normally, yes, if the line in the file ends with a newline.

### What happens when `readline()` reaches EOF?

It returns an empty string.

### What does `strip()` do?

It removes leading and trailing whitespace, including newline characters.

---

# Automation Principle

> Read only as much data as the task requires, and process large files incrementally whenever possible.


