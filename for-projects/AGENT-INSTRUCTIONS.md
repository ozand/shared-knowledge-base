# Agent Instructions: Shared KB Updates

**Purpose:** Critical instructions for AI agents working in projects that use Shared KB submodule

**Version:** 4.0.1+
**Last Updated:** 2026-01-08

---

## 🚨 3 Golden Rules

When working with Shared KB (`.kb/shared/`):

1. ⛔ **NEVER modify files in `.kb/shared/`** - submodule is read-only
2. ✅ **DATA is source of truth** - if tool breaks → tool has bug
3. ❓ **When unsure** → ASK, don't fix

---

## Quick Decision Tree

```
User asks to update Shared KB
│
├─ Is user asking to add/modify KB entries?
│  ├─ YES → Check scope
│  │       ├─ Universal (docker, postgresql, etc.)?
│  │       │  YES → Do NOT modify .kb/shared/
│  │       │        → Report to Shared KB repo
│  │       │
│  │       └─ Project-specific?
│  │          YES → Add to local KB/ (not .kb/shared/)
│  │
│  └─ NO → Continue below
│
├─ Is user asking to update Shared KB to latest version?
│  ├─ YES → Follow update steps
│  │
│  └─ NO → Continue below
│
└─ Tool shows error with .kb/shared/ data?
   ├─ Check: Is data format correct per spec?
   │  YES → Tool has bug → Fix tool
   │  NO  → Report data issue
   │
   └─ NEVER "fix" data format to make tool work
```

---

## Update Workflow

### When User Asks to Update Shared KB

**Step 1: Check Current Version**
```bash
cd .kb/shared
git describe --tags --abbrev=0
cd ../..
```

**Step 2: Check Latest Version**
```bash
cd .kb/shared
git fetch origin
git tag -l | sort -V | tail -n1
cd ../..
```

**Step 3: Update (if newer available)**
```bash
cd .kb/shared
git pull origin main
cd ../..
```

**Step 4: Rebuild Index**
```bash
python tools/kb.py index --force -v
```

**Step 5: Validate**
```bash
python tools/kb.py validate .
```

---

## Common Scenarios

### Scenario 1: Tool Error After Update

**Symptom:** `TypeError: 'int' object is not subscriptable` in `kb_domains.py`

**Diagnosis:**
```bash
# Check data format
python -c "import yaml; print(yaml.safe_load(open('_domain_index.yaml')))"

# If format is {docker: 11} (flat, int) → Data is CORRECT
# If format is {docker: {entries: 11}} (nested) → Data is WRONG
```

**Solution:**
- ✅ Update `tools/kb_domains.py` to handle flat format
- ❌ DO NOT modify `_domain_index.yaml` to nested format

**Real Example:**
```python
# BEFORE (buggy - expects nested)
for domain_name, data in sorted(index.get('domains', {}).items(),
                               key=lambda x: x[1]['entries'], reverse=True):
    print(f"  {domain_name:20} {data['entries']:3} entries")

# AFTER (fixed - handles both)
for domain_name, data in sorted(index.get('domains', {}).items(),
                               key=lambda x: x[1] if isinstance(x[1], int) else x[1].get('entries', 0),
                               reverse=True):
    entry_count = data if isinstance(data, int) else data.get('entries', 0)
    print(f"  {domain_name:20} {entry_count:3} entries")
```

### Scenario 2: User Wants to Add KB Entry

**Check Scope:**

1. **Universal scope** (docker, postgresql, python, javascript, universal):
   - ❌ DO NOT add to `.kb/shared/`
   - ✅ Report to Shared KB repository
   - ✅ Include: error, solution, code example

2. **Project scope** (framework, business logic, environment-specific):
   - ✅ Add to local KB (e.g., `universal/` in project root)
   - ✅ Mark as `local_only: true`
   - ✅ Commit to project repository

### Scenario 3: Validation Fails After Update

**Symptom:** `python tools/kb.py validate .` shows errors

**Diagnosis:**
```bash
# Check if error is in .kb/shared/ or local KB
python tools/kb.py validate .kb/shared/
python tools/kb.py validate universal/
```

**Solution:**
- If error in `.kb/shared/`:
  - ❌ DO NOT modify `.kb/shared/` files
  - ✅ Report to Shared KB repository with details

- If error in local KB:
  - ✅ Fix validation errors in local KB files
  - ✅ Re-run validation

---

