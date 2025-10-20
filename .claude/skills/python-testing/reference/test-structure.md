# Test File Structure Reference

## Standard module test pattern

Every test file follows this standard structure:

```python
# -*- coding: utf-8 -*-

from esc_mini_tools_lib.tools.example import (
    ExampleInput,
    ExampleOutput,
)


class TestExampleInput:
    def test(self):
        input = ExampleInput(
            param1="value1",
            param2=123,
        )
        output = input.main()
        assert output.result == expected_value


if __name__ == "__main__":
    from esc_mini_tools_lib.tests import run_cov_test

    run_cov_test(
        __file__,
        "esc_mini_tools_lib.tools.example",
        preview=False,
    )
```

**Key elements:**
- Import classes/functions from source module
- Test class named `Test<ClassName>`
- Test method named `test()`
- Use `run_cov_test(__file__, "module.path", preview=False)` in `__main__`

## Real examples in codebase

See these actual test files:
- `tests/test_api.py` - Public API test pattern
- `tests/test_tools_count_llm_token.py` - Standard tool test
- `tests/test_tools_add_up_two_number.py` - Simple test example
- `tests/all.py` - Package-level all.py pattern
