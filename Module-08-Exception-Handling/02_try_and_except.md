# 02 — try and except

## Objective

The `try` and `except` statements are the foundation of Python exception handling.

By the end of this document, you should understand:

- What `try` does
- What `except` does
- How Python executes `try`
- What happens when an exception occurs
- What happens when no exception occurs
- Catching specific exceptions
- Using `as` to access the exception object
- Multiple `except` blocks
- What should and should not be placed inside `try`
- Why broad exception handling is dangerous
- How to design reliable exception handling for automation

---

# 1. Basic Syntax

The basic structure is:

```python
try:
    # code that may raise an exception
except:
    # handle the exception
````

Example:

```python
try:
    result = 10 / 0
except:
    print("Something went wrong")
```

Output:

```text
Something went wrong
```

---

# 2. What Does `try` Mean?

`try` tells Python:

> Execute this block and watch for exceptions.

Example:

```python
try:
    value = int("100")
```

If the operation succeeds, execution continues.

If an exception occurs, Python looks for a matching `except`.

---

# 3. What Does `except` Mean?

`except` defines what Python should do when an exception occurs in the associated `try` block.

Example:

```python
try:
    value = int("abc")
except ValueError:
    print("Invalid integer")
```

Output:

```text
Invalid integer
```

---

# 4. Execution Flow — No Exception

Consider:

```python
print("A")

try:
    print("B")
    value = 10 + 20
    print("C")
except ValueError:
    print("D")

print("E")
```

Execution:

```text
A
B
C
E
```

Because no exception occurred:

```text
try
 ↓
successful
 ↓
skip except
 ↓
continue
```

---

# 5. Execution Flow — Exception

Consider:

```python
print("A")

try:
    print("B")
    value = int("abc")
    print("C")
except ValueError:
    print("D")

print("E")
```

Output:

```text
A
B
D
E
```

Notice:

```python
print("C")
```

was never executed.

Why?

Because:

```text
int("abc")
     ↓
ValueError
     ↓
remaining try block is skipped
     ↓
matching except executes
```

---

# 6. The Most Important Execution Rule

When an exception occurs inside `try`:

```text
Execution stops at the failing statement.
        ↓
Python searches for a matching except.
        ↓
Matching except executes.
        ↓
Execution continues after the try/except structure.
```

Example:

```python
try:
    print("1")
    10 / 0
    print("2")
except ZeroDivisionError:
    print("3")

print("4")
```

Output:

```text
1
3
4
```

`2` is never printed.

---

# 7. Catch a Specific Exception

Prefer:

```python
try:
    value = int("abc")
except ValueError:
    print("Invalid number")
```

over:

```python
try:
    value = int("abc")
except:
    print("Something went wrong")
```

Why?

Because the first version explicitly describes the failure we expect.

---

# 8. Why Specific Exceptions Are Better

Consider:

```python
try:
    value = int(user_input)
except ValueError:
    print("Invalid numeric input")
```

This handles exactly the problem we expect:

```text
String cannot be converted to integer
```

It does not hide unrelated programming errors.

This is an important production principle:

```text
Catch what you understand.
Let unexpected failures remain visible.
```

---

# 9. Using `as`

You can store the exception object in a variable.

Syntax:

```python
try:
    ...
except ExceptionType as exc:
    ...
```

Example:

```python
try:
    value = int("abc")
except ValueError as exc:
    print(exc)
```

Possible output:

```text
invalid literal for int() with base 10: 'abc'
```

---

# 10. What Is `exc`?

In:

```python
except ValueError as exc:
```

`exc` refers to the exception object.

You can inspect it:

```python
try:
    value = int("abc")
except ValueError as exc:
    print(type(exc))
    print(exc)
```

Output resembles:

```text
<class 'ValueError'>
invalid literal for int() with base 10: 'abc'
```

The variable name does not have to be `exc`.

These are equivalent:

```python
except ValueError as exc:
```

```python
except ValueError as error:
```

```python
except ValueError as err:
```

`exc` is simply a common naming convention.

---

# 11. Catching `TypeError`

Example:

```python
try:
    result = 10 + "20"
except TypeError as exc:
    print("Type problem:", exc)
```

Output:

```text
Type problem: unsupported operand type(s) for +: 'int' and 'str'
```

---

# 12. Catching `ZeroDivisionError`

```python
try:
    result = 100 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```

Output:

```text
Cannot divide by zero
```

---

# 13. Catching `IndexError`

```python
drives = ["/dev/sda", "/dev/sdb"]

