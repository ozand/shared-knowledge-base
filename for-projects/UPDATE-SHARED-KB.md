# How to Update Shared KB in Your Project

**For:** AI Agents working in projects that use Shared KB submodule
**Version:** 4.0.1+
**Last Updated:** 2026-01-08

---

## Quick Check: Do You Need to Update?

Run this command to check if your Shared KB is outdated:

```bash
cd .kb/shared
git log -1 --format="%H %s"
cd ../..
```

Compare with latest version: https://github.com/ozand/shared-knowledge-base/releases

---

## Update Instructions

### Option 1: Standard Update (Recommended)

```bash
# Navigate to submodule
cd .kb/shared

# Fetch latest changes
git fetch origin

# Check what's new (OPTIONAL)
git log HEAD..origin/main --oneline

# Update to latest version
git pull origin main

# Return to project root
cd ../..
```

### Option 2: Update to Specific Version

```bash
cd .kb/shared

# List available tags
git tag -l

# Checkout specific version
git checkout v4.0.1

cd ../..
```

### Option 3: Reset to Latest (If You Have Local Changes)

⚠️ **WARNING:** This will discard any local modifications to `.kb/shared/`

```bash
cd .kb/shared

# Reset to latest main
git fetch origin
git reset --hard origin/main

cd ../..
```

---

## After Update: Required Steps

### 1. Rebuild Index

```bash
python tools/kb.py index --force -v
```

### 2. Validate Entries

```bash
python tools/kb.py validate .
```

### 3. Check Domain Index

```bash
python tools/kb_domains.py list
```

---

## ⚠️ Critical Rules

**🚨 NEVER DO THIS:**
- ❌ Modify files in `.kb/shared/` directly
- ❌ Add fields not in Shared KB specification
- ❌ "Fix" data format - if tool breaks, tool has bug
- ❌ Commit changes to `.kb/shared/` in your project

**✅ INSTEAD:**
- ✅ Report issues to Shared KB repository
- ✅ Fix tool to match data format
- ✅ Keep `.kb/shared/` read-only
- ✅ Pull updates from upstream

---

## Troubleshooting

### Problem: "TypeError: 'int' object is not subscriptable"

**Cause:** Using Shared KB v4.0.0+ with old `kb_domains.py`

**Solution:** Update your project's tools:
```bash
# Check Shared KB version
cd .kb/shared && git describe --tags

# If v4.0.0+: update tools/kb_domains.py from Shared KB
cp .kb/shared/../tools/kb_domains.py tools/kb_domains.py
```

### Problem: "Validation failed"

**Cause:** Data format mismatch

**Solution:**
```bash
# DO NOT modify data in .kb/shared/
# INSTEAD: check if tool needs update
python tools/kb.py --version

# If tool is old: update tool, not data
```

### Problem: Git shows "diverged branches"

**Cause:** Local commits in submodule (shouldn't happen)

**Solution:**
```bash
cd .kb/shared
git status
# If you see uncommitted changes: DISCARD THEM
git reset --hard HEAD
git checkout main
git pull origin main
```

---

## Version-Specific Notes

### v4.0.1 (2026-01-08)

**Impact:** Fixed `kb_domains.py` compatibility with flat domain format

**Action Required:**
1. Update `.kb/shared/` to v4.0.1
2. Run `python tools/kb.py index --force -v`
3. Test: `python tools/kb_domains.py list`

**Files Changed:**
- `tools/kb_domains.py` - Now handles flat format (int) and nested format (dict)
- `.claude/CLAUDE.md` - Added agent instructions
- `docs/UPGRADE-4.0.md` - Added "For Agents" section

### v4.0.0 (2026-01-07)

**Impact:** New flat domain index format

**Action Required:**
1. Rebuild index: `python tools/kb.py index --force`
2. Validate entries: `python tools/kb.py validate .`

---

## Detection Script

Add this to your project's `.claude/hooks/session-setup.sh`:

```bash
#!/bin/bash

# Check if Shared KB needs update
cd .kb/shared
LATEST=$(git ls-remote --tags origin | grep -v '{}' | cut -f2 | sort -V | tail -n1 | sed 's/refs\/tags\//')
CURRENT=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")

if [ "$LATEST" != "$CURRENT" ]; then
    echo "⚠️  Shared KB update available: $CURRENT → $LATEST"
    echo "   Run: cd .kb/shared && git pull origin main"
    echo "   Then: python tools/kb.py index --force -v"
fi

cd ../..
```

---

## Feedback

If you encounter issues after updating Shared KB:

1. **DO NOT modify `.kb/shared/` files**
2. Check if tool needs update (not data)
3. Report issue: https://github.com/ozand/shared-knowledge-base/issues

---

## Reference

- **Shared KB Repository:** https://github.com/ozand/shared-knowledge-base
- **Agent Instructions:** `@for-claude-code/AGENT-UPDATE-INSTRUCTIONS.md`
- **Quick Reference:** `@for-claude-code/KB-UPDATE-QUICK-REFERENCE.md`
- **Changelog:** `@CHANGELOG.md`
