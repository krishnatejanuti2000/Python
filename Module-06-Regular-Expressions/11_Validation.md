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
---

# Question 2 – IPv4 Address Validation

---

## Problem Statement

Validate an IPv4 Address using Python Regular Expressions.

---

## Business Requirements

An IPv4 address contains four decimal octets.

Each octet must be within:

```text
0–255
```

For this exercise, we also decided not to accept leading-zero representations such as:

```text
01
001
010
```

Examples

✅ Valid

```text
192.168.1.1
10.0.0.1
255.255.255.255
0.0.0.0
```

❌ Invalid

```text
256.1.1.1
1.1.1.256
01.1.1.1
192.168.001.010
```

---

# Step 1 – Requirement Analysis

The biggest mistake would be trying to write the complete IPv4 regex immediately.

Instead,

break the IPv4 address into four identical components.

```text
192.168.1.10

│    │   │ │
│    │   │ └── Octet 4
│    │   └──── Octet 3
│    └──────── Octet 2
└───────────── Octet 1
```

Therefore:

```text
IPv4 Address

=

Octet
+
.
+
Octet
+
.
+
Octet
+
.
+
Octet
```

The difficult part is only:

```text
How do we validate one octet from 0–255?
```

So we solve one octet first.

---

# Step 2 – Designing One Octet

The range is:

```text
0–255
```

We cannot directly write:

```regex
\d{1,3}
```

because that would allow:

```text
256
999
500
```

Therefore, we split the range into smaller logical ranges.

```text
0–9
10–99
100–199
200–249
250–255
```

This is the same numeric-range engineering method used later for date validation.

---

# Step 3 – Range 0–9

Single digits:

```text
0
1
2
...
9
```

Regex:

```regex
\d
```

---

# Step 4 – Range 10–99

First digit cannot be zero.

```regex
[1-9]\d
```

This matches:

```text
10
11
...
99
```

It does not match:

```text
00
01
09
```

This also prevents the leading-zero representation.

---

# Step 5 – Range 100–199

The first digit is always:

```text
1
```

The remaining two digits can be anything.

Regex:

```regex
1\d{2}
```

Matches:

```text
100
101
...
199
```

---

# Step 6 – Range 200–249

The first digit is:

```text
2
```

The second digit can only be:

```text
0–4
```

The last digit can be anything.

Regex:

```regex
2[0-4]\d
```

Matches:

```text
200
201
...
249
```

---

# Step 7 – Range 250–255

The first two digits are:

```text
25
```

The final digit can only be:

```text
0–5
```

Regex:

```regex
25[0-5]
```

Matches:

```text
250
251
252
253
254
255
```

---

# Step 8 – Combine the Octet Ranges

We now have:

```regex
\d
```

```regex
[1-9]\d
```

```regex
1\d{2}
```

```regex
2[0-4]\d
```

```regex
25[0-5]
```

Using alternation:

```regex
(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)
```

This represents:

```text
0–9
10–99
100–199
200–249
250–255
```

---

# Step 9 – Four Octets

Now repeat the same octet pattern four times.

Separate each octet using a literal dot:

```regex
\.
```

Final IPv4 regex:

```regex
^(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)$
```

---

# Testing Strategy

Never test only valid inputs.

Always test the boundaries.

## Valid Cases

```text
0.0.0.0
1.1.1.1
9.9.9.9
10.10.10.10
99.99.99.99
100.100.100.100
199.199.199.199
200.200.200.200
249.249.249.249
250.250.250.250
255.255.255.255
192.168.1.10
```

---

## Invalid Cases

```text
256.1.1.1
1.256.1.1
1.1.256.1
1.1.1.256
01.1.1.1
001.1.1.1
192.168.001.010
999.999.999.999
1.1.1
1.1.1.1.1
```

---

# Engineering Lessons

The major lesson was:

> Never try to validate `0–255` as simply `\d{1,3}`.

Instead:

```text
Numeric Range
      ↓
Split into logical ranges
      ↓
Build each range
      ↓
Combine using alternation
```

This exact methodology was reused for:

- Month `01–12`
- Day `01–31`
- Year `1900–2099`
- Calendar validation

---

# Final Reference Code

```python
import re

text = input("Enter IPv4 address: ")

pattern = r"^(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.(25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)$"

result = re.fullmatch(pattern, text)

if result:
    print("Valid IPv4 address")
else:
    print("Invalid IPv4 address")
```

---

# Question 3 – MAC Address Validation

---

## Problem Statement

Validate MAC addresses using Python Regular Expressions.

We deliberately handled the three requested representations separately.

```text
Linux / Unix
Windows
Cisco
```

We did **NOT** combine them into one regex.

---

# Part A – Linux / Unix Format

## Format

```text
AA:BB:CC:DD:EE:FF
```

A MAC address contains six groups.

Each group contains two hexadecimal characters.

---

# Step 1 – Understand Hexadecimal

Allowed characters:

```text
0–9
A–F
a–f
```

Regex:

```regex
[A-Fa-f0-9]
```

---

# Step 2 – Two Hexadecimal Characters

Requirement:

```text
AA
```

Regex:

```regex
[A-Fa-f0-9]{2}
```

This became our reusable MAC group.

---

# Step 3 – Six Groups

The Linux representation uses:

```text
:
```

as the separator.

Final Linux regex:

```regex
^([A-Fa-f0-9]{2}):([A-Fa-f0-9]{2}):([A-Fa-f0-9]{2}):([A-Fa-f0-9]{2}):([A-Fa-f0-9]{2}):([A-Fa-f0-9]{2})$
```

---

# Part B – Windows Format

## Format

```text
AA-BB-CC-DD-EE-FF
```

The hexadecimal group remains:

```regex
[A-Fa-f0-9]{2}
```

Only the separator changes.

```text
-
```

Final Windows regex:

```regex
^([A-Fa-f0-9]{2})-([A-Fa-f0-9]{2})-([A-Fa-f0-9]{2})-([A-Fa-f0-9]{2})-([A-Fa-f0-9]{2})-([A-Fa-f0-9]{2})$
```

---

# Part C – Cisco Format

## Format

```text
AAAA.BBBB.CCCC
```

Cisco uses three groups.

Each group contains four hexadecimal characters.

---

# Step 1 – Four Hexadecimal Characters

```regex
[A-Fa-f0-9]{4}
```

---

# Step 2 – Three Groups

The separator is:

```text
.
```

Because `.` is a regex metacharacter, we escape it:

```regex
\.
```

Final Cisco regex:

```regex
^([A-Fa-f0-9]{4})\.([A-Fa-f0-9]{4})\.([A-Fa-f0-9]{4})$
```

---

# Testing Strategy

## Linux Valid

```text
00:11:22:33:44:55
AA:BB:CC:DD:EE:FF
aa:bb:cc:dd:ee:ff
A1:B2:C3:D4:E5:F6
```

## Linux Invalid

```text
00:11:22:33:44
00:11:22:33:44:55:66
GG:11:22:33:44:55
00-11-22-33-44-55
```

---

## Windows Valid

```text
00-11-22-33-44-55
AA-BB-CC-DD-EE-FF
aa-bb-cc-dd-ee-ff
A1-B2-C3-D4-E5-F6
```

## Windows Invalid

```text
00-11-22-33-44
00-11-22-33-44-55-66
GG-11-22-33-44-55
00:11:22:33:44:55
```

---

## Cisco Valid

```text
0011.2233.4455
AABB.CCDD.EEFF
aabb.ccdd.eeff
A1B2.C3D4.E5F6
```

## Cisco Invalid

```text
0011.2233
0011.2233.4455.6677
GG11.2233.4455
00:11:22:33:44:55
```

---

# Engineering Lessons

The important observation was:

```text
Same MAC data
      ↓
Different presentation format
      ↓
Different regex separator/group structure
```

Linux:

```text
XX:XX:XX:XX:XX:XX
```

Windows:

```text
XX-XX-XX-XX-XX-XX
```

Cisco:

```text
XXXX.XXXX.XXXX
```

We intentionally kept these validators separate rather than creating one complicated combined expression.

> Optimization of these three patterns was discussed but deliberately postponed for later documentation.

---

# Final Reference Code

## Linux

```python
import re

text = input("Enter the MAC address: ")

group = r"([A-Fa-f0-9]{2})"

pattern = rf"^{group}:{group}:{group}:{group}:{group}:{group}$"

result = re.fullmatch(pattern, text)

if result:
    print("Valid MAC address")
else:
    print("Invalid MAC address")
```

## Windows

```python
import re

text = input("Enter the MAC address: ")

group = r"([A-Fa-f0-9]{2})"

pattern = rf"^{group}-{group}-{group}-{group}-{group}-{group}$"

result = re.fullmatch(pattern, text)

if result:
    print("Valid MAC address")
else:
    print("Invalid MAC address")
```

## Cisco

```python
import re

text = input("Enter the MAC address: ")

group = r"([A-Fa-f0-9]{4})"

pattern = rf"^{group}\.{group}\.{group}$"

result = re.fullmatch(pattern, text)

if result:
    print("Valid MAC address")
else:
    print("Invalid MAC address")
```

---

# Question 4 – Password Validation

---

## Problem Statement

Validate a password using Python Regular Expressions.

---

## Business Requirements

The password must:

- Contain at least 8 characters.
- Contain at least one uppercase letter.
- Contain at least one lowercase letter.
- Contain at least one digit.
- Contain at least one special character.
- Not contain spaces or other whitespace.

---

# Step 1 – Positive Lookahead

The first requirement we solved was:

```text
At least one uppercase letter
```

Initial thought:

```regex
(?=[A-Z]{1,})
```

The issue was that this only checks from the current position.

We changed it to:

```regex
(?=.*[A-Z])
```

Meaning:

```text
Search anywhere
+
Find at least one uppercase letter
```

---

# Step 2 – Lowercase

```regex
(?=.*[a-z])
```

Meaning:

> At least one lowercase letter must exist somewhere.

---

# Step 3 – Digit

```regex
(?=.*\d)
```

Meaning:

> At least one digit must exist somewhere.

---

# Step 4 – Special Character

We considered a broad solution:

```regex
(?=.*[^\w])
```

But this can also match whitespace.

Since the requirement explicitly says a special character is required and whitespace is forbidden, we chose an explicit special-character set.

```regex
(?=.*[!@#$%^&*()_+=-])
```

---

# Step 5 – Minimum Length

Requirement:

```text
At least 8 characters
```

Regex:

```regex
.{8,}
```

Meaning:

```text
Any character
at least 8 times
```

---

# Step 6 – No Whitespace

Negative lookahead:

```regex
(?!.*\s)
```

Meaning:

> Reject if whitespace occurs anywhere.

---

# Final Password Regex

```regex
^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+=-])(?!.*\s).{8,}$
```

---

# Testing Strategy

## Valid

```text
Password1@
P@ssword123
Admin@2025
Hello@123
Abcdef1!
Qwerty9#
Strong_Pass1+
```

## Invalid

Less than 8 characters:

```text
Pass1@
Ab1@
```

No uppercase:

```text
password1@
hello123#
```

No lowercase:

```text
PASSWORD1@
ADMIN@123
```

No digit:

```text
Password@
HelloWorld#
```

