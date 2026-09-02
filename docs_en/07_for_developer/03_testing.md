# How to run tests

This project provides unit tests based on pytest.

## Test directory structure

```
tests/
├── __init__.py
├── conftest.py          # Common pytest settings and fixtures
├── unit/                # Unit tests
│   ├── __init__.py
│   ├── test_gurobi_config.py          # Tests for Gurobi configuration parameters
│   ├── test_name_ascii_validation.py  # Tests for the ASCII check of the "name" column
│   └── ...                            # Other unit tests
└── integration/         # Integration tests
    ├── __init__.py
    ├── test_data_mini_integration.py  # Connectivity test using data-mini
    └── ...                            # Other integration tests
```

## How to run tests

### Run all tests

```bash
poetry run pytest tests/ -v
```

Or use the poethepoet task:

```bash
poe test
```

### Run a specific test file

```bash
# Unit test
poetry run pytest tests/unit/test_gurobi_config.py -v

# Integration test
poetry run pytest tests/integration/test_data_mini_integration.py -v
```

### Run with a coverage report

```bash
poetry run pytest tests/ --cov=ucgrb --cov-report=html --cov-report=term
```

Or use the poethepoet task:

```bash
poe test-cov
```

The coverage report is generated at `htmlcov/index.html`.

### Run a specific test class or test function

```bash
# Specify a test class
poetry run pytest tests/unit/test_gurobi_config.py::TestGetPhysicalMemoryGB -v

# Specify a test function
poetry run pytest tests/unit/test_gurobi_config.py::TestGetPhysicalMemoryGB::test_get_physical_memory_gb_windows -v
```

### Run tests using markers

You can use pytest markers to run only a specific kind of test.

```bash
# Run unit tests only
poetry run pytest tests/ -m unit -v

# Run integration tests only
poetry run pytest tests/ -m integration -v

# Skip time-consuming tests
poetry run pytest tests/ -m "not slow" -v
```

## How to add new tests

### Adding a unit test

1. Create a new test file in the `tests/unit/` directory.
2. Name the file in the `test_*.py` format.
3. Begin the test class name with `Test`.
4. Begin the test function name with `test_`.
5. Add the `@pytest.mark.unit` marker (optional).

Example:

```python
# tests/unit/test_example.py
import pytest

@pytest.mark.unit
class TestExample:
    def test_example_function(self):
        assert True
```

### Adding an integration test

1. Create a new test file in the `tests/integration/` directory.
2. Name the file in the `test_*.py` format.
3. Begin the test class name with `Test`.
4. Begin the test function name with `test_`.
5. Add the `@pytest.mark.integration` marker.
6. If it is time-consuming, also add `@pytest.mark.slow`.

Example:

```python
# tests/integration/test_example_integration.py
import pytest

@pytest.mark.integration
class TestExampleIntegration:
    @pytest.mark.slow
    def test_example_integration(self):
        # Integration test using actual data
        assert True
```

## pytest configuration

The pytest configuration is written in the `[tool.pytest.ini_options]` section of `pyproject.toml`.

- `testpaths`: Search paths for test files
- `python_files`: Naming convention for test files
- `python_classes`: Naming convention for test classes
- `python_functions`: Naming convention for test functions
- `markers`: Available markers
