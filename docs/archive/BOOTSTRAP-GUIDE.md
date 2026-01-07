# Bootstrap Guide: Enterprise Knowledge Graph
## Setting up New Projects and Updating Existing Ones

**Version:** 1.0.0
**Last Updated:** 2026-01-07

---

## ⚠️ DEPRECATION NOTICE

**This document describes the OLD SKU CLI installation method.**

**Status:** DEPRECATED (2026-01-07)

**Why Deprecated:**
- SKU CLI is not published to PyPI
- Installation requires manual steps
- Not cross-platform (encoding issues on Windows)
- No longer recommended for new projects

**✅ RECOMMENDED:** Use **unified-install.py** instead:

```bash
# For new projects (one command)
python scripts/unified-install.py --full

# Or remote download
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/unified-install.py | python3 - --full
```

**See:**
- **[README.md](README.md)** - Updated Quick Start with unified installation
- **[HARMONIZED-INSTALLATION-GUIDE.md](HARMONIZED-INSTALLATION-GUIDE.md)** - Complete guide
- **[UNIFIED-INSTALL-001](universal/patterns/unified-installation-001.yaml)** - Pattern reference

**Migration:**
- If you're using SKU CLI, see [HARMONIZED-INSTALLATION-GUIDE.md](HARMONIZED-INSTALLATION-GUIDE.md) for migration guide
- For new projects, use unified-install.py directly

---

## 🎯 Problem Solved (Legacy Approach)

**The "Chicken and Egg" Problem:**
- New project needs SKU CLI to install artifacts
- But SKU CLI itself is an artifact that needs to be installed
- Existing projects need to update SKU CLI to get new features
- But how to update if update command is in the CLI itself?

**Solution:** Universal installer + self-update mechanism

---

## 📦 Quick Installation (One-Liner)

### For New Projects (No SKU CLI yet)

#### Linux/Mac:

```bash
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/install-sku.sh | bash
```

#### Windows (PowerShell):

```powershell
irm https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/install-sku.ps1 | iex
```

**What this does:**
1. Checks prerequisites (uv, Python)
2. Downloads SKU CLI files from GitHub
3. Installs to `~/.sku/bin/`
4. Adds to PATH
5. Downloads initial catalog (~10 KB)
6. Creates configuration files

**After installation:**
```bash
# Restart shell for PATH changes
source ~/.bashrc  # or ~/.zshrc

# Verify installation
sku --version

# Check system health
sku doctor
```

---

## 🚀 Setting Up New Projects

### Method 1: Automatic Initialization (Recommended)

```bash
cd /path/to/new-project

# Initialize with auto-detection
sku init

# Or with explicit type
sku init --type typescript --team backend-team
```

**What `sku init` does:**
1. Detects project type (package.json, pyproject.toml, etc.)
2. Creates `.claude/` directory structure
3. Creates `CLAUDE.md` with project context
4. Installs `check-artifact-updates.py` hook
5. Creates `.sku/config.yaml` with project settings
6. Creates `.skuignore` for exclusions

**Generated files:**
```
.claude/
├── CLAUDE.md              # Project-specific instructions
├── settings.json          # Claude Code configuration
└── hooks/
    └── check-artifact-updates.py  # Auto-update checker

.sku/
└── config.yaml            # SKU project config

.skuignore                 # What to exclude from publication
```

### Method 2: Manual Setup

```bash
cd /path/to/new-project

# 1. Create .claude directory
mkdir -p .claude/hooks

# 2. Create basic CLAUDE.md
cat > .claude/CLAUDE.md <<'EOF'
# My Project - Claude Code Instructions

**Project Type:** TypeScript
**Team:** backend-team

## Quick Start

```bash
uvx sku sync --index-only
uvx sku search --tag typescript
```

## Workflows

User: Generate tests for UserService
→ Claude uses installed testing skill
→ Follows project conventions
EOF

# 3. Create settings.json with update hook
cat > .claude/settings.json <<'EOF'
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python $CLAUDE_PROJECT_DIR/.claude/hooks/check-artifact-updates.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
EOF

# 4. Download update hook
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/.claude/hooks/check-artifact-updates.py \
  -o .claude/hooks/check-artifact-updates.py
chmod +x .claude/hooks/check-artifact-updates.py

# 5. Commit to git
git add .claude/
git commit -m "Initialize Enterprise Knowledge Graph"
```

