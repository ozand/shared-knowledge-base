# KB-UPDATE-001: Troubleshooting Guide

## Issue 1: Network Error

**Symptom:** Could not fetch from remote

**Causes:**
- No internet connection
- GitHub repository inaccessible
- Firewall blocking git requests
- SSH key authentication issues (if using SSH)

**Solutions:**

### Check internet connection
```bash
ping github.com
```

### Switch from SSH to HTTPS
```bash
# In .gitmodules
url = https://github.com/ozand/shared-knowledge-base.git
```

### Use VPN or proxy if needed

### Configure git proxy
```bash
git config --global http.proxy http://proxy.example.com:8080
```

---

## Issue 2: Merge Conflict

**Symptom:** Automatic merge failed; fix conflicts

**Causes:**
- Local changes in Shared KB directory
- Diverged history
- Both submodule and local modified same files

**Solutions:**

### Stash local changes first
```bash
cd docs/knowledge-base/shared
git stash
git submodule update --remote --merge
# Apply stash back if needed
git stash pop
```

### Reset to clean state
```bash
cd docs/knowledge-base/shared
git reset --hard origin/main
cd ../..
git add docs/knowledge-base/shared
git commit -m "Reset Shared KB to clean state"
```

### Resolve conflicts manually
```bash
cd docs/knowledge-base/shared
git status  # See conflicts
# Edit conflicted files, remove markers
git add <resolved-files>
git commit
```

---

## Issue 3: Submodule Detached

**Symptom:** Submodule in detached HEAD state

**Causes:**
- Manual git operations in submodule
- Incomplete update
- Checkout to specific commit

**Solutions:**

### Reattach to main branch
```bash
cd docs/knowledge-base/shared
git checkout main
git pull origin main
cd ../..
git add docs/knowledge-base/shared
git commit -m "Reattach Shared KB to main"
```

### Use submodule update
```bash
git submodule update --remote --merge docs/knowledge-base/shared
```

---

## Issue 4: Sparse Checkout Broken

**Symptom:** All files loaded, including curator/

**Causes:**
- Sparse checkout config lost
- .git/info/sparse-checkout deleted
- core.sparseCheckout reset to false

**Solutions:**

### Re-enable sparse checkout
```bash
cd docs/knowledge-base/shared
git config core.sparseCheckout true
cat > .git/info/sparse-checkout <<'EOF'
universal/
python/
postgresql/
docker/
javascript/
vps/
tools/
scripts/
README.md
GUIDE.md
AGENT_*.md
ROLE_SEPARATION_GUIDE.md
GITHUB_ATTRIBUTION_GUIDE.md
.kb-config.yaml
.gitignore.agents
EOF
git reset --hard HEAD
git checkout
```

### Use automated script
```bash
bash /path/to/shared-knowledge-base/scripts/setup-shared-kb-sparse.sh
```

---

## Issue 5: Feature Branch Not Merged

**Symptom:** Feature branch exists but submodule update doesn't merge it

**Example:**
```bash
git submodule update --remote --merge docs/knowledge-base/shared
# Output: * [new branch] fix/feature -> origin/fix/feature
# But no merge happens!
```

**Causes:**
- Feature branch not merged to main in upstream repository
- Submodule tracks 'main', not feature branches
- git submodule update --remote only updates tracked branch

**Explanation:**
git submodule update --remote updates to the **tracked branch**
(usually origin/main), NOT to any feature branches.

Feature branches must be merged to main in upstream repository
BEFORE projects can get them via standard submodule update.

**Solutions:**

### Verify content already in main (COMMON CASE)
```bash
cd docs/knowledge-base/shared
# Check if file/feature already exists
ls -la tools/kb_config.py

# If exists: Feature already merged to main
# If missing: Feature not yet in main
```
**When to use:** Feature branch was created before similar changes merged to main

### Wait for upstream merge (RECOMMENDED)
1. Check upstream repository status
2. Wait for feature branch to be merged to main
3. Then run: `git submodule update --remote --merge`
4. Usually takes 1-7 days

**Rationale:** Standard workflow, maintains alignment with upstream

### Request expedited merge
1. Comment on upstream PR/issue
2. Explain urgency: 'Need this feature for production'
3. Wait for merge, then update

**When to use:** Feature is critical for your project

### Manually merge feature branch (NOT RECOMMENDED)
```bash
cd docs/knowledge-base/shared
git fetch origin
git merge origin/fix/feature-branch
cd ../..
git add docs/knowledge-base/shared
git commit -m "Update Shared KB to feature branch"
```
**Warnings:**
- ⚠️ Creates divergence from main
- ⚠️ May cause conflicts later
- ⚠️ Non-standard workflow
- ⚠️ Use only if absolutely necessary

### Decision Framework

**Question:** Should you merge feature branch manually?

#### Check main first
```bash
git fetch origin
git log origin/main --oneline | grep feature-description
```

**If in main:**
- ✅ Stay on main, don't merge feature branch
- Standard update will get the changes

**If not in main:**
- ⏰ Wait for upstream merge OR request expedited merge

#### Evaluate urgency
**Question:** Is this feature critical for your project?

**If yes:**
1. Comment on upstream PR/issue requesting expedited merge
2. Explain business impact
3. Wait for merge (usually faster with maintainer context)

**If no:**
1. Wait for standard merge process
2. Usually 1-7 days
3. Then: `git submodule update --remote --merge`

