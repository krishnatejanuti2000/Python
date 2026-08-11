# 11 — Storage Automation Error Handling

## Objective

This document applies Python exception handling to real-world
Storage Test Automation.

The goal is to connect:

- Python exceptions
- Custom exceptions
- Exception hierarchy
- Logging
- Retry handling
- Device validation
- I/O execution
- Timeout handling
- Diagnostic collection
- Cleanup
- Result classification
- Exception propagation
- Root Cause Analysis

The important mindset is:

    Storage automation failure
            ↓
        Detect
            ↓
        Classify
            ↓
        Collect evidence
            ↓
        Recover / Retry / Fail
            ↓
        Cleanup
            ↓
        Report result

---

# 1. Why Storage Automation Needs Error Handling

A storage validation framework may perform operations such as:

```text
Device discovery
Device validation
Test preparation
READ
WRITE
Sequential I/O
Random I/O
Performance testing
Stress testing
Log collection
Result parsing
Report generation
Cleanup
````

Every stage can fail.

For example:

```text
/dev/sda not found
/dev/sda permission denied
READ timeout
WRITE failure
Device disconnected
Command failed
Test process crashed
Log missing
Log parsing failed
Cleanup failed
```

A production automation framework must distinguish these conditions.

---

# 2. Storage Automation Failure Pipeline

A useful model is:

```text
                Test Request
                     |
                     ↓
              Configuration
                     |
                     ↓
              Device Validation
                     |
                     ↓
              Test Preparation
                     |
                     ↓
              Test Execution
                     |
                     ↓
              Result Collection
                     |
                     ↓
               Log Parsing
                     |
                     ↓
                Reporting
                     |
                     ↓
                  Cleanup
```

Failures can occur at every stage.

---

# 3. Failure Classification

A storage framework should classify failures.

Example:

```text
Configuration failure
        ↓
StorageConfigurationError

Device validation failure
        ↓
DeviceValidationError

Test execution failure
        ↓
StorageTestError

Timeout
        ↓
StorageTimeoutError

Log parsing failure
        ↓
LogParsingError

Unexpected application failure
        ↓
Unexpected Exception
```

This allows different handling strategies.

---

# 4. Storage Exception Hierarchy

A practical hierarchy:

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

# 5. Configuration Validation

Before touching a device, validate configuration.

Example:

```python
def validate_config(config):

    if "device" not in config:
        raise StorageConfigurationError(
            "Device is missing from configuration"
        )
```

The important principle is:

```text
Invalid configuration
        ↓
Stop before test execution
```

Do not start an expensive storage test with invalid configuration.

---

# 6. Device Validation

Example:

```python
def validate_device(device):

    if not isinstance(device, str):
        raise DeviceValidationError(
            "Device must be a string"
        )

    if not device.startswith("/dev/"):
        raise DeviceValidationError(
            f"Invalid device path: {device}"
        )
```

Usage:

```python
try:
    validate_device("/dev/sda")

except DeviceValidationError as exc:
    print(f"Validation failed: {exc}")
```

---

# 7. Why Validation Should Happen First

Bad flow:

```text
Start test
    ↓
Open device
    ↓
Start I/O
    ↓
Discover invalid device
```

Better flow:

```text
Receive device
    ↓
Validate
    ↓
Prepare
    ↓
Execute test
```

This prevents avoidable failures.

---

# 8. Device Validation Is Not Device Health Validation

These are different.

### Device validation

Checks whether the input/device reference is valid.

Examples:

```text
Correct device path
Correct device type
Supported device
Expected configuration
```

### Device health

Determines whether the device is operating correctly.

Examples:

```text
I/O errors
Timeouts
Media errors
Transport errors
SMART warnings
Performance degradation
```

Do not confuse validation with health.

---

# 9. Test Preparation

After validation:

```python
validate_device(device)
prepare_test_environment(device)
```

Preparation itself can fail.

Example:

```python
def prepare_test_environment(device):

    if not device_ready(device):
        raise StorageTestError(
            f"Device is not ready: {device}"
        )
