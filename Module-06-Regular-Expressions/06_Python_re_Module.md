# Chapter 06 — Python re Module

## Chapter Objective

Until now, we have learned the theory behind Regular Expressions:

- Character Classes
- Quantifiers
- Groups
- Lookarounds

However, Regular Expressions become useful only when they are applied inside programs.

Python provides the built-in **`re` module** for working with Regular Expressions.

This module allows Python programs to:

- Search text
- Find multiple matches
- Extract information
- Validate input
- Replace text
- Split text
- Iterate through matches

Throughout this chapter, we will learn how Python's `re` module executes Regular Expressions and how it is used in Storage Engineering, Linux Automation and Test Automation.

---

# Topics Covered

1. Why Python's re Module?
2. What is the re Module?
3. Importing the re Module
4. re.search()
5. re.match()
6. re.fullmatch()
7. re.findall()
8. re.finditer()
9. Match Objects
10. group(), groups(), groupdict()
11. re.sub()
12. re.split()
13. re.compile()
14. Regex Flags
15. Exception Handling in Regex
16. Performance Tips
17. Real-World Applications
18. Chapter Summary

-------------------------------------------------------------------------------------------------------------

# 6.1 Why Python's `re` Module?

## Learning Objective

After completing this lesson, you will be able to:

- Understand why Python provides the `re` module.
- Explain why normal string functions are not sufficient for many automation tasks.
- Understand the relationship between Regular Expressions and Python.
- Recognize situations where the `re` module is required.
- Explain why the `re` module is widely used in enterprise automation.

---

# Previous Knowledge

In the previous five chapters, we learned how to write Regular Expressions.

We studied:

- Character Classes
- Quantifiers
- Groups
- Lookarounds

These concepts describe **what pattern we want to match**.

However,

a Regular Expression alone cannot search text.

It must be executed by a program.

In Python,

this responsibility belongs to the **`re` module**.

---

# Introduction

Suppose we have the following storage log.

```text
Drive ID      : NVME001
Capacity      : 2048GB
Temperature   : 42C
```

Earlier,

we learned how to write a Regular Expression that matches

```text
2048GB
```

But now we have a new question.

> How do we execute this Regular Expression inside a Python program?

Python provides a built-in library called

```python
re
```

which allows Python programs to use Regular Expressions.

---

# The Problem

Suppose we write

```python
text = """
Drive ID : NVME001
Capacity : 2048GB
"""
```

We already know the Regex

```regex
\d+GB
```

But Python cannot execute this pattern by itself.

Simply writing

```python
"\d+GB"
```

does nothing.

Python needs a module that understands Regular Expressions.

That module is

```python
re
```

---

# Why Can't Normal String Functions Solve This?

Suppose we write

```python
text.find("2048GB")
```

This works only when

```text
2048GB
```

is known beforehand.

Tomorrow,

the log may contain

```text
4096GB
```

or

```text
8192GB
```

The value changes.

The pattern remains the same.

The `re` module allows Python to search using patterns instead of fixed text.

---

# The Solution

Python's

```python
re
```

module acts as the bridge between

```
Python Code

↓

Regular Expression

↓

Regex Engine

↓

Match Result
```

Instead of manually searching text,

Python passes the Regular Expression to the Regex Engine through the `re` module.

---

# Relationship Between Python and the Regex Engine

```
Python Program

        │
        ▼

     re Module

        │
        ▼

   Regex Engine

        │
        ▼

Evaluate Pattern

        │
        ▼

Return Result
```

The `re` module does not perform the matching itself.

It communicates with Python's built-in Regex Engine.

---

# Python Execution Flow

```
Write Regex

↓

Import re

↓

Call re Function

↓

Regex Engine Executes Pattern

↓

Return Match Result
```

Every Regular Expression used in Python follows this workflow.

---

# Why is the `re` Module Important?

The `re` module allows Python programs to:

- Search text
- Extract values
- Validate input
- Replace text
- Split text
- Iterate through matches

Without the `re` module,

all of these tasks would require complex manual string processing.

---

# Real-World Usage

### Storage Engineering

- Extract Drive IDs
- Extract Capacities
- Validate Firmware Versions
- Parse Storage Logs

---

### Linux Automation

- Parse command output
- Extract IP addresses
- Read configuration files
- Validate log entries

---

### Python Automation

- Process reports
- Read CSV files
- Parse JSON logs
- Validate user input

---

### Test Automation

- Validate expected output
- Parse execution reports
- Extract execution times
- Verify log messages

---

# Important Observation

A Regular Expression describes

**what**

should be matched.

The `re` module determines

**how**

Python executes that Regular Expression.

Think of the process as

```
Regex

↓

Python re Module

↓

Regex Engine

↓

Match Result
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking that Regular Expressions work automatically in Python.

They must be executed through the `re` module.

---

### Mistake 2

Using normal string functions for dynamic data.

Pattern-based searching should use the `re` module.

---

### Mistake 3

Thinking the `re` module is a third-party library.

It is part of Python's Standard Library.

---

# Interview Questions

1. Why does Python provide the `re` module?

2. What problem does the `re` module solve?

3. Why are normal string functions not always sufficient?

4. How does the `re` module interact with the Regex Engine?

5. Where is the `re` module commonly used?

---

# Practice Questions

### Question 1

Explain why a Regular Expression cannot search text without the `re` module.

---

### Question 2

Why is the `re` module preferred over normal string searching for dynamic data?

---

### Question 3

List five enterprise applications of Python's `re` module.

---

# Memory Tip

```
Regex

↓

Needs

Execution

↓

Python

re Module

↓

Regex Engine

↓

Result
```

Remember

```
Regex

Describes

Pattern

-------------------

re

Executes

Pattern
```

---

# Revision Box

✔ Python uses the built-in `re` module for Regular Expressions.

✔ The `re` module communicates with the Regex Engine.

✔ Normal string functions search fixed text.

✔ The `re` module performs pattern-based searching.

✔ The `re` module is part of Python's Standard Library.

---

# Key Takeaways

- Regular Expressions require Python's `re` module for execution.
- The `re` module serves as the interface between Python code and the Regex Engine.
- Pattern-based searching is more flexible than fixed string searching.
- The `re` module is widely used in Storage Engineering, Linux Automation and Test Automation.
- Understanding the purpose of the `re` module prepares us for writing our first Regex programs in Python.

---

# Coming Up

Now that we understand **why Python provides the `re` module**,

the next lesson introduces **what the `re` module is**, explores its place in Python's Standard Library, and explains the services it provides before we begin writing Python code.

------------------------------------------------------------------------------------------------------------

# 6.2 What is the `re` Module?

## Learning Objective

After completing this lesson, you will be able to:

- Define the Python `re` module.
- Understand the purpose of the `re` module.
- Explain the relationship between Python, the `re` module and the Regex Engine.
- Recognize the services provided by the `re` module.
- Understand why the `re` module is part of Python's Standard Library.

---

# Previous Knowledge

In the previous lesson, we learned why Python needs the `re` module.

We discovered that:

- Regular Expressions describe patterns.
- Python itself cannot execute Regular Expressions directly.
- The `re` module acts as the bridge between Python and the Regex Engine.

Now let us formally define what the `re` module is.

---

# Introduction

Suppose we write the following Regular Expression.

```regex
\d+GB
```

This pattern describes

```
One or more digits

followed by

GB
```

However,

Python cannot execute this pattern by simply reading the string.

Instead,

Python sends the pattern to the `re` module.

The `re` module then passes it to the Regex Engine,

which performs the actual matching.

---

# Definition

The **`re` module** is Python's built-in library for working with Regular Expressions.

It provides functions that allow Python programs to:

- Search text
- Match text
- Extract values
- Replace text
- Split text
- Compile Regular Expressions

The `re` module provides the interface.

The Regex Engine performs the actual pattern matching.

---

# Understanding the Definition

The most important words are

```
Built-in Library
```

The `re` module is included with every standard Python installation.

No additional installation is required.

Unlike external libraries,

the `re` module is immediately available after importing it.

---

# Relationship Between Python, `re` and the Regex Engine

```
Python Program

        │
        ▼

     re Module

        │
        ▼

   Regex Engine

        │
        ▼

Pattern Matching

        │
        ▼

Return Result
```

Notice that

the Regex Engine performs the matching,

while the `re` module provides Python functions that communicate with the engine.

---

# Services Provided by the `re` Module

The `re` module provides several important functions.

| Function | Purpose |
|----------|---------|
| `search()` | Find the first occurrence of a pattern. |
| `match()` | Match from the beginning of the string. |
| `fullmatch()` | Match the entire string. |
| `findall()` | Return all matches. |
| `finditer()` | Return an iterator over all matches. |
| `sub()` | Replace matched text. |
| `split()` | Split text using a pattern. |
| `compile()` | Compile a Regular Expression for repeated use. |

Each of these functions will be studied in detail in the following lessons.

---

# Python Execution Flow

```
Write Pattern

↓

Import re

↓

Call re Function

↓

re Module

↓

Regex Engine

↓

Match Object

or

Result
```

Every Regular Expression in Python follows this workflow.

---

# Python Console Example

```python
>>> import re
>>> re
<module 're' from '...'>
```

This confirms that the `re` module has been successfully imported.

At this point,

we have access to all Regex functions provided by the module.

---

# Another Console Example

```python
>>> import re
>>> pattern = r"\d+GB"
>>> text = "Capacity : 2048GB"
>>> re.search(pattern, text)
<re.Match object; span=(11, 17), match='2048GB'>
```

Notice that

the `re` module returns a **Match Object**,

not simply the matched text.

We will study Match Objects later in this chapter.

---

# Regex Engine Explanation

```
Python Program

↓

Call

re.search()

↓

re Module

↓

Regex Engine

↓

Evaluate Pattern

↓

Create Match Object

↓

Return Result
```

The `re` module never performs matching itself.

It requests the Regex Engine to perform the operation.

---

# Engine Visualization

```
        Python Code

             │
             ▼

      +---------------+
      |   re Module   |
      +---------------+

             │
             ▼

      +---------------+
      | Regex Engine  |
      +---------------+

             │
             ▼

      Pattern Matching

             │
             ▼

      Match Object
```

---

# Real-World Usage

### Storage Engineering

- Parse storage logs.
- Extract firmware versions.
- Validate device identifiers.

---

### Linux Automation

- Parse command output.
- Validate configuration files.
- Extract IP addresses.

---

### Python Automation

- Process reports.
- Read log files.
- Validate structured input.

---

### Test Automation

- Verify expected output.
- Parse execution reports.
- Extract performance metrics.

---

# Important Observation

The `re` module

does **not** replace the Regex Engine.

Instead,

it provides Python functions that allow programs to communicate with the Regex Engine.

Think of the process as

```
Python

↓

re Module

↓

Regex Engine

↓

Match Result
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking the `re` module is a third-party package.

It is part of Python's Standard Library.

---

### Mistake 2

Thinking the `re` module performs pattern matching itself.

The Regex Engine performs the matching.

---

### Mistake 3

Trying to use Regex functions without importing the `re` module.

---

# Interview Questions

1. What is the `re` module?

2. Is the `re` module part of Python's Standard Library?

3. What services does the `re` module provide?

4. What is the relationship between the `re` module and the Regex Engine?

5. Why must the `re` module be imported?

---

# Practice Questions

### Question 1

Explain the relationship between Python, the `re` module and the Regex Engine.

---

### Question 2

List five functions provided by the `re` module.

---

### Question 3

Why is the `re` module considered a built-in library?

---

# Memory Tip

```
Python

↓

re Module

↓

Regex Engine

↓

Match Result
```

Remember

```
Regex

Describes

Pattern

--------------------

re

Provides

Functions

--------------------

Regex Engine

Performs

Matching
```

---

# Revision Box

✔ The `re` module is Python's built-in Regular Expression library.

✔ It is part of Python's Standard Library.

✔ It provides functions for searching, matching, replacing and splitting text.

✔ The Regex Engine performs the actual pattern matching.

✔ The `re` module acts as the interface between Python code and the Regex Engine.

---

# Key Takeaways

- The `re` module is Python's standard library for Regular Expressions.
- It provides high-level functions that communicate with the Regex Engine.
- The Regex Engine performs the actual pattern matching.
- Every Regex operation in Python begins with the `re` module.
- Understanding the `re` module prepares us to start writing real Python Regex programs.

---

# Coming Up

Now that we understand **what the `re` module is**,

the next lesson introduces **importing the `re` module**, explains Python's `import` statement, and prepares us to write our first executable Regular Expression program.

------------------------------------------------------------------------------------------------------------

# 6.3 Importing the `re` Module

## Learning Objective

After completing this lesson, you will be able to:

- Understand why the `re` module must be imported.
- Explain how Python imports modules.
- Import the `re` module correctly.
- Verify that the `re` module is available.
- Prepare Python programs to execute Regular Expressions.

---

# Previous Knowledge

In the previous lesson, we learned that:

- The `re` module is Python's built-in Regular Expression library.
- It provides functions such as:
  - `search()`
  - `match()`
  - `findall()`
  - `finditer()`
- These functions communicate with the Regex Engine.

Before we can use any of these functions,

Python must first load the `re` module.

---

# Introduction

Suppose we write the following program.

```python
pattern = r"\d+GB"

text = "Capacity : 2048GB"

re.search(pattern, text)
```

Running this program produces

```text
NameError: name 're' is not defined
```

Why?

Because Python has never been told what

```python
re
```

is.

Before using the module,

we must import it.

---

# Why Do We Need `import`?

Python keeps its functionality organized into **modules**.

Some modules provide

- Mathematical functions
- File operations
- Date and time handling
- Networking
- Regular Expressions

Python loads a module only when we explicitly request it.

This is done using the

```python
import
```

statement.

---

# Definition

The **`import` statement** tells Python to load a module so that its functions, classes and variables become available to the program.

For Regular Expressions,

the module is

```python
re
```

---

# Syntax

General Syntax

```python
import module_name
```

For Regular Expressions

```python
import re
```

This is the standard and recommended way to use Python's Regex library.

---

# What Happens Internally?

When Python executes

```python
import re
```

the following high-level process occurs.

```
Python Program

↓

import re

↓

Locate re Module

↓

Load Module

↓

Create Module Object

↓

Make Functions Available
```

After this process,

functions such as

```python
re.search()

re.findall()

re.sub()
```

become available.

---

# Python Execution Flow

```
Program Starts

↓

import re

↓

Module Loaded

↓

Regex Functions Available

↓

Call

re.search()

↓

Regex Engine

↓

Return Result
```

Every Regex program follows this sequence.

---

# Python Code Example

```python
import re

print("re module imported successfully.")
```

Output

```text
re module imported successfully.
```

---

# Python Console Example

```python
>>> import re
>>> re
<module 're' from '...'>
```

Python confirms that the module has been imported successfully.

---

# Another Console Example

```python
>>> import re
>>> dir(re)
```

Output (partial)

```text
[
 'compile',
 'findall',
 'finditer',
 'fullmatch',
 'match',
 'search',
 'split',
 'sub'
]
```

The `dir()` function lists the names available inside the `re` module.

We will study these functions one by one.

---

# Regex Engine Explanation

Notice something important.

Executing

```python
import re
```

does **not** execute any Regular Expression.

Instead,

it simply makes the Regex functions available.

The Regex Engine is called **only when** we invoke a function such as

```python
re.search()
```

---

# Engine Visualization

```
      Python Program

             │
             ▼

        import re

             │
             ▼

     +---------------+
     |   re Module   |
     +---------------+

             │
             ▼

Regex Functions Available

             │
             ▼

No Pattern Matching Yet
```

The Regex Engine has **not** been used at this stage.

---

# Storage Engineering Example

```python
import re

log = "Capacity : 2048GB"
```

The module is now ready.

In the next lesson,

we will search this log using

```python
re.search()
```

---

# Linux Automation Example

```python
import re

output = "inet 192.168.1.20/24"
```

Again,

the module is ready,

but no matching has occurred yet.

---

# Python Automation Example

```python
import re

report = """
Status : PASS
Execution Time : 12.45
"""
```

The Regular Expressions will be executed only when we call a function such as

```python
re.search()
```

---

# Important Observation

Importing the `re` module

```
Makes Functions Available
```

It does **not**

```
Execute Regular Expressions
```

Think of it as

```
Import

↓

Preparation

↓

Regex Function

↓

Regex Engine

↓

Result
```

---

# Common Beginner Mistakes

### Mistake 1

Forgetting to import the `re` module before calling

```python
re.search()
```

---

### Mistake 2

Thinking

```python
import re
```

performs pattern matching.

It only loads the module.

---

### Mistake 3

Writing

```python
search(...)
```

instead of

```python
re.search(...)
```

after using

```python
import re
```

---

# Interview Questions

1. Why must the `re` module be imported?

2. What does `import re` do?

3. Does importing the `re` module execute any Regular Expressions?

4. What happens internally when Python executes `import re`?

5. Why does `re.search()` fail without importing the module?

---

# Practice Questions

### Question 1

Write the Python statement required to import the Regular Expression module.

---

### Question 2

Explain why

```python
re.search(...)
```

cannot be used before

```python
import re
```

---

### Question 3

Describe the execution flow after

```python
import re
```

---

# Memory Tip

```
Program Starts

↓

import re

↓

Module Loaded

↓

Regex Functions Ready

↓

Pattern Matching Begins
```

Remember

```
import re

↓

Load Module

NOT

Run Regex
```

---

# Revision Box

✔ `import re` loads Python's Regular Expression module.

✔ Importing the module does not execute any Regex.

✔ Regex matching begins only when functions such as `re.search()` are called.

✔ The `re` module is part of Python's Standard Library.

✔ Every Regex program starts with `import re`.

---

# Key Takeaways

- Python requires `import re` before using Regular Expression functions.
- Importing prepares the program but does not perform matching.
- The Regex Engine is invoked only when a Regex function is called.
- Understanding the import process helps explain why Regex programs are structured the way they are.
- The next step is learning how to perform the first actual Regex search using `re.search()`.

---

# Coming Up

The next lesson introduces **`re.search()`**, the most commonly used Regular Expression function in Python.

You will learn:

- How `re.search()` works
- Its syntax and parameters
- The Match Object
- Practical examples from Storage Engineering, Linux Automation and Test Automation
- How the Regex Engine executes the search operation

------------------------------------------------------------------------------------------------------------

# 6.4 `re.search()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of `re.search()`.
- Explain how `re.search()` works.
- Use `re.search()` to search text using Regular Expressions.
- Understand the Match Object returned by `re.search()`.
- Apply `re.search()` in Storage Engineering, Linux Automation and Test Automation.

---

# Previous Knowledge

