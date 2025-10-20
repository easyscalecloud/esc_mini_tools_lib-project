# Sphinx Documentation Structure Reference

This guide establishes documentation structure standards for Sphinx projects using the autotoctree plugin.

## Directory Structure

All documentation lives in `docs/source/` following this pattern:

```
docs/source/
├── 01-Introduction/
│   └── index.rst
├── 02-Configuration/
│   └── index.rst
├── 03-User-Guide/
│   └── index.rst
└── 04-Developer-Guide/
    ├── index.rst
    ├── 01-Architecture-Overview/
    │   └── index.rst
    └── 02-Testing-Strategy/
        └── index.rst
```

## Naming Convention

```
${sequence-number}-${short-title}/index.rst
```

**Components:**
- **Sequence Number**: Two digits (01, 02, 03...) for ordering
- **Short Title**: Title-Case-With-Hyphens, no articles or prepositions
- **Always Directory**: Never standalone `.rst` files (required for autotoctree)

**Examples:**
- `01-Introduction/index.rst`
- `02-User-Guide/index.rst`
- `03-API-Reference/index.rst`
- `04-Developer-Guide/01-Architecture-Overview/index.rst`

## Document Header Format

Every `index.rst` must start with:

```rst
.. _${reference-label}:

${Document Title}
==============================================================================
*Optional subtitle*

Content starts here...
```

### Rules

1. **Reference Label**: Lowercase slugified title (permanent, unique)
2. **Title Underline**: 79 equals signs, or match title length if >79 chars
3. **Required Elements**: Reference label, title, underline

### Examples

**With subtitle:**

```rst
.. _user-authentication:

User Authentication and Authorization
==============================================================================
*Comprehensive guide to security implementation*

This guide covers authentication mechanisms...
```

**Without subtitle:**

```rst
.. _api-reference:

API Reference
==============================================================================

Complete API documentation for all modules.
```

**Long title:**

```rst
.. _advanced-deployment:

Advanced Deployment Strategies for Production Environments
========================================================================================

This section covers production deployment...
```

## Cross-References Between Documents

Link between documents using reference labels:

```rst
See :ref:`user-authentication` for security details.

For complete API documentation, refer to the :ref:`API Reference <api-reference>`.
```

## Integration with Autotoctree

The autotoctree plugin automatically discovers directories and builds table of contents:

```rst
.. autotoctree::
    :maxdepth: 1
```

This scans the current directory for subdirectories following the naming convention and includes them in order.

## Complete Example

### docs/source/01-Getting-Started/index.rst

```rst
.. _getting-started:

Getting Started
==============================================================================
*Quick start guide for new users*

This guide helps you get up and running quickly.

Installation
------------

Install the package using pip::

    pip install your-package

Configuration
-------------

Configure your environment by creating a config file.

For advanced configuration options, see :ref:`configuration-guide`.

Next Steps
----------

- Review the :ref:`user-guide` for detailed usage
- Check the :ref:`api-reference` for complete API documentation
- See :ref:`deployment-guide` for production setup

.. autotoctree::
    :maxdepth: 1
```

### docs/source/02-User-Guide/index.rst

```rst
.. _user-guide:

User Guide
==============================================================================

Complete guide for using the package in your projects.

Basic Usage
-----------

Start by importing the main class::

    from your_package import MainClass

    instance = MainClass(config="path/to/config")
    result = instance.process()

For installation instructions, see :ref:`getting-started`.

.. autotoctree::
    :maxdepth: 2
```

### docs/source/02-User-Guide/01-Authentication/index.rst

```rst
.. _authentication-guide:

Authentication
==============================================================================

Setting up authentication for secure access.

Basic Authentication
--------------------

Configure basic authentication::

    auth = BasicAuth(
        username="user",
        password="secret"
    )

OAuth Integration
-----------------

For OAuth configuration, see :ref:`oauth-setup`.

.. note::
    Always use environment variables for sensitive credentials.
    Never hardcode passwords in your source code.
```

## Section Organization Best Practices

### Top-level sections (01-, 02-, 03-)

Organize by user journey:
- `01-Introduction/` - What is this, why use it
- `02-Getting-Started/` - Installation and quick start
- `03-User-Guide/` - How to use features
- `04-API-Reference/` - Complete API documentation
- `05-Developer-Guide/` - Contributing, architecture
- `06-Deployment/` - Production deployment guides

### Subsections (within each top-level)

Group related topics:
```
03-User-Guide/
├── index.rst
├── 01-Basic-Concepts/
│   └── index.rst
├── 02-Authentication/
│   └── index.rst
├── 03-Data-Processing/
│   └── index.rst
└── 04-Advanced-Topics/
    └── index.rst
```

## Common Patterns

### Landing page (index.rst at root level)

```rst
.. _index:

Project Documentation
==============================================================================

Welcome to the project documentation.

.. autotoctree::
    :maxdepth: 2
```

### Section with subsections

```rst
.. _developer-guide:

Developer Guide
==============================================================================

Guide for contributors and maintainers.

This section covers:

- Architecture overview
- Development setup
- Testing strategy
- Release process

.. autotoctree::
    :maxdepth: 2
```

### Section without subsections

```rst
.. _changelog:

Changelog
==============================================================================

Release history and version notes.

Version 2.0.0 (2024-01-15)
--------------------------

**Breaking Changes:**
- Removed deprecated API endpoints

**New Features:**
- Added async support
- Improved performance by 50%
```

This structure ensures consistent, maintainable documentation across all Sphinx projects using autotoctree.
