# 06 — Custom Exceptions

## Objective

Python provides many built-in exceptions such as:

- `ValueError`
- `TypeError`
- `FileNotFoundError`
- `PermissionError`
- `OSError`
- `TimeoutError`

These are useful for general-purpose failures.

However, real applications often have **domain-specific failures**.

For example, a Storage Test Automation framework may need to distinguish:

```text
StorageTestError
DeviceValidationError
DeviceNotFoundError
StorageTestTimeoutError
StorageConfigurationError
````

Python allows us to create these using **custom exceptions**.

---

# 1. What Is a Custom Exception?

A custom exception is an exception class created by the programmer for a specific application or domain.

Example:

```python
class StorageTestError(Exception):
    pass
```

Now we have our own exception:

```python
StorageTestError
```

---

# 2. Why Create Custom Exceptions?

Built-in exceptions describe general programming failures.

Custom exceptions allow us to describe failures in the application's own terminology.

For example:

```text
Generic:
OSError

Domain-specific:
StorageTestError
```

This makes large applications easier to understand and maintain.

---

# 3. Basic Custom Exception

```python
class StorageTestError(Exception):
    pass
```

The important part is:

```python
(Exception)
```

Our custom exception inherits from Python's built-in `Exception`.

---

# 4. Raising a Custom Exception

Once defined:

```python
class StorageTestError(Exception):
    pass
```

we can raise it:

```python
raise StorageTestError("Storage test failed")
```

Output:

```text
StorageTestError: Storage test failed
```

---

# 5. Catching a Custom Exception

```python
class StorageTestError(Exception):
    pass


try:
    raise StorageTestError("Storage test failed")

except StorageTestError as exc:
    print(f"Test failure: {exc}")
```

Output:

```text
Test failure: Storage test failed
```

Flow:

```text
Custom condition
      ↓
raise StorageTestError
      ↓
except StorageTestError
      ↓
Handle failure
```

---

# 6. Custom Exception as a Domain Boundary

Consider:

```python
class StorageTestError(Exception):
    pass
```

Now the application can communicate:

```text
This is not simply a generic Python failure.

This is specifically a Storage Test failure.
```

That distinction becomes valuable in larger automation frameworks.

---

# 7. Naming Custom Exceptions

Python convention is to use a descriptive name ending in:

```text
Error
```

Examples:

```python
StorageTestError
DeviceValidationError
StorageConfigurationError
TestExecutionError
LogParsingError
```

Avoid vague names such as:

```python
Problem
Failure
SomethingWrong
```

Use names that communicate the failure category.

---

# 8. Custom Exception for Device Validation

Example:

```python
class DeviceValidationError(Exception):
    pass
```

Then:

```python
def validate_device(device):

    if not device.startswith("/dev/"):
        raise DeviceValidationError(
            f"Invalid device: {device}"
        )
```

Usage:

```python
try:
    validate_device("invalid_device")

except DeviceValidationError as exc:
    print(f"Validation failed: {exc}")
```

---

# 9. Why Not Just Use `ValueError`?

We could write:

```python
raise ValueError("Invalid device")
```

That is perfectly reasonable for a small program.

But in a larger storage framework, we may want:

```python
raise DeviceValidationError("Invalid device")
```

because the caller can distinguish:

```text
Device validation failure
```

from:

```text
Other ValueError
```

---

# 10. Custom Exceptions Improve Classification

Imagine a large automation framework.

It may produce:

```text
ValueError
TypeError
OSError
StorageTestError
DeviceValidationError
LogParsingError
```

A higher-level component can specifically handle:

```python
except DeviceValidationError:
    ...
```

without accidentally catching unrelated `ValueError` exceptions.

---

# 11. Custom Exception With No Additional Code

The simplest form is:

```python
class StorageTestError(Exception):
    pass
```

This is called a simple/custom exception class.

It inherits all the normal behavior from `Exception`.

---

# 12. Custom Exception With a Constructor

A custom exception can define its own attributes.

Example:

```python
class StorageTestError(Exception):

    def __init__(self, message, device):
        super().__init__(message)
        self.device = device