No special character:

```text
Password1
Admin2025
```

Whitespace:

```text
Pass word1@
Admin @123
Password 1!
```

---

# Engineering Lessons

The main lesson was the difference between:

```text
Must contain
```

and:

```text
Must NOT contain
```

For "must contain":

```regex
(?=.*PATTERN)
```

For "must NOT contain":

```regex
(?!.*PATTERN)
```

This is one of the most reusable patterns in validation regex.

---

# Final Reference Code

```python
import re

text = input("Enter password: ")

pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()_+=-])(?!.*\s).{8,}$"

result = re.fullmatch(pattern, text)

if result:
    print("Valid password")
else:
    print("Invalid password")
```

---

# Question 5 – Mobile Number Validation

---

## Problem Statement

Validate an Indian mobile number using Python Regular Expressions.

---

## Business Requirements

For this exercise:

- Mobile number contains exactly 10 digits.
- First digit must be `6–9`.
- Optional country code may be:
  - `91`
  - `+91`
- The country code is optional.

Accepted formats:

```text
9876543210
919876543210
+919876543210
```

---

# Step 1 – Country Code

We first thought about:

```regex
(+91|91|?)
```

This was incorrect.

Why?

The `+` character is a regex metacharacter.

A literal plus should be written:

```regex
\+91
```

Also,

```text
?
```

does not mean "nothing" in an alternation.

Instead, the whole group should be optional.

Correct:

```regex
(91|\+91)?
```

Meaning:

```text
91
OR
+91
OR
nothing
```

---

# Step 2 – Mobile Number

The first digit must be:

```text
6–9
```

Regex:

```regex
[6-9]
```

Remaining nine characters:

```regex
\d{9}
```

Combined:

```regex
[6-9]\d{9}
```

---

# Step 3 – Combine

Country code:

```regex
(91|\+91)?
```

Mobile number:

```regex
[6-9]\d{9}
```

Final:

```regex
^(91|\+91)?[6-9]\d{9}$
```

---

# Testing Strategy

## Valid

```text
9876543210
919876543210
+919876543210
8123456789
7012345678
6123456789
```

## Invalid

```text
5123456789
0123456789
987654321
98765432101
+929876543210
91919876543210
+91987654321
```

---

# Engineering Lessons

Optional group:

```regex
(A|B)?
```

means:

```text
A
OR
B
OR
nothing
```

Also remember:

```regex
\+
```

matches a literal `+`.

---

# Final Reference Code

```python
import re

text = input("Enter mobile number: ")

pattern = r"^(91|\+91)?[6-9]\d{9}$"

result = re.fullmatch(pattern, text)

if result:
    print("Valid mobile number")
else:
    print("Invalid mobile number")
```

---

# Question 6 – Date Validation

---

## Problem Statement

Validate dates using Python Regular Expressions.

---

## Frozen Business Requirements

For this exercise we selected:

```text
Format: MM/DD/YYYY
Year: 1900–2099
```

Calendar rules:

```text
31-day months:
01, 03, 05, 07, 08, 10, 12

30-day months:
04, 06, 09, 11

February:
01–28 normally
01–29 in leap years
```

Leap-year rules:

```text
Divisible by 400 → leap year
Divisible by 100 → not leap year
Divisible by 4   → leap year
```

Therefore:

```text
1900 → not leap
2000 → leap
2024 → leap
2023 → not leap
```

---

# Step 1 – Month Validation

Requirement:

```text
01–12
```

Split:

```text
01–09
10–12
```

Regex:

```regex
(0[1-9]|1[0-2])
```

### Mistake

We initially wrote:

```regex
(0[1-9]|1[1-2])
```

This excluded:

```text
10
```

Correct:

```regex
(0[1-9]|1[0-2])
```

---

# Step 2 – Basic Day Validation

Requirement:

```text
01–31
```

Split:

```text
01–09
10–19
20–29
30–31
```

Regex:

```regex
(0[1-9]|1[0-9]|2[0-9]|3[0-1])
```

### Mistake

We initially used:

```regex
(0[0-9]|1[0-9]|2[0-9]|3[0-1])
```

which allowed:

```text
00
```

We corrected it to:

```regex
0[1-9]
```

---

# Step 3 – Year Validation

Requirement:

```text
1900–2099
```

Initial attempt:

```regex
(1\d{3})|(20\d{2})
```

Problem:

```text
1000
1200
1500
1899
```

could match the first branch.

Correct:

```regex
(19\d{2}|20\d{2})
```

---

# Step 4 – Basic MM/DD/YYYY Regex

After assembling month, day, and year:

```regex
^(0[1-9]|1[0-2])/(0[1-9]|1[0-9]|2[0-9]|3[0-1])/(19\d{2}|20\d{2})$
```

This checks:

```text
Month range
Day range
Year range
Separators
Complete string
```

But it still accepts dates such as:

```text
02/31/2025
04/31/2025
02/29/2023
```

because month/day relationships are not yet represented.

---

# Step 5 – 31-Day Months

Months:

```text
01, 03, 05, 07, 08, 10, 12
```

Regex:

```regex
(01|03|05|07|08|10|12)
```

Day range:

```regex
(0[1-9]|1[0-9]|2[0-9]|3[0-1])
```

Complete branch:

```regex
(01|03|05|07|08|10|12)/(0[1-9]|1[0-9]|2[0-9]|3[0-1])/(19\d{2}|20\d{2})
```

---

# Step 6 – 30-Day Months

Months:

```text
04, 06, 09, 11
```

Day range:

```text
01–30
```

We derived:

```regex
(0[1-9]|1[0-9]|2[0-9]|30)
```

Complete branch:

```regex
(04|06|09|11)/(0[1-9]|1[0-9]|2[0-9]|30)/(19\d{2}|20\d{2})
```

---

# Step 7 – February 01–28

February is:

```text
02
```

Normal maximum day:

```text
28
```

We derived:

```regex
(0[1-9]|1[0-9]|2[0-8])
```

Complete branch:

```regex
02/(0[1-9]|1[0-9]|2[0-8])/(19\d{2}|20\d{2})
```

---

# Step 8 – Leap-Year Logic

The Gregorian rule is:

```text
Divisible by 400 → leap
Otherwise divisible by 100 → not leap
Otherwise divisible by 4 → leap
```

Within our restricted range:

```text
1900–2099
```

we split into:

```text
1900–1999
2000–2099
```

For two-digit endings divisible by 4:

```regex
([02468][048]|[13579][26])
```

For `1900–1999`, excluding `1900`:

```regex
19(?!00)([02468][048]|[13579][26])
```

For `2000–2099`:

```regex
20([02468][048]|[13579][26])
```

Combined:

```regex
(?:19(?!00)(?:[02468][048]|[13579][26])|20(?:[02468][048]|[13579][26]))
```

---

# Step 9 – February 29

February 29 is valid only when the year is a leap year.

Regex:

```regex
02/29/(?:19(?!00)(?:[02468][048]|[13579][26])|20(?:[02468][048]|[13579][26]))
```

Valid:

```text
02/29/2024
02/29/2000
02/29/1904
02/29/1996
```

Invalid:

```text
02/29/2023
02/29/1900
02/29/2100
```

---

# Final Calendar-Aware Date Regex

```python
pattern = r"^(?:(?:01|03|05|07|08|10|12)/(?:0[1-9]|1[0-9]|2[0-9]|3[0-1])/(?:19\d{2}|20\d{2})|(?:04|06|09|11)/(?:0[1-9]|1[0-9]|2[0-9]|30)/(?:19\d{2}|20\d{2})|02/(?:0[1-9]|1[0-9]|2[0-8])/(?:19\d{2}|20\d{2})|02/29/(?:19(?!00)(?:[02468][048]|[13579][26])|20(?:[02468][048]|[13579][26])))$"
```

---

# Date Testing Strategy

## Valid

```text
01/01/2025
01/31/2025
03/31/2025
04/30/2025
06/30/2025
09/30/2025
11/30/2025
02/28/2025
02/29/2024
02/29/2000
02/29/1904
12/31/2099
```

## Invalid

```text
00/01/2025
13/01/2025
01/00/2025
01/32/2025
04/31/2025
06/31/2025
09/31/2025
11/31/2025
02/29/2023
02/30/2025
02/31/2025
02/29/1900
01-01-2025
1/01/2025
01/1/2025
```

---

# Industry Engineering Note

The calendar-aware regex is useful for learning regex engineering.

However, in production Python, a cleaner architecture is normally:

```text
Input
  ↓
Regex
  ↓
Basic structure / format validation
  ↓
Python date library
  ↓
Actual calendar validation
```

Regex handles structure well.

A date library is better suited to actual calendar rules such as:

- Month-specific day limits.
- Leap years.
- February 29.

The engineering principle is:

> Use each tool for the responsibility it handles well and can maintain reliably.

---

# Final Reference Code

```python
import re

text = input("Enter date: ")

pattern = r"^(?:(?:01|03|05|07|08|10|12)/(?:0[1-9]|1[0-9]|2[0-9]|3[0-1])/(?:19\d{2}|20\d{2})|(?:04|06|09|11)/(?:0[1-9]|1[0-9]|2[0-9]|30)/(?:19\d{2}|20\d{2})|02/(?:0[1-9]|1[0-9]|2[0-8])/(?:19\d{2}|20\d{2})|02/29/(?:19(?!00)(?:[02468][048]|[13579][26])|20(?:[02468][048]|[13579][26])))$"

result = re.fullmatch(pattern, text)

if result:
    print("Valid date")
else:
    print("Invalid date")
```

---

# Overall Engineering Lessons from Questions 2–6

The same methodology kept appearing:

```text
Requirement
    ↓
Break into components
    ↓
Identify matching rules
    ↓
Identify restriction rules
    ↓
Split numeric ranges
    ↓
Build small regex components
    ↓
Combine components
    ↓
Test boundary values
    ↓
Test valid cases
    ↓
Test invalid cases
    ↓
Optimize only after understanding
```

## Important Regex Patterns

### Alternation

```regex
(A|B)
```

Means:

```text
A OR B
```

### Positive Lookahead

```regex
(?=.*PATTERN)
```

Means:

> PATTERN must exist somewhere.

### Negative Lookahead

```regex
(?!.*PATTERN)
```

Means:

> PATTERN must not exist anywhere.

### Optional Group

```regex
(A|B)?
```

Means:

```text
A
OR
B
OR
nothing
```

### Character Classes

```regex
[A-Z]
[a-z]
[0-9]
[6-9]
[A-Fa-f0-9]
```

### Quantifiers

```regex
\d{9}
```

Exactly nine digits.

```regex
.{8,}
```

At least eight characters.

### Anchors

```regex
^
$
```

Used to validate the complete string.

---

# Validation Progress

| Question | Problem | Status |
|---|---|---|
| 1 | Email Validation | ✅ Completed |
| 2 | IPv4 Validation | ✅ Completed |
| 3 | MAC Address Validation | ✅ Completed |
| 4 | Password Validation | ✅ Completed |
| 5 | Mobile Number Validation | ✅ Completed |
| 6 | Date Validation | ✅ Completed |

---

# Question 7 – Storage Device Identifier Validation

---

## Problem Statement

Validate a Linux Storage Device Identifier using Python Regular Expressions.

