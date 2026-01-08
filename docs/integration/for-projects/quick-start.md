# Quick Start: Install Shared KB in Your Project

**Time:** 5 minutes
**Difficulty:** Easy

---

## Prerequisites

- Python 3.8+
- Git
- Claude Code installed
- Your project directory

---

## Installation

### Step 1: Add Shared KB as Submodule (1 minute)

```bash
cd your-project/

# Add shared-knowledge-base as submodule
git submodule add https://github.com/ozand/shared-knowledge-base \
  docs/knowledge-base/shared

# Initialize submodule
git submodule update --init --recursive
```

**What this does:**
- Clones shared-knowledge-base into `docs/knowledge-base/shared/`
- Links to repository (always up-to-date)
- Keeps your project git history clean

### Step 2: Run Installation Script (1 minute)

```bash
# Full installation (recommended)
python docs/knowledge-base/shared/for-projects/scripts/install.py --full

# Or minimal installation (core components only)
python docs/knowledge-base/shared/for-projects/scripts/install.py --minimal
```

**What this does:**
- Creates `.claude/` directory structure
- Copies agent templates
- Copies skill templates
- Copies command templates
- Creates configuration files
- Creates local KB directories

**Output:**
```
🚀 Shared Knowledge Base Installation

ℹ️  Project root: /path/to/your-project
ℹ️  Shared KB root: /path/to/shared-knowledge-base

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Creating Directory Structure
✅ Directory structure created

Installing Agents
✅ Subagents installed (4 files)
✅ KB agent installed

Installing Skills
✅ All skills installed (7 skills)

Installing Commands
✅ All commands installed (7 commands)

Installing Configuration
✅ settings.json created
✅ .kb-config.yaml created
✅ hooks.json created

Creating Local KB
✅ Local KB directories created

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 Installation Complete!
```

### Step 3: Configure KB Paths (1 minute)

Edit `.kb-config.yaml`:

```yaml
# KB paths
shared_kb: "docs/knowledge-base/shared"
local_kb: "docs/knowledge-base"

# Search settings
search:
  ignore_case: true
  max_results: 50

# Validation settings
validation:
  min_quality_score: 75
  strict_mode: false

# Sync settings
sync:
  auto_push: false
  create_issues: true
```

### Step 4: Configure Claude Code (1 minute)

Edit `.claude/settings.json`:

```json
{
  "agents": {
    "paths": ["./.claude/agents"],
    "enabled": ["kb-agent"],
    "auto_discover": true
  },
  "skills": {
    "paths": ["./.claude/skills"],
    "enabled": [
      "kb-search",
      "kb-validate",
      "kb-create",
      "audit-quality"
    ],
    "auto_discover": true
  },
  "commands": {
    "paths": ["./.claude/commands"]
  },
  "hooks": {
    "error-handling": {
      "events": ["PreToolUse"],
      "condition": "error OR exception",
      "action": "launch_parallel_subagents"
    },
    "knowledge-capture": {
      "events": ["Stop"],
      "action": "launch_knowledge_curator"
    }
  }
}
```

### Step 5: Add Project Context (1 minute)

Create `.claude/CLAUDE.md`:

```markdown
# Project: Your Project Name

## Overview
[Brief description of your project]

## Tech Stack
- **Framework:** [FastAPI, React, etc.]
- **Language:** [Python 3.11, JavaScript, etc.]
- **Database:** [PostgreSQL, MongoDB, etc.]
- **Deployment:** [Docker, AWS, etc.]

## Project Structure
```
your-project/
├── src/              # Source code
├── tests/            # Tests
├── docs/             # Documentation
└── .claude/          # Claude Code configuration
```

## KB Integration
- **Shared KB:** `docs/knowledge-base/shared/`
- **Local KB:** `docs/knowledge-base/project/`
- **Index:** Build with `python docs/knowledge-base/shared/tools/kb.py index`

## Common Commands
- `/kb-search "query"` - Search KB
- `/kb-validate file.yaml` - Validate entry
- `/retrospective` - Capture knowledge from session
- `/kb-sync file.yaml` - Sync to shared repository
```

### Step 6: Build KB Index (30 seconds)

```bash
# Build search index
python docs/knowledge-base/shared/tools/kb.py index

# Verify index
python docs/knowledge-base/shared/tools/kb.py stats
```

**Output:**
```
Building index...
✅ Indexed 101 entries

Statistics:
- Total entries: 101
  - Python: 45
  - Docker: 20
  - Universal: 15
  - PostgreSQL: 12
  - JavaScript: 9
- Total size: 2.3 MB
- Last updated: 2026-01-07
```

---

## Testing

### Test 1: KB Search

```bash
/kb-search "docker volume"
```

**Expected output:**
```
🔍 KB SEARCH: "docker volume"

Found: 3 results

1. DOCKER-003: Docker Volume Permissions (Score: 95%)
   File: docker/errors/volume-permissions.yaml
   Severity: medium

2. DOCKER-015: Docker Volume Mount Issues (Score: 82%)
   File: docker/errors/volume-mounts.yaml
   Severity: high

3. DOCKER-020: Docker Automatically Recreates Directories (Score: 78%)
   File: docker/errors/volume-recreation.yaml
   Severity: low
```

