# OOP Interview Questions

## 1. OOP Fundamentals

### Q1. What is OOP?

OOP stands for Object-Oriented Programming. It is a programming approach where software is organized around objects that combine state and behavior.

---

### Q2. What is a class?

A class is a blueprint or definition used to create objects.

```python
class StorageDevice:
    pass
```

---

### Q3. What is an object?

An object is an instance of a class.

```python
device = StorageDevice()
```

---

### Q4. What is the difference between a class and an object?

```text
Class
→ Definition / blueprint

Object
→ Instance created from the class
```

---

### Q5. What is an attribute?

An attribute is data associated with an object or class.

Example:

```python
self.serial_number
self.model
```

---

### Q6. What is an instance attribute?

An attribute that belongs to a particular object.

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number
```

Different objects can have different values.

---

### Q7. What is a class attribute?

An attribute associated with the class and normally shared by its instances.

```python
class StorageDevice:

    device_type = "Storage Device"
```

---

### Q8. What is a method?

A function defined inside a class that represents behavior associated with the object or class.

---

### Q9. What is `self`?

`self` refers to the current object instance inside an instance method.

---

### Q10. What is `__init__()`?

`__init__()` is the object initialization method used to establish the initial state of an object.

---

# 2. Encapsulation

### Q11. What is encapsulation?

Encapsulation is the concept of combining data and behavior in an object while controlling how internal state is accessed or modified.

---

### Q12. What is a public attribute?

An attribute that can normally be accessed directly from outside the class.

```python
self.serial_number
```

---

### Q13. What does `_variable` mean in Python?

A leading underscore indicates that an attribute or method is intended to be internal/protected by convention.

Python does not strictly enforce protected access.

---

### Q14. What does `__variable` mean?

A double leading underscore triggers Python name mangling.

Example:

```python
self.__health_status
```

is internally represented approximately as:

```text
_StorageDevice__health_status
```

---

### Q15. Is a private attribute truly private in Python?

No.

Python's double underscore provides name mangling rather than absolute access protection.

---

### Q16. What is a property?

A property provides controlled access to an attribute using attribute-style syntax.

Example:

```python
@property
def health_status(self):
    return self.__health_status
```

---

### Q17. Why use a setter?

A setter allows controlled modification and validation of internal state.

Example:

```python
@temperature.setter
def temperature(self, value):

    if value < 0 or value > 100:
        raise ValueError("Invalid temperature")

    self._temperature = value
```

---

### Q18. Why is encapsulation useful in storage automation?

It can prevent test code and utilities from modifying important internal state arbitrarily and allows validation to be applied when state changes.

---

# 3. Methods

### Q19. What is an instance method?

A method that operates on a particular object and normally receives `self`.

---

### Q20. What is a class method?

A method declared with `@classmethod` that receives `cls` and operates in relation to the class.

---

### Q21. What is a static method?

A method declared with `@staticmethod` that does not automatically receive `self` or `cls`.

---

### Q22. Difference between instance, class and static methods?

```text
Instance Method
→ self
→ object-specific behavior

Class Method
→ cls
→ class-level behavior

Static Method
→ no automatic self/cls
→ independent logic related to the class
```

---

### Q23. When should you use an instance method?

When the operation requires the state of a specific object.

Example:

```python
device.check_health()
```

---

### Q24. When should you use a class method?

When the operation relates to class-level state or when an alternate constructor is appropriate.

---

### Q25. When should you use a static method?

When the logic requires neither instance state nor class state and is logically related to the class.

---

# 4. Special Methods

### Q26. What are dunder methods?

Special methods whose names use the double-underscore form, such as:

```text
__init__
__str__
__repr__
__eq__
__len__
```

---

### Q27. What is `__str__()`?

It provides a human-readable string representation of an object.

---

### Q28. What is `__repr__()`?

It provides a developer-oriented representation useful for debugging and inspection.

---

### Q29. Difference between `__str__()` and `__repr__()`?

```text
__str__()
→ human-readable

