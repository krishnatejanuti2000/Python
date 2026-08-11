# 14 — Exception Handling Quick Revision

## Purpose

This document is the quick-revision reference for the complete
Python Exception Handling module.

Use this document for:

- Daily revision
- Before coding practice
- Before interviews
- Storage automation revision
- Troubleshooting revision
- Quick syntax lookup

This is a revision document, not a replacement for the detailed
Module-8 documents.

---

# 1. Exception Handling

Exception handling allows a program to detect and handle runtime
failures in a controlled way.

Basic structure:

```python
try:
    risky_operation()

except SomeException:
    handle_failure()
````

Complete structure:

```python
try:
    risky_operation()

except SomeException:
    handle_failure()

else:
    success_path()

finally:
    cleanup()
```

---

# 2. `try`

Put code that may raise an exception inside `try`.

```python
try:
    value = int(user_input)
```

Do not put unnecessarily large amounts of code inside one `try`.

Prefer:

```python
try:
    value = int(user_input)

except ValueError:
    print("Invalid input")

process(value)
```

instead of:

```python
try:
    value = int(user_input)
    process(value)
    generate_report()
    cleanup()
```

A narrow `try` block makes failures easier to identify.

---

# 3. `except`

`except` handles a matching exception.

```python
try:
    value = int("abc")

except ValueError:
    print("Invalid integer")
```

---

# 4. Multiple `except` Blocks

```python
try:
    operation()

except ValueError:
    print("Invalid value")

except TypeError:
    print("Invalid type")

except ZeroDivisionError:
    print("Division by zero")
```

Use specific exceptions.

---

# 5. Exception Handler Ordering

Specific exceptions should come before broader exceptions.

Correct:

```python
try:
    operation()

except FileNotFoundError:
    print("File missing")

except OSError:
    print("OS error")
```

Because:

```text
FileNotFoundError
       ↓
     OSError
```

Incorrect:

```python
try:
    operation()

except OSError:
    print("OS error")

except FileNotFoundError:
    print("File missing")
```

The broader handler would catch the subclass first.

---

# 6. `else`

`else` executes only when the `try` block completes successfully.

```python
try:
    value = int("100")

except ValueError:
    print("Invalid")

else:
    print("Conversion successful")
```

Flow:

```text
try
 |
 +-- exception --> except
 |
 +-- success ----> else
```

---

# 7. `finally`

`finally` is used for code that must be attempted regardless of
whether the operation succeeds or fails.

```python
try:
    run_test()

finally:
    cleanup()
```

Typical use:

```text
Resource cleanup
Test cleanup
State restoration
Closing resources
```

---

# 8. Complete Control Flow

```python
try:
    operation()

except ExceptionType:
    handle_failure()

else:
    handle_success()

finally:
    cleanup()
```

Conceptually:

```text
             TRY
              |
       ┌──────┴──────┐
       |             |
    Failure        Success
       |             |
    EXCEPT          ELSE
       |             |
       └──────┬──────┘
              |
           FINALLY
```

---

# 9. `raise`

Use `raise` to explicitly generate an exception.

```python
if capacity <= 0:
    raise ValueError(
        "Capacity must be greater than zero"
    )
```

`raise` changes normal control flow.

---

# 10. `raise` vs `return`

`return`:

```python
return False
```

means:

```text
Normal function result
```

`raise`:

```python
raise ValueError("Invalid value")
```

means:

```text
Exceptional condition
```

---

# 11. Re-Raising

Inside an `except` block:

```python
except StorageTestError:
    logging.exception("Test failed")
    raise
```

A bare:

```python
raise
```

re-raises the currently handled exception.

---

# 12. Why Re-Raise?

Use re-raise when the current layer:

```text
Needs to log
Needs to add context
Needs to collect diagnostics
```

but:

```text
Does not own the final recovery decision
```

Example:

```text
Failure
  ↓
Current layer logs
  ↓
Current layer collects diagnostics
  ↓
raise
  ↓
