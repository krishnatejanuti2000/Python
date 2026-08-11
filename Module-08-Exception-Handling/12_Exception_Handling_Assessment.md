# 12 — Exception Handling Assessment

## Objective

This assessment validates practical knowledge of Python Exception Handling
and its application to Storage Test Automation.

The assessment covers:

- try
- except
- else
- finally
- raise
- Exception hierarchy
- Custom exceptions
- Exception chaining
- Exception propagation
- Logging
- Retry logic
- Validation
- Cleanup
- Storage automation error handling
- Failure classification
- Root Cause Analysis

---

# Assessment Rules

1. Solve every question independently first.
2. Do not look at the reference solutions before attempting the questions.
3. Write executable Python wherever requested.
4. Use specific exceptions.
5. Avoid unnecessary `except Exception`.
6. Never use bare `except:` unnecessarily.
7. Do not silently swallow exceptions.
8. Retry only failures that are logically retryable.
9. Always bound retry attempts.
10. Preserve the original exception when translating exceptions.
11. Preserve useful diagnostic information.
12. Treat storage failures and framework failures separately.

---

# SECTION 1 — BASIC EXCEPTION HANDLING

## Q1 — Safe Integer Conversion

Write:

```python
def convert_to_integer(value):
    pass
````

Requirements:

* Convert `value` to an integer.
* Handle invalid numeric input.
* Return the integer when successful.
* Return `None` when conversion fails.

### Example

```text
Input:
"100"

Output:
100
```

```text
Input:
"abc"

Output:
None
```

---

## Q1 — Reference Solution

```python
def convert_to_integer(value):

    try:
        return int(value)

    except ValueError:
        return None
```

### Test

```python
print(convert_to_integer("100"))
print(convert_to_integer("abc"))
```

### Output

```text
100
None
```

### Key Concept

Only `ValueError` is expected from invalid integer conversion.

---

# Q2 — Division

Write:

```python
def divide(a, b):
    pass
```

Requirements:

* Perform `a / b`.
* Handle division by zero.
* Handle invalid numeric values.
* Return the result when successful.

---

## Q2 — Reference Solution

```python
def divide(a, b):

    try:
        return a / b

    except ZeroDivisionError:
        return None

    except TypeError:
        return None
```

### Test

```python
print(divide(10, 2))
print(divide(10, 0))
print(divide(10, "x"))
```

### Output

```text
5.0
None
None
```

### Key Concept

Different failure conditions should have specific exception handlers.

---

# Q3 — Multiple Exceptions

Write a program that:

1. Reads a value from the user.
2. Converts it to an integer.
3. Divides `100` by that value.

Handle:

```text
ValueError
ZeroDivisionError
```

using separate handlers.

---

## Q3 — Reference Solution

```python
value = input("Enter a number: ")

try:

    number = int(value)
    result = 100 / number

    print("Result:", result)

except ValueError:
    print("Invalid integer")

except ZeroDivisionError:
    print("Zero is not allowed")
```

### Example

```text
Enter a number: 10
Result: 10.0
```

---

# SECTION 2 — ELSE AND FINALLY

# Q4 — Successful Processing

Write a program using:

```text
try
except
else
finally
```

Requirements:

* Convert user input to an integer.
* Print an error if conversion fails.
* Print `"Processing successful"` only when conversion succeeds.
* Always print `"Program completed"`.

---

## Q4 — Reference Solution

```python
value = input("Enter a number: ")

try:

    number = int(value)

except ValueError:

    print("Invalid integer")

else:

    print("Processing successful")
    print("Value:", number)

finally:

    print("Program completed")
```

### Flow

Successful input:

```text
try
 ↓
else
 ↓
finally
```

Invalid input:

```text
try
 ↓
except
 ↓
finally
```

---

# Q5 — File Handling

Write a program that:

1. Opens `storage.log`.
2. Reads its contents.
3. Handles `FileNotFoundError`.
4. Uses `else` for successful reading.
5. Uses `finally` to report that the operation completed.

---

## Q5 — Reference Solution

```python
try:

    file = open("storage.log", "r")
    data = file.read()

except FileNotFoundError:

    print("storage.log not found")

