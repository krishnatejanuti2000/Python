# Encapsulation

## 1. What is Encapsulation?

**Encapsulation** is the concept of keeping an object's data and the methods that operate on that data together, while controlling how that data is accessed or modified.

The main idea is:

```text
Object
│
├── Data
└── Methods
       ↓
Controlled Access
```

Encapsulation helps prevent uncontrolled modification of an object's internal state.

---

# 2. Why Encapsulation?

Consider a storage device object.

It may contain:

```text
Serial Number
Temperature
Health Status
Firmware Version
```

Some values should not be changed arbitrarily.

For example:

```text
Temperature → should be within valid range
Health Status → should not be directly modified
```

Without controlled access, any part of the program could potentially modify internal state incorrectly.

Encapsulation provides a boundary around that state.

---

# 3. Public Attributes and Methods

A **public** attribute or method can be accessed normally from outside the class.

Example:

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number

    def identify(self):
        print(self.serial_number)
```

Usage:

```python
device = StorageDevice("SN1001")

print(device.serial_number)

device.identify()
```

Both are publicly accessible.

---

# 4. Public Attribute

Example:

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number
```

The attribute:

```python
self.serial_number
```

is public.

It can be accessed and modified:

```python
device.serial_number = "SN2001"
```

Python does not prevent this.

---

# 5. Public Method

Example:

```python
class StorageDevice:

    def identify(self):
        print("Storage device identified")
```

It can be called directly:

```python
device.identify()
```

Public methods are intended to form part of the object's usable interface.

---

# 6. Protected Attributes and Methods

Python uses a leading underscore:

```python
_name
```

to indicate that an attribute or method is intended to be **protected/internal**.

Example:

```python
class StorageDevice:

    def __init__(self, temperature):
        self._temperature = temperature
```

The underscore communicates:

> This is intended for internal or subclass use.

---

# 7. Important Point About Protected Members

Python does **not** enforce protected access like some other languages.

This is still technically possible:

```python
print(device._temperature)
```

The underscore is primarily a convention.

Therefore:

```text
_ name
↓
"Treat this as internal"
```

not:

```text
"Python will prevent access"
```

---

# 8. Protected Method

Example:

```python
class StorageDevice:

    def _validate_temperature(self):
        print("Validating temperature")
```

The leading underscore indicates that the method is intended to be internal rather than part of the main public interface.

---

# 9. Private Attributes and Methods

Python uses double leading underscores:

```python
__name
```

for name mangling.

Example:

```python
class StorageDevice:

    def __init__(self, health_status):
        self.__health_status = health_status
```

The attribute is intended to be private to the class implementation.

---

# 10. Name Mangling

Python performs **name mangling** for double-underscore attributes.

For:

```python
self.__health_status
```

inside:

```python
class StorageDevice:
```

Python internally changes the name approximately to:

```text
_StorageDevice__health_status
```

Therefore:

```python
device.__health_status
```

does not directly refer to the original mangled attribute.

---

# 11. Name Mangling Example

```python
class StorageDevice:

    def __init__(self):
        self.__health_status = "PASS"
```

The internally mangled name is conceptually:

```text
_StorageDevice__health_status
```

So the class can access:

```python
self.__health_status
```

while the original attribute name is transformed internally.

---

# 12. Private Does Not Mean True Security

Python's double underscore is **not a security mechanism**.

Name mangling mainly prevents accidental name conflicts and discourages direct access.

It does not make data cryptographically secure or completely inaccessible.

For example, technically:

```python
device._StorageDevice__health_status
```

can access the mangled attribute.

Therefore:

```text
Private in Python
≠
absolute inaccessible memory
```

---

# 13. Properties

A property allows controlled access to an attribute through normal attribute syntax.

Example:

```python
class StorageDevice:

    def __init__(self, health_status):
        self.__health_status = health_status

    @property
    def health_status(self):
        return self.__health_status
```

Now:

```python
device = StorageDevice("PASS")

print(device.health_status)
```

The caller accesses:

```python
device.health_status
```

instead of directly accessing:

```python
device.__health_status
```

---

# 14. Read-Only Property

A property without a setter can provide read-only access.

Example:

```python
class StorageDevice:

    def __init__(self, health_status):
        self.__health_status = health_status

    @property
    def health_status(self):
        return self.__health_status
```

Usage:

```python
device = StorageDevice("PASS")

print(device.health_status)
```

But:

```python
device.health_status = "FAILED"
```

will fail because no setter has been provided.

This is useful when the class should control how its internal state changes.

---

# 15. Getters

A getter provides controlled access to internal data.

Example:

```python
class StorageDevice:

    def __init__(self, health_status):
        self.__health_status = health_status

    def get_health_status(self):
        return self.__health_status
```

Usage:

```python
print(device.get_health_status())
```

Python properties often provide a cleaner interface:

```python
print(device.health_status)
```

---

# 16. Setters

A setter provides controlled modification of internal data.

Example:

```python
class StorageDevice:

    def __init__(self, temperature):
        self.__temperature = temperature

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, new_temperature):
        self.__temperature = new_temperature
```

Now:

```python
device.temperature = 40
```

passes through the setter.

---

# 17. Controlled Access

The major purpose of a setter is that we can validate data before changing internal state.

Example:

```python
class StorageDevice:

    def __init__(self, temperature):
        self.__temperature = temperature

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, new_temperature):

        if new_temperature < 0 or new_temperature > 100:
            raise ValueError(
                "Temperature must be between 0 and 100"
            )

        self.__temperature = new_temperature
```

Now:

```python
device.temperature = 50
```

is valid.

But:

```python
device.temperature = 150
```

raises an exception.

---

# 18. Why Validate in the Setter?

Without controlled access:

```python
device.temperature = 150
```

could create an invalid object state.

With a setter:

```text
New Value
   ↓
Validation
   ↓
Valid?
 ┌─┴─┐
Yes No
 ↓   ↓
Store Error
```

The object protects its state.

---

# 19. Validate Initial State Too

A common mistake is to validate only later assignments.

For example:

```python
class StorageDevice:

    def __init__(self, temperature):
        self._temperature = temperature

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, new_temperature):
        if new_temperature < 0 or new_temperature > 100:
            raise ValueError("Invalid temperature")

        self._temperature = new_temperature
```

If the constructor directly does:

```python
self._temperature = temperature
```

the setter is bypassed.

A better approach is:

```python
self.temperature = temperature
```

so initialization also goes through validation.

---

# 20. Encapsulation Example — Storage Health

Consider:

```python
class StorageDevice:

    def __init__(self, health_status):
        self.__health_status = health_status

    @property
    def health_status(self):
        return self.__health_status
```

The caller can read:

```python
device.health_status
```

but cannot intentionally change the internal health state through the public property.

This establishes:

```text
Internal State
      ↓
Controlled Interface
      ↓
External Code
```

---

# 21. The Interface vs Internal Implementation

Encapsulation allows us to expose a simple interface while hiding implementation details.

For example:

```python
device.health_status
```

The caller does not need to know whether the value comes from:

```text
internal variable
database
device command
cache
calculation
```

The implementation can change while the external interface remains stable.

This idea becomes important later when designing automation components.

---

# 22. Encapsulation Example for Storage Automation

Suppose we create:

```python
class NVMeDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.__health_status = None
```

The object may later internally update:

```python
self.__health_status
```

through controlled methods or properties.

The test code can interact with:

```python
device.health_status
```

rather than modifying the internal state directly.

---

# 23. Public vs Protected vs Private

```text
Public
↓
name

Protected
↓
_name

Private
↓
__name
```

Meaning:

### Public

```text
Normal external access
```

### Protected

```text
Internal-use convention
```

### Private

```text
Name mangling
+ intended restricted internal access
```

---

# 24. Encapsulation Does Not Mean "Hide Everything"

Encapsulation does not mean every attribute must be private.

Good design decides which information should be exposed.

For example:

```text
serial_number
model
```

may reasonably be public/read-only.

While:

```text
internal health state
internal validation state
internal implementation data
```

may need controlled access.

The goal is:

> **Expose what users of the object need and control what must be protected.**

---

# 25. Encapsulation vs Abstraction

These concepts are related but different.

### Encapsulation

Focuses on:

```text
How data/state is packaged and accessed
```

### Abstraction

Focuses on:

```text
What functionality is exposed
while hiding implementation details
```

Simple mental distinction:

```text
Encapsulation
→ Control access to state/behavior

Abstraction
→ Hide unnecessary implementation complexity
```

Abstraction will be covered separately in this module.

---

# 26. Encapsulation and OOP Design

Encapsulation supports:

* Controlled state changes
* Validation
* Reduced accidental modification
* Clear interfaces
* Better maintainability
* Better separation between internal implementation and external usage

---

# 27. Storage Example — Complete

```python
class StorageDevice:

    def __init__(self, serial_number, temperature, health_status):
        self.serial_number = serial_number
        self.temperature = temperature
        self.__health_status = health_status

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, new_temperature):
        if new_temperature < 0 or new_temperature > 100:
            raise ValueError(
                "Temperature must be between 0 and 100"
            )

        self._temperature = new_temperature

    @property
    def health_status(self):
        return self.__health_status
```

The object provides:

```text
Public
→ serial_number

Controlled
→ temperature

Read-only property
→ health_status
```

---

# 28. Important Python Behavior

Consider:

```python
device.__health_status = "FAILED"
```

This does **not** modify the original:

```python
self.__health_status
```

inside the `StorageDevice` class.

Because the original private-style attribute is name-mangled.

The statement may create a different attribute on the instance.

This distinction is important when working with Python's private naming convention.

---

# 29. Name Mangling Example

```python
class StorageDevice:

    def __init__(self):
        self.__health_status = "PASS"


device = StorageDevice()

device.__health_status = "FAILED"

print(device.__health_status)
```

The value displayed by:

```python
device.__health_status
```

can be:

```text
FAILED
```

while the original internal attribute can still contain:

```text
PASS
```

because these are different attributes due to name mangling.

This is why controlled properties are preferable to manipulating private-style attributes directly.

---

# 30. Storage Automation Relevance

Encapsulation becomes particularly useful when an automation object represents a storage resource.

For example:

```text
NVMeDevice
│
├── serial_number
├── model
├── firmware
├── temperature
├── health_status
│
└── methods
    ├── identify()
    ├── check_health()
    └── reset()
```

The object should control how important state is modified.

This helps prevent tests and utilities from randomly changing internal state.

---

# 31. Key Takeaways

```text
Encapsulation
→ Package data and behavior together
→ Control access to internal state

Public
→ normal access

Protected (_name)
→ convention for internal use

Private (__name)
→ name mangling

Name Mangling
→ __name becomes approximately _ClassName__name

Property
→ controlled attribute-style access

Getter
→ read controlled internal state

Setter
→ modify controlled internal state

Controlled Access
→ validate before changing state
```

---

# 32. Final Mental Model

```text
                OBJECT
                   │
        ┌──────────┴──────────┐
        ↓                     ↓
     Internal               Public
      State                 Interface
        │                     │
        ↓                     ↓
   Protected /              Methods /
    Private                 Properties
        │                     │
        └──────────┬──────────┘
                   ↓
            Controlled Access
```

The main principle is:

> **An object should control how its important internal state is accessed and modified.**

