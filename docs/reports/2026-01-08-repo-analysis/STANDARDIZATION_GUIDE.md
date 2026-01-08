# Consistency Standardization Guide

**Version:** 1.0
**Last Updated:** 2026-01-08
**Maintained By:** Agent 6 - Consistency & Standards Validator

---

## Overview

This guide provides the standards and procedures for maintaining consistency across the Shared Knowledge Base repository. All contributors, agents, and automated tools should follow these standards to ensure quality and maintainability.

### Purpose

- Establish uniform formatting across all files
- Enable automated validation and indexing
- Improve searchability and discoverability
- Facilitate collaboration and maintenance
- Ensure professional presentation

### Scope

Applies to:
- All YAML files in `domains/` directory
- All Markdown documentation files
- Configuration files
- Agent instructions and skills

---

## YAML File Standards

### Required Fields (Minimum)

Every YAML entry **MUST** include these fields:

```yaml
version: "5.1"                    # Schema version (REQUIRED)
category: "category-name"          # Domain category (REQUIRED)
last_updated: "2026-01-08"        # Last modification date (REQUIRED)

errors:                            # or patterns:
  - id: "CATEGORY-001"             # Unique identifier (REQUIRED)
    title: "Descriptive Title"     # Human-readable title (REQUIRED)
    scope: "python"                # Domain scope (REQUIRED)
    problem: |                     # Problem description (REQUIRED)
      What went wrong
    solution:                      # Solution (REQUIRED)
      code: |
        # Solution code
      explanation: |
        How it works
```

### Version Field

**Format:** `"5.1"` (with double quotes)

**Allowed Values:**
- `"5.1"` - Current standard (✅ USE THIS)
- `"5.0"` - Previous version (acceptable)
- `"4.0"` - Legacy version (update to 5.1)

**Deprecated:**
- `"1.0"`, `"2.0"`, `"3.0"` - Migrate to 5.1

**Examples:**
```yaml
# ✅ Correct
version: "5.1"

# ❌ Wrong - missing quotes
version: 5.1

# ❌ Wrong - old version
version: "1.0"

# ❌ Wrong - incorrect format
version: v5.1
```

### ID Format

**Pattern:** `CATEGORY-NNN` or `CATEGORY-SUBCATEGORY-NNN`

**Rules:**
- All uppercase letters
- Hyphen-separated components
- Numeric suffix (001, 002, etc.)
- Sequential numbering within category

**Examples:**
```yaml
# ✅ Correct - Simple format
id: "DOCKER-001"
id: "PYTHON-042"

# ✅ Correct - Subcategory format
id: "JS-ASYNC-001"
id: "POSTGRES-PERF-001"
id: "CLAUDE-CODE-HOOKS-001"

# ❌ Wrong - lowercase
id: "docker-001"

# ❌ Wrong - wrong separator
id: "DOCKER_001"

# ❌ Wrong - wrong format
id: "error-1"
id: "ERROR001"
```

### Scope Field

**Allowed Values** (case-sensitive):

| Scope | Description | Directory |
|-------|-------------|-----------|
| `universal` | Cross-language patterns | `domains/universal/` |
| `python` | Python-specific | `domains/python/` |
| `javascript` | JavaScript/Node.js | `domains/javascript/` |
| `docker` | Docker/containerization | `domains/docker/` |
| `postgresql` | PostgreSQL database | `domains/postgresql/` |
| `vps` | VPS administration | `domains/vps/` |
| `fastapi` | FastAPI framework | `domains/framework/fastapi/` |
| `claude-code` | Claude Code specific | `domains/claude-code/` |
| `project` | Project-specific (local only) | `.kb/project/` |

**Examples:**
```yaml
# ✅ Correct
scope: "python"
scope: "universal"

# ❌ Wrong - lowercase
scope: "Python"

# ❌ Wrong - invalid value
scope: "backend"
```

### Date Format

**Field:** `last_updated`

**Format:** `YYYY-MM-DD` (ISO 8601)

**Rules:**
- Always with double quotes
- No time component (date only)
- Use current date when modifying

**Examples:**
```yaml
# ✅ Correct
last_updated: "2026-01-08"

# ❌ Wrong - missing quotes
last_updated: 2026-01-08

# ❌ Wrong - wrong format
last_updated: "01/08/2026"
last_updated: "Jan 8, 2026"

# ❌ Wrong - includes time (not needed)
last_updated: "2026-01-08T10:30:00Z"
```

