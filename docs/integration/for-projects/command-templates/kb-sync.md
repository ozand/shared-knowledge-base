# KB Sync

Synchronize local knowledge base changes with the shared repository.

## Usage
```
/kb-sync [file-or-directory]
```

## Examples

### Sync Specific File
```
/kb-sync python/errors/new-error.yaml
```
Validates, commits, and pushes to shared repository.

### Sync Directory
```
/kb-sync universal/errors/
```
Syncs all entries in directory.

### Sync All Changes
```
/kb-sync
```
Syncs all modified entries to shared repository.

## What happens

### For Shared KB Entries (universal, python, docker, etc.)

#### Step 1: Validate
```bash
python tools/kb.py validate <file>
python tools/validate-kb.py --path <file>
```
Ensures YAML syntax and quality score ≥75/100.

#### Step 2: Initialize Metadata
```bash
python tools/kb.py init-metadata <file>
```
Creates _meta.yaml with quality score and metadata.

#### Step 3: Rebuild Index
```bash
python tools/kb.py index
```
Updates search index with new entry.

#### Step 4: Commit
```bash
git add <file> *_meta.yaml
git commit -m "Add ERROR-ID: Title

- Brief description
- Related entries
- Real-world context

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

#### Step 5: Push
```bash
git push origin main
```

If push fails with conflicts:
```bash
git pull --rebase origin main
git push origin main
```

#### Step 6: Confirm
```
✅ KB entry added to shared-knowledge-base repository
📦 Committed: <commit-hash>
🚀 Pushed to: origin/main
🔍 Index rebuilt
🌐 Available at: https://github.com/ozand/shared-knowledge-base
```

### For Project KB Entries (project, domain, framework scope)

#### Step 1: Add Local Flag
Add to YAML:
```yaml
errors:
  - id: "PROJECT-001"
    local_only: true  # Marks as project-specific
    # ... rest of entry
```

#### Step 2: Validate
```bash
python tools/kb.py validate <file>
```

#### Step 3: Rebuild Index
```bash
python tools/kb.py index
```

#### Step 4: Commit to Project (NOT shared repo)
```bash
git add <file>
git commit -m "Add project KB entry: PROJECT-001"
```

**DO NOT push to shared-knowledge-base repository**

## Options

- `--dry-run` - Show what would be synced without actually doing it
- `--force` - Force push even if conflicts (use with caution)
- `--message "<msg>"` - Custom commit message

## Output Format

### Successful Sync (Shared KB)
```
🔄 KB SYNC: python/errors/async-timeout.yaml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Validation
✅ YAML syntax valid
✅ Quality score: 82/100 (≥75 required)

Step 2: Metadata
✅ Initialized: python/errors/async-timeout_meta.yaml

Step 3: Index
✅ Index rebuilt: 110 entries (was 109)

Step 4: Commit
✅ Committed: a1b2c3d4 - Add PYTHON-045: Async timeout handling

Step 5: Push
✅ Pushed to: origin/main

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ SUCCESS - Entry now available in Shared KB
🌐 https://github.com/ozand/shared-knowledge-base

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Successful Sync (Project KB)
```
🔄 KB SYNC: project/auth-flow.yaml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Validation
✅ YAML syntax valid
✅ Quality score: 78/100 (≥75 required)

Step 2: Scope Check
⚠️  Project-specific scope (marked local_only: true)
→ Will NOT push to shared repository

Step 3: Index
✅ Index rebuilt: 111 entries

Step 4: Commit
✅ Committed to project repository

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ SUCCESS - Entry added to Project KB only

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Scope Decision Guide

### Add to SHARED KB if:
✅ Scope is: universal, python, javascript, docker, postgresql
✅ Solution applies to multiple projects/environments
✅ Error is common across industry
✅ Framework-agnostic or standard use case
✅ Best practice worth sharing

### Keep in PROJECT KB if:
✅ Scope is: project, domain, framework
✅ Solution depends on specific infrastructure
✅ Environment-specific configuration
✅ Business logic specific
✅ One-time occurrence

## Common Workflows

### After Solving Universal Error
```bash
# 1. Create YAML entry
vim python/errors/async-error.yaml

