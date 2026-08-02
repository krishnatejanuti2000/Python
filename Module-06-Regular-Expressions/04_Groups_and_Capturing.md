# Chapter 04 — Groups and Capturing

## Chapter Objective

In the previous chapters, we learned how to describe patterns using:

- Character Classes
- Quantifiers
- Greedy Matching
- Lazy Matching
- Backtracking

Those concepts allow the Regex Engine to determine **whether text matches a pattern**.

However, matching text is often only the first step.

In real-world automation, we usually need to **extract specific portions** of the matched text.

For example, consider the following storage log.

```text
Drive ID     : NVME001
Capacity     : 1024GB
Temperature  : 42C
Health       : GOOD
```

Suppose our goal is not just to verify that the line matches a pattern.

Instead, we want to extract only:

```text
NVME001
```

or

```text
1024GB
```

or

```text
42C
```

This is where **Groups** become essential.

Groups allow us to:

- Organize complex Regular Expressions.
- Capture specific parts of a match.
- Reuse previously matched text.
- Build readable and maintainable Regex patterns.
- Extract structured information from logs and reports.

Throughout this chapter, we will study how the Regex Engine creates, stores and manages Groups during pattern matching.

---

# Topics Covered

1. Why Groups?
2. What is a Group?
3. Capturing Groups
4. Non-Capturing Groups
5. Nested Groups
6. Numbered Groups
7. Named Groups
8. Backreferences
9. Real-World Applications
10. Chapter Summary

-------------------------------------------------------------------------------------------------------------

# 4.1 Why Groups?

## Learning Objective

After completing this lesson, you will be able to:

- Understand why Groups are required in Regular Expressions.
- Identify the limitations of writing patterns without Groups.
- Explain how Groups help organize Regular Expressions.
- Understand why Groups are essential for capturing data.
- Recognize practical situations where Groups simplify complex patterns.

---

# Previous Knowledge

In the previous chapters, we learned how to build Regular Expressions using:

- Character Classes
- Quantifiers
- Greedy Matching
- Lazy Matching
- Backtracking

These concepts allow us to describe **what should be matched** and **how many times it should occur**.

However,

there is still one important limitation.

What if we want to treat **multiple parts of a pattern as a single unit?**

This is where Groups become necessary.

---

# Introduction

Consider the following input.

```text
abab

ababab

abababab
```

Suppose we want to repeat

```text
ab
```

three times.

A beginner might think

```regex
ab{3}
```

will work.

But this actually means

```
a

followed by

bbb
```

because the Quantifier applies only to

```
b
```

and **not** to the entire sequence

```
ab
```

Clearly,

we need a way to tell the Regex Engine that

```
ab
```

should be treated as one unit.

---

# The Problem

Suppose we want to repeat

```
ab
```

three times.

Desired result

```text
ababab
```

Without Groups,

the Regex Engine interprets

```regex
ab{3}
```

as

```
a

↓

b repeated 3 times
```

Result

```text
abbb
```

This is not what we intended.

---

# Another Example

Suppose we have

```text
ERROR123

WARNING456

INFO789
```

Later,

we may want to extract only the numeric part.

Without Groups,

the Regex Engine knows the overall match,

but it has no instruction about which part should be remembered separately.

---

# The Solution

Regular Expressions provide **Groups**.

Groups allow us to:

- Treat multiple patterns as a single unit.
- Apply Quantifiers to an entire pattern.
- Capture specific portions of a match.
- Organize complex Regular Expressions.
- Reuse previously matched text.

---

# Why Do We Need Groups?

Groups solve several important problems.

### Problem 1 — Repetition

Instead of

```regex
ab{3}
```

we write

```regex
(ab){3}
```

Now the Quantifier applies to the entire group.

---

### Problem 2 — Extraction

Suppose we have

```text
Capacity : 2048GB
```

The overall line matches,

but we may only need

```text
2048GB
```

Groups allow the Regex Engine to remember that specific portion for later use.

---

### Problem 3 — Readability

Large Regular Expressions quickly become difficult to understand.

Groups help divide complex expressions into logical sections,

making them easier to read and maintain.

---

# Regex Engine Perspective

Without Groups

```regex
ab{3}
```

Regex Engine

```
Read

a

↓

Read

b

↓

Read Quantifier

{3}

↓

Repeat

b
```

---

With Groups

```regex
(ab){3}
```

Regex Engine

```
Read Group

(ab)

↓

Treat Entire Group

As One Unit

↓

Read Quantifier

{3}

↓

Repeat Entire Group
```

The behavior changes completely.

---

# Engine Visualization

```
             Pattern

            (ab){3}

               │
               ▼

      +------------------+
      |   Regex Engine   |
      +------------------+

               │
               ▼

       Read Group (ab)

               │
               ▼

 Treat Group As One Unit

               │
               ▼

 Apply Quantifier

               │
               ▼

 Repeat Entire Group
```

---

# Real-World Usage

Groups are used extensively in:

### Storage Engineering

Extracting:

- Drive ID
- Capacity
- Temperature
- Firmware Version

---

### Linux Automation

Extracting:

- Process IDs
- IP Addresses
- Filesystem Names
- Mount Points

---

### Python Automation

Extracting:

- Log Fields
- Configuration Values
- CSV Columns
- Report Data

---

### Test Automation

Capturing:

- Expected Values
- Actual Values
- Error Messages
- Execution Times

---

# Important Observation

Groups do **not** change what the Regex matches.

Instead,

they change **how the Regex Engine treats portions of the pattern**.

Groups allow multiple smaller patterns to behave as one logical unit.

---

# Common Beginner Mistakes

### Mistake 1

Thinking parentheses are used only for readability.

In Regex,

parentheses have functional meaning.

---

### Mistake 2

Thinking Quantifiers automatically apply to multiple characters.

A Quantifier only applies to the immediately preceding pattern unless Groups are used.

---

### Mistake 3

Thinking Groups are only for capturing.

Capturing is only one use of Groups.

Grouping itself is equally important.

---

# Interview Questions

1. Why do we need Groups in Regular Expressions?

2. What problem do Groups solve?

3. Why does

```regex
ab{3}
```

not produce

```text
ababab
```

4. Give practical applications of Groups.

---

# Practice Questions

### Question 1

Explain why

```regex
(ab){3}
```

behaves differently from

```regex
ab{3}
```

---

### Question 2

List five real-world situations where Groups are useful.

---

### Question 3

Why are Groups important for automation?

---

# Memory Tip

```
Without Groups

↓

Quantifier

↓

One Pattern

------------------------

With Groups

↓

Quantifier

↓

Entire Group
```

Remember

```
()

↓

Treat

Multiple Patterns

As

One Unit
```

---

# Revision Box

✔ Groups combine multiple patterns into one logical unit.

✔ Quantifiers can be applied to an entire Group.

✔ Groups improve readability and maintainability.

✔ Groups make data extraction possible.

✔ Groups are heavily used in automation and log parsing.

---

# Key Takeaways

- Groups allow multiple patterns to be treated as a single unit.
- They solve problems involving repetition, extraction and organization.
- Quantifiers applied to Groups affect the entire grouped pattern.
- Groups are one of the most important building blocks for practical Regular Expressions.

---

# Coming Up

Now that we understand **why Groups are needed**,

the next lesson introduces the formal definition of a Group, its basic syntax using `()`, and how the Regex Engine creates and processes Groups during pattern matching.

-------------------------------------------------------------------------------------------------------------

# 4.2 What is a Group?

## Learning Objective

After completing this lesson, you will be able to:

- Define a Group in Regular Expressions.
- Understand the syntax of Groups.
- Explain how the Regex Engine processes Groups.
- Distinguish between individual patterns and grouped patterns.
- Recognize how Groups become the foundation for Capturing Groups and Backreferences.

---

# Previous Knowledge

In the previous lesson, we learned **why Groups are required**.

We discovered that:

- Quantifiers normally apply only to the immediately preceding pattern.
- Sometimes multiple patterns must behave as a single unit.
- Groups solve this problem.

Now we will formally define what a Group is.

---

# Introduction

Consider the following pattern.

```regex
(ab){3}
```

Input

```text
ababab
```

The Regex Engine treats

```text
ab
```

as **one logical unit**.

The Quantifier

```regex
{3}
```

is therefore applied to the entire sequence

```
ab
```

rather than only to

```
b
```

This behavior is made possible by **Groups**.

---

# Definition

A **Group** is a portion of a Regular Expression enclosed within parentheses.

```regex
(...)
```

The Regex Engine treats everything inside the parentheses as **one logical unit**.

Groups allow multiple patterns to be processed together instead of individually.

---

# Syntax

General Syntax

```regex
(pattern)
```

Examples

```regex
(ab)
```

```regex
(\d+)
```

```regex
([A-Z]{3})
```

```regex
(Drive\sID)
```

---

# Understanding the Syntax

Pattern

```regex
(ab)
```

The Group contains

```
a

↓

b
```

The Regex Engine first evaluates the contents of the Group.

The entire result is then treated as one pattern.

---

Another example

```regex
([A-Z]{3})
```

The Group contains

```
Three Uppercase Letters
```

The entire sequence becomes one logical unit.

---

# Without Groups

Pattern

```regex
ab{2}
```

Regex Engine Interpretation

```
a

↓

b repeated twice
```

Result

```text
abb
```

---

# With Groups

Pattern

```regex
(ab){2}
```

Regex Engine Interpretation

```
Group

↓

ab

↓

Repeat Entire Group
```

Result

```text
abab
```

---

# Regex Engine Explanation

Pattern

```regex
(ab){2}
```

Input

```text
abab
```

Regex Engine

