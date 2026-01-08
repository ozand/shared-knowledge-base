# Role Separation Enforcement Guide

**Date:** 2026-01-06
**Pattern:** AGENT-ROLE-SEPARATION-001
**Purpose:** Prevent project agents from taking Curator role

---

## 🎯 The Problem

**What Was Happening:**
Project agents were directly modifying Shared KB instead of contributing via GitHub issues.

**Real Example:**
```
✅ ОБНОВЛЕНИЕ ЗАВЕРШЕНО УСПЕШНО!
Статус: v5.1 → v5.1 (9 новых коммитов)
✅ Clean Directory Structure реализована
✅ YAML ошибки ИСПРАВЛЕНЫ!
✅ Новые паттерны (+5)
✅ PR #7 создан
```

**Why This Is Wrong:**
- ❌ Project Agent acted as Curator
- ❌ Bypassed quality review
- ❌ Violated AGENT-HANDOFF-001 workflow
- ❌ Quality control bypassed

---

## ✅ The Solution: Multi-Layer Enforcement

### Layer 1: Clear Role Definitions

**Project Agent:**
- Role: Contributes to Shared KB
- Access: **READ-ONLY** to shared-knowledge-base
- Can: Search, validate locally, create GitHub issues
- Cannot: Commit, create PR, modify KB files

**Curator Agent:**
- Role: Maintains Shared KB
- Access: Read-write to shared-knowledge-base
- Only agent who can commit to KB

### Layer 2: Agent Instructions

All agents auto-load `role_enforcement` section from:
`universal/agent-instructions/base-instructions.yaml`

Includes:
- Forbidden actions list
- Correct workflow steps
- Real-world examples
- Technical enforcement details

### Layer 3: Pre-Commit Hook

**Script:** `tools/pre-commit-role-check.py`

**What It Does:**
- Blocks non-curator commits to protected files
- Checks staged files before commit
- Provides clear error messages
- Guides to correct workflow

**Protected Files:**
- universal/ (patterns, agent-instructions)
- python/ (errors, patterns)
- postgresql/ (errors, patterns)
- tools/ (scripts, utilities)
- curator/ (Curator documentation)
- README.md, VERSION

### Layer 4: Repository Signage

**README.md:** Added ⚠️ Role-Based Access Control section

**.curator-only markers:** Added to protected directories:
- universal/.curator-only
- python/.curator-only
- postgresql/.curator-only
- tools/.curator-only
- curator/.curator-only

Each contains visible warning message.

---

## 🚀 Installation

### Step 1: Install Pre-Commit Hook

**In shared-knowledge-base repository:**

```bash
# Copy hook to .git/hooks/
cp tools/pre-commit-role-check.py .git/hooks/pre-commit

# Make executable
chmod +x .git/hooks/pre-commit

# Test (should allow - nothing to commit)
git commit --allow-empty -m "Test hook"
```

### Step 2: Verify Hook Installation

```bash
# Check hook exists
ls -la .git/hooks/pre-commit

# Should show:
# -rwxr-xr-x 1 user group 5432 Jan 6 03:40 pre-commit
```

### Step 3: Test Protection

**Test 1: Non-Curator Commit (Should Block)**

```bash
# Create test file
touch universal/test.yaml

# Try to commit (should be blocked)
git add universal/test.yaml
git commit -m "Test commit"

# Expected output:
# ❌ COMMIT BLOCKED: Curator-Only Files Modified
# 🚫 You are trying to modify Shared KB files directly.
# ❌ Forbidden Files:
#    • universal/test.yaml
```

**Test 2: Curator Commit (Should Allow)**

```bash
# Create .curator flag
touch .curator

# Try to commit (should succeed)
git commit -m "Curator commit"

# Clean up
rm .curator
```

---

## 📋 Usage

### For Project Agents

**What You CAN Do:**
```bash
# Search KB
kb search "async timeout"

# Validate local YAML
python tools/kb.py validate my-entry.yaml

# Pull KB updates
cd docs/knowledge-base/shared && git pull

# Create GitHub issue with attribution
gh issue create \
  --label "agent:claude-code" \
  --label "project:MY_PROJECT" \
  --label "kb-improvement" \
  --title "Add PYTHON-XXX: Pattern Name" \
  --body-file issue-template.md
```

**What You CANNOT Do:**
```bash
# ❌ These are BLOCKED
git commit -m "Add pattern"              # BLOCKED
gh pr create                             # BLOCKED
# Modify universal/, python/, etc.       # BLOCKED
```

### For Curator Agent

**Normal Operation:**
```bash
# Review issues
gh issue list --label "kb-improvement"

# Process contribution
# 1. Read issue
# 2. Validate YAML
# 3. Enhance entry
# 4. Commit to KB

# Enable curator mode
touch .curator

# Commit
git add universal/patterns/new-pattern.yaml
git commit -m "Add NEW-PATTERN-001

Contributed by: project-name
Reviewed by: Curator
Validated: ✓"

# Clean up
rm .curator
```

---

## 🔍 How It Works

### Pre-Commit Hook Flow

```
1. Agent runs: git commit
   ↓
2. Hook runs: .git/hooks/pre-commit
   ↓
3. Check: Is this shared-knowledge-base repo?
   No → Allow (not in KB)
   Yes ↓
4. Check: Is .curator file present?
   Yes → Allow (Curator mode)
   No ↓
5. Check: Are staged files protected?
   No → Allow (safe files)
   Yes ↓
6. BLOCK COMMIT
   Show error message
   Guide to correct workflow
   Exit with error code 1
```

