Here’s the updated `README` with the new exception test section included:

---

# Unit Test for `access_nested_map` Function

## Description

This task involves writing unit tests for the `access_nested_map` function from the `utils` module. The goal is to verify that the function correctly retrieves values from nested dictionaries using a specified path and raises appropriate exceptions when the path is invalid.

## Objective

* Create a unit test class `TestAccessNestedMap` that inherits from `unittest.TestCase`.
* Use the `@parameterized.expand` decorator to test the function with multiple input scenarios.
* Use `assertEqual` to check correct outputs and `assertRaises` to check exceptions.
* Keep the test body concise (maximum of 2 lines per test).

## Requirements

### Test Cases

#### Valid Inputs

| `nested_map`      | `path`       | Expected Result |
| ----------------- | ------------ | --------------- |
| `{"a": 1}`        | `("a",)`     | `1`             |
| `{"a": {"b": 2}}` | `("a",)`     | `{"b": 2}`      |
| `{"a": {"b": 2}}` | `("a", "b")` | `2`             |

#### Invalid Inputs (Should Raise `KeyError`)

| `nested_map` | `path`       | Expected Exception |
| ------------ | ------------ | ------------------ |
| `{}`         | `("a",)`     | `KeyError: 'a'`    |
| `{"a": 1}`   | `("a", "b")` | `KeyError: 'b'`    |

## Example Implementation

```python
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(path[len(nested_map):][0]))
```

---

### You can now run:

```bash
python3 -m unittest test_utils.py
```

