# Knowledge Base System Guide

**Universal guide for implementing knowledge bases in software projects**

This document explains the knowledge base approach used in this project. You can use this as a template to implement similar knowledge bases in other projects.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [File Structure](#file-structure)
- [YAML Schema](#yaml-schema)
- [Implementation Guide](#implementation-guide)
- [Cross-Project Knowledge Sharing](#cross-project-knowledge-sharing)
- [Maintenance](#maintenance)
- [Tools and Automation](#tools-and-automation)

## Overview

### What is a Knowledge Base?

A **knowledge base** is a structured collection of:
- **Common errors** and their solutions
- **Best practices** and design patterns
- **Lessons learned** during development
- **Architectural decisions** and rationale

### Why Build a Knowledge Base?

**For AI Agents (Claude Code):**
- Prevent repeating the same mistakes
- Find solutions to known issues quickly
- Learn project-specific patterns
- Understand architectural decisions

**For Human Developers:**
- Onboarding documentation
- Troubleshooting guide
- Code review reference
- Learning resource

**For Teams:**
- Preserve institutional knowledge
- Reduce time debugging known issues
- Standardize approaches
- Improve code quality

## Architecture

### Design Decisions

#### 1. Format Choice: YAML + Markdown

**YAML for Structured Data:**
- ✅ Human-readable and editable
- ✅ Machine-parseable for automation
- ✅ Supports comments and multi-line strings
- ✅ Ideal for key-value pairs and lists
- ✅ Standard format with broad tool support

**Markdown for Documentation:**
- ✅ Readable in git/GitHub
- ✅ Easy to write and edit
- ✅ Good for indexes and guides
- ✅ Widely supported

**Why not JSON?**
- ❌ Too verbose
- ❌ No comments
- ❌ Poor multi-line string support

**Why not SQLite/Database?**
- ❌ Requires special tools
- ❌ Not readable in git
- ❌ Harder to review in PRs

#### 2. Multiple Files vs Single File

**Multiple Files (Chosen):**
- ✅ Better organization by category
- ✅ Easier navigation
- ✅ Independent growth
- ✅ Better git diffs
- ✅ Can load selectively

**Single File:**
- ❌ Hard to navigate
- ❌ Merge conflicts
- ❌ Slower to load

#### 3. Error ID System

Each error gets a unique ID: `CATEGORY-NNN`

Examples:
- `IMPORT-001`: First import-related error
- `TYPE-002`: Second type-checking error
- `TEST-003`: Third testing error

Benefits:
- Quick reference in discussions
- Easy to link from code comments
- Searchable in git history
- Stable references (don't change if title changes)

## File Structure

### Recommended Structure

```
docs/knowledge-base/
├── README.md                          # Index and usage guide
├── KNOWLEDGE_BASE_GUIDE.md            # This file (meta-documentation)
├── quick-reference.md                 # Quick lookup
│
├── errors/                            # Error documentation
│   ├── imports-and-dependencies.yaml
│   ├── type-checking.yaml
│   ├── testing.yaml
│   └── [category].yaml
│
├── patterns/                          # Best practices
│   ├── architecture.yaml
│   ├── [framework].yaml
│   └── git-workflow.yaml
│
├── shared/                            # Cross-project knowledge (optional)
│   ├── python-common.yaml
│   ├── docker-patterns.yaml
│   └── git-universal.yaml
│
└── tools/                             # Automation scripts (optional)
    ├── search.py
    ├── validate.py
    └── merge.py
```

### File Naming Conventions

- **Lowercase with hyphens**: `imports-and-dependencies.yaml`
- **Descriptive names**: Not `errors1.yaml` but `type-checking.yaml`
- **Category-based**: Group related errors/patterns

## YAML Schema

### Error Entry Schema

```yaml
version: "1.0"
category: "category-name"
last_updated: "YYYY-MM-DD"

errors:
  - id: "CATEGORY-NNN"              # Unique ID
    title: "Short Descriptive Title"
    severity: "critical|high|medium|low"

    problem: |
      Multi-line description of what's wrong.
      Explain the context and why it happens.

    symptoms:
      - "Observable symptom 1"
      - "Error message example"
      - "Behavior description"

    root_cause: |
      Why this error occurs. Technical explanation.

    affected_files:
      - "path/to/file1.py"
      - "path/to/file2.py"

    solution:
      code: |
        # Working code example
        from typing import TYPE_CHECKING

        if TYPE_CHECKING:
            from module import Class

      explanation: |
        Why this solution works.

    prevention:
      - "How to avoid this error"
      - "Best practice to follow"
      - "Tool to use"

    related_commits:
      - "hash - Description"

    related_errors:
      - "CATEGORY-MMM"

    tags: ["tag1", "tag2", "tag3"]

best_practices:
  - rule: "Description"
    example: |
      Code example

tools:
  - name: "Tool name"
    purpose: "What it does"
    command: "how to run"

troubleshooting:
  - symptom: "What user sees"
    causes:
      - "Possible cause 1"
      - "Possible cause 2"
    solution: "How to fix"
```

### Pattern Entry Schema

```yaml
version: "1.0"
category: "pattern-name"
last_updated: "YYYY-MM-DD"

patterns:
  - pattern_name: "Pattern Name"
    use_case: "When to use this pattern"

    problem: |
      What problem does this solve?

    solution:
      code: |
        # Implementation example

      explanation: |
        How it works

    benefits:
      - "Benefit 1"
      - "Benefit 2"

    drawbacks:
      - "Limitation 1"

    alternatives:
      - "Alternative approach 1"

    examples:
      - name: "Example 1"
        code: |
          # Full working example

best_practices:
  - rule: "Rule description"
    good_example: |
      # Good code
    bad_example: |
      # Bad code
```

## Implementation Guide

### Step 1: Initialize Structure

```bash
# Create directory structure
mkdir -p docs/knowledge-base/{errors,patterns,tools}

# Create index files
touch docs/knowledge-base/README.md
touch docs/knowledge-base/quick-reference.md
touch docs/knowledge-base/KNOWLEDGE_BASE_GUIDE.md
```

### Step 2: Create First Error Entry

Create `docs/knowledge-base/errors/template.yaml`:

```yaml
version: "1.0"
category: "example-errors"
last_updated: "2026-01-04"

errors:
  - id: "EXAMPLE-001"
    title: "Example Error"
    severity: "medium"

    problem: |
      Description of the problem

    symptoms:
      - "What the user sees"

    solution:
      code: |
        # Solution

    prevention:
      - "How to avoid"

    tags: ["example"]
```

### Step 3: Create README

The README should include:
- Purpose of knowledge base
- How to search and use it
- File structure explanation
- Contributing guidelines
- Version history

See `docs/knowledge-base/README.md` in this project as template.

### Step 4: Create Quick Reference

A quick reference should include:
- Most common errors with quick fixes
- Essential commands
- Key patterns
- Configuration snippets

See `docs/knowledge-base/quick-reference.md` as template.

### Step 5: Start Collecting Knowledge

**Document errors as you fix them:**
1. Encounter error
2. Solve it
3. Document in knowledge base
4. Commit with reference to error ID

**Document patterns as you establish them:**
1. Identify recurring solution
2. Extract as pattern
3. Provide examples
4. Explain when to use

## Cross-Project Knowledge Sharing

### Strategy 1: Shared Knowledge Repository

**Setup:**
```bash
# Central knowledge repo
git clone https://github.com/org/shared-knowledge.git

# In each project, add as submodule
cd project-a
git submodule add https://github.com/org/shared-knowledge.git docs/shared-kb

# Or symlink
ln -s /path/to/shared-knowledge docs/shared-kb
```

**Structure:**
```
project-a/
├── docs/
│   ├── knowledge-base/          # Project-specific
│   │   ├── errors/
│   │   └── patterns/
│   └── shared-kb/               # Shared across projects
│       ├── python-common/
│       ├── docker-patterns/
│       └── git-workflows/

project-b/
├── docs/
│   ├── knowledge-base/          # Project-specific
│   └── shared-kb/               # Same shared repo
```

**Benefits:**
- ✅ Single source of truth
- ✅ Updates propagate to all projects
- ✅ Universal patterns in one place

**Drawbacks:**
- ⚠️ Need to manage submodules
- ⚠️ Coupling between projects

### Strategy 2: Scope-Based Organization

**Each entry has scope tag:**

```yaml
errors:
  - id: "IMPORT-001"
    title: "Circular Import"
    scope: "python-universal"      # Universal for all Python projects
    # ...

  - id: "IMPORT-002"
    title: "FastAPI Middleware Import"
    scope: "fastapi"               # Specific to FastAPI projects
    # ...

  - id: "IMPORT-003"
    title: "ETL Module Circular Dependency"
    scope: "project-specific"      # Only this project
    # ...
```

**Scope Levels:**
- `universal`: Any software project
- `python`: Any Python project
- `framework`: Specific framework (FastAPI, Django, etc.)
- `domain`: Specific domain (ETL, ML, API, etc.)
- `project`: This project only

**Merge Tool:**

```python
# tools/merge-knowledge.py
import yaml
from pathlib import Path

def merge_knowledge_bases(
    source_projects: list[Path],
    target_project: Path,
    scopes: list[str] = ["universal", "python", "fastapi"]
):
    """Merge knowledge from multiple projects."""
    merged = {"errors": [], "patterns": []}

    for project in source_projects:
        kb_path = project / "docs/knowledge-base"
        for yaml_file in kb_path.rglob("*.yaml"):
            with yaml_file.open() as f:
                data = yaml.safe_load(f)

            # Filter by scope
            if "errors" in data:
                for error in data["errors"]:
                    if error.get("scope") in scopes:
                        merged["errors"].append(error)

    # Write merged knowledge base
    output = target_project / "docs/knowledge-base/shared"
    output.mkdir(exist_ok=True)

    with (output / "merged.yaml").open("w") as f:
        yaml.dump(merged, f)

# Usage
merge_knowledge_bases(
    source_projects=[
        Path("/projects/project-a"),
        Path("/projects/project-b"),
    ],
    target_project=Path("/projects/project-c"),
    scopes=["universal", "python"]
)
```

### Strategy 3: Knowledge Package

**Create pip-installable package:**

```
knowledge-base-package/
├── pyproject.toml
├── src/
│   └── devknowledge/
│       ├── __init__.py
│       ├── data/
│       │   ├── python-common.yaml
│       │   ├── docker-patterns.yaml
│       │   └── git-workflows.yaml
│       └── search.py
└── README.md
```

**pyproject.toml:**
```toml
[project]
name = "devknowledge"
version = "1.0.0"
description = "Shared development knowledge base"

[project.optional-dependencies]
cli = ["click", "pyyaml"]
```

**Usage in projects:**
```bash
pip install devknowledge

# Search shared knowledge
devknowledge search "circular import"

# Export to local knowledge base
devknowledge export --scope python --output docs/knowledge-base/shared/
```

### Strategy 4: Knowledge Base as Service

**Central service approach:**

```
knowledge-api/
├── api/
│   ├── server.py
│   └── routes.py
├── data/
│   ├── errors/
│   └── patterns/
└── frontend/
    └── search-ui/
```

**API Endpoints:**
```
GET  /api/errors?scope=python&tag=async
GET  /api/errors/IMPORT-001
POST /api/errors (contribute new error)
GET  /api/search?q=circular+import
```

**Client in each project:**
```python
# tools/kb-search.py
import requests

def search_knowledge(query: str):
    response = requests.get(
        "https://kb.company.com/api/search",
        params={"q": query, "scope": "python"}
    )
    return response.json()

# Usage
results = search_knowledge("circular import")
for error in results:
    print(f"{error['id']}: {error['title']}")
```

## Recommended Approach

**Hybrid: Local + Shared with Scopes**

```
project/
├── docs/
│   └── knowledge-base/
│       ├── README.md
│       ├── quick-reference.md
│       │
│       ├── errors/              # Project-specific
│       │   ├── project-errors.yaml
│       │   └── domain-errors.yaml
│       │
│       ├── patterns/            # Project-specific
│       │   └── project-patterns.yaml
│       │
│       └── shared/              # From other projects
│           ├── python-common.yaml
│           ├── framework.yaml
│           └── git-universal.yaml
└── tools/
    └── sync-knowledge.py        # Sync from other projects
```

**sync-knowledge.py:**
```python
#!/usr/bin/env python3
"""Sync shared knowledge from other projects."""

import yaml
import shutil
from pathlib import Path

SHARED_SOURCES = [
    "/projects/project-a/docs/knowledge-base",
    "/projects/project-b/docs/knowledge-base",
]

SCOPES_TO_IMPORT = ["universal", "python", "fastapi", "docker"]

def sync_shared_knowledge():
    """Sync shared knowledge from source projects."""
    target = Path("docs/knowledge-base/shared")
    target.mkdir(exist_ok=True)

    for source in SHARED_SOURCES:
        source_path = Path(source)
        for yaml_file in source_path.rglob("*.yaml"):
            with yaml_file.open() as f:
                data = yaml.safe_load(f)

            # Filter by scope
            filtered_errors = []
            if "errors" in data:
                for error in data["errors"]:
                    if error.get("scope", "project") in SCOPES_TO_IMPORT:
                        filtered_errors.append(error)

            # Write if has content
            if filtered_errors:
                scope = data.get("category", "unknown")
                output_file = target / f"{scope}-shared.yaml"

                with output_file.open("w") as f:
                    yaml.dump({
                        "version": "1.0",
                        "category": scope,
                        "source": "shared",
                        "errors": filtered_errors
                    }, f)

if __name__ == "__main__":
    sync_shared_knowledge()
    print("✓ Shared knowledge synced")
```

**Usage:**
```bash
# Run periodically to get latest shared knowledge
python tools/sync-knowledge.py

# Add to pre-commit or CI/CD
```

## Maintenance

### Regular Tasks

**Weekly:**
- Review new errors encountered
- Document solutions found
- Update existing entries if better solutions found

**After Major Features:**
- Document new patterns established
- Add architectural decisions
- Update best practices

**Before Releases:**
- Review and validate all entries
- Update version numbers
- Check for outdated information

### Quality Standards

**Every entry must have:**
- ✅ Clear problem description
- ✅ Working solution with code
- ✅ Prevention strategies
- ✅ Relevant tags
- ✅ Last updated date

**Code examples must:**
- ✅ Be tested and working
- ✅ Be minimal but complete
- ✅ Include comments explaining key parts
- ✅ Show both wrong and correct approaches

### Version Control

**Commit messages:**
```bash
# Adding new error
git commit -m "kb: Add IMPORT-005 FastAPI dependency injection"

# Updating existing
git commit -m "kb: Update TYPE-002 with Python 3.12 syntax"

# Fixing error
git commit -m "kb: Fix code example in TEST-001"
```

**Versioning:**
```yaml
version: "1.0"  # Major.Minor
# Major: Breaking changes to schema
# Minor: New entries, updates to existing
```

## Tools and Automation

### Search Tool

```python
#!/usr/bin/env python3
"""Search knowledge base."""

import yaml
import sys
from pathlib import Path

def search(keyword: str):
    kb_path = Path("docs/knowledge-base")
    results = []

    for yaml_file in kb_path.rglob("*.yaml"):
        with yaml_file.open() as f:
            data = yaml.safe_load(f)

        if "errors" in data:
            for error in data["errors"]:
                if keyword.lower() in str(error).lower():
                    results.append({
                        "file": yaml_file.name,
                        "id": error["id"],
                        "title": error["title"],
                        "tags": error.get("tags", [])
                    })

    return results

if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else ""
    for result in search(keyword):
        print(f"{result['id']}: {result['title']}")
        print(f"  Tags: {', '.join(result['tags'])}")
        print(f"  File: {result['file']}")
        print()
```

### Validation Tool

```python
#!/usr/bin/env python3
"""Validate knowledge base YAML files."""

import yaml
from pathlib import Path

REQUIRED_FIELDS = ["id", "title", "severity", "problem", "solution"]

def validate():
    kb_path = Path("docs/knowledge-base")
    errors = []

    for yaml_file in kb_path.rglob("*.yaml"):
        with yaml_file.open() as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                errors.append(f"{yaml_file}: Invalid YAML - {e}")
                continue

        # Validate structure
        if "errors" in data:
            for i, error in enumerate(data["errors"]):
                for field in REQUIRED_FIELDS:
                    if field not in error:
                        errors.append(
                            f"{yaml_file}: Error {i} missing '{field}'"
                        )

    return errors

if __name__ == "__main__":
    errors = validate()
    if errors:
        for error in errors:
            print(f"❌ {error}")
        sys.exit(1)
    else:
        print("✓ All knowledge base files valid")
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Validate knowledge base before commit
python tools/validate-kb.py

if [ $? -ne 0 ]; then
    echo "Knowledge base validation failed!"
    exit 1
fi
```

## Summary

### Key Takeaways

1. **Use YAML + Markdown**: Best balance of readability and structure
2. **Organize by category**: Separate errors and patterns
3. **Use unique IDs**: `CATEGORY-NNN` for stable references
4. **Add scopes**: Enable cross-project knowledge sharing
5. **Document as you go**: Don't wait, document when you solve
6. **Automate validation**: Ensure quality with scripts
7. **Share knowledge**: Set up sync mechanism for multi-project teams

### Getting Started

1. Copy this guide to new project
2. Create directory structure
3. Start with one category (e.g., testing errors)
4. Document first 3-5 errors
5. Create quick reference
6. Set up search tool
7. Add to team workflow

### Resources

- **This Project**: Complete example implementation
- **Template Files**: Use YAML files as templates
- **Tools**: Copy scripts from `tools/` directory

---

**Version**: 1.0
**Last Updated**: 2026-01-04
**License**: MIT (adapt for your projects)