```

---

# 10. Test Execution

Example:

```python
def run_test(device):

    try:
        execute_io_test(device)

    except TimeoutError as exc:
        raise StorageTimeoutError(
            f"Storage test timed out: {device}"
        ) from exc
```

Here a low-level exception is converted into a domain-specific exception.

---

# 11. Why Translate Exceptions?

Suppose the low-level library produces:

```text
TimeoutError
```

The Storage Test Framework may need:

```text
StorageTimeoutError
```

because the framework understands:

```text
StorageTimeoutError
    ↓
Retry policy
    ↓
Diagnostic collection
```

The application-level exception gives the failure domain meaning.

---

# 12. Exception Chaining

Use:

```python
raise StorageTimeoutError(
    f"Storage test timed out: {device}"
) from exc
```

The original exception is preserved.

Conceptually:

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

# 13. Timeout Handling

Timeouts are important in storage testing.

Example:

```python
try:
    run_test(device)

except StorageTimeoutError as exc:
    logging.warning(
        "Storage timeout: device=%s error=%s",
        device,
        exc
    )
```

A timeout does not automatically mean:

```text
Drive is defective
```

It means:

```text
The operation exceeded the configured timeout.
```

Root cause requires further investigation.

---

# 14. Retryable vs Non-Retryable Failures

Not every exception should be retried.

Example:

```text
StorageTimeoutError
        ↓
Potentially retryable

DeviceValidationError
        ↓
Usually not retryable

StorageConfigurationError
        ↓
Usually not retryable

LogParsingError
        ↓
Usually investigate parsing pipeline
```

Retry policy must be based on failure semantics.

---

# 15. Retry Pattern

Example:

```python
max_retries = 3

for attempt in range(max_retries):

    try:
        run_test(device)
        break

    except StorageTimeoutError as exc:
        logging.warning(
            "Timeout: device=%s attempt=%d",
            device,
            attempt + 1
        )
```

This provides bounded retries.

---

# 16. Why Bounded Retry?

Never blindly use:

```python
while True:
    try:
        run_test(device)

    except StorageTimeoutError:
        retry()
```

A persistent failure could create:

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
Retry forever
```

Use an explicit maximum.

---

# 17. Retry With Diagnostics

A better pattern:

```python
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

        collect_diagnostics(device)
```

Now every timeout can produce useful evidence.

---

# 18. Final Failure After Retries

If all attempts fail:

```python
else:
    logging.error(
        "Storage test failed after %d attempts: device=%s",
        max_retries,
        device
    )
```

The final result should explicitly indicate failure.

For example:

```text
FAIL
```

rather than silently continuing.

---

# 19. Storage Test Result Classification

A framework may use results such as:

```text
PASS
FAIL
RETRY
INVALID_CONFIGURATION
BLOCKED
ERROR
```

The exact result model depends on the framework.

The important concept is:

```text
Exception
    ↓
Failure classification
    ↓
Test result
```

---

# 20. Example Result Mapping

A conceptual mapping:

```text
DeviceValidationError
        ↓
INVALID_CONFIGURATION

StorageTimeoutError
        ↓
RETRY → FAIL if retries exhausted

StorageTestError
        ↓
FAIL

LogParsingError
        ↓
ERROR

Unexpected Exception
        ↓
ERROR
```

---

# 21. Logging Storage Test Lifecycle

A useful test should log:

```text
TEST_START
operation start
operation result
retry
failure
diagnostics
TEST_END
```

Example:

```python
logging.info(
    "TEST_START device=%s",
    device
)
```

Then:

```python
logging.info(
    "READ_PASS device=%s",
    device
)
```

and on failure:

```python
logging.error(
    "READ_ERROR device=%s",
    device
)
```

---

# 22. Include Operation Context

Bad:

```python
logging.error("Operation failed")
```

Better:

```python
logging.error(
    "Operation failed: device=%s operation=%s",
    device,
    operation
)
```

For storage troubleshooting, context matters.

---

# 23. Include Diagnostic Information

Example:

```text
device=/dev/sda
operation=READ
error=READ_ERROR
sector=182736
retry=3
```

This is much more useful than:

```text
READ failed
```

---

# 24. Exception Logging

Use:

```python
try:
    run_test(device)

except StorageTestError:
    logging.exception(
        "Storage test failed: device=%s",
        device
    )
    raise
```

This provides:

```text
Exception
+
Traceback
+
Device context
+
Propagation
```

---

# 25. Diagnostic Collection

When a storage failure occurs, collect useful evidence before the test environment changes.

Conceptually:

```python
except StorageTestError:
    logging.exception(
        "Storage test failed"
    )

    collect_diagnostics(device)

    raise
```

Diagnostics may include:

```text
Test logs
Device state
System logs
Transport information
Error counters
Command output
Relevant configuration
```

The exact diagnostics depend on the test environment.

---

# 26. Why Collect Diagnostics Before Cleanup?

Suppose a failed test leaves temporary state that disappears during cleanup.

If diagnostics are collected after everything is cleaned:

```text
Failure
 ↓
Cleanup
 ↓
State disappears
 ↓
Diagnostics
 ↓
Missing evidence
```

Better:

```text
Failure
 ↓
Capture diagnostics
 ↓
Cleanup
 ↓
Report
```

---

# 27. Cleanup

Cleanup should happen even when the test fails.

Example:

```python
try:
    run_test(device)

finally:
    cleanup(device)
```

This prevents failed tests from contaminating later tests.

---

# 28. Cleanup Can Also Fail

Cleanup is not automatically successful.

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

The framework should define how cleanup failure affects the final result.

---

# 29. Test State

A storage test may maintain state such as:

```text
Test started
Device prepared
I/O running
Retrying
Diagnostics collected
Cleanup complete
```

The framework should maintain enough state to determine what actions are still required.

Example:

```python
test_started = False

try:
    start_test(device)
    test_started = True

    run_test(device)

finally:

    if test_started:
        cleanup(device)
```

---

# 30. Why Track State?

Suppose setup fails:

```text
Test never started
```

There may be nothing to clean up.

But if setup succeeds:

```text
Test started
```

cleanup may be mandatory.

Therefore:

```text
Current state
    ↓
Required cleanup/recovery
```

---

# 31. Storage Error Flow

A complete flow:

```text
Configuration
     ↓
Validation
     ↓
Preparation
     ↓
Execution
     ↓
Failure?
  /       \
No        Yes
 |         |
PASS     Classify
           |
     ┌─────┼─────┐
     |     |     |
 Validation Timeout Test
     |     |     |
    FAIL Retry   FAIL
           |
       Diagnostics
           |
        Cleanup
           |
         Report
```

---

# 32. Device Not Found

Example:

```python
try:
    open(device)

except FileNotFoundError as exc:
    raise DeviceValidationError(
        f"Device not found: {device}"
    ) from exc
```

Important:

```text
Device not found
≠
Device hardware failure
```

It may be:

```text
Incorrect path
Device not enumerated
Device disconnected
Environment issue
```

Root cause requires investigation.

---

# 33. Permission Failure

Example:

```python
try:
    access_device(device)

except PermissionError as exc:
    raise DeviceValidationError(
        f"Permission denied: {device}"
    ) from exc
```

This is usually not solved by repeatedly retrying the same operation.

The environment/configuration must be investigated.

---

# 34. I/O Failure

Example:

```python
try:
    execute_read(device)

except OSError as exc:
    raise StorageTestError(
        f"I/O failure on {device}"
    ) from exc
```

The original `OSError` remains available as the cause.

---

# 35. Timeout Failure

Example:

```python
try:
    execute_read(device)

except TimeoutError as exc:
    raise StorageTimeoutError(
        f"READ timeout on {device}"
    ) from exc
```

