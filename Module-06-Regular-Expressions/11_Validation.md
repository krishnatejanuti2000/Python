# Module 06 – Validation using Regular Expressions

> **Purpose of this Document**
>
> This document is **not** a collection of regex patterns.
>
> It is an **Engineering Notebook** that records the complete thought process behind designing validators.
>
> Every validation problem will answer the following questions:
>
> - What was the problem?
> - What requirements were given?
> - How did we think about the problem?
> - What mistakes did we make?
> - Why did those mistakes happen?
> - How was the final solution designed?
> - What engineering lessons were learned?
>
> **Goal:** Never memorize regex. Learn how to design regex from requirements.

---

# Validation Engineering Methodology

Every validation problem in this notebook will follow the same engineering process.

```
Problem Statement
        ↓
Requirement Analysis
        ↓
Convert Requirements into Rules
        ↓
Separate Rules

    ├── Matching Rules
    └── Restriction Rules

        ↓
Build Regex Incrementally
        ↓
Test Every Rule
        ↓
Combine Everything
        ↓
Boundary Testing
        ↓
Final Validation
        ↓
Lessons Learned
```

**Golden Rule**

> Never write a huge regex immediately.

Instead,

Build → Test → Improve → Repeat

This methodology will be used for every validation problem in this document.

---

# Question 1 – Email Validation

---

## Problem Statement

Validate an Email Address using Python Regular Expressions.

---

## Business Requirements

Only the following email providers are allowed.

```
gmail
yahoo
```

Only the following Top-Level Domains (TLD) are allowed.

```
.com
.in
.org
```

Any email violating these requirements must be rejected.

---

# Step 1 – Requirement Analysis

The biggest mistake beginners make is writing regex immediately.

Instead,

**First understand the problem.**

Break the email into logical components.

```
rahul@gmail.com

│        │        │
│        │        └── Top Level Domain (TLD)
│        │
│        └────────── Provider
│
└─────────────────── Local Part
```

Instead of solving the whole email,

solve one component at a time.

---

# Step 2 – Analyse the Local Part

The Local Part is everything before the '@'.

Example

```
rahul
rahul123
rahul.xyz
abc_def
```

Ignore everything after '@'.

We only want to solve this section first.

---

## Allowed Characters

The local part may contain

- Letters
- Digits
- Dot (`.`)
- Underscore (`_`)
- Hyphen (`-`)
- Plus (`+`)

---

## Rules

The Local Part must satisfy the following conditions.

### Rule 1

Must start with

- Letter
- Digit

Examples

✅ Valid

```
rahul
abc123
```

❌ Invalid

```
.rahul
+rahul
-rahul
```

---

### Rule 2

Middle characters may contain

- Letters
- Digits
- Dot
- Underscore
- Hyphen
- Plus

Examples

```
rahul.xyz
abc_def
abc-def
abc+office
```

---

### Rule 3

Must end with

- Letter
- Digit

Examples

✅ Valid

```
rahul
rahul123
abc.xyz
```

❌ Invalid

```
rahul.
abc+
abc-
abc_
```

---

### Rule 4

Must NOT contain consecutive dots.

Reject

```
..
```

Examples

❌ Invalid

```
abc..xyz
```

---

### Rule 5

Must NOT contain consecutive plus signs.

Reject

```
++
```

Examples

❌ Invalid

```
abc++office
```

---

# Step 3 – Separate the Rules

Every validation problem contains two kinds of rules.

Understanding this distinction makes regex design much easier.

---

## A. Matching Rules

Matching Rules describe

> **What is allowed**

Examples

- Letters
- Digits
- Allowed symbols
- '@'
- Provider
- TLD

Regex Features Used

- Character Classes
- Quantifiers
- Groups
- Alternation

---

## B. Restriction Rules

Restriction Rules describe

> **What is NOT allowed**

Examples

```
No ..

No ++

No Spaces

No @@
```

Regex Features Used

- Negative Lookahead

---

## Engineering Insight

Whenever a requirement says

```
Must NOT
```

your brain should immediately think

```
Negative Lookahead
```

This simple observation will help you design most real-world validators.

