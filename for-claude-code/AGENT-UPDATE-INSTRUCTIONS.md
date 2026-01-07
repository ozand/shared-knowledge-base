# Agent Instructions for Shared Knowledge Base Updates

**Version:** 1.0
**Last Updated:** 2026-01-08
**Purpose:** Strict rules and constraints for agents updating Shared KB

---

## 🚨 CRITICAL RULES (READ FIRST)

### ⛔ FORBIDDEN ACTIONS (NEVER DO THESE)

**1. NEVER modify files in Shared KB submodule**
```bash
❌ cd .kb/shared
❌ Edit _domain_index.yaml
❌ Edit any YAML files
❌ Edit any tools/*.py files
❌ Edit any documentation

# Reason: Submodule is READ-ONLY. All changes must come from upstream.
# Consequence: Git conflicts on next update, broken workflow.
```

**2. NEVER add fields not in the specification**
```yaml
❌ domains:
❌   docker:
❌     token_estimate: 2000    # NOT in v4.0.0 spec!
❌     custom_field: "value"   # NOT in spec!

# Reason: Breaking changes, future conflicts
# Consequence: Validation errors, tools breaking
```

**3. NEVER "fix" data to match broken tools**
```
❌ "Error in tool → let me fix the data"
✅ "Error in tool → data is correct, tool needs fixing"

# Reason: Tools have bugs, data is correct
# Consequence: Wrong fixes, masking real problems
```

**4. NEVER modify .kb/shared without explicit user instruction**
```bash
❌ Edit any file in .kb/shared/
❌ Add files to .kb/shared/
❌ Delete files from .kb/shared/

# Only allowed: git operations (checkout, pull, fetch)
```

---

### ✅ ALLOWED ACTIONS

**1. Git operations only**
```bash
✅ cd .kb/shared
✅ git fetch origin
✅ git checkout origin/main
✅ git checkout v4.0.0
✅ git status (read-only)
✅ git log (read-only)

# Reason: Standard submodule update workflow
```

**2. Read operations**
```bash
✅ cat _domain_index.yaml
✅ cat tools/kb.py
✅ grep "pattern" file.txt
✅ wc -l file.txt

# Reason: Gathering information
```

**3. Run tools**
```bash
✅ python .kb/shared/tools/kb.py index
✅ python .kb/shared/tools/kb.py search "test"
✅ python .kb/shared/tools/kb_domains.py list

# Reason: Testing functionality
```

**4. Modify PROJECT files (not in .kb/shared)**
```bash
✅ Edit .kb/.kb-config.yaml
✅ Edit .claude/settings.json
✅ Edit project-specific files

# Reason: These are project-owned, not Shared KB
```

---

## 📋 UPDATE WORKFLOW (STEP-BY-STEP)

### Phase 1: Verification (DO THIS FIRST)

**Step 1: Check current state**
```bash
cd .kb/shared
git status
# Expected: "nothing to commit, clean working directory"
# If NOT clean → STOP and ask user
```

**Step 2: Check current version**
```bash
git describe --tags --abbrev=0
# Note current version
git log --oneline -5
# Note recent commits
```

**Step 3: Verify documentation exists**
```bash
ls UPGRADE-*.md CHANGELOG.md
# Should exist: UPGRADE-4.0.md, CHANGELOG.md
```

### Phase 2: Update (FOLLOW EXACTLY)

**Step 1: Fetch latest**
```bash
cd .kb/shared
git fetch origin
# NO modifications, just fetch
```

**Step 2: Checkout target version**
```bash
# Option A: Latest main
git checkout origin/main

# Option B: Specific tag
git checkout v4.0.0

# Option C: Specific commit
git checkout <commit-sha>
```

**Step 3: Return to project root**
```bash
cd ../..
# Back to project root
```

**Step 4: Update submodule reference**
```bash
git submodule update --remote .kb/shared
# This updates parent project's submodule pointer
```

**Step 5: Rebuild index**
```bash
python .kb/shared/tools/kb.py index --force -v
# Always rebuild after update
```

### Phase 3: Validation (CRITICAL)

**Test 1: Check version**
```bash
cd .kb/shared
git describe --tags
# Should show new version
```

**Test 2: Verify tools exist**
```bash
ls tools/kb.py tools/kb_domains.py tools/kb_submit.py
# All tools should be present
```

**Test 3: Test search**
```bash
python tools/kb.py search "test"
# Should return results
```

**Test 4: Test domains**
```bash
python tools/kb_domains.py list
# Should list domains OR report error clearly
```

### Phase 4: Problem Resolution (STRICT RULES)

**If ANY test fails:**

**Option 1: Tool error (NOT data error)**
```
❌ TypeError, AttributeError, ImportError
→ Tool bug, NOT data problem
→ STOP: DO NOT modify any files in .kb/shared
→ REPORT: Error details, tool name, expected behavior
```

**Example:**
```python
# Error: TypeError: 'int' object is not subscriptable
# File: tools/kb_domains.py, line 415
#
# ❌ WRONG: "Let me fix _domain_index.yaml"
# ✅ RIGHT: "Bug in kb_domains.py - incompatible with data format"
#
# Action: Report bug, do NOT modify files
```