else:

    print("File read successfully")
    print(data)

finally:

    print("File operation completed")
```

### Better Resource-Management Version

For production Python, prefer:

```python
try:

    with open("storage.log", "r") as file:
        data = file.read()

except FileNotFoundError:

    print("storage.log not found")

else:

    print("File read successfully")
    print(data)

finally:

    print("File operation completed")
```

### Key Concept

`with` is preferred for resources that support context management.

---

# SECTION 3 — RAISE

# Q6 — Capacity Validation

Write:

```python
def validate_capacity(capacity):
    pass
```

Requirements:

* `capacity` must be an integer.
* Capacity must be greater than zero.
* Raise `TypeError` for the wrong type.
* Raise `ValueError` for an invalid value.

---

## Q6 — Reference Solution

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

### Tests

```python
print(validate_capacity(500))
```

Output:

```text
True
```

```python
validate_capacity(-10)
```

Raises:

```text
ValueError
```

```python
validate_capacity("500")
```

Raises:

```text
TypeError
```

---

# Q7 — Device Validation

Write:

```python
def validate_device(device):
    pass
```

Requirements:

* Device must be a string.
* Device must begin with `/dev/`.
* Raise an appropriate exception when validation fails.

Valid examples:

```text
/dev/sda
/dev/nvme0n1
```

---

## Q7 — Reference Solution

```python
def validate_device(device):

    if not isinstance(device, str):
        raise TypeError(
            "Device must be a string"
        )

    if not device.startswith("/dev/"):
        raise ValueError(
            f"Invalid device path: {device}"
        )

    return True
```

### Important

This validates the basic device-path requirement.

It does not prove that the physical device actually exists.

---

# SECTION 4 — CUSTOM EXCEPTIONS

# Q8 — Create a Storage Exception Hierarchy

Create:

```text
StorageError
    |
    +-- DeviceValidationError
    |
    +-- StorageTestError
           |
           +-- StorageTimeoutError
```

Then demonstrate raising and catching:

```text
StorageTimeoutError
```

---

## Q8 — Reference Solution

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

### Raising and Catching

```python
try:

    raise StorageTimeoutError(
        "Storage test timed out"
    )

except StorageTimeoutError as exc:

    print("Timeout:", exc)
```

### Hierarchy

```text
Exception
    |
    +-- StorageError
          |
          +-- DeviceValidationError
          |
          +-- StorageTestError
                |
                +-- StorageTimeoutError
```

---

# Q9 — Custom Storage Validation

Create:

```python
class DeviceValidationError(StorageError):
    pass
```

Then write:

```python
def validate_device(device):
    pass
```

Raise `DeviceValidationError` when the device is invalid.

Test:

```text
/dev/sda
/dev/nvme0n1
invalid_device
```

---

## Q9 — Reference Solution

```python
class StorageError(Exception):
    pass


class DeviceValidationError(StorageError):
    pass


def validate_device(device):

    if not isinstance(device, str):
        raise DeviceValidationError(
            "Device must be a string"
        )

    if not device.startswith("/dev/"):
        raise DeviceValidationError(
            f"Invalid device: {device}"
        )

    return True
```

### Test

```python
devices = [
    "/dev/sda",
    "/dev/nvme0n1",
    "invalid_device"
]

for device in devices:

    try:

        validate_device(device)
        print(device, "VALID")

    except DeviceValidationError as exc:

        print(device, "INVALID:", exc)
```

---

# SECTION 5 — EXCEPTION CHAINING

# Q10 — Convert Low-Level Exception

Write code where:

```text
ValueError
```

is converted into:

```text
LogParsingError
```

using:

```python
raise ... from exc
```

The original exception must remain the cause.

---

## Q10 — Reference Solution

```python
class LogParsingError(Exception):
    pass


try:

    value = int("ABC")

except ValueError as exc:

    raise LogParsingError(
        "Invalid numeric value in storage log"
    ) from exc
```

### Exception Chain

```text
ValueError
    ↓
original cause
    ↓
