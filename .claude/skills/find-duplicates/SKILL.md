---
name: "find-duplicates"
description: "Identify semantically duplicate or near-duplicate knowledge base entries. Suggest merge strategies and help consolidate redundant content"
version: "1.0"
author: "Shared KB Curator"
tags: ["duplicates", "merge", "consolidate", "cleanup"]
---

# Skill: Find Duplicates

## What this Skill does
Identify semantically duplicate or near-duplicate knowledge base entries. Suggest merge strategies and help consolidate redundant content.

## Trigger
- User mentions "duplicates", "similar entries", "merge entries"
- During PR review (check new entries against existing)
- Periodic KB cleanup (monthly)
- Before creating new entry
- Part of quality audit

## What Claude can do with this Skill

### 1. Exact Duplicate Check
```bash
# Find entries with identical titles
python tools/kb.py search --exact-match "Title"

# Check by file hash
find . -name "*.yaml" -exec sha256sum {} \; | sort | uniq -d
```

### 2. Semantic Similarity Search
```bash
# Search for similar problems
python tools/kb.py search --fuzzy "websocket timeout error"

# Find related entries by tags
python tools/kb.py search --tags async,websocket

# Cross-scope duplicate detection
python tools/kb.py find-duplicates --cross-scope
```

### 3. Duplicate Detection Strategy

#### Level 1: Exact Duplicates
```
Same ID, title, and content
→ Delete one, keep canonical source
```

#### Level 2: Near Duplicates
```
Same problem, slightly different solutions
→ Merge, preserve both solutions as alternatives
```

#### Level 3: Semantic Duplicates
```
Different wording, same underlying issue
→ Consolidate, note variations
```

#### Level 4: Related Entries
```
Different aspects of same problem
→ Cross-reference, not duplicates
```

### 4. Duplicate Analysis Output
```
🔍 Duplicate Detection Report
Generated: 2026-01-07 15:23:11

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXACT DUPLICATES (Action Required)
───────────────────────────────────────────
1. [PYTHON-012] Import Error
   📁 python/errors/imports.yaml
   📁 python/errors/import-errors.yaml

   Status: IDENTICAL CONTENT
   Similarity: 100%
   Action: Keep python/errors/imports.yaml
           Delete python/errors/import-errors.yaml

NEAR DUPLICATES (Review & Merge)
───────────────────────────────────────────
1. WebSocket Timeout Errors
   [PYTHON-045] WebSocket Timeout (high)
   📁 python/errors/websocket.yaml
   Score: 78/100

   [FASTAPI-023] FastAPI WebSocket Issues (high)
   📁 framework/fastapi/errors/websocket.yaml
   Score: 82/100

   Similarity: 87%
   Common elements:
    - Problem: WebSocket connections timing out
    - Root cause: Missing timeout configuration
   Differences:
    - PYTHON-045: Generic Python solution
    - FASTAPI-023: FastAPI-specific implementation

   Recommendation: Merge into UNIVERSAL-045
   - Keep generic solution in universal/
   - Add FastAPI-specific note in framework/fastapi/
   - Cross-reference both ways

SEMANTIC DUPLICATES (Consider Consolidation)
───────────────────────────────────────────
1. Async Error Handling
   [PYTHON-018] Async Exceptions (medium)
   📁 python/errors/async-exceptions.yaml

   [PYTHON-031] Awaitable Errors (medium)
   📁 python/errors/awaitable-errors.yaml

   Similarity: 72%
   Different terminology, same underlying issue
   Recommendation: Consolidate under "Async Error Handling"

   Merge strategy:
   - Keep PYTHON-018 as canonical
   - Merge unique content from PYTHON-031
   - Add redirect/alias in PYTHON-031
   - Update all cross-references

RELATED BUT UNIQUE (No Action)
───────────────────────────────────────────
1. Testing Patterns
   [UNIVERSAL-008] Unit Testing (high)
   [UNIVERSAL-009] Integration Testing (medium)
   [UNIVERSAL-010] E2E Testing (low)

   Status: Related topics, not duplicates
   Action: Add cross-references between them

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY
───────────────────────────────────────────
Exact Duplicates:    1 pair (DELETE 1 file)
Near Duplicates:     3 pairs (MERGE REQUIRED)
Semantic Duplicates: 5 pairs (CONSOLIDATE RECOMMENDED)
Related Entries:     8 sets (ADD CROSS-REFERENCES)

Priority Actions:
  1. Delete exact duplicate: python/errors/import-errors.yaml
  2. Merge near duplicates: WebSocket timeout entries
  3. Consolidate semantic duplicates: Async error handling

Estimated Time: 2-3 hours
```

## Key files to reference
- Search tool: `@tools/kb.py` (search command)
- Entry format: `@universal/patterns/shared-kb-yaml-format.yaml`
- Merge workflow: `@curator/WORKFLOWS.md`

