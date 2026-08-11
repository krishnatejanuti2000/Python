# 08 — Exception Handling Patterns

## Objective

This document brings together the exception-handling techniques learned so far and shows how they are applied in real Python programs.

We will focus on:

- Specific exception handling
- Multiple exception handling
- Exception tuples
- `else`
- `finally`
- `raise`
- Re-raising
- Custom exceptions
- Exception hierarchy
- Validation patterns
- Logging and propagation
- Resource cleanup
- Storage Test Automation patterns
- Good and bad exception-handling designs

---

# 1. Why Exception Handling Patterns Matter

Knowing individual keywords is not enough.

We need to understand how they work together:

```text
try
 ↓
Attempt operation
 ↓
Success / Failure
 ↓
except / else
 ↓
finally
 ↓
Return / Continue / Propagate
````

A production program should have a deliberate strategy for failures.

---

# 2. Pattern — Specific Exception Handling

Use a specific exception when you know exactly what failure you want to handle.

```python
try:
    value = int(user_input)

except ValueError:
    print("Invalid integer")
```

This is preferable to:

```python
try:
    value = int(user_input)

except Exception:
    print("Something went wrong")
```

because the first version communicates exactly what failure is expected.

---

# 3. Pattern — Multiple Specific Exceptions

When different exceptions need different handling:

```python
try:
    value = int(user_input)
    result = 100 / value

except ValueError:
    print("Invalid input")

except ZeroDivisionError:
    print("Zero is not allowed")
```

Flow:

```text
ValueError
    ↓
ValueError handler

ZeroDivisionError
    ↓
ZeroDivisionError handler
```

---

# 4. Pattern — Same Handling for Multiple Exceptions

If multiple exceptions genuinely require the same handling:

```python
try:
    process_input()

except (ValueError, TypeError):
    print("Invalid input")
```

Use a tuple rather than duplicating identical handlers.

---

# 5. Pattern — Specific Before General

Consider:

```python
try:
    open("missing.log")

except FileNotFoundError:
    print("File missing")

except OSError:
    print("Other OS error")
```

This is correct because:

```text
FileNotFoundError
       ↓
OSError
```

The specific exception comes first.

General rule:

```text
Specific
   ↓
Parent
   ↓
General fallback
```

---

# 6. Pattern — General Fallback

Sometimes an application layer needs a broad fallback:

```python
try:
    operation()

except ValueError:
    print("Invalid value")

except Exception as exc:
    print(f"Unexpected application error: {exc}")
```

The general handler should normally be last.

---

# 7. Pattern — `else` for Successful Processing

Use `else` when some code should execute only if the `try` operation succeeds.

```python
try:
    value = int(user_input)

except ValueError:
    print("Invalid input")

else:
    print("Input accepted")
    process(value)
```

Mental model:

```text
try succeeds
    ↓
else

try fails
    ↓
except
```

---

# 8. Pattern — `finally` for Cleanup

Use `finally` for actions that should happen during normal cleanup/finalization.

```python
try:
    start_operation()

except RuntimeError:
    print("Operation failed")

finally:
    cleanup()
```

Flow:

```text
Success ─────┐
             ↓
          finally
             ↓
          cleanup

Failure ─────┘
```

---

# 9. Pattern — Complete Structure

A complete pattern:

```python
try:
    value = int(user_input)

except ValueError:
    print("Invalid input")

else:
    process(value)

finally:
    cleanup()
```

Responsibilities:

```text
try
→ risky operation

except
→ failure handling

else
→ successful processing

finally
→ cleanup
```

---

# 10. Pattern — Validation With `raise`

Use `raise` when application rules are violated.

```python
def validate_capacity(capacity):

    if capacity <= 0:
        raise ValueError(
            "Capacity must be greater than zero"
        )
```

Python itself permits:

```python
capacity = -100
```

but the application does not.

Therefore:

```text
Invalid application state
        ↓
raise
        ↓
ValueError
```

---

# 11. Pattern — Type Validation

```python
def validate_capacity(capacity):

    if not isinstance(capacity, int):
        raise TypeError(
            "Capacity must be an integer"
        )
```

Now:

```text
Wrong type
    ↓
