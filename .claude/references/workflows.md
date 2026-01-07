# Workflows Reference - Critical KB Workflows

**Detailed workflows for common knowledge base operations**

---

## Workflow 1: User Reports an Error

### Step 1: Search Knowledge Base

```bash
# Search for error message or symptoms
python tools/kb.py search "error message"
python tools/kb.py search --category python "asyncio"
```

**Expected outcomes:**
- ✅ **Found:** Return solution to user → Done
- ❌ **Not found:** Proceed to Step 2

---

### Step 2: Solve and Document

1. **Solve the problem**
   - Investigate root cause
   - Develop solution
   - Test solution thoroughly

2. **Document in YAML**
   ```yaml
   version: "1.0"
   category: "category-name"
   last_updated: "2026-01-07"

   errors:
     - id: "ERROR-001"
       title: "Error Title"
       severity: "high"
       scope: "python"  # Determine scope (see below)
       problem: |
         Description of what went wrong
       symptoms:
         - "Error message or symptom"
       root_cause: |
         Explanation of why it happens
       solution:
         code: |
           # Correct code example
         explanation: |
           How the solution works
       prevention:
         - "How to avoid this error"
       tags: ["tag1", "tag2"]
   ```

---

### Step 3: Determine Scope

**Critical decision:** Is this error **universal** (shared) or **project-specific** (local)?

**Ask these questions:**

✅ **Add to SHARED KB if:**
- Scope is: `docker`, `universal`, `python`, `postgresql`, `javascript`
- Solution applies to multiple projects/environments
- Error is common across industry
- Framework-agnostic or standard use case

❌ **Keep in LOCAL KB if:**
- Scope is: `project`, `domain`, `framework`
- Solution depends on specific infrastructure
- Environment-specific or one-time occurrence
- Business logic specific

---

### Step 4A: Universal Scope Workflow

**If scope is universal** (docker, universal, python, postgresql, javascript):

```bash
# 1. Create in SHARED KB (not local)
path/to/shared-knowledge-base/<scope>/errors/error-file.yaml

# Example:
# shared-knowledge-base/python/errors/async/await-in-event-loop.yaml

# 2. Validate YAML
python tools/kb.py validate path/to/error-file.yaml

# 3. Initialize metadata
python tools/kb.py init-metadata

# 4. IMMEDIATELY commit and push to shared repository
cd path/to/shared-knowledge-base
git add <scope>/errors/error-file.yaml *_meta.yaml
git commit -m "Add ERROR-ID: Error Title

- Brief description
- Related issues
- Real-world example

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

git push origin main

# 5. If push fails with conflicts:
git pull --rebase origin main
git push origin main

# 6. Rebuild index
python tools/kb.py index --force -v
```

**✅ Confirm to user:**
```
✅ KB entry added to shared-knowledge-base repository
📦 Committed: <commit-hash>
🚀 Pushed to: origin/main
🔍 Index rebuilt
🌐 Available at: https://github.com/ozand/shared-knowledge-base
```

---

### Step 4B: Project-Specific Scope Workflow

**If scope is project-specific** (project, domain, framework):

```bash
# 1. Create in LOCAL KB (not shared)
path/to/project/docs/knowledge-base/<scope>/errors/error-file.yaml

# 2. Add local_only metadata
# In YAML:
local_only: true

# 3. Validate YAML
python tools/kb.py validate path/to/error-file.yaml

# 4. Rebuild index (local only)
python tools/kb.py index -v

# 5. Commit to local project (NOT shared repository)
cd path/to/project
git add docs/knowledge-base/
git commit -m "Add local ERROR-ID: Error Title"
```

**✅ Confirm to user:**
```
✅ KB entry added to local knowledge base
📝 Local only: Not shared with repository
🔍 Local index rebuilt
```

---

## Workflow 2: Quality Validation

### Before Committing to Shared Repository

**Checklist:**

