# 05 — raise

## Objective

The `raise` statement allows a Python program to deliberately generate an exception.

So far we learned how Python can automatically raise exceptions:

```python
10 / 0
````

Python raises:

```text
ZeroDivisionError
```

With `raise`, **we can decide when a failure condition should become an exception**.

This is especially important in validation, APIs, testing, and Storage Test Automation.

---

# 1. What Is `raise`?

`raise` is used to explicitly raise an exception.

Basic syntax:

```python
raise ExceptionType("message")
```

Example:

```python
raise ValueError("Invalid value")
```

Output:

```text
ValueError: Invalid value
```

---

# 2. Why Do We Need `raise`?

Python automatically detects some failures.

For example:

```python
10 / 0
```

Python knows division by zero is invalid.

But Python does not automatically know your application's business rules.

For example:

```python
capacity = -500
```

Python considers this a valid integer.

But your storage application may define:

```text
Capacity must be greater than zero
```

Therefore, we can explicitly raise an exception:

```python
if capacity <= 0:
    raise ValueError("Capacity must be greater than zero")
```

---

# 3. Basic Example

```python
age = -5

if age < 0:
    raise ValueError("Age cannot be negative")
```

Output:

```text
ValueError: Age cannot be negative
```

The program deliberately raises the exception.

---

# 4. `raise` With `ValueError`

`ValueError` is commonly used when a value violates an expected rule.

Example:

```python
capacity = -100

if capacity <= 0:
    raise ValueError("Capacity must be positive")
```

---

# 5. `raise` With `TypeError`

Use `TypeError` when the object has an inappropriate type for the operation.

Example:

```python
def set_capacity(capacity):

    if not isinstance(capacity, int):
        raise TypeError("Capacity must be an integer")

    return capacity
```

Example:

```python
set_capacity("500")
```

raises:

```text
TypeError: Capacity must be an integer
```

---

# 6. `raise` Inside a Function

Example:

```python
def divide(a, b):

    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")

    return a / b
```

Usage:

```python
print(divide(10, 2))
```

Output:

```text
5.0
```

But:

```python
print(divide(10, 0))
```

raises:

```text
ZeroDivisionError: Cannot divide by zero
```

---

# 7. `raise` and `try/except`

`raise` becomes especially useful when combined with exception handling.

Example:

```python
try:
    raise ValueError("Invalid storage configuration")

except ValueError as exc:
    print(f"Configuration error: {exc}")
```

Output:

```text
Configuration error: Invalid storage configuration
```

Flow:

```text
raise
  ↓
exception created
  ↓
exception raised
  ↓
matching except
  ↓
handler executes
```

---

# 8. `raise` Based on a Condition

This is one of the most important practical patterns.

```python
device = "/dev/sda"

if not device.startswith("/dev/"):
    raise ValueError("Invalid device path")
```

If the condition is valid:

```text
No exception
```

If invalid:

```text
ValueError
```

---

# 9. Storage Example — Device Validation

```python
def validate_device(device):

    if not device.startswith("/dev/"):
        raise ValueError(
            f"Invalid device path: {device}"
        )

    return True
```

Usage:

```python
validate_device("/dev/sda")
```

works.

But:

```python
validate_device("sda")
```

raises:

```text
ValueError: Invalid device path: sda
```

---

# 10. `raise` Enforces Application Rules

Consider:

```python
capacity = 0
```

Python accepts this:

```python
capacity = 0
```

There is no Python error.

But a storage application might require:

```text
capacity > 0
```

Therefore:

```python
if capacity <= 0:
    raise ValueError(
        "Storage capacity must be greater than zero"
    )
```

This converts a business-rule violation into an explicit exception.

---

# 11. `raise` Does Not Automatically Mean Something Went Wrong in Python

This is important.

Consider:

```python
capacity = -1
```

Python itself is perfectly capable of storing `-1`.

The problem is with **our application's rule**.

Therefore:

```text
Python-valid value
        ↓
Application-invalid value
        ↓
raise appropriate exception
```

---

# 12. Raising Built-in Exceptions

Common examples:

```python
raise ValueError("Invalid value")
```

```python
raise TypeError("Invalid type")
```

```python
raise RuntimeError("Operation failed")
```

```python
raise FileNotFoundError("Required file is missing")
```

```python
raise PermissionError("Permission denied")
```

The exception type should describe the failure accurately.

---

# 13. Choose the Correct Exception

Do not blindly use:

```python
raise Exception("Something failed")
```

when a more appropriate built-in exception exists.

Prefer:

```python
raise ValueError("Capacity must be positive")
```

instead of:

```python
raise Exception("Capacity problem")
```

The exception type provides useful semantic information.

---

# 14. `raise Exception` vs Specific Exception

Poor:

```python
if capacity <= 0:
    raise Exception("Invalid capacity")
