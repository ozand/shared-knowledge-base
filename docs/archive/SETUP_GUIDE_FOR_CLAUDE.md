# Complete Setup Guide for Claude Code Agent
## Installing Shared KB in New Project with Sparse Checkout

**Target Audience:** Claude Code AI Agent
**Purpose:** Install Shared Knowledge Base in a new project with ONLY Project Agent content (excludes Curator files)
**Last Updated:** 2026-01-06
**Version:** 1.0

---

## 🎯 Overview

This guide provides **complete step-by-step instructions** for Claude Code agent to set up Shared Knowledge Base in a new project from scratch.

**Key Principle:** Use **sparse checkout** to load ONLY Project Agent content, excluding ALL Curator-specific files.

**Why Sparse Checkout?**
- ✅ Reduces repository size by ~22%
- ✅ Prevents context contamination
- ✅ Enforces role separation (Project Agent vs Curator)
- ✅ Faster cloning and updates
- ✅ Cleaner AI context

---

## 📋 Prerequisites Check

**Before starting, verify:**

1. **Git is installed:**
   ```bash
   git --version
   # Expected: git version 2.x.x or higher
   ```

2. **Python is installed:**
   ```bash
   python --version
   # Expected: Python 3.8 or higher
   ```

3. **Project directory exists:**
   ```bash
   # If project doesn't exist yet:
   mkdir /path/to/your/project
   cd /path/to/your/project
   ```

4. **Git repository initialized (if not already):**
   ```bash
   cd /path/to/your/project
   git init
   git add .
   git commit -m "Initial commit"
   ```

---

## 🚀 Installation Methods

### Method 1: Automated Setup (RECOMMENDED) ⭐

**Best for:** Quick setup, less error-prone

#### Linux/Mac:

```bash
# Step 1: Navigate to your project
cd /path/to/your/project

# Step 2: Clone Shared KB temporarily to get setup script
git clone https://github.com/ozand/shared-knowledge-base.git /tmp/shared-kb-setup

# Step 3: Run automated sparse setup
bash /tmp/shared-kb-setup/scripts/setup-shared-kb-sparse.sh

# Step 4: Clean up temporary clone
rm -rf /tmp/shared-kb-setup
```

#### Windows (PowerShell):

```powershell
# Step 1: Navigate to your project
cd C:\path\to\your\project

# Step 2: Clone Shared KB temporarily
git clone https://github.com/ozand/shared-knowledge-base.git C:\temp\shared-kb-setup

# Step 3: Run automated sparse setup
powershell -ExecutionPolicy Bypass -File C:\temp\shared-kb-setup\scripts\setup-shared-kb-sparse.ps1

# Step 4: Clean up
Remove-Item -Recurse -Force C:\temp\shared-kb-setup
```

**What the script does:**
- ✅ Adds submodule: `git submodule add https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base/shared`
- ✅ Enables sparse checkout: `git config core.sparseCheckout true`
- ✅ Creates sparse-checkout file with Project Agent paths only
- ✅ Pulls only specified content
- ✅ Excludes curator/ directory and Curator-specific files

---

### Method 2: Manual Setup (For Custom Configuration)

**Best for:** Custom sparse checkout configuration, learning how it works

#### Complete Manual Setup:

```bash
# Step 1: Navigate to your project
cd /path/to/your/project

# Step 2: Create directory structure
mkdir -p docs/knowledge-base

# Step 3: Add submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base/shared

# Step 4: Enable sparse checkout
cd docs/knowledge-base/shared
git config core.sparseCheckout true

# Step 5: Create sparse-checkout file
cat > .git/info/sparse-checkout <<'EOF'
# Core documentation
README.md
GUIDE.md
QUICKSTART.md
README_INTEGRATION.md

# Agent guides
AGENT_INTEGRATION_GUIDE.md
AGENT_AUTOCONFIG_GUIDE.md
ROLE_SEPARATION_GUIDE.md
GITHUB_ATTRIBUTION_GUIDE.md
AGENT-QUICK-START.md

# Patterns (MAIN CONTENT for Project Agents)
universal/
python/
postgresql/
docker/
javascript/
vps/
framework/

# Tools
tools/
scripts/

# Base configuration
.kb-config.yaml
.gitignore.agents
.kb-version
EOF

# Step 6: Pull only specified content
git pull origin main

# Step 7: Return to project root
cd ../..
```

**What this does:**
- Line 14-23: Include only essential documentation
- Line 26-30: Include agent guides (NOT Curator guides)
- Line 33-39: Include ALL pattern directories (main content)
- Line 42-43: Include tools and scripts
- Line 46-48: Include configuration files

