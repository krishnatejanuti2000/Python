# `14_JSON.md`

# JSON

## 1. Introduction

JSON (**JavaScript Object Notation**) is a lightweight text format used to represent structured data.

It is extremely common in automation because many tools and systems exchange information using JSON.

Examples include:

* REST APIs
* Test configuration
* Test results
* Device information
* Storage metadata
* Automation parameters
* Command output
* Machine-readable reports

Example JSON:

```json
{
    "device": "device_01",
    "status": "ONLINE",
    "capacity_gb": 1024
}
```

Python provides the standard-library:

```python
import json
```

for working with JSON.

---

# 2. Why JSON Matters in Storage Automation

A storage automation framework may receive information such as:

```json
{
    "device": "nvme0",
    "model": "ExampleDrive",
    "capacity_gb": 2048,
    "status": "ONLINE"
}
```

Python can parse this information and work with individual fields.

For example:

```python
device_data["status"]
```

can give:

```text
ONLINE
```

This is much easier and safer than trying to parse arbitrary formatted text.

---

# 3. JSON Data Types

JSON supports several fundamental data types:

```text
Object
Array
String
Number
Boolean
Null
```

Example:

```json
{
    "name": "device_01",
    "capacity": 1024,
    "online": true,
    "temperature": null,
    "features": [
        "NVMe",
        "SMART"
    ]
}
```

Here:

| JSON          | Meaning |
| ------------- | ------- |
| `"device_01"` | String  |
| `1024`        | Number  |
| `true`        | Boolean |
| `null`        | Null    |
| `[...]`       | Array   |
| `{...}`       | Object  |

---

# 4. JSON Object

A JSON object is represented using:

```text
{
    ...
}
```

Example:

```json
{
    "device": "device_01",
    "status": "ONLINE"
}
```

It consists of key-value pairs.

Conceptually:

```text
key       → value
device    → device_01
status    → ONLINE
```

---

# 5. JSON Array

A JSON array is represented using:

```text
[
    ...
]
```

Example:

```json
{
    "devices": [
        "device_01",
        "device_02",
        "device_03"
    ]
}
```

The `devices` value is an array.

In Python, it becomes a list.

---

# 6. JSON to Python Mapping

When JSON is loaded into Python, the types map approximately like this:

| JSON    | Python          |
| ------- | --------------- |
| Object  | `dict`          |
| Array   | `list`          |
| String  | `str`           |
| Number  | `int` / `float` |
| `true`  | `True`          |
| `false` | `False`         |
| `null`  | `None`          |

Example:

```json
{
    "device": "device_01",
    "capacity": 1024,
    "online": true
}
```

becomes conceptually:

```python
{
    "device": "device_01",
    "capacity": 1024,
    "online": True
}
```

---

# 7. Importing the JSON Module

Use:

```python
import json
```

Example:

```python
import json

print(json)
```

The `json` module is part of Python's standard library.

You normally do **not** need to install an external package.

---

# 8. Reading JSON from a File

The primary function is:

```python
json.load()
```

Example file:

```text
device.json
```

Contents:

```json
{
    "device": "device_01",
    "status": "ONLINE",
    "capacity_gb": 1024
}
```

Python:

```python
import json

with open(
    "device.json",
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)

print(data)
```

The result is a Python dictionary.

---

# 9. Using `Path.open()`

Since this module uses `pathlib`, the same operation can be written as:

```python
from pathlib import Path
import json

path = Path("device.json")

with path.open(
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)

print(data)
```

This integrates naturally with the file-handling patterns already learned.

---

# 10. Accessing JSON Values

Suppose:

```python
data = {
    "device": "device_01",
    "status": "ONLINE",
    "capacity_gb": 1024
}
```

Access values using keys:

```python
print(data["device"])
```

Output:

```text
device_01
```

And:

```python
print(data["status"])
```

Output:

```text
ONLINE
```

---

