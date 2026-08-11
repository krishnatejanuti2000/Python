# 01 — Errors and Exceptions

## Objective

Before learning `try`, `except`, `else`, and `finally`, we need to understand exactly:

- What an error is
- What an exception is
- Why Python raises exceptions
- Different categories of errors
- How to read a traceback
- How to identify the actual failure
- How exceptions differ from logical mistakes

The goal is to develop the mindset:

```text
Program
   ↓
Something goes wrong
   ↓
Python detects the problem
   ↓
Python raises an exception
   ↓
Traceback is generated
   ↓
Program either handles it or terminates
````

---

# 1. What Is an Error?

An error means that something is wrong with a program.

Errors can occur at different stages.

The major categories we care about are:

```text
1. Syntax Errors
2. Runtime Errors / Exceptions
3. Logical Errors
```

---

# 2. Syntax Error

A syntax error occurs when Python cannot understand the structure of the code.

Example:

```python
if x > 10
    print(x)
```

Output:

```text
SyntaxError: expected ':'
```

Python cannot even correctly interpret the program.

Therefore:

```text
Syntax Error
    ↓
Program cannot start normally
```

---

# 3. Another Syntax Error Example

```python
print("Hello"
```

Output:

```text
SyntaxError: '(' was never closed
```

The problem is the syntax itself.

---

# 4. Syntax Errors Are Different From Exceptions

Consider:

```python
print("Hello"
```

Python reports:

```text
SyntaxError
```

Now consider:

```python
x = 10 / 0
```

Python understands the syntax, but execution fails.

Output:

```text
ZeroDivisionError: division by zero
```

Therefore:

```text
Syntax Error
    ↓
Python cannot correctly parse the code

Exception
    ↓
Python understands the code
    ↓
Something goes wrong during execution
```

---

# 5. Runtime Error / Exception

A runtime failure happens while the program is executing.

Example:

```python
x = 10
y = 0

result = x / y
```

Output:

```text
ZeroDivisionError: division by zero
```

The code is syntactically valid.

The problem occurs during execution.

Python therefore raises an exception.

---

# 6. What Is an Exception?

An exception is an object representing an abnormal condition that occurs during program execution.

Example:

```python
10 / 0
```

causes:

```text
ZeroDivisionError
```

Another example:

```python
int("abc")
```

causes:

```text
ValueError
```

Another:

```python
my_list = [10, 20, 30]

print(my_list[5])
```

causes:

```text
IndexError
```

---

# 7. Why Does Python Raise Exceptions?

Python raises an exception when an operation cannot be completed normally.

Examples:

```text
Divide by zero
      ↓
ZeroDivisionError

Invalid conversion
      ↓
ValueError

Invalid operation/type
      ↓
TypeError

Missing dictionary key
      ↓
KeyError

Invalid list index
      ↓
IndexError

Missing file
      ↓
FileNotFoundError
```

---

# 8. Basic Exception Flow

Consider:

```python
print("Start")

x = 10 / 0

print("End")
```

Execution:

```text
print("Start")
      ↓
Start
      ↓
10 / 0
      ↓
ZeroDivisionError
      ↓
Program stops
      ↓
print("End") is NOT executed
```

Output:

```text
Start
Traceback ...
ZeroDivisionError: division by zero
```

---

# 9. What Is a Traceback?

A traceback is Python's report showing the path the program followed before the exception occurred.

Example:

```python
def divide(a, b):
    return a / b

def calculate():
    return divide(10, 0)

calculate()
```

Possible output:

```text
Traceback (most recent call last):
  File "test.py", line 7, in <module>
    calculate()
  File "test.py", line 5, in calculate
    return divide(10, 0)
  File "test.py", line 2, in divide
    return a / b
ZeroDivisionError: division by zero
```

---

# 10. How to Read a Traceback

Do not panic when you see a long traceback.

Read it systematically.

Look at:

```text
1. Exception type
2. Exception message
3. Final failing line
4. Function call chain
5. Input/state involved
```

The most important information is normally near the bottom.

In the example:

```text
ZeroDivisionError: division by zero
```

is the exception.

The failing operation is:

```python
return a / b
```

The problematic value is:

```text
b = 0
```

---

# 11. Exception Type

The exception type tells you what kind of failure occurred.

Example:

```text
ValueError
```

means the value was inappropriate for the operation.

Example:

```text
TypeError
```

means the operation was used with an inappropriate type.

Example:

```text
FileNotFoundError
```

means the requested file could not be found.

---

# 12. Exception Message

The message provides additional information about the failure.

Example:

```text
ValueError: invalid literal for int() with base 10: 'abc'
```

Break it down:

```text
Exception Type:
ValueError

Message:
invalid literal for int() with base 10: 'abc'
```

This tells us that:

```python
int("abc")
```

was attempted.

---

# 13. Important Built-in Exception: `NameError`

Occurs when Python cannot find a variable or name.

Example:

```python
print(device)
```

if `device` was never defined.

Possible output:

```text
NameError: name 'device' is not defined
```

---

# 14. Important Built-in Exception: `TypeError`

Occurs when an operation is performed using incompatible types.

Example:

```python
result = 10 + "20"
```

Output:

```text
TypeError
```

The issue is:

```text
int + str
```

---

# 15. Important Built-in Exception: `ValueError`

Occurs when the type is acceptable but the value is inappropriate.

Example:

```python
value = int("abc")
```

Output:

```text
ValueError
```

The argument is a string, which `int()` can normally accept, but:

```text
"abc"
```

is not a valid integer representation.

---

# 16. `TypeError` vs `ValueError`

This is an important interview question.

## TypeError

Wrong type for the operation.

Example:

```python
10 + "20"
```

Conceptually:

```text
Expected numeric value
Received string
```

## ValueError

Correct general type, but invalid value.

Example:

```python
int("abc")
```

Conceptually:

```text
Expected a string containing an integer
Received "abc"
```

Remember:

```text
TypeError  → wrong type
ValueError → wrong value
```

---

# 17. `ZeroDivisionError`

Example:

```python
result = 100 / 0
```

Python raises:

```text
ZeroDivisionError
```

---

# 18. `IndexError`

Occurs when a sequence index does not exist.

Example:

```python
drives = ["/dev/sda", "/dev/sdb"]

print(drives[5])
```

Output:

```text
IndexError: list index out of range
```

Valid indexes are:

```text
0
1
```

---

# 19. `KeyError`

Occurs when a dictionary key does not exist.

Example:

```python
drive = {
    "device": "/dev/sda",
    "status": "PASS"
}

print(drive["capacity"])
```

Output:

```text
KeyError: 'capacity'
```

---

# 20. `AttributeError`

Occurs when an object does not have the requested attribute or method.

Example:

```python
text = "storage"

text.append("test")
```

Strings do not provide an `append()` method.

Python raises:

```text
AttributeError
```

---

# 21. `FileNotFoundError`

Occurs when Python attempts to access a file that does not exist.

Example:

```python
file = open("storage.log", "r")
```

If the file is missing:

```text
FileNotFoundError
```

This becomes especially important in automation.

---

# 22. `PermissionError`

Occurs when an operation is not permitted.

Example:

```python
file = open("/protected/storage.log", "r")
```

If the current process lacks permission:

```text
PermissionError
```

---

# 23. `OSError`

`OSError` represents operating-system-related failures.

Examples can include:

```text
File access failures
Device-related OS errors
Directory operations
System calls
```

Several more specific exceptions inherit from `OSError`.

For example:

```text
FileNotFoundError
PermissionError
```

are related to the OS error hierarchy.

---

# 24. `ImportError`

Occurs when an import cannot be completed.

Example:

```python
from math import something_that_does_not_exist
```

Python can raise:

```text
ImportError
```

---

# 25. `ModuleNotFoundError`

Occurs when Python cannot find the requested module.

Example:

```python
import storage_testing_framework
```

if that module is unavailable.

Possible result:

```text
ModuleNotFoundError
```

---

# 26. Logical Errors

Logical errors are different.

Example:

```python
capacity = 500
used = 100

free = capacity + used
```

Python may execute this successfully.

There may be no exception.

But the calculation is logically wrong.

The correct operation should be:

```python
free = capacity - used
```

Therefore:

```text
Program runs
    ↓
No exception
    ↓
Wrong result
    ↓
Logical error
```

---

# 27. Three Major Categories

| Category      | Example           | Program executes?  |
| ------------- | ----------------- | ------------------ |
| Syntax Error  | Missing `:`       | ❌                  |
| Exception     | Divide by zero    | Starts, then fails |
| Logical Error | Wrong calculation | ✅                  |

---

# 28. Exception vs Logical Error

Consider:

```python
capacity = 500
used = 100

free = capacity + used
```

No exception occurs.

Python has no knowledge of your intended business rule.

This is why:

```text
Exception Handling
```

cannot solve every type of software problem.

Exception handling deals primarily with abnormal runtime conditions.

---

# 29. Exception Object

When Python raises an exception, the exception is represented as an object.

For example:

```python
try:
    value = int("abc")
except ValueError as exc:
    print(exc)
```

The variable:

```python
exc
```

contains the exception object.

Printing it:

```python
print(exc)
```

might produce:

```text
invalid literal for int() with base 10: 'abc'
```

---

# 30. Exception Type and Message

You can inspect the type:

```python
try:
    value = int("abc")
except Exception as exc:
    print(type(exc))
    print(exc)
```

Possible output:

```text
<class 'ValueError'>
invalid literal for int() with base 10: 'abc'
```

This becomes useful during debugging.

---

# 31. Why Exception Type Matters

Suppose a storage test fails.

You should not treat every failure identically.

For example:

```text
FileNotFoundError
PermissionError
TimeoutError
OSError
ValueError
```

may require completely different actions.

For example:

```text
FileNotFoundError
    ↓
Check path

PermissionError
    ↓
Check permissions

TimeoutError
    ↓
Check command/device response

ValueError
    ↓
Check input/configuration
```

Therefore:

```text
Exception Type
      ↓
Failure Classification
      ↓
Correct Recovery Strategy
```

---

# 32. Exceptions in Storage Automation

Consider:

```python
device = "/dev/sda"

result = open("/logs/sda_test.log")
```

If the log does not exist:

```text
FileNotFoundError
```

The automation should not blindly continue as if the log exists.

It should determine:

```text
Was the log expected?
Is the path correct?
Did the test actually run?
Was the log generated?
```

---

# 33. Another Storage Example

Suppose an automation script executes:

```bash
smartctl -a /dev/sda
```

Possible failures include:

```text
Device does not exist
Permission denied
Command unavailable
Device communication failure
Timeout
Unexpected output
```

These are different failure conditions.

A robust automation framework must distinguish them.

---

# 34. Exception Handling Is Not Error Hiding

A dangerous mindset is:

```text
Something failed
    ↓
Catch it
    ↓
Ignore it
```

For example:

```python
try:
    run_storage_test()
except:
    pass
```

This can make the automation report success even though the test failed.

That is extremely dangerous.

---

# 35. Correct Engineering Mindset

Instead:

```text
Failure
   ↓
Detect
   ↓
Classify
   ↓
Determine root cause
   ↓
Recover OR propagate
   ↓
Record failure
```

Exception handling should make failures **understandable**, not invisible.

---

# 36. Exception Handling vs Debugging

Exception handling answers:

> What should the program do when this failure occurs?

Debugging answers:

> Why did this failure occur?

Example:

```text
FileNotFoundError
```

Exception handling:

```text
Catch it and report missing log
```

Debugging/RCA:

```text
Why was the log missing?
Was the test never started?
Did the command fail?
Was the path wrong?
Did another process remove the file?
```

Both skills are important.

---

# 37. Exception Handling vs Root Cause Analysis

Example:

```text
Storage test failed
        ↓
Python catches exception
        ↓
Exception = TimeoutError
```

That is not necessarily the root cause.

The root cause might be:

```text
Device stopped responding
```

or:

```text
SAS link reset
```

or:

```text
Controller timeout
```

or:

```text
Device disappeared
```

Therefore:

```text
Exception
    ≠
Root Cause
```

An exception is evidence of a failure condition.

---

# 38. Multiple Exceptions Can Occur

A single program may encounter different failures.

Example:

```python
value = int(user_input)
result = 100 / value
```

Possible exceptions:

```text
ValueError
ZeroDivisionError
```

depending on the input.

This is why later we need:

```text
Multiple Exception Handling
```

---

# 39. Exception Propagation Preview

If an exception is not handled at the current location, it can propagate to the caller.

Example:

```python
def read_device():
    return int("abc")

def run_test():
    read_device()

run_test()
```

Flow:

```text
run_test()
    ↓
read_device()
    ↓
ValueError
    ↓
Not handled in read_device()
    ↓
Propagates to run_test()
    ↓
Not handled
    ↓
Propagates to caller
    ↓
Program terminates
```

We will study this deeply later.

---

# 40. Why Tracebacks Are Valuable

A traceback provides a chain of execution.

It can tell you:

```text
Which file?
Which line?
Which function?
Which operation?
Which exception?
Which message?
```

Therefore, when troubleshooting:

```text
Never ignore the traceback.
```

Read it.

---

# 41. Practical Traceback Reading Method

When you see:

```text
Traceback (most recent call last):
    ...
ValueError: invalid literal for int()
```

Start from the bottom:

```text
1. What exception?
2. What message?
3. Which line caused it?
4. What function was executing?
5. What input caused it?
6. Why was that input invalid?
```

Then move upward through the traceback to understand how execution reached that point.

---

# 42. Common Mistakes

## Mistake 1 — Calling every problem an exception

Wrong:

```text
Wrong calculation = exception
```

Not necessarily.

It may be a logical error.

---

## Mistake 2 — Ignoring exception type

Bad troubleshooting:

```text
Something failed.
```

Better:

```text
FileNotFoundError occurred while opening the test log.
```

---

## Mistake 3 — Looking only at the first traceback line

The useful information is often near the bottom.

Always inspect:

```text
Exception type
+
Message
+
Failing line
```

---

## Mistake 4 — Treating all exceptions equally

This is poor automation design.

For example:

```text
PermissionError
```

should not necessarily be handled the same way as:

```text
TimeoutError
```

---

# 43. Interview Questions

## Q1. What is an exception?

### Answer

An exception is an abnormal runtime condition represented by an exception object that interrupts normal program execution unless it is handled.

---

## Q2. Difference between syntax error and exception?

### Answer

A syntax error occurs when Python cannot parse the program correctly.

An exception occurs during execution after the code has been successfully parsed.

---

## Q3. Difference between exception and logical error?

### Answer

An exception is a runtime failure detected by Python.

A logical error can produce an incorrect result even though the program executes without raising an exception.

---

## Q4. What is a traceback?

### Answer

A traceback is Python's report of the execution path leading to an exception, including relevant files, lines, function calls, and the final exception type and message.

---

## Q5. What is `ValueError`?

### Answer

`ValueError` occurs when an operation receives an argument of an appropriate general type but an inappropriate value.

Example:

```python
int("abc")
```

---

## Q6. Difference between `TypeError` and `ValueError`?

### Answer

```text
TypeError
→ inappropriate type

ValueError
→ appropriate type but inappropriate value
```

---

## Q7. What is `FileNotFoundError`?

### Answer

It is an exception raised when an operation attempts to access a file or resource that cannot be found.

---

## Q8. Why should exception types be understood in automation?

### Answer

Because different failure types require different recovery, retry, reporting, or escalation strategies.

---

# 44. Storage Engineering Interview Question

## Q9. A storage test automation script reports `FileNotFoundError`. What would you investigate?

### Answer

I would investigate:

```text
1. Is the path correct?
2. Does the file actually exist?
3. Was the test started?
4. Did the test generate the expected log?
5. Was the log generated somewhere else?
6. Did another process remove it?
7. Are we using the correct working directory?
```

The exception tells us **what failed**.

The investigation determines **why it failed**.

---

# 45. Storage Engineering Interview Question

## Q10. Is catching an exception enough to determine root cause?

### Answer

No.

An exception is an indication of a runtime failure.

Root Cause Analysis requires additional evidence such as:

```text
Logs
Command output
Device state
System state
Configuration
Timing
Previous events
```

---

# 46. Key Concepts to Remember

```text
Syntax Error
    ↓
Python cannot parse code

Exception
    ↓
Runtime abnormal condition

Logical Error
    ↓
Program executes but produces incorrect behavior

Traceback
    ↓
Execution path leading to exception

Exception Type
    ↓
Classifies failure

Exception Message
    ↓
Provides failure details
```

---

# 47. Mental Model

When you encounter a failure, think:

```text
What happened?
     ↓
What exception occurred?
     ↓
Where did it occur?
     ↓
What input/state caused it?
     ↓
Is it recoverable?
     ↓
Should I handle it?
     ↓
Should I propagate it?
     ↓
What evidence should I preserve?
```

---

# 48. Knowledge-Gap Checklist

Before moving to `try` and `except`, make sure you understand:

```text
[ ] Syntax error
[ ] Runtime exception
[ ] Logical error
[ ] Exception object
[ ] Exception type
[ ] Exception message
[ ] Traceback
[ ] Common built-in exceptions
[ ] TypeError
[ ] ValueError
[ ] NameError
[ ] IndexError
[ ] KeyError
[ ] AttributeError
[ ] ZeroDivisionError
[ ] FileNotFoundError
[ ] PermissionError
[ ] OSError
[ ] ImportError
[ ] ModuleNotFoundError
[ ] Exception vs root cause
[ ] Basic exception propagation
```

---

# 49. Final Summary

```text
Error
 ├── Syntax Error
 ├── Runtime Exception
 └── Logical Error
```

Runtime exceptions include:

```text
ValueError
TypeError
NameError
IndexError
KeyError
AttributeError
ZeroDivisionError
FileNotFoundError
PermissionError
OSError
ImportError
ModuleNotFoundError
```

The most important debugging flow is:

```text
Exception
    ↓
Type
    ↓
Message
    ↓
Failing line
    ↓
Input/state
    ↓
Root cause
    ↓
Recovery / propagation
```

And the most important engineering principle is:

```text
DO NOT HIDE FAILURES.

Understand them.
Handle them when appropriate.
Preserve useful information.
Propagate them when the current layer cannot safely recover.
```

# END


