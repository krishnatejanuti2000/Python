# 13 — Exception Handling Interview Questions

## Objective

This document contains interview-oriented questions for Python Exception Handling.

The questions progress from:

1. Basic concepts
2. Code understanding
3. Exception behavior
4. Custom exceptions
5. Exception propagation
6. Exception chaining
7. Logging
8. Retry handling
9. Cleanup
10. Storage Test Automation
11. Troubleshooting
12. Senior-level design

Every question includes a reference answer.

---

# SECTION 1 — BASIC QUESTIONS

## Q1. What is exception handling in Python?

### Answer

Exception handling is the mechanism used to detect and handle runtime errors without allowing the program to terminate unexpectedly.

Python provides:

```python
try
except
else
finally
````

and:

```python
raise
```

for explicit exception generation.

---

## Q2. What is the difference between an error and an exception?

### Answer

An error is a general condition indicating that something went wrong.

An exception is an object representing an exceptional condition that Python can raise and handle.

Example:

```python
10 / 0
```

produces:

```text
ZeroDivisionError
```

---

## Q3. Why is exception handling important in test automation?

### Answer

Test automation interacts with external systems and resources.

Examples:

```text
Devices
Files
Processes
Operating system
Storage controllers
I/O operations
Network resources
Test tools
```

These operations can fail.

Proper exception handling allows the framework to:

```text
Detect failure
 ↓
Classify failure
 ↓
Collect evidence
 ↓
Recover when possible
 ↓
Report accurate result
```

---

# SECTION 2 — TRY / EXCEPT

## Q4. What is the purpose of `try`?

### Answer

`try` contains code that may raise an exception.

Example:

```python
try:
    value = int("abc")
```

---

## Q5. What is the purpose of `except`?

### Answer

`except` defines how a particular exception should be handled.

Example:

```python
try:
    value = int("abc")

except ValueError:
    print("Invalid integer")
```

---

## Q6. Can we have multiple `except` blocks?

### Answer

Yes.

Example:

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

Only the matching handler is executed.

---

## Q7. In what order should multiple exception handlers be written?

### Answer

Specific exceptions should normally appear before broader exceptions.

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

---

## Q8. What is wrong with this?

```python
try:
    operation()

except Exception:
    print("Error")

except ValueError:
    print("Invalid value")
```

### Answer

`ValueError` is a subclass of `Exception`.

Therefore the first handler catches it.

The later `ValueError` handler becomes unreachable for that case.

Specific handlers should come first.

---

# SECTION 3 — ELSE AND FINALLY

## Q9. When is `else` executed?

### Answer

The `else` block executes when the `try` block completes without raising an exception.

Example:

```python
try:
    value = int("100")

except ValueError:
    print("Invalid")

else:
    print("Conversion successful")
```

---

## Q10. When is `finally` executed?

### Answer

`finally` is intended for code that must run regardless of whether an exception occurred.

Example:

```python
try:
    run_test()

finally:
    cleanup()
```

---

## Q11. What is the difference between `else` and `finally`?

### Answer

`else`:

```text
Runs when try succeeds.
```

`finally`:

```text
Runs regardless of normal success or exception handling.
```

Example:

```python
try:
    operation()

except Exception:
    handle_error()

else:
    report_success()

finally:
    cleanup()
```

---

# SECTION 4 — RAISE

## Q12. What is `raise`?

### Answer

`raise` is used to explicitly generate an exception.

Example:

```python
if capacity <= 0:
    raise ValueError("Capacity must be positive")
```

---

## Q13. Why would you explicitly raise an exception?

### Answer

To enforce application or domain rules.

Example:

```python
def validate_device(device):

    if not device.startswith("/dev/"):
        raise ValueError(
            f"Invalid device: {device}"
        )
```

---

## Q14. What is the difference between `raise` and `return`?

### Answer

`return` provides a normal function result.

```python
return False
```

`raise` interrupts normal execution and signals an exceptional condition.

```python
raise ValueError("Invalid input")
```

---

# SECTION 5 — RERAISE

## Q15. What does a bare `raise` do inside an `except` block?

### Answer

It re-raises the currently handled exception.

Example:

```python
try:
    run_test()

