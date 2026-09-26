# Object-Oriented Programming Fundamentals

## 1. What is OOP?

**Object-Oriented Programming (OOP)** is a programming approach where software is organized around **objects**.

An object combines:

```text
Data
+
Behavior
```

The data represents the object's state, while the behavior represents what the object can do.

---

# 2. Why OOP?

Without OOP, a program can become difficult to organize as it grows.

For example, a storage automation program may need to maintain information such as:

```text
Device
Serial Number
Model
Firmware
Temperature
Health
Capacity
```

and operations such as:

```text
Identify
Check Health
Reset
Collect Information
Validate
```

OOP allows related data and behavior to be organized together.

---

# 3. Class

A **class** is a blueprint or definition used to create objects.

Example:

```python
class StorageDevice:
    pass
```

The class describes what a `StorageDevice` object can contain or do.

At this point, no actual storage device object has been created.

---

# 4. Object

An **object** is an instance of a class.

Example:

```python
class StorageDevice:
    pass


device = StorageDevice()
```

Here:

```text
StorageDevice
     ↓
    class

device
     ↓
   object
```

`device` is an object created from the `StorageDevice` class.

---

# 5. Class vs Object

## Class

A class defines the structure and behavior.

```python
class StorageDevice:
    pass
```

## Object

An object is a concrete instance of that class.

```python
device1 = StorageDevice()
device2 = StorageDevice()
```

Now:

```text
StorageDevice
   ├── device1
   └── device2
```

Both objects belong to the same class.

---

# 6. Attributes

An **attribute** is data associated with an object or class.

Example:

```python
class StorageDevice:

    def __init__(self, model, capacity):
        self.model = model
        self.capacity = capacity
```

Create an object:

```python
device = StorageDevice("EnterpriseSSD", "1TB")
```

The object now has:

```text
model = EnterpriseSSD
capacity = 1TB
```

These are attributes of the object.

---

# 7. Instance Attributes

An **instance attribute** belongs to a particular object.

Example:

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number
```

Create two objects:

```python
device1 = StorageDevice("SN1001")
device2 = StorageDevice("SN1002")
```

Now:

```text
device1.serial_number → SN1001

device2.serial_number → SN1002
```

Each object has its own value.

---

# 8. Class Attributes

A **class attribute** belongs to the class and is shared unless an instance overrides it.

Example:

```python
class StorageDevice:

    device_type = "Storage Device"
```

Every object can access it:

```python
device1 = StorageDevice()
device2 = StorageDevice()

print(device1.device_type)
print(device2.device_type)
```

Both obtain:

```text
Storage Device
```

Mental model:

```text
Class Attribute
      ↓
Shared by instances
```

while:

```text
Instance Attribute
      ↓
Belongs to a particular object
```

---

# 9. Methods

A **method** is a function defined inside a class.

Example:

```python
class StorageDevice:

    def identify(self):
        print("Identifying storage device")
```

Create an object:

```python
device = StorageDevice()
```

Call the method:

```python
device.identify()
```

Output:

```text
Identifying storage device
```

Methods represent behavior associated with an object.

---

# 10. `self`

`self` refers to the **current object instance**.

Example:

```python
class StorageDevice:

    def identify(self):
        print(self)
```

When:

```python
device = StorageDevice()
device.identify()
```

`self` refers to:

```text
device
```

So `self` allows a method to access the current object's attributes and other methods.

---

# 11. Using `self` with Attributes

Example:

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number

    def show_serial(self):
        print(self.serial_number)
```

Create:

```python
device = StorageDevice("SN1001")
device.show_serial()
```

The method accesses the attribute belonging to that particular object.

---

# 12. Constructor

A constructor-related initialization method is used to initialize an object when it is created.

In Python, the commonly used initialization method is:

```python
__init__()
```

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

Python calls `__init__()` for the newly created instance.

---

# 13. `__init__()`

`__init__()` is used to initialize instance state.

Example:

```python
class StorageDevice:

    def __init__(self, serial_number, model):
        self.serial_number = serial_number
        self.model = model
```

Create:

```python
device = StorageDevice("SN1001", "NVMe-Enterprise")
```

