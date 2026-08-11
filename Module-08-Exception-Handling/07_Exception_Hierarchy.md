# 07 — Exception Hierarchy

## Objective

Python exceptions are organized in an inheritance hierarchy.

Understanding this hierarchy is important because it determines:

- Which `except` block matches an exception
- Why parent exceptions can catch child exceptions
- Why exception ordering matters
- When to use `Exception`
- Why `BaseException` should generally not be caught broadly
- How built-in exceptions are related
- How custom exception hierarchies work
- How exception hierarchy affects Storage Test Automation

---

# 1. What Is an Exception Hierarchy?

Python does not treat every exception as an unrelated object.

Exceptions are organized using class inheritance.

At the top is:

```python
BaseException
````

A simplified hierarchy is:

```text
BaseException
    |
    +-- Exception
    |     |
    |     +-- ArithmeticError
    |     |      |
    |     |      +-- ZeroDivisionError
    |     |
    |     +-- LookupError
    |     |      |
    |     |      +-- IndexError
    |     |      +-- KeyError
    |     |
    |     +-- OSError
    |     |      |
    |     |      +-- FileNotFoundError
    |     |      +-- PermissionError
    |     |      +-- TimeoutError
    |     |
    |     +-- ValueError
    |     +-- TypeError
    |     +-- NameError
    |     +-- AttributeError
    |
    +-- KeyboardInterrupt
    +-- SystemExit
    +-- GeneratorExit
```

This is a simplified view rather than the complete Python hierarchy.

---

# 2. Why Does the Hierarchy Matter?

Consider:

```python
try:
    open("missing.log")

except OSError:
    print("OS error")
```

The actual exception is:

```text
FileNotFoundError
```

Why does `OSError` catch it?

Because:

```text
FileNotFoundError
        ↓
OSError
        ↓
Exception
        ↓
BaseException
```

`FileNotFoundError` is a subclass of `OSError`.

Therefore an `OSError` handler can catch it.

---

# 3. Parent and Child Exceptions

Consider:

```python
class Parent(Exception):
    pass


class Child(Parent):
    pass
```

Hierarchy:

```text
Exception
    |
    +-- Parent
          |
          +-- Child
```

Now:

```python
raise Child("Something happened")
```

can be caught by:

```python
except Child:
```

and also by:

```python
except Parent:
```

because `Child` is a `Parent`.

---

# 4. The `isinstance()` Relationship

You can observe inheritance using `isinstance()`.

Example:

```python
class StorageError(Exception):
    pass


class StorageTestError(StorageError):
    pass
```

Then:

```python
error = StorageTestError()

print(isinstance(error, StorageTestError))
print(isinstance(error, StorageError))
print(isinstance(error, Exception))
```

Output:

```text
True
True
True
```

This demonstrates:

```text
StorageTestError
      ↓
StorageError
      ↓
Exception
```

---

# 5. `issubclass()`

You can also inspect the class relationship:

```python
print(issubclass(StorageTestError, StorageError))
```

Output:

```text
True
```

And:

```python
print(issubclass(StorageTestError, Exception))
```

Output:

```text
True
```

This is useful for understanding exception relationships.

---

# 6. `Exception` Is a Major Application-Level Parent

Most normal application exceptions inherit from:

```python
Exception
```

Therefore:

```python
except Exception:
```

can catch many ordinary application/runtime exceptions.

Example:

```python
try:
    int("abc")

except Exception as exc:
    print(type(exc).__name__)
```

Output:

```text
ValueError
```

---

# 7. `BaseException`

At the top of the normal hierarchy is:

```python
BaseException
```

Some important exceptions directly or indirectly related to `BaseException` include:

```text
SystemExit
KeyboardInterrupt
GeneratorExit
Exception
```

The important distinction is:

```text
BaseException
    |
    +-- Exception
    |
    +-- KeyboardInterrupt
    +-- SystemExit
    +-- GeneratorExit
```

---

# 8. Why `except Exception` Is Usually Preferred Over `except BaseException`

Consider:

```python
try:
    operation()

except Exception:
    handle_failure()
```

This generally handles normal application exceptions.

But:

```python
try:
    operation()

except BaseException:
    handle_failure()