TypeError
```

and:

```text
Correct type but invalid value
    ↓
ValueError
```

---

# 12. Pattern — Multiple Validation Rules

```python
def validate_device(device, capacity):

    if not isinstance(device, str):
        raise TypeError(
            "Device must be a string"
        )

    if not device.startswith("/dev/"):
        raise ValueError(
            f"Invalid device path: {device}"
        )

    if capacity <= 0:
        raise ValueError(
            f"Invalid capacity: {capacity}"
        )
```

The validation function stops when a rule is violated.

---

# 13. Pattern — Validate Before Executing

Good automation design:

```text
Input
  ↓
Validation
  ↓
Test execution
  ↓
Result processing
```

Not:

```text
Input
  ↓
Start test
  ↓
Discover invalid configuration
```

Example:

```python
validate_device(device)
validate_capacity(capacity)

run_storage_test(device)
```

---

# 14. Pattern — Custom Domain Exception

When a failure has domain-specific meaning:

```python
class StorageError(Exception):
    pass
```

Then:

```python
raise StorageError(
    "Storage operation failed"
)
```

This allows callers to distinguish storage failures from unrelated application exceptions.

---

# 15. Pattern — Custom Exception Hierarchy

A larger framework can define:

```python
class StorageError(Exception):
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
          +-- DeviceValidationError
          |
          +-- StorageTestError
          |      |
          |      +-- StorageTimeoutError
          |
          +-- LogParsingError
```

---

# 16. Pattern — Specific Custom Handling

```python
try:
    run_storage_test()

except StorageTimeoutError:
    print("Storage test timed out")

except StorageTestError:
    print("Storage test failed")

except StorageError:
    print("Storage-related failure")
```

Because of inheritance:

```text
StorageTimeoutError
        ↓
StorageTestError
        ↓
StorageError
```

the most specific handler comes first.

---

# 17. Pattern — Logging and Re-Raising

Sometimes the current layer can record the failure but cannot recover from it.

```python
try:
    run_storage_test()

except StorageTestError as exc:
    log_error(exc)
    raise
```

Flow:

```text
Failure
   ↓
Catch
   ↓
Log
   ↓
Re-raise
   ↓
Higher layer handles it
```

This prevents the failure from being silently swallowed.

---

# 18. Pattern — Re-Raise the Original Exception

Bare:

```python
raise
```

inside an active `except` block re-raises the current exception.

Example:

```python
try:
    process()

except ValueError as exc:
    log_error(exc)
    raise
```

The original exception continues propagating.

---

# 19. Pattern — Convert Low-Level Error to Domain Error

Sometimes a lower-level exception is technically correct but not meaningful enough for the application.

Example:

```python
class LogParsingError(StorageError):
    pass
```

Then:

```python
try:
    value = int(field)

except ValueError as exc:
    raise LogParsingError(
        "Invalid numeric field in storage log"
    ) from exc
```

Now the application receives:

```text
LogParsingError
```

while the original:

```text
ValueError
```

is preserved as the cause.

---

# 20. Pattern — Exception Chaining

Use:

```python
raise NewException(...) from exc
```

Example:

```python
try:
    open("storage.log")

except OSError as exc:
    raise StorageError(
        "Unable to load storage log"
    ) from exc
```

Conceptually:

```text
Original failure
      ↓
OSError
      ↓
Application context
      ↓
StorageError
```

---

# 21. Pattern — Resource Cleanup

For manually managed resources:

```python
resource = acquire_resource()

try:
    use_resource(resource)

finally:
    release_resource(resource)
```

The important pattern is:

```text
Acquire
   ↓
Use
   ↓
Release
```

---

# 22. Pattern — Prefer Context Managers for Supported Resources

For files:

```python
with open("storage.log", "r") as file:
    data = file.read()
```

This automatically manages the file resource.

Instead of manually:

```python
file = open("storage.log", "r")

try:
    data = file.read()

finally:
    file.close()
```

Use `with` when the resource supports the context-manager protocol.

---

# 23. Pattern — Storage Test Cleanup

Example:

```python
test_started = False

try:
    start_storage_test("/dev/sda")
    test_started = True

    result = collect_result()

