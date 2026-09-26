# Polymorphism

## 1. What is Polymorphism?

**Polymorphism** means that the same interface, method, or operation can work with different objects and produce behavior appropriate to each object.

The core idea is:

```text id="p4se1k"
Same operation
      ↓
Different objects
      ↓
Different behavior
```

The Python roadmap identifies these polymorphism concepts:

* Polymorphism
* Method Overriding
* Duck Typing
* Common Interfaces
* Practical Polymorphism

---

# 2. Simple Example

Consider:

```python id="9k50ps"
class NVMeDevice:

    def identify(self):
        print("Identifying NVMe device")


class SATADevice:

    def identify(self):
        print("Identifying SATA device")
```

Both classes provide:

```python id="uhgxt3"
identify()
```

But each implementation behaves differently.

```python id="pxi1kt"
nvme = NVMeDevice()
sata = SATADevice()

nvme.identify()
sata.identify()
```

Output:

```text id="0t0x1g"
Identifying NVMe device
Identifying SATA device
```

The operation is the same:

```text id="b5h7dh"
identify()
```

but the behavior is different.

---

# 3. Why Polymorphism?

Polymorphism allows code to interact with different objects through a common operation without needing completely separate code for each type.

Without polymorphism, code might become:

```python id="gdg09w"
if device_type == "NVMe":
    ...
elif device_type == "SATA":
    ...
elif device_type == "SAS":
    ...
```

With polymorphism, we can often write:

```python id="7s1e7w"
device.identify()
```

and let the object provide the appropriate behavior.

---

# 4. Method Overriding

Method overriding occurs when a child class provides its own implementation of a method inherited from a parent class.

Example:

```python id="9t7n99"
class StorageDevice:

    def identify(self):
        print("Generic storage device")


class NVMeDevice(StorageDevice):

    def identify(self):
        print("NVMe device")
```

Now:

```python id="l23f7q"
device = NVMeDevice()

device.identify()
```

produces:

```text id="p9e8gd"
NVMe device
```

The child implementation overrides the parent's implementation.

---

# 5. Polymorphism Through Inheritance

A common pattern is:

```python id="64v5c5"
class StorageDevice:

    def identify(self):
        print("Generic storage")


class NVMeDevice(StorageDevice):

    def identify(self):
        print("NVMe")


class SATADevice(StorageDevice):

    def identify(self):
        print("SATA")
```

Now:

```python id="zb3hhr"
devices = [
    NVMeDevice(),
    SATADevice()
]

for device in devices:
    device.identify()
```

Output:

```text id="yl05s0"
NVMe
SATA
```

The loop does not need to know which specific device class it is processing.

---

# 6. Common Interface

A **common interface** means different objects provide a consistent set of operations.

For example:

```text id="v5i1dy"
NVMeDevice
    ├── identify()
    └── check_health()

SATADevice
    ├── identify()
    └── check_health()
```

Both provide:

```text id="1l97ci"
identify()
check_health()
```

Their internal implementation can differ.

This allows client code to interact with them consistently.

---

# 7. Common Interface Does Not Mean Same Implementation

Suppose:

```python id="vqfdw6"
class NVMeDevice:

    def check_health(self):
        print("Reading NVMe health information")


class SATADevice:

    def check_health(self):
        print("Reading SATA health information")
```

Both implement:

```python id="9hge3l"
check_health()
```

But they may use completely different internal mechanisms.

Therefore:

```text id="loaw6z"
Common interface
≠
Common implementation
```

---

# 8. Practical Polymorphism

Practical polymorphism means writing code that operates on objects through their common behavior instead of writing separate logic for every object type.

Example:

```python id="y3ki8r"
def run_health_check(device):
    device.check_health()
```

Now:

```python id="oxiwv9"
run_health_check(NVMeDevice())
run_health_check(SATADevice())
```

The function does not need to know how each device performs the health check.

It only requires that the object provide:

```python id="rqa7ui"
check_health()
```

---

# 9. Polymorphism Reduces Type-Specific Logic

Without polymorphism:

```python id="a1tk0v"
def run_check(device):

    if isinstance(device, NVMeDevice):
        device.nvme_health_check()

    elif isinstance(device, SATADevice):
        device.sata_health_check()
```

With polymorphism:

```python id="dv4g9z"
def run_check(device):
    device.check_health()
```

Each object decides how its own `check_health()` operation works.

This generally makes the client code simpler.

---

# 10. Duck Typing

Python also supports polymorphism through **duck typing**.

The idea is:

> The object is used based on what it can do rather than what class it belongs to.

A common mental model is:

```text id="oocqjg"
"If it provides the required behavior,
I can use it."
```

