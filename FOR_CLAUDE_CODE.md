# For Claude Code: Setting Up Shared Knowledge Base in New Projects

**Instructions for Claude Code agents on how to deploy shared-knowledge-base**

---

## Quick Reference for Claude Code

When user asks to "set up shared knowledge base" or mentions knowledge base in a new project:

### Step 1: Check if Already Configured

```bash
# Check for existing KB setup
ls -la docs/knowledge-base/.kb-config.yaml
ls -la docs/knowledge-base/tools/kb.py
git submodule status | grep shared-knowledge-base
```

### Step 2: Add as Git Submodule (Recommended)

```bash
# Add shared-knowledge-base as submodule
cd /path/to/project
git submodule add https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base/shared

# Commit the change
git commit -m "Add shared-knowledge-base as git submodule"
```

### Step 3: Copy Configuration Files

```bash
# Copy kb.py tool to project (if not using submodule directly)
cp docs/knowledge-base/shared/tools/kb.py docs/knowledge-base/tools/kb.py

# Copy or create .kb-config.yaml
cp docs/knowledge-base/shared/.kb-config.yaml docs/knowledge-base/.kb-config.yaml
```

### Step 4: Update .kb-config.yaml for Project

```yaml
version: "2.0"
paths:
  kb_dir: "docs/knowledge-base"
  cache_dir: "docs/knowledge-base/.cache"
  index_db: "docs/knowledge-base/.cache/kb_index.db"

shared_sources:
  - name: "Universal Shared KB"
    url: "https://github.com/ozand/shared-knowledge-base.git"
    scopes: ["universal", "python"]
    enabled: true

import_scopes:
  - universal
  - python
```

### Step 5: Build Search Index

```bash
# Build index for fast search
python docs/knowledge-base/tools/kb.py index -v
```

### Step 6: Test Search

```bash
# Test that search works
python docs/knowledge-base/tools/kb.py search "websocket"
python docs/knowledge-base/tools/kb.py stats
```

---

## 🚨 Agent Behavior Rules - CRITICAL

### MANDATORY WORKFLOW FOR UNIVERSAL ERRORS

**When adding KB entries with these scopes:**
- **docker**
- **universal**
- **python**
- **postgresql**
- **javascript**

**YOU MUST:**

#### 1. Create file in SHARED KB (NOT local!)

```bash
# ✅ CORRECT: Create here
/home/ozand/docs/knowledge-base/shared/<scope>/errors/<filename>.yaml

# ❌ WRONG: NOT here
/home/ozand/docs/knowledge-base/<scope>/errors/<filename>.yaml
```

#### 2. Validate YAML

```bash
python3 /home/ozand/docs/knowledge-base/tools/kb.py validate /home/ozand/docs/knowledge-base/shared/
```

#### 3. IMMEDIATELY commit and push

```bash
cd /home/ozand/docs/knowledge-base/shared
git add <file>
git commit -m "Add ERROR-ID: Error Title

- Brief description
- Related issues
- Real-world example

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Push to remote
git push origin main

# If push fails with conflicts:
git pull --rebase origin main
git push origin main
```

#### 4. Rebuild index

```bash
cd /home/ozand
python3 docs/knowledge-base/tools/kb.py index --force -v
```

#### 5. Confirm to user

```
✅ KB entry added to shared-knowledge-base repository
📦 Committed: <commit-hash>
🚀 Pushed to: origin/main
🔍 Index rebuilt
🌐 Available at: https://github.com/ozand/shared-knowledge-base
```

**🚨 NEVER skip synchronization for universal errors!**

This creates knowledge silos and prevents other projects from benefiting.

**What happens if you skip sync:**
- ❌ Knowledge trapped in local repository
- ❌ Other projects can't benefit
- ❌ Duplicate work across projects
- ❌ Knowledge becomes stale

---

## Quick Decision Tree

