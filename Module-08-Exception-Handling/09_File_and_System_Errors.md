# 09 — Exception Logging and Debugging

## Objective

Exception handling tells us how to handle failures.

Logging and debugging help us answer:

- What failed?
- Where did it fail?
- When did it fail?
- Which device was involved?
- Which operation was running?
- What exception occurred?
- What was the original cause?
- What information should be preserved for troubleshooting?

This is especially important in Storage Test Automation because a test failure is not useful if we only know:

```text
Test failed
````

We need enough evidence to determine the root cause.

---

# 1. Why Logging Matters

Consider:

```python
try:
    run_storage_test("/dev/sda")

except Exception:
    print("Test failed")
```

The output tells us almost nothing.

We do not know:

```text
Device
Operation
Exception type
Timestamp
Failure reason
Location of failure
```

A better design records useful diagnostic information.

---

# 2. `print()` vs Logging

For simple learning programs:

```python
print("Test failed")
```

may be enough.

For real automation, Python provides the:

```python
logging
```

module.

Example:

```python
import logging

logging.error("Storage test failed")
```

---

# 3. Basic Logging

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Storage test started")
logging.warning("Retry required")
logging.error("Storage test failed")
```

Typical levels include:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

---

# 4. Logging Levels

## DEBUG

Detailed information useful while diagnosing a problem.

```python
logging.debug("Submitting READ command")
```

---

## INFO

Normal operational information.

```python
logging.info("Storage test started")
```

---

## WARNING

Something unexpected happened, but execution may continue.

```python
logging.warning("Test timeout detected; retrying")
```

---

## ERROR

An operation failed.

```python
logging.error("READ operation failed")
```

---

## CRITICAL

A severe failure affecting the application or system.

```python
logging.critical("Storage test framework cannot continue")
```

---

# 5. Logging an Exception

Inside an exception handler:

```python
try:
    run_test()

except Exception as exc:
    logging.error("Storage test failed: %s", exc)
```

This records the exception message.

---

# 6. Logging the Exception Type

Sometimes the message alone is not enough.

```python
try:
    run_test()

except Exception as exc:
    logging.error(
        "Exception type: %s",
        type(exc).__name__
    )
```

For example:

```text
Exception type: TimeoutError
```

---

# 7. Logging Device Information

For storage automation, always preserve the resource involved.

```python
device = "/dev/sda"

try:
    run_test(device)

except Exception as exc:
    logging.error(
        "Storage test failed for %s: %s",
        device,
        exc
    )
```

Now the log identifies the device.

---

# 8. Logging Operation Information

Include the operation when useful.

```python
device = "/dev/sda"
operation = "READ"

try:
    run_operation(device, operation)

except Exception as exc:
    logging.error(
        "Operation failed: device=%s operation=%s error=%s",
        device,
        operation,
        exc
    )
```

This is much more useful for troubleshooting.

---

# 9. Logging Timestamp

Python's logging framework automatically adds timestamps when configured with a format.

Example:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
```

Then:

```python
logging.info("Storage test started")
```

may produce:

```text
2026-08-11 09:10:01 INFO Storage test started
```

---

# 10. Useful Storage Log Format

A useful format might be:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
```

Then:

```python
logging.info(
    "device=/dev/sda operation=READ status=PASS"
)
```

produces information similar to:

```text
2026-08-11 09:10:02 [INFO] device=/dev/sda operation=READ status=PASS
```

---

# 11. Logging Exceptions With Traceback

One of the most important techniques is:

```python
logging.exception("Storage test failed")
```

Use this inside an `except` block.

Example:

```python
try:
    run_test()

except Exception:
    logging.exception("Storage test failed")
```

This records the exception together with traceback information.

---

# 12. Why Traceback Matters

Consider:

```python
try:
    run_test()

except Exception as exc:
    logging.error("Test failed: %s", exc)
```

You may know:

```text
Test failed: timeout
```

But not necessarily:

```text
Which function failed?
Which line failed?
What was the call path?
```

A traceback provides that execution context.

---

# 13. `logging.exception()` vs `logging.error()`

Inside an `except` block:

```python
logging.exception("Storage test failed")
```

automatically includes exception traceback information.

Whereas:

```python
logging.error("Storage test failed")
```

normally logs only the message unless exception information is explicitly included.

Therefore:

```text
Inside except + need traceback
        ↓
logging.exception()
```

---

# 14. `exc_info=True`

Another way to include exception information is:

```python
try:
    run_test()

except Exception:
    logging.error(
        "Storage test failed",
        exc_info=True
    )
```

This includes traceback information.

For an exception handler, `logging.exception()` is usually the clearer expression.

---

# 15. Basic Debugging Workflow

When an exception occurs:

```text
Failure
   ↓
Identify exception type
   ↓
Read exception message
   ↓
Read traceback
   ↓
Identify failing function
   ↓
Identify failing line
   ↓
Inspect inputs/state
   ↓
Determine root cause
```

This is more useful than simply fixing the visible error message.

---

# 16. Exception Type vs Root Cause

Suppose:

```text
FileNotFoundError
```

The exception type tells us:

```text
A file/resource could not be found.
```

But the root cause could be:

```text
Wrong path
Test did not generate the log
Device disappeared
Mount point changed
Configuration error
```

Therefore:

```text
Exception
≠
Root cause
```

The exception is evidence.

We still need to investigate.

---

# 17. Storage Troubleshooting Example

Suppose:

```text
FileNotFoundError: /var/log/storage_test.log
```

Do not immediately conclude:

```text
Storage device failed.
```

Possible causes include:

```text
Log path incorrect
Test never started
Test crashed before logging
Log generation failed
Permissions/environment problem
```

The correct approach is to investigate the complete execution path.

---

# 18. Logging Before the Operation

Good automation records important state before executing a risky operation.

```python
logging.info(
    "Starting storage test: device=%s",
    device
)

run_test(device)
```

This helps establish:

```text
What was the program attempting to do?
```

---

# 19. Logging After Success

Record successful completion too.

```python
logging.info(
    "Storage test completed: device=%s status=PASS",
    device
)
```

This allows logs to show:

```text
START
...
PASS
```

instead of only recording failures.

---

# 20. Logging Failure

```python
try:
    run_test(device)

except StorageTestError as exc:
    logging.exception(
        "Storage test failed: device=%s",
        device
    )
    raise
```

This provides:

```text
Device
Failure
Exception
Traceback
Propagation
```

---

# 21. Logging Retry Attempts

If a timeout is retryable:

```python
for attempt in range(3):

    try:
        run_test(device)
        break

    except StorageTimeoutError:
        logging.warning(
            "Timeout: device=%s attempt=%d",
            device,
            attempt + 1
        )
```

This tells us how many attempts occurred.

---

# 22. Logging Final Retry Failure

Do not only log individual retries.

Also record final failure.

```python
max_retries = 3

for attempt in range(max_retries):

    try:
        run_test(device)
        break

    except StorageTimeoutError:
        logging.warning(
            "Timeout: device=%s attempt=%d",
            device,
            attempt + 1
        )

else:
    logging.error(
        "Storage test failed after %d attempts: device=%s",
        max_retries,
        device
    )
```

The `else` here belongs to the `for` loop, not exception handling.

It executes when the loop completes without `break`.

---

# 23. Important — Two Different `else` Concepts

Python has:

```python
try:
    ...
except:
    ...
else:
    ...
```

and:

```python
for item in items:
    ...
else:
    ...
```

These are different mechanisms.

For exception handling:

```text
try/except else
→ runs if try succeeds
```

For loops:

```text
for else
→ runs if loop completes without break
```

Do not confuse them.

---

# 24. Logging Cleanup

Cleanup should also be visible.

```python
finally:
    logging.info(
        "Cleaning up storage test: device=%s",
        device
    )

    cleanup(device)
```

Now the log tells us:

```text
Test started
Test failed
Cleanup started
```

This can be extremely useful when diagnosing test contamination.

---

# 25. Logging Cleanup Failures

Cleanup can fail too.

Example:

```python
finally:
    try:
        cleanup(device)

    except Exception:
        logging.exception(
            "Cleanup failed: device=%s",
            device
        )
```

The cleanup failure should not silently disappear.

The exact strategy depends on whether cleanup failure should fail the overall operation.

---

# 26. Preserve Original Exception

Consider:

```python
try:
    run_test()

except StorageTestError:
    logging.exception("Storage test failed")
    raise
```

The original exception continues upward.

This gives us:

```text
Log
 +
Original exception
 +
Original traceback
```

---

# 27. Logging and Exception Chaining

Example:

```python
try:
    parse_log()

except ValueError as exc:
    logging.exception(
        "Low-level parsing failure"
    )

    raise LogParsingError(
        "Storage log parsing failed"
    ) from exc
```

Now we have:

```text
ValueError
   ↓
original cause
   ↓
LogParsingError
   ↓
domain-level failure
```