```

Better:

```python
if capacity <= 0:
    raise ValueError("Capacity must be positive")
```

Why?

Because callers can specifically handle:

```python
except ValueError:
    ...
```

The failure classification is preserved.

---

# 15. Raising an Exception With a Message

Always provide useful context when appropriate.

Bad:

```python
raise ValueError()
```

Better:

```python
raise ValueError("Capacity must be greater than zero")
```

Even better in automation:

```python
raise ValueError(
    f"Invalid capacity for {device}: {capacity}"
)
```

Now the failure contains context.

---

# 16. Good Error Messages

A useful error message should help answer:

```text
What failed?
What value caused it?
Which resource was involved?
What rule was violated?
```

Example:

```python
raise ValueError(
    f"Invalid capacity for {device}: {capacity}GB"
)
```

This is more useful than:

```python
raise ValueError("Invalid input")
```

---

# 17. `raise` Without an Argument

There is another form:

```python
raise
```

This is mainly used **inside an exception handler to re-raise the currently handled exception**.

Example:

```python
try:
    value = int("abc")

except ValueError:
    print("Logging error")
    raise
```

Output includes:

```text
Logging error
```

followed by the original:

```text
ValueError
```

---

# 18. Why Use Bare `raise`?

Suppose a low-level function detects an error but cannot safely recover.

It may record information and then re-raise the original exception.

```python
try:
    process_device()

except OSError as exc:
    print(f"Device operation failed: {exc}")
    raise
```

The exception is not swallowed.

It continues propagating.

---

# 19. `raise` vs `raise Exception(...)`

These are different.

## Create a new exception

```python
raise ValueError("Invalid value")
```

This creates and raises a new exception.

## Re-raise current exception

```python
raise
```

This re-raises the currently active exception inside an `except` block.

---

# 20. Re-Raising Example

```python
def process():

    try:
        value = int("abc")

    except ValueError:
        print("Recording failure")
        raise
```

The function:

```text
detects failure
    ↓
records/logs it
    ↓
does not know how to recover
    ↓
re-raises it
```

The caller can then decide what to do.

---

# 21. Re-Raising Preserves the Original Exception

Example:

```python
try:
    int("abc")

except ValueError as exc:
    print("Original:", exc)
    raise
```

The original `ValueError` remains the exception being propagated.

This is useful for preserving the original failure information.

---

# 22. Why Swallowing Is Dangerous

Bad:

```python
try:
    run_test()

except Exception as exc:
    print(f"Test failed: {exc}")
```

If the function simply continues without reporting failure to the appropriate caller, the higher-level automation may incorrectly assume success.

Sometimes we want:

```python
except Exception as exc:
    log_failure(exc)
    raise
```

This means:

```text
Log it
  ↓
Preserve it
  ↓
Propagate it
```

---

# 23. `raise` in Validation

Validation is one of the most common uses.

Example:

```python
def validate_capacity(capacity):

    if not isinstance(capacity, int):
        raise TypeError(
            "Capacity must be an integer"
        )

    if capacity <= 0:
        raise ValueError(
            "Capacity must be greater than zero"
        )

    return True
```

Now the function enforces two rules:

```text
Wrong type
    ↓
TypeError

Wrong value
    ↓
ValueError
```

---

# 24. Multiple Validation Rules

Example:

```python
def validate_drive(device, capacity):

    if not device.startswith("/dev/"):
        raise ValueError(
            f"Invalid device: {device}"
        )

    if capacity <= 0:
        raise ValueError(
            f"Invalid capacity: {capacity}"
        )

    return True
```

This creates a clear validation boundary.

---

# 25. Storage Validation Example

```python
def validate_storage_test(device, block_size):

    if not device.startswith("/dev/"):
        raise ValueError(
            f"Invalid storage device: {device}"
        )

    if block_size <= 0:
        raise ValueError(
            f"Invalid block size: {block_size}"
        )

    return True