try:
    device = drives[5]
except IndexError:
    print("Device index does not exist")
```

Output:

```text
Device index does not exist
```

---

# 14. Catching `KeyError`

```python
drive = {
    "device": "/dev/sda",
    "status": "PASS"
}

try:
    capacity = drive["capacity"]
except KeyError:
    print("Capacity field is missing")
```

Output:

```text
Capacity field is missing
```

---

# 15. Catching `FileNotFoundError`

```python
try:
    file = open("storage.log", "r")
except FileNotFoundError:
    print("Storage log does not exist")
```

This is extremely common in automation.

---

# 16. Catching `PermissionError`

```python
try:
    file = open("/protected/storage.log", "r")
except PermissionError:
    print("Permission denied")
```

---

# 17. Storage Example — Reading a Test Log

```python
log_path = "/tmp/sda_test.log"

try:
    with open(log_path, "r") as file:
        data = file.read()

    print("Log loaded successfully")

except FileNotFoundError:
    print("Test log was not generated")

except PermissionError:
    print("Permission denied while reading test log")
```

Different failures receive different handling.

---

# 18. Why Separate Exceptions?

Consider:

```python
try:
    with open(log_path, "r") as file:
        data = file.read()

except FileNotFoundError:
    print("Log is missing")

except PermissionError:
    print("Log exists but cannot be accessed")
```

These are operationally different.

```text
FileNotFoundError
    ↓
Check log generation/path

PermissionError
    ↓
Check permissions/access
```

This gives better troubleshooting information.

---

# 19. Multiple Operations Inside `try`

You can technically put multiple statements inside `try`:

```python
try:
    data = open("storage.log").read()
    value = int(data)
    result = 100 / value
except:
    print("Failure")
```

But this can make troubleshooting difficult.

Which operation failed?

```text
open()
int()
division?
```

The broad `try` block hides the operation boundary.

---

# 20. Better Design

Keep the risky operation as focused as practical.

Instead of:

```python
try:
    data = open("storage.log").read()
    value = int(data)
    result = 100 / value
except ValueError:
    ...
```

you should design the code so that the exception handling corresponds to the operation you understand.

For example:

```python
try:
    value = int(data)
except ValueError:
    print("Invalid numeric data")
```

The principle is:

```text
Small, meaningful try blocks
        ↓
More precise exception handling
        ↓
Better troubleshooting
```

---

# 21. What Happens If the Exception Is Not Caught?

Example:

```python
try:
    value = int("abc")
except TypeError:
    print("Type problem")
```

The actual exception is:

```text
ValueError
```

not:

```text
TypeError
```

Therefore the `except` does not match.

The exception remains unhandled and propagates outward.

Eventually Python reports:

```text
ValueError
```

and the program terminates if nothing else handles it.

---

# 22. Important Rule — Matching Exception Type

The `except` clause must match the raised exception or an appropriate superclass.

Example:

```python
try:
    int("abc")
except ValueError:
    print("Handled")
```

works.

But:

```python
try:
    int("abc")
except TypeError:
    print("Handled")
```

does not handle the `ValueError`.

---

# 23. Multiple `except` Blocks

You can handle different exception types separately.

```python
try:
    value = int(user_input)
    result = 100 / value

except ValueError:
    print("Input is not a valid integer")

except ZeroDivisionError:
    print("Value cannot be zero")
```

Possible inputs:

```text
abc
0
10
```

Results:

```text
abc → ValueError
0   → ZeroDivisionError
10  → successful
```

---

# 24. Exception Tuple

If multiple exceptions should receive the same handling:

```python
try:
    ...
except (ValueError, TypeError):
    print("Invalid input")
```

This means:

```text
ValueError OR TypeError
        ↓
same handler
```

---

# 25. Separate vs Combined Exceptions

Separate:

```python
try:
    ...
except ValueError:
    print("Invalid value")
except TypeError:
    print("Invalid type")
```

Use this when different recovery actions are required.

Combined:

```python
try:
    ...
except (ValueError, TypeError):
    print("Invalid input")
```

Use this when both exceptions genuinely require the same handling.

---

# 26. Exception Ordering

Exception handlers are checked from top to bottom.

Example:

```python
try:
    int("abc")

except ValueError:
    print("Value error")

except Exception:
    print("Other error")