**What's EXCLUDED (not listed):**
- ❌ `curator/` (entire Curator directory)
- ❌ `*_ANALYSIS.md` (analysis documents)
- ❌ `*_REPORT.md` (Curator reports)
- ❌ `CHAT_*.md` (chat analysis)
- ❌ `.agent-config.local` (generated files)
- ❌ `_index*.yaml` (generated indexes)

---

## ✅ Verification Steps

**After installation, verify the setup:**

### Test 1: Verify submodule status

```bash
git submodule status docs/knowledge-base/shared
```

**Expected output:**
```
 c023036...docs/knowledge-base/shared (v3.0-10-gc023036)
^
Leading space = properly initialized ✅
```

### Test 2: Verify sparse checkout is active

```bash
cd docs/knowledge-base/shared
git config core.sparseCheckout
```

**Expected output:**
```
true
```

### Test 3: Verify Curator files are NOT loaded

```bash
cd docs/knowledge-base/shared
ls -la curator/
```

**Expected output:**
```
ls: cannot access 'curator/': No such file or directory ✅
```

**This confirms sparse checkout is working!**

### Test 4: Verify Project Agent files ARE loaded

```bash
cd docs/knowledge-base/shared
ls -la universal/patterns/
```

**Expected output:**
```
(agent-role-separation.yaml)
(agent-handoff.yaml)
(agent-direct-submodule-access.yaml)
(stale-context.yaml)
...etc ✅
```

### Test 5: Count files

```bash
# Count loaded files
find docs/knowledge-base/shared -type f | wc -l

# Should be: ~100-150 files (not 500+ with full checkout)
```

---

## 🔧 Post-Installation Setup

### Step 1: Copy kb.py tool to project

```bash
# Create tools directory
mkdir -p docs/knowledge-base/tools

# Copy kb.py from Shared KB
cp docs/knowledge-base/shared/tools/kb.py docs/knowledge-base/tools/

# Make executable (Linux/Mac)
chmod +x docs/knowledge-base/tools/kb.py
```

### Step 2: Create local KB index

```bash
# Create cache directory
mkdir -p docs/knowledge-base/.cache

# Build search index
python docs/knowledge-base/tools/kb.py index -v
```

**Expected output:**
```
Indexing Shared KB entries...
Found: 95 entries (pattern, error)
Indexed: 95 entries
Database: docs/knowledge-base/.cache/kb_index.db
```

### Step 3: Test search functionality

```bash
# Test search
python docs/knowledge-base/tools/kb.py search "async"
```

**Expected output:**
```
Searching for: async
Found: X results
1. universal/patterns/async-anti-pattern.yaml
2. python/errors/async-timeout.yaml
...
```

### Step 4: Verify auto-configuration

**Check if agent instructions are loaded:**

```bash
ls -la docs/knowledge-base/shared/universal/agent-instructions/
```

**Expected files:**
```
base-instructions.yaml  (auto-loaded by all agents)
templates/  (issue/PR templates)
```

**What auto-configuration provides:**
- ✅ Submodule access rules (forbidden/required commands)
- ✅ Role-based access control (Project Agent vs Curator)
- ✅ GitHub attribution requirements
- ✅ Quality standards and workflows

---

## 📖 Daily Usage for Claude Code Agent

### Update Shared KB

```bash
# Check current status
git submodule status docs/knowledge-base/shared

# Update to latest
git submodule update --remote docs/knowledge-base/shared

# Verify update
git submodule status docs/knowledge-base/shared
```

### Search Knowledge Base

```bash
# Basic search
python docs/knowledge-base/tools/kb.py search "keyword"

# Advanced search
python docs/knowledge-base/tools/kb.py search --category python --severity high

# Search by tags
python docs/knowledge-base/tools/kb.py search --tags async,docker
```

### Check for Updates

```bash
python docs/knowledge-base/shared/tools/kb.py check-updates
```

**Expected output:**
```
Checking for Shared KB updates...
Current commit: c023036
Remote commit: a1b2c3d
Status: Updates available!

Recent commits:
a1b2c3d Add new pattern
b4c5d6f Fix YAML error

To update:
git submodule update --remote docs/knowledge-base/shared
```

---

## 🎯 Critical Rules for Claude Code Agent

### ✅ ALWAYS Do These:

1. **Use git submodule commands:**
   ```bash
   git submodule status docs/knowledge-base/shared
   git submodule update --remote docs/knowledge-base/shared
   ```

