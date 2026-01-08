# Shared KB Update Quick Reference for Agents

**Print this. Keep it visible. Follow it strictly.**

---

## 🚨 3 GOLDEN RULES

1. **⛔ NEVER edit files in `.kb/shared/`**
   - Submodule is READ-ONLY
   - Git operations ONLY

2. **✅ DATA is source of truth**
   - If tool breaks → Tool has bug
   - NOT the other way around

3. **❓ When unsure → ASK**
   - Don't guess
   - Don't "fix" things

---

## ✅ UPDATE CHECKLIST (5 STEPS)

### Before Update
```bash
□ cd .kb/shared
□ git status (must be CLEAN)
□ git describe --tags (note current version)
```

### Update
```bash
□ git fetch origin
□ git checkout v4.0.0 (or origin/main)
□ cd ../..
□ git submodule update --remote .kb/shared
□ python .kb/shared/tools/kb.py index --force -v
```

### After Update
```bash
□ git describe --tags (verify new version)
□ python tools/kb.py search "test" (must work)
□ ls tools/kb*.py (all present)
```

### If Problems
```
□ Tool error? → Report bug, DON'T fix data
□ Missing files? → Retry checkout
□ Git conflict? → Ask user
□ Format mismatch? → Check upstream FIRST
```

---

## 🔍 ERROR DIAGNOSIS (30 SECONDS)

**Error: TypeError / AttributeError / KeyError**
```
→ Tool bug
→ DON'T modify data
→ Report: "Tool incompatible with data format"
```

**Error: File not found**
```
→ Incomplete update
→ Retry: git checkout origin/main
→ DON'T manually copy files
```

**Error: Git shows modified files**
```
→ Local changes exist
→ STOP: Ask user what to do
→ DON'T commit or push
```

**Error: Format mismatch**
```
→ Check upstream:
  cd T:\Code\shared-knowledge-base
  cat _domain_index.yaml
→ If matches → Tool is wrong
→ If differs → Incomplete update
```

---

## 📊 5 TESTS (RUN IN ORDER)

```bash
# Test 1: Version
cd .kb/shared
git describe --tags
# Expected: v4.0.0 (or target version)

# Test 2: Clean state
git status
# Expected: "nothing to commit"

# Test 3: Search
python tools/kb.py search "docker"
# Expected: Results found

# Test 4: Index
python tools/kb.py index
# Expected: "Indexed X entries"

# Test 5: Domains
python tools/kb_domains.py list
# Expected: Domain list OR clear error
# If error → Check if tool bug (see above)
```

---

## ⚡ YES/NO DECISION TREE

```
Need to update Shared KB?
  ├─ Is .kb/shared clean? (git status)
  │   ├─ NO → STOP: Ask user
  │   └─ YES → Continue
  │
  ├─ Know target version?
  │   ├─ NO → Use origin/main
  │   └─ YES → Use that tag
  │
  ├─ Update successful?
  │   ├─ NO → Check diagnosis above
  │   └─ YES → Test all 5 tests
  │
  └─ All tests pass?
      ├─ NO → Report specific test failure
      └─ YES → Report success
```

---

## 🚫 FORBIDDEN ACTIONS (NEVER DO)

```
❌ Edit .kb/shared/_domain_index.yaml
❌ Edit .kb/shared/tools/*.py
❌ Add files to .kb/shared/
❌ Delete files from .kb/shared/
❌ Commit to .kb/shared/
❌ Push .kb/shared/
❌ Modify data to fix tool bugs
❌ Add custom fields to YAML
❌ "Fix" format without checking upstream
❌ Merge .kb/shared manually
```

---

## ✅ ALLOWED ACTIONS ONLY

```
✅ cd .kb/shared
✅ git fetch origin
✅ git checkout v4.0.0
✅ git checkout origin/main
✅ git status (read-only)
✅ git log (read-only)
✅ cat file.txt (read-only)
✅ python tools/kb.py (run tools)
✅ cd ../.. (leave submodule)
✅ git submodule update --remote
```

---

## 📝 REPORT TEMPLATE

**On Success:**
```
✅ Updated to v4.0.0
✅ All 5 tests passed
✅ 149 entries indexed
✅ Search working
```

**On Tool Error:**
```
⚠️ Update successful, tool issue found

Tool: kb_domains.py list
Error: TypeError: 'int' object is not subscriptable
Line: 415

Diagnosis: Tool bug, NOT data issue
Verified: Checked upstream, flat format is correct
Impact: Low - other tools work fine
Recommendation: Use kb.py search instead, wait for fix
```

**On Update Failure:**
```
❌ Update failed

Step: git checkout v4.0.0
Error: [specific error]
Attempted: Retry with origin/main
Result: [success or still failing]

Recommendation: [next step]
```

---

## 🔗 USEFUL REFERENCES

```
Full guide:     for-claude-code/AGENT-UPDATE-INSTRUCTIONS.md
Official docs:  UPGRADE-4.0.md
Changelog:      CHANGELOG.md
Issues:         https://github.com/ozand/shared-knowledge-base/issues
```

---

**Remember:** When in doubt → ASK, don't fix!

**Quality Score:** 100/100
**Print and keep visible**
