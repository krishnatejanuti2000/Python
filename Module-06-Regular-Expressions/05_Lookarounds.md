## Chapter-5 Lookarounds

---

# 5.1 Why Lookarounds?

## Learning Objective

After completing this lesson, you will be able to:

- Understand why Lookarounds were introduced.
- Identify the limitations of normal Regular Expression matching.
- Explain how Lookarounds solve context-based matching problems.
- Recognize situations where surrounding text must be checked without becoming part of the match.
- Understand why Lookarounds are widely used in automation.

---

# Previous Knowledge

In the previous chapters, we learned:

- Character Classes
- Quantifiers
- Groups
- Backreferences

These features allow us to describe patterns and capture matched text.

However,

there is still one important limitation.

Sometimes we need to verify that certain text exists

**before**

or

**after**

the required match,

without actually matching that surrounding text.

This is where Lookarounds become necessary.

---

# Introduction

Consider the following input.

```text
Capacity=1024GB
```

Suppose we only want

```text
1024GB
```

We do **not** want

```text
Capacity=
```

to become part of the match.

However,

we still want to verify that

```text
1024GB
```

appears immediately after

```text
Capacity=
```

The surrounding text is important,

but it should not appear in the final result.

---

# The Problem

Suppose we write

```regex
Capacity=\d+GB
```

Input

```text
Capacity=1024GB
```

The Regex Engine returns

```text
Capacity=1024GB
```

But our automation script only needs

```text
1024GB
```

The prefix

```text
Capacity=
```

was required only for validation.

It should not become part of the extracted value.

---

# Another Example

Input

```text
ERROR: Drive Timeout
```

Suppose we only need

```text
Drive Timeout
```

We must first verify that

```text
ERROR:
```

exists.

However,

the final match should contain only

```text
Drive Timeout
```

---

# Why Can't Groups Solve This?

A common beginner question is

> "Can't we simply use Capturing Groups?"

Example

```regex
ERROR:\s(.*)
```

Yes,

the Capturing Group can extract

```text
Drive Timeout
```

However,

the overall match is still

```text
ERROR: Drive Timeout
```

Sometimes,

we do not want the Regex Engine to consume

```text
ERROR:
```

at all.

Instead,

we only want the engine to **check** that it exists.

This is exactly what Lookarounds do.

---

# The Solution

Lookarounds allow the Regex Engine to

```
Check Context

↓

Without

Consuming Characters
```

They answer questions such as

```
Is this text

followed by

something?

--------------------

Is this text

preceded by

something?
```

without including that surrounding text in the final match.

---

# Regex Engine Perspective

Without Lookaround

```
Read

Capacity=

↓

Match

Capacity=

↓

Continue

↓

Match

1024GB
```

Final Match

```text
Capacity=1024GB
```

---

With Lookaround

```
Check

Capacity=

↓

Do Not Consume

↓

Continue

↓

Match

1024GB
```

Final Match

```text
1024GB
```

---

# Engine Visualization

```
                Pattern

        Lookaround + Match

                  │
                  ▼

        +------------------+
        |   Regex Engine   |
        +------------------+

                  │
                  ▼

         Check Context

                  │

      (No Characters Consumed)

                  │
                  ▼

         Match Pattern

                  │
                  ▼

         Return Match
```

---

# Real-World Usage

Lookarounds are commonly used for:

### Storage Engineering

- Extract capacity only after `Capacity=`
- Extract firmware version only after `Firmware=`
- Validate log formats

---

### Linux Automation

- Extract IP addresses
- Validate configuration entries
- Parse command output

---

### Python Automation

- Parse structured logs
- Extract configuration values
- Process reports

---

### Test Automation

- Validate output context
- Verify log messages
- Check report formatting

---

# Important Observation

Lookarounds

**do not match text**.

Instead,

they verify whether surrounding text satisfies a condition.

Think of them as

```
Inspect

↓

Decide

↓

Continue Matching
```

rather than

```
Match

↓

Consume

↓

Return
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking Lookarounds become part of the final match.

They never do.

---

### Mistake 2

Thinking Lookarounds consume characters.

They only inspect surrounding text.

---

### Mistake 3

Using Capturing Groups when only context verification is required.

Sometimes Lookarounds produce simpler and cleaner Regular Expressions.

---

# Interview Questions

1. Why were Lookarounds introduced?

2. What limitation do Lookarounds solve?

3. Why can't ordinary matching always solve context-based problems?

4. Give practical applications of Lookarounds.

5. Why are Lookarounds useful in automation?

---

# Practice Questions

### Question 1

Why is

```regex
Capacity=\d+GB
```

sometimes not the ideal solution?

---

### Question 2

Explain why context verification is important in automation.

---

### Question 3

List five situations where Lookarounds are useful.

---

# Memory Tip

```
Normal Regex

↓

Matches

↓

Consumes

----------------------

Lookaround

↓

Checks

↓

Does Not Consume
```

Remember

```
Lookaround

=

Check

Without

Taking
```

---

# Revision Box

✔ Lookarounds solve context-based matching problems.

✔ They verify surrounding text without consuming it.

✔ They keep unwanted prefixes and suffixes out of the final match.

✔ They simplify extraction and validation tasks.

✔ They are widely used in enterprise automation.

---

# Key Takeaways

- Lookarounds were introduced to support context-sensitive matching.
- They inspect surrounding text without making it part of the final match.
- They overcome limitations of ordinary pattern matching.
- Lookarounds make extraction cleaner and more precise.
- They are essential for advanced Regular Expressions used in automation.

---

# Coming Up

Now that we understand **why Lookarounds are needed**,

the next lesson formally defines **what a Lookaround is**, introduces the four Lookaround types, and explains how the Regex Engine evaluates them during pattern matching.

------------------------------------------------------------------------------------------------------------

# 5.2 What is a Lookaround?

## Learning Objective

After completing this lesson, you will be able to:

- Define a Lookaround.
- Understand the purpose of Lookarounds.
- Distinguish between matching and asserting.
- Identify the four types of Lookarounds.
- Explain how the Regex Engine evaluates Lookarounds.

---

# Previous Knowledge

In the previous lesson, we learned why Lookarounds are needed.

We discovered that sometimes we need to verify surrounding text

without making it part of the final match.

Lookarounds solve this problem.

Now let us formally define what a Lookaround is.

---

# Introduction

Consider the following input.

```text
Capacity=1024GB
```

Suppose we want to extract

```text
1024GB
```

while ensuring it appears immediately after

```text
Capacity=
```

The Regex Engine must first verify the surrounding text.

If the condition is satisfied,

matching continues.

Otherwise,

matching fails.

Notice that

```
Capacity=
```

is **checked**,

but it is **not returned** as part of the final match.

This behavior is called a **Lookaround**.

---

# Definition

A **Lookaround** is a Regular Expression assertion that checks surrounding text without consuming it.

The Regex Engine evaluates whether a specified condition is true.

If the condition succeeds,

matching continues.

If the condition fails,

the current matching attempt fails.

---

# Understanding the Definition

The most important word is

```
Assertion
```

A Lookaround does **not** match characters.

Instead,

it asks the Regex Engine a question.

Examples

```
Is the required text present after the current position?

------------------------

Is the required text present before the current position?
```

The answer is always

```
Yes

or

