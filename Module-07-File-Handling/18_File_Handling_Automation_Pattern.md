# 18 — File Handling Automation Pattern

````markdown
# File Handling Automation Pattern

## 1. Introduction

File handling becomes especially valuable when it is combined with automation logic.

In Storage Test Automation, files are commonly used to:

- Read test input
- Load configuration
- Process test results
- Parse logs
- Store execution data
- Compare expected and actual results
- Generate reports
- Preserve test artifacts

A strong automation script should not treat file handling as isolated operations.

Instead, it should follow a predictable processing pattern:

```text
Input
  ↓
Read
  ↓
Parse
  ↓
Validate
  ↓
Process
  ↓
Generate Output
  ↓
Report
````

This pattern can be reused across many automation tasks.

---

# 2. The Core Automation Pattern

A practical file-based automation workflow is:

```text
              Input Files
                  |
                  ↓
              File Access
                  |
                  ↓
                Parse
                  |
                  ↓
              Validate
                  |
                  ↓
               Process
                  |
                  ↓
            Generate Results
                  |
                  ↓
               Report
```

Each stage has a specific responsibility.

### Input

Obtain information from:

* TXT
* CSV
* JSON
* YAML
* Logs

### Parse

Convert raw file content into useful Python structures.

### Validate

Check whether the input is correct.

### Process

Perform the actual automation logic.

### Output

Write results, reports, or artifacts.

---

# 3. Separation of Responsibilities

A maintainable automation script should avoid putting everything into one large block.

Instead:

```text
Read
 ↓
Parse
 ↓
Validate
 ↓
Process
 ↓
Write
```

Each stage should have a clear purpose.

For example:

```python
def read_results(filename):
    pass


def validate_results(results):
    pass


def process_results(results):
    pass


def write_report(filename, report):
    pass
```

This makes the automation easier to:

* Understand
* Test
* Debug
* Modify
* Reuse

---

# 4. Input Stage

The first stage is obtaining the input.

Example:

```python
from pathlib import Path

input_path = Path("results.txt")

