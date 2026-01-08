# 🚨 Shared KB Update Notification

**Current Version:** 4.0.1 | **Release Date:** 2026-01-08

---

## ⚡ Quick Actions

### If You're Setting Up New Project:

```bash
# 1. Add submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared

# 2. Copy tools
cp .kb/shared/tools/kb.py tools/
cp .kb/shared/tools/kb_domains.py tools/

# 3. Build index
python tools/kb.py index -v
```

**Full guide:** `@for-projects/START-HERE.md` (Step 1)

---

### If You're Updating Existing Project:

```bash
# 1. Update submodule
cd .kb/shared && git pull origin main && cd ../..

# 2. Rebuild index
python tools/kb.py index -v

# 3. Verify
python tools/kb_domains.py --kb-dir .kb/shared list
```

**Full guide:** `@for-projects/START-HERE.md` (Step 2)

---

## 🆕 What's New in v4.0.1

**Hotfix:** Fixed `kb_domains.py` compatibility + agent instructions

### Fixed
- ✅ `kb_domains.py` now handles flat domain format (v4.0.0 standard)
- ✅ Compatible with both flat (int) and nested (dict) formats
- ✅ Windows compatibility: removed `$CLAUDE_PROJECT_DIR` from hooks

### Added
- 📚 Complete agent instructions (1,500+ lines)
- 📚 Automatic update detection script
- 📚 Validation tests for domain index

**Critical:** If you had "TypeError: 'int' object is not subscriptable" - this fixes it!

---

## ⚠️ Critical Rules (Updated for v4.0.1)

**🚨 3 Golden Rules:**

1. ⛔ **NEVER modify files in `.kb/shared/`** (submodule is read-only)
2. ✅ **DATA is source of truth** (if tool breaks → tool has bug)
3. ❓ **When unsure** → ASK, don't fix

**🚨 Common Mistake (DON'T DO THIS):**
- ❌ Modifying `_domain_index.yaml` to add `token_estimate`, `tags`, `description`
- ✅ v4.0.0 format is `{domain: 11}` (flat, int)
- ✅ If tool fails → update tool, NOT data

---

## 🔧 If Tool Shows Error After Update

### Error: "TypeError: 'int' object is not subscriptable"

**Diagnosis:**
```bash
# Check format
python -c "import yaml; print(yaml.safe_load(open('.kb/shared/_domain_index.yaml')))"
```

**If output is `{"domains": {"docker": 11}}`:**
- ✅ Data is CORRECT (v4.0.0 flat format)
- ❌ Tool is buggy (expects nested format)
- ✅ Fix: `cp .kb/shared/tools/kb_domains.py tools/kb_domains.py`

**DO NOT:**
- ❌ Modify `_domain_index.yaml`
- ❌ Add fields like `token_estimate`, `tags`

---

## 📖 Must Read Documentation

**Essential (5-10 min):**
1. **`@for-projects/START-HERE.md`** - Single entry point (NEW or UPDATE)
2. **`@for-projects/AGENT-INSTRUCTIONS.md`** - Complete agent guide

**Reference:**
3. **`@.kb/shared/for-claude-code/AGENT-UPDATE-INSTRUCTIONS.md`** - Full instructions
4. **`@.kb/shared/for-claude-code/KB-UPDATE-QUICK-REFERENCE.md`** - Quick reference

---

## 🔗 Links

- **Repository:** https://github.com/ozand/shared-knowledge-base
- **This version:** https://github.com/ozand/shared-knowledge-base/releases/tag/v4.0.1
- **Issues:** https://github.com/ozand/shared-knowledge-base/issues
- **Full Changelog:** `@.kb/shared/CHANGELOG.md`

---

## 🎯 Next Steps

1. ✅ Read `@for-projects/START-HERE.md` (choose: New or Existing project)
2. ✅ Follow the steps
3. ✅ Read `@for-projects/AGENT-INSTRUCTIONS.md` for complete guide
4. ✅ Bookmark: `@for-projects/START-HERE.md` for future reference

---

**Auto-updated:** This file is updated with each release
**Last Check:** 2026-01-08
