# 17 — Choosing File Formats

````markdown
# Choosing File Formats

## 1. Introduction

Different automation tasks require different ways of storing data.

Common formats used in Python automation include:

- TXT
- CSV
- JSON
- YAML

Choosing the correct format is important because the format affects:

- Readability
- Structure
- Data validation
- Interoperability
- Ease of processing
- Maintainability

For Storage Test Automation, the goal is not to use one format everywhere.

Instead:

> Choose the format based on the type of data being stored.

---

# 2. TXT — Plain Text

TXT is appropriate for simple, human-readable text.

Example:

```text
TEST_001 PASS
TEST_002 FAIL
TEST_003 PASS
````

Python:

```python
with open("results.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

## Good use cases

TXT is useful for:

* Logs
* Simple reports
* Command output
* Debug information
* Human-readable summaries

Example:

```text
Storage Test Execution Report

Total Tests : 100
Passed      : 96
Failed      : 4
```

## Advantages

* Very simple
* Human-readable
* Easy to generate
* Easy to inspect manually

## Limitations

TXT has little inherent structure.

For example:

```text
NVMe /dev/nvme0n1 4096 60
```

A program must already know what each field means.

---

# 3. CSV — Tabular Data

CSV stands for:

> Comma-Separated Values

CSV is useful when data naturally fits into rows and columns.

Example:

```csv
test_id,status,duration
TEST_001,PASS,12
TEST_002,FAIL,18
TEST_003,PASS,10
```

Python:

```python
import csv

with open("results.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row["test_id"], row["status"])
```

## Good use cases

CSV is useful for:

* Test results
* Device inventories
* Performance measurements
* Benchmark results
* Test execution summaries
* Spreadsheet-compatible data

Example:

```csv
device,protocol,capacity_gb,status
nvme0n1,NVMe,1024,PASS
sda,SATA,512,PASS
sdb,SAS,2048,FAIL
```

## Advantages

* Simple tabular structure
* Easy to process
* Compatible with spreadsheets
* Good for large row-based datasets
* Easy to generate reports

## Limitations

CSV is not naturally designed for deeply nested structures.

For example, this is awkward in CSV:

```text
storage
  controller
    protocol
    driver
  device
    path
    capacity
```

A hierarchical format such as JSON or YAML is usually better.

---

# 4. JSON — Structured Data

JSON stands for:

> JavaScript Object Notation

JSON is commonly used for structured data exchange.

Example:

```json
{
    "storage": {
        "protocol": "NVMe",
        "device": "/dev/nvme0n1"
    },
    "execution": {
        "timeout": 60,
        "retries": 2
    }
}
```

Python:

```python
import json

with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

print(config["storage"]["protocol"])
```

## Good use cases

JSON is useful for:

* API responses
* API requests
* Structured test results
* Machine-readable metadata
* Nested data
* Inter-process data exchange

Example:

```json
{
    "test": {
        "name": "sequential_read",
        "status": "PASS",
        "duration": 42
    }
}
```

## Advantages

* Structured
* Widely supported
* Excellent for APIs
* Naturally represents dictionaries and lists
* Easy for Python to process

## Limitations

JSON can become verbose for large configuration files.

For example:

```json
{
    "storage": {
        "protocol": "NVMe",
        "device": "/dev/nvme0n1"
    }
}
```

requires more punctuation than the equivalent YAML:

```yaml
storage:
  protocol: NVMe
  device: /dev/nvme0n1
```

---

# 5. YAML — Configuration

YAML is particularly useful for human-maintained configuration.

Example:

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

Python:

```python
import yaml

with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
```

## Good use cases

YAML is useful for:

* Automation configuration
* Test configuration
* Environment settings
* Test suites
* CI/CD configuration
* Human-maintained configuration

## Advantages

* Highly readable
* Natural hierarchy
* Less punctuation
* Supports comments
* Good for configuration

## Limitations

* Indentation is significant
* Formatting mistakes can cause parsing errors
* Type interpretation can sometimes surprise users
* Requires an external Python package such as PyYAML

---

# 6. TXT vs CSV vs JSON vs YAML

A useful high-level comparison:

| Format | Best For            | Structure | Human Readability |
| ------ | ------------------- | --------- | ----------------- |
| TXT    | Logs/simple text    | Low       | High              |
| CSV    | Tables/results      | Tabular   | High              |
| JSON   | Structured/API data | High      | Medium            |
| YAML   | Configuration       | High      | Very High         |

---

# 7. Choosing Based on Data Shape

One of the easiest ways to choose a format is to ask:

> What does my data look like?

### Simple text

Use:

```text
TXT
```

Example:

```text
Test execution started
Test execution completed
```

---

### Rows and columns

Use:

```text
CSV
```

Example:

```text
Test ID | Status | Duration
```

---

### Nested machine-readable data

Use:

```text
JSON
```

Example:

```text
test
 ├── name
 ├── status
 └── metrics
      ├── read_iops
      └── latency
```

---

### Human-maintained configuration

Use:

```text
YAML
```

Example:

```text
execution
 ├── timeout
 ├── retries
 └── parallel
```

---

# 8. Storage Test Automation Example

Suppose a storage validation framework needs four different kinds of information.

## 8.1 Execution Log

Use TXT.

```text
Starting NVMe validation
Device detected: /dev/nvme0n1
Running read test
Read test PASS
Running write test
Write test PASS
```

---

## 8.2 Test Results

Use CSV.

```csv
test_id,status,duration
READ_001,PASS,20
WRITE_001,PASS,35
VERIFY_001,FAIL,12
```

This is convenient for:

* Filtering
* Sorting
* Spreadsheet analysis
* Result reporting

---

## 8.3 Structured Metadata

Use JSON.

```json
{
    "device": {
        "name": "nvme0n1",
        "protocol": "NVMe",
        "capacity_gb": 1024
    }
}
```

---

## 8.4 Test Configuration

Use YAML.

```yaml
execution:
  timeout: 60
  retries: 2

tests:
  - read
  - write
  - verify
```

This produces a clean separation:

```text
                  Storage Automation
                         |
       +-----------------+-----------------+
       |                 |                 |
      YAML              JSON              CSV/TXT
       |                 |                 |
 Configuration       Metadata        Results/Logs
```

---

# 9. Configuration vs Results

This distinction is important.

### Configuration

Configuration describes:

> What should the automation do?

Example:

```yaml
tests:
  - read
  - write
  - verify
```

### Results

Results describe:

> What actually happened?

Example:

```csv
test_id,status,duration
READ_001,PASS,20
WRITE_001,FAIL,35
```

These should generally be treated as different data.

---

# 10. Human vs Machine Consumers

Another useful decision factor is:

> Who or what will consume the data?

### Human-focused

Prefer:

```text
TXT
YAML
```

### Machine/API-focused

Prefer:

```text
JSON
CSV
```

This is not an absolute rule.

For example, engineers routinely inspect JSON manually, and spreadsheets routinely consume CSV.

The point is to consider the primary consumer.

---

# 11. Interoperability

Sometimes the choice is determined by another system.

For example:

```text
Python
   ↓
REST API
   ↓
JSON
```

If an API expects JSON, your automation should produce JSON.

Similarly:

```text
Python
   ↓
Spreadsheet/reporting
   ↓
CSV
```

CSV may be the appropriate output.

Therefore:

> External interface requirements can determine the correct file format.

---

# 12. File Format Conversion

Python can convert between formats.

Example:

```text
CSV
 ↓
Python data structures
 ↓
JSON
```

Or:

```text
YAML
 ↓
Python dictionary
 ↓
JSON
```

The Python object acts as the intermediate representation.

Example:

```python
data = {
    "test_id": "TEST_001",
    "status": "PASS"
}
```

Then the same data can be written as:

### JSON

```json
{
    "test_id": "TEST_001",
    "status": "PASS"
}
```

### YAML

```yaml
test_id: TEST_001
status: PASS
```

### CSV

```csv
test_id,status
TEST_001,PASS
```

The underlying information is similar, but the representation and intended use differ.

---

# 13. Large Data Considerations

Format selection can also depend on data size.

For large line-oriented data:

```text
TXT
CSV
```

can be convenient because Python can process records incrementally.

Example:

```python
with open("results.csv", "r", newline="", encoding="utf-8") as file:
    for row in file:
        process(row)
```

Large JSON documents can require more care because a single JSON document may represent a large nested structure.

For very large datasets, consider:

* Streaming
* Line-by-line processing
* Chunking
* Structured streaming formats
* Database storage

Do not automatically load a huge file into memory just because the format supports it.

---

# 14. Maintainability

A good file format makes automation easier to maintain.

Consider configuration written as plain text:

```text
NVMe /dev/nvme0n1 60 2 read write verify
```

An engineer must remember what each field means.

YAML is clearer:

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

The structure explains itself.

This is one reason YAML is useful for automation configuration.

---

# 15. A Practical Decision Process

When choosing a file format, ask these questions.

### Question 1

Is it simply text?

```text
→ TXT
```

### Question 2

Is it naturally rows and columns?

```text
→ CSV
```

### Question 3

Is it nested structured data or API data?

```text
→ JSON
```

### Question 4

Is it human-maintained configuration?

```text
→ YAML
```

### Question 5

Does an external system require a specific format?

```text
→ Follow the interface requirement
```

### Question 6

Is the data extremely large?

```text
→ Consider processing strategy in addition to format
```

---

# 16. Common Mistakes

## Mistake 1 — Using TXT for structured data

Example:

```text
NVMe /dev/nvme0n1 1024 PASS
```

This works, but the structure is implicit.

If the data is genuinely tabular, CSV may be better.

---

## Mistake 2 — Using CSV for deeply nested configuration

CSV is designed around rows and columns.

For hierarchical configuration, YAML or JSON is usually more natural.

---

## Mistake 3 — Using YAML simply because it is readable

YAML is excellent for configuration, but JSON may be more appropriate when interacting with an API.

Always consider the consumer.

---

## Mistake 4 — Choosing based only on personal preference

The correct format depends on:

```text
Data structure
+
Consumer
+
External requirements
+
Scale
+
Maintainability
```

---

# 17. Storage Automation Architecture

A practical framework might use:

```text
                Storage Test Framework
                         |
              +----------+----------+
              |                     |
         Configuration          Execution
              |                     |
            YAML                  Python
              |                     |
              +----------+----------+
                         |
                  Test Execution
                         |
             +-----------+-----------+
             |                       |
           Logs                   Results
             |                       |
            TXT                     CSV
                                     |
                              Detailed Metadata
                                     |
                                    JSON
```

This is a realistic separation of responsibilities.

---

# 18. Recommended Default Choices

For the Storage Test Automation work:

| Requirement               | Recommended Format |
| ------------------------- | ------------------ |
| Simple logs               | TXT                |
| Human-readable reports    | TXT                |
| Test result tables        | CSV                |
| Device/test metadata      | JSON               |
| API data                  | JSON               |
| Automation configuration  | YAML               |
| Test suite configuration  | YAML               |
| Environment configuration | YAML               |

These are defaults, not rigid rules.

---

# 19. Interview Questions

### Basic

**1. When would you use TXT?**

For simple text such as logs, command output, or human-readable reports.

**2. When would you use CSV?**

When data naturally consists of rows and columns.

**3. When would you use JSON?**

For structured data, APIs, metadata, and nested machine-readable information.

**4. When would you use YAML?**

For human-readable configuration and hierarchical settings.

---

### Intermediate

**5. Why is YAML commonly used for configuration?**

Because it represents hierarchical configuration clearly and is easy for humans to maintain.

**6. Why is CSV useful for test results?**

Test results often naturally fit into rows and columns and can easily be analyzed with spreadsheet tools.

**7. Why is JSON common with APIs?**

Because it provides a standardized structured representation that is widely supported by applications and programming languages.

**8. Can Python convert between these formats?**

Yes. Python can load data into dictionaries/lists and then serialize those structures into different formats.

---

### Storage Automation

**9. What format would you choose for test configuration?**

Usually YAML.

**10. What format would you choose for test execution results?**

Usually CSV when the results are tabular.

**11. What format would you choose for API responses?**

Usually JSON.

**12. What format would you choose for logs?**

Usually TXT or a logging system/file format appropriate to the framework.

**13. What factors should influence file-format selection?**

```text
Data structure
Consumer
Interoperability
Scale
Readability
Maintainability
External requirements
```

---

# 20. Key Takeaways

Remember:

```text
TXT
→ Simple text / logs

CSV
→ Rows and columns

JSON
→ Structured data / APIs / metadata

YAML
→ Human-readable configuration
```

The most important principle is:

> **Do not choose a file format because it is popular. Choose it because it matches the data and its consumer.**

For Storage Test Automation, a practical combination is:

```text
YAML → Configuration
JSON → Structured metadata / APIs
CSV  → Test results
TXT  → Logs / simple reports
```

---

# Automation Principle

> **Use the simplest format that represents the data clearly and satisfies the consumer's requirements.**