except StorageTestError as exc:
    print(f"Test failed: {exc}")

finally:
    if test_started:
        stop_storage_test("/dev/sda")

    collect_diagnostics()
```

The important principle is:

```text
Test failure
    ↓
Do not leave test environment dirty
```

---

# 24. Pattern — Success Processing With `else`

```python
try:
    result = run_storage_test("/dev/sda")

except StorageTestError as exc:
    print(f"Test failed: {exc}")

else:
    generate_report(result)

finally:
    collect_diagnostics()
```

Responsibilities are clearly separated:

```text
try
→ execute

except
→ failure

else
→ success

finally
→ cleanup/diagnostics
```

---

# 25. Pattern — Retry Only Appropriate Failures

Do not retry every exception.

Example:

```python
try:
    run_storage_test()

except StorageTimeoutError:
    retry_test()
```

But:

```python
except DeviceValidationError:
    fail_configuration()
```

A configuration error generally should not be blindly retried.

---

# 26. Pattern — Retry With a Limit

A simple retry design:

```python
max_retries = 3

for attempt in range(max_retries):

    try:
        run_storage_test()
        break

    except StorageTimeoutError:
        print(f"Attempt {attempt + 1} timed out")
```

A real framework should also decide what happens when all retries fail.

---

# 27. Pattern — Do Not Retry Invalid Configuration

Bad:

```python
try:
    validate_device(device)

except DeviceValidationError:
    retry()
```

This can repeatedly execute the same invalid configuration.

Better:

```python
try:
    validate_device(device)

except DeviceValidationError as exc:
    report_configuration_failure(exc)
```

---

# 28. Pattern — Preserve Diagnostic Evidence

When a storage test fails, useful information may include:

```text
Device
Operation
Timestamp
Exception type
Exception message
Command
Exit status
stdout
stderr
Retry count
Relevant system state
```

A handler should not destroy useful diagnostic information.

---

# 29. Pattern — Catch Only What You Can Handle

Bad:

```python
try:
    operation()

except Exception:
    print("Failed")
```

If the current layer cannot recover meaningfully, broad catching can hide failures.

Prefer:

```python
try:
    operation()

except SpecificKnownError as exc:
    handle_known_case(exc)
```

and allow unexpected failures to propagate when appropriate.

---

# 30. Pattern — Narrow `try` Blocks

Prefer:

```python
try:
    data = read_log()

except FileNotFoundError:
    handle_missing_log()

parse_log(data)
generate_report(data)
```

rather than:

```python
try:
    data = read_log()
    parse_log(data)
    generate_report(data)

except Exception:
    print("Something failed")
```

The narrow version makes failure location clearer.

---

# 31. Why Narrow `try` Blocks Matter

Suppose:

```python
try:
    read_log()
    parse_log()
    generate_report()
except Exception:
    print("Failed")
```

Which operation failed?

```text
read?
parse?
report?
```

The exception boundary is too broad.

A focused design makes troubleshooting easier.

---

# 32. Pattern — Separate Failure Domains

For a storage framework:

```text
Configuration
      ↓
Validation
      ↓
Execution
      ↓
Log Parsing
      ↓
Reporting
```

Each stage can have its own failure category.

Example:

```text
Configuration
→ StorageConfigurationError

Validation
→ DeviceValidationError

Execution
→ StorageTestError

Timeout
→ StorageTimeoutError

Parsing
→ LogParsingError
```

---

# 33. Pattern — Exception at the Right Layer

Ask:

```text
Can this layer recover?
```

If yes:

```text
Handle
```

If no:

```text
Propagate
```

Mental model:

```text
Low-level layer
      ↓
Detect failure
      ↓
Can recover?
   /        \
 Yes        No
  ↓          ↓
Handle     raise
```

---

# 34. Pattern — Don't Use Exceptions for Normal Flow

Exceptions should represent exceptional conditions.

Avoid unnecessarily using:

```python
try:
    value = dictionary["status"]

except KeyError:
    value = "UNKNOWN"
```

when a normal lookup is more appropriate:

```python
value = dictionary.get("status", "UNKNOWN")
```

The exact choice depends on the application, but the principle remains:

```text
Normal condition
    ↓
