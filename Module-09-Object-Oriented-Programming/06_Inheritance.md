# Inheritance

## 1. What is Inheritance?

**Inheritance** is an OOP mechanism where a new class derives from an existing class and can reuse or extend its attributes and methods.

The relationship represented by inheritance is:

```text
IS-A
```

Example:

```python
class StorageDevice:
    pass


class NVMeDevice(StorageDevice):
    pass
```

Here:

```text
NVMeDevice
    IS-A
StorageDevice
```

Inheritance is one of the major OOP concepts in the Python roadmap.

---

# 2. Why Inheritance?

Inheritance can be useful when several classes share common behavior.

Suppose all storage devices need:

```text
Identify
Check Health
Reset
```

We can place common behavior in a base class and specialize it in derived classes.

```text
StorageDevice
      ↓
  common behavior
      ↓
 ┌────┴─────┐
 ↓          ↓
NVMe      SATA
```

---

# 3. Parent / Base Class

The class being inherited from is called the:

* Parent class
* Base class
* Superclass

Example:

```python
class StorageDevice:
    pass
```

`StorageDevice` is the base class.

---

# 4. Child / Derived Class

The class that inherits from another class is called the:

* Child class
* Derived class
* Subclass

Example:

```python
class NVMeDevice(StorageDevice):
    pass
```

`NVMeDevice` is the derived class.

---

# 5. Basic Inheritance Example

```python
class StorageDevice:

    def identify(self):
        print("Storage device identified")


class NVMeDevice(StorageDevice):
    pass
```

Create:

```python
device = NVMeDevice()

device.identify()
```

The `NVMeDevice` object can use the inherited method.

---

# 6. Method Inheritance

A child class automatically receives accessible methods defined by its parent according to Python's method lookup rules.

Example:

```python
class StorageDevice:

    def identify(self):
        print("Identifying storage device")


class NVMeDevice(StorageDevice):
    pass
```

Then:

```python
device = NVMeDevice()

device.identify()
```

works because `identify()` is inherited from `StorageDevice`.

---

# 7. Adding New Behavior in the Child Class

A child class can add behavior specific to itself.

Example:

```python
class StorageDevice:

    def identify(self):
        print("Identifying storage device")


class NVMeDevice(StorageDevice):

    def show_namespace(self):
        print("Showing NVMe namespace")
```

Now:

```python
device = NVMeDevice()

device.identify()
device.show_namespace()
```

The object has:

```text
Inherited behavior
+
NVMe-specific behavior
```

---

# 8. Common Example

```python
class StorageDevice:

    def identify(self):
        print("Generic storage identification")


class NVMeDevice(StorageDevice):

    def identify_controller(self):
        print("Identifying NVMe controller")
```

Here:

```text
NVMeDevice
├── identify()              ← inherited
└── identify_controller()   ← own method
```

---

# 9. Method Overriding

A child class can provide its own implementation of a method inherited from the parent.

This is called **method overriding**.

Example:

```python
class StorageDevice:

    def identify(self):
        print("Generic storage device")


class NVMeDevice(StorageDevice):

    def identify(self):
        print("NVMe device")
```

Now:

```python
device = NVMeDevice()

device.identify()
```

produces:

```text
NVMe device
```

The child implementation overrides the inherited implementation.

---

# 10. Why Override a Method?

A child class may inherit a general behavior but need specialized behavior.

For example:

```text
StorageDevice
→ generic identification

NVMeDevice
→ NVMe-specific identification

SATADevice
→ SATA-specific identification
```

The common method name can remain the same while behavior differs.

This becomes especially relevant to polymorphism.

---

# 11. `super()`

`super()` is used to access behavior from the parent class.

Example:

```python
class StorageDevice:

    def identify(self):
        print("Generic storage identification")


class NVMeDevice(StorageDevice):

    def identify(self):
        super().identify()
        print("NVMe-specific identification")
```

Call:

```python
device = NVMeDevice()

device.identify()
```

Output:

```text
Generic storage identification
NVMe-specific identification
```

---

# 12. Why Use `super()`?

Sometimes the child wants to:

```text
Reuse parent behavior
+
Add child-specific behavior
```

instead of completely replacing the parent behavior.

Example:

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number


class NVMeDevice(StorageDevice):

    def __init__(self, serial_number, namespace_count):
        super().__init__(serial_number)
        self.namespace_count = namespace_count
```

The child constructor reuses the parent initialization and then adds its own state.

---

# 13. Constructor Inheritance

If a child class does not define its own `__init__()`, it can use the inherited initialization behavior from the parent.

Example:

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number


class NVMeDevice(StorageDevice):
    pass
```

Now:

```python
device = NVMeDevice("SN1001")
```

can use the inherited `__init__()`.

---

# 14. Child Constructor with `super()`