# 11. Accessing Numeric Values

```python
capacity = data["capacity_gb"]

print(capacity)
```

Output:

```text
1024
```

The resulting Python object is an integer.

You can perform normal Python operations:

```python
if data["capacity_gb"] >= 1000:
    print("Capacity requirement satisfied")
```

---

# 12. Nested JSON Objects

JSON can contain objects inside objects.

Example:

```json
{
    "device": {
        "name": "device_01",
        "status": "ONLINE",
        "capacity_gb": 1024
    }
}
```

After loading:

```python
data["device"]
```

returns a dictionary.

To access `name`:

```python
print(data["device"]["name"])
```

Output:

```text
device_01
```

---

# 13. Nested Arrays

JSON can contain arrays of objects.

Example:

```json
{
    "devices": [
        {
            "name": "device_01",
            "status": "ONLINE"
        },
        {
            "name": "device_02",
            "status": "OFFLINE"
        }
    ]
}
```

Access the first device:

```python
print(data["devices"][0])
```

Access its name:

```python
print(data["devices"][0]["name"])
```

Output:

```text
device_01
```

---

# 14. Iterating Through JSON Arrays

Example:

```python
for device in data["devices"]:
    print(device["name"])
```

Output:

```text
device_01
device_02
```

This is a common automation pattern.

---

# 15. Filtering JSON Data

Suppose:

```python
for device in data["devices"]:

    if device["status"] == "ONLINE":
        print(device["name"])
```

Output:

```text
device_01
```

This can be used to validate storage-device state.

---

# 16. JSON Arrays of Test Results

Example:

```json
{
    "tests": [
        {
            "id": "TEST_001",
            "status": "PASS"
        },
        {
            "id": "TEST_002",
            "status": "FAIL"
        },
        {
            "id": "TEST_003",
            "status": "PASS"
        }
    ]
}
```

Python:

```python
import json

with open(
    "results.json",
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)

for test in data["tests"]:

    if test["status"] == "FAIL":
        print(test["id"])
```

Output:

```text
TEST_002
```

---

# 17. `json.loads()`

There are two important JSON-reading functions:

```python
json.load()
```

and:

```python
json.loads()
```

The difference is what they consume.

### `json.load()`

Reads JSON from a file-like object.

```python
data = json.load(file)
```

### `json.loads()`

Reads JSON from a Python string.

```python
data = json.loads(text)
```

Remember:

```text
load  → file
loads → string
```

---

# 18. Example of `json.loads()`

```python
import json

text = '''
{
    "device": "device_01",
    "status": "ONLINE"
}
'''

data = json.loads(text)

print(data["device"])
```

Output:

```text
device_01
```

---

# 19. `json.dump()`

When we want to write Python data to a JSON file, use:

```python
json.dump()
```

Example:

```python
import json

data = {
    "device": "device_01",
    "status": "ONLINE",
    "capacity_gb": 1024
}

with open(
    "device.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(data, file)
```

The JSON file is created or overwritten.

---

# 20. `json.dumps()`

The second writing function is:

```python
json.dumps()
```

It converts a Python object into a JSON string.

Example:

```python
import json

data = {
    "device": "device_01",
    "status": "ONLINE"
}

text = json.dumps(data)

print(text)
```

Output will be similar to:

```text
{"device": "device_01", "status": "ONLINE"}
```

Remember:

```text
dump  → file
dumps → string
```

---

# 21. The Four Core JSON Functions

This is one of the most important interview points.

| Function       | Purpose                     |
| -------------- | --------------------------- |
| `json.load()`  | JSON file → Python object   |
| `json.loads()` | JSON string → Python object |
| `json.dump()`  | Python object → JSON file   |
| `json.dumps()` | Python object → JSON string |

Think:

```text
FILE  → load  → Python
STRING → loads → Python

Python → dump  → FILE
Python → dumps → STRING
```

---

# 22. Pretty-Printing JSON