2. **Verify before referencing:**
   ```bash
   gh issue view NUMBER --json state,title
   ```

3. **Check submodule status first:**
   ```bash
   git submodule status docs/knowledge-base/shared
   ```

4. **Work from project root:**
   ```bash
   # Stay in project root, use relative paths
   python docs/knowledge-base/tools/kb.py search "keyword"
   ```

### ❌ NEVER Do These:

1. **Direct submodule access:**
   ```bash
   # WRONG
   git -C docs/knowledge-base/shared fetch origin
   cd docs/knowledge-base/shared && git pull
   ```

2. **Assume state without verification:**
   ```bash
   # WRONG
   echo "Waiting for Issue #11"  # Issue might be closed!
   ```

3. **Commit to Shared KB:**
   ```bash
   # WRONG - Project Agents CANNOT commit to Shared KB
   cd docs/knowledge-base/shared
   git commit -m "Add pattern"  # FORBIDDEN
   ```

4. **Create PR to Shared KB:**
   ```bash
   # WRONG - Use GitHub Issues instead
   gh pr create  # FORBIDDEN for Project Agents
   ```

---

## 🔄 Typical Workflow for Claude Code Agent

### Scenario 1: Starting Work on New Feature

```bash
# Step 1: Update Shared KB
git submodule update --remote docs/knowledge-base/shared

# Step 2: Search for relevant patterns
python docs/knowledge-base/tools/kb.py search "authentication"

# Step 3: Read relevant patterns
# (Claude Code reads the YAML files and applies the knowledge)

# Step 4: Implement feature using best practices from KB
```

### Scenario 2: Encountering an Error

```bash
# Step 1: Search KB for error
python docs/knowledge-base/tools/kb.py search "error message"

# Step 2: If found, apply solution
# (Claude Code reads pattern and implements fix)

# Step 3: If not found, consider creating new pattern
# (Follow AGENT-HANDOFF-001 workflow)
```

### Scenario 3: Contributing New Pattern

```bash
# Step 1: Search KB first (prevent duplicates)
python docs/knowledge-base/tools/kb.py search "pattern keywords"

# Step 2: Create YAML locally
cat > my-pattern.yaml <<'EOF'
version: "1.0"
category: "pattern-category"
last_updated: "2026-01-06"

patterns:
  - id: "PATTERN-001"
    title: "Pattern Title"
    # ... complete pattern
EOF

# Step 3: Validate
python docs/knowledge-base/tools/kb.py validate my-pattern.yaml

# Step 4: Create GitHub issue with FULL YAML
gh issue create \
  --repo shared-knowledge-base \
  --label "agent:claude-code" \
  --label "project:YOUR_PROJECT" \
  --label "kb-improvement" \
  --title "Add PATTERN-001: Pattern Title" \
  --body-file issue-template.md

# Step 5: Wait for Curator review (24h SLA)
```

---

## 🐛 Troubleshooting

### Problem: "fatal: not a git repository"

**Cause:** Project not initialized as git repository

**Solution:**
```bash
cd /path/to/your/project
git init
git add .
git commit -m "Initial commit"
# Then re-run Shared KB setup
```

### Problem: "curator/ directory exists"

**Cause:** Sparse checkout not configured correctly

**Solution:**
```bash
cd docs/knowledge-base/shared
git config core.sparseCheckout true
# Verify sparse-checkout file exists:
cat .git/info/sparse-checkout
# Should list Project Agent files only, NOT curator/
# Then reset:
git reset --hard HEAD
```

### Problem: "Submodule shows - prefix (not initialized)"

**Cause:** Submodule not properly initialized

**Solution:**
```bash
git submodule init docs/knowledge-base/shared
git submodule update docs/knowledge-base/shared
```

### Problem: "Update command shows 'No output'"

**This is GOOD!** It means already up to date.

```bash
# No output = Already at latest version ✅
git submodule update --remote docs/knowledge-base/shared
# (No output = success)
```

### Problem: "Can't find patterns in search"

**Cause:** Index not built or outdated

**Solution:**
```bash
# Rebuild index
python docs/knowledge-base/tools/kb.py index -v

# Test search
python docs/knowledge-base/tools/kb.py search "test"
```

---

## 📊 What You Get vs What's Excluded

### ✅ Loaded (Project Agent Content):

