# `13_File_Comparison.md`

# File Comparison

## 1. Introduction

File comparison is the process of determining whether two files are:

* Identical
* Different
* Partially different
* Different in specific lines or sections

This is highly useful in storage test automation.

For example, an automation framework may need to compare:

```text
Expected result
        vs
Actual result
```

or:

```text
Baseline configuration
        vs
Current configuration
```

or:

```text
Before test
        vs
After test
```

Python provides several approaches for comparison.

The appropriate method depends on **what exactly you want to compare**.

---

# 2. Types of File Comparison

There are several common levels of comparison:

```text
Level 1 → Exact content comparison
Level 2 → Line-by-line comparison
Level 3 → Human-readable difference report
Level 4 → Structured-data comparison
```

For this topic, we will primarily focus on text-file comparison using Python.

---

# 3. Exact File Content Comparison

The simplest approach is to read both files and compare their contents.

Example:

```python
from pathlib import Path

file1 = Path("expected.txt")
file2 = Path("actual.txt")

with file1.open("r", encoding="utf-8") as f:
    content1 = f.read()

with file2.open("r", encoding="utf-8") as f:
    content2 = f.read()

if content1 == content2:
    print("Files are identical")
else:
    print("Files are different")
```

The comparison:

```python
content1 == content2
```

checks whether the two strings contain exactly the same content.

---

# 4. What Does "Identical" Mean?

Consider:

### File A

```text
TEST_001 PASS
TEST_002 PASS
```

### File B

```text
TEST_001 PASS
TEST_002 PASS
```

The contents are identical.

Therefore:

```python
content1 == content2
```

returns:

```text
True
```

---

# 5. Whitespace Matters

Consider:

### File A

```text
TEST_001 PASS
```

### File B

```text
TEST_001 PASS 
```

The second file contains an additional trailing space.

Therefore, an exact comparison may report:

```text
Different
```

Similarly:

```text
TEST_001 PASS
```

and:

```text
TEST_001  PASS
```

are different strings because the spacing differs.

This is important in test automation.

---

# 6. Newline Differences

Consider:

### File A

```text
TEST_001 PASS
TEST_002 PASS
```

and File B containing different newline conventions.

Depending on how the files are opened and processed, newline representation can affect comparisons.

For exact comparison, you should understand whether you care about:

* Actual byte-level content
* Logical text content
* Line structure

---

# 7. Text Comparison vs Binary Comparison

There are two fundamentally different approaches.

### Text comparison

```python
with open("file.txt", "r", encoding="utf-8") as file:
    ...
```

Useful when comparing:

* Logs
* Reports
* Configuration files
* Test results

### Binary comparison

```python
with open("file.bin", "rb") as file:
    ...
```

Useful when comparing:

* Binary test artifacts
* Raw storage data
* Firmware images
* Binary dumps

Do not assume that every file should be treated as text.

---

# 8. Line-by-Line Comparison

Sometimes we want to know **which lines differ**.

Python's standard library provides:

```python
difflib
```

Import:

```python
import difflib
```

A simple example:

```python
from pathlib import Path
import difflib

file1 = Path("expected.txt")
file2 = Path("actual.txt")

with file1.open("r", encoding="utf-8") as f:
    expected = f.readlines()

with file2.open("r", encoding="utf-8") as f:
    actual = f.readlines()

diff = difflib.unified_diff(
    expected,
    actual,
    fromfile="expected.txt",
    tofile="actual.txt"
)

for line in diff:
    print(line, end="")
```

This generates a human-readable unified diff.

---

# 9. Understanding `unified_diff()`

The function:

```python
difflib.unified_diff()
```

compares sequences.

In our case:

```python
expected
```

and:

```python
actual
```

are lists of lines.

It does **not** itself read files.

We read the files first:

```python
expected = f.readlines()
actual = f.readlines()
```

and then give those sequences to `difflib`.

This distinction is important.

---

# 10. Example Unified Diff

Suppose expected:

```text
TEST_001 PASS
TEST_002 PASS
TEST_003 PASS
```

Actual:

```text
TEST_001 PASS
TEST_002 FAIL
TEST_003 PASS
```

The unified diff may look like:

```text
--- expected.txt
+++ actual.txt
@@ ...
 TEST_001 PASS
-TEST_002 PASS
+TEST_002 FAIL
 TEST_003 PASS
```

The symbols are important.

---

# 11. Meaning of `-`

A line beginning with:

```text
-
```

represents content from the first sequence that is absent or changed relative to the second sequence.

Example:

```text
-TEST_002 PASS
```

means the expected version contains:

```text
TEST_002 PASS
```

but that line differs in the actual version.

---

# 12. Meaning of `+`

A line beginning with:

```text
+
```

represents content present in the second sequence.

Example:

```text
+TEST_002 FAIL
```

means the actual version contains:

```text
TEST_002 FAIL
```

---

# 13. Meaning of a Space

A line beginning with a space in unified diff output generally represents an unchanged context line.

Example:

```text
 TEST_001 PASS
```

means that line is present in both sequences in that context.

So:

```text
 TEST_001 PASS
-TEST_002 PASS
+TEST_002 FAIL
 TEST_003 PASS
```

can be read as:

```text
TEST_001 → unchanged
TEST_002 → changed
TEST_003 → unchanged
```

---

# 14. The `@@` Section

You may see:

```text
@@ -1,3 +1,3 @@
```

This is called a **hunk header**.

It describes where the changed section occurs in the two sequences.

You do not normally need to memorize every detail of the hunk format for everyday automation, but you should recognize it when reading a diff.

---

# 15. Why Diff Reports Are Better Than Boolean Comparison

Consider:

```python
if expected == actual:
    print("PASS")
else:
    print("FAIL")
```

This tells us only:

```text
Files are different.
```

But a test engineer often needs to know:

> **What changed?**

A diff gives:

```text
Expected:
TEST_002 PASS

Actual:
TEST_002 FAIL
```

That information is much more useful for troubleshooting.

---

# 16. File Comparison in Test Automation

A very common pattern is:

```text
Test execution
      ↓
Generate actual result
      ↓
Load expected result
      ↓
Compare
      ↓
PASS / FAIL
      ↓
Generate difference report
```

For example:

```text
expected_result.txt
actual_result.txt
```

The automation compares them.

---

# 17. Example: Expected vs Actual

Expected:

```text
DEVICE: device_01
STATUS: ONLINE
SECTORS: 100000
```

Actual:

```text
DEVICE: device_01
STATUS: ONLINE
SECTORS: 99999
```

Exact comparison:

```python
expected == actual
```

returns:

```text
False
```

A diff provides:

```text
 DEVICE: device_01
 STATUS: ONLINE
-SECTORS: 100000
+SECTORS: 99999
```

Now the engineer immediately knows the mismatch.

---

# 18. Creating a Reusable Comparison Function

We can encapsulate the logic:

```python
from pathlib import Path
import difflib

def compare_files(expected_path, actual_path):

    expected_path = Path(expected_path)
    actual_path = Path(actual_path)

    with expected_path.open("r", encoding="utf-8") as file:
        expected = file.readlines()

    with actual_path.open("r", encoding="utf-8") as file:
        actual = file.readlines()

    return list(
        difflib.unified_diff(
            expected,
            actual,
            fromfile=str(expected_path),
            tofile=str(actual_path)
        )
    )
```

Then:

```python
diff = compare_files(
    "expected.txt",
    "actual.txt"
)

for line in diff:
    print(line, end="")
```

---

# 19. Returning a Boolean and Diff

A more useful automation function can return both:

```python
from pathlib import Path
import difflib

def compare_files(expected_path, actual_path):

    expected_path = Path(expected_path)
    actual_path = Path(actual_path)

    with expected_path.open("r", encoding="utf-8") as file:
        expected = file.readlines()

    with actual_path.open("r", encoding="utf-8") as file:
        actual = file.readlines()

    diff = list(
        difflib.unified_diff(
            expected,
            actual,
            fromfile=str(expected_path),
            tofile=str(actual_path)
        )
    )

    return expected == actual, diff
```

Usage:

```python
same, diff = compare_files(
    "expected.txt",
    "actual.txt"
)

if same:
    print("PASS")
else:
    print("FAIL")

    for line in diff:
        print(line, end="")
```

This is a practical test-automation pattern.

---

# 20. Comparing Large Files

There is an important limitation in the previous approach.

This:

```python
expected = file.readlines()
actual = file.readlines()
```

loads both files into memory.

That may be perfectly acceptable for small test-result files.

But for very large files, it can consume substantial memory.

Therefore, always consider the size of the files being compared.

---

# 21. Small Files vs Large Files

### Small result files

Using:

```python
readlines()
```

and:

```python
difflib.unified_diff()
```

may be perfectly reasonable.

### Very large logs

You may need a more memory-conscious comparison strategy.

For example:

```text
Streaming comparison
Chunk comparison
Hash comparison
External diff tools
```

depending on the exact requirement.

---

# 22. Comparing File Sizes

Before reading two files, you can inspect their sizes:

```python
from pathlib import Path

file1 = Path("expected.bin")
file2 = Path("actual.bin")

size1 = file1.stat().st_size
size2 = file2.stat().st_size

print(size1)
print(size2)
```

If:

```python
size1 != size2
```

the files cannot be byte-for-byte identical.

Example:

```python
if size1 != size2:
    print("Files have different sizes")
```

This can be a useful early check.

---