```

is much broader.

It can also catch special control-flow exceptions such as:

```text
KeyboardInterrupt
SystemExit
```

which normally should be allowed to propagate.

Therefore, for ordinary application-level handling:

```text
Prefer:
except Exception
```

rather than:

```text
except BaseException
```

unless you have a very specific reason.

---

# 9. `KeyboardInterrupt`

When the user presses:

```text
Ctrl+C
```

Python can raise:

```text
KeyboardInterrupt
```

It is not a normal `Exception` subclass in the same branch.

Conceptually:

```text
BaseException
    |
    +-- KeyboardInterrupt
```

This is one reason broad:

```python
except BaseException:
```

can be dangerous.

---

# 10. `SystemExit`

Python can raise:

```python
SystemExit
```

when the program exits through mechanisms such as:

```python
sys.exit()
```

Again, this is outside the normal `Exception` branch.

Therefore:

```python
except Exception:
```

does not normally catch `SystemExit`.

---

# 11. Why This Matters in Automation

Suppose a Storage Test Automation program is running:

```text
Test
 ↓
Monitoring
 ↓
Log collection
 ↓
Result reporting
```

If the user presses:

```text
Ctrl+C
```

the automation may need to terminate rather than have a generic exception handler silently continue.

Therefore:

```python
except Exception:
```

is generally safer than:

```python
except BaseException:
```

for normal application failures.

---

# 12. Arithmetic Exception Hierarchy

A simplified branch is:

```text
ArithmeticError
    |
    +-- ZeroDivisionError
    +-- OverflowError
    +-- FloatingPointError
```

Example:

```python
try:
    10 / 0

except ArithmeticError:
    print("Arithmetic failure")
```

This can catch:

```text
ZeroDivisionError
```

because it inherits from `ArithmeticError`.

---

# 13. Specific Arithmetic Exception

You can instead write:

```python
try:
    10 / 0

except ZeroDivisionError:
    print("Division by zero")
```

This is more precise when you specifically care about division by zero.

---

# 14. Lookup Exception Hierarchy

A simplified branch is:

```text
LookupError
    |
    +-- IndexError
    +-- KeyError
```

Therefore:

```python
except LookupError:
```

can catch both:

```text
IndexError
KeyError
```

---

# 15. `IndexError`

Example:

```python
drives = ["/dev/sda", "/dev/sdb"]

try:
    print(drives[5])

except IndexError:
    print("Invalid index")
```

The specific handler is:

```text
IndexError
```

---

# 16. `KeyError`

Example:

```python
drive = {
    "device": "/dev/sda"
}

try:
    print(drive["capacity"])

except KeyError:
    print("Missing dictionary key")
```

Again, this belongs to:

```text
LookupError
    |
    +-- KeyError
```

---

# 17. Catching the Parent

You could write:

```python
try:
    print(drives[5])

except LookupError:
    print("Lookup operation failed")
```

This catches `IndexError`.

Similarly:

```python
try:
    print(drive["capacity"])

except LookupError:
    print("Lookup operation failed")
```

can catch `KeyError`.

---

# 18. When Should You Use the Parent?

Use a parent exception when:

```text
Several child exceptions
        +
Same recovery strategy
```

For example:

```python
try:
    process_data()

except LookupError:
    print("Required data could not be located")
```

If the application does not need to distinguish `IndexError` from `KeyError`, the parent may be appropriate.

---

# 19. When Should You Use the Child?

Use the specific exception when different failures require different actions.

Example:

```python
try:
    process_data()

except IndexError:
    print("List index is invalid")

except KeyError:
    print("Required dictionary key is missing")
```

This provides more precise failure classification.

---

# 20. OSError Hierarchy

This branch is particularly important for Storage Engineering.

A simplified view:

```text
OSError
    |
    +-- FileNotFoundError
    +-- PermissionError
    +-- FileExistsError
    +-- IsADirectoryError
    +-- NotADirectoryError
    +-- TimeoutError
    +-- ...
```

These represent operating-system/resource-related failures.

---

# 21. `FileNotFoundError` as an `OSError`

Example:

```python
try:
    open("missing.log")

except OSError:
    print("OS-level failure")
```

This can catch:

```text
FileNotFoundError
```

because:

```text
FileNotFoundError
       ↓
OSError
```

---

# 22. Storage Example — Specific Handling

```python
try:
    with open("/var/log/storage.log") as file:
        data = file.read()

except FileNotFoundError:
    print("Storage log is missing")

except PermissionError:
    print("Permission denied")

