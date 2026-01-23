# For Projects: Shared KB Integration Templates

**Purpose:** Provides templates and scripts for integrating Shared Knowledge Base into your projects.

**Version:** 1.1
**Last Updated:** 2026-01-19

---

## Quick Start

```bash
# 1. In your project directory
cd your-project/

# 2. Add shared-knowledge-base as submodule
git submodule add https://github.com/ozand/shared-knowledge-base .kb/shared

# 3. Run installation script
python .kb/shared/scripts/unified-install.py --full

# 4. Configure for your project
# Edit: .kb/project/PROJECT.yaml

# 5. Build KB index
python .kb/shared/tools/kb.py index

# 6. Test integration
python .kb/shared/tools/kb.py search "docker"
```

---

## Directory Structure

```
.kb/shared/
├── domains/                   # Knowledge entries by domain
│   ├── python/                # Python-specific
│   ├── docker/                # Docker-specific
│   ├── postgresql/            # PostgreSQL-specific
│   ├── javascript/            # JavaScript-specific
│   ├── universal/             # Cross-language patterns
│   └── vps/                   # VPS administration
├── tools/                     # CLI tools
│   ├── kb.py                  # Main CLI
│   ├── kb_search.py           # Search functionality
│   └── kb_sync.py             # Sync with shared repo
├── docs/                      # Documentation
│   ├── integration/           # Integration guides
│   ├── v5.1/                  # v5.1 Architecture docs
│   └── standards/             # YAML standards, quality gates
├── agents/                    # Curator agent configs
└── scripts/                   # Installation scripts
    └── unified-install.py     # Cross-platform installer
```

---

## What You Get

After installation, your project will have:

### 1. Shared Knowledge (`.kb/shared/`)

Reusable knowledge across all projects:
- **domains/**: Categorized knowledge entries (Python, Docker, etc.)
- **tools/**: CLI tools for search, validation, indexing
- **docs/**: Integration guides and standards

### 2. Project Knowledge (`.kb/project/`)

Project-specific knowledge (safe to commit):
- **PROJECT.yaml**: Project metadata and configuration
- **context-archive/**: Condensed session summaries
- **domains/**: Project-local knowledge entries

---

## Installation Options

### Option 1: Full Installation (Recommended)

```bash
python .kb/shared/scripts/unified-install.py --full
```

Installs:
- ✅ Two-tier structure (project + shared KB)
- ✅ PROJECT.yaml with project metadata
- ✅ Context archive system
- ✅ Git configuration

### Option 2: Minimal Installation

```bash
python .kb/shared/scripts/unified-install.py
```

Installs:
- ✅ Basic two-tier structure
- ✅ PROJECT.yaml template

---

## Updating from Remote

When shared-knowledge-base is updated:

```bash
# 1. Pull latest changes
cd .kb/shared
git pull origin main

# 2. Rebuild index
python tools/kb.py index -v
```

---

## Customization

### Project-Specific Knowledge

Add project-local knowledge:

```bash
# Create local knowledge entry
cat > .kb/project/domains/local/my-project-001.yaml << 'EOF'
version: "1.0"
category: "my-project"
last_updated: "2026-01-19"

errors:
  - id: "ERROR-001"
    title: "Project-specific error"
    severity: "high"
    scope: "project"
    problem: |
      Description of the problem
    solution:
      code: |
        # Solution code
      explanation: |
        How it works
EOF
```

### PROJECT.yaml Configuration

Edit `.kb/project/PROJECT.yaml`:

```yaml
name: "my-project"
description: "My project description"
repository: "user/repo"
stack:
  - python
  - docker
  - postgresql
status: "active"
maintainer_agent:
  name: "Claude"
  role: "Project Lead"
kb_tier: "shared"
last_updated: "2026-01-19"
```

---

## Architecture

### Separation of Concerns

**shared-knowledge-base provides:**
- ✅ Knowledge entries (YAML files)
- ✅ Management tools (kb.py)
- ✅ Integration scripts (unified-install.py)

**Your project provides:**
- ✅ Application code
- ✅ Local knowledge (`.kb/project/`)
- ✅ Project configuration (PROJECT.yaml)

### Benefits

1. **Clear separation:** Shared vs. local knowledge
2. **Easy updates:** Pull from shared repo
3. **Clean git history:** Local KB committed separately

---

## Troubleshooting

### Installation Failed

**Problem:** Installation script fails

**Solutions:**
1. Check Python version (3.10+ required)
2. Check git is initialized
3. Check file permissions

### KB Search Not Working

**Problem:** Search returns no results

**Solutions:**
1. Build index: `python .kb/shared/tools/kb.py index`
2. Check KB is at `.kb/shared/`
3. Check YAML files exist in domains/

---

## Documentation

| Document | Purpose |
|----------|---------|
| **[BOOTSTRAP.md](BOOTSTRAP.md)** | Complete integration guide |
| **[AGENT-QUICK-START.md](AGENT-QUICK-START.md)** | Agent quick start |
| **[v5.1/README.md](../v5.1/README.md)** | v5.1 Architecture & Workflows |
| **[MCP-SERVER.md](../MCP-SERVER.md)** | MCP Server Integration |

---

**Version:** 1.1
**Last Updated:** 2026-01-19
**Maintained By:** KB Curator
