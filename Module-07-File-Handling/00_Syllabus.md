# Module 07 — File Handling

## Objective

Learn Python file handling from fundamentals through practical automation patterns.

The goal of this module is to develop the ability to:

- Create, read, write, append, and manage files.
- Work safely with files using context managers.
- Navigate and manipulate filesystem paths using `pathlib`.
- Create and traverse directories.
- Perform file operations such as rename, copy, move, and delete.
- Process large files efficiently.
- Compare file contents and identify differences.
- Work with structured data formats such as JSON, CSV, and YAML.
- Select the appropriate file format for an automation requirement.
- Build practical file-based automation workflows.
- Diagnose and troubleshoot common file and filesystem problems.

---

# Module Structure

## 7.1 — File Fundamentals

### Topics
- What is a file?
- Files and persistent data
- File objects
- `open()`
- Basic file handling workflow
- Text files vs binary files
- File resource management

---

## 7.2 — File Modes

### Topics
- `r` — Read
- `w` — Write
- `a` — Append
- `x` — Exclusive creation
- Default mode
- File creation behavior
- File truncation behavior
- Read/write permissions
- Encoding
- Common file-mode mistakes

---

## 7.3 — Reading Files

### Topics
- `read()`
- `readline()`
- `readlines()`
- Iterating over a file
- Reading line-by-line
- Newline handling
- `strip()`
- Memory considerations
- Processing text files

---

## 7.4 — File Position

### Topics
- File cursor / position
- `tell()`
- `seek()`
- Moving the file position
- Reading from specific positions
- Resetting to the beginning
- Understanding sequential file access

---

## 7.5 — Writing Files

### Topics
- `write()`
- Writing strings
- Newline handling
- Writing multiple records
- `writelines()`
- Return value of `write()`
- Writing formatted data
- Common writing mistakes

---

## 7.6 — Appending and `writelines()`

### Topics
- Append mode
- Preserving existing content
- Appending records
- Newline considerations
- `writelines()`
- Difference between `write()` and `writelines()`

---

## 7.7 — Context Managers

### Topics
- `with`
- Resource management
- Automatic file closure
- `__enter__`
- `__exit__`
- Exception-safe cleanup
- Why context managers are preferred
- Resource lifetime vs object lifetime

---

## 7.8 — `pathlib`

### Topics
- Why path handling matters
- Relative paths
- Absolute paths
- `Path`
- `Path.cwd()`
- `exists()`
- `is_file()`
- `is_dir()`
- `resolve()`
- Path joining with `/`
- `.name`
- `.parent`
- `.stem`
- `.suffix`
- `Path.open()`
- Dynamic path construction

---

## 7.9 — Directory Handling

### Topics
- Directory paths
- `mkdir()`
- `parents=True`
- `exist_ok=True`
- Creating nested directories
- Checking directory existence
- File vs directory distinction

---

## 7.10 — Directory Traversal

### Topics
- `Path.iterdir()`
- Listing directory contents
- Files vs directories
- Direct-level traversal
- Recursive vs non-recursive traversal

---

## 7.11 — File Operations

### Topics
- `Path.rename()`
- `Path.unlink()`
- `shutil.copy2()`
- `shutil.move()`
- Rename vs copy vs move
- Safe deletion
- File operation validation

---

## 7.12 — Large File Processing

### Topics
- Memory considerations
- Why `read()` can be problematic for huge files
- Line-by-line processing
- Incremental processing
- Processing large logs
- Counting and filtering records efficiently

---

## 7.13 — File Comparison

### Topics
- Comparing file contents
- `difflib`
- `unified_diff()`
- Expected vs actual files
- Understanding diff output
- Changed vs unchanged lines
- Practical validation use cases

---

## 7.14 — JSON File Handling

### Topics
- JSON fundamentals
- JSON objects and arrays
- JSON ↔ Python mappings
- `json.load()`
- `json.loads()`
- `json.dump()`
- `json.dumps()`
- Pretty formatting with `indent`
- Nested JSON
- JSON validation
- `JSONDecodeError`
- Missing keys
- `.get()`
- Practical automation use cases

---

## 7.15 — CSV File Handling

### Topics
- CSV fundamentals
- Tabular data
- `csv.reader()`
- `csv.DictReader()`
- `csv.writer()`
- `csv.DictWriter()`
- `writerow()`
- `writerows()`
- `writeheader()`
- CSV values as strings
- Numeric conversion
- `newline=""`
- Practical test-result reporting

---

## 7.16 — YAML File Handling

### Topics
- YAML fundamentals
- YAML configuration files
- YAML ↔ Python mappings
- PyYAML
- `yaml.safe_load()`
- `yaml.safe_dump()`
- Nested YAML
- YAML lists
- YAML indentation
- Configuration management
- Automation use cases

---

## 7.17 — Choosing File Formats

### Topics
- TXT vs CSV vs JSON vs YAML
- Plain text data
- Tabular data
- Structured data
- Configuration data
- Machine-readable vs human-readable formats
- Selecting formats based on requirements

---

## 7.18 — File Handling Automation Pattern

### Topics
- Input → Parse → Process → Report
- Reading test results
- Parsing test records
- Calculating test statistics
- Identifying failures
- Generating reports
- Combining multiple file-handling concepts
- Practical automation workflow

---

## 7.19 — Troubleshooting and Edge Cases

### Topics
- `FileNotFoundError`
- Invalid paths
- Directory vs file errors
- Permission problems
- Encoding problems
- Empty files
- Malformed structured data
- Invalid JSON/YAML
- Unexpected file contents
- Files modified during processing
- Large-file considerations
- Safe deletion and movement
- Defensive validation
- Root-cause analysis for file failures

---

## 7.20 — Interview Questions

### Topics
- File handling fundamentals
- File modes
- Reading and writing
- Context managers
- `pathlib`
- Directory traversal
- File operations
- Large-file processing
- JSON
- CSV
- YAML
- Troubleshooting scenarios
- Automation-oriented interview questions

---

# Final Revision

## File Handling Quick Revision

A concise revision reference covering:

- Core APIs
- Important syntax
- File modes
- Reading/writing patterns
- `pathlib`
- JSON
- CSV
- YAML
- Common troubleshooting points

---

# Final Cheat Sheet

## File Handling Cheat Sheet

A compact reference containing:

- Important functions and methods
- Common syntax
- Common exceptions
- Format selection guide
- Automation patterns
- Interview reminders

---

# Module Completion Criteria

By the end of Module 07, the learner should be able to:

1. Work confidently with text files.
2. Select appropriate file modes.
3. Read files efficiently.
4. Write and append structured results.
5. Use context managers correctly.
6. Manipulate filesystem paths using `pathlib`.
7. Create and traverse directories.
8. Rename, copy, move, and delete files safely.
9. Process large files incrementally.
10. Compare expected and actual files.
11. Read and write JSON.
12. Read and write CSV.
13. Read and write YAML.
14. Select an appropriate file format.
15. Build a practical file-based automation workflow.
16. Diagnose common filesystem and parsing failures.
17. Explain file-handling concepts clearly in technical interviews.

---

# Primary Engineering Principle

> **Locate → Validate → Open Safely → Read/Write → Parse → Process → Report → Handle Failures**

File handling in automation is not simply about reading and writing files.

It is about reliably moving data between the filesystem and an automation system while maintaining correctness, efficiency, traceability, and safe failure behavior.
