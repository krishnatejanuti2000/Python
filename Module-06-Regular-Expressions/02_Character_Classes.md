# Chapter 02 — Character Classes

---

# 2.1 Why Character Classes?

## Learning Objective

After completing this lesson, you will be able to:

- Understand why Character Classes were introduced.
- Recognize the limitations of matching only literal characters.
- Explain how Character Classes simplify pattern matching.
- Understand how the Regex Engine interprets a Character Class.

---

## Introduction

In the previous chapter, we learned that Regular Expressions are used to match **patterns** instead of fixed values.

However, until now, we have only discussed the idea of pattern matching.

We have not yet learned how to write patterns.

The first building block of every Regular Expression is the **Character Class**.

Character Classes allow us to express that a particular position in a pattern may contain **one of several possible characters**.

---

## The Problem

Suppose we want to match the following drive names.

```text
DriveA
DriveB
DriveC
DriveD
```

One solution is to write four separate patterns.

```text
DriveA

DriveB

DriveC

DriveD
```

Although this works, it quickly becomes inefficient.

Imagine there are 26 possible drive names.

```text
DriveA
DriveB
DriveC
...
DriveZ
```

Writing 26 separate patterns is unnecessary.

There should be a better way.

---

## Another Example

Suppose we want to match any lowercase vowel.

Possible inputs are

```text
a

e

i

o

u
```

Without Character Classes, we would again need multiple separate patterns.

This approach becomes difficult to maintain as the number of possibilities increases.

---

## The Need for Character Classes

Instead of writing many individual patterns,

we want a way to tell the Regex Engine:

> "At this position, accept **any one character from this group**."

This is exactly what Character Classes provide.

They allow multiple possible characters to be represented using a single expression.

---

## Visualizing the Idea

Without Character Classes

```text
DriveA

OR

DriveB

OR

DriveC

OR

DriveD
```

With Character Classes

```text
Drive[ABCD]
```

Instead of four separate patterns,

we now have one compact pattern.

---

## Another Visualization

Without Character Classes

```text
cat

bat

hat

mat
```

With Character Classes

```text
[cbhm]at
```

The first position may contain:

```text
c

b

h

m
```

The remaining characters remain the same.

---

## How the Regex Engine Thinks

Suppose the pattern is

```text
Drive[ABCD]
```

and the input is

```text
DriveC
```

The Regex Engine thinks like this:

```text
Compare

Drive

↓

Matched

↓

Current Character

C

↓

Is C present inside

[A B C D] ?

↓

YES

↓

Match Successful
```

Notice an important point.

The Regex Engine does **not** compare the entire group at once.

It simply checks whether the current character belongs to the allowed set.

---

## Engine Visualization

```
Pattern

Drive[ABCD]

Input

DriveC

--------------------------------------------------

Literal Match

Drive

↓

Current Input Character

C

↓

Allowed Characters

A

B

C

D

↓

Is C inside the allowed set?

        │
   ┌────┴────┐
   │         │
  YES        NO
   │
   ▼
 Continue Matching
```

---

## Why Character Classes are Powerful

Character Classes provide several advantages.

- Reduce repetitive patterns.
- Improve readability.
- Make patterns easier to maintain.
- Allow flexible matching.
- Form the foundation for more advanced Regex patterns.

Almost every non-trivial Regular Expression uses Character Classes.

---

## Real-World Usage

Character Classes are frequently used for:

- Matching alphabets.
- Matching digits.
- Matching hexadecimal values.
- Matching storage device names.
- Matching log levels.
- Matching file extensions.
- Validating identifiers.
- Parsing command output.

As we progress through this chapter, every one of these use cases will become clearer.

---

## Common Beginner Mistakes

### Mistake 1

Thinking a Character Class matches an entire word.

A Character Class matches **exactly one character** at its current position.

---

### Mistake 2

Thinking Character Classes are only shortcuts.

They are much more than shortcuts.

They fundamentally change how the Regex Engine decides whether a character is acceptable.

---

## Interview Questions

1. Why were Character Classes introduced?

2. What problem do Character Classes solve?

3. Does a Character Class match multiple characters?

4. How does the Regex Engine evaluate a Character Class?

---

## Practice Questions

1. Why is writing multiple separate patterns considered inefficient?

2. Explain how Character Classes reduce redundancy.

3. Describe how the Regex Engine processes a Character Class.

4. Give three situations where Character Classes would simplify a Regular Expression.

---

## Revision Box

✔ Character Classes allow one position to accept multiple possible characters.

✔ A Character Class matches **one character**, not multiple characters.

✔ Character Classes reduce repetitive patterns.

✔ The Regex Engine checks whether the current input character belongs to the allowed set.

---

## Key Takeaways

- Character Classes are the first major building block of Regular Expressions.
- They allow multiple possible characters to be represented using one pattern.
- They improve readability and maintainability.
- Understanding Character Classes is essential before learning ranges, predefined classes and quantifiers.

------------------------------------------------------------------------------------------------------------

# 2.2 Square Brackets `[]`

## Learning Objective

After completing this lesson, you will be able to:

- Understand the purpose of square brackets `[]`.
- Write simple Character Classes.
- Explain how the Regex Engine interprets `[]`.
- Predict whether a character matches a Character Class.
- Understand that `[]` always represents a single character position.

---

# Introduction

Square Brackets (`[]`) are used to create a **Character Class**.

A Character Class tells the Regex Engine:

> **"At this position, accept any ONE character from the characters written inside these brackets."**

This is the first real Regex syntax that allows flexible pattern matching.

---

# Why Do We Need Square Brackets?

Suppose we want to match the following words.

```text
cat
bat
hat
mat
```

Without Character Classes, we would need four separate patterns.

```text
cat

bat

hat

mat
```

Instead, we can write one pattern.

```regex
[cbhm]at
```

This single pattern matches all four words.

---

# Definition

A **Character Class** is created using square brackets `[]`.

Everything written inside the brackets represents the **allowed characters** for that position.

Only **one character** is matched from the Character Class.

---

# Syntax

```regex
[characters]
```

General Form

```regex
[ABC]

[abc]

[123]

[xyz]

[ABC123]
```

The Regex Engine treats everything inside the brackets as the set of allowed characters.

---

# How the Regex Engine Thinks

Pattern

```regex
[ABC]
```

Input

```text
B
```

The Regex Engine thinks:

```
Current Pattern

↓

[ABC]

↓

Current Input Character

↓

B

↓

Is B inside

A B C ?

↓

YES

↓

Match Successful
```

Notice that the engine is **not** comparing the entire string.

It only checks the **current input character** against the allowed set.

---

# Engine Visualization

```
Pattern

[ABC]

Input

B

----------------------------------

Regex Engine

↓

Current Character

B

↓

Allowed Characters

A

B

C

↓

Is B present?

      │
 ┌────┴────┐
 │         │
YES       NO
 │
 ▼
MATCH
```

---

# Example 1

Pattern

```regex
[ABC]
```

Input

```text
A
```

Result

```text
✔ Match
```

Reason

```
A exists inside

[ABC]
```

---

# Example 2

Pattern

```regex
[ABC]
```

Input

```text
C
```

Result

```text
✔ Match
```

---

# Example 3

Pattern

```regex
[ABC]
```

Input

```text
D
```

Result

```text
✘ No Match
```

Reason

```
D is not inside

[ABC]
```

---

# Example 4

Pattern

```regex
Drive[AB]
```

Possible Matches

```text
DriveA

DriveB
```

Does Not Match

```text
DriveC
```

---

# Important Rule

A Character Class always matches **exactly ONE character**.

Pattern

```regex
[ABC]
```

Matches

```text
A

B

C
```

It does **NOT** match

```text
AB

ABC

AC
```

Because the Character Class represents only one character position.

---

# Visual Explanation

```
Pattern

Drive[AB]

Input

DriveA

        │
        ▼

Current Character

A

↓

Allowed Set

A

B

↓

A belongs to the set

↓

Continue Matching
```

---

# Common Misconception

Many beginners think

```regex
[ABC]
```

means

```
ABC
```

This is incorrect.

It actually means

```
A

OR

B

OR

C
```

Never think of it as a word.

Always think of it as **one position with multiple possibilities**.

---

# Real-World Usage

Character Classes are used extensively for matching:

Storage Devices

```text
DriveA

DriveB

DriveC
```

Drive Status

```text
GOOD

BAD

WARN
```

Log Levels

```text
INFO

WARN

ERROR
```

File Types

```text
.txt

.log

.cfg
```

As we learn ranges (`[a-z]`, `[0-9]`, etc.), these patterns become even more powerful.

---

# Common Beginner Mistakes

### Mistake 1

Thinking `[]` matches multiple characters.

It matches only **one** character.

---

### Mistake 2

Thinking

```regex
[ABC]
```

means

```text
ABC
```

It actually means

```text
A OR B OR C
```

---

### Mistake 3

Thinking order matters.

The following are identical.

```regex
[ABC]

[CBA]

[BCA]
```

The Regex Engine only checks whether the current character exists in the set.

---

# Interview Questions

1. What is a Character Class?

2. What is the purpose of square brackets?

3. Does `[ABC]` match one character or multiple characters?

4. How does the Regex Engine process `[ABC]`?

5. Is `[ABC]` different from `[CBA]`?

---

# Practice Questions

1. Which of the following match `[ABC]`?

```
A

B

C

D
```

2. Will `[ABC]` match `"AB"`? Explain why.

3. Write a Character Class that matches:

```
X

Y

Z
```

4. Explain why `[ABC]` represents one position instead of three.

---

# Revision Box

✔ `[]` creates a Character Class.

✔ A Character Class represents one position.

✔ Only one character is matched.

✔ `[ABC]` means `A OR B OR C`.

✔ Order inside `[]` does not matter.

---

# Key Takeaways

- Square Brackets are used to create Character Classes.
- Character Classes simplify pattern matching by allowing multiple possible characters at a single position.
- The Regex Engine checks whether the current input character belongs to the allowed set.
- Understanding `[]` is the foundation for learning ranges like `[a-z]`, `[0-9]`, and predefined classes such as `\d` and `\w`.

------------------------------------------------------------------------------------------------------------

# 2.3 Character Ranges

## Learning Objective

After completing this lesson, you will be able to:

- Understand why Character Ranges were introduced.
- Explain the purpose of the hyphen (`-`) inside a Character Class.
- Understand how Character Ranges simplify Regular Expressions.
- Explain how the Regex Engine interprets a Character Range.
- Differentiate between listing characters individually and using a range.

---

# Introduction

In the previous lesson, we learned that square brackets (`[]`) allow us to specify multiple possible characters at a single position.

For example,

```regex
[ABC]
```

means

```
A OR B OR C
```

This works well for a small number of characters.

But what happens when we want to match all lowercase letters?

Would we write

```regex
[abcdefghijklmnopqrstuvwxyz]
```

Technically, yes.

Practically, no.

It is difficult to read, easy to make mistakes, and harder to maintain.

Regex provides a much simpler solution.

That solution is called a **Character Range**.

---

# The Problem

Suppose we want to match any lowercase letter.

One approach is

```regex
[abcdefghijklmnopqrstuvwxyz]
```

Although correct,

this pattern is:

- Very long
- Difficult to read
- Easy to mistype
- Hard to maintain

There should be a shorter and clearer way.

---

# The Solution

Regex allows consecutive characters to be represented as a range.

Instead of writing

```regex
[abcdefghijklmnopqrstuvwxyz]
```

we write

```regex
[a-z]
```

Both represent exactly the same set of characters.

The second version is much shorter and easier to understand.

---

# What is a Character Range?

A **Character Range** represents a sequence of consecutive characters inside a Character Class.

It is written using the hyphen (`-`) between the starting and ending characters.

General syntax:

```regex
[start-end]
```

Examples:

```regex
[a-z]

[A-Z]

[0-9]
```

---

# Understanding the Hyphen (`-`)

Inside a Character Class, the hyphen does **not** mean subtraction.

