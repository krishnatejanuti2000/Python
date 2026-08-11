# 10 — Exception Handling Best Practices

## Objective

This document focuses on writing exception handling that is:

- Clear
- Predictable
- Maintainable
- Debuggable
- Safe
- Appropriate for automation
- Suitable for Storage Test Engineering

The goal is not simply to know how to use `try/except`.

The goal is to design exception handling correctly.

---

# 1. Best Practice — Catch Specific Exceptions

Prefer:

```python
try:
    value = int(user_input)

except ValueError:
    print("Invalid integer")
````

Avoid unnecessarily broad handling:

```python
try:
    value = int(user_input)

except Exception:
    print("Something went wrong")
```

Why?

Because the specific version communicates exactly what failure is expected.

---

# 2. Best Practice — Do Not Catch Exceptions You Cannot Handle

An exception should generally be caught only when the current layer knows what to do with it.

Good:

```python
try:
    value = int(user_input)

except ValueError:
    value = 0
```

The program knows how to recover.

But:

```python
try:
    run_storage_test()

except StorageTestError:
    print("Failed")
```

is questionable if the program does nothing meaningful after the failure.

If the current layer cannot recover, allow the exception to propagate.

---

# 3. Best Practice — Keep `try` Blocks Small

Prefer:

```python
try:
    data = read_log()

except FileNotFoundError:
    handle_missing_log()

parse_log(data)
generate_report(data)
```

instead of:

```python
try:
    data = read_log()
    parse_log(data)
    generate_report(data)

except Exception:
    print("Something failed")
```

A small `try` block makes it easier to determine which operation caused the exception.

---

# 4. Why Large `try` Blocks Are Dangerous

Consider:

```python
try:
    read_log()
    parse_log()
    validate_result()
    generate_report()
```

If an exception occurs, the handler may not clearly communicate which operation failed.

Possible failures:

```text
read_log()
parse_log()
validate_result()
generate_report()
```

A narrow exception boundary improves troubleshooting.

---

# 5. Best Practice — Order Exceptions from Specific to General

Correct:

```python
try:
    open("storage.log")

except FileNotFoundError:
    print("Log file missing")

except PermissionError:
    print("Permission denied")

except OSError:
    print("Other OS error")
```

General rule:

```text
Specific
   ↓
More general
   ↓
Fallback
```

---

# 6. Best Practice — Do Not Catch `BaseException` Broadly

Avoid:

```python
try:
    operation()

except BaseException:
    print("Failure")
```

This can catch special exceptions such as:

```text
KeyboardInterrupt
SystemExit
GeneratorExit
```

For normal application-level broad handling, use:

```python
except Exception:
```

when a broad boundary is genuinely required.

---

# 7. Best Practice — Do Not Silently Swallow Exceptions

Bad:

```python
try:
    run_test()

except Exception:
    pass
```

This is dangerous because the failure disappears.

The application may continue as though nothing happened.

---

# 8. Why Swallowing Exceptions Is Dangerous

Consider:

```text
Storage test fails
      ↓
Exception occurs
      ↓
except Exception:
    pass
      ↓
Program continues
      ↓
Report says PASS
```

This can produce a false result.

In test automation, this is particularly dangerous.

---

# 9. Best Practice — Preserve the Failure

If the current layer cannot recover:

```python
try:
    run_test()

except StorageTestError:
    logging.exception("Storage test failed")
    raise
```

The failure is:

```text
Logged
+
Preserved
+
Propagated
```

---

# 10. Best Practice — Use `raise` Correctly

Inside an `except` block:

```python
raise
```

re-raises the current exception.

Example:

```python
try:
    run_test()

except StorageTestError:
    logging.exception("Test failed")
    raise
```

This preserves the original exception and traceback.

---

# 11. Best Practice — Do Not Recreate an Exception Unnecessarily

Avoid:

```python
try:
    run_test()

except StorageTestError as exc:
    raise StorageTestError(str(exc))
```

This is unnecessary if no additional context is being added.

Prefer:

```python
except StorageTestError:
    raise
