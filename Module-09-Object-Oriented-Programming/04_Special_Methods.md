# Special Methods

## 1. What are Special Methods?

**Special methods** are predefined Python methods with names that begin and end with double underscores.

Examples:

```python
__init__()
__str__()
__repr__()
__eq__()
__len__()
```

They allow Python objects to work with built-in language operations.

They are commonly called **dunder methods** because "double underscore" is often shortened to "dunder".

---

# 2. Why Special Methods?

Normally, Python already knows how to perform operations such as:

```python
print()
len()
==
```

Special methods allow our classes to define how those operations should behave for our objects.

Mental model:

```text
Python operation
      ↓
Special method
      ↓
Object-specific behavior
```

---

# 3. Dunder Method Basics

A special method follows the naming pattern:

```python
__name__
```

Examples:

```python
__init__
__str__
__repr__
__eq__
__len__
```

These are not ordinary naming conventions. Python gives these methods special meaning.

---

# 4. `__init__()`

You have already learned `__init__()`.

It is used to initialize an object.

Example:

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number
```

When:

```python
device = StorageDevice("SN1001")
```

the initialization process invokes `__init__()` for that instance.

---

# 5. `__str__()`

`__str__()` defines the human-readable string representation of an object.

Example:

```python
class StorageDevice:

    def __init__(self, serial_number, model):
        self.serial_number = serial_number
        self.model = model

    def __str__(self):
        return f"{self.serial_number} - {self.model}"
```

Now:

```python
device = StorageDevice("SN1001", "NVMeSSD")

print(device)
```

produces:

```text
SN1001 - NVMeSSD
```

---

# 6. Why `__str__()`?

Without a custom `__str__()`, printing an object usually produces a less useful default representation.

With `__str__()`:

```python
print(device)
```

can provide information that is immediately understandable to a human.

This is particularly useful in:

* logs
* debugging
* test output
* reports

---

# 7. `str()` and `__str__()`

When:

```python
print(device)
```

or:

```python
str(device)
```

is used, Python can use the object's `__str__()` method.

Conceptually:

```text
print(device)
      ↓
str(device)
      ↓
device.__str__()
```

---

# 8. Rules for `__str__()`

`__str__()` should return a string.

Correct:

```python
def __str__(self):
    return "Storage Device"
```

Incorrect:

```python
def __str__(self):
    return 123
```

The return value must be a string.

---

# 9. `__repr__()`

`__repr__()` provides a representation intended primarily for developers and debugging.

Example:

```python
class StorageDevice:

    def __init__(self, serial_number, model):
        self.serial_number = serial_number
        self.model = model

    def __repr__(self):
        return (
            f"StorageDevice("
            f"serial_number='{self.serial_number}', "
            f"model='{self.model}')"
        )
```

Now:

```python
device = StorageDevice("SN1001", "NVMeSSD")

print(repr(device))
```

may produce:

```text
StorageDevice(serial_number='SN1001', model='NVMeSSD')
```

---

# 10. `__str__()` vs `__repr__()`

The main distinction is:

```text
__str__()
→ human-readable representation

__repr__()
→ developer/debugging representation
```

Example:

```text
__str__
→ SN1001 - NVMeSSD

__repr__
→ StorageDevice(serial_number='SN1001', model='NVMeSSD')
```

---

# 11. Why `__repr__()` is Useful in Automation

Suppose a pytest failure contains:

```python
print(device)
```

A useful `__str__()` can give a readable message.

During debugging, a more detailed `__repr__()` can make object state easier to understand.

Example:

```text
StorageDevice(serial_number='SN1001', model='NVMeSSD')
```

is much more useful than an opaque object address.

---

# 12. `__eq__()`

`__eq__()` defines how equality using `==` behaves between objects.

Example:

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number

    def __eq__(self, other):
        return self.serial_number == other.serial_number
```

Now:

```python
device1 = StorageDevice("SN1001")
device2 = StorageDevice("SN1001")

print(device1 == device2)
```

can produce:

```text
True
```

because both represent the same serial number according to our definition.

---

# 13. Equality is About Logical Value

Without customizing equality, two separately created objects may not be considered equal simply because they contain the same information.

With `__eq__()`, we define what "equal" means for the object.

For a storage device, a logical identity might be based on:

```text
Serial Number
```

or another domain-specific identifier.

The definition depends on the application's requirements.

---

# 14. `__eq__()` Example

```python
class StorageDevice:

    def __init__(self, serial_number, model):
        self.serial_number = serial_number
        self.model = model

    def __eq__(self, other):
        if not isinstance(other, StorageDevice):
            return NotImplemented

        return (
            self.serial_number == other.serial_number
            and self.model == other.model
        )
```

Now:

```python
device1 = StorageDevice("SN1001", "NVMeSSD")
device2 = StorageDevice("SN1001", "NVMeSSD")

print(device1 == device2)
```

returns:

```text
True
```

---

# 15. Why Check the Type?

Consider:

```python
device == "SN1001"
```

The other value is not a `StorageDevice`.

A defensive implementation can check:

```python
if not isinstance(other, StorageDevice):
    return NotImplemented
```

This avoids blindly assuming that `other` has the attributes our comparison expects.

---

# 16. `__len__()`

`__len__()` defines what `len(object)` should return.

Example:

```python
class StorageDevice:

    def __init__(self):
        self.partitions = []

    def __len__(self):
        return len(self.partitions)
```