This allows:

```python
except StorageTimeoutError:
    retry()
```

without losing the original cause.

---

# 36. Log Parsing Failure

Suppose the test completed, but the result parser cannot understand the log.

```python
try:
    result = parse_log(log)

except ValueError as exc:
    raise LogParsingError(
        "Unable to parse storage test log"
    ) from exc
```

Important distinction:

```text
Test execution may have succeeded.
Result processing failed.
```

Do not automatically mark this as a device failure.

---

# 37. Test Execution vs Result Processing

These are different stages.

```text
Test execution
       ↓
Did the device/test operation work?

Result processing
       ↓
Can the framework correctly interpret the result?
```

A parser failure does not necessarily mean the storage device failed.

---

# 38. Unexpected Exception

Example:

```python
try:
    run_test(device)

except StorageError:
    handle_storage_failure()

except Exception:
    logging.exception(
        "Unexpected framework failure"
    )
    raise
```

This distinguishes:

```text
Known storage failure
```

from:

```text
Unexpected programming/framework failure
```

---

# 39. Why Unexpected Exceptions Should Remain Visible

Suppose there is a programming bug:

```python
result = results[index_that_does_not_exist]
```

This may produce:

```text
IndexError
```

Do not automatically classify it as:

```text
Storage device failure
```

It may be a framework bug.

---

# 40. Storage Automation Layers

A useful architecture:

```text
                    Test Framework
                          |
              +-----------+-----------+
              |                       |
         Validation               Execution
              |                       |
      DeviceValidationError     StorageTestError
                                      |
                              StorageTimeoutError
              |
              +-----------+
                          |
                    Result Parser
                          |
                    LogParsingError
```

Each layer has its own responsibility.

---

# 41. Exception Propagation Between Layers

Example:

```text
Low-level I/O
      ↓
OSError
      ↓
Execution layer
      ↓
StorageTestError
      ↓
Test runner
      ↓
FAIL
```

The exception becomes more meaningful as it moves upward while preserving the original cause.

---

# 42. Do Not Destroy Original Information

Bad:

```python
except OSError:
    raise StorageTestError("Failed")
```

Better:

```python
except OSError as exc:
    raise StorageTestError(
        f"I/O failed on {device}"
    ) from exc
```

The second version preserves the causal chain.

---

# 43. Storage Timeout Recovery

A conceptual recovery sequence:

```text
Timeout
  ↓
Log
  ↓
Capture diagnostics
  ↓
Determine whether retry is allowed
  ↓
Retry
  ↓
Success?
 /     \
Yes     No
 |       |
PASS    Continue retry
          |
       Retry limit
          ↓
         FAIL
```

---

# 44. Persistent Failure

Suppose:

```text
Attempt 1 → timeout
Attempt 2 → timeout
Attempt 3 → timeout
```

The framework should not continue indefinitely.

Final state:

```text
FAIL
```

with evidence:

```text
attempts=3
device=/dev/sda
operation=READ
failure=TIMEOUT
```

---

# 45. Retry Does Not Mean Ignore

Incorrect mindset:

```text
Timeout
 ↓
Retry
 ↓
Forget first failure
```

Correct mindset:

```text
Timeout
 ↓
Record failure
 ↓
Collect evidence
 ↓
Retry
 ↓
Record result
```

Every attempt is part of the diagnostic history.

---

# 46. Example — Complete Retry Pattern

```python
max_retries = 3

for attempt in range(1, max_retries + 1):

    try:

        logging.info(
            "Test attempt=%d device=%s",
            attempt,
            device
        )

        run_test(device)

        logging.info(
            "Test PASS device=%s attempt=%d",
            device,
            attempt
        )

        break

    except StorageTimeoutError:

        logging.exception(
            "Test timeout device=%s attempt=%d",
            device,
            attempt
        )

        collect_diagnostics(device)

else:

    logging.error(
        "Test FAILED after %d attempts device=%s",
        max_retries,
        device
    )
```