When a child needs additional initialization:

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number


class NVMeDevice(StorageDevice):

    def __init__(self, serial_number, namespace_count):
        super().__init__(serial_number)
        self.namespace_count = namespace_count
```

Now:

```python
device = NVMeDevice("SN1001", 4)
```

produces:

```text
serial_number   → SN1001
namespace_count → 4
```

---

# 15. Parent and Child Responsibilities

A useful design approach is:

### Parent

Contains behavior common to all child types.

```text
StorageDevice
├── serial number
├── identify
├── health
└── reset
```

### Child

Contains behavior specific to its type.

```text
NVMeDevice
├── namespace operations
├── controller operations
└── NVMe-specific behavior
```

This is appropriate only when there is a genuine IS-A relationship.

---

# 16. `isinstance()`

`isinstance()` checks whether an object is an instance of a specified class or a class in its inheritance hierarchy.

Example:

```python
class StorageDevice:
    pass


class NVMeDevice(StorageDevice):
    pass


device = NVMeDevice()

print(isinstance(device, NVMeDevice))
print(isinstance(device, StorageDevice))
```

Both can be:

```text
True
True
```

because an `NVMeDevice` is also a `StorageDevice`.

---

# 17. Why `isinstance()` Matters

It can be used when code needs to determine the type relationship of an object.

Example:

```python
if isinstance(device, StorageDevice):
    print("Storage device object")
```

It is important not to use type checks everywhere simply because inheritance exists. Good polymorphic design can often avoid unnecessary type-specific branching.

---

# 18. `issubclass()`

`issubclass()` checks whether one class derives from another class.

Example:

```python
class StorageDevice:
    pass


class NVMeDevice(StorageDevice):
    pass
```

Then:

```python
print(issubclass(NVMeDevice, StorageDevice))
```

returns:

```text
True
```

Compare:

```text
isinstance()
→ object relationship

issubclass()
→ class relationship
```

---

# 19. `isinstance()` vs `issubclass()`

```text
isinstance(object, Class)
→ Is this object an instance of this class?

issubclass(ChildClass, ParentClass)
→ Is this class derived from this parent class?
```

Example:

```python
device = NVMeDevice()

isinstance(device, NVMeDevice)
```

checks the object.

While:

```python
issubclass(NVMeDevice, StorageDevice)
```

checks the classes.

---

# 20. Types of Inheritance

Python supports several inheritance structures.

The major forms are:

* Single inheritance
* Multilevel inheritance
* Hierarchical inheritance
* Multiple inheritance

---

# 21. Single Inheritance

One child derives from one parent.

```python
class StorageDevice:
    pass


class NVMeDevice(StorageDevice):
    pass
```

Diagram:

```text
StorageDevice
      ↓
NVMeDevice
```

---

# 22. Multilevel Inheritance

A class derives from another derived class.

```python
class StorageDevice:
    pass


class NVMeDevice(StorageDevice):
    pass


class EnterpriseNVMeDevice(NVMeDevice):
    pass
```

Diagram:

```text
StorageDevice
      ↓
NVMeDevice
      ↓
EnterpriseNVMeDevice
```

---

# 23. Hierarchical Inheritance

Multiple child classes derive from the same parent.

```python
class StorageDevice:
    pass


class NVMeDevice(StorageDevice):
    pass


class SATADevice(StorageDevice):
    pass
```

Diagram:

```text
         StorageDevice
          /         \
         ↓           ↓
      NVMe         SATA
```

This can be useful when different device types share common storage behavior.

---

# 24. Multiple Inheritance

A class can inherit from more than one parent.

Example:

```python
class StorageDevice:
    pass


class FirmwareValidator:
    pass


class NVMeDevice(StorageDevice, FirmwareValidator):
    pass
```

Now `NVMeDevice` derives from both:

```text
StorageDevice
FirmwareValidator
       ↓
   NVMeDevice
```

Python supports this form of inheritance.

---

# 25. Why Multiple Inheritance Requires Care

Suppose both parent classes define a method with the same name.

Example:

```python
class A:

    def run(self):
        print("A")


class B:

    def run(self):
        print("B")


class C(A, B):
    pass
```

When:

```python
obj = C()
obj.run()
```

Python needs a deterministic method lookup order.

This leads to **Method Resolution Order (MRO)**.

---

# 26. Method Resolution Order (MRO)

MRO defines the order Python follows when looking for a method or attribute in an inheritance hierarchy.

Example:

```python
class A:
    pass


class B(A):
    pass


class C(B):
    pass
```

The MRO can be inspected using:

```python
print(C.mro())
```

or:

```python
print(C.__mro__)
```

Conceptually:

```text
C
↓
B
↓
A
↓
object
```

---

# 27. MRO with Multiple Inheritance

Example:

```python
class A:

    def run(self):
        print("A")