Instead, it means

> "Include every character from the starting character to the ending character."

For example,

```regex
[a-z]
```

means

```
a
b
c
d
e
...
z
```

The Regex Engine expands this range internally.

---

# How the Regex Engine Thinks

Pattern

```regex
[a-z]
```

Input

```text
g
```

The Regex Engine performs the following logic:

```
Current Character

↓

g

↓

Allowed Range

a → z

↓

Does g fall within this range?

↓

YES

↓

Match Successful
```

Notice that the engine is checking **membership within a range**, not comparing against every letter individually.

---

# Engine Visualization

```
Pattern

[a-z]

↓

Current Input Character

g

↓

Allowed Range

a ---------------------- z

          ↑
          │
          g

↓

g lies within the allowed range

↓

MATCH
```

---

# Example 1

Pattern

```regex
[a-z]
```

Input

```text
m
```

Result

```
✔ Match
```

Reason

```
m lies between a and z.
```

---

# Example 2

Pattern

```regex
[a-z]
```

Input

```text
Z
```

Result

```
✘ No Match
```

Reason

Uppercase letters are not part of the lowercase range.

---

# Example 3

Pattern

```regex
[a-z]
```

Input

```text
5
```

Result

```
✘ No Match
```

Digits are outside the specified range.

---

# Why Character Ranges are Better

Instead of

```regex
[abcdefghijklmnopqrstuvwxyz]
```

we simply write

```regex
[a-z]
```

Advantages:

- Shorter
- Easier to read
- Easier to maintain
- Less chance of typing mistakes
- Widely used in professional Regular Expressions

---

# Real-World Usage

Character Ranges are commonly used for:

- Lowercase letters
- Uppercase letters
- Digits
- File names
- Usernames
- Hostnames
- Storage identifiers
- Log parsing

They are one of the most frequently used Regex features.

---

# Important Observation

A Character Range is still a **Character Class**.

It still matches **only one character**.

The only difference is that the allowed characters are represented using a compact range notation.

---

# Common Beginner Mistakes

### Mistake 1

Thinking

```regex
[a-z]
```

matches a complete word.

It matches only **one lowercase character**.

---

### Mistake 2

Thinking the hyphen means subtraction.

Inside a Character Class,

the hyphen represents a range.

---

### Mistake 3

Thinking

```regex
[a-z]
```

matches uppercase letters.

It does not.

Uppercase letters require a different range.

---

# Interview Questions

1. Why were Character Ranges introduced?

2. What does the hyphen (`-`) represent inside a Character Class?

3. Is `[a-z]` different from listing every lowercase letter individually?

4. Does `[a-z]` match a complete word?

---

# Practice Questions

1. Rewrite the following using a Character Range:

```regex
[abcdefghijklmnopqrstuvwxyz]
```

2. Will `[a-z]` match the following?

```
a
k
z
A
5
```

Explain your answer.

3. Why are Character Ranges preferred in professional Regex patterns?

---

# Revision Box

✔ Character Ranges simplify large Character Classes.

✔ The hyphen (`-`) represents a range of consecutive characters.

✔ `[a-z]` is equivalent to listing every lowercase letter individually.

✔ A Character Range still matches only **one** character.

---

# Key Takeaways

- Character Ranges are a compact way to represent consecutive characters.
- They improve readability and maintainability.
- The Regex Engine checks whether the current character lies within the specified range.
- Character Ranges form the basis for patterns such as `[a-z]`, `[A-Z]`, and `[0-9]`.

-----------------------------------------------------------------------------------------------------------

# 2.4 Lowercase Character Range `[a-z]`

## Learning Objective

After completing this lesson, you will be able to:

- Understand what `[a-z]` represents.
- Explain how the Regex Engine interprets `[a-z]`.
- Predict which characters match and which do not.
- Use `[a-z]` in practical Regular Expressions.
- Understand why `[a-z]` is one of the most frequently used Character Classes.

---

# Introduction

In the previous lesson, we learned about Character Ranges.

Now we study the first and most commonly used range:

```regex
[a-z]
```

This Character Class is used whenever we need to match **any one lowercase English alphabet**.

It is one of the most fundamental building blocks of Regular Expressions.

---

# Why Do We Need `[a-z]`?

Suppose we want to match any lowercase letter.

One approach is

```regex
[abcdefghijklmnopqrstuvwxyz]
```

Although correct,

it is unnecessarily long.

Regex provides a compact representation.

```regex
[a-z]
```

Both patterns are identical.

The second one is shorter, easier to read and easier to maintain.

---

# Definition

```regex
[a-z]
```

matches **exactly one lowercase English alphabet**.

The allowed characters are

```text
a b c d e f g h i j k l m
n o p q r s t u v w x y z
```

Nothing else is allowed.

---

# Syntax

```regex
[a-z]
```

General Meaning

```
Match any ONE lowercase letter
```

---

# How the Regex Engine Thinks

Pattern

```regex
[a-z]
```

Input

```text
k
```

Regex Engine

```text
Current Pattern

[a-z]

↓

Current Input Character

k

↓

Allowed Range

a ---------------------- z

↓

Does 'k' lie between 'a' and 'z'?

↓

YES

↓

MATCH
```

Notice that the Regex Engine is **not comparing against all 26 letters individually**.

It simply checks whether the current character belongs to the specified range.

---

# Engine Visualization

```
                 Pattern

                 [a-z]

                    │
                    ▼

          Current Character

                   k

                    │
                    ▼

        a -------------------- z
                ▲
                │
                k

                    │
                    ▼

               ✔ MATCH
```

---

# Example 1

Pattern

```regex
[a-z]
```

Input

```text
a
```

Result

```text
✔ Match
```

Reason

```
'a' belongs to the lowercase range.
```

---

# Example 2

Pattern

```regex
[a-z]
```

Input

```text
m
```

Result

```text
✔ Match
```

---

# Example 3

Pattern

```regex
[a-z]
```

Input

```text
z
```

Result

```text
✔ Match
```

---

# Example 4

Pattern

```regex
[a-z]
```

Input

```text
A
```

Result

```text
✘ No Match
```

Reason

Uppercase letters are outside the specified range.

---

# Example 5

Pattern

```regex
[a-z]
```

Input

```text
7
```

Result

```text
✘ No Match
```

Reason

Digits are not lowercase letters.

---

# Example 6

Pattern

```regex
[a-z]
```

Input

```text
@
```

Result

```text
✘ No Match
```

Reason

Special characters are not part of the range.

---

# Engine Trace

Pattern

```regex
[a-z]
```

Input

```text
g
```

```
Regex Engine Trace

----------------------------------------

Current Pattern Token

[a-z]

Current Input Character

g

Allowed Range

a → z

Decision

Does 'g' belong to the range?

YES

Action

Move to next pattern token.
```

---

# Important Observation

`[a-z]`

does **not** mean

```
abcdefghijklmnopqrstuvwxyz
```

It means

```
Choose ONE character

from

a to z
```

One position.

One character.

Never multiple characters.

---

# Real-World Usage

Lowercase ranges are frequently used for:

### Usernames

```
john

alex

smith
```

---

### Linux User Accounts

```
root

daemon

ubuntu
```

---

### Hostnames

```
server

storage

backup
```

---

### Storage Labels

```
diska

diskb

cache
```

---

### Configuration Keys

```
host

port

device

health
```

---

# Common Beginner Mistakes

## Mistake 1

Thinking

```regex
[a-z]
```

matches

```
apple
```

Wrong.

It matches only

```
a
```

then

```
p
```

then

```
p
```

...

Each character is matched individually.

---

## Mistake 2

Thinking uppercase letters are included.

They are not.

```
A

B

C
```

will not match.

---

## Mistake 3

Thinking digits belong to the range.

They do not.

```
0

5

9
```

are outside

```
[a-z]
```

---

# Interview Questions

1. What does `[a-z]` represent?

2. Does `[a-z]` match a complete word?

3. How does the Regex Engine evaluate `[a-z]`?

4. Why is `[a-z]` preferred over listing all lowercase letters individually?

5. Will `[a-z]` match digits? Explain.

---

# Practice Questions

## Question 1

Will `[a-z]` match?

```
a

m

z

A

9

@
```

Explain each answer.

---

## Question 2

Why is

```regex
[a-z]
```

considered better than

```regex
[abcdefghijklmnopqrstuvwxyz]
```

---

## Question 3

Explain, in your own words, how the Regex Engine processes `[a-z]`.

---

# Revision Box

✔ `[a-z]` matches one lowercase English letter.

✔ It is a Character Range.

✔ It matches exactly one character.

✔ Uppercase letters do not match.

✔ Digits do not match.

✔ Special characters do not match.

✔ The Regex Engine checks whether the current character lies between `a` and `z`.

---

# Key Takeaways

- `[a-z]` is one of the most commonly used Character Classes.
- It provides a compact way to represent all lowercase English letters.
- The Regex Engine evaluates whether the current character belongs to the specified range.
- `[a-z]` always matches **one lowercase character**, never an entire word.

-----------------------------------------------------------------------------------------------------------

# 2.5 Uppercase Character Range `[A-Z]`

## Learning Objective

After completing this lesson, you will be able to:

- Understand what `[A-Z]` represents.
- Explain how `[A-Z]` differs from `[a-z]`.
- Predict which characters match `[A-Z]`.
- Understand how the Regex Engine evaluates uppercase ranges.
- Use `[A-Z]` in practical Regular Expressions.

---

# Introduction

In the previous lesson, we learned about the lowercase character range.

```regex
[a-z]
```

which matches any one lowercase English alphabet.

Sometimes, however, we need to match uppercase letters instead.

Examples include:

```text
A

B

C

X

Y

Z
```

For these situations, Regular Expressions provide the uppercase range.

```regex
[A-Z]
```

---

# Why Do We Need `[A-Z]`?

Suppose we want to match any uppercase alphabet.

Without Character Ranges, we would write

```regex
[ABCDEFGHIJKLMNOPQRSTUVWXYZ]
```

Although correct,

this is unnecessarily long.

Regex provides a compact alternative.

```regex
[A-Z]
```

Both expressions represent exactly the same set of characters.

---

# Definition

```regex
[A-Z]
```

matches **exactly one uppercase English alphabet**.

Allowed characters are

```text
A B C D E F G H I J K L M
N O P Q R S T U V W X Y Z
```

Nothing else is included.

---

# Syntax

```regex
[A-Z]
```

Meaning

```
Match any ONE uppercase English letter.
```

---

# How the Regex Engine Thinks

Pattern

```regex
[A-Z]
```

Input

```text
R
```

Regex Engine

```
Current Pattern

↓

[A-Z]

↓

Current Input Character

↓

R

↓

Allowed Range

A ---------------------- Z

↓

Does 'R' lie within this range?

↓

YES

↓

MATCH
```

---

# Engine Visualization

```
               Pattern

               [A-Z]

                  │
                  ▼

          Current Character

                  R

                  │
                  ▼

      A ---------------------- Z
                 ▲
                 │
                 R

                  │
                  ▼

             ✔ MATCH
```

---

# Matching Matrix

| Input | Match | Reason |
|------|:-----:|--------|
| `A` | ✅ | Uppercase letter |
| `M` | ✅ | Uppercase letter |
| `Z` | ✅ | Uppercase letter |
| `a` | ❌ | Lowercase letter |
| `5` | ❌ | Digit |
| `@` | ❌ | Special character |
| `_` | ❌ | Not in the range |

---

# Engine Trace

Pattern

```regex
[A-Z]
```

Input

```text
G
```

```
Regex Engine Trace

-------------------------------------

Current Pattern Token

[A-Z]

Current Input Character

G

Allowed Range

A → Z

Decision

Is G inside A-Z?

YES

Action

Move to the next pattern token.
```

---

# Comparing `[a-z]` and `[A-Z]`

| Pattern | Matches |
|---------|---------|
| `[a-z]` | Lowercase letters |
| `[A-Z]` | Uppercase letters |