except StorageTestError:
    logging.exception("Test failed")
    raise
```

The original exception continues propagating.

---

## Q16. Why would you log an exception and then re-raise it?

### Answer

Because the current layer may need to record useful context but does not own the final recovery decision.

Example:

```text
Failure
 ↓
Log context
 ↓
Preserve traceback
 ↓
Re-raise
 ↓
Higher layer decides what to do
```

---

# SECTION 6 — CUSTOM EXCEPTIONS

## Q17. Why create custom exceptions?

### Answer

Custom exceptions provide domain-specific meaning.

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

The framework can now distinguish storage timeout failures from unrelated failures.

---

## Q18. How do you create a custom exception?

### Answer

```python
class StorageError(Exception):
    pass
```

Then:

```python
raise StorageError("Storage operation failed")
```

---

## Q19. How would you design a storage exception hierarchy?

### Answer

Example:

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

# SECTION 7 — EXCEPTION CHAINING

## Q20. What is exception chaining?

### Answer

Exception chaining preserves the original exception when raising a higher-level exception.

Example:

```python
try:
    execute_io()

except TimeoutError as exc:
    raise StorageTimeoutError(
        "Storage operation timed out"
    ) from exc
```

The `TimeoutError` remains the original cause.

---

## Q21. Why is exception chaining useful in storage automation?

### Answer

It allows the framework to provide domain-specific information while preserving low-level diagnostic information.

Example:

```text
TimeoutError
     ↓
Original cause
     ↓
StorageTimeoutError
     ↓
Storage framework
```

---

## Q22. What is the difference between:

```python
raise StorageTestError("I/O failed")
```

and:

```python
raise StorageTestError("I/O failed") from exc
```

### Answer

The second version explicitly preserves `exc` as the cause of the new exception.

This is useful for troubleshooting and debugging.

---

# SECTION 8 — BROAD EXCEPTION HANDLING

## Q23. Why should `except Exception` not be used everywhere?

### Answer

Because it can hide unexpected failures and incorrectly classify unrelated exceptions as recoverable.

Bad:

```python
try:
    run_test()

except Exception:
    retry()
```

A programming bug could be retried as if it were a transient storage failure.

---

## Q24. Why should bare `except:` generally be avoided?

### Answer

A bare `except:` catches a very broad range of exceptions, including exceptions such as:

```text
KeyboardInterrupt
SystemExit
```

Normal application code should generally catch the specific exceptions it can handle.

---

## Q25. What is wrong with this code?

```python
try:
    run_test()

except Exception:
    pass
```

### Answer

The exception is silently swallowed.

Consequences:

```text
Failure disappears
 ↓
No useful diagnostic
 ↓
Framework may continue incorrectly
 ↓
Possible false result
```

---

# SECTION 9 — LOGGING

## Q26. Why use logging instead of `print()` in automation?

### Answer

Logging provides structured information such as:

```text
Timestamp
Severity
Message
Exception traceback
Configurable output
```

Example:

```python
logging.error(
    "Storage test failed: device=%s",
    device
)
```

---

## Q27. What does `logging.exception()` provide?

### Answer

When used inside an `except` block, it logs the exception and traceback.

Example:

```python
try:
    run_test()

except StorageTestError:
    logging.exception(
        "Storage test failed"
    )
```

---

## Q28. What information should a storage failure log contain?

### Answer

Where applicable:

```text
Timestamp
Severity
Device
Operation
Test phase
Exception type
Error message
Retry count
Configuration
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

# SECTION 10 — RETRY

## Q29. Should every exception be retried?

### Answer

No.

Retry should be based on the meaning of the failure.

Example:

```text
DeviceValidationError
→ normally do not retry

StorageTimeoutError
→ potentially retry

LogParsingError
→ investigate

Programming error
→ do not blindly retry
```

---

