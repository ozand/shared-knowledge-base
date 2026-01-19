---
title: "Code Quality & Automation"
version: "1.0.0"
last_updated: "2025-01-01"
category: "quality_assurance"
priority: contextual
applies_to: ["all_projects"]
agent_usage: "Reference when writing code, setting up CI, or refactoring"
keywords: ["ruff", "mypy", "pre-commit", "linting", "formatting", "maintenance"]
related_docs: ["00-core-principles.md", "01-project-structure.md"]
---

# Code Quality & Automation

> Automated tools and processes to maintain code quality

## Linting & Formatting with Ruff

### Configuration (pyproject.toml)

```toml
[tool.ruff]
line-length = 88                    # Standard Python convention (Black compatible)
target-version = "py311"

# Rule selection
select = [
    "F",      # Pyflakes
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "I",      # isort (import sorting)
    "UP",     # pyupgrade (modern Python idioms)
    "B",      # flake8-bugbear
    "BLE",    # flake8-blind-except
]

ignore = [
    "E501",   # Line too long (handled by formatter)
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.ruff.lint.isort]
known-first-party = ["src"]
```

### Usage

```bash
# Check and fix issues
ruff check . --fix

# Format code
ruff format .

# Check only (CI mode)
ruff check . --no-fix
```

---

## Type Checking with mypy

### Configuration (pyproject.toml)

```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true

# Per-module options
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

### Usage

```bash
# Type check entire project
mypy src/

# Type check specific module
mypy src/project_name/payments/
```

---

## Pre-commit Hooks

### Setup

1. **Install pre-commit:**
```bash
uv add --dev pre-commit
```

2. **Create .pre-commit-config.yaml:**

```yaml
repos:
  # Ruff - linting and formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
        args: [--strict]

  # Standard checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: [--maxkb=500]
      - id: check-merge-conflict

  # Custom project validators (optional)
  - repo: local
    hooks:
      - id: validate-kb
        name: Validate Knowledge Base
        entry: python scripts/development/validate_kb.py
        language: python
        types: [markdown]
        pass_filenames: false
```

3. **Install hooks:**
```bash
pre-commit install
```

4. **Run manually (optional):**
```bash
# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
```

---

## Maintenance Tasks

### Dead Code Detection & Removal

```bash
# Find unused imports and variables
ruff check . --select F401,F841 --fix

# Find unused functions (manual review needed)
ruff check . --select F401,F821,F841
```

### Dependency Audits

```bash
# Check for outdated packages
uv pip list --outdated

# Security vulnerability check (use pip-audit)
uv add --dev pip-audit
uv run pip-audit
```

### Update All Dependencies

```bash
# Update to latest compatible versions
uv sync --upgrade
```

---

## Refactoring Process

Follow this systematic approach when refactoring:

1. **Isolate change:** Focus on one small improvement
2. **Run tests:** Ensure all tests pass before starting
3. **Make change:** Implement the refactoring
4. **Run tests again:** Verify nothing broke
5. **Commit:** Create atomic commit with clear message
6. **Repeat:** Continue with next small step

### Example Workflow

```bash
# 1. Ensure clean state
uv run pytest

# 2. Make small change (e.g., rename function)
# ... edit code ...

# 3. Auto-fix code quality
ruff check . --fix
ruff format .

# 4. Verify with tests
uv run pytest

# 5. Commit
git add .
git commit -m "refactor: rename process_payment to execute_payment"

# 6. Continue with next change
```

---

## Script Execution Protocol

**MANDATORY:** After running ANY script or command, always:

1. **Capture output:** Both stdout and stderr
2. **Analyze results:**
   - ✅ What succeeded?
   - ❌ What failed?
   - ⚠️  What warnings appeared?
3. **Decide next action:**
   - If errors: investigate and fix
   - If warnings: evaluate severity
   - Use `ask_followup_question` when uncertain
4. **Never ignore warnings** - they often indicate real issues

### Example Analysis

```bash
$ ruff check . --fix

# Output analysis:
# ✅ Fixed 15 issues automatically
# ⚠️  Warning: Unused import in src/payments/processor.py
# ❌ Error: Undefined name 'process_paymen' in src/api/routes.py

# Action: Fix typo in routes.py, remove unused import
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Quality Checks

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v1
      
      - name: Install dependencies
        run: uv sync
      
      - name: Lint
        run: uv run ruff check . --no-fix
      
      - name: Format check
        run: uv run ruff format --check .
      
      - name: Type check
        run: uv run mypy src/
      
      - name: Run tests
        run: uv run pytest --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Quality Metrics

### Minimum Standards

| Metric | Target | Tool |
|--------|--------|------|
| Code coverage | ≥80% | pytest-cov |
| Type coverage | 100% | mypy --strict |
| Linting issues | 0 | ruff |
| Cyclomatic complexity | ≤10 per function | ruff (CCR rules) |

### When to Measure

- **Every commit:** via pre-commit hooks
- **Every PR:** via CI pipeline
- **Weekly:** full project audit
- **Before release:** comprehensive quality review
