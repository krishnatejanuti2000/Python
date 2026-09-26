# Composition, Aggregation, and Dependency Injection

## 1. Composition

**Composition** is an object relationship in which one object contains another object as part of its structure.

The main relationship is:

```text
HAS-A
```

Example:

```python
class Engine:

    def start(self):
        print("Engine started")


class Car:

    def __init__(self):
        self.engine = Engine()
```

Here:

```text
Car
 ↓
HAS-A
 ↓
Engine
```

`Car` contains an `Engine` object.

---

# 2. Why Composition?

Composition is useful when one object needs another object to perform its responsibility.

Instead of putting everything into one large class, responsibilities can be separated into different objects.

Example:

```text
StorageDevice
      ↓
HAS-A
      ↓
CommandRunner
```

The storage device can use the command runner without implementing all command-execution logic itself.

---

# 3. Storage Automation Example

Consider:

```python
class CommandRunner:

    def run(self, command):
        print("Running:", command)


class StorageDevice:

    def __init__(self):
        self.runner = CommandRunner()
```

The relationship is:

```text
StorageDevice
     ↓
   HAS-A
     ↓
CommandRunner
```

This is composition.

---

# 4. Aggregation

**Aggregation** is also a HAS-A relationship, but the contained object can exist independently of the object using it.

Example:

```python
class Employee:

    def __init__(self, name):
        self.name = name


class Company:

    def __init__(self, employee):
        self.employee = employee
```

The employee exists independently:

```python
employee = Employee("Revanth")

company = Company(employee)
```

The `Employee` object can continue to exist independently of `Company`.

---

# 5. Composition vs Aggregation

Both represent:

```text
HAS-A
```

The distinction is mainly about ownership and object lifetime.

### Composition

```text
Object A
   ↓
strongly contains
   ↓
Object B
```

Object B is generally treated as part of A's structure.

### Aggregation

```text
Object A
   ↓
uses / references
   ↓
Object B
```

Object B can exist independently.

---

# 6. HAS-A vs IS-A

This is one of the most important OOP design distinctions.

## IS-A

Represents inheritance.

Example:

```python
class StorageDevice:
    pass


class NVMeDevice(StorageDevice):
    pass
```

Relationship:

```text
NVMeDevice
    IS-A
StorageDevice
```

Therefore:

```text
IS-A → Inheritance
```

---

## HAS-A

Represents composition or aggregation.

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

Therefore:

```text
HAS-A → Composition / Aggregation
```

---

# 7. Composition vs Inheritance

Inheritance should represent a genuine:

```text
IS-A
```

relationship.

Composition should represent a:

```text
HAS-A
```

relationship.

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

These relationships should determine the design.

---

# 8. Why Prefer Composition in Many Designs?

Composition allows functionality to be assembled from separate objects.

For example:

```text
StorageDevice
     │
     ├── CommandRunner
     ├── Logger
     └── Configuration
```

Each component can have its own responsibility.

This can make components easier to replace and test.

---

# 9. Dependency

A **dependency** is something an object needs in order to perform its responsibility.

Example:

```python
class CommandRunner:

    def run(self, command):
        print("Running:", command)


class StorageDevice:

    def __init__(self, runner):
        self.runner = runner
```

`StorageDevice` needs `runner` in order to execute commands.

Therefore:

```text
CommandRunner
      ↓
dependency of
      ↓
StorageDevice
```

---

# 10. Dependency Injection

**Dependency Injection** is a design technique in which an object's dependency is supplied from outside instead of being created internally by that object.

Without injection:

```python
class StorageDevice:

    def __init__(self):
        self.runner = CommandRunner()
```

Here:

```text
StorageDevice
      ↓
creates
      ↓
CommandRunner
```

The dependency is hard-coded into the class.

---

# 11. Dependency Injection Example

With injection:

```python
class StorageDevice:

    def __init__(self, runner):
        self.runner = runner
```

Now the dependency is supplied from outside:

```python
runner = CommandRunner()

device = StorageDevice(runner)
```

The relationship becomes:

```text
Outside code
     ↓
creates dependency
     ↓
CommandRunner
     ↓
injects
     ↓
StorageDevice
```