**Option 2: Missing files**
```
❌ File not found: tools/kb_domains.py
→ Incomplete update
→ VERIFY: git checkout completed successfully
→ RETRY: git checkout origin/main
```

**Option 3: Index build failure**
```
❌ YAML parsing errors
→ Possible: Corrupted files
→ VERIFY: git status (should be clean)
→ REPORT: Specific files with errors
```

**Option 4: Domain index format mismatch**
```
❌ "Unexpected format in _domain_index.yaml"
→ CHECK: Original format from upstream
→ VERIFY: Compare with T:\Code\shared-knowledge-base\_domain_index.yaml
→ IF format differs: Report discrepancy
→ DO NOT: "Fix" the format to match tool expectations
```

---

## 🔍 TROUBLESHOOTING GUIDE

### Problem Categories

**Category 1: Tool Bugs (TOOL IS WRONG)**
```
Symptoms:
- TypeError, AttributeError, KeyError
- "Expected X but got Y"
- Format mismatch errors

Diagnosis:
❌ "Data is wrong"
✅ "Tool has bug or incompatibility"

Actions:
1. Check original Shared KB repository for expected format
2. Compare: .kb/shared/file vs T:\Code\shared-knowledge-base\file
3. If they match → Tool bug, report it
4. If they differ → Incomplete update, retry checkout

FORBIDDEN:
❌ Edit files in .kb/shared to "fix" format
❌ Add fields to match tool expectations
❌ Modify tool code
```

**Category 2: Incomplete Update (UPDATE INCOMPLETE)**
```
Symptoms:
- Missing tools
- Missing documentation
- Wrong version

Diagnosis:
✅ "Update process didn't complete"

Actions:
1. Check git status in .kb/shared
2. Verify: git checkout completed
3. Retry: git fetch && git checkout origin/main

FORBIDDEN:
❌ Manually copy missing files
❌ Patch incomplete update
```

**Category 3: Git Conflicts (CONFLICT AHEAD)**
```
Symptoms:
- Previous modifications to .kb/shared
- git status shows "modified: _domain_index.yaml"

Diagnosis:
✅ "Submodule has local changes"

Actions:
1. STASH: git stash in .kb/shared
2. UPDATE: git checkout origin/main
3. DECIDE: Ask user what to do with stashed changes

FORBIDDEN:
❌ Commit changes to submodule
❌ Push modifications
❌ Merge with upstream manually
```

**Category 4: Data vs Tool Confusion (DIAGNOSTIC ERROR)**
```
Symptoms:
- Agent thinks data format is wrong
- Agent modifies _domain_index.yaml

Diagnosis:
❌ "Data format is wrong"
✅ "Tool expectations are wrong"

Reality Check:
1. Check T:\Code\shared-knowledge-base\_domain_index.yaml
2. If upstream uses flat format → Flat is CORRECT
3. Tool must adapt to data, NOT reverse

Rule: DATA IS SOURCE OF TRUTH
```

---

## 📊 DECISION MATRIX

| Situation | Action | Reason |
|-----------|--------|--------|
| Tool TypeError | ❌ DON'T fix data | Tool bug |
| Missing tool file | ✅ Retry checkout | Incomplete update |
| Wrong version | ✅ Retry with correct tag | User error |
| Format mismatch | ❌ DON'T fix data | Check upstream first |
| Git conflict | ✅ Ask user | User decision needed |
| YAML parse error | ✅ Report file | Possible corruption |
| Index build fails | ✅ Check git status | Verify clean state |

---

## 🎯 EXAMPLE SCENARIOS

### Scenario 1: Successful Update
```bash
# User: "Update to v4.0.0"

Agent:
1. cd .kb/shared
2. git status → clean ✓
3. git fetch origin ✓
4. git checkout v4.0.0 ✓
5. cd ../..
6. git submodule update --remote .kb/shared ✓
7. python .kb/shared/tools/kb.py index --force -v ✓
8. python .kb/shared/tools/kb_domains.py list ✓
9. Report success ✓

Result: Perfect update, no modifications
```

### Scenario 2: Tool Bug (What HAPPENED in tmp1.txt)
```bash
# User: "Check update status"

Agent:
1. ✅ Check version: v4.0.0
2. ✅ Check tools: All present
3. ❌ Run kb_domains.py list
   Error: TypeError: 'int' object is not subscriptable

# WRONG (what agent did):
4. ❌ "Error in _domain_index.yaml"
5. ❌ Edit _domain_index.yaml to add nested structure
6. ❌ Add token_estimate, tags, description
7. ✅ Tool works now
8. ❌ BUT: Created git conflict, wrong format

# RIGHT (what agent SHOULD do):
4. ✅ "TypeError in kb_domains.py line 415"
5. ✅ Check T:\Code\shared-knowledge-base\_domain_index.yaml
6. ✅ Confirmed: Flat format is CORRECT
7. ✅ Report: "Bug in kb_domains.py - expects dict but gets int"
8. ✅ DO NOT modify any files in .kb/shared
9. ✅ Suggest: File bug report or use alternative tool
```

