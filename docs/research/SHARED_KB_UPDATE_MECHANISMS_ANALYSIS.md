# Shared KB Update Mechanisms Analysis

**Date:** 2026-01-06
**Issue:** How do projects using Shared KB learn about new patterns?
**Critical Gap:** No systematic update mechanism for plain clone projects

---

## 📊 Executive Summary

**Current State:**
- ✅ Submodule projects: Can update (`git submodule update`)
- ❌ Plain clone projects: NO update mechanism!
- ❌ No notifications: Projects don't know about new patterns
- ❌ No version checking: Agents don't know if KB is stale

**Impact:** Projects work with outdated knowledge, missing new patterns

---

## 🔍 Current Mechanisms

### Mechanism 1: Git Submodule (AUTO)

**How it works:**
```bash
# Initial setup
git submodule add https://github.com/ozand/shared-knowledge-base.git \
  docs/knowledge-base/shared

# Update to latest
git submodule update --remote --merge docs/knowledge-base/shared
```

**Pros:**
- ✅ Automatic updates available
- ✅ Simple command
- ✅ Merge conflict resolution built-in

**Cons:**
- ❌ Requires git init (not all projects are git repos)
- ❌ More complex setup
- ❌ Submodule learning curve

**Projects using:** Unknown (not tracked)

### Mechanism 2: Plain Clone (MANUAL - NO TOOL!)

**How it works:**
```bash
# Initial clone
git clone https://github.com/ozand/shared-knowledge-base.git \
  docs/knowledge-base/shared

# Update to latest (NOT DOCUMENTED!)
cd docs/knowledge-base/shared
git pull origin main
```

**Pros:**
- ✅ Simple setup
- ✅ Works without git init

**Cons:**
- ❌ NO update mechanism documented
- ❌ No notifications about new patterns
- ❌ Manual process required
- ❌ Agents don't know when to update
- ❌ No version checking

**Projects using:** PARSER, APP-SW, likely others

### Mechanism 3: AGENT-AUTO-001 (Bootstrap Only)

**What it does:**
- Auto-discovers Shared KB location
- Loads base-instructions.yaml
- Generates .agent-config.local

**What it DOESN'T do:**
- ❌ Check for KB updates
- ❌ Notify about new patterns
- ❌ Auto-update Shared KB
- ❌ Compare versions

**Gap:** Bootstrap happens ONCE, never updates again

---

## ❌ Critical Gaps

### Gap 1: No Version Tracking

**Problem:** No way to know if local KB is stale

**Current state:**
```bash
# Agent doesn't know:
- What version of Shared KB is local?
- What version is latest on GitHub?
- Are there new patterns since last update?
- Should I update now?
```

**Impact:** Agents work with outdated knowledge

### Gap 2: No Update Notifications

**Problem:** Agents don't know when to update

**Example scenario:**
```
Day 1: Project clones Shared KB (87 entries)
Day 7: Curator adds 3 new patterns (90 entries)
Day 30: Agent still has 87 entries!
Day 60: Agent still has 87 entries!
Result: Agent missing 3 patterns
```

**Impact:** Knowledge gap grows over time

### Gap 3: No Automated Update Process

**Problem:** Manual git pull required, not automated

**Current state:**
- Agent must remember to: `cd shared && git pull`
- No reminder/note to update
- No integration with agent workflow
- No check at start of session

**Impact:** Updates happen rarely or never

### Gap 4: No Change Detection

**Problem:** Agents don't know WHAT changed

**Current state:**
```bash
git pull origin main
# Shows 50 commits, 5000 lines changed
# Agent has no idea:
# - Which patterns affect me?
# - Which categories updated?
# - Should I re-read instructions?
```

**Impact:** Information overload, agent ignores updates

---

## 💡 Proposed Solutions

### Solution A: Add KB-UPDATE-001 Pattern ⭐

**Create pattern documenting update process:**