### Real-World Example

**Project:** CompanyBase

**Situation:**
```bash
git submodule update --remote --merge docs/knowledge-base/shared
# Shows: * [new branch] fix/add-kb-config-v5.1
# But: No merge, submodule stays on main
```

**Analysis:**
Feature branch fix/add-kb-config-v5.1 adds kb_config.py
BUT: Main already has commit 347ecea that adds kb_config.py

**Root Cause:**
Feature branch created before commit was merged to main
Content is duplicate/old version

**Solution Applied:**
1. Verified: tools/kb_config.py already exists in main
2. Stayed on main branch
3. No need to merge feature branch

**Result:**
- ✅ v5.1 features working via main branch
- ✅ No divergence from upstream
- ✅ Standard update workflow maintained

---

## Issue 6: Plain Clone Not Git Repo

**Symptom:** git submodule commands fail - 'not a git repository'

**Example:**
```bash
git submodule update --remote --merge docs/knowledge-base/shared
fatal: not a git repository (or any of the parent directories)
```

**Causes:**
- Project not initialized as git repository
- Shared KB installed as plain clone, not submodule
- No .git directory in project root

**Explanation:**
Project uses plain clone installation method:
- Shared KB added via: `git clone https://github.com/...`
- Not via: `git submodule add`
- Project root has no .git directory

**Result:**
- git submodule commands don't work from project root
- But shared/ directory IS a git repository
- Can update shared/ directly with git commands

**Solutions:**

### Update shared/ directly (WORKAROUND)
```bash
cd docs/knowledge-base/shared
git pull origin main
```

**When to use:** Short-term, before git init

**Pros:**
- Works immediately
- No setup required

**Cons:**
- Manual process
- Must remember to update
- No submodule benefits

### Initialize git and migrate to submodule (RECOMMENDED)

```bash
# 1. Initialize git for project
cd /path/to/project
git init

# 2. Create .gitignore
# (Exclude: venv, __pycache__, .idea, etc.)

# 3. Initial commit
git add .
git commit -m "Initial commit"

# 4. Remove old clone
rm -rf docs/knowledge-base/shared

# 5. Add as submodule (optionally with sparse checkout)
git submodule add https://github.com/ozand/shared-knowledge-base.git \
  docs/knowledge-base/shared

# OR use automated sparse setup
bash /path/to/shared-knowledge-base/scripts/setup-shared-kb-sparse.sh

# 6. Test
git submodule update --remote --merge docs/knowledge-base/shared
```

**When to use:** When ready for professional setup

**Pros:**
- git submodule update works
- Version pinning available
- Team collaboration enabled
- Can use sparse checkout
- Automatic update checks

**Cons:**
- One-time setup required
- Takes ~5 minutes

### Use sparse checkout during migration (OPTIMAL)
```bash
# Use automated script with sparse checkout
bash /path/to/shared-knowledge-base/scripts/setup-shared-kb-sparse.sh
```

**Benefits:**
- Loads only patterns + agent guides
- Excludes Curator files (~22% savings)
- Clean context for Project Agents
- Role separation enforced

### Real-World Example

**Project:** PARSER

**Situation:**
```bash
git submodule update --remote --merge docs/knowledge-base/shared
fatal: not a git repository

cd docs/knowledge-base/shared
git status
# On branch main
# Your branch is up to date with 'origin/main'
```

**Analysis:**
PARSER project:
- Not under git (no .git in root)
- Shared KB installed as plain clone
- But shared/ IS a git repository

**Verification:**
```bash
ls docs/knowledge-base/shared/.git
# Exists! It's a git repository
```

**Current Solution:**
```bash
# Update shared/ directly
cd docs/knowledge-base/shared
git pull origin main
# Already up to date
```

**Recommended Migration:**
1. Initialize git: `cd /path/to/PARSER && git init`
2. Initial commit: `git add . && git commit -m "Initial"`
3. Migrate to submodule: Remove old clone, add as submodule
4. Setup sparse checkout: Exclude Curator files
5. Test: `git submodule update --remote --merge`

**Benefits of Migration:**
- ✅ Standard submodule commands work
- ✅ Clean context (sparse checkout)
- ✅ Easy updates
- ✅ Team collaboration
- ✅ Automatic update checks

**Timeline:**
- Phase 1 (Current): Continue with plain clone
- Phase 2 (When ready): Initialize git
- Phase 3 (Migration): Add submodule + sparse checkout
- Phase 4 (Long-term): Enable auto-update checks

### Decision Framework

**Question:** Should project initialize git?

**Checklist:**

**Is code stable?**
- ✅ Ready for git init
- ⏰ Wait until stable

**Will others work on it?**
- ✅ Git init recommended
- ❌ Local is fine

**Need collaboration?**
- ✅ Git required
- ❌ Local OK

**Want automatic updates?**
- ✅ Submodule helps
- ⚠️ Manual update OK

**Recommendation:**
- 3+ YES answers: Initialize git ✅
- 1-2 YES answers: Can continue plain clone ⏰

### See Also

- **PLAIN_CLONE_PROJECT_ANALYSIS.md** - Detailed PARSER analysis
- **SUBMODULE_VS_CLONE.md** - Comparison of approaches
- **scripts/setup-shared-kb-sparse.sh** - Automated setup
- **SHARED_KB_UPDATE_MECHANISMS_ANALYSIS.md** - Update mechanisms