Higher layer decides
```

---

# 13. Built-in Exceptions

Common exceptions:

| Exception           | Typical Meaning             |
| ------------------- | --------------------------- |
| `ValueError`        | Invalid value               |
| `TypeError`         | Invalid type                |
| `ZeroDivisionError` | Division by zero            |
| `FileNotFoundError` | File does not exist         |
| `PermissionError`   | Permission problem          |
| `KeyError`          | Missing dictionary key      |
| `IndexError`        | Invalid sequence index      |
| `OSError`           | OS/resource-related failure |
| `TimeoutError`      | Operation timed out         |
| `NameError`         | Name not defined            |

Choose the exception according to meaning.

---

# 14. `ValueError` vs `TypeError`

Use `TypeError` when the type is inappropriate.

```python
if not isinstance(capacity, int):
    raise TypeError(
        "Capacity must be an integer"
    )
```

Use `ValueError` when the type is correct but the value is invalid.

```python
if capacity <= 0:
    raise ValueError(
        "Capacity must be greater than zero"
    )
```

Mental model:

```text
Wrong type
   ↓
TypeError

Correct type + invalid value
   ↓
ValueError
```

---

# 15. Custom Exceptions

Create a custom exception by inheriting from `Exception`.

```python
class StorageError(Exception):
    pass
```

Example:

```python
raise StorageError(
    "Storage operation failed"
)
```

---

# 16. Storage Exception Hierarchy

A practical example:

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

# 17. Why Custom Exceptions?

They provide domain-specific meaning.

Instead of:

```python
raise Exception("Timeout")
```

use:

```python
raise StorageTimeoutError(
    "READ operation timed out"
)
```

Now the framework can specifically identify:

```text
Storage timeout
```

and apply an appropriate policy.

---

# 18. Exception Chaining

Use:

```python
raise NewException(...) from exc
```

Example:

```python
try:
    execute_io()

except TimeoutError as exc:

    raise StorageTimeoutError(
        "Storage operation timed out"
    ) from exc
```

Relationship:

```text
TimeoutError
     ↓
Original cause
     ↓
StorageTimeoutError
```

The higher-level exception provides domain context while the
original cause remains available.

---

# 19. Why Exception Chaining Matters

Without proper chaining:

```text
Low-level failure
      ↓
New exception
      ↓
Original cause may be obscured
```

With chaining:

```text
Low-level failure
      ↓
Original cause preserved
      ↓
Domain-specific exception
      ↓
Higher-level handling
```

This is especially useful during troubleshooting.

---

# 20. Broad Exception Handling

Avoid unnecessarily broad handlers.

Bad:

```python
try:
    run_test()

except Exception:
    retry()
```

Why?

Because this can catch:

```text
Validation problems
Programming bugs
Unexpected failures
Configuration errors
Storage failures
```

and treat all of them as retryable.

---

# 21. Bare `except`

Avoid:

```python
try:
    operation()

except:
    pass
```

Problems:

```text
Very broad
Hides failures
Poor diagnostics
Can hide programming problems
Can produce incorrect test results
```

---

# 22. Never Silently Swallow Important Exceptions

Bad:

```python
try:
    run_test()

except Exception:
    pass
```

Possible consequence:

```text
Test fails
   ↓
Exception swallowed
   ↓
Framework continues
   ↓
Incorrect result
```

In test automation this can produce a false PASS.

---

# 23. Logging

Use logging for automation.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
```

Example:

```python
logging.info(
    "TEST_START device=%s",
    device
)
```

---

# 24. `logging.exception()`

Inside an exception handler:

```python
try:
    run_test()

except StorageTestError:
    logging.exception(
        "Storage test failed"
    )
```

This records the exception and traceback.

---

# 25. Useful Storage Log Context

A useful storage failure record may contain:

```text
Timestamp
Severity
Device
Operation
Test phase
Exception type
Error message
Retry count
Relevant configuration
Diagnostic information
```

Example:

```text
2026-08-11 09:10:04
[ERROR]
device=/dev/sda
operation=READ
error=READ ERROR
sector=182736
retry=1
```

---

# 26. Retry

Not every exception should be retried.