__repr__()
→ developer/debugging representation
```

---

### Q30. What does `__eq__()` do?

It defines how two objects compare for equality using `==`.

---

### Q31. What does `__len__()` do?

It defines what `len(object)` returns for a custom class.

---

### Q32. Why are special methods useful in automation?

They can make test objects, result objects, and device objects easier to display, compare and debug.

---

# 5. Identity and Equality

### Q33. What is object identity?

Object identity refers to whether two references point to the exact same Python object.

---

### Q34. What does `id()` do?

`id()` returns an identity value associated with the Python object during its lifetime.

It is not a hardware identifier.

---

### Q35. What does `is` do?

`is` checks object identity.

```python
a is b
```

asks whether `a` and `b` refer to the same object.

---

### Q36. What does `==` do?

`==` checks equality.

For custom classes, it can use the class's `__eq__()` implementation.

---

### Q37. Difference between `is` and `==`?

```text
is
→ same object?

==
→ logically equal?
```

---

### Q38. Can two different objects be equal?

Yes.

Two different objects can have different identities while comparing equal through `__eq__()`.

---

### Q39. Is Python `id()` the SSD serial number?

No.

```text
id(device)
→ Python object identity

device serial number
→ physical/logical storage identifier
```

These are completely different concepts.

---

# 6. Inheritance

### Q40. What is inheritance?

Inheritance allows one class to derive from another and reuse or extend its behavior.

---

### Q41. What is a base class?

The class being inherited from.

Also called:

```text
Parent
Superclass
Base class
```

---

### Q42. What is a derived class?

A class that inherits from another class.

Also called:

```text
Child
Subclass
Derived class
```

---

### Q43. What is an IS-A relationship?

It is the conceptual relationship represented by inheritance.

Example:

```text
NVMeDevice IS-A StorageDevice
```

---

### Q44. What is method inheritance?

A child class can use methods defined by its parent.

---

### Q45. What is method overriding?

A child class provides its own implementation of an inherited method.

---

### Q46. What is `super()`?

`super()` is used to access the next implementation in the inheritance hierarchy according to Python's method resolution order.

---

### Q47. Can a child inherit the parent's constructor?

Yes.

If the child does not define its own `__init__()`, it can use the inherited initialization behavior.

A child can also call the parent initialization using:

```python
super().__init__(...)
```

---

### Q48. What is `isinstance()`?

It checks whether an object is an instance of a specified class or compatible class in its inheritance hierarchy.

---

### Q49. What is `issubclass()`?

It checks whether one class derives from another class.

---

### Q50. What is single inheritance?

One child class derives from one parent.

---

### Q51. What is multilevel inheritance?

Inheritance occurs in a chain.

```text
StorageDevice
      ↓
NVMeDevice
      ↓
EnterpriseNVMeDevice
```

---

### Q52. What is hierarchical inheritance?

Multiple child classes derive from the same parent.

```text
        StorageDevice
         /         \
        ↓           ↓
      NVMe         SATA
```

---

### Q53. What is multiple inheritance?

A class derives from more than one parent class.

---

### Q54. What is MRO?

MRO stands for **Method Resolution Order**.

It determines the order Python follows when searching for methods and attributes in an inheritance hierarchy.

---

### Q55. How do you see the MRO?

```python
ClassName.mro()
```

or:

```python
ClassName.__mro__
```

---

### Q56. Why is MRO important with multiple inheritance?

When multiple parent classes contain overlapping methods, Python needs a deterministic order to decide which implementation is found first.

---

# 7. Polymorphism

### Q57. What is polymorphism?

Polymorphism allows the same operation or interface to work with different objects while each object provides appropriate behavior.

---

### Q58. What is method overriding as polymorphism?

A base class defines an operation and child classes provide different implementations.

Example:

```python
device.identify()
```

may behave differently for NVMe and SATA devices.

---

### Q59. What is a common interface?

Different objects provide a consistent set of operations.

Example:

```text
identify()
check_health()
reset()
```

---

### Q60. What is duck typing?

Duck typing means code focuses on whether an object provides the required behavior rather than requiring a specific class hierarchy.

---

### Q61. Does duck typing require inheritance?

No.

Different unrelated classes can provide the same required method.

---

### Q62. Why is polymorphism useful in automation?

It allows generic test or validation code to operate with different device implementations without putting every device-specific implementation inside the higher-level test.

---

### Q63. What is practical polymorphism?

Writing general code that works with multiple compatible objects.

Example:

```python
def run_health_check(device):
    device.check_health()