```

Now:

```python
raise StorageTestError(
    "Storage test failed",
    "/dev/sda"
)
```

The exception contains:

```text
message
device
```

---

# 13. Accessing Custom Exception Data

Example:

```python
class StorageTestError(Exception):

    def __init__(self, message, device):
        super().__init__(message)
        self.device = device
```

Then:

```python
try:
    raise StorageTestError(
        "Read test failed",
        "/dev/sda"
    )

except StorageTestError as exc:
    print(exc)
    print(exc.device)
```

Output:

```text
Read test failed
/dev/sda
```

---

# 14. Why Store Additional Data?

In automation, a message alone may not be enough.

Instead of:

```text
Storage test failed
```

we may need:

```text
Device: /dev/sda
Operation: READ
Test: sequential_read
Reason: timeout
```

Structured information makes troubleshooting easier.

---

# 15. Custom Exception With Multiple Attributes

Example:

```python
class StorageTestError(Exception):

    def __init__(self, message, device, operation):
        super().__init__(message)
        self.device = device
        self.operation = operation
```

Usage:

```python
raise StorageTestError(
    "Read operation failed",
    "/dev/sda",
    "READ"
)
```

Now the exception contains:

```text
message
device
operation
```

---

# 16. Catching the Structured Exception

```python
try:
    raise StorageTestError(
        "Read operation failed",
        "/dev/sda",
        "READ"
    )

except StorageTestError as exc:

    print("Message:", exc)
    print("Device:", exc.device)
    print("Operation:", exc.operation)
```

This is useful when building structured automation reports.

---

# 17. Always Call the Parent Constructor

When overriding `__init__`, use:

```python
super().__init__(message)
```

Example:

```python
class StorageTestError(Exception):

    def __init__(self, message, device):
        super().__init__(message)
        self.device = device
```

This preserves the normal exception message behavior.

---

# 18. Custom Exception Hierarchy

Custom exceptions can also have their own hierarchy.

Example:

```python
class StorageError(Exception):
    pass


class DeviceValidationError(StorageError):
    pass


class StorageTestError(StorageError):
    pass
```

Hierarchy:

```text
Exception
    |
    +-- StorageError
          |
          +-- DeviceValidationError
          |
          +-- StorageTestError
```

---

# 19. Why Create a Parent Custom Exception?

This allows higher-level code to catch all storage-related failures:

```python
except StorageError:
    ...
```

while still allowing specific handling:

```python
except DeviceValidationError:
    ...
```

This is very useful in enterprise automation.

---

# 20. Specific and General Storage Exceptions

Example:

```python
class StorageError(Exception):
    pass


class DeviceValidationError(StorageError):
    pass


class StorageTestError(StorageError):
    pass
```

Then:

```python
try:
    run_storage_test()

except DeviceValidationError:
    print("Device validation failed")

except StorageTestError:
    print("Storage test failed")

except StorageError:
    print("Other storage-related failure")
```

---

# 21. Exception Ordering Still Matters

Because:

```text
DeviceValidationError
        ↓
StorageError
```

the specific handler should come first.

Correct:

```python
except DeviceValidationError:
    ...

except StorageError:
    ...
```

Incorrect:

```python
except StorageError:
    ...

except DeviceValidationError:
    ...
```

The general handler would catch the child exception first.

---

# 22. Custom Exception Hierarchy Design

A practical hierarchy might be:

```text
Exception
   |
   +-- StorageError
         |
         +-- StorageConfigurationError
         |
         +-- DeviceValidationError
         |
         +-- StorageTestError
         |
         +-- StorageTimeoutError
         |
         +-- LogParsingError
```

This allows failures to be classified at multiple levels.

---

# 23. Storage Configuration Error

```python
class StorageConfigurationError(StorageError):
    pass
```

Usage:

```python
def validate_config(config):

    if "device" not in config:
        raise StorageConfigurationError(
            "Device is missing from configuration"
        )