---

## 🔄 Updating Existing Projects

### Scenario 1: Update SKU CLI

**Check for updates:**
```bash
sku self-update
```

**Output:**
```
SKU CLI Update Available
  Current: 1.0.0
  Latest:  1.1.0
  Type:    minor

Updating SKU CLI: 1.0.0 → 1.1.0
  Downloading: __init__.py
  Downloading: cli.py
  Downloading: init.py
  ...

  Installing new version...

✓ Updated SKU CLI to 1.1.0
```

**Auto-update policy:**
- **Patch** (1.0.0 → 1.0.1): Auto-update (bug fixes)
- **Minor** (1.0.0 → 1.1.0): Prompt (new features)
- **Major** (1.0.0 → 2.0.0): Warn + Prompt (breaking changes)

**Force update without prompt:**
```bash
sku self-update --auto-patch
```

### Scenario 2: Update Installed Artifacts

```bash
# Check what needs updating
sku check-updates

# Update all (smart: patches auto)
sku update --all

# Update specific artifact
sku update skill testing
```

### Scenario 3: Project Needs Update Hook

**For projects created before update hooks were added:**

```bash
# 1. Check if hook exists
ls .claude/hooks/check-artifact-updates.py

# 2. If not found, download it
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/.claude/hooks/check-artifact-updates.py \
  -o .claude/hooks/check-artifact-updates.py

# 3. Update settings.json
# Add to .claude/settings.json -> hooks -> SessionStart:
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python $CLAUDE_PROJECT_DIR/.claude/hooks/check-artifact-updates.py",
            "timeout": 30
          }
        ]
      }
    ]
  }
}

# 4. Restart Claude Code to see effect
```

---

## 🔧 Troubleshooting

### Problem: SKU command not found

**Symptoms:**
```bash
sku: command not found
```

**Diagnosis:**
```bash
sku doctor
```

**Solutions:**

1. **Restart shell:**
```bash
source ~/.bashrc  # or ~/.zshrc
```

2. **Check if installed:**
```bash
ls ~/.sku/bin/sku
```

3. **Add to PATH manually:**
```bash
export PATH="$HOME/.sku/bin:$PATH"
# Add to ~/.bashrc or ~/.zshrc for persistence
```

4. **Reinstall:**
```bash
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/install-sku.sh | bash
```

### Problem: Update hook not working

**Symptoms:**
- No update notifications at Claude Code start
- Hook errors in terminal

**Diagnosis:**
```bash
# Test hook manually
python .claude/hooks/check-artifact-updates.py

# Check permissions
ls -l .claude/hooks/check-artifact-updates.py
```

**Solutions:**

1. **Make executable:**
```bash
chmod +x .claude/hooks/check-artifact-updates.py
```

2. **Check Python path:**
```bash
which python
# Update settings.json if python is in different location
```

3. **Re-download hook:**
```bash
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/.claude/hooks/check-artifact-updates.py \
  -o .claude/hooks/check-artifact-updates.py
```

### Problem: Catalog not syncing

**Symptoms:**
```bash
$ sku list
Error: Catalog not found
```

**Diagnosis:**
```bash
sku doctor
```

**Solutions:**

1. **Sync catalog:**
```bash
sku sync --index-only
```

2. **Manual download:**
```bash
mkdir -p ~/.sku/catalog
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/catalog/index.yaml \
  -o ~/.sku/catalog/index.yaml
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/catalog/categories.yaml \
  -o ~/.sku/catalog/categories.yaml
```

3. **Check network:**
```bash
curl -I https://github.com/ozand/shared-knowledge-base
```

