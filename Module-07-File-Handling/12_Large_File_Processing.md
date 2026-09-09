# `12_Large_File_Processing.md`

# Large File Processing

## 1. Introduction

Storage test automation frequently generates **large files**.

Examples include:

* Kernel logs
* Storage controller logs
* SMART reports
* Command output
* Test execution logs
* Debug traces
* Performance measurements
* Failure dumps
* Long-duration stress-test logs

A file may contain:

```text
10,000 lines
100,000 lines
1,000,000 lines
```

or much more.

The automation challenge is:

> **How can we process large files without unnecessarily loading the entire file into memory?**

The fundamental solution is **streaming / line-by-line processing**.

---

# 2. The Memory Problem

Suppose a file contains:

```text
10 GB of logs
```

If we do:

```python
with open("large.log", "r", encoding="utf-8") as file:
    data = file.read()
```

Python attempts to load the file contents into memory.

Conceptually:

```text
Disk
 │
 │ 10 GB
 ▼
RAM
 │
 └── large string
```

This can consume a huge amount of memory.

It may cause:

* High memory usage
* Slow processing
* Memory pressure
* `MemoryError`
* Poor scalability

For automation, this is usually undesirable.

---

# 3. Line-by-Line Processing

Instead of:

```python
data = file.read()
```

process the file incrementally:

```python
with open("large.log", "r", encoding="utf-8") as file:

    for line in file:
        process(line)
```

Conceptually:

```text
Disk
 │
 ├── line 1 ──→ process ──→ discard
 ├── line 2 ──→ process ──→ discard
 ├── line 3 ──→ process ──→ discard
 └── ...
```

The entire file does not need to be stored in memory.

---

# 4. Why File Iteration Is Efficient

Python file objects are iterable.

Example:

```python
with open("large.log", "r", encoding="utf-8") as file:

    for line in file:
        print(line)
```

Python reads the file incrementally rather than constructing one enormous string containing the entire file.

This makes:

```python
for line in file:
```

the preferred pattern for many large-file processing tasks.

---

# 5. `read()` vs Iteration

Compare:

### Entire file

```python
data = file.read()
```

Conceptually:

```text
Entire file → memory
```

### Line-by-line

```python
for line in file:
    ...
```

Conceptually:

```text
One portion at a time → processing
```

For large logs:

```text
Prefer iteration
```

unless there is a specific reason to load the entire content.

---

# 6. `readlines()` and Memory

This also needs attention:

```python
lines = file.readlines()
```

`readlines()` creates a list containing all lines.

For a very large file:

```text
Large file
    ↓
All lines
    ↓
Large Python list
    ↓
High memory usage
```

Therefore, for large files:

```python
for line in file:
```

is generally preferable to:

```python
file.readlines()
```

---

# 7. Processing a Large Log

Suppose:

```text
storage.log
```

contains millions of lines.

We want to count failures.

```python
from pathlib import Path

log_file = Path("storage.log")

failure_count = 0

with log_file.open("r", encoding="utf-8") as file:

    for line in file:

        if "FAIL" in line:
            failure_count += 1

print("Failures:", failure_count)
```

Memory usage does not grow with the number of log lines stored in the file.

We maintain only the information needed:

```python
failure_count
```

---

# 8. Large File Processing Pattern

A common pattern is:

```python
from pathlib import Path

file_path = Path("large.log")

with file_path.open("r", encoding="utf-8") as file:

    for line in file:

        line = line.strip()

        if not line:
            continue

        # Process line
```

This provides:

```text
Open
 ↓
Read one line
 ↓
Clean
 ↓
Validate
 ↓
Process
 ↓
Read next line
```

---

# 9. Counting Different Results

Suppose a test log contains:

```text
TEST_001 PASS
TEST_002 FAIL
TEST_003 PASS
TEST_004 FAIL
```

We can process it without loading the entire file:

```python
from pathlib import Path

file_path = Path("test_results.txt")

passed = 0
failed = 0

with file_path.open("r", encoding="utf-8") as file:

    for line in file:

        line = line.strip()

        if not line:
            continue

        test_id, status = line.split()

        if status == "PASS":
            passed += 1

        elif status == "FAIL":
            failed += 1

print("Passed:", passed)
print("Failed:", failed)
```

Only the current line needs to be processed.

---

# 10. Searching for Errors

A common storage troubleshooting task is finding error messages.

```python
from pathlib import Path

log_file = Path("controller.log")

with log_file.open("r", encoding="utf-8") as file:

    for line in file:

        if "ERROR" in line:
            print(line.strip())
```

This works even when the log is very large.

---

# 11. Searching for Multiple Conditions

Example:

```python
with log_file.open("r", encoding="utf-8") as file:

    for line in file:

        if "ERROR" in line or "FAIL" in line:
            print(line.strip())
```

Or:

```python
with log_file.open("r", encoding="utf-8") as file:

    for line in file:

        if "timeout" in line.lower():
            print(line.strip())
```

This is useful when log capitalization is inconsistent.

---

# 12. Counting Errors Without Storing Them

Avoid:

```python
errors = []

with log_file.open("r", encoding="utf-8") as file:

    for line in file:

        if "ERROR" in line:
            errors.append(line)
```

if the file may contain millions of matching lines and you only need the count.

Instead:

```python
error_count = 0

with log_file.open("r", encoding="utf-8") as file:

    for line in file:

        if "ERROR" in line:
            error_count += 1
```

This keeps memory usage small.

---

# 13. Streaming vs Collecting

Consider two requirements.

### Requirement A

> Count the number of failures.

Use:

```python
failed_count = 0
```

and increment it.

### Requirement B

> Produce a report containing every failed test ID.

Then storing the IDs may be necessary:

```python
failed_tests = []
```

The important principle is:

> **Store only the information the automation actually needs.**

---

# 14. Processing and Writing Simultaneously

A large input file can be processed while generating a smaller output file.

Example:

```python
from pathlib import Path

input_file = Path("large.log")
output_file = Path("errors.log")

with (
    input_file.open("r", encoding="utf-8") as source,
    output_file.open("w", encoding="utf-8") as destination
):

    for line in source:

        if "ERROR" in line:
            destination.write(line)
```

Conceptually:

```text
large.log
   ↓
read line
   ↓
check ERROR
   ↓
write matching line
   ↓
next line
```

This avoids loading the large input into memory.

---

# 15. Generating a Summary from a Large File

Suppose a large test log contains:

```text
INFO Test started
PASS TEST_001
PASS TEST_002
FAIL TEST_003
ERROR Controller timeout
PASS TEST_004
```

We can produce a summary:

```python
from pathlib import Path

log_file = Path("test.log")

total = 0
passed = 0
failed = 0
errors = 0

with log_file.open("r", encoding="utf-8") as file:

    for line in file:

        if "PASS" in line:
            passed += 1

        elif "FAIL" in line:
            failed += 1

        if "ERROR" in line:
            errors += 1

        total += 1

print("Total lines:", total)
print("Passed:", passed)
print("Failed:", failed)
print("Errors:", errors)
```

This demonstrates a core automation principle:

```text
Large input
    ↓
Streaming processing
    ↓
Small summary state
```

---

# 16. Reading in Chunks

Line-by-line processing is excellent for text logs.

Sometimes you need to process binary data or fixed-size blocks.

Python supports:

```python
file.read(size)
```

Example:

```python
with open("large.bin", "rb") as file:

    while True:

        chunk = file.read(4096)

        if not chunk:
            break

        process(chunk)
```

Here:

```python
4096
```

means approximately 4 KiB of data per read.

---

# 17. Chunk Processing Concept

Instead of:

```text
10 GB file
     ↓
RAM
```

we process:

```text
10 GB file
     ↓
4 KB chunk
     ↓
process
     ↓
next 4 KB
     ↓
process
     ↓
...
```

This is especially relevant when dealing with binary storage data.

---

# 18. Text Lines vs Binary Chunks

Different workloads may require different strategies.

### Text logs

Prefer:

```python
for line in file:
    ...
```

### Binary data

Often use:

```python
chunk = file.read(4096)
```

or another appropriate chunk size.

Therefore:

```text
Text log → line-oriented processing
Binary data → chunk-oriented processing
```

---

# 19. Processing Large Files with `pathlib`

The same approach works with `Path.open()`:

```python
from pathlib import Path

log_file = Path("large.log")

with log_file.open("r", encoding="utf-8") as file:

    for line in file:
        if "ERROR" in line:
            print(line.strip())
```

This is consistent with the `pathlib` approach used throughout this module.

---

# 20. Large File Processing with Regex

The regular-expression knowledge from Module 6 can be combined with file processing.

Example:

```python
import re
from pathlib import Path

pattern = re.compile(r"ERROR\s+\w+")

log_file = Path("controller.log")

with log_file.open("r", encoding="utf-8") as file:

    for line in file:

        if pattern.search(line):
            print(line.strip())
```

The file is still processed line-by-line.

There is no requirement to load the entire log into memory before applying the regex.

---

# 21. Large File Processing with CSV

Large CSV files should also be processed incrementally when possible.

Example:

```python
import csv
from pathlib import Path

csv_file = Path("results.csv")

with csv_file.open(
    "r",
    encoding="utf-8",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        if row["status"] == "FAIL":
            print(row["test_id"])
```