In the previous lesson, we learned how to import Python's `re` module.

```python
import re
```

Importing the module makes Regex functions available,

but it does **not** perform any matching.

To execute a Regular Expression,

we must call one of the functions provided by the `re` module.

The most commonly used function is

```python
re.search()
```

---

# Introduction

Suppose we have the following storage log.

```text
Drive ID : NVME001

Capacity : 2048GB

Temperature : 42C
```

Earlier,

we learned the Regular Expression

```regex
\d+GB
```

Now the question is

> How do we search this log using Python?

The answer is

```python
re.search()
```

---

# Why Do We Need `re.search()`?

Suppose we write

```python
pattern = r"\d+GB"
```

and

```python
text = "Capacity : 2048GB"
```

Writing the pattern alone does nothing.

Python needs a function that sends the pattern to the Regex Engine.

That function is

```python
re.search()
```

---

# Definition

`re.search()` searches the **entire input string** for the **first occurrence** of a pattern.

If a match is found,

it returns a **Match Object**.

If no match exists,

it returns

```python
None
```

---

# Syntax

```python
re.search(pattern, string)
```

---

# Function Reference

| Property | Value |
|----------|-------|
| Function | `re.search()` |
| Searches Entire String? | ✅ Yes |
| Returns | Match Object or `None` |
| Finds First Match Only? | ✅ Yes |
| Case Sensitive? | ✅ Yes (default) |
| Uses Regex Engine? | ✅ Yes |

---

# Parameters

## `pattern`

The Regular Expression that describes what should be searched.

Example

```python
r"\d+GB"
```

---

## `string`

The input text on which the search is performed.

Example

```python
"Capacity : 2048GB"
```

---

# Return Value

If the pattern is found

```
↓

Match Object
```

If the pattern is not found

```
↓

None
```

This behavior is extremely important because it allows Python programs to determine whether matching succeeded.

---

# Python Execution Flow

```
Write Pattern

↓

Write Input Text

↓

Call

re.search()

↓

re Module

↓

Regex Engine

↓

Pattern Found?

│
├── Yes → Match Object
│
└── No → None
```

---

# Regex Engine Explanation

Pattern

```regex
\d+GB
```

Input

```text
Capacity : 2048GB
```

Regex Engine

```
Receive Pattern

↓

Receive Input

↓

Search Entire String

↓

First Match Found?

↓

YES

↓

Create Match Object

↓

Return To Python
```

---

# Engine Visualization

```
Pattern

      │
      ▼

+------------------+
|   Regex Engine   |
+------------------+

      │
      ▼

Search Entire String

      │
 ┌────┴────┐
 │         │
 ▼         ▼

Match    No Match

 │         │

 ▼         ▼

Match     None

Object
```

---

# Python Code Example

```python
import re

pattern = r"\d+GB"

text = "Capacity : 2048GB"

result = re.search(pattern, text)

print(result)
```

Output

```text
<re.Match object; span=(11, 17), match='2048GB'>
```

Notice that

`re.search()` returns a **Match Object**,

not the matched text itself.

---

# Python Console Example

```python
>>> import re
>>> text = "Capacity : 2048GB"
>>> re.search(r"\d+GB", text)
<re.Match object; span=(11, 17), match='2048GB'>
```

---

# Example — No Match

```python
import re

text = "Capacity : 2048GB"

result = re.search(r"\d+TB", text)

print(result)
```

Output

```text
None
```

No Match Object is created because the pattern does not exist.

---

# Storage Engineering Example

```python
import re

log = "Capacity : 4096GB"

match = re.search(r"\d+GB", log)

print(match)
```

Output

```text
<re.Match object ...>
```

Application

- Capacity Extraction
- Log Validation

---

# Linux Automation Example

```python
import re

output = "inet 192.168.1.15/24"

match = re.search(r"\d+\.\d+\.\d+\.\d+", output)

print(match)
```

Application

- IP Address Extraction
- Network Automation

---

# Python Automation Example

```python
import re

report = "Status : PASS"

match = re.search(r"PASS", report)

print(match)
```

Application

- Report Validation
- Test Result Verification

---

# Important Observation

`re.search()` always searches the **entire input string**,

but it **stops after finding the first match**.

If multiple matches exist,

only the first one is returned.

To retrieve every match,

another function is required.

We will study that later.

---

# Common Beginner Mistakes

### Mistake 1

Thinking `re.search()` returns the matched text.

It returns a **Match Object**.

---

### Mistake 2

Expecting `re.search()` to return all matches.

It returns only the **first** match.

---

### Mistake 3

Forgetting to check whether the returned value is

```python
None
```

before using it.

---

# Interview Questions

1. What is the purpose of `re.search()`?

2. What does `re.search()` return?

3. Does `re.search()` search the entire string?

4. What happens if no match is found?

5. Does `re.search()` return all matches?

---

# Practice Questions

### Question 1

Write a Python program that searches for a storage capacity using `re.search()`.

---

### Question 2

Explain why `re.search()` returns a Match Object instead of plain text.

---

### Question 3

What is returned when no match exists?

---

# Memory Tip

```
re.search()

↓

Entire String

↓

First Match

↓

Match Object

or

None
```

Remember

```
Search Everything

Return First Match
```

---

# Revision Box

✔ `re.search()` searches the entire input string.

✔ It returns only the first match.

✔ A successful search returns a Match Object.

✔ An unsuccessful search returns `None`.

✔ The Regex Engine performs the actual matching.

---

# Key Takeaways

- `re.search()` is the most commonly used Regex function in Python.
- It searches the entire input string for the first occurrence of a pattern.
- Successful searches return a Match Object; unsuccessful searches return `None`.
- It is widely used in Storage Engineering, Linux Automation and Test Automation.
- Understanding `re.search()` provides the foundation for every other Regex function in Python.

---

# Coming Up

Now that we understand **`re.search()`**,

the next lesson introduces **Match Objects**, explaining what they are, why Python returns them instead of plain text, and how to retrieve useful information such as the matched text, position and captured groups.

------------------------------------------------------------------------------------------------------------

# 6.5 Match Objects

## Learning Objective

After completing this lesson, you will be able to:

- Understand what a Match Object is.
- Explain why `re.search()` returns a Match Object instead of plain text.
- Identify the information stored inside a Match Object.
- Understand the relationship between the Regex Engine and the Match Object.
- Prepare for extracting information using Match Object methods.

---

# Previous Knowledge

In the previous lesson, we learned that

```python
re.search()
```

returns something like

```python
<re.Match object; span=(11, 17), match='2048GB'>
```

Notice that

Python did **not** return

```text
2048GB
```

Instead,

it returned a **Match Object**.

Now let us understand why.

---

# Introduction

Suppose we search

```python
import re

text = "Capacity : 2048GB"

result = re.search(r"\d+GB", text)

print(result)
```

Output

```text
<re.Match object; span=(11, 17), match='2048GB'>
```

Many beginners expect

```text
2048GB
```

Instead,

Python returns a Match Object.

This is intentional.

---

# Why Doesn't Python Return Only the Matched Text?

Suppose Python returned only

```text
2048GB
```

Could we answer questions like:

- Where was the match found?
- Where did the match start?
- Where did it end?
- Which groups were captured?

No.

The matched text alone is insufficient.

Python therefore returns an object that stores much more information.

---

# Definition

A **Match Object** is a Python object created by the `re` module whenever a Regular Expression successfully matches text.

The Match Object stores information about the successful match,

including:

- The matched text
- Start position
- End position
- Span
- Captured groups

---

# Understanding the Definition

Think of the Match Object as a **container**.

Instead of storing only

```text
2048GB
```

it stores

```
Matched Text

↓

Start Position

↓

End Position

↓

Span

↓

Captured Groups
```

Later lessons will show how to retrieve each piece of information.

---

# Relationship Between the Regex Engine and Match Object

```
Python Program

↓

re.search()

↓

Regex Engine

↓

Pattern Found?

│
├── YES
│      ↓
│  Create Match Object
│      ↓
│  Return To Python
│
└── NO
       ↓
      None
```

The Regex Engine creates the Match Object only after a successful match.

---

# Python Execution Flow

```
Write Pattern

↓

Call

re.search()

↓

Regex Engine

↓

Successful Match?

│
├── Yes
│      ↓
│ Match Object
│
└── No
       ↓
      None
```

---

# Python Code Example

```python
import re

text = "Capacity : 2048GB"

result = re.search(r"\d+GB", text)

print(result)
```

Output

```text
<re.Match object; span=(11, 17), match='2048GB'>
```

---

# Python Console Example

```python
>>> import re
>>> text = "Capacity : 2048GB"
>>> match = re.search(r"\d+GB", text)
>>> match
<re.Match object; span=(11, 17), match='2048GB'>
```

---

# What Information Does It Store?

A Match Object stores information such as

| Information | Example |
|------------|---------|
| Matched Text | `2048GB` |
| Start Position | `11` |
| End Position | `17` |
| Span | `(11, 17)` |
| Captured Groups | Available if groups exist |

We will learn how to retrieve each value in the next lessons.

---

# Regex Engine Explanation

Suppose the Regex Engine searches

```text
Capacity : 2048GB
```

using

```regex
\d+GB
```

Engine Workflow

```
Receive Pattern

↓

Search Input

↓

First Match Found

↓

Collect Match Information

↓

Create Match Object

↓

Return To Python
```

The Match Object is therefore a **result produced by the Regex Engine**.

---

# Engine Visualization

```
Pattern

      │
      ▼

+------------------+
|   Regex Engine   |
+------------------+

      │
      ▼

Successful Match

      │
      ▼

+------------------+
|  Match Object    |
+------------------+

      │
      ▼

Return To Python
```

---

# Storage Engineering Example

```python
import re

log = "Capacity : 4096GB"

match = re.search(r"\d+GB", log)

print(match)
```

Application

- Capacity Extraction
- Storage Log Processing

---

# Linux Automation Example

```python
import re

output = "inet 192.168.1.20/24"

match = re.search(r"\d+\.\d+\.\d+\.\d+", output)

print(match)
```

Application

- IP Address Extraction
- Network Automation

---

# Python Automation Example

```python
import re

report = "Status : PASS"

match = re.search(r"PASS", report)

print(match)
```

Application

- Report Validation
- Automated Testing

---

# Important Observation

The Match Object is **not** the final information we usually want.

Instead,

it is a container that stores useful information about the match.

Later,

we will retrieve values from it using methods such as

```python
group()

start()

end()

span()

groups()
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking the Match Object is the matched text.

It stores the matched text,

but it also stores additional information.

---

### Mistake 2

Trying to print the Match Object when only the matched text is required.

---

### Mistake 3

Assuming every Regex function returns a Match Object.

Some functions return lists,

others return iterators,

and unsuccessful searches return `None`.

---

# Interview Questions

1. What is a Match Object?

2. Why does `re.search()` return a Match Object?

3. Who creates the Match Object?

4. What information does a Match Object contain?

5. What is returned if no match exists?

---

# Practice Questions

### Question 1

Explain why returning only the matched text would be insufficient.

---

### Question 2

List five pieces of information stored inside a Match Object.

---

### Question 3

Describe how the Regex Engine creates a Match Object.

---

# Memory Tip

```
Regex Engine

↓

Successful Match

↓

Match Object

↓

Contains

Everything

About

The Match
```

Remember

```
Match Object

≠

Matched Text

It

Contains

The Matched Text
```

---

# Revision Box

✔ A Match Object is created only after a successful match.

✔ It stores much more than the matched text.

✔ It contains positions, span and captured groups.

✔ Unsuccessful searches return `None`.

✔ Match Objects are returned by functions such as `re.search()`, `re.match()` and `re.fullmatch()`.

---

# Key Takeaways

- A Match Object is Python's representation of a successful Regular Expression match.
- It acts as a container holding detailed information about the match.
- The Regex Engine creates the Match Object after finding a successful match.
- Understanding Match Objects is essential before learning methods such as `group()`, `start()` and `span()`.
- Most Python Regex functions build upon the concept of the Match Object.

---

# Coming Up

Now that we understand **what a Match Object is**,

the next lesson introduces **`re.match()`**, explaining how it differs from `re.search()` and why it only attempts to match at the **beginning of the input string**.

------------------------------------------------------------------------------------------------------------

# 6.6 `re.match()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of `re.match()`.
- Explain how `re.match()` differs from `re.search()`.
- Understand why `re.match()` only checks the beginning of a string.
- Apply `re.match()` in practical Python programs.
- Recognize situations where `re.match()` is appropriate.

---

# Previous Knowledge

In the previous lesson, we learned that

```python
re.search()
```

searches the **entire input string** for the **first occurrence** of a pattern.

Now we will study

```python
re.match()
```

Although the syntax is similar,

its behavior is very different.

---

# Introduction

Consider the following input.

```text
Capacity : 2048GB
```

Suppose we search

```regex
Capacity
```

using

```python
re.match()
```

A match is found because the pattern appears at the **beginning** of the string.

Now consider

```text
Drive Capacity : 2048GB
```

Searching for

```regex
Capacity
```

using

```python
re.match()
```

fails,

even though

```
Capacity
```

exists in the string.

Why?

Because it is **not at the beginning**.

---

# Why Do We Need `re.match()`?

Some applications require verification that a string starts with a specific pattern.

Examples

- Configuration keys
- Log prefixes
- File headers
- Command identifiers

In such situations,

searching the entire string is unnecessary.

We only care about the beginning.

---

# Definition

`re.match()` attempts to match a Regular Expression **only at the beginning of the input string**.

If the pattern matches from the first character,

a **Match Object** is returned.

Otherwise,

`None` is returned.

---

# Syntax

```python
re.match(pattern, string)
```

---

# Function Reference

| Property | Value |
|----------|-------|
| Function | `re.match()` |
| Searches Entire String? | ❌ No |
| Checks Beginning Only? | ✅ Yes |
| Returns | Match Object or `None` |
| Finds First Match Only? | ✅ Yes |
| Uses Regex Engine? | ✅ Yes |

---

# Parameters

## `pattern`

The Regular Expression to match.

---

## `string`

The input string.

---

# Return Value

```
Beginning Matches

↓

Match Object

-----------------------

Beginning Does Not Match

↓

None
```

---

# Python Execution Flow

```
Write Pattern

↓

Write Input

↓

Call

re.match()

↓

Regex Engine

↓

Check Beginning

│
├── Match → Match Object
│
└── No Match → None
```

---

# Regex Engine Explanation

Pattern

```regex
Capacity
```

Input

```text
Capacity : 2048GB
```

Regex Engine

```
Receive Pattern

↓

Receive Input

↓

Current Position

↓

Beginning Of String

↓

Pattern Matches?

↓

YES

↓

Create Match Object

↓

Return To Python
```

Notice that

the engine does **not** continue searching later in the string.

---

# Engine Visualization

```
Beginning

      │
      ▼

+------------------+
|   Regex Engine   |
+------------------+

      │
      ▼

Compare Pattern

      │
 ┌────┴────┐
 │         │
 ▼         ▼

Match    No Match

 │         │

 ▼         ▼

Match     None

Object
```

---

# Python Code Example

```python
import re

text = "Capacity : 2048GB"

result = re.match(r"Capacity", text)

print(result)
```

Output

```text
<re.Match object ...>
```

---

# Example — No Match

```python
import re

text = "Drive Capacity : 2048GB"

result = re.match(r"Capacity", text)

print(result)
```

Output

```text
None
```

Although

```
Capacity
```

exists,

it is **not** at the beginning.

---

# Python Console Example

```python
>>> import re
>>> re.match(r"Capacity", "Capacity : 2048GB")
<re.Match object ...>

>>> re.match(r"Capacity", "Drive Capacity : 2048GB")
None
```

---

# Storage Engineering Example

```python
import re

log = "Drive=NVME001"

match = re.match(r"Drive=", log)

print(match)
```

Application

- Validate log prefixes.
- Verify storage record formats.

---

# Linux Automation Example

```python
import re

line = "HOST=10.10.20.15"

match = re.match(r"HOST=", line)

print(match)
```

Application

- Validate configuration entries.
- Parse key-value files.

---

# Python Automation Example

```python
import re

report = "Status=PASS"

match = re.match(r"Status=", report)

print(match)
```

Application

- Validate report formats.
- Verify structured output.

---

# Compare `re.search()` vs `re.match()`

| Feature | `re.search()` | `re.match()` |
|---------|---------------|--------------|
| Searches entire string | ✅ Yes | ❌ No |
| Checks beginning only | ❌ No | ✅ Yes |
| Returns Match Object | ✅ Yes | ✅ Yes |
| Returns `None` on failure | ✅ Yes | ✅ Yes |

---

# Regex Engine Comparison

## `re.search()`

```
Beginning

↓

Middle

↓

End

↓

First Match
```

---

## `re.match()`

```
Beginning

↓

Match?

│
├── Yes
│
└── No

Stop
```

---

# Important Observation

Many beginners expect

```python
re.match()
```

to behave like

```python
re.search()
```

It does not.

If the pattern is not found at the **beginning**,

matching immediately fails.

---

# Common Beginner Mistakes

### Mistake 1

Thinking `re.match()` searches the entire string.

It only checks the beginning.

---

### Mistake 2

Using `re.match()` when `re.search()` is actually required.

---

### Mistake 3

Confusing `re.match()` with `re.fullmatch()`.

`re.match()` checks only the beginning.

`re.fullmatch()` checks the entire string.

---

# Interview Questions

1. What is the purpose of `re.match()`?

2. How does `re.match()` differ from `re.search()`?

3. What does `re.match()` return?

4. Why might `re.match()` return `None` even when the pattern exists in the string?

5. Give practical applications of `re.match()`.

---

# Practice Questions

### Question 1

Write a Python program using `re.match()` to validate that a configuration line starts with `HOST=`.

---

### Question 2

Explain why

```python
re.match(r"Capacity", "Drive Capacity : 2048GB")
```

returns `None`.

---

### Question 3

List three situations where `re.match()` is more appropriate than `re.search()`.

---

# Memory Tip

```
re.match()

↓

Beginning Only

↓

Match?

↓

Match Object

or

None
```

Remember

```
match()

=

Beginning

Only
```

---

# Revision Box

✔ `re.match()` checks only the beginning of the input string.

✔ It returns a Match Object or `None`.

✔ It does not continue searching after the beginning.

✔ It is useful for validating prefixes and structured input.

✔ `re.search()` and `re.match()` serve different purposes.

---

# Key Takeaways

- `re.match()` attempts to match a pattern only at the beginning of the input string.
- Unlike `re.search()`, it never scans the rest of the string.
- Successful matches return a Match Object; failures return `None`.
- `re.match()` is commonly used for validating prefixes and structured formats.
- Understanding the difference between `re.search()` and `re.match()` is a common interview requirement.