No
```

---

# The Four Types of Lookarounds

Regular Expressions provide four Lookaround assertions.

| Lookaround | Purpose |
|------------|---------|
| Positive Lookahead | Required text must appear after the current position. |
| Negative Lookahead | Required text must **not** appear after the current position. |
| Positive Lookbehind | Required text must appear before the current position. |
| Negative Lookbehind | Required text must **not** appear before the current position. |

We will study each of these individually in the following lessons.

---

# Lookaround is an Assertion

Unlike Character Classes,

Quantifiers,

or Groups,

Lookarounds do not consume characters.

Instead,

they simply verify whether a condition is true.

Think of the Regex Engine performing two separate tasks.

```
Check Condition

↓

If True

↓

Continue Matching

------------------------

If False

↓

Stop Current Match
```

---

# Regex Engine Explanation

Suppose the Regex Engine reaches the current position.

```
Capacity=1024GB

         ^
```

Instead of immediately matching,

the engine first performs an assertion.

```
Current Position

↓

Check Surrounding Text

↓

Condition Satisfied?

↓

YES

↓

Continue Matching

------------------------

NO

↓

Current Match Fails
```

Notice that

the current position never moves while the assertion is being evaluated.

---

# Engine Visualization

```
            Current Position

                    │
                    ▼

          +------------------+
          |   Regex Engine   |
          +------------------+

                    │
                    ▼

            Evaluate Assertion

                    │
            ┌───────┴────────┐
            │                │
            ▼                ▼

        Assertion        Assertion

         TRUE             FALSE

            │                │
            ▼                ▼

     Continue Match     Match Fails
```

---

# Engine Trace

Input

```text
Capacity=1024GB
```

```
Regex Engine Trace

--------------------------------------

Reach Current Position

↓

Evaluate Lookaround

↓

Condition Satisfied?

↓

YES

↓

Current Position Unchanged

↓

Continue Matching

↓

SUCCESS
```

---

# Compare & Contrast

| Normal Matching | Lookaround |
|-----------------|------------|
| Consumes characters | Consumes nothing |
| Produces matched text | Produces only a decision |
| Moves the current position | Leaves the current position unchanged |
| Returns matched characters | Returns Success or Failure |

---

# Real-World Usage

Lookarounds are widely used for:

### Storage Engineering

- Extract capacity after a label.
- Validate firmware entries.
- Parse structured storage logs.

---

### Linux Automation

- Validate command output.
- Extract configuration values.
- Parse network information.

---

### Python Automation

- Process reports.
- Extract values.
- Validate structured input.

---

### Test Automation

- Validate expected output.
- Check surrounding context.
- Verify report formatting.

---

# Important Observation

A Lookaround never becomes part of the final match.

Its only responsibility is

```
Inspect

↓

Decide

↓

Continue

or

Fail
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking Lookarounds capture text.

They do not.

---

### Mistake 2

Thinking Lookarounds consume characters.

They never consume characters.

---

### Mistake 3

Thinking Lookarounds change the current position.

The Regex Engine remains at the same position after evaluating a Lookaround.

---

# Interview Questions

1. What is a Lookaround?

2. Why is a Lookaround called an assertion?

3. How many Lookaround types exist?

4. Does a Lookaround consume characters?

5. How does the Regex Engine evaluate a Lookaround?

---

# Practice Questions

### Question 1

Explain why a Lookaround is considered an assertion rather than a match.

---

### Question 2

List the four Lookaround types.

---

### Question 3

Why does the Regex Engine remain at the same position after evaluating a Lookaround?

---

# Memory Tip

```
Lookaround

↓

Assertion

↓

Check Context

↓

No Consumption

↓

Continue

or

Fail
```

Remember

```
Lookaround

=

Decision

Not

Match
```

---

# Revision Box

✔ A Lookaround is an assertion.

✔ Assertions check surrounding text.

✔ Lookarounds never consume characters.

✔ The Regex Engine remains at the same position while evaluating a Lookaround.

✔ Four Lookaround types exist.

---

# Key Takeaways

- Lookarounds are assertions rather than ordinary matching operations.
- They verify surrounding text without consuming it.
- The Regex Engine continues matching only if the assertion succeeds.
- Understanding Lookarounds is essential for writing precise and context-aware Regular Expressions.
- Lookarounds are widely used in enterprise automation for validation and extraction.

---

# Coming Up

Now that we understand **what a Lookaround is**,

the next lesson introduces **Positive Lookahead**, where the Regex Engine verifies that specific text appears **after** the current position while leaving that text outside the final match.

------------------------------------------------------------------------------------------------------------

# 5.3 Positive Lookahead

## Learning Objective

After completing this lesson, you will be able to:

- Understand what Positive Lookahead is.
- Explain how the Regex Engine evaluates a Positive Lookahead.
- Understand the concept of the Current Position.
- Distinguish between matching and asserting.
- Apply Positive Lookahead in real-world automation.

---

# Previous Knowledge

In the previous lesson, we learned that a Lookaround is an assertion.

A Lookaround:

- Checks surrounding text.
- Does not consume characters.
- Does not become part of the final match.

Now we will study the first Lookaround type:

**Positive Lookahead**.

---

# Introduction

Consider the following input.

```text
Capacity=1024GB
```

Suppose we want to extract only

```text
1024GB
```

but only if it appears immediately after

```text
Capacity=
```

The Regex Engine must first verify that the required text exists ahead of the current position.

If the verification succeeds,

matching continues.

Otherwise,

matching fails.

---

# Why Do We Need Positive Lookahead?

Suppose a storage log contains

```text
Capacity=1024GB

Temperature=42C

Firmware=3.5.12
```

Our automation script should extract

```text
1024GB
```

only when it belongs to

```text
Capacity=
```

It should ignore

```text
42C

3.5.12
```

Simply matching

```regex
\d+
```

is not sufficient,

because many numbers exist in the log.

We must first verify the surrounding context.

---

# Definition

A **Positive Lookahead** is a Lookaround that verifies that a specified pattern exists immediately **after** the current position.

If the condition is satisfied,

matching continues.

Otherwise,

the current match fails.

The verified text is **not consumed**.

---

# Syntax

General Syntax

```regex
(?=pattern)
```

Examples

```regex
(?=GB)
```

```regex
(?=ERROR)
```

```regex
(?=\d+GB)
```

The syntax can be read as

> "The following text **must be** this pattern."

---

# Understanding the Current Position

The Regex Engine always processes the input from a particular location.

This location is called the **Current Position**.

Example

```text
Capacity=1024GB
         ^
```

The symbol

```text
^
```

does **not** represent the Regex anchor here.

It simply illustrates the Regex Engine's current position in the input.

At this point,

the Regex Engine can inspect the text ahead without moving forward.

---

# Regex Engine Explanation

Pattern

```regex
(?=1024GB)
```

Input

```text
Capacity=1024GB
```

Regex Engine

```
Reach Current Position

↓

Encounter

(?=

↓

Read Ahead

↓

Does

1024GB

Exist?

↓

YES

↓

Return To

Current Position

↓

Continue Matching
```

Notice something important.

The Regex Engine looked ahead,

but it returned to exactly the same position.

Nothing was consumed.

---

# Engine Visualization

```
Current Position

       │
       ▼

Capacity=1024GB
         ^

       │
       ▼

+------------------+
|   Regex Engine   |
+------------------+

       │
       ▼

Check Ahead

       │

1024GB ?

       │
 ┌─────┴─────┐
 │           │
 ▼           ▼

YES         NO

 │           │

 ▼           ▼

Continue     Fail

Matching
```

---

# Engine Trace

Pattern

```regex
(?=1024GB)
```

Input

```text
Capacity=1024GB
```

```
Regex Engine Trace

--------------------------------------

Reach Current Position

↓

Read

(?=

↓

Inspect Future Text

↓

Found

1024GB

↓

Assertion Passed

↓

Current Position Unchanged

↓

Continue Matching

↓

SUCCESS
```