## Implementation rules
1. **Always check** before creating new entries
2. **Preserve information** when merging (don't delete content)
3. **Update cross-references** after merge
4. **Document merge** in entry metadata
5. **Verify search** still works after changes

## Common commands
```bash
# Check for duplicates before creating
python tools/kb.py search "potential title"

# Find similar entries
python tools/kb.py find-duplicates --scope python

# Cross-scope duplicate check
python tools/kb.py find-duplicates --cross-scope

# Find entries with similar tags
python tools/kb.py search --tags async,websocket --all

# Fuzzy search for similar problems
python tools/kb.py search --fuzzy "timeout error"
```

## Merge Workflow

### Step 1: Identify Duplicates
```bash
# Search for potential duplicates
python tools/kb.py search "websocket timeout"

# Review all results
# Compare content
# Confirm duplicate status
```

### Step 2: Choose Canonical Entry
```
Criteria for canonical entry:
  ✓ Higher quality score
  ✓ More complete documentation
  ✓ Better code examples
  ✓ More recent (usually)
  ✓ Broader scope (universal > language > framework)
```

### Step 3: Merge Content
```yaml
# Canonical entry
version: "1.0"
category: "websocket-errors"
last_updated: "2026-01-07"

errors:
  - id: "UNIVERSAL-045"
    title: "WebSocket Timeout Handling"
    severity: "high"
    scope: "universal"

    problem: |
      WebSocket connections timing out after inactivity.
      Original sources:
      - PYTHON-045 (Generic Python solution)
      - FASTAPI-023 (FastAPI-specific implementation)

    # ... rest of merged content

    framework_specific:
      fastapi: |
        # FastAPI-specific implementation
        # See framework/fastapi/errors/websocket.yaml for details

    related_entries:
      - "PYTHON-045" # Merged into this entry
      - "FASTAPI-023" # Merged into this entry
```

### Step 4: Update References
```bash
# Find all cross-references to old IDs
grep -r "PYTHON-045" .

# Update to canonical ID
# sed or manual edit

# Validate all changes
python tools/kb.py validate .
```

### Step 5: Mark Old Entries
```yaml
# Deprecated entry
version: "1.0"
category: "websocket-errors"
last_updated: "2026-01-07"

errors:
  - id: "PYTHON-045"
    title: "[DEPRECATED] WebSocket Timeout Handling"
    severity: "high"
    scope: "python"

    problem: |
      This entry has been merged into UNIVERSAL-045.
      Please use UNIVERSAL-045 for the most complete solution.

    solution:
      code: |
        # See UNIVERSAL-045 for complete solution
        # This entry kept for backward compatibility

    deprecated: true
    replaced_by: "UNIVERSAL-045"
    migration_date: "2026-01-07"
```

## Prevention Strategies

### Before Creating New Entry
```bash
# 1. Search for duplicates
python tools/kb.py search "keywords from title"

# 2. Check similar scopes
python tools/kb.py search --scope <target_scope> "keywords"

# 3. Review related tags
python tools/kb.py search --tags <relevant_tags>

# 4. If duplicate found:
#    - Merge instead of creating
#    - Or add to existing entry as alternative
#    - Or cross-reference clearly
```

### During PR Review
```bash
# Check new entries against existing KB
python tools/kb.py validate <new-entry.yaml>
python tools/kb.py search "<keywords from new entry>"

# If duplicate found in PR:
#   - Request changes
#   - Suggest merge strategy
#   - Or provide alternative
```

## Duplicate Types

### Type 1: Exact Duplicate (100% match)
**Action:** Delete one, keep canonical

### Type 2: Near Duplicate (80-99% match)
**Action:** Merge, preserve both solutions

### Type 3: Semantic Duplicate (60-79% match)
**Action:** Consolidate, note variations

### Type 4: Related (40-59% match)
**Action:** Cross-reference, not duplicates

### Type 5: Distinct (<40% match)
**Action:** Keep both, no action needed

## Related Skills
- `kb-search` - Search for potential duplicates
- `kb-create` - Check duplicates before creating
- `merge-entries` - Merge duplicate entries
- `audit-quality` - Quality audit finds duplicates

## Troubleshooting

### Issue: "False positive duplicates"
**Solution:**
- Review content carefully
- Check if solutions are actually different
- Consider if different scopes justify separate entries
- When in doubt, keep both with cross-references

### Issue: "Too many duplicates to handle"
**Strategy:**
1. Prioritize by severity (critical > high > medium)
2. Focus on exact duplicates first (quick wins)
3. Batch similar merges together
4. Schedule cleanup sessions

### Issue: "Merged entry becomes too large"
**Solution:**
- Split into multiple specific entries
- Keep main entry with overview
- Link to specific implementations
- Use progressive disclosure (overview → details)

---
**Version:** 1.0
**Last Updated:** 2026-01-07
**Skill Type:** Content Management
**Similarity Threshold:** 70% (flag for review)