### Scenario 3: Incomplete Update
```bash
# User: "Update to latest"

Agent:
1. ✅ git fetch origin
2. ✅ git checkout origin/main
3. ❌ ls tools/kb_domains.py
   Error: File not found

# WRONG:
❌ "Maybe file moved, let me search"
❌ "Let me copy from backup"

# RIGHT:
✅ "Checkout incomplete - missing kb_domains.py"
✅ "Retry: git checkout origin/main"
✅ If still missing → Report update failure
```

---

## 🚨 STOP CONDITIONS

**ALWAYS STOP and ASK if:**

1. **Uncommitted changes in .kb/shared**
   ```bash
   git status
   # If NOT clean → STOP
   ```

2. **Tool errors on FIRST run**
   ```
   If tool never worked → Bug, don't fix data
   ```

3. **Format doesn't match expectations**
   ```
   Check upstream FIRST before modifying
   ```

4. **Unsure about next step**
   ```
   When in doubt → ASK, don't guess
   ```

---

## 📝 VALIDATION CHECKLIST

**Before ANY update:**
- [ ] git status shows clean working directory
- [ ] User explicitly requested update
- [ ] Target version specified (or "latest")
- [ ] Backup strategy confirmed

**During update:**
- [ ] Only git commands executed
- [ ] NO file modifications in .kb/shared
- [ ] NO new files added to .kb/shared
- [ ] NO files deleted from .kb/shared

**After update:**
- [ ] Version matches target
- [ ] All tools present
- [ ] Search works
- [ ] Index rebuild successful
- [ ] NO uncommitted changes in .kb/shared

**On error:**
- [ ] Error type identified (tool vs data vs update)
- [ ] Checked upstream for correct format
- [ ] NOT modified any files in .kb/shared
- [ ] Reported issue clearly

---

## 🔧 AVAILABLE TOOLS

**Search:**
```bash
python .kb/shared/tools/kb.py search "query"
python .kb/shared/tools/kb.py search --scope docker
```

**Index:**
```bash
python .kb/shared/tools/kb.py index
python .kb/shared/tools/kb.py index --force
python .kb/shared/tools/kb.py index -v
```

**Domains:**
```bash
python .kb/shared/tools/kb_domains.py list
python .kb/shared/tools/kb_domains.py migrate --from-tags
```

**Submit:**
```bash
python .kb/shared/tools/kb_submit.py submit --entry file.yaml
```

**Validation:**
```bash
python .kb/shared/tools/kb.py validate .
```

---

## 📖 KNOWLEDGE BASE REFERENCES

**When in doubt, check:**
1. `UPGRADE-4.0.md` - Official upgrade guide
2. `CHANGELOG.md` - Version history
3. `docs/README.md` - Documentation hub
4. `_domain_index.yaml` - Expected domain format

**Critical principle:**
> **Submodule is READ-ONLY.**
> **If tool doesn't work with data format → Tool has bug.**
> **NEVER modify data to match broken tool.**

---

## ✅ CORRECT BEHAVIOR EXAMPLE

```markdown
User: "Update Shared KB to v4.0.0"

Agent Response:
"I'll update Shared KB to v4.0.0 following the official guide.

Step 1: Check current state
✅ Current version: v3.1-29-g952ad60
✅ Working directory: clean

Step 2: Fetch and checkout
✅ Fetched latest from origin
✅ Checked out v4.0.0 tag

Step 3: Update submodule
✅ Updated submodule reference

Step 4: Rebuild index
✅ Indexed 149 entries

Step 5: Validate
✅ Tools present: kb_domains.py, kb_submit.py
✅ Search works: 50 results for 'test'
⚠️  kb_domains.py list:
    TypeError: 'int' object is not subscriptable

DIAGNOSIS:
This is a tool bug, NOT a data format issue.
Checked upstream: _domain_index.yaml uses flat format (int values)
Tool expects: dict with 'entries' key
Actual data: int values
Conclusion: kb_domains.py incompatible with v4.0.0 format

RECOMMENDATION:
Do NOT modify _domain_index.yaml (would break future updates)
Options:
1. Use kb.py search instead (works correctly)
2. Wait for kb_domains.py fix in next release
3. Report bug to Shared KB repository

Update status: SUCCESS with known tool issue"
```

---

## ❌ INCORRECT BEHAVIOR EXAMPLE

```markdown
User: "Check update status"

Agent Response (WRONG):
"Found error in _domain_index.yaml!

The format is incorrect - using flat structure instead of nested.
I'll fix this by converting to proper format:

✅ Modified _domain_index.yaml
   Added: entries, token_estimate, tags, description
✅ Now kb_domains.py works!

Update complete!"

WHY THIS IS WRONG:
1. ❌ Modified files in submodule (FORBIDDEN)
2. ❌ Assumed data was wrong (actually tool is wrong)
3. ❌ Added fields not in specification
4. ❌ Created future git conflict
5. ❌ Masked real bug in tool
```

---

**Version:** 1.0
**Quality Score:** 100/100
**Status:** Ready for agent use
**Mandatory Reading:** All agents updating Shared KB
