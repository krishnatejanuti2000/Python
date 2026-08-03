# Advanced `re.sub()`

## Overview

`re.sub()` searches for a regular expression pattern and replaces every match with the specified replacement.

Unlike `str.replace()`, `re.sub()` supports **Regular Expressions**, **Capturing Groups**, **Named Groups**, and **Callback Functions**.

---

# Syntax

```python
re.sub(pattern, replacement, string, count=0, flags=0)
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `pattern` | Regular expression pattern |
| `replacement` | Replacement string or callback function |
| `string` | Input string |
| `count` | Maximum number of replacements (Default: 0 = replace all) |
| `flags` | Regular expression flags (optional) |

---

# Return Value

Returns a **new string** after performing all replacements.

> **Note:** Python strings are immutable, so the original string is never modified.

---

# Why `re.sub()`?

## `str.replace()`

Works only with exact text.

```python
text = "Disk100 Disk200"

print(text.replace("100", "X"))
```

Output

```
DiskX Disk200
```

---

## `re.sub()`

Works with patterns.

```python
import re

text = "Disk100 Disk200"

result = re.sub(r"\d+", "X", text)

print(result)
```

Output

```
DiskX DiskX
```

---

# Fixed Replacement

Replace every digit with `"***"`.

```python
import re

text = "Order-123 Order-456 Order-789"

result = re.sub(r"\d+", "***", text)

print(result)
```

Output

```
Order-*** Order-*** Order-***
```

---

# Using Capturing Groups

Captured values can be reused in the replacement string.

```python
import re

text = "Rahul 85"

result = re.sub(
    r"(\w+)\s+(\d+)",
    r"\1 scored \2 marks",
    text
)

print(result)
```

Output

```
Rahul scored 85 marks
```

---

# Numbered Backreferences

| Syntax | Meaning |
|--------|---------|
| `\1` | First captured group |
| `\2` | Second captured group |
| `\3` | Third captured group |

Example

```python
import re

text = "Drive01 2048"

result = re.sub(
    r"(\w+)\s+(\d+)",
    r"Device=\1 Capacity=\2GB",
    text
)

print(result)
```

Output

```
Device=Drive01 Capacity=2048GB
```

---

# Using Named Groups

Named groups improve readability.

```python
import re

text = """Rahul 85
Priya 90
Amit 78"""

result = re.sub(
    r"(?P<name>[A-Za-z]+)\s+(?P<marks>\d+)",
    r"\g<name> scored \g<marks> marks",
    text
)

print(result)
```

Output

```
Rahul scored 85 marks
Priya scored 90 marks
Amit scored 78 marks
```

---

# Named Backreference Syntax

```
\g<group_name>
```

Examples

```
\g<name>
\g<marks>
```

---

# Callback Functions

Instead of a replacement string, a callback function can be provided.

The callback function is executed once for every regex match.

---

## Syntax

```python
def replace(match):
    return replacement

re.sub(pattern, replace, string)
```

---

## Example

```python
import re

def replace(match):
    return match.group(0).upper()

text = """Rahul
Priya
Amit"""

result = re.sub(
    r"[A-Za-z]+",
    replace,
    text
)

print(result)
```

Output

```
RAHUL
PRIYA
AMIT
```

---

# Using Capturing Groups Inside Callback

```python
import re

def replace(match):

    name = match.group(1)

    return name.upper()

text = """Rahul
Priya
Amit"""

result = re.sub(
    r"([A-Za-z]+)",
    replace,
    text
)

print(result)
```

Output

```
RAHUL
PRIYA
AMIT
```

---

# Match Object Methods

Inside a callback function, the parameter is a Match object.

```python
match.group(0)
```

Returns the complete matched text.

```python
match.group(1)
```

Returns the first captured group.

```python
match.group("name")
```

Returns the named captured group.

---

# Callback Execution Flow

```
Regex finds a match
        ↓
Calls callback function
        ↓
Function receives Match object
        ↓
Processes the match
        ↓
Returns replacement text
        ↓
Regex inserts returned value
        ↓
Continues searching for the next match
```

If there are **N matches**, the callback function is called **N times**.

---

# Difference Between `replace()` and `re.sub()`

| `str.replace()` | `re.sub()` |
|-----------------|------------|
| Exact string replacement | Pattern-based replacement |
| No regex support | Full regex support |
| Static replacement | Static or dynamic replacement |
| No capturing groups | Supports capturing groups |
| No callback functions | Supports callback functions |

---

# Common Use Cases

- Log sanitization
- Data cleaning
- Report generation
- Configuration updates
- Text formatting
- Storage log normalization
- Automation scripts
- Data transformation

---

# Best Practices

- Use raw strings (`r""`) for regex patterns.
- Use **Named Groups** for better readability.
- Use callback functions when replacement depends on matched data.
- Prefer meaningful group names such as `device`, `capacity`, and `status`.

---

# Interview Questions

## Q1. What is `re.sub()`?

`re.sub()` searches for a regex pattern and replaces every match with a replacement string or callback function.

---

## Q2. Does `re.sub()` modify the original string?

No.

It returns a new string.

---

## Q3. What is the difference between `replace()` and `re.sub()`?

`replace()` performs exact string replacement.

`re.sub()` performs pattern-based replacement using regular expressions.

---

## Q4. What is `\1`?

It refers to the first captured group in the replacement string.

---

## Q5. What is `\g<name>`?

It refers to a named captured group in the replacement string.

---

## Q6. When should callback functions be used?

Use callback functions when the replacement depends on the matched content, such as conditional logic, formatting, calculations, or masking sensitive information.

---

## Key Takeaways

- `re.sub()` performs pattern-based replacement.
- Supports numbered and named backreferences.
- Callback functions enable dynamic replacements.
- The callback receives a Match object.
- Callback functions are executed once per regex match.
- `re.sub()` always returns a new string.