### Agent Bootstrap Flow

```
1. Agent starts
   ↓
2. Runs: python tools/kb-agent-bootstrap.py
   ↓
3. Loads: universal/agent-instructions/base-instructions.yaml
   ↓
4. Reads: role_enforcement section
   ↓
5. Agent knows:
   - ❌ Cannot commit to shared-knowledge-base
   - ❌ Cannot create PR to shared-knowledge-base
   - ✅ Must use GitHub issues
   - ✅ Follow AGENT-HANDOFF-001
```

---

## 🛠️ Troubleshooting

### Problem: Hook blocks legitimate Curator commit

**Solution:**
```bash
# Make sure .curator file exists
touch .curator

# Commit
git commit

# Clean up (optional)
rm .curator
```

### Problem: Hook not installed

**Solution:**
```bash
# Reinstall hook
cp tools/pre-commit-role-check.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Verify
ls -la .git/hooks/pre-commit
```

### Problem: Agent ignores role enforcement

**Solution:**
```bash
# Re-run bootstrap to reload instructions
python tools/kb-agent-bootstrap.py

# Check .agent-config.local
cat .agent-config.local

# Should have:
# {
#   "enabled_features": [
#     "role_enforcement",
#     ...
#   ]
# }
```

### Problem: Need to bypass hook temporarily

**Solution (Curator ONLY):**
```bash
# Method 1: Use --no-verify (NOT RECOMMENDED)
git commit --no-verify -m "Message"

# Method 2: Use .curator file (RECOMMENDED)
touch .curator
git commit -m "Message"
rm .curator
```

---

## 📊 Verification Checklist

### For Shared KB Maintainers

- [ ] Pre-commit hook installed: `.git/hooks/pre-commit`
- [ ] Hook is executable: `chmod +x .git/hooks/pre-commit`
- [ ] .curator-only markers in all protected directories
- [ ] README.md has role-based access control section
- [ ] base-instructions.yaml v1.1+ with role_enforcement
- [ ] AGENT-ROLE-SEPARATION-001 pattern present

### For Project Agents

- [ ] Can search KB: `kb search "query"`
- [ ] Can validate locally: `kb validate file.yaml`
- [ ] Can pull updates: `git pull`
- [ ] Can create issues: `gh issue create`
- [ ] Cannot commit to KB (blocked by hook)
- [ ] Know to follow AGENT-HANDOFF-001

### For Curator Agent

- [ ] Can commit with `.curator` flag
- [ ] Reviews issues within 24h SLA
- [ ] Validates all contributions
- [ ] Enhances before merging
- [ ] Credits contributors in commits

---

## 🎓 Real-World Examples

### Example 1: Wrong (Role Violation)

**What Agent Did:**
```
Project Agent updated KB to v5.1:
• Committed to shared-knowledge-base ❌
• Fixed YAML errors ❌
• Added 5 patterns ❌
• Created PR #7 ❌
```

**Why Wrong:**
- Violated AGENT-ROLE-SEPARATION-001
- Bypassed Curator review
- Quality control bypassed

**What Should Have Done:**
```
1. Create YAML entries for 5 patterns
2. Validate locally
3. Create GitHub issue:
   Title: "Add 5 universal patterns for agent workflow"
   Labels: agent:claude-code, project:PROJECT, kb-improvement
   Body: Attach validated YAML entries
4. Curator reviews (24h)
5. Curator commits with attribution
```

### Example 2: Correct (Issue Workflow)

**Scenario:** Project Agent discovers async timeout pattern

**Steps:**
```
1. Encounters asyncio.TimeoutError
2. Searches KB: kb search "asyncio timeout"
3. Not found
4. Creates YAML: async-timeout.yaml
5. Validates: kb validate async-timeout.yaml ✓
6. Creates GitHub issue:
   • Title: "Add PYTHON-016: Async Timeout Pattern"
   • Labels: agent:claude-code, project:ECOMMERCE, agent-type:debugging
   • Body: Validated YAML + real-world example
7. Curator reviews (within 24h)
8. Curator enhances: adds more examples
9. Curator commits: python/errors/async-timeout.yaml
10. Curator closes issue with attribution
11. Project agent pulls updates
```

**Result:** ✅ Clean workflow, quality maintained, proper attribution

---

## 📚 Related Documentation

- **AGENT-ROLE-SEPARATION-001** - Full pattern documentation
- **AGENT-HANDOFF-001** - Cross-repository collaboration workflow
- **GITHUB-ATTRIB-001** - GitHub attribution for issues
- **AGENT-AUTO-001** - Agent auto-configuration from KB
- **universal/agent-instructions/base-instructions.yaml** - Agent instructions

---

## 🔄 Maintenance

### Updating Forbidden Actions

Edit `universal/agent-instructions/base-instructions.yaml`:
```yaml
role_enforcement:
  forbidden_actions:
    - action: "new forbidden action"
      severity: "BLOCKED"
      error: "Error message"
      correct_action: "What to do instead"
```

### Updating Protected Files

Edit `tools/pre-commit-role-check.py`:
```python
CURATOR_PATHS = [
    "universal/",
    "python/",
    # Add new protected paths here
]
```

### Versioning

Update `base-instructions.yaml` when changing:
```yaml
version: "1.2"  # Increment
last_updated: "2026-01-07"
```

---

**Status:** ✅ Production Ready
**Last Updated:** 2026-01-06
**Pattern:** AGENT-ROLE-SEPARATION-001