Normal control flow

Exceptional condition
    ↓
Exception
```

---

# 35. Pattern — Meaningful Error Messages

Bad:

```python
raise ValueError("Invalid")
```

Better:

```python
raise ValueError(
    f"Invalid block size: {block_size}"
)
```

For storage:

```python
raise DeviceValidationError(
    f"Unsupported device path: {device}"
)
```

Good messages help troubleshooting.

---

# 36. Pattern — Structured Exception Data

If the framework needs structured information:

```python
class StorageTestError(Exception):

    def __init__(self, message, device, operation):
        super().__init__(message)
        self.device = device
        self.operation = operation
```

Then:

```python
raise StorageTestError(
    "Read operation failed",
    "/dev/sda",
    "READ"
)
```

The caller can access:

```python
except StorageTestError as exc:
    print(exc.device)
    print(exc.operation)
```

---

# 37. Pattern — Top-Level Exception Boundary

A top-level application may have a final safety boundary:

```python
def main():

    try:
        run_test_suite()

    except Exception as exc:
        log_error(exc)
        return 1

    return 0
```

This should be used deliberately.

The lower layers should still classify meaningful failures rather than allowing everything to become:

```text
Something failed
```

---

# 38. Pattern — Main Application Flow

A storage automation program might conceptually look like:

```text
main()
  |
  +-- Load configuration
  |
  +-- Validate configuration
  |
  +-- Validate device
  |
  +-- Execute test
  |
  +-- Parse result
  |
  +-- Generate report
  |
  +-- Cleanup
```

Failure handling:

```text
Configuration
    ↓
StorageConfigurationError

Device
    ↓
DeviceValidationError

Test
    ↓
StorageTestError

Timeout
    ↓
StorageTimeoutError

Parsing
    ↓
LogParsingError
```

---

# 39. Complete Storage Test Pattern

```python
class StorageError(Exception):
    pass


class DeviceValidationError(StorageError):
    pass


class StorageTestError(StorageError):
    pass


class StorageTimeoutError(StorageTestError):
    pass


def validate_device(device):

    if not device.startswith("/dev/"):
        raise DeviceValidationError(
            f"Invalid device: {device}"
        )


def run_test(device):

    try:
        execute_test(device)

    except TimeoutError as exc:
        raise StorageTimeoutError(
            f"Storage test timed out on {device}"
        ) from exc


def main(device):

    validate_device(device)

    try:
        result = run_test(device)

    except StorageTimeoutError as exc:
        print(f"Timeout: {exc}")
        return "RETRY"

    except StorageTestError as exc:
        print(f"Test failure: {exc}")
        return "FAIL"

    else:
        print("Test completed successfully")
        return "PASS"

    finally:
        collect_diagnostics(device)
```

The architecture is:

```text
Validate
   ↓
Execute
   ↓
Classify
   ↓
Handle
   ↓
Report
   ↓
Cleanup
```

---

# 40. What This Pattern Gives Us

The framework can distinguish:

```text
RETRY
FAIL
PASS
```

instead of treating every problem as:

```text
ERROR
```

This is the real value of structured exception handling.

---

# 41. Bad Enterprise Pattern

Avoid:

```python
try:
    everything()

except:
    print("Test failed")
```

Problems:

```text
No failure classification
No diagnostic context
May hide bugs
May catch unintended control-flow exceptions
No recovery strategy
Difficult troubleshooting
```

---

# 42. Better Enterprise Pattern

Prefer:

```text
Specific exceptions
        ↓
Meaningful classification
        ↓
Appropriate recovery
        ↓
Useful logging
        ↓
Cleanup
        ↓
Propagation when necessary
```

---

# 43. Exception Handling Decision Tree

Use this decision process:

```text
                Operation
                    |
              Can it fail?
                    |
                   Yes
                    |
          What failures are expected?
                    |
          ┌─────────┴─────────┐
          |                   |
      Known failure       Unknown failure
          |                   |
          ↓                   ↓
   Specific except      Propagate or
                         broad boundary
          |
    Can we recover?
      /       \
    Yes       No
     |         |
   Handle    raise
     |
     ↓
