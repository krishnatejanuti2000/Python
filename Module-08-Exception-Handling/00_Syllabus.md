# Module 08 — Exception Handling

## Objective

Exception Handling is used to detect, handle, propagate, and recover from runtime failures without allowing the entire program to terminate unexpectedly.

The goal of this module is to understand:

- What errors and exceptions are
- Why exceptions occur
- How Python represents exceptions
- How to catch exceptions safely
- How to handle different exception types
- How to use `else` and `finally`
- How to deliberately raise exceptions
- How to create custom exceptions
- How exception hierarchy works
- How exceptions propagate
- How to preserve the original error information
- How to design reliable exception-handling code
- How to troubleshoot failures
- How to apply exception handling in Storage Test Automation

---

# 1. Errors and Exceptions

## Topics

- What is an error?
- Syntax errors
- Runtime errors
- Logical errors
- What is an exception?
- Difference between error and exception
- When Python raises an exception
- Reading Python exception messages
- Tracebacks
- Understanding:
  - Exception type
  - Exception message
  - File
  - Line number
  - Call stack

## Important Built-in Exceptions

- `NameError`
- `TypeError`
- `ValueError`
- `IndexError`
- `KeyError`
- `AttributeError`
- `ZeroDivisionError`
- `FileNotFoundError`
- `PermissionError`
- `OSError`
- `ImportError`
- `ModuleNotFoundError`

---

# 2. `try` and `except`

## Topics

- Basic `try`
- Basic `except`
- How exception handling works
- Execution flow
- Catching a specific exception
- Catching multiple exception types
- Using the exception object
- Understanding `as`
- Why specific exception handling is preferred
- Avoiding unnecessary broad exception handling

## Basic Structure

```python
try:
    # risky operation
except SomeException:
    # recovery / handling
````

---

# 3. Multiple Exceptions

## Topics

* Multiple `except` blocks
* Handling different exception types separately
* Handling multiple exception types with one `except`
* Exception ordering
* Most-specific exception first
* Common mistakes with exception ordering
* Exception tuples

Example:

```python
try:
    ...
except ValueError:
    ...
except TypeError:
    ...
```

---

# 4. `else` and `finally`

## `else`

Topics:

* Purpose of `else`
* When `else` executes
* `else` vs code after `try/except`
* Using `else` for successful execution

## `finally`

Topics:

* Purpose of `finally`
* Guaranteed cleanup
* `finally` after successful execution
* `finally` after an exception
* `finally` with `return`
* Resource cleanup
* File handling
* Connection cleanup

## Complete Structure

```python
try:
    ...
except:
    ...
else:
    ...
finally:
    ...
```

---

# 5. `raise`

## Topics

* Why `raise` is used
* Raising built-in exceptions
* Raising exceptions based on conditions
* `raise` without an exception
* Re-raising an exception
* Preserving the original exception
* Designing meaningful exception messages

Example:

```python
if capacity <= 0:
    raise ValueError("Capacity must be greater than zero")
```

---

# 6. Custom Exceptions

## Topics

* Why custom exceptions are needed
* Creating a custom exception
* Inheriting from `Exception`
* Raising custom exceptions
* Catching custom exceptions
* Adding meaningful messages
* Custom exception design

Example:

```python
class StorageTestError(Exception):
    pass
```

---

# 7. Exception Hierarchy

## Topics

* Python exception hierarchy
* `BaseException`
* `Exception`
* Built-in exception branches
* Parent vs child exceptions
* Catching a parent exception
* Why `except Exception` is different from bare `except`
* Exception ordering

Important concept:

```text
BaseException
    |
    +-- Exception
          |
          +-- ValueError
          +-- TypeError
          +-- OSError
          +-- ...
