# Public API Testing Reference

## API module pattern (api.py)

The `api.py` file exposes public APIs using **one import per line**:

```python
# In esc_mini_tools_lib/api.py
from .tools.example import ExampleInput
from .tools.example import ExampleOutput
from .tools.another import AnotherFunction
```

**Never use** multiple imports per line:
```python
# WRONG - avoid this pattern
from .tools.example import ExampleInput, ExampleOutput
```

## API test pattern (tests/test_api.py)

The test file imports all public API objects to catch API changes:

```python
# -*- coding: utf-8 -*-

from esc_mini_tools_lib import api


def test():
    _ = api
    _ = api.ExampleInput
    _ = api.ExampleOutput
    _ = api.AnotherFunction


if __name__ == "__main__":
    from esc_mini_tools_lib.tests import run_cov_test

    run_cov_test(
        __file__,
        "esc_mini_tools_lib.api",
        preview=False,
    )
```

## Real example

See the actual implementation:
- Source: `esc_mini_tools_lib/api.py`
- Test: `tests/test_api.py`