Was resource cleanup required?
          |
         Yes
          ↓
       finally
```

---

# 44. Exception Handling Checklist

Before finalizing a function, ask:

```text
[ ] What can fail?
[ ] Which exceptions are expected?
[ ] Which exceptions should be handled here?
[ ] Which should propagate?
[ ] Are specific handlers before general handlers?
[ ] Am I catching more than necessary?
[ ] Is retry appropriate?
[ ] Is cleanup required?
[ ] Is `finally` needed?
[ ] Is `else` useful?
[ ] Are error messages meaningful?
[ ] Is diagnostic information preserved?
[ ] Should a custom exception be used?
[ ] Is exception chaining useful?
[ ] Could this handler hide a real bug?
```

---

# 45. Interview Questions

## Q1. What is a good exception-handling strategy?

Identify expected failures, handle them at the appropriate layer, preserve diagnostic information, perform required cleanup, and propagate failures that cannot be safely handled.

---

## Q2. Why should `try` blocks be narrow?

To make exception boundaries precise and prevent unrelated operations from being incorrectly classified as the same failure.

---

## Q3. When should an exception be re-raised?

When the current layer cannot safely recover but needs to record or process information before passing the failure upward.

---

## Q4. When should an exception be converted into a custom exception?

When the application needs a meaningful domain-specific failure category.

---

## Q5. When should `finally` be used?

For cleanup or finalization that should occur regardless of normal success or handled failure paths.

---

## Q6. When should `else` be used?

For logic that should execute only when the `try` block succeeds.

---

## Q7. Why is broad exception handling dangerous?

It can hide programming errors, destroy failure classification, and allow the application to continue in an invalid state.

---

# 46. Storage Engineering Interview Questions

## Q8. A storage test times out. Should the framework immediately mark the drive failed?

Not necessarily.

The timeout should first be classified.

The framework may need to:

```text
Record timeout
    ↓
Collect diagnostics
    ↓
Determine retry policy
    ↓
Retry if appropriate
    ↓
Fail if retry policy is exhausted
```

---

## Q9. A device path is invalid. Should the framework retry?

Normally, retrying the exact same invalid configuration is not useful.

The framework should report the configuration/validation failure.

---

## Q10. Why should a storage test cleanup happen even after failure?

Because failed tests can leave behind:

```text
Processes
Locks
Temporary files
Device state
Monitoring resources
```

which can contaminate subsequent tests.

---

# 47. Knowledge-Gap Checklist

Before moving to advanced exception topics:

```text
[ ] Specific exception handling
[ ] Multiple exceptions
[ ] Exception tuples
[ ] Exception ordering
[ ] `else`
[ ] `finally`
[ ] `raise`
[ ] Bare `raise`
[ ] Re-raising
[ ] Exception chaining
[ ] Custom exceptions
[ ] Exception hierarchy
[ ] Validation
[ ] Retry strategy
[ ] Cleanup
[ ] Resource management
[ ] Narrow try blocks
[ ] Failure classification
[ ] Exception propagation
[ ] Storage automation patterns
```

---

# 48. Final Mental Model

The complete engineering model is:

```text
                  OPERATION
                      |
                      ↓
                 TRY / EXECUTE
                      |
             ┌────────┴────────┐
             |                 |
          SUCCESS            FAILURE
             |                 |
             ↓                 ↓
           ELSE             EXCEPT
             |                 |
             |          classify failure
             |                 |
             |          ┌──────┴──────┐
             |          |             |
             |       Recover        Cannot recover
             |          |             |
             |        Handle         raise
             |          |             |
             └──────────┴─────────────┘
                        |
                        ↓
                     FINALLY
                        |
                        ↓
                Cleanup / Diagnostics
                        |
                        ↓
                  Continue / Return
                  / Propagate
```

---

# 49. Final Engineering Rule

Do not think of exception handling as:

```text
try
except
print(error)
```

Think of it as:

```text
Detect
  ↓
Classify
  ↓
Decide
  ↓
Recover OR Propagate
  ↓
Preserve Evidence
  ↓
Cleanup
  ↓
Report
```

That is the exception-handling mindset required for reliable automation.

# END

````


