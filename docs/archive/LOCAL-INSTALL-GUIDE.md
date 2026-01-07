# Local Installation Guide for Team Members
## Installing SKU CLI from Private Repository

**For:** Team members with access to shared-knowledge-base repository
**Platform:** All (Linux/Mac/Windows)
**Goal:** Install SKU CLI without public PyPI

---

## 🎯 Overview

Since this is a **private repository**, SKU CLI cannot be published to public PyPI. This guide shows team members how to install SKU CLI from the local repository.

---

## 📦 Installation Methods

### Method 1: Clone and Install (Recommended)

#### For All Platforms:

```bash
# 1. Clone the repository (if not already cloned)
git clone https://github.com/ozand/shared-knowledge-base.git
cd shared-knowledge-base

# 2. Install SKU CLI in editable mode
pip install -e tools/skb-cli/

# 3. Verify installation
sku --version
```

**Benefits:**
- ✅ Editable install (changes reflect immediately)
- ✅ No need to reinstall after updates
- ✅ Works on all platforms

---

### Method 2: Using uv (Faster)

```bash
# 1. Clone repository
git clone https://github.com/ozand/shared-knowledge-base.git
cd shared-knowledge-base

# 2. Install with uv (faster than pip)
uv pip install -e tools/skb-cli/

# 3. Verify
sku --version
```

---

### Method 3: Direct from Existing Clone

If you already have the repository cloned (e.g., as a submodule):

```bash
# From your project directory
cd docs/knowledge-base/shared

# Install SKU CLI
pip install -e tools/skb-cli/

# Or if using uv
uv pip install -e tools/skb-cli/
```

---

## 🔄 Updating SKU CLI

With editable install (`pip install -e`), updates are automatic:

```bash
# Update the repository
cd shared-knowledge-base
git pull origin main

# SKU CLI is automatically updated (no reinstall needed!)
sku --version
```

---

## 🚀 Initial Setup After Installation

After installing SKU CLI:

```bash
# 1. Check system health
sku doctor

# 2. Sync catalog
sku sync --index-only

# 3. Authenticate (if using private repo)
export GITHUB_TOKEN="your_token_here"
export SKU_REPO="ozand/shared-knowledge-base"

# 4. List available artifacts
sku list

# 5. Install artifact
sku install skill testing
```

---

## 📁 Project Initialization

For new projects:

```bash
cd /path/to/new-project

# Initialize with SKU CLI
sku init

# Or with explicit parameters
sku init --type typescript --team backend-team
```

**What `sku init` creates:**
- `.claude/` directory structure
- `CLAUDE.md` with project context
- `.sku/config.yaml` configuration
- `.skuignore` file
- Update check hooks

---

## 🛠️ Troubleshooting

### Problem: sku command not found

**Solution:**

```bash
# Check if installed
pip show sku-cli

# If not installed, install it
cd shared-knowledge-base
pip install -e tools/skb-cli/

# Or check PATH
echo $PATH  # Should include Python Scripts directory
```

### Problem: Permission denied

**Solution:**

```bash
# Use user installation
pip install --user -e tools/skb-cli/

# Or use virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e tools/skb-cli/
```

### Problem: Dependencies not found

**Solution:**

```bash
# Install with dependencies
cd tools/skb-cli
pip install -e .[dev]

# Or install manually
pip install click pyyaml requests gitpython rich questionary semver
```

---

## 📖 Daily Usage

### Check for Updates

```bash
# Update SKU CLI itself
cd shared-knowledge-base
git pull origin main
# No reinstall needed!

# Check artifact updates
sku check-updates

# Update artifacts
sku update --all
```

### Common Commands

```bash
# Search artifacts
sku search --tag testing

# List installed
sku status

# Install artifact
sku install skill testing

# Publish project artifact
sku publish docs/mcp --type mcp --version 1.0.0

# System health
sku doctor
```

---

## 🎓 Best Practices

### For Development

1. **Always use editable install** (`pip install -e`)
   - Changes reflect immediately
   - No reinstall after git pull

2. **Keep repository updated**
   ```bash
   cd shared-knowledge-base
   git pull origin main
   ```

3. **Use virtual environments**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e tools/skb-cli/
   ```

### For Teams

1. **Standardize installation method**
   - Document in team wiki
   - Use same command for everyone

2. **Version pinning** (optional)
   ```bash
   # Install specific version
   git checkout v1.1.0
   pip install -e tools/skb-cli/
   ```

3. **Update schedule**
   - Weekly updates recommended
   - Test in staging first

---

## 🔐 Private Repository Access

### Setting up GitHub Token

```bash
# Create GitHub Personal Access Token
# 1. Go to https://github.com/settings/tokens
# 2. Generate new token (repo scope)
# 3. Set environment variable:

export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"

# Or add to ~/.bashrc or ~/.zshrc:
echo 'export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"' >> ~/.bashrc
source ~/.bashrc
```

### Configuring SKU

```bash
# Set repository URL
export SKU_REPO="ozand/shared-knowledge-base"

# Or add to ~/.sku/config.yaml:
cat > ~/.sku/config.yaml <<'EOF'
github:
  repository: "ozand/shared-knowledge-base"
  branch: "main"
EOF
```

---

## 📊 Comparison: Methods

| Method | Pros | Cons | Recommended |
|--------|------|------|-------------|
| **pip install -e** | Editable, auto-update | Requires repo access | ✅ Yes |
| **uv pip install -e** | Faster | Requires uv | ✅ Yes |
| **One-line installer** | Quick | Encoding issues on Windows | ⚠️ Use with caution |
| **kb.py only** | No install needed | Limited features | ✅ Fallback |

---

## 🎯 Summary

**Recommended Installation:**

```bash
# Clone (once)
git clone https://github.com/ozand/shared-knowledge-base.git
cd shared-knowledge-base

# Install (once)
pip install -e tools/skb-cli/

# Update (whenever)
git pull origin main
# No reinstall needed!
```

**Key Points:**
- ✅ Use editable install: `pip install -e tools/skb-cli/`
- ✅ No need to reinstall after updates
- ✅ Works on all platforms
- ✅ Requires repo access (private)

**Alternative:** Use `kb.py` directly (no installation needed)

---

**Need help?**
- **Documentation:** BOOTSTRAP-GUIDE.md
- **Installation Analysis:** docs/research/claude-code/INSTALLATION-ANALYSIS.md
- **Issues:** https://github.com/ozand/shared-knowledge-base/issues

---

**Quality Score:** 95/100
