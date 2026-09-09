
# 07 — Context Managers

## 1. Introduction

A context manager provides a structured way to acquire a resource, use it, and guarantee appropriate cleanup.

File handling is one of the most common uses of context managers in Python.

The preferred pattern is:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read()
```

The context manager ensures that the file resource is properly closed when the `with` block finishes.

---

# 2. Why Context Managers Matter

A file is an external resource.

When Python opens a file, it obtains access to an underlying operating-system resource.

The general lifecycle is:

```text
Acquire resource
      ↓
Use resource
      ↓
Release resource
```

For files:

```text
open()
  ↓
read/write
  ↓
close()
```

A context manager automates the cleanup portion of this lifecycle.

---

# 3. The `with` Statement

Basic syntax:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read()
```

The file is available inside the `with` block.

After leaving the block, Python exits the context and the file resource is closed.

---

# 4. Why Not Manually Call `close()`?

This approach is possible:

```python
file = open("results.txt", "r", encoding="utf-8")

data = file.read()

file.close()
```

But it becomes unsafe if an exception occurs before `close()`:

```python
file = open("results.txt", "r", encoding="utf-8")

data = file.read()

# An exception occurs here

file.close()
```

The `close()` statement may never execute.

A context manager handles cleanup even when an exception occurs inside the block.

Preferred:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read()
```

---

# 5. Exception Safety

Consider:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read()

    raise RuntimeError("Processing failed")
```

The exception interrupts normal execution.

However, exiting the `with` block still causes the context manager to perform its cleanup.

This is one of the major reasons context managers are valuable.

---

# 6. `__enter__()` and `__exit__()`

Context managers implement two special methods:

```python
__enter__()
__exit__()
```

Conceptually, when Python executes:

```python
with resource as value:
    ...
```

the context manager performs operations similar to:

```text
Enter context
     ↓
Use resource
     ↓
Exit context
     ↓
Cleanup
```

For file objects, the `with` statement handles the resource lifecycle for you.

You normally do not need to call `__enter__()` or `__exit__()` yourself.

---

# 7. What `as file` Means

Consider:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read()
```

The expression:

```python
open(...)
```

produces the file object.

The `as file` portion assigns the context manager's entered resource to the variable:

```python
file
```

You then use that variable inside the block.

---

# 8. Scope of the `with` Block

The file is intended to be used inside the context:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read()
    print(data)
```

After the block:

```python
# file resource has been closed
```

The cleanup has already occurred.

The important rule is:

> Perform file operations while the file is inside its active context.

---

# 9. Checking Whether a File Is Closed

A file object provides the `closed` attribute.

Example:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    print(file.closed)

print(file.closed)
```

Inside the context, the file is normally open:

```text
False
```

After the context ends:

```text
True
```

This demonstrates that the context manager has closed the file resource.

---

# 10. Context Managers Are Not Limited to Files

The same pattern is useful for many resources.

Examples include:

* Files
* Database connections
* Locks
* Network resources
* Temporary resources

The general principle is:

```text
Acquire
   ↓
Use
   ↓
Guaranteed cleanup
```

Therefore, understanding context managers is an important general Python skill, not merely a file-handling feature.

---

# 11. Context Manager and Resource Lifetime

An important distinction:

### Python object lifetime

The Python file object is a Python object managed by Python's object/lifetime mechanisms.

### Resource lifetime

The underlying file resource is open while it is being used and is closed when the context exits.

These are not necessarily the same concept.

For normal file handling, the important requirement is:

> Ensure the underlying file resource is closed promptly and reliably.

The `with` statement provides this behavior.

---

# 12. Multiple Files

Multiple resources can be managed using context managers.

For example:

```python
with open("expected.txt", "r", encoding="utf-8") as expected_file:
    with open("actual.txt", "r", encoding="utf-8") as actual_file:
        expected = expected_file.read()
        actual = actual_file.read()
```

Both resources are managed by their respective contexts.

The code can also be structured using multiple context managers in one `with` statement:

```python
with (
    open("expected.txt", "r", encoding="utf-8") as expected_file,
    open("actual.txt", "r", encoding="utf-8") as actual_file
):
    expected = expected_file.read()
    actual = actual_file.read()
```

The important concept is the same:

> Each acquired resource has a defined cleanup lifecycle.

---

# 13. Context Managers and Writing

Context managers are equally important when writing.

Example:

```python
with open("report.txt", "w", encoding="utf-8") as file:
    file.write("Storage Test Report\n")
```

When the block finishes, the file is closed.

This is especially important for output files because closing the file is part of properly completing the file operation.

---

# 14. Context Managers with `pathlib`

The same principle works with `Path.open()`:

```python
from pathlib import Path

path = Path("results.txt")

with path.open("r", encoding="utf-8") as file:
    data = file.read()
```

This combines two important Module 7 practices:

```text
pathlib
   +
context manager
   +
file handling
```

---

# 15. Common Mistakes

## Mistake 1 — Forgetting the `with` statement

Manual management:

```python
file = open("results.txt", "r")
data = file.read()
file.close()
```

This can work, but cleanup becomes the programmer's responsibility.

Preferred:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read()
```

---

## Mistake 2 — Doing file operations after the context

For example:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read()

file.read()
```

The file resource has already been closed.

File operations should normally occur inside the appropriate context.

---

## Mistake 3 — Assuming `with` prevents every exception

A context manager guarantees appropriate cleanup.

It does not automatically prevent or solve every exception.

For example:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    data = file.read()

    raise ValueError("Invalid data")
```

The `ValueError` still occurs.

The important benefit is that the resource is properly cleaned up while the exception propagates.

Exception handling itself is covered in Module 8.

---

# 16. Automation Relevance

Reliable resource management is critical in automation.

A test automation framework may open:

* Result files
* Log files
* Configuration files
* Temporary files
* Multiple input/output files

If resources are not properly managed, long-running automation can encounter problems such as:

* Resource exhaustion
* File locking issues
* Incomplete writes
* Unexpected access failures

Using context managers reduces these risks.

---

# 17. Practical Automation Pattern

A typical automation operation:

```python
from pathlib import Path

result_path = Path("results.txt")

with result_path.open("r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if "FAIL" in line:
            print("Failure:", line)
```

The lifecycle is:

```text
Path identified
      ↓
File opened
      ↓
Results processed
      ↓
Context exits
      ↓
File resource closed
```

This is the standard pattern to prefer.

---

# 18. Key Takeaways

1. A context manager manages a resource lifecycle.
2. `with` is the standard syntax for using context managers.
3. File objects are common context managers.
4. Context managers ensure file resources are properly closed.
5. Cleanup occurs even when an exception interrupts the block.
6. `__enter__()` and `__exit__()` are the core context-manager protocol methods.
7. `as file` provides the entered resource through a variable.
8. File operations should normally occur inside the `with` block.
9. Context managers are useful beyond file handling.
10. Context managers improve reliability and resource safety in automation.

---

# Interview Points

### Why should you use `with open(...)`?

It ensures that the file resource is properly closed when the context ends, including when an exception occurs.

### What are `__enter__()` and `__exit__()`?

They are the core methods used by Python's context-manager protocol to establish and clean up a managed context.

### Does a context manager prevent exceptions?

No. It guarantees appropriate cleanup; exceptions can still propagate unless they are explicitly handled or suppressed.

### What happens when a `with` block ends?

The context manager's exit logic executes, and for a file context this closes the file resource.

### Can context managers be used for resources other than files?

Yes. They can manage many resources such as database connections, locks, and other external resources.

---

# Automation Principle

> Acquire resources safely, use them within a controlled context, and guarantee cleanup when the operation ends.



