# Agent Handoff Pattern - Quality Assurance & Examples

**Extracted from:** agent-handoff.yaml
**Pattern ID:** AGENT-HANDOFF-001

## Quality Assurance

### Before Submitting

- YAML validates without errors
- All required fields present
- ID format correct (CATEGORY-NNN)
- Code examples tested
- No duplicates in KB
- Appropriate scope chosen

### Before Merging

- Validation passes
- Quality score ≥ 75
- No duplicates found
- Enhanced for clarity
- Proper location determined
- Indexed successfully

## Example Workflows

### Scenario 1: New Error Pattern

**Title:** Python Async Timeout Error
**Project:** E-commerce Backend

**Project Agent Steps:**
1. Encounters asyncio.TimeoutError in production
2. Searches KB: `kb search "asyncio timeout"`
3. Not found
4. Implements solution with timeout handling
5. Determines: "Reusable for any async Python code"
6. Creates YAML: `python/errors/async-timeout.yaml`
7. Validates: ✓ Passed
8. Creates GitHub issue #15

**Curator Agent (24h later):**
1. Reviews issue #15
2. Validates YAML: ✓ Passed
3. Checks for duplicates: None found
4. Enhances: Adds more examples, prevention tips
5. Commits: `python/errors/async-timeout.yaml`
6. Closes issue #15 with "Merged!"

**Project Agent:**
1. Receives closure notification
2. Pulls updates: `git pull origin main`
3. Searches: `kb search "async timeout"`
4. Finds contributed entry
5. Benefits: All future projects can use this pattern

### Scenario 2: YAML Error Fix

**Title:** YAML Syntax Error in postgresql/errors.yaml
**Project:** Data Analytics Platform

**Project Agent Steps:**
1. Trying to initialize KB metadata
2. Gets error: "Invalid YAML at line 410"
3. Investigates: `postgresql/errors.yaml:410`
4. Finds: mapping value with colon not quoted
5. Fixes: Changes to single quotes
6. Validates: ✓ Passed
7. Creates GitHub issue #16 with label "yaml-error"

**Curator Agent:**
1. Reviews issue #16 (high priority label)
2. Validates fix: ✓ Correct
3. Commits fix directly (simple fix)
4. Closes issue #16

**Result:** KB metadata initialization works for everyone

## Common Submission Failures

### Title: Common Submission Mistakes to Avoid

### Failure Mode 1: External File References

**Description:** Contributor references local file path instead of embedding YAML

**Example:**
❌ WRONG:
```
The complete YAML file is located at:
docs/knowledge-base/shared/universal/patterns/pattern.yaml
```

**Problem:** File exists in contributor's local repository, NOT in shared-knowledge-base

**Fix:** Always embed full YAML content in issue body

### Failure Mode 2: Missing Actual YAML Content

**Description:** Issue describes pattern but doesn't include YAML entry

**Example:**
❌ WRONG:
- Title, ID, severity specified ✓
- Problem description ✓
- File path provided ✓
- ✗ Actual YAML entry MISSING

**Problem:** Description ≠ Complete YAML entry

**Fix:** Include complete YAML with all required fields

### Failure Mode 3: Template Structure Without Content

**Description:** Follows template but missing actual YAML content

**Example:**
❌ WRONG:
```markdown
## Proposed Entry
**ID:** XXX-YYY
**Title:** Pattern Title
**Category:** category-name

(Stops here, no YAML content)
```

**Problem:** Template structure ≠ Complete entry

**Fix:** Add full YAML content after template headers

## Correct Submission Checklist

### ✅ Before Submitting - Verify All Items

- [ ] Full YAML embedded in issue body (not just file path) **CRITICAL**
- [ ] All required fields present:
  - version
  - category
  - last_updated
  - errors/patterns
  - id
  - title
  - problem
  - solution
- [ ] YAML validated locally:
  ```bash
  python tools/kb.py validate your-entry.yaml
  ```
- [ ] Code examples included and tested
- [ ] Appropriate scope chosen (universal, python, javascript, docker, postgresql)
- [ ] No duplicates in KB:
  ```bash
  kb search 'your keywords'
  ```

## Complete Issue Template

```markdown
---
**Created By:** 🤖 Agent Name
**Project:** PROJECT_NAME
**Date:** YYYY-MM-DD
**Validation:** ✅ Validated locally
---

## Proposed KB Entry

**Full YAML content:**

\`\`\`yaml
version: "1.0"
category: "category-name"
last_updated: "YYYY-MM-DD"

errors:  # or patterns:
  - id: "CATEGORY-NNN"
    title: "Descriptive Title"
    severity: "high"
    scope: "universal"
    tags: ["tag1", "tag2", "tag3"]

    problem: |
      Detailed problem description
      with multiple paragraphs

    root_cause: |
      Explanation of root cause

    solution:
      code: |
        # Solution code here
      explanation: |
        How it works

    prevention:
      - "Prevention tip 1"
      - "Prevention tip 2"
\`\`\`

## Real-World Example

**Project:** PROJECT_NAME
**Scenario:** What happened
**Problem:** Error description
**Solution:** How you fixed it
```

## Real World Failure Examples

### Issue #13: PRE-COMMIT-001
- **Mistake:** Referenced file path instead of embedding YAML
- **Result:** Closed as incomplete, ID reserved
- **Lesson:** Always embed full YAML in issue body

### Issue #12: PY-IMPORT-005
- **Mistake:** Described pattern without including YAML
- **Result:** Closed as incomplete, ID reserved
- **Lesson:** Pattern description ≠ Complete YAML entry

### Issue #14: YAML-VALIDATION-001
- **Mistake:** Followed template but skipped actual content
- **Result:** Closed as incomplete, ID reserved
- **Lesson:** Template structure ≠ Complete entry