Now:

```python
device = StorageDevice()

device.partitions.append("partition1")
device.partitions.append("partition2")

print(len(device))
```

returns:

```text
2
```

---

# 17. Why `__len__()`?

It allows our object to participate naturally in Python's `len()` operation.

Conceptually:

```text
len(device)
     ↓
device.__len__()
```

The meaning depends on the object.

For example, for a storage-device abstraction, it might represent:

```text
number of partitions
```

if that is what the class defines.

---

# 18. Complete Example

```python
class StorageDevice:

    def __init__(self, serial_number, model):
        self.serial_number = serial_number
        self.model = model
        self.partitions = []

    def __str__(self):
        return f"{self.serial_number} - {self.model}"

    def __repr__(self):
        return (
            f"StorageDevice("
            f"serial_number='{self.serial_number}', "
            f"model='{self.model}')"
        )

    def __eq__(self, other):
        if not isinstance(other, StorageDevice):
            return NotImplemented

        return (
            self.serial_number == other.serial_number
            and self.model == other.model
        )

    def __len__(self):
        return len(self.partitions)
```

Usage:

```python
device1 = StorageDevice("SN1001", "NVMeSSD")
device2 = StorageDevice("SN1001", "NVMeSSD")

device1.partitions.append("p1")
device1.partitions.append("p2")

print(device1)
print(repr(device1))
print(device1 == device2)
print(len(device1))
```

Possible output:

```text
SN1001 - NVMeSSD
StorageDevice(serial_number='SN1001', model='NVMeSSD')
True
2
```

---

# 19. Special Methods and Python Operators

Special methods connect Python syntax and operations to our class behavior.

Examples:

```text
Operation        Special Method

object creation  __init__()
str(object)      __str__()
repr(object)     __repr__()
a == b           __eq__()
len(object)      __len__()
```

This allows custom classes to behave more naturally like built-in Python objects.

---

# 20. `__str__()` vs `__repr__()` Practical Rule

When designing an object, think:

### `__str__()`

Ask:

> "What would be useful for a person reading logs or output?"

Example:

```text
SN1001 - NVMeSSD
```

### `__repr__()`

Ask:

> "What would help a developer understand exactly what this object contains?"

Example:

```text
StorageDevice(serial_number='SN1001', model='NVMeSSD')
```

---

# 21. Special Methods and Automation

Special methods are useful in automation because automation deals with many objects and results.

For example:

```python
print(device)
```

can make logs readable.

```python
print(result)
```

can make validation output clearer.

```python
device1 == device2
```

can compare logical device representations.

```python
len(device)
```

can expose a meaningful object-level count when appropriate.

---

# 22. Special Methods and pytest

Special methods can make pytest failures and debugging more understandable.

For example:

```python
assert actual_device == expected_device
```

can use `__eq__()` to perform logical comparison.

Similarly, a useful `__repr__()` can make assertion failure output easier to understand.

The important point is that special methods can improve the readability and usefulness of test objects.

---

# 23. Common Mistakes

## Mistake 1 — Returning the wrong type from `__str__()`

`__str__()` must return a string.

---

## Mistake 2 — Making `__eq__()` assume every object has the same attributes

Use an appropriate type or capability check.

---

## Mistake 3 — Confusing `__str__()` and `__repr__()`

Remember:

```text
__str__
→ user/human-readable

__repr__
→ developer/debugging-oriented
```

---

## Mistake 4 — Using special methods without a meaningful object design

Do not implement special methods merely because they exist.

There should be a meaningful behavior associated with the object.

---

# 24. Special Method Basics

Special methods are part of Python's object model.

They allow user-defined classes to participate in standard Python operations.

Examples covered here:

```text
__init__()
__str__()
__repr__()
__eq__()
__len__()
```

There are many more special methods in Python, but we focus here on the ones required by this OOP roadmap.

---

# 25. Storage Automation Example

Imagine an automation framework produces a validation result:

```python
class ValidationResult:

    def __init__(self, test_name, status):
        self.test_name = test_name
        self.status = status

    def __str__(self):
        return f"{self.test_name}: {self.status}"

    def __repr__(self):
        return (
            f"ValidationResult("
            f"test_name='{self.test_name}', "
            f"status='{self.status}')"
        )
```

Then:

```python
result = ValidationResult(
    "NVMe Health Validation",
    "PASS"
)

print(result)
```

can produce:

```text
NVMe Health Validation: PASS
```

while:

```python
repr(result)
```

can provide the detailed developer representation.

This demonstrates how special methods can make automation objects easier to use and debug.

---

# 26. Key Takeaways

```text
Special Method
→ Python-defined method with special meaning

Dunder Method
→ Common name for __method__ style methods

__init__()
→ Initialize object

__str__()
→ Human-readable representation

__repr__()
→ Developer/debugging representation

__eq__()
→ Define equality using ==

__len__()
→ Define behavior of len()
```

---

# 27. Final Mental Model

```text
Python Operation
       ↓
Special Method
       ↓
Object-Specific Behavior
```

Examples:

```text
print(device)
      ↓
__str__()

repr(device)
      ↓
__repr__()

device1 == device2
      ↓
__eq__()

len(device)
      ↓
__len__()
```

The main principle is:

> **Special methods allow your objects to participate naturally in Python's built-in operations.**

