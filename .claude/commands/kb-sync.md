# KB Sync

Synchronize local knowledge base changes with the shared repository.

## Usage
```
/kb-sync [file-or-directory]
```

## Quick Examples

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

## What This Command Does

1. **Validates** entries using `python tools/kb.py validate`
2. **Checks scope** - only syncs universal scopes (docker, universal, python, postgresql, javascript)
3. **Initializes metadata** if needed
4. **Commits** with proper format (including GitHub attribution)
5. **Pushes** to shared repository immediately
6. **Rebuilds index** after sync

**⚠️ Important:** Only syncs entries with **universal scope**. Project-specific entries (project, domain, framework) stay local.

## Scope Decision

**Sync to shared repository if:**
- Scope is: `docker`, `universal`, `python`, `postgresql`, `javascript`
- Solution applies to multiple projects
- Industry-standard pattern

**Keep local if:**
- Scope is: `project`, `domain`, `framework`
- Environment-specific
- Business logic specific

**📘 Detailed Workflows:** `@references/workflows.md` - Complete synchronization workflows

## Workflow Steps

### Step 1: Validate
```bash
python tools/kb.py validate <file>
```

### Step 2: Check Scope
Verify entry has universal scope before syncing.

### Step 3: Initialize Metadata
```bash
python tools/kb.py init-metadata
```

### Step 4: Commit
```bash
git add <file> *_meta.yaml
git commit -m "Add ERROR-ID: Title

- Brief description
- Real-world example

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

### Step 5: Push
```bash
git push origin main
```

### Step 6: Handle Conflicts
If push fails:
```bash
git pull --rebase origin main
git push origin main
```

### Step 7: Rebuild Index
```bash
python tools/kb.py index --force -v
```

## Output

**Success:**
```
✅ Entry synced to shared repository
📦 Committed: abc123def
🚀 Pushed to: origin/main
🔍 Index rebuilt
🌐 Available at: https://github.com/ozand/shared-knowledge-base
```

**Error (wrong scope):**
```
⚠️  Entry has project-specific scope
📝 Not syncing to shared repository
💡 Keep in local KB only
```

## Related

- `@skills/kb-create/SKILL.md` - Create new entries
- `@references/workflows.md` - Detailed sync workflows
- `@references/cli-reference.md` - Complete CLI reference
