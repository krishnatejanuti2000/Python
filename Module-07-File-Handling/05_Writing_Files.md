
# 05 — Writing Files

## 1. Introduction

Python provides file-writing operations for storing data persistently.

The primary method is:

```python
file.write()
```

Writing is commonly used in automation for:

* Test results
* Reports
* Logs
* Generated configuration
* Command output
* Validation records

---

# 2. Opening a File for Writing

Use write mode:

```python
with open("results.txt", "w", encoding="utf-8") as file:
    file.write("TEST-101 PASS\n")
```

If the file does not exist, Python creates it.

If it already exists, its contents are truncated when opened in `w` mode.

Therefore, use `w` when replacing the existing contents is intentional.

---

# 3. `write()`

`write()` writes a string to the file.

Example:

```python
with open("results.txt", "w", encoding="utf-8") as file:
    file.write("TEST-101 PASS\n")
    file.write("TEST-102 FAIL\n")
```

The resulting file:

```text
TEST-101 PASS
TEST-102 FAIL
```

---

# 4. `write()` Expects a String

In text mode, `write()` expects a string.

This is valid:

```python
file.write("100")
```

This is also valid:

```python
file.write(str(100))
```

But this is invalid:

```python
file.write(100)
```

because `100` is an integer, not a string.

For formatted values, f-strings are convenient:

```python
test_id = "TEST-101"
status = "PASS"

file.write(f"{test_id} {status}\n")
```

---

# 5. `write()` Does Not Add a Newline

This:

```python
file.write("TEST-101 PASS")
file.write("TEST-102 FAIL")
```

produces:

```text
TEST-101 PASSTEST-102 FAIL
```

because `write()` writes exactly the supplied string.

To separate records:

```python
file.write("TEST-101 PASS\n")
file.write("TEST-102 FAIL\n")
```

produces:

```text
TEST-101 PASS
TEST-102 FAIL
```

Important principle:

> `write()` does not automatically add formatting or line breaks.

---

# 6. Writing a List of Results

Suppose:

```python
results = [
    "TEST-101 PASS",
    "TEST-102 FAIL",
    "TEST-103 PASS"
]
```

You can write each record:

```python
with open("results.txt", "w", encoding="utf-8") as file:
    for result in results:
        file.write(result + "\n")
```

Result:

```text
TEST-101 PASS
TEST-102 FAIL
TEST-103 PASS
```

This is a common pattern for simple line-based automation output.

---

# 7. Returning the Number of Characters Written

In text mode, `write()` returns the number of characters written.

Example:

```python
with open("results.txt", "w", encoding="utf-8") as file:
    count = file.write("TEST-101 PASS\n")

print(count)
```

The returned value represents the number of characters accepted by the text stream for that write operation.

It should not automatically be interpreted as the number of bytes stored on disk.

Encoding can affect the relationship between characters and encoded bytes.

---

# 8. `writelines()`

`writelines()` writes an iterable of strings.

Example:

```python
results = [
    "TEST-101 PASS\n",
    "TEST-102 FAIL\n",
    "TEST-103 PASS\n"
]

with open("results.txt", "w", encoding="utf-8") as file:
    file.writelines(results)
```

The resulting file:

```text
TEST-101 PASS
TEST-102 FAIL
TEST-103 PASS
```

---

# 9. `writelines()` Does Not Add Newlines

This is important.

Given:

```python
results = [
    "TEST-101 PASS",
    "TEST-102 FAIL"
]
```

doing:

```python
file.writelines(results)
```

does not automatically produce separate lines.

The strings must already contain their required separators:

```python
results = [
    "TEST-101 PASS\n",
    "TEST-102 FAIL\n"
]
```

Therefore:

> `writelines()` writes the supplied strings as they are.

---

# 10. `write()` vs `writelines()`

### `write()`

Writes one string:

```python
file.write("TEST-101 PASS\n")
```

### `writelines()`

Writes multiple strings from an iterable:

```python
file.writelines([
    "TEST-101 PASS\n",
    "TEST-102 FAIL\n"
])
```

Comparison:

| Method         | Input               | Adds newline automatically? |
| -------------- | ------------------- | --------------------------- |
| `write()`      | One string          | No                          |
| `writelines()` | Iterable of strings | No                          |

---

