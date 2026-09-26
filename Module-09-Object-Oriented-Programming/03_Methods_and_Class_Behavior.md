# Methods and Class Behavior

## 1. What is a Method?

A **method** is a function defined inside a class and used to represent behavior associated with objects or the class itself.

Example:

```python
class StorageDevice:

    def identify(self):
        print("Storage device identified")
```

Here:

```text
identify()
    ↓
method of StorageDevice
```

A method can access the object's state and perform operations related to that object.

---

# 2. Instance Methods

An **instance method** operates on a particular object instance.

Example:

```python
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number

    def identify(self):
        print(self.serial_number)
```

Create an object:

```python
device = StorageDevice("SN1001")

device.identify()
```

The method operates on the specific `device` object.

---

# 3. `self` in Instance Methods

Instance methods normally receive the current object through `self`.

Example:

```python
class StorageDevice:

    def show_serial(self):
        print(self.serial_number)
```

When:

```python
device.show_serial()
```

Python supplies the instance as `self`.

Conceptually:

```text
device.show_serial()
        ↓
show_serial(device)
```

`self` allows the method to access instance attributes and other instance methods.

---

# 4. Instance Method Accessing Multiple Attributes

Example:

```python
class StorageDevice:

    def __init__(self, serial_number, model):
        self.serial_number = serial_number
        self.model = model

    def identify(self):
        print("Serial:", self.serial_number)
        print("Model:", self.model)
```

The method operates on the state belonging to the current object.

---

# 5. Methods with Parameters

An instance method can accept additional parameters.

Example:

```python
class StorageDevice:

    def update_firmware(self, version):
        print("Updating firmware to:", version)
```

Usage:

```python
device.update_firmware("1.2.0")
```

Here:

```text
self
→ current object

version
→ method argument
```

---

# 6. Methods with Return Values

Methods can return values just like normal functions.

Example:

```python
class StorageDevice:

    def get_temperature(self):
        return self._temperature
```

Usage:

```python
temperature = device.get_temperature()

print(temperature)
```

The return value can then be used by another part of the program.

---

# 7. Instance Method Responsibilities

A good instance method should generally perform behavior related to the object it belongs to.

For example:

```python
class StorageDevice:

    def check_health(self):
        ...

    def identify(self):
        ...

    def reset(self):
        ...
```

These operations are naturally associated with a storage device.

---

# 8. Class Methods

A **class method** operates in relation to the class rather than one specific object.

It is declared using:

```python
@classmethod
```

and receives the class as the first argument, conventionally named `cls`.

Example:

```python
class StorageDevice:

    device_count = 0

    @classmethod
    def get_device_count(cls):
        return cls.device_count
```

Usage:

```python
print(StorageDevice.get_device_count())
```

---

# 9. `cls`

For a class method:

```python
@classmethod
def method_name(cls):
    ...
```

`cls` refers to the class itself.

Compare:

```text
Instance method
→ self → object instance

Class method
→ cls → class
```

---

# 10. Class Method Example

```python
class StorageDevice:

    device_count = 0

    def __init__(self):
        StorageDevice.device_count += 1

    @classmethod
    def get_device_count(cls):
        return cls.device_count
```

Create objects:

```python
device1 = StorageDevice()
device2 = StorageDevice()
```

Then:

```python
print(StorageDevice.get_device_count())
```

returns:

```text
2
```

The method is concerned with class-level state.

---

# 11. Why Use Class Methods?

Class methods are useful when the operation:

* relates to the class
* works with class-level state
* provides an alternate way to construct an object
* represents behavior shared at the class level

Example:

```python
class StorageDevice:

    default_type = "NVMe"

    @classmethod
    def get_default_type(cls):
        return cls.default_type
```

---

# 12. Class Method as an Alternate Constructor

A class method can be used as an alternate constructor.

Example:

```python
class StorageDevice:

    def __init__(self, model, capacity):
        self.model = model
        self.capacity = capacity

    @classmethod
    def from_string(cls, value):
        model, capacity = value.split(",")
        return cls(model, capacity)
```

Usage:

```python
device = StorageDevice.from_string("NVMeSSD,1TB")
```

The class method creates an object using a different input format.

The important idea is:

```text
Class method
     ↓
creates / manages
     ↓
class-related objects or state
```

---

# 13. Static Methods

A **static method** is a method placed inside a class namespace but does not automatically receive `self` or `cls`.

It is declared using:

```python
@staticmethod
```

Example:

```python
class StorageDevice:

    @staticmethod
    def validate_serial(serial_number):
        return serial_number.startswith("SN")
```

Usage:

```python
print(StorageDevice.validate_serial("SN1001"))
```

---

# 14. Why Static Methods?

A static method is useful when functionality is related conceptually to the class but does not need:

```text
self
```

or:

```text
cls
```

Example:

```python
class StorageDevice:

    @staticmethod
    def validate_serial(serial_number):
        if not serial_number.startswith("SN"):
            return False

        return True
```

The validation does not need a particular device object or class state.

---

# 15. Instance vs Class vs Static Method

## Instance Method

```python
def identify(self):
    ...
```

Uses:

```text
self
```

Represents behavior of a specific object.

---

## Class Method

```python
@classmethod
def get_count(cls):
    ...
```

Uses:

```text
cls
```

Represents class-level behavior.

---

## Static Method

```python
@staticmethod
def validate_serial(serial):
    ...
```

Uses neither:

```text
self
cls
```

It is a utility logically associated with the class.

---

# 16. Comparison Table