```yaml
version: "1.0"
category: "knowledge-base"
patterns:
  - id: "KB-UPDATE-001"
    title: "Shared KB Update Process for Projects"
    severity: "high"
    scope: "universal"

    workflows:
      submodule_approach:
        update_command: |
          git submodule update --remote --merge \
            docs/knowledge-base/shared

        check_for_updates: |
          cd docs/knowledge-base/shared
          git fetch origin
          git log HEAD..origin/main --oneline

      plain_clone_approach:
        update_command: |
          cd docs/knowledge-base/shared
          git pull origin main

        check_for_updates: |
          cd docs/knowledge-base/shared
          git fetch origin
          git log HEAD..origin/main --oneline

        recommended_frequency: |
          - Before starting major work
          - Weekly if active development
          - Monthly if maintenance mode
```

### Solution B: Add kb.py check-updates Command ⭐⭐

**Create command to check and notify:**

```python
# tools/kb.py
def check_updates():
    """Check if Shared KB has updates since last pull"""

    shared_dir = get_shared_kb_dir()

    # Fetch latest (don't merge)
    subprocess.run(["git", "-C", shared_dir, "fetch", "origin"])

    # Check for new commits
    result = subprocess.run(
        ["git", "-C", shared_dir, "log", "HEAD..origin/main", "--oneline"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0 and result.stdout.strip():
        # New commits available
        commits = result.stdout.strip().split('\n')
        print(f"⚠️  {len(commits)} new updates available:")
        for commit in commits[:10]:  # Show first 10
            print(f"  - {commit}")

        print("\nTo update:")
        print("  cd docs/knowledge-base/shared && git pull")

        return True
    else:
        print("✅ Shared KB is up to date")
        return False
```

**Usage:**
```bash
# At start of agent session
python tools/kb.py check-updates
```

**Example output:**
```
⚠️  3 new updates available:
  - de93da6 Add Curator Decision Framework...
  - b56ffa6 Add APP SW role confusion case...
  - 99f9736 Add 3 new patterns from session...

To update: cd docs/knowledge-base/shared && git pull
```

### Solution C: Auto-Check on Session Start ⭐⭐⭐

**Modify AGENT-AUTO-001 bootstrap to check updates:**

```python
# tools/kb-agent-bootstrap.py
def bootstrap_with_updates():
    """Bootstrap agent and check for KB updates"""

    # 1. Load base instructions (existing)
    instructions = load_base_instructions()

    # 2. Check for KB updates (NEW!)
    check_kb_updates()

    # 3. Generate .agent-config.local (existing)
    generate_config()

def check_kb_updates():
    """Check and notify about KB updates"""

    shared_dir = get_shared_kb_dir()

    if not is_git_repo(shared_dir):
        print("ℹ️  Shared KB is not a git repo (plain clone)")
        return

    # Fetch updates
    result = subprocess.run(
        ["git", "-C", shared_dir, "fetch", "origin"],
        capture_output=True
    )

    if result.returncode != 0:
        return  # Not a git clone or no network

    # Check for new commits
    log_result = subprocess.run(
        ["git", "-C", shared_dir, "log", "HEAD..origin/main",
         "--since", "1 month ago", "--oneline"],
        capture_output=True,
        text=True
    )

    if log_result.stdout.strip():
        commits = log_result.stdout.strip().split('\n')
        print(f"\n🆕 {len(commits)} Shared KB updates available:")
        print("Most recent changes:")
        for commit in commits[:5]:
            print(f"  {commit}")

        print(f"\n💡 Recommended: Update Shared KB")
        print("   cd docs/knowledge-base/shared && git pull")
```

**Result:** Agent automatically notified on session start!

### Solution D: Version Tracking File ⭐

**Add .kb-version file to track last update:**

```bash
# In shared-knowledge-base repo
echo "version: 3.1
commit: de93da6
date: 2026-01-06
entries: 87" > .kb-version
```

**In project:**
```python
# tools/kb.py
def get_kb_version():
    """Check local KB version"""

    version_file = get_shared_kb_dir() / ".kb-version"

    if version_file.exists():
        with version_file.open() as f:
            local_version = yaml.safe_load(f)
    else:
        local_version = {"commit": "unknown"}

    # Fetch remote version
    result = subprocess.run(
        ["gh", "api", "repos/ozand/shared-knowledge-base/commits/main"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        import json
        remote_commit = json.loads(result.stdout)["sha"]

        if local_version["commit"] != remote_commit:
            print(f"⚠️  KB update available!")
            print(f"   Local: {local_version['commit'][:7]}")
            print(f"   Remote: {remote_commit[:7]}")
            return True

    return False
```