# 23. File Size Is Not Enough

Two files can have the same size but different contents.

Example:

```text
File A:
AAAA

File B:
BBBB
```

Both contain four characters.

Therefore:

```python
size1 == size2
```

does **not** mean:

```text
contents are identical
```

File size can eliminate some comparisons quickly, but it cannot prove equality.

---

# 24. Hash-Based Comparison

For large files, cryptographic hashes can be useful.

For example:

```python
import hashlib

def file_hash(path):

    hash_object = hashlib.sha256()

    with open(path, "rb") as file:

        for chunk in iter(
            lambda: file.read(4096),
            b""
        ):
            hash_object.update(chunk)

    return hash_object.hexdigest()
```

Then:

```python
hash1 = file_hash("expected.bin")
hash2 = file_hash("actual.bin")

if hash1 == hash2:
    print("Files have matching SHA-256 hashes")
else:
    print("Files differ")
```

The important part is that the files are processed in chunks.

---

# 25. Why Hashing Is Useful

Suppose two binary files are:

```text
5 GB each
```

We do not necessarily want to load both completely into memory.

Instead:

```text
File
 ↓
Chunk
 ↓
Hash
 ↓
Next chunk
 ↓
Hash
 ↓
...
```

At the end, compare the resulting hashes.

This provides an efficient way to determine whether the file contents match with the properties of the selected hash algorithm.

---

# 26. Hash Equality and Absolute Guarantees

For practical engineering purposes, matching cryptographic hashes are commonly treated as evidence that files match.

However, mathematically, a hash function can have collisions.

Therefore:

```text
same hash
```

is not the same theoretical statement as:

```text
every byte proven identical
```

For most integrity and automation workflows, a strong cryptographic hash such as SHA-256 is widely useful.

If absolute byte-for-byte verification is required, direct byte comparison is the definitive comparison method.

---

# 27. Binary Comparison in Chunks

For direct byte comparison, files can be processed incrementally.

Example:

```python
def files_are_identical(path1, path2):

    with open(path1, "rb") as file1, \
         open(path2, "rb") as file2:

        while True:

            chunk1 = file1.read(4096)
            chunk2 = file2.read(4096)

            if chunk1 != chunk2:
                return False

            if not chunk1:
                return True
```

The algorithm:

```text
Read chunk from file 1
        ↓
Read chunk from file 2
        ↓
Compare
        ↓
Different → False
        ↓
Both EOF → True
```

This avoids loading the entire files into memory.

---

# 28. Text Comparison and Normalization

Sometimes two files may be logically equivalent but differ in formatting.

For example:

```text
File A:
TEST_001 PASS
```

and:

```text
File B:
TEST_001 PASS   
```

If trailing spaces are irrelevant to the test requirement, we can normalize the lines.

Example:

```python
def normalized_lines(path):

    with open(path, "r", encoding="utf-8") as file:

        for line in file:
            yield line.strip()
```

Then comparison can be performed on normalized content.

But this should be done **only when the test specification says whitespace differences are irrelevant**.

Do not normalize blindly.

---

# 29. Why Blind Normalization Is Dangerous

Suppose the expected output is:

```text
BLOCK_SIZE=4096
```

and actual output is:

```text
BLOCK_SIZE=4096 
```

Maybe the trailing space is irrelevant.

But suppose the file contains:

```text
COMMAND=echo "hello "
```

Here whitespace could be meaningful.

Therefore:

> **Normalization must be driven by the comparison requirement, not convenience.**

---

# 30. Comparing Structured Data

Text comparison is not always the best comparison method.

Suppose two JSON files contain the same data but different formatting.

File A:

```json
{
    "device": "device_01",
    "status": "ONLINE"
}
```

File B:

```json
{"status":"ONLINE","device":"device_01"}
```

Raw text comparison says:

```text
Different
```

But logically, the JSON objects contain the same information.

In such cases, parse the JSON first:

```python
import json

with open("expected.json", "r", encoding="utf-8") as file:
    expected = json.load(file)

with open("actual.json", "r", encoding="utf-8") as file:
    actual = json.load(file)

if expected == actual:
    print("Equivalent JSON data")
```

This is an important distinction:

```text
Text equality
        vs
Data equality
```

---

# 31. Choosing the Right Comparison

Use the comparison method according to the requirement.

| Requirement                         | Approach                       |
| ----------------------------------- | ------------------------------ |
| Exact small text files              | `read()` + `==`                |
| Human-readable text differences     | `difflib.unified_diff()`       |
| Large binary files                  | Chunk comparison               |
| Large-file integrity/equality check | Hash comparison                |
| JSON logical equality               | Parse with `json` then compare |
| Whitespace-insensitive comparison   | Explicit normalization         |
| CSV logical comparison              | Parse records and compare      |

---

