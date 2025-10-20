---
name: Python Testing Strategy
description: Manages Python unit testing and code coverage using the project's testing conventions. Use when writing tests, running coverage analysis, checking test structure, or achieving 95%+ coverage goals. Use when user mentions testing, coverage, test files, or pytest.
---

# Python Testing Strategy

Execute unit tests with code coverage using the project's standardized test structure and `run_cov_test()` framework.

## Test file naming convention

Source files map to test files with this pattern:

**Source:** `esc_mini_tools_lib/<subpackage>/<module>.py`
**Test:** `tests/<subpackage>/test_<subpackage>_<module>.py`

Examples:
- Source: `esc_mini_tools_lib/tools/calculator.py` → Test: `tests/tools/test_tools_calculator.py`
- Source: `esc_mini_tools_lib/api.py` → Test: `tests/test_api.py`

The test file name includes the full relative path to prevent naming collisions.

## Running tests

### Individual module test (most common workflow)

Run coverage test for a specific module:

```bash
.venv/bin/python tests/<subpackage>/test_<subpackage>_<module>.py
```

Examples:
```bash
.venv/bin/python tests/test_api.py
.venv/bin/python tests/tools/test_tools_count_llm_token.py
.venv/bin/python tests/tools/test_tools_add_up_two_number.py
```

This is the primary development workflow - 90% of development involves editing a single source file and running its corresponding test.

### Package-level tests

Each test directory has an `all.py` file for package-wide coverage:

```bash
.venv/bin/python tests/all.py                    # All tests
.venv/bin/python tests/<subpackage>/all.py       # Specific package
```

### Full project coverage

Use makefile command for complete coverage:

```bash
make cov  # Runs all tests with coverage analysis
```

## Test file structure

All test files follow a standard pattern with these key elements:
- Import classes/functions from source module
- Test class named `Test<ClassName>`
- Test method named `test()`
- Use `run_cov_test(__file__, "module.path", preview=False)` in `__main__`

**For complete structure and examples:** See [reference/test-structure.md](reference/test-structure.md)

**Real examples in codebase:**
- `tests/test_api.py` - Public API test
- `tests/test_tools_count_llm_token.py` - Standard tool test
- `tests/test_tools_add_up_two_number.py` - Simple example
- `tests/all.py` - Package-level test

## Public API testing

The `api.py` file uses **one import per line**. The `tests/test_api.py` file imports all API objects to catch changes.

**For API testing pattern:** See [reference/api-testing.md](reference/api-testing.md)

## Package-level testing

Package `all.py` files use `is_folder=True` to test entire packages.

**For all.py pattern:** See [reference/package-tests.md](reference/package-tests.md)

## Coverage reports

After running tests, coverage reports are generated:

**Location:** `htmlcov/${random_hash}_<module>_py.html`

**To view:** Open the HTML file in a browser to see:
- Green lines: Code executed during tests
- Red lines: Code not covered by tests
- Line-by-line coverage details

**Coverage goal:** Target 95%+ code coverage for all implementation files.

**Excluding untestable code:** Use `# pragma: no cover` for platform-specific or untestable code.

## Coverage configuration

The `.coveragerc` file in the project root configures the coverage tool, including which files to exclude in the `omit` section.

## Common workflows

**Developing a new module:**
1. Create source file: `esc_mini_tools_lib/tools/new_feature.py`
2. Create test file: `tests/tools/test_tools_new_feature.py`
3. Run test: `.venv/bin/python tests/tools/test_tools_new_feature.py`
4. Iterate until 95%+ coverage achieved

**Adding to public API:**
1. Add imports to `esc_mini_tools_lib/api.py` (one per line)
2. Update `tests/test_api.py` to import new API objects
3. Run: `.venv/bin/python tests/test_api.py`

**Quick coverage check:**
```bash
.venv/bin/python tests/test_<module>.py  # Run and view coverage
```

**Full project verification:**
```bash
make cov  # Run all tests with coverage
```
