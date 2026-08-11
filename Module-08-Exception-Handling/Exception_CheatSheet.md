# 15 — Exception Handling Cheat Sheet

## 1. Basic Syntax

### try / except

```python
try:
    risky_operation()

except ValueError:
    handle_error()
````

---

### Multiple Exceptions

```python
try:
    operation()

except ValueError:
    handle_value_error()

except TypeError:
    handle_type_error()

except ZeroDivisionError:
    handle_zero_division()
```

**Rule:**

```text
Specific exception
        ↓
More general exception
```

---

# 2. try / except / else / finally

```python
try:
    operation()

except SomeError:
    handle_error()

else:
    success()

finally:
    cleanup()
```

### Execution

```text
TRY
 |
 +-- exception --> EXCEPT --> FINALLY
 |
 +-- success ----> ELSE ----> FINALLY
```

### Remember

```text
try     → risky code
except  → failure handling
else    → success path
finally → cleanup
```

---

# 3. `raise`

Explicitly generate an exception:

```python
raise ValueError("Invalid value")
```

Example:

```python
if capacity <= 0:
    raise ValueError(
        "Capacity must be greater than zero"
    )
```

---

# 4. `raise` vs `return`

```python
return False
```

means:

```text
Normal result
```

while:

```python
raise ValueError("Invalid input")
```

means:

```text
Exceptional condition
```

---

# 5. Re-Raise

Inside an `except` block:

```python
except StorageTestError:
    logging.exception("Test failed")
    raise
```

Bare:

```python
raise
```

means:

```text
Re-raise current exception
```

---

# 6. Built-in Exceptions

| Exception           | Meaning                     |
| ------------------- | --------------------------- |
| `ValueError`        | Correct type, invalid value |
| `TypeError`         | Wrong/inappropriate type    |
| `ZeroDivisionError` | Division by zero            |
| `FileNotFoundError` | File does not exist         |
| `PermissionError`   | Permission problem          |
| `KeyError`          | Missing dictionary key      |
| `IndexError`        | Invalid sequence index      |
| `OSError`           | OS/resource failure         |
| `TimeoutError`      | Operation timed out         |
| `NameError`         | Name is not defined         |

---

# 7. ValueError vs TypeError

### TypeError

Wrong type:

```python
if not isinstance(capacity, int):
    raise TypeError(
        "Capacity must be an integer"
    )
```

### ValueError

Correct type but invalid value:

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

# 8. Custom Exceptions

Basic:

```python
class StorageError(Exception):
    pass
```

Raise:

```python
raise StorageError(
    "Storage operation failed"
)
```

---

# 9. Storage Exception Hierarchy

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

# 10. Why Custom Exceptions?

Use them when a failure needs domain-specific meaning.

Instead of:

```python
raise Exception("Timeout")
```

prefer:

```python
raise StorageTimeoutError(
    "READ operation timed out"
)
```

---

# 11. Exception Chaining

Syntax:

```python
try:
    operation()

except SomeError as exc:
    raise NewError(
        "Higher-level failure"
    ) from exc
```

Example:

```python
try:
    perform_io(device)

except TimeoutError as exc:
    raise StorageTimeoutError(
        f"READ timeout on {device}"
    ) from exc
```

Flow:

```text
TimeoutError
     ↓
Original cause
     ↓
StorageTimeoutError
```

---

# 12. Why Use `from exc`?

It preserves the original cause while adding higher-level context.

```text
Low-level exception
        +
Domain-specific context
        ↓
Better troubleshooting
```

---

# 13. Specific Exception Handling

Prefer:

```python
try:
    value = int(user_input)

except ValueError:
    print("Invalid integer")
```

Avoid unnecessarily broad handling:

```python
try:
    value = int(user_input)

except Exception:
    print("Something went wrong")
```

---

# 14. Avoid Bare `except`

Avoid:

```python
try:
    operation()

except:
    pass
```

Problems:

```text
Failure hidden
No diagnostics
Poor debugging
Possible false result
```

---

# 15. Avoid Swallowing Exceptions

Bad:

```python
try:
    run_test()

except Exception:
    pass
```

Better:

```python
try:
    run_test()

except StorageTestError:
    logging.exception(
        "Storage test failed"
    )
    raise
```

---

# 16. Narrow `try` Blocks

Prefer:

```python
try:
    value = int(user_input)

except ValueError:
    handle_error()

process(value)
```

Avoid:

```python
try:
    value = int(user_input)
    process(value)
    generate_report()
    cleanup()

except Exception:
    handle_error()
```

Small `try` blocks make the failure location clearer.

---

# 17. Logging

Basic configuration:

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

# 18. Logging Levels

Common levels:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Typical storage usage:

```text
INFO
→ Test started

WARNING
→ Retry / transient condition

ERROR
→ Test failure

