# 03 — Multiple Exceptions

## Objective

A real Python program can fail in different ways.

For example, a storage automation script may encounter:

- Invalid input
- Missing files
- Permission failures
- Invalid device information
- Division by zero
- Command execution failures
- Unexpected operating-system errors

This document covers how to handle multiple exception types correctly and how to decide whether exceptions should share the same handler or have different handling logic.

---

# 1. Why Multiple Exceptions Matter

Consider:

```python
value = int(user_input)
result = 100 / value
````

There are at least two possible exceptions:

```text
Invalid input
    ↓
ValueError

Input is zero
    ↓
ZeroDivisionError
```

Therefore, exception handling must sometimes distinguish between different failures.

---

# 2. Multiple `except` Blocks

Python allows multiple `except` blocks:

```python
try:
    # risky operation
except ValueError:
    # handle ValueError
except TypeError:
    # handle TypeError
except ZeroDivisionError:
    # handle ZeroDivisionError
```

Only one matching handler executes for a particular exception.

---

# 3. Basic Example

```python
try:
    value = int(input("Enter a number: "))
    result = 100 / value
    print(result)

except ValueError:
    print("Please enter a valid integer")

except ZeroDivisionError:
    print("Zero is not allowed")
```

Possible inputs:

```text
abc
0
10
```

Results:

```text
abc
↓
ValueError
↓
Please enter a valid integer
```

```text
0
↓
ZeroDivisionError
↓
Zero is not allowed
```

```text
10
↓
100 / 10
↓
10.0
```

---

# 4. How Python Chooses the Handler

Python evaluates the `except` blocks from top to bottom.

Example:

```python
try:
    int("abc")

except ValueError:
    print("ValueError handler")

except TypeError:
    print("TypeError handler")
```

The exception is:

```text
ValueError
```

Therefore:

```text
ValueError handler
```

is executed.

The other handlers are skipped.

---

# 5. Only One Handler Executes

Consider:

```python
try:
    int("abc")

except ValueError:
    print("Handler 1")

except Exception:
    print("Handler 2")
```

Output:

```text
Handler 1
```

Python does not execute both handlers.

Once a matching handler is found:

```text
Exception
   ↓
First matching except
   ↓
Execute it
   ↓
Leave exception-handling structure
```

---

# 6. Handling the Same Exception in Different Situations

Different exceptions can require different actions.

Example:

```python
try:
    value = int(user_input)

except ValueError:
    print("Input format is invalid")

except TypeError:
    print("Input type is invalid")
```

The messages are different because the failure meanings are different.

---

# 7. Exception Tuple

If multiple exceptions require exactly the same handling, they can be grouped.

Syntax:

```python
except (ExceptionType1, ExceptionType2):
    ...
```

Example:

```python
try:
    value = int(user_input)

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

# 8. Why Use a Tuple?

Compare:

```python
try:
    value = int(user_input)

except ValueError:
    print("Invalid input")

except TypeError:
    print("Invalid input")
```

with:

```python
try:
    value = int(user_input)

except (ValueError, TypeError):
    print("Invalid input")
```

The second version is more concise when the handling is genuinely identical.

---

# 9. Do Not Combine Exceptions Automatically

This is important.

Do not write:

```python
except (ValueError, FileNotFoundError, PermissionError):
    print("Something went wrong")
```

just because all are exceptions.

Ask:

```text
Do they have the same meaning?
Do they have the same recovery?
Do they need the same logging?
```

If not, separate them.

---

# 10. Separate Handling

Example:

```python
try:
    with open("storage.log", "r") as file:
        data = file.read()

except FileNotFoundError:
    print("Storage log does not exist")

except PermissionError:
    print("Storage log cannot be accessed")

except OSError:
    print("Operating system error occurred")
```

This gives different actions for different failures.

---

# 11. Storage Engineering Example

Suppose an automation tool reads a storage test log.

```python
log_path = "/var/log/storage_test.log"

try:
    with open(log_path, "r") as file:
        data = file.read()

except FileNotFoundError:
    print("FAIL: Test log was not generated")

except PermissionError:
    print("FAIL: Permission denied while reading test log")

except OSError as exc:
    print(f"FAIL: OS error while reading test log: {exc}")
```

This gives useful failure classification.

---

# 12. Why `OSError` Comes After Specific Exceptions

Some filesystem-related exceptions are subclasses of `OSError`.

Conceptually:

```text
OSError
   |
   +-- FileNotFoundError
   |
   +-- PermissionError
   |
   +-- ...
```

Therefore:

```python
except FileNotFoundError:
    ...

except PermissionError:
    ...

except OSError:
    ...
```

is useful.

The specific cases are handled first.

The more general OS error acts as a fallback.

---

# 13. Incorrect Ordering

Avoid:

```python
try:
    ...
except OSError:
    print("OS error")

except FileNotFoundError:
    print("File missing")
```

Why?

Because:

```text
FileNotFoundError
       ↓
is an OSError
       ↓
OSError handler catches it first
```

Therefore the `FileNotFoundError` handler becomes unreachable for that exception.

---

# 14. General Rule for Exception Ordering

Use:

```text
Specific
   ↓
More specific
   ↓
General
```

Example:

```python
except FileNotFoundError:
    ...

except PermissionError:
    ...

except OSError:
    ...

except Exception:
    ...
```

This allows specific failures to be classified correctly.

---

# 15. Parent and Child Exceptions

Python exceptions form an inheritance hierarchy.

For example:

```text
Exception
   |
   +-- OSError
         |
         +-- FileNotFoundError
         +-- PermissionError
```

A handler for the parent can catch a child.

Example:

```python
try:
    open("missing.log")
except OSError:
    print("OS failure")
```

This can catch:

```text
FileNotFoundError
PermissionError
```

because both belong to the `OSError` branch.

---

# 16. Specific Handler vs Parent Handler

Specific:

```python
except FileNotFoundError:
    print("File is missing")
```

Parent:

```python
except OSError:
    print("Some OS operation failed")
```

Use the specific handler when you know what action to take.

Use the parent handler when several child failures genuinely share the same fallback handling.

---

# 17. `Exception` as a Broad Handler

Example:

```python
try:
    operation()

except ValueError:
    print("Invalid value")

except Exception as exc:
    print(f"Unexpected application error: {exc}")
```

This pattern can be useful at an appropriate application boundary.

The first handler deals with a known failure.

The second handles other ordinary exceptions that the current layer has decided to catch.

---

# 18. Why `except Exception` Should Usually Be Last

Consider:

```python
try:
    value = int("abc")

except Exception:
    print("General failure")

except ValueError:
    print("Invalid value")
```

The first handler catches `ValueError`.

Therefore:

```text
ValueError handler
```

will never execute.

Correct:

```python
try:
    value = int("abc")

except ValueError:
    print("Invalid value")

except Exception:
    print("General failure")
```

---

# 19. Multiple Exceptions With Different Recovery

Example:

```python
try:
    value = int(user_input)
    result = 100 / value

except ValueError:
    print("Ask the user for a valid number")

except ZeroDivisionError:
    print("Ask the user for a non-zero number")
```

Recovery depends on the exception.

This is one of the main reasons to distinguish exceptions.

---

# 20. Multiple Exceptions With the Same Recovery

Example:

```python
try:
    process_input()

except (ValueError, TypeError):
    print("Invalid input")
```

Both exceptions mean the same thing for this particular operation:

```text
Input cannot be processed
```

Therefore a shared handler is reasonable.

---

# 21. Using `as` With Multiple Exception Types

You can also capture the exception object:

```python
try:
    process_input()

except (ValueError, TypeError) as exc:
    print(f"Invalid input: {exc}")
```

The variable `exc` contains the actual exception object.

---

# 22. Identifying Which Exception Occurred

If multiple exceptions share a handler:

```python
try:
    process_input()

except (ValueError, TypeError) as exc:
    print(type(exc).__name__)
    print(exc)
```

For example:

```text
ValueError
invalid literal for int() with base 10: 'abc'
```

or:

```text
TypeError
unsupported operand type...
```

The actual exception type is preserved.

---

# 23. Why This Matters in Automation

Suppose:

```python
try:
    run_storage_test()

except (TimeoutError, ConnectionError) as exc:
    print(f"Transient storage communication problem: {exc}")
```

These failures may share a retry strategy.

But:

```python
except PermissionError:
    print("Permission problem")
```

should not necessarily be treated as a transient communication failure.

Therefore:

```text
Exception type
      ↓
Failure classification
      ↓
Recovery strategy
```

---

# 24. Retryable vs Non-Retryable Exceptions

This is an important engineering concept.

Not every exception should trigger a retry.

Potentially retryable:

```text
Timeout
Temporary connection failure
Transient resource unavailability
```