The Storage Test Automation framework receives a device identifier and must determine whether it follows one of the supported storage-device formats.

---

## Business Requirements

Two storage-device formats are supported.

### SATA/SCSI-style devices

```text
/dev/sda
/dev/sdb
/dev/sda1
/dev/sdb12
````

### NVMe devices

```text
/dev/nvme0n1
/dev/nvme1n1
/dev/nvme0n1p1
/dev/nvme2n3p16
```

---

## Invalid Examples

```text
/dev/
/dev/s
/dev/sdaabc
/dev/sda-1
/dev/nvme
/dev/nvmeXn1
/dev/nvme0
/dev/nvme0n
/dev/nvme0n1abc
```

---

# Step 1 – Requirement Analysis

The biggest mistake would be trying to write the complete device-validation regex immediately.

Instead, break the requirement into the two supported device formats.

```text
Storage Device
      |
      +----------------------+
      |                      |
   SATA/SCSI                NVMe
      |                      |
   /dev/sda...           /dev/nvme...
```

Therefore, solve each device format independently.

---

# Step 2 – Designing SATA/SCSI Device Format

Consider:

```text
/dev/sda
/dev/sda1
/dev/sdb12
```

Break the structure:

```text
/dev/sda12

│   │ │  │
│   │ │  └── Partition number
│   │ └───── Device letter
│   └─────── sd
└─────────── /dev/
```

The requirements are:

```text
/dev/       → mandatory
sd          → mandatory
[a-z]       → one lowercase device letter
\d*         → optional partition number
```

---

## SATA/SCSI Regex

```regex
/dev/sd[a-z]\d*
```

---

## Why `\d*`?

The partition number is optional.

Therefore both:

```text
/dev/sda
/dev/sda1
```

must be accepted.

If we used:

```regex
\d+
```

then:

```text
/dev/sda
```

would fail because at least one digit would be required.

Therefore:

```regex
\d*
```

is correct.

---

# Step 3 – Designing NVMe Device Format

Consider:

```text
/dev/nvme0n1
/dev/nvme1n1
/dev/nvme0n1p1
/dev/nvme2n3p16
```

Break the structure:

```text
/dev/nvme2n3p16

│        │ │ │  │
│        │ │ │  └── Partition number
│        │ │ └───── p
│        │ └─────── Namespace number
│        └───────── n
└────────────────── Controller number
```

The structure is:

```text
/dev/nvme
controller number
n
namespace number
optional p + partition number
```

---

## NVMe Regex

```regex
/dev/nvme\dn\d(?:p\d+)?
```

---

## Why Is `p` Optional?

Consider:

```text
/dev/nvme0n1
```

This is the namespace itself.

A partition is represented as:

```text
/dev/nvme0n1p1
```

Therefore:

```regex
(?:p\d+)?
```

means:

```text
p + partition number
```

is optional.

---

# Step 4 – Combining Both Device Formats

We now have two independent patterns.

SATA/SCSI:

```regex
/dev/sd[a-z]\d*
```

NVMe:

```regex
/dev/nvme\dn\d(?:p\d+)?
```

Because the input may match either format, use alternation.

```regex
(A|B)
```

Therefore:

```regex
(/dev/sd[a-z]\d*|/dev/nvme\dn\d(?:p\d+)?)
```

---

# Step 5 – Complete Validation

This is a validation problem.

We don't want to find a valid device name somewhere inside a larger string.

The **entire input** must be valid.

Therefore:

```regex
^
```

and:

```regex
$
```

are required.

Final pattern:

```regex
^(/dev/sd[a-z]\d*|/dev/nvme\dn\d(?:p\d+)?)$
```

---

# Final Solution

```python
import re

pattern = r"^(/dev/sd[a-z]\d*|/dev/nvme\dn\d(?:p\d+)?)$"

devices = [
    # Valid
    "/dev/sda",
    "/dev/sdb",
    "/dev/sda1",
    "/dev/sdb12",
    "/dev/nvme0n1",
    "/dev/nvme1n1",
    "/dev/nvme0n1p1",
    "/dev/nvme2n3p16",

    # Invalid
    "/dev/",
    "/dev/s",
    "/dev/sdaabc",
    "/dev/sda-1",
    "/dev/nvme",
    "/dev/nvmeXn1",
    "/dev/nvme0",
    "/dev/nvme0n",
    "/dev/nvme0n1abc"
]

print("========== STORAGE DEVICE VALIDATION ==========\n")

for device in devices:
    if re.fullmatch(pattern, device):
        print(f"VALID   : {device}")
    else:
        print(f"INVALID : {device}")
```

---

# Why `re.fullmatch()`?

The requirement is:

> The complete input must represent a valid storage device.

We do not want:

```text
abc/dev/sda/xyz
```

to be accepted just because `/dev/sda` appears inside it.

Therefore:

```python
re.fullmatch()
```

is appropriate.

---

# Boundary Testing

### Valid Boundaries

```text
/dev/sda
/dev/sda1
/dev/sda999
/dev/nvme0n1
/dev/nvme0n1p1
/dev/nvme0n1p999
```

### Invalid Boundaries

```text
/dev/s
/dev/sdaX
/dev/sda-1
/dev/nvmeXn1
/dev/nvme0
/dev/nvme0n
/dev/nvme0n1X
```

---

# Engineering Lesson

The important lesson is not the final regex.

The important design process was:

```text
Two device families
        ↓
Separate each format
        ↓
Build individual regex components
        ↓
Combine using alternation
        ↓
Require complete input
        ↓
Use re.fullmatch()
        ↓