By default:

```python
json.dump(data, file)
```

may produce compact JSON.

For human-readable output, use:

```python
indent=4
```

Example:

```python
import json

with open(
    "device.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        data,
        file,
        indent=4
    )
```

Output:

```json
{
    "device": "device_01",
    "status": "ONLINE",
    "capacity_gb": 1024
}
```

This is much easier to inspect manually.

---

# 23. Pretty-Printing with `dumps()`

```python
text = json.dumps(
    data,
    indent=4
)

print(text)
```

This produces formatted JSON as a Python string.

---

# 24. `ensure_ascii`

When writing JSON containing non-ASCII characters, you may encounter escaped representations.

Python supports:

```python
ensure_ascii=False
```

Example:

```python
json.dump(
    data,
    file,
    indent=4,
    ensure_ascii=False
)
```

This is useful when preserving Unicode characters in a human-readable form.

---

# 25. JSON Configuration Files

JSON is commonly used for automation configuration.

Example:

```json
{
    "device": "/dev/nvme0n1",
    "block_size": 4096,
    "queue_depth": 32,
    "test_duration": 3600
}
```

Python:

```python
import json

with open(
    "config.json",
    "r",
    encoding="utf-8"
) as file:

    config = json.load(file)

device = config["device"]
block_size = config["block_size"]
queue_depth = config["queue_depth"]
duration = config["test_duration"]
```

Now the test parameters come from configuration rather than being hard-coded throughout the program.

---

# 26. Configuration Validation

Loading JSON does not guarantee that the data is valid for your application.

For example:

```json
{
    "device": "/dev/nvme0n1",
    "queue_depth": -5
}
```

This may be valid JSON.

But:

```text
queue_depth = -5
```

may be invalid for the test.

Therefore:

```python
if config["queue_depth"] <= 0:
    raise ValueError(
        "queue_depth must be greater than zero"
    )
```

This separates:

```text
JSON validity
```

from:

```text
Application validity
```

---

# 27. Missing Keys

Consider:

```python
device = config["device"]
```

If `"device"` does not exist, Python raises:

```text
KeyError
```

Example:

```python
config = {
    "queue_depth": 32
}

print(config["device"])
```

Result:

```text
KeyError: 'device'
```

This is useful when a configuration field is mandatory.

---

# 28. Using `.get()`

If a field is optional:

```python
timeout = config.get("timeout")
```

If the key is missing, `.get()` returns:

```text
None
```

You can also specify a default:

```python
timeout = config.get(
    "timeout",
    30
)
```

If `timeout` is absent:

```text
30
```

is returned.

---

# 29. `[]` vs `.get()`

Use:

```python
config["device"]
```

when the key is required.

Use:

```python
config.get("timeout")
```

when the key is optional.

This distinction is useful in automation.

For example:

```python
device = config["device"]
```

The test cannot run without a target device.

But:

```python
timeout = config.get("timeout", 30)
```

can provide a default if timeout is optional.

---

# 30. Handling Invalid JSON

Consider malformed JSON:

```json
{
    "device": "device_01",
    "status": "ONLINE",
}
```

The trailing comma makes this invalid JSON.

Trying:

```python
data = json.load(file)
```

can raise:

```text
json.JSONDecodeError
```

Handle it when appropriate:

```python
import json

try:

    with open(
        "config.json",
        "r",
        encoding="utf-8"
    ) as file:

        config = json.load(file)

except json.JSONDecodeError as error:

    print(f"Invalid JSON: {error}")
```

---

# 31. Handling Missing JSON Files

```python
from pathlib import Path
import json

path = Path("config.json")

try:

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        config = json.load(file)

except FileNotFoundError:
    print(f"Configuration file not found: {path}")

except json.JSONDecodeError as error:
    print(f"Invalid JSON: {error}")
```

This combines:

```text
File handling
+
Exception handling
+
JSON parsing
```

