---
name: Python Project Automation
description: Manages Python project lifecycle using Makefile commands for virtual environment setup, dependency management, testing, documentation, and package builds. Use when setting up projects, installing dependencies, running tests, building docs, or creating releases. Use for operations starting with "make" or Python project lifecycle tasks.
---

# Python Project Automation

Automate Python project operations using predefined Makefile commands. All operations use `~/.pyenv/shims/python` for bootstrap commands and `.venv/bin/python` for project-specific execution.

## Essential workflows

### First-time project setup

```bash
make venv-create    # Create .venv directory
make install-all    # Install all dependencies
```

### After updating pyproject.toml

Always run this sequence when dependencies change:

```bash
make poetry-lock && make poetry-export && make install
```

This resolves dependencies (poetry.lock), exports to requirements.txt, and installs them.

### Daily development workflow

```bash
make cov            # Run tests with coverage (most common)
make test           # Run unit tests only
make build-doc      # Build Sphinx documentation
make view-doc       # Open docs in browser
```

## Available commands by category

### Environment setup

- `make venv-create` - Create .venv directory (required first step)
- `make venv-remove` - Delete .venv completely
- `make install` - Install runtime dependencies
- `make install-all` - Install all dependency groups
- `make install-dev` - Install development tools
- `make install-test` - Install testing frameworks
- `make install-doc` - Install Sphinx documentation tools
- `make install-automation` - Install CI/CD automation tools

### Dependency management

- `make poetry-lock` - Resolve dependencies, update poetry.lock
- `make poetry-export` - Export poetry.lock to requirements.txt

### Testing

- `make test` - Run unit tests with dependency check
- `make cov` - Run tests with coverage analysis (use this for comprehensive testing)
- `make view-cov` - Open coverage report in browser
- `make int` - Run integration tests

### Documentation

- `make nb-to-md` - Convert Jupyter notebooks to Markdown
- `make build-doc` - Build Sphinx HTML documentation
- `make view-doc` - Open built documentation in browser

### Build and release

- `make build` - Build wheel and source distribution
- `make publish` - Build and publish package to PyPI
- `make release` - Create GitHub release with version tag

### CI/CD setup

- `make setup-codecov` - Configure Codecov token
- `make setup-rtd` - Create ReadTheDocs project
- `make edit-github` - Update GitHub repository settings

## Key rules

**Check .venv first**: If .venv doesn't exist, run `make venv-create` before any other commands.

**Dependency updates**: After modifying pyproject.toml, ALWAYS run:
```bash
make poetry-lock && make poetry-export && make install
```

**Testing**: Use `make cov` for comprehensive coverage testing of entire codebase. Use `make test` for faster unit tests only.

**Python execution**: For scripts in `tests/`, `debug/`, `scripts/`, `config/` directories, use `.venv/bin/python path/to/script.py`.

## Command dependencies

Commands with dependencies automatically run prerequisites:
- `make test` runs `install` and `install-test` first
- `make cov` runs `install` and `install-test` first
- `make build-doc` runs `install` and `install-doc` first
- `make publish` runs `build` first

## Common scenarios

**Starting work on existing project:**
```bash
make venv-create
make install-all
make cov  # Verify everything works
```

**Adding a new dependency:**
1. Edit pyproject.toml
2. Run: `make poetry-lock && make poetry-export && make install`
3. Verify: `make cov`

**Before committing code:**
```bash
make cov  # Ensure tests pass with coverage
```

**Building and viewing documentation:**
```bash
make build-doc && make view-doc
```

**Preparing a release:**
```bash
make cov      # Verify tests pass
make publish  # Build and publish package to PyPI
make release  # Create GitHub release
```
