# 1. **Degiro Connector : Tests**

This document is here to explain how to use tests inside the library `degiro-connector`.

## 1.1. Requirements

All the tests require the installation of the following packages :
- pytest
- pytest-mock

## 1.2. How to run tests ?

The usage of the package `pytest` is explained here :
- https://docs.pytest.org

The usage of the `markers` inside `pytest` is explained here :
- https://docs.pytest.org/en/6.2.x/example/markers.html
- https://docs.pytest.org/en/6.2.x/mark.html

Usage :
```bash
# ONLY CORE
pytest -m core

# ONLY QUOTECAST
pytest -m quotecast

# ONLY TRADING
pytest -m trading

# ONLY NETWORK
pytest -m network

# ONLY WITHOUT NETWORK
pytest -m "not network"

# ONLY QUOTECAST WITHOUT NETWORK
pytest -m "not network" tests\quotecast

# ONLY TRADING WITHOUT NETWORK
pytest -m "not network" tests\trading
```

## 1.3. How to check coverage ?

Usage :
```bash
coverage run --source=degiro_connector --module pytest
coverage report -m
```

# 2. Adding tests

## 2.1. Where to put the tests ?

Tests must be in the folder :
- `/tests`

The test must have the same path then the tested module.

For instance if the tested module is :
- `degiro_connector.core.helpers.lazy_loader`

Then the test must be in :
- `tests/degiro_connector/core/helpers/test_lazy_loader.py`

## 2.2. How to test an `action` ?

Suppose your action is in this path :
- `degiro_connector.trading.actions.action_my_action`

First you need to add a test file :
- `tests/degiro_connector/trading/actions/test_action_my_action.py`

Here is how your test can look like :
```python
import pytest

@pytest.mark.trading
@pytest.mark.network
def test_my_action(trading_connected):
    # SETUP
    some_request = "MY-REQUEST"

    # EXECUTE
    response = trading.my_action(some_request=some_request)

    # CHECK
    assert response is True
```


# 3. Mocking elements

Something you can't test the complete workflow (for instance for API calls) : you need to simulate the result from part of your code.

The package `pytest-mock` will help you with that :
- https://github.com/pytest-dev/pytest-mock

You can find example using the `fixture` called `mocker` in the tests of `degiro-connector`.