---

# 47. Important `for-else` Behavior

The `else` executes only if:

```text
The loop completes without break.
```

In the previous example:

```python
break
```

means:

```text
Test succeeded
```

so the `else` is skipped.

If every attempt times out:

```text
No break
 ↓
for-else executes
 ↓
Final failure
```

---

# 48. Cleanup After Retry

A framework may need cleanup:

```python
try:
    run_test(device)

finally:
    cleanup(device)
```

But if each retry requires specific reset operations, the framework may need:

```text
Attempt
 ↓
Failure
 ↓
Reset test state
 ↓
Next attempt
```

The exact cleanup/reset policy depends on the test.

---

# 49. Test Environment Contamination

A failed test can leave:

```text
Processes
Temporary files
Locks
Outstanding I/O
Changed device state
Changed configuration
```

If not cleaned:

```text
Test 1 fails
    ↓
State remains
    ↓
Test 2 starts
    ↓
Test 2 fails
```

Now the second failure may be a consequence of the first.

This is why cleanup matters.

---

# 50. Failure Evidence Preservation

For every significant failure, think:

```text
What evidence will disappear if I continue?
```

Examples:

```text
Current device state
Current process state
Current logs
Current counters
Current command output
```

Collect important evidence before destructive cleanup when appropriate.

---

# 51. Root Cause Analysis

Exception handling is not the same as root cause analysis.

Example:

```text
Observed:
StorageTimeoutError
```

Possible causes:

```text
Device busy
Transport issue
Controller problem
Queue congestion
System overload
Firmware behavior
Configuration
Hardware failure
```

Therefore:

```text
Exception
    ↓
Evidence collection
    ↓
Correlation
    ↓
Hypothesis
    ↓
Verification
    ↓
Root cause
```

---

# 52. Storage Troubleshooting Example

Suppose:

```text
2026-08-11 09:10:04 [ERROR]
device=/dev/sda
operation=READ
error=READ ERROR
sector=182736
```

The framework should preserve:

```text
Timestamp
Device
Operation
Error
Sector
Retry count
Test phase
```

Then correlate with additional system evidence.

---

# 53. Exception Handling and Test Reporting

A test report should distinguish:

```text
PASS
FAIL
INVALID
ERROR
```

For example:

```text
Device validation failed
→ INVALID

Storage READ operation failed
→ FAIL

Framework crashed unexpectedly
→ ERROR

Storage test completed successfully
→ PASS
```

The exact categories depend on the framework's result model.

---

# 54. Do Not Misclassify Framework Failures

Consider:

```text
Log parser crashes with IndexError
```

That does not automatically mean:

```text
Drive failed.
```

It may mean:

```text
Automation framework defect
```

Correct classification is critical.

---

# 55. Failure Ownership

Ask:

```text
Who owns this failure?
```

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

Exception type alone may not determine ownership.

Evidence is required.

---

# 56. Error Handling Decision Matrix

A conceptual model:

| Failure                        | Typical Action             |
| ------------------------------ | -------------------------- |
| Invalid configuration          | Stop / report              |
| Invalid device path            | Stop / report              |
| Permission problem             | Stop / fix environment     |
| Timeout                        | Diagnose / possibly retry  |
| Transient I/O failure          | Diagnose / possibly retry  |
| Persistent I/O failure         | Fail test                  |
| Log parsing failure            | Report processing error    |
| Unexpected framework exception | Log + investigate          |
| Cleanup failure                | Log + apply cleanup policy |

This is a design example, not a universal policy.

---

# 57. Complete Enterprise Flow

