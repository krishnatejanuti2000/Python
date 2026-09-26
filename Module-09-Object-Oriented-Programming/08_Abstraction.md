# Abstraction

## 1. What is Abstraction?

**Abstraction** is the concept of exposing the functionality that is important to the user while hiding unnecessary implementation details.

The central idea is:

```text id="x8y5s4"
WHAT
↓
Expose required behavior

HOW
↓
Hide implementation details
```

Abstraction allows code to interact with an object through a defined behavior without requiring knowledge of its internal implementation.

---

# 2. Why Abstraction?

Consider a storage validation system.

A test may need to perform:

```text id="6c6f5j"
Identify device
Check health
Reset device
```

The test does not always need to know exactly how those operations are implemented internally.

For example:

```text id="46eixr"
check_health()
      ↓
implementation hidden
      ↓
NVMe commands / Linux / driver / device
```

The caller only needs the appropriate interface.

---

# 3. Simple Abstraction Example

```python id="cm0n9y"
class StorageDevice:

    def check_health(self):
        print("Checking storage health")
```

A caller can simply use:

```python id="l5fww7"
device.check_health()
```

The caller does not need to know the internal steps performed by the method.

That is the basic idea of abstraction.

---

# 4. Abstraction vs Encapsulation

These concepts are related but they solve different problems.

## Encapsulation

Focuses on controlling and organizing:

```text id="q2v3jl"
Data
+
Behavior
+
Access
```

Example:

```python id="r43rsg"
device.health_status
```

may be controlled through a property.

---

## Abstraction

Focuses on:

```text id="jzwz9u"
What the object provides
```

while hiding:

```text id="n0pj3p"
How it implements that behavior
```

Simple distinction:

```text id="o3tq0j"
Encapsulation
→ Control access

Abstraction
→ Hide unnecessary implementation details
```

---

# 5. Real-World Analogy

Consider a car.

You use:

```text id="v2n5i8"
Steering
Brake
Accelerator
```

You do not need to know every internal mechanical detail of the engine to drive it.

The interface exposes:

```text id="8azw6y"
WHAT you can do
```

while the implementation hides:

```text id="7l0j9q"
HOW it happens
```

Software abstraction follows the same general principle.

---

# 6. Abstraction in Storage Automation

Imagine a test contains:

```python id="wpl2m0"
device.check_health()
```

The test does not need to directly implement:

```text id="v8cgic"
nvme command
 ↓
subprocess
 ↓
stdout
 ↓
JSON parsing
 ↓
health extraction
```

Those details can be hidden inside the device or utility implementation.

The test interacts with a higher-level operation:

```text id="6nbt7k"
check_health()
```

---

# 7. Abstract Class

An **abstract class** is a class intended to define a common structure or contract for derived classes rather than being used directly as a fully implemented object.

For example:

```python id="d4x0yw"
from abc import ABC, abstractmethod


class StorageDevice(ABC):

    @abstractmethod
    def check_health(self):
        pass
```

Here `StorageDevice` defines that a concrete storage-device implementation must provide:

```python id="cx54af"
check_health()
```

---

# 8. `ABC`

Python provides `ABC` through the `abc` module.

Example:

```python id="wov8hh"
from abc import ABC


class StorageDevice(ABC):
    pass
```

`ABC` allows a class to participate in Python's Abstract Base Class mechanism.

However:

> Simply inheriting from `ABC` does not automatically make a method abstract.

An abstract method must be explicitly marked using `@abstractmethod`.

---

# 9. `@abstractmethod`

`@abstractmethod` marks a method as required for concrete subclasses.

Example:

```python id="yl5h0a"
from abc import ABC, abstractmethod


class StorageDevice(ABC):

    @abstractmethod
    def check_health(self):
        pass
```

The class now specifies a required operation.

A concrete implementation must provide the required method before it can be instantiated as a concrete class.

---

# 10. Abstract Class Example

```python id="rcj16w"
from abc import ABC, abstractmethod


class StorageDevice(ABC):

    @abstractmethod
    def identify(self):
        pass

    @abstractmethod
    def check_health(self):
        pass
```

The class defines a contract:

```text id="z5h5f4"
StorageDevice
├── identify()
└── check_health()
```

It describes what a storage-device implementation must provide.

---

# 11. Concrete Class

A **concrete class** provides the required implementations and can be instantiated when no abstract requirements remain.

Example:

```python id="51osap"
from abc import ABC, abstractmethod


class StorageDevice(ABC):

    @abstractmethod
    def identify(self):
        pass

    @abstractmethod
    def check_health(self):
        pass


class NVMeDevice(StorageDevice):

    def identify(self):
        print("NVMe identification")

    def check_health(self):
        print("NVMe health check")
```

Now `NVMeDevice` provides both required methods and can be instantiated.

---

# 12. Abstract vs Concrete Class

### Abstract Class

```text id="6j1h2f"
Defines the contract
+
May provide common implementation
+
Not complete for direct instantiation
```