---

# 28. Logging Context Before Re-Raising

A good pattern:

```python
try:
    run_operation(device)

except TimeoutError as exc:
    logging.exception(
        "Timeout during operation: device=%s",
        device
    )
    raise
```

The lower layer contributes useful context.

The higher layer still receives the failure.

---

# 29. Do Not Log the Same Exception Excessively

A common problem in large applications is duplicate logging.

Example:

```text
Low-level function:
ERROR: test failed

Middle layer:
ERROR: test failed

Top-level:
ERROR: test failed
```

This creates noisy logs.

A better architecture decides where the detailed traceback is logged and where higher layers add only meaningful context.

---

# 30. Logging vs Handling

Logging does not mean handling.

Example:

```python
try:
    run_test()

except StorageTestError:
    logging.exception("Test failed")
    raise
```

The exception was:

```text
Logged
+
Re-raised
```

It was not recovered.

Remember:

```text
log
≠
handle
```

---

# 31. Logging vs Recovery

Example:

```python
except StorageTimeoutError:
    logging.warning("Timeout occurred")
    retry_test()
```

Here:

```text
Logging
    ↓
Information

Retry
    ↓
Recovery strategy
```

They are separate responsibilities.

---

# 32. Logging Sensitive Information

Do not blindly log everything.

Avoid exposing:

```text
Passwords
Tokens
Credentials
Private keys
Sensitive configuration
Secrets
```

Even in debugging output.

For storage automation, also consider whether device identifiers or environment information need controlled handling depending on the environment.

---

# 33. Logging Commands Carefully

Suppose:

```python
command = [
    "storage-test",
    device,
    "--token",
    token
]
```

Do not blindly log:

```python
logging.info("Running command: %s", command)
```

because the token could appear in logs.

Instead, sanitize sensitive values before logging.

---

# 34. Debug Logging

Use DEBUG for detailed diagnostic information.

Example:

```python
logging.debug(
    "Submitting READ operation: device=%s block=%d",
    device,
    block
)
```

This information may be useful while troubleshooting but too noisy for normal INFO-level operation.

---

# 35. INFO Logging

Use INFO for major lifecycle events.

Example:

```python
logging.info(
    "Storage test started: device=%s",
    device
)
```

```python
logging.info(
    "Storage test completed: device=%s status=PASS",
    device
)
```

---

# 36. WARNING Logging

Use WARNING when something unexpected happened but the system can continue.

Example:

```python
logging.warning(
    "Storage test timeout; retrying: device=%s",
    device
)
```

---

# 37. ERROR Logging

Use ERROR when an operation failed.

```python
logging.error(
    "Storage test failed: device=%s",
    device
)
```

If traceback is needed inside `except`:

```python
logging.exception(
    "Storage test failed: device=%s",
    device
)
```

---

# 38. CRITICAL Logging

Use CRITICAL for severe failures.

Example:

```python
logging.critical(
    "Storage test framework cannot continue"
)
```

This should not be used for every test failure.

---

# 39. Logging a Custom Exception

```python
try:
    validate_device(device)

except DeviceValidationError as exc:
    logging.error(
        "Device validation failed: device=%s error=%s",
        device,
        exc
    )
```

This combines:

```text
Domain exception
+
Device context
+
Useful message
```

---

# 40. Structured Logging Concept

Even if using standard Python logging, write messages with consistent fields.

Example:

```text
device=/dev/sda
operation=READ
status=PASS
```

Failure:

```text
device=/dev/sda
operation=READ
status=FAIL
error=READ_ERROR
sector=182736
```

Consistent fields make logs easier to search and analyze.

---

# 41. Example Storage Log

A useful format:

```text
2026-08-11 09:10:01 [INFO] device=/dev/sda event=TEST_START
2026-08-11 09:10:02 [INFO] device=/dev/sda operation=READ status=PASS
2026-08-11 09:10:03 [INFO] device=/dev/sda operation=WRITE status=PASS
2026-08-11 09:10:04 [ERROR] device=/dev/sda operation=READ status=FAIL error=READ_ERROR sector=182736
2026-08-11 09:10:05 [INFO] device=/dev/sda event=TEST_END
```

This gives a timeline.

---

# 42. Timeline Is Important

When debugging a storage test, reconstruct:

```text
T0
Test started

T1
READ started

T2
READ passed

T3
WRITE started

T4
WRITE failed

T5
Retry started

T6
Retry failed

T7
Test ended
```