# 32. Example: Storage Configuration Comparison

Suppose:

```text
baseline.conf
current.conf
```

contain storage configuration.

The automation can compare them:

```python
from pathlib import Path
import difflib

baseline = Path("baseline.conf")
current = Path("current.conf")

with baseline.open("r", encoding="utf-8") as file:
    expected = file.readlines()

with current.open("r", encoding="utf-8") as file:
    actual = file.readlines()

diff = list(
    difflib.unified_diff(
        expected,
        actual,
        fromfile="baseline.conf",
        tofile="current.conf"
    )
)

if diff:
    print("Configuration mismatch detected.")

    for line in diff:
        print(line, end="")
else:
    print("Configuration matches baseline.")
```

This can help identify unexpected configuration changes.

---

# 33. Example: Storage Test Expected vs Actual

Suppose a test requires:

```text
Expected:
DEVICE device_01 ONLINE
QUEUE_DEPTH 32
BLOCK_SIZE 4096
```

Actual:

```text
DEVICE device_01 ONLINE
QUEUE_DEPTH 16
BLOCK_SIZE 4096
```

The comparison should identify:

```text
-QUEUE_DEPTH 32
+QUEUE_DEPTH 16
```

The automation can then classify:

```text
Test: FAIL
Reason: Queue depth mismatch
```

This is much more useful than simply:

```text
Files differ
```

---

# 34. File Comparison Workflow

A production-style comparison workflow might be:

```text
Receive expected file
        ↓
Receive actual file
        ↓
Validate both paths
        ↓
Check file types
        ↓
Choose comparison strategy
        ↓
Compare
        ↓
If mismatch:
    Generate diff
        ↓
Report failure
```

---

# 35. Common Mistakes

### Mistake 1 — Comparing filenames

```python
if file1.name == file2.name:
    print("Same")
```

This only compares filenames.

It says nothing about file contents.

---

### Mistake 2 — Comparing file sizes only

```python
if file1.stat().st_size == file2.stat().st_size:
    print("Same")
```

Equal size does not guarantee equal content.

---

### Mistake 3 — Loading huge files unnecessarily

```python
data1 = file1.read()
data2 = file2.read()
```

This can consume significant memory.

Use streaming/chunk processing when files are large.

---

### Mistake 4 — Blind normalization

```python
line.strip()
```

may remove whitespace that is actually meaningful.

Normalize only when the test requirement allows it.

---

### Mistake 5 — Using text comparison for binary files

Binary data should generally be opened using:

```python
"rb"
```

rather than assuming UTF-8 text.

---

# 36. Interview Questions

### Q1. How do you compare two text files in Python?

For small files:

```python
content1 == content2
```

For a human-readable difference report:

```python
difflib.unified_diff()
```

---

### Q2. What is `difflib`?

`difflib` is a Python standard-library module that provides tools for comparing sequences, including generating human-readable differences.

---

### Q3. Does `difflib` read files directly?

No.

You normally read the files first and provide their sequences, such as lists of lines, to `difflib`.

---

### Q4. What does `-` mean in a unified diff?

It indicates content from the first sequence that differs from or is absent in the second sequence.

---

### Q5. What does `+` mean?

It indicates content from the second sequence.

---

### Q6. Why isn't file size enough to compare files?

Two different files can have the same size.

---

### Q7. How would you compare very large binary files without loading them entirely into memory?

Read both files in chunks and compare corresponding chunks.

---

### Q8. When would you use hashing?

When you need an efficient integrity/equality check for potentially large files without storing the entire files in memory.

---

### Q9. When should you parse a file instead of doing raw text comparison?

When the logical data matters more than formatting—for example, comparing JSON objects regardless of whitespace or key ordering.

---

# 37. Key Takeaways

### Exact comparison

```python
content1 == content2
```

### Human-readable diff

```python
difflib.unified_diff(
    expected,
    actual
)
```

### Large binary comparison

```python
with open(path1, "rb") as file1, \
     open(path2, "rb") as file2:

    # compare chunks
```

### Hash comparison

```python
hashlib.sha256()
```

### Structured data comparison

```python
expected = json.load(file)
actual = json.load(file)

expected == actual
```

The most important decision is:

> **Choose the comparison method based on what "same" actually means for the test.**

---

# 38. Automation Principle

> **A good test comparison does not merely detect that two files differ—it provides enough information to explain the difference.**

Think:

```text
Expected
   ↓
Actual
   ↓
Comparison
   ↓
Difference
   ↓
Diagnosis
   ↓
Test result
```

For storage automation, this distinction is critical.

A result such as:

```text
FAIL
```

is useful.

But:

```text
FAIL
QUEUE_DEPTH expected=32 actual=16
```

is far more valuable for troubleshooting and debugging.

**Next file:** `14_JSON.md`