Examples

| Input | `[a-z]` | `[A-Z]` |
|------|:-------:|:-------:|
| `a` | ✅ | ❌ |
| `A` | ❌ | ✅ |
| `m` | ✅ | ❌ |
| `M` | ❌ | ✅ |
| `5` | ❌ | ❌ |

---

# Real-World Usage

Uppercase ranges are commonly used for:

### Drive Letters

```text
C:

D:

E:
```

---

### Storage Device Codes

```text
NVME

SSD

SAS
```

---

### Country Codes

```text
IN

US

UK
```

---

### Log Levels

```text
INFO

ERROR

WARN
```

---

### Product Codes

```text
ABC123

XYZ789
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking `[A-Z]` also matches lowercase letters.

It does not.

---

### Mistake 2

Thinking `[A-Z]` matches an entire uppercase word.

It matches **only one uppercase character**.

---

### Mistake 3

Thinking digits belong to the range.

They do not.

---

# Interview Questions

1. What does `[A-Z]` represent?

2. How does `[A-Z]` differ from `[a-z]`?

3. Does `[A-Z]` match `"HELLO"`?

4. Explain how the Regex Engine evaluates `[A-Z]`.

---

# Practice Questions

1. Which of the following match `[A-Z]`?

```
A

M

Z

a

9

@
```

Explain your answer.

---

2. Why is

```regex
[A-Z]
```

better than

```regex
[ABCDEFGHIJKLMNOPQRSTUVWXYZ]
```

---

# Revision Box

✔ `[A-Z]` matches one uppercase English letter.

✔ It is a Character Range.

✔ It matches exactly one character.

✔ Lowercase letters do not match.

✔ Digits do not match.

✔ The Regex Engine checks whether the current character lies between `A` and `Z`.

---

# Key Takeaways

- `[A-Z]` is the uppercase counterpart of `[a-z]`.
- It provides a compact representation of all uppercase English letters.
- The Regex Engine evaluates whether the current character belongs to the specified range.
- `[A-Z]` always matches **one uppercase character**, never an entire word.

-----------------------------------------------------------------------------------------------------------

# 2.6 Numeric Character Range `[0-9]`

## Learning Objective

After completing this lesson, you will be able to:

- Understand what `[0-9]` represents.
- Explain how the Regex Engine interprets numeric ranges.
- Distinguish between `[0-9]` and multiple literal digits.
- Use `[0-9]` in practical automation tasks.
- Prepare for the upcoming predefined character class `\d`.

---

# Introduction

In the previous lessons, we learned how Character Ranges can represent groups of alphabets.

Examples:

```regex
[a-z]

[A-Z]
```

Now we move to another extremely important range:

```regex
[0-9]
```

This Character Range matches **exactly one numeric digit**.

Numbers appear everywhere in software systems, making `[0-9]` one of the most frequently used Character Classes.

---

# Why Do We Need `[0-9]`?

Suppose we want to match any digit.

Without Character Ranges, we would have to write

```regex
[0123456789]
```

Although correct,

this pattern is unnecessarily long.

Regex provides a compact representation.

```regex
[0-9]
```

Both expressions are identical.

The second version is much cleaner and easier to maintain.

---

# Definition

```regex
[0-9]
```

matches **exactly one numeric digit**.

Allowed characters are

```text
0 1 2 3 4 5 6 7 8 9
```

Nothing else is included.

---

# Syntax

```regex
[0-9]
```

Meaning

```
Match any ONE numeric digit.
```

---

# How the Regex Engine Thinks

Pattern

```regex
[0-9]
```

Input

```text
7
```

Regex Engine

```text
Current Pattern

↓

[0-9]

↓

Current Input Character

↓

7

↓

Allowed Range

0 ---------------------- 9

↓

Does '7' lie within this range?

↓

YES

↓

MATCH
```

Notice that the Regex Engine is checking whether the current character belongs to the numeric range.

It is **not** trying to match multiple digits.

---

# Engine Visualization

```
                 Pattern

                 [0-9]

                    │
                    ▼

          Current Character

                    7

                    │
                    ▼

        0 -------------------- 9
                ▲
                │
                7

                    │
                    ▼

               ✔ MATCH
```

---

# Matching Matrix

| Input | Match | Reason |
|------|:-----:|--------|
| `0` | ✅ | Numeric digit |
| `4` | ✅ | Numeric digit |
| `9` | ✅ | Numeric digit |
| `a` | ❌ | Alphabet |
| `A` | ❌ | Uppercase letter |
| `@` | ❌ | Special character |
| `_` | ❌ | Underscore |

---

# Engine Trace

Pattern

```regex
[0-9]
```

Input

```text
5
```

```
Regex Engine Trace

--------------------------------------

Current Pattern Token

[0-9]

Current Input Character

5

Allowed Range

0 → 9

Decision

Does '5' belong to the range?

YES

Action

Move to the next pattern token.
```

---

# Important Observation

Many beginners think

```regex
[0-9]
```

means

```
0123456789
```

This is incorrect.

It actually means

```
0

OR

1

OR

2

...

OR

9
```

Only **one** digit is matched.

---

# Another Important Observation

Pattern

```regex
[0-9]
```

Input

```text
512
```

The Character Class does **not** match the complete number.

The Regex Engine processes one character at a time.

```
5

↓

1

↓

2
```

Each digit is matched individually.

Later, we will learn how **Quantifiers** allow us to match multiple consecutive digits.

---

# Real-World Usage

`[0-9]` is commonly used for matching:

### Capacity

```text
512GB

1024GB

2048GB
```

---

### Temperature

```text
42C

38C

55C
```

---

### Port Numbers

```text
22

80

443

8080
```

---

### Error Codes

```text
404

500

200
```

---

### Device IDs

```text
NVME001

NVME045

SSD123
```

---

# Comparison with Previous Character Ranges

| Pattern | Matches |
|---------|----------|
| `[a-z]` | Lowercase letters |
| `[A-Z]` | Uppercase letters |
| `[0-9]` | Numeric digits |

---

# Common Beginner Mistakes

### Mistake 1

Thinking `[0-9]` matches complete numbers.

It matches only **one digit**.

---

### Mistake 2

Thinking letters also belong to the range.

They do not.

---

### Mistake 3

Confusing `[0-9]` with `\d`.

At first glance they appear similar.

Later in this chapter, we will study `\d` and compare both patterns in detail.

---

# Interview Questions

1. What does `[0-9]` represent?

2. Does `[0-9]` match `"512"`?

3. How does the Regex Engine process `[0-9]`?

4. Why is `[0-9]` preferred over `[0123456789]`?

---

# Practice Questions

1. Which of the following match `[0-9]`?

```
0

5

9

A

m

@
```

Explain your answer.

---

2. Why does `[0-9]` not match `"2048"` as a single unit?

---

3. Give five real-world examples where `[0-9]` is useful.

---

# Revision Box

✔ `[0-9]` matches one numeric digit.

✔ It is a Character Range.

✔ It matches exactly one character.

✔ Letters do not match.

✔ Special characters do not match.

✔ Multiple digits require Quantifiers, which are covered later.

---

# Key Takeaways

- `[0-9]` represents any one numeric digit.
- The Regex Engine evaluates one input character at a time.
- `[0-9]` is heavily used in automation for capacities, temperatures, IDs, ports and error codes.
- Matching complete numbers requires combining `[0-9]` with Quantifiers, which will be introduced in Chapter 03.

---
-----------------------------------------------------------------------------------------------------------
# 2.7 Alphabet Character Range `[A-Za-z]`

## Learning Objective

After completing this lesson, you will be able to:

- Understand what `[A-Za-z]` represents.
- Explain why multiple Character Ranges can be combined.
- Understand how the Regex Engine evaluates combined Character Ranges.
- Predict which characters match and which do not.
- Use `[A-Za-z]` in practical Regular Expressions.

---

# Introduction

In the previous lessons, we studied individual Character Ranges.

Lowercase letters

```regex
[a-z]
```

Uppercase letters

```regex
[A-Z]
```

Many real-world applications require matching **any alphabet**, regardless of its case.

Examples include:

```text
A

b

M

x

Z

q
```

Instead of writing separate Regular Expressions for uppercase and lowercase letters, Regex allows us to combine both Character Ranges into a single Character Class.

```regex
[A-Za-z]
```

---

# Why Do We Need `[A-Za-z]`?

Suppose we want to match any English alphabet.

One approach would be to write two separate patterns.

```regex
[a-z]

OR

[A-Z]
```

This quickly becomes inconvenient.

Regex allows both Character Ranges to be combined into a single Character Class.

```regex
[A-Za-z]
```

Now both uppercase and lowercase letters are accepted.

---

# Definition

```regex
[A-Za-z]
```

matches **exactly one English alphabet**, regardless of whether it is uppercase or lowercase.

Allowed characters include

```text
A B C ... Z

a b c ... z
```

Digits, spaces and special characters are **not** included.

---

# Syntax

```regex
[A-Za-z]
```

Meaning

```
Match any ONE English alphabet.
```

---

# How the Regex Engine Thinks

Pattern

```regex
[A-Za-z]
```

Input

```text
G
```

Regex Engine

```text
Current Pattern

↓

[A-Za-z]

↓

Current Input Character

↓

G

↓

Check First Range

A → Z

↓

Does G belong?

↓

YES

↓

MATCH
```

---

Input

```text
m
```

Regex Engine

```text
Current Pattern

↓

[A-Za-z]

↓

Current Character

↓

m

↓

Check First Range

A → Z

↓

NO

↓

Check Second Range

a → z

↓

YES

↓

MATCH
```

Notice that the Regex Engine checks whether the current character belongs to **any one of the allowed ranges**.

---

# Engine Visualization

```
Pattern

[A-Za-z]

↓

Allowed Character Sets

A ---------------- Z

a ---------------- z

↓

Current Character

m

↓

Does 'm' belong to either range?

        │
   ┌────┴────┐
   │         │
  YES        NO
   │
   ▼
MATCH
```

---

# Matching Matrix

| Input | Match | Reason |
|------|:-----:|--------|
| `A` | ✅ | Uppercase alphabet |
| `M` | ✅ | Uppercase alphabet |
| `Z` | ✅ | Uppercase alphabet |
| `a` | ✅ | Lowercase alphabet |
| `k` | ✅ | Lowercase alphabet |
| `z` | ✅ | Lowercase alphabet |
| `5` | ❌ | Digit |
| `@` | ❌ | Special character |
| `_` | ❌ | Underscore |
| ` ` (space) | ❌ | Space |

---

# Engine Trace

Pattern

```regex
[A-Za-z]
```

Input

```text
t
```

```
Regex Engine Trace

--------------------------------------

Current Pattern Token

[A-Za-z]

Current Input Character

t

First Range

A → Z

Result

NO

Second Range

a → z

Result

YES

Action

Move to the next pattern token.
```

---

# Real-World Usage

`[A-Za-z]` is commonly used for matching:

### Person Names

```text
John

Alice

David
```

---

### Hostnames

```text
server

storage

backup
```

---

### Device Labels

```text
Disk

Cache

Controller
```

---

### Configuration Keys

```text
host

device

status
```

---

### Log Levels

```text
INFO

Error

Warning
```

---

# Comparison

| Pattern | Matches |
|---------|----------|
| `[a-z]` | Lowercase letters only |
| `[A-Z]` | Uppercase letters only |
| `[A-Za-z]` | Both uppercase and lowercase letters |

---

# Important Observation

`[A-Za-z]`

does **not** match

```text
Storage123
```

It only matches the alphabetic characters individually.

```
S

t

o

r

a

g

e
```

The digits are not matched by this Character Class.

---

# Common Beginner Mistakes

### Mistake 1

Thinking `[A-Za-z]` matches words.

It matches **one alphabetic character at a time**.

---

### Mistake 2

Thinking digits are included.

They are not.

---

### Mistake 3

Thinking spaces are included.

They are not.

---

# Interview Questions

1. What does `[A-Za-z]` represent?

2. How does `[A-Za-z]` differ from `[a-z]`?

3. Does `[A-Za-z]` match `"Python"` as a single unit?

4. Explain how the Regex Engine evaluates `[A-Za-z]`.

---

# Practice Questions

1. Which of the following match `[A-Za-z]`?

```
A