```text
                TEST REQUEST
                     |
                     ↓
              LOAD CONFIG
                     |
              Validation
                     |
          ┌──────────┴──────────┐
          |                     |
       INVALID                VALID
          |                     |
          ↓                     ↓
        STOP              Device Validation
                                |
                       ┌────────┴────────┐
                       |                 |
                    INVALID            VALID
                       |                 |
                       ↓                 ↓
                     STOP          Test Preparation
                                         |
                                         ↓
                                  Test Execution
                                         |
                              ┌──────────┴─────────┐
                              |                    |
                           SUCCESS              FAILURE
                              |                    |
                              |              Classify exception
                              |                    |
                              |          ┌─────────┼─────────┐
                              |          |         |         |
                              |       Timeout   TestError  Other
                              |          |         |         |
                              |        Retry?    FAIL     ERROR
                              |          |
                              |      Diagnostics
                              |          |
                              |       Retry
                              |          |
                              └──────────┴─────────────┐
                                                       ↓
                                                Result Parsing
                                                       |
                                                       ↓
                                                  Reporting
                                                       |
                                                       ↓
                                                   Cleanup
```

---

# 58. Complete Example

```python
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


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


def validate_config(config):

    if "device" not in config:
        raise StorageConfigurationError(
            "Device missing from configuration"
        )


def validate_device(device):

    if not isinstance(device, str):
        raise DeviceValidationError(
            "Device must be a string"
        )

    if not device.startswith("/dev/"):
        raise DeviceValidationError(
            f"Invalid device: {device}"
        )


def execute_test(device):

    try:
        perform_io_test(device)

    except TimeoutError as exc:

        raise StorageTimeoutError(
            f"Storage test timed out: {device}"
        ) from exc

    except OSError as exc:

        raise StorageTestError(
            f"I/O failure on {device}"
        ) from exc


def run_storage_test(config):

    device = config["device"]

    validate_config(config)
    validate_device(device)

    logging.info(
        "TEST_START device=%s",
        device
    )

    try:

        execute_test(device)

    except StorageTimeoutError:

        logging.exception(
            "TEST_TIMEOUT device=%s",
            device
        )

        collect_diagnostics(device)

        raise

    except StorageTestError:

        logging.exception(
            "TEST_FAILURE device=%s",
            device
        )

        collect_diagnostics(device)

        raise

    else:

        logging.info(
            "TEST_PASS device=%s",
            device
        )

    finally:

        cleanup(device)

        logging.info(
            "TEST_END device=%s",
            device
        )
```

---

# 59. Analyze the Flow

Configuration:

```text
validate_config()
```

Device:

```text
validate_device()
```

Execution:

```text
execute_test()
```

Timeout:

```text
TimeoutError
    ↓
StorageTimeoutError
```

I/O failure:

```text
OSError
    ↓
StorageTestError
```

Failure:

```text
log
 ↓
diagnostics
 ↓
raise
```

Success:

```text
else
 ↓
PASS
```

Always:

```text
finally
 ↓
cleanup
 ↓
TEST_END
```

---

# 60. What This Architecture Achieves

It provides:

```text
Validation
Classification
Exception translation
Exception chaining
Logging
Diagnostics
Propagation
Cleanup
Explicit results
```

Most importantly, it creates a predictable failure path.

---

# 61. Best Practices Summary

```text
1. Validate before execution.
2. Use meaningful exception classes.
3. Keep exception boundaries narrow.
4. Catch specific exceptions.
5. Order handlers from specific to general.
6. Retry only appropriate failures.
7. Bound retry attempts.
8. Preserve the original exception.
9. Use exception chaining when translating errors.
10. Log useful context.
11. Collect diagnostics.
12. Always perform required cleanup.
13. Do not swallow exceptions.
14. Do not broadly catch BaseException.
15. Distinguish test failure from framework failure.
16. Do not assume an exception is the root cause.
17. Preserve failure evidence.
18. Make final results explicit.
19. Test failure paths.
20. Verify recovery.
```

---

# 62. Interview Questions

## Q1. How would you design exception handling for a storage test framework?

A strong answer:

```text
Validate configuration and devices first.
Use domain-specific exceptions.
Classify failures by type.
Retry only explicitly retryable failures.
Collect diagnostics on significant failures.
Use logging with device/operation context.
Preserve original causes through exception chaining.
Guarantee cleanup.
Propagate failures that cannot be handled.
Convert the final state into an explicit test result.
```

---

## Q2. Should every storage timeout cause a test failure immediately?

Not necessarily.

A timeout may be retryable depending on the test policy.

A reasonable flow is:

```text
Timeout
 ↓
Log
 ↓
Collect diagnostics
 ↓
Retry if policy allows
 ↓
Retry exhausted
 ↓
FAIL
```

---

## Q3. Why should device validation happen before test execution?

To prevent invalid inputs from causing unnecessary test execution and misleading failures.

---

## Q4. Why is `StorageTimeoutError` better than simply raising `TimeoutError`?

It gives the storage framework a domain-specific category that can be associated with a retry and diagnostic policy while preserving the original `TimeoutError` as the cause.

---

## Q5. Why should a log parsing failure not automatically mean the drive failed?

Because the test may have executed successfully; only the result-processing stage failed.

---

## Q6. Why should unexpected framework exceptions be distinguished from storage failures?

Because a framework bug should not be incorrectly reported as a device failure.

---

# 63. Storage Troubleshooting Questions

## Q7. A READ command times out. What would you investigate?

Do not immediately conclude hardware failure.

Investigate:

```text
Device state
Transport/link state
Controller state
I/O queue
System load
Timeout configuration
Previous errors
Retry behavior
Kernel/system evidence
Device health information
```

The exact investigation depends on the environment.

---

## Q8. A test fails, but cleanup also fails. What should happen?

The framework should:

```text
Preserve the original test failure
        +
Record cleanup failure
        +
Apply defined cleanup policy
        +
Report both pieces of evidence
```

The exact precedence depends on the framework's result model.

---

## Q9. Why collect diagnostics before cleanup?

Because cleanup can change or destroy state that may be required to determine the root cause.

---

# 64. Knowledge-Gap Checklist

Before considering this topic complete:

```text
[ ] Storage exception hierarchy
[ ] Configuration errors
[ ] Device validation errors
[ ] Test execution errors
[ ] Timeout errors
[ ] Log parsing errors
[ ] Exception translation
[ ] Exception chaining
[ ] Retry classification
[ ] Bounded retry
[ ] Diagnostic collection
[ ] Cleanup
[ ] Test state
[ ] Result classification
[ ] Failure ownership
[ ] Test failure vs framework failure
[ ] Logging
[ ] Propagation
[ ] Root Cause Analysis
[ ] Failure evidence
[ ] Storage troubleshooting flow
```

---

# 65. Final Mental Model

The complete Storage Automation error-handling model:

```text
                INPUT
                  |
                  ↓
            VALIDATION
                  |
             valid?
             /     \
           No       Yes
           |         |
        INVALID    EXECUTE
                     |
                 success?
                 /     \
               Yes      No
                |        |
               PASS    CLASSIFY
                         |
              ┌──────────┼──────────┐
              |          |          |
           Timeout     Test       Unexpected
              |         Error         |
           Retry?        |            |
              |         FAIL       ERROR
              |
        Diagnostics
              |
            Retry
              |
         Exhausted?
          /      \
        No        Yes
        |          |
      Retry       FAIL
          \       /
           \     /
            ↓   ↓
          REPORT
             |
             ↓
          CLEANUP
             |
             ↓
        FINAL RESULT
```

---

# 66. Final Engineering Rule

In Storage Test Automation:

```text
Do not treat every exception as a device failure.
```

Instead:

```text
Detect
  ↓
Classify
  ↓
Preserve evidence
  ↓
Determine ownership
  ↓
Recover / Retry / Fail
  ↓
Cleanup
  ↓
Report
  ↓
Verify
```

The exception tells you **what the software observed**.

The evidence and investigation tell you **why it happened**.

The final engineering goal is:

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


