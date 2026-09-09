# 16 — YAML

````markdown
# YAML

## 1. Introduction

YAML is a human-readable data serialization format commonly used for:

- Configuration files
- Test automation configuration
- CI/CD pipelines
- Application settings
- Infrastructure definitions
- Structured test data

YAML is especially useful in automation because configuration can be represented in a readable hierarchical structure.

Example:

```yaml
environment: lab
timeout: 30
retries: 3

storage:
  protocol: NVMe
  device: /dev/nvme0n1

tests:
  - test_read
  - test_write
  - test_verify
````

Python can work with YAML using the `PyYAML` library.

Install:

```bash
pip install pyyaml
```

Import:

```python
import yaml
```

---

# 2. YAML Basic Structure

YAML uses indentation to represent hierarchy.

Example:

```yaml
storage:
  protocol: NVMe
  capacity: 1024
  device: /dev/nvme0n1
```

The structure is equivalent to a Python dictionary:

```python
{
    "storage": {
        "protocol": "NVMe",
        "capacity": 1024,
        "device": "/dev/nvme0n1"
    }
}
```

## Important

YAML indentation is meaningful.

Correct:

```yaml
storage:
  protocol: NVMe
  device: /dev/nvme0n1
```

Incorrect:

```yaml
storage:
protocol: NVMe
device: /dev/nvme0n1
```

Use consistent spaces.

---

# 3. YAML Data Types

YAML supports common data types.

## String

```yaml
protocol: NVMe
device: /dev/nvme0n1
```

## Integer

```yaml
timeout: 30
retries: 3
```

## Float

```yaml
temperature: 35.5
```

## Boolean

```yaml
enabled: true
debug: false
```

## Null

```yaml
device: null
```

## List

```yaml
protocols:
  - SATA
  - SAS
  - NVMe
```

## Mapping

```yaml
storage:
  protocol: NVMe
  device: /dev/nvme0n1
```

---

# 4. YAML Lists

Lists are represented using `-`.

Example:

```yaml
tests:
  - test_read
  - test_write
  - test_verify
```

Python representation:

```python
[
    "test_read",
    "test_write",
    "test_verify"
]
```

Lists can contain mappings:

```yaml
tests:
  - name: read_test
    timeout: 30

  - name: write_test
    timeout: 60
```

Python representation:

```python
[
    {
        "name": "read_test",
        "timeout": 30
    },
    {
        "name": "write_test",
        "timeout": 60
    }
]
```

This is extremely useful for automation configuration.

---

# 5. Nested YAML

YAML supports deeply nested structures.

Example:

```yaml
storage:
  controller:
    protocol: NVMe
    driver: nvme

  device:
    path: /dev/nvme0n1
    capacity_gb: 1024

  tests:
    read:
      enabled: true
      timeout: 30

    write:
      enabled: true
      timeout: 60
```

This becomes nested Python dictionaries.

Access:

```python
config["storage"]["controller"]["protocol"]
```

Output:

```text
NVMe
```

---

# 6. Reading YAML

Suppose `config.yaml` contains:

```yaml
environment: lab
timeout: 30
retries: 3
```

Python:

```python
import yaml

with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

print(config)
```

Output:

```text
{'environment': 'lab', 'timeout': 30, 'retries': 3}
```

The YAML document has been converted into Python objects.

---

# 7. yaml.safe_load()

Use:

```python
yaml.safe_load()
```

for reading YAML from untrusted or normal configuration files.

Example:

```python
with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
```

### Why `safe_load()`?

YAML can represent more than simple data structures.

For automation configuration, we generally want:

```text
YAML
 ↓
Python dictionaries/lists/values
```

without allowing arbitrary Python object construction.

Therefore:

```python
yaml.safe_load()
```

is the preferred approach for configuration data.

---

# 8. YAML File to Python Objects

Example YAML:

```yaml
storage:
  protocol: NVMe
  device: /dev/nvme0n1
  retries: 3

tests:
  - read
  - write
  - verify
```

Python:

```python
import yaml

with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

protocol = config["storage"]["protocol"]
device = config["storage"]["device"]
retries = config["storage"]["retries"]

tests = config["tests"]