```

if the goal is simply propagation.

---

# 12. Best Practice — Add Context When Re-Raising

If additional domain context is useful:

```python
try:
    run_test(device)

except TimeoutError as exc:
    raise StorageTimeoutError(
        f"Storage test timed out on {device}"
    ) from exc
```

Now we have:

```text
Original exception
        ↓
TimeoutError
        ↓
Additional context
        ↓
StorageTimeoutError
```

---

# 13. Best Practice — Use Exception Chaining

Use:

```python
raise NewError(...) from exc
```

Example:

```python
try:
    value = int(field)

except ValueError as exc:
    raise LogParsingError(
        "Invalid numeric field in storage log"
    ) from exc
```

This preserves the original cause.

---

# 14. Best Practice — Use Meaningful Custom Exceptions

Instead of:

```python
raise Exception("Invalid device")
```

use:

```python
raise DeviceValidationError(
    f"Invalid device: {device}"
)
```

The exception itself communicates the domain meaning.

---

# 15. Best Practice — Build Logical Exception Hierarchies

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
```

This allows:

```text
Specific handling
        ↓
StorageTimeoutError

Broader test handling
        ↓
StorageTestError

General storage handling
        ↓
StorageError
```

---

# 16. Best Practice — Use Built-in Exceptions When Appropriate

Do not create a custom exception when a standard exception already describes the condition well.

For example:

```python
raise ValueError("Capacity must be positive")
```

is perfectly reasonable.

Likewise:

```python
raise TypeError("Device must be a string")
```

is appropriate for a type violation.

Use custom exceptions when domain-specific classification adds value.

---

# 17. Best Practice — Choose Exceptions by Meaning

A useful distinction:

```text
Wrong type
    ↓
TypeError

Correct type but invalid value
    ↓
ValueError

OS/resource failure
    ↓
OSError or appropriate subclass

Domain-specific storage failure
    ↓
StorageError / child exception
```

Choose the exception that best describes the condition.

---

# 18. Best Practice — Validate Early

Validate inputs before starting expensive operations.

Example:

```python
validate_device(device)
validate_capacity(capacity)

run_storage_test(device)
```

Not:

```python
run_storage_test(device)

# discover later that the device was invalid
```

Early validation prevents unnecessary work.

---

# 19. Best Practice — Do Not Retry Every Exception

Retry should be based on the failure type.

Example:

```python
except StorageTimeoutError:
    retry_test()
```

But:

```python
except DeviceValidationError:
    report_configuration_failure()
```

A validation error normally should not be retried without changing the input/configuration.

---

# 20. Best Practice — Limit Retries

Avoid:

```python
while True:
    try:
        run_test()

    except StorageTimeoutError:
        retry()
```

A permanent failure could cause an infinite loop.

Prefer a bounded retry policy:

```python
max_retries = 3

for attempt in range(max_retries):

    try:
        run_test()
        break

    except StorageTimeoutError:
        logging.warning(
            "Timeout on attempt %d",
            attempt + 1
        )
```

---

# 21. Best Practice — Make Retry Policy Explicit

A good framework should define:

```text
Maximum attempts
Retryable exceptions
Delay/backoff
Diagnostic collection
Final failure behavior
```

For example:

```text
StorageTimeoutError
    ↓
Collect diagnostics
    ↓
Retry up to 3 times
    ↓
Still failing?
    ↓
Mark test FAILED
```

---

# 22. Best Practice — Use `finally` for Required Cleanup

Example:

```python
try:
    run_storage_test()

finally:
    cleanup()
```

Cleanup should not depend only on the success path.

---

# 23. Best Practice — Prefer Context Managers for Supported Resources

For files:

```python
with open("storage.log", "r") as file:
    data = file.read()
```

This is preferable to manually managing the file whenever the context-manager interface is appropriate.

---

# 24. Best Practice — Preserve Diagnostic Information

For a storage failure, useful information may include:

```text
Timestamp
Device
Operation
Exception type
Error message
Retry count
Test configuration
Command/result
Relevant diagnostic information
```

