# Unit Test for `access_nested_map` Function

## Description

This task involves writing a unit test for the `access_nested_map` function from the `utils` module. The goal is to verify that the function correctly retrieves values from nested dictionaries using a specified path.

## Objective

- Create a unit test class `TestAccessNestedMap` that inherits from `unittest.TestCase`.
- Use the `@parameterized.expand` decorator to test the function with multiple input scenarios.
- Ensure each test case uses `assertEqual` to check the output.
- Keep the test body concise (maximum of 2 lines).

## Requirements

### Test Cases

The following inputs are to be tested:

| `nested_map`              | `path`       | Expected Result |
|--------------------------|--------------|------------------|
| `{"a": 1}`               | `("a",)`     | `1`              |
| `{"a": {"b": 2}}`        | `("a",)`     | `{"b": 2}`       |
| `{"a": {"b": 2}}`        | `("a", "b")` | `2`              |

### Example Implementation

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