### Test 2: Retrospective

```bash
/retrospective
```

**Expected output:**
```
🔍 RETROSPECTIVE ANALYSIS

Session Duration: 5 minutes
Key Moments Found: 0

No knowledge captured yet. Keep working!
```

### Test 3: KB Query

```bash
/kb-query "websocket timeout"
```

**Expected output:**
```
🔍 KB QUERY: "websocket timeout"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Best Match: PYTHON-045 (Score: 87%)

Problem: WebSocket timeout after 5 seconds

Solution:
[Code example and explanation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## What You Got

After installation, your project has:

```
your-project/
├── .claude/                    ✅ NEW
│   ├── agents/                 # Agents
│   │   ├── kb-agent.md        # KB management agent
│   │   └── subagents/          # Subagents
│   ├── skills/                 # Skills
│   │   ├── kb-search/         # KB search
│   │   ├── kb-validate/       # KB validation
│   │   └── kb-create/         # KB creation
│   ├── commands/               # Commands
│   │   ├── kb-search.md
│   │   ├── kb-validate.md
│   │   └── retrospective.md
│   ├── settings.json          # Configuration
│   └── CLAUDE.md              # Project memory
├── docs/
│   └── knowledge-base/         ✅ NEW
│       ├── shared/            # Submodule
│       │   ├── python/        # Shared knowledge
│       │   ├── docker/
│       │   └── tools/
│       └── project/           # Local knowledge
│           ├── errors/
│           └── patterns/
└── .kb-config.yaml            ✅ NEW
```

---

## Installation Options

### Full Installation (Recommended)

```bash
python docs/knowledge-base/shared/for-projects/scripts/install.py --full
```

**Installs:**
- ✅ All agents (kb-agent + 4 subagents)
- ✅ All skills (7 skills)
- ✅ All commands (7 commands)
- ✅ All configuration files

**Use when:** You want complete KB integration with all features

### Minimal Installation

```bash
python docs/knowledge-base/shared/for-projects/scripts/install.py --minimal
```

**Installs:**
- ✅ Core skills (kb-search, kb-validate, kb-create)
- ✅ Core commands (kb-search, kb-validate, kb-create)
- ✅ Configuration files

**Use when:** You want basic KB functionality, can add more later

### Custom Installation

```bash
# Install only agents
python docs/knowledge-base/shared/for-projects/scripts/install.py --agents

# Install specific skills
python docs/knowledge-base/shared/for-projects/scripts/install.py \
  --skills kb-search,kb-validate

# Install only commands
python docs/knowledge-base/shared/for-projects/scripts/install.py --commands
```

---

## Updating

When shared-knowledge-base templates are updated:

```bash
# 1. Pull latest changes
cd docs/knowledge-base/shared
git pull origin main

# 2. Update your project
cd ../../..
python docs/knowledge-base/shared/for-projects/scripts/update.py

# 3. Review changes
# The script will show diffs and ask for confirmation
```

---

## Troubleshooting

### Problem: Installation fails

**Solution:**
```bash
# Check Python version (3.8+ required)
python --version

# Check submodule is cloned
git submodule status

# Initialize submodule if needed
git submodule update --init --recursive

# Re-run installation
python docs/knowledge-base/shared/for-projects/scripts/install.py
```

### Problem: KB search returns no results

**Solution:**
```bash
# Build index
python docs/knowledge-base/shared/tools/kb.py index

# Check index exists
ls docs/knowledge-base/shared/_index.yaml

# Check KB paths in .kb-config.yaml
cat .kb-config.yaml
```

### Problem: Agents not launching

**Solution:**
```bash
# Check agents are enabled in .claude/settings.json
cat .claude/settings.json | grep agents

# Check agent files exist
ls .claude/agents/

# Restart Claude Code
```

---

## Next Steps

1. **Read full guide:** `docs/knowledge-base/shared/for-projects/PROJECT-INTEGRATION.md`
2. **Customize agents:** Edit `.claude/agents/kb-agent.md` for your project
3. **Add project-specific skills:** Create skills in `.claude/skills/`
4. **Configure hooks:** Set up automation in `.claude/settings.json`
5. **Build knowledge:** Start capturing knowledge with `/retrospective`

---

## Summary

✅ Added shared-knowledge-base as submodule
✅ Ran installation script
✅ Configured KB paths
✅ Configured Claude Code
✅ Added project context
✅ Built KB index

**Time:** 5 minutes
**Status:** Ready to use!

---

**Need Help?**
- Full guide: `for-projects/PROJECT-INTEGRATION.md`
- Examples: `for-projects/examples/`
- Issues: https://github.com/ozand/shared-knowledge-base/issues

---

**Version:** 1.0
**Last Updated:** 2026-01-07
