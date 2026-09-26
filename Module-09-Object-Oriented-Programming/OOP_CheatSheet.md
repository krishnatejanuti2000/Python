# OOP Cheat Sheet

## 1. OOP Fundamentals

| Concept            | Meaning                                  |
| ------------------ | ---------------------------------------- |
| Class              | Blueprint / definition for objects       |
| Object             | Instance of a class                      |
| Attribute          | Data associated with object or class     |
| Instance Attribute | Attribute belonging to a specific object |
| Class Attribute    | Attribute associated with the class      |
| Method             | Function defined inside a class          |
| `self`             | Current object instance                  |
| `__init__()`       | Object initialization method             |

---

# 2. Encapsulation

```text
Encapsulation
→ Package data + behavior
→ Control access to internal state
```

### Access conventions

```text
name
→ Public

_name
→ Protected/internal convention

__name
→ Name mangling
```

### Property

```python
@property
def value(self):
    return self._value
```

### Setter

```python
@value.setter
def value(self, new_value):
    ...
```

### Core idea

```text
External Code
      ↓
Controlled Interface
      ↓
Internal State
```

---

# 3. Methods

## Instance Method

```python
def identify(self):
    ...
```

```text
Uses self
→ Object-specific behavior
```

## Class Method

```python
@classmethod
def get_count(cls):
    ...
```

```text
Uses cls
→ Class-level behavior
```

## Static Method

```python
@staticmethod
def validate_serial(serial):
    ...
```

```text
No automatic self / cls
→ Independent logic related to the class
```

### Quick Rule

```text
Needs object state
→ Instance Method

Needs class state
→ Class Method

Needs neither
→ Static Method
```

---

# 4. Special Methods

```text
__init__()
→ Initialize object

__str__()
→ Human-readable representation

__repr__()
→ Developer/debug representation

__eq__()
→ Equality using ==

__len__()
→ Behavior of len()
```

### Mental model

```text
Python Operation
      ↓
Special Method
      ↓
Custom Object Behavior
```

---

# 5. Identity vs Equality

## `is`

Checks identity:

```python
a is b
```

Meaning:

```text
Are these the exact same object?
```

## `==`

Checks equality:

```python
a == b
```

Meaning:

```text
Do these values compare as equal?
```

## `id()`

```python
id(obj)
```

Returns a Python object identity value during its lifetime.

It is **not**:

```text
SSD serial number
WWN
NQN
Namespace ID
PCIe address
```

### Remember

```text
is
→ Identity

==
→ Equality
```

---

# 6. Inheritance

```text
Child
  IS-A
Parent
```

Example:

```python
class StorageDevice:
    pass


class NVMeDevice(StorageDevice):
    pass
```

### Important concepts

```text
Parent / Base Class
Child / Derived Class
Method Inheritance
Method Overriding
super()
Constructor Inheritance
isinstance()
issubclass()
```

---

# 7. `super()`

Used to access the next implementation in the inheritance hierarchy according to Python's MRO.

Example:

```python
class StorageDevice:

    def __init__(self, serial):
        self.serial = serial


class NVMeDevice(StorageDevice):

    def __init__(self, serial, namespaces):
        super().__init__(serial)
        self.namespaces = namespaces
```

---

# 8. `isinstance()` vs `issubclass()`

```python
isinstance(object, Class)
```

```text
Checks object relationship
```

```python
issubclass(ChildClass, ParentClass)
```

```text
Checks class inheritance relationship
```

---

# 9. Types of Inheritance

### Single

```text
A
↓
B
```

### Multilevel

```text
A
↓
B
↓
C
```

### Hierarchical

```text
      A
     / \
    B   C
```

### Multiple

```text
A   B
 \ /
  C
```

---

# 10. MRO

**MRO = Method Resolution Order**

It determines the order Python follows when looking for methods and attributes.

Inspect using:

```python
ClassName.mro()
```

or:

```python
ClassName.__mro__
```

Important with multiple inheritance.

---

# 11. Polymorphism

```text
Same operation
      ↓
Different objects
      ↓
Different behavior
```

Example:

```python
def check_health(device):
    return device.check_health()
```

The function can work with different compatible objects.

---

# 12. Method Overriding

Parent:

```python
class StorageDevice:

    def identify(self):
        print("Generic")
```

Child:

```python
class NVMeDevice(StorageDevice):

    def identify(self):
        print("NVMe")
```

The child provides its own implementation.

---

# 13. Common Interface

Different objects provide common operations:

```text
identify()
check_health()
reset()
```

The implementations can be different.

---

# 14. Duck Typing

Python focuses on what an object **can do** rather than requiring a specific inheritance relationship.

```python
def run_check(device):
    device.check_health()
```

Any compatible object providing `check_health()` can potentially be used.

```text
Inheritance not required
```

---

# 15. Abstraction

```text
WHAT
→ Expose required behavior

HOW
→ Hide unnecessary implementation details
```

Example:

```python
device.check_health()
```

The caller does not need to know every internal step used to obtain the health information.

---

# 16. Abstract Base Class

```python
from abc import ABC, abstractmethod
```

Example:

```python
class StorageDevice(ABC):

    @abstractmethod
    def check_health(self):
        pass
```

### `ABC`

Provides the Abstract Base Class mechanism.

### `@abstractmethod`

Marks required abstract behavior.

### Concrete Class

Implements all required abstract methods and can then be instantiated.

---

# 17. Composition

```text
HAS-A
```

Example:

```python
class StorageDevice:

    def __init__(self, runner):
        self.runner = runner
```

Relationship:

```text
StorageDevice
     HAS-A
CommandRunner
```