```
Read

(

↓

Start New Group

↓

Read

a

↓

Read

b

↓

)

↓

End Group

↓

Store Group

↓

Read

{2}

↓

Repeat Stored Group
```

Notice that the Regex Engine does not repeat individual characters.

It repeats the **entire grouped pattern**.

---

# Engine Visualization

```
             Pattern

            (ab){2}

                │
                ▼

      +------------------+
      |   Regex Engine   |
      +------------------+

                │
                ▼

        Start Group

                │
                ▼

         Read Contents

                │
                ▼

          End Group

                │
                ▼

     Treat As One Unit

                │
                ▼

      Apply Quantifier
```

---

# Engine Trace

Pattern

```regex
(ab){2}
```

Input

```text
abab
```

```
Regex Engine Trace

--------------------------------------

Read

(

↓

Start Group

↓

Read

a

↓

Read

b

↓

Group Complete

↓

Read

{2}

↓

Repeat Group

↓

First Match

ab

↓

Second Match

ab

↓

SUCCESS
```

---

# Matching Matrix

Pattern

```regex
(ab){2}
```

| Input | Match | Reason |
|------|:-----:|--------|
| `ab` | ❌ | Only one repetition |
| `abab` | ✅ | Two repetitions |
| `ababab` | ✅* | First two repetitions satisfy the pattern |
| `abb` | ❌ | Group structure differs |
| `aabb` | ❌ | Characters are not grouped correctly |

> **Note**
>
> The pattern `(ab){2}` matches **two consecutive repetitions** of `ab`.
>
> It does not require the entire input to end after the match unless anchors (`^` and `$`) are used.

---

# Compare & Contrast

| Without Groups | With Groups |
|----------------|------------|
| Quantifier affects one pattern | Quantifier affects entire Group |
| `ab{2}` → `abb` | `(ab){2}` → `abab` |
| Difficult to organize large patterns | Easier to organize complex patterns |

---

# Real-World Usage

Groups are commonly used for:

### Storage Engineering

- Drive identifiers
- Firmware versions
- Capacity fields

---

### Linux Automation

- IP addresses
- Device names
- Mount information

---

### Python Automation

- Log parsing
- Configuration extraction
- Report processing

---

### Test Automation

- Capturing expected values
- Extracting execution results
- Validating structured output

---

# Important Observation

A Group itself does **not** change what is matched.

It changes **how the Regex Engine processes multiple patterns together**.

Later,

the same Group can also be used for:

- Capturing
- Backreferences
- Named Groups
- Nested Groups

---

# Common Beginner Mistakes

### Mistake 1

Thinking parentheses are decorative.

In Regex,

parentheses have operational meaning.

---

### Mistake 2

Thinking every Group is only for capturing.

Grouping and capturing are related,

but they are not the same concept.

---

### Mistake 3

Forgetting that Quantifiers applied after a Group affect the **entire Group**.

---

# Interview Questions

1. What is a Group in Regular Expressions?

2. What is the syntax of a Group?

3. Why does `(ab){2}` behave differently from `ab{2}`?

4. How does the Regex Engine process a Group?

5. Why are Groups important in automation?

---

# Practice Questions

### Question 1

Explain the difference between

```regex
ab{3}
```

and

```regex
(ab){3}
```

---

### Question 2

Write three practical situations where Groups simplify a Regular Expression.

---

### Question 3

Why are Groups considered one logical unit by the Regex Engine?

---

# Memory Tip

```
()

↓

Start Group

↓

End Group

↓

Treat Everything

Inside

As One Unit
```

Remember

```
Parentheses

↓

Logical Unit
```

---

# Revision Box

✔ A Group is enclosed within parentheses `()`.

✔ The Regex Engine treats everything inside a Group as one logical unit.

✔ Quantifiers applied after a Group affect the entire Group.

✔ Groups improve readability and simplify complex Regular Expressions.

✔ Groups form the foundation for Capturing Groups, Named Groups and Backreferences.

---

# Key Takeaways

- A Group combines multiple patterns into one logical unit.
- Parentheses define the boundaries of a Group.
- The Regex Engine processes the Group as a single pattern.
- Groups enable repetition, organization and advanced Regex features.
- Understanding Groups is essential before learning Capturing Groups.

---

# Coming Up

So far, we have learned **how Groups organize patterns**.

The next lesson introduces **Capturing Groups**, where the Regex Engine not only matches a Group but also **stores its matched text** so that it can be retrieved and reused later.

-------------------------------------------------------------------------------------------------------------

# 4.3 Capturing Groups

## Learning Objective

After completing this lesson, you will be able to:

- Understand what a Capturing Group is.
- Explain how the Regex Engine stores matched Groups.
- Understand how Groups receive group numbers.
- Distinguish between matching and capturing.
- Recognize practical situations where Capturing Groups are used.

---

# Previous Knowledge

In the previous lesson, we learned that Groups allow multiple patterns to behave as a single logical unit.

Example

```regex
(ab){3}
```

The Regex Engine treats

```
ab
```

as one unit.

However,

Groups provide another powerful capability.

They can **remember the text they match**.

This behavior is called **Capturing**.

---

# Introduction

Consider the following input.

```text
Drive ID : NVME001
```

Suppose our pattern is

```regex
Drive ID : ([A-Z]+\d+)
```

The overall Regular Expression matches

```text
Drive ID : NVME001
```

But suppose we only need

```text
NVME001
```

instead of the entire line.

A Capturing Group allows the Regex Engine to **store**

```text
NVME001
```

so it can be retrieved later.

---

# Why Do We Need Capturing Groups?

Suppose a storage log contains

```text
Capacity : 1024GB

Temperature : 42C

Firmware : 3.5.1
```

The overall line is useful,

but automation scripts usually need only the value.

Examples

```
1024GB

42C

3.5.1
```

Capturing Groups allow us to extract only the required portion.

---

# Definition

A **Capturing Group** is a Group whose matched text is automatically stored by the Regex Engine.

Every successful Capturing Group receives:

- A Group Number
- The Text Matched by that Group

This stored value can later be accessed by the programming language.

---

# Syntax

General Syntax

```regex
(pattern)
```

Examples

```regex
(\d+)
```

```regex
([A-Z]+)
```

```regex
([A-Z]+\d+)
```

```regex
(Capacity : (\d+GB))
```

By default,

every Group created with

```regex
()
```

is a Capturing Group.

---

# Matching vs Capturing

These are two different concepts.

### Matching

Determines whether the pattern exists.

Example

```regex
\d+
```

Input

```text
512GB
```

Match

```text
512
```

---

### Capturing

Stores the matched text.

Example

```regex
(\d+)
```

Stored Group

```text
512
```

Matching answers

```
Did the pattern match?
```

Capturing answers

```
What exactly matched?
```

---

# Regex Engine Explanation

Pattern

```regex
([A-Z]+\d+)
```

Input

```text
NVME001
```

Regex Engine

```
Read

(

↓

Start Group

↓

Read

[A-Z]+

↓

Match

NVME

↓

Read

\d+

↓

Match

001

↓

)

↓

End Group

↓

Store

NVME001

↓

Assign

Group 1
```

Notice that the Regex Engine stores the matched text after the Group successfully completes.

---

# Engine Visualization

```
              Pattern

          ([A-Z]+\d+)

                 │
                 ▼

       +------------------+
       |   Regex Engine   |
       +------------------+

                 │
                 ▼

          Start Group

                 │
                 ▼

          Match Pattern

                 │
                 ▼

           End Group

                 │
                 ▼

        Store Matched Text

                 │
                 ▼

        Assign Group Number
```

---

# Engine Trace

Pattern

```regex
([A-Z]+\d+)
```

Input

```text
NVME001
```

```
Regex Engine Trace

--------------------------------------

(

↓

Start Group

↓

[A-Z]+

↓

Matches

NVME

↓

\d+

↓

Matches

001

↓

)

↓

End Group

↓

Captured Text

NVME001

↓

Group Number

1

↓

SUCCESS
```

---

# Matching Matrix

Pattern

```regex
([A-Z]+\d+)
```

| Input | Overall Match | Group 1 |
|------|---------------|----------|
| `NVME001` | ✅ | `NVME001` |
| `SSD25` | ✅ | `SSD25` |
| `123ABC` | ❌ | — |
| `NVME` | ❌ | — |

---

# Compare & Contrast

| Normal Group | Capturing Group |
|--------------|-----------------|
| Groups patterns together | Groups patterns together |
| Can receive Quantifiers | Can receive Quantifiers |
| Stores nothing | Stores matched text |
| Foundation for organization | Foundation for extraction |

> **Note**
>
> In most Regex engines (including Python), ordinary parentheses `()` are **capturing by default**.
>
> We will learn **Non-Capturing Groups** later in this chapter.

---

# Real-World Usage

Capturing Groups are used extensively for extracting:

### Storage Engineering

- Drive ID
- Capacity
- Temperature
- Firmware Version
- Serial Number

---

### Linux Automation

- IP Address
- Process ID
- Filesystem Name
- Device Name

---

### Python Automation

- CSV Fields
- Log Values
- Configuration Values
- Report Fields

---

### Test Automation

- Expected Output
- Actual Output
- Error Codes
- Execution Time

---

# Important Observation

A Capturing Group performs **two jobs** simultaneously.

```
Group

↓

Matches Pattern

↓

Stores Match
```

Grouping and Capturing happen together unless a Non-Capturing Group is explicitly used.

---

# Common Beginner Mistakes

### Mistake 1

Thinking every match is automatically stored.

Only Capturing Groups store matched text.

---

### Mistake 2

Thinking Capturing changes what the Regex matches.

Capturing stores the match.

It does not change the matching rules.

---

### Mistake 3

Confusing the overall match with the captured Group.

