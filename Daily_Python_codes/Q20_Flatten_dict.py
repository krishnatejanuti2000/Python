def flatten_dict(data, prefix=""):
    result = {}

    for key, value in data.items():

        if prefix:
            new_key = prefix + "." + key
        else:
            new_key = key

        if isinstance(value, dict):
            nested_result = flatten_dict(value, new_key)
            result.update(nested_result)
        else:
            result[new_key] = value

    return result

data = {"a": {"b": 10,"c": {"d": 20}},"k1": 100,"k2": {"x": 300,"y": 400}}
result = flatten_dict(data)

print(result)