## Q30. Why should retry attempts be bounded?

### Answer

To prevent infinite loops.

Bad:

```python
while True:

    try:
        run_test()

    except StorageTimeoutError:
        retry()
```

Better:

```python
for attempt in range(3):

    try:
        run_test()
        break

    except StorageTimeoutError:
        ...
```

---

## Q31. What should happen before retrying a storage timeout?

### Answer

Depending on the framework:

```text
Log failure
 ↓
Capture relevant diagnostics
 ↓
Determine whether retry is permitted
 ↓
Reset required test state
 ↓
Retry
```

The exact actions depend on the test.

---

## Q32. Does a successful retry prove there was no problem?

### Answer

No.

A successful retry proves that the later attempt succeeded.

The original failure remains useful evidence.

Example:

```text
Attempt 1 → TIMEOUT
Attempt 2 → PASS
```

The first timeout should still be recorded and investigated when relevant.

---

# SECTION 11 — CLEANUP

## Q33. Why is `finally` important in storage automation?

### Answer

A failed test may leave:

```text
Processes
Locks
Temporary resources
Outstanding operations
Changed test state
```

`finally` can ensure required cleanup is attempted.

---

## Q34. What if cleanup itself fails?

### Answer

The framework should have an explicit cleanup-failure policy.

At minimum:

```python
try:
    cleanup()

except Exception:
    logging.exception(
        "Cleanup failed"
    )
```

The original test failure should not be accidentally hidden.

---

# SECTION 12 — STORAGE TEST AUTOMATION

## Q35. A `/dev/sda` READ operation times out. What should the framework do?

### Answer

A reasonable flow:

```text
READ timeout
     ↓
StorageTimeoutError
     ↓
Log failure
     ↓
Collect diagnostics
     ↓
Check retry policy
     ↓
Retry if allowed
     ↓
Retry limit reached?
     ↓
FAIL
     ↓
Cleanup
     ↓
Report
```

---

## Q36. Does `StorageTimeoutError` prove that the drive is defective?

### Answer

No.

It proves that the operation exceeded the configured timeout.

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

Evidence is required to determine root cause.

---

## Q37. A device path does not exist. Should the framework retry?

### Answer

Normally, not blindly.

The framework should investigate:

```text
Incorrect path
Device enumeration
Device connection
Environment
Configuration
```

Repeatedly executing the same invalid path usually does not solve the problem.

---

## Q38. A log parser raises `IndexError` after a successful storage test. Is the drive necessarily bad?

### Answer

No.

The failure may belong to the result-processing layer.

The framework should distinguish:

```text
Test execution failure
```

from:

```text
Result parsing failure
```

---

# SECTION 13 — TROUBLESHOOTING QUESTIONS

## Q39. What is the difference between an exception and root cause?

### Answer

An exception describes an observed failure condition.

Root cause explains why the failure occurred.

Example:

```text
Exception:
READ timeout

Possible root causes:
Transport issue
Controller issue
System overload
Configuration
Device problem
```

The exception is evidence, not automatically the root cause.

---

## Q40. What information would you collect after a storage failure?

### Answer

Depending on the environment:

```text
Test logs
Device state
System/kernel logs
Transport state
Controller information
I/O state
Error counters
Retry history
Test configuration
Command output
Device health information
```

---

## Q41. Why should diagnostics be collected before cleanup when appropriate?

### Answer

Cleanup may alter or remove the state required for troubleshooting.

Preferred flow:

```text
Failure
 ↓
Diagnostics
 ↓
Cleanup
 ↓
Report
```

---

# SECTION 14 — CODE ANALYSIS

## Q42. What is wrong with this code?

```python
try:
    run_test()

except Exception:
    print("Failed")

finally:
    cleanup()
```

### Answer

The main issue is the broad exception handling.

Problems:

```text
Unexpected exceptions are classified the same way
No traceback
No structured logging
No failure classification
No propagation
```

A better design depends on what the caller should do with the failure.

---

## Q43. What is wrong here?