---

# Step 4 – Designing the Local Part

Now that all requirements are known,

we can finally begin writing the regex.

**Important**

We will NOT write the final regex immediately.

We will build it one rule at a time.

This makes debugging much easier and helps us understand *why* each part exists.

# Step 4 – Designing the Local Part

Now that the requirements are clear, we can start building the regex.

**Important Principle**

Never try to write the final regex in one attempt.

Instead,

```
Write a small regex
        ↓
Test it
        ↓
Find the problem
        ↓
Improve it
        ↓
Repeat
```

This is exactly how we solved the problem.

------------------------------------------------------------------------------

# Attempt 1

## Thought Process

The first character must always be a letter or digit.

Therefore,

the first thing we match is

```regex
^[A-Za-z0-9]
```

### Why?

We do not want emails like

```
.gmail
+yahoo
-office
```

The local part should always begin with an alphanumeric character.

Result

✅ Correct

This became the foundation of our regex.

------------------------------------------------------------------------------

# Attempt 2

## Thought Process

After the first character,

the remaining characters may contain

- Letters
- Digits
- Dot
- Underscore
- Hyphen
- Plus

Regex

```regex
^[A-Za-z0-9][A-Za-z0-9.+_-]*
```

At first glance,

this looked correct.

But testing revealed a problem.

------------------------------------------------------------------------------

## Problem Found

Input

```
abc.
```

Expected

```
Reject
```

Actual

```
Accepted
```

Question

Why?

Because our regex never checks the last character.

The regex only says

```
After the first character,

keep accepting these characters.
```

A dot is one of the allowed characters.

Therefore

```
abc.
```

matches successfully.

We needed another rule.

------------------------------------------------------------------------------

# Attempt 3

## Thought Process

Since the last character must also be alphanumeric,

let us simply add one more character class.

Regex

```regex
^[A-Za-z0-9][A-Za-z0-9.+_-]*[A-Za-z0-9]?$
```

Expected

```
abc.
```

should fail.

Actual Result

```
abc.
```

still matched.

This confused us because

the last character clearly says

```
[A-Za-z0-9]
```

------------------------------------------------------------------------------

# Why Did It Fail?

This became the biggest lesson of the entire exercise.

Look carefully.

```regex
[A-Za-z0-9.+_-]*
```

uses

```
*
```

which is greedy.

Greedy means

```
Match as many characters as possible.
```

Therefore

for

```
abc.
```

the middle portion becomes

```
abc.
```

The regex engine happily consumes the final dot.

Now

```regex
[A-Za-z0-9]?
```

has nothing left to match.

Since

```
?
```

means

```
Zero OR One
```

matching nothing is perfectly valid.

Therefore

the regex succeeds.

------------------------------------------------------------------------------

# Root Cause Analysis

The problem was NOT

- Character Classes
- Quantifiers
- Anchors

The real problem was

```
Regex Design
```

We designed the pattern incorrectly.

------------------------------------------------------------------------------

# Design Improvement

Old Design

```
First Character
        ↓
Middle Characters
        ↓
Optional Last Character
```

This design allows the greedy middle portion to consume the final character.

Instead,

change the design itself.

New Design

```
First Character
        ↓
(Optional Middle + Last Character)
```

Instead of making

```
Last Character
```

optional,

make the

```
Entire Remaining Portion
```

optional.

------------------------------------------------------------------------------

# Final Local Part Regex

```regex
[A-Za-z0-9]([A-Za-z0-9.+_-]*[A-Za-z0-9])?
```

Why does this work?

If the Local Part contains only one character

```
a
```

the optional group disappears.

Result

```
a
```

matches successfully.

If additional characters exist,

the optional group becomes active.

The final character inside the group **must** be alphanumeric.

Therefore

Accepted

```
a

abc

abc.xyz

abc_123

abc-def

abc+office
```

Rejected

```
abc.

abc_

abc-

abc+
```

------------------------------------------------------------------------------

# Engineering Lesson

The solution was NOT

"Add another quantifier."

The solution was

"Redesign the regex."

This is an important engineering principle.

Whenever regex behaves unexpectedly,

