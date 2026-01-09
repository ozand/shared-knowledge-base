# Automated Validation Setup

**Version:** 1.0
**Last Updated:** 2026-01-09
**Status:** ✅ Active

---

## Overview

The Shared Knowledge Base includes a comprehensive automated validation system that ensures quality standards are maintained. The system runs checks at multiple points:

1. **Pre-commit hooks** - Local validation before commits
2. **GitHub Actions CI/CD** - Automated validation on push/PR
3. **Claude Code hooks** - Agent-side quality gates

---

## Pre-Commit Hooks

### Location
`.git/hooks/pre-commit`

### What It Validates

1. **YAML Syntax**
   - Ensures all YAML files are syntactically valid
   - Uses Python's yaml.safe_load() for validation

2. **KB Entry Structure**
   - Required fields: `version`, `category`, `last_updated`
   - Required sections: `errors:` or `patterns:`
   - Valid for files in `domains/` directory

3. **Version Consistency**
   - Warns if version doesn't match current standard (5.1)
   - Allows 5.0 for backward compatibility

4. **ID Format**
   - Validates CATEGORY-NNN format (e.g., DOCKER-001)
   - Only checks if `errors:` section exists

5. **Markdown Line Length**
   - Warns about lines > 200 characters
   - Helps with readability

### Installation

The hook is automatically installed when you clone the repository. To manually install:

```bash
cp .git/hooks/pre-commit.example .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### Bypassing the Hook

If you need to bypass validation (not recommended):

```bash
git commit --no-verify -m "Your message"
```

---

## GitHub Actions CI/CD

### Location
`.github/workflows/kb-validation.yml`

### Triggers

- **Push** to main/master/develop branches
- **Pull Request** to main/master/develop branches
- **Manual** workflow dispatch

### Jobs

#### 1. validate-yaml
Validates YAML syntax and KB entry structure

**Checks:**
- YAML parsing
- Required fields (version, category, last_updated)
- Entry structure (id, title, severity, scope, problem, solution)
- ID format validation

#### 2. validate-python
Validates Python tools and scripts

**Checks:**
- Python syntax (py_compile)
- Runs pytest if tests/ directory exists
- All files in tools/ directory

#### 3. quality-check
Runs quality gate checks

**Checks:**
- Required fields presence
- Version field format
- Category field format
- last_updated field format

### Viewing Results

Validation results appear in:
- GitHub Actions tab (workflow runs)
- PR checks section
- Commit status

---

## Claude Code Hooks

### Location
`.claude/hooks/`

### Available Hooks

1. **quality-gate.sh**
   - Validates YAML entries before writing
   - Checks required fields
   - Validates ID format
   - Returns error code if validation fails

2. **validate-yaml-before-edit.sh**
   - Validates YAML before editing
   - Ensures file is parseable

3. **validate-yaml-before-write.sh**
   - Validates YAML after editing
   - Catches syntax errors early

4. **auto-format-yaml.sh**
   - Automatically formats YAML files
   - Ensures consistent indentation

5. **check-index.sh**
   - Validates search index
   - Rebuilds if needed

### Hook Configuration

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [".claude/hooks/validate-yaml-before-edit.sh"],
    "PostToolUse": [".claude/hooks/quality-gate.sh", ".claude/hooks/auto-format-yaml.sh"],
    "SessionStart": [".claude/hooks/check-index.sh"]
  }
}
```

---

## Validation Criteria

### Required Fields (Top-Level)

Every KB entry must have:

```yaml
version: "5.1"           # Schema version
category: "category-name" # Domain category
last_updated: "2026-01-09" # Last modification date
```

### Required Sections

Every KB entry must have either:

```yaml
errors:
  - id: "ERROR-001"
    # ... error fields
```

OR

```yaml
patterns:
  - id: "PATTERN-001"
    # ... pattern fields
```

### Required Entry Fields (if errors section)

```yaml
errors:
  - id: "CATEGORY-NNN"      # Unique identifier
    title: "Error Title"     # Human-readable title
    severity: "high"         # critical | high | medium | low
    scope: "python"          # Domain scope
    problem: |               # Problem description
      What went wrong
    solution:                # Solution
      code: |
        # Solution code
      explanation: |
        How it works
```