except OSError as exc:
    print(f"Other OS failure: {exc}")
```

This is a good pattern because:

```text
Specific failures
       ↓
specific handling

Other OSError failures
       ↓
general OS fallback
```

---

# 23. Exception Ordering

Because child exceptions are also instances of their parent classes, order matters.

Correct:

```python
try:
    open("missing.log")

except FileNotFoundError:
    print("File missing")

except OSError:
    print("Other OS error")
```

Incorrect:

```python
try:
    open("missing.log")

except OSError:
    print("OS error")

except FileNotFoundError:
    print("File missing")
```

The second `FileNotFoundError` handler is unreachable for that exception.

---

# 24. General Rule

Always think:

```text
Specific
   ↓
Parent
   ↓
General fallback
```

Example:

```python
except FileNotFoundError:
    ...

except PermissionError:
    ...

except OSError:
    ...

except Exception:
    ...
```

---

# 25. Why Exception Ordering Is a Design Issue

This is not merely syntax.

The order determines:

```text
Which handler receives the failure
What recovery occurs
What gets logged
Whether the correct classification is preserved
```

Therefore incorrect ordering can cause incorrect automation behavior.

---

# 26. Custom Exception Hierarchy

From the previous document:

```python
class StorageError(Exception):
    pass


class StorageTestError(StorageError):
    pass


class StorageTimeoutError(StorageTestError):
    pass
```

Hierarchy:

```text
Exception
    |
    +-- StorageError
          |
          +-- StorageTestError
                |
                +-- StorageTimeoutError
```

---

# 27. Catching Different Levels

You can catch the most specific type:

```python
except StorageTimeoutError:
    retry_test()
```

or the parent:

```python
except StorageTestError:
    fail_test()
```

or the broader domain:

```python
except StorageError:
    report_storage_failure()
```

or the broad application-level type:

```python
except Exception:
    report_unexpected_failure()
```

---

# 28. How Python Searches for a Handler

Suppose:

```python
raise StorageTimeoutError("Test timed out")
```

and handlers are:

```python
except StorageTimeoutError:
    ...

except StorageTestError:
    ...

except StorageError:
    ...

except Exception:
    ...
```

Python checks from top to bottom.

The first compatible handler is:

```text
StorageTimeoutError
```

Therefore it executes that handler.

---

# 29. If the Specific Handler Is Missing

Suppose:

```python
try:
    raise StorageTimeoutError("Timeout")

except StorageTestError:
    print("Storage test failure")

except StorageError:
    print("Storage failure")
```

`StorageTimeoutError` is a subclass of `StorageTestError`.

Therefore:

```text
StorageTimeoutError
      ↓
StorageTestError handler
```

will execute.

---

# 30. Multi-Level Matching

Given:

```text
StorageTimeoutError
       ↓
StorageTestError
       ↓
StorageError
       ↓
Exception
```

all of these can potentially match the same exception:

```python
except StorageTimeoutError:
```

```python
except StorageTestError:
```

```python
except StorageError:
```

```python
except Exception:
```

But only the **first matching handler** executes.

---

# 31. Exception Hierarchy and Recovery Strategy

This gives us a powerful design pattern.

```text
Specific exception
       ↓
Specific recovery
```

Example:

```python
except StorageTimeoutError:
    retry_test()
```

If no specific handler exists:

```text
Parent exception
       ↓
Broader recovery
```

Example:

```python
except StorageTestError:
    mark_test_failed()
```

---

# 32. Storage Automation Example

Consider:

```python
class StorageError(Exception):
    pass


class StorageTestError(StorageError):
    pass


class StorageTimeoutError(StorageTestError):
    pass
```

Then:

```python
def run_test():
    raise StorageTimeoutError(
        "Device did not respond within timeout"
    )
```

Handling:

```python
try:
    run_test()

except StorageTimeoutError:
    print("Timeout — evaluate retry policy")

except StorageTestError:
    print("Storage test failed")

except StorageError:
    print("Storage-related failure")

except Exception:
    print("Unexpected application failure")