LogParsingError
```

The original `ValueError` is preserved.

---

# Q11 — Storage Timeout Translation

Simulate:

```text
TimeoutError
```

and convert it into:

```text
StorageTimeoutError
```

Requirements:

* Preserve the original exception.
* Include the device name.

---

## Q11 — Reference Solution

```python
class StorageError(Exception):
    pass


class StorageTestError(StorageError):
    pass


class StorageTimeoutError(StorageTestError):
    pass


device = "/dev/sda"

try:

    raise TimeoutError(
        "READ operation timed out"
    )

except TimeoutError as exc:

    raise StorageTimeoutError(
        f"Storage test timed out: {device}"
    ) from exc
```

The original exception remains the cause.

---

# SECTION 6 — LOGGING

# Q12 — Basic Storage Logging

Configure Python logging with:

```text
timestamp
log level
message
```

Then log:

```text
TEST_START
READ PASS
WRITE PASS
TEST_END
```

for:

```text
/dev/sda
```

---

## Q12 — Reference Solution

```python
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


device = "/dev/sda"

logging.info(
    "TEST_START device=%s",
    device
)

logging.info(
    "READ PASS device=%s",
    device
)

logging.info(
    "WRITE PASS device=%s",
    device
)

logging.info(
    "TEST_END device=%s",
    device
)
```

---

# Q13 — Exception Logging

Write code that uses:

```python
logging.exception()
```

to record a storage failure and traceback.

---

## Q13 — Reference Solution

```python
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


try:

    raise RuntimeError(
        "Storage test failed"
    )

except RuntimeError:

    logging.exception(
        "Storage test failure"
    )
```

### Key Concept

`logging.exception()` is normally used inside an `except` block and includes traceback information.

---

# SECTION 7 — RETRY LOGIC

# Q14 — Bounded Timeout Retry

Write a program that:

* Executes a storage test.
* Catches `StorageTimeoutError`.
* Retries up to 3 times.
* Logs every attempt.
* Stops immediately when successful.
* Reports final failure if all attempts fail.

---

## Q14 — Reference Solution

```python
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


class StorageTimeoutError(Exception):
    pass


attempts_before_success = 2
max_retries = 3


for attempt in range(1, max_retries + 1):

    try:

        logging.info(
            "TEST_ATTEMPT attempt=%d",
            attempt
        )

        if attempt <= attempts_before_success:
            raise StorageTimeoutError(
                "Storage test timed out"
            )

        logging.info(
            "TEST_PASS attempt=%d",
            attempt
        )

        break

    except StorageTimeoutError:

        logging.exception(
            "TEST_TIMEOUT attempt=%d",
            attempt
        )

else:

    logging.error(
        "TEST_FAILED after %d attempts",
        max_retries
    )
```

### Important

The `for ... else` block executes only when the loop completes without `break`.

---

# Q15 — Retry Classification

Classify:

```text
DeviceValidationError
StorageTimeoutError
StorageTestError
LogParsingError
```

Determine:

```text
Retry?
Do not retry?
Investigate?
```

---

## Q15 — Reference Answer

### DeviceValidationError

```text
Normally: Do not retry
```

Reason:

The configuration/input must usually be corrected.

---

### StorageTimeoutError

```text
Potentially retryable
```

Reason:

Timeouts may be transient.

The actual retry policy must depend on the test.

---

### StorageTestError

```text
Depends on the specific failure
```

Some storage test errors may be transient.

Others may represent persistent failures.

---

### LogParsingError

```text
Normally investigate
```

Reason:

The test may have succeeded but result processing failed.

It should not automatically be treated as a device failure.

---

# SECTION 8 — CLEANUP

# Q16 — Guaranteed Cleanup

Write:

```python
def run_test(device):
    pass
```

Requirements:

* Start the test.
* Execute the test.
* Handle a possible failure.
* Always execute cleanup.

---

## Q16 — Reference Solution

```python
def run_test(device):

    try:

        print("Starting test:", device)

        execute_test(device)

    except Exception as exc:

        print("Test failed:", exc)

    finally:

        print("Cleanup:", device)