do not immediately change syntax.

Instead ask

```
Is my regex design correct?
```

Most difficult regex problems are solved by redesigning the pattern,

not by adding more symbols.

------------------------------------------------------------------------------

# Step 5 – Designing Restriction Rules

Until now,

we designed rules describing

> **What is allowed**

Now,

we move to rules describing

> **What is NOT allowed**

Examples

```
No ..

No ++

No Spaces

No @@
```

These are called

```
Restriction Rules
```

Unlike Matching Rules,

Restriction Rules are usually implemented using

```
Negative Lookahead
```

------------------------------------------------------------------------------

# Rule 4 – Reject Consecutive Dots

Requirement

```
The Local Part must NOT contain

..
```

------------------------------------------------------------------------------

## First Thought

Initially we thought

```regex
(?!\.\.)
```

should solve the problem.

Question

What does this actually check?

Answer

It checks only the current position.

Suppose the input is

```
abc..xyz
```

The regex engine starts here

```
abc..xyz
^
```

Question

Are the next two characters

```
..
```

Answer

No.

Therefore

the lookahead succeeds.

But

```
..
```

still exists later in the string.

So this solution is incorrect.

------------------------------------------------------------------------------

# Understanding the Requirement

Our requirement was never

```
The next two characters must not be '..'
```

Our actual requirement was

```
Reject the string if '..' exists ANYWHERE.
```

That completely changes the regex.

------------------------------------------------------------------------------

# Final Solution

Regex

```regex
(?!.*\.\.)
```

Break it into pieces.

```
(?!      Negative Lookahead

.*       Search through the remaining string

\.\.     Find two consecutive dots
```

Meaning

```
Reject if ".." exists anywhere in the string.
```

------------------------------------------------------------------------------

# Why is .* Required?

This was one of the biggest learning moments.

Many beginners think

```
.*
```

simply consumes everything.

That is NOT the complete story.

The regex engine first allows

```
.*
```

to match as much as possible.

If the remaining pattern cannot match,

it starts

```
Backtracking
```

until

```
\.\.
```

can be found.

Therefore

```
.*
```

acts like

```
Search the remaining string.
```

This is why

```regex
(?!.*\.\.)
```

means

```
Reject if ".." exists anywhere.
```

------------------------------------------------------------------------------

# Rule 5 – Reject Consecutive Plus Signs

Requirement

```
Must NOT contain

++
```

Same engineering thinking.

Regex

```regex
(?!.*\+\+)
```

Meaning

```
Reject if "++" exists anywhere.
```

------------------------------------------------------------------------------

# Engineering Observation

Whenever requirements say

```
Must NOT contain
```

Immediately think

```
Negative Lookahead
```

Examples

```
No ..

No ++

No @@

No Spaces

No Tabs

No Multiple Hyphens
```

------------------------------------------------------------------------------

# Step 6 – Provider Validation

Now that the Local Part is complete,

we moved to

```
@
```

Initially,

we discussed two different approaches.

------------------------------------------------------------------------------

## Approach 1

Generic Email Validation

Accept

```
abc@company.com

abc@microsoft.com

abc@google.org
```

This validates only

```
Email Format
```

It does NOT verify whether the domain actually exists.

------------------------------------------------------------------------------

## Approach 2

Business Validation

Our requirement was

```
Allow only

gmail

yahoo
```

Therefore,

instead of building a generic domain validator,

we simply used

```regex
(gmail|yahoo)
```

This satisfies the business requirement directly.

------------------------------------------------------------------------------

# Step 7 – Top Level Domain

Allowed

```
.com

.in

.org
```

Regex

```regex
(com|in|org)
```

Reason

Alternation

```
|
```

means

```
OR
```

------------------------------------------------------------------------------

# Step 8 – Final Regex

```regex
^(?!.*\.\.)(?!.*\+\+)[A-Za-z0-9]([A-Za-z0-9.+_-]*[A-Za-z0-9])?@(gmail|yahoo)\.(com|in|org)$
```

------------------------------------------------------------------------------

# Engineering Note – Why Didn't We Add a Space Rule?