```

The first matching handler executes.

---

# 27. Parent and Child Exceptions

Some exceptions are related through inheritance.

Conceptually:

```text
Exception
    |
    +-- ValueError
    +-- TypeError
    +-- OSError
```

If you catch:

```python
except Exception:
```

it can catch many normal application exceptions.

Therefore:

```python
except ValueError:
```

is more specific.

---

# 28. Why Order Matters

Suppose:

```python
try:
    int("abc")

except Exception:
    print("General error")

except ValueError:
    print("Value error")
```

The `ValueError` handler will never be reached because:

```text
ValueError
    ↓
is an Exception
    ↓
first handler already catches it
```

Therefore:

```text
Specific
   ↓
General
```

is the correct ordering.

Example:

```python
except ValueError:
    ...

except Exception:
    ...
```

---

# 29. Bare `except`

You can technically write:

```python
try:
    operation()
except:
    print("Failed")
```

This catches almost everything, including exceptions outside the normal `Exception` hierarchy.

This should generally be avoided unless there is a very deliberate reason.

Prefer:

```python
except Exception as exc:
```

when a broad application-level catch is actually required.

---

# 30. Why Bare `except` Is Dangerous

Consider:

```python
try:
    run_storage_test()
except:
    print("Test passed")
```

This is terrible.

A test could fail because of:

```text
PermissionError
TimeoutError
KeyboardInterrupt
SystemExit
Programming bug
```

and the automation could incorrectly continue.

Exception handling should never convert a failure into a false success.

---

# 31. `except Exception`

A broader but usually safer application-level form is:

```python
try:
    operation()
except Exception as exc:
    print(f"Operation failed: {exc}")
```

This catches exceptions derived from `Exception`.

But even this should not automatically be used everywhere.

Ask:

```text
Can I recover?
Do I understand the failure?
Should I report and continue?
Should I propagate it?
```

---

# 32. Do Not Use Exceptions to Hide Programming Bugs

Bad:

```python
try:
    result = some_complex_function()
except Exception:
    result = None
```

This may hide:

```text
Programming errors
Unexpected state
Incorrect assumptions
Real system failures
```

A broad catch is appropriate only when the program has a clear strategy for handling the failure.

---

# 33. `try` Should Contain Risky Operations

Good:

```python
try:
    data = int(user_input)
except ValueError:
    print("Invalid number")
```

Less useful:

```python
try:
    print("Starting test")
    data = int(user_input)
    print("Processing")
    generate_report()
    send_email()
    cleanup()
except:
    print("Something failed")
```

The second version makes it difficult to know which operation failed and whether partial operations occurred.

---

# 34. Storage Automation Example

Suppose:

```python
def read_test_result(path):
    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Test result missing: {path}")
```

The function has a clear responsibility:

```text
Read test result
     ↓
Missing file?
     ↓
Handle missing result
```

---

# 35. Storage Device Validation Example

```python
import os

device = "/dev/sda"

try:
    exists = os.path.exists(device)

    if not exists:
        raise FileNotFoundError(
            f"Device not found: {device}"
        )

    print("Device exists")

except FileNotFoundError as exc:
    print(f"Validation failed: {exc}")
```

Here, the exception represents a meaningful failure condition.

---

# 36. Command Execution Example

Suppose Python executes a storage command.

Conceptually:

```python
import subprocess

try:
    result = subprocess.run(
        ["some_storage_command", "/dev/sda"],
        check=True,
        capture_output=True,
        text=True
    )

except FileNotFoundError:
    print("Storage command is not installed")

except subprocess.CalledProcessError as exc:
    print("Storage command failed")
```

Different failures can now be distinguished.

---

# 37. What `check=True` Does

When using:

```python
subprocess.run(..., check=True)
```

a non-zero command exit status causes Python to raise:

```text
subprocess.CalledProcessError
```

This is useful for automation because:

```text
Command
   ↓
Exit status
   ↓
Failure
   ↓
Python exception
```

can be handled explicitly.

---

# 38. Important Engineering Principle

An exception handler should answer:

```text
What failure occurred?
        ↓
Can I recover?
        ↓
If yes → recover safely
If no  → propagate/report
```

Not:

```text
Something failed
        ↓
Ignore it
```

---

# 39. Common Mistakes

## Mistake 1 — Empty handler

```python
try:
    operation()
except:
    pass
```

Problem:

```text
Failure disappears.
```

---

## Mistake 2 — Catching the wrong exception

```python
try:
    int("abc")