---

# Coming Up

The next lesson introduces **`re.fullmatch()`**, which performs the strictest type of matching by requiring the **entire input string** to satisfy the Regular Expression.

------------------------------------------------------------------------------------------------------------

# 6.7 `re.fullmatch()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of `re.fullmatch()`.
- Explain how `re.fullmatch()` differs from `re.search()` and `re.match()`.
- Understand why `re.fullmatch()` requires the entire string to satisfy the Regular Expression.
- Apply `re.fullmatch()` for input validation.
- Recognize practical applications in automation.

---

# Previous Knowledge

We have already learned two important search functions.

`re.search()`

- Searches the entire string.
- Returns the first match.

`re.match()`

- Checks only the beginning of the string.

Now we will study the strictest matching function.

```python
re.fullmatch()
```

---

# Introduction

Consider the following input.

```text
2048GB
```

Searching with

```regex
\d+GB
```

using

```python
re.fullmatch()
```

returns a successful match.

Now consider

```text
Capacity : 2048GB
```

Using the same pattern

```regex
\d+GB
```

returns

```python
None
```

Why?

Because the **entire string** does not match the pattern.

Only part of it does.

---

# Why Do We Need `re.fullmatch()`?

Many applications require the entire input to follow a specific format.

Examples include:

- Email validation
- IPv4 validation
- Phone numbers
- Device IDs
- Hostnames
- Password validation

In these situations,

matching only a part of the string is not sufficient.

The complete input must satisfy the Regular Expression.

---

# Definition

`re.fullmatch()` attempts to match a Regular Expression against the **entire input string**.

A Match Object is returned only if the **complete string** satisfies the pattern.

Otherwise,

`None` is returned.

---

# Syntax

```python
re.fullmatch(pattern, string)
```

---

# Function Reference

| Property | Value |
|----------|-------|
| Function | `re.fullmatch()` |
| Searches Entire String? | ✅ Entire string must match |
| Partial Match Allowed? | ❌ No |
| Returns | Match Object or `None` |
| Uses Regex Engine? | ✅ Yes |

---

# Parameters

## `pattern`

The Regular Expression describing the required format.

---

## `string`

The complete input string to validate.

---

# Return Value

```
Entire String Matches

↓

Match Object

------------------------

Entire String Does Not Match

↓

None
```

---

# Python Execution Flow

```
Write Pattern

↓

Write Input

↓

Call

re.fullmatch()

↓

Regex Engine

↓

Entire String Matches?

│
├── Yes → Match Object
│
└── No → None
```

---

# Regex Engine Explanation

Pattern

```regex
\d+GB
```

Input

```text
2048GB
```

Regex Engine

```
Receive Pattern

↓

Receive Input

↓

Compare Entire String

↓

Entire String Matches?

↓

YES

↓

Create Match Object

↓

Return To Python
```

Notice that

every character must satisfy the pattern.

---

# Engine Visualization

```
Entire String

      │
      ▼

+------------------+
|   Regex Engine   |
+------------------+

      │
      ▼

Entire String Valid?

      │
 ┌────┴────┐
 │         │
 ▼         ▼

YES       NO

 │         │

 ▼         ▼

Match     None

Object
```

---

# Python Code Example

```python
import re

text = "2048GB"

result = re.fullmatch(r"\d+GB", text)

print(result)
```

Output

```text
<re.Match object ...>
```

---

# Example — No Match

```python
import re

text = "Capacity : 2048GB"

result = re.fullmatch(r"\d+GB", text)

print(result)
```

Output

```text
None
```

Although

```text
2048GB
```

exists,

the complete string does not match.

---

# Python Console Example

```python
>>> import re
>>> re.fullmatch(r"\d+GB", "2048GB")
<re.Match object ...>

>>> re.fullmatch(r"\d+GB", "Capacity : 2048GB")
None
```

---

# Storage Engineering Example

```python
import re

capacity = "4096GB"

match = re.fullmatch(r"\d+GB", capacity)

print(match)
```

Application

- Capacity Validation
- Input Verification

---

# Linux Automation Example

```python
import re

hostname = "server01"

match = re.fullmatch(r"[a-z]+\d+", hostname)

print(match)
```

Application

- Hostname Validation
- Configuration Verification

---

# Python Automation Example

```python
import re

status = "PASS"

match = re.fullmatch(r"PASS|FAIL", status)

print(match)
```

Application

- Report Validation
- Test Result Verification

---

# Comparison

| Feature | `re.search()` | `re.match()` | `re.fullmatch()` |
|---------|---------------|--------------|------------------|
| Searches entire string | ✅ | ❌ | ✅ |
| Matches only beginning | ❌ | ✅ | ❌ |
| Entire string must match | ❌ | ❌ | ✅ |
| Returns Match Object | ✅ | ✅ | ✅ |

---

# Visual Comparison

```
re.search()

Beginning ───────────────────── End
      ▲         ▲         ▲
      Can Match Anywhere

------------------------------------

re.match()

Beginning ───────────────────── End
▲
Must Match Here

------------------------------------

re.fullmatch()

Beginning ───────────────────── End
▲──────────────────────────────▲

Entire String Must Match
```

---

# Important Observation

Think of the three functions like this:

```
re.search()

↓

Find It Anywhere

-------------------------

re.match()

↓

Must Start Here

-------------------------

re.fullmatch()

↓

Everything Must Match
```

---

# Common Beginner Mistakes

### Mistake 1

Expecting `re.fullmatch()` to return a match when only part of the string matches.

---

### Mistake 2

Using `re.search()` for input validation.

Validation usually requires `re.fullmatch()`.

---

### Mistake 3

Confusing `re.match()` with `re.fullmatch()`.

One checks only the beginning.

The other checks the entire string.

---

# Interview Questions

1. What is the purpose of `re.fullmatch()`?

2. How does `re.fullmatch()` differ from `re.search()`?

3. How does `re.fullmatch()` differ from `re.match()`?

4. Why is `re.fullmatch()` useful for validation?

5. Give practical applications of `re.fullmatch()`.

---

# Practice Questions

### Question 1

Write a Python program that validates storage capacities such as

```text
2048GB
```

using `re.fullmatch()`.

---

### Question 2

Explain why

```python
re.fullmatch(r"\d+GB", "Capacity : 2048GB")
```

returns `None`.

---

### Question 3

List five situations where `re.fullmatch()` is preferred over `re.search()`.

---

# Memory Tip

```
re.fullmatch()

↓

Whole String

↓

Everything Must Match

↓

Match Object

or

None
```

Remember

```
search()

↓

Anywhere

----------------

match()

↓

Beginning

----------------

fullmatch()

↓

Entire String
```

---

# Revision Box

✔ `re.fullmatch()` validates the entire input string.

✔ Partial matches are not accepted.

✔ It returns a Match Object or `None`.

✔ It is commonly used for input validation.

✔ It is stricter than both `re.search()` and `re.match()`.

---

# Key Takeaways

- `re.fullmatch()` requires the entire input string to satisfy the Regular Expression.
- It is the preferred function for validation tasks.
- Successful validation returns a Match Object; otherwise `None`.
- It complements `re.search()` and `re.match()` by providing strict whole-string matching.
- Understanding the differences among these three functions is essential for practical Python Regex programming.

---

# Coming Up

So far, each function returns **only one Match Object**.

The next lesson introduces **`re.findall()`**, which retrieves **every match** in the input string and returns them as a Python list.

------------------------------------------------------------------------------------------------------------

# 6.8 `re.findall()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of `re.findall()`.
- Explain how `re.findall()` differs from `re.search()`.
- Understand why `re.findall()` returns a Python list.
- Apply `re.findall()` to extract multiple values.
- Use `re.findall()` in Storage Engineering, Linux Automation and Test Automation.

---

# Previous Knowledge

So far, we have learned:

- `re.search()`
- `re.match()`
- `re.fullmatch()`

Each of these functions returns **only one Match Object**.

However,

many real-world automation tasks require extracting **every occurrence** of a pattern.

For that,

Python provides

```python
re.findall()
```

---

# Introduction

Consider the following storage log.

```text
Drive1 : 512GB

Drive2 : 1024GB

Drive3 : 2048GB
```

Suppose we want to extract

```text
512GB

1024GB

2048GB
```

Using

```python
re.search()
```

returns only

```text
512GB
```

because it stops after the first match.

To retrieve every capacity,

we use

```python
re.findall()
```

---

# Why Do We Need `re.findall()`?

Automation scripts frequently process

- Storage Logs
- Linux Command Output
- Reports
- Configuration Files

These files usually contain many matching values.

Examples

```
Multiple Capacities

Multiple IP Addresses

Multiple Error Codes

Multiple Device IDs
```

Retrieving only the first match is often insufficient.

---

# Definition

`re.findall()` searches the **entire input string** and returns **every non-overlapping match** as a Python list.

If no match is found,

an empty list is returned.

---

# Syntax

```python
re.findall(pattern, string)
```

---

# Function Reference

| Property | Value |
|----------|-------|
| Function | `re.findall()` |
| Searches Entire String? | ✅ Yes |
| Finds All Matches? | ✅ Yes |
| Returns | Python List |
| Returns Match Object? | ❌ No |
| Uses Regex Engine? | ✅ Yes |

---

# Parameters

## `pattern`

The Regular Expression to search.

---

## `string`

The input text.

---

# Return Value

```
Matches Found

↓

Python List

------------------------

No Matches

↓

[]
```

Notice that

`re.findall()` never returns a Match Object.

---

# Python Execution Flow

```
Write Pattern

↓

Write Input

↓

Call

re.findall()

↓

Regex Engine

↓

Search Entire String

↓

Collect Every Match

↓

Return List
```

---

# Regex Engine Explanation

Pattern

```regex
\d+GB
```

Input

```text
512GB 1024GB 2048GB
```

Regex Engine

```
Receive Pattern

↓

Search Entire String

↓

First Match

↓

Continue Searching

↓

Second Match

↓

Continue Searching

↓

Third Match

↓

End Of Input

↓

Return List
```

Unlike `re.search()`,

the Regex Engine continues searching until the entire string has been processed.

---

# Engine Visualization

```
Pattern

      │
      ▼

+------------------+
|   Regex Engine   |
+------------------+

      │
      ▼

Entire String

      │
      ▼

Collect Every Match

      │
      ▼

Python List
```

---

# Python Code Example

```python
import re

text = "512GB 1024GB 2048GB"

result = re.findall(r"\d+GB", text)

print(result)
```

Output

```python
['512GB', '1024GB', '2048GB']
```

---

# Example — No Match

```python
import re

text = "Temperature : 42C"

result = re.findall(r"\d+GB", text)

print(result)
```

Output

```python
[]
```

An empty list indicates that no matches were found.

---

# Python Console Example

```python
>>> import re
>>> text = "512GB 1024GB 2048GB"
>>> re.findall(r"\d+GB", text)
['512GB', '1024GB', '2048GB']
```

---

# Storage Engineering Example

```python
import re

log = """
Drive1 : 512GB
Drive2 : 1024GB
Drive3 : 2048GB
"""

capacities = re.findall(r"\d+GB", log)

print(capacities)
```

Output

```python
['512GB', '1024GB', '2048GB']
```

Application

- Capacity Extraction
- Storage Report Generation

---

# Linux Automation Example

```python
import re

output = """
inet 192.168.1.10
inet 10.10.20.15
"""

ips = re.findall(r"\d+\.\d+\.\d+\.\d+", output)

print(ips)
```

Application

- Network Discovery
- Configuration Validation

---

# Python Automation Example

```python
import re

report = """
PASS
FAIL
PASS
"""

results = re.findall(r"PASS|FAIL", report)

print(results)
```

Output

```python
['PASS', 'FAIL', 'PASS']
```

Application

- Test Report Analysis
- Result Statistics

---

# Compare

| Feature | `re.search()` | `re.findall()` |
|---------|---------------|----------------|
| Searches entire string | ✅ Yes | ✅ Yes |
| Stops after first match | ✅ Yes | ❌ No |
| Returns Match Object | ✅ Yes | ❌ No |
| Returns List | ❌ No | ✅ Yes |

---

# Regex Engine Comparison

## `re.search()`

```
First Match

↓

Stop
```

---

## `re.findall()`

```
First Match

↓

Continue

↓

Second Match

↓

Continue

↓

Third Match

↓

Continue

↓

End

↓

Return List
```

---

# Important Observation

`re.findall()` returns **only the matched text**.

It does **not** return:

- Start position
- End position
- Span
- Match Objects

If position information is required,

another function is needed.

We will study that next.

---

# Common Beginner Mistakes

### Mistake 1

Expecting `re.findall()` to return Match Objects.

It returns a list of matched strings.

---

### Mistake 2

Thinking `re.findall()` stops after the first match.

It searches the entire input.

---

### Mistake 3

Confusing an empty list

```python
[]
```

with

```python
None
```

`re.findall()` returns an empty list when nothing matches.

---

# Interview Questions

1. What is the purpose of `re.findall()`?

2. What does `re.findall()` return?

3. Why doesn't `re.findall()` return Match Objects?

4. What is returned if no matches exist?

5. Give practical applications of `re.findall()`.

---

# Practice Questions

### Question 1

Write a Python program that extracts all storage capacities from a log.

---

### Question 2

Explain why `re.findall()` is useful for log parsing.

---

### Question 3

List five situations where `re.findall()` is preferred over `re.search()`.

---

# Memory Tip

```
re.findall()

↓

Search Entire String

↓

Collect Every Match

↓

Return Python List
```

Remember

```
search()

↓

One Match

--------------------

findall()

↓

All Matches
```

---

# Revision Box

✔ `re.findall()` searches the entire input string.

✔ It returns every non-overlapping match.

✔ The return type is a Python list.

✔ No matches produce an empty list.

✔ It is widely used for extraction tasks.

---

# Key Takeaways

- `re.findall()` retrieves every non-overlapping match in the input string.
- It returns a Python list rather than Match Objects.
- It is ideal for extracting multiple values from logs, reports and command output.
- Unlike `re.search()`, it processes the entire input before returning.
- `re.findall()` is one of the most frequently used functions in automation.

---

# Coming Up

Although `re.findall()` returns every match,

it returns **only the matched text**.

The next lesson introduces **`re.finditer()`**, which returns a sequence of **Match Objects**, allowing access to the matched text, positions, spans and captured groups for every match.

------------------------------------------------------------------------------------------------------------

# 6.9 `re.finditer()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of `re.finditer()`.
- Explain how `re.finditer()` differs from `re.findall()`.
- Understand why `re.finditer()` returns an iterator.
- Apply `re.finditer()` to process multiple Match Objects.
- Recognize practical applications in automation.

---

# Previous Knowledge

In the previous lesson, we learned that

```python
re.findall()
```

searches the entire input string and returns

```python
['512GB', '1024GB', '2048GB']
```

Although this is useful,

it provides only the matched text.

Sometimes,

automation scripts also need:

- Start Position
- End Position
- Span
- Captured Groups

For these situations,

Python provides

```python
re.finditer()
```

---

# Introduction

Suppose we have the following storage log.

```text
Drive1 : 512GB

Drive2 : 1024GB

Drive3 : 2048GB
```

We want to know

- Every capacity
- Where each capacity appears
- The span of each match

A list of strings is no longer sufficient.

We need complete Match Objects.

---

# Why Do We Need `re.finditer()`?

Many automation tasks require more than the matched text.

Examples include:

- Highlighting matches
- Recording positions
- Generating reports
- Replacing selected matches
- Processing captured groups

For these tasks,

Match Objects are much more useful than plain strings.

---

# Definition

`re.finditer()` searches the entire input string and returns an **iterator** that produces a **Match Object** for every non-overlapping match.

If no matches exist,

the iterator simply produces no Match Objects.

---

# Syntax

```python
re.finditer(pattern, string)
```

---

# Function Reference

| Property | Value |
|----------|-------|
| Function | `re.finditer()` |
| Searches Entire String? | ✅ Yes |
| Finds All Matches? | ✅ Yes |
| Returns | Iterator |
| Returns Match Objects? | ✅ Yes |
| Uses Regex Engine? | ✅ Yes |

---

# Parameters

## `pattern`

The Regular Expression describing the required matches.

---

## `string`

The input text.

---

# Return Value

```
Matches Found

↓

Iterator

↓

Match Object

↓

Match Object

↓

Match Object
```

Unlike

```python
re.findall()
```

no list is created.

Instead,

Match Objects are produced one at a time.

---

# Python Execution Flow

```
Write Pattern

↓

Write Input

↓

Call

re.finditer()

↓

Regex Engine

↓

Search Entire String

↓

Create Match Objects

↓

Return Iterator
```

---

# Regex Engine Explanation

Pattern

```regex
\d+GB
```

Input

```text
512GB 1024GB 2048GB
```

Regex Engine

```
Receive Pattern

↓

Search Entire String

↓

First Match

↓

Create Match Object

↓

Second Match

↓

Create Match Object

↓

Third Match

↓

Create Match Object

↓

Return Iterator
```

Unlike

```python
re.findall()
```

the engine creates Match Objects rather than strings.

---

# Engine Visualization

```
Pattern

      │
      ▼

+------------------+
|   Regex Engine   |
+------------------+

      │
      ▼

Entire String

      │
      ▼

Create Match Objects

      │
      ▼

Iterator
```

---

# Python Code Example

```python
import re

text = "512GB 1024GB 2048GB"

matches = re.finditer(r"\d+GB", text)

for match in matches:
    print(match)
```

Output

```text
<re.Match object ...>

<re.Match object ...>

<re.Match object ...>
```

---

# Python Console Example

```python
>>> import re
>>> text = "512GB 1024GB 2048GB"
>>> matches = re.finditer(r"\d+GB", text)
>>> for match in matches:
...     print(match)
...
<re.Match object ...>
<re.Match object ...>
<re.Match object ...>
```

---

# Storage Engineering Example

```python
import re

log = """
Drive1 : 512GB
Drive2 : 1024GB
Drive3 : 2048GB
"""

matches = re.finditer(r"\d+GB", log)

for match in matches:
    print(match)
```

Application

- Capacity Analysis
- Storage Report Processing

---

# Linux Automation Example

```python
import re

output = """
inet 192.168.1.10
inet 10.10.20.15
"""

matches = re.finditer(r"\d+\.\d+\.\d+\.\d+", output)

for match in matches:
    print(match)
```

Application

- IP Address Processing
- Network Monitoring

---

# Python Automation Example

```python
import re

report = """
PASS
FAIL
PASS
"""

matches = re.finditer(r"PASS|FAIL", report)

for match in matches:
    print(match)
```

Application

- Report Processing
- Test Result Analysis