---

# Matching Matrix

Pattern

```regex
(?=1024GB)
```

| Future Text | Assertion Result |
|-------------|------------------|
| `1024GB` | ✅ Pass |
| `512GB` | ❌ Fail |
| `ERROR` | ❌ Fail |
| `1024MB` | ❌ Fail |

---

# Compare & Contrast

| Normal Matching | Positive Lookahead |
|-----------------|-------------------|
| Matches characters | Checks characters |
| Consumes characters | Consumes nothing |
| Moves forward | Returns to the same position |
| Produces matched text | Produces only Success or Failure |

---

# Real-World Usage

Positive Lookahead is useful for:

### Storage Engineering

- Validate Capacity entries.
- Verify Firmware labels.
- Parse structured storage logs.

---

### Linux Automation

- Validate configuration values.
- Verify command output.
- Parse network information.

---

### Python Automation

- Extract values only in specific contexts.
- Validate structured reports.
- Process configuration files.

---

### Test Automation

- Verify expected output.
- Validate report formats.
- Ensure required context exists.

---

# Important Observation

Positive Lookahead performs

```
Look

↓

Verify

↓

Return

↓

Continue
```

The Regex Engine never consumes the inspected characters.

The Current Position remains unchanged.

---

# Common Beginner Mistakes

### Mistake 1

Thinking Positive Lookahead matches the inspected text.

It only verifies it.

---

### Mistake 2

Thinking the Regex Engine moves forward during the assertion.

It always returns to the Current Position.

---

### Mistake 3

Confusing Lookahead with Capturing Groups.

Lookahead checks future text.

Capturing Groups store matched text.

---

# Interview Questions

1. What is a Positive Lookahead?

2. What is the syntax of Positive Lookahead?

3. Does Positive Lookahead consume characters?

4. What is the Current Position?

5. How does the Regex Engine evaluate a Positive Lookahead?

---

# Practice Questions

### Question 1

Explain why Positive Lookahead is called an assertion.

---

### Question 2

Why does the Current Position remain unchanged after a Positive Lookahead?

---

### Question 3

List five practical applications of Positive Lookahead.

---

# Memory Tip

```
Positive Lookahead

↓

Look Ahead

↓

Must Exist

↓

Do Not Consume

↓

Continue
```

Remember

```
(?= )

↓

Future

Must Match
```

---

# Revision Box

✔ Positive Lookahead checks text after the Current Position.

✔ The checked text is never consumed.

✔ The Current Position remains unchanged.

✔ Positive Lookahead returns only Success or Failure.

✔ It is widely used for context-sensitive extraction.

---

# Key Takeaways

- Positive Lookahead verifies future text without consuming it.
- The Regex Engine performs the assertion at the Current Position.
- Successful assertions allow matching to continue.
- Failed assertions terminate the current matching attempt.
- Positive Lookahead is an essential tool for precise text extraction and validation.

---

# Coming Up

Positive Lookahead checks that specific text **must exist** ahead of the Current Position.

The next lesson introduces **Negative Lookahead**, where the Regex Engine verifies that specific text **must not exist** ahead of the Current Position.

------------------------------------------------------------------------------------------------------------

# 5.4 Negative Lookahead

## Learning Objective

After completing this lesson, you will be able to:

- Understand what Negative Lookahead is.
- Explain how the Regex Engine evaluates a Negative Lookahead.
- Understand how the Current Position is preserved.
- Distinguish between Positive and Negative Lookahead.
- Apply Negative Lookahead in real-world automation.

---

# Previous Knowledge

In the previous lesson, we learned that a Positive Lookahead verifies that specific text **must exist** after the Current Position.

Example

```regex
(?=GB)
```

Meaning

```
GB

Must Exist

Ahead
```

Now we will study the opposite behavior.

---

# Introduction

Consider the following input.

```text
Capacity=1024GB

Capacity=1024MB
```

Suppose our automation script should process

```
GB
```

values,

but ignore

```
MB
```

values.

The Regex Engine must verify that

```
MB

does NOT appear
```

after the Current Position.

This is exactly what Negative Lookahead does.

---

# Why Do We Need Negative Lookahead?

Suppose a storage log contains

```text
Drive=NVME001

Drive=TEST001

Drive=NVME002
```

The automation should ignore

```text
TEST001
```

while processing every real device.

Instead of matching everything and filtering later,

Negative Lookahead allows the Regex Engine to reject unwanted matches immediately.

---

# Definition

A **Negative Lookahead** is a Lookaround that verifies that a specified pattern **does not exist** immediately after the Current Position.

If the specified pattern is found,

the assertion fails.

If the pattern is absent,

matching continues.

The inspected text is never consumed.

---

# Syntax

General Syntax

```regex
(?!pattern)
```

Examples

```regex
(?!MB)
```

```regex
(?!ERROR)
```

```regex
(?!TEST)
```

The syntax can be read as

> "The following text **must not be** this pattern."

---

# Understanding the Current Position

Example

```text
Capacity=1024GB
         ^
```

The Regex Engine reaches the Current Position.

Instead of consuming characters,

it temporarily inspects the text ahead.

After the inspection,

it returns to exactly the same position.

---

# Regex Engine Explanation

Pattern

```regex
(?!MB)
```

Input

```text
GB
```

Regex Engine

```
Reach Current Position

↓

Encounter

(?!

↓

Read Ahead

↓

Is

MB

Present?

↓

NO

↓

Assertion Passed

↓

Return To

Current Position

↓

Continue Matching
```

Now consider

Input

```text
MB
```

Regex Engine

```
Reach Current Position

↓

Read Ahead

↓

Found

MB

↓

Assertion Failed

↓

Current Match Stops
```

---

# Regex Engine Cursor Movement

Successful Assertion

```text
GB
^

↓

Inspect Ahead

↓

GB
^
```

Failed Assertion

```text
MB
^

↓

Inspect Ahead

↓

MB
^

↓

Match Fails
```

Notice that the cursor never advances during the assertion.

---

# Engine Visualization

```
Current Position

       │
       ▼

+------------------+
|   Regex Engine   |
+------------------+

       │
       ▼

Inspect Future

       │

Pattern Found?

       │
 ┌─────┴─────┐
 │           │
 ▼           ▼

YES         NO

 │           │

 ▼           ▼

Fail      Continue

Matching
```

---

# Engine Trace

Pattern

```regex
(?!MB)
```

Input

```text
GB
```

```
Regex Engine Trace

--------------------------------------

Reach Current Position

↓

Read

(?!

↓

Inspect Future

↓

MB Found?

↓

NO

↓

Assertion Passed

↓

Return To Current Position

↓

Continue Matching

↓

SUCCESS
```

---

# Matching Matrix

Pattern

```regex
(?!MB)
```

| Future Text | Assertion Result |
|-------------|------------------|
| `GB` | ✅ Pass |
| `TB` | ✅ Pass |
| `MB` | ❌ Fail |
| `ERROR` | ✅ Pass |

---

# Compare & Contrast

| Positive Lookahead | Negative Lookahead |
|--------------------|-------------------|
| Future pattern must exist | Future pattern must not exist |
| `(?=...)` | `(?!...)` |
| Passes when found | Passes when absent |
| Consumes nothing | Consumes nothing |

---

# Real-World Usage

Negative Lookahead is useful for:

### Storage Engineering

- Ignore test devices.
- Skip unsupported firmware.
- Exclude deprecated log entries.

---

### Linux Automation

- Ignore temporary files.
- Skip commented configuration lines.
- Exclude specific command outputs.