```

### Key Concept

`finally` executes regardless of whether the `try` block succeeds or fails.

In production code, the exception type should normally be narrowed rather than using a broad handler unnecessarily.

---

# Q17 — Conditional Cleanup

Use:

```python
test_started = False
```

Requirements:

* Set it to `True` only after the test starts.
* Cleanup only if the test actually started.
* Cleanup must still happen if execution fails.

---

## Q17 — Reference Solution

```python
def run_test(device):

    test_started = False

    try:

        start_test(device)

        test_started = True

        execute_test(device)

    except StorageTestError as exc:

        print("Test failed:", exc)

    finally:

        if test_started:
            cleanup(device)
```

### Flow

If startup fails:

```text
start_test()
   ↓
failure
   ↓
test_started remains False
   ↓
cleanup skipped
```

If startup succeeds:

```text
start_test()
   ↓
test_started = True
   ↓
execute
   ↓
cleanup
```

---

# SECTION 9 — STORAGE LOG FAILURE ANALYSIS

Given:

```text
2026-08-11 09:10:01 [INFO] /dev/sda TEST_START
2026-08-11 09:10:02 [INFO] /dev/sda READ PASS
2026-08-11 09:10:03 [ERROR] /dev/sda READ ERROR sector=182736
2026-08-11 09:10:04 [WARN] /dev/sda RETRY attempt=1
2026-08-11 09:10:05 [ERROR] /dev/sda READ TIMEOUT
2026-08-11 09:10:06 [INFO] /dev/sda TEST_END
```

# Q18 — Analyze the Failure

Answer:

1. Which operation failed?
2. What was the first observed failure?
3. Was a retry attempted?
4. What happened during the retry?
5. Does the log prove hardware failure?
6. What additional evidence would you collect?
7. What should the final automation result be?

---

## Q18 — Reference Answer

### 1. Which operation failed?

```text
READ
```

---

### 2. First observed failure

```text
READ ERROR
sector=182736
```

at:

```text
09:10:03
```

---

### 3. Was a retry attempted?

Yes.

```text
RETRY attempt=1
```

---

### 4. What happened during retry?

The retry resulted in:

```text
READ TIMEOUT
```

---

### 5. Does this log prove hardware failure?

No.

It proves that the READ operation encountered errors and subsequently timed out.

It does not by itself prove the physical device is defective.

---

### 6. Additional evidence

Depending on the environment, investigate:

```text
Device state
Kernel logs
Transport/link state
Controller state
I/O queue
Device health information
Error counters
Previous failures
System load
Test configuration
```

---

### 7. Final automation result

A reasonable result is:

```text
FAIL
```

because the operation did not successfully complete according to the shown test sequence.

The failure should retain all diagnostic evidence.

---

# SECTION 10 — DEBUGGING

# Q19 — Exception vs Root Cause

Suppose:

```text
StorageTimeoutError:
READ operation timed out
```

Explain why this does not automatically prove:

```text
/dev/sda is defective
```

---

## Q19 — Reference Answer

`StorageTimeoutError` describes an observed failure condition.

It does not automatically identify the underlying cause.

Possible investigation areas include:

```text
1. Device state
2. Transport/link state
3. Controller state
4. I/O queue
5. System load
6. Timeout configuration
7. Previous errors
8. Retry behavior
9. Kernel/system evidence
10. Device health information
```

The engineering process is:

```text
Observed exception
       ↓
Collect evidence
       ↓
Correlate evidence
       ↓
Form hypothesis
       ↓
Verify hypothesis
       ↓
Determine root cause
```

---

# Q20 — Failure Classification

Classify:

### Scenario A

```text
Device path does not exist.
```

### Scenario B

```text
READ operation timed out.
```

### Scenario C

```text
Storage log parser crashes with IndexError.
```

### Scenario D

```text
Configuration does not contain a device.
```

### Scenario E

```text
Storage test completes successfully.
```

---

## Q20 — Reference Answer

| Scenario | Classification                        | Typical Action          | Retry?      | Result                |
| -------- | ------------------------------------- | ----------------------- | ----------- | --------------------- |
| A        | Device validation/environment failure | Investigate device/path | Usually no  | INVALID / ERROR       |
| B        | Storage timeout                       | Collect diagnostics     | Potentially | RETRY → FAIL          |
| C        | Framework/result-processing failure   | Investigate parser      | Usually no  | ERROR                 |
| D        | Configuration failure                 | Fix configuration       | No          | INVALID_CONFIGURATION |
| E        | Successful execution                  | Continue reporting      | No          | PASS                  |

The exact result categories depend on the framework design.

---

# SECTION 11 — ADVANCED PRACTICAL PROBLEM

# Q21 — Complete Storage Test Function

Implement:

```python
def run_storage_test(config):
    pass
