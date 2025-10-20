# Cross-Reference Guide for Sphinx Documentation

This guide explains how to properly reference Python objects (modules, classes, methods, functions) in both `.py` docstrings and `.rst` documentation files using Sphinx cross-reference syntax.

## Overview

Sphinx provides role directives that create clickable links between documentation elements. These references work in both Python docstrings and reStructuredText files, enabling rich interconnected documentation.

## Cross-Reference Syntax by Type

### 1. Referencing Classes

**Different module (external reference):**

```python
# Syntax: :class:`~full.module.path.ClassName`
# The ~ hides the full path, showing only the class name to users

def process_user():
    """
    Process user data using authentication.

    Creates a :class:`~myapp.auth.users.User` instance and validates
    permissions through :class:`~myapp.auth.permissions.Role`.
    """
    pass
```

**Rendered as**: Creates a `User` instance and validates permissions through `Role`.

**Same module (internal reference):**

```python
class User:
    """
    User account management.

    Uses :class:`Role` for permission checking.
    """
```

### 2. Referencing Methods

**Different module:**

```python
# Syntax: :meth:`ClassName.method_name <full.module.path.ClassName.method_name>`
# Shows only ClassName.method_name to users

def update_profile():
    """
    Update user profile information.

    Uses :meth:`User.get_profile <myapp.auth.users.User.get_profile>`
    to retrieve current data before updating.
    """
    pass
```

**Rendered as**: Uses `User.get_profile` to retrieve current data.

**Same module:**

```python
class User:
    def get_profile(self) -> dict:
        """
        Get user profile data.

        Call :meth:`save` after modifying profile data.
        """
        pass

    def save(self) -> None:
        """Save changes to database."""
        pass
```

### 3. Referencing Functions

**Different module:**

```python
# Syntax: :func:`~full.module.path.function_name`
# The ~ hides the full path, showing only the function name

def login_user():
    """
    Handle user login process.

    Calls :func:`~myapp.auth.users.authenticate` to verify credentials
    and :func:`~myapp.auth.permissions.check_permission` for authorization.
    """
    pass
```

**Rendered as**: Calls `authenticate` to verify credentials and `check_permission` for authorization.

**Same module:**

```python
def authenticate(username: str, password: str) -> bool:
    """
    Authenticate user credentials.

    Uses :func:`hash_password` for secure password comparison.
    """
    pass

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    pass
```

### 4. Referencing Modules

**Module references:**

```python
# Syntax: :mod:`full.module.path`
# Shows the full module path (no ~ used for modules)

def setup_auth():
    """
    Initialize authentication system.

    Configures components from :mod:`myapp.auth.users` and
    :mod:`myapp.auth.permissions` modules.
    """
    pass
```

**Rendered as**: Configures components from `myapp.auth.users` and `myapp.auth.permissions` modules.

### 5. Referencing Documentation Sections

**In .rst files, set up labels:**

```rst
.. _getting-started:

Getting Started
===============

This section covers basic setup.

.. _installation-guide:

Installation
------------

Step-by-step installation instructions.
```

**Reference from docstrings or other .rst files:**

```python
def setup_project():
    """
    Initialize a new project.

    Follow the :ref:`getting-started` guide for complete setup instructions.
    See :ref:`authentication section <auth-guide>` for security configuration.

    For installation help, check the :ref:`installation-guide`.
    """
    pass
```

**In .rst files:**

```rst
Database Models
===============

The database layer provides several key components. Start with the
:ref:`getting-started` guide, then review the :class:`~myapp.database.models.BaseModel`
class documentation.
```

## Complete Cross-Module Example

### myapp/database/models.py