The CSV reader provides records incrementally.

This is useful for large test-result datasets.

---

# 22. Large JSON Files — Important Consideration

Standard:

```python
json.load(file)
```

normally loads the JSON document into Python objects.

For a very large JSON document, this can require substantial memory.

Therefore, do not automatically assume:

```python
json.load()
```

is appropriate for arbitrarily large JSON data.

Large JSON processing may require a streaming-oriented format or parser depending on the data structure.

For ordinary configuration files, however, `json.load()` is usually perfectly reasonable.

---

# 23. Large File Processing and Memory Complexity

Suppose a file has:

```text
N lines
```

If we load the entire file:

```python
data = file.read()
```

memory usage can grow approximately with the size of the input.

With streaming:

```python
for line in file:
    ...
```

the amount of state maintained by the processing logic can remain approximately constant, assuming we don't accumulate results.

Conceptually:

```text
Entire-file approach:
Memory ≈ O(file size)

Streaming approach:
Memory ≈ O(processing state)
```

The exact runtime and buffering behavior depends on the implementation and workload, but the architectural distinction is important.

---

# 24. Large File Processing and Time Complexity

If we need to inspect every line:

```python
for line in file:
    ...
```

and the file contains `N` lines, we generally need to examine those `N` lines.

Therefore:

```text
Time ≈ O(N)
```

The key optimization is often not reducing the number of lines that must be inspected, but avoiding unnecessary memory consumption and unnecessary work per line.

---

# 25. Avoid Repeated Expensive Operations

Suppose:

```python
for line in file:

    if "ERROR" in line.upper():
        ...
```

The conversion occurs for every line.

Sometimes that's perfectly acceptable.

But if several checks need the normalized form:

```python
for line in file:

    normalized = line.upper()

    if "ERROR" in normalized:
        ...

    if "TIMEOUT" in normalized:
        ...
```

Now the normalization happens once per line.

The general principle:

> **Avoid repeating expensive processing unnecessarily inside large-file loops.**

---

# 26. Large File Processing and Output

If the input is huge but the output is also potentially huge, avoid accumulating the entire output.

Avoid:

```python
matching_lines = []

for line in file:

    if "ERROR" in line:
        matching_lines.append(line)
```

followed later by:

```python
output.write("".join(matching_lines))
```

Instead, write matches as they are found:

```python
for line in file:

    if "ERROR" in line:
        output.write(line)
```

This maintains the streaming model:

```text
Read
 ↓
Process
 ↓
Write
 ↓
Discard
```

---

# 27. Example: Generate Failure Report

```python
from pathlib import Path

input_file = Path("test_results.log")
report_file = Path("failure_report.txt")

failure_count = 0

with (
    input_file.open("r", encoding="utf-8") as source,
    report_file.open("w", encoding="utf-8") as report
):

    for line in source:

        if "FAIL" in line:

            failure_count += 1
            report.write(line)

    report.write(
        f"\nTotal failures: {failure_count}\n"
    )
```

This can process a large input without storing every failure in memory.

---

# 28. Handling Empty Files

An empty file is valid.

Example:

```python
with log_file.open("r", encoding="utf-8") as file:

    for line in file:
        ...
```

The loop simply performs zero iterations.

If the automation requires content, explicitly validate:

```python
if log_file.stat().st_size == 0:
    raise RuntimeError("Log file is empty")
```

The correct behavior depends on the test requirement.

---

# 29. Handling Encoding Problems

A large text file may not use UTF-8.

For example:

```python
with log_file.open(
    "r",
    encoding="utf-8"
) as file:
    ...
```

may fail with a decoding error if the file uses another encoding.

Possible approaches include:

* Determine the expected encoding
* Use the correct encoding explicitly
* Handle decoding errors when appropriate

Do not blindly ignore encoding errors because doing so can silently corrupt diagnostic information.

---

# 30. Handling Files That Change During Processing

Logs may still be written by another process.

Example:

```text
Test process
     │
     ├── writes controller.log
     │
     └── Python analyzer reads controller.log
```

The file can change while the automation is processing it.

This can create questions such as:

* Has the writer finished?
* Is the file complete?
* Could lines be appended during processing?
* Should the automation wait for the test to finish?
* Is a stable snapshot required?

For post-test analysis, a good design is often:

```text
Test completes
    ↓
File becomes stable
    ↓
Analyzer starts
```

rather than analyzing an actively changing file unless live monitoring is specifically required.

---

# 31. Large Files and Storage Testing

Large-file processing is particularly important in storage engineering because long-running tests can generate enormous logs.

For example:

```text
24-hour stress test
        ↓
Controller logs
Kernel logs
I/O logs
Performance logs
Error logs
        ↓
Several GB of data
```

A Python analyzer should not assume that:

```python
file.read()
```

is always safe.

Instead:

```python
for line in file:
    ...
```

allows the automation to process the data incrementally.

---

# 32. Practical Storage Log Analyzer

Example:

```python
from pathlib import Path

log_file = Path("storage_test.log")

errors = 0
timeouts = 0
failures = 0

with log_file.open("r", encoding="utf-8") as file:

    for line in file:

        normalized = line.upper()

        if "ERROR" in normalized:
            errors += 1

        if "TIMEOUT" in normalized:
            timeouts += 1

        if "FAIL" in normalized:
            failures += 1

print("Errors  :", errors)
print("Timeouts:", timeouts)
print("Failures:", failures)
```

The script maintains only three counters regardless of whether the log contains:

```text
1,000 lines
```

or:

```text
10 million lines
```

---

# 33. Combining Traversal + Large File Processing

The previous topic taught:

```python
root.rglob("*.log")
```

This topic teaches:

```python
for line in file:
```

Together:

```python
from pathlib import Path

root = Path("test_runs")

for log_file in root.rglob("*.log"):

    with log_file.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            if "ERROR" in line:
                print(
                    log_file,
                    line.strip()
                )
```

This is a powerful storage automation pattern:

```text
Directory tree
      ↓
Find every log
      ↓
Open one log
      ↓
Process line-by-line
      ↓
Find errors
      ↓
Next log
```

---

# 34. Common Mistakes

### Mistake 1 — Using `read()` on huge files

```python
data = file.read()
```

Potentially consumes large amounts of memory.

Prefer:

```python
for line in file:
    ...
```

---

### Mistake 2 — Using `readlines()` unnecessarily

```python
lines = file.readlines()
```

creates a list of all lines.

For large files, prefer direct iteration.

---

### Mistake 3 — Accumulating everything

```python
results = []

for line in file:
    results.append(line)
```

This defeats the memory advantage of streaming.

Store only what you actually need.

---

### Mistake 4 — Loading large output into memory

Instead of:

```python
output_lines = []
```

and accumulating potentially millions of lines, write results incrementally when appropriate.

---

### Mistake 5 — Forgetting binary data

Do not assume every large file is text.

Binary storage data should generally be opened with:

```python
open("data.bin", "rb")
```

and processed appropriately.

---

# 35. Interview Questions

### Q1. How do you efficiently process a large text file?

Use line-by-line iteration:

```python
with open("large.log", "r", encoding="utf-8") as file:
    for line in file:
        process(line)
```

---

### Q2. Why is `read()` potentially problematic for large files?

Because it attempts to load the entire file contents into memory.

---

### Q3. Why is `readlines()` potentially problematic?

It creates a list containing all lines, which can consume substantial memory.

---

### Q4. What is the preferred approach for large log files?

```python
for line in file:
    ...
```

Process each line incrementally.

---

### Q5. How would you process a large binary file?

Read it in chunks:

```python
with open("large.bin", "rb") as file:

    while True:

        chunk = file.read(4096)

        if not chunk:
            break

        process(chunk)
```

---

### Q6. What is the difference between streaming and loading the whole file?

Streaming processes data incrementally, while loading the whole file stores the complete content in memory.

---

### Q7. How can you process a large log and create a smaller report?

Read the log line-by-line and write matching/summary information directly to the report.

---

### Q8. Why is large-file processing important in storage automation?

Storage tests can generate very large logs and result files. Efficient processing prevents unnecessary memory consumption and allows automation to scale to long-running tests.

---

# 36. Key Takeaways

### Preferred pattern for large text files

```python
with file.open("r", encoding="utf-8") as file:

    for line in file:
        process(line)
```

### Avoid unnecessarily

```python
file.read()
```

and:

```python
file.readlines()
```

for very large files.

### Large binary files

```python
with file.open("rb") as file:

    while True:

        chunk = file.read(4096)

        if not chunk:
            break

        process(chunk)
```

### Large-file architecture

```text
Read incrementally
       ↓
Process
       ↓
Store only required state
       ↓
Write results incrementally
```

---

# 37. Automation Principle

> **Never load a large file into memory unless the problem genuinely requires the entire file in memory.**

For storage automation, the preferred architecture is:

```text
Directory traversal
        ↓
Find relevant file
        ↓
Open file
        ↓
Stream data
        ↓
Process
        ↓
Generate result
        ↓
Continue
```

This allows a Python automation framework to handle large logs and long-running storage tests without unnecessarily consuming system memory.

**Next file:** `13_File_Comparison.md`

