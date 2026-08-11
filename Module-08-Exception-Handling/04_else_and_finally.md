# 04 — else and finally

## Objective

Python provides `else` and `finally` as part of the exception-handling structure.

By the end of this document, you should understand:

- What `else` does
- When `else` executes
- When `else` does not execute
- Difference between `else` and code after `try/except`
- What `finally` does
- Why `finally` is used for cleanup
- `finally` with successful execution
- `finally` with exceptions
- `finally` with `return`
- `finally` with `break` and `continue`
- Resource cleanup
- Storage automation use cases
- Common mistakes

---

# 1. Complete Exception Handling Structure

Python allows:

```python
try:
    # risky operation

except SomeException:
    # handle exception

else:
    # execute when no exception occurred

finally:
    # execute regardless
````

All four parts are not mandatory.

Possible combinations include:

```text
try + except
try + finally
try + except + else
try + except + finally
try + except + else + finally
```

---

# 2. What Is `else`?

The `else` block executes **only when the `try` block completes without raising an exception**.

Example:

```python
try:
    value = int("100")

except ValueError:
    print("Invalid value")

else:
    print("Conversion successful")
```

Output:

```text
Conversion successful
```

Flow:

```text
try
 ↓
No exception
 ↓
skip except
 ↓
execute else
```

---

# 3. `else` When an Exception Occurs

```python
try:
    value = int("abc")

except ValueError:
    print("Invalid value")

else:
    print("Conversion successful")
```

Output:

```text
Invalid value
```

The `else` block does not execute.

Flow:

```text
try
 ↓
ValueError
 ↓
except executes
 ↓
else skipped
```

---

# 4. Basic Rule for `else`

Remember:

```text
try succeeds
    ↓
else executes

try fails
    ↓
matching except executes
    ↓
else does NOT execute
```

Therefore:

```text
else = successful try path
```

---

# 5. Why Not Just Put Code After `try/except`?

Consider:

```python
try:
    value = int(user_input)

except ValueError:
    print("Invalid input")

print("Processing value")
```

The final statement executes after the `try/except` structure regardless of whether the exception occurred.

That may not be what we want.

Instead:

```python
try:
    value = int(user_input)

except ValueError:
    print("Invalid input")

else:
    print("Processing value")
```

Now:

```text
Successful conversion
    ↓
Processing value

Failed conversion
    ↓
Processing value is skipped
```

---

# 6. `else` Defines the Success Path

This is a useful mental model:

```text
try
 ↓
Attempt operation
 ↓
 ┌───────────────┐
 │               │
Success        Failure
 │               │
 ↓               ↓
else           except
```

The `else` block is therefore useful for code that should execute only after the risky operation succeeded.

---

# 7. Example — File Reading

```python
try:
    with open("storage.log", "r") as file:
        data = file.read()

except FileNotFoundError:
    print("Log file does not exist")

else:
    print("Log loaded successfully")
```

If the file exists:

```text
Log loaded successfully
```

If it does not:

```text
Log file does not exist
```

---

# 8. Example — Parsing After Successful File Read

```python
try:
    with open("storage.log", "r") as file:
        data = file.read()

except FileNotFoundError:
    print("Log file missing")

else:
    print("Log loaded")
    print("Parsing log...")
```

The parsing step belongs to the successful path.

---

# 9. Keep the `try` Focused

A good design is:

```python
try:
    with open("storage.log", "r") as file:
        data = file.read()

except FileNotFoundError:
    print("Log missing")

else:
    process_log(data)
```

The `try` handles the operation whose failure we understand.

The `else` handles the successful path.

---

# 10. What Is `finally`?

`finally` is a block that is intended to execute regardless of whether the `try` block succeeds or raises an exception.

Example:

```python
try:
    print("Running operation")

finally:
    print("Cleanup")
```

Output:

```text
Running operation
Cleanup
```

---

# 11. `finally` After an Exception

```python
try:
    result = 10 / 0

except ZeroDivisionError:
    print("Division failed")

finally:
    print("Cleanup")
```

Output:

```text
Division failed
Cleanup
```

The `finally` block still executes.

---

# 12. `finally` Without `except`

This is valid:

```python
try:
    operation()

finally:
    cleanup()
```

If `operation()` succeeds:

```text
operation
 ↓