CRITICAL
→ Severe application/system condition
```

---

# 19. `logging.exception()`

Use inside `except`:

```python
try:
    run_test(device)

except StorageTestError:
    logging.exception(
        "Storage test failed: device=%s",
        device
    )
```

Provides:

```text
Log message
+
Exception
+
Traceback
```

---

# 20. Storage Failure Log Context

Useful fields:

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

# 21. Retry

Not every exception is retryable.

Typical approach:

```text
DeviceValidationError
    ↓
Normally NO retry

StorageTimeoutError
    ↓
Potentially retry

StorageTestError
    ↓
Depends on specific failure

LogParsingError
    ↓
Investigate

Programming error
    ↓
Do not blindly retry
```

---

# 22. Bounded Retry

Avoid:

```python
while True:
    try:
        run_test()

    except StorageTimeoutError:
        retry()
```

Prefer:

```python
max_retries = 3

for attempt in range(1, max_retries + 1):

    try:
        run_test()
        break

    except StorageTimeoutError:
        logging.exception(
            "Timeout attempt=%d",
            attempt
        )
```

---

# 23. Retry With Diagnostics

```python
for attempt in range(1, max_retries + 1):

    try:
        run_test(device)
        break

    except StorageTimeoutError:

        logging.exception(
            "Timeout device=%s attempt=%d",
            device,
            attempt
        )

        collect_diagnostics(device)
```

---

# 24. Retry Does Not Mean Ignore

Wrong:

```text
TIMEOUT
   ↓
RETRY
   ↓
Forget failure
```

Correct:

```text
TIMEOUT
   ↓
LOG
   ↓
DIAGNOSTICS
   ↓
RETRY
   ↓
RECORD RESULT
```

---

# 25. `for ... else` Retry Pattern

```python
for attempt in range(3):

    try:
        run_test()
        break

    except StorageTimeoutError:
        logging.warning(
            "Timeout attempt=%d",
            attempt + 1
        )

else:
    print("All retries failed")
```

The `else` executes only if the loop finishes without `break`.

---

# 26. Cleanup

Use `finally`:

```python
try:
    run_test(device)

finally:
    cleanup(device)
```

Mental model:

```text
Success ──┐
          ↓
       FINALLY
          ↑
Failure ──┘
```

---

# 27. Context Manager

For files:

```python
with open("storage.log", "r") as file:
    data = file.read()
```

Prefer context managers when the resource supports them.

---

# 28. Conditional Cleanup

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

# 29. Configuration Validation

```python
def validate_config(config):

    if "device" not in config:
        raise StorageConfigurationError(
            "Device missing from configuration"
        )
```

Validate before execution.

---

# 30. Device Validation

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

Remember:

```text
Valid path
   ≠
Healthy device
```

---

# 31. Device Not Found

Possible causes:

```text
Incorrect path
Device not enumerated
Device disconnected
Configuration issue
Environment issue
```

Do not immediately conclude:

```text
Hardware failure
```

---

# 32. Permission Failure

Possible cause:

```text
Insufficient privileges
```

Usually investigate/fix the environment instead of blindly retrying.

---

# 33. Storage Timeout

A timeout means:

```text
Operation exceeded configured timeout
```

It does NOT automatically mean:

```text
Drive is defective
```

Investigate:

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

---

# 34. Low-Level → Domain Exception

Example:

```python
try:
    perform_io(device)

except TimeoutError as exc:

    raise StorageTimeoutError(
        f"READ timeout on {device}"
    ) from exc
```

Flow:

```text
TimeoutError
      ↓
StorageTimeoutError
      ↓
Retry policy
```

---

# 35. I/O Error Translation

```python
try:
    perform_io(device)

except OSError as exc:

    raise StorageTestError(
        f"I/O failure on {device}"
    ) from exc
```

---

# 36. Log Parsing Error

```python
try:
    result = parse_log(log)

except ValueError as exc:

    raise LogParsingError(
        "Unable to parse storage log"
    ) from exc
```

Important:

```text
Test execution may have succeeded
        ↓
Result processing failed
```

---

# 37. Test Failure vs Framework Failure

### Storage failure

```text
READ ERROR
WRITE ERROR
TIMEOUT
```

### Framework failure

```text
IndexError
NameError
Parser bug
Automation logic bug
```

Do not automatically classify both as device failures.

---

# 38. Result Classification

Typical conceptual results:

```text
PASS
FAIL
INVALID
ERROR
RETRY
BLOCKED
```

Example:

```text
DeviceValidationError
    ↓
INVALID

StorageTimeoutError
    ↓
RETRY → FAIL

Persistent StorageTestError
    ↓
FAIL

Parser crash
    ↓
ERROR

Successful test
    ↓