Example:

```text
DeviceValidationError
    ↓
Normally no retry

StorageTimeoutError
    ↓
Potentially retryable

LogParsingError
    ↓
Investigate

Programming error
    ↓
Do not blindly retry
```

The actual policy depends on the test.

---

# 27. Bounded Retry

Bad:

```python
while True:

    try:
        run_test()

    except StorageTimeoutError:
        retry()
```

This can continue forever.

Better:

```python
max_retries = 3

for attempt in range(max_retries):

    try:
        run_test()
        break

    except StorageTimeoutError:
        logging.exception(
            "Timeout on attempt %d",
            attempt + 1
        )
```

---

# 28. Retry Does Not Mean Ignore

Incorrect:

```text
TIMEOUT
   ↓
RETRY
   ↓
Forget previous failure
```

Correct:

```text
TIMEOUT
   ↓
Log
   ↓
Collect evidence
   ↓
Retry
   ↓
Record result
```

Every attempt is useful diagnostic information.

---

# 29. Retry Example

```python
max_retries = 3

for attempt in range(1, max_retries + 1):

    try:

        run_test(device)

        print("PASS")
        break

    except StorageTimeoutError:

        logging.exception(
            "Timeout device=%s attempt=%d",
            device,
            attempt
        )

        collect_diagnostics(device)

else:

    print("FAIL")
```

The `else` executes when the loop finishes without `break`.

---

# 30. Cleanup

Use `finally` when cleanup is required.

```python
try:
    run_test(device)

finally:
    cleanup(device)
```

Typical cleanup:

```text
Stop process
Release resources
Restore state
Remove temporary state
Close resources
```

---

# 31. Context Managers

For resources such as files, prefer:

```python
with open("storage.log", "r") as file:
    data = file.read()
```

The context manager handles resource cleanup automatically.

---

# 32. Conditional Cleanup

Sometimes cleanup should occur only after a resource/test was successfully started.

```python
test_started = False

try:

    start_test(device)
    test_started = True

    execute_test(device)

finally:

    if test_started:
        cleanup(device)
```

---

# 33. Storage Validation

Validate before execution.

```python
def validate_device(device):

    if not isinstance(device, str):
        raise DeviceValidationError(
            "Device must be a string"
        )

    if not device.startswith("/dev/"):
        raise DeviceValidationError(
            f"Invalid device: {device}"
        )
```

Important:

```text
Valid path format
      ≠
Healthy physical device
```

---

# 34. Storage Test Execution

A low-level operation may produce:

```text
TimeoutError
OSError
PermissionError
FileNotFoundError
```

The storage execution layer can translate them into meaningful
domain exceptions where appropriate.

Example:

```python
try:
    perform_io(device)

except TimeoutError as exc:

    raise StorageTimeoutError(
        f"READ timeout on {device}"
    ) from exc
```

---

# 35. Storage Timeout

A timeout means:

```text
Operation exceeded configured timeout
```

It does NOT automatically mean:

```text
Drive is defective
```

Possible causes include:

```text
Device state
Transport
Controller
I/O queue
System load
Configuration
Firmware
Hardware
```

Investigate before assigning root cause.

---

# 36. Device Not Found

Example:

```text
/dev/sda does not exist
```

Possible causes:

```text
Incorrect path
Device not enumerated
Device disconnected
Environment issue
Configuration issue
```

Do not automatically classify this as a hardware failure.

---

# 37. Permission Failure

Example:

```text
PermissionError
```

Possible cause:

```text
Insufficient privileges
```

Usually investigate/fix the execution environment rather than
blindly retrying the same operation.

---

# 38. Log Parsing Failure

Example:

```python
try:
    result = parse_log(log)

except ValueError as exc:

    raise LogParsingError(
        "Unable to parse storage log"
    ) from exc
```

Important distinction:

```text
Storage test execution
        ↓
may have succeeded

Result parsing
        ↓
failed
```

A parser failure does not automatically mean the storage device failed.

---

# 39. Test Failure vs Framework Failure

Storage test failure:

```text
READ ERROR
WRITE ERROR
TIMEOUT
```

Framework failure:

```text
Parser IndexError
Unexpected NameError
Automation logic bug
```

These must not automatically be reported as the same failure.

---

# 40. Failure Classification

A conceptual mapping:

| Failure                 | Typical Action              |
| ----------------------- | --------------------------- |
| Configuration error     | Stop / fix configuration    |
| Device validation error | Stop / investigate          |
| Timeout                 | Diagnose / possibly retry   |
| Transient test error    | Diagnose / possibly retry   |
| Persistent test error   | FAIL                        |
| Log parsing error       | Investigate processing      |
| Unexpected exception    | Log + propagate/investigate |

---

# 41. Diagnostics

After an important storage failure, collect relevant evidence.

Depending on the environment:

```text
Test logs
Device state
System/kernel logs
Transport state
Controller information
I/O state
Error counters
Device health information
Command output
Retry history
Configuration
```

---

# 42. Diagnostics Before Cleanup

Preferred flow:

```text
Failure
   ↓
Collect diagnostics
   ↓
Cleanup
   ↓
Report
```

Why?

Cleanup can alter the state required for troubleshooting.

---

# 43. Root Cause Analysis

Do not confuse:

```text
Exception
```

with:

```text
Root Cause
```

Example:

```text
Observed:
READ timeout

Possible causes:
Transport
Controller
System load
Queue congestion
Configuration
Device
```

RCA flow:

```text
Exception
   ↓
Evidence
   ↓
Correlation
   ↓
Hypothesis
   ↓
Verification
   ↓
Root Cause
```

---

# 44. Symptom vs Root Cause

Example:

```text
Symptom:
StorageTimeoutError

Possible root cause:
Transport problem
```

Another:

```text
Symptom:
READ ERROR

Possible root cause:
Media problem
```

The root cause must be established using evidence.

---

# 45. Failure Ownership

Ask:

```text
Who owns the failure?
```

Possible areas:

```text
Configuration
Automation framework
Operating system
Transport
Controller
Device
Test environment
```

Exception type alone may not determine ownership.

---

# 46. Storage Automation Complete Flow

```text
TEST REQUEST
     |
     ↓
LOAD CONFIG
     |
     ↓
VALIDATE
     |
     ↓
EXECUTE
     |
     ↓
FAILURE?
   /     \
 No       Yes
 |         |
PASS    CLASSIFY
           |
      ┌────┼────┐
      |    |    |
 Validation Timeout Other
      |    |    |
     STOP RETRY  ERROR
           |
       Diagnostics
           |
        Retry
           |
      Limit reached?
        /       \
      No         Yes
      |           |
    Retry        FAIL
        \         /
         \       /
          REPORT
             |
             ↓
          CLEANUP
             |
             ↓
          FINAL RESULT
             |
             ↓
             RCA
```

---

# 47. Common Anti-Patterns

## Anti-Pattern 1

```python
except:
    pass
```

Problem:

```text
Failure hidden
```

---

## Anti-Pattern 2

```python
except Exception:
    retry()
```

Problem:

```text
Every failure treated as retryable
```

---

## Anti-Pattern 3

```python
while True:
    retry()
```

Problem:

```text
Potential infinite retry
```

---

## Anti-Pattern 4

```python
except Exception:
    print("Failed")
```

Problem:

```text
No structured logging
No traceback
Insufficient diagnostics
```

---

## Anti-Pattern 5

```python
try:
    everything()
```

Problem:

```text
Large exception boundary
Unknown failure location
```

---

# 48. Good Exception Handling Pattern

```text
Specific exception
        ↓
Meaningful handler
        ↓
Useful logging
        ↓
Diagnostics
        ↓
Recovery / Retry if appropriate
        ↓
Re-raise if necessary
        ↓
Cleanup
        ↓
Explicit result
```

---

# 49. Quick Comparison