---

# 12. Why Dependency Injection?

Dependency Injection helps with:

* Loose coupling
* Replaceability
* Reusability
* Testability

The important idea is:

```text
Dependency
    ↓
supplied from outside
    ↓
object
```

---

# 13. Constructor Injection

The most relevant form for our automation design is **constructor injection**.

Example:

```python
class StorageDevice:

    def __init__(self, runner):
        self.runner = runner
```

Then:

```python
runner = CommandRunner()
device = StorageDevice(runner)
```

The dependency is provided through `__init__()`.

---

# 14. Method Injection

A dependency can also be supplied to a specific method.

Example:

```python
class StorageDevice:

    def check_health(self, runner):
        return runner.run(
            ["nvme", "smart-log"]
        )
```

Usage:

```python
device.check_health(runner)
```

Here the dependency is supplied when the method is called.

---

# 15. Attribute / Property Injection

A dependency can also be assigned after object creation.

Example:

```python
class StorageDevice:
    pass


device = StorageDevice()

device.runner = CommandRunner()
```

The dependency is injected after object creation.

For our framework, constructor injection is the primary pattern when a dependency is required for normal object operation.

---

# 16. Dependency Injection and Replaceability

Consider two command-runner implementations:

```python
class RealCommandRunner:

    def run(self, command):
        print("Running real command")
```

and:

```python
class MockCommandRunner:

    def run(self, command):
        print("Simulating command")
```

The storage device can receive either one:

```python
device1 = StorageDevice(
    RealCommandRunner()
)

device2 = StorageDevice(
    MockCommandRunner()
)
```

`StorageDevice` does not need to change.

---

# 17. Why This Matters in Automation Testing

Real storage automation may interact with:

```text
Linux commands
SSH
NVMe tools
FIO
Storage-platform CLI tools
```

Testing every failure condition using real hardware is not always practical.

For example, we may want to test:

```text
nvme command
      ↓
device not found
```

without physically removing an NVMe drive.

A fake or mocked dependency can simulate that condition.

---

# 18. Example of a Fake Dependency

```python
class FakeCommandRunner:

    def run(self, command):
        return {
            "return_code": 1,
            "stdout": "",
            "stderr": "NVMe device not found"
        }
```

Then:

```python
runner = FakeCommandRunner()

device = StorageDevice(runner)
```

The storage-device code can now be tested against a simulated command failure.

---

# 19. Dependency Injection and Testing

The key testing benefit is **dependency replacement**.

Production:

```text
StorageDevice
      ↓
RealCommandRunner
      ↓
Linux
```

Testing:

```text
StorageDevice
      ↓
MockCommandRunner
      ↓
Simulated result
```

The main object remains unchanged.

---

# 20. Dependency Injection Does Not Require Inheritance

Dependency Injection and inheritance solve different problems.

Inheritance:

```text
NVMeDevice
    IS-A
StorageDevice
```

Dependency Injection:

```text
StorageDevice
    receives
CommandRunner
```

A dependency does not need to inherit from the class using it.

---

# 21. Dependency Injection Is Not a Python Keyword

There is no special Python keyword such as:

```python
inject
```

Dependency Injection is a design technique.

Python supports it naturally by allowing objects to be passed as arguments.

Example:

```python
class Dependency:
    pass


class Service:

    def __init__(self, dependency):
        self.dependency = dependency


dependency = Dependency()

service = Service(dependency)
```

The dependency was supplied from outside.

---

# 22. Composition and Dependency Injection Together

These concepts commonly work together.

Example:

```python
class StorageDevice:

    def __init__(self, runner):
        self.runner = runner
```

This gives us:

```text
Composition
    ↓
StorageDevice HAS-A runner
```

and:

```text
Dependency Injection
    ↓
runner was supplied from outside
```

Therefore:

```text
Composition
→ object contains/uses another object

Dependency Injection
→ dependency is externally supplied
```

They are related but not identical.

---

# 23. Composition and Dependency Injection in Automation

A future automation component could look conceptually like:

```text
NVMeDevice
    │
    ├── CommandRunner
    ├── Logger
    └── Configuration
```

The device object focuses on device-related responsibilities.