with input_path.open("r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

The important principle is:

> Open the file, process the data, and release the resource safely.

Using:

```python
with
```

ensures proper cleanup.

---

# 5. Parsing Stage

Raw file data is often not directly useful.

Example input:

```text
TEST_001 PASS
TEST_002 FAIL
TEST_003 PASS
```

The automation can parse each line:

```python
test_id, status = line.split()
```

Now the data has meaning:

```text
test_id → TEST_001
status  → PASS
```

Parsing converts:

```text
Raw text
   ↓
Structured Python data
```

---

# 6. Validation Stage

Parsing does not necessarily mean the data is valid.

Consider:

```text
TEST_001 PASS
TEST_002 UNKNOWN
TEST_003
```

Potential problems:

* Missing fields
* Invalid status
* Empty lines
* Unexpected format

Validation should detect these conditions before processing.

Example:

```python
valid_statuses = {"PASS", "FAIL"}

if status not in valid_statuses:
    raise ValueError(f"Invalid status: {status}")
```

The automation pipeline becomes:

```text
Read
 ↓
Parse
 ↓
Validate
 ↓
Process
```

---

# 7. Processing Stage

After validation, perform the actual automation logic.

Example:

```python
total = 0
passed = 0
failed = 0

for test_id, status in results:
    total += 1

    if status == "PASS":
        passed += 1

    elif status == "FAIL":
        failed += 1
```

The processing stage should focus on the actual requirement.

For example:

* Count failures
* Calculate pass rate
* Identify failed tests
* Extract error messages
* Compare results
* Aggregate performance data

---

# 8. Output Stage

After processing, generate an output file.

Example:

```python
from pathlib import Path

report_path = Path("report.txt")

with report_path.open("w", encoding="utf-8") as file:
    file.write("Storage Test Report\n")
    file.write("===================\n")
    file.write(f"Total : {total}\n")
    file.write(f"Passed: {passed}\n")
    file.write(f"Failed: {failed}\n")
```

The output should clearly communicate the result.

---

# 9. Complete Example

Suppose:

```text
results.txt
```

contains:

```text
TEST_001 PASS
TEST_002 FAIL
TEST_003 PASS
TEST_004 FAIL
```

A simple automation workflow:

```python
from pathlib import Path

input_path = Path("results.txt")
report_path = Path("report.txt")

total = 0
passed = 0
failed = 0
failed_tests = []

with input_path.open("r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        test_id, status = line.split()

        if status not in {"PASS", "FAIL"}:
            raise ValueError(f"Invalid status: {status}")

        total += 1

        if status == "PASS":
            passed += 1

        else:
            failed += 1
            failed_tests.append(test_id)

with report_path.open("w", encoding="utf-8") as file:
    file.write("Storage Test Report\n")
    file.write("===================\n\n")

    file.write(f"Total Tests : {total}\n")
    file.write(f"Passed      : {passed}\n")
    file.write(f"Failed      : {failed}\n\n")

    file.write("Failed Tests:\n")

    for test_id in failed_tests:
        file.write(f"{test_id}\n")

print("Report generated.")
```

The workflow is:

```text
results.txt
     ↓
Read
     ↓
Parse
     ↓
Validate
     ↓
Count results
     ↓
Collect failures
     ↓
report.txt
```

---

# 10. Configuration-Driven Automation

File handling becomes even more powerful when configuration is separated from Python code.

Example:

```yaml
execution:
  timeout: 60
  retries: 2

tests:
  - read
  - write
  - verify
```

Python loads it:

```python
import yaml

with open("config.yaml", "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)
```

Then:

```python
timeout = config["execution"]["timeout"]
retries = config["execution"]["retries"]
tests = config["tests"]
```

The automation logic does not need to hard-code these values.

---

# 11. Input → Processing → Output

A useful mental model is:

```text
INPUT
  |
  |  File / Config / Log
  ↓
PROCESSING
  |
  |  Parse / Validate / Analyze
  ↓
OUTPUT
  |
  |  Report / Result / Artifact
  ↓
CONSUMER
```

Example:

```text
test_results.csv
       ↓
Python automation
       ↓
Analyze failures
       ↓
failure_report.txt
```

---

# 12. Multiple Input Files

Automation may need multiple input files.

Example:

```text
expected.json
actual.json
```

The automation can:

```text
expected.json ──┐
                ├──→ Compare → Report
actual.json ────┘
```

Python:

```python
import json

with open("expected.json", "r", encoding="utf-8") as file:
    expected = json.load(file)

with open("actual.json", "r", encoding="utf-8") as file:
    actual = json.load(file)

if expected == actual:
    print("PASS")
else:
    print("FAIL")
```

For detailed differences, `difflib` or structured comparison logic can be used.

---

# 13. Directory-Based Automation

Sometimes the input is not one file.

For example:

```text
logs/
├── controller.log
├── kernel.log
├── storage.log
└── test.log
```

The automation can discover files:

```python
from pathlib import Path

log_dir = Path("logs")

for path in log_dir.rglob("*.log"):
    print(path)
```

Then:

```text
Discover
   ↓
Read
   ↓
Parse
   ↓
Analyze
   ↓
Report
```

This is common in storage validation because test runs can produce many artifacts.

---

# 14. Large File Automation

For large files, avoid:

```python
data = file.read()
```

when the complete file is unnecessary.

Prefer:

```python
with open("large.log", "r", encoding="utf-8") as file:
    for line in file:
        process(line)
```

This keeps memory usage low.

The pattern remains the same:

```text
Read incrementally
       ↓
Parse
       ↓
Process
       ↓
Report
```

Only the reading strategy changes.

---

# 15. Error Handling in the Automation Pipeline

Each stage can fail.

Example:

```text
Input
 ↓
FileNotFoundError
```

or:

```text
Parse
 ↓
ValueError
```

or:

```text
JSON parsing
 ↓
JSONDecodeError
```

or:

```text
YAML parsing
 ↓
YAMLError
```

Therefore, automation should handle expected failures appropriately.

Example:

```python
try:
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

except FileNotFoundError:
    print("Configuration file not found.")

except json.JSONDecodeError:
    print("Configuration file contains invalid JSON.")
```

The goal is not to catch every possible exception blindly.

The goal is:

> Handle failures that the automation can reasonably understand and report.

---

# 16. Logging vs Printing

During small scripts:

```python
print("Test started")
```

is acceptable.

For larger automation frameworks, proper logging is preferable.

Example:

```python
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Test execution started")
logging.warning("Retrying test")
logging.error("Test execution failed")
```

This provides better diagnostic information than scattered `print()` statements.

File handling and logging often work together:

```text
Automation
    |
    +── Results
    |
    +── Reports
    |
    +── Logs
```

---

# 17. Safe Output Generation

Be careful when using:

```python
open("report.txt", "w")
```

because `w` truncates the existing file.

If the previous report must be preserved, consider:

```text
report_001.txt
report_002.txt
```

or create an output directory for each test run:

```text
results/
└── run_001/
    ├── report.txt
    ├── results.csv
    └── execution.log
```

This is much safer for test artifact preservation.

---

# 18. Dynamic Output Directories

Using `pathlib`:

```python
from pathlib import Path

output_dir = Path("results") / "run_001"

output_dir.mkdir(parents=True, exist_ok=True)

report_path = output_dir / "report.txt"
log_path = output_dir / "execution.log"
```

Now the automation has a dedicated location for artifacts.

This prevents different test runs from unnecessarily overwriting each other.

---

# 19. Artifact Preservation

Storage testing often generates valuable artifacts.

Examples:

```text
dmesg.log
smart.log
nvme_list.json
test_results.csv
performance.csv
report.txt
```

A good automation framework should preserve these artifacts.

A useful structure is:

```text
test_run/
├── config.yaml
├── logs/
│   ├── kernel.log
│   └── test.log
├── results/
│   ├── results.csv
│   └── metadata.json
└── report/
    └── report.txt
```

This makes troubleshooting much easier.

---

# 20. Idempotent File Operations

Automation may be executed multiple times.

A good script should behave predictably when rerun.

For example:

```python
output_dir.mkdir(parents=True, exist_ok=True)
```

is idempotent.

Running it once:

```text
Directory created
```

Running it again:

```text
No failure because directory already exists
```

This is useful in automation frameworks.

---

# 21. Avoid Hard-Coded Paths

Avoid:

```python
open("/home/user/project/results/report.txt")
```

Prefer:

```python
from pathlib import Path

base_dir = Path("project")
report_path = base_dir / "results" / "report.txt"
```

Even better, derive paths dynamically:

```python
base_dir = Path.cwd()
output_dir = base_dir / "results"
```

This makes the automation more portable.

---

# 22. File Handling Pipeline Example

A realistic storage test flow could be:

```text
                   config.yaml
                       |
                       ↓
                  Load Config
                       |
                       ↓
                  Validate Config
                       |
                       ↓
                 Execute Tests
                       |
              +--------+--------+
              |                 |
              ↓                 ↓
          test logs        test results
              |                 |
              ↓                 ↓
             TXT               CSV
              |                 |
              +--------+--------+
                       |
                       ↓
                   Analyze
                       |
                       ↓
                 Generate Report
                       |
                       ↓
                    report.txt
```

This is a common automation architecture.

---

# 23. A More Structured Implementation

As automation grows, functions can represent stages.

```python
from pathlib import Path


def read_results(path):
    results = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            test_id, status = line.split()
            results.append((test_id, status))

    return results


def validate_results(results):
    valid_statuses = {"PASS", "FAIL"}

    for test_id, status in results:
        if status not in valid_statuses:
            raise ValueError(
                f"Invalid status for {test_id}: {status}"
            )


def process_results(results):
    total = len(results)
    passed = sum(status == "PASS" for _, status in results)
    failed = sum(status == "FAIL" for _, status in results)

    failed_tests = [
        test_id
        for test_id, status in results
        if status == "FAIL"
    ]

    return total, passed, failed, failed_tests
```

Then:

```python
input_path = Path("results.txt")

results = read_results(input_path)
validate_results(results)

total, passed, failed, failed_tests = process_results(results)
```

This separates responsibilities.

---

# 24. Why Separation Matters

Compare:

```text
One huge function
      ↓
Read
Parse
Validate
Process
Write
Log
Error handling
Everything mixed together
```

with:

```text
read_results()
      ↓
validate_results()
      ↓
process_results()
      ↓
write_report()
```

The second structure is easier to:

* Debug
* Test
* Modify
* Reuse
* Review

This becomes increasingly important as automation frameworks grow.

---

# 25. Common Automation Mistakes

## Mistake 1 — Mixing all responsibilities together

Avoid creating one enormous block that:

* Opens files
* Parses data
* Executes tests
* Generates reports
* Handles every error

Separate logical responsibilities.

---

## Mistake 2 — Loading huge files unnecessarily

Avoid:

```python
data = file.read()
```

when processing can happen line-by-line.

---

## Mistake 3 — Overwriting valuable artifacts

Be careful with:

```python
open(path, "w")
```

because it truncates the file.

---

## Mistake 4 — Ignoring malformed input

Do not assume every input line is valid.

Validate important input.

---

## Mistake 5 — Hard-coding paths

Use `Path` and construct paths dynamically.

---

## Mistake 6 — Losing diagnostic information

Do not delete logs/results immediately when a test fails.

Preserve artifacts needed for troubleshooting.

---

## Mistake 7 — Catching every exception

Avoid:

```python
try:
    ...
except Exception:
    pass
```

This can hide real failures.

Handle known failures explicitly.

---

# 26. Industry-Oriented Pattern

A maintainable file-based automation framework can be viewed as:

```text
             Configuration
                  |
                  ↓
             Input Manager
                  |
                  ↓
                Parser
                  |
                  ↓
              Validator
                  |
                  ↓
             Test Engine
                  |
                  ↓
            Result Collector
                  |
          +-------+-------+
          |               |
          ↓               ↓
        Logger          Reporter
          |               |
          ↓               ↓
       log files      report files
```

The exact architecture will depend on the framework, but the separation of responsibilities is broadly useful.

---

# 27. Interview Questions

## Basic

**1. What is a file-handling automation pipeline?**

A sequence that reads input, parses and validates it, processes the information, and generates output.

**2. Why separate parsing from processing?**

It makes the code easier to understand, test, debug, and maintain.

**3. Why use `pathlib` in automation?**

It provides a clear and portable way to construct and manipulate filesystem paths.

---

## Intermediate

**4. Why shouldn't large files always be loaded using `read()`?**

Because the entire file is loaded into memory. Iterating line-by-line is usually more memory-efficient.

**5. Why is validation a separate stage?**

Parsing establishes structure; validation determines whether the data satisfies the requirements.

**6. Why preserve test artifacts?**

They provide evidence and diagnostic information when tests fail.

**7. What is idempotency in file automation?**

An operation can be repeated without causing unintended additional effects or failures.

---

## Storage Automation

**8. Give an example of an automation pipeline for storage testing.**

```text
config.yaml
    ↓
Load configuration
    ↓
Validate
    ↓
Execute storage tests
    ↓
Collect logs/results
    ↓
Analyze
    ↓
Generate report
```

**9. Why should configuration be separated from automation logic?**

The same automation can operate with different environments, devices, test selections, and execution parameters without changing the core implementation.

**10. What files might a storage test produce?**

Examples:

```text
Execution logs
Test results
Device metadata
Performance measurements
Failure reports
Debug artifacts
```

---

# 28. Key Takeaways

The core pattern to remember is:

```text
INPUT
 ↓
READ
 ↓
PARSE
 ↓
VALIDATE
 ↓
PROCESS
 ↓
OUTPUT
 ↓
REPORT
```

For larger automation:

```text
Configuration
      ↓
Execution
      ↓
Collection
      ↓
Analysis
      ↓
Reporting
      ↓
Artifact Preservation
```

Important engineering principles:

```text
Use context managers
Use pathlib
Validate input
Process large files incrementally
Separate responsibilities
Avoid unnecessary hard-coded paths
Preserve useful artifacts
Handle expected errors
Make operations predictable and repeatable
```

---

# Automation Principle

> **A good automation script should not merely process files; it should create a predictable pipeline from input to validated result and preserved evidence.**

The reusable mental model is:

```text
          INPUT
            ↓
          PARSE
            ↓
         VALIDATE
            ↓
         PROCESS
            ↓
          RESULT
            ↓
          REPORT
            ↓
        ARTIFACTS
```

This pattern will repeatedly appear when building real Storage Test Automation tools.