```

The function does not silently accept invalid configuration.

---

# 26. `raise` and `return`

Do not confuse them.

```python
return False
```

means:

```text
Function completed normally
and returned False.
```

Whereas:

```python
raise ValueError("Invalid configuration")
```

means:

```text
An exceptional condition occurred.
```

This distinction is important in automation.

---

# 27. `return False` vs `raise`

Consider:

```python
def validate_device(device):

    if not device.startswith("/dev/"):
        return False
```

The caller must remember to check:

```python
if not validate_device(device):
    ...
```

With:

```python
def validate_device(device):

    if not device.startswith("/dev/"):
        raise ValueError("Invalid device")
```

an invalid configuration cannot silently pass through unless the caller explicitly handles the exception.

---

# 28. When Should You Use `raise`?

Use `raise` when:

```text
A condition violates a contract
A value is invalid
An operation cannot safely continue
A required resource is unavailable
A lower layer cannot recover
A failure must be propagated
A custom failure must be communicated
```

---

# 29. When Should You NOT Use `raise`?

Do not use exceptions unnecessarily for normal expected control flow.

Poor:

```python
try:
    value = data["status"]
except KeyError:
    value = "UNKNOWN"
```

This may be valid in some situations, but if missing data is a normal expected case, a clearer design might be:

```python
value = data.get("status", "UNKNOWN")
```

The principle is:

```text
Exceptions
    ↓
Exceptional conditions

Normal alternatives
    ↓
Normal control flow
```

---

# 30. Re-Raising After Logging

A useful production pattern:

```python
def run_test():

    try:
        execute_test()

    except TimeoutError as exc:
        log_error(f"Storage test timeout: {exc}")
        raise
```

This does two things:

```text
1. Records diagnostic information
2. Preserves failure propagation
```

---

# 31. Storage Automation Example

```python
def execute_storage_test(device):

    try:
        run_test(device)

    except TimeoutError as exc:
        print(
            f"Timeout during storage test on {device}: {exc}"
        )
        raise
```

The lower layer does not decide that the entire test framework should continue.

It preserves the failure.

---

# 32. `raise` From a Validation Layer

Consider:

```python
def validate_device(device):

    if device is None:
        raise ValueError("Device cannot be None")

    if not device.startswith("/dev/"):
        raise ValueError(
            f"Invalid device path: {device}"
        )
```

Then:

```python
def run_test(device):

    validate_device(device)
    execute_test(device)
```

If validation fails:

```text
run_test
   ↓
validate_device
   ↓
raise ValueError
   ↓
propagates to run_test caller
```

This creates a clean validation boundary.

---

# 33. `raise` and Custom Exceptions

Later we will create:

```python
class StorageTestError(Exception):
    pass
```

Then:

```python
raise StorageTestError(
    "Storage test failed"
)
```

This allows storage-specific failures to be distinguished from generic Python failures.

Custom exceptions are covered in:

```text
06_Custom_Exceptions.md
```

---

# 34. Exception Chaining Preview

Sometimes we catch one exception and want to raise another while preserving the original cause.

Example:

```python
try:
    open("missing.log")

except OSError as exc:
    raise RuntimeError(
        "Unable to load storage test log"
    ) from exc
```

The:

```python
from exc
```

preserves the relationship between the new exception and the original exception.

We will study exception chaining in detail later.

---

# 35. `raise from None` Preview

Python also supports:

```python
raise NewError(...) from None
```

This suppresses the display of the automatic exception context.

Example:

```python
try:
    int("abc")

except ValueError:
    raise RuntimeError(
        "Configuration contains an invalid number"
    ) from None
```

This is an advanced feature and should be used deliberately.

---

# 36. Exception Boundaries

Consider:

```text
Input
  ↓
Validation
  ↓
Test execution
  ↓
Result processing
  ↓
Reporting
```

Each layer may detect failures.

The important question is:

```text
Which layer understands the failure well enough to handle it?
```

If it cannot recover:

```text
raise
```

can move the failure to a higher layer.

---

# 37. Common Mistake — Raising Generic `Exception`

Avoid:

```python
raise Exception("Bad device")
```

when the problem is clearly a value/configuration issue.

Prefer:

```python
raise ValueError("Invalid device")
```

or, for a domain-specific failure:

```python
raise StorageTestError("Storage test failed")
```

---

# 38. Common Mistake — Losing Context

Bad:

```python
raise ValueError("Failed")
```

Better:

```python
raise ValueError(
    f"Invalid block size: {block_size}"
)
```

Useful context makes troubleshooting much easier.

---

# 39. Common Mistake — Catch and Forget

Bad:

```python
try:
    execute_test()