cleanup
```

If `operation()` raises an exception:

```text
operation
 ↓
exception
 ↓
cleanup
 ↓
exception continues propagating
```

This pattern is useful when cleanup must happen but the current code does not want to handle the exception.

---

# 13. `try + finally`

Example:

```python
try:
    file = open("storage.log", "r")
    data = file.read()

finally:
    file.close()
```

The `finally` block ensures the file is closed.

However, modern Python usually prefers:

```python
with open("storage.log", "r") as file:
    data = file.read()
```

because the context manager handles cleanup automatically.

---

# 14. `finally` and Resource Cleanup

Typical cleanup operations include:

```text
Close file
Release connection
Release lock
Delete temporary file
Stop test process
Release device resource
Disconnect session
Reset temporary state
```

This is why `finally` is important in automation.

---

# 15. Complete Structure

Example:

```python
try:
    value = int(user_input)

except ValueError:
    print("Invalid input")

else:
    print("Input accepted")

finally:
    print("Execution finished")
```

If input is valid:

```text
Input accepted
Execution finished
```

If input is invalid:

```text
Invalid input
Execution finished
```

The `finally` block executes in both normal paths.

---

# 16. Execution Flow

Successful case:

```text
try
 ↓
success
 ↓
else
 ↓
finally
 ↓
continue
```

Failure case:

```text
try
 ↓
exception
 ↓
except
 ↓
finally
 ↓
continue
```

---

# 17. `finally` Does Not Mean "Handle the Error"

This is important.

`except` handles an exception.

`finally` performs code that should run during cleanup/finalization.

Therefore:

```text
except
    ↓
Handle failure

finally
    ↓
Cleanup / final action
```

Do not confuse them.

---

# 18. Storage Test Example

Imagine:

```python
test_running = False

try:
    test_running = True
    run_storage_test("/dev/sda")

except TimeoutError:
    print("Storage test timed out")

finally:
    test_running = False
    print("Test state cleaned up")
```

If the test succeeds:

```text
Test state cleaned up
```

If the test times out:

```text
Storage test timed out
Test state cleaned up
```

The cleanup happens in both cases.

---

# 19. Cleanup After a Storage Test

A realistic automation flow may look like:

```text
Start test
   ↓
Run storage operation
   ↓
SUCCESS / FAILURE
   ↓
finally
   ↓
Stop background process
Release resources
Collect final diagnostics
Reset temporary state
```

This prevents failed tests from leaving the environment in a bad state.

---

# 20. `finally` With `return`

This is an important advanced behavior.

Example:

```python
def test():
    try:
        return "PASS"

    finally:
        print("Cleanup")
```

Calling:

```python
print(test())
```

produces:

```text
Cleanup
PASS
```

The `finally` block executes before the function actually returns.

---

# 21. `finally` Can Override a Return

Consider:

```python
def test():
    try:
        return "PASS"

    finally:
        return "FAIL"
```

Result:

```text
FAIL
```

Why?

Because the `return` in `finally` overrides the earlier return.

This is technically possible but **strongly discouraged**.

---

# 22. Why `return` in `finally` Is Dangerous

Example:

```python
def run_test():
    try:
        return "PASS"

    finally:
        return "FAIL"
```

The original result is silently replaced.

This can produce extremely confusing automation behavior.

Therefore:

```text
Avoid `return` inside `finally`.
```

Especially in test automation.

---

# 23. `finally` With Exceptions

Example:

```python
def test():
    try:
        10 / 0

    finally:
        print("Cleanup")
```

Output:

```text
Cleanup
```

After that, the `ZeroDivisionError` still propagates because there is no `except` handling it.

Conceptually:

```text
Exception occurs
     ↓
finally executes
     ↓
original exception continues
```

---

# 24. `finally` and Exception Propagation

Consider:

```python
def read_test():
    try:
        raise ValueError("Invalid test data")

    finally:
        print("Cleanup complete")

read_test()
```

Output includes:

```text
Cleanup complete
```

followed by the unhandled `ValueError`.

Therefore:

```text
finally ≠ exception suppression
```

---

# 25. `finally` With `break`

Example:

```python
for i in range(5):
    try:
        if i == 2:
            break
    finally:
        print("Cleanup:", i)