```

---

# 8. Abstraction

### Q64. What is abstraction?

Abstraction exposes the behavior the consumer needs while hiding unnecessary implementation details.

---

### Q65. What is the difference between abstraction and encapsulation?

```text
Encapsulation
→ controls access to state/behavior

Abstraction
→ hides unnecessary implementation details
```

---

### Q66. What is an abstract class?

A class designed to define a common contract for derived classes and potentially contain abstract methods that concrete implementations must provide.

---

### Q67. What is `ABC`?

`ABC` is the Abstract Base Class mechanism provided by Python's `abc` module.

---

### Q68. What does `@abstractmethod` do?

It marks a method as abstract and requires concrete subclasses to provide an implementation before they can be instantiated as concrete classes.

---

### Q69. Does inheriting from `ABC` alone make a class abstract?

No.

Abstract methods need to be defined using `@abstractmethod`.

---

### Q70. What is a concrete class?

A class that has provided implementations for all of its required abstract methods and can therefore be instantiated.

---

### Q71. Can an abstract subclass implement only some abstract methods?

Yes.

It can remain abstract until all required abstract methods are implemented.

---

# 9. Composition, Aggregation and Dependency Injection

### Q72. What is composition?

Composition is a strong HAS-A relationship where one object contains another object as part of its structure.

---

### Q73. What is aggregation?

Aggregation is a HAS-A relationship where the associated object can exist independently.

---

### Q74. What is the difference between HAS-A and IS-A?

```text
IS-A
→ inheritance

HAS-A
→ composition / aggregation
```

---

### Q75. Why use composition instead of inheritance?

Use composition when the relationship is HAS-A rather than IS-A.

Composition is often useful for assembling separate responsibilities into an object.

---

### Q76. What is a dependency?

A dependency is something an object needs in order to perform its responsibility.

Example:

```text
StorageDevice
      ↓
needs
      ↓
CommandRunner
```

---

### Q77. What is Dependency Injection?

Dependency Injection is a design technique where a dependency is supplied from outside rather than created internally by the object.

---

### Q78. What is constructor injection?

Supplying the dependency through `__init__()`.

```python
class StorageDevice:

    def __init__(self, runner):
        self.runner = runner
```

---

### Q79. Why is Dependency Injection useful in automation?

It allows dependencies such as:

```text
CommandRunner
SSH client
Device interface
```

to be replaced or mocked, which improves testability and reduces coupling.

---

### Q80. Is Dependency Injection inheritance?

No.

It is a design technique for supplying dependencies from outside.

---

# 10. OOP Design Questions

### Q81. Why should a class have a clear responsibility?

A clear responsibility makes the class easier to understand, reuse, test and maintain.

---

### Q82. What is Single Responsibility?

A class should have a focused responsibility rather than becoming a container for unrelated behavior.

---

### Q83. What is coupling?

Coupling describes how strongly components depend on one another.

Lower coupling generally makes components easier to replace and maintain.

---

### Q84. What is cohesion?

Cohesion describes how closely the responsibilities within a component belong together.

High cohesion is generally desirable.

---

### Q85. Why can composition be preferable to excessive inheritance?

Composition allows behavior to be assembled from independent components and can reduce rigid inheritance hierarchies.

---

### Q86. What makes a class testable?

A class is easier to test when:

* responsibilities are clear
* dependencies are controllable
* external behavior can be replaced or mocked
* state changes are predictable

---

# 11. Storage Automation Scenario Questions

### Q87. How would you model an NVMe device in Python?

A possible abstraction is:

```text
NVMeDevice
├── serial_number
├── model
├── firmware
├── temperature
└── behavior
    ├── identify()
    ├── check_health()
    └── reset()