except TimeoutError:
    print("Timeout")
```

If the caller needs to know the test failed, simply printing may not be enough.

Depending on the architecture:

```python
except TimeoutError as exc:
    log_error(exc)
    raise
```

may be more appropriate.

---

# 40. Common Mistake — Using `raise` Outside an Exception Handler

This:

```python
raise
```

without an active exception context results in an error because there is no current exception to re-raise.

Use:

```python
raise
```

inside an appropriate `except` block when re-raising.

---

# 41. Common Mistake — Raising After Successful Validation

Bad:

```python
if device.startswith("/dev/"):
    raise ValueError("Invalid device")
```

The condition is reversed.

Correct:

```python
if not device.startswith("/dev/"):
    raise ValueError("Invalid device")
```

Always make the validation condition explicit.

---

# 42. Interview Questions

## Q1. What is `raise`?

`raise` explicitly raises an exception.

Example:

```python
raise ValueError("Invalid value")
```

---

## Q2. Why use `raise`?

To enforce application rules, report invalid conditions, stop unsafe execution, or propagate failures.

---

## Q3. Difference between `raise` and `return`?

`return` indicates normal function completion with a value.

`raise` interrupts normal execution by generating an exception.

---

## Q4. What does bare `raise` do?

Inside an active `except` block, bare `raise` re-raises the current exception.

---

## Q5. Why re-raise an exception?

To preserve failure propagation after performing actions such as logging, cleanup preparation, or adding diagnostic information.

---

## Q6. Why should you use specific exception types with `raise`?

Because the exception type communicates the nature of the failure and allows callers to handle it appropriately.

---

## Q7. What is `raise ... from ...`?

It explicitly chains a new exception to the original exception, preserving the original cause.

---

# 43. Storage Engineering Interview Questions

## Q8. Why would you use `raise` during device validation?

To prevent invalid storage configuration from proceeding into test execution.

Example:

```python
if not device.startswith("/dev/"):
    raise ValueError(
        f"Invalid device path: {device}"
    )
```

---

## Q9. A low-level storage function catches an exception. Should it always handle it completely?

No.

If the function cannot safely recover, it can log relevant information and re-raise the exception so a higher-level component can make the appropriate decision.

---

## Q10. Why is this useful?

```python
except TimeoutError as exc:
    log_error(exc)
    raise
```

Because it:

```text
records the failure
      +
preserves the original exception
      +
allows higher-level handling
```

---

## Q11. Why is this better than:

```python
except TimeoutError:
    print("Timeout")
```

Because merely printing the failure may allow the program to continue without the higher-level framework knowing that the operation failed.

---

# 44. Knowledge-Gap Checklist

Before moving to custom exceptions:

```text
[ ] What `raise` does
[ ] Raising built-in exceptions
[ ] Raising with a message
[ ] Validation with `raise`
[ ] `raise` inside functions
[ ] `raise` with try/except
[ ] `raise` vs return
[ ] Bare `raise`
[ ] Re-raising
[ ] Preserving original exceptions
[ ] Choosing correct exception types
[ ] Useful error messages
[ ] Logging + re-raising
[ ] `raise ... from ...`
[ ] `raise ... from None`
[ ] Exception boundaries
[ ] Storage validation
[ ] Storage test failure propagation
```

---

# 45. Final Mental Model

There are three important patterns:

## Pattern 1 — Create a failure

```python
raise ValueError("Invalid configuration")
```

```text
Condition
   ↓
raise
   ↓
New exception
```

---

## Pattern 2 — Handle a failure

```python
try:
    operation()

except ValueError:
    handle()
```

```text
Exception
   ↓
except
   ↓
Handle
```

---

## Pattern 3 — Preserve and propagate a failure

```python
try:
    operation()

except ValueError as exc:
    log_error(exc)
    raise
```

```text
Exception
   ↓
Catch
   ↓
Log
   ↓
raise
   ↓
Propagate original exception
```

---

# 46. Final Engineering Rule

The key principle is:

```text
Use `raise` to make invalid or unsafe conditions explicit.

Use specific exception types.

Provide useful context.

If you cannot recover safely, do not silently swallow
the failure — propagate it appropriately.
```

For Storage Test Automation:

```text
Invalid configuration
        ↓
raise
        ↓
Prevent unsafe test execution

Runtime failure
        ↓
log + raise
        ↓
Preserve evidence and notify higher layer
```

# END

````

