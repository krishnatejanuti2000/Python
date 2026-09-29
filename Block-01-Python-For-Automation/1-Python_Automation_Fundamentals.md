# BLOCK 1.1 — PYTHON AUTOMATION FUNDAMENTALS

## Purpose

Python automation for Storage Testing is not about writing large Python applications.

The goal is to write **reusable, predictable, maintainable, and failure-aware automation functions** that can later become components of a Storage Test Automation framework.

The master syllabus requires:

* Writing reusable automation functions
* Function design for automation
* Arguments and return values
* Reusable utility functions
* Exception-safe function design
* Modules and packages
* Importing reusable utilities

---

# 1. Reusable Automation Functions

A function is used to group a specific piece of logic so that it can be reused with different inputs.

Basic structure:

```python
def function_name(arguments):
    # processing
    return result
```

Example:

```python
def validate_firmware(actual, expected):
    return actual == expected
```

Usage:

```python
print(validate_firmware("MD220200", "MD220200"))
print(validate_firmware("MD220200", "MD220201"))
```

Output:

```text
True
False
```

The same validation logic can now be reused for different firmware versions.

---

# 2. Function Design for Automation

A good automation function should normally have a clear responsibility.

A useful mental model is:

```text
Input
  ↓
Validation / Processing
  ↓
Result
```

Example:

```python
def validate_temperature(actual, maximum):
    return actual <= maximum
```

The function receives:

```text
actual temperature
maximum allowed temperature
```

and returns:

```text
True / False
```

The caller can then decide what to do with the result.

```python
result = validate_temperature(45, 70)

if result:
    print("PASS")
else:
    print("FAIL")
```

A reusable function should avoid unnecessarily controlling the entire program.

---

# 3. Arguments

Arguments allow the same function to work with different values.

Example:

```python
def add(a, b):
    return a + b
```

Usage:

```python
print(add(10, 20))
print(add(100, 200))
```

Output:

```text
30
300
```

Storage automation example:

```python
def validate_temperature(actual, maximum):
    return actual <= maximum
```

Different devices or test configurations can provide different values:

```python
validate_temperature(45, 70)
validate_temperature(65, 70)
```

The function itself does not need to change.

---

# 4. Return Values

Return values are especially important in automation.

Consider:

```python
def check_device(device):

    if device == "/dev/nvme0n1":
        return True

    return False
```

The caller receives the result:

```python
result = check_device("/dev/nvme0n1")

if result:
    print("PASS")
else:
    print("FAIL")
```

This is more useful than simply printing inside the function.

The automation component performing the check should generally provide a result that another component can consume.

---

# 5. Returning Structured Information

Not every automation function should return only `True` or `False`.

Sometimes the function needs to return multiple related values.

Example:

```python
def get_device_info():

    return {
        "device": "/dev/nvme0n1",
        "model": "SN101",
        "firmware": "MD220200"
    }
```

Usage:

```python
info = get_device_info()

print(info["device"])
print(info["model"])
print(info["firmware"])
```

Output:

```text
/dev/nvme0n1
SN101
MD220200
```

This approach becomes useful later when automation collects device information and passes it to parsers or validators.

---

# 6. Reusable Utility Functions

Common operations should not be duplicated across many test files.

For example:

```python
def validate_firmware(actual, expected):
    return actual == expected
```

could eventually be placed in a reusable utility module:

```text
utilities/
└── validators.py
```

Then multiple tests can import and reuse the same function.

Conceptually:

```text
Reusable utility
      ↓
Multiple tests
      ↓
Less duplicated logic
      ↓
Easier maintenance
```

This becomes especially important as the automation framework grows.

---

# 7. Exception-Safe Function Design

Automation works with operations that can fail:

```text
File missing
Command failure
Invalid input
Timeout
Device unavailable
SSH failure
```

Functions should handle expected failures deliberately rather than allowing failures to become confusing or hidden.

Example:

```python
def read_file(file_path):

    try:
        with open(file_path, "r") as file:
            return file.read()

    except FileNotFoundError:
        return None
```

The caller can then handle the result:

```python
content = read_file("test.log")

if content is None:
    print("File does not exist")
else:
    print(content)
```

---

# 8. Do Not Hide Failures

Avoid patterns such as:

```python
try:
    # operation
except:
    pass
```

This can silently hide failures.