class B:

    def run(self):
        print("B")


class C(A, B):
    pass
```

Python follows the class's MRO to determine which `run()` implementation is selected.

The declared inheritance order matters.

```python
class C(A, B):
    ...
```

is not identical to:

```python
class C(B, A):
    ...
```

---

# 28. `super()` and MRO

In multiple inheritance, `super()` does not simply mean:

> "Call my direct parent."

It follows the MRO.

This is an important concept.

Example:

```python
class A:

    def run(self):
        print("A")


class B(A):

    def run(self):
        print("B")
        super().run()


class C(B):

    def run(self):
        print("C")
        super().run()
```

Calling:

```python
C().run()
```

follows the MRO chain.

---

# 29. Inheritance vs Code Reuse

One of the most important design lessons:

> Do not use inheritance merely to reuse code.

The relationship should make semantic sense.

Good:

```text
NVMeDevice
    IS-A
StorageDevice
```

Potentially inappropriate:

```text
StorageDevice
    IS-A
CommandRunner
```

A storage device is not a command runner.

It may instead:

```text
StorageDevice
    HAS-A
CommandRunner
```

This is where composition becomes preferable.

---

# 30. Storage Example

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number

    def identify(self):
        print("Generic storage device")


class NVMeDevice(StorageDevice):

    def identify(self):
        print("NVMe device:", self.serial_number)

    def identify_controller(self):
        print("NVMe controller")


class SATADevice(StorageDevice):

    def identify(self):
        print("SATA device:", self.serial_number)
```

Here:

```text
StorageDevice
     / \
    /   \
   ↓     ↓
NVMe   SATA
```

Both children share the common storage concept while specializing behavior.

---

# 31. Inheritance and Polymorphism

Inheritance often provides the class relationship required for one form of polymorphism.

Example:

```python
class StorageDevice:

    def identify(self):
        print("Generic")


class NVMeDevice(StorageDevice):

    def identify(self):
        print("NVMe")


class SATADevice(StorageDevice):

    def identify(self):
        print("SATA")
```

Then:

```python
devices = [
    NVMeDevice(),
    SATADevice()
]

for device in devices:
    device.identify()
```

The same method call:

```python
device.identify()
```

produces different behavior.

The broader concept of polymorphism is documented separately.

---

# 32. Common Inheritance Mistakes

## Mistake 1 — Using inheritance for unrelated classes

Do not force an IS-A relationship where none exists.

---

## Mistake 2 — Excessive inheritance depth

A very deep inheritance hierarchy can become difficult to understand and maintain.

---

## Mistake 3 — Overriding without understanding the parent contract

If a child overrides a method, its behavior should remain consistent with the intended abstraction.

---

## Mistake 4 — Forgetting `super()`

When the child needs parent initialization or behavior, failing to call `super()` can leave required parent state uninitialized.

---

## Mistake 5 — Assuming `super()` always means direct parent

In multiple inheritance, `super()` follows the MRO.

---

# 33. Inheritance and Automation

Inheritance can be useful when our automation objects represent genuine specializations.

For example:

```text
StorageDevice
      ↓
NVMeDevice
```

because:

```text
NVMeDevice IS-A StorageDevice
```

However, dependencies such as:

```text
CommandRunner
SSHClient
LogCollector
```

are generally better thought of as components or dependencies rather than parent classes.

This distinction is important when we later design the automation framework.

---

# 34. Key Takeaways

```text
Inheritance
→ Create a class based on another class

Parent / Base Class
→ Class being inherited from

Child / Derived Class
→ Class that inherits

IS-A
→ Main inheritance relationship

Method Inheritance
→ Child receives inherited behavior

Method Overriding
→ Child replaces inherited implementation

super()
→ Access next implementation in the MRO

Constructor Inheritance
→ Child can use inherited __init__()

isinstance()
→ Checks object/class-instance relationship

issubclass()
→ Checks class inheritance relationship

Single Inheritance
→ One parent

Multilevel Inheritance
→ Chain of inheritance

Hierarchical Inheritance
→ Multiple children, one parent

Multiple Inheritance
→ Multiple parents

MRO
→ Method lookup order
```

---

# 35. Final Mental Model

```text
                         Base Class
                      StorageDevice
                            │
              ┌─────────────┴─────────────┐
              ↓                           ↓
         NVMeDevice                   SATADevice
              │                           │
              ↓                           ↓
      NVMe-specific behavior      SATA-specific behavior
```

The core relationship is:

```text
NVMeDevice IS-A StorageDevice
SATADevice IS-A StorageDevice
```

And the key design rule is:

> **Use inheritance when the child genuinely IS-A specialized form of the parent; do not use inheritance merely as a code-reuse mechanism.**