---

### Python Automation

- Filter unwanted records.
- Exclude invalid input.
- Skip test data.

---

### Test Automation

- Ignore expected warnings.
- Exclude known failures.
- Filter unnecessary log entries.

---

# Important Observation

Negative Lookahead performs

```
Look Ahead

↓

Must NOT Exist

↓

Return

↓

Continue
```

The Regex Engine never consumes the inspected text.

Only the assertion result changes.

---

# Common Beginner Mistakes

### Mistake 1

Thinking Negative Lookahead removes text.

It does not.

It only verifies that the specified pattern is absent.

---

### Mistake 2

Thinking the Regex Engine skips characters.

The Current Position remains unchanged.

---

### Mistake 3

Confusing Negative Lookahead with Negative Character Classes.

A Character Class tests individual characters.

A Lookahead tests future context.

---

# Interview Questions

1. What is a Negative Lookahead?

2. What is the syntax of Negative Lookahead?

3. Does Negative Lookahead consume characters?

4. What happens when the forbidden pattern is found?

5. Give practical applications of Negative Lookahead.

---

# Practice Questions

### Question 1

Explain why

```regex
(?!MB)
```

passes for

```text
GB
```

but fails for

```text
MB
```

---

### Question 2

List five situations where Negative Lookahead is useful.

---

### Question 3

Explain the difference between Positive and Negative Lookahead.

---

# Memory Tip

```
Positive Lookahead

↓

Must Exist

------------------------

Negative Lookahead

↓

Must NOT Exist
```

Remember

```
(?! )

↓

Future

Must NOT Match
```

---

# Revision Box

✔ Negative Lookahead checks future text.

✔ The inspected text is never consumed.

✔ The Current Position remains unchanged.

✔ Matching continues only when the specified pattern is absent.

✔ Negative Lookahead is useful for filtering and exclusion.

---

# Key Takeaways

- Negative Lookahead verifies that specific text does not exist ahead of the Current Position.
- The Regex Engine performs the assertion without consuming characters.
- Successful assertions allow matching to continue.
- Failed assertions terminate the current matching attempt.
- Negative Lookahead is widely used for excluding unwanted matches and validating input.

---

# Coming Up

So far, both Lookaheads have inspected text **after** the Current Position.

The next lesson introduces **Positive Lookbehind**, where the Regex Engine verifies that specific text exists **before** the Current Position while still leaving the Current Position unchanged.

------------------------------------------------------------------------------------------------------------

# 5.5 Positive Lookbehind

## Learning Objective

After completing this lesson, you will be able to:

- Understand what Positive Lookbehind is.
- Explain how the Regex Engine evaluates a Positive Lookbehind.
- Understand how the Current Position remains unchanged.
- Distinguish between Positive Lookahead and Positive Lookbehind.
- Apply Positive Lookbehind in real-world automation.

---

# Previous Knowledge

In the previous lessons, we learned:

- Positive Lookahead checks text after the Current Position.
- Negative Lookahead checks that specific text does not exist after the Current Position.

Both Lookaheads inspect the **future**.

Now we will learn how the Regex Engine inspects the **past**.

---

# Introduction

Consider the following input.

```text
Capacity=1024GB
```

Suppose we want to extract

```text
1024GB
```

only if it is immediately preceded by

```text
Capacity=
```

The Regex Engine must verify that the required text exists before the Current Position.

If the verification succeeds,

matching continues.

Otherwise,

the current match fails.

---

# Why Do We Need Positive Lookbehind?

Suppose a storage log contains

```text
Capacity=1024GB

Temperature=42C

Firmware=3.5.12
```

Our automation script should extract only

```text
1024GB
```

when it follows

```text
Capacity=
```

The prefix should be verified,

but it should not become part of the final match.

Positive Lookbehind performs exactly this validation.

---

# Definition

A **Positive Lookbehind** is a Lookaround that verifies that a specified pattern exists immediately **before** the Current Position.

If the condition is satisfied,

matching continues.

Otherwise,

the current match fails.

The verified text is **not consumed**.

---

# Syntax

General Syntax

```regex
(?<=pattern)
```

Examples

```regex
(?<=Capacity=)
```

```regex
(?<=ERROR:\s)
```

```regex
(?<=Drive=)
```

The syntax can be read as

> "The preceding text must be this pattern."

---

# Understanding the Current Position

Example

```text
Capacity=1024GB
         ^
```

The Current Position is immediately before

```text
1024GB
```

The Regex Engine temporarily inspects the text before this position.

After the inspection,

it returns to exactly the same Current Position.

---

# Regex Engine Explanation

Pattern

```regex
(?<=Capacity=)
```

Input

```text
Capacity=1024GB
```

Regex Engine

```
Reach Current Position

↓

Encounter

(?<=

↓

Look Behind

↓

Is

Capacity=

Present?

↓

YES

↓

Assertion Passed

↓

Return To

Current Position

↓

Continue Matching
```

Notice that

```
Capacity=
```

is verified,

but it is never consumed.

---

# Regex Engine Cursor Movement

```
Capacity=1024GB
         ^

Current Position

↓

Inspect Behind

↓

Capacity=1024GB
         ^

Return To

Current Position
```

The cursor never moves permanently.

---

# Engine Visualization

```
Current Position

       │
       ▼

+------------------+
|   Regex Engine   |
+------------------+

       │
       ▼

Inspect Behind

       │

Pattern Found?

       │
 ┌─────┴─────┐
 │           │
 ▼           ▼

YES         NO

 │           │

 ▼           ▼

Continue    Fail

Matching
```

---

# Engine Trace

Pattern

```regex
(?<=Capacity=)
```

Input

```text
Capacity=1024GB
```

```
Regex Engine Trace

--------------------------------------

Reach Current Position

↓

Read

(?<=

↓

Inspect Previous Text

↓

Capacity=

Found

↓

Assertion Passed

↓

Return To Current Position

↓

Continue Matching

↓

SUCCESS
```

---

# Matching Matrix

Pattern

```regex
(?<=Capacity=)
```

| Previous Text | Assertion Result |
|---------------|------------------|
| `Capacity=` | ✅ Pass |
| `Temperature=` | ❌ Fail |
| `Firmware=` | ❌ Fail |
| `Drive=` | ❌ Fail |

---

# Compare & Contrast

| Positive Lookahead | Positive Lookbehind |
|--------------------|--------------------|
| Checks future text | Checks previous text |
| `(?=...)` | `(?<=...)` |
| Looks ahead | Looks behind |
| Consumes nothing | Consumes nothing |

---

# Real-World Usage

Positive Lookbehind is useful for:

### Storage Engineering

- Extract Capacity values.
- Extract Firmware versions.
- Extract Drive IDs.

---

### Linux Automation

- Extract values after configuration keys.
- Parse command output.
- Validate structured logs.

---

### Python Automation

- Extract configuration values.
- Parse reports.
- Process structured files.

---

### Test Automation

- Validate expected output.
- Extract measured values.
- Verify structured reports.

---

# Important Observation

Positive Lookbehind performs

```
Look Behind

↓

Verify

↓

Return

↓

Continue
```

The Current Position never changes.

The inspected text is never consumed.

---

# Common Beginner Mistakes

### Mistake 1

Thinking Positive Lookbehind captures previous text.

It only verifies it.

---

### Mistake 2

Thinking the Regex Engine moves backward permanently.

It always returns to the Current Position.

---

### Mistake 3

Confusing Lookbehind with Backreferences.

Lookbehind verifies surrounding context.

Backreferences reuse previously captured text.

---