The entire Regular Expression may match more text than the Capturing Group stores.

---

# Interview Questions

1. What is a Capturing Group?

2. How does the Regex Engine process a Capturing Group?

3. What information does the Regex Engine store for each Capturing Group?

4. What is the difference between matching and capturing?

5. Give practical uses of Capturing Groups.

---

# Practice Questions

### Question 1

Pattern

```regex
([A-Z]+\d+)
```

Input

```text
NVME001
```

What is:

- The overall match?
- Group 1?

---

### Question 2

Why are Capturing Groups useful in automation?

---

### Question 3

Give five practical examples where Capturing Groups are required.

---

# Memory Tip

```
()

↓

Group

↓

Match

↓

Store

↓

Capture
```

Remember

```
Capturing Group

=

Remember

What

Matched
```

---

# Revision Box

✔ A Capturing Group stores the text matched by the Group.

✔ Parentheses `()` create Capturing Groups by default.

✔ Each successful Capturing Group receives a Group Number.

✔ Capturing is essential for data extraction and automation.

✔ Matching and Capturing are related but different concepts.

---

# Key Takeaways

- Capturing Groups organize patterns and store matched text.
- The Regex Engine automatically assigns group numbers to Capturing Groups.
- Captured values can later be accessed by programming languages such as Python.
- Capturing Groups are fundamental for log parsing, report processing and automation.

---

# Coming Up

Now that we understand **what a Capturing Group is**,

the next lesson explains **Group Numbering**, showing how the Regex Engine assigns numbers to multiple Capturing Groups and how those numbers are used to retrieve captured values.

-------------------------------------------------------------------------------------------------------------

# 4.4 Group Numbering

## Learning Objective

After completing this lesson, you will be able to:

- Understand how the Regex Engine assigns Group Numbers.
- Explain the numbering order of Capturing Groups.
- Predict Group Numbers in complex Regular Expressions.
- Understand why Group Numbers are important for data extraction.
- Prepare for Multiple Capturing Groups and Backreferences.

---

# Previous Knowledge

In the previous lesson, we learned that every Capturing Group stores the text it matches.

Example

```regex
([A-Z]+\d+)
```

The Regex Engine stores

```text
NVME001
```

as

```
Group 1
```

But what happens if a Regular Expression contains multiple Capturing Groups?

The Regex Engine needs a way to identify each captured value.

It does this using **Group Numbers**.

---

# Introduction

Consider the following pattern.

```regex
([A-Z]+)-(\d+)
```

Input

```text
NVME-001
```

The Regex Engine captures

```
NVME

↓

001
```

Both Groups are stored separately.

To distinguish them,

the Regex Engine assigns numbers.

```
First Group

↓

Group 1

---------------------

Second Group

↓

Group 2
```

---

# Why Do We Need Group Numbers?

Suppose we have

```text
Drive : NVME001

Capacity : 1024GB
```

Pattern

```regex
(Drive)\s:\s([A-Z]+\d+)
```

The Regex Engine captures

```
Drive

↓

NVME001
```

If both Groups were simply called

```
Captured Value
```

there would be no way to distinguish them.

Group Numbers uniquely identify each Captured Group.

---

# Definition

A **Group Number** is the numeric identifier automatically assigned to every Capturing Group by the Regex Engine.

Numbering begins at

```
1
```

and proceeds

**from left to right**

based on the opening parenthesis.

---

# Numbering Rule

The Regex Engine assigns Group Numbers according to this rule.

```
Read Pattern

↓

Encounter

(

↓

Assign Next Group Number
```

The numbering depends on the **opening parenthesis**, not on where the Group ends.

---

# Example 1

Pattern

```regex
([A-Z]+)(\d+)
```

Input

```text
NVME001
```

Groups

| Group | Captured Text |
|--------|---------------|
| Group 1 | `NVME` |
| Group 2 | `001` |

---

# Example 2

Pattern

```regex
(Drive)\s(ID)
```

Input

```text
Drive ID
```

Groups

| Group | Captured Text |
|--------|---------------|
| Group 1 | `Drive` |
| Group 2 | `ID` |

---

# Regex Engine Explanation

Pattern

```regex
([A-Z]+)(\d+)
```

Regex Engine

```
Read

(

↓

Assign

Group 1

↓

Read

[A-Z]+

↓

)

↓

End Group 1

↓

Read

(

↓

Assign

Group 2

↓

Read

\d+

↓

)

↓

End Group 2
```

Notice that numbering happens when the Regex Engine encounters the **opening parenthesis**.

---

# Engine Visualization

```
             Pattern

      ([A-Z]+)(\d+)

                 │
                 ▼

      +------------------+
      |   Regex Engine   |
      +------------------+

                 │
                 ▼

Encounter (

↓

Assign Group 1

↓

Read Group

↓

Encounter (

↓

Assign Group 2

↓

Read Group
```

---

# Engine Trace

Pattern

```regex
([A-Z]+)(\d+)
```

Input

```text
NVME001
```

```
Regex Engine Trace

--------------------------------------

(

↓

Group 1 Assigned

↓

Matches

NVME

↓

)

↓

Group 1 Stored

↓

(

↓

Group 2 Assigned

↓

Matches

001

↓

)

↓

Group 2 Stored

↓

SUCCESS
```

---

# Matching Matrix

Pattern

```regex
([A-Z]+)(\d+)
```

| Input | Group 1 | Group 2 |
|------|---------|---------|
| `NVME001` | `NVME` | `001` |
| `SSD25` | `SSD` | `25` |
| `ABC1234` | `ABC` | `1234` |

---

# Compare & Contrast

| Pattern | Group 1 | Group 2 |
|---------|---------|---------|
| `([A-Z]+)` | Letters | — |
| `([A-Z]+)(\d+)` | Letters | Digits |
| `(Drive)(ID)` | Drive | ID |

---

# Real-World Usage

Group Numbers are heavily used for extracting:

### Storage Engineering

- Drive Name
- Capacity
- Temperature

---

### Linux Automation

- IP Address
- Port Number
- Filesystem Name

---

### Python Automation

Using Python's `re` module,

Group Numbers are commonly accessed as

```python
match.group(1)

match.group(2)
```

We will study these methods in **Chapter 6 — Python `re` Module**.

---

# Important Observation

Group Numbers are assigned

**from left to right**

using the **opening parenthesis**.

The closing parenthesis has no effect on numbering.

---

# Common Beginner Mistakes

### Mistake 1

Thinking numbering starts from zero.

Capturing Groups start at

```
Group 1
```

---

### Mistake 2

Thinking numbering depends on where a Group ends.

It depends only on the **opening parenthesis**.

---

### Mistake 3

Confusing the overall match with Group Numbers.

The overall match contains the entire Regular Expression.

Group Numbers identify individual Capturing Groups.

---

# Interview Questions

1. What is a Group Number?

2. How does the Regex Engine assign Group Numbers?

3. Does numbering depend on the opening or closing parenthesis?

4. Why are Group Numbers important?

5. How are Group Numbers used in Python?

---

# Practice Questions

### Question 1

Determine the Group Numbers for

```regex
([A-Z]+)-(\d+)
```

---

### Question 2

Explain why numbering begins with

```
1
```

instead of

```
0
```

---

### Question 3

Predict the captured Groups for

```regex
(Drive)(ID)(\d+)
```

---

# Memory Tip

```
(

↓

Opening Parenthesis

↓

Assign

Next Group Number
```

Remember

```
Left

↓

Right

↓

Opening Parenthesis
```

---

# Revision Box

✔ Every Capturing Group receives a Group Number.

✔ Numbering begins with Group 1.

✔ Groups are numbered from left to right.

✔ Numbering depends on the opening parenthesis.

✔ Group Numbers make captured values easy to retrieve.

---

# Key Takeaways

- The Regex Engine automatically numbers Capturing Groups.
- Numbering starts at 1 and proceeds from left to right.
- The opening parenthesis determines the Group Number.
- Group Numbers are essential for extracting individual captured values.
- Understanding Group Numbering prepares you for Multiple Capturing Groups and Backreferences.

---

# Coming Up

Now that we know **how Groups receive numbers**,

the next lesson demonstrates **Multiple Capturing Groups**, showing how several Groups work together to extract structured data from a single match.

-------------------------------------------------------------------------------------------------------------

# 4.5 Multiple Capturing Groups

## Learning Objective

After completing this lesson, you will be able to:

- Understand how multiple Capturing Groups work together.
- Explain how the Regex Engine stores multiple captured values.
- Predict the contents of each Group.
- Extract multiple fields from a single input.
- Prepare for Nested Groups and Backreferences.

---

# Previous Knowledge

In the previous lesson, we learned that every Capturing Group receives a Group Number.

Example

```regex
([A-Z]+)(\d+)
```

Input

```text
NVME001
```

Captured Groups

```
Group 1

↓

NVME

--------------------

Group 2

↓

001
```

Real-world data, however, usually contains multiple pieces of information.

The Regex Engine must capture all of them independently.

---

# Introduction

Consider the following storage log.

```text
Drive=NVME001 Capacity=1024GB Health=GOOD
```

Suppose we need to extract

```
NVME001

1024GB

GOOD
```

One Capturing Group is not enough.

Instead,

we create multiple Capturing Groups.

---

# Why Do We Need Multiple Capturing Groups?

Automation rarely extracts only one value.

Storage logs may contain

```text
Drive=NVME001 Capacity=1024GB Health=GOOD
```

Linux output may contain

```text
Filesystem=/dev/sda1 Size=500G Used=120G
```

Configuration files may contain

```text
HOST=10.10.20.15 PORT=8080 MODE=production
```

Each field should be captured separately.

---

# Example Pattern