```

The `finally` block still executes before the loop exits.

---

# 26. `finally` With `continue`

Similarly:

```python
for i in range(3):
    try:
        continue
    finally:
        print("Cleanup:", i)
```

The `finally` block executes before the iteration continues.

The important concept is:

```text
Control-flow change
      ↓
finally executes first
```

---

# 27. `finally` and Program Termination

`finally` is designed for normal Python control flow involving:

```text
try
except
return
break
continue
exception propagation
```

It should not be interpreted as an absolute guarantee against every possible process termination scenario.

For example, external termination or abrupt process termination can prevent normal Python cleanup from completing.

---

# 28. `else` vs `finally`

This is a common interview question.

## `else`

Runs only if `try` succeeds.

```text
Success → else
Failure → no else
```

## `finally`

Runs during both success and handled/unhandled exception paths in normal control flow.

```text
Success → finally
Failure → finally
```

Remember:

```text
else    = success path
finally = cleanup/finalization path
```

---

# 29. `except` vs `else` vs `finally`

| Block     | Purpose                      |
| --------- | ---------------------------- |
| `try`     | Attempt risky operation      |
| `except`  | Handle matching exception    |
| `else`    | Run when `try` succeeds      |
| `finally` | Perform finalization/cleanup |

---

# 30. Complete Example

```python
try:
    value = int(user_input)

except ValueError:
    print("Invalid input")

else:
    print("Input accepted")
    process(value)

finally:
    cleanup()
```

Flow:

```text
                 try
                  |
          ┌───────┴───────┐
          |               |
       Success          Failure
          |               |
          ↓               ↓
        else            except
          |               |
          └───────┬───────┘
                  ↓
               finally
                  ↓
               continue
```

---

# 31. Storage Automation Example

Consider a test runner:

```python
test_started = False

try:
    test_started = True
    start_storage_test("/dev/sda")
    result = collect_result()

except TimeoutError:
    print("Test timed out")

except OSError as exc:
    print(f"Storage operation failed: {exc}")

else:
    print("Storage test completed successfully")
    print("Result:", result)

finally:
    if test_started:
        stop_storage_test("/dev/sda")

    collect_diagnostics()
```

This structure separates responsibilities:

```text
try
    ↓
Perform test

except
    ↓
Handle known failure

else
    ↓
Process successful result

finally
    ↓
Cleanup + diagnostics
```

---

# 32. Why Cleanup Matters in Storage Automation

Imagine a test starts:

```text
Storage test process
Background monitoring
Temporary files
Device locks
Log collection
```

Then the test fails.

If cleanup does not happen:

```text
Failed test
   ↓
Process remains running
   ↓
Resource remains locked
   ↓
Next test starts
   ↓
Unexpected behavior
```

Therefore cleanup is part of reliable automation.

---

# 33. Cleanup Must Be Safe

Bad:

```python
finally:
    stop_test()
```

if `stop_test()` itself can fail unexpectedly.

A robust system should consider whether cleanup operations can themselves raise exceptions and how those failures should be handled.

For critical automation, cleanup needs its own error strategy.

---

# 34. Do Not Hide Cleanup Failures

Avoid:

```python
finally:
    try:
        cleanup()
    except:
        pass
```

unless there is a deliberate reason and the failure is recorded appropriately.

Otherwise:

```text
Cleanup failed
    ↓
Failure disappears
```

This can leave the environment corrupted.

---

# 35. Context Managers vs `finally`

Python provides context managers for many resource-management tasks.

Example:

```python
with open("storage.log", "r") as file:
    data = file.read()
```

This is generally preferred over manually writing:

```python
file = open("storage.log", "r")

try:
    data = file.read()

finally:
    file.close()
```

Both express the same fundamental idea:

```text
Acquire resource
      ↓
Use resource
      ↓
Release resource
```

The `with` statement automates the cleanup pattern.

---

# 36. When `finally` Is Still Useful

`finally` remains useful when cleanup is not already provided by a context manager.

Examples:

```text
Stop test process
Release custom lock
Reset device state
Delete temporary state
Restore configuration
Collect diagnostics
```

---

# 37. Common Mistake — Putting Success Logic in `finally`

Bad:

```python
try:
    run_test()

finally:
    print("Test passed")