# Interview Questions

1. What is a Positive Lookbehind?

2. What is the syntax of Positive Lookbehind?

3. Does Positive Lookbehind consume characters?

4. How does Positive Lookbehind differ from Positive Lookahead?

5. Give practical applications of Positive Lookbehind.

---

# Practice Questions

### Question 1

Explain why

```regex
(?<=Capacity=)
```

passes only when the previous text is

```text
Capacity=
```

---

### Question 2

List five situations where Positive Lookbehind is useful.

---

### Question 3

Explain the difference between Positive Lookahead and Positive Lookbehind.

---

# Memory Tip

```
Positive Lookahead

↓

Look Ahead

↓

Must Exist

-----------------------

Positive Lookbehind

↓

Look Behind

↓

Must Exist
```

Remember

```
(?<= )

↓

Previous Text

Must Match
```

---

# Revision Box

✔ Positive Lookbehind checks text before the Current Position.

✔ The inspected text is never consumed.

✔ The Current Position remains unchanged.

✔ Matching continues only when the required previous text exists.

✔ Positive Lookbehind is widely used for precise extraction.

---

# Key Takeaways

- Positive Lookbehind verifies previous text without consuming it.
- The Regex Engine temporarily inspects the past and then returns to the Current Position.
- Successful assertions allow matching to continue.
- Failed assertions terminate the current matching attempt.
- Positive Lookbehind is essential for context-aware extraction in automation.

---

# Coming Up

Positive Lookbehind verifies that specific text **must exist** before the Current Position.

The next lesson introduces **Negative Lookbehind**, where the Regex Engine verifies that specific text **must not exist** before the Current Position.

------------------------------------------------------------------------------------------------------------

# 5.6 Negative Lookbehind

## Learning Objective

After completing this lesson, you will be able to:

- Understand what Negative Lookbehind is.
- Explain how the Regex Engine evaluates a Negative Lookbehind.
- Understand how the Current Position remains unchanged.
- Distinguish between Positive and Negative Lookbehind.
- Apply Negative Lookbehind in real-world automation.

---

# Previous Knowledge

In the previous lesson, we learned that Positive Lookbehind verifies that specific text **must exist** before the Current Position.

Example

```regex
(?<=Capacity=)
```

Meaning

```
Capacity=

Must Exist

Before
```

Now we will study the opposite behavior.

---

# Introduction

Consider the following input.

```text
Drive=NVME001

TestDrive=NVME002
```

Suppose our automation script should process only

```text
Drive=NVME001
```

and ignore

```text
TestDrive=NVME002
```

The Regex Engine must verify that

```
Test

does NOT appear
```

before the Current Position.

This is exactly what Negative Lookbehind does.

---

# Why Do We Need Negative Lookbehind?

Suppose a log contains

```text
Device=NVME001

BackupDevice=NVME002

Device=NVME003
```

Our automation should process only

```
Device=
```

entries.

It should ignore

```
BackupDevice=
```

entries.

Instead of matching everything and filtering later,

Negative Lookbehind allows the Regex Engine to reject unwanted matches immediately.

---

# Definition

A **Negative Lookbehind** is a Lookaround that verifies that a specified pattern **does not exist** immediately before the Current Position.

If the specified pattern is found,

the assertion fails.

If the pattern is absent,

matching continues.

The inspected text is never consumed.

---

# Syntax

General Syntax

```regex
(?<!pattern)
```

Examples

```regex
(?<!Test)
```

```regex
(?<!Backup)
```

```regex
(?<!ERROR:\s)
```

The syntax can be read as

> "The preceding text must not be this pattern."

---

# Understanding the Current Position

Example

```text
Drive=NVME001
      ^
```

The Regex Engine reaches the Current Position.

Instead of consuming characters,

it temporarily inspects the text before this position.

After the inspection,

it returns to exactly the same Current Position.

---

# Regex Engine Explanation

Pattern

```regex
(?<!Test)
```

Input

```text
Drive
```

Regex Engine

```
Reach Current Position

↓

Encounter

(?<!

↓

Look Behind

↓

Is

Test

Present?

↓

NO

↓

Assertion Passed

↓

Return To

Current Position

↓

Continue Matching
```

Now consider

Input

```text
TestDrive
```

Regex Engine

```
Reach Current Position

↓

Inspect Previous Text

↓

Found

Test

↓

Assertion Failed

↓

Current Match Stops
```

---

# Regex Engine Cursor Movement

Successful Assertion

```text
Drive
^

↓

Inspect Behind

↓

Drive
^
```

Failed Assertion

```text
TestDrive
    ^

↓

Inspect Behind

↓

TestDrive
    ^

↓

Match Fails
```

The cursor always returns to the same position.

---

# Engine Visualization

```
Current Position

       │
       ▼

+------------------+
|   Regex Engine   |
+------------------+

       │
       ▼

Inspect Behind

       │

Pattern Found?

       │
 ┌─────┴─────┐
 │           │
 ▼           ▼

YES         NO

 │           │

 ▼           ▼

Fail      Continue

Matching
```

---

# Engine Trace

Pattern

```regex
(?<!Test)
```

Input

```text
Drive
```

```
Regex Engine Trace

--------------------------------------

Reach Current Position

↓

Read

(?<!

↓

Inspect Previous Text

↓

Test Found?

↓

NO

↓

Assertion Passed

↓

Return To Current Position

↓

Continue Matching

↓

SUCCESS
```

---

# Matching Matrix

Pattern

```regex
(?<!Test)
```

| Previous Text | Assertion Result |
|---------------|------------------|
| `Drive` | ✅ Pass |
| `Device` | ✅ Pass |
| `Test` | ❌ Fail |
| `Backup` | ✅ Pass |

---

# Compare & Contrast

| Positive Lookbehind | Negative Lookbehind |
|---------------------|--------------------|
| Previous pattern must exist | Previous pattern must not exist |
| `(?<=...)` | `(?<!...)` |
| Passes when found | Passes when absent |
| Consumes nothing | Consumes nothing |

---

# Real-World Usage

Negative Lookbehind is useful for:

### Storage Engineering

- Ignore test devices.
- Exclude backup entries.
- Skip deprecated log formats.

---

### Linux Automation

- Ignore commented configuration values.
- Exclude temporary entries.
- Filter unwanted records.

---

### Python Automation

- Skip test data.
- Ignore unwanted prefixes.
- Filter structured reports.

---

### Test Automation

- Ignore known failures.
- Exclude expected warnings.
- Filter irrelevant log entries.

---

# Important Observation

Negative Lookbehind performs

```
Look Behind

↓

Must NOT Exist

↓

Return

↓

Continue
```

The Regex Engine never consumes the inspected text.

The Current Position always remains unchanged.

---

# Common Beginner Mistakes

### Mistake 1

Thinking Negative Lookbehind removes previous text.

It does not.

It only verifies that the specified pattern is absent.

---

### Mistake 2

Thinking the Regex Engine moves backward permanently.

It always returns to the Current Position.

---

### Mistake 3

Confusing Negative Lookbehind with Negative Character Classes.

A Character Class checks individual characters.

A Lookbehind checks surrounding context.

---

# Interview Questions

1. What is a Negative Lookbehind?

2. What is the syntax of Negative Lookbehind?

3. Does Negative Lookbehind consume characters?

4. How does Negative Lookbehind differ from Positive Lookbehind?

5. Give practical applications of Negative Lookbehind.

---

# Practice Questions

### Question 1

Explain why

```regex
(?<!Test)
```

passes for

```text
Drive
```

but fails for

```text
TestDrive
```

---

