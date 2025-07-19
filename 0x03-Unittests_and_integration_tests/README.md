# 📦 0x03 - Unittests and Integration Tests

This project is part of the **ALX Backend Specialization** and focuses on writing **unit tests** and **integration tests** in Python using the `unittest` module and `unittest.mock`. It also introduces techniques for mocking external API calls and building fixtures for robust test suites.

---

## 📚 Learning Objectives

By completing this project, you will be able to:

- Understand the difference between unit and integration tests.
- Write unit tests using `unittest`.
- Use `unittest.mock` to isolate units under test.
- Patch objects, methods, and requests.
- Implement integration tests by only mocking external services.
- Organize fixtures and reuse them across tests.

---

## 🧠 Core Concepts

### 🔸 Unit Testing
- Tests isolated parts of the application logic.
- Uses `@patch` decorators or context managers to mock external dependencies.
- Example:
  ```python
  @patch('utils.get_json')
  def test_fetch_data(self, mock_get_json):
      mock_get_json.return_value = {"payload": True}
      self.assertEqual(get_json("http://example.com"), {"payload": True})

Sure! Here's the complete README.md content in one copy-pasteable block for your project:


---

# 📦 0x03 - Unittests and Integration Tests

This project is part of the **ALX Backend Specialization** and focuses on writing **unit tests** and **integration tests** in Python using the `unittest` module and `unittest.mock`. It also introduces techniques for mocking external API calls and building fixtures for robust test suites.

---

## 📚 Learning Objectives

By completing this project, you will be able to:

- Understand the difference between unit and integration tests.
- Write unit tests using `unittest`.
- Use `unittest.mock` to isolate units under test.
- Patch objects, methods, and requests.
- Implement integration tests by only mocking external services.
- Organize fixtures and reuse them across tests.

---

## 🧪 Project Structure

alx-backend-python/ └── 0x03-Unittests_and_integration_tests/ ├── client.py            # Contains GithubOrgClient class for GitHub API calls ├── fixtures.py          # Static data used for integration testing ├── test_client.py       # Unit and integration tests for GithubOrgClient ├── utils.py             # Utility functions for JSON retrieval ├── test_utils.py        # Unit tests for utils.py └── README.md            # Project documentation

---

## 🧠 Core Concepts

### 🔸 Unit Testing
- Tests isolated parts of the application logic.
- Uses `@patch` decorators or context managers to mock external dependencies.
- Example:
  ```python
  @patch('utils.get_json')
  def test_fetch_data(self, mock_get_json):
      mock_get_json.return_value = {"payload": True}
      self.assertEqual(get_json("http://example.com"), {"payload": True})

## 🔸 Integration Testing

- Tests the interaction between components.
- Only mocks external services (e.g., requests.get) to simulate real scenarios.


## 🔸 Fixtures

- Reusable test data defined in fixtures.py.
- Used to parameterize integration tests for multiple scenarios.


---

# 🔧 Setup & Usage

## ✅ Requirements

- Python 3.8+

- requests

- parameterized


- __You can install dependencies using pip:__

`
pip install requests parameterized
`


---

## 🚀 Running the Tests

* From the root of the project, run:

    `
    python3 -m unittest discover 0x03-Unittests_and_integration_tests/
    `
* To run a specific file:
```
python3 0x03-Unittests_and_integration_tests/test_utils.py
python3 0x03-Unittests_and_integration_tests/test_client.py
```


---

## 🧾 Files Description

| File | Description |
|---|:---|
| utils.py | Contains helper functions like get_json() |
| client.py | Implements GithubOrgClient, which interfaces with GitHub’s API |
| fixtures.py |	Contains static JSON-like objects used for integration test simulation | 
| test_utils.py | Unit tests for utility functions |
| test_client.py| Unit & integration tests for GithubOrgClient using mocks and patching |