### Category Field

**Format:** Lowercase, hyphen-separated

**Rules:**
- Should relate to domain/directory
- Descriptive but concise
- Use existing categories when possible

**Examples:**
```yaml
# ✅ Correct
category: "docker-errors"
category: "python-testing"
category: "claude-code-organization"

# ❌ Wrong - uppercase
category: "Docker-Errors"

# ❌ Wrong - underscores
category: "docker_errors"
```

### Complete Example

```yaml
version: "5.1"
category: "docker-errors"
last_updated: "2026-01-08"

errors:
  - id: "DOCKER-024"
    title: "Healthcheck Command Not Available in Container Image"
    severity: "medium"
    scope: "docker"
    tags:
      - docker
      - healthcheck
      - containers

    problem: |
      Healthcheck configured to use a command that doesn't exist in the
      container image (e.g., curl in minimal Python images). Container
      shows unhealthy even though application is working correctly.

    solution:
      code: |
        services:
          app:
            image: python:3.11-slim
            healthcheck:
              test: ["CMD-SHELL", "python -c 'import urllib.request; urllib.request.urlopen(\"http://localhost:8501/_stcore/health\").read()'"]
              interval: 30s
              timeout: 10s
              retries: 3
              start_period: 40s

      explanation: |
        Uses Python's built-in urllib library instead of external curl command.
        This works in minimal images that don't include curl.
```

---

## Markdown File Standards

### Filename Conventions

**Rule:** Use `kebab-case` for all filenames

**Exceptions:** Standard names like `README.md`, `LICENSE.md`, `CHANGELOG.md`

**Examples:**
```
✅ Correct:
quick-start-guide.md
api-reference.md
yaml-standards.md
README.md

❌ Wrong:
Quick Start Guide.md
api_reference.md
YAML-Standards.md
quick start guide.md
```

### Header Hierarchy

**Rules:**
- Start with h1 (`# Title`)
- No skipped levels (h1 → h2 → h3)
- Use sentence case for headers
- One blank line before headers

**Examples:**
```markdown
# Main Title (h1)

## Section (h2)

### Subsection (h3)

#### Detail (h4)

# ✅ Correct - progressive levels

## Main Section

### Subsection

#### Detail

# ❌ Wrong - skipped level
## Main Section

#### Detail (skipped h3)
```

### Code Block Formatting

**Rule:** Always specify language after opening ```

**Language Tags:**
- Use lowercase for languages
- Use standard language identifiers

**Examples:**
````markdown
✅ Correct:
```python
def hello():
    print("Hello, World!")
```

```bash
npm install
```

```yaml
version: "5.1"
```

❌ Wrong:
```Python
def hello():
    print("Hello, World!")
```

``` (no language tag)
def hello():
    print("Hello, World")
```
````

### List Formatting

**Rule:** Use `-` for all bullet points (consistent)

**Examples:**
```markdown
✅ Correct:
- First item
- Second item
  - Nested item
  - Another nested
- Third item

❌ Wrong - mixed styles:
- First item
* Second item
+ Third item
```

### Table of Contents

**Rule:** Files >500 lines MUST have TOC

**Location:** Within first 50 lines

**Format:**
```markdown
## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Steps](#steps)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
```

### Cross-References

**Format:** `@path/to/file.md`

**Rules:**
- Use relative paths from repository root
- All references must be valid
- Test references before committing

**Examples:**
```markdown
✅ Correct:
See `@standards/yaml-standards.md` for details.
Reference: `@references/cli-reference.md`

❌ Wrong:
See `yaml-standards.md` (missing @)
Reference: `@nonexistent-file.md` (broken link)
```

---

## Validation Commands

### Check YAML Syntax

```bash
# Check all YAML files
yamllint domains/**/*.yaml

# Check specific file
yamllint domains/docker/errors/common-errors.yaml

# Find files with syntax errors
find domains -name "*.yaml" -exec yamllint {} \; 2>&1 | grep "error"
```

### Validate with kb.py

```bash
# Validate all files
python tools/kb.py validate domains/

# Validate specific file
python tools/kb.py validate domains/docker/errors/common-errors.yaml

# Validate and show details
python tools/kb.py validate domains/ --verbose
```

### Find Inconsistencies

```bash
# Find non-standard version fields
grep -r 'version:' domains/ | grep -v 'version: "5.1"' | grep -v 'version: "5.0"'

