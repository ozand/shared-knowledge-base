---
title: "Project Structure & Organization"
version: "1.0.0"
last_updated: "2025-01-01"
category: "project_setup"
priority: critical
applies_to: ["all_projects"]
agent_usage: "Reference when setting up projects or organizing code"
keywords: ["directory_structure", "organization", "src", "tests", "scripts"]
related_docs: ["00-core-principles.md", "03-testing-strategy.md"]
---

# Project Structure & Organization

> Standard layout for Python projects with clear separation of concerns

## Standard Directory Layout

```
project_name/
├── src/
│   └── project_name/           # Production code only
│       ├── __init__.py
│       ├── payments/
│       │   ├── __init__.py
│       │   ├── processor.py
│       │   └── models.py
│       └── search/
│           ├── __init__.py
│           └── engine.py
├── tests/
│   ├── unit/                   # Fast, isolated tests
│   │   ├── payments/
│   │   └── search/
│   ├── integration/            # Component interaction tests
│   └── e2e/                    # End-to-end user journeys
├── scripts/
│   ├── development/            # Engineering automation
│   │   ├── README.md
│   │   ├── utils.py
│   │   ├── migrate_db.py
│   │   └── reorganize_modules.py
│   └── archive/                # Deprecated scripts
├── docs/                       # Project documentation
├── pyproject.toml              # Project metadata & dependencies
├── .gitignore
├── .pre-commit-config.yaml
└── README.md
```

---

## Directory Rules

### src/ - Production Code Only

**Purpose:** Contains only application code that will be deployed to production

**Rules:**
- No temporary scripts, experiments, or one-off utilities
- No migration scripts or data processing scripts
- No test fixtures or test utilities
- Ensures CI/CD builds exclude auxiliary files

**Structure:**
- Mirror business domains/features as subdirectories
- Each subdirectory is a Python package (`__init__.py`)
- Use absolute imports: `from src.project_name.payments import ...`

---

### tests/ - Test Code

**Purpose:** All test code, mirroring src/ structure

**Subdirectories:**

#### tests/unit/
- Fast, isolated component tests
- No external dependencies (DB, network, filesystem)
- Mirror src/ structure exactly
```
src/project_name/payments/processor.py
→ tests/unit/payments/test_processor.py
```

#### tests/integration/
- Test component interactions
- May use database, external APIs, filesystem
- Example: API endpoint tests, database query tests

#### tests/e2e/
- Critical user journey validation
- Uses Playwright for browser automation
- Page Object Model structure
- See [03-testing-strategy.md](03-testing-strategy.md) for details

---

### scripts/development/ - Engineering Automation

**Purpose:** All non-production scripts (migrations, fixes, bulk operations)

**Rules:**
1. **Name clearly:** `reorganize_modules.py`, `migrate_imports.py`, `seed_test_data.py`
2. **Document in code:**
   - Module-level docstring explaining purpose
   - CLI argument documentation
   - Usage examples
3. **Create README.md** in `scripts/development/` listing all scripts
4. **Use Python modules,** not bash one-liners:
```python
# ✅ Good - scripts/development/migrate_db.py
def main():
    parser = argparse.ArgumentParser()
    # ... proper CLI interface

if __name__ == "__main__":
    main()
```
5. **Extract reusable logic** into `scripts/development/utils.py`
6. **Archive when done:** Move obsolete scripts to `scripts/archive/`

**Never put in scripts/:**
- Production application code
- Reusable business logic
- Tests

---

## Dependency Management

### Using uv (Recommended)

```bash
# Initialize new project
uv init project_name

# Add runtime dependency
uv add requests

# Add development dependency
uv add --dev pytest pytest-cov

# Synchronize environment
uv sync
```

### pyproject.toml Structure

```toml
[project]
name = "project_name"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

## Version Control (.gitignore)

**Always exclude:**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Virtual environments
.venv/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp

# Testing
.pytest_cache/
.coverage
htmlcov/

# Build artifacts
dist/
build/
*.egg-info/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

---

## Initialization Checklist

When starting a new project:

- [ ] Run `uv init project_name`
- [ ] Create src/project_name/ structure
- [ ] Create tests/ with unit/integration/e2e subdirs
- [ ] Create scripts/development/ with README.md
- [ ] Add .gitignore
- [ ] Configure Ruff and pre-commit (see 02-code-quality.md)
- [ ] Write initial README.md
- [ ] Initialize git repository