The other components provide specialized capabilities.

This separation helps keep the framework modular.

---

# 24. Storage Automation Architecture Example

A possible dependency chain is:

```text
Test
 ↓
Validator
 ↓
StorageDevice
 ↓
CommandRunner
 ↓
Linux Tool
 ↓
Storage Device
```

Another possible arrangement for a remote target is:

```text
Test
 ↓
Validator
 ↓
NVMeDevice
 ↓
SSH Executor
 ↓
Remote Linux
 ↓
nvme-cli
 ↓
NVMe SSD
```

The exact framework architecture will be designed later.

---

# 25. Dependency Injection and Mocking

Dependency Injection makes mocking easier because the test can provide a substitute dependency.

Example:

```python
real_runner = CommandRunner()

mock_runner = FakeCommandRunner()
```

Then:

```python
production_device = StorageDevice(real_runner)

test_device = StorageDevice(mock_runner)
```

This separates:

```text
Production execution
```

from:

```text
Test simulation
```

---

# 26. When Should Dependency Injection Be Used?

Use Dependency Injection when a class has an external dependency that may reasonably need to be:

* Replaced
* Mocked
* Configured
* Isolated
* Tested independently

Examples relevant to automation:

```text
Command executor
SSH client
Device interface
Configuration provider
Logger
External service
```

Do not inject every object merely to use the pattern.

The dependency should represent a meaningful responsibility.

---

# 27. Common Design Mistake

Do not write:

```python
class StorageDevice:

    def __init__(
        self,
        runner,
        logger,
        config,
        parser,
        validator,
        reporter,
        ...
    ):
        ...
```

simply because Dependency Injection exists.

Too many unnecessary dependencies make a design harder to understand.

Good design keeps the dependency list meaningful.

---

# 28. Composition vs Aggregation vs Dependency Injection

| Concept              | Main Idea                                               | Relationship               |
| -------------------- | ------------------------------------------------------- | -------------------------- |
| Composition          | Object contains another object as part of its structure | HAS-A                      |
| Aggregation          | Object uses another independently existing object       | HAS-A                      |
| Dependency Injection | Dependency is supplied from outside                     | External dependency supply |
| Inheritance          | One class derives from another                          | IS-A                       |

---

# 29. Storage Example

Consider:

```python
class CommandRunner:

    def run(self, command):
        return "command output"


class NVMeDevice:

    def __init__(self, runner):
        self.runner = runner

    def identify(self):
        return self.runner.run(
            ["nvme", "id-ctrl", "/dev/nvme0"]
        )
```

Here:

```text
NVMeDevice
      ↓
HAS-A
      ↓
CommandRunner
```

and:

```text
CommandRunner
      ↓
injected from outside
      ↓
NVMeDevice
```

The device does not create the command runner internally.

---

# 30. Practical Testing Example

Production:

```python
device = NVMeDevice(CommandRunner())

device.identify()
```

Testing:

```python
device = NVMeDevice(FakeCommandRunner())

device.identify()
```

The same `NVMeDevice` class can work with both dependencies.

---

# 31. Key Takeaways

```text
Composition
→ HAS-A relationship

Aggregation
→ HAS-A relationship with independent existence

Inheritance
→ IS-A relationship

Dependency
→ Something an object needs

Dependency Injection
→ Supply the dependency from outside

Constructor Injection
→ Dependency supplied through __init__()

Main benefits
→ Lower coupling
→ Replaceability
→ Testability
→ Reusability
```

---

# 32. Final Mental Model

```text
                 OBJECT RELATIONSHIPS
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
       IS-A            HAS-A          NEEDS
          │              │              │
          ↓              ↓              ↓
    Inheritance      Composition      Dependency
                     Aggregation          │
                                         ↓
                              Supplied from outside
                                         │
                                         ↓
                              Dependency Injection
```

---

# 33. Automation Mental Model

```text
Production Environment
        ↓
Real Dependency
        ↓
Storage Component


Test Environment
        ↓
Mock / Fake Dependency
        ↓
Same Storage Component
```

The central principle is:

> **Build objects from meaningful components, and supply replaceable dependencies from outside when doing so improves coupling, reuse, or testability.**