PASS
```

Exact categories depend on framework design.

---

# 39. Diagnostics

Collect relevant evidence after important failures.

Possible evidence:

```text
Test logs
Device state
Kernel/system logs
Transport state
Controller information
I/O state
Error counters
Device health
Command output
Retry history
Configuration
```

---

# 40. Diagnostic Timing

Preferred:

```text
FAILURE
   ↓
DIAGNOSTICS
   ↓
CLEANUP
   ↓
REPORT
```

Why?

Cleanup may change the state needed for RCA.

---

# 41. Root Cause Analysis

Do not assume:

```text
Exception = Root Cause
```

Instead:

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

# 42. Symptom vs Root Cause

Example:

```text
Symptom:
READ timeout

Possible causes:
Transport
Controller
System load
Queue congestion
Configuration
Device
```

The timeout alone is not sufficient to determine root cause.

---

# 43. Failure Ownership

Possible owners:

```text
Configuration
Automation framework
Operating system
Transport
Controller
Device
Test environment
```

Ask:

```text
Who owns this failure?
```

before assigning root cause.

---

# 44. Storage Automation Flow

```text
TEST REQUEST
     ↓
CONFIGURATION
     ↓
VALIDATION
     ↓
EXECUTION
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
     STOP RETRY ERROR
           |
       DIAGNOSTICS
           |
         RETRY
           |
       LIMIT?
       /    \
     No      Yes
     |        |
   RETRY     FAIL
       \     /
        \   /
        REPORT
           |
        CLEANUP
           |
      FINAL RESULT
           |
           ↓
           RCA
```

---

# 45. Complete Pattern

```python
import logging


class StorageError(Exception):
    pass


class DeviceValidationError(StorageError):
    pass


class StorageTestError(StorageError):
    pass


class StorageTimeoutError(StorageTestError):
    pass


def run_storage_test(device):

    try:

        validate_device(device)
        execute_test(device)

    except StorageTimeoutError:

        logging.exception(
            "Storage timeout: device=%s",
            device
        )

        collect_diagnostics(device)

        raise

    except StorageTestError:

        logging.exception(
            "Storage test failed: device=%s",
            device
        )

        collect_diagnostics(device)

        raise

    finally:

        cleanup(device)
```

---

# 46. Common Anti-Patterns

## Don't

```python
except:
    pass
```

## Don't

```python
except Exception:
    retry()
```

## Don't

```python
while True:
    retry()
```

## Don't

```python
try:
    everything()
```

## Don't

```python
logging.error("Failed")
```

when useful context is available.

## Don't

```python
raise NewError(str(exc))
```

when the original cause should be preserved.

Prefer:

```python
raise NewError(
    "Higher-level failure"
) from exc
```

---

# 47. Good Pattern

```text
Specific Exception
        ↓
Meaningful Handling
        ↓
Logging
        ↓
Diagnostics
        ↓
Recovery / Retry
        ↓
Propagation if necessary
        ↓
Cleanup
        ↓
Explicit Result
        ↓
RCA
```

---

# 48. Quick Interview Rules

```text
Specific exceptions → better handling

Narrow try → easier debugging

finally → cleanup

raise → explicit failure

raise ... from exc → preserve cause

Custom exception → domain meaning

logging.exception() → traceback

Bounded retry → prevents infinite loops

Diagnostics → preserve evidence

Exception ≠ root cause

Parser failure ≠ automatically device failure

Never silently swallow important failures

Unexpected framework failure ≠ device failure
```

---

# 49. One-Page Mental Model

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
               DECIDE
             /     |      \
         HANDLE   RETRY   FAIL
                    |
                LIMIT?
               /      \
             NO        YES
             |          |
           RETRY       FAIL
                \      /
                 \    /
                  ↓  ↓
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

# 50. Golden Rules

```text
1. Catch specific exceptions.
2. Keep try blocks small.
3. Use else for the success path.
4. Use finally for required cleanup.
5. Use raise for explicit validation/failure.
6. Use custom exceptions for domain-specific failures.
7. Preserve causes with exception chaining.
8. Never silently swallow important failures.
9. Retry only appropriate failures.
10. Always bound retries.
11. Log useful context.
12. Preserve traceback information.
13. Collect diagnostics.
14. Distinguish framework and device failures.
15. Do not confuse symptoms with root causes.
16. Produce explicit final test results.
17. Preserve the complete failure timeline.
```

---

# 51. Final Storage Engineering Rule

Remember:

```text
Exception
    ↓
Classification
    ↓
Evidence
    ↓
Decision
    ↓
Recovery / Retry / Fail
    ↓
Cleanup
    ↓
Report
    ↓
Root Cause Analysis
```

The exception tells you:

```text
WHAT happened
```

The evidence helps determine:

```text
WHY it happened
```

The automation framework must determine:

```text
WHAT TO DO NEXT
```

# END