```

Requirements:

### Configuration validation

```text
device must exist
```

### Device validation

```text
device must be a string
device must start with /dev/
```

### Execution

Call:

```python
execute_test(device)
```

### Exception handling

Handle:

```text
DeviceValidationError
StorageTimeoutError
StorageTestError
```

### Logging

Log:

```text
TEST_START
FAILURE
RETRY
PASS
TEST_END
```

### Diagnostics

Call:

```python
collect_diagnostics(device)
```

for important failures.

### Cleanup

Always call:

```python
cleanup(device)
```

when appropriate.

### Propagation

Unexpected exceptions must not be silently swallowed.

---

## Q21 — Reference Solution

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


def validate_device(device):

    if not isinstance(device, str):
        raise DeviceValidationError(
            "Device must be a string"
        )

    if not device.startswith("/dev/"):
        raise DeviceValidationError(
            f"Invalid device: {device}"
        )


def run_storage_test(config):

    if "device" not in config:
        raise StorageConfigurationError(
            "Device missing from configuration"
        )

    device = config["device"]

    validate_device(device)

    logging.info(
        "TEST_START device=%s",
        device
    )

    try:

        execute_test(device)

    except StorageTimeoutError:

        logging.exception(
            "FAILURE timeout device=%s",
            device
        )

        collect_diagnostics(device)

        raise

    except StorageTestError:

        logging.exception(
            "FAILURE storage test device=%s",
            device
        )

        collect_diagnostics(device)

        raise

    else:

        logging.info(
            "PASS device=%s",
            device
        )

    finally:

        cleanup(device)

        logging.info(
            "TEST_END device=%s",
            device
        )
```

### Important Design Points

The solution:

```text
Validates configuration
        ↓
Validates device
        ↓
Starts test
        ↓
Handles known storage failures
        ↓
Collects diagnostics
        ↓
Propagates known failures
        ↓
Reports success
        ↓
Always performs cleanup
```

Unexpected exceptions are not silently swallowed.

---

# SECTION 12 — DESIGN QUESTION

# Q22 — Design an Exception Strategy

You are designing a storage validation framework.

The framework contains:

```text
Device Validation
Test Execution
Result Parsing
Reporting
Cleanup
```

Design the exception hierarchy and explain:

```text
Exception classes
Inheritance
Retryable failures
Permanent failures
Handling location
Propagation
Diagnostics
Cleanup
```

---

## Q22 — Reference Answer

A reasonable hierarchy:

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

Possible strategy:

```text
StorageConfigurationError
→ stop
→ fix configuration
→ no blind retry

DeviceValidationError
→ stop
→ fix device/configuration
→ normally no retry

StorageTimeoutError
→ collect diagnostics
→ retry if policy permits
→ fail after retry limit

StorageTestError
→ classify based on specific failure
→ possibly retry
→ otherwise fail

LogParsingError
→ investigate result-processing pipeline
→ do not automatically blame device

Unexpected Exception
→ log traceback
→ preserve evidence
→ propagate/investigate
```

Cleanup:

```text
Test failure
    ↓
Collect diagnostics
    ↓
Cleanup
    ↓
Report final result
```

---

# SECTION 13 — DEBUGGING SCENARIO

# Q23 — Production Failure

A test framework reports:

```text
TEST FAILED
```

The only log is:

```text
ERROR Test failed
```

Explain:

1. Why the logging is insufficient.
2. What information should have been logged.
3. What traceback should be captured.
4. What storage-specific information should be collected.
5. How to reconstruct the timeline.
6. How to distinguish symptom from root cause.

---

## Q23 — Reference Answer

### 1. Why is the logging insufficient?