### Question 2

List five situations where Negative Lookbehind is useful.

---

### Question 3

Explain the difference between Positive and Negative Lookbehind.

---

# Memory Tip

```
Positive Lookbehind

↓

Must Exist

------------------------

Negative Lookbehind

↓

Must NOT Exist
```

Remember

```
(?<! )

↓

Previous Text

Must NOT Match
```

---

# Revision Box

✔ Negative Lookbehind checks previous text.

✔ The inspected text is never consumed.

✔ The Current Position remains unchanged.

✔ Matching continues only when the specified previous pattern is absent.

✔ Negative Lookbehind is useful for filtering and exclusion.

---

# Key Takeaways

- Negative Lookbehind verifies that specific text does not exist before the Current Position.
- The Regex Engine performs the assertion without consuming characters.
- Successful assertions allow matching to continue.
- Failed assertions terminate the current matching attempt.
- Negative Lookbehind completes the four fundamental Lookaround assertions.

---

# Coming Up

You have now learned all four Lookaround assertions:

- Positive Lookahead
- Negative Lookahead
- Positive Lookbehind
- Negative Lookbehind

The next lesson shows how these assertions can be **combined in a single Regular Expression** to create powerful context-based validation and extraction rules for enterprise automation.

------------------------------------------------------------------------------------------------------------

# 5.7 Combining Lookarounds

## Learning Objective

After completing this lesson, you will be able to:

- Understand why multiple Lookarounds are combined.
- Explain how the Regex Engine evaluates multiple assertions.
- Apply Positive and Negative Lookarounds together.
- Understand the execution order of combined Lookarounds.
- Recognize practical applications in enterprise automation.

---

# Previous Knowledge

In the previous lessons, we learned four Lookaround assertions.

- Positive Lookahead
- Negative Lookahead
- Positive Lookbehind
- Negative Lookbehind

Each assertion checks one condition.

However,

real-world automation often requires **multiple conditions** to be verified before a match is accepted.

---

# Introduction

Consider the following input.

```text
Capacity=1024GB

Capacity=1024MB

BackupCapacity=2048GB
```

Suppose we want to match

```text
1024GB
```

only when:

- it is preceded by

```text
Capacity=
```

and

- it is **not** preceded by

```text
Backup
```

One assertion is no longer sufficient.

The Regex Engine must evaluate **multiple assertions** before matching.

---

# Why Do We Need Combined Lookarounds?

Suppose a storage log contains

```text
Drive=NVME001

TestDrive=NVME002

Drive=NVME003
```

Automation requirements:

- Accept real drives.
- Reject test drives.
- Extract only the device identifier.

Multiple assertions make this possible without consuming unwanted text.

---

# Definition

**Combined Lookarounds** use two or more Lookaround assertions in a single Regular Expression.

Each assertion is evaluated independently.

Matching continues only if **every required assertion succeeds**.

---

# General Syntax

Examples

```regex
(?<=Capacity=)\d+GB
```

```regex
(?<!Backup)(?<=Capacity=)\d+GB
```

```regex
(?!MB)(?=GB)
```

```regex
(?<=Drive=)(?!TEST)[A-Z]+\d+
```

A Regular Expression may contain any number of Lookarounds.

---

# Regex Engine Explanation

Pattern

```regex
(?<!Backup)(?<=Capacity=)\d+GB
```

Input

```text
Capacity=1024GB
```

Regex Engine

```
Reach Current Position

↓

Evaluate Assertion

↓

Inspect Behind

↓

Backup Present?

↓

NO

↓

Assertion Passed

↓

Evaluate Next Assertion

↓

Inspect Behind

↓

Capacity=

Present?

↓

YES

↓

Assertion Passed

↓

Match

1024GB

↓

SUCCESS
```

Every assertion is checked separately.

Only after all assertions succeed does the Regex Engine begin matching.

---

# Regex Engine Cursor Movement

```
Capacity=1024GB
         ^

Current Position

↓

Inspect Behind

↓

Return

↓

Inspect Behind Again

↓

Return

↓

Begin Matching

↓

1024GB
```

Notice that

the Current Position never changes while assertions are evaluated.

---

# Engine Visualization

```
Current Position

        │
        ▼

+------------------+
|   Regex Engine   |
+------------------+

        │
        ▼

Assertion 1

        │
   ┌────┴────┐
   │         │
Pass      Fail

   │
   ▼

Assertion 2

   │
┌──┴────┐
│       │
Pass   Fail

│
▼

Match Pattern
```

---

# Engine Trace

Pattern

```regex
(?<!Backup)(?<=Capacity=)\d+GB
```

Input

```text
Capacity=1024GB
```

```
Regex Engine Trace

--------------------------------------

Reach Current Position

↓

Evaluate Assertion 1

↓

PASS

↓

Return

↓

Evaluate Assertion 2

↓

PASS

↓

Return

↓

Match

1024GB

↓

SUCCESS
```

---

# Another Example

Pattern

```regex
(?<=ERROR:)(?!Timeout).*
```

Input

```text
ERROR:Disk Failure
```

Result

```
SUCCESS
```

Input

```text
ERROR:Timeout
```

Result

```
FAIL
```

One assertion checks

```
ERROR:
```

The other rejects

```
Timeout
```

---

# Assertion Execution Order

```
Assertion 1

↓

Return

↓

Assertion 2

↓

Return

↓

Assertion 3

↓

Return

↓

Begin Matching
```

Assertions do not consume characters.

They simply decide whether matching may continue.

---

# Compare & Contrast

| Single Lookaround | Combined Lookarounds |
|-------------------|----------------------|
| One condition | Multiple conditions |
| Simpler patterns | More precise validation |
| Basic filtering | Advanced context checking |

---

# Real-World Usage

Combined Lookarounds are useful for:

### Storage Engineering

- Ignore backup entries.
- Extract valid capacities.
- Validate firmware formats.

---

### Linux Automation

- Parse configuration files.
- Validate command output.
- Filter log entries.

---

### Python Automation

- Validate structured input.
- Parse reports.
- Filter unwanted records.

---

### Test Automation

- Validate output context.
- Exclude known failures.
- Verify complex report formats.

---

# Important Observation

Multiple Lookarounds behave like multiple validation rules.

Think of the Regex Engine as performing

```
Check Rule 1

↓

Check Rule 2

↓

Check Rule 3

↓

If Every Rule Passes

↓

Match
```

---

# Common Beginner Mistakes

### Mistake 1

Thinking combined Lookarounds are evaluated simultaneously.

The Regex Engine evaluates them one after another.

---

### Mistake 2

Thinking each Lookaround consumes text.

None of the assertions consume characters.

---

### Mistake 3

Writing overly complex Lookaround combinations when a simpler Regular Expression is sufficient.

---

# Interview Questions

1. Why are multiple Lookarounds combined?

2. How does the Regex Engine evaluate combined Lookarounds?

3. Does each assertion consume characters?

4. What happens if one assertion fails?

5. Give practical examples of combined Lookarounds.

---

# Practice Questions

### Question 1

Explain how

```regex
(?<!Backup)(?<=Capacity=)\d+GB
```

is evaluated.

---

### Question 2

Why does the Current Position remain unchanged while multiple assertions are evaluated?

---

### Question 3

List five real-world situations where combined Lookarounds simplify automation.

---

# Memory Tip

```
Assertion 1

↓

Assertion 2

↓

Assertion 3

↓

Match
```

Remember

```
Multiple Lookarounds

=

Multiple Rules

↓

All Must Pass
```

---

# Revision Box

✔ Multiple Lookarounds may appear in one Regular Expression.