```
User reports error
    ↓
Search KB: python3 docs/knowledge-base/tools/kb.py search "error"
    ↓
Found? ──Yes──→ Return solution ✅
    ↓
   No
    ↓
Solve problem + Document in YAML
    ↓
Determine scope:
    ├─ docker, universal, python, postgresql, javascript?
    │   ↓
    │   Create in /docs/knowledge-base/shared/<scope>/
    │   ↓
    │   Validate YAML
    │   ↓
    │   cd /home/ozand/docs/knowledge-base/shared
    │   git add <file>
    │   git commit -m "Add ERROR-ID: Title"
    │   git push origin main
    │   ↓ (if conflict)
    │   git pull --rebase origin main
    │   git push origin main
    │   ↓
    │   Rebuild index
    │   ↓
    │   Confirm: "✅ Synced to shared-knowledge-base"
    │   └→ Done ✅
    │
    └─ project, domain, framework?
        ↓
        Create in /docs/knowledge-base/<scope>/
        ↓
        Add metadata: local_only: true
        ↓
        Validate YAML
        ↓
        Rebuild index
        ↓
        Confirm: "✅ Added to local KB (project-specific)"
        └→ Done ✅
```

**Key Rules:**
- 🚨 Universal scopes → ALWAYS sync to shared immediately
- 🏠 Project-specific → Keep local, mark as `local_only: true`
- ✅ Index rebuild ALWAYS required after changes
- 📝 User confirmation ALWAYS required
- ⚠️ Handle merge conflicts with `git pull --rebase`

---

## Criteria: Universal vs Local KB

### Add to SHARED KB if:

**✅ Error scope is:**
- `docker` - Docker/container issues
- `universal` - System-level, filesystem, networking
- `python` - Python language errors
- `postgresql` - PostgreSQL database errors
- `javascript` - JavaScript/Node.js errors

**✅ Solution applies to:**
- Multiple projects
- Different environments
- Various configurations
- Standard use cases

**✅ Error is:**
- Common across industry
- Not infrastructure-specific
- Framework-agnostic
- Reusable knowledge

**Examples of Shared KB entries:**
- DOCKER-001: Port Already in Use (universal Docker issue)
- PYTHON-001: ImportError Module Not Found (universal Python issue)
- UNIVERSAL-001: Broken Symlink Detection (filesystem issue)
- POSTGRES-001: Connection Refused (PostgreSQL issue)

### Keep in LOCAL KB if:

**❌ Error scope is:**
- `project` - Single project issues
- `domain` - Business logic specific
- `framework` - Specific framework version quirks

**❌ Solution depends on:**
- Specific infrastructure setup
- External systems (APIs, services)
- Organization-specific configuration
- Non-standard environment

**❌ Error is:**
- One-time occurrence
- Environment-specific
- Not reusable
- Temporary workaround

**Examples of Local KB entries:**
- PROJECT-001: Production database timeout (specific infrastructure)
- DOMAIN-001: Payment gateway integration (business logic)
- FRAMEWORK-001: Custom FastAPI middleware (project-specific)

---

## Detailed Setup Guide

### Method 1: Git Submodule (Recommended)

**Advantages:**
- Easy updates via `git submodule update --remote`
- Clear separation between shared and project-specific KB
- Tracks which version of shared KB is used

**Steps:**

```bash
# 1. Add submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base/shared

# 2. Copy tool to project root (for easier access)
cp docs/knowledge-base/shared/tools/kb.py docs/knowledge-base/tools/kb.py

# 3. Create .kb-config.yaml
cat > docs/knowledge-base/.kb-config.yaml << 'EOF'
version: "2.0"
paths:
  kb_dir: "docs/knowledge-base"
  cache_dir: "docs/knowledge-base/.cache"
  index_db: "docs/knowledge-base/.cache/kb_index.db"

shared_sources:
  - name: "Universal Shared KB"
    url: "https://github.com/ozand/shared-knowledge-base.git"
    scopes: ["universal", "python"]
    enabled: true

import_scopes:
  - universal
  - python
  - framework
  - domain
  - project
EOF

# 4. Build index
python docs/knowledge-base/tools/kb.py index -v

# 5. Test
python docs/knowledge-base/tools/kb.py search "import"
```

**Updating shared KB:**

```bash
# Update to latest version from GitHub
git submodule update --remote docs/knowledge-base/shared

# Rebuild index
python docs/knowledge-base/tools/kb.py index -v
```

### Method 2: Direct Clone (Simple)

**Advantages:**
- Simpler setup
- Full control over shared KB files
- Can edit and contribute back easily

**Steps:**