During implementation, one question came up.

> We wrote rules for

```
No ..

No ++
```

but we never wrote

```
No Spaces
```

### Why?

Because spaces are **already impossible**.

Our Local Part allows only

```regex
[A-Za-z0-9.+_-]
```

Our Provider allows only

```regex
(gmail|yahoo)
```

Our TLD allows only

```regex
(com|in|org)
```

Since **space (' ')** is not included anywhere,

inputs like

```
abc def@gmail.com
```

are automatically rejected.

Therefore,

an explicit rule like

```regex
(?!.*\s)
```

is **not required** for this validator.

---

## Defensive Programming

Some production systems still write

```regex
(?!.*\s)
```

at the beginning of the regex.

Reason

Even if someone accidentally modifies the character classes in the future,

the validator will still reject whitespace.

Example

```regex
^(?!.*\s)(?!.*\.\.)(?!.*\+\+)...
```

This is called **Defensive Programming**.

---

## Engineering Lesson

Never add unnecessary regex.

Ask yourself

```
Is this already impossible because of my current design?
```

If the answer is **Yes**,

adding another rule only makes the regex more complex without improving correctness.
------------------------------------------------------------------------------
# Complete Design

```
Start
 │
 │
 ├──────── Restriction Rules
 │            │
 │            ├── Reject ..
 │            └── Reject ++
 │
 ├──────── Local Part
 │
 ├──────── @
 │
 ├──────── Provider
 │
 ├──────── .
 │
 ├──────── Top Level Domain
 │
End
```

------------------------------------------------------------------------------

# Testing Strategy

Never test only valid inputs.

Always test

## Valid Cases

```
a@gmail.com

abc@gmail.com

abc123@gmail.com

abc.xyz@gmail.com

abc_def@gmail.com

abc-def@gmail.com

abc+office@gmail.com

abc@yahoo.com

abc@yahoo.in

abc@yahoo.org
```

------------------------------------------------------------------------------

## Invalid Cases

```
@gmail.com

.abc@gmail.com

abc.@gmail.com

abc..xyz@gmail.com

abc++xyz@gmail.com

abc@gmail

abc@gmail.

abc@gmail.xyz

abc@hotmail.com

abc@teja.com

abc@@gmail.com

abc gmail@gmail.com

abc#gmail@gmail.com
```

------------------------------------------------------------------------------

# Engineering Lessons Learned

This exercise was NOT about Email Validation.

It was about learning a systematic way to design validators.

The major lessons learned were

✅ Collect requirements before writing regex.

✅ Convert requirements into rules.

✅ Separate Matching Rules from Restriction Rules.

✅ Build regex incrementally.

✅ Test after every modification.

✅ When regex fails,

perform Root Cause Analysis instead of randomly changing syntax.

✅ When requirements say

```
Must NOT
```

think

```
Negative Lookahead
```

✅ Most regex bugs are Design Problems,

not Syntax Problems.

------------------------------------------------------------------------------

# Common Beginner Mistakes

During this exercise, the following mistakes were encountered.

---

## Mistake 1

Escaping Character Classes

Incorrect

```regex
\[A-Za-z]
```

Reason

```
\[
```

matches a literal '[' character.

Correct

```regex
[A-Za-z]
```

---

## Mistake 2

Escaping Groups

Incorrect

```regex
\(
```

Reason

```
\(
```

matches a literal '('.

Correct

```regex
(
```

---

## Mistake 3

Escaping Quantifiers

Incorrect

```regex
\*
```

Reason

```
\*
```

matches a literal '*'.

Correct

```regex
*
```

---

## Mistake 4

Thinking

```regex
(?!\.\.)
```

checks the whole string.

Reality

It checks only the current position.

Correct

```regex
(?!.*\.\.)
```

---

## Mistake 5

Trying to solve the entire validation in one regex.

Correct Engineering Practice

```
Requirement
        ↓
Rules
        ↓
Small Regex
        ↓
Testing
        ↓
Improve
```

------------------------------------------------------------------------------

# Interview Questions

### Q1

Why do we use '^' ?

Answer

To indicate the start of the string.

---

### Q2

