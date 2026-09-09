
# 04 — File Position: `tell()` and `seek()`

## 1. Introduction

When Python opens a file, it maintains a current position within that file.

This position determines where the next read or write operation takes place.

Think of it as a cursor:

```text
TEST-101 PASS
^
current position
```

As data is read, the position moves forward.

The two important methods are:

* `tell()` — reports the current position.
* `seek()` — moves the current position.

---

# 2. `tell()`

`tell()` returns the current file position.

Example:

```python
from pathlib import Path

path = Path("results.txt")

with path.open("r", encoding="utf-8") as file:
    print(file.tell())
```

When the file is first opened, the position is normally:

```text
0
```

Therefore:

```python
file.tell()
```

returns:

```text
0
```

---

# 3. Reading Changes the Position

Consider:

```text
TEST-001 PASS
```

Suppose the program starts at position `0`.

```python
with path.open("r", encoding="utf-8") as file:
    print(file.tell())

    data = file.read(4)

    print(data)
    print(file.tell())
```

The first four characters are:

```text
TEST
```

The position then advances.

Conceptually:

```text
Before reading:

TEST-001 PASS
^
0


After read(4):

TEST-001 PASS
    ^
    4
```

Therefore:

> Reading consumes data and advances the current file position.

---

# 4. `seek()`

`seek()` moves the current file position.

Basic syntax:

```python
file.seek(position)
```

Example:

```python
with path.open("r", encoding="utf-8") as file:
    file.seek(5)
```

The next read begins from position `5`.

Important:

> `seek()` moves the position; it does not itself read data.

---

# 5. `seek(0)`

One of the most common uses is returning to the beginning.

```python
file.seek(0)
```

Example:

```python
with path.open("r", encoding="utf-8") as file:
    first = file.read(4)

    print(first)

    file.seek(0)

    second = file.read(4)

    print(second)
```

Both reads start from the beginning because `seek(0)` resets the position.

---

# 6. `tell()` + `seek()` Together

These methods are often used together when investigating or controlling file position.

Example:

```python
with path.open("r", encoding="utf-8") as file:
    print("Initial:", file.tell())

    file.read(4)

    print("After read:", file.tell())

    file.seek(0)

    print("After seek:", file.tell())
```

Conceptually:

```text
Open
 ↓
position = 0
 ↓
read()
 ↓
position moves forward
 ↓
seek(0)
 ↓
position = 0
```

---

# 7. Practical Example

Suppose:

```text
results.txt

TEST-001 PASS
TEST-002 FAIL
TEST-003 PASS
```

You can inspect positions:

```python
from pathlib import Path

path = Path("results.txt")

with path.open("r", encoding="utf-8") as file:

    print("Position:", file.tell())

    data = file.read(4)

    print("Read:", data)
    print("Position:", file.tell())

    file.seek(0)

    print("Position after seek:", file.tell())

    data = file.read(4)

    print("Read again:", data)
```

The important observation is not the exact numeric positions.

The important model is:

```text
tell() → Where am I?
seek() → Move me there.
```

---

# 8. File Position Is Independent of Path

A `Path` object represents where the file is located.

The file object's position represents where you currently are while accessing that file.

For example:

```python
path = Path("results.txt")
```

describes the file location.

After:

```python
with path.open("r", encoding="utf-8") as file:
```

`file` represents an open file resource with its own current position.

Therefore:

```text
Path
 ↓
Where is the file?

File object
 ↓
Where am I within the open file?
```

These are different concepts.

---

# 9. `seek()` Does Not Modify File Content

This is an important distinction.

Suppose:

```python
file.seek(10)
```

This does not:

* delete data
* insert data
* modify characters
* move the physical file

It only changes the current position used by subsequent operations.

For example:

```python
file.seek(10)
data = file.read()
```

means:

> Move to position 10, then read from there.

---

# 10. Position and Writing

File position also matters when writing.

For example, modes such as:

```text
r+
w+
a+
```

allow combinations of reading and writing.

In these situations, understanding the current file position becomes especially important.

For simple automation workflows, however, separate read/write operations using appropriate modes are often easier to reason about.

---

# 11. Common Mistakes

## Mistake 1 — Thinking `seek()` reads data

Incorrect understanding:

```python
file.seek(10)
```

does not read anything.

It only moves the position.

---

## Mistake 2 — Expecting another read to start from the beginning

Example:

```python
data = file.read()
data_again = file.read()
```

The second `read()` starts from the current position, which may already be EOF.

If you intentionally want to read again from the beginning:

```python
file.seek(0)
```

first.

---

## Mistake 3 — Confusing `tell()` with file size

`tell()` reports the current position.

It should not automatically be interpreted as "the size of the file."

For example, after reading part of a file:

```python
file.tell()
```

reports the current position, not necessarily the total file size.

---

# 12. Automation Relevance

Most normal automation scripts do not need frequent random positioning.

Line-by-line processing:

```python
with path.open("r", encoding="utf-8") as file:
    for line in file:
        process(line)
```

is often simpler.

However, `tell()` and `seek()` are useful when:

* Inspecting file positions.
* Re-reading content.
* Returning to a known location.
* Working with specific portions of a file.
* Understanding file I/O behavior.
* Working with certain read/write workflows.

---

# 13. Mental Model

Remember this simple model:

```text
              FILE
                │
                ▼
        Current Position
                │
       ┌────────┴────────┐
       │                 │
     tell()            seek()
       │                 │
       ▼                 ▼
  "Where am I?"      "Move here"
```

Reading generally moves the position forward:

```text
read()
  ↓
position advances
```

`seek()` changes it explicitly:

```text
seek(n)
  ↓
position = n
```

---

# 14. Key Takeaways

1. An open file has a current position.
2. The initial position is normally `0`.
3. Reading advances the current position.
4. `tell()` reports the current position.
5. `seek(n)` moves the current position to `n`.
6. `seek(0)` returns to the beginning.
7. `seek()` does not itself read or modify file content.
8. File position belongs to the open file object.
9. File position is different from the filesystem path.
10. Understanding file position is important when controlling sequential or random file access.

---

# Interview Points

### What does `tell()` do?

`tell()` returns the current position within the open file.

### What does `seek()` do?

`seek()` changes the current file position.

### What does `seek(0)` do?

It moves the current file position back to the beginning of the file.

### Does `seek()` read the file?

No. It only changes the current position.

### Does `tell()` return the file size?

Not necessarily. It returns the current file position.

### Why might you use `seek(0)`?

To return to the beginning so that subsequent reads start from the beginning again.

---

# Automation Principle

> Know where the file position is, and deliberately control it when your workflow requires non-sequential access.