---

# 11. Duck Typing Example

Consider:

```python id="wgw8py"
class NVMeDevice:

    def identify(self):
        print("NVMe identification")


class MockStorageDevice:

    def identify(self):
        print("Mock identification")
```

There is no inheritance relationship between these classes.

But both provide:

```python id="dmjbj2"
identify()
```

We can write:

```python id="r6y9d4"
def run_identification(device):
    device.identify()
```

Then:

```python id="l9x1st"
run_identification(NVMeDevice())
run_identification(MockStorageDevice())
```

Both work because the required operation exists.

---

# 12. Duck Typing Does Not Require Inheritance

This is an important distinction.

Consider:

```text id="h8pj8u"
NVMeDevice
      IS-A
StorageDevice
```

This is inheritance-based polymorphism.

But:

```text id="yu6snu"
MockStorageDevice
      and
NVMeDevice
```

can both support:

```text id="3g2zua"
identify()
```

without sharing a base class.

That is duck typing.

---

# 13. Duck Typing Mental Model

```text id="p57u7z"
Required behavior
      ↓
Does the object provide it?
      ↓
Yes → use it
No  → failure
```

The focus is on **capability** rather than class hierarchy.

---

# 14. Storage Automation Example

Suppose our test runner expects an object with:

```python id="cvjk2p"
run_validation()
```

We could have:

```python id="c7q9v4"
class NVMeValidation:

    def run_validation(self):
        print("NVMe validation")


class MockValidation:

    def run_validation(self):
        print("Mock validation")
```

Then:

```python id="gyy7g5"
def execute(validation):
    validation.run_validation()
```

The function does not care whether the object is:

```text id="3m0jeh"
NVMeValidation
```

or:

```text id="q70zdm"
MockValidation
```

It only cares that:

```python id="54x6ut"
run_validation()
```

exists.

---

# 15. Duck Typing and Testing

Duck typing is particularly useful when testing because a test can use a lightweight substitute object that provides the required behavior.

Example:

```python id="2l6i5u"
class FakeCommandRunner:

    def run(self, command):
        return "simulated output"
```

A component that only requires:

```python id="6ca5v2"
runner.run(...)
```

can use this fake object even though `FakeCommandRunner` does not inherit from the production command-runner class.

This idea becomes useful later when we study mocking and test isolation.

---

# 16. Common Interface and Duck Typing

These concepts are related, but not identical.

### Common interface

Focuses on:

```text id="m1mgn2"
Different objects provide the same expected operations
```

### Duck typing

Focuses on:

```text id="uhdc8x"
The object's capabilities matter more than its declared type
```

Python allows the interface to be informal.

---

# 17. Polymorphism Through Different Implementations

Consider:

```python id="r9f5o0"
class NVMeDevice:

    def reset(self):
        print("NVMe reset")


class SATADevice:

    def reset(self):
        print("SATA reset")


class MockDevice:

    def reset(self):
        print("Mock reset")
```

We can write:

```python id="7u7o9j"
def reset_device(device):
    device.reset()
```

Now:

```python id="jgd3ia"
reset_device(NVMeDevice())
reset_device(SATADevice())
reset_device(MockDevice())
```

The caller uses one interface:

```python id="e0bdsm"
reset()
```

while each object supplies different behavior.

---

# 18. Polymorphism and Abstraction

These concepts often work together.

### Abstraction

Defines what the object should provide.

Example:

```text id="o4k6f1"
Device
→ identify()
→ reset()
→ check_health()
```

### Polymorphism

Allows different objects to implement those operations differently.

```text id="c75va3"
NVMeDevice
→ NVMe implementation

SATADevice
→ SATA implementation
```

So:

```text id="hgl8mm"
Abstraction
   ↓
common contract / expected behavior

Polymorphism
   ↓
different implementations
```

---

# 19. Polymorphism and Inheritance

Inheritance can provide the relationship:

```text id="ypb09v"
NVMeDevice
    IS-A
StorageDevice
```

and method overriding can provide different behavior:

```text id="da4g5n"
StorageDevice.identify()
        ↓
NVMeDevice.identify()
```

That produces inheritance-based polymorphism.

But Python also supports polymorphism without inheritance through duck typing.

---

# 20. Generic Function Example

A practical polymorphic function should focus on the operation it needs.

Example:

```python id="l8qhec"
def collect_health(device):
    return device.check_health()
```

This function can work with any object that provides:

```python id="biw8qy"
check_health()
```

This is useful because the function does not contain type-specific implementation details.

---

# 21. Storage Validation Example

Suppose:

```python id="34akj5"
class NVMeDevice:

    def check_health(self):
        return "NVMe health data"


class SATADevice:

    def check_health(self):
        return "SATA health data"
```

Then:

```python id="dpcyo4"
def validate_device(device):
    health = device.check_health()
    print(health)
```

Usage:

```python id="71lcqz"
validate_device(NVMeDevice())
validate_device(SATADevice())
```

The validator is generic.

The device implementation remains device-specific.

---

# 22. Why This Matters in Automation Frameworks

A well-designed framework may contain common operations such as:

```text id="kzc7y9"
identify()
check_health()
reset()
collect_logs()
validate()
```

Different implementations may support these operations.

For example:

```text id="2y5xqo"
RealNVMeDevice
MockNVMeDevice
RemoteNVMeDevice
```

All may provide:

```text id="g5r5i6"
identify()
check_health()
```

The higher-level test code can operate against the common behavior.

---

# 23. Polymorphism and Framework Extensibility

Suppose the framework initially supports:

```text id="u4ajba"
NVMe
```

Later we add:

```text id="r7n9a6"
SAS
```

If the framework depends on a common interface:

```text id="mql0jt"
identify()
check_health()
reset()
```

we can add the new implementation without rewriting every higher-level operation.

This is one of the practical benefits of polymorphism.

---

# 24. Method Overriding vs Duck Typing

### Method Overriding

Usually involves inheritance:

```text id="f1k4kb"
Base class
   ↓
Child class
   ↓
override method
```

### Duck Typing

Does not require inheritance:

```text id="7dt9wt"
Object A ──┐
           ├── provides check_health()
Object B ──┘
```

Both can be used by a function that requires `check_health()`.

---

# 25. Common Mistakes

## Mistake 1 — Thinking polymorphism always requires inheritance

It does not.

Duck typing provides polymorphism without inheritance.

---

## Mistake 2 — Thinking different classes must have identical internal code

They do not.

Only the required interface/behavior needs to be compatible.

---

## Mistake 3 — Excessive `isinstance()` checks

If every function contains:

```python id="hlq2up"
if isinstance(...):
```

for every device type, the design may not be using polymorphism effectively.

Often the object itself should provide the required behavior.

---

## Mistake 4 — Assuming duck typing ignores errors

Duck typing does not magically guarantee that an object has the required method.

If the required operation is absent, the call can fail.

---

# 26. Polymorphism in Storage Automation

A possible architecture:

```text id="7j1qhd"
                    Validation
                       │
                       ↓
                 common interface
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       NVMeDevice   SATADevice   MockDevice
          │            │            │
          ↓            ↓            ↓
      NVMe logic    SATA logic   Test logic
```

The validation layer can operate on the common behavior.

---

# 27. Practical Example with Duck Typing

```python id="4xv8fz"
class NVMeDevice:

    def check_health(self):
        return "NVMe health: PASS"


class MockDevice:

    def check_health(self):
        return "Mock health: PASS"


def run_health_validation(device):
    result = device.check_health()
    print(result)


run_health_validation(NVMeDevice())
run_health_validation(MockDevice())
```

No inheritance is required.

The function depends only on the presence of:

```python id="d4i6e5"
check_health()
```

---

# 28. Practical Example with Inheritance

```python id="33v1jr"
class StorageDevice:

    def check_health(self):
        return "Generic health"


class NVMeDevice(StorageDevice):

    def check_health(self):
        return "NVMe health"


class SATADevice(StorageDevice):

    def check_health(self):
        return "SATA health"


def run_health_validation(device):
    print(device.check_health())
```

Now:

```python id="is9qdz"
run_health_validation(NVMeDevice())
run_health_validation(SATADevice())
```

Again, one operation produces different behavior.

---

# 29. Key Takeaways

```text id="6jntx3"
Polymorphism
→ Same interface/operation, different behavior

Method Overriding
→ Child replaces inherited implementation

Common Interface
→ Different objects expose common operations

Duck Typing
→ Focus on supported behavior rather than declared type

Practical Polymorphism
→ Generic code works with different compatible objects

Inheritance-based polymorphism
→ Uses inheritance + overriding

Duck-typed polymorphism
→ Does not require inheritance
```

---

# 30. Final Mental Model

```text id="x6eqc9"
                 COMMON OPERATION
                        │
            ┌───────────┼───────────┐
            ↓           ↓           ↓
         NVMe         SATA        Mock
            │           │           │
            ↓           ↓           ↓
       NVMe logic   SATA logic   Mock logic
```

The caller can use:

```python id="yq3stt"
device.check_health()
```

without needing to know the internal implementation.

The central principle is:

> **Polymorphism allows common code to work with different objects while each object provides its own appropriate behavior.**