Why do we use '$' ?

Answer

To indicate the end of the string.

Without '$',

partial matches become possible.

---

### Q3

Why was the following regex incorrect?

```regex
^[A-Za-z0-9][A-Za-z0-9.+_-]*[A-Za-z0-9]?$
```

Answer

The middle portion was greedy.

The optional last character allowed the regex to succeed even when the string ended with '.'

---

### Q4

Why was grouping required?

Answer

Grouping changed the design from

```
First

↓

Middle

↓

Optional Last
```

to

```
First

↓

(Optional Middle + Last)
```

which prevented the greedy middle portion from consuming the final character.

---

### Q5

When should Negative Lookahead be used?

Answer

Whenever requirements contain

```
Must NOT
```

Examples

```
No ..

No ++

No Spaces

No @@
```

---

### Q6

What is the purpose of

```regex
.*
```

inside

```regex
(?!.*PATTERN)
```

Answer

It searches the remaining string for the forbidden pattern.

Meaning

```
Reject if PATTERN exists anywhere.
```

------------------------------------------------------------------------------

# Engineering Summary

Email validation was not the actual goal.

The real goal was learning an engineering process for designing validators.

That process is

```
Understand the Problem

        ↓

Collect Requirements

        ↓

Convert Requirements into Rules

        ↓

Separate Rules

        ↓

Matching Rules

        ↓

Restriction Rules

        ↓

Design Regex

        ↓

Test

        ↓

Debug

        ↓

Improve

        ↓

Finalize
```

This exact workflow will be reused for every future validation problem.

------------------------------------------------------------------------------

# Skills Learned

By completing this exercise, the following Regex concepts were mastered.

✅ Character Classes

✅ Anchors

✅ Quantifiers

✅ Greedy Matching

✅ Grouping

✅ Optional Groups

✅ Alternation

✅ Negative Lookahead

✅ Business Rule Validation

✅ Engineering Methodology

------------------------------------------------------------------------------

# Future Validation Problems

Question 2

IPv4 Address Validation

---

Question 3

MAC Address Validation

---

Question 4

URL Validation

---

Question 5

Phone Number Validation

---

Question 6

Password Validation

---

Question 7

Serial Number Validation

---

Question 8

UUID Validation

---

Question 9

Product ID Validation

---

Question 10

Storage Device Name Validation

------------------------------------------------------------------------------
```
import re

pattern = r"^(?!.*\.\.)(?!.*\+\+)[A-Za-z0-9]([A-Za-z0-9.+_-]*[A-Za-z0-9])?@(gmail|yahoo)\.(com|in|org)$"

emails = [
    # Valid
    "a@gmail.com",
    "abc@gmail.com",
    "abc123@gmail.com",
    "abc.xyz@gmail.com",
    "abc_xyz@gmail.com",
    "abc-def@gmail.com",
    "abc+office@gmail.com",
    "abc@yahoo.com",
    "abc@yahoo.in",
    "abc@yahoo.org",

    # Invalid
    "@gmail.com",
    ".abc@gmail.com",
    "abc.@gmail.com",
    "abc..xyz@gmail.com",
    "abc++xyz@gmail.com",
    "abc@gmail",
    "abc@gmail.",
    "abc@gmail.xyz",
    "abc@hotmail.com",
    "abc@teja.com",
    "abc@@gmail.com",
    "abc gmail@gmail.com",
    "abc#gmail@gmail.com",
]

print("========== EMAIL VALIDATION ==========\n")

for email in emails:
    if re.fullmatch(pattern, email):
        print(f"✅ VALID   : {email}")
    else:
        print(f"❌ INVALID : {email}")
```
# Final Note

This notebook is intentionally written as an engineering diary rather than a collection of regex patterns.

Whenever solving a new validation problem:

1. Never start with the regex.
2. Start with the requirements.
3. Convert requirements into rules.
4. Separate matching rules from restriction rules.
5. Build the regex incrementally.
6. Test every step.
7. Analyze failures instead of guessing.
8. Improve the design until all test cases pass.

If this methodology is followed consistently, even complex validators become manageable and easier to debug.