---

# Compare

| Feature | `re.findall()` | `re.finditer()` |
|---------|----------------|-----------------|
| Searches entire string | ✅ Yes | ✅ Yes |
| Finds all matches | ✅ Yes | ✅ Yes |
| Returns List | ✅ Yes | ❌ No |
| Returns Iterator | ❌ No | ✅ Yes |
| Returns Match Objects | ❌ No | ✅ Yes |

---

# Regex Engine Comparison

## `re.findall()`

```
Search

↓

Collect Strings

↓

Return List
```

---

## `re.finditer()`

```
Search

↓

Create Match Objects

↓

Return Iterator
```

---

# Important Observation

Use

```python
re.findall()
```

when only the matched text is required.

Use

```python
re.finditer()
```

when detailed match information such as

- positions
- spans
- captured groups

is required.

---

# Common Beginner Mistakes

### Mistake 1

Expecting `re.finditer()` to return a list.

It returns an iterator.

---

### Mistake 2

Printing the iterator directly instead of iterating through it.

---

### Mistake 3

Using `re.findall()` when Match Objects are actually required.

---

# Interview Questions

1. What is the purpose of `re.finditer()`?

2. What does `re.finditer()` return?

3. How does `re.finditer()` differ from `re.findall()`?

4. Why does `re.finditer()` return Match Objects?

5. Give practical applications of `re.finditer()`.

---

# Practice Questions

### Question 1

Write a Python program that prints every Match Object produced by `re.finditer()`.

---

### Question 2

Explain why `re.finditer()` is useful for log processing.

---

### Question 3

List five situations where `re.finditer()` is preferred over `re.findall()`.

---

# Memory Tip

```
re.finditer()

↓

Search Everything

↓

Create Match Objects

↓

Return Iterator
```

Remember

```
findall()

↓

Strings

--------------------

finditer()

↓

Match Objects
```

---

# Revision Box

✔ `re.finditer()` searches the entire input string.

✔ It returns an iterator.

✔ Each element produced by the iterator is a Match Object.

✔ It is useful when detailed match information is required.

✔ It is widely used in enterprise automation.

---

# Key Takeaways

- `re.finditer()` retrieves every non-overlapping match as Match Objects.
- It returns an iterator instead of a list.
- Match Objects provide access to positions, spans and captured groups.
- It is preferred over `re.findall()` when detailed match information is needed.
- `re.finditer()` is one of the most important functions for professional automation scripts.

---

# Coming Up

So far, we have learned that Match Objects contain detailed information about each successful match.

The next lessons explore the methods provided by Match Objects, beginning with **`group()`**, which retrieves the actual matched text from a Match Object.

------------------------------------------------------------------------------------------------------------

# 6.10 `group()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of the `group()` method.
- Explain why `group()` is used with Match Objects.
- Retrieve the matched text from a Match Object.
- Apply `group()` in Storage Engineering, Linux Automation and Test Automation.
- Recognize situations where `group()` is required.

---

# Previous Knowledge

In the previous lessons, we learned that functions such as

```python
re.search()

re.match()

re.fullmatch()

re.finditer()
```

return **Match Objects**.

A Match Object stores information about a successful match.

However,

the Match Object itself is **not** the matched text.

To retrieve the matched text,

we use

```python
group()
```

---

# Introduction

Suppose we search a storage log.

```python
import re

text = "Capacity : 2048GB"

match = re.search(r"\d+GB", text)

print(match)
```

Output

```text
<re.Match object; span=(11, 17), match='2048GB'>
```

This is useful,

but suppose we only want

```text
2048GB
```

How do we retrieve it?

The answer is

```python
group()
```

---

# Why Do We Need `group()`?

The Match Object stores many pieces of information.

Examples include

- Matched Text
- Start Position
- End Position
- Span
- Captured Groups

Sometimes,

we need only the matched text.

Instead of returning the entire Match Object,

Python allows us to retrieve the matched text using

```python
group()
```

---

# Definition

The `group()` method returns the text matched by the Regular Expression.

It is called on a **Match Object**.

If the Match Object represents a successful match,

`group()` returns the matched string.

---

# Syntax

```python
match.group()
```

---

# Method Reference

| Property | Value |
|----------|-------|
| Method | `group()` |
| Called On | Match Object |
| Returns | Matched Text (`str`) |
| Requires Successful Match? | ✅ Yes |

---

# Parameters

Basic form

```python
group()
```

No arguments are required to retrieve the complete matched text.

*(Captured groups will be studied in later lessons.)*

---

# Return Value

```
Successful Match

↓

Matched Text

------------------------

No Match Object

↓

AttributeError
```

Therefore,

always ensure that the Match Object is **not `None`** before calling `group()`.

---

# Python Execution Flow

```
Write Pattern

↓

Call

re.search()

↓

Match Object

↓

Call

group()

↓

Matched Text
```

---

# Regex Engine Explanation

```
Regex Engine

↓

Pattern Found

↓

Create Match Object

↓

Python Calls

group()

↓

Return Matched Text
```

Notice that

the Regex Engine has already finished its work.

`group()` simply retrieves information already stored inside the Match Object.

---

# Engine Visualization

```
Regex Engine

      │
      ▼

+------------------+
|  Match Object    |
+------------------+

      │
      ▼

 group()

      │
      ▼

Matched Text
```

---

# Python Code Example

```python
import re

text = "Capacity : 2048GB"

match = re.search(r"\d+GB", text)

print(match.group())
```

Output

```text
2048GB
```

---

# Python Console Example

```python
>>> import re
>>> text = "Capacity : 2048GB"
>>> match = re.search(r"\d+GB", text)
>>> match.group()
'2048GB'
```

---

# Example — Safe Usage

```python
import re

text = "Temperature : 42C"

match = re.search(r"\d+GB", text)

if match:
    print(match.group())
else:
    print("No Match Found")
```

Output

```text
No Match Found
```

This avoids calling `group()` on `None`.

---

# Storage Engineering Example

```python
import re

log = "Capacity : 4096GB"

match = re.search(r"\d+GB", log)

print(match.group())
```

Output

```text
4096GB
```

Application

- Capacity Extraction
- Storage Report Generation

---

# Linux Automation Example

```python
import re

output = "inet 192.168.1.20/24"

match = re.search(r"\d+\.\d+\.\d+\.\d+", output)

print(match.group())
```

Output

```text
192.168.1.20
```

Application

- IP Address Extraction
- Network Automation

---

# Python Automation Example

```python
import re

report = "Status : PASS"

match = re.search(r"PASS", report)

print(match.group())
```

Output

```text
PASS
```

Application

- Test Report Processing
- Result Validation

---

# Important Observation

The Match Object contains the matched text,

but it does **not** automatically display it.

The `group()` method retrieves the matched text from the Match Object.

Think of it as

```
Match Object

↓

group()

↓

Matched Text
```

---

# Common Beginner Mistakes

### Mistake 1

Trying to call

```python
group()
```

when the Match Object is

```python
None
```

---

### Mistake 2

Printing the Match Object when only the matched text is required.

---

### Mistake 3

Thinking `group()` performs the search.

The search has already been completed.

`group()` only retrieves stored information.

---

# Interview Questions

1. What is the purpose of `group()`?

2. Why is `group()` called on a Match Object?

3. What does `group()` return?

4. Why should we check for `None` before calling `group()`?

5. Does `group()` execute the Regular Expression?

---

# Practice Questions

### Question 1

Write a Python program that extracts a storage capacity using `group()`.

---

### Question 2

Explain why calling

```python
match.group()
```

on

```python
None
```

causes an error.

---

### Question 3

Describe the relationship between the Regex Engine, Match Object and `group()`.

---

# Memory Tip

```
Regex Engine

↓

Match Object

↓

group()

↓

Matched Text
```

Remember

```
group()

Does NOT

Search

It

Retrieves
```

---

# Revision Box

✔ `group()` is a Match Object method.

✔ It returns the matched text.

✔ It requires a successful Match Object.

✔ Calling `group()` on `None` causes an error.

✔ `group()` retrieves information; it does not perform matching.

---

# Key Takeaways

- `group()` is the primary method used to retrieve matched text from a Match Object.
- It is called only after a successful Regular Expression match.
- Always verify that the Match Object is not `None` before calling `group()`.
- `group()` is one of the most frequently used methods in Python Regex programming.
- Understanding `group()` is essential before learning other Match Object methods.

---

# Coming Up

The next lesson introduces **`start()`**, which returns the **starting position** of the matched text within the input string.

This method is widely used in log parsing, text highlighting and report generation.

------------------------------------------------------------------------------------------------------------

# 6.11 `start()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of the `start()` method.
- Retrieve the starting position of a match.
- Explain how `start()` differs from `group()`.
- Apply `start()` in log parsing and automation.
- Understand why match positions are useful.

---

# Previous Knowledge

In the previous lesson, we learned that

```python
group()
```

returns the matched text.

Example

```python
match.group()
```

Output

```text
2048GB
```

Now suppose we want to know

> Where does this match begin?

For that,

Python provides

```python
start()
```

---

# Introduction

Suppose we search

```python
import re

text = "Capacity : 2048GB"

match = re.search(r"\d+GB", text)
```

We already know

```python
match.group()
```

returns

```text
2048GB
```

But where does

```
2048GB
```

begin inside the string?

The answer is obtained using

```python
start()
```

---

# Why Do We Need `start()`?

Many automation tasks require knowing the exact location of a match.

Examples

- Highlight matched text
- Parse log files
- Annotate reports
- Display error locations
- Modify specific text

For these tasks,

the starting position is essential.

---

# Definition

The `start()` method returns the **starting index** of the matched text within the input string.

It is called on a **Match Object**.

---

# Syntax

```python
match.start()
```

---

# Method Reference

| Property | Value |
|----------|-------|
| Method | `start()` |
| Called On | Match Object |
| Returns | Integer (`int`) |
| Meaning | Starting index of the match |
| Requires Successful Match? | ✅ Yes |

---

# Return Value

```
Successful Match

↓

Starting Index

------------------------

No Match Object

↓

AttributeError
```

Always verify that the Match Object is not `None` before calling `start()`.

---

# Understanding String Indexing

Input

```text
Capacity : 2048GB
```

Character Positions

```text
C a p a c i t y   :   2 0 4 8 G B
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
                      ↑
                 Match Starts
```

The matched text

```text
2048GB
```

begins at index

```text
11
```

---

# Python Execution Flow

```
Regex Engine

↓

Match Object

↓

start()

↓

Starting Index
```

---

# Regex Engine Explanation

```
Regex Engine

↓

Pattern Found

↓

Create Match Object

↓

Store Start Position

↓

Python Calls

start()

↓

Return Starting Index
```

The Regex Engine records the starting position during matching.

The `start()` method simply retrieves it.

---

# Engine Visualization

```
Regex Engine

      │
      ▼

+------------------+
|  Match Object    |
+------------------+

      │
      ▼

 start()

      │
      ▼

Starting Index
```

---

# Python Code Example

```python
import re

text = "Capacity : 2048GB"

match = re.search(r"\d+GB", text)

print(match.start())
```

Output

```text
11
```

---

# Python Console Example

```python
>>> import re
>>> text = "Capacity : 2048GB"
>>> match = re.search(r"\d+GB", text)
>>> match.start()
11
```

---

# Storage Engineering Example

```python
import re

log = "Capacity : 4096GB"

match = re.search(r"\d+GB", log)

print(match.start())
```

Output

```text
11
```

Application

- Storage Log Parsing
- Capacity Location Tracking

---

# Linux Automation Example

```python
import re

output = "inet 192.168.1.20/24"

match = re.search(r"\d+\.\d+\.\d+\.\d+", output)

print(match.start())
```

Application

- Network Output Parsing
- IP Position Detection

---

# Python Automation Example

```python
import re

report = "Status : PASS"

match = re.search(r"PASS", report)

print(match.start())
```

Output

```text
9
```

Application

- Report Analysis
- Text Highlighting

---

# Compare

| Method | Returns |
|---------|----------|
| `group()` | Matched text |
| `start()` | Starting index |

---

# Important Observation

`start()` does **not** return the matched text.

It returns **where the matched text begins**.

Think of it as

```
Match Object

↓

start()

↓

Beginning Position
```

---

# Common Beginner Mistakes

### Mistake 1

Expecting `start()` to return the matched string.

It returns an integer.

---

### Mistake 2

Calling `start()` on `None`.

---

### Mistake 3

Confusing character positions with word positions.

`start()` returns the **character index**.

---

# Interview Questions

1. What is the purpose of `start()`?

2. What data type does `start()` return?

3. Why is `start()` useful in automation?

4. What happens if `start()` is called on `None`?

5. How does `start()` differ from `group()`?

---

# Practice Questions

### Question 1

Write a Python program that prints the starting position of a storage capacity.

---

### Question 2

Explain how `start()` can be used in log parsing.

---

### Question 3

Describe the difference between `group()` and `start()`.

---

# Memory Tip

```
Match Object

↓

start()

↓

Beginning Index
```

Remember

```
group()

↓

What Matched

--------------------

start()

↓

Where It Begins
```

---

# Revision Box

✔ `start()` returns the starting index of a match.

✔ It is a Match Object method.

✔ It returns an integer.

✔ It requires a successful Match Object.

✔ It is useful for locating matches within text.

---

# Key Takeaways

- `start()` retrieves the starting position of the matched text.
- It is commonly used in log parsing, highlighting and report generation.
- It complements `group()` by providing location instead of content.
- The Regex Engine records the starting position during matching.
- Understanding `start()` prepares us for `end()` and `span()`.

---

# Coming Up

The next lesson introduces **`end()`**, which returns the **ending position** of the matched text, allowing us to determine the complete range of a match before combining both values using **`span()`**.

------------------------------------------------------------------------------------------------------------

# 6.12 `end()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of the `end()` method.
- Retrieve the ending position of a match.
- Explain how `end()` differs from `start()`.
- Apply `end()` in log parsing and automation.
- Understand why ending positions are useful.

---

# Previous Knowledge

In the previous lesson, we learned that

```python
start()
```

returns the **starting index** of the matched text.

Example

```python
match.start()
```

Output

```text
11
```

Now we will learn how to determine

> Where does the match end?

For that,

Python provides

```python
end()
```

---

# Introduction

Suppose we search

```python
import re

text = "Capacity : 2048GB"

match = re.search(r"\d+GB", text)
```

We already know

```python
match.group()
```

returns

```text
2048GB
```

and

```python
match.start()
```

returns

```text
11
```

Now we want to know

> Where does this match end?

The answer is

```python
match.end()
```

---

# Why Do We Need `end()`?

Many automation tasks require knowing where a match finishes.

Examples

- Highlight matched text
- Replace only the matched portion
- Extract surrounding text
- Calculate match length
- Parse structured logs

---

# Definition

The `end()` method returns the **ending index** of the matched text.

The returned index is **one position after the last matched character**.

It is called on a **Match Object**.

---

# Syntax

```python
match.end()
```

---

# Method Reference

| Property | Value |
|----------|-------|
| Method | `end()` |
| Called On | Match Object |
| Returns | Integer (`int`) |
| Meaning | Ending index (exclusive) |
| Requires Successful Match? | ✅ Yes |

---

# Return Value

```
Successful Match

↓

Ending Index

------------------------

No Match Object

↓

AttributeError
```

Always verify that the Match Object is not `None` before calling `end()`.

---

# Understanding the Ending Index

Input

```text
Capacity : 2048GB
```

Character Positions

```text
C a p a c i t y   :   2 0 4 8 G B
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
                      └──────────────┘
                           Match

Returned by

start() → 11

end() → 17
```

Notice that

```
17
```

is **not** the index of

```
B
```

It is the position **immediately after** the last matched character.

---

# Why Is the Ending Index Exclusive?

Python uses the same indexing rule for string slicing.

For example,

```python
text[11:17]
```

returns

```text
2048GB
```

Notice that

```python
17
```

is excluded from the slice.

The `end()` method follows the same convention.

---

# Python Execution Flow

```
Regex Engine

↓

Match Object

↓

end()

↓

Ending Index
```

---

# Regex Engine Explanation

```
Regex Engine

↓

Pattern Found

↓

Store Ending Position

↓

Python Calls

end()

↓

Return Ending Index
```

The Regex Engine records the ending position while matching.

The `end()` method retrieves that stored value.

---

# Engine Visualization

```
Regex Engine

      │
      ▼

+------------------+
|  Match Object    |
+------------------+

      │
      ▼

 end()

      │
      ▼

Ending Index
```

---

# Python Code Example

```python
import re

text = "Capacity : 2048GB"

match = re.search(r"\d+GB", text)

print(match.end())
```

Output

```text
17
```

---

# Python Console Example

```python
>>> import re
>>> text = "Capacity : 2048GB"
>>> match = re.search(r"\d+GB", text)
>>> match.end()
17
```

---

# Storage Engineering Example

```python
import re

log = "Capacity : 4096GB"

match = re.search(r"\d+GB", log)

print(match.end())
```

Output

```text
17
```

Application

- Storage Log Parsing
- Capacity Position Tracking

---

# Linux Automation Example

```python
import re

output = "inet 192.168.1.20/24"

match = re.search(r"\d+\.\d+\.\d+\.\d+", output)

print(match.end())
```

Application

- Network Output Processing
- IP Range Detection

---

# Python Automation Example

```python
import re

report = "Status : PASS"

match = re.search(r"PASS", report)

print(match.end())
```

Application

- Report Analysis
- Text Processing

---

# Compare

| Method | Returns |
|---------|----------|
| `group()` | Matched text |
| `start()` | Starting index |
| `end()` | Ending index (exclusive) |

---

# Important Observation

`end()` does **not** return the index of the last matched character.

Instead,

it returns the position **immediately after** the match.

This makes it consistent with Python string slicing.

```
Match Object

↓

end()

↓

Exclusive Ending Index
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking `end()` returns the index of the last matched character.

It returns the position immediately after it.

---

### Mistake 2

Calling `end()` on `None`.

---

### Mistake 3

Confusing inclusive and exclusive indexes.

Python uses **exclusive ending indexes**.

---

# Interview Questions

1. What is the purpose of `end()`?

2. What data type does `end()` return?

3. Why is the ending index exclusive?

4. How does `end()` differ from `start()`?

5. Why is `end()` useful in automation?

---

# Practice Questions

### Question 1

Write a Python program that prints the ending position of a storage capacity.

---

### Question 2

Explain why `match.end()` returns `17` instead of `16`.

---

### Question 3

Describe the relationship between `end()` and Python string slicing.

---

# Memory Tip

```
Match Object

↓

end()

↓

Exclusive

Ending Index
```

Remember

```
start()

↓

Beginning

