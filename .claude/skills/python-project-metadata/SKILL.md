---
name: Python Project Metadata
description: Extracts Python project metadata from pyproject.toml including project name, version, Python version requirements, dependencies, and GitHub repository info. Use when needing project configuration, dependencies, versions, or repository details.
---

# Python Project Metadata

Understand Python project configuration by reading `pyproject.toml`.

## Key metadata locations

**Project basics:**
- `project.name` - Project name (source code folder has same name)
- `project.version` - Current version (source of truth)
- `project.description` - Project description

**Python versions:**
- `project.requires-python` - Supported Python version range
- `tool.pywf.dev_python` - Specific Python version for development and production

**Dependencies:**
- `project.dependencies` - Core runtime dependencies
- `project.optional-dependencies` - Optional dependency groups (dev, test, doc, auto)

**Repository info:**
- `project.urls.Repository` - GitHub URL
  - Extract account and repo name from URL format: `https://github.com/{account}/{repo}`

## Reading metadata

```bash
# View entire pyproject.toml
cat pyproject.toml

# Extract specific fields
grep "^name = " pyproject.toml
grep "^version = " pyproject.toml
grep "^requires-python = " pyproject.toml
grep "dev_python = " pyproject.toml
```

## Adding dependencies

When adding new dependencies:
1. Check `project.requires-python` for Python version compatibility
2. Add to appropriate section:
   - `project.dependencies` - Runtime requirements
   - `project.optional-dependencies.dev` - Development tools
   - `project.optional-dependencies.test` - Testing frameworks
   - `project.optional-dependencies.doc` - Documentation tools
3. Ensure compatibility with `project.requires-python` range

## Additional configuration

The `tool.pywf` section contains project-specific configuration:
- `dev_python` - Python version for development and deployment
- `github_account` - GitHub account name