---

# 32. JSON and Exception Handling

A robust JSON-loading function can be:

```python
import json
from pathlib import Path

def load_json(path):

    path = Path(path)

    try:

        with path.open(
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"JSON file not found: {path}"
        )

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Invalid JSON in {path}: {error}"
        )
```

This creates clearer application-level errors.

---

# 33. Writing JSON Test Results

Suppose a test produces:

```python
results = {
    "test": "READ_WRITE_TEST",
    "status": "PASS",
    "duration_seconds": 125
}
```

Write it:

```python
import json

with open(
    "results.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        results,
        file,
        indent=4
    )
```

Result:

```json
{
    "test": "READ_WRITE_TEST",
    "status": "PASS",
    "duration_seconds": 125
}
```

---

# 34. Nested Storage Test Results

A more realistic result:

```python
results = {
    "device": {
        "name": "device_01",
        "status": "ONLINE"
    },
    "test": {
        "name": "READ_WRITE_TEST",
        "status": "PASS",
        "duration_seconds": 125
    }
}
```

Write:

```python
with open(
    "results.json",
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        results,
        file,
        indent=4
    )
```

This produces a structured test artifact.

---

# 35. JSON and APIs

JSON is commonly used when communicating with APIs.

For example, an API may return:

```json
{
    "device": "device_01",
    "status": "ONLINE",
    "temperature": 42
}
```

The API response can be parsed into Python data.

Conceptually:

```text
API
 ↓
JSON
 ↓
Python dictionary
 ↓
Automation logic
```

The `json` module handles JSON serialization/deserialization itself, while an HTTP library handles the network communication.

---

# 36. JSON and Storage Metadata

Storage automation can represent device information using JSON:

```json
{
    "device": "nvme0",
    "model": "ExampleDrive",
    "serial": "ABC123",
    "capacity_gb": 2048,
    "firmware": "1.2.3",
    "status": "ONLINE"
}
```

Python can access:

```python
data["model"]
data["capacity_gb"]
data["firmware"]
```

This makes structured validation straightforward.

---

# 37. JSON Validation Example

Suppose the expected state is:

```text
status = ONLINE
capacity >= 1000
```

Code:

```python
if data["status"] != "ONLINE":
    raise RuntimeError("Device is not online")

if data["capacity_gb"] < 1000:
    raise RuntimeError(
        "Device capacity is below requirement"
    )
```

This is a simple example of turning structured JSON data into automated validation.

---

# 38. JSON Comparison

As covered in the file-comparison topic, JSON should sometimes be compared as **data rather than raw text**.

Example:

```python
import json

with open(
    "expected.json",
    "r",
    encoding="utf-8"
) as file:

    expected = json.load(file)

with open(
    "actual.json",
    "r",
    encoding="utf-8"
) as file:

    actual = json.load(file)

if expected == actual:
    print("PASS")
else:
    print("FAIL")
```

This ignores differences caused purely by JSON formatting.

---

# 39. JSON and File Handling

The complete flow is:

```text
JSON file
   ↓
open()
   ↓
json.load()
   ↓
Python dict/list
   ↓
Process / Validate
   ↓
json.dump()
   ↓
JSON result file
```

This is one of the most important automation patterns from this topic.

---

# 40. JSON vs Plain Text

Suppose we need to store:

```text
device=nvme0
status=ONLINE
capacity=2048
```

Plain text can work.

But JSON:

```json
{
    "device": "nvme0",
    "status": "ONLINE",
    "capacity": 2048
}
```

provides explicit structure.

Python can directly access:

```python
data["capacity"]
```

instead of manually parsing:

```python
line.split("=")
```

For structured data, JSON is generally much easier to consume programmatically.

---

# 41. JSON vs CSV

JSON:

```json
{
    "device": "nvme0",
    "status": "ONLINE",
    "capacity": 2048
}
```

is well suited to:

* Nested data
* Configuration
* API responses
* Structured records

CSV is better suited to:

```text
device,status,capacity
nvme0,ONLINE,2048
nvme1,OFFLINE,1024
```

where the data is primarily tabular.

---

# 42. Common Mistakes

### Mistake 1 — Confusing `load()` and `loads()`

Incorrect:

```python
json.loads(file)
```

when you intend to parse a file object.

Use:

```python
json.load(file)
```

For a JSON string:

```python
json.loads(text)
```

Remember:

```text
load  → file
loads → string
```

---

### Mistake 2 — Confusing `dump()` and `dumps()`

For a file:

```python
json.dump(data, file)
```

For a string:

```python
text = json.dumps(data)
```

---

### Mistake 3 — Assuming JSON numbers are strings

Given:

```json
{
    "capacity": 1024
}
```

the resulting Python value is numeric:

```python
data["capacity"]
```

not:

```text
"1024"
```

unless the JSON explicitly contains a string:

```json
{
    "capacity": "1024"
}
```

---

### Mistake 4 — Assuming JSON validity means application validity

This:

```json
{
    "queue_depth": -10
}
```

can be valid JSON.

It may still be invalid for your storage test.

Always validate application requirements separately.

---

### Mistake 5 — Ignoring malformed JSON

Always consider:

```text
json.JSONDecodeError
```

when reading externally generated JSON.

---

### Mistake 6 — Assuming a key always exists

This:

```python
data["status"]
```

can raise:

```text
KeyError
```

if the key is absent.

Choose between:

```python
data["status"]
```

and:

```python
data.get("status")
```

based on whether the field is mandatory.

---

# 43. Interview Questions

### Q1. What is JSON?

JSON is a lightweight text-based data-interchange format commonly used to represent structured data.

---

### Q2. Which Python module is used for JSON?

```python
import json
```

It is part of the Python standard library.

---

### Q3. What is the difference between `json.load()` and `json.loads()`?

```text
json.load()
```

parses JSON from a file-like object.

```text
json.loads()
```

parses JSON from a string.

---

### Q4. What is the difference between `json.dump()` and `json.dumps()`?

```text
json.dump()
```

writes JSON to a file-like object.

```text
json.dumps()
```

returns JSON as a string.

---

### Q5. What Python type represents a JSON object?

Usually:

```python
dict
```

---

### Q6. What Python type represents a JSON array?

Usually:

```python
list
```

---

### Q7. What exception is commonly raised for malformed JSON?

```python
json.JSONDecodeError
```

---

### Q8. How do you make JSON human-readable?

Use:

```python
json.dump(
    data,
    file,
    indent=4
)
```

---

### Q9. How do you access a JSON value?

For example:

```python
data["device"]
```

---

### Q10. Why might `.get()` be preferable to `[]`?

`.get()` can provide a default or return `None` when an optional key is missing, while `[]` raises `KeyError`.

---

# 44. Key Takeaways

The four functions to remember:

```python
json.load()
json.loads()
json.dump()
json.dumps()
```

### JSON file → Python

```python
with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
```

### JSON string → Python

```python
data = json.loads(text)
```

### Python → JSON file

```python
with open("data.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)
```

### Python → JSON string

```python
text = json.dumps(data, indent=4)
```

---

# 45. Automation Principle

> **Use JSON when automation needs structured, machine-readable data that can be exchanged, stored, validated, or consumed by other tools.**

A common storage-automation flow is:

```text
Device / API / Test
        ↓
      JSON
        ↓
   json.load()
        ↓
Python dictionary/list
        ↓
Validate
        ↓
Process
        ↓
Generate result
        ↓
   json.dump()
        ↓
Result JSON
```

JSON becomes particularly powerful when combined with the concepts already learned:

```text
Pathlib
   +
File handling
   +
Exception handling
   +
JSON
   =
Structured automation
```

**Next file:** `15_CSV.md`

