# Quick Setup: Shared KB for Claude Code
## 5-Minute Installation Guide (Sparse Checkout)

**For:** Claude Code AI Agent
**Platform:** Linux/Mac/Windows
**Goal:** Install Shared KB with ONLY Project Agent content

---

## 🚀 Quick Installation (One Command)

### Linux/Mac:

```bash
cd /path/to/your/project && \
git clone https://github.com/ozand/shared-knowledge-base.git /tmp/shared-kb-setup && \
bash /tmp/shared-kb-setup/scripts/setup-shared-kb-sparse.sh && \
rm -rf /tmp/shared-kb-setup
```

### Windows (PowerShell):

```powershell
cd C:\path\to\your\project
git clone https://github.com/ozand/shared-knowledge-base.git C:\temp\shared-kb-setup
powershell -ExecutionPolicy Bypass -File C:\temp\shared-kb-setup\scripts\setup-shared-kb-sparse.ps1
Remove-Item -Recurse -Force C:\temp\shared-kb-setup
```

---

## ✅ Verify Installation

```bash
# 1. Check submodule status
git submodule status docs/knowledge-base/shared
# Expected:  c023036... (leading space = good)

# 2. Verify curator/ is NOT loaded
ls docs/knowledge-base/shared/curator/
# Expected: "No such file or directory" ✅

# 3. Verify patterns ARE loaded
ls docs/knowledge-base/shared/universal/patterns/
# Expected: List of .yaml files ✅

# 4. Build search index
python docs/knowledge-base/shared/tools/kb.py index -v
# Expected: "Indexed: 95 entries"

# 5. Test search
python docs/knowledge-base/shared/tools/kb.py search "async"
# Expected: Search results ✅
```

---

## 📖 What You Get

### ✅ Loaded (Project Agent):
- **Patterns:** universal/, python/, postgresql/, docker/, javascript/
- **Documentation:** README.md, AGENT-QUICK-START.md, agent guides
- **Tools:** tools/kb.py, scripts/
- **Agent Instructions:** universal/agent-instructions/base-instructions.yaml

### ❌ Excluded (Curator):
- **Curator docs:** curator/ (entire directory)
- **Analysis:** *_ANALYSIS.md, *_REPORT.md, CHAT_*.md
- **Generated:** .agent-config.local, _index*.yaml

---

## 🎯 Daily Commands

```bash
# Update Shared KB
git submodule update --remote docs/knowledge-base/shared

# Search knowledge
python docs/knowledge-base/shared/tools/kb.py search "keyword"

# Check for updates
python docs/knowledge-base/shared/tools/kb.py check-updates
```

---

## ⚠️ Critical Rules

### ✅ Always:
```bash
git submodule status docs/knowledge-base/shared
git submodule update --remote docs/knowledge-base/shared
```

### ❌ Never:
```bash
git -C docs/knowledge-base/shared fetch  # WRONG
cd docs/knowledge-base/shared && git pull  # WRONG
```

---

## 📚 Full Documentation

- **Complete Guide:** [SETUP_GUIDE_FOR_CLAUDE.md](SETUP_GUIDE_FOR_CLAUDE.md)
- **Agent Quick Start:** [AGENT-QUICK-START.md](docs/knowledge-base/shared/AGENT-QUICK-START.md)
- **Setup Details:** [QUICKSTART.md](docs/knowledge-base/shared/QUICKSTART.md)

---

**Done!** 🎉 Shared KB is ready for use in ~5 minutes.

**Need help?** See [SETUP_GUIDE_FOR_CLAUDE.md](SETUP_GUIDE_FOR_CLAUDE.md) for troubleshooting.