Do not reduce everything to:

```text
Test failed
```

---

# 25. Best Practice — Use Logging Instead of Debug `print()` in Production

Learning example:

```python
print("Test failed")
```

Automation framework:

```python
logging.error(
    "Storage test failed: device=%s",
    device
)
```

Logging provides:

```text
Levels
Timestamps
Formatting
Handlers
Files/streams
Tracebacks
Centralized configuration
```

---

# 26. Best Practice — Use `logging.exception()` When Traceback Is Needed

Inside `except`:

```python
try:
    run_test()

except StorageTestError:
    logging.exception(
        "Storage test failed"
    )
    raise
```

This is useful during troubleshooting because the traceback is preserved in the log.

---

# 27. Best Practice — Include Context in Logs

Weak:

```python
logging.error("Failed")
```

Better:

```python
logging.error(
    "Storage test failed: device=%s operation=%s",
    device,
    operation
)
```

The second version provides actionable context.

---

# 28. Best Practice — Do Not Log Secrets

Avoid:

```python
logging.info(
    "Password=%s",
    password
)
```

Never expose credentials, tokens, or other sensitive values unnecessarily in logs.

---

# 29. Best Practice — Avoid Duplicate Logging

A low-level function might log:

```text
Storage test failed
```

Then every higher layer may log the same failure again.

This can create noisy logs.

A better design determines:

```text
Where should detailed traceback be logged?
Where should context be added?
Where should final result be reported?
```

---

# 30. Best Practice — Separate Logging From Recovery

Logging:

```python
logging.exception("Test failed")
```

does not mean the failure has been handled.

Recovery might be:

```python
retry_test()
```

or:

```python
mark_test_failed()
```

or:

```python
raise
```

Keep these responsibilities conceptually separate.

---

# 31. Best Practice — Do Not Use Exceptions for Normal Control Flow

Exceptions should represent exceptional situations.

Avoid using exceptions where normal operations already exist.

Example:

```python
value = dictionary.get("status", "UNKNOWN")
```

may be preferable to intentionally causing and catching:

```python
try:
    value = dictionary["status"]

except KeyError:
    value = "UNKNOWN"
```

when a missing key is an expected normal condition.

---

# 32. Best Practice — Write Useful Error Messages

Weak:

```python
raise ValueError("Invalid")
```

Better:

```python
raise ValueError(
    f"Invalid capacity: {capacity}"
)
```

Storage example:

```python
raise DeviceValidationError(
    f"Unsupported device path: {device}"
)
```

A good message helps the engineer understand the failure immediately.

---

# 33. Best Practice — Include the Relevant State

Example:

```python
try:
    run_test(
        device=device,
        block_size=block_size,
        timeout=timeout
    )

except StorageTestError:
    logging.exception(
        "Test failed: device=%s block_size=%s timeout=%s",
        device,
        block_size,
        timeout
    )
    raise
```

Now the failure contains useful execution context.

---

# 34. Best Practice — Do Not Over-Catch

Avoid:

```python
try:
    everything()

except Exception:
    recover()
```

This can catch:

```text
Programming bugs
Unexpected states
Configuration errors
Library failures
Logic errors
```

and incorrectly treat all of them as recoverable.

---

# 35. Best Practice — Separate Expected and Unexpected Failures

Expected:

```text
DeviceValidationError
StorageTimeoutError
FileNotFoundError
```

depending on the application.

Unexpected:

```text
Programming bug
Impossible state
Unexpected library failure
```

Expected failures can often be handled deliberately.

Unexpected failures should usually remain visible.

---

# 36. Best Practice — Use a Top-Level Safety Boundary Carefully

A top-level application may use:

```python
def main():

    try:
        run_test_suite()

    except Exception as exc:
        logging.exception(
            "Unhandled application failure"
        )
        return 1

    return 0
```

This prevents an uncontrolled application crash from producing no useful diagnostic information.

However, lower layers should still perform proper classification and handling.

---

# 37. Best Practice — Do Not Hide Programming Bugs

Consider:

```python
def calculate():
    return value_that_does_not_exist
```

This produces:

```text
NameError
```

A broad handler:

```python
except Exception:
    print("Retry")
```

may incorrectly turn a programming bug into a retry.

This is dangerous.

Not every exception means:

```text
Retry
```

---

# 38. Best Practice — Think in Failure Categories

For Storage Test Automation:

```text
Configuration failure
        ↓
Do not blindly retry

Validation failure
        ↓
Fix input/configuration

Transient timeout
        ↓
Possibly retry

Persistent test failure
        ↓
Mark test failed

Log parsing failure
        ↓
Investigate result-processing pipeline

Unexpected application exception
        ↓
Capture diagnostics + investigate
```

---

# 39. Best Practice — Preserve the Original Cause

Bad:

```python
except ValueError:
    raise LogParsingError("Parsing failed")
```

Better:

```python
except ValueError as exc:
    raise LogParsingError(
        "Parsing failed"
    ) from exc
```

The second version preserves:

```text
Original cause
+
Higher-level context
```

---

# 40. Best Practice — Design for Troubleshooting

Exception handling should make these questions answerable:

```text
What failed?
Where did it fail?
When did it fail?
Which device?
Which operation?
Which configuration?
How many retries?
What was the original exception?
What diagnostics were collected?
Was cleanup completed?
Was the failure propagated?
```

---

# 41. Best Practice — Think in Layers

A storage framework might contain:

```text
Test Runner
    ↓
Validation Layer
    ↓
Execution Layer
    ↓
Transport Layer
    ↓
Device
```

Failures may originate at different layers.

For example:

```text
Validation
→ DeviceValidationError

Execution
→ StorageTestError

Timeout
→ StorageTimeoutError

Transport
→ OSError / transport-specific error
```

Each layer should add meaningful context without destroying the original cause.

---

# 42. Best Practice — Exception Translation

A lower layer may expose:

```python
OSError
```

while the higher application layer needs:

```python
StorageTestError
```

Use exception chaining:

```python
try:
    perform_io()

except OSError as exc:
    raise StorageTestError(
        f"I/O failed on {device}"
    ) from exc
```

This translates technical details into domain meaning.

---

# 43. Best Practice — Do Not Translate Everything

Do not blindly convert every exception into:

```python
StorageError
```

If the original exception already provides useful meaning and the caller can handle it correctly, translation may be unnecessary.

Use translation when it provides meaningful abstraction.

---

# 44. Best Practice — Make Failure Classification Consistent

If the framework defines:

```text
DeviceValidationError
StorageTestError
StorageTimeoutError
LogParsingError
```

use those categories consistently.

Do not sometimes represent the same failure as:

```text
ValueError
```

and elsewhere:

```text
Exception("Invalid device")
```

without a reason.

Consistency makes automation easier to maintain.

---

# 45. Best Practice — Keep Error Handling Close to the Decision

Example:

```python
try:
    run_test()

except StorageTimeoutError:
    retry_test()
```

The retry decision belongs near the component that knows whether a timeout is recoverable.

Do not scatter retry logic randomly across the codebase.

---

# 46. Best Practice — Cleanup Should Be Independent of Success

Bad:

```python
try:
    run_test()
    cleanup()
```

If `run_test()` fails, `cleanup()` may never execute.

Better:

```python
try:
    run_test()

finally:
    cleanup()
```

---

# 47. Best Practice — Collect Diagnostics After Failure

For storage automation:

```python
try:
    run_test(device)

except StorageTestError:
    logging.exception(
        "Storage test failed: device=%s",
        device
    )

    collect_diagnostics(device)

    raise
```

This preserves evidence before the environment changes.

---

# 48. Best Practice — Do Not Assume the Exception Is the Root Cause

Example:

```text
TimeoutError
```

is not automatically:

```text
Drive failure
```

Investigate:

```text
Device state
Transport
Controller
Queue
System load
Configuration
Timeout settings
Previous events
```

The exception is a symptom/evidence point.

---

# 49. Best Practice — Verify After Recovery

