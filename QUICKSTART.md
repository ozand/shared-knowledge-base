# Quick Start Guide

**5 минут до полной настройки** 🚀

---

## Installation (2 minutes)

### Unified Installation (Recommended)

```bash
# Method 1: From cloned repository
python scripts/unified-install.py --full

# Method 2: Remote download (one-line)
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/unified-install.py | python3 - --full
```

**What it does:**
- ✅ Adds submodule with sparse checkout (excludes curator/)
- ✅ Installs agents (1 main + 4 subagents)
- ✅ Installs skills (7 skills)
- ✅ Installs commands (7 commands)
- ✅ Creates configuration files
- ✅ Builds search index
- ✅ Verifies installation

**For existing projects:**
```bash
# Check for updates
python docs/knowledge-base/shared/scripts/unified-install.py --check

# Update existing installation
python docs/knowledge-base/shared/scripts/unified-install.py --update
```

---

## First Use (1 minute)

### Build Search Index

```bash
python docs/knowledge-base/shared/tools/kb.py index -v
```

**Output:**
```
Building index from: docs/knowledge-base
  [OK] Indexed: IMPORT-001 - Circular Import Between ETL Modules
  [OK] Indexed: TYPE-001 - Mypy Too Strict for Test Files
  ...
[OK] Indexed 101 entries
```

### First Search

```bash
python docs/knowledge-base/shared/tools/kb.py search "async test"
```

**Output:**
```
Found 2 result(s):

1. TEST-001: Async Test Without @pytest.mark.asyncio
   Category: testing | Severity: high | Scope: python
   Tags: async, pytest, decorator
   File: docs/knowledge-base/shared/python/errors/testing.yaml
```

---

## Common Commands

### Search

```bash
# Simple search
python docs/knowledge-base/shared/tools/kb.py search "websocket"

# By category
python docs/knowledge-base/shared/tools/kb.py search --category python

# By severity
python docs/knowledge-base/shared/tools/kb.py search --severity high

# By tags
python docs/knowledge-base/shared/tools/kb.py search --tags async pytest

# By ID
python docs/knowledge-base/shared/tools/kb.py search --id ERROR-001
```

### Statistics

```bash
python docs/knowledge-base/shared/tools/kb.py stats
```

### Maintenance

```bash
# Rebuild index
python docs/knowledge-base/shared/tools/kb.py index --force -v

# Validate entry
python docs/knowledge-base/shared/tools/kb.py validate path/to/file.yaml

# Validate all
python docs/knowledge-base/shared/tools/kb.py validate .

# Export to JSON
python docs/knowledge-base/shared/tools/kb.py export --format json --output kb.json
```

### Updates

```bash
# Check for updates
python docs/knowledge-base/shared/scripts/unified-install.py --check

# Update KB
python docs/knowledge-base/shared/scripts/unified-install.py --update
```

---

## Optional: Create Alias

### Windows (PowerShell)

```powershell
# Add to PowerShell profile
notepad $PROFILE

# Add this line:
function kb { python docs/knowledge-base/shared/tools/kb.py $args }

# Restart PowerShell, then:
kb search "async"
kb stats
```

### macOS / Linux

```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'alias kb="python docs/knowledge-base/shared/tools/kb.py"' >> ~/.bashrc
source ~/.bashrc

# Then:
kb search "async"
kb stats
```

---

## Next Steps

### For Users

- **[docs/guides/installation/HARMONIZED-INSTALLATION-GUIDE.md](docs/guides/installation/HARMONIZED-INSTALLATION-GUIDE.md)** - Complete installation guide (migration, troubleshooting)
- **[GUIDE.md](GUIDE.md)** - Implementation guide
- **[for-claude-code/README.md](for-claude-code/README.md)** - Claude Code integration

### For AI Agents

- **[AGENT-QUICK-START.md](AGENT-QUICK-START.md)** - Quick start for agents
- **[docs/guides/workflows/ROLE_SEPARATION_GUIDE.md](docs/guides/workflows/ROLE_SEPARATION_GUIDE.md)** - Project Agent vs Curator roles
- **[docs/guides/workflows/GITHUB_ATTRIBUTION_GUIDE.md](docs/guides/workflows/GITHUB_ATTRIBUTION_GUIDE.md)** - Contribution workflow

### Advanced Usage

- **[docs/guides/integration/SUBMODULE_VS_CLONE.md](docs/guides/integration/SUBMODULE_VS_CLONE.md)** - Submodule vs Clone comparison
- **[docs/research/](docs/research/)** - Research papers and analysis
- **[universal/patterns/](universal/patterns/)** - Best practices patterns

---

## Troubleshooting

### Problem: Search returns no results

**Fix:** Rebuild index
```bash
python docs/knowledge-base/shared/tools/kb.py index --force -v
```

### Problem: YAML validation fails

**Fix:** Check syntax
```bash
python docs/knowledge-base/shared/tools/kb.py validate path/to/file.yaml
```

### Problem: Installation fails

**See:** [docs/guides/installation/HARMONIZED-INSTALLATION-GUIDE.md](docs/guides/installation/HARMONIZED-INSTALLATION-GUIDE.md)

---

**Version:** 3.2
**Last Updated:** 2026-01-07
**For Help:** [GitHub Issues](https://github.com/ozand/shared-knowledge-base/issues)