# 2. Validate
/kb-validate python/errors/async-error.yaml

# 3. Sync to shared KB
/kb-sync python/errors/async-error.yaml

# Output: Validates, commits, pushes, confirms
```

### After Solving Project Issue
```bash
# 1. Create YAML entry with local_only: true
vim project/auth-error.yaml

# 2. Validate
/kb-validate project/auth-error.yaml

# 3. Sync to project KB
/kb-sync project/auth-error.yaml

# Output: Validates, commits to project repo
```

### After Multiple Changes
```bash
# Sync all shared KB changes
/kb-sync universal/
/kb-sync python/
/kb-sync docker/

# Sync all project KB changes
/kb-sync project/
```

## Related Commands
- `/kb-validate` - Validate before syncing
- `/kb-search` - Check for duplicates before creating
- `/retrospective` - Analyze session for KB-worthy content
- `/kb-index` - Rebuild index after syncing

## Troubleshooting

### Issue: "Validation failed"
**Fix:**
```bash
# Check quality score
python tools/validate-kb.py --path <file>

# Fix issues:
# - Missing required fields
# - YAML syntax errors
# - Score <75

# Re-validate
/kb-validate <file>
```

### Issue: "Push rejected - conflicts"
**Fix:**
```bash
# Pull with rebase
git pull --rebase origin main

# Resolve conflicts if any
# Test that kb.py still works

# Push again
git push origin main
```

### Issue: "Wrong scope"
**Fix:**
```bash
# If pushed to shared KB but should be project:
# 1. Add local_only: true to YAML
# 2. Remove from shared repo (contact curator)
# 3. Add to project KB instead

# If in project KB but should be shared:
# 1. Remove local_only: true
# 2. /kb-sync to shared repo
```

## Best Practices

### Before Syncing
1. ✅ Always validate first (`/kb-validate`)
2. ✅ Check for duplicates (`/kb-search`)
3. ✅ Ensure quality score ≥75/100
4. � Determine correct scope

### During Sync
1. ✅ Let command handle all steps automatically
2. ✅ Review commit message before pushing
3. ✅ Confirm successful push

### After Syncing
1. ✅ Verify entry appears in index (`/kb-search`)
2. ✅ Test that other projects can access it
3. ✅ Document if related to existing entries

### For Teams
- ✅ Establish scope decision guidelines
- ✅ Review shared KB additions weekly
- ✅ Communicate new entries to team
- ✅ Project KB stays local, shared KB gets pushed

## Advanced Features

### Batch Sync
```bash
# Sync multiple scopes at once
for scope in universal python docker; do
  /kb-sync $scope/
done
```

### Sync with Custom Message
```bash
/kb-sync python/errors/new-error.yaml --message "Fix PYTHON-123: Added async timeout solution"
```

### Dry Run Mode
```bash
/kb-sync python/errors/new-error.yaml --dry-run

# Shows what would happen without doing it
# Useful for verification
```

## Integration with CI/CD

### Pre-commit Hook
Automatically validates KB entries before commit:
```bash
# .git/hooks/pre-commit
for file in $(git diff --cached --name-only | grep '\.yaml$'); do
  python tools/kb.py validate "$file" || exit 1
done
```

### Post-commit Hook
Automatically syncs to shared KB for specific scopes:
```bash
# .git/hooks/post-commit
for file in $(git diff --name-only HEAD~1 HEAD | grep 'universal/\|python/\|docker/\|postgresql/\|javascript/'); do
  if [ -f "$file" ]; then
    git add "${file%.*}_meta.yaml" 2>/dev/null
  fi
done
```

## See Also
- Skill: `kb-create` - Create new entries
- Skill: `kb-validate` - Validate quality
- Command: `/retrospective` - Find KB-worthy content
- Guide: `@for-claude-code/README.md` - Project integration

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Command Type:** Workflow Automation
**Integration:** git, GitHub API