except TypeError:
    ...
```

Actual exception:

```text
ValueError
```

---

## Mistake 3 — Huge `try` block

```python
try:
    everything()
except Exception:
    ...
```

Problem:

```text
Hard to identify failure
Hard to recover correctly
Hard to debug
```

---

## Mistake 4 — Treating every exception identically

```python
except Exception:
    retry()
```

Not every failure is retryable.

For example:

```text
Invalid configuration
    ↓
Retrying will not fix it.
```

---

# 40. Interview Questions

## Q1. What does `try` do?

### Answer

It defines a block of code whose execution is monitored for exceptions.

---

## Q2. What does `except` do?

### Answer

It defines how a matching exception should be handled when one occurs inside the associated `try` block.

---

## Q3. What happens when no exception occurs?

### Answer

The `except` block is skipped and execution continues after the `try/except` structure.

---

## Q4. What happens when an exception occurs?

### Answer

Execution stops at the failing statement inside the `try` block, Python searches for a matching `except`, and if found, executes it before continuing after the structure.

---

## Q5. Why catch specific exceptions?

### Answer

Specific exceptions make the code more predictable, easier to debug, and allow different failures to receive appropriate recovery strategies.

---

## Q6. What does `except ValueError as exc` mean?

### Answer

It catches a `ValueError` and stores the exception object in the variable `exc`.

---

## Q7. Can multiple exceptions be handled?

### Answer

Yes.

Using multiple handlers:

```python
except ValueError:
    ...
except TypeError:
    ...
```

or one handler with a tuple:

```python
except (ValueError, TypeError):
    ...
```

---

## Q8. Why should specific exceptions appear before general exceptions?

### Answer

Because exception handlers are evaluated from top to bottom. A general parent exception such as `Exception` could otherwise catch the error before the more specific handler gets a chance.

---

## Q9. Why is bare `except` generally discouraged?

### Answer

Because it can catch unexpected failures and can hide important problems, making debugging and reliable automation more difficult.

---

## Q10. Should every exception be caught?

### Answer

No.

Only exceptions that the current layer can meaningfully handle should normally be caught. Unexpected or unrecoverable exceptions should often propagate to a higher-level handler.

---

# 41. Storage Engineering Interview Questions

## Q11. A storage test command returns a non-zero exit code. Should you always retry?

### Answer

No.

First determine why it failed.

For example:

```text
Transient communication problem
    → possibly retry

Invalid device path
    → retry will not help

Invalid configuration
    → retry will not help

Permission failure
    → fix permission first

Device failure
    → investigate device
```

---

## Q12. Why should storage automation distinguish `FileNotFoundError` and `PermissionError`?

### Answer

Because their recovery actions differ.

```text
FileNotFoundError
    → verify path/log generation

PermissionError
    → verify permissions/access
```

---

## Q13. What is wrong with this?

```python
try:
    run_test()
except Exception:
    print("Test failed")
```

### Answer

It catches everything derived from `Exception` and may lose important context.

A better design is to:

```text
Catch known failures specifically
        ↓
Handle them appropriately
        ↓
Log useful context
        ↓
Allow unexpected failures to propagate
```

---

# 42. Knowledge-Gap Checklist

Before moving to the next document, you should understand:

```text
[ ] try
[ ] except
[ ] Exception matching
[ ] Specific exceptions
[ ] Exception object
[ ] `as`
[ ] Multiple except blocks
[ ] Exception tuples
[ ] Exception ordering
[ ] Parent vs child exceptions
[ ] Bare except
[ ] `except Exception`
[ ] Try-block scope
[ ] Exception propagation when not caught
[ ] Storage file failures
[ ] Command execution failures
[ ] Retry considerations
```

---

# 43. Core Mental Model

Remember this:

```text
try
 ↓
Run risky operation
 ↓
 ┌─────────────────────┐
 │                     │
No exception       Exception
 │                     │
 ↓                     ↓
Skip except       Find matching except
 │                     │
 └──────────┬──────────┘
            ↓
 Continue after try/except
```

---

# 44. Final Engineering Rule

The most important rule of this document is:

```text
DO NOT CATCH AN EXCEPTION
UNLESS YOU KNOW WHAT TO DO WITH IT.
```

Good exception handling is not:

```text
Catch everything
```

It is:

```text
Detect
 ↓
Classify
 ↓
Handle what you understand
 ↓
Preserve information
 ↓
Propagate what you cannot safely handle
```

# END

