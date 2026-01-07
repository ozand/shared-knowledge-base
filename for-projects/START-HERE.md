# Shared KB: Agent Quick Start

**You are here because:** You're working in a project that uses Shared Knowledge Base

**📍 GitHub URL:** https://github.com/ozand/shared-knowledge-base/blob/main/for-projects/START-HERE.md

**📖 How to access:**
- If you see `@for-projects/START-HERE.md` → Read local file in `.kb/shared/`
- If you see a GitHub URL → Use WebFetch tool to read it
- If you're reading this → You're already in the right place!

**Choose your path:**

- **New Project?** → Go to **[Step 1: New Project Setup](#step-1-new-project-setup)**
- **Existing Project?** → Go to **[Step 2: Update Existing Project](#step-2-update-existing-project)**

---

## Step 1: New Project Setup

**Time:** 3 minutes | **Difficulty:** Easy

### 1.1. Add Shared KB Submodule

```bash
# Navigate to your project
cd your-project/

# Add Shared KB as submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared

# Initialize
git submodule update --init --recursive
```

### 1.2. Copy Tools & Hooks

```bash
# Copy KB tools
cp .kb/shared/tools/kb.py tools/
cp .kb/shared/tools/kb_domains.py tools/

# Copy hooks
mkdir -p .claude/hooks
cp .kb/shared/.claude/hooks/*.sh .claude/hooks/

# Copy commands (optional)
cp -r .kb/shared/for-projects/command-templates/* .claude/commands/
```

### 1.3. Build Index

```bash
python tools/kb.py index --force -v
```

### 1.4. Test

```bash
# Search KB
python tools/kb.py search "docker"

# List domains
python tools/kb_domains.py list
```

**✅ Done!** Your project now has Shared KB integrated.

**📚 Learn more:** `@for-projects/README.md`

---

## Step 2: Update Existing Project

**Time:** 2 minutes | **Difficulty:** Easy

### 2.1. Check for Updates

```bash
cd .kb/shared

# Current version
git describe --tags --abbrev=0

# Latest version
git fetch origin
git tag -l | sort -V | tail -n1
```

### 2.2. Update (if needed)

If latest > current:

```bash
# Pull updates
git pull origin main

# Go back to project root
cd ../..

# Rebuild index
python tools/kb.py index --force -v
```

### 2.3. Verify

```bash
# Should work without errors
python tools/kb_domains.py list

# Should show no errors
python tools/kb.py validate .kb/shared/
```

**✅ Done!** Your Shared KB is updated.

---

## ⚠️ Critical Rules

**🚨 3 Golden Rules:**

1. ⛔ **NEVER modify files in `.kb/shared/`** (read-only submodule)
2. ✅ **DATA is source of truth** (if tool breaks → tool has bug)
3. ❓ **When unsure** → ASK, don't fix

**Common Mistakes:**

- ❌ Modifying `_domain_index.yaml` in `.kb/shared/`
- ❌ Adding fields not in specification (token_estimate, tags, description)
- ❌ "Fixing" data format to make broken tool work
- ❌ Committing changes to `.kb/shared/` in your project

**If tool shows error:**
- ✅ Update tool from Shared KB
- ❌ DO NOT modify data format

---

## 🚨 Troubleshooting

### Problem: "TypeError: 'int' object is not subscriptable"

**Cause:** Old `kb_domains.py` doesn't support v4.0.0+ flat format

**Fix:**
```bash
cp .kb/shared/tools/kb_domains.py tools/kb_domains.py
```

**DO NOT:** Modify `_domain_index.yaml` to nested format

### Problem: ".kb/shared/ has uncommitted changes"

**Cause:** Accidental modification of submodule

**Fix:**
```bash
cd .kb/shared
git reset --hard HEAD
git checkout main
cd ../..
```

### Problem: Update shows conflicts

**Cause:** Local commits in submodule (shouldn't exist)

**Fix:**
```bash
cd .kb/shared
git fetch origin
git reset --hard origin/main
cd ../..
```

---

## 📖 Essential Documentation

**Must Read:**
1. **`@for-projects/AGENT-INSTRUCTIONS.md`** (~5 min) - Complete agent guide with decision trees
2. **`@for-projects/UPDATE-SHARED-KB.md`** (~5 min) - Detailed update instructions

**Reference:**
3. **`@.kb/shared/for-claude-code/AGENT-UPDATE-INSTRUCTIONS.md`** - Full instructions (600+ lines)
4. **`@.kb/shared/for-claude-code/KB-UPDATE-QUICK-REFERENCE.md`** - Quick reference card
5. **`@.kb/shared/docs/validation/DOMAIN-INDEX-SCHEMA.md`** - v4.0.0 format specification

---

## 🔍 Quick Diagnostic Commands

```bash
# Check Shared KB status
cd .kb/shared && git status && cd ../..

# Check current version
cd .kb/shared && git describe --tags && cd ../..

# Check for uncommitted changes (CRITICAL)
cd .kb/shared && git status --porcelain

# Test tools
python tools/kb_domains.py list
python tools/kb.py validate .
```

---

## 💡 Tips

1. **Auto-detection:** Every session start checks for updates automatically (via `session-setup.sh`)
2. **Version notification:** Check `@.kb/shared/.kb-version-notification.md` for latest updates
3. **Before updating:** Always read `.kb-version-notification.md` for critical changes
4. **After updating:** Always rebuild index: `python tools/kb.py index --force -v`

---

## 🆘 Need Help?

**Before modifying `.kb/shared/`:**
1. Read `@for-projects/AGENT-INSTRUCTIONS.md`
2. Check decision tree
3. Read troubleshooting section

**If you encounter bugs:**
- Report: https://github.com/ozand/shared-knowledge-base/issues
- Include: Shared KB version, tool version, error message, steps to reproduce

---

## 📦 Quick Commands

| Task | Command |
|------|---------|
| **Setup new project** | `git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared && git submodule update --init --recursive` |
| **Check version** | `cd .kb/shared && git describe --tags` |
| **Check updates** | `cd .kb/shared && git fetch && git log HEAD..origin/main --oneline` |
| **Update** | `cd .kb/shared && git pull origin main && cd ../.. && python tools/kb.py index --force -v` |
| **Rebuild index** | `python tools/kb.py index --force -v` |
| **Validate** | `python tools/kb.py validate .` |
| **Search** | `python tools/kb.py search "query"` |

---

**Version:** 4.0.1
**Last Updated:** 2026-01-08

**🎯 You should spend:** 3-10 minutes reading this
**📚 Then read:** `@for-projects/AGENT-INSTRUCTIONS.md` (complete guide)