```

This is incorrect.

`finally` executes even if the test fails.

Therefore:

```text
finally
≠
success
```

If you need success-specific behavior, use `else`.

---

# 38. Common Mistake — Putting Cleanup in `else`

Bad design:

```python
try:
    run_test()

except Exception:
    print("Test failed")

else:
    cleanup()
```

Now cleanup only occurs on success.

If the test fails, cleanup may never happen.

Cleanup that must happen regardless should normally be placed in `finally`.

---

# 39. Common Mistake — Large `try` Block

Avoid:

```python
try:
    start_test()
    read_logs()
    parse_logs()
    generate_report()
    send_report()
    cleanup()
except Exception:
    print("Something failed")
```

If something fails, it can be difficult to identify which operation failed.

Better:

```text
Each operation
    ↓
Clear responsibility
    ↓
Appropriate exception boundary
```

---

# 40. Common Mistake — Returning From `finally`

Avoid:

```python
def run_test():
    try:
        return "PASS"
    finally:
        return "FAIL"
```

The `finally` return overrides the earlier return.

This can corrupt test results.

---

# 41. Interview Questions

## Q1. When does `else` execute?

Only when the `try` block completes without raising an exception.

---

## Q2. When does `finally` execute?

In normal Python control flow, `finally` executes during both successful and exceptional paths before control leaves the `try` statement.

---

## Q3. What is the difference between `else` and `finally`?

```text
else
→ success-only path

finally
→ finalization/cleanup path
```

---

## Q4. Can `try` have `finally` without `except`?

Yes.

```python
try:
    operation()
finally:
    cleanup()
```

---

## Q5. Does `finally` suppress an exception?

No.

Without other handling, the exception continues to propagate after `finally`.

---

## Q6. Can `finally` execute if there is a `return`?

Yes.

The `finally` block executes before the function returns.

---

## Q7. What happens if `finally` contains `return`?

It can override a pending return or exception.

This is why returning from `finally` is generally discouraged.

---

## Q8. Why is `else` useful?

It allows success-only logic to remain separate from the risky operation and exception-handling logic.

---

# 42. Storage Engineering Interview Questions

## Q9. A storage test fails halfway through. Where should cleanup happen?

Cleanup that must occur regardless of success or failure should generally be placed in `finally` or implemented through an appropriate resource-management mechanism.

---

## Q10. Why shouldn't "test passed" be printed in `finally`?

Because `finally` executes on failure as well as success.

Therefore it cannot represent success.

---

## Q11. What belongs in `finally` in a storage test framework?

Potential examples:

```text
Stop test process
Release resources
Restore state
Collect final diagnostics
Remove temporary resources
Close custom connections
```

---

## Q12. Why is cleanup important after a failed storage test?

Because a failed test may leave processes, locks, temporary files, device state, or other resources behind and can contaminate subsequent tests.

---

# 43. Knowledge-Gap Checklist

Before moving to `raise`, make sure you understand:

```text
[ ] `else`
[ ] `finally`
[ ] `try + except + else`
[ ] `try + except + finally`
[ ] `try + except + else + finally`
[ ] else executes only after successful try
[ ] finally executes during normal cleanup paths
[ ] finally does not mean success
[ ] finally does not automatically suppress exceptions
[ ] finally with return
[ ] finally with break
[ ] finally with continue
[ ] Resource cleanup
[ ] Context managers
[ ] Cleanup failures
[ ] Storage test cleanup
```

---

# 44. Final Mental Model

```text
             TRY
              |
       ┌──────┴──────┐
       |             |
    SUCCESS        FAILURE
       |             |
       ↓             ↓
     ELSE          EXCEPT
       |             |
       └──────┬──────┘
              ↓
           FINALLY
              ↓
        Continue / Return
        / Propagate
```

Remember:

```text
try
→ attempt

except
→ handle failure

else
→ successful path

finally
→ cleanup/finalization
```

---

# 45. Final Engineering Rule

The key principle is:

```text
Use `else` for success-specific work.
Use `except` for failure handling.
Use `finally` for cleanup/finalization.
```

And for storage automation:

```text
START TEST
    ↓
TRY
    ↓
SUCCESS ─────────→ ELSE → process result
    |
FAILURE ─────────→ EXCEPT → classify/report
    |
    └───────────────────────┐
                            ↓
                         FINALLY
                            ↓
                     cleanup/diagnostics
```

# END

````