Boundary testing
```

---

# Question 8 – Storage Capacity Validation

---

## Problem Statement

Validate a Storage Capacity value using Python Regular Expressions.

The Storage Test Automation framework receives capacity values such as:

```text
512MB
500GB
1TB
1.5TB
10.25GB
4PB
```

---

## Business Requirements

The format is:

```text
<number><unit>
```

Allowed units:

```text
MB
GB
TB
PB
```

The numeric portion may contain:

```text
Integer
```

or:

```text
Decimal number
```

---

## Valid Examples

```text
512MB
500GB
1TB
2TB
1.5TB
10.25GB
4PB
```

---

## Invalid Examples

```text
500
500KB
500gb
1.5
TB
.5TB
1..5TB
1TBextra
abcGB
-1TB
```

---

# Step 1 – Requirement Analysis

Break the capacity into two components.

```text
Storage Capacity
       |
       +----------+
       |          |
     Number      Unit
```

For:

```text
1.5TB
```

we have:

```text
1.5 → Number
TB  → Unit
```

---

# Step 2 – Designing the Number

The number may be:

```text
1
500
1.5
10.25
```

The integer portion requires:

```regex
\d+
```

A decimal portion is optional:

```regex
(?:\.\d+)?
```

Therefore:

```regex
\d+(?:\.\d+)?
```

---

# Step 3 – Designing the Unit

Allowed units are:

```text
MB
GB
TB
PB
```

Therefore:

```regex
(?:MB|GB|TB|PB)
```

---

# Step 4 – Combine Number and Unit

```regex
\d+(?:\.\d+)?(?:MB|GB|TB|PB)
```

---

# Step 5 – Complete Validation

The entire input must represent a capacity.

Therefore:

```regex
^\d+(?:\.\d+)?(?:MB|GB|TB|PB)$
```

---

# Final Solution

```python
import re

pattern = r"^\d+(?:\.\d+)?(?:MB|GB|TB|PB)$"

capacities = [
    # Valid
    "512MB",
    "500GB",
    "1TB",
    "2TB",
    "1.5TB",
    "10.25GB",
    "4PB",

    # Invalid
    "500",
    "500KB",
    "500gb",
    "1.5",
    "TB",
    ".5TB",
    "1..5TB",
    "1TBextra",
    "abcGB",
    "-1TB"
]

print("========== STORAGE CAPACITY VALIDATION ==========\n")

for capacity in capacities:
    if re.fullmatch(pattern, capacity):
        print(f"VALID   : {capacity}")
    else:
        print(f"INVALID : {capacity}")
```

---

# Boundary Testing

```text
1MB          → VALID
1GB          → VALID
1TB          → VALID
1PB          → VALID
1.5TB        → VALID
10.25GB      → VALID

.5TB         → INVALID
1.TB         → INVALID
1..5TB       → INVALID
1KB          → INVALID
1tb          → INVALID
1TBextra     → INVALID
```

---

# Important Engineering Note

Regex is validating the **format**.

It is not determining whether the capacity is physically realistic.

For example:

```text
999999999PB
```

may be structurally valid even though it is not a realistic storage capacity.

Therefore:

```text
Regex
  ↓
Format validation

Python/business logic
  ↓
Range/business validation
```

This separation is important in production automation.

---

# Engineering Lesson

Do not make the regex responsible for every possible business rule.

First determine:

> Is the value structurally valid?

Then perform additional business validation separately when required.

---

# Question 9 – Storage Firmware Version Validation

---

## Problem Statement

Validate a Storage Device Firmware Version using Python Regular Expressions.

The required format is:

```text
FW<major>.<minor>.<patch>
```

---

## Business Requirements

`FW` is mandatory.

The following must be numeric:

```text
major
minor
patch
```

Each component must contain one or more digits.

---

## Valid Examples

```text
FW1.0.0
FW2.5.13
FW10.2.4
FW123.45.678
```

---

## Invalid Examples

```text
1.0.0
FW1
FW1.0
FW1.0.0.1
FWa.b.c
FW1-0-0
FW1.0.x
XFW1.0.0
FW1.0.0beta
```

---

# Step 1 – Requirement Analysis

Break the version into components.

```text
FW1.2.3

││ │ │
││ │ └── Patch
││ └──── Minor
│└────── Major
└─────── Mandatory FW prefix
```

Therefore:

```text
FW
+
major
+
.
+
minor
+
.
+
patch
```

---

# Step 2 – Firmware Prefix

```regex
FW
```

---

# Step 3 – Major Version

One or more digits:

```regex
\d+
```

---

# Step 4 – Dot Separator

A literal dot must be escaped.

```regex
\.
```

Why?

Because:

```regex
.
```

means:

> Any character.

But:

```regex
\.
```

means:

> Literal dot.

---

# Step 5 – Minor Version

```regex
\d+
```

---

# Step 6 – Second Dot

```regex
\.
```

---

# Step 7 – Patch Version

```regex
\d+
```

---

# Step 8 – Combine

```regex
FW\d+\.\d+\.\d+
```

---

# Step 9 – Complete Validation

```regex
^FW\d+\.\d+\.\d+$
```

---

# Final Solution

```python
import re

pattern = r"^FW\d+\.\d+\.\d+$"

versions = [
    # Valid
    "FW1.0.0",
    "FW2.5.13",
    "FW10.2.4",
    "FW123.45.678",

    # Invalid
    "1.0.0",
    "FW1",
    "FW1.0",
    "FW1.0.0.1",
    "FWa.b.c",
    "FW1-0-0",
    "FW1.0.x",
    "XFW1.0.0",
    "FW1.0.0beta"
]

print("========== FIRMWARE VERSION VALIDATION ==========\n")

for version in versions:
    if re.fullmatch(pattern, version):
        print(f"VALID   : {version}")
    else:
        print(f"INVALID : {version}")