### Concrete Class

```text id="cn3i0e"
Provides required implementations
+
Can be instantiated
```

Mental model:

```text id="91q94t"
Abstract Class
      ↓
Defines required behavior
      ↓
Concrete Child
      ↓
Implements behavior
```

---

# 13. Abstract Method Does Not Always Mean Empty Method

An abstract method can define a required interface.

Example:

```python id="2otgxh"
from abc import ABC, abstractmethod


class StorageDevice(ABC):

    @abstractmethod
    def check_health(self):
        pass
```

The important property is that concrete subclasses are required to satisfy the abstract contract.

---

# 14. Partial Implementation

An abstract subclass can implement only some abstract methods and remain abstract.

Example:

```python id="asf6ej"
from abc import ABC, abstractmethod


class StorageDevice(ABC):

    @abstractmethod
    def identify(self):
        pass

    @abstractmethod
    def check_health(self):
        pass


class IntermediateStorageDevice(StorageDevice):

    def identify(self):
        print("Generic identification")
```

`IntermediateStorageDevice` has not implemented:

```python id="lpp47y"
check_health()
```

so it can remain abstract.

---

# 15. Completing the Implementation

Another subclass can implement the remaining method.

```python id="uxxyn7"
class NVMeDevice(IntermediateStorageDevice):

    def check_health(self):
        print("NVMe health check")
```

Now all required abstract methods are implemented.

Conceptually:

```text id="x04e84"
StorageDevice
      ↓
abstract contract
      ↓
IntermediateStorageDevice
      ↓
implements identify()
      ↓
NVMeDevice
      ↓
implements check_health()
      ↓
Concrete
```

---

# 16. Attempting to Instantiate an Incomplete Abstract Class

Suppose:

```python id="l7k5uv"
from abc import ABC, abstractmethod


class StorageDevice(ABC):

    @abstractmethod
    def check_health(self):
        pass
```

Trying:

```python id="35tq5n"
device = StorageDevice()
```

fails because the class contains an unimplemented abstract method.

This is the mechanism that enforces the abstract contract.

---

# 17. Why Use Abstract Classes?

Abstract classes are useful when several concrete classes should follow a common contract.

For example:

```text id="n21nsg"
StorageDevice
      ↓
common interface
      ↓
 ┌────┴────┐
 ↓         ↓
NVMe      SATA
```

Both implementations may need:

```text id="eq0u3d"
identify()
check_health()
reset()
```

but the internal implementation can differ.

---

# 18. Abstraction in Storage Validation

Suppose we define:

```python id="3u5s7q"
from abc import ABC, abstractmethod


class StorageDevice(ABC):

    @abstractmethod
    def identify(self):
        pass

    @abstractmethod
    def check_health(self):
        pass

    @abstractmethod
    def reset(self):
        pass
```

The abstract class defines the expected behavior.

Then:

```python id="n0a1li"
class NVMeDevice(StorageDevice):

    def identify(self):
        print("NVMe identify")

    def check_health(self):
        print("NVMe health")

    def reset(self):
        print("NVMe reset")
```

And another implementation:

```python id="0j8a9d"
class SATADevice(StorageDevice):

    def identify(self):
        print("SATA identify")

    def check_health(self):
        print("SATA health")

    def reset(self):
        print("SATA reset")
```

The interface is common:

```text id="6p5ohe"
identify()
check_health()
reset()
```

while the implementation differs.

---

# 19. Abstraction and Polymorphism

These concepts work closely together.

### Abstraction

Defines the required operations:

```text id="6pne2s"
identify()
check_health()
reset()
```

### Polymorphism

Allows different implementations:

```text id="rd9t7l"
NVMe → NVMe implementation
SATA → SATA implementation
```

Together:

```text id="62r6of"
Abstract Interface
       ↓
Different Implementations
       ↓
Polymorphic Behavior
```

---

# 20. Abstraction Without ABC

Abstraction does not always require `ABC`.

A class can provide a high-level interface while hiding implementation details without formally using an abstract base class.

Example:

```python id="q8h5hy"
class StorageDevice:

    def check_health(self):
        return self._collect_health_data()
        
    def _collect_health_data(self):
        return "Health data"
```

The caller uses:

```python id="uj9c0b"
device.check_health()
```

without needing to know the internal implementation.

This is abstraction through interface design.

`ABC` adds a formal mechanism for defining required methods.

---

# 21. ABC vs Normal Base Class

### Normal Base Class

Can usually be instantiated unless other design choices prevent it.

```python id="ipj2cf"
class StorageDevice:

    def identify(self):
        ...
```

### Abstract Base Class

Uses the ABC mechanism and abstract methods to define requirements.

```python id="b4ey1g"
from abc import ABC, abstractmethod


class StorageDevice(ABC):

    @abstractmethod
    def identify(self):
        pass
```

The abstract class is enforcing a contract for concrete subclasses.

---

# 22. Abstraction and Interface

An interface represents the operations that a component is expected to provide.

