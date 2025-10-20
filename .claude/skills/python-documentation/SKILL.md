---
name: Python Documentation
description: Writes Python docstrings and Sphinx documentation following reStructuredText standards. Use when writing docstrings for functions/classes/modules, creating Sphinx docs in docs/source/, or adding cross-references. Use when user mentions documentation, docstrings, Sphinx, RST, or API docs.
---

# Python Documentation

Write comprehensive Python documentation using standardized docstring formats and Sphinx documentation structure.

## Documentation types

### 1. Docstrings (in .py files)

Write docstrings for:
- **Functions/Methods** - Describe purpose, parameters, and return values
- **Classes** - Document constructor parameters and class purpose
- **Modules** - Explain module purpose and design patterns

**Key principles:**
- Concise but complete descriptions
- Don't duplicate type information from type hints
- Use reStructuredText syntax for Sphinx compatibility

**For complete docstring patterns:** See [reference/docstrings.md](reference/docstrings.md)

### 2. Sphinx documentation (in docs/source/)

Create structured documentation in `docs/source/` directory:
- Follow numbered directory structure: `01-Introduction/`, `02-User-Guide/`
- Each section is a directory with `index.rst`
- Use autotoctree for automatic table of contents

**For Sphinx structure rules:** See [reference/sphinx-structure.md](reference/sphinx-structure.md)

### 3. Cross-references

Link between code and documentation using Sphinx roles:
- `:class:` - Reference Python classes
- `:func:` - Reference functions
- `:meth:` - Reference methods
- `:mod:` - Reference modules
- `:ref:` - Reference documentation sections

**For cross-reference syntax:** See [reference/cross-references.md](reference/cross-references.md)

## Quick reference

### Writing function docstrings

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """
    Brief description of what the function does.

    :param param1: Description of first parameter
    :param param2: Description of second parameter

    :returns: Description of return value
    """
```

### Writing class docstrings

```python
@dataclass
class ClassName:
    """
    Brief description of the class purpose.

    :param field1: Description of constructor parameter/field
    :param field2: Description of constructor parameter/field
    """
    field1: Type1
    field2: Type2
```

### Creating Sphinx documentation

Directory structure:
```
docs/source/01-Introduction/index.rst
docs/source/02-User-Guide/index.rst
docs/source/03-API-Reference/index.rst
```

Each index.rst starts with:
```rst
.. _reference-label:

Document Title
==============================================================================

Content here...
```

### Adding cross-references in docstrings

```python
def process_data():
    """
    Process data using authentication.

    Uses :class:`~package.module.User` and
    :func:`~package.module.authenticate` for validation.
    See :ref:`getting-started` guide for setup.
    """
```

## Common workflows

**Writing new module documentation:**
1. Add module docstring at top of .py file
2. Add docstrings to all classes and functions
3. Create corresponding Sphinx doc in `docs/source/`
4. Add cross-references linking code and docs

**Documenting a new function:**
1. Write brief description (one line)
2. Add `:param` entries for each parameter
3. Add `:returns` describing return value
4. Include examples if parameters are complex

**Creating new Sphinx section:**
1. Create directory: `docs/source/XX-Section-Name/`
2. Create `index.rst` with reference label and title
3. Link from other docs using `:ref:`label``

## Best practices

- **First line**: Always a complete sentence ending with period
- **Present tense**: Use "Returns..." not "Will return..."
- **Active voice**: Prefer active over passive
- **Be specific**: Describe what parameters represent, not just their type
- **Include constraints**: Mention valid ranges, formats, or patterns
- **Link related items**: Use cross-references to connect documentation

## Tools and commands

**Build documentation:**
```bash
make build-doc      # Build Sphinx HTML docs
make view-doc       # Open docs in browser
```

**Verify docstrings:**
```bash
.venv/bin/python -m pydocstyle module.py    # Check docstring style
```