# Find missing required fields
for file in domains/**/*.yaml; do
  if ! grep -q 'version:' "$file"; then
    echo "Missing version: $file"
  fi
  if ! grep -q 'category:' "$file"; then
    echo "Missing category: $file"
  fi
  if ! grep -q 'last_updated:' "$file"; then
    echo "Missing last_updated: $file"
  fi
done

# Find wrong ID formats
grep -rh 'id:' domains/ | grep -vE 'id: "[A-Z]+-[\w-]*-\d+"'

# Find broken references
grep -rh '@[a-z/]*\.md' docs/ | while read ref; do
  path="${ref#@}"
  if [ ! -f "$path" ]; then
    echo "Broken reference: $ref"
  fi
done
```

---

## Migration Procedures

### When Updating Existing Files

**Checklist:**
- [ ] Read current file content
- [ ] Update version to `"5.1"` if needed
- [ ] Verify/fix ID format
- [ ] Check scope value is valid
- [ ] Ensure `last_updated` is current date
- [ ] Validate: `python tools/kb.py validate <file>`
- [ ] Rebuild index: `python tools/kb.py index -v`
- [ ] Test search: `python tools/kb.py search <id>`

### When Creating New Files

**Checklist:**
- [ ] Use kebab-case filename
- [ ] Include all required fields
- [ ] Assign sequential ID in category
- [ ] Set appropriate scope
- [ ] Write clear problem/solution
- [ ] Validate before committing
- [ ] Add to domain index if applicable

### Batch Updates

**Script for adding missing metadata:**

```python
#!/usr/bin/env python3
import yaml
from datetime import datetime
from pathlib import Path