---

# 18. Aggregation

Also:

```text
HAS-A
```

but the associated object can exist independently.

```text
Company
   ↓
uses
   ↓
Employee
```

The employee can exist independently of the company object.

---

# 19. Composition vs Inheritance

```text
IS-A
→ Inheritance

HAS-A
→ Composition / Aggregation
```

Example:

```text
NVMeDevice
    IS-A
StorageDevice
```

but:

```text
NVMeDevice
    HAS-A
CommandRunner
```

---

# 20. Dependency

A dependency is something an object needs to perform its responsibility.

Example:

```text
StorageDevice
      ↓
needs
      ↓
CommandRunner
```

---

# 21. Dependency Injection

Dependency Injection means supplying the dependency from outside rather than creating it internally.

### Tight coupling

```python
class StorageDevice:

    def __init__(self):
        self.runner = CommandRunner()
```

### Dependency Injection

```python
class StorageDevice:

    def __init__(self, runner):
        self.runner = runner
```

Usage:

```python
runner = CommandRunner()

device = StorageDevice(runner)
```

---

# 22. Constructor Injection

```python
class StorageDevice:

    def __init__(self, runner):
        self.runner = runner
```

Dependency supplied through `__init__()`.

This is the main DI pattern relevant to our automation framework.

---

# 23. Why Dependency Injection?

```text
Dependency Injection
       ↓
Lower Coupling
       ↓
Replaceable Dependencies
       ↓
Better Testability
```

Example:

```text
Production
    ↓
RealCommandRunner
```

Testing:

```text
Test
 ↓
MockCommandRunner
```

---

# 24. OOP Design Rules

### Single Responsibility

A class should have a clear, focused responsibility.

### High Cohesion

The responsibilities inside a class should strongly belong together.

### Low Coupling

Avoid unnecessary strong dependencies between components.

### Favor Composition Where Appropriate

Do not use inheritance merely for code reuse.

Choose based on:

```text
IS-A
vs
HAS-A
```

### Testable Design

Dependencies should be controllable when necessary.

---

# 25. Storage Automation OOP Model

A possible model:

```text
                    Test
                     │
                     ↓
                  Validator
                     │
                     ↓
                StorageDevice
                     │
                   HAS-A
                     ↓
                CommandRunner
                     │
                     ↓
                   Linux
                     │
                     ↓
              Storage CLI Tool
                     │
                     ↓
               Storage Device
```

For remote execution:

```text
Test
 ↓
Validator
 ↓
NVMeDevice
 ↓
SSH / Paramiko
 ↓
Remote Linux
 ↓
nvme-cli
 ↓
NVMe SSD
```

---

# 26. Choosing the Right OOP Concept

```text
Need object-specific behavior?
→ Instance Method

Need class-level behavior?
→ Class Method

Need independent utility logic?
→ Static Method

Need an IS-A relationship?
→ Inheritance

Need different implementations?
→ Polymorphism

Need to hide implementation details?
→ Abstraction

Need controlled state access?
→ Encapsulation

Need a HAS-A relationship?
→ Composition / Aggregation

Need externally replaceable dependency?
→ Dependency Injection
```

---

# 27. Interview One-Liners

```text
Class
→ Blueprint for objects.

Object
→ Instance of a class.

Encapsulation
→ Controlled access to object state and behavior.

Inheritance
→ Deriving one class from another.

Polymorphism
→ Same operation, different object-specific behavior.

Abstraction
→ Expose required behavior while hiding unnecessary implementation.

Composition
→ HAS-A relationship.

Aggregation
→ HAS-A relationship with independent object lifetime.

Dependency
→ Something an object needs.

Dependency Injection
→ Supplying that dependency from outside.

MRO
→ Method Resolution Order.

is
→ Identity comparison.

==
→ Equality comparison.
```

---

# 28. Storage Interview Examples

### Inheritance

```text
NVMeDevice IS-A StorageDevice
```

### Composition

```text
StorageDevice HAS-A CommandRunner
```

### Encapsulation

```text
health_status
→ controlled property
```

### Polymorphism

```text
NVMeDevice.check_health()
SATADevice.check_health()
MockDevice.check_health()
```

### Abstraction

```text
device.check_health()
```

without exposing all command/parsing details.

### Dependency Injection

```text
StorageDevice
       ↓
receives
       ↓
CommandRunner
```

---

# 29. Final OOP Mental Model

```text
                    OOP
                     │
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
     State         Behavior     Relationships
       │             │             │
       ↓             ↓             ↓
 Attributes        Methods      IS-A / HAS-A
       │                           │
       ↓                           ↓
 Encapsulation              Inheritance /
                            Composition
                                  │
                                  ↓
                         Polymorphism /
                         Abstraction /
                       Dependency Injection
```

---

# 30. Most Important Rules

```text
1. Class defines.
2. Object represents a specific instance.
3. self refers to the current object.
4. Encapsulation controls access.
5. is checks identity.
6. == checks equality.
7. Inheritance represents IS-A.
8. Composition represents HAS-A.
9. Polymorphism allows common operations with different behavior.
10. Abstraction focuses on WHAT rather than unnecessary HOW.
11. Dependency Injection supplies dependencies externally.
12. Use OOP when it improves structure, reuse, maintainability, or testability.
13. Do not force OOP concepts where simple functions are sufficient.
```

---

# Storage Automation Principle

The objective of OOP in our automation work is not:

```text
"Use as many OOP features as possible."
```

The objective is:

```text
Clear Responsibilities
        ↓
Reusable Components
        ↓
Low Coupling
        ↓
Testable Design
        ↓
Maintainable Automation
```

