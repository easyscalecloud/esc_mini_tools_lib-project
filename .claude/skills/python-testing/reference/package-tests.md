# Package-Level Testing Reference

## all.py pattern

Package-level `all.py` files run coverage for an entire package using `is_folder=True`:

```python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from esc_mini_tools_lib.tests import run_cov_test

    run_cov_test(
        __file__,
        "esc_mini_tools_lib",  # or "esc_mini_tools_lib.subpackage"
        is_folder=True,
        preview=False,
    )
```

## Running package tests

```bash
.venv/bin/python tests/all.py                    # All tests
.venv/bin/python tests/<subpackage>/all.py       # Specific package
```

## Real example

See: `tests/all.py`