**Documentation:**
- README.md
- GUIDE.md
- QUICKSTART.md
- AGENT-QUICK-START.md
- AGENT_INTEGRATION_GUIDE.md
- AGENT_AUTOCONFIG_GUIDE.md
- ROLE_SEPARATION_GUIDE.md
- GITHUB_ATTRIBUTION_GUIDE.md

**Patterns (MAIN CONTENT):**
- universal/ (all universal patterns)
- python/ (Python-specific patterns)
- postgresql/ (PostgreSQL patterns)
- docker/ (Docker patterns)
- javascript/ (JavaScript patterns)
- vps/ (VPS patterns)
- framework/ (Framework-specific patterns)

**Tools:**
- tools/kb.py (main CLI tool)
- tools/kb_*.py (metadata tools)
- scripts/ (automation scripts)

**Agent Configuration:**
- universal/agent-instructions/base-instructions.yaml
- universal/agent-instructions/templates/

### ❌ Excluded (Curator Content):

**Curator Directory:**
- curator/ (entire directory)
  - AGENT.md (Curator role definition)
  - SKILLS.md (Curator skills)
  - WORKFLOWS.md (Curator workflows)
  - QUALITY_STANDARDS.md (Quality rubric)
  - PROMPTS.md (AI prompt templates)
  - metadata/ (metadata system docs)

**Analysis Documents:**
- *_ANALYSIS.md (all analysis documents)
- *_REPORT.md (all Curator reports)
- CHAT_*.md (chat analysis documents)

**Generated Files:**
- .agent-config.local
- _index*.yaml (generated indexes)
- *_meta.yaml (metadata files)

---

## 🎓 Key Concepts

### What is Sparse Checkout?

Git sparse checkout allows you to **checkout only part of a repository**, excluding files/directories you don't need.

**Benefits:**
- Smaller repository size
- Faster clone/update operations
- Cleaner context for AI agents
- Enforced role separation

### How Does It Work?

1. **Enable sparse checkout:**
   ```bash
   git config core.sparseCheckout true
   ```

2. **Define what to include:**
   ```bash
   # Create .git/info/sparse-checkout
   echo "universal/" >> .git/info/sparse-checkout
   echo "python/" >> .git/info/sparse-checkout
   # (NOT including curator/)
   ```

3. **Pull only specified content:**
   ```bash
   git pull origin main
   # Only universal/ and python/ are checked out
   ```

### Role Separation Enforcement

**Project Agents:**
- Get: patterns/, tools/, agent guides
- Cannot: Access curator/ documentation
- Result: Clean context, focused on project work

**Curators:**
- Get: Full repository (including curator/)
- Can: Access all Curator documentation
- Result: Complete context for curation work

---

## 📚 Further Reading

**Setup Guides:**
- [QUICKSTART.md](docs/knowledge-base/shared/QUICKSTART.md) - 5-minute setup
- [SUBMODULE_VS_CLONE.md](docs/knowledge-base/shared/SUBMODULE_VS_CLONE.md) - Submodule vs Clone comparison

**Agent Guides:**
- [AGENT-QUICK-START.md](docs/knowledge-base/shared/AGENT-QUICK-START.md) - Agent quick reference
- [AGENT_INTEGRATION_GUIDE.md](docs/knowledge-base/shared/AGENT_INTEGRATION_GUIDE.md) - Complete integration guide

**Patterns:**
- [GIT-SUBMODULE-001](docs/knowledge-base/shared/universal/patterns/git-submodule-init.yaml) - Submodule integration
- [KB-UPDATE-001](docs/knowledge-base/shared/universal/patterns/kb-update.yaml) - Update process
- [AGENT-DIRECT-SUBMODULE-ACCESS-001](docs/knowledge-base/shared/universal/patterns/agent-direct-submodule-access.yaml) - Access rules

---

## ✅ Setup Checklist

Use this checklist to verify complete setup:

- [ ] Git repository initialized in project
- [ ] Shared KB added as submodule
- [ ] Sparse checkout enabled
- [ ] sparse-checkout file created (excludes curator/)
- [ ] Initial pull completed
- [ ] Submodule status shows leading space (good)
- [ ] curator/ directory NOT present (verified)
- [ ] Pattern directories ARE present (verified)
- [ ] kb.py copied to tools/
- [ ] Search index built successfully
- [ ] Test search returns results
- [ ] Auto-configuration loaded (base-instructions.yaml present)

**All checks passed?** You're ready to use Shared KB! 🎉

---

**Last Updated:** 2026-01-06
**Version:** 1.0
**For:** Claude Code AI Agent
**Questions?** Create GitHub issue with label `kb-improvement`