```

This creates a structured failure-handling model.

---

# 33. Why `BaseException` Should Be at the Top of Your Awareness

Think of the hierarchy like:

```text
BaseException
│
├── Exception
│   │
│   ├── normal application/runtime exceptions
│   │
│   └── custom application exceptions
│
├── KeyboardInterrupt
│
├── SystemExit
│
└── GeneratorExit
```

Normal application code generally operates under:

```text
Exception
```

rather than catching all of:

```text
BaseException
```

---

# 34. `Exception` Is Not "Every Possible Python Exception"

This is an important distinction.

It is common to hear:

> `except Exception` catches all exceptions.

More accurately:

```text
except Exception
```

catches exceptions deriving from `Exception`.

It does not normally catch:

```text
KeyboardInterrupt
SystemExit
GeneratorExit
```

because those are outside the `Exception` branch.

---

# 35. Why This Is Useful

Suppose:

```python
try:
    run_storage_test()

except Exception as exc:
    log_error(exc)
```

This can handle ordinary application failures while still allowing:

```text
Ctrl+C
```

or an explicit:

```python
sys.exit()
```

to retain their intended control-flow behavior.

---

# 36. Exception Hierarchy and `except` Design

Before writing:

```python
except Something:
```

ask:

```text
What is Something's parent?
What child exceptions could it catch?
Could it catch more than intended?
Should I handle the child separately?
```

This prevents accidental over-catching.

---

# 37. Inspecting Exception Hierarchy in Python

You can inspect relationships programmatically.

Example:

```python
print(FileNotFoundError.__mro__)
```

`__mro__` means:

```text
Method Resolution Order
```

It shows the class inheritance path.

You may see a structure similar to:

```text
(
    FileNotFoundError,
    OSError,
    Exception,
    BaseException,
    object
)
```

This demonstrates:

```text
FileNotFoundError
      ↓
OSError
      ↓
Exception
      ↓
BaseException
      ↓
object
```

---

# 38. Inspecting a Custom Hierarchy

Example:

```python
class StorageError(Exception):
    pass


class StorageTestError(StorageError):
    pass


class StorageTimeoutError(StorageTestError):
    pass
```

Now:

```python
print(StorageTimeoutError.__mro__)
```

The hierarchy will follow the chain:

```text
StorageTimeoutError
StorageTestError
StorageError
Exception
BaseException
object
```

---

# 39. `__bases__`

Another useful attribute is:

```python
print(StorageTimeoutError.__bases__)
```

This shows the immediate parent class.

For:

```python
class StorageTimeoutError(StorageTestError):
    pass
```

the immediate parent is:

```text
StorageTestError
```

---

# 40. Why This Is Useful During Debugging

If you encounter an unfamiliar exception:

```text
SomeException
```

you can investigate:

```python
print(SomeException.__mro__)
```

to understand:

```text
What does it inherit from?
Which broader handlers could catch it?
```

This is particularly useful when designing exception handling for unfamiliar libraries.

---

# 41. Exception Hierarchy and Library Exceptions

Third-party libraries may define their own exception hierarchies.

For example:

```text
LibraryError
    |
    +-- ConnectionError
    +-- AuthenticationError
    +-- TimeoutError
```

Before catching a library exception broadly, understand its hierarchy.

The same principle applies:

```text
Specific
   ↓
Parent
   ↓
General
```

---

# 42. Common Mistake — Catching the Parent Too Early

Bad:

```python
try:
    operation()

except StorageError:
    print("Storage error")

except StorageTimeoutError:
    print("Timeout")
```

Because:

```text
StorageTimeoutError
        ↓
StorageTestError
        ↓
StorageError
```

the first handler may catch it.

Correct:

```python
try:
    operation()

except StorageTimeoutError:
    print("Timeout")

except StorageError:
    print("Storage error")
```

---

# 43. Common Mistake — Catching `BaseException`

Avoid:

```python
try:
    operation()

except BaseException:
    print("Everything failed")
```

This can interfere with:

```text
KeyboardInterrupt
SystemExit
GeneratorExit
```

and other intended control-flow behavior.

Use:

```python
except Exception:
```

for ordinary broad application-level handling when appropriate.

---

# 44. Common Mistake — Assuming Parent Means Same Failure

Just because:

```text
FileNotFoundError
```

and:

```text
PermissionError
```

are both `OSError` subclasses does not mean they should always receive identical recovery.

Hierarchy tells you:

```text
They are related.
```

It does not automatically tell you:

```text
They need the same operational response.
```

---

# 45. Exception Hierarchy vs Exception Handling Strategy

Important distinction:

```text
Hierarchy
    ↓