z

M

k

5

@

_
```

Explain your answer.

---

2. Why is `[A-Za-z]` preferred over writing separate Regular Expressions for uppercase and lowercase letters?

---

3. Explain how the Regex Engine processes `[A-Za-z]`.

---

# Coming Up

So far, we have learned how to match:

- Lowercase letters
- Uppercase letters
- Digits
- Any alphabet

The next lesson introduces one of the most important Character Classes in Regex:

```regex
[^]
```

which allows us to match characters by **excluding** specific characters instead of including them.

---

# Revision Box

✔ `[A-Za-z]` matches one English alphabet.

✔ It combines uppercase and lowercase Character Ranges.

✔ Digits are not included.

✔ Spaces are not included.

✔ Special characters are not included.

✔ The Regex Engine checks both Character Ranges before deciding.

---

# Key Takeaways

- `[A-Za-z]` combines two Character Ranges into one Character Class.
- It matches exactly one alphabetic character.
- It is commonly used when letter case does not matter.
- The Regex Engine checks whether the current character belongs to either the uppercase or lowercase range.

-----------------------------------------------------------------------------------------------------------

# 2.8 Negated Character Classes `[^]`

## Learning Objective

After completing this lesson, you will be able to:

- Understand what a negated Character Class is.
- Explain the purpose of `^` inside square brackets.
- Differentiate between including and excluding characters.
- Understand how the Regex Engine evaluates a negated Character Class.
- Predict which characters match and which do not.

---

# Introduction

So far, every Character Class we have learned specifies the characters that are **allowed**.

Examples

```regex
[a-z]

[A-Z]

[0-9]

[A-Za-z]
```

These patterns tell the Regex Engine

> Match **one character that belongs to this set.**

Sometimes, however, the problem is easier to describe by specifying the characters that are **not allowed**.

For these situations, Regex provides the **negated Character Class**.

---

# The Problem

Suppose we want to match every character **except digits**.

One approach would be to list every possible non-digit character.

This is practically impossible because there are thousands of possible characters.

Instead,

Regex lets us describe the opposite.

```
Match anything

EXCEPT

digits.
```

---

# The Solution

A caret (`^`) placed **immediately after the opening square bracket** changes the meaning of the Character Class.

Instead of

```
Include these characters
```

it becomes

```
Exclude these characters
```

General syntax

```regex
[^characters]
```

---

# Definition

A **Negated Character Class** matches **exactly one character that does NOT belong to the specified Character Class.**

The caret (`^`) must appear immediately after the opening square bracket.

Example

```regex
[^0-9]
```

Meaning

```
Match one character

that is NOT

a digit.
```

---

# Understanding the Caret (`^`)

This is one of the most common beginner confusions.

Notice these two patterns.

```regex
[a-z]
```

Meaning

```
Allow

a-z
```

Now

```regex
[^a-z]
```

Meaning

```
Reject

a-z

Match everything else.
```

Adding the caret completely reverses the meaning of the Character Class.

---

# How the Regex Engine Thinks

Pattern

```regex
[^0-9]
```

Input

```text
A
```

Regex Engine

```text
Current Pattern

↓

[^0-9]

↓

Current Input Character

↓

A

↓

Is A inside

0 → 9 ?

↓

NO

↓

Since it is NOT inside the excluded range,

↓

MATCH
```

Notice something important.

The Regex Engine first checks whether the character belongs to the excluded set.

If it does,

the match fails.

If it does not,

the match succeeds.

---

# Engine Visualization

```
Pattern

[^0-9]

↓

Excluded Range

0 ---------------------- 9

↓

Current Character

A

↓

Does A belong to the excluded range?

        │
   ┌────┴────┐
   │         │
  YES        NO
   │         │
   ▼         ▼
 NO MATCH   MATCH
```

---

# Matching Matrix

| Pattern | Input | Match | Reason |
|---------|:-----:|:-----:|--------|
| `[^0-9]` | `A` | ✅ | Not a digit |
| `[^0-9]` | `@` | ✅ | Not a digit |
| `[^0-9]` | `_` | ✅ | Not a digit |
| `[^0-9]` | `5` | ❌ | Digit is excluded |
| `[^0-9]` | `0` | ❌ | Digit is excluded |

---

# Example 1

Pattern

```regex
[^A-Z]
```

Matches

```text
a

7

@

_
```

Does NOT match

```text
A

B

Z
```

---

# Example 2

Pattern

```regex
[^a-z]
```

Matches

```text
A

5

@

_
```

Does NOT match

```text
a

m

z
```

---

# Example 3

Pattern

```regex
[^A-Za-z]
```

Matches

```text
5

@

_

#
```

Does NOT match

```text
A

m

Z
```

---

# Engine Trace

Pattern

```regex
[^A-Z]
```

Input

```text
k
```

```
Regex Engine Trace

----------------------------------------

Current Pattern Token

[^A-Z]

Current Input Character

k

Excluded Range

A → Z

Decision

Does 'k' belong to the excluded range?

NO

Action

Character is accepted.

