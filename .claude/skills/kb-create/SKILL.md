---
name: "kb-create"
description: "Create new knowledge base entries from scratch following Shared KB standards. Validates, categorizes, and ensures quality before adding to repository"
version: "1.0"
author: "Shared KB Curator"
tags: ["create", "new-entry", "document", "yaml"]
---

# Skill: KB Create

## What this Skill does
Create new knowledge base entries from scratch following Shared KB standards. Validates, categorizes, and ensures quality before adding to repository.

## Trigger
- User mentions "create entry", "add to kb", "new error", "document this"
- After solving a problem that should be documented
- Called by create-entry command
- Part of audit-quality workflow

## What Claude can do with this Skill

### 1. Entry Creation Workflow

#### Step 1: Research & Duplicate Check
```bash
# Check for duplicates
python tools/kb.py search "problem keywords"

# Search by scope
python tools/kb.py search --scope python "async error"
```

#### Step 2: Determine Scope
Use the scope decision tree:
```
Is this error/pattern...
├─ Universal across languages? → universal/
├─ Specific to one language? → <language>/
├─ Framework-specific? → framework/<name>/
├─ Domain/business logic? → domain/
└─ Project-specific only? → project/ (DON'T push to shared KB)
```

#### Step 3: Create Entry Structure
```yaml
version: "1.0"
category: "category-name"
last_updated: "2026-01-07"

errors:
  - id: "CATEGORY-NNN"     # Auto-generate next ID
    title: "Descriptive Title"
    severity: "high"       # critical | high | medium | low
    scope: "python"        # universal | language | framework | domain | project

    problem: |
      Clear description of what went wrong.
      Include symptoms and when it occurs.

    symptoms:
      - "Error message or observable symptom"
      - "Another symptom"

    root_cause: |
      Explanation of why this happens.
      Technical details and context.

    solution:
      code: |
        # Working solution example
        def solution():
            # Correct code
            pass

      explanation: |
        How the solution works.
        Why this approach is correct.

    prevention:
      - "How to avoid this error"
      - "Best practice to follow"

    tags: ["tag1", "tag2", "tag3"]
```

#### Step 4: Validate & Score
```bash
# Validate the entry
python tools/kb.py validate new-entry.yaml

# Check quality score (must be ≥75/100)
python tools/kb.py validate new-entry.yaml --score
```

#### Step 5: Initialize Metadata
```bash
# Create _meta.yaml
python tools/kb.py init-metadata new-entry.yaml
```

#### Step 6: Update Index
```bash
# Rebuild index
python tools/kb.py index --force
```

### 2. ID Generation

Auto-generate next ID in category:
```bash
# Find next available ID
python tools/kb.py create --next-id python
# Output: PYTHON-046
```

ID Format: `CATEGORY-NNN`
- CATEGORY: Scope (PYTHON, JAVASCRIPT, DOCKER, UNIVERSAL, etc.)
- NNN: Sequential number (001-999)

### 3. Template Creation

Generate entry template:
```bash
# Interactive template
python tools/kb.py create --template

# Pre-filled template
python tools/kb.py create --template --scope python --category testing
```

## Key files to reference
- Entry format: `@universal/patterns/shared-kb-yaml-format.yaml`
- Quality standards: `@curator/QUALITY_STANDARDS.md`
- Validation: `@tools/validate-kb.py`
- Curator docs: `@curator/AGENT.md`

## Implementation rules

### Before Creating
1. ✅ **Search for duplicates** (kb-search skill)
2. ✅ **Determine correct scope**
3. ✅ **Check if solution is unique**
4. ✅ **Verify it's not project-specific only**

### While Creating
1. ✅ **Use YAML format** exactly as specified
2. ✅ **Include all required fields**
3. ✅ **Provide working code examples**
4. ✅ **Add prevention strategies**
5. ✅ **Include relevant tags**

### After Creating
1. ✅ **Validate** (kb-validate skill)
2. ✅ **Score ≥75/100** required
3. ✅ **Initialize metadata**
4. ✅ **Rebuild index**
5. ✅ **Add cross-references**