```

---

# Boundary Testing

### Valid

```text
FW0.0.0
FW1.0.0
FW10.20.30
FW999.999.999
```

### Invalid

```text
FW1
FW1.0
FW1.0.0.1
FW1..0
FW1.0.
FW.1.0
FWa.1.0
FW1.0.x
```

---

# Engineering Lesson

This problem reinforces:

```text
Literal characters
+
Character classes
+
Quantifiers
+
Anchors
```

Before using lookarounds or complicated logic, first ask:

> Can the requirement be expressed directly through structure?

If yes, prefer the simpler regex.

---

# Question 10 – Enterprise Storage Test Parameter Validation

---

## Problem Statement

The Storage Test Automation framework receives an I/O test configuration as a single parameter string.

The validator must determine whether the complete configuration follows the required format.

---

## Business Requirements

The required format is:

```text
MODE=<mode> SIZE=<capacity> BLOCK=<block_size> QUEUE=<queue_depth>
```

All four fields are mandatory.

---

# MODE Requirements

Only these values are allowed:

```text
read
write
randread
randwrite
```

---

# SIZE Requirements

The size must contain:

```text
number + unit
```

Allowed units:

```text
MB
GB
TB
```

Examples:

```text
512MB
1GB
4GB
1.5TB
```

---

# BLOCK Requirements

The block size must contain:

```text
integer + KB
```

Examples:

```text
4KB
8KB
64KB
128KB
```

Decimal block sizes are not allowed.

---

# QUEUE Requirements

Queue depth must be a positive integer.

Examples:

```text
1
4
8
32
128
```

Zero and negative values are invalid.

---

## Valid Examples

```text
MODE=read SIZE=1TB BLOCK=128KB QUEUE=32
MODE=write SIZE=500GB BLOCK=4KB QUEUE=8
MODE=randread SIZE=1.5TB BLOCK=64KB QUEUE=128
MODE=randwrite SIZE=512MB BLOCK=8KB QUEUE=1
```

---

## Invalid Examples

```text
MODE=delete SIZE=1TB BLOCK=128KB QUEUE=32
MODE=read SIZE=1PB BLOCK=128KB QUEUE=32
MODE=read SIZE=1TB BLOCK=1.5KB QUEUE=32
MODE=read SIZE=1TB BLOCK=128MB QUEUE=32
MODE=read SIZE=1TB BLOCK=128KB QUEUE=0
MODE=read SIZE=1TB BLOCK=128KB QUEUE=-1
MODE=read SIZE=1TB BLOCK=128KB
MODE=read SIZE=1TB BLOCK=128KB QUEUE=32 EXTRA=x
```

---

# Step 1 – Requirement Analysis

The complete configuration contains four fields.

```text
Configuration
      |
      +-----------------------------+
      |             |       |       |
     MODE          SIZE   BLOCK   QUEUE
```

Do not build the complete regex immediately.

Solve each field independently.

---

# Step 2 – MODE Validation

Allowed values:

```text
read
write
randread
randwrite
```

Therefore:

```regex
(?:read|write|randread|randwrite)
```

---

# Step 3 – SIZE Validation

From Question 8, the numeric portion is:

```regex
\d+(?:\.\d+)?
```

Allowed units for this question:

```regex
(?:MB|GB|TB)
```

Therefore:

```regex
\d+(?:\.\d+)?(?:MB|GB|TB)
```

---

# Step 4 – BLOCK Validation

The requirement says:

```text
Integer + KB
```

Therefore:

```regex
\d+KB
```

A decimal value such as:

```text
1.5KB
```

must fail.

---

# Step 5 – QUEUE Validation

The queue depth must be a positive integer.

A positive integer can be represented as:

```regex
[1-9]\d*
```

The first digit must be from:

```text
1–9
```

and additional digits are optional.

Therefore:

```text
1
8
32
128
```

are accepted.

But:

```text
0
```

is rejected.

---

# Step 6 – Field Names

The field names are mandatory:

```text
MODE=
SIZE=
BLOCK=
QUEUE=
```

---

# Step 7 – Field Separators

Fields are separated by whitespace.

Therefore:

```regex
\s+
```

is used between fields.

---

# Step 8 – Combine Everything

Conceptually:

```text
MODE=<mode>
    ↓
whitespace
    ↓
SIZE=<size>
    ↓
whitespace
    ↓
BLOCK=<block>
    ↓
whitespace
    ↓
QUEUE=<queue>
```

---

# Step 9 – Complete Validation

The final structure is:

```regex
^MODE=(?:read|write|randread|randwrite)\s+SIZE=\d+(?:\.\d+)?(?:MB|GB|TB)\s+BLOCK=\d+KB\s+QUEUE=[1-9]\d*$
```

---

# Final Solution

```python
import re

pattern = (
    r"^MODE=(?:read|write|randread|randwrite)"
    r"\s+SIZE=\d+(?:\.\d+)?(?:MB|GB|TB)"
    r"\s+BLOCK=\d+KB"
    r"\s+QUEUE=[1-9]\d*$"
)

tests = [
    # Valid
    "MODE=read SIZE=1TB BLOCK=128KB QUEUE=32",
    "MODE=write SIZE=500GB BLOCK=4KB QUEUE=8",
    "MODE=randread SIZE=1.5TB BLOCK=64KB QUEUE=128",
    "MODE=randwrite SIZE=512MB BLOCK=8KB QUEUE=1",

    # Invalid
    "MODE=delete SIZE=1TB BLOCK=128KB QUEUE=32",
    "MODE=read SIZE=1PB BLOCK=128KB QUEUE=32",
    "MODE=read SIZE=1TB BLOCK=1.5KB QUEUE=32",
    "MODE=read SIZE=1TB BLOCK=128MB QUEUE=32",
    "MODE=read SIZE=1TB BLOCK=128KB QUEUE=0",
    "MODE=read SIZE=1TB BLOCK=128KB QUEUE=-1",
    "MODE=read SIZE=1TB BLOCK=128KB",
    "MODE=read SIZE=1TB BLOCK=128KB QUEUE=32 EXTRA=x"
]