```

This is more meaningful than a generic:

```python
Exception("Invalid configuration")
```

---

# 24. Device Validation Error

```python
class DeviceValidationError(StorageError):
    pass
```

Example:

```python
def validate_device(device):

    if not device.startswith("/dev/"):
        raise DeviceValidationError(
            f"Invalid device path: {device}"
        )
```

---

# 25. Storage Test Error

```python
class StorageTestError(StorageError):
    pass
```

Example:

```python
def execute_test(device):

    if test_failed:
        raise StorageTestError(
            f"Storage test failed on {device}"
        )
```

---

# 26. Storage Timeout Error

```python
class StorageTimeoutError(StorageTestError):
    pass
```

Now:

```text
Exception
   ↓
StorageError
   ↓
StorageTestError
   ↓
StorageTimeoutError
```

A timeout can therefore be handled specifically:

```python
except StorageTimeoutError:
    retry_test()
```

while still being recognized as:

```text
StorageTestError
```

and:

```text
StorageError
```

---

# 27. Log Parsing Error

```python
class LogParsingError(StorageError):
    pass
```

Example:

```python
def parse_log(line):

    if not valid_format(line):
        raise LogParsingError(
            f"Invalid log record: {line}"
        )
```

This allows log-processing failures to be distinguished from device failures.

---

# 28. Why This Matters in Storage Automation

Consider a complete framework:

```text
Configuration
      ↓
Device Validation
      ↓
Test Execution
      ↓
Log Parsing
      ↓
Result Reporting
```

Different stages can produce different custom exceptions.

```text
Configuration
    ↓
StorageConfigurationError

Device Validation
    ↓
DeviceValidationError

Test Execution
    ↓
StorageTestError

Timeout
    ↓
StorageTimeoutError

Log Parsing
    ↓
LogParsingError
```

This makes the automation architecture much easier to reason about.

---

# 29. Custom Exception + `raise`

Example:

```python
class DeviceValidationError(StorageError):
    pass


def validate_device(device):

    if not device.startswith("/dev/"):
        raise DeviceValidationError(
            f"Invalid device path: {device}"
        )
```

The validation layer is responsible for identifying the problem.

---

# 30. Custom Exception + `try/except`

```python
try:
    validate_device("/invalid")

except DeviceValidationError as exc:
    print(f"Validation failed: {exc}")
```

The caller decides how to handle it.

---

# 31. Custom Exception + Re-Raising

A lower-level component can log and propagate:

```python
try:
    validate_device(device)

except DeviceValidationError as exc:
    log_error(exc)
    raise
```

This preserves the original exception.

---

# 32. Custom Exception + Exception Chaining

Sometimes we want to convert a low-level failure into a domain-specific failure.

Example:

```python
class LogParsingError(StorageError):
    pass
```

Then:

```python
try:
    data = int(value)

except ValueError as exc:
    raise LogParsingError(
        "Invalid numeric field in storage log"
    ) from exc
```

Now the application sees:

```text
LogParsingError
```

while the original:

```text
ValueError
```

is preserved as the cause.

---

# 33. Why Exception Chaining Is Useful

Suppose the low-level failure is:

```text
ValueError
```

But the application-level meaning is:

```text
Storage log parsing failed
```

The custom exception provides domain context while preserving the original technical cause.

Conceptually:

```text
Original cause
    ↓
ValueError
    ↓
wrapped with context
    ↓
LogParsingError
```

---

# 34. Do Not Create Custom Exceptions for Everything

Custom exceptions are useful when they provide meaningful domain classification.

Do not create:

```text
One custom exception for every line of code
```

Instead, create them when:

```text
The application has a meaningful failure category
        +
Callers may need to handle that category differently
```

---

# 35. Custom Exception vs Built-in Exception

Use a built-in exception when the built-in type already communicates the problem clearly.

Example:

```python
raise ValueError("Capacity must be positive")
```

is perfectly reasonable.

Use a custom exception when the failure has domain-specific meaning.

Example:

```python
raise DeviceValidationError(
    "Unsupported storage device"
)
```

---

# 36. Practical Decision

Ask:

```text
Does a built-in exception describe this failure well?
       |
   Yes → Use it
       |
   No
       ↓