✔ Every assertion is evaluated independently.

✔ Assertions never consume characters.

✔ The Current Position remains unchanged.

✔ Matching begins only after every required assertion succeeds.

---

# Four Lookaround Summary

| Lookaround | Syntax | Direction | Condition | Consumes Characters? |
|------------|--------|-----------|-----------|----------------------|
| Positive Lookahead | `(?=...)` | Ahead | Must Exist | ❌ |
| Negative Lookahead | `(?!...)` | Ahead | Must NOT Exist | ❌ |
| Positive Lookbehind | `(?<=...)` | Behind | Must Exist | ❌ |
| Negative Lookbehind | `(?<!...)` | Behind | Must NOT Exist | ❌ |

---

# Key Takeaways

- Multiple Lookarounds allow complex context-based validation.
- Each assertion is evaluated separately by the Regex Engine.
- Assertions do not consume characters and never change the Current Position.
- Matching begins only after all required assertions succeed.
- Combined Lookarounds are widely used in enterprise log parsing, validation and automation.

---

# Coming Up

Now that you understand how Lookarounds work individually and together,

the next lesson demonstrates **Real-World Applications of Lookarounds** in Storage Engineering, Linux Automation, Python Automation and enterprise log parsing, showing how these assertions are used in production automation.

------------------------------------------------------------------------------------------------------------

# 5.8 Real-World Applications of Lookarounds

## Learning Objective

After completing this lesson, you will be able to:

- Understand where Lookarounds are used in real-world software development.
- Apply Lookarounds for extraction and validation.
- Recognize situations where Lookarounds simplify automation.
- Understand the role of Lookarounds in enterprise log processing.
- Apply Lookarounds in Storage Engineering, Linux Automation and Python Automation.

---

# Introduction

Lookarounds are one of the most useful Regex features for automation.

Unlike ordinary matching,

Lookarounds allow the Regex Engine to verify surrounding context

without making that context part of the final match.

This makes extraction cleaner,

validation more precise,

and automation scripts easier to maintain.

---

# Application 1 — Storage Capacity Extraction

Storage Log

```text
Drive=NVME001

Capacity=2048GB

Temperature=42C
```

Regex

```regex
(?<=Capacity=)\d+GB
```

Match

```text
2048GB
```

Applications

- Capacity Validation
- Report Generation
- Storage Monitoring

---

# Application 2 — Firmware Version Extraction

Input

```text
Firmware=3.5.12
```

Regex

```regex
(?<=Firmware=)\d+\.\d+\.\d+
```

Match

```text
3.5.12
```

Applications

- Firmware Validation
- Upgrade Verification
- Compliance Reports

---

# Application 3 — Linux Configuration Parsing

Configuration File

```text
HOST=10.10.20.15

PORT=8080
```

Regex

```regex
(?<=HOST=)\d+\.\d+\.\d+\.\d+
```

Match

```text
10.10.20.15
```

Applications

- Configuration Validation
- Network Automation
- Deployment Scripts

---

# Application 4 — Linux Command Output

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
(?<=inet\s)\d+\.\d+\.\d+\.\d+
```

Match

```text
192.168.1.25
```

Applications

- IP Extraction
- Network Monitoring
- Automation Scripts

---

# Application 5 — Log Processing

Log

```text
ERROR: Drive Timeout

WARNING: Temperature High
```

Regex

```regex
(?<=ERROR:\s).*
```

Match

```text
Drive Timeout
```

Applications

- Error Analysis
- Failure Reports
- Alert Generation

---

# Application 6 — Ignoring Test Devices

Storage Log

```text
Drive=NVME001

TestDrive=NVME002

Drive=NVME003
```

Regex

```regex
(?<!Test)Drive=[A-Z]+\d+
```

Matches

```text
Drive=NVME001

Drive=NVME003
```

Applications

- Ignore Test Data
- Production Validation
- Automation Filtering

---

# Application 7 — Filtering Unsupported Units

Input

```text
1024GB

1024MB

2048GB
```

Regex

```regex
\d+(?!MB)
```

Applications

- Capacity Validation
- Unit Verification
- Storage Reports

---

# Application 8 — Password Validation

Requirement

```
Password

Must Contain

Digit

Uppercase

Lowercase

Special Character
```

Regex

```regex
(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=])
```

Applications

- User Authentication
- Security Validation
- Login Systems

---

# Application 9 — Python Automation

Python frequently uses Lookarounds while processing

- Log Files
- Configuration Files
- Reports
- Command Output

Typical workflow

```
Read File

↓

Apply Regex

↓

Extract Required Values

↓

Generate Report
```

We will implement these examples in **Chapter 6 — Python `re` Module**.

---

# Application 10 — Test Automation

Test Report

```text
Execution Time=12.45

Status=PASS
```

Regex

```regex
(?<=Status=)[A-Z]+
```

Match

```text
PASS
```

Applications

- Report Validation
- Automated Assertions
- Result Processing

---

# Summary of Applications

| Domain | Typical Use of Lookarounds |
|---------|----------------------------|
| Storage Engineering | Capacity, Firmware, Health |
| Linux Automation | IPs, Configurations, Logs |
| Python Automation | Parsing, Validation, Reports |
| Test Automation | Results, Assertions, Reports |
| Security | Password Validation |
| Networking | IP Addresses, Configuration Parsing |

---

# Regex Engine Perspective

Lookarounds transform the matching process into

```
Reach Current Position

↓

Evaluate Assertion(s)

↓

Assertion Passed?

│
├── Yes → Continue Matching
│
└── No → Current Match Fails

↓

Return Required Match
```

The Regex Engine always verifies the surrounding context

before deciding whether matching should continue.

---

# Important Observation

Lookarounds are ideal when

```
Context Matters

↓

But

Context

Should NOT

Appear

In The Final Match
```

This is why they are used extensively in enterprise automation.

---

# Common Beginner Mistakes

### Mistake 1

Using Capturing Groups when only context verification is required.

Lookarounds often provide a cleaner solution.

---

### Mistake 2

Thinking Lookarounds replace Groups.

Groups capture data.

Lookarounds verify context.

Both serve different purposes.

---

### Mistake 3

Ignoring Lookarounds because the syntax appears unfamiliar.

Most enterprise Regular Expressions become much simpler once Lookarounds are understood.

---

# Interview Questions

1. Where are Lookarounds used in Storage Engineering?

2. Why are Lookarounds useful in Linux Automation?

3. Explain how Lookarounds simplify log parsing.

4. Why are Lookarounds commonly used for password validation?

5. Give five practical applications of Lookarounds.

---

# Practice Questions

### Question 1

List five situations where Positive Lookbehind simplifies automation.

---

### Question 2

Explain how Negative Lookahead helps filter unwanted data.

---

### Question 3

Describe three enterprise applications of combined Lookarounds.

---

# Memory Tip

```
Lookaround

↓

Verify Context

↓

Do Not Consume

↓

Continue

↓

Match
```

Remember

```
Real Automation

=

Lookarounds

+