Logs allow us to reconstruct this sequence.

---

# 43. Logging Is Evidence

For troubleshooting:

```text
Symptom
   ↓
Logs
   ↓
Timeline
   ↓
Exception
   ↓
State
   ↓
Root cause
```

The log should help us move from symptom to evidence.

---

# 44. Root Cause vs Symptom

Suppose the final log says:

```text
Storage test failed
```

That is the symptom.

A better log may say:

```text
READ ERROR
device=/dev/sda
sector=182736
retry=3
```

This provides more evidence.

The root cause still requires investigation.

---

# 45. Example — Debugging a Storage Failure

Suppose:

```text
ERROR device=/dev/sda operation=READ
error=TimeoutError
```

Do not immediately conclude:

```text
Drive is defective.
```

Investigate:

```text
Device state
Kernel logs
Link state
Timeout configuration
Controller state
Previous retries
I/O queue
Transport errors
```

The exception is only one piece of evidence.

---

# 46. Logging Kernel/System Evidence

A storage automation framework may collect external diagnostic evidence such as:

```text
Kernel messages
Device state
SMART information
Transport status
Command output
Test logs
Application logs
```

The exact commands depend on the platform and test environment.

The important principle is:

```text
Application exception
+
System evidence
=
better troubleshooting
```

---

# 47. Exception Debugging Workflow

Use this workflow:

```text
1. Capture exception
        ↓
2. Identify exception type
        ↓
3. Read message
        ↓
4. Read traceback
        ↓
5. Identify device/resource
        ↓
6. Identify operation
        ↓
7. Reconstruct timeline
        ↓
8. Collect external evidence
        ↓
9. Form hypotheses
        ↓
10. Test hypotheses
        ↓
11. Identify root cause
        ↓
12. Apply corrective action
        ↓
13. Verify
```

---

# 48. Do Not Debug From the Exception Message Alone

Example:

```text
TimeoutError: operation timed out
```

This does not tell us automatically:

```text
Why?
```

Possible causes:

```text
Device busy
Transport problem
Controller issue
Firmware behavior
Queue congestion
Invalid timeout
System load
Device failure
```

Investigate before assigning root cause.

---

# 49. Debugging With Variables

When debugging, inspect the state that existed at failure time.

Example:

```python
try:
    result = run_test(
        device=device,
        block_size=block_size,
        timeout=timeout
    )

except Exception:
    logging.exception(
        "Test failed: device=%s block_size=%s timeout=%s",
        device,
        block_size,
        timeout
    )
    raise
```

This captures relevant execution state.

---

# 50. Avoid Excessive Logging

More logs do not automatically mean better troubleshooting.

Bad:

```text
Entering function
Entering variable
Entering loop
Incrementing variable
Checking condition
...
```

Useful logging should answer:

```text
What meaningful event happened?
What resource was involved?
What important state changed?
What failed?
```

---

# 51. Logging Strategy

A good storage automation framework should log:

```text
Test lifecycle
Device
Operation
Configuration
Retries
Failures
Exceptions
Diagnostics
Cleanup
Final result
```

Avoid unnecessary noise.

---

# 52. Complete Example

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


class StorageError(Exception):
    pass


class StorageTimeoutError(StorageError):
    pass


def run_storage_test(device):

    logging.info(
        "Storage test started: device=%s",
        device
    )

    try:
        execute_test(device)

    except TimeoutError as exc:

        logging.exception(
            "Storage test timeout: device=%s",
            device
        )

        raise StorageTimeoutError(
            f"Storage test timed out: {device}"
        ) from exc

    else:

        logging.info(
            "Storage test completed: device=%s status=PASS",
            device
        )

    finally:

        logging.info(
            "Collecting diagnostics: device=%s",
            device
        )

        collect_diagnostics(device)
```

This combines:

```text
Logging
Exception handling
Exception chaining
else
finally
Custom exception
Storage context
```

---

# 53. What Happens in This Example?

Successful test:

```text
START
   ↓
execute
   ↓
SUCCESS
   ↓
else
   ↓
PASS log
   ↓
finally
   ↓
diagnostics
```

Timeout:

```text
START
   ↓
execute
   ↓
TimeoutError
   ↓
logging.exception()
   ↓
StorageTimeoutError
   ↓
finally
   ↓
diagnostics
   ↓
propagate
```

---

# 54. Common Mistake — Logging Without Context

Bad:

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

---

# 55. Common Mistake — Losing Traceback

Bad:

```python
except Exception as exc:
    logging.error(str(exc))
