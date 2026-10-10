d1 = {'a': 1, 'b': 'hello', 'c': 3}
d2 = {'b': 'hi', 'c': 2, 'd': 8}

result = {}

for i in d1:
    result[i] = d1[i]

for i in d2:
    if i in result:
        if type(result[i]) == int and type(d2[i]) == int:
            result[i] = result[i]+d2[i]
        elif type(result[i]) == str and type(d2[i]) == str:
            result [i] = result[i]+ " "+d2[i]
        else:
            print(f"Incompatible data types for key : {i}")
    else:
        result[i] = d2[i]

print(result)


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