```regex
Drive=([A-Z]+\d+)\sCapacity=(\d+GB)\sHealth=([A-Z]+)
```

Input

```text
Drive=NVME001 Capacity=1024GB Health=GOOD
```

Captured Values

| Group | Captured Text |
|--------|---------------|
| Group 1 | `NVME001` |
| Group 2 | `1024GB` |
| Group 3 | `GOOD` |

---

# Definition

**Multiple Capturing Groups** allow a single Regular Expression to store multiple independent portions of a successful match.

Each Group receives

- its own Group Number
- its own captured text

The captured values remain independent of one another.

---

# Regex Engine Explanation

Pattern

```regex
Drive=([A-Z]+\d+)\sCapacity=(\d+GB)\sHealth=([A-Z]+)
```

Regex Engine

```
Read

Drive=

↓

(

↓

Assign Group 1

↓

Match

NVME001

↓

Store Group 1

↓

(

↓

Assign Group 2

↓

Match

1024GB

↓

Store Group 2

↓

(

↓

Assign Group 3

↓

Match

GOOD

↓

Store Group 3

↓

SUCCESS
```

Notice that each completed Group is stored independently.

---

# Engine Visualization

```
                 Pattern

Drive=(...)\sCapacity=(...)\sHealth=(...)

                      │
                      ▼

             +------------------+
             |   Regex Engine   |
             +------------------+

                      │
                      ▼

             Group 1 Stored

                      │
                      ▼

             Group 2 Stored

                      │
                      ▼

             Group 3 Stored

                      │
                      ▼

              Overall Match
```

---

# Engine Trace

Pattern

```regex
Drive=([A-Z]+\d+)\sCapacity=(\d+GB)\sHealth=([A-Z]+)
```

Input

```text
Drive=NVME001 Capacity=1024GB Health=GOOD
```

```
Regex Engine Trace

--------------------------------------

Read

Drive=

↓

Group 1

↓

Captured

NVME001

↓

Group 2

↓

Captured

1024GB

↓

Group 3

↓

Captured

GOOD

↓

SUCCESS
```

---

# Capture Table

| Overall Match | Group 1 | Group 2 | Group 3 |
|---------------|---------|---------|---------|
| `Drive=NVME001 Capacity=1024GB Health=GOOD` | `NVME001` | `1024GB` | `GOOD` |

This is one of the most useful ways to visualize Capturing Groups.

---

# Matching Matrix

Pattern

```regex
Drive=([A-Z]+\d+)\sCapacity=(\d+GB)\sHealth=([A-Z]+)
```

| Input | G1 | G2 | G3 |
|------|----|----|----|
| `Drive=NVME001 Capacity=1024GB Health=GOOD` | `NVME001` | `1024GB` | `GOOD` |
| `Drive=SSD25 Capacity=512GB Health=BAD` | `SSD25` | `512GB` | `BAD` |

---

# Compare & Contrast

| Single Capturing Group | Multiple Capturing Groups |
|-------------------------|---------------------------|
| Captures one value | Captures several values |
| One Group Number | Multiple Group Numbers |
| Simple extraction | Structured extraction |

---

# Real-World Usage

Multiple Capturing Groups are widely used for:

### Storage Engineering

Extract simultaneously:

- Drive ID
- Capacity
- Temperature
- Health Status

---

### Linux Automation

Extract:

- Filesystem
- Total Size
- Used Space
- Available Space

---

### Python Automation

Extract:

- Configuration Keys
- Values
- Log Fields
- CSV Columns

---

### Test Automation

Extract:

- Expected Value
- Actual Value
- Execution Time
- Test Status

---

# Python Preview

Later, in **Chapter 6**, these Groups will be retrieved as

```python
match.group(1)

match.group(2)

match.group(3)
```

or all at once using

```python
match.groups()
```

This is why understanding Multiple Capturing Groups is important.

---

# Important Observation

The entire Regular Expression still produces **one overall match**.

The Capturing Groups simply divide that match into meaningful pieces.

Think of it like this:

```
Overall Match

↓

Split Into

↓

Group 1

Group 2

Group 3
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking each Group performs a separate Regex search.

All Groups belong to the same overall match.

---

### Mistake 2

Confusing the overall match with the captured values.

The overall match contains everything matched by the Regular Expression.

Each Group stores only its own portion.

---

### Mistake 3

Assuming Groups are numbered based on where they finish.

They are numbered according to the opening parenthesis.

---

# Interview Questions

1. What are Multiple Capturing Groups?

2. How does the Regex Engine store multiple captured values?

3. What is the difference between the overall match and individual Groups?

4. How are Multiple Capturing Groups used in Python?

5. Give practical examples where Multiple Capturing Groups are useful.

---

# Practice Questions

### Question 1

Determine the captured values.

Pattern

```regex
([A-Z]+)-(\d+)-([A-Z]+)
```

Input

```text
NVME-001-GOOD
```

---

### Question 2

Why are Multiple Capturing Groups useful in Storage Automation?

---

### Question 3

Create a capture table for

```text
Filesystem=/dev/sda1 Size=500G Used=120G
```

---

# Memory Tip

```
One Regex

↓

One Match

↓

Many Groups

↓

Many Captured Values
```

Remember

```
Overall Match

↓

Divide Into

↓

Group 1

Group 2

Group 3
```

---

# Revision Box

✔ One Regular Expression can contain multiple Capturing Groups.

✔ Each Group stores its own matched text.

✔ Every Group has a unique Group Number.

✔ Multiple Capturing Groups make structured data extraction possible.

✔ They are heavily used in automation and Python's `re` module.

---

# Key Takeaways

- Multiple Capturing Groups allow one Regular Expression to extract multiple independent values.
- The Regex Engine stores each Group separately.
- The overall match remains a single match, while Groups provide structured access to individual fields.
- This concept is fundamental for log parsing, configuration parsing and automation.

---

# Coming Up

So far, all our Groups have been arranged one after another.

The next lesson introduces **Nested Groups**, where one Group is placed inside another, allowing the Regex Engine to create hierarchical Group structures.

-------------------------------------------------------------------------------------------------------------

# 4.6 Nested Groups

## Learning Objective

After completing this lesson, you will be able to:

- Understand what Nested Groups are.
- Explain how the Regex Engine processes Nested Groups.
- Predict Group Numbers in Nested Group structures.
- Understand how outer and inner Groups capture text.
- Apply Nested Groups in practical Regular Expressions.

---

# Previous Knowledge

In the previous lesson, we learned that a Regular Expression may contain multiple Capturing Groups.

Example

```regex
([A-Z]+)(\d+)
```

Each Group captures its own portion of the input.

Sometimes,

however,

one Group naturally belongs inside another Group.

This is called **Nested Grouping**.

---

# Introduction

Consider the following pattern.

```regex
((NVME)(\d+))
```

Input

```text
NVME001
```

Notice something interesting.

There are Groups inside another Group.

```
Outer Group

↓

NVME001

-------------------

Inner Group

↓

NVME

-------------------

Inner Group

↓

001
```

The Regex Engine must keep track of every Group independently.

---

# Why Do We Need Nested Groups?

Suppose we have

```text
Firmware : 3.5.12
```

Sometimes we need

```
3.5.12
```

Sometimes we need

```
3

↓

5

↓

12
```

Nested Groups allow us to capture

both the complete value

and

its individual components.

---

# Definition

A **Nested Group** is a Capturing Group that is completely enclosed within another Capturing Group.

Both the outer Group and the inner Group participate independently in matching and capturing.

---

# Syntax

General Syntax

```regex
((pattern))
```

Example

```regex
((NVME)(\d+))
```

Another Example

```regex
((\d+)\.(\d+)\.(\d+))
```

---

# Regex Engine Explanation

Pattern

```regex
((NVME)(\d+))
```

Input

```text
NVME001
```

Regex Engine

```
Read

