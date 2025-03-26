# SCOPE Tests

This directory contains tests for the SCOPE project.

## Running Tests

To run tests, use the following command from the project root:

```bash
python -m pytest
```

Or to run a specific test file:

```bash
python -m pytest tests/test_utils.py
```

## Test Coverage

Currently implemented tests:

- `test_utils.py`: Tests for utility functions in the `scope.utils` package
  - Tests for `find_file` function
  - Tests for `find_column_by_pattern` function

## Adding New Tests

When adding new functionality, please add corresponding tests. All test files should be prefixed with `test_` to be automatically discovered by pytest.
