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

**IMPORTANT:** If PowerShell script shows encoding errors, use manual commands below.

---

## ✅ Verify Installation

```bash
# 1. Check submodule status
git submodule status docs/knowledge-base/shared
# Expected:  c023036... (leading space = good)

# 2. Verify curator/ is NOT loaded
ls docs/knowledge-base/shared/curator/
# Expected: "No such file or directory" [OK]

# 3. Verify patterns ARE loaded
ls docs/knowledge-base/shared/universal/patterns/
# Expected: List of .yaml files [OK]

# 4. Build search index
python docs/knowledge-base/shared/tools/kb.py index -v
# Expected: "Indexed: 95 entries"

# 5. Test search
python docs/knowledge-base/shared/tools/kb.py search "async"
# Expected: Search results [OK]
```

---

## 📖 What You Get

### [OK] Loaded (Project Agent):
- **Patterns:** universal/, python/, postgresql/, docker/, javascript/
- **Documentation:** README.md, AGENT-QUICK-START.md, agent guides
- **Tools:** tools/kb.py, scripts/
- **Agent Instructions:** universal/agent-instructions/base-instructions.yaml

### [X] Excluded (Curator):
- **Curator docs:** curator/ (entire directory)
- **Analysis:** *_ANALYSIS.md, *_REPORT.md, CHAT_*.md
- **Generated:** .agent-config.local, _index*.yaml

---

## 🛠️ Daily Commands

```bash
# Update Shared KB
git submodule update --remote docs/knowledge-base/shared

# Search knowledge
python docs/knowledge-base/shared/tools/kb.py search "keyword"

# Check for updates
python docs/knowledge-base/shared/tools/kb.py check-updates
```

---

## 🔄 Troubleshooting

### Problem: PowerShell Script Shows Encoding Errors

**Symptoms:**
- `[X]` or `???` instead of boxes
- "Missing argument in parameter list" errors

**Solution:** Use manual commands

```powershell
cd C:\path\to\your\project

# Add submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base/shared

# Enable sparse checkout
cd docs/knowledge-base/shared
git config core.sparsecheckout true

# Create sparse checkout file
mkdir .git\info
cat > .git\info\sparse-checkout <<'EOF'
README.md
GUIDE.md
QUICKSTART.md
universal/
python/
postgresql/
docker/
javascript/
tools/
scripts/
EOF

# Checkout
git read-tree -mu HEAD
cd ..\..\..

# Verify
python docs\knowledge-base\shared\tools\kb.py index -v
```

### Problem: SKU CLI Installation Fails

**Symptoms:**
- `sku: command not found`
- Encoding errors in installer
- `pip install sku-cli` fails

**Solution:** Use kb.py directly (no SKU CLI needed!)

```bash
# kb.py works standalone
python docs/knowledge-base/shared/tools/kb.py search "keyword"

# Build index
python docs/knowledge-base/shared/tools/kb.py index -v

# Check stats
python docs/knowledge-base/shared/tools/kb.py stats
```

**Note:** SKU CLI is OPTIONAL. kb.py provides all core functionality.

---

## ⚠️ Critical Rules

### [OK] Always:
```bash
git submodule status docs/knowledge-base/shared
git submodule update --remote docs/knowledge-base/shared
```

### [X] Never:
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

**Done!** [OK] Shared KB is ready for use in ~5 minutes.

**Need help?** See [SETUP_GUIDE_FOR_CLAUDE.md](SETUP_GUIDE_FOR_CLAUDE.md) for troubleshooting.

---

## Appendix: kb.py Command Reference

```bash
# Search
python docs/knowledge-base/shared/tools/kb.py search "async"
python docs/knowledge-base/shared/tools/kb.py search --category python "websocket"

# Index
python docs/knowledge-base/shared/tools/kb.py index
python docs/knowledge-base/shared/tools/kb.py index --force

# Stats
python docs/knowledge-base/shared/tools/kb.py stats

# Validate
python docs/knowledge-base/shared/tools/kb.py validate path/to/file.yaml

# Export
python docs/knowledge-base/shared/tools/kb.py export --format json --output kb.json

# Check updates
python docs/knowledge-base/shared/tools/kb.py check-updates
```

**All kb.py commands work without SKU CLI!**