print(protocol)
print(device)
print(retries)
print(tests)
```

Output:

```text
NVMe
/dev/nvme0n1
3
['read', 'write', 'verify']
```

---

# 9. Writing YAML

Python can convert Python objects into YAML.

Example:

```python
import yaml

config = {
    "environment": "lab",
    "timeout": 30,
    "retries": 3
}

with open("config.yaml", "w", encoding="utf-8") as file:
    yaml.safe_dump(config, file)
```

Generated YAML:

```yaml
environment: lab
retries: 3
timeout: 30
```

---

# 10. yaml.safe_dump()

Use:

```python
yaml.safe_dump()
```

to write normal Python data structures into YAML.

Example:

```python
data = {
    "storage": {
        "protocol": "SAS",
        "device": "/dev/sdb"
    }
}

with open("storage.yaml", "w", encoding="utf-8") as file:
    yaml.safe_dump(data, file)
```

---

# 11. Pretty YAML with indent

For readable configuration files:

```python
yaml.safe_dump(
    config,
    file,
    indent=2
)
```

Example:

```python
config = {
    "storage": {
        "protocol": "NVMe",
        "device": "/dev/nvme0n1"
    }
}
```

Output:

```yaml
storage:
  device: /dev/nvme0n1
  protocol: NVMe
```

---

# 12. yaml.dump() vs yaml.safe_dump()

You may encounter:

```python
yaml.dump()
```

and:

```python
yaml.safe_dump()
```

For normal automation configuration:

```python
yaml.safe_dump()
```

is preferred.

Similarly, for reading:

```python
yaml.safe_load()
```

is preferred.

The important automation habit is:

> Use safe YAML APIs when handling configuration/data.

---

# 13. Reading Multiple YAML Documents

YAML can contain multiple documents separated by:

```yaml
---
```

Example:

```yaml
name: test_read
status: PASS
---
name: test_write
status: FAIL
```

Python:

```python
with open("results.yaml", "r", encoding="utf-8") as file:
    documents = list(yaml.safe_load_all(file))
```

Result:

```python
[
    {
        "name": "test_read",
        "status": "PASS"
    },
    {
        "name": "test_write",
        "status": "FAIL"
    }
]
```

For normal automation configuration, a single YAML document is usually sufficient.

---

# 14. YAML and Python Data Structures

The most important mapping is:

| YAML           | Python  |
| -------------- | ------- |
| mapping        | `dict`  |
| sequence       | `list`  |
| string         | `str`   |
| integer        | `int`   |
| floating-point | `float` |
| boolean        | `bool`  |
| null           | `None`  |

Example:

```yaml
name: storage_test
enabled: true
retries: 3

protocols:
  - SATA
  - SAS
  - NVMe
```

Python:

```python
{
    "name": "storage_test",
    "enabled": True,
    "retries": 3,
    "protocols": [
        "SATA",
        "SAS",
        "NVMe"
    ]
}
```

Understanding this mapping is critical when writing automation code.

---

# 15. Accessing YAML Safely

Direct access:

```python
timeout = config["timeout"]
```

This raises:

```text
KeyError
```

if the key doesn't exist.

For optional configuration:

```python
timeout = config.get("timeout", 30)
```

This means:

> Use the configured timeout if present; otherwise use 30.

Example:

```python
retries = config.get("retries", 3)
```

This is useful for optional automation settings.

---

# 16. YAML Configuration for Storage Automation

A realistic configuration might look like:

```yaml
environment:
  name: lab

storage:
  protocol: NVMe
  device: /dev/nvme0n1
  block_size: 4096

execution:
  timeout: 60
  retries: 2

tests:
  - read
  - write
  - verify
```

Python:

```python
import yaml

with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

protocol = config["storage"]["protocol"]
device = config["storage"]["device"]

timeout = config["execution"]["timeout"]
retries = config["execution"]["retries"]

tests = config["tests"]

print(protocol)
print(device)
print(timeout)
print(retries)
print(tests)
```

Now the test script does not need to hard-code every configuration value.

---

# 17. Configuration-Driven Automation

A strong automation architecture separates:

```text
Configuration
      ↓
YAML
      ↓
Python Automation
      ↓
Execution
      ↓
Results
```

For example:

```text
config.yaml
    ↓
test_runner.py
    ↓
