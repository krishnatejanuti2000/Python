"""
Given two dictionaries, create a result dictionary.
Rules:
- Key exists only in d1 → keep d1 value.
- Key exists only in d2 → keep d2 value.
- Key exists in both:
  - integer + integer → add
  - string + string → concatenate
  - incompatible types → report the problem and do not overwrite the existing value.
"""
d1 = {'a': 1, 'b': 'hello', 'c': 3}
d2 = {'b': 'hi', 'c': 2, 'd': 8}

result = {}

for key in d1:
    result[key] = d1[key]

for key in d2:

    if key in result:

        if type(result[key]) == int and type(d2[key]) == int:
            result[key] = result[key] + d2[key]

        elif type(result[key]) == str and type(d2[key]) == str:
            result[key] = result[key] + d2[key]

        else:
            print("Incompatible data types for key:", key)

    else:
        result[key] = d2[key]

print(result)