Suppose a retry succeeds.

Do not automatically assume:

```text
Everything is healthy.
```

Depending on the test requirements, the framework may need to verify:

```text
Test result
Device state
Error history
Consistency
Diagnostics
```

Recovery should be validated.

---

# 50. Best Practice — Make Failure Results Explicit

Instead of:

```python
except StorageTimeoutError:
    print("Retry")
```

a framework may have explicit outcomes:

```text
PASS
FAIL
RETRY
BLOCKED
INVALID_CONFIGURATION
ERROR
```

The exact result model depends on the framework.

The important principle is:

```text
Exception
   ↓
Decision
   ↓
Explicit result
```

---

# 51. Best Practice — Test Exception Paths

Do not test only:

```text
PASS
```

Test:

```text
PASS
Validation failure
Timeout
Retry
Persistent failure
Log parsing failure
Cleanup failure
Unexpected exception
```

Exception paths are part of the software behavior.

---

# 52. Best Practice — Test Failure Recovery

Example:

```text
Timeout
 ↓
Retry
 ↓
PASS
```

and:

```text
Timeout
 ↓
Retry
 ↓
Timeout
 ↓
Retry
 ↓
Timeout
 ↓
FAIL
```

Both paths should be tested.

---

# 53. Best Practice — Do Not Lose Failure State During Cleanup

Suppose:

```python
try:
    run_test()

finally:
    cleanup()
```

If cleanup itself fails, the overall exception behavior can become complicated.

Therefore cleanup operations should be designed carefully.

For important automation:

```python
try:
    run_test()

finally:
    try:
        cleanup()

    except Exception:
        logging.exception(
            "Cleanup failed"
        )
```

The exact policy should be defined by the framework.

---

# 54. Best Practice — Document Recovery Policy

For each important exception, document:

```text
Exception
Meaning
Retryable?
Maximum retries
Diagnostics
Final result
Escalation behavior
```

Example:

```text
StorageTimeoutError

Meaning:
Storage operation exceeded timeout.

Retry:
Yes

Maximum retries:
3

Diagnostics:
Collect device and system state.

Final result:
FAIL if all retries fail.
```

---

# 55. Exception Handling Design Checklist

Before considering exception handling complete:

```text
[ ] Are expected exceptions identified?
[ ] Are handlers specific?
[ ] Are broad handlers avoided where possible?
[ ] Are handlers ordered correctly?
[ ] Are try blocks narrow?
[ ] Are exceptions silently swallowed?
[ ] Is retry policy explicit?
[ ] Is retry bounded?
[ ] Is cleanup guaranteed?
[ ] Is diagnostic information preserved?
[ ] Are useful logs generated?
[ ] Is traceback available where needed?
[ ] Are custom exceptions meaningful?
[ ] Is the hierarchy logical?
[ ] Is exception chaining used when appropriate?
[ ] Are secrets excluded from logs?
[ ] Are unexpected exceptions still visible?
[ ] Are failure paths tested?
[ ] Is recovery verified?
[ ] Is the final result explicit?
```

---

# 56. Storage Test Engineering Checklist

For every storage test, ask:

```text
1. What can fail?
2. Which failures are expected?
3. Which failures are retryable?
4. Which failures are permanent?
5. What diagnostics should be collected?
6. What should be logged?
7. What should be cleaned up?
8. What should be re-raised?
9. What should the final test result be?
```

---

# 57. Example — Recommended Pattern

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


def run_test(device):

    try:
        validate_device(device)
        execute_test(device)

    except DeviceValidationError:
        logging.exception(
            "Device validation failed: device=%s",
            device
        )
        raise

    except TimeoutError as exc:
        logging.exception(
            "Storage timeout: device=%s",
            device
        )

        raise StorageTimeoutError(
            f"Storage test timed out: {device}"
        ) from exc

    except StorageTestError:
        logging.exception(
            "Storage test failed: device=%s",
            device
        )
        raise

    finally:
        collect_diagnostics(device)