-------------------

end()

↓

One Position

After

The Match
```

---

# Revision Box

✔ `end()` returns the ending index of the match.

✔ The ending index is exclusive.

✔ It returns an integer.

✔ It is a Match Object method.

✔ It follows Python's string slicing convention.

---

# Key Takeaways

- `end()` returns the exclusive ending position of a matched string.
- It complements `start()` by identifying where the match finishes.
- The exclusive ending index matches Python's string slicing behavior.
- It is useful for text extraction, highlighting and automation.
- Understanding `end()` prepares us for `span()`, which returns both positions together.

---

# Coming Up

The next lesson introduces **`span()`**, which combines both **`start()`** and **`end()`** into a single method, returning the complete range of the matched text.

------------------------------------------------------------------------------------------------------------

# 6.13 `span()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of the `span()` method.
- Retrieve both the starting and ending positions of a match.
- Explain how `span()` relates to `start()` and `end()`.
- Apply `span()` in text processing and automation.
- Understand why `span()` is useful for slicing strings.

---

# Previous Knowledge

In the previous lessons, we learned

```python
match.start()
```

returns

```text
11
```

and

```python
match.end()
```

returns

```text
17
```

Now suppose we want both values together.

Instead of calling

```python
match.start()

match.end()
```

Python provides

```python
match.span()
```

---

# Introduction

Suppose we search

```python
import re

text = "Capacity : 2048GB"

match = re.search(r"\d+GB", text)
```

Calling

```python
match.start()
```

returns

```text
11
```

Calling

```python
match.end()
```

returns

```text
17
```

Calling

```python
match.span()
```

returns

```text
(11, 17)
```

---

# Why Do We Need `span()`?

Many automation tasks require both positions.

Examples

- Highlight matched text
- Slice strings
- Generate reports
- Record match locations
- Process log files

Instead of calling two methods,

`span()` retrieves both values at once.

---

# Definition

The `span()` method returns a tuple containing the **starting index** and the **exclusive ending index** of the matched text.

It is called on a **Match Object**.

---

# Syntax

```python
match.span()
```

---

# Method Reference

| Property | Value |
|----------|-------|
| Method | `span()` |
| Called On | Match Object |
| Returns | Tuple (`start`, `end`) |
| Requires Successful Match? | ✅ Yes |

---

# Return Value

```
Successful Match

↓

(Start, End)

------------------------

No Match Object

↓

AttributeError
```

Always verify that the Match Object is not `None` before calling `span()`.

---

# Understanding `span()`

Input

```text
Capacity : 2048GB
```

Character Positions

```text
C a p a c i t y   :   2 0 4 8 G B
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
                      └──────────────┘
                      Match
```

Methods

```python
match.start()
```

Output

```text
11
```

```python
match.end()
```

Output

```text
17
```

```python
match.span()
```

Output

```text
(11, 17)
```

---

# Relationship with Python String Slicing

Suppose

```python
text = "Capacity : 2048GB"
```

Then

```python
start, end = match.span()

print(text[start:end])
```

Output

```text
2048GB
```

Notice how `span()` works naturally with Python slicing.

---

# Python Execution Flow

```
Regex Engine

↓

Match Object

↓

span()

↓

(Start, End)

↓

Tuple Returned
```

---

# Regex Engine Explanation

```
Regex Engine

↓

Pattern Found

↓

Store Start Position

↓

Store End Position

↓

Python Calls

span()

↓

Return Tuple
```

The Regex Engine stores both positions during matching.

The `span()` method simply returns them together.

---

# Engine Visualization

```
Regex Engine

      │
      ▼

+------------------+
|  Match Object    |
+------------------+

      │
      ▼

 span()

      │
      ▼

(Start, End)
```

---

# Python Code Example

```python
import re

text = "Capacity : 2048GB"

match = re.search(r"\d+GB", text)

print(match.span())
```

Output

```text
(11, 17)
```

---

# Python Console Example

```python
>>> import re
>>> text = "Capacity : 2048GB"
>>> match = re.search(r"\d+GB", text)
>>> match.span()
(11, 17)
```

---

# Storage Engineering Example

```python
import re

log = "Capacity : 4096GB"

match = re.search(r"\d+GB", log)

print(match.span())
```

Output

```text
(11, 17)
```

Application

- Storage Log Parsing
- Capacity Location Tracking

---

# Linux Automation Example

```python
import re

output = "inet 192.168.1.20/24"

match = re.search(r"\d+\.\d+\.\d+\.\d+", output)

print(match.span())
```

Application

- Network Log Processing
- IP Position Tracking

---

# Python Automation Example

```python
import re

report = "Status : PASS"

match = re.search(r"PASS", report)

print(match.span())
```

Application

- Report Processing
- Text Highlighting

---

# Compare

| Method | Returns |
|---------|----------|
| `group()` | Matched text |
| `start()` | Starting index |
| `end()` | Exclusive ending index |
| `span()` | (`start`, `end`) tuple |

---

# Visual Comparison

```
Capacity : 2048GB
           └──────┘
           11    17

group()  → "2048GB"

start()  → 11

end()    → 17

span()   → (11, 17)

text[11:17] → "2048GB"
```

---

# Important Observation

`span()` does not calculate anything new.

It simply combines the values returned by

```python
match.start()

match.end()
```

into a single tuple.

Think of it as

```
start()

+

end()

↓

span()
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking `span()` returns the matched text.

It returns positions, not content.

---

### Mistake 2

Assuming the ending value is inclusive.

The ending index remains **exclusive**, just like `end()`.

---

### Mistake 3

Calling `span()` on `None`.

---

# Interview Questions

1. What is the purpose of `span()`?

2. What does `span()` return?

3. How is `span()` related to `start()` and `end()`?

4. Why is `span()` useful with Python string slicing?

5. What happens if `span()` is called on `None`?

---

# Practice Questions

### Question 1

Write a Python program that prints the tuple returned by `span()`.

---

### Question 2

Use `span()` to extract the matched text using string slicing.

---

### Question 3

Explain why `span()` is convenient compared to calling `start()` and `end()` separately.

---

# Memory Tip

```
Match Object

↓

span()

↓

(Start, End)
```

Remember

```
start()

+

end()

=

span()
```

---

# Revision Box

✔ `span()` returns both the starting and ending positions.

✔ The return type is a tuple.

✔ The ending index is exclusive.

✔ `span()` is useful for Python string slicing.

✔ It combines the information from `start()` and `end()`.

---

# Key Takeaways

- `span()` returns a tuple containing the starting and exclusive ending positions of a match.
- It combines the functionality of `start()` and `end()`.
- It integrates naturally with Python string slicing.
- It is widely used in log parsing, highlighting and text processing.
- Understanding `span()` completes the core Match Object position methods.

---

# Coming Up

So far, we have learned how to retrieve:

- The matched text using `group()`
- The starting position using `start()`
- The ending position using `end()`
- Both positions using `span()`

The next lesson introduces **`groups()`**, which retrieves **captured groups** from a Match Object and begins our exploration of advanced group handling in Python.

------------------------------------------------------------------------------------------------------------

# 6.14 `groups()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of the `groups()` method.
- Explain how `groups()` differs from `group()`.
- Retrieve all captured groups from a Match Object.
- Understand the relationship between Capturing Groups and `groups()`.
- Apply `groups()` in automation tasks.

---

# Previous Knowledge

In Chapter 4, we learned about **Capturing Groups**.

Example

```regex
(\d+)(GB)
```

This pattern creates two capturing groups.

In previous lessons, we used

```python
match.group()
```

which returned the **entire matched text**.

Now we will learn how to retrieve **every captured group individually**.

---

# Introduction

Suppose we search

```python
import re

text = "2048GB"

match = re.search(r"(\d+)(GB)", text)
```

The pattern contains

```
Group 1

↓

(\d+)

------------------

Group 2

↓

(GB)
```

The complete match is

```text
2048GB
```

But suppose we want

```text
2048

GB
```

separately.

The solution is

```python
groups()
```

---

# Why Do We Need `groups()`?

Many automation tasks require processing different parts of a match independently.

Examples

- Capacity value
- Capacity unit
- Date components
- Version numbers
- Device identifiers

Capturing Groups divide a match into logical parts.

`groups()` retrieves all of them together.

---

# Definition

The `groups()` method returns a **tuple containing all captured groups** from a successful Match Object.

Each element of the tuple corresponds to one capturing group in the Regular Expression.

---

# Syntax

```python
match.groups()
```

---

# Method Reference

| Property | Value |
|----------|-------|
| Method | `groups()` |
| Called On | Match Object |
| Returns | Tuple |
| Requires Capturing Groups? | ✅ Yes |
| Requires Successful Match? | ✅ Yes |

---

# Return Value

```
Successful Match

↓

Captured Groups

↓

Tuple

------------------------

No Capturing Groups

↓

()
```

If the Regular Expression contains **no capturing groups**,

`groups()` returns an empty tuple.

---

# Understanding Capturing Groups

Pattern

```regex
(\d+)(GB)
```

Input

```text
2048GB
```

Captured Groups

```
Group 1

↓

2048

--------------------

Group 2

↓

GB
```

Therefore

```python
match.groups()
```

returns

```python
('2048', 'GB')
```

---

# Python Execution Flow

```
Regex Engine

↓

Pattern Matched

↓

Store Captured Groups

↓

Match Object

↓

groups()

↓

Tuple Returned
```

---

# Regex Engine Explanation

```
Regex Engine

↓

Successful Match

↓

Capture Group 1

↓

Capture Group 2

↓

Store Groups

↓

Python Calls

groups()

↓

Return Tuple
```

The Regex Engine stores every captured group during matching.

The `groups()` method retrieves them.

---

# Engine Visualization

```
Regex Engine

      │
      ▼

+------------------+
|  Match Object    |
+------------------+

      │
      ▼

 groups()

      │
      ▼

('2048', 'GB')
```

---

# Python Code Example

```python
import re

text = "2048GB"

match = re.search(r"(\d+)(GB)", text)

print(match.groups())
```

Output

```python
('2048', 'GB')
```

---

# Python Console Example

```python
>>> import re
>>> match = re.search(r"(\d+)(GB)", "2048GB")
>>> match.groups()
('2048', 'GB')
```

---

# Example — No Capturing Groups

```python
import re

match = re.search(r"\d+GB", "2048GB")

print(match.groups())
```

Output

```python
()
```

No capturing groups exist,

so an empty tuple is returned.

---

# Storage Engineering Example

```python
import re

log = "Capacity : 4096GB"

match = re.search(r"(\d+)(GB)", log)

print(match.groups())
```

Output

```python
('4096', 'GB')
```

Application

- Separate Capacity Value
- Separate Unit

---

# Linux Automation Example

```python
import re

output = "Kernel 6.8"

match = re.search(r"(\d+)\.(\d+)", output)

print(match.groups())
```

Output

```python
('6', '8')
```

Application

- Kernel Version Parsing

---

# Python Automation Example

```python
import re

report = "Version=3.5.12"

match = re.search(r"(\d+)\.(\d+)\.(\d+)", report)

print(match.groups())
```

Output

```python
('3', '5', '12')
```

Application

- Version Processing
- Report Analysis

---

# Compare

| Method | Returns |
|---------|----------|
| `group()` | Entire matched text |
| `groups()` | Tuple of captured groups |

---

# Visual Comparison

Pattern

```regex
(\d+)(GB)
```

Input

```text
2048GB
```

```
group()

↓

2048GB

--------------------

groups()

↓

('2048', 'GB')
```

---

# Important Observation

`groups()` returns **only captured groups**.

It does **not** return the complete matched text.

To retrieve the entire match,

use

```python
group()
```

---

# Common Beginner Mistakes

### Mistake 1

Expecting `groups()` to return the entire match.

It returns only captured groups.

---

### Mistake 2

Using `groups()` when the pattern contains no capturing groups.

---

### Mistake 3

Confusing

```python
group()
```

with

```python
groups()
```

---

# Interview Questions

1. What is the purpose of `groups()`?

2. What does `groups()` return?

3. What happens if the pattern contains no capturing groups?

4. How does `groups()` differ from `group()`?

5. Give practical applications of `groups()`.

---

# Practice Questions

### Question 1

Write a Python program that extracts a capacity value and its unit separately.

---

### Question 2

Explain why

```python
match.groups()
```

returns an empty tuple when no capturing groups exist.

---

### Question 3

List five situations where `groups()` is useful.

---

# Memory Tip

```
group()

↓

Entire Match

----------------------

groups()

↓

Captured Groups
```

Remember

```
One Match

↓

group()

Many Groups

↓

groups()
```

---

# Revision Box

✔ `groups()` returns a tuple of captured groups.

✔ It requires capturing groups in the pattern.

✔ It is a Match Object method.

✔ Without capturing groups, it returns an empty tuple.

✔ It is useful for structured data extraction.

---

# Key Takeaways

- `groups()` retrieves every captured group from a Match Object.
- It returns a tuple rather than a string.
- It complements `group()` by providing access to individual captured components.
- It is widely used for parsing structured values such as versions, capacities and dates.
- Understanding `groups()` prepares us for working with named capturing groups using `groupdict()`.

---

# Coming Up

The next lesson introduces **`groupdict()`**, which retrieves **named capturing groups** as a Python dictionary, making complex Regular Expressions much easier to understand and maintain.

------------------------------------------------------------------------------------------------------------

# 6.15 `groupdict()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of the `groupdict()` method.
- Explain how named capturing groups work.
- Retrieve named groups as a Python dictionary.
- Compare `groupdict()` with `group()` and `groups()`.
- Apply `groupdict()` in enterprise automation.

---

# Previous Knowledge

In Chapter 4, we learned about **Named Capturing Groups**.

Example

```regex
(?P<capacity>\d+)(?P<unit>GB)
```

Unlike ordinary capturing groups,

each group has a meaningful name.

In the previous lesson,

```python
groups()
```

returned

```python
('2048', 'GB')
```

But suppose we want

```python
{
    'capacity': '2048',
    'unit': 'GB'
}
```

Python provides

```python
groupdict()
```

---

# Introduction

Suppose we search

```python
import re

text = "2048GB"

match = re.search(
    r"(?P<capacity>\d+)(?P<unit>GB)",
    text
)
```

The Regular Expression contains two named groups.

```
capacity

↓

2048

----------------------

unit

↓

GB
```

Instead of remembering

```
Group 1

Group 2
```

we can access them by name.

---

# Why Do We Need `groupdict()`?

Large enterprise Regular Expressions often contain many capturing groups.

Remembering

```
Group 1

Group 2

Group 3

...

Group 12
```

is difficult.

Named groups make Regular Expressions easier to read,

and `groupdict()` retrieves them as a Python dictionary.

---

# Definition

The `groupdict()` method returns a **dictionary containing all named capturing groups** from a successful Match Object.

The dictionary keys are the group names.

The dictionary values are the corresponding matched strings.

---

# Syntax

```python
match.groupdict()
```

---

# Method Reference

| Property | Value |
|----------|-------|
| Method | `groupdict()` |
| Called On | Match Object |
| Returns | Dictionary (`dict`) |
| Requires Named Groups? | ✅ Yes |
| Requires Successful Match? | ✅ Yes |

---

# Return Value

```
Successful Match

↓

Named Groups

↓

Dictionary

------------------------

No Named Groups

↓

{}
```

If the Regular Expression contains no named groups,

`groupdict()` returns an empty dictionary.

---

# Understanding Named Groups

Pattern

```regex
(?P<capacity>\d+)(?P<unit>GB)
```

Input

```text
2048GB
```

Named Groups

```
capacity

↓

2048

----------------------

unit

↓

GB
```

Therefore

```python
match.groupdict()
```

returns

```python
{
    'capacity': '2048',
    'unit': 'GB'
}
```

---

# Python Execution Flow

```
Regex Engine

↓

Pattern Matched

↓

Store Named Groups

↓

Match Object

↓

groupdict()

↓

Dictionary Returned
```

---

# Regex Engine Explanation

```
Regex Engine

↓

Successful Match

↓

Capture Named Groups

↓

Store Group Names

↓

Store Values

↓

Python Calls

groupdict()

↓

Return Dictionary
```

The Regex Engine stores both

- group names
- matched values

inside the Match Object.

---

# Engine Visualization

```
Regex Engine

      │
      ▼

+------------------+
|  Match Object    |
+------------------+

      │
      ▼

 groupdict()

      │
      ▼

{
 capacity : 2048

 unit : GB
}
```

---

# Python Code Example

```python
import re

text = "2048GB"

match = re.search(
    r"(?P<capacity>\d+)(?P<unit>GB)",
    text
)

print(match.groupdict())
```

Output

```python
{
    'capacity': '2048',
    'unit': 'GB'
}
```

---

# Python Console Example

```python
>>> import re
>>> match = re.search(
...     r"(?P<capacity>\d+)(?P<unit>GB)",
...     "2048GB"
... )
>>> match.groupdict()
{'capacity': '2048', 'unit': 'GB'}
```

---

# Example — No Named Groups

```python
import re

match = re.search(r"(\d+)(GB)", "2048GB")

print(match.groupdict())
```

Output

```python
{}
```

The pattern contains capturing groups,

but none of them are named.

---

# Storage Engineering Example

```python
import re

log = "Capacity : 4096GB"

match = re.search(
    r"(?P<capacity>\d+)(?P<unit>GB)",
    log
)

print(match.groupdict())
```

Output

```python
{
    'capacity': '4096',
    'unit': 'GB'
}
```

Application

- Capacity Parsing
- Structured Report Generation

---

# Linux Automation Example

```python
import re

output = "Kernel 6.8"

match = re.search(
    r"(?P<major>\d+)\.(?P<minor>\d+)",
    output
)

print(match.groupdict())
```

Output

```python
{
    'major': '6',
    'minor': '8'
}
```

Application

- Version Parsing
- Configuration Validation

---

# Python Automation Example

```python
import re

report = "Version=3.5.12"

match = re.search(
    r"(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)",
    report
)

print(match.groupdict())
```

Output

```python
{
    'major': '3',
    'minor': '5',
    'patch': '12'
}
```

Application

- Software Version Processing
- Automated Report Parsing

---

# Compare

| Method | Returns |
|---------|----------|
| `group()` | Entire matched text |
| `groups()` | Tuple of captured groups |
| `groupdict()` | Dictionary of named groups |

---

# Visual Comparison

Pattern

```regex
(?P<capacity>\d+)(?P<unit>GB)
```

Input

```text
2048GB
```

```
group()

↓

2048GB

---------------------

groups()

↓

('2048', 'GB')

---------------------

groupdict()

↓

{
 capacity : 2048

 unit : GB
}
```

---

# Important Observation