```bash
# 1. Validate YAML syntax
python tools/kb.py validate <file>

# Expected output: ✅ All validation checks passed

# 2. Check quality score
python tools/kb.py check-quality <file>

# Minimum score for shared repository: 75/100

# 3. Test code examples
# Copy code from solution.code
# Run in relevant environment
# Verify it works as described

# 4. Check required fields
# Required: id, title, severity, scope, problem, solution
# Optional: symptoms, root_cause, prevention, tags, examples

# 5. Verify scope decision
# Is this truly universal? (see Workflow 1, Step 3)
# Should this be in local KB instead?

# 6. Check for duplicates
python tools/kb.py search --category <category> "<keywords>"

# If similar entry exists:
# - Merge content into existing entry
# - OR update existing entry with new information
# - OR document why separate entry is needed
```

**Quality Gate:**
```
IF quality_score >= 75 AND validation_passes AND tested AND scope_correct:
    COMMIT to shared repository
ELSE:
    Improve entry before committing
```

---

## Workflow 3: Regular Maintenance

### Weekly Maintenance (5 minutes)

```bash
# 1. Check for stale entries
python tools/kb.py check-freshness

# 2. Rebuild index if needed
python tools/kb.py index -v

# 3. Review recent searches
python tools/kb.py analyze-usage | grep "last_7_days"
```

**Actions:**
- Update entries with declining quality
- Consider adding entries for frequent searches with no results
- Archive entries with very low usage (if outdated)

---

### Monthly Maintenance (30 minutes)

```bash
# 1. Full validation
python tools/kb.py validate .

# 2. Analyze usage patterns
python tools/kb.py analyze-usage

# 3. Check library versions
python -m tools.kb_versions check --all

# 4. Predict updates needed
python -m tools.kb_predictive predict-updates --days 30

# 5. Suggest new entries
python -m tools.kb_predictive suggest-entries
```

**Actions:**
- Update entries with old library versions
- Add entries for suggested topics
- Improve low-quality entries (< 75/100)
- Remove or archive obsolete entries

---

### Quarterly Maintenance (2 hours)

```bash
# 1. Comprehensive quality review
python tools/kb.py validate .
python tools/kb.py check-freshness
python tools/kb.py analyze-usage

# 2. Update all version information
python -m tools.kb_versions scan
python -m tools.kb_versions check --all

# 3. Long-term predictions
python -m tools.kb_predictive predict-updates --days 90

# 4. Review documentation
# - Check if all examples still work
# - Update for latest best practices
# - Add new patterns discovered

# 5. Clean up
# - Archive entries with usage_count = 0
# - Merge duplicate entries
# - Reorganize categories if needed
```

**Actions:**
- Major update of outdated entries
- Restructure categories based on usage patterns
- Deprecate obsolete entries
- Add comprehensive examples

---

## Workflow 4: Synchronization with Shared Repository

### Initial Setup (One-time)

```bash
# 1. Navigate to project's knowledge base directory
cd path/to/project/docs/knowledge-base

# 2. Clone shared repository as submodule
git submodule add https://github.com/ozand/shared-knowledge-base shared
cd shared
git submodule update --init --recursive

# 3. Create symlink to shared entries (optional)
ln -s shared/python/ ../python-shared
ln -s shared/docker/ ../docker-shared
```

---

### Regular Updates (Weekly)

```bash
# In parent project
cd path/to/project

# 1. Update submodule to latest
git submodule update --remote docs/knowledge-base/shared

# 2. Rebuild local index (includes shared entries)
python tools/kb.py index --force -v

# 3. Commit submodule update
git add docs/knowledge-base/shared
git commit -m "Update shared-knowledge-base to latest"
```

---

### Contributing to Shared Repository

**When you create universal scope entries:**

```bash
# 1. Create in shared repository (not local!)
cd docs/knowledge-base/shared
# Create/edit <scope>/errors/file.yaml

# 2. Validate and test
python tools/kb.py validate <file>
# Test code examples

# 3. Commit to shared repository
git add <file>
git commit -m "Add ERROR-ID: Title

- Description
- Real-world example

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# 4. Push to shared repository
git push origin main

# 5. In parent project, update submodule
cd ../../..
git submodule update --remote docs/knowledge-base/shared
git add docs/knowledge-base/shared
git commit -m "Update shared-knowledge-base with new entry"
```

