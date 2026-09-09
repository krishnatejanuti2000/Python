
# 02 — File Modes

## 1. What Is a File Mode?

A file mode tells Python how the program intends to interact with a file.

The mode controls things such as:

- Whether the file is being read or written.
- Whether existing content is preserved.
- Whether existing content is truncated.
- Whether a missing file is created.
- Whether creation must be exclusive.

Basic syntax:

```python
open("filename.txt", "mode")
```

Example:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read()
```

---

# 2. Common File Modes

The most important text modes are:

| Mode | Purpose          | Missing file | Existing content |
| ---- | ---------------- | ------------ | ---------------- |
| `r`  | Read             | Error        | Preserved        |
| `w`  | Write            | Created      | Truncated        |
| `a`  | Append           | Created      | Preserved        |
| `x`  | Exclusive create | Created      | Error            |

The default mode is:

```python
r
```

---

# 3. `r` — Read Mode

Use `r` when you want to read an existing file.

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read()
```

### Behavior

If the file exists:

* It can be read.
* Existing content is preserved.
* The file is not writable through this mode.

If the file does not exist:

```text
FileNotFoundError
```

Example:

```python
open("missing.txt", "r")
```

results in a `FileNotFoundError`.

### Important principle

`r` does **not** create a missing file.

---

# 4. `w` — Write Mode

Use `w` when you want to write a new file or replace the contents of an existing file.

```python
with open("results.txt", "w", encoding="utf-8") as file:
    file.write("TEST-101 PASS\n")
```

### If the file does not exist

Python creates it.

### If the file already exists

Its existing contents are truncated when the file is opened for writing.

For example, suppose the file initially contains:

```text
TEST-101 PASS
TEST-102 FAIL
```

Then:

```python
with open("results.txt", "w", encoding="utf-8") as file:
    file.write("TEST-103 PASS\n")
```

The resulting file contains only:

```text
TEST-103 PASS
```

The previous contents were replaced.

### Important warning

`w` is destructive to existing file contents.

Use it intentionally.

---

# 5. `a` — Append Mode

Use `a` when you want to add data to the end of a file while preserving existing contents.

```python
with open("results.txt", "a", encoding="utf-8") as file:
    file.write("TEST-103 PASS\n")
```

If the file already contains:

```text
TEST-101 PASS
TEST-102 FAIL
```

the result becomes:

```text
TEST-101 PASS
TEST-102 FAIL
TEST-103 PASS
```

### If the file does not exist

Python creates it.

### Important point

Append mode writes at the end of the file.

It does not automatically add a newline.

Therefore:

```python
file.write("TEST-103 PASS")
```

does not guarantee that the next record starts on a new line.

If records are line-based, explicitly include:

```python
"\n"
```

Example:

```python
file.write("TEST-103 PASS\n")
```

---

# 6. Append Boundary Edge Case

Suppose an existing file contains:

```text
TEST-101 PASS
```

but does not end with a newline.

Then:

```python
with open("results.txt", "a", encoding="utf-8") as file:
    file.write("TEST-102 FAIL\n")
```

can produce:

```text
TEST-101 PASSTEST-102 FAIL
```

The two records become concatenated.

Therefore, a robust appender may need to consider whether the existing file already ends with a newline before adding a new record.

This matters when files may have been created by different programs or tools.

---

# 7. `x` — Exclusive Creation

Use `x` when you want to create a new file and require that the file must not already exist.

```python
with open("results.txt", "x", encoding="utf-8") as file:
    file.write("TEST-101 PASS\n")
```

### If the file does not exist

The file is created.

### If the file already exists

Python raises:

```text
FileExistsError
```

This makes `x` useful when overwriting an existing file would be dangerous.

---

# 8. Default Mode

If no mode is specified:

```python
open("results.txt")
```

Python uses:

```python
r
```

So this:

```python
open("results.txt")
```

is effectively:

```python
open("results.txt", "r")
```

For clarity, explicitly specifying the mode is often preferable.

---

# 9. File Mode and Encoding Are Different

Consider:

```python
with open(
    "results.txt",
    "r",
    encoding="utf-8"
) as file:
    data = file.read()
```

There are two separate concepts here.

### Mode

```python
"r"
```