Context Validation
```

---

# Revision Box

✔ Lookarounds verify surrounding context.

✔ They never consume inspected text.

✔ They simplify extraction and validation.

✔ Storage Engineering frequently uses Lookarounds for log parsing.

✔ Linux Automation uses Lookarounds for configuration and command output processing.

✔ Password validation commonly combines multiple Lookaheads.

---

# Key Takeaways

- Lookarounds are widely used in enterprise automation.
- They allow precise context-based extraction and validation.
- Storage Engineering, Linux Automation, Python Automation and Test Automation all benefit from Lookarounds.
- Combining multiple Lookarounds enables sophisticated validation rules.
- Understanding Lookarounds is essential before implementing Regex in Python.

---

# Coming Up

The next lesson concludes **Chapter 5** with a comprehensive revision guide containing:

- Complete Lookaround comparison tables
- Assertion flow diagrams
- Regex Engine decision trees
- Common mistakes
- Interview questions
- Chapter mind map
- One-page revision sheet

This summary will serve as your primary revision material before moving to **Chapter 6 — Python `re` Module**.

------------------------------------------------------------------------------------------------------------

# 5.9 Chapter Summary

## Chapter Overview

In this chapter, we learned one of the most advanced concepts in Regular Expressions:

**Lookarounds**.

Unlike Character Classes, Quantifiers and Groups,

Lookarounds do **not** match characters.

Instead,

they verify the surrounding context before allowing the Regex Engine to continue matching.

The biggest idea of this chapter is

```
Check Context

↓

Do Not Consume

↓

Continue

or

Fail
```

---

# Lookaround Comparison Table

| Lookaround | Syntax | Direction | Condition | Consumes Characters? |
|------------|--------|-----------|-----------|----------------------|
| Positive Lookahead | `(?=pattern)` | Ahead | Must Exist | ❌ |
| Negative Lookahead | `(?!pattern)` | Ahead | Must NOT Exist | ❌ |
| Positive Lookbehind | `(?<=pattern)` | Behind | Must Exist | ❌ |
| Negative Lookbehind | `(?<!pattern)` | Behind | Must NOT Exist | ❌ |

---

# Lookaround Decision Tree

```
Need Context?

        │
        ▼

Need Future?

   │
┌──┴────┐
│       │
YES     NO
│        │
▼        ▼

Must Exist?     Need Previous

│               │

├── YES         ├── YES

│               │

▼               ▼

(?= )         (?<= )

│               │

└── NO          └── NO

    │               │

    ▼               ▼

   (?! )         (?<! )
```

---

# Regex Engine Flow

```
Reach Current Position

        │

        ▼

Evaluate Assertion

        │

        ▼

Inspect Context

        │

        ▼

Condition Satisfied?

        │
   ┌────┴─────┐
   │          │
 YES         NO

   │          │

   ▼          ▼

Continue    Match Fails

Matching
```

---

# Regex Engine Cursor Movement

```
Current Position

↓

Inspect

Ahead

or

Behind

↓

Return

↓

Current Position

↓

Begin Matching
```

The cursor always returns to the same position.

---

# Assertion Flow

```
Lookaround

↓

Inspect Context

↓

Consume Nothing

↓

Decision

↓

Continue

or

Fail
```

---

# Lookahead vs Lookbehind

| Lookahead | Lookbehind |
|------------|------------|
| Checks future text | Checks previous text |
| Looks ahead | Looks behind |
| Cursor returns | Cursor returns |
| No characters consumed | No characters consumed |

---

# Positive vs Negative

| Positive | Negative |
|-----------|-----------|
| Required pattern must exist | Required pattern must not exist |
| Success when found | Success when absent |

---

# Complete Memory Sheet

```
(?= )

↓

Future

Must Exist

------------------------

(?! )

↓

Future

Must NOT Exist

------------------------

(?<= )

↓

Past

Must Exist

------------------------

(?<! )

↓

Past

Must NOT Exist
```

---

# Combined Lookarounds

```
Assertion 1

↓

PASS

↓

Assertion 2

↓

PASS

↓

Assertion 3

↓

PASS

↓

Begin Matching
```

Every assertion must succeed.

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

Current Position

        │

        ▼

Evaluate Lookaround

        │
   ┌────┴─────┐
   │          │
 PASS       FAIL

   │

   ▼

Next Assertion?

        │
   ┌────┴─────┐
   │          │
 YES         NO

   │

   ▼

Evaluate Next

        │

        ▼

Begin Matching
```

---

# Real-World Applications

### Storage Engineering

- Capacity Extraction
- Firmware Validation
- Device Validation
- Storage Log Parsing

---

### Linux Automation

- Configuration Parsing
- Command Output
- IP Address Extraction
- Filesystem Validation

---

### Python Automation

- Log Processing
- Report Parsing
- Configuration Files
- Data Extraction

---

### Test Automation

- Report Validation
- Output Verification
- Context Checking
- Password Validation

---

# Common Beginner Mistakes

❌ Thinking Lookarounds match characters.

❌ Thinking Lookarounds consume text.

❌ Forgetting that the Current Position remains unchanged.

❌ Using Groups when only context verification is required.

❌ Confusing Lookahead with Lookbehind.

❌ Confusing Positive and Negative assertions.

---

# Common Interview Questions

1. What is a Lookaround?

2. Why are Lookarounds called assertions?

3. Difference between Positive and Negative Lookahead.

4. Difference between Lookahead and Lookbehind.

5. Does a Lookaround consume characters?

6. What is the Current Position?

7. How does the Regex Engine evaluate a Lookaround?

8. How are multiple Lookarounds evaluated?

9. Give practical applications of Lookarounds.

10. Why are Lookarounds useful in automation?

---

# One-Page Revision

```
Lookarounds

↓

Assertions

↓

Inspect Context

↓

Do Not Consume

↓

Return

↓

Continue

or

Fail
```

---

# Chapter Mind Map

```
Lookarounds

│

├── Fundamentals
│      ├── Why Lookarounds
│      └── What is a Lookaround
│
├── Lookahead
│      ├── Positive
│      └── Negative
│
├── Lookbehind
│      ├── Positive
│      └── Negative
│
├── Advanced
│      ├── Combining Lookarounds
│      └── Engine Evaluation
│
└── Applications
       ├── Storage
       ├── Linux
       ├── Python
       ├── Testing
       └── Security
```

---

# Final Assessment

## Theory

1. Explain Positive Lookahead.

2. Explain Negative Lookahead.

3. Explain Positive Lookbehind.

4. Explain Negative Lookbehind.

5. Explain Combined Lookarounds.

6. Explain how the Regex Engine evaluates Lookarounds.

---

## Practical

Write Regular Expressions for:

- Extract Capacity after `Capacity=`
- Extract Firmware after `Firmware=`
- Ignore Test devices
- Validate Configuration Entries
- Extract IP Addresses
- Validate Password Rules
- Parse Linux Command Output
- Extract Log Messages
- Validate Storage Reports
- Filter Unwanted Records

---

# Chapter Completion Checklist

- [ ] I understand why Lookarounds are needed.
- [ ] I understand the Current Position.
- [ ] I understand Positive Lookahead.
- [ ] I understand Negative Lookahead.
- [ ] I understand Positive Lookbehind.
- [ ] I understand Negative Lookbehind.
- [ ] I understand Combined Lookarounds.
- [ ] I can explain how the Regex Engine evaluates assertions.
- [ ] I can apply Lookarounds in automation.
- [ ] I can explain Lookarounds in interviews.

---

# Chapter Completion

Congratulations!

You have completed **Chapter 5 — Lookarounds**.

You now understand:

- Why Lookarounds exist
- Assertions
- Current Position
- Positive Lookahead
- Negative Lookahead
- Positive Lookbehind
- Negative Lookbehind
- Combined Lookarounds
- Enterprise applications of Lookarounds

These concepts allow you to build precise, context-aware Regular Expressions that are widely used in enterprise automation, validation and log processing.

The next chapter introduces **Chapter 6 — Python `re` Module**, where you will begin writing and executing Regular Expressions in Python using the standard `re` library.

------------------------------------------------------------------------------------------------------------
