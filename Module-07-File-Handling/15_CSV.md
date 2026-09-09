# `15_CSV.md`

# CSV

## 1. Introduction

CSV stands for **Comma-Separated Values**.

It is a simple text-based format used to represent **tabular data**.

Example:

```text
device,status,capacity_gb
device_01,ONLINE,1024
device_02,OFFLINE,2048
device_03,ONLINE,4096
```

CSV is commonly used in automation for:

* Test results
* Device inventories
* Performance measurements
* Benchmark results
* Test-case lists
* Execution summaries
* Data exchange between tools

Python provides the standard-library:

```python
import csv
```

for working with CSV files.

---

# 2. Why CSV Matters in Storage Automation

Storage testing can generate large amounts of structured tabular information.

For example:

```text
test_id,device,status,duration
TEST_001,nvme0,PASS,120
TEST_002,nvme0,FAIL,145
TEST_003,nvme1,PASS,98
```

A Python automation framework can read this data and:

* Filter failed tests
* Calculate statistics
* Validate device state
* Generate reports
* Convert results into another format

CSV is particularly useful when the data naturally fits rows and columns.

---

# 3. CSV Structure

A CSV file usually consists of:

```text
Header
Row
Row
Row
```

Example:

```text
test_id,status,duration
TEST_001,PASS,120
TEST_002,FAIL,145
TEST_003,PASS,98
```

Here:

### Header

```text
test_id,status,duration
```

### First data row

```text
TEST_001,PASS,120
```

### Second data row

```text
TEST_002,FAIL,145
```

---

# 4. Importing the CSV Module

Python's built-in CSV support is provided by:

```python
import csv
```

No external package is required for normal CSV processing.

---

# 5. Reading a CSV with `csv.reader`

The basic CSV reader is:

```python
csv.reader()
```

Example:

```python
import csv

with open(
    "results.csv",
    "r",
    encoding="utf-8",
    newline=""
) as file:

    reader = csv.reader(file)

    for row in reader:
        print(row)
```

For:

```text
test_id,status,duration
TEST_001,PASS,120
TEST_002,FAIL,145
```

the rows are represented as Python lists.

Conceptually:

```python
[
    "test_id",
    "status",
    "duration"
]
```

and:

```python
[
    "TEST_001",
    "PASS",
    "120"
]
```

---

# 6. Important: CSV Values Are Strings

Consider:

```text
test_id,status,duration
TEST_001,PASS,120
```

When read with `csv.reader`:

```python
for row in reader:
    print(row)
```

the result is approximately:

```python
[
    "TEST_001",
    "PASS",
    "120"
]
```

Notice:

```text
"120"
```

is a string.

It is **not automatically converted to an integer**.

---

# 7. Converting Numeric Values

If the duration is needed as a number:

```python
duration = int(row[2])
```

Example:

```python
for row in reader:

    duration = int(row[2])

    print(duration)
```

Now:

```python
type(duration)
```

is:

```text
int
```

This is an important part of processing CSV data.

---

# 8. Accessing Columns by Index

Using:

```python
csv.reader()
```

each row behaves like a list.

Example:

```text
test_id,status,duration
TEST_001,PASS,120
```

Then:

```python
row[0]
```

means:

```text
TEST_001
```

and:

```python
row[1]
```

means:

```text
PASS
```

and:

```python
row[2]
```

means:

```text
120
```

---

# 9. Problem with Numeric Indexes

Code such as:

```python
if row[1] == "FAIL":
```

works, but the meaning of `row[1]` is not immediately obvious.

Someone reading the code has to remember:

```text
column 0 → test_id
column 1 → status
column 2 → duration
```

For structured automation, `DictReader` can make the code clearer.

---

# 10. `csv.DictReader`

Python provides:

```python
csv.DictReader()
```

Example:

```python
import csv

with open(
    "results.csv",
    "r",
    encoding="utf-8",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:
        print(row)
```

Each row behaves like a dictionary.

Example:

```python
{
    "test_id": "TEST_001",
    "status": "PASS",
    "duration": "120"
}
```

---

# 11. Accessing `DictReader` Values

Now we can write:

```python
for row in reader:

    print(row["test_id"])
    print(row["status"])
    print(row["duration"])
```

This is much more readable than:

```python
print(row[0])
print(row[1])
print(row[2])
```

For automation code, named fields are often easier to maintain.

---

# 12. Filtering Failed Tests

Example CSV:

```text
test_id,status,duration
TEST_001,PASS,120
TEST_002,FAIL,145
TEST_003,PASS,98
TEST_004,FAIL,175
```

Python:

```python
import csv

with open(
    "results.csv",
    "r",
    encoding="utf-8",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        if row["status"] == "FAIL":
            print(row["test_id"])
```

Output:

```text
TEST_002
TEST_004
```

---

# 13. `DictReader` and Numeric Conversion

Remember that even with `DictReader`:

```python
row["duration"]
```

is initially a string.

Convert it:

```python
duration = int(row["duration"])
```

Example:

```python
for row in reader:

    duration = int(row["duration"])

    if duration > 150:
        print(row["test_id"])
```

This finds tests whose duration exceeds 150 seconds.

---

# 14. Handling CSV Headers

`DictReader` automatically uses the first row as field names by default.

Given:

```text
test_id,status,duration
TEST_001,PASS,120
```

Python interprets:

```text
test_id
status
duration
```

as dictionary keys.

This is one reason `DictReader` is convenient for CSV files with headers.

---

# 15. Using Explicit Field Names

You can also provide field names manually.

Example:

```python
reader = csv.DictReader(
    file,
    fieldnames=[
        "test_id",
        "status",
        "duration"
    ]
)
```

This is useful when the CSV does not contain a header row.

However, if the file already has a header and you manually provide `fieldnames`, you need to handle that header explicitly.

---

# 16. Reading CSV with `Path`

Using `pathlib`:

```python
from pathlib import Path
import csv

path = Path("results.csv")

with path.open(
    "r",
    encoding="utf-8",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:
        print(row)
```

This follows the file-handling approach used throughout this module.

---

# 17. Why `newline=""` Is Recommended

When opening CSV files with Python's `csv` module, use:

```python
newline=""
```

Example:

```python
with open(
    "results.csv",
    "r",
    encoding="utf-8",
    newline=""
) as file:
```

and when writing:

```python
with open(
    "results.csv",
    "w",
    encoding="utf-8",
    newline=""
) as file:
```

This allows the CSV module to handle newline conventions correctly.

It is a recommended practice for Python CSV processing.

---

# 18. Writing CSV with `csv.writer`

To create CSV rows, use:

```python
csv.writer()
```

Example:

```python
import csv

with open(
    "results.csv",
    "w",
    encoding="utf-8",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow(
        ["test_id", "status", "duration"]
    )

    writer.writerow(
        ["TEST_001", "PASS", 120]
    )
```

Result:

```text
test_id,status,duration
TEST_001,PASS,120
```

---

# 19. `writerow()`

`writerow()` writes one row.

Example:

```python
writer.writerow(
    ["TEST_002", "FAIL", 145]
)
```

Use it when adding a single record at a time.

---

# 20. `writerows()`

`writerows()` writes multiple rows.

Example:

```python
rows = [
    ["TEST_001", "PASS", 120],
    ["TEST_002", "FAIL", 145],
    ["TEST_003", "PASS", 98]
]

writer.writerows(rows)
```

Result:

```text
TEST_001,PASS,120
TEST_002,FAIL,145
TEST_003,PASS,98
```

---

# 21. Writing Headers

A common pattern:

```python
writer.writerow(
    ["test_id", "status", "duration"]
)
```

Then:

```python
writer.writerow(
    ["TEST_001", "PASS", 120]
)
```

This creates a header followed by data.

---

# 22. `csv.DictWriter`

For dictionary-based data, use:

```python
csv.DictWriter()
```

Example:

```python
import csv

fieldnames = [
    "test_id",
    "status",
    "duration"
]

with open(
    "results.csv",
    "w",
    encoding="utf-8",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerow({
        "test_id": "TEST_001",
        "status": "PASS",
        "duration": 120
    })
```

Result:

```text
test_id,status,duration
TEST_001,PASS,120
```

---

# 23. `writeheader()`

`DictWriter` provides:

```python
writer.writeheader()
```

This writes the column names.

Instead of manually doing:

```python
writer.writerow(
    ["test_id", "status", "duration"]
)
```

you define:

```python
fieldnames = [
    "test_id",
    "status",
    "duration"
]
```

and call:

```python
writer.writeheader()
```

---

# 24. Writing Multiple Dictionary Records

Example:

```python
import csv

results = [
    {
        "test_id": "TEST_001",
        "status": "PASS",
        "duration": 120
    },
    {
        "test_id": "TEST_002",
        "status": "FAIL",
        "duration": 145
    }
]

fieldnames = [
    "test_id",
    "status",
    "duration"
]

with open(
    "results.csv",
    "w",
    encoding="utf-8",
    newline=""
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(results)
```

This produces:

```text
test_id,status,duration
TEST_001,PASS,120
TEST_002,FAIL,145
```

---

# 25. Reading and Writing CSV Together

A common automation workflow is:

```text
CSV input
   ↓
Read
   ↓
Parse
   ↓
Filter / Validate
   ↓
CSV output
```

Example:

```python
import csv

with open(
    "results.csv",
    "r",
    encoding="utf-8",
    newline=""
) as source:

    reader = csv.DictReader(source)

    with open(
        "failed_results.csv",
        "w",
        encoding="utf-8",
        newline=""
    ) as destination:

        fieldnames = reader.fieldnames

        writer = csv.DictWriter(
            destination,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for row in reader:

            if row["status"] == "FAIL":
                writer.writerow(row)
```

This creates a smaller CSV containing only failed tests.

---

# 26. CSV as a Test-Result Format

Example:

```text
test_id,device,status,duration
TEST_001,nvme0,PASS,120
TEST_002,nvme0,FAIL,145
TEST_003,nvme1,PASS,98
TEST_004,nvme1,FAIL,210
```

A test framework can use this as an execution record.

Python can calculate:

```text
Total tests
Passed tests
Failed tests
Average duration
Longest test
Failures by device
```

---

# 27. Counting PASS and FAIL Results

```python
import csv

passed = 0
failed = 0

with open(
    "results.csv",
    "r",
    encoding="utf-8",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        if row["status"] == "PASS":
            passed += 1

        elif row["status"] == "FAIL":
            failed += 1

print("Passed:", passed)
print("Failed:", failed)
```

This is a simple but realistic automation pattern.

---

# 28. Calculating Average Duration

Because CSV values are strings:

```python
duration = int(row["duration"])
```

Then:

```python
total_duration = 0
count = 0

with open(
    "results.csv",
    "r",
    encoding="utf-8",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        total_duration += int(row["duration"])
        count += 1

if count:
    average = total_duration / count
else:
    average = 0

print("Average duration:", average)
```

---

# 29. Handling Malformed Numeric Data

Suppose the CSV contains:

```text
TEST_002,FAIL,unknown
```

Then:

```python
int(row["duration"])
```

raises:

```text
ValueError
```

A robust automation script can handle this:

```python
try:
    duration = int(row["duration"])
except ValueError:
    print(
        f"Invalid duration for {row['test_id']}"
    )
```

This connects CSV processing with the exception-handling concepts already learned.

---

# 30. Handling Missing Columns

Suppose the expected CSV contains:

```text
test_id,status,duration
```

but the actual file contains:

```text
test_id,status
```

Then:

```python
row["duration"]
```

may raise:

```text
KeyError
```

A robust automation tool should validate the expected columns before processing.

Example:

```python
required_columns = {
    "test_id",
    "status",
    "duration"
}

actual_columns = set(reader.fieldnames or [])

missing = required_columns - actual_columns

if missing:
    raise ValueError(
        f"Missing columns: {missing}"
    )
```

---

# 31. CSV Validation Pattern

A production-oriented flow can be:

```text
Open CSV
   ↓
Read header
   ↓
Validate required columns
   ↓
Read records
   ↓
Validate individual values
   ↓
Process
   ↓
Generate report
```

This is better than assuming the CSV is always perfect.

---

# 32. CSV and Different Delimiters

CSV does not always literally use a comma.

Some files use:

```text
;
```

or:

```text
\t
```

For example:

```text
device;status;capacity
nvme0;ONLINE;2048
```

You can specify the delimiter:

```python
reader = csv.reader(
    file,
    delimiter=";"
)
```

For tab-separated data:

```python
reader = csv.reader(
    file,
    delimiter="\t"
)
```

Therefore, CSV-style tabular files can use different delimiters.

---

# 33. Quoted Fields

CSV supports fields containing commas by using quoting.

Example:

```text
test_id,description,status
TEST_001,"Read, write and verify",PASS
```

A naive:

```python
line.split(",")
```

can incorrectly split the description.

The `csv` module understands CSV quoting rules.

Therefore:

> **Use Python's `csv` module instead of manually splitting CSV lines with `str.split(",")`.**

---

# 34. Why `split(",")` Is Not a Proper CSV Parser

Consider:

```text
TEST_001,"Read, write test",PASS
```

Using:

```python
line.split(",")
```

can produce an incorrect number of fields because the comma inside the quoted description is data, not a delimiter.

The CSV module handles this correctly:

```python
reader = csv.reader(file)
```

This is an important practical distinction.

---

# 35. CSV and Storage Device Inventory

CSV works well for device inventories.

Example:

```text
device,model,capacity_gb,status
nvme0,DriveA,1024,ONLINE
nvme1,DriveB,2048,ONLINE
nvme2,DriveC,1024,OFFLINE
```

Python:

```python
import csv

with open(
    "devices.csv",
    "r",
    encoding="utf-8",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for device in reader:

        if device["status"] == "OFFLINE":
            print(
                f"Offline device: {device['device']}"
            )
```

Output:

```text
Offline device: nvme2
```

---

# 36. CSV and Performance Results

Storage benchmarks naturally produce tabular data:

```text
device,operation,iops,latency_us
nvme0,read,125000,80
nvme0,write,95000,110
nvme1,read,130000,75
```

Python can process these records:

```python
for row in reader:

    iops = int(row["iops"])
    latency = int(row["latency_us"])

    if latency > 100:
        print(
            f"High latency: {row['device']}"
        )
```

This is a realistic use of CSV in storage engineering.

---

# 37. Large CSV Files

The `csv` module supports iteration.

Example:

```python
with open(
    "large_results.csv",
    "r",
    encoding="utf-8",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:
        process(row)
```

This allows records to be processed incrementally.

You do not necessarily need:

```python
rows = list(reader)
```

which would store every record in memory.

For large datasets, direct iteration is generally preferable when possible.

---

# 38. CSV + Large File Processing

This combines the concepts from the previous topic.

Instead of:

```python
rows = list(reader)
```

prefer:

```python
for row in reader:
    process(row)
```

Conceptually:

```text
CSV file
   ↓
Read record
   ↓
Process
   ↓
Read next record
   ↓
Process
   ↓
...
```

This is a scalable automation pattern.

---

# 39. CSV + Pathlib

A complete modern pattern:

```python
from pathlib import Path
import csv

path = Path("results.csv")

with path.open(
    "r",
    encoding="utf-8",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:
        print(row["test_id"])
```

This combines:

```text
Pathlib
+
Context managers
+
CSV
+
Iteration
```

---

# 40. Common Mistakes

### Mistake 1 — Forgetting that CSV values are strings

```python
duration = row["duration"]
```

does not automatically produce an integer.

Use:

```python
duration = int(row["duration"])
```

when numeric processing is required.

---

### Mistake 2 — Using `split(",")`

Avoid:

```python
line.split(",")
```

for real CSV parsing.

Quoted commas and CSV formatting rules make manual splitting unreliable.

Use:

```python
csv.reader()
```

or:

```python
csv.DictReader()
```

---

### Mistake 3 — Forgetting `newline=""`

For CSV files, use:

```python
newline=""
```

when opening them with Python's `csv` module.

---

### Mistake 4 — Using the wrong column index

With:

```python
csv.reader()
```

this:

```python
row[2]
```

depends on the column order.

If the schema changes, the code may break or read the wrong field.

`DictReader` often makes such code clearer.

---

### Mistake 5 — Loading huge CSV files into a list

Avoid unnecessarily:

```python
rows = list(reader)
```

For large files, process:

```python
for row in reader:
    ...
```

instead.

---

### Mistake 6 — Assuming required columns exist

Validate:

```python
reader.fieldnames
```

before processing mandatory fields.

---

# 41. Interview Questions

### Q1. What is CSV?

CSV is a text-based format for representing tabular data using rows and fields, commonly separated by commas.

---

### Q2. Which Python module is used for CSV?

```python
import csv
```

It is part of the standard library.

---

### Q3. What is the difference between `csv.reader()` and `csv.DictReader()`?

`csv.reader()` returns rows as sequences such as lists.

`csv.DictReader()` maps each row to column names, providing dictionary-like access.

---

### Q4. Why is `DictReader` often easier to maintain?

Because fields can be accessed by meaningful names:

```python
row["status"]
```

instead of positional indexes:

```python
row[1]
```

---

### Q5. Are CSV values automatically converted to integers?

No.

They are generally returned as strings and must be converted explicitly.

```python
duration = int(row["duration"])
```

---

### Q6. Why shouldn't you parse CSV with `split(",")`?

Because CSV supports quoting and fields may themselves contain commas.

---

### Q7. Why use `newline=""` with the CSV module?

It allows the CSV module to handle newline processing correctly across platforms.

---

### Q8. How do you write one CSV row?

```python
writer.writerow(row)
```

---

### Q9. How do you write multiple rows?

```python
writer.writerows(rows)
```

---

### Q10. What is `DictWriter` used for?

It writes dictionary-based records to CSV using specified field names.

---

### Q11. How do you write CSV headers with `DictWriter`?

```python
writer.writeheader()
```

---

### Q12. How can you process a large CSV efficiently?

Iterate over the CSV reader directly rather than converting the entire reader into a list.

---

# 42. Key Takeaways

### Read CSV rows

```python
reader = csv.reader(file)

for row in reader:
    print(row)
```

### Read CSV as dictionaries

```python
reader = csv.DictReader(file)

for row in reader:
    print(row["status"])
```

### Write CSV

```python
writer = csv.writer(file)

writer.writerow(
    ["test_id", "status"]
)
```

### Write dictionary records

```python
writer = csv.DictWriter(
    file,
    fieldnames=["test_id", "status"]
)

writer.writeheader()
writer.writerow({
    "test_id": "TEST_001",
    "status": "PASS"
})
```

### Convert numeric values

```python
duration = int(row["duration"])
```

### Process large CSV files

```python
for row in reader:
    process(row)
```

---

# 43. Automation Principle

> **Use CSV when your data naturally fits rows and columns, and use Python's `csv` module instead of manually parsing comma-separated text.**

A typical storage automation workflow is:

```text
Test execution
      ↓
Generate tabular results
      ↓
CSV file
      ↓
csv.DictReader()
      ↓
Validate records
      ↓
Calculate statistics
      ↓
Filter failures
      ↓
Generate report
```

CSV is particularly effective for:

* Test-result tables
* Device inventories
* Benchmark data
* Performance measurements
* Execution summaries

The next topic covers **YAML**, which is especially useful for human-readable configuration files.

**Next file:** `16_YAML.md`