```python
"""
Database model definitions.

This module provides base classes for all database operations. Models inherit
from :class:`BaseModel` and use connections created by
:func:`~myapp.database.connection.connect`.

See the :ref:`api-reference` documentation for complete usage examples.
"""

from typing import Optional

class BaseModel:
    """
    Base class for all database models.

    Provides common functionality for database operations. Subclasses should
    implement their own validation logic while using the connection established
    through :func:`~myapp.database.connection.connect`.

    Integration with authentication is handled through
    :class:`~myapp.auth.users.User` instances. User permissions are
    validated using :func:`~myapp.auth.permissions.check_permission`.

    :param table_name: Database table name for this model
    :param connection: Database connection instance

    Example:
        Creating a model with authentication::

            user = User("john_doe")
            if check_permission(user.username, "read"):
                model = BaseModel("users", db_connection)
                profile = user.get_profile()

    .. note::
        See :ref:`getting-started` for setup instructions and
        :ref:`authentication-api` for security best practices.
    """

    def __init__(self, table_name: str, connection):
        self.table_name = table_name
        self.connection = connection

    def save(self) -> None:
        """
        Save model instance to database.

        Uses the connection established by :func:`~myapp.database.connection.connect`.
        Requires authentication through :func:`~myapp.auth.users.authenticate`.
        """
        pass

    def find_by_id(self, record_id: int) -> Optional[dict]:
        """
        Find record by primary key.

        :param record_id: Primary key value to search for

        :returns: Record data if found, None otherwise

        .. seealso::
            :meth:`save` for creating new records and
            :func:`~myapp.database.connection.Database.query` for custom queries.
        """
        pass
```

## Reference Syntax Quick Reference

### Same Module References

```python
:class:`ClassName`              # Class in same module
:meth:`ClassName.method_name`   # Method in same module
:func:`function_name`           # Function in same module
```

### Different Module References

```python
:class:`~package.module.ClassName`                        # External class
:meth:`ClassName.method <package.module.ClassName.method>` # External method
:func:`~package.module.function_name`                     # External function
:mod:`package.module`                                     # Module (no ~)
```

### Documentation Section References

```python
:ref:`section-label`                    # Reference by label
:ref:`Custom Text <section-label>`      # Custom link text
```

## Best Practices

### 1. Consistency Rules

- **Always use `~`** for classes and functions from other modules (hides full path)
- **Never use `~`** for modules (users need to see full module path)
- **Use descriptive text** with angle brackets when the default text isn't clear

### 2. Grouping Related References

```python
class UserManager:
    """
    Comprehensive user management system.

    **Core Components:**

    - User creation: :class:`~myapp.auth.users.User`
    - Authentication: :func:`~myapp.auth.users.authenticate`
    - Authorization: :func:`~myapp.auth.permissions.check_permission`
    - Data persistence: :class:`~myapp.database.models.BaseModel`

    **Related Documentation:**

    - Setup guide: :ref:`getting-started`
    - API reference: :ref:`authentication-api`
    - Advanced patterns: :ref:`user-management-patterns`
    """
    pass
```

### 3. Error Prevention

```python
# ❌ Wrong - missing backticks
:class:User

# ❌ Wrong - unnecessary ~ for same module
:class:`~User`

# ❌ Wrong - missing ~ for external module
:class:`myapp.auth.users.User`

# ✅ Correct - same module
:class:`User`

# ✅ Correct - external module with ~
:class:`~myapp.auth.users.User`
```

## Quick Reference Table

| Element Type | Same Module | Different Module | Display Result |
|--------------|-------------|------------------|----------------|
| **Class** | `:class:\`User\`` | `:class:\`~package.module.User\`` | `User` |
| **Method** | `:meth:\`User.save\`` | `:meth:\`User.save <package.module.User.save>\`` | `User.save` |
| **Function** | `:func:\`authenticate\`` | `:func:\`~package.module.authenticate\`` | `authenticate` |
| **Module** | N/A | `:mod:\`package.module\`` | `package.module` |
| **Documentation** | `:ref:\`section-label\`` | `:ref:\`Custom Text <section-label>\`` | `section-label` or `Custom Text` |

This cross-reference system creates rich, navigable documentation that helps users understand relationships between code components and find relevant information quickly.