`groupdict()` works **only with named capturing groups**.

Unnamed capturing groups are ignored.

Think of it as

```
Named Groups

↓

Dictionary

↓

Easy To Read

↓

Easy To Maintain
```

---

# Common Beginner Mistakes

### Mistake 1

Expecting `groupdict()` to return unnamed capturing groups.

It returns only named groups.

---

### Mistake 2

Using `groupdict()` when no named groups exist.

It returns an empty dictionary.

---

### Mistake 3

Confusing `groups()` with `groupdict()`.

`groups()` returns a tuple.

`groupdict()` returns a dictionary.

---

# Interview Questions

1. What is the purpose of `groupdict()`?

2. What does `groupdict()` return?

3. What happens if no named groups exist?

4. How does `groupdict()` differ from `groups()`?

5. Why are named groups useful in enterprise automation?

---

# Practice Questions

### Question 1

Write a Python program that extracts a capacity value and unit using named capturing groups.

---

### Question 2

Explain why `groupdict()` improves code readability.

---

### Question 3

List five situations where named capturing groups are preferred.

---

# Memory Tip

```
group()

↓

Entire Match

--------------------

groups()

↓

Tuple

--------------------

groupdict()

↓

Dictionary
```

Remember

```
Named Groups

↓

Named Dictionary
```

---

# Revision Box

✔ `groupdict()` returns a dictionary.

✔ It retrieves only named capturing groups.

✔ Without named groups, it returns `{}`.

✔ Dictionary keys are group names.

✔ Dictionary values are matched strings.

---

# Key Takeaways

- `groupdict()` retrieves named capturing groups as a Python dictionary.
- It improves readability by replacing numeric group indexes with meaningful names.
- It is especially valuable in large Regular Expressions used in enterprise automation.
- Unnamed capturing groups are not included in the returned dictionary.
- `groupdict()` completes the core Match Object retrieval methods.

---

# Coming Up

Before moving to the text-processing functions (`re.sub()`, `re.split()`, and `re.compile()`),

the next lesson provides a **Master Match Object Summary**, comparing every Match Object method learned so far, with diagrams, comparison tables, interview questions and a one-page revision sheet.

------------------------------------------------------------------------------------------------------------

# 6.16 Match Object Summary

## Learning Objective

After completing this lesson, you will be able to:

- Review every Match Object method learned so far.
- Compare the purpose of each Match Object method.
- Choose the correct method for different automation tasks.
- Understand how Match Objects are used in enterprise applications.
- Prepare for interview questions related to Match Objects.

---

# Chapter Overview

So far, we have learned the following Match Object methods:

- `group()`
- `start()`
- `end()`
- `span()`
- `groups()`
- `groupdict()`

Each method retrieves different information stored inside a Match Object.

---

# Match Object Creation Flow

```
Python Program

↓

re.search()

or

re.match()

or

re.fullmatch()

↓

Regex Engine

↓

Successful Match

↓

Create Match Object

↓

Retrieve Information
```

The Match Object acts as a container holding all information about a successful match.

---

# Match Object Relationship

```
Regex Engine

↓

Match Object

├── group()
├── start()
├── end()
├── span()
├── groups()
└── groupdict()
```

Each method retrieves different information from the same Match Object.

---

# Method Comparison Table

| Method | Returns | Data Type | Requires Capturing Groups? |
|---------|----------|-----------|----------------------------|
| `group()` | Entire matched text | `str` | ❌ No |
| `start()` | Starting index | `int` | ❌ No |
| `end()` | Exclusive ending index | `int` | ❌ No |
| `span()` | (`start`, `end`) | `tuple` | ❌ No |
| `groups()` | Captured groups | `tuple` | ✅ Yes |
| `groupdict()` | Named groups | `dict` | ✅ Named groups |

---

# Running Example

Pattern

```regex
(?P<capacity>\d+)(?P<unit>GB)
```

Input

```text
Capacity : 2048GB
```

Python

```python
import re

text = "Capacity : 2048GB"

match = re.search(
    r"(?P<capacity>\d+)(?P<unit>GB)",
    text
)
```

---

# Output Comparison

| Method | Output |
|---------|--------|
| `match.group()` | `'2048GB'` |
| `match.start()` | `11` |
| `match.end()` | `17` |
| `match.span()` | `(11, 17)` |
| `match.groups()` | `('2048', 'GB')` |
| `match.groupdict()` | `{'capacity': '2048', 'unit': 'GB'}` |

---

# Visual Comparison

```
Input

Capacity : 2048GB
           └──────┘
           11    17

group()

↓

2048GB

--------------------

start()

↓

11

--------------------

end()

↓

17

--------------------

span()

↓

(11,17)

--------------------

groups()

↓

('2048','GB')

--------------------

groupdict()

↓

{
 capacity : 2048

 unit : GB
}
```

---

# Decision Guide

Need the matched text?

↓

Use

```python
group()
```

------------------------

Need where the match begins?

↓

Use

```python
start()
```

------------------------

Need where the match ends?

↓

Use

```python
end()
```

------------------------

Need both positions?

↓

Use

```python
span()
```

------------------------

Need all captured groups?

↓

Use

```python
groups()
```

------------------------

Need named captured groups?

↓

Use

```python
groupdict()
```

---

# Python Execution Summary

```
Regex Engine

↓

Pattern Found

↓

Create Match Object

↓

Choose Method

│
├── group()
├── start()
├── end()
├── span()
├── groups()
└── groupdict()

↓

Required Information
```

---

# Storage Engineering Applications

| Method | Example Use |
|---------|-------------|
| `group()` | Extract capacity value |
| `start()` | Locate capacity in logs |
| `end()` | Determine match boundary |
| `span()` | Highlight matched text |
| `groups()` | Separate value and unit |
| `groupdict()` | Parse structured storage reports |

---

# Linux Automation Applications

- Parse configuration files.
- Locate IP addresses.
- Process command output.
- Extract kernel versions.
- Analyze log entries.

---

# Python Automation Applications

- Report generation.
- Configuration parsing.
- Structured data extraction.
- Log analysis.
- Validation scripts.

---

# Common Beginner Mistakes

❌ Calling Match Object methods on `None`.

❌ Confusing `group()` with `groups()`.

❌ Forgetting that `end()` is exclusive.

❌ Using `groups()` without capturing groups.

❌ Using `groupdict()` without named groups.

---

# Interview Questions

1. What is a Match Object?

2. Which Regex functions return Match Objects?

3. Difference between `group()` and `groups()`.

4. Difference between `groups()` and `groupdict()`.

5. Why is `span()` useful?

6. Why is `end()` exclusive?

7. What happens when Match Object methods are called on `None`?

8. Why are named groups preferred in enterprise applications?

9. Which method returns a dictionary?

10. Which method returns a tuple?

---

# Practice Questions

### Question 1

Using the pattern

```regex
(?P<capacity>\d+)(?P<unit>GB)
```

list the output of every Match Object method.

---

### Question 2

Explain when `groups()` should be used instead of `group()`.

---

### Question 3

Describe three enterprise situations where `groupdict()` improves readability.

---

# Memory Sheet

```
group()

↓

Entire Match

----------------------

start()

↓

Beginning

----------------------

end()

↓

Exclusive End

----------------------

span()

↓

(Start, End)

----------------------

groups()

↓

Tuple

----------------------

groupdict()

↓

Dictionary
```

---

# One-Page Revision

| Need | Method |
|------|--------|
| Entire Match | `group()` |
| Beginning | `start()` |
| Ending | `end()` |
| Both Positions | `span()` |
| Captured Groups | `groups()` |
| Named Groups | `groupdict()` |

---

# Revision Box

✔ Match Objects store complete information about successful matches.

✔ Different methods retrieve different parts of that information.

✔ `group()` retrieves text.

✔ `start()`, `end()` and `span()` retrieve positions.

✔ `groups()` retrieves captured groups.

✔ `groupdict()` retrieves named captured groups.

---

# Key Takeaways

- Match Objects are central to Python Regular Expressions.
- Each Match Object method serves a specific purpose.
- Choosing the correct method makes automation code simpler and more maintainable.
- Named groups improve readability in complex Regular Expressions.
- Mastering Match Object methods prepares you for advanced text processing with the `re` module.

---

# Coming Up

You have now completed the **Searching and Match Object** section of Chapter 6.

The next lesson begins **Text Processing Functions** with **`re.sub()`**, which replaces matched text using Regular Expressions and is one of the most widely used functions in enterprise automation.

------------------------------------------------------------------------------------------------------------

# 6.17 `re.sub()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of `re.sub()`.
- Replace matched text using Regular Expressions.
- Explain how `re.sub()` differs from search functions.
- Apply `re.sub()` in Storage Engineering, Linux Automation and Test Automation.
- Recognize practical applications of text replacement.

---

# Previous Knowledge

So far, we have learned functions that **search** text.

Examples

- `re.search()`
- `re.match()`
- `re.fullmatch()`
- `re.findall()`
- `re.finditer()`

These functions **retrieve information**.

They do **not** modify the original text.

Now we will study the first function that performs **text transformation**.

---

# Introduction

Suppose we have the following storage log.

```text
Capacity : 2048MB
```

Suppose our automation script must convert

```text
MB
```

to

```text
GB
```

Searching is not enough.

We need to **replace** text.

Python provides

```python
re.sub()
```

---

# Why Do We Need `re.sub()`?

Many automation tasks require modifying text.

Examples

- Normalize log formats.
- Mask sensitive information.
- Replace deprecated values.
- Standardize configuration files.
- Clean input data.

Instead of manually editing strings,

the Regex Engine can locate matching text,

and `re.sub()` replaces it automatically.

---

# Definition

`re.sub()` searches the input string for **every non-overlapping match** of a Regular Expression and replaces each match with the specified replacement text.

The function returns a **new string**.

The original string remains unchanged.

---

# Syntax

```python
re.sub(pattern, replacement, string)
```

---

# Function Reference

| Property | Value |
|----------|-------|
| Function | `re.sub()` |
| Searches Entire String? | ✅ Yes |
| Replaces Matches? | ✅ Yes |
| Returns | New String (`str`) |
| Modifies Original String? | ❌ No |
| Uses Regex Engine? | ✅ Yes |

---

# Parameters

## `pattern`

The Regular Expression describing what should be replaced.

---

## `replacement`

The text that will replace each match.

---

## `string`

The input string.

---

# Return Value

```
Original String

↓

Regex Engine

↓

Replace Matches

↓

Return New String
```

The original string is **not modified** because Python strings are immutable.

---

# Python Execution Flow

```
Write Pattern

↓

Write Replacement

↓

Write Input

↓

Call

re.sub()

↓

Regex Engine

↓

Find Matches

↓

Replace Matches

↓

Return New String
```

---

# Regex Engine Explanation

Pattern

```regex
MB
```

Replacement

```text
GB
```

Input

```text
2048MB
```

Regex Engine

```
Receive Pattern

↓

Search Input

↓

Match Found

↓

Replace Match

↓

Continue Searching

↓

Return New String
```

---

# Engine Visualization

```
Pattern

      │
      ▼

+------------------+
|   Regex Engine   |
+------------------+

      │
      ▼

Find Matches

      │
      ▼

Replace

      │
      ▼

New String
```

---

# Python Code Example

```python
import re

text = "Capacity : 2048MB"

result = re.sub(r"MB", "GB", text)

print(result)
```

Output

```text
Capacity : 2048GB
```

---

# Python Console Example

```python
>>> import re
>>> re.sub(r"MB", "GB", "Capacity : 2048MB")
'Capacity : 2048GB'
```

---

# Example — Multiple Replacements

```python
import re

text = "512MB 1024MB 2048MB"

result = re.sub(r"MB", "GB", text)

print(result)
```

Output

```text
512GB 1024GB 2048GB
```

Every non-overlapping match is replaced.

---

# Storage Engineering Example

```python
import re

log = """
Drive1 : PASS
Drive2 : PASS
"""

result = re.sub(r"PASS", "SUCCESS", log)

print(result)
```

Application

- Log Standardization
- Report Formatting

---

# Linux Automation Example

```python
import re

config = "HOST=localhost"

result = re.sub(r"localhost", "server01", config)

print(result)
```

Application

- Configuration Updates
- Deployment Automation

---

# Python Automation Example

```python
import re

report = "Status=FAIL"

result = re.sub(r"FAIL", "FAILED", report)

print(result)
```

Application

- Report Normalization
- Result Formatting

---

# Compare

| Function | Purpose |
|----------|----------|
| `re.search()` | Find first match |
| `re.findall()` | Find all matches |
| `re.finditer()` | Iterate over Match Objects |
| `re.sub()` | Replace matched text |

---

# Important Observation

`re.sub()` does **not** modify the original string.

Example

```python
import re

text = "2048MB"

result = re.sub(r"MB", "GB", text)

print(text)
print(result)
```

Output

```text
2048MB
2048GB
```

The original value remains unchanged.

---

# Common Beginner Mistakes

### Mistake 1

Thinking `re.sub()` modifies the original string.

Python strings are immutable.

---

### Mistake 2

Ignoring the returned value.

Always store or use the returned string.

---

### Mistake 3

Confusing `re.sub()` with `str.replace()`.

`str.replace()` replaces fixed text.

`re.sub()` replaces text matched by a **Regular Expression**.

---

# Interview Questions

1. What is the purpose of `re.sub()`?

2. What does `re.sub()` return?

3. Does `re.sub()` modify the original string?

4. How does `re.sub()` differ from `re.search()`?

5. Give practical applications of `re.sub()`.

---

# Practice Questions

### Question 1

Write a Python program that replaces every occurrence of `MB` with `GB`.

---

### Question 2

Explain why the original string remains unchanged after calling `re.sub()`.

---

### Question 3

List five situations where `re.sub()` is useful in enterprise automation.

---

# Memory Tip

```
Input String

↓

Regex Engine

↓

Find Matches

↓

Replace Matches

↓

Return New String
```

Remember

```
search()

↓

Find

--------------------

sub()

↓

Find

+

Replace
```

---

# Revision Box

✔ `re.sub()` replaces matched text using a Regular Expression.

✔ It returns a new string.

✔ The original string is not modified.

✔ Every non-overlapping match is replaced.

✔ It is widely used for text transformation and data normalization.

---

# Key Takeaways

- `re.sub()` combines Regex searching with text replacement.
- It searches the entire input and replaces every non-overlapping match.
- The return value is a new string because Python strings are immutable.
- It is extensively used in enterprise automation for log normalization, configuration updates and report formatting.
- `re.sub()` marks the transition from searching to text transformation in Python's `re` module.

---

# Coming Up

The next lesson introduces **`re.split()`**, which uses Regular Expressions to split text into smaller components based on pattern matches, making it ideal for parsing logs, configuration files and structured data.

------------------------------------------------------------------------------------------------------------

# 6.18 `re.split()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of `re.split()`.
- Split text using Regular Expressions.
- Explain how `re.split()` differs from Python's built-in `split()`.
- Apply `re.split()` in Storage Engineering, Linux Automation and Test Automation.
- Recognize situations where Regex-based splitting is useful.

---

# Previous Knowledge

In the previous lesson, we learned

```python
re.sub()
```

which searches for text and replaces every matching occurrence.

Now we will study another text-processing function,

```python
re.split()
```

Instead of replacing text,

it divides the input string into multiple parts.

---

# Introduction

Suppose we have the following storage log.

```text
Drive1,Drive2;Drive3|Drive4
```

Notice that the values are separated by different delimiters.

- `,`
- `;`
- `|`

Python's normal

```python
split()
```

can split using only **one delimiter** at a time.

To split using multiple delimiters,

we use

```python
re.split()
```

---

# Why Do We Need `re.split()`?

Many enterprise data sources use inconsistent separators.

Examples

- Log files
- Configuration files
- CSV-like reports
- Network command output
- Storage reports

Regular Expressions allow multiple delimiters to be handled using a single pattern.

---

# Definition

`re.split()` splits an input string wherever the Regular Expression matches.

The matched delimiter is removed,

and the remaining parts are returned as a Python list.

---

# Syntax

```python
re.split(pattern, string)
```

---

# Function Reference

| Property | Value |
|----------|-------|
| Function | `re.split()` |
| Searches Entire String? | ✅ Yes |
| Splits Text? | ✅ Yes |
| Returns | Python List |
| Uses Regex Engine? | ✅ Yes |

---

# Parameters

## `pattern`

The Regular Expression describing the delimiter(s).

---

## `string`

The input string to split.

---

# Return Value

```
Input String

↓

Regex Engine

↓

Find Delimiters

↓

Split Text

↓

Return Python List
```

---

# Python Execution Flow

```
Write Pattern

↓

Write Input

↓

Call

re.split()

↓

Regex Engine

↓

Find Delimiters

↓

Split String

↓

Return List
```

---

# Regex Engine Explanation

Pattern

```regex
[,;|]
```

Input

```text
Drive1,Drive2;Drive3|Drive4
```

Regex Engine

```
Receive Pattern

↓

Search Input

↓

Delimiter Found

↓

Split

↓

Continue Searching

↓

Return List
```

---

# Engine Visualization

```
Pattern

      │
      ▼

+------------------+
|   Regex Engine   |
+------------------+

      │
      ▼

Find Delimiters

      │
      ▼

Split Text

      │
      ▼

Python List
```

---

# Python Code Example

```python
import re

text = "Drive1,Drive2;Drive3|Drive4"

result = re.split(r"[,;|]", text)

print(result)
```

Output

```python
['Drive1', 'Drive2', 'Drive3', 'Drive4']
```

---

# Python Console Example

```python
>>> import re
>>> re.split(r"[,;|]", "Drive1,Drive2;Drive3|Drive4")
['Drive1', 'Drive2', 'Drive3', 'Drive4']
```

---

# Example — Split on Whitespace

```python
import re

text = "Drive1   Drive2\tDrive3"

result = re.split(r"\s+", text)

print(result)
```

Output

```python
['Drive1', 'Drive2', 'Drive3']
```

The pattern `\s+` matches one or more whitespace characters.

---

# Storage Engineering Example

```python
import re

log = "Disk1|Disk2|Disk3"

drives = re.split(r"\|", log)

print(drives)
```

Application

- Storage Inventory Parsing
- Device List Processing

---

# Linux Automation Example

```python
import re

path = "/home/user/logs"

parts = re.split(r"/", path)

print(parts)
```

Application

- File Path Processing
- Script Automation

---

# Python Automation Example

```python
import re

report = "PASS,FAIL,PASS"

results = re.split(r",", report)

print(results)
```

Application

- Report Parsing
- Test Result Processing

---

# Compare

| Function | Purpose |
|----------|----------|
| `str.split()` | Split using a fixed delimiter |
| `re.split()` | Split using a Regular Expression |

