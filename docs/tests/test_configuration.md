# Test Configuration

## Writing New Tests

- Tests are located in the `tests` directory
- All tests have a leading `test_` to the function and/or class - following the `pytest` convention

## Running Tests

Simply run the following command to run all tests:

```bash
uv run pytest -v tests (--cov=recipes)
```

For a full test suite, including pre-commit checks, dependency updates, package building, and test coverage reporting, run the following command:

```bash
make test
```

![make-test](../assets/make-test.png)