### Problem: Self-update fails

**Symptoms:**
```bash
$ sku self-update
✗ Update failed: Connection timeout
```

**Solutions:**

1. **Check network:**
```bash
curl -I https://raw.githubusercontent.com
```

2. **Update manually:**
```bash
# Download installer
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/install-sku.sh -o /tmp/install.sh

# Run reinstall
bash /tmp/install.sh
```

3. **Use proxy:**
```bash
export https_proxy=http://proxy.example.com:8080
sku self-update
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
│                 shared-knowledge-base                        │
│                                                               │
│  scripts/install-sku.sh  ← Universal installer              │
│  tools/skb-cli/          ← SKU CLI source                    │
│  catalog/                ← Always updated metadata           │
└─────────────────────────────────────────────────────────────┘
         ↓ One-liner install                  ↑ Self-update
┌─────────────────────────────────────────────────────────────┐
│                      Developer Machine                        │
│                                                               │
│  ~/.sku/                                                      │
│  ├── bin/sku*              ← Installed CLI                   │
│  ├── catalog/              ← Downloaded metadata             │
│  └── config.yaml           ← Configuration                   │
│                                                               │
│  /path/to/project/                                             │
│  ├── .claude/                                               │
│  │   ├── CLAUDE.md                                          │
│  │   ├── settings.json                                      │
│  │   └── hooks/check-artifact-updates.py  ← Auto-checker    │
│  └── .sku/config.yaml                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎓 Best Practices

### For New Projects

1. **Always use `sku init`**
   - Auto-detects project type
   - Creates proper structure
   - Installs update hooks

2. **Commit `.claude/` to git**
   - Share configuration with team
   - Hooks work for everyone

3. **Customize CLAUDE.md**
   - Add project-specific context
   - Document workflows
   - Link to shared artifacts

### For Existing Projects

1. **Run `sku doctor` regularly**
   - Checks installation health
   - Identifies issues early

2. **Keep SKU CLI updated**
   - Get new features
   - Bug fixes
   - Security patches

3. **Review update notifications**
   - Don't blindly update
   - Check changelogs for major versions
   - Test before deploying

### For Teams

1. **Standardize installation**
   - Share installer link in onboarding docs
   - Use same SKU_REPO for everyone

2. **Centralize artifact management**
   - Curate shared artifacts
   - Review before publishing
   - Document breaking changes

3. **Automate updates**
   - Enable patch auto-updates
   - Schedule review of minor/major updates
   - Test in staging first

---

## 📖 Full Command Reference

### Installation

```bash
# Install SKU CLI (one-liner)
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/install-sku.sh | bash

# Check health
sku doctor

# Check version
sku --version
```

### Project Setup

```bash
# Initialize new project
sku init

# Initialize with options
sku init --type typescript --team backend-team

# Initialize without hooks
sku init --no-hooks
```

### Updates

```bash
# Update SKU CLI
sku self-update

# Check artifact updates
sku check-updates

# Update all artifacts
sku update --all

# Update specific artifact
sku update skill testing
```

### Troubleshooting

```bash
# System health check
sku doctor

# Check installation
sku status

# Sync catalog
sku sync --index-only
```

---

## 🎯 Summary

**For New Projects:**
1. Install: `curl ... | bash`
2. Restart shell
3. `cd /path/to/project`
4. `sku init`
5. Done! ✅

**For Existing Projects:**
1. `sku self-update` - Update CLI
2. `sku check-updates` - Check artifacts
3. `sku update --all` - Update artifacts
4. Done! ✅

**Troubleshooting:**
1. `sku doctor` - Diagnose issues
2. Check this guide
3. Reinstall if needed

---

**Need help?**
- **Documentation:** https://github.com/ozand/shared-knowledge-base
- **Issues:** https://github.com/ozand/shared-knowledge-base/issues
- **Enterprise Guide:** ENTERPRISE-KNOWLEDGE-GRAPH.md

---

**Quality Score:** 95/100