In test automation, hiding failures is dangerous because the framework might continue without recording the actual problem.

The goal is:

```text
Failure
  ↓
Recognize it
  ↓
Preserve useful information
  ↓
Handle or propagate it correctly
```

Later, the framework will distinguish different failure types such as:

```text
Product failure
Automation failure
Infrastructure failure
Command failure
```

---

# 9. File Handling and Function Design

A useful example is a file-reading utility:

```python
def read_file(file_path):

    try:
        with open(file_path, "r") as file:
            return file.read()

    except FileNotFoundError:
        return None
```

The success and failure results should be understandable to the caller.

Avoid returning unrelated types unless the design explicitly requires it.

For example, returning:

```python
return file.read()
```

on success and:

```python
return exception_object
```

on failure creates two different result types.

For simple utilities, a consistent result such as `None` for "not available" may be easier for the caller to handle.

---

# 10. Modules

A module is a Python file containing reusable code.

Example:

```text
validators.py
```

Contents:

```python
def validate_firmware(actual, expected):
    return actual == expected
```

Another Python file can import it:

```python
from validators import validate_firmware

result = validate_firmware("MD220200", "MD220200")

print(result)
```

This allows reusable automation logic to be separated from test execution code.

---

# 11. Packages

As automation becomes larger, related modules can be organized into packages.

Example:

```text
automation/
├── devices/
├── health/
├── firmware/
├── utilities/
└── tests/
```

For example:

```text
utilities/
├── validators.py
└── file_utils.py
```

This separation helps organize responsibilities.

A framework should not become one large Python file containing every test, utility, parser, and execution function.

---

# 12. Automation-Oriented Thinking

When writing normal Python, the question may be:

> How do I make this program work?

For automation, the question should become:

> How can I make this operation reusable, testable, diagnosable, and safe to execute repeatedly?

For example:

### Less reusable

```python
print("Checking firmware")
```

### More automation-oriented

```python
def validate_firmware(actual, expected):
    return actual == expected
```

This can later fit into a larger flow:

```text
Test
 ↓
Utility
 ↓
Collect Data
 ↓
Validate
 ↓
Result
```

---

# 13. Storage Automation Example

A future Storage Test Automation flow may look like:

```text
Test
 ↓
Device information
 ↓
Validation utility
 ↓
Result
```

For example:

```python
def validate_firmware(actual, expected):
    return actual == expected


actual_firmware = "MD220200"
expected_firmware = "MD220200"

result = validate_firmware(
    actual_firmware,
    expected_firmware
)

if result:
    print("PASS")
else:
    print("FAIL")
```

Later, the actual firmware value will come from a storage command rather than a hardcoded string.

The function itself can remain reusable.

---

# 14. Key Design Principles

## Single Responsibility

A function should have a clear purpose.

Good:

```python
def validate_firmware(actual, expected):
    ...
```

Less desirable:

```python
def run_everything():
    # discover device
    # collect firmware
    # parse output
    # validate temperature
    # run fio
    # collect logs
    # generate report
```

Large workflows can be composed from smaller reusable functions.

---

## Reusability

The function should accept inputs rather than depending unnecessarily on hardcoded values.

Example:

```python
def validate_temperature(actual, maximum):
    return actual <= maximum
```

---

## Clear Return Values

A caller should be able to understand what the function returned and why it matters.

Examples:

```text
True / False
None when data is unavailable
Dictionary containing structured information
```

The exact return design depends on the operation.

---

## Failure Awareness

Automation should not silently hide failures.

The function should either:

```text
Handle an expected failure appropriately
```

or:

```text
Allow the failure to propagate when the caller must deal with it
```

---

# 15. Concepts Covered

```text
✓ Reusable automation functions
✓ Automation-oriented function design
✓ Arguments
✓ Return values
✓ Reusable utility functions
✓ Exception-safe function design
✓ Modules
✓ Packages
✓ Importing reusable utilities
✓ Storage-oriented function examples
```

---

# 16. Core Mental Model

Remember:

```text
Function
   ↓
Input
   ↓
Processing
   ↓
Return Result
```

And for reusable automation:

```text
Reusable Function
       ↓
Multiple Tests
       ↓
Less Duplication
       ↓
Maintainable Automation
```

The objective is not simply to write Python functions.

The objective is to build functions that can later become reliable components of a Storage Test Automation framework.