---

## 🎯 Recommended Implementation

### Phase 1: Immediate (Pattern + Tool)

1. **Create KB-UPDATE-001 pattern**
   - Document update workflows (submodule vs clone)
   - Add recommended frequencies
   - Add troubleshooting

2. **Add `kb.py check-updates` command**
   - Check for new commits
   - Show commit summary
   - Provide update command

### Phase 2: Short-term (Integration)

1. **Update AGENT-AUTO-001 bootstrap**
   - Add `check_kb_updates()` call
   - Notify on session start
   - Non-blocking (doesn't fail update check)

2. **Add .kb-version tracking**
   - Commit to shared-knowledge-base repo
   - Track version, commit, date, entries count
   - Simple version comparison

### Phase 3: Long-term (Automation)

1. **Automatic update notifications**
   - GitHub Actions webhook
   - Email/Slack notifications
   - Project dashboard

2. **Smart update recommendations**
   - "Pattern X was added that matches your tech stack"
   - "3 new Python errors added since your last update"
   - Categorized notifications

3. **Update analytics**
   - Track which projects update frequently
   - Identify stale projects
   - Reminder notifications

---

## 📋 Implementation Priority

| Priority | Solution | Effort | Impact |
|----------|-----------|---------|--------|
| 🔴 HIGH | Solution B (check-updates command) | Low | High |
| 🟠 MEDIUM | Solution C (auto-check on bootstrap) | Medium | High |
| 🟡 LOW | Solution A (KB-UPDATE-001 pattern) | Low | Medium |
| 🟢 LOW | Solution D (version tracking) | Medium | Low |

**Recommended Start:** Solution B (check-updates command)

**Why:**
- Quick to implement (1-2 hours)
- Immediate value (agents can check)
- No breaking changes
- Can add to bootstrap later (Solution C)

---

## ✅ Success Criteria

After implementation:

- [ ] Agents can check: `python tools/kb.py check-updates`
- [ ] Agents notified on session start (if updates available)
- [ ] Clear update commands documented
- [ ] Update frequency recommendations provided
- [ ] Version tracking implemented (.kb-version)

**Target Outcome:**
- Agents aware of stale KB
- Simple update process
- Projects stay current with Shared KB
- Knowledge gap minimized

---

## 🎓 Key Insights

### Insight 1: Submodule vs Clone Trade-off

**Submodule:**
- Pros: Automatic updates
- Cons: Requires git init, complexity

**Plain Clone:**
- Pros: Simple setup
- Cons: Manual updates, NO notifications

**Decision:** Support both, add update tools

### Insight 2: Update Frequency Matters

**Active projects:** Weekly or before major work
**Maintenance projects:** Monthly
**Critical:** Before using critical patterns

**Default:** Check on every session start (non-blocking)

### Insight 3: Change Detection is Important

Agents need to know:
- WHAT changed (categories, counts)
- WHEN it changed (date)
- WHY it matters (relevance)

**Solution:** Commit summaries with categories

---

## 📊 Current State Assessment

| Mechanism | Exists? | Documented? | Automated? |
|-----------|----------|-------------|------------|
| Submodule update | ✅ Yes | ⚠️ Partial | ✅ Git native |
| Clone update | ✅ Git | ❌ No | ❌ Manual |
| Update check | ❌ No | ❌ No | ❌ No |
| Version tracking | ❌ No | ❌ No | ❌ No |
| Notifications | ❌ No | ❌ No | ❌ No |
| Bootstrap check | ❌ No | ❌ No | ❌ No |

**Overall:** ❌ 5/6 mechanisms missing

---

**Analysis Date:** 2026-01-06
**Analyst:** Shared KB Curator Agent
**Critical Gaps:** 5 mechanisms missing
**Recommendation:** Implement Solutions B + C (check-updates + auto-check)
**Priority:** 🔴 HIGH - Projects working with stale knowledge