```bash
# 1. Clone to shared directory
git clone https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base/shared

# 2. Copy tool and config
cp docs/knowledge-base/shared/tools/kb.py docs/knowledge-base/tools/kb.py
cp docs/knowledge-base/shared/.kb-config.yaml docs/knowledge-base/.kb-config.yaml

# 3. Build index
python docs/knowledge-base/tools/kb.py index -v

# 4. Add to .gitignore
echo "docs/knowledge-base/shared/" >> .gitignore
```

### Method 3: Copy Specific Content (Minimal)

**Advantages:**
- Only copy what you need
- No git overhead
- Project-specific customization

**Steps:**

```bash
# 1. Create directory structure
mkdir -p docs/knowledge-base/errors
mkdir -p docs/knowledge-base/patterns
mkdir -p docs/knowledge-base/tools
mkdir -p docs/knowledge-base/.cache

# 2. Clone shared KB temporarily to extract content
git clone https://github.com/ozand/shared-knowledge-base.git /tmp/shared-kb-temp

# 3. Copy relevant content
cp /tmp/shared-kb-temp/python/errors/*.yaml docs/knowledge-base/errors/
cp /tmp/shared-kb-temp/universal/patterns/*.yaml docs/knowledge-base/patterns/
cp /tmp/shared-kb-temp/tools/kb.py docs/knowledge-base/tools/kb.py

# 4. Create .kb-config.yaml
cat > docs/knowledge-base/.kb-config.yaml << 'EOF'
version: "2.0"
paths:
  kb_dir: "docs/knowledge-base"
  cache_dir: "docs/knowledge-base/.cache"
  index_db: "docs/knowledge-base/.cache/kb_index.db"

import_scopes:
  - universal
  - python
EOF

# 5. Build index
python docs/knowledge-base/tools/kb.py index -v

# 6. Clean up
rm -rf /tmp/shared-kb-temp
```

---

## .gitignore Configuration

Ensure these entries are in `.gitignore`:

```gitignore
# Knowledge Base cache (auto-generated by kb.py)
docs/knowledge-base/.cache/
docs/knowledge-base/.cache/**/*
docs/knowledge-base/shared/

# JSON exports for AI tools
.kb-export.json
.kb-snapshot.json

# But allow these
!docs/knowledge-base/.kb-config.yaml
!docs/knowledge-base/tools/kb.py
!docs/knowledge-base/errors/
!docs/knowledge-base/patterns/
```

---

## Updating CLAUDE.md

Add to project's `CLAUDE.md`:

```markdown
## Knowledge Base

This project uses a shared knowledge base for common errors, solutions, and best practices.

**Quick search:**
```bash
python docs/knowledge-base/tools/kb.py search "keyword"
```

**Build index:**
```bash
python docs/knowledge-base/tools/kb.py index -v
```

**Statistics:**
```bash
python docs/knowledge-base/tools/kb.py stats
```

**Knowledge base includes:**
- Universal Python errors (import, testing, type-checking)
- Framework-specific patterns (Clean Architecture, WebSocket)
- Best practices and troubleshooting guides

For more details, see: [docs/knowledge-base/README.md](docs/knowledge-base/README.md)
```

---

## Common Workflows for Claude Code

### When User Reports an Error - INTEGRATED WORKFLOW

**Step 1: Search knowledge base first:**
```bash
python docs/knowledge-base/tools/kb.py search "error message"
```

**Step 2: If error is not in KB:**
- Solve the problem
- Determine scope (docker, universal, python, postgresql, javascript, project, etc.)
- Document the solution in appropriate YAML file
- Run validation: `python docs/knowledge-base/tools/kb.py validate`

**Step 3: Determine KB location and sync:**

**IF scope is universal (docker, universal, python, postgresql, javascript):**
- ✅ Create file in: `/docs/knowledge-base/shared/<scope>/errors/`
- ✅ Validate YAML
- ✅ IMMEDIATELY commit to shared repository:
  ```bash
  cd /home/ozand/docs/knowledge-base/shared
  git add <file>
  git commit -m "Add ERROR-ID: Title

  - Brief description
  - Real-world example

  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
  git push origin main

  # If push fails:
  git pull --rebase origin main
  git push origin main
  ```