```

---

# 8. Exception Handling Patterns

## Topics

* Specific exception handling
* Multiple exception handling
* Cleanup pattern
* Validation pattern
* Retry pattern
* Fail-fast pattern
* Graceful failure
* Exception propagation
* Re-raising
* Exception chaining
* Preserving original failure context
* `raise ... from ...`
* Designing useful error messages
* Avoiding swallowed exceptions
* Avoiding empty `except` blocks
* Avoiding unnecessary nested `try` blocks

---

# 9. File and System Errors

This section prepares exception handling for real Python automation.

## Topics

* `FileNotFoundError`
* `PermissionError`
* `IsADirectoryError`
* `NotADirectoryError`
* `FileExistsError`
* `OSError`
* Handling missing files
* Handling inaccessible files
* Handling invalid paths
* Handling filesystem failures
* Handling command execution failures
* Distinguishing recoverable and non-recoverable errors

---

# 10. Debugging and Troubleshooting

## Topics

* Reading tracebacks
* Identifying the root exception
* Understanding exception propagation
* Finding the actual failure location
* Debugging nested exceptions
* Logging exception information
* Preserving original errors
* Avoiding misleading error messages
* Reproducing failures
* Designing useful diagnostic information
* Root Cause Analysis

## Troubleshooting Flow

```text
Failure
   ↓
Read traceback
   ↓
Identify exception type
   ↓
Identify failing operation
   ↓
Identify input/state
   ↓
Determine root cause
   ↓
Decide recovery
   ↓
Handle or propagate
   ↓
Report
```

---

# 11. Storage Automation Error Handling

This section connects Python Exception Handling with Storage Test Engineering.

## Topics

### Device Validation

* Invalid device paths
* Unsupported device types
* Invalid device states

### Command Execution

* Command failures
* Non-zero exit codes
* Missing commands
* Permission problems

### Storage Tests

* Read test failure
* Write test failure
* I/O failure
* Timeout
* Device disappearance
* Incomplete test
* Invalid test parameters

### Log Processing

* Missing log file
* Corrupt log
* Unexpected log format
* Missing fields
* Invalid values

### Automation

* Retryable failures
* Non-retryable failures
* Cleanup after failure
* Failure reporting
* Preserving diagnostic information

---

# 12. Exception Handling Projects

Projects will progress from simple to realistic.

## Project 1 — Safe Calculator

Handle:

* Invalid input
* Division by zero
* Invalid operations

## Project 2 — File Reader

Handle:

* Missing file
* Permission failure
* Invalid input

## Project 3 — Storage Device Validator

Handle:

* Invalid device path
* Unsupported device
* Invalid parameters

## Project 4 — Storage Test Runner

Handle:

* Command failure
* Timeout
* Device failure
* Invalid test configuration

## Project 5 — Storage Log Analyzer

Handle:

* Missing log
* Invalid log records
* Parsing failures
* Unexpected data

## Project 6 — Enterprise Storage Test Execution

Combine:

```text
Validation
   ↓
Test Execution
   ↓
Exception Handling
   ↓
Cleanup
   ↓
Log Collection
   ↓
Failure Analysis
   ↓
Final Report
```

---

# 13. Interview Questions

Questions will progress from fundamentals to advanced engineering scenarios.

## Levels

### Level 1 — Fundamentals

* What is an exception?
* What is a traceback?
* Difference between syntax and runtime errors?
* What does `try` do?
* What does `except` do?

### Level 2 — Core Exception Handling

* Multiple `except` blocks
* Specific vs broad exceptions
* `as`
* `else`
* `finally`

### Level 3 — Advanced

* Exception hierarchy
* Exception propagation
* Re-raising
* Exception chaining
* `raise from`
* Custom exceptions

### Level 4 — Troubleshooting

* Debugging real failures
* Identifying root cause
* Designing recovery logic
* Avoiding swallowed exceptions

### Level 5 — Storage Engineering

* Device command failures
* Timeout handling
* Permission failures
* Device disappearance
* Test cleanup
* Retry decisions
* Failure reporting

---

# 14. Exception Handling Best Practices

The module must establish production-quality practices.

## Prefer

```python
try:
    operation()
except FileNotFoundError:
    handle_missing_file()
```

over unnecessarily broad handling.

## Avoid

```python
try:
    operation()
except:
    pass
```

because it can silently hide failures.

## Prefer

```python
except Exception as exc:
    print(f"Operation failed: {exc}")