Potentially non-retryable:

```text
Invalid configuration
Invalid device path
Permission failure
Invalid user input
Unsupported operation
```

The exact classification depends on the system.

---

# 25. Storage Test Example

Imagine:

```python
try:
    run_test("/dev/sda")

except TimeoutError:
    print("Transient timeout — retry may be appropriate")

except PermissionError:
    print("Permission failure — fix permissions")

except FileNotFoundError:
    print("Device/path unavailable — investigate path or device state")

except ValueError:
    print("Invalid test configuration")
```

Each failure has a different operational meaning.

---

# 26. Handling Command Execution Exceptions

Example:

```python
import subprocess

try:
    result = subprocess.run(
        ["storage-test", "/dev/sda"],
        check=True,
        capture_output=True,
        text=True
    )

except FileNotFoundError:
    print("storage-test command is not installed")

except subprocess.CalledProcessError as exc:
    print(f"Storage test command failed: {exc}")

except PermissionError:
    print("Permission denied while executing storage test")
```

This is much more useful than:

```python
except:
    print("Test failed")
```

---

# 27. Exception Matching Is Based on Type

Suppose:

```python
try:
    int("abc")

except ValueError:
    print("Value")

except TypeError:
    print("Type")
```

Python evaluates the actual exception:

```text
ValueError
```

and finds the matching handler.

It does not select based on the printed message.

This is why exception types matter.

---

# 28. Do Not Match Exception Messages

Avoid designing logic like:

```python
try:
    operation()
except Exception as exc:
    if "file not found" in str(exc):
        ...
```

when a specific exception class is available.

Prefer:

```python
except FileNotFoundError:
    ...
```

Exception classes provide a more reliable classification mechanism.

---

# 29. Exception Tuple vs Multiple Handlers

Use a tuple when:

```text
Different exception types
        +
Same recovery
        +
Same reporting
```

Use separate handlers when:

```text
Different exception types
        +
Different recovery
```

---

# 30. Nested `try` Blocks

Python allows nested exception handling.

Example:

```python
try:
    try:
        value = int("abc")
    except ValueError:
        print("Inner handler")
except Exception:
    print("Outer handler")
```

Output:

```text
Inner handler
```

The inner handler handled the exception.

---

# 31. When Does the Outer Handler Run?

If the inner block does not handle the exception:

```python
try:
    try:
        value = int("abc")
    except TypeError:
        print("Inner handler")
except ValueError:
    print("Outer handler")
```

The inner handler does not match.

The exception propagates to the outer `try`.

Therefore:

```text
Inner try
   ↓
No matching handler
   ↓
Outer try
   ↓
Matching handler
```

---

# 32. Avoid Unnecessary Nested `try`

Although nesting is possible, do not use it without a reason.

Poor:

```python
try:
    try:
        try:
            operation()
        except:
            ...
    except:
        ...
except:
    ...
```

This makes control flow difficult to understand.

Prefer clear exception boundaries.

---

# 33. Exception Handling Boundaries

Think about where an exception should be handled.

For example:

```text
Low-level function
        ↓
Detects failure
        ↓
Does it know how to recover?
       / \
     Yes  No
      ↓    ↓
   Handle  Propagate
```

The layer that understands the failure best should usually make the recovery decision.

---

# 34. Example With Functions

```python
def read_log(path):
    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError:
        raise
```

The function detects the exception but chooses not to hide it.

The caller can decide what to do:

```python
try:
    data = read_log("/tmp/test.log")
except FileNotFoundError:
    print("Test log is unavailable")
```

This is an example of propagation.

We will study propagation more deeply later.

---

# 35. Common Mistake — Duplicate Handling

Avoid unnecessary duplication:

```python
try:
    operation()

except ValueError:
    print("Failed")

except TypeError:
    print("Failed")
```

If the behavior is genuinely identical:

```python
try:
    operation()

except (ValueError, TypeError):
    print("Failed")
```

is clearer.

---

# 36. Common Mistake — Combining Unrelated Failures

Avoid:

```python
except (
    ValueError,
    PermissionError,
    FileNotFoundError,
    TimeoutError
):
    retry()
```

Why?

Because the failures may require completely different actions.

```text
ValueError
    → fix input

PermissionError
    → fix access

FileNotFoundError
    → investigate path/resource

TimeoutError
    → possibly retry
```

---

# 37. Common Mistake — Catching `Exception` Too Early