- ✅ Rebuild index: `python docs/knowledge-base/tools/kb.py index --force -v`
- ✅ Confirm to user: "✅ Synced to shared-knowledge-base repository"

**IF scope is project-specific (project, domain, framework):**
- ✅ Create file in: `/docs/knowledge-base/<scope>/errors/`
- ✅ Mark metadata with `local_only: true`
- ✅ Validate YAML
- ✅ Rebuild index
- ✅ Inform user: "✅ Added to local KB (project-specific, not shared)"

**Step 4: Always rebuild index after changes:**
```bash
python docs/knowledge-base/tools/kb.py index --force -v
```

**MANDATORY CHECKLIST:**
- [ ] File created in correct location (shared vs local)
- [ ] YAML validated
- [ ] No duplicates found
- [ ] **If universal: Committed to shared repo**
- [ ] **If universal: Pushed to origin/main**
- [ ] **If universal: Conflicts resolved (if any)**
- [ ] Index rebuilt
- [ ] User notified

### When Starting New Task

1. **Search for related patterns:**
   ```bash
   python docs/knowledge-base/tools/kb.py search "task keyword"
   ```

2. **Review best practices:**
   ```bash
   python docs/knowledge-base/tools/kb.py search --scope pattern "best practice"
   ```

3. **Check for common pitfalls:**
   ```bash
   python docs/knowledge-base/tools/kb.py search --severity high,critical
   ```

### When User Asks for Best Practices

1. **Search for specific topic:**
   ```bash
   python docs/knowledge-base/tools/kb.py search "async testing"
   ```

2. **List all patterns:**
   ```bash
   python docs/knowledge-base/tools/kb.py search --scope pattern
   ```

3. **Show statistics:**
   ```bash
   python docs/knowledge-base/tools/kb.py stats
   ```

---

## Contributing to Shared KB

When you document an error that's universally applicable:

1. **Check shared KB structure:**
   ```bash
   ls docs/knowledge-base/shared/python/errors/
   ```

2. **Add to appropriate file in shared KB:**
   ```bash
   # Edit shared KB file
   nano docs/knowledge-base/shared/python/errors/testing.yaml

   # Or if not using submodule, clone and edit:
   git clone https://github.com/ozand/shared-knowledge-base.git /tmp/shared-kb
   nano /tmp/shared-kb/python/errors/testing.yaml
   ```

3. **Validate:**
   ```bash
   python docs/knowledge-base/tools/kb.py validate docs/knowledge-base/shared/
   ```

4. **Commit and push to shared KB:**
   ```bash
   cd docs/knowledge-base/shared
   git add python/errors/testing.yaml
   git commit -m "Add PY-TEST-XXX: New Error Title"
   git push origin main
   ```

5. **Update project submodule:**
   ```bash
   cd /path/to/project
   git submodule update --remote docs/knowledge-base/shared
   ```

---

## Troubleshooting

### kb.py Command Not Found

```bash
# Use full path
python docs/knowledge-base/tools/kb.py search "keyword"

# Or create alias
echo 'alias kb="python docs/knowledge-base/tools/kb.py"' >> ~/.bashrc
source ~/.bashrc
kb search "keyword"
```

### Index Out of Date

```bash
# Rebuild index
python docs/knowledge-base/tools/kb.py index --force -v
```

### Submodule Not Updating

```bash
# Check submodule status
git submodule status

# Update submodule
git submodule update --remote docs/knowledge-base/shared

# If needed, init submodule first
git submodule init
git submodule update
```

### Python Dependencies Missing

```bash
# Install PyYAML
pip install pyyaml

# Or with uv
uv add pyyaml --optional dev
```

---

## Verification Checklist

After setup, verify:

- [ ] `docs/knowledge-base/tools/kb.py` exists
- [ ] `docs/knowledge-base/.kb-config.yaml` exists
- [ ] `docs/knowledge-base/.cache/kb_index.db` exists (after running index)
- [ ] `kb.py search` returns results
- [ ] `kb.py stats` shows statistics
- [ ] Git submodule status shows shared-knowledge-base (if using submodule)
- [ ] `.gitignore` includes cache directory
- [ ] `CLAUDE.md` mentions knowledge base
- [ ] User can successfully search for errors

---

## Quick Command Reference

