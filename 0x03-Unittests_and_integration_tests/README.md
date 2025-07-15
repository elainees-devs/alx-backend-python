---

# Unit Tests for `utils` Module

## Description

This repository contains unit tests for utility functions found in the `utils` module. These tests validate the behavior of nested dictionary access and HTTP JSON fetching functions.

---

## ✅ `access_nested_map`

### Purpose

To verify that the `access_nested_map` function correctly retrieves values from nested dictionaries using a specified path and raises `KeyError` when necessary.

### Test Cases

#### ✅ Valid Inputs

| `nested_map`      | `path`       | Expected Result |
| ----------------- | ------------ | --------------- |
| `{"a": 1}`        | `("a",)`     | `1`             |
| `{"a": {"b": 2}}` | `("a",)`     | `{"b": 2}`      |
| `{"a": {"b": 2}}` | `("a", "b")` | `2`             |

#### ❌ Invalid Inputs (Expect `KeyError`)

| `nested_map` | `path`       | Expected Exception |
| ------------ | ------------ | ------------------ |
| `{}`         | `("a",)`     | `KeyError: 'a'`    |
| `{"a": 1}`   | `("a", "b")` | `KeyError: 'b'`    |

### Example Test Implementation

```python
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

## 🌐 `get_json`

### Purpose

To ensure that `get_json` correctly performs an HTTP GET request and returns the parsed JSON response. External calls are mocked using `unittest.mock`.

### Test Cases

| `url`                   | `mocked json()`      |
| ----------------------- | -------------------- |
| `"http://example.com"`  | `{"payload": True}`  |
| `"http://holberton.io"` | `{"payload": False}` |

### Mocking Strategy

* `requests.get` is patched to prevent real HTTP calls.
* A `Mock` object with a `json()` method is returned.
* Assert that `requests.get` was called exactly once per test case.
* Assert that the returned value equals the expected payload.

### Example Test Implementation

```python
@parameterized.expand([
    ("http://example.com", {"payload": True}),
    ("http://holberton.io", {"payload": False}),
])
@patch("utils.requests.get")
def test_get_json(self, test_url, test_payload, mock_get):
    mock_response = Mock()
    mock_response.json.return_value = test_payload
    mock_get.return_value = mock_response

    result = get_json(test_url)

    mock_get.assert_called_once_with(test_url)
    self.assertEqual(result, test_payload)
```

---

## 🧪 Running the Tests

```bash
python3 -m unittest test_utils.py
```

---