Avoid:

```python
try:
    operation()

except Exception:
    print("Failed")

except ValueError:
    print("Invalid value")
```

The general handler catches the `ValueError` first.

Correct:

```python
try:
    operation()

except ValueError:
    print("Invalid value")

except Exception:
    print("Unexpected failure")
```

---

# 38. Common Mistake — Treating a General Exception as Success

Never do:

```python
try:
    run_storage_test()
except Exception:
    print("Storage test completed successfully")
```

This is logically incorrect.

An exception indicates abnormal execution.

---

# 39. Practical Decision Table

| Situation                                | Approach                                               |
| ---------------------------------------- | ------------------------------------------------------ |
| Different exceptions, different recovery | Separate `except`                                      |
| Different exceptions, same recovery      | Exception tuple                                        |
| Specific + general fallback              | Specific first, `Exception` last                       |
| Unexpected failure                       | Usually propagate or handle at an appropriate boundary |
| Retryable failure                        | Handle only if retry policy is appropriate             |
| Non-retryable failure                    | Report/fail rather than blindly retry                  |

---

# 40. Interview Questions

## Q1. Can Python have multiple `except` blocks?

Yes.

```python
try:
    ...
except ValueError:
    ...
except TypeError:
    ...
```

---

## Q2. How does Python select an `except` block?

Python checks handlers from top to bottom and executes the first compatible handler.

---

## Q3. Can multiple exception types be handled by one `except`?

Yes.

```python
except (ValueError, TypeError):
    ...
```

---

## Q4. When should you use an exception tuple?

When multiple exception types require the same handling and recovery logic.

---

## Q5. Why should specific exceptions come before general exceptions?

Because a general parent exception can match the specific exception and prevent the specific handler from being reached.

---

## Q6. Can `OSError` catch `FileNotFoundError`?

Yes, because `FileNotFoundError` is part of the `OSError` hierarchy.

---

## Q7. Should every exception trigger a retry?

No.

Retry decisions should be based on the failure type and whether the condition is expected to be transient.

---

## Q8. Why is this bad?

```python
except (ValueError, PermissionError):
    retry()
```

Because those failures generally have different meanings and may require different recovery actions.

---

# 41. Storage Engineering Questions

## Q9. A storage log is missing. A permission error occurs. Should both be handled identically?

No.

```text
FileNotFoundError
    → investigate path/log generation

PermissionError
    → investigate access permissions
```

---

## Q10. A storage command times out. What should the exception handler do?

It should not blindly assume the device is permanently failed.

The automation should:

```text
Record timeout
    ↓
Capture diagnostic information
    ↓
Determine whether timeout is retryable
    ↓
Retry according to policy OR fail
    ↓
Preserve evidence
```

---

## Q11. Why is exception classification important in Storage Test Automation?

Because automation decisions depend on the failure type.

For example:

```text
Invalid configuration
    → FAIL

Permission problem
    → environment/configuration issue

Transient timeout
    → possible RETRY

Device disappearance
    → investigate device/system state
```

---

# 42. Knowledge-Gap Checklist

Before moving forward:

```text
[ ] Multiple except blocks
[ ] Exception matching
[ ] First matching handler
[ ] Exception tuples
[ ] Specific vs general exceptions
[ ] Parent/child exceptions
[ ] Exception ordering
[ ] `except Exception`
[ ] `as exc`
[ ] Same handling vs different handling
[ ] Nested try blocks
[ ] Exception propagation
[ ] Retryable vs non-retryable failures
[ ] Storage-specific failure classification
[ ] Command execution failures
```

---

# 43. Final Mental Model

```text
                Exception
                    |
        ┌───────────┴───────────┐
        |                       |
   Specific?                General?
        |                       |
        ↓                       ↓
Specific handler          General fallback
        |
        ↓
Correct recovery
```

When multiple exceptions are possible:

```text
Identify possible failures
        ↓
Classify them
        ↓
Ask whether recovery differs
        |
   ┌────┴────┐
   |         |
Different   Same
   |         |
   ↓         ↓
Separate   Tuple
handlers   handler
```

---

# 44. Final Engineering Rule

Do not ask:

```text
"How can I catch every exception?"
```

Ask:

```text
"What failures can this operation produce?"
             ↓
"What does each failure mean?"
             ↓
"Can I recover from it?"
             ↓
"Should I retry, report, or propagate?"
```

That mindset produces reliable exception handling.

# END

````
