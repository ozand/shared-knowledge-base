# Migration Guide: v5.1 → v5.1

**Version:** 5.1.0
**Last Updated:** 2026-01-08
**Status:** ✅ Ready for Migration

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Pre-Migration Checklist](#pre-migration-checklist)
3. [Migration Methods](#migration-methods)
4. [Step-by-Step Migration](#step-by-step-migration)
5. [Post-Migration Verification](#post-migration-verification)
6. [Troubleshooting](#troubleshooting)
7. [Rollback Instructions](#rollback-instructions)

---

## Overview

### What's Changing?

v5.1 introduces a **two-tier knowledge management system**:

| Feature | v5.1 | v5.1 |
|---------|------|------|
| **KB Structure** | Single Shared KB | Project KB + Shared KB |
| **Submission** | Direct commit (dangerous) | GitHub Issues (safe) |
| **Context Loading** | Manual | Automatic via hook |
| **Decision Making** | Agent guesses | Explicit criteria |
| **Tools** | tools/*.py | tools/*.py (v5.1 still works) |

### Why Migrate?

- ✅ **Safer** - No more direct commits to Shared KB
- ✅ **Smarter** - Agents know what to share automatically
- ✅ **Faster** - Automatic context loading on session start
- ✅ **Better** - Quality scoring ensures high standards

### Backward Compatibility

**IMPORTANT:** v5.1 tools **still work**. Migration is **optional**, not forced.

You can:
- ✅ Keep using v5.1 tools
- ✅ Migrate gradually
- ✅ Use both v5.1 and v5.1 side-by-side

---

## Pre-Migration Checklist

### 1. Check Your Current Setup

```bash
# Check if you have .kb directory
ls -la .kb/

# Check Shared KB submodule
git submodule status

# Check current tools
ls -la .kb/shared/tools/

# Check for existing context
find . -name "PROJECT.yaml" -o -name "MEMORY.md"
```

### 2. Backup Your Work

```bash
# Backup .kb directory (if exists)
cp -r .kb .kb.backup.$(date +%Y%m%d)

# Backup project config
cp .claude/settings.json .claude/settings.json.backup

# Note down any custom configurations
```

### 3. Verify Requirements

```bash
# Check Python version (need 3.11+)
python --version

# Check Git version
git --version

# Check if PyGithub is installed
python -c "import github; print('PyGithub installed')"

# Install PyGithub if needed
pip install PyGithub
```

### 4. Gather Information

You'll need:
- [ ] GitHub personal access token (for submissions)
- [ ] Project name and ID
- [ ] Technology stack details
- [ ] Integration information (Stripe, SendGrid, etc.)

---

## Migration Methods

### Method 1: Automated Script (Recommended)

**Best for:** Most users, fast migration

```bash
# Run migration script
cd /path/to/your/project
python .kb/shared/tools/migrate-to-v5.1.sh

# Follow prompts
# Script will:
# - Create directory structure
# - Copy templates
# - Preserve existing configs
# - Run validation checks
```

### Method 2: Manual Migration

**Best for:** Custom setups, learning the system

Follow [Step-by-Step Migration](#step-by-step-migration) below

### Method 3: Gradual Migration

**Best for:** Large teams, cautious approach

1. **Week 1:** Install v5.1 alongside v5.1
2. **Week 2:** Test v5.1 tools on one agent
3. **Week 3:** Roll out to team
4. **Week 4:** Deprecate v5.1 tools

---

## Step-by-Step Migration

### Step 1: Update Shared KB Submodule

```bash
# Navigate to your project
cd /path/to/your/project

# Update Shared KB to latest (includes v5.1)
cd .kb/shared
git pull origin main
cd ../..

# Verify v5.1 tools exist
ls -la .kb/shared/tools/
```

**Expected output:**
```
kb_submit.py
kb_search.py
kb_curate.py
hooks/
  └── session-start.sh
```

### Step 2: Create Directory Structure

```bash
# Create .kb directories
mkdir -p .kb/context
mkdir -p .kb/project/{integrations,endpoints,decisions,lessons,pending}

# Verify structure
tree .kb/
```

**Expected structure:**
```
.kb/
├── context/          # Will hold PROJECT.yaml and MEMORY.md
├── project/          # Your private KB
│   ├── integrations/
│   ├── endpoints/
│   ├── decisions/
│   ├── lessons/
│   └── pending/
└── shared/           # Submodule (already exists)
```

### Step 3: Create PROJECT.yaml

```bash
# Copy template
cp .kb/shared/examples/v5.1/PROJECT.yaml.example .kb/context/PROJECT.yaml

# Edit with your project details
nano .kb/context/PROJECT.yaml
# or use your preferred editor
```

**Minimum required fields:**
```yaml
meta:
  name: "Your Project Name"
  id: "your-project-id"

sharing_criteria:
  universal_if:
    - "Generic solution applicable to other projects"
  project_specific_if:
    - "Business logic specific to this project"
```

### Step 4: Create MEMORY.md (Optional)

```bash
# Copy template
cp .kb/shared/examples/v5.1/MEMORY.md.example .kb/context/MEMORY.md

# Edit with your project knowledge
nano .kb/context/MEMORY.md
```

### Step 5: Install SessionStart Hook

```bash
# Create hooks directory if not exists
mkdir -p .claude/hooks

# Copy session-start.sh
cp .kb/shared/tools/hooks/session-start.sh .claude/hooks/

# Make executable
chmod +x .claude/hooks/session-start.sh

# Verify
ls -la .claude/hooks/
```

### Step 6: Configure Environment

```bash
# Copy .env template
cp .kb/shared/examples/v5.1/.env.example .env

# Edit .env with your values
nano .env
```

**Add to .env:**
```bash
GITHUB_TOKEN=ghp_your_token_here
SHARED_KB_REPO=ozand/shared-knowledge-base

# Add .env to .gitignore if not already
echo ".env" >> .gitignore
```

**Get GitHub token:**
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo` (for private) or `public_repo` (for public)
4. Copy token and paste into `.env`

### Step 7: Verify Installation

```bash
# Test v5.1 search
python .kb/shared/tools/kb_search.py --stats

# Expected output:
# 📊 Knowledge Base Statistics
# ✅ SHARED KB: 149 entries
# ⚠️  Project KB: Not found at .kb/project

# Test context loading (manual test)
bash .claude/hooks/session-start.sh

# Expected output:
# 🤖 KB System Initialization v5.1
# 🔄 Step 1: Checking Shared KB updates...
# ✅ Shared KB is up to date
# 📥 Step 2: Loading Project Context...
# ✅ PROJECT.yaml found
# === PROJECT IDENTITY ===
# [Your PROJECT.yaml content]
```

### Step 8: Commit Changes

```bash
# Add new structure
git add .kb/
git add .claude/hooks/
git add .env.example

# Commit
git commit -m "Migrate to KB v5.1

- Add two-tier KB structure (Project KB + Shared KB)
- Install session-start.sh hook for context loading
- Add PROJECT.yaml with sharing criteria
- Configure environment for GitHub Issues workflow
- Backward compatible: v5.1 tools still work"

# Optional: Create backup branch first
git checkout -b backup/before-v5.1-migration
git checkout main  # or master
```

---

## Post-Migration Verification

### Checklist

Run through these checks to ensure migration was successful:

#### 1. Directory Structure
```bash
# Verify all directories exist
ls -d .kb/context .kb/project .claude/hooks

# Expected: All directories exist (no errors)
```

#### 2. Configuration Files
```bash
# Check PROJECT.yaml is valid YAML
python -c "import yaml; yaml.safe_load(open('.kb/context/PROJECT.yaml'))"

# Check .env exists and has required vars
grep -q "GITHUB_TOKEN" .env && echo "✅ GITHUB_TOKEN set"

# Check hook is executable
ls -l .claude/hooks/session-start.sh | grep -q "rwxr-xr-x"
```

#### 3. Tool Functionality

**Test search:**
```bash
python .kb/shared/tools/kb_search.py "docker"

# Expected: Shows results from Shared KB
```

**Test submit (local):**
```bash
# Create test entry
cat > /tmp/test.yaml << 'EOF'
version: "1.0"
category: "test"
last_updated: "2026-01-08"

errors:
  - id: "TEST-001"
    title: "Test entry"
    severity: "low"
    scope: "universal"
    problem: "Test problem"
    solution:
      code: "print('test')"
      explanation: "Test explanation"
EOF

# Submit to local
python .kb/shared/tools/kb_submit.py \
    --target local \
    --file /tmp/test.yaml

# Expected: ✅ [Local] File saved
```

**Test submit (shared - dry run):**
```bash
# Don't actually submit, just test validation
python .kb/shared/tools/kb_submit.py \
    --target shared \
    --file /tmp/test.yaml \
    --title "Test submission" \
    --domain testing

# Expected: Validation passes, asks for confirmation
# Press N to cancel (don't actually submit test)
```

#### 4. Context Loading

**Start new Claude Code session:**
```bash
# In new terminal/window
claude

# Watch for session-start.sh output
# Should see:
# 🤖 KB System Initialization v5.1
# ✅ Shared KB is up to date
# ✅ PROJECT.yaml found
```

#### 5. Backward Compatibility

```bash
# Test v5.1 tools still work
python .kb/shared/tools/kb.py search "docker"

# Expected: v5.1 search works normally
```

---

## Troubleshooting

### Issue 1: "PyGithub not installed"

**Error:**
```
❌ Error: PyGithub library not installed
   Install it: pip install PyGithub
```

**Solution:**
```bash
pip install PyGithub

# Or with pipenv
pipenv install PyGithub

# Or with poetry
poetry add PyGithub
```

### Issue 2: "GITHUB_TOKEN not found"

**Error:**
```
❌ Error: GITHUB_TOKEN not found in environment
```

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check .env has token
grep GITHUB_TOKEN .env

# Make sure Claude Code loads .env
# Add to Claude Code settings:
# "dotenv": [".env"]
```

### Issue 3: "PROJECT.yaml not found"

**Error:**
```
⚠️  PROJECT.yaml not found
   Agent will run without specific project instructions
```

**Solution:**
```bash
# Verify file exists
ls -la .kb/context/PROJECT.yaml

# If missing, recreate from template
cp .kb/shared/examples/v5.1/PROJECT.yaml.example .kb/context/PROJECT.yaml
```

### Issue 4: Hook not executing

**Symptom:** Context not loaded on session start

**Solution:**
```bash
# Check hook exists
ls -la .claude/hooks/session-start.sh

# Check hook is executable
chmod +x .claude/hooks/session-start.sh

# Manually test hook
bash .claude/hooks/session-start.sh

# Check Claude Code settings
# .claude/settings.json should have:
# {
#   "hooks": {
#     "SessionStart": ["hooks/session-start.sh"]
#   }
# }
```

### Issue 5: Permission denied on .kb directory

**Error:**
```
Permission denied: .kb/project/
```

**Solution:**
```bash
# Fix permissions
chmod -R 755 .kb/

# Or create directories with correct permissions
mkdir -p .kb/{context,project}
chmod 755 .kb/context .kb/project
```

### Issue 6: Git issues with submodule

**Error:**
```
fatal: not a git repository: .kb/shared
```

**Solution:**
```bash
# Reinitialize submodule
git submodule deinit .kb/shared
git submodule update --init --recursive .kb/shared

# Or remove and re-add
rm -rf .kb/shared
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared
```

---

## Rollback Instructions

### If You Need to Rollback

```bash
# Restore from backup
cp -r .kb.backup.YYYYMMDD/* .kb/

# Or revert git commit
git revert <commit-hash>

# Or reset to backup branch
git reset --hard backup/before-v5.1-migration

# Remove new directories
rm -rf .kb/context
rm -rf .kb/project
rm .claude/hooks/session-start.sh

# Restore old .env
cp .env.backup .env
```

### When to Rollback

- ❌ v5.1 tools don't work in your environment
- ❌ Team not ready for new workflow
- ❌ Critical bugs in v5.1
- ❌ Need more time to prepare

**Remember:** v5.1 tools still work, so you can use both!

---

## Success Criteria

Migration is successful when:

- ✅ All directories created correctly
- ✅ PROJECT.yaml configured with your project details
- ✅ SessionStart hook loads context automatically
- ✅ `kb_search.py` returns results
- ✅ `kb_submit.py --target local` works
- ✅ GITHUB_TOKEN configured (for shared submissions)
- ✅ v5.1 tools still work (backward compatibility)
- ✅ Team trained on new workflow

---

## Next Steps

### After Migration

1. **Train Your Team:**
   - Share [docs/v5.1/README.md](README.md) with team
   - Review [docs/v5.1/WORKFLOWS.md](WORKFLOWS.md)
   - Practice with test submissions

2. **Customize PROJECT.yaml:**
   - Add your specific sharing criteria
   - Document your integrations
   - Define your project goals

3. **Populate MEMORY.md:**
   - Document architectural decisions
   - Add lessons learned
   - Include onboarding tips

4. **Monitor Usage:**
   - Check GitHub Issues for submissions
   - Review quality scores
   - Gather team feedback

5. **Iterate:**
   - Adjust sharing criteria based on experience
   - Improve documentation
   - Share feedback with Shared KB maintainers

---

## Additional Resources

- **[Architecture](ARD.md)** - Complete v5.1 architecture
- **[Workflows](WORKFLOWS.md)** - Agent and curator protocols
- **[Context Schema](CONTEXT_SCHEMA.md)** - PROJECT.yaml reference
- **[Migration Plan](MIGRATION-PLAN.md)** - Detailed migration strategy
- **[v5.1 README](README.md)** - Quick start guide

---

## Support

**Issues? Questions?**

- 📖 Check [Troubleshooting](#troubleshooting) above
- 🔍 Search existing issues: [GitHub Issues](https://github.com/ozand/shared-knowledge-base/issues)
- 💬 Create new issue with tag `migration`
- 📧 Contact: [Open GitHub Issue](https://github.com/ozand/shared-knowledge-base/issues/new)

---

**Migration Status:** ✅ Document Complete
**Last Updated:** 2026-01-08
**Maintainer:** Shared KB Curator