| Bad Practice               | Better Practice                       |
| -------------------------- | ------------------------------------- |
| Bare `except`              | Specific exception                    |
| `pass`                     | Handle/log/propagate                  |
| Infinite retry             | Bounded retry                         |
| `print()` only             | Structured logging                    |
| Huge `try`                 | Narrow `try`                          |
| Lose original cause        | Exception chaining                    |
| Retry everything           | Retry only appropriate failures       |
| Ignore cleanup             | Guaranteed cleanup                    |
| "Drive failed" immediately | Investigate evidence                  |
| Hide framework bugs        | Distinguish framework/device failures |

---

# 50. Interview Quick Answers

## Why use custom exceptions?

To represent domain-specific failures.

---

## Why use `finally`?

To perform required cleanup.

---

## Why use `raise`?

To explicitly signal or propagate an exceptional condition.

---

## Why use `raise ... from exc`?

To preserve the original cause while adding higher-level context.

---

## Why avoid broad exception handling?

It can hide unexpected failures and misclassify them.

---

## Why bound retries?

To prevent infinite retry loops.

---

## Does timeout mean hardware failure?

No.

It is an observed condition requiring investigation.

---

## Why collect diagnostics?

To preserve evidence required for troubleshooting and RCA.

---

## Why distinguish parser failures from device failures?

Because the test may have succeeded while result processing failed.

---

# 51. Rapid Revision — Syntax

## Basic

```python
try:
    operation()

except ValueError:
    handle()
```

## Multiple Exceptions

```python
try:
    operation()

except ValueError:
    handle_value()

except TypeError:
    handle_type()
```

## Else

```python
try:
    operation()

except ExceptionType:
    handle()

else:
    success()
```

## Finally

```python
try:
    operation()

finally:
    cleanup()
```

## Raise

```python
raise ValueError("Invalid value")
```

## Re-raise

```python
except SomeError:
    raise
```

## Chaining

```python
except SomeError as exc:
    raise NewError("Higher-level failure") from exc
```

## Custom Exception

```python
class StorageError(Exception):
    pass
```

---

# 52. Exception Handling Decision Tree

```text
Did an exception occur?
        |
       No
        |
       PASS
        |
       Yes
        |
        ↓
Can this layer handle it?
      /       \
    Yes        No
     |          |
   Handle     Propagate
     |
     ↓
Is it retryable?
   /       \
 Yes        No
  |          |
Retry       FAIL
  |
Limit reached?
 /          \
No           Yes
 |            |
Retry        FAIL
       \      /
        \    /
        REPORT
           |
        CLEANUP
           |
           RCA
```

---

# 53. Storage Engineering Golden Rules

```text
1. Validate before execution.
2. Catch specific exceptions.
3. Keep try blocks narrow.
4. Do not swallow failures.
5. Preserve original causes.
6. Retry only appropriate failures.
7. Always bound retries.
8. Log device and operation context.
9. Collect diagnostics.
10. Perform required cleanup.
11. Distinguish framework failures from device failures.
12. Do not confuse symptoms with root causes.
13. Preserve the complete failure timeline.
14. Produce an explicit final test result.
```

---

# 54. Final Mental Model

Remember:

```text
          FAILURE
             |
             ↓
          DETECT
             |
             ↓
         CLASSIFY
             |
             ↓
           LOG
             |
             ↓
      COLLECT EVIDENCE
             |
             ↓
        DECIDE ACTION
             |
       ┌─────┼─────┐
       |     |     |
     HANDLE RETRY FAIL
             |
             ↓
          CLEANUP
             |
             ↓
          REPORT
             |
             ↓
       ROOT CAUSE
```

---

# 55. Final Rule

Exception handling is not simply:

```python
try:
    ...
except:
    ...
```

Professional exception handling means:

```text
Detect
 ↓
Classify
 ↓
Preserve evidence
 ↓
Handle what you can
 ↓
Retry only when justified
 ↓
Propagate what you cannot handle
 ↓
Cleanup
 ↓
Report accurately
 ↓
Investigate root cause
```

For Storage Test Automation:

```text
Exception
    ↓
Reliable classification
    ↓
Reliable recovery/reporting
    ↓
Accurate test result
    ↓
Root Cause Analysis
```

# END