print("========== STORAGE TEST PARAMETER VALIDATION ==========\n")

for test in tests:
    if re.fullmatch(pattern, test):
        print(f"VALID   : {test}")
    else:
        print(f"INVALID : {test}")
```

---

# Why `re.fullmatch()`?

This is a complete validation problem.

The input must contain exactly:

```text
MODE
SIZE
BLOCK
QUEUE
```

Therefore:

```text
MODE=read SIZE=1TB BLOCK=128KB QUEUE=32 EXTRA=x
```

must be rejected.

We do not want a partial match.

Therefore:

```python
re.fullmatch()
```

is appropriate.

---

# Boundary Testing

## MODE

```text
read        → VALID
write       → VALID
randread    → VALID
randwrite   → VALID
delete      → INVALID
READ        → INVALID
```

---

## SIZE

```text
1MB         → VALID
1GB         → VALID
1TB         → VALID
1.5TB       → VALID
1PB         → INVALID
1KB         → INVALID
.5TB        → INVALID
```

---

## BLOCK

```text
1KB         → VALID
4KB         → VALID
128KB       → VALID
1.5KB       → INVALID
128MB       → INVALID
```

---

## QUEUE

```text
1           → VALID
8           → VALID
128         → VALID
0           → INVALID
-1          → INVALID
```

---

## Structure

```text
Missing MODE       → INVALID
Missing SIZE       → INVALID
Missing BLOCK      → INVALID
Missing QUEUE      → INVALID
Extra field        → INVALID
Wrong field order  → INVALID
```

---

# Engineering Lesson

This final question combines the validation techniques learned throughout the module.

```text
Requirement
      ↓
Break into components
      ↓
Matching rules
      ↓
Restriction rules
      ↓
Build small regex components
      ↓
Test components
      ↓
Combine components
      ↓
Anchor complete input
      ↓
Use fullmatch()
      ↓
Boundary testing
```

The objective is not to memorize the final regex.

The objective is to be able to derive it from the requirements.

---

# Overall Engineering Lessons from Questions 7–10

The same methodology continues from Questions 1–6.

```text
Requirement
    ↓
Break into components
    ↓
Identify matching rules
    ↓
Identify restriction rules
    ↓
Build small regex components
    ↓
Combine components
    ↓
Test boundary values
    ↓
Test valid cases
    ↓
Test invalid cases
    ↓
Optimize only after understanding
```

---

# Important Validation Patterns

## Alternation

```regex
(A|B)
```

Means:

```text
A OR B
```

---

## Optional Group

```regex
(A)?
```

Means:

```text
A
OR
nothing
```

---

## Non-Capturing Group

```regex
(?:A|B)
```

Used when grouping is required but the matched value does not need to be captured.

---

## Positive Lookahead

```regex
(?=.*PATTERN)
```

Means:

> PATTERN must exist somewhere.

---

## Negative Lookahead

```regex
(?!.*PATTERN)
```

Means:

> PATTERN must not exist anywhere.

---

## Character Classes

```regex
[A-Z]
[a-z]
[0-9]
```

---

## Quantifiers

```regex
\d+
```

One or more digits.

```regex
\d*
```

Zero or more digits.

```regex
\d?
```

Zero or one digit.

```regex
\d{3}
```

Exactly three digits.

---

## Anchors

```regex
^
$
```

Used when validating the complete input.

---

# Validation Progress

| Question | Problem                                      | Status      |
| -------- | -------------------------------------------- | ----------- |
| 1        | Email Validation                             | ✅ Completed |
| 2        | IPv4 Validation                              | ✅ Completed |
| 3        | MAC Address Validation                       | ✅ Completed |
| 4        | Password Validation                          | ✅ Completed |
| 5        | Mobile Number Validation                     | ✅ Completed |
| 6        | Date Validation                              | ✅ Completed |
| 7        | Storage Device Identifier Validation         | ✅ Completed |
| 8        | Storage Capacity Validation                  | ✅ Completed |
| 9        | Firmware Version Validation                  | ✅ Completed|
| 10       | Enterprise Storage Test Parameter Validation | ✅ Completed |

---

# Final Validation Engineering Goal

After completing Questions 1–10, the target skill is:

```text
Validation Requirement
        ↓
Understand the input
        ↓
Break input into components
        ↓
Identify Matching Rules
        ↓
Identify Restriction Rules
        ↓
Build each component independently
        ↓
Test each component
        ↓
Combine components
        ↓
Anchor complete input
        ↓
Select appropriate validation API
        ↓
Test valid cases
        ↓
Test invalid cases
        ↓
Test boundary cases
        ↓
Test near-miss cases
        ↓
Final Validator
```

The goal is not:

> Memorize regex patterns.

The goal is:

> **Design a validator from requirements.**

---

# Final Note

This notebook continues to follow the engineering-diary approach established in Questions 1–6.

Whenever solving a new validation problem:

1. Never start with the regex.
2. Start with the requirements.
3. Convert requirements into rules.
4. Separate matching rules from restriction rules.
5. Build the regex incrementally.
6. Test every step.
7. Analyze failures instead of guessing.
8. Improve the design until all test cases pass.

If this methodology is followed consistently, complex validation problems become manageable, testable, and easier to debug.