---

# Important Observation

`re.split()` removes the matched delimiter from the returned list.

Example

```python
import re

text = "A,B,C"

print(re.split(r",", text))
```

Output

```python
['A', 'B', 'C']
```

The commas do not appear in the result.

---

# Common Beginner Mistakes

### Mistake 1

Using `str.split()` when multiple delimiters are required.

---

### Mistake 2

Forgetting that special Regex characters (such as `|`) may need to be escaped when used literally.

Example

```python
re.split(r"\|", text)
```

---

### Mistake 3

Expecting the delimiters to remain in the output.

By default, matched delimiters are removed.

---

# Interview Questions

1. What is the purpose of `re.split()`?

2. What does `re.split()` return?

3. How does `re.split()` differ from `str.split()`?

4. Why is `re.split()` useful for log parsing?

5. Give practical applications of `re.split()`.

---

# Practice Questions

### Question 1

Write a Python program that splits a string using commas, semicolons and pipes.

---

### Question 2

Explain why `re.split()` is preferred over `str.split()` when multiple delimiters exist.

---

### Question 3

List five enterprise situations where `re.split()` is useful.

---

# Memory Tip

```
Input String

↓

Regex Engine

↓

Find Delimiters

↓

Split

↓

Python List
```

Remember

```
str.split()

↓

One Delimiter

--------------------

re.split()

↓

Regex Pattern

↓

Many Delimiters
```

---

# Revision Box

✔ `re.split()` splits text wherever the Regular Expression matches.

✔ It returns a Python list.

✔ Multiple delimiters can be handled using a single Regex.

✔ It is ideal for parsing logs and structured text.

✔ It provides much greater flexibility than `str.split()`.

---

# Key Takeaways

- `re.split()` uses Regular Expressions to divide text into multiple parts.
- It returns a Python list of the resulting substrings.
- It supports complex delimiter patterns, unlike `str.split()`.
- It is widely used in enterprise automation for parsing logs, configuration files and reports.
- `re.split()` is a key text-processing function in Python's `re` module.

---

# Coming Up

The next lesson introduces **`re.compile()`**, which compiles a Regular Expression into a reusable pattern object. This improves code readability and can improve performance when the same Regular Expression is used repeatedly.

------------------------------------------------------------------------------------------------------------

# 6.19 `re.compile()`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of `re.compile()`.
- Explain why compiled patterns are useful.
- Create reusable Regular Expression objects.
- Apply compiled patterns in enterprise automation.
- Understand the relationship between `re.compile()` and Regex performance.

---

# Previous Knowledge

So far, we have used functions such as

```python
re.search()

re.findall()

re.sub()

re.split()
```

In every example,

we passed the Regular Expression directly.

Example

```python
re.search(r"\d+GB", text)
```

This works well,

but what if the same pattern is used hundreds or thousands of times?

Python provides

```python
re.compile()
```

to solve this problem.

---

# Introduction

Suppose an automation script processes

- 10,000 storage logs
- 50,000 Linux log entries
- 100,000 test reports

Every record needs the same pattern

```regex
\d+GB
```

Without `re.compile()`,

the same pattern is supplied repeatedly.

With `re.compile()`,

the pattern is prepared once and reused.

---

# Why Do We Need `re.compile()`?

Many enterprise applications repeatedly use the same Regular Expression.

Examples

- Log parsing
- Configuration validation
- Storage report analysis
- Test automation
- Monitoring systems

Instead of repeatedly writing

```python
re.search(r"\d+GB", text)
```

we create a reusable pattern object.

---

# Definition

`re.compile()` compiles a Regular Expression into a **Pattern Object**.

The Pattern Object can then be reused to perform searches, matching, substitutions and splitting operations.

---

# Syntax

```python
pattern = re.compile(regex_pattern)
```

Example

```python
pattern = re.compile(r"\d+GB")
```

---

# Function Reference

| Property | Value |
|----------|-------|
| Function | `re.compile()` |
| Returns | Pattern Object |
| Reusable | ✅ Yes |
| Uses Regex Engine? | ✅ Yes |

---

# Return Value

```
Regular Expression

↓

re.compile()

↓

Pattern Object
```

The returned Pattern Object provides methods such as

- `search()`
- `match()`
- `fullmatch()`
- `findall()`
- `finditer()`
- `sub()`
- `split()`

---

# Python Execution Flow

Without `re.compile()`

```
Loop

↓

re.search()

↓

Regex Pattern

↓

Regex Engine

↓

Search

↓

Repeat
```

With `re.compile()`

```
Compile Once

↓

Pattern Object

↓

Loop

↓

pattern.search()

↓

Regex Engine

↓

Search
```

The Pattern Object is reused throughout the program.

---

# Regex Engine Explanation

```
Regular Expression

↓

re.compile()

↓

Pattern Object Created

↓

Pattern Object

↓

search()

↓

Regex Engine

↓

Result
```

The Pattern Object stores the compiled Regular Expression.

---

# Engine Visualization

```
Regular Expression

      │
      ▼

 re.compile()

      │
      ▼

+------------------+
| Pattern Object   |
+------------------+

      │
      ▼

search()

match()

findall()

sub()

split()
```

---

# Python Code Example

```python
import re

pattern = re.compile(r"\d+GB")

text = "Capacity : 2048GB"

match = pattern.search(text)

print(match.group())
```

Output

```text
2048GB
```

---

# Python Console Example

```python
>>> import re
>>> pattern = re.compile(r"\d+GB")
>>> pattern.search("Capacity : 2048GB").group()
'2048GB'
```

---

# Example — Reusing the Pattern

```python
import re

pattern = re.compile(r"\d+GB")

logs = [
    "512GB",
    "1024GB",
    "2048GB"
]

for log in logs:
    print(pattern.search(log).group())
```

Output

```text
512GB
1024GB
2048GB
```

The same compiled pattern is reused for every search.

---

# Storage Engineering Example

```python
import re

capacity_pattern = re.compile(r"\d+GB")

logs = [
    "Drive1 : 512GB",
    "Drive2 : 1024GB",
    "Drive3 : 2048GB"
]

for log in logs:
    print(capacity_pattern.search(log).group())
```

Application

- Capacity Extraction
- Large Storage Log Processing

---

# Linux Automation Example

```python
import re

ip_pattern = re.compile(r"\d+\.\d+\.\d+\.\d+")

output = "inet 192.168.1.20/24"

print(ip_pattern.search(output).group())
```

Application

- Network Log Parsing
- IP Address Detection

---

# Python Automation Example

```python
import re

status_pattern = re.compile(r"PASS|FAIL")

report = "Status : PASS"

print(status_pattern.search(report).group())
```

Application

- Report Validation
- Test Result Processing

---

# Compare

| Without `re.compile()` | With `re.compile()` |
|------------------------|---------------------|
| Pattern supplied each time | Pattern compiled once |
| Less reusable | Highly reusable |
| Repeated function calls with raw pattern | Pattern object methods |

---

# Important Observation

`re.compile()` does **not** perform any matching by itself.

It only creates a Pattern Object.

Matching begins only when methods such as

```python
pattern.search()

pattern.findall()

pattern.sub()
```

are called.

---

# Common Beginner Mistakes

### Mistake 1

Thinking `re.compile()` searches text.

It only creates a reusable Pattern Object.

---

### Mistake 2

Compiling a pattern and never using the Pattern Object.

---

### Mistake 3

Assuming `re.compile()` is mandatory.

It is optional but highly recommended when the same pattern is reused.

---

# Interview Questions

1. What is the purpose of `re.compile()`?

2. What does `re.compile()` return?

3. Why is `re.compile()` useful in enterprise automation?

4. Does `re.compile()` perform matching?

5. What methods are available on a Pattern Object?

---

# Practice Questions

### Question 1

Write a Python program that compiles a pattern and searches three different strings.

---

### Question 2

Explain why `re.compile()` improves code readability.

---

### Question 3

List five situations where compiling a Regular Expression is beneficial.

---

# Memory Tip

```
Regular Expression

↓

Compile Once

↓

Pattern Object

↓

Reuse Everywhere
```

Remember

```
re.compile()

↓

Prepare Pattern

--------------------

pattern.search()

↓

Use Pattern
```

---

# Revision Box

✔ `re.compile()` creates a reusable Pattern Object.

✔ The Pattern Object provides methods such as `search()`, `match()`, `findall()`, `sub()` and `split()`.

✔ `re.compile()` itself performs no matching.

✔ It improves code organization and is especially useful when the same pattern is reused.

✔ It is widely used in enterprise log processing and automation.

---

# Key Takeaways

- `re.compile()` converts a Regular Expression into a reusable Pattern Object.
- It improves readability by separating pattern creation from pattern usage.
- The Pattern Object can perform searching, matching, substitution and splitting operations.
- Compiling patterns is particularly valuable when processing large amounts of data with the same Regular Expression.
- `re.compile()` is a best practice for reusable and maintainable Regex code.

---

# Coming Up

The next lesson introduces **Regex Flags**, which modify how the Regex Engine performs matching. You will learn flags such as `IGNORECASE`, `MULTILINE`, `DOTALL` and others that change the behavior of Regular Expressions without changing the pattern itself.

----------------------------------------------------------------------------------------------------------

# 6.20 Regex Flags

## Learning Objective

After completing this lesson, you will be able to:

- Understand what Regex Flags are.
- Explain why Regex Flags are used.
- Use common flags such as `IGNORECASE`, `MULTILINE`, `DOTALL`, and `VERBOSE`.
- Apply Regex Flags in Storage Engineering, Linux Automation and Test Automation.
- Recognize situations where Regex Flags improve readability and flexibility.

---

# Previous Knowledge

So far, every Regular Expression has behaved according to Python's default matching rules.

Example

```python
re.search(r"pass", "PASS")
```

Output

```python
None
```

Why?

Because Regular Expressions are **case-sensitive** by default.

Sometimes we want different behavior.

Python allows us to change the behavior of the Regex Engine using **Regex Flags**.

---

# Why Do We Need Regex Flags?

Different applications require different matching behavior.

Examples

- Ignore letter case
- Search across multiple lines
- Allow `.` to match newline characters
- Write readable multi-line Regular Expressions

Instead of changing the Regular Expression itself,

we can modify the Regex Engine using flags.

---

# Definition

A **Regex Flag** is an option passed to the `re` module that changes how the Regex Engine performs pattern matching.

Flags affect the matching behavior,

not the pattern itself.

---

# Syntax

Without flags

```python
re.search(pattern, text)
```

With flags

```python
re.search(pattern, text, flags=re.IGNORECASE)
```

Multiple flags

```python
re.search(
    pattern,
    text,
    flags=re.IGNORECASE | re.MULTILINE
)
```

---

# Common Regex Flags

| Flag | Short Form | Purpose |
|------|------------|---------|
| `re.IGNORECASE` | `re.I` | Ignore letter case |
| `re.MULTILINE` | `re.M` | `^` and `$` work on every line |
| `re.DOTALL` | `re.S` | `.` matches newline |
| `re.VERBOSE` | `re.X` | Write readable multi-line regex |

---

# 1. `re.IGNORECASE`

Purpose

Ignore uppercase and lowercase differences.

---

### Example

```python
import re

text = "Status : PASS"

match = re.search(
    r"pass",
    text,
    flags=re.IGNORECASE
)

print(match.group())
```

Output

```text
PASS
```

Without `IGNORECASE`

```python
None
```

---

# Storage Engineering Example

```python
import re

log = "Status : PASS"

match = re.search(
    r"pass",
    log,
    flags=re.IGNORECASE
)

print(match.group())
```

Application

- Status Validation
- Log Analysis

---

# 2. `re.MULTILINE`

Purpose

Treat every line as a separate beginning and ending.

Without `MULTILINE`

`^` matches only the beginning of the entire string.

With `MULTILINE`

`^` matches the beginning of every line.

---

### Example

```python
import re

text = """PASS
FAIL
PASS"""

matches = re.findall(
    r"^PASS",
    text,
    flags=re.MULTILINE
)

print(matches)
```

Output

```python
['PASS', 'PASS']
```

---

# Linux Automation Example

```python
import re

output = """HOST=server01
HOST=server02"""

matches = re.findall(
    r"^HOST=.*",
    output,
    flags=re.MULTILINE
)

print(matches)
```

Application

- Configuration Parsing
- Multi-line Log Processing

---

# 3. `re.DOTALL`

Purpose

Allow the dot (`.`) to match newline characters.

Normally,

`.` does **not** match `\n`.

---

### Example

```python
import re

text = """START
DATA
END"""

match = re.search(
    r"START.*END",
    text,
    flags=re.DOTALL
)

print(match.group())
```

Output

```text
START
DATA
END
```

---

# Test Automation Example

```python
import re

report = """BEGIN
Execution Passed
END"""

match = re.search(
    r"BEGIN.*END",
    report,
    flags=re.DOTALL
)

print(match.group())
```

Application

- Multi-line Report Processing
- Log Parsing

---

# 4. `re.VERBOSE`

Purpose

Write complex Regular Expressions over multiple lines with comments.

Example

```python
pattern = re.compile(
    r"""
    \d+      # Number
    GB       # Unit
    """,
    re.VERBOSE
)
```

The comments and whitespace improve readability.

---

# Combining Flags

Multiple flags can be combined using the bitwise OR operator (`|`).

Example

```python
import re

match = re.search(
    r"pass",
    "PASS",
    flags=re.IGNORECASE | re.MULTILINE
)
```

---

# Python Execution Flow

```
Pattern

↓

Regex Flags

↓

Regex Engine

↓

Modified Matching Rules

↓

Search

↓

Result
```

---

# Engine Visualization

```
Pattern

      │
      ▼

Regex Flags

      │
      ▼

+------------------+
|   Regex Engine   |
+------------------+

      │
      ▼

Modified Behavior

      │
      ▼

Result
```

---

# Compare

| Flag | Effect |
|------|--------|
| `IGNORECASE` | Ignore letter case |
| `MULTILINE` | `^` and `$` work per line |
| `DOTALL` | `.` matches newlines |
| `VERBOSE` | Multi-line readable regex |

---

# Important Observation

Flags do **not** change the Regular Expression.

They change **how the Regex Engine interprets the pattern**.

Think of it as

```
Pattern

+

Flags

↓

Regex Engine

↓

Modified Behavior
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking flags modify the input string.

They only modify matching behavior.

---

### Mistake 2

Forgetting to combine multiple flags using `|`.

---

### Mistake 3

Using `IGNORECASE` when exact case-sensitive matching is required.

---

# Interview Questions

1. What are Regex Flags?

2. What is the purpose of `re.IGNORECASE`?

3. How does `re.MULTILINE` affect `^` and `$`?

4. What is the purpose of `re.DOTALL`?

5. Why is `re.VERBOSE` useful?

---

# Practice Questions

### Question 1

Write a Python program that matches `"PASS"` regardless of letter case.

---

### Question 2

Explain the difference between `MULTILINE` and `DOTALL`.

---

### Question 3

Write a readable multi-line pattern using `re.VERBOSE`.

---

# Memory Tip

```
IGNORECASE

↓

Ignore Case

--------------------

MULTILINE

↓

Every Line

--------------------

DOTALL

↓

Dot Matches Newline

--------------------

VERBOSE

↓

Readable Regex
```

---

# Revision Box

✔ Regex Flags modify the behavior of the Regex Engine.

✔ `IGNORECASE` ignores letter case.

✔ `MULTILINE` changes how `^` and `$` behave.

✔ `DOTALL` allows `.` to match newline characters.

✔ `VERBOSE` improves readability of complex Regular Expressions.

---

# Key Takeaways

- Regex Flags provide a powerful way to customize pattern matching without changing the Regular Expression itself.
- Different flags solve different matching problems, such as case sensitivity, multi-line text, and readable pattern formatting.
- Multiple flags can be combined using the `|` operator.
- Flags are widely used in enterprise log parsing, configuration processing, and automation.
- Understanding Regex Flags is essential for writing flexible and maintainable Regular Expressions.

---

# Coming Up

The next lesson introduces **Regex Best Practices, Performance Tips, and Common Pitfalls**, including techniques for writing efficient, maintainable Regular Expressions and avoiding mistakes commonly seen in production automation.

----------------------------------------------------------------------------------------------------------

# 6.21 Regex Best Practices, Performance Tips & Common Pitfalls

## Learning Objective

After completing this lesson, you will be able to:

- Write safer and more maintainable Regular Expression code.
- Apply Regex best practices in enterprise automation.
- Avoid common mistakes made by beginners.
- Understand performance considerations.
- Follow industry-standard coding practices.

---

# Previous Knowledge

Throughout this chapter, we have learned:

- Searching functions
- Match Objects
- Text transformation
- Pattern compilation
- Regex Flags

Now let us learn how experienced Python developers write Regular Expressions in real-world applications.

---

# Why Are Best Practices Important?

Regular Expressions are powerful,

but poorly written Regex patterns can become

- difficult to understand
- difficult to maintain
- slower than necessary
- more likely to contain bugs

Following best practices makes code

- cleaner
- safer
- easier to debug
- easier to maintain

---

# Best Practice 1 — Always Use Raw Strings

Preferred

```python
pattern = r"\d+GB"
```

Avoid

```python
pattern = "\\d+GB"
```

Raw strings reduce escaping and improve readability.

---

# Best Practice 2 — Check for `None`

Avoid

```python
match = re.search(pattern, text)

print(match.group())
```

If no match exists,

this raises an error.

Preferred

```python
match = re.search(pattern, text)

if match:
    print(match.group())
```

Always verify that the Match Object exists.

---

# Best Practice 3 — Compile Reusable Patterns

Instead of

```python
for line in logs:
    re.search(r"\d+GB", line)
```

Prefer

```python
pattern = re.compile(r"\d+GB")

for line in logs:
    pattern.search(line)