```bash
# Build index
python docs/knowledge-base/tools/kb.py index -v

# Search
python docs/knowledge-base/tools/kb.py search "keyword"
python docs/knowledge-base/tools/kb.py search --id ERROR-ID
python docs/knowledge-base/tools/kb.py search --tag async --scope python

# Statistics
python docs/knowledge-base/tools/kb.py stats

# Validate
python docs/knowledge-base/tools/kb.py validate

# Export for AI tools
python docs/knowledge-base/tools/kb.py export --format json

# Update shared KB (if using submodule)
git submodule update --remote docs/knowledge-base/shared
```

---

## Summary for Claude Code

**When user says "set up knowledge base":**

1. Check if already configured
2. Add git submodule: `git submodule add https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base/shared`
3. Copy `kb.py` and `.kb-config.yaml`
4. Build index: `python docs/knowledge-base/tools/kb.py index -v`
5. Test search: `python docs/knowledge-base/tools/kb.py search "test"`
6. Update `.gitignore`
7. Update `CLAUDE.md`

**Estimated time:** 3-5 minutes

**Files created/modified:**
- `.gitmodules` (new)
- `docs/knowledge-base/shared/` (new, submodule)
- `docs/knowledge-base/tools/kb.py` (copied)
- `docs/knowledge-base/.kb-config.yaml` (copied/created)
- `docs/knowledge-base/.cache/kb_index.db` (auto-generated)
- `.gitignore` (modified)
- `CLAUDE.md` (modified)

---

## Session Completion Checklist

**KB Entry Creation:**
- [ ] YAML file created
- [ ] YAML syntax validated (`python3 kb.py validate`)
- [ ] No duplicates found (searched by ID, title, tags)
- [ ] Related entries linked
- [ ] Real-world example included

**Synchronization (if universal scope):**
- [ ] File created in `/docs/knowledge-base/shared/<scope>/` (NOT local!)
- [ ] `git add <file>` executed
- [ ] `git commit` executed with proper message format
- [ ] `git push origin main` executed successfully
- [ ] Conflicts resolved with `git pull --rebase` (if any)
- [ ] Changes visible in GitHub repository

**Index & Verification:**
- [ ] KB index rebuilt (`python3 kb.py index --force -v`)
- [ ] Search returns new entry
- [ ] Stats updated (`python3 kb.py stats`)
- [ ] User notified of sync status

**Documentation:**
- [ ] Session report created (if multi-step session)
- [ ] Related files updated (README.md, CLAUDE.md, etc.)
- [ ] Commit message follows format

**Final Confirmation Template:**
```
✅ KB entry: ERROR-ID created
📦 Location: shared/<scope>/errors/
🚀 Synced: origin/main (commit: <hash>)
🔍 Index: rebuilt
📊 Stats: updated
🌐 Available: https://github.com/ozand/shared-knowledge-base
```

---

## Example Workflows

### ✅ GOOD: Universal Error Workflow

**User:** "Container shows unhealthy"

**Claude:**
1. ✅ Search KB: `python3 kb.py search "unhealthy"`
2. ✅ Not found → Investigate issue
3. ✅ Find root cause: curl not installed in minimal Python image
4. ✅ Determine scope: "docker" (universal)
5. ✅ Create file in: `/docs/knowledge-base/shared/docker/errors/best-practices.yaml`
6. ✅ Add DOCKER-024 entry with:
   - Problem description
   - Wrong/correct code examples
   - Solution steps
   - Real-world example
7. ✅ Validate: `python3 kb.py validate shared/`
8. ✅ **IMMEDIATELY sync to repository:**
   ```bash
   cd /home/ozand/docs/knowledge-base/shared
   git add docker/errors/best-practices.yaml
   git commit -m "Add DOCKER-024: Healthcheck Command Not Available

   - Minimal images don't include curl
   - Use language built-ins instead
   - Real example: notebooklm-mindmap fix

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
   git push origin main
   ```
9. ✅ Rebuild index: `python3 kb.py index --force -v`
10. ✅ Confirm: "✅ Synced to shared-knowledge-base repository"

**Result:**
- Knowledge immediately available to all projects ✅
- No manual sync required later ✅
- Prevents duplicate work ✅
- Follows best practices ✅

---

### ❌ BAD: What NOT to Do

**User:** "Container shows unhealthy"