### What NOT to Add
❌ Project-specific errors (use local KB)
❌ One-time occurrences
❌ Incomplete solutions
❌ Theoretical problems (never occurred)
❌ Proprietary information

## Common commands
```bash
# Check for duplicates first
python tools/kb.py search "websocket timeout"

# Create new entry
python tools/kb.py create --scope python --category async

# Generate template
python tools/kb.py create --template > my-entry.yaml

# Validate after creation
python tools/kb.py validate my-entry.yaml

# Initialize metadata
python tools/kb.py init-metadata my-entry.yaml

# Update index
python tools/kb.py index
```

## Quality Checklist

### Completeness (30 points)
- [ ] All required fields present
- [ ] Problem clearly described
- [ ] Solution complete with code
- [ ] Prevention strategies included
- [ ] Tags relevant and specific

### Technical Accuracy (30 points)
- [ ] Code works as described
- [ ] Solution tested
- [ ] No syntax errors
- [ ] Dependencies clear
- [ ] Edge cases addressed

### Documentation (20 points)
- [ ] Clear problem statement
- [ ] Reproducible symptoms
- [ ] Thorough explanation
- [ ] Real-world context
- [ ] Examples provided

### Best Practices (20 points)
- [ ] Follows standards
- [ ] Security considered
- [ ] Performance noted
- [ ] Maintainable solution
- [ ] Cross-references added

**Minimum: 75/100 to commit**

## Entry Types

### Error Entry
```yaml
errors:
  - id: "PYTHON-046"
    title: "TypeError: 'NoneType' object is not subscriptable"
    severity: "high"
    scope: "python"
    # ... rest of structure
```

### Pattern Entry
```yaml
patterns:
  - id: "PATTERN-015"
    title: "Async Context Manager Pattern"
    severity: "medium"
    scope: "universal"
    # ... rest of structure
```

## Related Skills
- `kb-search` - Find duplicates before creating
- `kb-validate` - Validate entry quality
- `kb-index` - Update index after creation
- `audit-quality` - Comprehensive quality check
- `find-duplicates` - Check for similar entries

## Automation
This skill integrates with:
- **PreToolUse hook** - Validates YAML before write
- **PostToolUse hook** - Auto-creates metadata, validates quality
- **quality-gate.sh** - Blocks commit if score < 75

## Example Workflow

### Scenario: Documenting FastAPI WebSocket Error

```bash
# 1. Check for duplicates
python tools/kb.py search "fastapi websocket disconnect"
# No results found ✓

# 2. Determine scope
# Framework-specific (FastAPI) → framework/fastapi/

# 3. Create entry
cat > framework/fastapi/errors/websocket-disconnect.yaml << 'EOF'
version: "1.0"
category: "websocket-errors"
last_updated: "2026-01-07"

errors:
  - id: "FASTAPI-023"
    title: "WebSocket Disconnect Handling"
    severity: "high"
    scope: "framework"
    # ... rest of entry
EOF

# 4. Validate
python tools/kb.py validate framework/fastapi/errors/websocket-disconnect.yaml
# Score: 82/100 ✓

# 5. Initialize metadata
python tools/kb.py init-metadata framework/fastapi/errors/websocket-disconnect.yaml

# 6. Update index
python tools/kb.py index

# 7. Commit
git add framework/fastapi/errors/websocket-disconnect.yaml *_meta.yaml
git commit -m "Add FASTAPI-023: WebSocket Disconnect Handling"
git push origin main
```

## Troubleshooting

### Issue: "Duplicate found"
**Solution:**
- Review existing entry
- Merge if appropriate
- Or add cross-reference instead

### Issue: "Score < 75"
**Fix:**
- Add missing fields
- Improve documentation
- Add more examples
- Include prevention strategies

### Issue: "Wrong scope"
**Check:**
- Is it universal? → universal/
- Language-specific? → <language>/
- Framework-specific? → framework/<name>/
- Project-only? → Don't push to shared KB

---
**Version:** 1.0
**Last Updated:** 2026-01-07
**Skill Type:** Content Creation
**Minimum Quality:** 75/100
