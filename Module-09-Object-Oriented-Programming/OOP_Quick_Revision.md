# OOP Quick Revision

## OOP Basics

```text
Class
→ Blueprint / definition

Object
→ Instance of a class

Attribute
→ Data / state

Method
→ Behavior

self
→ Current object instance

__init__()
→ Object initialization
```

---

## Encapsulation

```text
Encapsulation
→ Package data + behavior
→ Control access to internal state
```

```text
name
→ Public

_name
→ Protected/internal convention

__name
→ Name mangling
```

```text
@property
→ Controlled attribute access

@property + setter
→ Controlled read/write access
```

Remember:

```text
Private in Python
≠
absolute security
```

---

## Methods

```text
Instance Method
→ self
→ Object state

Class Method
→ cls
→ Class state

Static Method
→ No automatic self/cls
→ Independent related logic
```

### Rule

```text
Needs object state
→ Instance method

Needs class state
→ Class method

Needs neither
→ Static method
```

---

## Special Methods

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

---

## Identity vs Equality

```text
is
→ Same exact object?

==
→ Logically equal?

id()
→ Python object identity
```

Important:

```text
id(device)
≠
SSD serial number
```

Example:

```python
a = StorageDevice("SN1001")
b = StorageDevice("SN1001")
c = a
```

```text
a is b
→ False

a == b
→ Depends on __eq__()

a is c
→ True
```

---

## Inheritance

```text
Inheritance
→ IS-A relationship
```

Example:

```text
NVMeDevice
    IS-A
StorageDevice
```

### Terms

```text
Parent
→ Base class

Child
→ Derived class

Overriding
→ Child provides its own implementation

super()
→ Access next implementation in MRO
```

### Type checks

```text
isinstance()
→ Object relationship

issubclass()
→ Class relationship
```

---

## Types of Inheritance

```text
Single
A
↓
B
```

```text
Multilevel
A
↓
B
↓
C
```

```text
Hierarchical
    A
   / \
  B   C
```

```text
Multiple
A   B
 \ /
  C
```

---

## MRO

```text
MRO
→ Method Resolution Order
```

Check:

```python
ClassName.mro()
```

or:

```python
ClassName.__mro__
```

Used especially when multiple inheritance exists.

---

## Polymorphism

```text
Same operation
      ↓
Different objects
      ↓
Different behavior
```

Example:

```python
device.check_health()
```

can behave differently for:

```text
NVMeDevice
SATADevice
MockDevice
```

---

## Duck Typing

```text
Focus on behavior
rather than declared type
```

Example:

```python
def run_check(device):
    device.check_health()
```

Any compatible object providing `check_health()` can potentially be used.

```text
Duck typing
→ Inheritance not required
```

---

## Abstraction

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

The caller does not need to know every internal implementation detail.

---

## Abstract Base Class

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

```text
ABC
→ Abstract Base Class mechanism

@abstractmethod
→ Required behavior

Concrete class
→ Implements required abstract methods
```

Remember:

```text
ABC alone
≠
abstract method
```

`@abstractmethod` is required to mark a method as abstract.

---

## Composition

```text
Composition
→ HAS-A
```

Example:

```text
StorageDevice
     HAS-A
CommandRunner
```

---

## Aggregation

```text
Aggregation
→ HAS-A
→ Associated object can exist independently
```

---

## IS-A vs HAS-A

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

```text
StorageDevice
    HAS-A
CommandRunner
```

---

## Dependency

```text
Dependency
→ Something an object needs to perform its responsibility
```

Example:

```text
StorageDevice
      ↓
needs
      ↓
CommandRunner
```

---

## Dependency Injection

```text
Dependency Injection
→ Supply dependency from outside
```

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

### Main benefits

```text
Lower coupling
Replaceability
Testability
Reusability
```

---

# OOP Relationships

```text
                  OOP
                   │
        ┌──────────┴──────────┐
        ↓                     ↓
     Classes              Relationships
        │                     │
        ↓               ┌─────┴─────┐
     Objects             ↓           ↓
        │              IS-A        HAS-A
        ↓                │           │
      State         Inheritance   Composition
        │                          Aggregation
        ↓
   Encapsulation
```

---

# Most Important Distinctions

## Encapsulation vs Abstraction

```text
Encapsulation
→ Control access

Abstraction
→ Hide unnecessary implementation
```

## Inheritance vs Composition

```text
Inheritance
→ IS-A

Composition
→ HAS-A
```

## `is` vs `==`

```text
is
→ Identity

==
→ Equality
```

## Composition vs Dependency Injection

```text
Composition
→ Object contains/uses another object

Dependency Injection
→ Dependency is supplied externally
```

## Class Method vs Static Method

```text
Class Method
→ cls

Static Method
→ no automatic self/cls
```

---

# Storage Automation OOP Mental Model

```text
                    Test
                     ↓
                  Validator
                     ↓
                StorageDevice
                     ↓
                 HAS-A
                     ↓
                CommandRunner
                     ↓
                   Linux
                     ↓
                Storage Tool
                     ↓
              Storage Hardware
```

Possible concrete device hierarchy:

```text
              StorageDevice
               /        \
              ↓          ↓
           NVMeDevice   SATADevice
```

Different implementations:

```text
NVMeDevice
SATADevice
MockDevice
```

can provide common operations such as:

```text
identify()
check_health()
reset()
```

---

# OOP Design Rules

```text
1. Use classes when they provide meaningful state + behavior.

2. Keep class responsibilities clear.

3. Prefer low coupling.

4. Keep related behavior together.

5. Use inheritance only for genuine IS-A relationships.

6. Use composition for genuine HAS-A relationships.

7. Use Dependency Injection when external dependencies
   should be replaceable or testable.

8. Do not force every piece of code into a class.

9. Do not use OOP features merely because they exist.

10. Design for readability, reuse and testability.
```

---

# Interview Rapid Recall

```text
Class
→ Blueprint

Object
→ Instance

Attribute
→ State

Method
→ Behavior

Encapsulation
→ Controlled access

Inheritance
→ IS-A

Polymorphism
→ Same operation, different behavior

Abstraction
→ WHAT, hide unnecessary HOW

Composition
→ HAS-A

Aggregation
→ HAS-A with independent existence

Dependency
→ Required external component

Dependency Injection
→ Dependency supplied from outside

MRO
→ Method Resolution Order

is
→ Identity

==
→ Equality

ABC
→ Abstract Base Class mechanism

@abstractmethod
→ Required abstract behavior
```

---

# Final OOP Mental Model

```text
                    OBJECT
                      │
             ┌────────┴────────┐
             ↓                 ↓
           STATE            BEHAVIOR
        Attributes          Methods
             │                 │
             └────────┬────────┘
                      ↓
                ENCAPSULATION
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
     Inheritance   Composition  Abstraction
       IS-A          HAS-A         WHAT
          │             │           │
          └──────┬──────┴───────────┘
                 ↓
            Polymorphism
                 │
                 ↓
       Dependency Injection
                 │
                 ↓
          Testable Design
```

## One-Line Summary

> **Use OOP to organize meaningful state, behavior and relationships into clear, reusable and testable components.**

