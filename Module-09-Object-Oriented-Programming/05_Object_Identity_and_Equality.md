# Object Identity and Equality

## 1. What is Object Identity?

**Object identity** refers to the fact that every object created in Python is a distinct object.

Even when two objects contain the same data, they can still be two different objects.

Example:

```python id="dj0pnm"
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number


device1 = StorageDevice("SN1001")
device2 = StorageDevice("SN1001")
```

Both objects contain:

```text id="jpwv7b"
serial_number = SN1001
```

but they are still separate objects.

---

# 2. `id()`

Python provides the built-in:

```python id()
```

which returns an identity value for an object during its lifetime.

Example:

```python id="zkzuxv"
print(id(device1))
print(id(device2))
```

The values will normally be different because `device1` and `device2` are different objects.

Mental model:

```text id="k7kzpt"
device1
   ↓
Object A
   ↓
identity A


device2
   ↓
Object B
   ↓
identity B
```

---

# 3. Identity vs Value

Two objects can have:

```text id="4h9q2g"
same value
```

while still having:

```text id="0xas6x"
different identity
```

Example:

```python id="2hcl84"
device1 = StorageDevice("SN1001")
device2 = StorageDevice("SN1001")
```

They may represent the same logical device information, but they are two separately created Python objects.

---

# 4. The `is` Operator

The `is` operator checks **object identity**.

Example:

```python id="ikv6um"
device1 is device2
```

This asks:

> Are these two references pointing to the exact same object?

For separately created objects:

```python id="ze7e9w"
device1 = StorageDevice("SN1001")
device2 = StorageDevice("SN1001")

print(device1 is device2)
```

the result is:

```text id="jyq6ty"
False
```

---

# 5. Same Object

Consider:

```python id="9wkhrp"
device1 = StorageDevice("SN1001")
device2 = device1
```

Now both variables refer to the same object.

Conceptually:

```text id="rq6g0x"
device1 ─────┐
             ↓
          Object A
             ↑
device2 ─────┘
```

Therefore:

```python id="quk3xl"
print(device1 is device2)
```

returns:

```text id="2zt44y"
True
```

---

# 6. `==` Operator

The `==` operator checks **equality**.

It asks:

> Do these two values compare as equal?

Example:

```python id="f9njyf"
device1 == device2
```

The meaning of equality for custom objects depends on how the class defines it.

This is different from `is`.

---

# 7. `is` vs `==`

This distinction is extremely important.

### `is`

Checks:

```text id="tdaz1q"
Identity
```

Meaning:

> Are these the exact same object?

### `==`

Checks:

```text id="t9mz1i"
Equality
```

Meaning:

> Do these values compare as equal?

Mental model:

```text id="f4v2bm"
is
↓
same object?


==
↓
same value / logically equal?
```

---

# 8. Example Without Custom `__eq__()`

```python id="qfvwhq"
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number


device1 = StorageDevice("SN1001")
device2 = StorageDevice("SN1001")

print(device1 is device2)
print(device1 == device2)
```

The first expression is clearly:

```text id="nke2r1"
False
```

because they are different objects.

Without a custom equality definition, the second comparison also does not automatically mean "same serial number".

---

# 9. Defining Logical Equality with `__eq__()`

We can define what equality means for our class.

Example:

```python id="zmpupg"
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number

    def __eq__(self, other):
        if not isinstance(other, StorageDevice):
            return NotImplemented

        return self.serial_number == other.serial_number
```

Now:

```python id="17ez5k"
device1 = StorageDevice("SN1001")
device2 = StorageDevice("SN1001")
```

we can have:

```python id="nacuv8"
print(device1 == device2)
```

which returns:

```text id="0uw0r6"
True
```

because our class defines them as logically equal when their serial numbers match.

But:

```python id="ki3qkv"
print(device1 is device2)
```

still returns:

```text id="3m0p0t"
False
```

because they remain separate objects.

---

# 10. Identity and Equality Together

Consider:

```python id="1e2eea"
device1 = StorageDevice("SN1001")
device2 = StorageDevice("SN1001")
device3 = device1
```

Then:

```python id="0qg0b4"
device1 is device2
```

is:

```text id="h0h1hj"
False
```

because they are different objects.

But:

```python id="ivfws6"
device1 == device2
```

may be:

```text id="1b0u5d"
True
```

because their serial numbers are equal according to `__eq__()`.

And:

```python id="4d1n3r"
device1 is device3
```

is:

```text id="g1p8bw"
True
```

because both names reference the same object.

---

# 11. Why `is` Should Not Normally Be Used for Value Comparison

Suppose:

```python id="q5k9bg"
status1 = "PASS"
status2 = "PASS"
```

The correct conceptual operation for checking their values is:

```python id="7l3ovf"
status1 == status2
```

not:

```python id="y5rnnr"
status1 is status2
```

Use `is` when identity itself matters.

Use `==` when value equality matters.

---

# 12. `None` and `is`

One common Python pattern is:

```python id="yhb8ls"
if result is None:
    ...
```

Here identity is appropriate because `None` is a singleton object.

The important general rule remains:

```text id="pfkq3o"
is  → identity
==  → equality
```

---

# 13. Reference Assignment

Consider:

```python id="8z6tih"
device1 = StorageDevice("SN1001")
device2 = device1
```

No new `StorageDevice` object is created for `device2`.

Instead:

```text id="j5le7s"
device1 ──┐
          ↓
       same object
          ↑
device2 ──┘
```

Therefore:

```python id="m0i1aw"
device1 is device2
```

returns:

```text id="9ypsww"
True
```

---

# 14. Changing Through One Reference

Because `device1` and `device2` point to the same object:

```python id="bai27l"
device2.serial_number = "SN2001"

print(device1.serial_number)
```

will produce:

```text id="3p5b2i"
SN2001
```

The change is visible through both references because they reference the same object.

---

# 15. Two Different Objects with the Same Data

Consider:

```python id="0bvwv6"
device1 = StorageDevice("SN1001")
device2 = StorageDevice("SN1001")
```

Conceptually:

```text id="cqxfak"
device1 → Object A → SN1001

device2 → Object B → SN1001
```

Same data:

```text id="9bxygy"
SN1001
```

Different objects:

```text id="7e1xqm"
Object A ≠ Object B
```

So identity and equality are separate concepts.

---

# 16. Why This Matters in Storage Automation

Storage automation frequently deals with logical resources such as:

```text id="8h4irx"
Drive
Controller
Namespace
Volume
LUN
Validation Result
```

Two Python objects may represent:

```text id="qy8dqn"
the same logical device
```

without being:

```text id="0jyl8c"
the same Python object
```

For example:

```python id="bvxw3k"
device_from_discovery
device_from_inventory
```

may contain the same serial number.

We might want:

```python id="ryquz6"
device_from_discovery == device_from_inventory
```

to represent logical equality.

But:

```python id="8i2tnw"
device_from_discovery is device_from_inventory
```

may still be `False`.

---

# 17. Equality Depends on Domain Rules

There is no universal answer for what makes two storage-device objects equal.

The class designer must define the rule.

Possible identifiers might include:

```text id="wdd1jx"
Serial Number
WWN
NQN
Device Identifier
Controller Identifier
```

The correct equality rule depends on what the object represents.

For a drive object, serial number may be an appropriate logical identity.

For another object, a different identifier may be appropriate.

---

# 18. `id()` Is Not a Device Identifier

This is very important for storage automation.

Python:

```python id(device)
```

is an identifier for the Python object during its lifetime.

It is **not**:

```text id="7j4y00"
SSD serial number
NVMe namespace ID
WWN
NQN
PCIe device address
```

For example:

```python id="9jps1p"
id(device)
```

might return some integer such as:

```text id="xw6biw"
140123456789
```

That number should not be treated as the physical device's identifier.

---

# 19. Equality and `__eq__()`

When a class implements:

```python id="nyqz8w"
def __eq__(self, other):
    ...
```

Python can use that definition when evaluating:

```python id="dyo3r9"
device1 == device2
```

This allows the class to define meaningful logical equality.

---

# 20. Safe `__eq__()` Design

A defensive implementation is:

```python id="2h5ik8"
def __eq__(self, other):

    if not isinstance(other, StorageDevice):
        return NotImplemented

    return self.serial_number == other.serial_number
```

This prevents the method from assuming that every object being compared has:

```python id="g5k6aq"
serial_number
```

---

# 21. Identity Test Example

```python id="ehwq8h"
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number


device1 = StorageDevice("SN1001")
device2 = device1
device3 = StorageDevice("SN1001")

print(device1 is device2)
print(device1 is device3)
```

Expected:

```text id="ejhw28"
True
False
```

Because:

```text id="1w1pkz"
device1 and device2
→ same object

device1 and device3
→ different objects
```

---

# 22. Equality Test Example

```python id="n4cahp"
class StorageDevice:

    def __init__(self, serial_number):
        self.serial_number = serial_number

    def __eq__(self, other):

        if not isinstance(other, StorageDevice):
            return NotImplemented

        return self.serial_number == other.serial_number


device1 = StorageDevice("SN1001")
device2 = StorageDevice("SN1001")
device3 = StorageDevice("SN2001")

print(device1 == device2)
print(device1 == device3)
```

Result:

```text id="5s38b0"
True
False
```

---

# 23. Identity + Equality Example

```python id="hc3y1h"
device1 = StorageDevice("SN1001")
device2 = StorageDevice("SN1001")
device3 = device1
```

| Comparison           | Meaning          | Result  |
| -------------------- | ---------------- | ------- |
| `device1 is device2` | Same object?     | `False` |
| `device1 == device2` | Logically equal? | `True`  |
| `device1 is device3` | Same object?     | `True`  |
| `device1 == device3` | Logically equal? | `True`  |

---

# 24. Common Mistakes

## Mistake 1 — Using `is` for ordinary value comparison

Incorrect:

```python id="eqd3sr"
if status is "PASS":
    ...
```

Use value comparison:

```python id="v5wj2d"
if status == "PASS":
    ...
```

The important principle is that `is` tests identity rather than string/value equality.

---

## Mistake 2 — Thinking same data means same object

```python id="5ks3q0"
device1 = StorageDevice("SN1001")
device2 = StorageDevice("SN1001")
```

These are still two different objects.

---

## Mistake 3 — Thinking different objects cannot be equal

With a suitable `__eq__()` implementation, different objects can be logically equal.

---

## Mistake 4 — Treating Python `id()` as hardware identity

`id()` identifies the Python object, not the storage device.

---

# 25. Identity vs Equality in Automation

This distinction becomes useful when automation compares:

```text id="3wblcm"
Expected Device
        vs
Discovered Device
```

Suppose:

```python id="rsbwxx"
expected = StorageDevice("SN1001")
actual = StorageDevice("SN1001")
```

They can be:

```python id="0bnjtm"
expected == actual
```

while:

```python id="4t6tqy"
expected is actual
```

remains false.

For validation, logical equality is generally more useful than asking whether two independently created Python objects are the exact same instance.

---

# 26. Relationship with `__eq__()`

The concepts are connected:

```text id="1whn7w"
Object Identity
       ↓
is
```

and:

```text id="d4l6e1"
Object Equality
       ↓
==
       ↓
__eq__()
```

So:

```text id="pluf8t"
a is b
→ identity comparison

a == b
→ equality comparison
→ can invoke a.__eq__(b)
```

---

# 27. Final Mental Model

```text id="p3il7p"
                 TWO OBJECTS
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
      Identity               Equality
          │                     │
          ↓                     ↓
         is                     ==
          │                     │
          ↓                     ↓
   Same exact object?     Logically equal?
```

---

# 28. Key Takeaways

```text id="7yyb9f"
Object Identity
→ Whether two references point to the same object

id()
→ Python object identity value during the object's lifetime

is
→ Identity comparison

Equality
→ Whether two objects compare as equal

==
→ Equality comparison

__eq__()
→ Defines equality behavior for a custom class

Same identity
→ Same object

Different identity
→ Can still be equal

id()
→ Python object identity
→ NOT hardware/device identity
```

---

# 29. Storage Automation Example to Remember

```text id="fsn8jx"
Python Object
      ↓
id()
      ↓
Python object identity


Storage Device
      ↓
serial number / WWN / NQN / other identifier
      ↓
Domain-specific device identity
```

These are different concepts.

The core rule is:

> **Use `is` when object identity matters; use `==` when logical/value equality matters.**