Because it does not identify:

```text
Device
Operation
Timestamp
Exception type
Failure reason
Test phase
Retry count
```

---

### 2. Information that should be logged

At minimum, where relevant:

```text
Timestamp
Severity
Device
Operation
Test phase
Status
Exception type
Error message
Retry count
Relevant configuration
```

---

### 3. Traceback

Use:

```python
logging.exception(
    "Storage test failed"
)
```

inside an exception handler.

This preserves traceback information.

---

### 4. Storage-specific evidence

Depending on the environment:

```text
Device state
Kernel/system logs
Transport state
Controller state
I/O information
Device health information
Error counters
Command output
Test logs
```

---

### 5. Reconstructing the timeline

Example:

```text
TEST_START
    ↓
READ_START
    ↓
READ_ERROR
    ↓
RETRY
    ↓
TIMEOUT
    ↓
DIAGNOSTICS
    ↓
CLEANUP
    ↓
TEST_END
```

Correlate timestamps across the available logs.

---

### 6. Symptom vs root cause

Example:

```text
Symptom:
READ timeout

Possible causes:
Transport issue
Controller problem
Device state
System load
Configuration
Hardware issue
```

The timeout is evidence.

It is not automatically the root cause.

---

# SECTION 14 — CODE REVIEW

# Q24 — Identify Problems

Review:

```python
try:

    device = config["device"]

    validate_device(device)

    run_test(device)

except:

    print("Test failed")

while True:

    try:
        run_test(device)
        break

    except Exception:
        pass
```

Identify as many problems as possible.

Then rewrite it using good practices.

---

## Q24 — Problems

### Problem 1 — Bare `except`

```python
except:
```

is too broad.

---

### Problem 2 — Exceptions are swallowed

```python
except Exception:
    pass
```

The failure disappears.

---

### Problem 3 — Infinite retry loop

```python
while True:
```

can retry forever.

---

### Problem 4 — No retry policy

Every exception is retried.

That is incorrect.

---

### Problem 5 — No logging

Only:

```python
print()
```

is used.

There is no structured diagnostic information.

---

### Problem 6 — No traceback

The original failure evidence is not preserved.

---

### Problem 7 — No exception classification

A validation failure, timeout, programming bug, and device failure are all treated the same.

---

### Problem 8 — Possible false result

A swallowed exception can allow the framework to continue incorrectly.

---

### Problem 9 — No cleanup

There is no guaranteed cleanup.

---

### Problem 10 — Test may execute twice

The first block calls:

```python
run_test(device)
```

and the retry loop may call it again without a clear result/recovery policy.

---

## Q24 — Reference Rewrite

```python
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


max_retries = 3


def run_storage_test(config):

    device = config["device"]

    validate_device(device)

    for attempt in range(1, max_retries + 1):

        try:

            logging.info(
                "TEST_START device=%s attempt=%d",
                device,
                attempt
            )

            run_test(device)

            logging.info(
                "TEST_PASS device=%s attempt=%d",
                device,
                attempt
            )

            return "PASS"

        except StorageTimeoutError:

            logging.exception(
                "TEST_TIMEOUT device=%s attempt=%d",
                device,
                attempt
            )

            collect_diagnostics(device)

        except StorageTestError:

            logging.exception(
                "TEST_FAILURE device=%s attempt=%d",
                device,
                attempt
            )

            collect_diagnostics(device)

            return "FAIL"

        finally:

            cleanup(device)

    logging.error(
        "TEST_FAILED_AFTER_RETRIES device=%s attempts=%d",
        device,
        max_retries
    )

    return "FAIL"
```

### Important

This is a reference architecture.

The exact retry and cleanup policy should be adapted to the actual storage test.

---

# SECTION 15 — SENIOR-LEVEL DESIGN

# Q25 — Enterprise Storage Failure Flow

Design the complete failure flow for:

```text
/dev/sda
READ operation
timeout
retry
timeout
retry
timeout
```

Explain:

1. Exception generated.
2. Exception classification.
3. Logging.
4. Diagnostic collection.
5. Retry decision.
6. Retry limit.
7. Final result.
8. Cleanup.
9. Evidence preservation.
10. Root Cause Analysis.

