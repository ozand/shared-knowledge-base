# Agent Prompt Template

**Copy and paste this to agent when setting up Shared KB:**

---

## 📦 Setup Shared Knowledge Base

Your project uses Shared Knowledge Base - a centralized collection of verified solutions for common errors.

### What You Need to Do:

**Choose ONE:**

**A) New Project Setup (first time):**
```bash
# 1. Add submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared

# 2. Copy tools
cp .kb/shared/tools/kb.py tools/
cp .kb/shared/tools/kb_domains.py tools/

# 3. Copy hooks
mkdir -p .claude/hooks
cp .kb/shared/.claude/hooks/*.sh .claude/hooks/

# 4. Build index
python tools/kb.py index --force -v
```

**B) Update Existing Project:**
```bash
# 1. Update submodule
cd .kb/shared && git pull origin main && cd ../..

# 2. Rebuild index
python tools/kb.py index --force -v

# 3. Verify
python tools/kb_domains.py list
```

### ⚠️ Critical Rules:

1. ⛔ **NEVER modify files in `.kb/shared/`** (read-only submodule)
2. ✅ **DATA is source of truth** (if tool breaks → tool has bug)
3. ❓ **When unsure** → Read documentation below

### 📖 Full Documentation:

https://github.com/ozand/shared-knowledge-base/blob/main/for-projects/START-HERE.md

### 🆘 Troubleshooting:

**Error: "TypeError: 'int' object is not subscriptable"**
```bash
# Fix: Update tool from Shared KB
cp .kb/shared/tools/kb_domains.py tools/kb_domains.py
```

**DO NOT modify `_domain_index.yaml` format**

---

**That's it!** Ask if you have questions.