The resulting object contains:

```text
serial_number = SN1001
model = NVMe-Enterprise
```

---

# 14. Object Initialization

Object initialization means establishing the initial state of an object when it is created.

Example:

```python
class StorageDevice:

    def __init__(self, serial_number, temperature):
        self.serial_number = serial_number
        self.temperature = temperature
```

Creating the object:

```python
device = StorageDevice("SN1001", 35)
```

initializes:

```text
serial_number → SN1001
temperature   → 35
```

---

# 15. Class State vs Instance State

This distinction is important.

### Instance state

Belongs to one specific object.

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number
```

```text
device1 → SN1001
device2 → SN1002
```

### Class state

Belongs to the class.

```python
class StorageDevice:

    device_type = "NVMe"
```

Conceptually:

```text
Class State
     ↓
shared class-level information

Instance State
     ↓
object-specific information
```

---

# 16. Attribute Lookup

When Python evaluates:

```python
device.serial_number
```

it looks for the attribute associated with that object.

For a class/instance lookup, Python considers the object's available attributes and then the class and its inheritance hierarchy as applicable.

A simple example:

```python
class StorageDevice:

    device_type = "Storage"

device = StorageDevice()
```

There is no `device_type` created directly on `device`, but:

```python
print(device.device_type)
```

can still access the class attribute.

---

# 17. Simple Complete Example

```python
class StorageDevice:

    device_type = "Storage Device"

    def __init__(self, serial_number, model):
        self.serial_number = serial_number
        self.model = model

    def identify(self):
        print("Serial:", self.serial_number)
        print("Model:", self.model)


device = StorageDevice("SN1001", "EnterpriseNVMe")

print(device.device_type)

device.identify()
```

Possible output:

```text
Storage Device
Serial: SN1001
Model: EnterpriseNVMe
```

---

# 18. Multiple Objects

A class can create many independent objects.

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number

    def identify(self):
        print(self.serial_number)


device1 = StorageDevice("SN1001")
device2 = StorageDevice("SN1002")

device1.identify()
device2.identify()
```

Output:

```text
SN1001
SN1002
```

The same class defines the behavior, while each object maintains its own instance state.

---

# 19. OOP Mental Model

Think of a storage device object as:

```text
Object
│
├── State
│   ├── serial_number
│   ├── model
│   └── temperature
│
└── Behavior
    ├── identify()
    ├── check_health()
    └── reset()
```

The class defines the structure and behavior from which such objects are created.

---

# 20. Key Concepts

```text
Class
→ Blueprint / definition

Object
→ Instance of a class

Attribute
→ Data associated with an object or class

Instance Attribute
→ Object-specific data

Class Attribute
→ Class-level data

Method
→ Function defined inside a class

self
→ Current object instance

__init__()
→ Object initialization method
```

---

# 21. Storage Automation Connection

These fundamentals later allow us to model automation components as objects.

For example:

```python
class StorageDevice:
    ...

class NVMeDevice:
    ...

class LogParser:
    ...

class Validator:
    ...

class TestRunner:
    ...
```

The purpose is not to turn every small piece of code into a class.

OOP is useful when an object provides a meaningful combination of:

```text
State
+
Behavior
+
Responsibility
```

This becomes important when designing the reusable automation components later in the automation track.

---

# 22. Important Distinctions

### Class vs Object

```text
Class
→ definition

Object
→ instance
```

### Instance Attribute vs Class Attribute

```text
Instance Attribute
→ object-specific

Class Attribute
→ class-level/shared
```

### Function vs Method

```text
Function
→ defined independently

Method
→ defined inside a class
```

### Object State vs Object Behavior

```text
State
→ attributes

Behavior
→ methods
```

---

# 23. Final Mental Model

```text
                    CLASS
                      │
        ┌─────────────┴─────────────┐
        ↓                           ↓
      State                      Behavior
   (Attributes)                  (Methods)
        │                           │
        └─────────────┬─────────────┘
                      ↓
                   OBJECT
                      │
                      ↓
              Specific Instance
```

The fundamental idea of OOP is:

> **Organize related state and behavior into objects with clearly defined responsibilities.**