For example:

```text id="0mygn8"
Storage Device Interface
├── identify()
├── check_health()
└── reset()
```

Different device implementations can satisfy that interface.

The consumer can work with the interface without depending on the implementation details.

---

# 23. Storage Automation Example

A validation component might depend on the following abstraction:

```text id="b2tu8s"
Device
├── identify()
├── health()
└── reset()
```

The underlying implementation might use:

```text id="1uyxi8"
Linux
 ↓
nvme-cli
 ↓
driver
 ↓
PCIe
 ↓
NVMe controller
```

The validation code does not need to know every internal step.

It uses the defined device operations.

---

# 24. Why Abstraction Helps Framework Design

Abstraction can help separate:

```text id="xg3uwk"
WHAT a component does
```

from:

```text id="v20h1v"
HOW the component does it
```

For example:

```python id="hxy2ce"
device.check_health()
```

can hide:

```text id="4j1p8a"
command execution
parsing
error handling
data extraction
```

This allows higher-level test code to remain focused on validation rather than implementation details.

---

# 25. Abstraction and Framework Layers

A possible automation architecture is:

```text id="nhy84k"
Test
 ↓
Validator
 ↓
Device Interface
 ↓
Execution Layer
 ↓
Linux / SSH
 ↓
Storage Tool
 ↓
Hardware
```

Each layer can expose a useful interface while hiding lower-level implementation details.

This reduces the amount of implementation knowledge required by higher-level components.

---

# 26. Common Mistakes

## Mistake 1 — Thinking abstraction means "hide all code"

Abstraction does not mean code cannot be inspected.

It means unnecessary implementation details are not required by the consumer.

---

## Mistake 2 — Thinking `ABC` alone creates abstract methods

This:

```python id="p4v7sj"
class StorageDevice(ABC):
    pass
```

does not by itself define an abstract method.

Use:

```python id="i8h1n7"
@abstractmethod
```

to define required abstract operations.

---

## Mistake 3 — Confusing abstraction and encapsulation

Remember:

```text id="alh8kj"
Encapsulation
→ control access

Abstraction
→ hide implementation complexity
```

---

## Mistake 4 — Using abstract classes everywhere

Use an abstract class when there is a genuine shared contract that benefits from formal enforcement.

Not every simple class needs to inherit from `ABC`.

---

# 27. Abstraction vs Polymorphism

### Abstraction

```text id="g2r0a9"
Defines WHAT is available
```

### Polymorphism

```text id="0o8f5e"
Allows different implementations of that behavior
```

Example:

```text id="ppg0jk"
Abstraction
→ check_health()

Polymorphism
→ NVMe check_health()
→ SATA check_health()
```

---

# 28. Abstraction vs Composition

These solve different problems.

### Abstraction

Controls the interface and hides implementation details.

### Composition

Builds an object from other objects.

Example:

```python id="rm7rc1"
class NVMeDevice:

    def __init__(self, runner):
        self.runner = runner
```

Here:

```text id="7pjjqp"
Composition
→ NVMeDevice HAS-A runner
```

The public device operations can still provide abstraction:

```python id="y8mxk8"
device.check_health()
```

So these concepts can work together.

---

# 29. Automation-Oriented Example

Imagine:

```python id="8k7sq9"
class Device(ABC):

    @abstractmethod
    def identify(self):
        pass

    @abstractmethod
    def check_health(self):
        pass
```

Then:

```python id="5j1i7m"
class NVMeDevice(Device):

    def identify(self):
        ...

    def check_health(self):
        ...
```

and:

```python id="3yoq8u"
class MockDevice(Device):

    def identify(self):
        ...

    def check_health(self):
        ...
```

The test code can depend on the common abstraction while different implementations are used underneath.

---

# 30. Storage Automation Mental Model

```text id="d4x8q3"
             ABSTRACTION
                  │
                  ↓
          Define required behavior
                  │
        ┌─────────┴─────────┐
        ↓                   ↓
    NVMeDevice          MockDevice
        │                   │
        ↓                   ↓
 NVMe implementation   Test implementation
```

The higher-level code can work through the common interface.

---

# 31. Key Takeaways

```text id="kjx1fb"
Abstraction
→ Expose what is needed
→ Hide unnecessary implementation details

Abstract Class
→ Defines a common contract

ABC
→ Python's Abstract Base Class mechanism

@abstractmethod
→ Marks a method as required

Concrete Class
→ Fully implements required abstract behavior

Abstraction
≠
Encapsulation

Abstraction
→ WHAT

Implementation
→ HOW
```

---

# 32. Final Mental Model

```text id="y9x3rc"
                 USER / TEST
                      │
                      ↓
                  INTERFACE
                      │
                      ↓
                 ABSTRACTION
                      │
             hides implementation
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
        NVMe        SATA        Mock
      implementation implementation implementation
```

The central principle is:

> **Expose the behavior the consumer needs while hiding implementation details that the consumer does not need to know.**