(

↓

Assign

Group 1

↓

Read

(

↓

Assign

Group 2

↓

Match

NVME

↓

Store

Group 2

↓

Read

(

↓

Assign

Group 3

↓

Match

001

↓

Store

Group 3

↓

Outer Group Complete

↓

Store

Group 1

↓

SUCCESS
```

Notice that

Group Numbers are assigned

**when the opening parenthesis is encountered**,

even though the outer Group finishes last.

---

# Engine Visualization

```
                Pattern

          ((NVME)(\d+))

                    │
                    ▼

          +------------------+
          |   Regex Engine   |
          +------------------+

                    │
                    ▼

           Group 1 Begins

                    │
          ┌─────────┴─────────┐
          ▼                   ▼

      Group 2            Group 3

          │                   │
          ▼                   ▼

      Capture             Capture

          └─────────┬─────────┘
                    ▼

            Store Group 1
```

---

# Engine Trace

Pattern

```regex
((NVME)(\d+))
```

Input

```text
NVME001
```

```
Regex Engine Trace

--------------------------------------

(

↓

Assign Group 1

↓

(

↓

Assign Group 2

↓

Match

NVME

↓

Store Group 2

↓

(

↓

Assign Group 3

↓

Match

001

↓

Store Group 3

↓

Outer Group Complete

↓

Store Group 1

↓

SUCCESS
```

---

# Capture Table

| Overall Match | Group 1 | Group 2 | Group 3 |
|---------------|---------|---------|---------|
| `NVME001` | `NVME001` | `NVME` | `001` |

Notice that the outer Group captures

```
NVME001
```

while the inner Groups capture their own portions.

---

# Another Example

Pattern

```regex
((\d+)\.(\d+)\.(\d+))
```

Input

```text
3.5.12
```

Capture Table

| Overall Match | Group 1 | Group 2 | Group 3 | Group 4 |
|---------------|---------|---------|---------|---------|
| `3.5.12` | `3.5.12` | `3` | `5` | `12` |

---

# Matching Matrix

Pattern

```regex
((NVME)(\d+))
```

| Input | Group 1 | Group 2 | Group 3 |
|------|---------|---------|---------|
| `NVME001` | `NVME001` | `NVME` | `001` |
| `NVME25` | `NVME25` | `NVME` | `25` |

---

# Compare & Contrast

| Multiple Groups | Nested Groups |
|-----------------|---------------|
| Groups are independent | One Group contains another |
| Sequential structure | Hierarchical structure |
| Easier numbering | Requires careful numbering |

---

# Real-World Usage

Nested Groups are useful for:

### Storage Engineering

- Firmware Versions
- Serial Numbers
- Device Identifiers

---

### Linux Automation

- IPv4 Addresses
- Version Numbers
- Kernel Releases

---

### Python Automation

- Structured Log Parsing
- Configuration Values
- CSV Processing

---

### Test Automation

- Extracting composite values
- Breaking structured output into components

---

# Important Observation

Nested Groups create

```
One Overall Match

↓

Outer Group

↓

Inner Groups
```

Every Group is stored independently.

The outer Group usually contains everything matched by the inner Groups.

---

# Common Beginner Mistakes

### Mistake 1

Thinking nested Groups receive numbers after the outer Group finishes.

Numbering depends on the **opening parenthesis**, not the closing parenthesis.

---

### Mistake 2

Thinking only the innermost Group is captured.

Every Capturing Group stores its own match.

---

### Mistake 3

Confusing the outer Group with the overall match.

They are often identical,

but they are conceptually different.

---

# Interview Questions

1. What is a Nested Group?

2. How are Nested Groups numbered?

3. What does the outer Group capture?

4. What do the inner Groups capture?

5. Give practical examples of Nested Groups.

---

# Practice Questions

### Question 1

Determine the captured values.

Pattern

```regex
((ABC)(123))
```

Input

```text
ABC123
```

---

### Question 2

Create the capture table for

```regex
((\d+)\.(\d+))
```

Input

```text
10.25
```

---

### Question 3

Why are Nested Groups useful in automation?

---

# Memory Tip

```
Outer Group

↓

Contains

↓

Inner Groups

↓

Every Group

Captures

Its Own Match
```

Remember

```
Nested

≠

Shared

Every Group

Stores

Its Own Value
```

---

# Revision Box

✔ A Nested Group is a Group inside another Group.

✔ Both outer and inner Groups capture matched text.

✔ Group Numbers are assigned from left to right using the opening parenthesis.

✔ Nested Groups allow hierarchical data extraction.

✔ Nested Groups are widely used for structured data such as version numbers and composite identifiers.

---

# Key Takeaways

- Nested Groups create hierarchical Group structures.
- Every Capturing Group stores its own matched text independently.
- The Regex Engine numbers Nested Groups exactly like ordinary Groups.
- Nested Groups make it possible to extract both complete values and their individual components.
- Understanding Nested Groups prepares you for Non-Capturing Groups and Backreferences.

---

# Coming Up

So far, every Group we've created has automatically captured its matched text.

The next lesson introduces **Non-Capturing Groups**, where the Regex Engine groups patterns **without storing** the matched text, improving readability and avoiding unnecessary Group Numbers.

-------------------------------------------------------------------------------------------------------------

# 4.7 Non-Capturing Groups

## Learning Objective

After completing this lesson, you will be able to:

- Understand what a Non-Capturing Group is.
- Explain why Non-Capturing Groups exist.
- Distinguish between Capturing and Non-Capturing Groups.
- Explain how the Regex Engine processes Non-Capturing Groups.
- Identify situations where Non-Capturing Groups improve Regular Expressions.

---

# Previous Knowledge

In the previous lessons, we learned that Groups serve two purposes:

- Treat multiple patterns as one logical unit.
- Store matched text (Capturing).

Every Group created using

```regex
()
```

automatically becomes a Capturing Group.

However,

sometimes we only need grouping.

We do **not** need to store the matched text.

Regex provides **Non-Capturing Groups** for this purpose.

---

# Introduction

Consider the following pattern.

```regex
(?:ab){3}
```

Input

```text
ababab
```

The Regex Engine still treats

```
ab
```

as one logical unit.

The Quantifier

```regex
{3}
```

still repeats the entire sequence.

However,

unlike

```regex
(ab){3}
```

nothing is stored.

No Group Number is assigned.

---

# Why Do We Need Non-Capturing Groups?

Suppose we want to repeat a pattern.

Example

```regex
(?:ERROR|WARNING|INFO)
```

Our goal is simply to match one of these words.

We do **not** need to retrieve

```
ERROR

or

WARNING

or

INFO
```

later.

Capturing would only create unnecessary Groups.

---

# Definition

A **Non-Capturing Group** groups multiple patterns together **without storing the matched text**.

The Regex Engine still treats the contents as one logical unit,

but no Capturing Group is created.

---

# Syntax

General Syntax

```regex
(?:pattern)
```

Examples

```regex
(?:ab)
```

```regex
(?:\d+)
```

```regex
(?:ERROR|WARNING|INFO)
```

```regex
(?:[A-Z]{3})
```

---

# Capturing vs Non-Capturing

Capturing

```regex
(ab)
```

Regex Engine

```
Group

↓

Capture

↓

Assign Group Number
```

---

Non-Capturing

```regex
(?:ab)
```

Regex Engine

```
Group

↓

No Capture

↓

No Group Number
```

---

# Regex Engine Explanation

Pattern

```regex
(?:ab){3}
```

Input

```text
ababab
```

Regex Engine

```
Read

(

↓

?

↓

:

↓

Non-Capturing Group

↓

Read

ab

↓

End Group

↓

Read

{3}

↓

Repeat Group

↓

SUCCESS
```

Notice that the Regex Engine never stores the matched text.

---

# Engine Visualization

```
              Pattern

            (?:ab){3}

                  │
                  ▼

        +------------------+
        |   Regex Engine   |
        +------------------+

                  │
                  ▼

       Start Non-Capturing Group

                  │
                  ▼

         Read Contents

                  │
                  ▼

      Treat As One Unit

                  │
                  ▼

       Do NOT Store Match

                  │
                  ▼

       Apply Quantifier
```

---

# Engine Trace

Pattern

```regex
(?:ab){3}
```

Input

```text
ababab
```

```
Regex Engine Trace

--------------------------------------

(

↓

?

↓

:

↓

Non-Capturing Group

↓

Read

ab

↓

Read

{3}

↓

Repeat Group

↓

SUCCESS

↓

No Group Stored
```

---

# Capture Table

Pattern

```regex
(?:ab){3}
```

Input

```text
ababab
```

| Overall Match | Group 1 |
|---------------|---------|
| `ababab` | — |

Notice that there is **no Group 1** because the Group is non-capturing.

---

# Compare & Contrast

| Capturing Group | Non-Capturing Group |
|-----------------|---------------------|
| `(ab)` | `(?:ab)` |
| Stores matched text | Does not store matched text |
| Receives Group Number | No Group Number |
| Used for extraction | Used for grouping only |

---

# Real-World Usage

Non-Capturing Groups are useful for:

### Storage Engineering

Grouping optional log formats without storing intermediate values.

---

### Linux Automation

Grouping command alternatives.

---

### Python Automation

Building readable Regular Expressions while reducing unnecessary Capturing Groups.

---

### Test Automation

Organizing complex validation patterns.

---

# Important Observation

A Non-Capturing Group still behaves like a normal Group.

It can:

- Receive Quantifiers.
- Participate in Alternation (`|`).
- Organize complex patterns.

The only difference is

```
No Capturing

↓

No Stored Value

↓

No Group Number
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking a Non-Capturing Group is ignored.

The Regex Engine still processes it normally.

---

### Mistake 2

Thinking Non-Capturing Groups cannot receive Quantifiers.

They can.

---

### Mistake 3

Using Capturing Groups everywhere,

even when no captured value is needed.

---

# Interview Questions

1. What is a Non-Capturing Group?

2. Why were Non-Capturing Groups introduced?

3. What is the syntax of a Non-Capturing Group?

4. How does the Regex Engine process a Non-Capturing Group?

5. When would you choose a Non-Capturing Group instead of a Capturing Group?

---

# Practice Questions

### Question 1

Explain the difference between

```regex
(ab)
```

and

```regex
(?:ab)
```

---

### Question 2

Why does

```regex
(?:ERROR|WARNING|INFO)
```

not create a Capturing Group?

---

### Question 3

List five situations where Non-Capturing Groups are useful.

---

# Memory Tip

```
()

↓

Capture

--------------------

(?:)

↓

Group

Only

↓

No Capture
```

Remember

```
?:

↓

Don't

Remember

The Match
```

---

# Revision Box

✔ `(?:...)` creates a Non-Capturing Group.

✔ The Regex Engine still groups the pattern.

✔ No matched text is stored.

✔ No Group Number is assigned.

✔ Non-Capturing Groups improve readability and avoid unnecessary Capturing Groups.

---

# Key Takeaways

- Non-Capturing Groups organize patterns without storing matched text.
- They behave like normal Groups except they do not participate in capturing.
- They reduce unnecessary Group Numbers and simplify complex Regular Expressions.
- They are especially useful when grouping is required but data extraction is not.

---

# Coming Up

So far, our Capturing Groups have been identified only by numbers.

The next lesson introduces **Named Groups**, allowing Capturing Groups to be identified using meaningful names instead of numeric Group Numbers.

-------------------------------------------------------------------------------------------------------------

# 4.8 Named Groups

## Learning Objective

After completing this lesson, you will be able to:

- Understand what Named Groups are.
- Explain why Named Groups were introduced.
- Distinguish between Numbered Groups and Named Groups.
- Explain how the Regex Engine processes Named Groups.
- Recognize situations where Named Groups improve readability and maintainability.

---

# Previous Knowledge

In the previous lessons, we learned that every Capturing Group receives a Group Number.

Example

```regex
([A-Z]+)(\d+)
```

The Regex Engine stores

```
Group 1

↓

Letters

------------------

Group 2

↓

Digits
```

For small Regular Expressions,

this works well.

However,

large Regular Expressions may contain many Groups.

Remembering

```
Group 7

↓

Capacity

Group 8

↓

Temperature

Group 9

↓

Health
```

quickly becomes difficult.

Named Groups solve this problem.

---

# Introduction

Consider the following storage log.

```text
Drive=NVME001 Capacity=1024GB
```

Instead of writing

```regex
([A-Z]+\d+)\s(\d+GB)
```

we can write

```regex
(?P<drive>[A-Z]+\d+)\s(?P<capacity>\d+GB)
```

Now,

instead of remembering

```
Group 1

↓

Drive

Group 2

↓

Capacity
```

the Regex Engine stores

```
drive

↓

NVME001

-------------------

capacity

↓

1024GB
```

The Regular Expression becomes much easier to understand.

---

# Why Do We Need Named Groups?

Suppose a large Regular Expression contains

10

or

20

Capturing Groups.

Referring to

```
Group 12
```

provides very little information.

Compare these two approaches.

Numbered Groups

```
Group 1

Group 2

Group 3
```

Named Groups

```
drive

capacity

health
```

The second approach is far more readable.

---

# Definition

A **Named Group** is a Capturing Group that is assigned a meaningful name.

The Regex Engine stores both:

- the Group Number
- the Group Name

Both identify the same captured value.

---

# Syntax (Python)

Python's `re` module uses the following syntax:

```regex
(?P<name>pattern)
```

Examples

```regex
(?P<drive>[A-Z]+\d+)
```

```regex
(?P<capacity>\d+GB)
```

```regex
(?P<temperature>\d+C)
```

> **Note**
>
> The syntax shown here is **Python-specific**, since this roadmap focuses on Python Regular Expressions.
>
> Other programming languages may use different syntax for Named Groups.

---

# Numbered vs Named

Numbered

```regex
([A-Z]+\d+)
```

Named

```regex
(?P<drive>[A-Z]+\d+)
```

Both create Capturing Groups.

The only difference is

```
Named Groups

↓

Meaningful Identifier
```

---

# Regex Engine Explanation

Pattern

```regex
(?P<drive>[A-Z]+\d+)
```

Input

```text
NVME001
```

Regex Engine

```
Read

(

↓

?

↓

P

↓

Read Name

drive

↓

Assign

Group 1

↓

Associate Name

drive

↓

Match

NVME001

↓

Store

Group Number

1

↓

Store

Group Name

drive

↓

SUCCESS
```

The Regex Engine stores both the numeric identifier and the descriptive name.

---

# Engine Visualization

```
                Pattern

     (?P<drive>[A-Z]+\d+)

                     │
                     ▼

          +------------------+
          |   Regex Engine   |
          +------------------+

                     │
                     ▼

            Read Group Name

                     │
                     ▼

          Assign Group Number

                     │
                     ▼

            Store Match

                     │
                     ▼

       Number + Name Available
```

---

# Engine Trace

Pattern

```regex
(?P<drive>[A-Z]+\d+)
```

Input

```text
NVME001
```

```
Regex Engine Trace

--------------------------------------

(

↓

?

↓

P

↓

Read Name

drive

↓

Assign

Group 1

↓

Match

NVME001

↓

Store

Group Name

drive

↓

SUCCESS
```

---

# Capture Table

| Overall Match | Group 1 | Group Name |
|---------------|---------|------------|
| `NVME001` | `NVME001` | `drive` |

---

# Another Example

Pattern

```regex
Drive=(?P<drive>[A-Z]+\d+)\sCapacity=(?P<capacity>\d+GB)
```

Input

```text
Drive=NVME001 Capacity=1024GB
```

Capture Table

| Overall Match | Group 1 | Group 2 | Name |
|---------------|---------|---------|------|
| `Drive=NVME001 Capacity=1024GB` | `NVME001` | `1024GB` | `drive`, `capacity` |

---

# Compare & Contrast

| Numbered Groups | Named Groups |
|-----------------|--------------|
| Group 1 | drive |
| Group 2 | capacity |
| Harder to remember | Self-explanatory |
| Good for simple Regex | Better for large Regex |

---

# Real-World Usage

Named Groups are especially useful for:

### Storage Engineering

- Drive ID
- Capacity
- Temperature
- Firmware Version
- Health Status

---

### Linux Automation

- Hostname
- IP Address
- Port Number
- Filesystem

---

### Python Automation

Large parsing scripts become much easier to understand when descriptive names replace numeric group references.

---

### Test Automation

Named Groups improve the readability of validation patterns and reporting scripts.

---

# Python Preview

In **Chapter 6**, we will retrieve Named Groups using

```python
match.group("drive")

match.group("capacity")
```

or

```python
match.groupdict()
```

which returns all Named Groups as a dictionary.

---

# Important Observation

Named Groups are still **Capturing Groups**.

They receive

- a Group Number
- a Group Name

Both refer to the same captured text.

---

# Common Beginner Mistakes

### Mistake 1

Thinking Named Groups replace Group Numbers.

They do not.

The Regex Engine still assigns numeric Group Numbers.

---

### Mistake 2

Thinking Named Groups are Python variables.

They are identifiers used by the Regex Engine.

---

### Mistake 3

Using unclear names such as

```
group1

temp1

abc
```

Choose descriptive names such as

```
drive

capacity

temperature
```

---

# Interview Questions

1. What is a Named Group?

2. Why are Named Groups useful?

3. What is the syntax of a Named Group in Python?

4. Does a Named Group also receive a Group Number?

5. When would you choose Named Groups over Numbered Groups?

---

# Practice Questions

### Question 1

Convert

```regex
([A-Z]+\d+)
```

into a Named Group.

---

### Question 2

Create Named Groups for

- Drive ID
- Capacity
- Temperature

---

### Question 3

Why are Named Groups preferred in large automation projects?

---

# Memory Tip

```
()

↓

Capturing Group

----------------------

(?P<name>)

↓

Named

Capturing Group
```

Remember

```
Named Group

=

Capture

+

Meaningful Name
```

---

# Revision Box

✔ Named Groups are Capturing Groups with descriptive names.

✔ Python uses the syntax `(?P<name>pattern)`.

✔ Named Groups receive both a Group Number and a Group Name.

✔ Named Groups improve readability and maintainability.

✔ They are widely used in large automation projects.

---

# Key Takeaways

- Named Groups provide meaningful identifiers for captured values.
- They improve readability without changing the matching behavior.
- The Regex Engine stores both the numeric Group Number and the descriptive Group Name.
- Named Groups are especially valuable in large Regular Expressions and automation scripts.

---

# Coming Up

So far, we have learned how to capture text.

The next lesson introduces **Backreferences**, where a Regular Expression can refer to text that was captured earlier, allowing patterns to enforce repetition and consistency within the same match.

-------------------------------------------------------------------------------------------------------------

# 4.9 Backreferences

## Learning Objective

After completing this lesson, you will be able to:

- Understand what a Backreference is.
- Explain how the Regex Engine uses previously captured text.
- Distinguish between matching a pattern and matching previously captured text.
- Understand the role of Backreferences in validation.
- Recognize practical applications of Backreferences.

---

# Previous Knowledge

In the previous lessons, we learned that Capturing Groups store matched text.

Example

```regex
([A-Z]+)
```

Input

```text
NVME
```

Captured

```text
NVME
```

The Regex Engine remembers this captured value.

An important question now arises.

> Can the Regex Engine use this stored value later in the same Regular Expression?

The answer is **Yes**.

This feature is called a **Backreference**.

---

# Introduction

Consider the following input.

```text
ERROR ERROR
```

Suppose we want to verify that

both words are identical.

Instead of writing

```regex
(ERROR)\sERROR
```

we can write

```regex
(ERROR)\s\1
```

Here,

```regex
\1
```

means

```
Match exactly

what

Group 1

captured.
```

The Regex Engine is no longer matching a new pattern.

It is matching **previously captured text**.

---

# Why Do We Need Backreferences?

Suppose we have

```text
Device Device
```

Valid

```text
Drive Drive
```

Valid

```text
Storage Storage
```

Valid

```text
Drive Storage
```

Invalid

The second word must be **identical** to the first.

Backreferences make this validation possible.

---

# Definition

A **Backreference** is a reference to text previously captured by a Capturing Group.

Instead of describing a new pattern,

a Backreference instructs the Regex Engine to match the **same text that was captured earlier**.

---

# Syntax

### Numbered Backreference

```regex
\1
```

```regex
\2
```

```regex
\3
```

where

```
\1

↓

Group 1

\2

↓

Group 2

\3

↓

Group 3
```

---

### Named Backreference (Python)

```regex
(?P=name)
```

Example

```regex
(?P<drive>[A-Z]+\d+)\s(?P=drive)
```

> **Note**
>
> Python uses `(?P=name)` to reference a Named Group.
>
> Since this roadmap focuses on Python, all Named Backreference examples follow Python's syntax.

---

# Example 1 — Numbered Backreference

Pattern

```regex
(ERROR)\s\1
```

Input

```text
ERROR ERROR
```

Regex Engine

```
Group 1

↓

ERROR

↓

\1

↓

Match

ERROR

↓

SUCCESS
```

---

Input

```text
ERROR WARNING
```

Regex Engine

```
Group 1

↓

ERROR

↓

\1

↓

Expected

ERROR

↓

Found

WARNING

↓

FAIL
```

---

# Example 2 — Named Backreference

Pattern

```regex
(?P<word>[A-Z]+)\s(?P=word)
```

Input

```text
STORAGE STORAGE
```

Result

```
SUCCESS
```

---

# Regex Engine Explanation

Pattern

```regex
(ERROR)\s\1
```

Input

```text
ERROR ERROR
```

Regex Engine

```
Read

(

↓

Assign

Group 1

↓

Match

ERROR

↓

Store

ERROR

↓

Read

\1

↓

Retrieve

Group 1

↓

Compare

Stored Value

↓

ERROR

↓

SUCCESS
```

Notice that

```
\1
```

does **not** describe a new pattern.

It retrieves previously captured text.

---

# Engine Visualization

```
               Pattern

          (ERROR)\s\1

                  │
                  ▼

        +------------------+
        |   Regex Engine   |
        +------------------+

                  │
                  ▼

        Capture Group 1

                  │
                  ▼

         Store "ERROR"

                  │
                  ▼

          Encounter \1

                  │
                  ▼

 Retrieve Stored Group 1

                  │
                  ▼

 Compare With Input

                  │
          ┌───────┴────────┐
          │                │
          ▼                ▼

      Match             No Match
```

---

# Engine Trace

Pattern

```regex
(ERROR)\s\1
```

Input

```text
ERROR ERROR
```

```
Regex Engine Trace

--------------------------------------

(

↓

Assign Group 1

↓

Match

ERROR

↓

Store Group 1

↓

Read

\1

↓

Retrieve Group 1

↓

Compare

ERROR

↓

SUCCESS
```

---

# Capture Table

Pattern

```regex
(ERROR)\s\1
```

| Overall Match | Group 1 | Backreference |
|---------------|---------|---------------|
| `ERROR ERROR` | `ERROR` | `ERROR` |

Notice that

```
\1
```

does not create a new Group.

It simply reuses Group 1.

---

# Compare & Contrast

| Capturing Group | Backreference |
|-----------------|---------------|
| Stores matched text | Reuses stored text |
| Creates Group Number | Refers to existing Group |
| Captures new value | Matches previous value |

---

# Real-World Usage

Backreferences are useful for:

### Storage Engineering

- Verifying repeated identifiers
- Detecting duplicate values

---

### Linux Automation

- Validating repeated configuration values
- Checking duplicated fields

---

### Python Automation

- Detecting duplicate words
- Validating repeated input
- Parsing structured text

---

### Test Automation

- Verifying expected and repeated values
- Detecting inconsistent outputs

---

# Important Observation

A Backreference

**does not create another Capturing Group**.

Instead,

it retrieves the value already stored by an earlier Group.

Think of it as

```
Capture

↓

Store

↓

Reuse
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking

```regex
\1
```

matches the pattern again.

It matches the **captured text**, not the original pattern.

---

### Mistake 2

Using a Backreference before the corresponding Capturing Group exists.

The Group must be captured first.

---

### Mistake 3

Thinking a Backreference creates another Group.

It does not.

It only refers to an existing Group.

---

# Interview Questions

1. What is a Backreference?

2. How does a Backreference differ from a Capturing Group?

3. What is the syntax of a numbered Backreference?

4. What is the syntax of a Named Backreference in Python?

5. Where are Backreferences useful?

---

# Practice Questions

### Question 1

Explain why

```regex
(ERROR)\s\1
```

matches

```text
ERROR ERROR
```

but not

```text
ERROR WARNING
```

---

### Question 2

Write a Named Group and Named Backreference for repeated device names.

---

### Question 3

List five practical applications of Backreferences.

---

# Memory Tip

```
Capture

↓

Store

↓

Reuse
```

Remember

```
\1

↓

Group 1

Again

---------------------

(?P=name)

↓

Named Group

Again
```

---

# Revision Box

✔ A Backreference matches previously captured text.

✔ `\1`, `\2`, `\3` refer to numbered Groups.

✔ Python uses `(?P=name)` for Named Backreferences.

✔ Backreferences reuse captured values rather than creating new Groups.

✔ They are useful for validating repeated or identical text.

---

# Key Takeaways

- A Backreference refers to text previously captured by a Group.
- The Regex Engine retrieves stored values instead of matching a new pattern.
- Numbered and Named Backreferences improve validation capabilities.
- Backreferences are widely used for duplicate detection, consistency checks and structured text validation.
- Understanding Backreferences completes the foundation of Group-based Regular Expressions.

---

# Coming Up

You have now learned all major Group types:

- Capturing Groups
- Multiple Capturing Groups
- Nested Groups
- Non-Capturing Groups
- Named Groups
- Backreferences

The next lesson demonstrates **Real-World Applications of Groups**, showing how these concepts are used together in Storage Engineering, Linux Automation, Python Automation and enterprise log parsing.

-------------------------------------------------------------------------------------------------------------

# 4.10 Real-World Applications of Groups

## Learning Objective

After completing this lesson, you will be able to:

- Understand where Groups are used in real-world software development.
- Apply Capturing Groups to data extraction.
- Recognize when to use Non-Capturing Groups.
- Understand the role of Named Groups in automation.
- Apply Backreferences for validation.

---

# Introduction

Groups are one of the most frequently used features of Regular Expressions.

Almost every automation project needs to:

- Extract values
- Organize patterns
- Validate repeated data
- Parse structured text

Groups make these tasks significantly easier.

---

# Application 1 — Storage Log Parsing

Storage Log

```text
Drive ID : NVME001

Capacity : 1024GB

Health : GOOD
```

Regex

```regex
Drive ID\s:\s([A-Z]+\d+)

Capacity\s:\s(\d+GB)

Health\s:\s([A-Z]+)
```

Capture Table

| Overall Match | Group 1 | Group 2 | Group 3 |
|---------------|---------|---------|---------|
| Storage Log | `NVME001` | `1024GB` | `GOOD` |

Applications

- Device Validation
- Report Generation
- Capacity Verification

---

# Application 2 — Firmware Version Extraction

Input

```text
Firmware Version : 3.5.12
```

Regex

```regex
Firmware Version\s:\s((\d+)\.(\d+)\.(\d+))
```

Capture Table

| Overall Match | Group 1 | Group 2 | Group 3 | Group 4 |
|---------------|---------|---------|---------|---------|
| `3.5.12` | `3.5.12` | `3` | `5` | `12` |

Nested Groups allow us to capture

- Complete Version
- Major Version
- Minor Version
- Patch Version

---

# Application 3 — Linux Command Output

Command

```bash
df -h
```

Output

```text
/dev/nvme0n1 500G 220G 280G
```

Regex

```regex
(\S+)\s(\d+G)\s(\d+G)\s(\d+G)
```

Capture Table

| Group 1 | Group 2 | Group 3 | Group 4 |
|---------|---------|---------|---------|
| Filesystem | Size | Used | Available |

Applications

- Disk Monitoring
- Capacity Reports
- Health Checks

---

# Application 4 — IP Address Extraction

Command

```bash
ip addr
```

Output

```text
inet 192.168.1.25/24
```

Regex

```regex
((\d+)\.(\d+)\.(\d+)\.(\d+))
```

Capture Table

| Group | Value |
|--------|-------|
| Group 1 | Entire IP |
| Group 2 | 192 |
| Group 3 | 168 |
| Group 4 | 1 |
| Group 5 | 25 |

Applications

- Network Validation
- Configuration Parsing
- Monitoring

---

# Application 5 — Configuration Files

Input

```text
HOST=10.10.20.15

PORT=8080
```

Regex

```regex
([A-Z]+)=(.+)
```

Capture Table

| Group 1 | Group 2 |
|---------|---------|
| HOST | 10.10.20.15 |

Applications

- Configuration Parsing
- Deployment Automation
- Environment Validation

---

# Application 6 — Named Groups

Regex

```regex
Drive=(?P<drive>[A-Z]+\d+)

Capacity=(?P<capacity>\d+GB)
```

Captured Values

```
drive

↓

NVME001

---------------------

capacity

↓

1024GB
```

Advantages

- Better readability
- Easier maintenance
- Self-documenting patterns

---

# Application 7 — Non-Capturing Groups

Regex

```regex
(?:ERROR|WARNING|INFO)
```

Applications

- Log Filtering
- Keyword Matching
- Validation Rules

Grouping is required,

but storing the matched value is unnecessary.

---

# Application 8 — Backreferences

Regex

```regex
([A-Z]+)\s\1
```

Valid

```text
ERROR ERROR
```

Invalid

```text
ERROR WARNING
```

Applications

- Duplicate Detection
- Repeated Value Validation
- Configuration Consistency

---

# Application 9 — Python Automation

Groups are commonly used with Python's `re` module.

Examples

```python
match.group(1)

match.group(2)

match.groups()

match.groupdict()
```

These methods allow automation scripts to retrieve captured values efficiently.

We will study them in detail in **Chapter 6 — Python `re` Module**.

---

# Application 10 — Test Automation

Typical Output

```text
Execution Time : 12.45 sec

Status : PASS
```

Regex

```regex
Execution Time\s:\s(\d+\.\d+)

Status\s:\s([A-Z]+)
```

Capture Table

| Group 1 | Group 2 |
|---------|---------|
| 12.45 | PASS |

Applications

- Report Validation
- Performance Testing
- Test Result Analysis

---

# Summary of Applications

| Domain | Typical Use of Groups |
|---------|-----------------------|
| Storage Engineering | Drive IDs, Firmware, Capacity |
| Linux Automation | Filesystems, IPs, Processes |
| Python Automation | Parsing, Extraction, Validation |
| Test Automation | Reports, Logs, Results |
| Networking | IP Addresses, Ports |
| Configuration | Keys and Values |

---

# Important Observation

Groups are not limited to matching.

They enable

```
Match

↓

Capture

↓

Organize

↓

Extract

↓

Validate

↓

Reuse
```

This is why Groups are one of the most important Regex features.

---

# Common Beginner Mistakes

### Mistake 1

Using Groups only for repetition.

Groups are primarily used for data extraction.

---

### Mistake 2

Creating Capturing Groups for every pair of parentheses.

Use Non-Capturing Groups when the captured value is not needed.

---

### Mistake 3

Using numbered Groups in very large Regular Expressions.

Named Groups often improve readability.

---

# Interview Questions

1. Where are Groups used in Storage Engineering?

2. Why are Named Groups preferred in large projects?

3. When should Non-Capturing Groups be used?

4. What are Backreferences used for?

5. How are Groups used in Python automation?

---

# Practice Questions

### Question 1

List five real-world applications of Capturing Groups.

---

### Question 2

Explain why Named Groups improve maintainability.

---

### Question 3

Create a Capture Table for

```text
Drive=NVME001 Capacity=2048GB Health=GOOD
```

---

# Memory Tip

```
Groups

↓

Organize

↓

Capture

↓

Extract

↓

Validate

↓

Reuse
```

Remember

```
Real Automation

=

Groups

+

Extraction
```

---

# Revision Box

✔ Groups are used extensively in automation.

✔ Capturing Groups extract structured data.

✔ Named Groups improve readability.

✔ Non-Capturing Groups simplify complex patterns.

✔ Backreferences validate repeated values.

✔ Python's `re` module relies heavily on Groups.

---

# Key Takeaways

- Groups are fundamental to enterprise Regular Expressions.
- They simplify extraction, organization, validation and reuse of matched text.
- Storage Engineering, Linux Automation and Python Automation all rely heavily on Groups.
- Understanding Groups is essential before working with Python's `re` module.
- Groups form the bridge between pattern matching and practical automation.

---

# Coming Up

The next lesson concludes **Chapter 4** with a comprehensive revision guide containing:

- Complete Group comparison tables
- Numbering rules
- Capture tables
- Decision trees
- Common mistakes
- Interview questions
- Chapter mind map
- One-page revision sheet

This summary will serve as your primary revision material before moving to **Chapter 5 — Lookarounds**.

-------------------------------------------------------------------------------------------------------------

# 4.11 Chapter Summary

## Chapter Overview

In this chapter, we learned how Groups allow the Regex Engine to treat multiple patterns as a single logical unit.

Unlike Character Classes and Quantifiers, Groups introduce an additional capability:

```
Matching

↓

Capturing

↓

Reusing
```

Groups are one of the most powerful features of Regular Expressions because they make extraction, validation and organization possible.

---

# Group Comparison Table

| Feature | Syntax | Captures? | Group Number? | Typical Use |
|---------|--------|-----------|---------------|-------------|
| Capturing Group | `(pattern)` | ✅ | ✅ | Data Extraction |
| Non-Capturing Group | `(?:pattern)` | ❌ | ❌ | Grouping Only |
| Named Group (Python) | `(?P<name>pattern)` | ✅ | ✅ | Readable Extraction |
| Backreference | `\1` | ❌ | Uses Existing | Repeat Captured Text |
| Named Backreference (Python) | `(?P=name)` | ❌ | Uses Existing | Repeat Named Group |

---

# Group Decision Tree

```
Need Parentheses?

        │
        ▼

Need Captured Value?

        │
   ┌────┴────┐
   │         │
 YES        NO
   │         │
   ▼         ▼

Need Readable Name?

   │
┌──┴──┐
│     │
NO   YES
│      │
▼      ▼

()   (?P<name>)

---------------------

Grouping Only?

↓

(?:)

---------------------

Need Same Text Again?

↓

\1

or

(?P=name)
```

---

# Group Numbering Rules

```
Encounter

(

↓

Assign Next Group Number

↓

Continue Matching
```

Remember

```
Opening Parenthesis

↓

Assign Number

NOT

Closing Parenthesis
```

---

# Group Numbering Example

Pattern

```regex
((Drive)(\d+))
```

Capture Table

| Overall Match | Group 1 | Group 2 | Group 3 |
|---------------|---------|---------|---------|
| `Drive123` | `Drive123` | `Drive` | `123` |

Numbering

```
First (

↓

Group 1

Second (

↓

Group 2

Third (

↓

Group 3
```

---

# Capture Flow

```
Regex Pattern

↓

Regex Engine

↓

Start Group

↓

Match Pattern

↓

Capture Text

↓

Assign Group Number

↓

Store Value

↓

Continue Matching
```

---

# Group Hierarchy

```
Overall Match

        │

        ▼

Outer Group

        │

 ┌──────┴──────┐

 ▼             ▼

Inner      Inner

Group      Group
```

---

# Capturing vs Non-Capturing

| Capturing | Non-Capturing |
|-----------|---------------|
| Stores Match | No Storage |
| Receives Number | No Number |
| Used for Extraction | Used for Organization |
| `( )` | `(?: )` |

---

# Numbered vs Named Groups

| Numbered | Named |
|----------|-------|
| Group 1 | drive |
| Group 2 | capacity |
| Group 3 | health |
| Harder to Read | Self-Documenting |

---

# Backreference Flow

```
Capture

↓

Store

↓

Encounter

\1

↓

Retrieve Stored Value

↓

Compare

↓

Match / Fail
```

---

# Complete Memory Sheet

```
()

↓

Capturing

--------------------

(?:)

↓

Grouping Only

--------------------

(?P<name>)

↓

Named Group

--------------------

\1

↓

Reuse Group 1

--------------------

(?P=name)

↓

Reuse Named Group
```

---

# Regex Engine Summary

```
Regex Pattern

        │

        ▼

+----------------------+
|    Regex Engine      |
+----------------------+

        │

        ▼

Read Pattern

        │

        ▼

Start Group?

        │
   ┌────┴─────┐
   │          │
 YES         NO

   │

   ▼

Capturing?

   │
┌──┴─────┐
│        │
YES      NO
│         │
▼         ▼

Store   Continue

        │

        ▼

Need Backreference?

        │
   ┌────┴─────┐
   │          │
 YES         NO
```

---

# Real-World Applications

### Storage Engineering

- Drive IDs
- Capacity
- Firmware Version
- SMART Logs
- Health Status

---

### Linux Automation

- Filesystems
- Device Names
- IP Addresses
- Configuration Parsing

---

### Python Automation

- Log Parsing
- CSV Processing
- JSON Validation
- Configuration Files

---

### Test Automation

- Result Validation
- Report Parsing
- Execution Time
- Error Messages

---

# Common Beginner Mistakes

❌ Thinking every Group is only for Capturing.

❌ Forgetting that Group Numbers start from **1**.

❌ Assuming Group Numbers depend on the closing parenthesis.

❌ Using Capturing Groups when `(?: )` is sufficient.

❌ Confusing the Overall Match with individual Groups.

❌ Thinking a Backreference creates a new Group.

---

# Common Interview Questions

1. What is a Group?

2. Why are Groups required?

3. Difference between Capturing and Non-Capturing Groups.

4. How are Group Numbers assigned?

5. What are Named Groups?

6. What is a Backreference?

7. Difference between `()` and `(?:)`.

8. Difference between Numbered and Named Groups.

9. How does the Regex Engine process Groups?

10. Give practical applications of Groups.

---

# One-Page Revision

```
Groups

↓

Organize

↓

Capture

↓

Store

↓

Retrieve

↓

Reuse

↓

Validate
```

---

# Chapter Mind Map

```
Groups

│

├── Basic
│      ├── Why Groups
│      ├── What is a Group
│      └── Capturing Groups
│
├── Numbering
│      ├── Group Numbers
│      ├── Multiple Groups
│      └── Nested Groups
│
├── Advanced
│      ├── Non-Capturing
│      ├── Named Groups
│      └── Backreferences
│
└── Applications
       ├── Storage
       ├── Linux
       ├── Python
       ├── Testing
       └── Automation
```

---

# Final Assessment

## Theory

1. Explain Capturing Groups.

2. Explain Group Numbering.

3. Explain Nested Groups.

4. Explain Non-Capturing Groups.

5. Explain Named Groups.

6. Explain Backreferences.

---

## Practical

Write Regular Expressions for:

- Drive ID
- Firmware Version
- IPv4 Address
- Filesystem Information
- Capacity
- Temperature
- Username
- Duplicate Words
- Configuration Key-Value Pair
- Version Number

---

# Chapter Completion Checklist

- [ ] I understand why Groups are needed.
- [ ] I understand Capturing Groups.
- [ ] I understand Group Numbering.
- [ ] I can predict Group Numbers.
- [ ] I understand Nested Groups.
- [ ] I understand Non-Capturing Groups.
- [ ] I understand Named Groups.
- [ ] I understand Backreferences.
- [ ] I can apply Groups in Storage Automation.
- [ ] I can explain Groups in interviews.

---

# Chapter Completion

Congratulations!

You have completed **Chapter 4 — Groups and Capturing**.

You now understand:

- Group Fundamentals
- Capturing Groups
- Group Numbering
- Multiple Groups
- Nested Groups
- Non-Capturing Groups
- Named Groups
- Backreferences

These concepts form the foundation for advanced Regular Expression techniques used in enterprise automation.

The next chapter introduces **Lookarounds**, where the Regex Engine can inspect surrounding text **without consuming it**, enabling highly precise pattern matching and validation.

-------------------------------------------------------------------------------------------------------------