Move to the next pattern token.
```

---

# Important Rule

The caret (`^`) has this meaning **only when it appears immediately after the opening square bracket.**

Example

```regex
[^0-9]
```

Here,

`^` means

```
NOT
```

We will later learn that the same symbol has a completely different meaning outside Character Classes.

Its meaning depends on its position.

---

# Real-World Usage

Negated Character Classes are commonly used for:

- Ignoring digits
- Removing punctuation
- Extracting words
- Splitting text
- Cleaning log files
- Parsing configuration files
- Data preprocessing

---

# Common Beginner Mistakes

### Mistake 1

Thinking

```regex
[^0-9]
```

matches numbers.

It actually matches everything **except** numbers.

---

### Mistake 2

Forgetting that `^` must appear immediately after `[`.

Only then does it negate the Character Class.

---

### Mistake 3

Thinking `[^A-Za-z]` matches words.

It matches **one non-alphabetic character**.

---

# Interview Questions

1. What is a negated Character Class?

2. What is the purpose of `^` inside `[]`?

3. How does `[^0-9]` differ from `[0-9]`?

4. Explain how the Regex Engine processes a negated Character Class.

---

# Practice Questions

1. Which of the following match `[^a-z]`?

```
A

5

@

m

z
```

Explain each answer.

---

2. Write a Character Class that matches everything except uppercase letters.

---

3. Explain why `[^0-9]` is useful in text processing.

---

# Coming Up

So far we have manually written Character Ranges.

Regex also provides built-in Character Classes that make patterns even shorter.

Instead of writing

```regex
[0-9]
```

we can simply write

```regex
\d
```

The next lesson introduces the first predefined Character Class.

---

# Revision Box

✔ `^` inside `[]` creates a negated Character Class.

✔ A negated Character Class matches one character that is **not** in the specified set.

✔ `[^0-9]` matches any non-digit character.

✔ Position matters—`^` must appear immediately after `[`.

✔ The Regex Engine accepts characters that are outside the excluded set.

---

# Key Takeaways

- Negated Character Classes reverse the meaning of a Character Class.
- They are useful when it is easier to describe what should be excluded rather than included.
- The Regex Engine first checks whether the current character belongs to the excluded set before deciding whether to match.
- Negated Character Classes are widely used in log parsing, validation, and text preprocessing.

-----------------------------------------------------------------------------------------------------------

# 2.9 Predefined Character Class `\d`

## Learning Objective

After completing this lesson, you will be able to:

- Understand what `\d` represents.
- Explain why predefined Character Classes exist.
- Compare `\d` with `[0-9]`.
- Understand how the Regex Engine interprets `\d`.
- Use `\d` in practical Regular Expressions.

---

# Introduction

In the previous lesson, we learned that

```regex
[0-9]
```

matches any one numeric digit.

Although this works perfectly, it is not the shortest way to express this idea.

Since matching digits is an extremely common operation, Regular Expressions provide a predefined Character Class.

```regex
\d
```

Instead of writing

```regex
[0-9]
```

we can simply write

```regex
\d
```

Both patterns represent the same concept in most regular expression engines.

---

# Why Do We Need `\d`?

Suppose we want to match a digit.

We can write

```regex
[0-9]
```

or

```regex
\d
```

Both perform the same task.

The second version is shorter, cleaner and easier to read.

For this reason, professional Regular Expressions often use `\d` instead of `[0-9]`.

---

# Definition

```regex
\d
```

matches **exactly one numeric digit**.

Equivalent Character Range

```regex
[0-9]
```

Allowed characters

```text
0 1 2 3 4 5 6 7 8 9
```

---

# Syntax

```regex
\d
```

Meaning

```
Match any ONE digit.
```

---

# How the Regex Engine Thinks

Pattern

```regex
\d
```

Input

```text
7
```

Regex Engine

```text
Current Pattern

↓

\d

↓

Current Input Character

↓

7

↓

Is 7 a digit?

↓

YES

↓

MATCH
```

Notice that the Regex Engine does not literally expand `\d` into `[0-9]`.

Instead, it recognizes `\d` as a predefined Character Class representing digits.

---

# Engine Visualization

```
Pattern

\d

↓

Current Character

7

↓

Is the character a digit?

        │
   ┌────┴────┐
   │         │
  YES        NO
   │
   ▼
 MATCH
```

---

# Matching Matrix

| Input | Match | Reason |
|------|:-----:|--------|
| `0` | ✅ | Digit |
| `5` | ✅ | Digit |
| `9` | ✅ | Digit |
| `A` | ❌ | Uppercase letter |
| `m` | ❌ | Lowercase letter |
| `@` | ❌ | Special character |
| `_` | ❌ | Underscore |
| Space | ❌ | Not a digit |

---

# Engine Trace

Pattern

```regex
\d
```

Input

```text
4
```

```
Regex Engine Trace

--------------------------------------

Current Pattern Token

\d

Current Input Character

4

Decision

Is '4' a digit?

YES

Action

Move to the next pattern token.
```

---

# Comparing `[0-9]` and `\d`

| Feature | `[0-9]` | `\d` |
|---------|:-------:|:----:|
| Matches digits | ✅ | ✅ |
| Matches one character | ✅ | ✅ |
| Easier to type | ❌ | ✅ |
| Easier to read | ❌ | ✅ |
| Commonly used in production Regex | ✅ | ✅ |

---

# Important Observation

Pattern

```regex
\d
```

Input

```text
512
```

The Regex Engine processes the input one character at a time.

```
5

↓

1

↓

2
```

`\d` matches **one digit** at each position.

It does **not** match the complete number.

To match multiple consecutive digits, Quantifiers are required.

---

# Real-World Usage

`\d` is commonly used for matching:

### Storage Capacities

```text
512GB

2048GB

8192GB
```

---

### Temperatures

```text
42C

38C

55C
```

---

### Port Numbers

```text
22

80

443

8080
```

---

### Process IDs

```text
1024

2256

4098
```

---

### Error Codes

```text
404

500

200
```

---

# Edge Cases

Pattern

```regex
\d
```

Input

```text
12
```

Result

The first `\d` matches only

```text
1
```

The second digit requires another `\d` or a Quantifier.

---

Pattern

```regex
\d
```

Input

```text
A5
```

The first character does not match.

The Regex Engine continues searching until it finds

```text
5
```

which matches.

---

# Common Beginner Mistakes

### Mistake 1

Thinking `\d` matches complete numbers.

It matches only one digit.

---

### Mistake 2

Thinking `\d` is different from `[0-9]`.

For the purpose of this course, treat them as equivalent.

---

### Mistake 3

Thinking `\d` matches letters.

It matches digits only.

---

# Interview Questions

1. What does `\d` represent?

2. How does `\d` differ from `[0-9]`?

3. Does `\d` match `"512"`?

4. Explain how the Regex Engine evaluates `\d`.

---

# Practice Questions

### Question 1

Will `\d` match?

```
0

7

9

A

m

@
```

Explain each answer.

---

### Question 2

Why is `\d` preferred over `[0-9]` in many Regular Expressions?

---

### Question 3

Explain how the Regex Engine processes `\d`.

---

# Compare & Contrast

| Pattern | Meaning |
|---------|---------|
| `[0-9]` | Match one digit |
| `\d` | Match one digit (predefined Character Class) |

---

# Coming Up

If

```regex
\d
```

matches digits,

what matches **everything except digits**?

The next lesson introduces

```regex
\D
```

the predefined Character Class for matching non-digit characters.

---

# Revision Box

✔ `\d` is a predefined Character Class.

✔ `\d` matches exactly one digit.

✔ It is commonly used instead of `[0-9]`.

✔ The Regex Engine recognizes `\d` as the predefined digit class.

✔ Matching complete numbers requires Quantifiers.

---

# Key Takeaways

- `\d` is the predefined Character Class for digits.
- It is a concise alternative to `[0-9]`.
- It matches exactly one numeric digit.
- It is one of the most frequently used constructs in Regular Expressions and automation.

-----------------------------------------------------------------------------------------------------------

# 2.10 Predefined Character Class `\D`

## Learning Objective

After completing this lesson, you will be able to:

- Understand what `\D` represents.
- Explain why `\D` exists.
- Compare `\D` with `\d` and `[^0-9]`.
- Understand how the Regex Engine evaluates `\D`.
- Use `\D` in practical Regular Expressions.

---

# Introduction

In the previous lesson, we learned

```regex
\d
```

which matches any one numeric digit.

Sometimes, however, we need the exact opposite.

Instead of matching digits,

we want to match **every character that is NOT a digit**.

For these situations, Regex provides another predefined Character Class.

```regex
\D
```

---

# Why Do We Need `\D`?

Suppose we want to ignore digits and process everything else.

Consider the following input.

```text
Drive123
```

Sometimes we only want

```text
Drive
```

Instead of manually listing every non-digit character,

Regex provides

```regex
\D
```

which simply means

```
Match any NON-DIGIT character.
```

---

# Definition

```regex
\D
```

matches **exactly one character that is NOT a numeric digit**.

Equivalent Pattern

```regex
[^0-9]
```

---

# Syntax

```regex
\D
```

Meaning

```
Match any ONE non-digit character.
```

---

# Equivalent Pattern

| Pattern | Equivalent |
|---------|------------|
| `\D` | `[^0-9]` |

Both patterns represent the same concept.

---

# How the Regex Engine Thinks

Pattern

```regex
\D
```

Input

```text
A
```

Regex Engine

```text
Current Pattern

↓

\D

↓

Current Input Character

↓

A

↓

Is A a digit?

↓

NO

↓

MATCH
```

Notice that the Regex Engine first checks whether the current character is a digit.

If it is,

the match fails.

Otherwise,

the match succeeds.

---

# Engine Visualization

```
Pattern

\D

↓

Current Character

A

↓

Is it a digit?

        │
   ┌────┴────┐
   │         │
  YES        NO
   │         │
   ▼         ▼
NO MATCH    MATCH
```

---

# Matching Matrix

| Input | Match | Reason |
|------|:-----:|--------|
| `A` | ✅ | Non-digit |
| `m` | ✅ | Non-digit |
| `@` | ✅ | Non-digit |
| `_` | ✅ | Non-digit |
| Space | ✅ | Non-digit |
| `0` | ❌ | Digit |
| `5` | ❌ | Digit |
| `9` | ❌ | Digit |

---

# Engine Trace

Pattern

```regex
\D
```

Input

```text
@
```

```
Regex Engine Trace

----------------------------------------

Current Pattern Token

\D

Current Input Character

@

Decision

Is '@' a digit?

NO

Action

Character accepted.

Move to the next pattern token.
```

---

# Compare & Contrast

| Pattern | Matches |
|---------|----------|
| `\d` | One digit |
| `\D` | One non-digit |

Examples

| Input | `\d` | `\D` |
|------|:----:|:----:|
| `5` | ✅ | ❌ |
| `A` | ❌ | ✅ |
| `@` | ❌ | ✅ |
| `_` | ❌ | ✅ |
| Space | ❌ | ✅ |

---

# Real-World Usage

`\D` is commonly used for:

### Removing digits

```
Drive123

↓

Drive
```

---

### Extracting text from mixed strings

```
NVME001

↓

NVME
```

---

### Parsing log messages

```
Error500

↓

Error
```

---

### Cleaning user input

```
ABC123XYZ

↓

ABCXYZ
```

---

# Edge Cases

Pattern

```regex
\D
```

Input

```text
5A
```

The first character

```
5
```

does not match.

The Regex Engine continues searching.

The second character

```
A
```

matches successfully.

---

Pattern

```regex
\D
```

Input

```text
123
```

Every character is a digit.

Result

```
No Match
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking `\D` matches multiple non-digit characters.

It matches only **one** character.

---

### Mistake 2

Thinking `\D` is unrelated to `[^0-9]`.

They are equivalent.

---

### Mistake 3

Thinking spaces are excluded.

Spaces are **not digits**, so they match `\D`.

---

# Interview Questions

1. What does `\D` represent?

2. How does `\D` differ from `\d`?

3. What is the equivalent Character Class for `\D`?

4. Explain how the Regex Engine evaluates `\D`.

---

# Practice Questions

## Question 1

Will `\D` match?

```
A

m

@

_

Space

5

0
```

Explain each answer.

---

## Question 2

Why is

```regex
\D
```

equivalent to

```regex
[^0-9]
```

---

## Question 3

Explain how the Regex Engine processes `\D`.

---

# Coming Up

So far we have learned:

- Alphabets
- Digits
- Non-digits

The next predefined Character Class is

```regex
\w
```

which introduces the concept of **word characters**—one of the most frequently used shorthand classes in Regular Expressions.

---

# Revision Box

✔ `\D` is the predefined Character Class for non-digits.

✔ `\D` matches exactly one non-digit character.

✔ `\D` is equivalent to `[^0-9]`.

✔ Spaces and special characters match `\D`.

✔ Digits do not match `\D`.

---

# Key Takeaways

- `\D` is the opposite of `\d`.
- It matches any single character that is not a numeric digit.
- It is commonly used for removing digits and extracting textual information.
- The Regex Engine first checks whether the current character is a digit before deciding whether to match.

-----------------------------------------------------------------------------------------------------------

# 2.11 Predefined Character Class `\w`

## Learning Objective

After completing this lesson, you will be able to:

- Understand what `\w` represents.
- Explain why `\w` exists.
- Identify all characters included in `\w`.
- Understand how the Regex Engine evaluates `\w`.
- Compare `\w` with `[A-Za-z0-9_]`.
- Use `\w` in practical Regular Expressions.

---

# Introduction

So far, we have learned predefined Character Classes for digits.

```regex
\d

\D
```

Regex also provides another predefined Character Class called

```regex
\w
```

The letter **w** stands for

```
Word
```

A Word Character is commonly used when matching identifiers, names, usernames, variables and many other text-based values.

---

# Why Do We Need `\w`?

Suppose we want to match the following characters.

```
A-Z

a-z

0-9

_
```

One way is

```regex
[A-Za-z0-9_]
```

Although correct,

it is lengthy.

Regex provides a predefined Character Class.

```regex
\w
```

which represents exactly the same set of characters.

---

# Definition

```regex
\w
```

matches **exactly one word character**.

A word character is any of the following:

- Uppercase letter
- Lowercase letter
- Digit
- Underscore (`_`)

Equivalent Pattern

```regex
[A-Za-z0-9_]
```

---

# Syntax

```regex
\w
```

Meaning

```
Match any ONE word character.
```

---

# Equivalent Pattern

| Pattern | Equivalent |
|---------|------------|
| `\w` | `[A-Za-z0-9_]` |

---

# What Exactly is a Word Character?

A word character includes

```
A-Z

a-z

0-9

_
```

Notice something important.

The underscore (`_`) is included.

Many beginners forget this.

---

# How the Regex Engine Thinks

Pattern

```regex
\w
```

Input

```text
_
```

Regex Engine

```
Current Pattern

↓

\w

↓

Current Character

↓

_

↓

Is it

Letter

OR

Digit

OR

Underscore?

↓

YES

↓

MATCH
```

---

# Engine Visualization

```
Pattern

\w

↓

Current Character

R

↓

Is it

Letter?

OR

Digit?

OR

Underscore?

        │
   ┌────┴────┐
   │         │
  YES        NO
   │
   ▼
 MATCH
```

---

# Matching Matrix

| Input | Match | Reason |
|------|:-----:|--------|
| `A` | ✅ | Letter |
| `z` | ✅ | Letter |
| `5` | ✅ | Digit |
| `_` | ✅ | Underscore |
| `@` | ❌ | Special character |
| `#` | ❌ | Special character |
| `-` | ❌ | Hyphen |
| Space | ❌ | Whitespace |

---

# Engine Trace

Pattern

```regex
\w
```

Input

```text
5
```

```
Regex Engine Trace

--------------------------------------

Current Pattern Token

\w

Current Input Character

5

Decision

Is it

Letter

OR

Digit

OR

Underscore?

YES

Action

Move to the next pattern token.
```

---

# Compare & Contrast

| Pattern | Matches |
|---------|----------|
| `\w` | Letters, digits, underscore |
| `[A-Za-z0-9_]` | Letters, digits, underscore |

These two patterns are equivalent.

---

# Real-World Usage

`\w` is widely used for matching:

### Usernames

```
john123

alex_01

storage_admin
```

---

### Variable Names

```python
user_name

device_id

total_count
```

---

### Configuration Keys

```
HOST_NAME

DEVICE_ID

PORT1
```

---

### Storage Device IDs

```
NVME001

SSD_01

Drive12
```

---

### Log Tokens

```
PASS

FAIL

ERROR123

CACHE_01
```

---

# Edge Cases

Pattern

```regex
\w
```

Input

```text
-
```

Result

```
No Match
```

Reason

A hyphen is not a word character.

---

Pattern

```regex
\w
```

Input

```text
@
```

Result

```
No Match
```

Reason

Special characters are excluded.

---

Pattern

```regex
\w
```

Input

```text
_
```

Result

```
MATCH
```

Reason

Underscore is part of the definition of a word character.

---

# Memory Tip

Think of

```
\w

↓

Word Character

↓

Letters

+

Digits

+

Underscore
```

Whenever you see `\w`, immediately remember

```
[A-Za-z0-9_]
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking `\w` matches only letters.

It also matches digits and underscores.

---

### Mistake 2

Forgetting that `_` is included.

Underscore is a valid word character.

---

### Mistake 3

Thinking spaces belong to `\w`.

Spaces are not word characters.

---

# Interview Questions

1. What does `\w` represent?

2. What is the equivalent Character Class for `\w`?

3. Does `\w` match `_`? Explain.

4. Explain how the Regex Engine evaluates `\w`.

---

# Practice Questions

### Question 1

Will `\w` match?

```
A

z

7

_

@

-

Space
```

Explain your answer.

---

### Question 2

Why is

```regex
\w
```

equivalent to

```regex
[A-Za-z0-9_]
```

---

### Question 3

Give five real-world examples where `\w` is useful.

---

# Coming Up

If

```regex
\w
```

matches word characters,

what matches

everything except word characters?

The next lesson introduces

```regex
\W
```

which is the exact opposite of `\w`.

---

# Revision Box

✔ `\w` matches one word character.

✔ Word characters include letters, digits and underscore.

✔ `\w` is equivalent to `[A-Za-z0-9_]`.

✔ Special characters are excluded.

✔ Spaces are excluded.

✔ `_` is included.

---

# Key Takeaways

- `\w` is the predefined Character Class for word characters.
- It is equivalent to `[A-Za-z0-9_]`.
- It matches exactly one letter, digit or underscore.
- It is one of the most frequently used Character Classes in programming, automation and log parsing.

-----------------------------------------------------------------------------------------------------------

# 2.12 Predefined Character Class `\W`

## Learning Objective

After completing this lesson, you will be able to:

- Understand what `\W` represents.
- Explain why `\W` exists.
- Compare `\W` with `\w`.
- Understand how the Regex Engine evaluates `\W`.
- Use `\W` in practical Regular Expressions.

---

# Introduction

In the previous lesson, we learned

```regex
\w
```

which matches **word characters**.

Sometimes, however, we need the exact opposite.

Instead of matching letters, digits and underscores,

we want to match **everything else**.

Regex provides another predefined Character Class.

```regex
\W
```

---

# Why Do We Need `\W`?

Suppose we want to detect separators inside text.

Example

```text
NVME-001

Storage@Test

user.name

hello world
```

Sometimes the useful information is not the letters.

Instead,

we want to identify

```
-

@

.

Space
```

These are not word characters.

Regex provides

```regex
\W
```

to match them easily.

---

# Definition

```regex
\W
```

matches **exactly one non-word character**.

A non-word character is any character that is **not**

- Uppercase letter
- Lowercase letter
- Digit
- Underscore (`_`)

Equivalent Pattern

```regex
[^A-Za-z0-9_]
```

---

# Syntax

```regex
\W
```

Meaning

```
Match any ONE non-word character.
```

---

# Regex Equivalence

| Pattern | Equivalent |
|---------|------------|
| `\W` | `[^A-Za-z0-9_]` |

---

# How the Regex Engine Thinks

Pattern

```regex
\W
```

Input

```text
@
```

Regex Engine

```text
Current Pattern

↓

\W

↓

Current Input Character

↓

@

↓

Is it

Letter

OR

Digit

OR

Underscore?

↓

NO

↓

MATCH
```

The Regex Engine checks whether the character is a word character.

If it is not,

the match succeeds.

---

# Engine Visualization

```
Pattern

\W

↓

Current Character

@

↓

Is it

Letter?

OR

Digit?

OR

Underscore?

        │
   ┌────┴────┐
   │         │
  YES        NO
   │         │
   ▼         ▼
NO MATCH    MATCH
```

---

# Matching Matrix

| Input | Match | Reason |
|------|:-----:|--------|
| `@` | ✅ | Special character |
| `#` | ✅ | Special character |
| `-` | ✅ | Hyphen |
| `.` | ✅ | Dot |
| Space | ✅ | Whitespace |
| `A` | ❌ | Word character |
| `m` | ❌ | Word character |
| `8` | ❌ | Digit |
| `_` | ❌ | Underscore |

---

# Engine Trace

Pattern

```regex
\W
```

Input

```text
-
```

```
Regex Engine Trace

--------------------------------------

Current Pattern Token

\W

Current Input Character

-

Decision

Is it

Letter

OR

Digit

OR

Underscore?

NO

Action

Character accepted.

Move to the next pattern token.
```

---

# Compare & Contrast

| Pattern | Matches |
|---------|----------|
| `\w` | Letters, digits, underscore |
| `\W` | Everything except letters, digits and underscore |

Examples

| Input | `\w` | `\W` |
|------|:----:|:----:|
| `A` | ✅ | ❌ |
| `5` | ✅ | ❌ |
| `_` | ✅ | ❌ |
| `@` | ❌ | ✅ |
| `-` | ❌ | ✅ |
| Space | ❌ | ✅ |

---

# Real-World Usage

`\W` is commonly used for:

### Detecting Separators

```text
NVME-001
```

Matches

```
-
```

---

### Finding Special Characters

```text
admin@test.com
```

Matches

```
@

.
```

---

### Password Validation

Detecting characters such as

```
!

@

#

$

%
```

---

### Cleaning Input

Removing punctuation from text.

---

### Parsing Log Files

Finding delimiters between values.

---

# Edge Cases

Pattern

```regex
\W
```

Input

```text
_
```

Result

```
No Match
```

Reason

Underscore is a word character.

---

Pattern

```regex
\W
```

Input

```text
```

(space)

Result

```
MATCH
```

Reason

Whitespace is not a word character.

---

Pattern

```regex
\W
```

Input

```text
@
```

Result

```
MATCH
```

Reason

Special characters are non-word characters.

---

# Memory Tip

```
\w

↓

Word Character

↓

Letters

Digits

Underscore

-----------------------

\W

↓

NOT

Word Character
```

Think of

```
Uppercase W

↓

Without Word
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking `\W` means "only special characters."

It matches **every non-word character**, including spaces.

---

### Mistake 2

Forgetting that `_` is **not** matched.

Underscore belongs to `\w`.

---

### Mistake 3

Thinking `\W` matches multiple characters.

It matches only one character.

---

# Interview Questions

1. What does `\W` represent?

2. What is the equivalent Character Class for `\W`?

3. Does `\W` match spaces?

4. Explain how the Regex Engine evaluates `\W`.

---

# Practice Questions

## Question 1

Will `\W` match?

```
@

-

.

Space

A

7

_
```

Explain your answer.

---

## Question 2

Why is

```regex
\W
```

equivalent to

```regex
[^A-Za-z0-9_]
```

---

## Question 3

Give five practical situations where `\W` is useful.

---

# Coming Up

So far we have learned:

- Digits
- Non-digits
- Word characters
- Non-word characters

The next predefined Character Class introduces another extremely important concept:

```regex
\s
```

which matches **whitespace characters** such as spaces, tabs and newlines.

---

# Revision Box

✔ `\W` matches one non-word character.

✔ `\W` is equivalent to `[^A-Za-z0-9_]`.

✔ Spaces match `\W`.

✔ Special characters match `\W`.

✔ Letters, digits and underscore do not match `\W`.

---

# Key Takeaways

- `\W` is the predefined Character Class for non-word characters.
- It is the opposite of `\w`.
- It matches exactly one character that is not a letter, digit or underscore.
- It is commonly used to detect separators, punctuation and special characters.

-----------------------------------------------------------------------------------------------------------

# 2.13 Predefined Character Class `\s`

## Learning Objective

After completing this lesson, you will be able to:

- Understand what `\s` represents.
- Identify all whitespace characters matched by `\s`.
- Explain how the Regex Engine evaluates `\s`.
- Compare `\s` with ordinary spaces.
- Use `\s` in practical automation tasks.

---

# Introduction

So far, we have learned predefined Character Classes for:

- Digits
- Non-digits
- Word characters
- Non-word characters

Now we introduce another important Character Class:

```regex
\s
```

The letter **s** stands for

```
Whitespace
```

Whitespace characters are invisible characters used to separate text.

Although they are not visible, they play an important role in programming, configuration files, logs and command outputs.

---

# Why Do We Need `\s`?

Consider the following log.

```text
Drive ID : NVME001

Capacity : 512GB

Temperature : 42C
```

Notice the spaces between words.

Sometimes we want to match those spaces.

Regex provides

```regex
\s
```

to match whitespace characters.

---

# Definition

```regex
\s
```

matches **exactly one whitespace character**.

Whitespace includes

- Space
- Tab
- Newline
- Carriage Return
- Form Feed
- Vertical Tab

---

# Syntax

```regex
\s
```

Meaning

```
Match any ONE whitespace character.
```

---

# What is Whitespace?

Whitespace refers to characters that create spacing but are generally not visible.

Examples include:

```
Space

Tab

Newline

Carriage Return

Vertical Tab

Form Feed
```

Among these, the most commonly encountered are:

- Space
- Tab
- Newline

---

# How the Regex Engine Thinks

Pattern

```regex
\s
```

Input

```text
(space)
```

Regex Engine

```text
Current Pattern

↓

\s

↓

Current Input Character

↓

Space

↓

Is it a whitespace character?

↓

YES

↓

MATCH
```

---

# Engine Visualization

```
Pattern

\s

↓

Current Character

Space

↓

Is it

Space?

Tab?

Newline?

Carriage Return?

        │
   ┌────┴────┐
   │         │
  YES        NO
   │
   ▼
 MATCH
```

---

# Matching Matrix

| Input | Match | Reason |
|------|:-----:|--------|
| Space | ✅ | Whitespace |
| Tab | ✅ | Whitespace |
| Newline | ✅ | Whitespace |
| Carriage Return | ✅ | Whitespace |
| `A` | ❌ | Letter |
| `5` | ❌ | Digit |
| `_` | ❌ | Word character |
| `@` | ❌ | Special character |

---

# Engine Trace

Pattern

```regex
\s
```

Input

```text
Tab
```

```
Regex Engine Trace

--------------------------------------

Current Pattern Token

\s

Current Input Character

Tab

Decision

Is it a whitespace character?

YES

Action

Move to the next pattern token.
```

---

# Compare & Contrast

| Pattern | Matches |
|---------|----------|
| Space | Only the space character |
| `\s` | Any whitespace character |

Notice that `\s` is more powerful than typing a literal space because it also matches tabs and newlines.

---

# Real-World Usage

`\s` is commonly used for:

### Parsing Linux Command Output

```text
Filesystem      Size      Used
```

Multiple spaces can be matched using `\s`.

---

### Configuration Files

```text
HOST = server01
```

Matching optional spaces around `=`.

---

### Log Parsing

```text
INFO    Device Connected
```

Handling variable spacing.

---

### Data Cleaning

Removing unnecessary whitespace from text.

---

### CSV and Text Processing

Splitting text separated by spaces or tabs.

---

# Edge Cases

Pattern

```regex
\s
```

Input

```text
A
```

Result

```
No Match
```

Reason

Letters are not whitespace.

---

Pattern

```regex
\s
```

Input

```text
(space)
```

Result

```
MATCH
```

---

Pattern

```regex
\s
```

Input

```text
Tab
```

Result

```
MATCH
```

---

# Memory Tip

```
\s

↓

Space

↓

Whitespace
```

Remember

```
\s

↓

Space

Tab

Newline
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking `\s` matches only spaces.

It also matches tabs and newlines.

---

### Mistake 2

Confusing a literal space with `\s`.

A literal space matches only one specific character.

`\s` matches the entire whitespace family.

---

### Mistake 3

Thinking letters match `\s`.

They do not.

---

# Interview Questions

1. What does `\s` represent?

2. Which characters belong to the whitespace family?

3. How does `\s` differ from a literal space?

4. Explain how the Regex Engine evaluates `\s`.

---

# Practice Questions

## Question 1

Will `\s` match?

```
Space

Tab

Newline

A

5

@
```

Explain your answer.

---

## Question 2

Why is `\s` preferred over a literal space in log parsing?

---

## Question 3

Give five practical situations where `\s` is useful.

---

# Coming Up

If

```regex
\s
```

matches whitespace,

what matches **everything except whitespace**?

The next lesson introduces

```regex
\S
```

the predefined Character Class for matching non-whitespace characters.

---

# Revision Box

✔ `\s` matches one whitespace character.

✔ Whitespace includes spaces, tabs and newlines.

✔ `\s` is more flexible than a literal space.

✔ The Regex Engine checks whether the current character belongs to the whitespace family.

---

# Key Takeaways

- `\s` is the predefined Character Class for whitespace.
- It matches exactly one whitespace character.
- It is widely used in parsing logs, command output and configuration files.
- It simplifies handling variable spacing in text processing.

-----------------------------------------------------------------------------------------------------------

# 2.14 Predefined Character Class `\S`

## Learning Objective

After completing this lesson, you will be able to:

- Understand what `\S` represents.
- Explain why `\S` exists.
- Compare `\S` with `\s`.
- Understand how the Regex Engine evaluates `\S`.
- Use `\S` in practical automation tasks.

---

# Introduction

In the previous lesson, we learned

```regex
\s
```

which matches **whitespace characters** such as spaces, tabs and newlines.

Sometimes we need exactly the opposite.

Instead of matching whitespace,

we want to match every visible character.

Regex provides

```regex
\S
```

---

# Why Do We Need `\S`?

Suppose we have

```text
Drive ID : NVME001
```

Sometimes we want to ignore all spaces and process only

```text
Drive

ID

:

NVME001
```

Instead of describing every possible visible character,

Regex simply provides

```regex
\S
```

---

# Definition

```regex
\S
```

matches **exactly one non-whitespace character**.

It matches every character except

- Space
- Tab
- Newline
- Carriage Return
- Form Feed
- Vertical Tab

---

# Syntax

```regex
\S
```

Meaning

```
Match any ONE non-whitespace character.
```

---

# Regex Equivalence

Equivalent Pattern

```regex
[^\t\r\n\f\v ]
```

> **Note**
>
> Unlike `\d` and `\w`, the equivalent form of `\S` is longer and less readable.
>
> In practice, almost everyone prefers using `\S`.

---

# How the Regex Engine Thinks

Pattern

```regex
\S
```

Input

```text
N
```

Regex Engine

```text
Current Pattern

↓

\S

↓

Current Input Character

↓

N

↓

Is it a whitespace character?

↓

NO

↓

MATCH
```

The Regex Engine first checks whether the character belongs to the whitespace family.

If it does,

the match fails.

Otherwise,

the match succeeds.

---

# Engine Visualization

```
Pattern

\S

↓

Current Character

N

↓

Is it

Space?

Tab?

Newline?

        │
   ┌────┴────┐
   │         │
  YES        NO
   │         │
   ▼         ▼
NO MATCH    MATCH
```

---

# Matching Matrix

| Input | Match | Reason |
|------|:-----:|--------|
| `A` | ✅ | Non-whitespace |
| `5` | ✅ | Non-whitespace |
| `_` | ✅ | Non-whitespace |
| `@` | ✅ | Non-whitespace |
| Space | ❌ | Whitespace |
| Tab | ❌ | Whitespace |
| Newline | ❌ | Whitespace |

---

# Engine Trace

Pattern

```regex
\S
```

Input

```text
@
```

```
Regex Engine Trace

--------------------------------------

Current Pattern Token

\S

Current Input Character

@

Decision

Is '@' whitespace?

NO

Action

Character accepted.

Move to the next pattern token.
```

---

# Compare & Contrast

| Pattern | Matches |
|---------|----------|
| `\s` | Whitespace |
| `\S` | Non-whitespace |

Examples

| Input | `\s` | `\S` |
|------|:----:|:----:|
| Space | ✅ | ❌ |
| Tab | ✅ | ❌ |
| Newline | ✅ | ❌ |
| `A` | ❌ | ✅ |
| `7` | ❌ | ✅ |
| `@` | ❌ | ✅ |

---

# Literal vs Regex

| Pattern | Matches |
|---------|----------|
| `" "` | One literal space |
| `\s` | Any whitespace character |
| `\S` | Any non-whitespace character |

---

# Real-World Usage

`\S` is commonly used for:

### Ignoring Extra Spaces

```text
Device     Connected
```

Extract only the visible text.

---

### Parsing Command Output

```text
Filesystem      Size
```

Capture the actual values while ignoring whitespace.

---

### Reading Configuration Files

```text
HOST = server01
```

Extract

```text
HOST

server01
```

without the surrounding spaces.

---

### Log Processing

Skip whitespace and capture only meaningful tokens.

---

### Input Validation

Detect values that contain actual content instead of blank spaces.

---

# Edge Cases

Pattern

```regex
\S
```

Input

```text
Space
```

Result

```
No Match
```

---

Pattern

```regex
\S
```

Input

```text
Tab
```

Result

```
No Match
```

---

Pattern

```regex
\S
```

Input

```text
A
```

Result

```
MATCH
```

---

# Memory Tip

```
\s

↓

Whitespace

----------------

\S

↓

NOT

Whitespace
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking `\S` means "special characters."

It matches **every non-whitespace character**, including letters and digits.

---

### Mistake 2

Thinking spaces match `\S`.

They do not.

---

### Mistake 3

Thinking `\S` matches multiple characters.

It matches exactly **one** character.

---

# Interview Questions

1. What does `\S` represent?

2. How does `\S` differ from `\s`?

3. Give practical uses of `\S`.

4. Explain how the Regex Engine evaluates `\S`.

---

# Practice Questions

### Question 1

Will `\S` match?

```
A

5

@

_

Space

Tab

Newline
```

Explain your answer.

---

### Question 2

Why is `\S` useful when parsing command output?

---

### Question 3

Explain how the Regex Engine processes `\S`.

---

# Predefined Character Class Family

| Positive | Negative |
|----------|----------|
| `\d` | `\D` |
| `\w` | `\W` |
| `\s` | `\S` |

---

# Coming Up

So far, we have completed all predefined Character Classes.

The next lesson introduces one of the most powerful and frequently misunderstood metacharacters in Regular Expressions:

```regex
.
```

The **dot (`.`)**, which matches almost any single character.

---

# Revision Box

✔ `\S` matches one non-whitespace character.

✔ It is the opposite of `\s`.

✔ Letters, digits and special characters all match `\S`.

✔ Spaces, tabs and newlines do not match `\S`.

✔ The Regex Engine first checks whether the current character belongs to the whitespace family.

---

# Key Takeaways

- `\S` is the predefined Character Class for non-whitespace characters.
- It is the opposite of `\s`.
- It matches exactly one visible (non-whitespace) character.
- It is widely used in log parsing, configuration parsing and text processing.

-----------------------------------------------------------------------------------------------------------

# 2.15 Combining Character Classes

## Learning Objective

After completing this lesson, you will be able to:

- Understand how multiple Character Classes can be combined.
- Explain why combined Character Classes are useful.
- Predict how the Regex Engine evaluates combined Character Classes.
- Write compact Character Classes for practical automation problems.
- Avoid common mistakes while combining Character Classes.

---

# Introduction

So far, we have learned several Character Classes individually.

Examples include

```regex
[a-z]

[A-Z]

[0-9]

[A-Za-z]

\d

\w
```

Each Character Class represents a specific set of characters.

In real-world Regular Expressions, however, we often need to match **multiple types of characters simultaneously**.

Regex allows us to combine Character Classes into a single Character Class.

---

# Why Combine Character Classes?

Suppose we want to match

- Uppercase letters
- Lowercase letters
- Digits

One option is to write separate Regular Expressions.

```
[a-z]

OR

[A-Z]

OR

[0-9]
```

This is unnecessary.

Instead, Regex allows us to combine all three.

```regex
[A-Za-z0-9]
```

Now a single Character Class matches any alphabet or digit.

---

# Definition

A **Combined Character Class** contains multiple Character Ranges or literal characters inside the same square brackets.

Example

```regex
[A-Za-z0-9]
```

Meaning

```
Match any ONE character that is

Uppercase Letter

OR

Lowercase Letter

OR

Digit
```

---

# General Syntax

```regex
[Range1Range2Range3...]
```

Example

```regex
[A-Za-z0-9]
```

---

# How the Regex Engine Thinks

Pattern

```regex
[A-Za-z0-9]
```

Input

```text
8
```

Regex Engine

```text
Current Pattern

↓

[A-Za-z0-9]

↓

Current Input Character

↓

8

↓

Check

A → Z ?

↓

NO

↓

Check

a → z ?

↓

NO

↓

Check

0 → 9 ?

↓

YES

↓

MATCH
```

The Regex Engine checks every allowed range until one succeeds.

If any range matches,

the Character Class matches.

---

# Engine Visualization

```
                Pattern

           [A-Za-z0-9]

                  │
                  ▼

          Current Character

                  8

                  │
                  ▼

        ┌────────────────────┐
        │ Check A-Z          │
        └─────────┬──────────┘
                  │
                 NO
                  │
                  ▼
        ┌────────────────────┐
        │ Check a-z          │
        └─────────┬──────────┘
                  │
                 NO
                  │
                  ▼
        ┌────────────────────┐
        │ Check 0-9          │
        └─────────┬──────────┘
                  │
                 YES
                  │
                  ▼
               MATCH
```

---

# Example 1

Pattern

```regex
[A-Za-z]
```

Matches

```
A

m

Z

x
```

Does not match

```
5

@
```

---

# Example 2

Pattern

```regex
[A-Za-z0-9]
```

Matches

```
A

z

7

0
```

Does not match

```
@

#

Space
```

---

# Example 3

Pattern

```regex
[A-F0-9]
```

Matches

```
A

B

F

0

8

9
```

Does not match

```
G

a

@
```

---

# Example 4

Pattern

```regex
[a-z0-9_]
```

Matches

```
a

m

7

_

z
```

Does not match

```
@

#

Space
```

---

# Example 5

Pattern

```regex
[ABC123]
```

Matches

```
A

B

C

1

2

3
```

Does not match

```
D

4

a
```

Notice that this example contains **literal characters**, not ranges.

---

# Matching Matrix

## Pattern

```regex
[A-Za-z0-9]
```

| Input | Match | Reason |
|------|:-----:|--------|
| `A` | ✅ | Uppercase |
| `m` | ✅ | Lowercase |
| `5` | ✅ | Digit |
| `0` | ✅ | Digit |
| `_` | ❌ | Not included |
| `@` | ❌ | Not included |
| Space | ❌ | Not included |

---

# Real-World Usage

Combined Character Classes are commonly used for:

### Usernames

```text
john123

admin01

storage99
```

---

### Device IDs

```text
NVME001

SSD123

DISK09
```

---

### Product Codes

```text
AB123

ZX900

PQR456
```

---

### Configuration Values

```text
DEVICE01

HOST02

CACHE01
```

---

### License Keys

```text
ABC123

XYZ999
```

---

# Compare & Contrast

| Pattern | Matches |
|---------|----------|
| `[a-z]` | Lowercase letters |
| `[A-Z]` | Uppercase letters |
| `[0-9]` | Digits |
| `[A-Za-z]` | Any alphabet |
| `[A-Za-z0-9]` | Any alphabet or digit |

---

# Edge Cases

Pattern

```regex
[A-Za-z0-9]
```

Input

```text
_
```

Result

```
No Match
```

Reason

Underscore is not included.

---

Pattern

```regex
[A-Za-z0-9]
```

Input

```text
@
```

Result

```
No Match
```

Reason

Special characters are excluded.

---

Pattern

```regex
[A-Za-z0-9]
```

Input

```text
M
```

Result

```
MATCH
```

---

# Memory Tip

Think of

```
[A-Za-z0-9]

↓

Letters

+

Digits
```

Simply combine the sets you want to allow.

---

# Common Beginner Mistakes

### Mistake 1

Thinking Character Ranges must always be written separately.

They can be combined inside one Character Class.

---

### Mistake 2

Thinking

```regex
[A-Za-z0-9]
```

matches an entire word.

It matches **one character**.

---

### Mistake 3

Assuming `_` is included.

It is **not** included unless explicitly written.

Correct version:

```regex
[A-Za-z0-9_]
```

---

# Interview Questions

1. What is a Combined Character Class?

2. How does the Regex Engine evaluate `[A-Za-z0-9]`?

3. What is the difference between `[A-Za-z0-9]` and `\w`?

4. Why are Combined Character Classes useful?

---

# Practice Questions

## Question 1

Will

```regex
[A-Za-z0-9]
```

match?

```
A

z

5

@

_

Space
```

Explain your answer.

---

## Question 2

Write a Character Class that matches:

- Uppercase letters
- Digits

---

## Question 3

Write a Character Class that matches:

- Lowercase letters
- Digits
- Underscore

---

# Coming Up

So far, every Character Class has matched a **specific set of characters**.

The next lesson introduces one of the most powerful metacharacters in Regular Expressions:

```regex
.
```

Unlike Character Classes, the **dot (`.`)** has a completely different meaning.

It represents **almost any single character**, making it one of the most frequently used metacharacters in Regular Expressions.

---

# Revision Box

✔ Character Classes can be combined.

✔ Combined Character Classes match one character from multiple allowed sets.

✔ The Regex Engine checks each allowed range until one matches.

✔ `[A-Za-z0-9]` matches letters and digits.

✔ Add `_` explicitly if you want underscores.

---

# Key Takeaways

- Multiple Character Classes can be combined into one Character Class.
- Combined Character Classes make Regular Expressions shorter and easier to read.
- The Regex Engine accepts a character if it belongs to **any one** of the specified sets.
- Combined Character Classes are heavily used in usernames, identifiers, storage device names and configuration values.

-----------------------------------------------------------------------------------------------------------

# 2.16 Dot Metacharacter `.`

## Learning Objective

After completing this lesson, you will be able to:

- Understand what the dot (`.`) metacharacter represents.
- Explain why the dot is different from Character Classes.
- Understand how the Regex Engine evaluates the dot.
- Identify what the dot matches and what it does not match.
- Use the dot effectively in practical Regular Expressions.

---

# Introduction

Until now, every Character Class we learned explicitly described **which characters were allowed**.

Examples

```regex
[a-z]

[A-Z]

[0-9]

\d

\w
```

Each of these matches a specific set of characters.

Sometimes, however, we do not care about the type of character.

We simply want to match **any character**.

Regex provides the dot metacharacter for this purpose.

```regex
.
```

---

# Why Do We Need `.`?

Suppose we have the following values.

```text
A

7

@

_

x
```

Instead of writing a Character Class that includes every possible character,

Regex allows us to simply write

```regex
.
```

---

# Definition

The dot (`.`) is a **metacharacter** that matches **almost any single character**.

In most Regex engines,

it matches every character **except the newline character**.

---

# Syntax

```regex
.
```

Meaning

```
Match any ONE character

except a newline.
```

---

# How the Regex Engine Thinks

Pattern

```regex
.
```

Input

```text
@
```

Regex Engine

```text
Current Pattern

↓

.

↓

Current Input Character

↓

@

↓

Is it a newline?

↓

NO

↓

MATCH
```

Unlike Character Classes,

the Regex Engine does **not** check for letters, digits or symbols.

It simply checks whether the current character is a newline.

If it is not,

the match succeeds.

---

# Engine Visualization

```
              Pattern

                 .

                 │
                 ▼

        Current Character

                 @

                 │
                 ▼

      Is it a newline?

          │
     ┌────┴────┐
     │         │
    YES       NO
     │         │
     ▼         ▼
 NO MATCH    MATCH
```

---

# Matching Matrix

| Input | Match | Reason |
|------|:-----:|--------|
| `A` | ✅ | Any character |
| `7` | ✅ | Any character |
| `@` | ✅ | Any character |
| `_` | ✅ | Any character |
| Space | ✅ | Space is a character |
| `.` | ✅ | Dot can match a literal dot in the input |
| Newline | ❌ | Dot does not match newline by default |

---

# Example 1

Pattern

```regex
.
```

Input

```text
A
```

Result

```
MATCH
```

---

# Example 2

Pattern

```regex
.
```

Input

```text
9
```

Result

```
MATCH
```

---

# Example 3

Pattern

```regex
.
```

Input

```text
@
```

Result

```
MATCH
```

---

# Example 4

Pattern

```regex
.
```

Input

```text
(Newline)
```

Result

```
NO MATCH
```

---

# Engine Trace

Pattern

```regex
.
```

Input

```text
A
```

```
Regex Engine Trace

--------------------------------------

Current Pattern Token

.

Current Input Character

A

Decision

Is it a newline?

NO

Action

Move to the next pattern token.
```

---

# Compare & Contrast

| Pattern | Matches |
|---------|----------|
| `[A-Za-z]` | One alphabet |
| `[0-9]` | One digit |
| `\w` | One word character |
| `.` | Almost any one character |

---

# Real-World Usage

The dot is commonly used for:

### Unknown Characters

```
NVME001

NVME101

NVMEA01
```

When one position may contain any character.

---

### File Names

```text
report.pdf

image.png

notes.txt
```

Matching unknown filenames.

---

### Log Processing

Matching variable text between fixed patterns.

---

### Validation

Accepting any character at a specific position.

---

# Edge Cases

Pattern

```regex
.
```

Input

```text
Space
```

Result

```
MATCH
```

---

Pattern

```regex
.
```

Input

```text
(Newline)
```

Result

```
NO MATCH
```

---

Pattern

```regex
.
```

Input

```text
.
```

Result

```
MATCH
```

The dot in the **input** is treated like any other character.

---

# Important Note

Do **not** confuse:

```regex
.
```

with

```text
.
```

The first is a **Regex metacharacter**.

The second is a **literal dot** in the input text.

Later, you will learn how to match a literal dot using:

```regex
\.
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking `.` matches multiple characters.

It matches **exactly one** character.

---

### Mistake 2

Thinking `.` matches newline characters.

By default, it does not.

---

### Mistake 3

Thinking `.` matches only letters.

It matches almost every character type.

---

# Interview Questions

1. What does the dot (`.`) metacharacter represent?

2. Does `.` match newline characters?

3. How does the Regex Engine evaluate `.`?

4. How is `.` different from `[A-Za-z]`?

---

# Practice Questions

## Question 1

Will `.` match?

```
A

5

@

_

Space

Newline
```

Explain your answer.

---

## Question 2

Why is the dot called a metacharacter instead of a Character Class?

---

## Question 3

Give three practical situations where `.` is useful.

---

# Coming Up

Now that we know how to match characters,

the next chapter answers another important question:

> **"How many times should a character appear?"**

This introduces **Quantifiers**, beginning with the `*` (asterisk) quantifier.

---

# Revision Box

✔ `.` matches almost any single character.

✔ It matches exactly one character.

✔ By default, it does not match newline characters.

✔ `.` is a metacharacter, not a Character Class.

✔ A literal dot requires escaping (`\.`), which will be covered later.

---

# Key Takeaways

- The dot (`.`) is one of the most commonly used metacharacters in Regular Expressions.
- It matches almost any single character.
- It is useful when the exact character is unknown or unimportant.
- By default, it does not match newline characters.
- It differs from Character Classes because it is a special metacharacter rather than an explicit set of allowed characters.

-----------------------------------------------------------------------------------------------------------

# 2.17 Character Classes & Metacharacters Summary

## Chapter Overview

In this chapter, we learned how Regular Expressions identify individual characters using **Character Classes**, **Predefined Character Classes**, and the **Dot Metacharacter**.

These concepts form the foundation for every advanced Regex topic, including Quantifiers, Groups, Lookarounds and Pattern Matching.

---

# Character Range Summary

| Pattern | Meaning | Matches |
|---------|---------|----------|
| `[a-z]` | Lowercase letters | `a-z` |
| `[A-Z]` | Uppercase letters | `A-Z` |
| `[0-9]` | Digits | `0-9` |
| `[A-Za-z]` | Alphabets | Uppercase + Lowercase |
| `[^a-z]` | Not lowercase | Everything except `a-z` |
| `[^0-9]` | Not digits | Everything except digits |

---

# Predefined Character Classes

| Pattern | Equivalent | Meaning |
|---------|------------|---------|
| `\d` | `[0-9]` | One digit |
| `\D` | `[^0-9]` | One non-digit |
| `\w` | `[A-Za-z0-9_]` | One word character |
| `\W` | `[^A-Za-z0-9_]` | One non-word character |
| `\s` | Whitespace family | One whitespace character |
| `\S` | Non-whitespace | One non-whitespace character |

---

# Positive vs Negative Character Classes

| Positive | Negative |
|----------|----------|
| `\d` | `\D` |
| `\w` | `\W` |
| `\s` | `\S` |

Remember:

```
Lowercase

↓

Positive

Uppercase

↓

Negative
```

Examples

```
\d

Digit

---------------

\D

Not Digit
```

---

# Character Class Comparison

| Pattern | Letters | Digits | `_` | Space | `@` |
|---------|:------:|:------:|:---:|:-----:|:---:|
| `[A-Za-z]` | ✅ | ❌ | ❌ | ❌ | ❌ |
| `[0-9]` | ❌ | ✅ | ❌ | ❌ | ❌ |
| `\w` | ✅ | ✅ | ✅ | ❌ | ❌ |
| `\W` | ❌ | ❌ | ❌ | ✅ | ✅ |
| `\d` | ❌ | ✅ | ❌ | ❌ | ❌ |
| `\D` | ✅ | ❌ | ✅ | ✅ | ✅ |
| `\s` | ❌ | ❌ | ❌ | ✅ | ❌ |
| `\S` | ✅ | ✅ | ✅ | ❌ | ✅ |
| `.` | ✅ | ✅ | ✅ | ✅ | ✅* |

\* By default, `.` does **not** match the newline character.

---

# Dot (`.`) Summary

| Pattern | Meaning |
|---------|---------|
| `.` | Match almost any single character |

Important points:

- Matches exactly one character.
- Does not match newline by default.
- It is a metacharacter.
- A literal dot is matched using `\.` (covered later).

---

# Choosing the Right Character Class

| Requirement | Pattern |
|------------|---------|
| Any lowercase letter | `[a-z]` |
| Any uppercase letter | `[A-Z]` |
| Any alphabet | `[A-Za-z]` |
| Any digit | `\d` |
| Any non-digit | `\D` |
| Any word character | `\w` |
| Any non-word character | `\W` |
| Any whitespace | `\s` |
| Any non-whitespace | `\S` |
| Almost any character | `.` |

---

# Regex Engine Review

Whenever the Regex Engine encounters a Character Class, it follows the same decision process.

```
           Read Pattern
                 │
                 ▼
      Read Current Character
                 │
                 ▼
    Does it satisfy the rule?
           │            │
         YES           NO
          │             │
          ▼             ▼
      MATCH        NO MATCH
```

For combined Character Classes, the engine checks each allowed range until one succeeds.

---

# Common Beginner Mistakes

- Thinking Character Classes match entire words.
- Forgetting that Character Classes match **one character**.
- Forgetting `_` belongs to `\w`.
- Thinking `.` matches newlines.
- Confusing `\d` with complete numbers.
- Confusing a literal space with `\s`.
- Forgetting that `^` inside `[]` creates a negated Character Class.

---

# Interview Questions

1. What is a Character Class?
2. What is the difference between `[A-Za-z]` and `\w`?
3. Explain the difference between `\d` and `[0-9]`.
4. What does `\W` match?
5. What does `\S` match?
6. Why does `.` not match newline characters?
7. Explain how the Regex Engine evaluates Character Classes.
8. What is a negated Character Class?
9. When would you use `\s`?
10. When would you use `.` instead of a Character Class?

---

# Practice Questions

1. Which Character Class would you use to match:

- Storage Device IDs
- Usernames
- Port Numbers
- IP Address digits
- Spaces
- Non-whitespace characters

---

2. Which of the following match `\w`?

```
A

5

_

@

Space
```

---

3. Which of the following match `.`?

```
A

@

Space

Newline
```

---

4. Explain the difference between

```
[A-Za-z]

\w

.
```

---

# Chapter Revision Checklist

Before moving to Chapter 3, ensure you can confidently answer:

- [ ] What is a Character Class?
- [ ] What is a Character Range?
- [ ] What is a Negated Character Class?
- [ ] Difference between `[0-9]` and `\d`.
- [ ] Difference between `[A-Za-z0-9]` and `\w`.
- [ ] Difference between `\s` and a literal space.
- [ ] Difference between `.` and Character Classes.
- [ ] How the Regex Engine evaluates Character Classes.
- [ ] Common mistakes related to Character Classes.

---

# Chapter Completion

Congratulations!

You have completed **Chapter 2 — Character Classes & Metacharacters**.

You can now identify:

- Letters
- Digits
- Word characters
- Whitespace
- Non-whitespace
- Negated character sets
- Almost any single character

These concepts are the foundation for the next chapter.

-----------------------------------------------------------------------------------------------------------