storage test execution
    ↓
test_results.csv
```

This makes the automation reusable.

Instead of changing Python code:

```python
device = "/dev/nvme0n1"
```

the tester can change:

```yaml
device: /dev/nvme0n1
```

or:

```yaml
device: /dev/sdb
```

without modifying the automation logic.

---

# 18. YAML Validation

Loading YAML successfully does **not** mean the configuration is valid.

Example:

```yaml
execution:
  timeout: hello
```

YAML can parse this successfully.

But the automation may require:

```text
timeout → integer
```

Therefore validation should happen after parsing.

Example:

```python
timeout = config["execution"]["timeout"]

if not isinstance(timeout, int):
    raise ValueError("timeout must be an integer")
```

Configuration processing becomes:

```text
Load
 ↓
Parse
 ↓
Validate
 ↓
Use
```

not simply:

```text
Load
 ↓
Use
```

---

# 19. Handling YAML Errors

A malformed YAML file can raise:

```python
yaml.YAMLError
```

Example:

```python
import yaml

try:
    with open("config.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

except yaml.YAMLError as error:
    print(f"Invalid YAML: {error}")
```

File errors must also be considered:

```python
try:
    with open("config.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

except FileNotFoundError:
    print("Configuration file not found.")

except yaml.YAMLError as error:
    print(f"Invalid YAML: {error}")
```

This combines:

* File handling
* YAML parsing
* Exception handling

which is directly relevant to automation.

---

# 20. Empty YAML Files

An empty YAML file can produce:

```python
None
```

Example:

```python
config = yaml.safe_load(file)

if config is None:
    raise ValueError("Configuration file is empty")
```

This prevents later failures such as:

```python
config["storage"]
```

when `config` is actually `None`.

---

# 21. YAML vs JSON

Both can represent structured data.

JSON:

```json
{
  "storage": {
    "protocol": "NVMe",
    "timeout": 30
  }
}
```

YAML:

```yaml
storage:
  protocol: NVMe
  timeout: 30
```

### YAML advantages

* Human-readable
* Less punctuation
* Excellent for configuration
* Supports comments
* Natural hierarchical structure

### JSON advantages

* Very widely supported
* Common in APIs
* Strict and predictable syntax
* Native Python `json` module

Typical automation usage:

```text
YAML → configuration
JSON → APIs / structured data exchange
```

This is a guideline, not an absolute rule.

---

# 22. YAML Comments

YAML supports comments using `#`.

Example:

```yaml
# Storage configuration

storage:
  protocol: NVMe
  device: /dev/nvme0n1

  # Timeout in seconds
  timeout: 60
```

Comments are useful for documenting configuration.

---

# 23. YAML Common Mistakes

## Mistake 1 — Incorrect indentation

```yaml
storage:
protocol: NVMe
```

Correct:

```yaml
storage:
  protocol: NVMe
```

---

## Mistake 2 — Mixing indentation styles

Avoid inconsistent indentation.

Use a consistent number of spaces.

---

## Mistake 3 — Assuming YAML parsing validates configuration

This:

```python
config = yaml.safe_load(file)
```

only parses the document.

It does not guarantee that:

* required keys exist
* values have correct types
* paths exist
* devices exist
* values are within valid ranges

Validation is a separate step.

---

## Mistake 4 — Using unsafe YAML loading unnecessarily

For ordinary configuration:

```python
yaml.safe_load()
```

is the preferred choice.

---

## Mistake 5 — Forgetting empty YAML

An empty document can result in:

```python
None
```

Always consider this when configuration is mandatory.

---

# 24. YAML in Storage Test Automation

YAML can describe:

### Test configuration

```yaml
test:
  name: sequential_read
  block_size: 4096
  runtime: 60
```

### Device configuration

```yaml
device:
  path: /dev/nvme0n1
  protocol: NVMe
```

### Execution configuration

```yaml
execution:
  timeout: 120
  retries: 3
```

### Test suites

```yaml
tests:
  - read
  - write
  - verify
  - reset
```

### Environment configuration

```yaml
environment:
  name: lab
  os: linux
```

This makes the automation framework configuration-driven rather than hard-coded.

---

# 25. Practical Automation Pattern

A good YAML-based automation flow is:

```text
             config.yaml
                  |
                  ↓
            yaml.safe_load()
                  |
                  ↓
             Python dict
                  |
                  ↓
              Validate
                  |
                  ↓
             Execute Tests
                  |
                  ↓
             Collect Results
                  |
                  ↓
             Generate Report
```

This connects several concepts already learned:

```text
Pathlib
   +
File Handling
   +
Exception Handling
   +
YAML
   +
Data Structures
   +
Automation
```

---

# 26. Complete Example

### config.yaml

```yaml
storage:
  protocol: NVMe
  device: /dev/nvme0n1

execution:
  timeout: 60
  retries: 2

tests:
  - read
  - write
  - verify
```

### Python

```python
from pathlib import Path
import yaml

config_path = Path("config.yaml")

try:
    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not config:
        raise ValueError("Configuration is empty")

    protocol = config["storage"]["protocol"]
    device = config["storage"]["device"]

    timeout = config["execution"].get("timeout", 30)
    retries = config["execution"].get("retries", 1)

    tests = config["tests"]

    if not isinstance(timeout, int):
        raise ValueError("timeout must be an integer")

    if not isinstance(retries, int):
        raise ValueError("retries must be an integer")

    print(f"Protocol : {protocol}")
    print(f"Device   : {device}")
    print(f"Timeout  : {timeout}")
    print(f"Retries  : {retries}")
    print(f"Tests    : {tests}")

except FileNotFoundError:
    print("Configuration file not found.")

except yaml.YAMLError as error:
    print(f"Invalid YAML: {error}")

except KeyError as error:
    print(f"Missing configuration key: {error}")

except ValueError as error:
    print(f"Invalid configuration: {error}")
```

This is a realistic pattern for configuration-driven automation.

---

# 27. Interview Questions

### Basic

**1. What is YAML?**

A human-readable data serialization format commonly used for configuration and structured data.

**2. What Python library is commonly used for YAML?**

`PyYAML`.

**3. How do you read a YAML file?**

```python
yaml.safe_load(file)
```

**4. How do you write YAML?**

```python
yaml.safe_dump(data, file)
```

**5. What does YAML indentation represent?**

Hierarchy.

---

### Intermediate

**6. What is the difference between `safe_load()` and `safe_dump()`?**

`safe_load()` converts YAML into safe Python data structures.

`safe_dump()` serializes Python data structures into YAML.

**7. Why is `safe_load()` preferred for configuration?**

Because configuration normally requires data structures rather than arbitrary Python object construction.

**8. What happens when an empty YAML document is loaded?**

It can produce `None`.

**9. Does successful YAML parsing guarantee valid configuration?**

No.

The configuration must still be validated.

**10. How would you handle malformed YAML?**

Catch:

```python
yaml.YAMLError
```

---

### Storage Automation

**11. Why is YAML useful in test automation?**

It allows test parameters, devices, timeouts, retries, environments, and test selections to be stored separately from Python logic.

**12. Why is configuration-driven automation better than hard-coded configuration?**

The same automation can run against different devices, environments, and test configurations without modifying the core Python code.

**13. What is the recommended flow when processing YAML configuration?**

```text
Load
 ↓
Parse
 ↓
Validate
 ↓
Use
```

**14. Give an example of storage information that could be represented in YAML.**

```yaml
storage:
  protocol: NVMe
  device: /dev/nvme0n1
```

---

# 28. Key Takeaways

Remember these points:

```text
YAML
 ↓
Human-readable configuration format

PyYAML
 ↓
Python YAML library

safe_load()
 ↓
YAML → Python

safe_dump()
 ↓
Python → YAML

Indentation
 ↓
Represents hierarchy

Mapping
 ↓
dict

Sequence
 ↓
list

Configuration
 ↓
Load → Parse → Validate → Use
```

For Storage Test Automation, YAML is particularly valuable for keeping **test configuration separate from automation logic**.

---

# Automation Principle

> **Configuration should describe what to run; Python should determine how to run it.**

For example:

```yaml
tests:
  - read
  - write
  - verify
```

The YAML selects the tests.

The Python automation contains the implementation.

This separation is an important step toward building maintainable automation frameworks.

```

**Next:** `17_Choosing_File_Formats.md`
```