Does the application need a domain-specific category?
       |
   Yes → Create custom exception
```

---

# 37. Common Mistake — Forgetting `Exception`

Bad:

```python
class StorageTestError:
    pass
```

This does not create a normal exception type.

Correct:

```python
class StorageTestError(Exception):
    pass
```

Then:

```python
raise StorageTestError("Test failed")
```

---

# 38. Common Mistake — Using Generic Exception Everywhere

Avoid:

```python
raise Exception("Device validation failed")
```

when you have a meaningful domain exception:

```python
raise DeviceValidationError(
    "Device validation failed"
)
```

The latter allows targeted handling.

---

# 39. Common Mistake — Poor Custom Exception Names

Avoid:

```python
class BadThing(Exception):
    pass
```

Prefer:

```python
class DeviceValidationError(Exception):
    pass
```

The name should explain the failure.

---

# 40. Common Mistake — Losing the Original Cause

Bad:

```python
try:
    parse_log()

except ValueError:
    raise LogParsingError("Log parsing failed")
```

The original cause may be less explicit in the exception chain.

Better:

```python
try:
    parse_log()

except ValueError as exc:
    raise LogParsingError(
        "Log parsing failed"
    ) from exc
```

Now the original failure is preserved as the cause.

---

# 41. Common Mistake — Catching the Parent Too Early

Given:

```python
class StorageError(Exception):
    pass


class DeviceValidationError(StorageError):
    pass
```

Avoid:

```python
try:
    validate_device()

except StorageError:
    print("Storage error")

except DeviceValidationError:
    print("Device validation error")
```

Correct:

```python
try:
    validate_device()

except DeviceValidationError:
    print("Device validation error")

except StorageError:
    print("Other storage error")
```

---

# 42. Custom Exceptions and API Design

Custom exceptions can define a clear contract between layers.

For example:

```text
Validation Layer
       ↓
DeviceValidationError
       ↓
Test Runner
       ↓
Report failure
```

The caller does not need to inspect arbitrary strings to determine what happened.

---

# 43. Custom Exceptions and Automation Reporting

A test framework can use the exception type to classify results:

```text
DeviceValidationError
    → CONFIGURATION / VALIDATION FAILURE

StorageTimeoutError
    → TIMEOUT / POSSIBLE RETRY

StorageTestError
    → TEST FAILURE

LogParsingError
    → INFRASTRUCTURE / RESULT PROCESSING FAILURE
```

This is much more reliable than parsing messages such as:

```text
"something failed"
```

---

# 44. Example — Complete Storage Exception Hierarchy

```python
class StorageError(Exception):
    pass


class StorageConfigurationError(StorageError):
    pass


class DeviceValidationError(StorageError):
    pass


class StorageTestError(StorageError):
    pass


class StorageTimeoutError(StorageTestError):
    pass


class LogParsingError(StorageError):
    pass
```

Hierarchy:

```text
Exception
   |
   +-- StorageError
         |
         +-- StorageConfigurationError
         |
         +-- DeviceValidationError
         |
         +-- StorageTestError
         |      |
         |      +-- StorageTimeoutError
         |
         +-- LogParsingError
```

---

# 45. Example — Complete Flow

```python
class StorageError(Exception):
    pass


class DeviceValidationError(StorageError):
    pass


class StorageTestError(StorageError):
    pass


def validate_device(device):

    if not device.startswith("/dev/"):
        raise DeviceValidationError(
            f"Invalid device: {device}"
        )


def run_test(device):

    validate_device(device)

    raise StorageTestError(
        f"Test failed on {device}"
    )


try:
    run_test("/dev/sda")

except DeviceValidationError as exc:
    print(f"Validation failure: {exc}")

except StorageTestError as exc:
    print(f"Test failure: {exc}")

except StorageError as exc:
    print(f"Storage failure: {exc}")