```

The exact design depends on the framework requirements.

---

### Q88. Why should `CommandRunner` not necessarily inherit from `StorageDevice`?

Because:

```text
CommandRunner
IS-A
StorageDevice
```

is not a meaningful relationship.

A more natural relationship is:

```text
StorageDevice
HAS-A
CommandRunner
```

---

### Q89. Why might a `MockCommandRunner` be useful?

It can simulate command results, errors and timeouts without requiring a real storage failure or hardware manipulation.

---

### Q90. How does Dependency Injection help here?

The storage object can receive either:

```text
RealCommandRunner
```

or:

```text
MockCommandRunner
```

without changing the storage object's main implementation.

---

### Q91. How would polymorphism help a storage framework?

A common operation such as:

```python
check_health()
```

can be implemented differently by different device types while higher-level code uses the same operation.

---

### Q92. How would abstraction help a storage framework?

A test can use:

```python
device.check_health()
```

without needing to know all lower-level details such as command execution, parsing and device communication.

---

### Q93. Give an example of composition in storage automation.

```text
NVMeDevice
    HAS-A
CommandRunner
```

The device uses the command runner as a component.

---

### Q94. Give an example of inheritance in storage automation.

```text
NVMeDevice
    IS-A
StorageDevice
```

when the domain model genuinely supports that specialization.

---

### Q95. What is the difference between product/device identity and Python object identity?

```text
Python object identity
→ id()

Storage device identity
→ serial number / appropriate device identifier
```

They should not be confused.

---

# 12. Interview Scenario Questions

### Q96. Your storage object creates its own SSH client internally. What design issue can this create?

It can create tight coupling to a specific SSH implementation and make isolated testing more difficult.

---

### Q97. How could you improve it?

Supply the SSH dependency from outside, for example through constructor injection.

---

### Q98. You have NVMe, SATA and mock devices. How can one function validate all of them?

Use a common operation/interface such as:

```python
def validate(device):
    return device.check_health()
```

provided each object supports the required behavior.

---

### Q99. Two objects have the same serial number. Are they necessarily the same Python object?

No.

They can be different Python objects that compare equal according to the class's logical equality rules.

---

### Q100. What is the most important OOP design principle for our storage automation?

Use OOP to create **clear, focused, reusable and testable components**, and choose relationships based on the actual responsibility of each component rather than using inheritance or other OOP mechanisms unnecessarily.

---

# Rapid Revision

```text
Class
→ Blueprint

Object
→ Instance

Attribute
→ State

Method
→ Behavior

self
→ Current object

__init__()
→ Initialization

Encapsulation
→ Controlled access

_
→ Internal/protected convention

__
→ Name mangling

@property
→ Controlled attribute access

__str__()
→ Human-readable representation

__repr__()
→ Debug/developer representation

__eq__()
→ Equality

__len__()
→ len() behavior

is
→ Identity

==
→ Equality

Inheritance
→ IS-A

super()
→ Next implementation in MRO

isinstance()
→ Object/class-instance relationship

issubclass()
→ Class inheritance relationship

MRO
→ Method Resolution Order

Polymorphism
→ Same operation, different behavior

Duck Typing
→ Behavior over declared type

Abstraction
→ WHAT, hide unnecessary HOW

ABC
→ Abstract Base Class mechanism

@abstractmethod
→ Required abstract behavior

Composition
→ HAS-A

Aggregation
→ HAS-A with independent lifetime

Dependency
→ Something an object needs

Dependency Injection
→ Dependency supplied externally
```

# Storage Automation Mental Model

```text
                    OOP
                     │
      ┌──────────────┼──────────────┐
      ↓              ↓              ↓
   Device          Validator      Runner
      │                              │
      │ HAS-A                        │
      └──────────────┐               │
                     ↓               │
                CommandRunner ◄──────┘
                     │
                     ↓
                  Linux
                     │
                     ↓
              Storage Tool
                     │
                     ↓
                Storage Device
```

The objective is not to use every OOP feature everywhere.

The objective is to use the appropriate OOP concept when it makes the automation design clearer, more reusable and more testable.