```python
for attempt in range(3):

    try:
        run_test()
        break

    except Exception:
        continue
```

### Answer

Problems:

```text
Catches every Exception
No logging
No diagnostics
No distinction between retryable and non-retryable failures
No final failure reporting
```

---

# SECTION 15 — ADVANCED QUESTIONS

## Q44. Where should an exception be handled?

### Answer

An exception should generally be handled at the layer that has enough information and authority to make a meaningful decision.

Example:

```text
Low-level layer
    ↓
Generate technical exception

Execution layer
    ↓
Translate/classify

Test runner
    ↓
Retry/fail decision

Reporting layer
    ↓
Final result
```

---

## Q45. Should every layer log the same exception?

### Answer

Not necessarily.

Repeated logging can create duplicate and noisy logs.

A better design determines:

```text
Where detailed traceback is logged
Where context is added
Where final result is reported
```

---

## Q46. Why should exception handling be designed together with test-result handling?

### Answer

Because an exception must eventually lead to a meaningful test state.

For example:

```text
StorageTimeoutError
        ↓
Retry
        ↓
Retry exhausted
        ↓
FAIL
```

The framework must connect the technical exception to the test result.

---

# SECTION 16 — SENIOR STORAGE AUTOMATION QUESTIONS

## Q47. Design the failure flow for three consecutive READ timeouts.

### Answer

```text
Attempt 1
 ↓
READ timeout
 ↓
Log
 ↓
Diagnostics

Attempt 2
 ↓
READ timeout
 ↓
Log
 ↓
Diagnostics

Attempt 3
 ↓
READ timeout
 ↓
Log
 ↓
Diagnostics

Retry limit reached
 ↓
FINAL RESULT = FAIL
 ↓
Cleanup
 ↓
Report
 ↓
RCA
```

---

## Q48. How would you distinguish a device failure from a framework failure?

### Answer

Look at where the failure originated.

Example:

```text
Device operation
 ↓
I/O error
```

may indicate a device/transport/environment issue.

But:

```text
Log parser
 ↓
IndexError
```

may indicate a framework defect.

The classification requires evidence and correlation.

---

## Q49. How would you design an exception hierarchy for enterprise storage automation?

### Answer

Example:

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

The hierarchy should represent meaningful failure domains.

---

## Q50. How would you handle a low-level `OSError` from a storage operation?

### Answer

If the storage execution layer needs to expose a domain-specific exception:

```python
try:
    perform_io()

except OSError as exc:
    raise StorageTestError(
        f"I/O failure on {device}"
    ) from exc
```

This gives the higher layer:

```text
StorageTestError
```

while preserving:

```text
OSError
```

as the original cause.

---

# SECTION 17 — SCENARIO-BASED QUESTIONS

## Q51. Scenario

You receive:

```text
2026-08-11 09:10:04 [ERROR]
/dev/sda READ ERROR sector=182736
```

What do you conclude?

### Answer

We can conclude that:

```text
/dev/sda
READ operation
encountered an error
associated with sector 182736
```

We should not immediately conclude:

```text
The drive is permanently defective.
```

Additional evidence is required.

---

## Q52. Scenario

The first READ attempt fails, the second succeeds.

What should the report contain?

### Answer

It should preserve both events.

Example:

```text
Attempt 1 → READ ERROR
Attempt 2 → READ PASS

Final result → PASS
```

But the intermittent failure should remain visible for investigation.

---

## Q53. Scenario

The device test passes, but the parser crashes.

What is the likely ownership?

### Answer

The immediate failure likely belongs to the result-processing/automation layer rather than automatically to the storage device.

The test execution result and parser result should be tracked separately.

---

# SECTION 18 — DESIGN INTERVIEW

## Q54. How would you prevent false PASS results in a storage automation framework?

### Answer

Use explicit result handling.

A failure must not be swallowed.

For example:

```text
Exception
 ↓
Classify
 ↓
Recover if appropriate
 ↓
If recovery fails
 ↓
Explicit FAIL
```

Avoid:

```python
except Exception:
    pass
```

because the framework may continue without recording the failure.

---

## Q55. How would you make storage automation failures easy to debug?

### Answer

Design the framework to capture:

```text
Timestamp
Device
Operation
Test phase
Exception type
Error message
Traceback
Retry count
Configuration
System evidence
Device evidence
Diagnostic output
Final result
```

Then preserve the complete failure timeline.

---

# SECTION 19 — RAPID-FIRE QUESTIONS

## Q56. Can `try` exist without `except`?

### Answer

Yes, when paired with `finally`.

```python
try:
    operation()

finally:
    cleanup()
```

---

## Q57. Can `try` exist without `finally`?

### Answer

Yes.

A `try` can use `except`, `else`, or both without `finally`.

---

## Q58. Can there be multiple `except` blocks?

### Answer

Yes.

---

## Q59. Can `finally` execute after an exception?

### Answer

Yes.

---

## Q60. Does `finally` execute after `return`?

### Answer

Normally, yes.

Example:

```python
def test():

    try:
        return "PASS"

    finally:
        print("Cleanup")
```

The cleanup executes before the function returns.

---

## Q61. Does `raise` stop normal execution?

### Answer

Yes.

It transfers control to an appropriate exception handler.

---

## Q62. Should all exceptions be logged?

### Answer

Important failures should be appropriately recorded, but logging strategy should avoid unnecessary duplicate logging and sensitive information.

---

## Q63. Should passwords or secrets be logged?

### Answer

No.

Sensitive information should not be exposed in logs.

---

# SECTION 20 — FINAL SENIOR-LEVEL QUESTION

## Q64. Explain your complete exception-handling philosophy for Storage Test Automation.

### Reference Answer

A strong answer:

```text
I would first validate configuration and device inputs
before starting the storage operation.

I would use domain-specific exceptions so that the framework
can distinguish validation failures, execution failures,
timeouts, and parsing failures.

At the execution layer, low-level exceptions can be translated
into storage-specific exceptions using exception chaining so
that the original cause is preserved.

I would catch only exceptions that the current layer can
meaningfully handle.

For retryable failures such as certain timeouts, I would use
a bounded retry policy. Before retrying, I would record the
failure and collect appropriate diagnostics.

I would never silently swallow exceptions because that could
produce false PASS results.

Required cleanup would be performed using finally or suitable
context managers.

Unexpected exceptions would remain visible and would be logged
with traceback information.

Finally, I would convert the execution state into an explicit
test result such as PASS, FAIL, INVALID, or ERROR.

The exception itself is not automatically the root cause.
I would preserve the evidence and use the failure timeline,
system information, device information, and test data to
perform Root Cause Analysis.
```

---

# FINAL INTERVIEW MENTAL MODEL

```text
                 EXCEPTION
                     |
                     ↓
                 CLASSIFY
                     |
          ┌──────────┼──────────┐
          |          |          |
      Validation   Timeout    Unexpected
          |          |          |
          ↓          ↓          ↓
         STOP      RETRY      LOG
                     |          |
                 Diagnostics    |
                     |          |
                  Retry limit  |
                     |          |
                     ↓          ↓
                    FAIL      PROPAGATE
                     \          /
                      \        /
                       ↓      ↓
                         REPORT
                           |
                           ↓
                        CLEANUP
                           |
                           ↓
                    ROOT CAUSE ANALYSIS
```

---

# FINAL INTERVIEW RULES

Remember these principles:

```text
1. Catch specific exceptions.
2. Do not swallow failures.
3. Use narrow try blocks.
4. Use finally for required cleanup.
5. Use raise for explicit validation failures.
6. Use custom exceptions for domain-specific failures.
7. Use exception chaining to preserve causes.
8. Retry only appropriate failures.
9. Always bound retries.
10. Log useful context.
11. Preserve traceback information.
12. Collect diagnostics.
13. Distinguish device failures from framework failures.
14. Do not confuse symptoms with root causes.
15. Always produce an explicit final test result.
```

# END

