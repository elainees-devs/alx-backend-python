# Unit Tests for `utils` and `client` Modules

## Description

This repository contains unit tests for utility functions in the `utils` module and the `GithubOrgClient` class in the `client` module.
These tests validate nested dictionary access, HTTP JSON fetching, and GitHub organization data handling with license filtering.

---

## ✅ `access_nested_map`

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

## 🐙 `GithubOrgClient` (`client.py`)

### Purpose

To test the `GithubOrgClient` class, which interacts with the GitHub API to retrieve organization data and list public repositories, optionally filtered by license.

### Test Cases

| Method              | What is tested                                                                 |
| ------------------- | ------------------------------------------------------------------------------ |
| `org`               | That it returns correct organization data from the API (mocked).               |
| `_public_repos_url` | That it correctly extracts the repos URL from the org payload.                 |
| `repos_payload`     | That it returns the JSON list of repos from the repos URL (mocked).            |
| `public_repos`      | That it correctly lists repo names, and filters repos when a license is given. |
| `has_license`       | That it returns True only when the repo contains the expected license key.     |

---

### Mocking Strategy

* Patch `utils.get_json` to avoid real API calls.
* Patch/memoize properties when necessary to test isolated logic.
* Use `parameterized` to test `has_license` with multiple scenarios.

---

### Example Test Implementation

```python
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

class TestGithubOrgClient(unittest.TestCase):
    @patch('client.get_json')
    def test_org(self, mock_get_json):
        mock_get_json.return_value = {"login": "test-org"}
        client = GithubOrgClient("test-org")
        self.assertEqual(client.org, {"login": "test-org"})
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        mock_get_json.side_effect = [
            {"repos_url": "https://api.github.com/orgs/test-org/repos"},
            [
                {"name": "repo1", "license": {"key": "mit"}},
                {"name": "repo2", "license": {"key": "apache-2.0"}},
            ],
        ]
        client = GithubOrgClient("test-org")
        repos = client.public_repos()
        self.assertIn("repo1", repos)
        self.assertIn("repo2", repos)

    @parameterized.expand([
        ({"license": {"key": "mit"}}, "mit", True),
        ({"license": {"key": "apache-2.0"}}, "mit", False),
        ({}, "mit", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)
```

---

## 🧪 Running the Tests

```bash
python3 -m unittest test_utils.py
python3 -m unittest test_client.py
```

---