---

## Q25 — Reference Answer

### Step 1 — Exception

The low-level operation produces:

```text
TimeoutError
```

---

### Step 2 — Classification

The execution layer translates it into:

```text
StorageTimeoutError
```

while preserving the original cause:

```python
raise StorageTimeoutError(
    f"READ timeout on {device}"
) from exc
```

---

### Step 3 — Logging

Record:

```text
Timestamp
Device
Operation
Attempt
Exception
Failure message
```

Example:

```text
ERROR device=/dev/sda operation=READ attempt=1
error=StorageTimeoutError
```

---

### Step 4 — Diagnostics

Collect appropriate evidence:

```text
Device state
System/kernel evidence
Transport state
Controller state
Error information
Test logs
```

---

### Step 5 — Retry Decision

Determine whether:

```text
StorageTimeoutError
```

is retryable under the current test policy.

If yes:

```text
Retry
```

---

### Step 6 — Retry Limit

Example:

```text
Maximum attempts = 3
```

Execution:

```text
Attempt 1 → TIMEOUT
Attempt 2 → TIMEOUT
Attempt 3 → TIMEOUT
```

No fourth attempt.

---

### Step 7 — Final Result

All retry attempts failed.

Therefore:

```text
FINAL RESULT = FAIL
```

The failure evidence must be preserved.

---

### Step 8 — Cleanup

Perform required cleanup:

```text
Stop test processes
Release resources
Restore test state
Collect final state if required
```

---

### Step 9 — Evidence Preservation

Preserve:

```text
All three timeout events
Retry count
Timestamps
Device
Operation
Diagnostics
Original exception cause
Final failure
```

Do not retain only the final timeout.

---

### Step 10 — Root Cause Analysis

Do not immediately state:

```text
/dev/sda is defective
```

Instead investigate the evidence.

Possible areas:

```text
Device
Transport
Controller
I/O queue
System
Configuration
Firmware
Hardware
```

Then correlate and verify the evidence before assigning root cause.

---

# FINAL MODULE ASSESSMENT

## Core Knowledge

You should be able to explain:

```text
try
except
else
finally
raise
```

---

## Exception Design

You should be able to design:

```text
Built-in exceptions
Custom exceptions
Exception hierarchy
Exception chaining
Exception propagation
```

---

## Automation

You should be able to implement:

```text
Validation
Execution
Retry
Diagnostics
Cleanup
Result classification
```

---

## Troubleshooting

You should be able to distinguish:

```text
Symptom
Exception
Evidence
Failure
Root Cause
```

---

# FINAL ENGINEERING MODEL

```text
                    INPUT
                      |
                      ↓
                 VALIDATION
                      |
              ┌───────┴───────┐
              |               |
           INVALID           VALID
              |               |
              ↓               ↓
          STOP/REPORT      EXECUTION
                              |
                       ┌──────┴──────┐
                       |             |
                    SUCCESS        FAILURE
                       |             |
                       ↓             ↓
                     PASS        CLASSIFY
                                     |
                          ┌──────────┼──────────┐
                          |          |          |
                       Timeout     Test       Unexpected
                          |         Error        |
                          ↓          ↓           ↓
                       RETRY       FAIL      LOG + PROPAGATE
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
                         ↓     ↓
                         REPORT
                            |
                            ↓
                         CLEANUP
                            |
                            ↓
                       FINAL RESULT
                            |
                            ↓
                     ROOT CAUSE ANALYSIS
```

---

# FINAL RULE

Exception handling is not simply:

```text
try
except
```

For Storage Test Automation, the complete engineering approach is:

```text
DETECT
  ↓
CLASSIFY
  ↓
LOG
  ↓
COLLECT EVIDENCE
  ↓
DECIDE
  ↓
RECOVER / RETRY / FAIL
  ↓
CLEANUP
  ↓
PROPAGATE WHEN REQUIRED
  ↓
REPORT
  ↓
VERIFY
  ↓
ROOT CAUSE ANALYSIS
```

The exception tells us what happened.

The evidence tells us what was happening around it.

The investigation determines why it happened.

# END

