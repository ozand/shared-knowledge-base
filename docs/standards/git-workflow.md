# Git Workflow Standards

**Standard git workflow for Shared Knowledge Base repository**

---

## Commit Message Format

### Conventional Commits

**Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `Add` - Add new entry or feature
- `Update` - Update existing entry
- `Fix` - Fix bug or error in entry
- `Refactor` - Refactor structure
- `Docs` - Documentation only changes

### Example Commit Message

```
Add PYTHON-123: Async timeout in FastAPI

- Problem: Coroutine hangs indefinitely
- Solution: Add timeout handling with asyncio.wait_for()
- Tested on Python 3.11+, FastAPI 0.104+

Real-world example: Production API endpoint timeout

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## GitHub Attribution (GITHUB-ATTRIB-001)

**Required footer for all commits:**
```markdown
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Purpose:**
- Proper attribution for AI-generated contributions
- Transparency for repository users
- Compliance with open source best practices

---

## Branch Naming

### Main Branch
- `main` - Protected, no direct commits

### Feature Branches
- `add/<CATEGORY>-<id>` - Add new entry
- `update/<CATEGORY>-<id>` - Update entry
- `fix/<CATEGORY>-<id>` - Fix entry
- `refactor/<area>` - Refactor structure

**Examples:**
```
add/PYTHON-123
update/DOCKER-045
fix/async-handling
refactor/metadata-system
```

---

## Push Workflow

### Universal Scope Entries (IMMEDIATE PUSH)

**Critical:** Universal scope entries MUST be pushed immediately after creation.

```bash
# 1. Create entry
# 2. Validate
python tools/kb.py validate <file>

# 3. Initialize metadata
python tools/kb.py init-metadata

# 4. Commit
git add <file> *_meta.yaml
git commit -m "Add ERROR-ID: Title

- Description
- Real-world example

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# 5. IMMEDIATELY push
git push origin main

# 6. If conflicts:
git pull --rebase origin main
git push origin main
```

**⚠️ NEVER use `git push --force`**

---

## Pull Request Process

### When to Use PRs

- **Large refactors** - Multiple files changed
- **Controversial changes** - Need discussion
- **Breaking changes** - Affects existing structure
- **Documentation updates** - Non-critical changes

### PR Template

```markdown
## Summary
Brief description of changes

## Type
- [ ] Add entries
- [ ] Update entries
- [ ] Refactor structure
- [ ] Update documentation

## Changes
- List of files changed
- Entry IDs affected

## Testing
- [ ] All entries validated: `python tools/kb.py validate .`
- [ ] Index rebuilt: `python tools/kb.py index --force -v`
- [ ] Tested KB operations

## Checklist
- [ ] Commit messages follow convention
- [ ] GitHub attribution included
- [ ] No force push used
- [ ] Conflicts resolved with rebase
```

---

## Conflict Resolution

### Pull with Rebase (PREFERRED)

```bash
git pull --rebase origin main
```

**Advantages:**
- Linear history
- Cleaner commits
- Easier to understand

### If Rebase Conflicts

```bash
# 1. Start rebase
git pull --rebase origin main

# 2. If conflicts:
# Edit conflicting files
# Resolve conflicts
git add <resolved-files>

# 3. Continue rebase
git rebase --continue

# 4. Push
git push origin main
```

**⚠️ NEVER use:**
```bash
git push --force  # FORBIDDEN!
git merge origin/main  # Creates merge commits
```

---

## Submodule Workflow

### Update Submodule

```bash
# In parent project
cd path/to/project
git submodule update --remote docs/knowledge-base/shared

# Commit submodule update
git add docs/knowledge-base/shared
git commit -m "Update shared-knowledge-base to latest"
git push origin main
```

### Contribute to Submodule

```bash
# Navigate to submodule
cd docs/knowledge-base/shared

# Make changes
# Validate
python tools/kb.py validate .

# Commit and push to shared repo
git add .
git commit -m "Add ERROR-ID: Title"
git push origin main

# In parent project, update submodule reference
cd ../../..
git add docs/knowledge-base/shared
git commit -m "Update shared-knowledge-base with new entry"
```

---

## Workflow Rules

### ✅ DO
- Use conventional commit format
- Include GitHub attribution
- Push universal scope entries immediately
- Use rebase for conflict resolution
- Create PRs for large changes
- Validate before committing

### ❌ DON'T
- Use `git push --force`
- Use `git merge` for conflicts
- Commit without validation
- Delay pushing universal entries
- Create vague commit messages
- Forget GitHub attribution

---

## Related

- `@references/workflows.md` - Complete workflow documentation
- `@standards/yaml-standards.md` - YAML entry standards
- `@standards/quality-gates.md` - Quality requirements

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Pattern:** GITHUB-ATTRIB-001