## Diagnostic Commands

### Check Shared KB Status

```bash
cd .kb/shared

# Current version
git describe --tags --abbrev=0

# Current branch
git rev-parse --abbrev-ref HEAD

# Uncommitted changes (should be NONE)
git status --porcelain

# Latest available version
git fetch origin
git tag -l | sort -V | tail -n1

# Compare with latest
git log --oneline HEAD..origin/main | head -n5
```

### Check Data Format

```bash
# Domain index format
python -c "import yaml; import json; print(json.dumps(yaml.safe_load(open('.kb/shared/_domain_index.yaml')), indent=2))"

# Should show:
# {"domains": {"docker": 11, "universal": 8, ...}}
# NOT:
# {"domains": {"docker": {"entries": 11, ...}}}
```

### Check Tool Compatibility

```bash
# KB tool version
python tools/kb.py --version

# kb_domains.py compatibility
python tools/kb_domains.py list
# Should work without errors
```

---

## Red Flags 🚩

**STOP if you see:**

1. Uncommitted changes in `.kb/shared/`
   ```bash
   cd .kb/shared && git status --porcelain
   # If output is not empty → DO NOT commit
   ```

2. Modified `_domain_index.yaml` in `.kb/shared/`
   - This should NEVER be modified in submodule
   - If tool fails → tool has bug

3. Added fields not in specification
   - v4.0.0 spec: `domain: int` (flat format)
   - If you added `token_estimate`, `tags`, `description` → WRONG
   - Revert changes

4. Commit to `.kb/shared/` in project repo
   - This creates git conflict
   - Submodule should point to Shared KB commit only

---

## Reporting Issues

When reporting to Shared KB repository:

**Include:**
1. Shared KB version (`git describe --tags` in `.kb/shared/`)
2. Tool version (`python tools/kb.py --version`)
3. Full error message
4. Steps to reproduce
5. Expected vs actual behavior

**Example Report:**
```markdown
## Issue: kb_domains.py fails with flat domain format

**Shared KB Version:** v4.0.0
**Tool Version:** kb.py 4.0.0
**OS:** Windows 10

**Error:**
```
TypeError: 'int' object is not subscriptable
File "tools/kb_domains.py", line 415, in list_domains
```

**Steps:**
1. Updated `.kb/shared/` to v4.0.0
2. Ran: `python tools/kb_domains.py list`
3. Error occurred

**Expected:** List domains with entry counts
**Actual:** TypeError

**Analysis:**
- _domain_index.yaml uses flat format: `{docker: 11}`
- Tool expects nested format: `{docker: {entries: 11}}`
- Tool needs update to handle flat format
```

---

## Validation Checklist

Before completing any Shared KB update:

- [ ] Checked current version in `.kb/shared/`
- [ ] Checked latest version available
- [ ] Updated via `git pull origin main` (if needed)
- [ ] Rebuilt index: `python tools/kb.py index --force -v`
- [ ] Validated entries: `python tools/kb.py validate .`
- [ ] Tested tools work: `python tools/kb_domains.py list`
- [ ] NO modifications to `.kb/shared/` files
- [ ] NO uncommitted changes in `.kb/shared/`
- [ ] `.kb/shared/` on `main` branch
- [ ] If error: diagnosed tool bug vs data issue correctly

---

## Quick Reference

| Task | Command | Notes |
|------|---------|-------|
| Check version | `cd .kb/shared && git describe --tags` | Shows current version |
| Check updates | `cd .kb/shared && git fetch && git log HEAD..origin/main --oneline` | Shows available updates |
| Update | `cd .kb/shared && git pull origin main && cd ../..` | Pulls latest changes |
| Rebuild index | `python tools/kb.py index --force -v` | Required after update |
| Validate | `python tools/kb.py validate .` | Check entry quality |
| Check status | `cd .kb/shared && git status` | Should be clean |

---

## Full Documentation

- **Complete Guide:** `@.kb/shared/for-claude-code/AGENT-UPDATE-INSTRUCTIONS.md`
- **Quick Reference:** `@.kb/shared/for-claude-code/KB-UPDATE-QUICK-REFERENCE.md`
- **Update Instructions:** `@for-projects/UPDATE-SHARED-KB.md`
- **Format Spec:** `@.kb/shared/docs/validation/DOMAIN-INDEX-SCHEMA.md`

---

**Version:** 4.0.1
**Last Updated:** 2026-01-08