determines how the file is accessed.

### Encoding

```python
encoding="utf-8"
```

determines how text bytes are interpreted as characters.

Therefore:

> `r` is an access mode; `utf-8` is a text encoding.

They solve different problems.

---

# 10. Binary Modes

The common binary equivalents are:

| Mode | Meaning       |
| ---- | ------------- |
| `rb` | Read binary   |
| `wb` | Write binary  |
| `ab` | Append binary |

Example:

```python
with open("data.bin", "rb") as file:
    data = file.read()
```

Binary mode returns bytes rather than text strings.

Example:

```python
type(data)
```

would normally be:

```python
bytes
```

Binary files are outside the main focus of this module, which primarily deals with text and structured automation data.

---

# 11. Read/Write Combination Modes

Python also supports modes that combine reading and writing.

Examples include:

```text
r+
w+
a+
```

Their general meanings are:

| Mode | Meaning                                  |
| ---- | ---------------------------------------- |
| `r+` | Read and write existing file             |
| `w+` | Read and write, truncating/creating file |
| `a+` | Read and append, creating if needed      |

These modes require careful understanding of the file position and are not necessary for most straightforward automation tasks.

Prefer the simplest mode that correctly expresses the intended operation.

---

# 12. Common Mistakes

## Mistake 1 — Using `r` for a missing file

```python
open("new_file.txt", "r")
```

If the file doesn't exist:

```text
FileNotFoundError
```

---

## Mistake 2 — Accidentally using `w`

Suppose you want to add a result:

```python
with open("results.txt", "w") as file:
    file.write("TEST-105 PASS\n")
```

If `results.txt` already contains important results, they will be truncated.

If the intention is to add a record, use:

```python
"a"
```

instead.

---

## Mistake 3 — Assuming append adds a newline

It doesn't.

This:

```python
file.write("TEST-105 PASS")
```

doesn't automatically add:

```text
\n
```

---

## Mistake 4 — Using `x` when the file may already exist

```python
open("results.txt", "x")
```

fails if the file already exists.

That's the intended behavior of exclusive creation.

---

# 13. Automation Examples

### Read existing test results

```python
with open("results.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line)
```

### Create a new report

```python
with open("report.txt", "w", encoding="utf-8") as file:
    file.write("Test Report\n")
```

### Add a new test result

```python
with open("results.txt", "a", encoding="utf-8") as file:
    file.write("TEST-106 PASS\n")
```

### Require a new file

```python
with open("run.lock", "x", encoding="utf-8") as file:
    file.write("RUNNING\n")
```

The last pattern can be useful when accidental overwriting must be prevented.

---

# 14. File Mode Decision Guide

When deciding which mode to use, ask:

### Do I only need to read?

```text
r
```

### Do I want to replace the existing contents?

```text
w
```

### Do I want to add to the existing contents?

```text
a
```

### Do I need to create a new file and fail if it already exists?

```text
x
```

---

# 15. Key Takeaways

1. File mode defines how Python accesses a file.
2. `r` reads an existing file.
3. `w` writes and truncates existing content.
4. `a` preserves existing content and writes at the end.
5. `x` creates a new file and fails if it already exists.
6. `r` raises `FileNotFoundError` for a missing file.
7. `w` and `a` create a file if it doesn't exist.
8. `x` raises `FileExistsError` when the file already exists.
9. Append mode does not automatically add newlines.
10. Mode and encoding are separate concepts.
11. Binary modes use `b`, such as `rb`, `wb`, and `ab`.
12. Choose the simplest mode that matches the intended operation.

---

# Interview Points

### What happens when you open an existing file with `w`?

The existing contents are truncated when the file is opened for writing.

### What is the difference between `w` and `a`?

`w` replaces/truncates existing contents, while `a` preserves existing contents and writes new data at the end.

### What happens when you use `r` on a missing file?

Python raises `FileNotFoundError`.

### What is the purpose of `x`?

It creates a new file only if the file does not already exist. If it exists, Python raises `FileExistsError`.

### Does append mode automatically add a newline?

No. The program must write the newline explicitly when line separation is required.

---

# Automation Principle

> Choose the file mode based on the intended data lifecycle: read, replace, append, or exclusive creation.