```

when a broad catch is genuinely appropriate and the failure is intentionally being handled.

---

# 15. Exception Propagation

Topics:

* What happens when an exception is not handled?
* Propagation through function calls
* Caller handling
* Re-raising
* Designing exception boundaries
* When to handle locally
* When to propagate upward

Example flow:

```text
Function A
   ↓
Function B
   ↓
Function C
   ↓
Exception
   ↓
C cannot handle
   ↓
B cannot handle
   ↓
A handles
```

---

# 16. Exception Chaining

Topics:

* Original exception
* New exception
* Why context matters
* Implicit exception chaining
* Explicit chaining
* `raise ... from ...`

Example:

```python
try:
    ...
except OSError as exc:
    raise StorageTestError("Storage operation failed") from exc
```

This preserves the original cause.

---

# 17. Cleanup and Resource Safety

Topics:

* Why cleanup matters
* `finally`
* Closing files
* Releasing resources
* Cleaning temporary files
* Disconnecting resources
* Stopping tests safely
* Cleanup after partial failure

---

# 18. Exception Handling and Logging

Topics:

* Difference between printing and logging
* Recording exception type
* Recording useful context
* Recording the failed operation
* Recording device information
* Recording timestamps
* Preserving traceback information
* Avoiding sensitive information in logs

---

# 19. Testing Exception Handling

Exception-handling code must also be tested.

Test:

```text
Valid input
Invalid input
Expected exception
Unexpected exception
Missing resource
Permission failure
Boundary condition
Cleanup after failure
```

The goal is not only:

```text
Does the program work?
```

but also:

```text
Does the program fail correctly?
```

---

# 20. Common Mistakes

We will explicitly cover:

```text
Bare except
Swallowing exceptions
Catching Exception unnecessarily
Wrong exception ordering
Using exceptions for normal control flow
Overly broad try blocks
Missing cleanup
Losing the original exception
Poor error messages
Incorrect retry behavior
Ignoring root cause
```

---

# 21. Final Engineering Model

Exception handling should follow:

```text
Detect
  ↓
Understand
  ↓
Classify
  ↓
Handle / Recover / Propagate
  ↓
Cleanup
  ↓
Log
  ↓
Report
```

Not:

```text
Error
 ↓
except
 ↓
pass
```

---

# Module 8 Completion Standard

Module 8 will be considered complete only when the engineer can:

```text
Understand exceptions
        ↓
Read tracebacks
        ↓
Catch specific exceptions
        ↓
Handle multiple exceptions
        ↓
Use else/finally correctly
        ↓
Raise exceptions
        ↓
Create custom exceptions
        ↓
Understand hierarchy
        ↓
Understand propagation
        ↓
Use exception chaining
        ↓
Design cleanup
        ↓
Debug failures
        ↓
Handle system errors
        ↓
Build resilient automation
        ↓
Handle Storage Test failures
```

---

# Documentation Sequence

The documentation will be completed in this order:

```text
00_Syllabus.md
        ↓
01_Errors_and_Exceptions.md
        ↓
02_try_and_except.md
        ↓
03_Multiple_Exceptions.md
        ↓
04_else_and_finally.md
        ↓
05_raise.md
        ↓
06_Custom_Exceptions.md
        ↓
07_Exception_Hierarchy.md
        ↓
08_Exception_Handling_Patterns.md
        ↓
09_File_and_System_Errors.md
        ↓
10_Debugging_and_Troubleshooting.md
        ↓
11_Storage_Automation_Error_Handling.md
        ↓
12_Exception_Handling_Projects.md
        ↓
13_Interview_Questions.md
        ↓
Exception_CheatSheet.md
        ↓
Exception_Quick_Revision.md
```

---

# Important Note

This syllabus deliberately includes topics that are often missed in basic Python courses, especially:

* Exception propagation
* Exception chaining
* `raise from`
* Root Cause Analysis
* Cleanup/resource safety
* Retryable vs non-retryable failures
* System-level exceptions
* Storage automation failure handling

These will be documented and practiced rather than merely listed.

# END