# 11. Writing Formatted Results

Automation frequently generates structured output.

Example:

```python
test_id = "TEST-101"
status = "PASS"
duration = 10.5

with open("results.txt", "w", encoding="utf-8") as file:
    file.write(f"{test_id} {status} {duration}\n")
```

Result:

```text
TEST-101 PASS 10.5
```

This is useful when generating simple human-readable reports or intermediate result files.

For true tabular data, however, using the CSV module is generally better than manually constructing CSV strings.

---

# 12. Writing Through `Path`

Since `pathlib` is part of this module, the same operation can be written as:

```python
from pathlib import Path

path = Path("results.txt")

with path.open("w", encoding="utf-8") as file:
    file.write("TEST-101 PASS\n")
```

This is particularly convenient when the program is already using `Path` objects.

---

# 13. Writing a Report

Example:

```python
from pathlib import Path

report_path = Path("Practice/test_report.txt")

with report_path.open("w", encoding="utf-8") as file:
    file.write("Storage Test Execution Report\n")
    file.write("==============================\n\n")
    file.write("Total Tests : 5\n")
    file.write("Passed      : 3\n")
    file.write("Failed      : 2\n")
```

Generated report:

```text
Storage Test Execution Report
==============================

Total Tests : 5
Passed      : 3
Failed      : 2
```

This is a simple example of file writing in an automation workflow.

---

# 14. Common Mistakes

## Mistake 1 — Passing a non-string to `write()`

Incorrect:

```python
file.write(100)
```

Correct:

```python
file.write(str(100))
```

or:

```python
file.write(f"{100}")
```

---

## Mistake 2 — Forgetting the newline

Incorrect:

```python
file.write("TEST-101 PASS")
file.write("TEST-102 FAIL")
```

Correct:

```python
file.write("TEST-101 PASS\n")
file.write("TEST-102 FAIL\n")
```

---

## Mistake 3 — Using `w` when you intended to append

Incorrect when preserving previous results:

```python
with open("results.txt", "w") as file:
    file.write("TEST-105 PASS\n")
```

If the file already contains results, they are truncated.

Use append mode when the requirement is to add new data:

```python
with open("results.txt", "a", encoding="utf-8") as file:
    file.write("TEST-105 PASS\n")
```

---

## Mistake 4 — Expecting `writelines()` to add newlines

Incorrect:

```python
file.writelines([
    "TEST-101 PASS",
    "TEST-102 FAIL"
])
```

The strings do not automatically become separate lines.

Correct:

```python
file.writelines([
    "TEST-101 PASS\n",
    "TEST-102 FAIL\n"
])
```

---

# 15. Automation Pattern

A simple result-writing function can be structured as:

```python
from pathlib import Path

def write_results(filename, results):
    path = Path(filename)

    with path.open("w", encoding="utf-8") as file:
        for result in results:
            file.write(result + "\n")
```

Example:

```python
results = [
    "TEST-101 PASS",
    "TEST-102 FAIL",
    "TEST-103 PASS"
]

write_results("results.txt", results)
```

This separates the file-writing operation into a reusable function.

---

# 16. Key Takeaways

1. `write()` writes a string to a file.
2. Text-mode `write()` expects a string.
3. `write()` does not automatically add a newline.
4. `write()` returns the number of characters written to the text stream.
5. `writelines()` writes multiple strings from an iterable.
6. `writelines()` does not automatically add newlines.
7. `w` mode creates a missing file but truncates an existing file.
8. Use `a` when existing content must be preserved and new records added.
9. f-strings are useful for writing formatted automation results.
10. `Path.open()` can be used when working with `pathlib`.
11. Structured formats such as CSV should generally use their dedicated Python modules rather than manual string construction.

---

# Interview Points

### What does `write()` accept in text mode?

A string.

### Does `write()` automatically add a newline?

No.

### What does `writelines()` do?

It writes each string from an iterable to the file.

### Does `writelines()` add newlines?

No. The strings must contain the required newline characters.

### What does `write()` return?

In text I/O, it returns the number of characters written to the text stream.

### What happens if `write()` is used with an integer?

It raises a `TypeError` because text-mode `write()` expects a string.

---

# Automation Principle

> Generate output deliberately: choose the correct file mode, write the correct data type, and explicitly control record boundaries such as newlines.