**Claude (WRONG):**
1. ✅ Search KB: `python3 kb.py search "unhealthy"`
2. ✅ Not found → Investigate
3. ✅ Find root cause
4. ✅ Determine scope: "docker" (universal)
5. ❌ **Create file in WRONG location:** `/docs/knowledge-base/docker/errors/`
6. ✅ Add DOCKER-024 entry
7. ✅ Validate
8. ❌ **Skip sync** - tell user "Added to KB"
9. ❌ User thinks it's shared
10. ❌ **Actually only local** - not in repository

**Problems:**
- ❌ Knowledge silo (only local)
- ❌ Not reusable across projects
- ❌ Against documentation guidelines
- ❌ Violates agent behavior rules
- ❌ Requires manual sync later (often forgotten)
- ❌ Other projects can't benefit
- ❌ Creates duplicate work

**What should happen instead:**
- ✅ Create in `/docs/knowledge-base/shared/docker/errors/`
- ✅ Immediately git add + git commit + git push
- ✅ Confirm sync status to user

---

### ✅ GOOD: Local-Only Error Workflow

**User:** "Production database timeout in project X"

**Claude:**
1. ✅ Search KB: `python3 kb.py search "database timeout"`
2. ✅ Not found → Investigate
3. ✅ Find issue: Specific infrastructure configuration
4. ✅ Determine scope: "project" (infrastructure-specific)
5. ✅ Create file in: `/docs/knowledge-base/project/errors/database-timeouts.yaml`
6. ✅ Add PROJECT-001 entry with metadata:
   ```yaml
   metadata:
     local_only: true
     reason: "Production-specific infrastructure configuration"
     environment: "production"
     applies_to: "project-x only"
   ```
7. ✅ Validate
8. ✅ Rebuild index
9. ✅ Confirm: "✅ Added to local KB (project-specific, not shared)"

**Result:**
- Correctly kept local (not universal) ✅
- Properly marked as local-only ✅
- Won't pollute shared KB ✅
- Clear documentation of why it's local ✅

---

### ✅ GOOD: Handling Merge Conflicts

**Scenario:** Another agent pushed changes while you were working

**Claude:**
1. ✅ Create file in shared KB
2. ✅ Add and commit locally
3. ❌ Push fails: "Updates were rejected"
4. ✅ **Handle conflict properly:**
   ```bash
   git pull --rebase origin main
   # Resolve conflicts if needed
   git push origin main
   ```
5. ✅ Rebuild index
6. ✅ Confirm: "✅ Synced after resolving merge conflicts"

**Result:**
- Conflicts resolved correctly ✅
- No force push needed ✅
- Preserves all changes ✅

---

### ❌ BAD: Mishandling Conflicts

**Claude (WRONG):**
1. ✅ Create file and commit
2. ❌ Push fails
3. ❌ **Force push:** `git push --force`
4. ❌ **Overwrites other agent's work**

**Problems:**
- ❌ Loses other agent's changes
- ❌ Creates repository corruption
- ❌ Bad collaboration practice

**Correct approach:**
- ✅ Always use `git pull --rebase`
- ✅ Resolve conflicts manually
- ✅ Never force push to main branch

---

## Quick Reference for Agent Behavior

**When adding KB entry, ALWAYS:**

1. **Check scope first**
   - Universal? → shared/
   - Project-specific? → local/

2. **Follow the path:**
   - Universal: `/docs/knowledge-base/shared/<scope>/errors/`
   - Local: `/docs/knowledge-base/<scope>/errors/`

3. **Sync immediately if universal:**
   - git add
   - git commit
   - git push (with conflict handling)
   - Rebuild index
   - Confirm to user

4. **Never skip steps:**
   - Don't say "will sync later"
   - Don't create universal errors locally
   - Don't forget to rebuild index
   - Don't forget to confirm to user

**Remember:**
- 🚨 Universal scopes = immediate sync required
- 🏠 Project scopes = keep local, mark as local_only
- ✅ Index rebuild = always required
- 📝 User confirmation = always required

---

**Last Updated:** 2026-01-05
**Maintained By:** Development Team & Claude Code
**Questions?** See: [docs/knowledge-base/HYBRID_APPROACH.md](HYBRID_APPROACH.md)