def add_missing_metadata(file_path):
    """Add missing metadata to YAML file."""
    with open(file_path) as f:
        data = yaml.safe_load(f) or {}

    # Add missing fields
    if 'version' not in data:
        data['version'] = "5.1"

    if 'last_updated' not in data:
        data['last_updated'] = datetime.now().strftime('%Y-%m-%d')

    # Write back
    with open(file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    print(f"Updated: {file_path}")

# Process all YAML files
for yaml_file in Path('domains').rglob('*.yaml'):
    if '_meta' not in yaml_file.name:  # Skip metadata files
        add_missing_metadata(yaml_file)
```

---

## Quality Scoring

### Consistency Score Rubric

| Score | Grade | Criteria | Action |
|-------|-------|----------|--------|
| **95-100** | Excellent | Perfect consistency, no issues | KEEP |
| **85-94** | Very Good | Minor inconsistencies (1-2 issues) | MONITOR |
| **75-84** | Good | Some inconsistencies (3-5 issues) | UPDATE |
| **65-74** | Fair | Multiple inconsistencies (6-10 issues) | STANDARDIZE |
| **<65** | Poor | Major consistency problems | STANDARDIZE (Critical) |

### Score Calculation

**Points Deducted:**
- Missing version: -15 points
- Missing category: -10 points
- Missing last_updated: -10 points
- Non-standard version: -5 points
- ID format issue: -3 points each
- Invalid scope: -5 points
- Date format issue: -3 points

**Minimum Passing Score:** 75/100 (Good)

---

## Automated Enforcement

### Pre-Commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "🔍 Running consistency checks..."

# Check YAML syntax
if ! yamllint domains/**/*.yaml; then
    echo "❌ YAML syntax errors found"
    exit 1
fi

# Validate with kb.py
if ! python tools/kb.py validate domains/; then
    echo "❌ Validation failed"
    exit 1
fi

echo "✅ All checks passed"
```

**Make executable:**
```bash
chmod +x .git/hooks/pre-commit
```

### GitHub Actions Workflow

Create `.github/workflows/consistency.yml`:

```yaml
name: Consistency Checks

on:
  push:
    paths:
      - 'domains/**/*.yaml'
      - 'docs/**/*.md'
  pull_request:
    paths:
      - 'domains/**/*.yaml'
      - 'docs/**/*.md'

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install yamllint
          pip install pyyaml

      - name: Validate YAML syntax
        run: |
          yamllint domains/**/*.yaml

      - name: Validate with kb.py
        run: |
          python tools/kb.py validate domains/

      - name: Check consistency
        run: |
          python tools/check_consistency.py
```

### Markdown Linting

**Install markdownlint:**
```bash
npm install -g markdownlint-cli
```

**Configuration:** `.markdownlint.json`
```json
{
  "default": true,
  "MD013": false,  # Line length (disable)
  "MD033": false,  # HTML (allow)
  "MD041": false   # First line heading (flexible)
}
```

**Run:**
```bash
markdownlint '**/*.md'
```

---

## Common Issues and Fixes

### Issue: Missing Version Field

**Problem:**
```yaml
category: "docker-errors"
last_updated: "2026-01-08"
# Missing version!
```

**Fix:**
```yaml
version: "5.1"  # Add this line
category: "docker-errors"
last_updated: "2026-01-08"
```

### Issue: Wrong ID Format

**Problem:**
```yaml
errors:
  - id: "docker_001"  # Wrong format
```

**Fix:**
```yaml
errors:
  - id: "DOCKER-001"  # Correct format
```

### Issue: Invalid Scope

**Problem:**
```yaml
errors:
  - id: "DOCKER-001"
    scope: "Docker"  # Wrong case
```

**Fix:**
```yaml
errors:
  - id: "DOCKER-001"
    scope: "docker"  # Correct (lowercase)
```

### Issue: Missing TOC

**Problem:** File has 600 lines but no TOC

**Fix:** Add after title:
```markdown
# Main Title

## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)
- [Section 3](#section-3)
```

---

## Best Practices

### 1. Progressive Disclosure

- Keep files focused on single topic
- Use @references for additional details
- Link to related resources

### 2. Consistent Naming

- Use existing category names when possible
- Follow established ID patterns
- Maintain sequential numbering

### 3. Regular Updates

- Update `last_updated` when modifying
- Increment version when breaking changes
- Document changes in commit messages

### 4. Validation First

- Always validate before committing
- Run tests after changes
- Verify search functionality

### 5. Documentation

- Comment complex sections
- Provide examples in solutions
- Link to external resources

---

## Tools and Resources

### Internal Tools

- **`tools/kb.py`** - Main validation and indexing tool
- **`tools/kb_validate.py`** - Specific validation commands
- **`python tools/kb.py validate <file>`** - Validate single file
- **`python tools/kb.py index -v`** - Rebuild search index

### External Tools

- **`yamllint`** - YAML syntax validation
- **`markdownlint`** - Markdown linting
- **`pre-commit`** - Git hooks framework

### Documentation

- **`@standards/yaml-standards.md`** - Complete YAML spec
- **`@standards/quality-gates.md`** - Quality requirements
- **`@references/cli-reference.md`** - CLI commands
- **`@references/workflows.md`** - Update workflows

---

## Maintenance

### Regular Tasks

**Daily:**
- Validate new files before committing
- Run `kb.py validate` after changes

**Weekly:**
- Check for broken references
- Update stale dates
- Review consistency scores

**Monthly:**
- Full repository validation
- Update standards as needed
- Review and update this guide

### Version Updates

When schema version changes:
1. Update all files to new version
2. Update this guide
3. Update validation tools
4. Communicate changes to team

---

## Troubleshooting

### Validation Fails

**Error:** `Missing required field: version`

**Fix:** Add version field to file:
```yaml
version: "5.1"
```

**Error:** `Invalid ID format`

**Fix:** Ensure ID matches `CATEGORY-NNN`:
```yaml
id: "DOCKER-001"  # ✅ Correct
```

### Search Not Working

**Symptom:** Can't find entry with `kb.py search`

**Fixes:**
1. Rebuild index: `python tools/kb.py index --force -v`
2. Check ID format is correct
3. Verify file is in indexed directory
4. Check for validation errors

### Broken References

**Symptom:** `@reference/file.md` link doesn't work

**Fixes:**
1. Verify file exists at path
2. Check for typos in reference
3. Use absolute paths from repository root
4. Test reference by opening file

---

## Conclusion

Following these standards ensures:

✅ **Consistency** - Uniform formatting across repository
✅ **Quality** - High-quality, maintainable content
✅ **Discoverability** - Easy to find and use
✅ **Automation** - Enables validation and indexing
✅ **Collaboration** - Clear standards for contributors

**Remember:** Consistency is not about rigid rules, but about creating a reliable, professional knowledge base that serves everyone effectively.

---

**Questions or Issues?**

- Check `@references/cli-reference.md` for command help
- Review `@standards/yaml-standards.md` for detailed spec
- Run `python tools/kb.py validate <file>` for specific errors

---

**End of Guide**