```

This demonstrates:

```text
Specific handling
Exception chaining
Logging
Context
Propagation
Cleanup
Custom hierarchy
```

---

# 58. What Makes This Production-Oriented?

The code does not simply say:

```text
Error happened.
```

Instead it provides:

```text
Failure classification
        +
Device context
        +
Traceback
        +
Original cause
        +
Diagnostic collection
        +
Propagation
```

That is much more useful in real automation.

---

# 59. Anti-Pattern Summary

Avoid:

```python
except:
    pass
```

Avoid:

```python
except BaseException:
    pass
```

Avoid:

```python
except Exception:
    print("failed")
```

Avoid:

```python
try:
    everything()
except Exception:
    retry()
```

Avoid infinite retries.

Avoid logging secrets.

Avoid hiding programming errors.

Avoid unnecessarily translating every exception.

Avoid huge `try` blocks.

Avoid losing the original cause.

---

# 60. Good Pattern Summary

Prefer:

```text
Specific exceptions
        ↓
Narrow try blocks
        ↓
Meaningful handling
        ↓
Bounded retry
        ↓
Useful logging
        ↓
Preserved diagnostics
        ↓
Cleanup
        ↓
Re-raise when necessary
        ↓
Explicit final result
```

---

# 61. Interview Questions

## Q1. What are the most important exception-handling best practices?

A strong answer should include:

```text
Catch specific exceptions
Use narrow try blocks
Do not swallow exceptions
Order handlers correctly
Use custom exceptions where useful
Preserve original causes
Use logging appropriately
Use finally for cleanup
Bound retry operations
Do not broadly catch BaseException
```

---

## Q2. Why should you avoid `except Exception` everywhere?

Because it can hide unexpected bugs and incorrectly treat unrelated failures as recoverable.

---

## Q3. Why should retry logic be exception-specific?

Because some failures are transient while others are deterministic or configuration-related.

---

## Q4. Why should exceptions be logged with context?

Because the exception message alone may not identify the affected device, operation, configuration, or test execution state.

---

## Q5. Why is exception chaining important?

It allows higher-level code to add meaningful domain context while preserving the original technical cause.

---

# 62. Storage Engineering Interview Questions

## Q6. A `/dev/sda` READ test timed out three times. What should the framework do?

A reasonable approach is:

```text
Timeout detected
      ↓
Log timeout
      ↓
Collect diagnostics
      ↓
Apply retry policy
      ↓
Retry up to configured limit
      ↓
If still failing
      ↓
Mark test FAILED
      ↓
Preserve evidence
      ↓
Report/escalate
```

The exact recovery policy depends on the test design.

---

## Q7. Why shouldn't a device validation error be blindly retried?

Because the input/configuration itself may be invalid.

Retrying the same invalid condition does not change the underlying state.

---

## Q8. Why is swallowing an exception especially dangerous in test automation?

Because the automation may incorrectly report success or continue from an invalid state, producing unreliable test results.

---

# 63. Final Mental Model

Think about exception handling as an engineering pipeline:

```text
             OPERATION
                 |
                 ↓
              FAILURE
                 |
                 ↓
             CLASSIFY
                 |
        ┌────────┼─────────┐
        |        |         |
    Expected   Retryable  Unexpected
        |        |         |
        ↓        ↓         ↓
     Handle    Retry     Log + Propagate
        |        |         |
        └────────┴─────────┘
                 |
                 ↓
          Collect Evidence
                 |
                 ↓
              Cleanup
                 |
                 ↓
          Final Test Result
```

---

# 64. Final Engineering Rule

Good exception handling is not:

```text
"Catch every error."
```

It is:

```text
"Understand the failure,
classify it correctly,
handle only what you can recover from,
preserve evidence,
clean up safely,
and propagate what you cannot handle."
```

For Storage Test Automation:

```text
Exception
    ↓
Classification
    ↓
Logging
    ↓
Diagnostics
    ↓
Recovery / Retry
    ↓
Cleanup
    ↓
Explicit Result
    ↓
Root Cause Analysis
```

That is the standard to follow when writing production-quality Python automation.

# END

