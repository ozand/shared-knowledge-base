# KB Create

Create new knowledge base entries following Shared KB standards.

## Usage
```
/kb-create [options]
```

## Quick Examples

### Interactive Creation
```
/kb-create
```
Guides through all required fields.

### Quick Entry
```
/kb-create --scope python --category async --title "Timeout in await"
```
Generates template with pre-filled fields.

### From Error Message
```
/kb-create --error "TypeError: 'NoneType' object is not subscriptable"
```
Creates entry from error message.

## What This Command Does

1. **Checks for duplicates** using KB search
2. **Generates YAML template** with proper structure
3. **Validates entry** (quality score ≥75/100)
4. **Initializes metadata** if needed
5. **Suggests location** based on scope

**📘 YAML Standards:** `@standards/yaml-standards.md` - Complete format requirements

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `--scope <scope>` | Set scope | `--scope python` |
| `--category <cat>` | Set category | `--category async` |
| `--title <title>` | Set entry title | `--title "Timeout error"` |
| `--error <msg>` | Parse error message | `--error "TypeError"` |
| `--severity <sev>` | Set severity | `--severity high` |

## Workflow

### Step 1: Check Duplicates
```bash
python tools/kb.py search "<keywords>"
```
If exists → update existing entry

### Step 2: Create Entry
Generate YAML with required fields:
- ID (auto-generated: CATEGORY-NNN)
- Title
- Severity
- Scope
- Problem
- Solution

### Step 3: Validate
```bash
python tools/kb.py validate <entry>.yaml
```
Requires quality score ≥75/100

### Step 4: Determine Scope
**Universal scopes** (shared repo):
- docker, universal, python, postgresql, javascript

**Project-specific** (local only):
- framework, domain, project

### Step 5: Save & Index
- Save to appropriate location
- Rebuild index: `python tools/kb.py index -v`

## Entry Template

**Minimal required:**
```yaml
version: "1.0"
category: "<category>"
last_updated: "2026-01-07"

errors:
  - id: "CATEGORY-NNN"
    title: "<Title>"
    severity: "high"
    scope: "python"
    problem: |  # Required
      What went wrong
    solution:   # Required
      code: |
        # Solution
      explanation: |
        How it works
```

**📘 Complete Standards:** `@standards/yaml-standards.md` - All fields, ID format, quality requirements

## Quality Checklist

Before saving:
- [ ] ID format correct (CATEGORY-NNN)
- [ ] All required fields present
- [ ] Code examples tested
- [ ] Quality score ≥75/100
- [ ] Scope correctly identified
- [ ] No duplicate IDs

## Claude's Role

When using this command:

1. **Ask for entry details** (title, scope, problem)
2. **Check for duplicates** in KB
3. **Generate YAML template**
4. **Help write content** (problem, solution, code)
5. **Validate entry** using `kb.py validate`
6. **Determine scope** (universal vs local)
7. **Suggest next steps** (save location, index rebuild)

## Output

**Success:**
```
✅ Entry created: python/errors/async-timeout.yaml
📝 Location: python/errors/
📊 Quality score: 82/100
✅ Validation passed
🔄 Next: Rebuild index with /kb-index
```

**Duplicate found:**
```
⚠️  Similar entry exists: python/errors/async-timeout.yaml
💡 Update existing entry instead?
```

## Common Patterns

### Async Error Entry
```
/kb-create --scope python --category async \
  --title "Coroutine hangs indefinitely"
```
Generates async-focused template

### Docker Error Entry
```
/kb-create --scope docker --category permissions \
  --error "Permission denied"
```
Generates permission error template

### Universal Pattern
```
/kb-create --scope universal --category patterns \
  --title "Progressive Disclosure"
```
Generates pattern entry template

## Related

- `@skills/kb-create/SKILL.md` - KB create skill
- `@standards/yaml-standards.md` - YAML format requirements
- `@standards/quality-gates.md` - Quality requirements (75/100 min)
- `@references/workflows.md` - Complete creation workflow