### ID Format

**Pattern:** `CATEGORY-NNN`

**Examples:**
- ✅ `DOCKER-001`
- ✅ `PYTHON-042`
- ✅ `JS-ASYNC-001`
- ❌ `docker-001` (lowercase)
- ❌ `ERROR-1` (wrong format)
- ❌ `ERROR001` (missing hyphen)

### Scope Values

Valid scopes (case-sensitive):
- `universal` - Cross-language patterns
- `python` - Python-specific
- `javascript` - JavaScript/Node.js
- `docker` - Docker/containerization
- `postgresql` - PostgreSQL database
- `vps` - VPS administration
- `claude-code` - Claude Code specific
- `framework` - Framework-specific
- `project` - Project-specific (local only)

### Severity Values

Valid severities (case-sensitive):
- `critical` - Breaking changes, security issues
- `high` - Major problems
- `medium` - Moderate issues
- `low` - Minor improvements

---

## Local Validation Commands

### Validate Single File

```bash
python tools/kb.py validate domains/docker/errors/common-errors.yaml
```

### Validate All Files

```bash
python tools/kb.py validate domains/
```

### Validate with Verbose Output

```bash
python tools/kb.py validate domains/ --verbose
```

### Rebuild Index After Validation

```bash
python tools/kb.py index --force -v
```

---

## Troubleshooting

### Pre-commit hook not running

**Problem:** Commits go through without validation

**Solution:**
```bash
# Check if hook exists
ls -la .git/hooks/pre-commit

# Make executable
chmod +x .git/hooks/pre-commit

# Test hook
.git/hooks/pre-commit
```

### Validation failures

**Problem:** Validation fails but file looks correct

**Solution:**
```bash
# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('your_file.yaml'))"

# Validate with detailed output
python tools/kb.py validate your_file.yaml --verbose

# Check for hidden characters
cat -A your_file.yaml | grep "\\^M\\$"  # Check for Windows line endings
```

### CI/CD failures

**Problem:** GitHub Actions fails but local passes

**Solution:**
1. Check Python version (CI uses 3.11)
2. Check for platform-specific issues
3. Review workflow logs in Actions tab
4. Test locally with same Python version:
   ```bash
   python3.11 -m pip install pyyaml
   python3.11 tools/kb.py validate domains/
   ```

### False positives

**Problem:** Valid file fails validation

**Solution:**
1. Check if file is in `domains/` (only these are validated)
2. Verify all required fields are present
3. Check ID format matches CATEGORY-NNN
4. Ensure scope and severity values are valid
5. Review validation error messages carefully

---

## Best Practices

### 1. Commit frequently
Small commits make it easier to identify validation failures

### 2. Run validation locally
Save time by catching errors before pushing

### 3. Don't bypass hooks
Only use `--no-verify` when absolutely necessary

### 4. Fix validation errors immediately
Don't accumulate validation debt

### 5. Keep dependencies updated
```bash
pip install --upgrade pyyaml
```

### 6. Test workflow changes
Use workflow dispatch to test before pushing

---

## Maintenance

### Updating Validation Rules

1. Modify `.git/hooks/pre-commit` for local validation
2. Modify `.github/workflows/kb-validation.yml` for CI/CD
3. Update this documentation
4. Test with both valid and invalid files

### Adding New Checks

1. Implement check in hook script
2. Test locally with `./.git/hooks/pre-commit`
3. Update CI/CD workflow if needed
4. Document in VALIDATION-SETUP.md

---

## Related Documentation

- **YAML Standards:** `@standards/yaml-standards.md`
- **Quality Gates:** `@standards/quality-gates.md`
- **KB Tools Reference:** `@references/cli-reference.md`
- **Agent Instructions:** `@universal/agent-instructions/base-instructions.yaml`

---

## Support

If you encounter validation issues:

1. Check this documentation first
2. Review error messages carefully
3. Search existing issues on GitHub
4. Create new issue with:
   - File being validated
   - Error message
   - Steps to reproduce
   - Your environment (OS, Python version)

---

**End of Documentation**