```

Benefits

- Better organization
- Reusable code
- Potential performance improvement for repeated use

---

# Best Practice 4 — Use Meaningful Named Groups

Instead of

```regex
(\d+)(GB)
```

Prefer

```regex
(?P<capacity>\d+)(?P<unit>GB)
```

Then

```python
match.groupdict()
```

is much easier to understand.

---

# Best Practice 5 — Use `re.VERBOSE` for Complex Patterns

Instead of one long unreadable pattern,

write

```python
pattern = re.compile(
    r"""
    \d+      # Capacity value
    GB       # Unit
    """,
    re.VERBOSE
)
```

Readable Regex is easier to maintain.

---

# Best Practice 6 — Choose the Right Function

Need one match?

↓

```python
re.search()
```

Need every match?

↓

```python
re.findall()
```

Need Match Objects?

↓

```python
re.finditer()
```

Need replacement?

↓

```python
re.sub()
```

Need splitting?

↓

```python
re.split()
```

Selecting the correct function keeps code simple.

---

# Best Practice 7 — Keep Patterns Simple

Avoid overly complicated expressions when a simpler one works.

Example

Instead of

```regex
([0-9])([0-9])([0-9])([0-9])
```

Prefer

```regex
\d{4}
```

Simpler patterns are easier to read and maintain.

---

# Performance Tips

### Compile frequently reused patterns

```python
pattern = re.compile(...)
```

Reuse the Pattern Object.

---

### Avoid unnecessary searches

If only the beginning matters,

use

```python
re.match()
```

instead of

```python
re.search()
```

---

### Retrieve only what you need

Need the first match?

↓

```python
re.search()
```

Need all matches?

↓

```python
re.findall()
```

Avoid extra work.

---

# Common Pitfalls

### Pitfall 1

Calling

```python
group()
```

on

```python
None
```

Always check first.

---

### Pitfall 2

Confusing

```python
group()
```

with

```python
groups()
```

One returns the entire match.

The other returns captured groups.

---

### Pitfall 3

Using

```python
findall()
```

when Match Objects are required.

Use

```python
finditer()
```

instead.

---

### Pitfall 4

Forgetting that

```python
end()
```

returns an **exclusive** index.

---

### Pitfall 5

Using

```python
str.replace()
```

when Regex replacement is required.

Use

```python
re.sub()
```

---

### Pitfall 6

Ignoring Regex Flags.

Sometimes

```python
re.IGNORECASE
```

or

```python
re.MULTILINE
```

produces the intended behavior without changing the pattern.

---

# Storage Engineering Example

```python
import re

capacity_pattern = re.compile(r"\d+GB")

for log in logs:
    match = capacity_pattern.search(log)

    if match:
        print(match.group())
```

Good practices demonstrated

- Compiled pattern
- Safe Match Object check
- Reusable code

---

# Linux Automation Example

```python
import re

ip_pattern = re.compile(r"\d+\.\d+\.\d+\.\d+")

match = ip_pattern.search(output)

if match:
    print(match.group())
```

Application

- Safe automation
- Log parsing

---

# Python Automation Example

```python
import re

status_pattern = re.compile(
    r"PASS|FAIL",
    re.IGNORECASE
)

match = status_pattern.search(report)

if match:
    print(match.group())
```

Application

- Flexible validation
- Readable code

---

# Engineering Checklist

Before writing a Regex program, ask yourself:

✔ Should I use a raw string?

✔ Should I compile the pattern?

✔ Do I need one match or all matches?

✔ Should I check for `None`?

✔ Would named groups improve readability?

✔ Do I need any Regex Flags?

---

# Interview Questions

1. Why should raw strings be used for Regular Expressions?

2. Why should Match Objects be checked before calling `group()`?

3. When is `re.compile()` recommended?

4. What are the advantages of named groups?

5. Why is `re.VERBOSE` useful?

---

# Practice Questions

### Question 1

Rewrite a Regex program to use `re.compile()` and safe Match Object handling.

---

### Question 2

List five Regex best practices.

---

### Question 3

Explain three common beginner mistakes and how to avoid them.

---

# Memory Tip

```
Raw String

↓

Compile

↓

Search

↓

Check Match

↓

Retrieve Data
```

Remember

```
Readable

Reusable

Reliable
```

These are the goals of professional Regex programming.

---

# Revision Box

✔ Use raw strings for Regular Expressions.

✔ Check Match Objects before using Match Object methods.

✔ Compile reusable patterns.

✔ Prefer named groups for readability.

✔ Use Regex Flags when appropriate.

✔ Choose the correct Regex function for the task.

---

# Key Takeaways

- Following Regex best practices produces cleaner, safer and more maintainable code.
- Compiled patterns, named groups and raw strings improve readability.
- Always verify Match Objects before accessing their methods.
- Select the appropriate Regex function based on the problem being solved.
- These practices reflect how Regular Expressions are used in professional software engineering.

---

# Coming Up

The next lesson demonstrates **Real-World Applications of Regular Expressions**, bringing together everything learned in this chapter through complete examples from Storage Engineering, Linux Automation, Test Automation and log analysis before concluding with the Chapter 6 summary.

----------------------------------------------------------------------------------------------------------

# 6.22 Real-World Applications of Regular Expressions

## Learning Objective

After completing this lesson, you will be able to:

- Apply multiple Regex concepts together.
- Solve practical text-processing problems.
- Understand how Regular Expressions are used in enterprise automation.
- Recognize common Regex workflows in Storage Engineering, Linux Automation and Test Automation.
- Build confidence in designing Regex-based solutions.

---

# Previous Knowledge

In this chapter, we learned:

- Searching functions
- Match Objects
- Text transformation
- Pattern compilation
- Regex Flags
- Best practices

Now we will combine these concepts into complete, practical workflows.

---

# Application 1 — Storage Capacity Extraction

### Problem

Extract every storage capacity from a storage report.

Input

```text
Drive1 : 512GB
Drive2 : 1024GB
Drive3 : 2048GB
```

---

### Solution

```python
import re

pattern = re.compile(r"\d+GB")

report = """
Drive1 : 512GB
Drive2 : 1024GB
Drive3 : 2048GB
"""

capacities = pattern.findall(report)

print(capacities)
```

Output

```python
['512GB', '1024GB', '2048GB']
```

---

### Concepts Used

✔ `re.compile()`

✔ `findall()`

---

# Application 2 — Storage Log Validation

### Problem

Determine whether a storage log contains a valid capacity.

Input

```text
Capacity : 4096GB
```

---

### Solution

```python
import re

match = re.search(r"\d+GB", "Capacity : 4096GB")

if match:
    print("Valid Capacity")
else:
    print("Invalid Capacity")
```

Output

```text
Valid Capacity
```

---

### Concepts Used

✔ `search()`

✔ `group()`

✔ Safe Match Object handling

---

# Application 3 — Linux IP Address Extraction

### Problem

Extract every IPv4 address from command output.

Input

```text
inet 192.168.1.20
inet 10.10.20.15
```

---

### Solution

```python
import re

output = """
inet 192.168.1.20
inet 10.10.20.15
"""

ips = re.findall(
    r"\d+\.\d+\.\d+\.\d+",
    output
)

print(ips)
```

Output

```python
['192.168.1.20', '10.10.20.15']
```

---

### Concepts Used

✔ `findall()`

✔ Character classes

✔ Quantifiers

---

# Application 4 — Software Version Parsing

### Problem

Separate version components.

Input

```text
Version=3.5.12
```

---

### Solution

```python
import re

match = re.search(
    r"(\d+)\.(\d+)\.(\d+)",
    "Version=3.5.12"
)

print(match.groups())
```

Output

```python
('3', '5', '12')
```

---

### Concepts Used

✔ Capturing Groups

✔ `groups()`

---

# Application 5 — Named Group Parsing

### Problem

Extract structured information.

Input

```text
2048GB
```

---

### Solution

```python
import re

match = re.search(
    r"(?P<capacity>\d+)(?P<unit>GB)",
    "2048GB"
)

print(match.groupdict())
```

Output

```python
{
    'capacity': '2048',
    'unit': 'GB'
}
```

---

### Concepts Used

✔ Named Groups

✔ `groupdict()`

---

# Application 6 — Log Normalization

### Problem

Replace every occurrence of

```text
PASS
```

with

```text
SUCCESS
```

---

### Solution

```python
import re

log = """
PASS
FAIL
PASS
"""

result = re.sub(
    r"PASS",
    "SUCCESS",
    log
)

print(result)
```

Output

```text
SUCCESS
FAIL
SUCCESS
```

---

### Concepts Used

✔ `sub()`

---

# Application 7 — Configuration Parsing

### Problem

Split configuration values separated by different delimiters.

Input

```text
A,B;C|D
```

---

### Solution

```python
import re

values = re.split(
    r"[,;|]",
    "A,B;C|D"
)

print(values)
```

Output

```python
['A', 'B', 'C', 'D']
```

---

### Concepts Used

✔ `split()`

✔ Character Classes

---

# Application 8 — Case-Insensitive Search

### Problem

Detect

```text
PASS
```

regardless of letter case.

Input

```text
Pass
```

---

### Solution

```python
import re

match = re.search(
    r"pass",
    "Pass",
    flags=re.IGNORECASE
)

print(match.group())
```

Output

```text
Pass
```

---

### Concepts Used

✔ `IGNORECASE`

---

# Application 9 — Multi-Line Log Parsing

### Problem

Find every line beginning with

```text
ERROR
```

Input

```text
INFO Start
ERROR Disk Failure
INFO Retry
ERROR Timeout
```

---

### Solution

```python
import re

log = """INFO Start
ERROR Disk Failure
INFO Retry
ERROR Timeout"""

errors = re.findall(
    r"^ERROR.*",
    log,
    flags=re.MULTILINE
)

print(errors)
```

Output

```python
['ERROR Disk Failure', 'ERROR Timeout']
```

---

### Concepts Used

✔ `MULTILINE`

✔ `findall()`

---

# Enterprise Workflow

```
Input Data

↓

Compile Pattern

↓

Regex Engine

↓

Search

↓

Match Object

↓

Extract Data

↓

Validate

↓

Transform

↓

Generate Report
```

This is a common Regex processing pipeline.

---

# Function Selection Guide

| Need | Function |
|------|----------|
| First Match | `search()` |
| Beginning Only | `match()` |
| Entire String | `fullmatch()` |
| All Matches | `findall()` |
| Match Objects | `finditer()` |
| Replace Text | `sub()` |
| Split Text | `split()` |
| Reusable Pattern | `compile()` |

---

# Storage Engineering Workflow

```
Storage Log

↓

Regex Pattern

↓

Extract Capacity

↓

Validate Format

↓

Generate Report
```

---

# Linux Automation Workflow

```
Command Output

↓

Regex Pattern

↓

Extract IP

↓

Validate

↓

Automation Script
```

---

# Test Automation Workflow

```
Test Report

↓

Regex Pattern

↓

Extract Status

↓

Generate Summary

↓

Decision
```

---

# Common Enterprise Uses

- Log parsing
- Configuration validation
- Report generation
- Data extraction
- File processing
- Automation scripts
- Monitoring tools
- Validation pipelines

---

# Interview Questions

1. Why are Regular Expressions important in automation?

2. Which Regex function would you use to replace text?

3. Which function returns Match Objects?

4. Why use named groups in enterprise applications?

5. When would you choose `finditer()` instead of `findall()`?

---

# Practice Questions

### Question 1

Design a Regex solution to extract storage capacities from a report.

---

### Question 2

Write a Regex program that normalizes log statuses.

---

### Question 3

Describe an enterprise workflow that combines `re.compile()`, `search()`, `group()` and `sub()`.

---

# Memory Sheet

```
Compile

↓

Search

↓

Extract

↓

Validate

↓

Transform

↓

Report
```

---

# Revision Box

✔ Regular Expressions are widely used in enterprise automation.

✔ Multiple Regex functions often work together in complete workflows.

✔ Pattern compilation improves reusability.

✔ Match Objects enable detailed data extraction.

✔ Regex supports searching, validation, transformation and parsing.

---

# Key Takeaways

- Regular Expressions are not isolated functions—they are typically combined into complete processing pipelines.
- Enterprise automation frequently uses `re.compile()`, search functions, Match Objects and text transformation together.
- The choice of Regex function depends on the task: searching, extracting, validating or transforming.
- Understanding practical workflows is essential for applying Regex effectively in real-world software engineering.
- You are now ready to consolidate everything learned in the final chapter summary.

---

# Coming Up

The next lesson is the **Chapter 6 Summary**, where we review every concept, function and Match Object method covered throughout the chapter, followed by a complete revision sheet and interview preparation guide.

----------------------------------------------------------------------------------------------------------

# 6.23 Chapter Summary

## Learning Objective

After completing this lesson, you will be able to:

- Review every major concept covered in Chapter 6.
- Recall the purpose of each `re` module function.
- Select the appropriate Regex function for different tasks.
- Revise Match Object methods efficiently.
- Prepare for interviews and practical automation work.

---

# Chapter Overview

In this chapter, we explored Python's **Regular Expression (`re`) module**, learning how to:

- Search text
- Validate input
- Extract information
- Transform text
- Split text
- Reuse Regular Expressions
- Control Regex behavior using flags

These skills form the foundation of Regex programming in Python.

---

# Topics Covered

## Module Introduction

- Why Python provides the `re` module.
- Importing the module.
- Understanding the Regex Engine.

---

## Searching Functions

| Function | Purpose |
|----------|----------|
| `re.search()` | Find the first match anywhere in the string |
| `re.match()` | Match only at the beginning |
| `re.fullmatch()` | Match the entire string |
| `re.findall()` | Return all matches as a list |
| `re.finditer()` | Return Match Objects for all matches |

---

## Match Object Methods

| Method | Returns |
|---------|----------|
| `group()` | Entire matched text |
| `start()` | Starting index |
| `end()` | Exclusive ending index |
| `span()` | (`start`, `end`) tuple |
| `groups()` | Tuple of captured groups |
| `groupdict()` | Dictionary of named groups |

---

## Text Processing Functions

| Function | Purpose |
|----------|----------|
| `re.sub()` | Replace matched text |
| `re.split()` | Split text using Regex |
| `re.compile()` | Create a reusable Pattern Object |

---

## Regex Flags

| Flag | Purpose |
|------|---------|
| `re.IGNORECASE` | Ignore letter case |
| `re.MULTILINE` | `^` and `$` work on every line |
| `re.DOTALL` | Dot matches newline |
| `re.VERBOSE` | Write readable multi-line Regex |

---

# Complete Regex Workflow

```
Import re

↓

Write Pattern

↓

(Optional)

Compile Pattern

↓

Choose Regex Function

↓

Regex Engine

↓

Match Object

↓

Retrieve Data

↓

Transform / Validate

↓

Final Result
```

This represents a typical Regex workflow used in enterprise applications.

---

# Function Selection Guide

Need to...

| Requirement | Function |
|-------------|----------|
| Find the first match | `re.search()` |
| Check only the beginning | `re.match()` |
| Validate the entire string | `re.fullmatch()` |
| Get all matched strings | `re.findall()` |
| Get all Match Objects | `re.finditer()` |
| Replace text | `re.sub()` |
| Split text | `re.split()` |
| Reuse a pattern | `re.compile()` |

---

# Match Object Quick Reference

Need to retrieve...

| Requirement | Method |
|-------------|--------|
| Matched text | `group()` |
| Start position | `start()` |
| End position | `end()` |
| Start and end together | `span()` |
| Captured groups | `groups()` |
| Named groups | `groupdict()` |

---

# Enterprise Workflow Examples

### Storage Engineering

```
Storage Log

↓

Compile Pattern

↓

Extract Capacity

↓

Validate Format

↓

Generate Report
```

---

### Linux Automation

```
Command Output

↓

Regex Search

↓

Extract IP Address

↓

Validate

↓

Automation Script
```

---

### Test Automation

```
Execution Report

↓

Extract PASS / FAIL

↓

Analyze Results

↓

Generate Summary
```

---

# Best Practices

✔ Use raw strings (`r"..."`).

✔ Compile frequently reused patterns.

✔ Check Match Objects before calling Match Object methods.

✔ Use named groups for readability.

✔ Apply Regex Flags only when needed.

✔ Choose the correct Regex function for the task.

---

# Common Beginner Mistakes

❌ Forgetting `import re`

❌ Calling `group()` on `None`

❌ Confusing `group()` and `groups()`

❌ Forgetting that `end()` is exclusive

❌ Using `findall()` when Match Objects are required

❌ Using `str.replace()` instead of `re.sub()` for Regex-based replacement

---

# Memory Sheet

```
Import

↓

Compile

↓

Search

↓

Match Object

↓

Retrieve Data

↓

Transform

↓

Result
```

---

# One-Page Revision

## Search Functions

```
search()

↓

Anywhere

----------------

match()

↓

Beginning

----------------

fullmatch()

↓

Entire String

----------------

findall()

↓

List

----------------

finditer()

↓

Match Objects
```

---

## Match Object Methods

```
group()

↓

Text

----------------

start()

↓

Beginning

----------------

end()

↓

Exclusive End

----------------

span()

↓

(Start, End)

----------------

groups()

↓

Tuple

----------------

groupdict()

↓

Dictionary
```

---

## Text Processing

```
sub()

↓

Replace

----------------

split()

↓

Split

----------------

compile()

↓

Reusable Pattern
```

---

## Flags

```
IGNORECASE

↓

Ignore Case

----------------

MULTILINE

↓

Every Line

----------------

DOTALL

↓

Dot Matches Newline

----------------

VERBOSE

↓

Readable Regex
```

---

# Interview Questions

### Basic

1. Why do we use the `re` module?
2. What is the purpose of `re.search()`?
3. Difference between `search()` and `match()`.
4. Difference between `match()` and `fullmatch()`.
5. Difference between `findall()` and `finditer()`.

---

### Intermediate

6. What is a Match Object?
7. Explain `group()`, `groups()`, and `groupdict()`.
8. Why is `end()` exclusive?
9. Why should Match Objects be checked before calling `group()`?
10. When should `re.compile()` be used?

---

### Advanced

11. Explain the purpose of Regex Flags.
12. Why are named groups useful?
13. Why use `re.VERBOSE`?
14. Describe a real-world Regex workflow.
15. How would you parse enterprise logs using Python Regex?

---

# Practice Exercises

### Exercise 1

Extract all storage capacities from a storage report.

---

### Exercise 2

Validate software version strings.

---

### Exercise 3

Replace deprecated log messages.

---

### Exercise 4

Split configuration values using multiple delimiters.

---

### Exercise 5

Extract named groups from structured data.

---

# Chapter Achievement

After completing Chapter 6, you can now:

✅ Search text using Regular Expressions.

✅ Validate structured input.

✅ Extract matched information.

✅ Work with Match Objects.

✅ Replace and split text.

✅ Reuse compiled patterns.

✅ Modify matching behavior using Regex Flags.

✅ Apply Regex in Storage Engineering, Linux Automation, Test Automation and general Python programming.

---

# Final Key Takeaways

- The `re` module is Python's standard library for Regular Expressions.
- Different functions serve different purposes: searching, validation, extraction and transformation.
- Match Objects provide detailed information about successful matches.
- `re.compile()` improves reusability and code organization.
- Regex Flags customize matching behavior without changing the pattern.
- Following best practices results in cleaner, safer and more maintainable Regex code.
- You now have a complete foundation for using Regular Expressions effectively in Python.

-----------------------------------------------------------------------------------------------------------