---

## Workflow 5: Troubleshooting

### Issue: Search Returns No Results

**Diagnosis:**
```bash
# 1. Check if index exists
ls -la _index.yaml

# 2. Check index freshness
stat _index.yaml  # Last modified date?

# 3. Validate entries
python tools/kb.py validate . | grep "ERROR"
```

**Solutions:**
```bash
# Rebuild index
python tools/kb.py index --force -v

# If entries have errors, fix them:
# - Fix YAML syntax
# - Add missing required fields
# - Correct ID format (CATEGORY-NNN)

# Rebuild after fixes
python tools/kb.py index --force -v
```

---

### Issue: Validation Fails

**Common errors and fixes:**

**Error:** `Missing required field: id`
```yaml
# Fix: Add unique ID
errors:
  - id: "PYTHON-001"  # Add this line
    title: "Error Title"
```

**Error:** `Invalid ID format: python-error-1`
```yaml
# Fix: Use CATEGORY-NNN format
errors:
  - id: "PYTHON-001"  # Not: python-error-1
```

**Error:** `Duplicate ID found`
```bash
# Find duplicate
grep -r "PYTHON-001" .

# Fix: Change one ID to unique value
errors:
  - id: "PYTHON-002"  # Changed from PYTHON-001
```

**Error:** `YAML syntax error`
```bash
# Check syntax
python -c "import yaml; yaml.safe_load(open('file.yaml'))"

# Common YAML issues:
# - Indentation (use spaces, not tabs)
# - Missing quotes around special characters
# - Multiline strings need | or >
```

---

### Issue: Git Push Fails with Conflicts

```bash
# Diagnose conflict
git push origin main
# ERROR: failed to push some refs

# Solution: Rebase with remote
git pull --rebase origin main

# If conflicts:
# 1. Edit conflicted files
# 2. Mark as resolved: git add <file>
# 3. Continue rebase: git rebase --continue
# 4. Push again: git push origin main
```

**Prevention:**
```bash
# Before starting work, pull latest
git pull origin main

# After committing, push immediately
git push origin main

# Avoid long-running branches with many commits
```

---

### Issue: Hook Not Executing

```bash
# Check hook configuration
cat .claude/settings.json

# Test hook manually
# For shell hooks:
bash .claude/hooks/validate-yaml-before-edit.sh

# For LLM hooks:
# Check prompt syntax
# Verify matchers are correct

# Check hook logs
tail -f ~/.claude-code/logs/hooks.log
```

**Common issues:**
- Hook not executable: `chmod +x .claude/hooks/*.sh`
- Incorrect matcher syntax
- Hook timeout (> 2 seconds)

---

## Workflow 6: Bulk Operations

### Bulk Import Entries

```bash
# 1. Prepare YAML files in directory
mkdir -p new-entries/python/errors
# Add YAML files

# 2. Validate all
python tools/kb.py validate new-entries/

# 3. Move to correct location
mv new-entries/python/errors/* python/errors/

# 4. Initialize metadata for all
python tools/kb.py init-metadata

# 5. Rebuild index
python tools/kb.py index --force -v

# 6. Commit all
git add python/errors/
git commit -m "Add bulk Python error entries

- Multiple asyncio errors
- Testing pattern errors

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

git push origin main
```

---

### Bulk Category Changes

```bash
# 1. Find entries to change
grep -r "category: \"old-category\"" . --include="*.yaml"

# 2. Backup
cp -r python/errors/ python/errors-backup/

# 3. Replace category (use sed or IDE)
find . -name "*.yaml" -exec sed -i 's/category: "old"/category: "new"/' {} \;

# 4. Validate all
python tools/kb.py validate .

# 5. Rebuild index
python tools/kb.py index --force -v

# 6. Commit
git add .
git commit -m "Rename category: old → new"
```

---

**Version:** 3.0
**Last Updated:** 2026-01-07