| Method Type     | First Argument     | Works With         | Typical Use                                     |
| --------------- | ------------------ | ------------------ | ----------------------------------------------- |
| Instance Method | `self`             | Object state       | Device operations                               |
| Class Method    | `cls`              | Class state        | Class-level operations / alternate constructors |
| Static Method   | None automatically | Independent inputs | Related utility logic                           |

---

# 17. Storage Example Using All Three

```python
class StorageDevice:

    device_count = 0

    def __init__(self, serial_number, model):
        self.serial_number = serial_number
        self.model = model
        StorageDevice.device_count += 1

    def identify(self):
        return self.serial_number, self.model

    @classmethod
    def get_device_count(cls):
        return cls.device_count

    @staticmethod
    def validate_serial(serial_number):
        return (
            serial_number.startswith("SN")
            and len(serial_number) == 6
        )
```

Usage:

```python
device = StorageDevice("SN1001", "NVMeSSD")

print(device.identify())

print(StorageDevice.get_device_count())

print(StorageDevice.validate_serial("SN1001"))
```

Each method has a different responsibility.

---

# 18. Method Parameters

Methods can receive:

* positional arguments
* keyword arguments
* default arguments
* variable arguments

Example:

```python
class StorageDevice:

    def configure(self, mode="default"):
        print("Mode:", mode)
```

Usage:

```python
device.configure()

device.configure("performance")
```

The same Python parameter rules learned for normal functions apply to methods.

---

# 19. Return Values

A method may:

```text
return nothing
return one value
return multiple values
return an object
return a collection
raise an exception
```

Example:

```python
class StorageDevice:

    def get_health(self):
        return {
            "temperature": 35,
            "status": "PASSED"
        }
```

The caller receives structured information.

---

# 20. Method Calling Another Method

An instance method can call another instance method using `self`.

Example:

```python
class StorageDevice:

    def identify(self):
        return self.serial_number

    def display_information(self):
        serial = self.identify()
        print("Serial:", serial)
```

The object can coordinate its own behavior through its methods.

---

# 21. Class Method Calling Class State

A class method can work with class-level state through `cls`.

Example:

```python
class StorageDevice:

    device_count = 0

    @classmethod
    def get_device_count(cls):
        return cls.device_count
```

Using `cls` makes the method operate on the class that invoked it.

---

# 22. Static Method and Class Namespace

A static method belongs to the class namespace:

```python
class StorageDevice:

    @staticmethod
    def validate_serial(serial):
        ...
```

but does not automatically receive an object or class reference.

Therefore it is not inherently tied to object state.

---

# 23. Choosing the Correct Method Type

Ask:

### Does the method need an individual object's state?

Use:

```text
Instance method
```

Example:

```python
device.check_health()
```

---

### Does the method need class-level state?

Use:

```text
Class method
```

Example:

```python
StorageDevice.get_device_count()
```

---

### Does the method need neither object nor class state?

Use:

```text
Static method
```

Example:

```python
StorageDevice.validate_serial("SN1001")
```

---

# 24. Important Design Principle

Do not use `@staticmethod` or `@classmethod` simply because they are available.

Choose based on responsibility and required state.

```text
Needs object state
→ instance method

Needs class state
→ class method

Needs neither
→ static method
```

---

# 25. Storage Automation Relevance

Methods are important because automation components need clearly defined behaviors.

For example:

```text
StorageDevice
├── identify()
├── check_health()
├── reset()
└── get_firmware()

Validator
├── validate_health()
├── validate_firmware()
└── validate_temperature()

LogParser
├── parse()
├── find_errors()
└── extract_events()
```

Each method should perform a responsibility belonging to its object.

---

# 26. Connection to Automation Design

Later, an automation component may look conceptually like:

```text
Test
 ↓
Validator
 ↓
StorageDevice
 ↓
CommandRunner
```

For example:

```python
device.check_health()
```

might internally use a command execution dependency.

The public method provides the behavior while implementation details remain inside the class.

---

# 27. Instance, Class and Static Methods in Framework Design

A useful mental model:

```text
Object-specific operation
        ↓
Instance Method
```

```text
Class-wide operation
        ↓
Class Method
```

```text
Independent helper logically related to class
        ↓
Static Method
```

---

# 28. Common Mistakes

## Mistake 1 — Forgetting `self`

Incorrect:

```python
class StorageDevice:

    def identify():
        print("Device")
```

Correct:

```python
class StorageDevice:

    def identify(self):
        print("Device")
```

---

## Mistake 2 — Using `self` in a static method

Incorrect:

```python
@staticmethod
def validate(serial):
    print(self.serial_number)
```

A static method does not automatically receive `self`.

---

## Mistake 3 — Using instance state from a class method

A class method has `cls`, not a specific object `self`.

---

## Mistake 4 — Making every helper static

Not every utility belongs inside a class.

Sometimes a normal module-level function is more appropriate.

Good design is about responsibility, not maximizing the use of OOP features.

---

# 29. Key Takeaways

```text
Method
→ Function defined inside a class

Instance Method
→ Uses self
→ Works with object state

Class Method
→ Uses cls
→ Works with class state

Static Method
→ No automatic self or cls
→ Independent utility related to the class

Parameters
→ Allow methods to receive input

Return Values
→ Allow methods to provide results
```

---

# 30. Final Mental Model

```text
                    METHODS
                       │
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
   INSTANCE          CLASS          STATIC
     METHOD           METHOD          METHOD
       │               │               │
      self             cls          no automatic
       │               │             object/class
       ↓               ↓               ↓
 Object State       Class State     Independent
                                      Logic
```

The core rule is:

> **Choose the method type based on what state and responsibility the operation needs.**