```

The caller now has a structured way to classify failures.

---

# 46. Interview Questions

## Q1. What is a custom exception?

A programmer-defined exception class used to represent a domain-specific failure.

---

## Q2. Why should custom exceptions inherit from `Exception`?

Because `Exception` is the standard base class for normal application-level exceptions and provides the expected exception behavior.

---

## Q3. How do you create a custom exception?

```python
class StorageTestError(Exception):
    pass
```

---

## Q4. How do you raise it?

```python
raise StorageTestError("Storage test failed")
```

---

## Q5. Can custom exceptions have additional attributes?

Yes.

Example:

```python
class StorageTestError(Exception):

    def __init__(self, message, device):
        super().__init__(message)
        self.device = device
```

---

## Q6. Can custom exceptions inherit from other custom exceptions?

Yes.

Example:

```python
class StorageError(Exception):
    pass


class StorageTestError(StorageError):
    pass
```

---

## Q7. Why create a custom exception hierarchy?

It allows both specific and broad handling.

For example:

```python
except StorageTimeoutError:
    ...

except StorageError:
    ...
```

---

## Q8. Should every error have a custom exception?

No.

Use a built-in exception when it already clearly represents the failure. Create a custom exception when the application needs a meaningful domain-specific category.

---

# 47. Storage Engineering Interview Questions

## Q9. Why would a Storage Test Automation framework need custom exceptions?

To classify domain-specific failures such as:

```text
Device validation failure
Storage test failure
Storage timeout
Configuration failure
Log parsing failure
```

This allows the framework to apply different recovery and reporting strategies.

---

## Q10. Why might `StorageTimeoutError` inherit from `StorageTestError`?

Because a timeout is a specific type of storage test failure.

This provides:

```text
Specific handling:
StorageTimeoutError

General handling:
StorageTestError
```

---

## Q11. Why is this useful?

The framework could:

```text
StorageTimeoutError
    ↓
Retry according to policy

Other StorageTestError
    ↓
Fail test

StorageError
    ↓
General storage failure handling
```

---

## Q12. Why use exception chaining when converting `ValueError` into `LogParsingError`?

Because the application gets a meaningful domain-specific exception while preserving the original technical cause.

---

# 48. Knowledge-Gap Checklist

Before moving to Exception Hierarchy:

```text
[ ] What custom exceptions are
[ ] Why custom exceptions are useful
[ ] Creating custom exceptions
[ ] Raising custom exceptions
[ ] Catching custom exceptions
[ ] Naming conventions
[ ] Custom exception attributes
[ ] `super().__init__()`
[ ] Custom exception hierarchy
[ ] Parent custom exception
[ ] Child custom exception
[ ] Specific vs general handling
[ ] Built-in vs custom exceptions
[ ] Custom exceptions in validation
[ ] Custom exceptions in storage automation
[ ] Exception chaining
[ ] Preserving original causes
[ ] Avoiding unnecessary custom exceptions
```

---

# 49. Final Mental Model

```text
Built-in exception
        |
        | already describes failure?
        |
       YES
        ↓
Use built-in exception

       NO
        ↓
Domain-specific failure?
        |
       YES
        ↓
Create custom exception
        |
        ↓
Add to appropriate hierarchy
        |
        ↓
Raise
        |
        ↓
Catch specifically or propagate
```

For Storage Engineering:

```text
                    StorageError
                         |
        ┌────────────────┼────────────────┐
        |                |                |
Configuration      Validation          TestError
        |                |                |
        |                |          TimeoutError
        |                |
        └────────────────┴───────────────┐
                                         |
                                  LogParsingError
```

---

# 50. Final Engineering Rule

Custom exceptions should answer one question clearly:

> **What kind of failure happened in my application's domain?**

Use them to provide:

```text
Meaningful classification
        +
Clear exception hierarchy
        +
Targeted handling
        +
Better reporting
        +
Better troubleshooting
```

Do not create custom exceptions merely to make the code look more advanced.

Create them when they provide **real semantic value**.

# END

````