Describes relationships between exception classes

Handling strategy
    ↓
Determines what the application should do
```

Example:

```text
FileNotFoundError
    ↓
OSError
```

does not mean:

```text
Always handle both identically.
```

You may still want:

```python
except FileNotFoundError:
    regenerate_or_locate_log()

except OSError:
    investigate_os_failure()
```

---

# 46. Interview Questions

## Q1. What is an exception hierarchy?

It is the inheritance structure that organizes Python exception classes into parent and child relationships.

---

## Q2. Why does exception hierarchy matter?

Because a parent exception can catch child exceptions, which affects handler matching and exception-handling design.

---

## Q3. Can `OSError` catch `FileNotFoundError`?

Yes.

`FileNotFoundError` is derived from `OSError`.

---

## Q4. Can `Exception` catch `ValueError`?

Yes.

`ValueError` inherits from `Exception`.

---

## Q5. Can `Exception` catch `KeyboardInterrupt`?

Normally, no.

`KeyboardInterrupt` derives directly from `BaseException`, not from `Exception`.

---

## Q6. Why should specific handlers come before parent handlers?

Because Python uses the first compatible handler. A parent handler could otherwise catch the child exception first.

---

## Q7. What is `BaseException`?

It is the root class for Python's built-in exception hierarchy.

---

## Q8. Why should `BaseException` generally not be caught broadly?

Because doing so can intercept special control-flow exceptions such as `KeyboardInterrupt` and `SystemExit`.

---

## Q9. What is `__mro__`?

It shows the method resolution order, which can be used to inspect a class's inheritance chain.

---

# 47. Storage Engineering Interview Questions

## Q10. Why might you create this hierarchy?

```text
StorageError
    ↓
StorageTestError
    ↓
StorageTimeoutError
```

### Answer

It allows the framework to represent increasing specificity.

A timeout is a storage test error, which is itself a storage-related error.

Therefore the framework can provide:

```text
Specific timeout handling
        OR
General storage test handling
        OR
General storage failure handling
```

---

## Q11. What happens if `StorageError` is placed before `StorageTimeoutError`?

The broader `StorageError` handler may catch the timeout before the specific timeout handler can execute.

Therefore the specific handler should come first.

---

## Q12. Should `FileNotFoundError` and `PermissionError` always have the same handling because both inherit from `OSError`?

No.

The hierarchy shows their relationship, but recovery should depend on the operational meaning of the specific failure.

---

# 48. Knowledge-Gap Checklist

Before moving to Exception Handling Patterns:

```text
[ ] Exception hierarchy
[ ] Parent exception
[ ] Child exception
[ ] Exception inheritance
[ ] isinstance()
[ ] issubclass()
[ ] __mro__
[ ] __bases__
[ ] BaseException
[ ] Exception
[ ] KeyboardInterrupt
[ ] SystemExit
[ ] GeneratorExit
[ ] ArithmeticError
[ ] LookupError
[ ] IndexError
[ ] KeyError
[ ] OSError
[ ] FileNotFoundError
[ ] PermissionError
[ ] Parent/child matching
[ ] Exception ordering
[ ] Custom exception hierarchy
[ ] Specific vs general recovery
[ ] Why not broadly catch BaseException
```

---

# 49. Final Mental Model

Think of exceptions as a tree:

```text
                    BaseException
                         |
              ┌──────────┴──────────┐
              |                     |
          Exception            special exits
              |
      ┌───────┼────────┐
      |       |        |
   ValueError OSError TypeError
              |
       ┌──────┴────────┐
       |               |
FileNotFoundError PermissionError
```

And your custom exceptions can form another branch:

```text
Exception
    |
StorageError
    |
    +-- DeviceValidationError
    |
    +-- StorageTestError
           |
           +-- StorageTimeoutError
```

---

# 50. Final Engineering Rule

The most important rule is:

```text
Understand the hierarchy
        ↓
Identify the most specific meaningful exception
        ↓
Handle specific failures first
        ↓
Use parent exceptions as broader fallbacks
        ↓
Avoid unnecessarily catching BaseException
```

In Storage Test Automation:

```text
Specific failure
      ↓
Specific recovery

Unknown storage failure
      ↓
StorageError fallback

Unexpected application failure
      ↓
Exception fallback
```

Exception hierarchy gives the framework a structured way to understand failures.

# END

````