```

This may omit the traceback.

If traceback is required:

```python
except Exception:
    logging.exception("Storage test failed")
```

---

# 56. Common Mistake — Catching and Swallowing

Bad:

```python
except Exception as exc:
    logging.error(str(exc))
```

and then silently continuing.

Potential problem:

```text
Failure
 ↓
Logged
 ↓
Ignored
 ↓
Program continues
 ↓
Incorrect result
```

If the current layer cannot recover:

```python
except Exception:
    logging.exception("Operation failed")
    raise
```

may be appropriate.

---

# 57. Common Mistake — Logging Sensitive Data

Bad:

```python
logging.info(
    "Connecting with password=%s",
    password
)
```

Never expose secrets unnecessarily.

---

# 58. Common Mistake — Logging Only Final Failure

Suppose:

```text
TEST FAILED
```

is the only log.

You may not know:

```text
When did it start?
Which device?
Which operation?
Was there a retry?
What happened before failure?
Was cleanup completed?
```

A useful lifecycle log is better.

---

# 59. Interview Questions

## Q1. Why is logging important in exception handling?

It preserves diagnostic information about failures and helps reconstruct what happened.

---

## Q2. Difference between `logging.error()` and `logging.exception()`?

`logging.exception()` is intended for use inside an exception handler and includes traceback information.

---

## Q3. Why should storage logs contain device information?

Because a test framework may operate on many devices, and failure evidence must identify the affected resource.

---

## Q4. Why is traceback useful?

It shows where the exception occurred and provides the execution path leading to the failure.

---

## Q5. Does logging an exception mean it has been handled?

No.

Logging records information. Handling means deciding what the application should do with the failure.

---

## Q6. Why might an exception be logged and then re-raised?

To preserve diagnostic evidence while allowing a higher layer to make the final recovery or reporting decision.

---

# 60. Storage Engineering Interview Questions

## Q7. A test reports `TimeoutError`. Is that enough to declare the drive faulty?

No.

A timeout is a symptom/failure condition. Additional evidence is required to determine root cause.

---

## Q8. What information should be logged for a storage I/O failure?

At minimum, where relevant:

```text
Timestamp
Device
Operation
Exception type
Error message
Retry count
Test context
Relevant diagnostic data
```

---

## Q9. Why should logs capture the timeline?

Because storage failures often require correlation between events:

```text
Command
 ↓
Retry
 ↓
Timeout
 ↓
Transport event
 ↓
Device state change
```

Timeline correlation helps determine root cause.

---

## Q10. What is the difference between symptom and root cause?

Example:

```text
Symptom:
READ timeout

Possible root cause:
Transport/link/controller/device/system issue
```

The symptom is observed behavior.

The root cause is the underlying reason that produced it.

---

# 61. Knowledge-Gap Checklist

Before moving forward:

```text
[ ] logging module
[ ] Logging levels
[ ] DEBUG
[ ] INFO
[ ] WARNING
[ ] ERROR
[ ] CRITICAL
[ ] logging.error()
[ ] logging.exception()
[ ] traceback
[ ] Exception type logging
[ ] Device/context logging
[ ] Operation logging
[ ] Retry logging
[ ] Cleanup logging
[ ] Exception propagation
[ ] Exception chaining
[ ] Structured log fields
[ ] Timeline reconstruction
[ ] Symptom vs root cause
[ ] Debugging workflow
[ ] Storage failure investigation
[ ] Sensitive information handling
```

---

# 62. Final Mental Model

Exception handling tells us:

```text
What failed?
```

Logging tells us:

```text
What happened around the failure?
```

Debugging tells us:

```text
Why did it happen?
```

Therefore:

```text
Exception
   ↓
Capture
   ↓
Log
   ↓
Traceback
   ↓
Context
   ↓
System evidence
   ↓
Timeline
   ↓
Root Cause Analysis
```

---

# 63. Final Engineering Rule

Never design automation around:

```text
"Something failed."
```

Design it around:

```text
What failed?
        ↓
Where?
        ↓
When?
        ↓
On which device?
        ↓
During which operation?
        ↓
What exception occurred?
        ↓
What evidence exists?
        ↓
Can we recover?
        ↓
If not, how do we propagate and report it?
```

For Storage Test Automation:

```text
Exception
   +
Structured logging
   +
Traceback
   +
Device context
   +
Operation context
   +
System evidence
   ↓
Effective troubleshooting
   ↓
Root Cause Analysis
```

# END

````
