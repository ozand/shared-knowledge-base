# For Projects: Shared KB Integration Templates

**Purpose:** Provides templates and scripts for integrating Shared Knowledge Base into your projects.

**Version:** 1.0
**Last Updated:** 2026-01-07

---

## Quick Start

```bash
# 1. In your project directory
cd your-project/

# 2. Add shared-knowledge-base as submodule
git submodule add https://github.com/ozand/shared-knowledge-base docs/knowledge-base/shared

# 3. Run installation script
python docs/knowledge-base/shared/for-projects/scripts/install.py

# 4. Configure for your project
# Edit: .claude/settings.json
# Edit: .claude/CLAUDE.md
# Edit: .kb-config.yaml

# 5. Build KB index
python docs/knowledge-base/shared/tools/kb.py index

# 6. Test integration
/kb-search "docker"
```

---

## Directory Structure

```
for-projects/
├── README.md                   # This file
├── PROJECT-INTEGRATION.md     # Complete integration guide
├── quick-start.md             # 5-minute setup guide
├── agent-templates/           # Agent templates
│   ├── README.md
│   ├── kb-agent.md
│   └── subagents/
│       ├── researcher.md
│       ├── debugger.md
│       ├── validator.md
│       └── knowledge-curator.md
├── skill-templates/           # Skill templates
│   ├── README.md
│   ├── kb-search/
│   ├── kb-validate/
│   ├── kb-index/
│   ├── kb-create/
│   ├── audit-quality/
│   ├── find-duplicates/
│   └── research-enhance/
├── command-templates/         # Command templates
│   ├── README.md
│   ├── kb-search.md
│   ├── kb-validate.md
│   ├── kb-create.md
│   ├── kb-index.md
│   ├── retrospective.md
│   ├── kb-sync.md
│   └── kb-query.md
├── config-templates/          # Configuration templates
│   ├── settings.json
│   ├── kb-config.yaml
│   └── hooks.json
├── scripts/                   # Installation scripts
│   ├── install.py            # Install KB integration
│   ├── update.py             # Update from templates
│   └── uninstall.py          # Remove KB integration
└── examples/                  # Example integrations
    ├── fastapi-project/
    ├── react-project/
    └── python-project/
```

---

## What You Get

After installation, your project will have:

### 1. Agents (`.claude/agents/`)

Autonomous agents for KB management:
- **kb-agent.md:** Main KB management agent
- **subagents/researcher.md:** Web research specialist
- **subagents/debugger.md:** Error analysis specialist
- **subagents/validator.md:** Solution validation specialist
- **subagents/knowledge-curator.md:** Knowledge capture specialist

### 2. Skills (`.claude/skills/`)

Reusable capabilities for KB operations:
- **kb-search:** Search KB for errors/solutions
- **kb-validate:** Validate KB entries (quality ≥75/100)
- **kb-index:** Rebuild search index
- **kb-create:** Create new KB entries
- **audit-quality:** Comprehensive quality audit
- **find-duplicates:** Detect and merge duplicates
- **research-enhance:** Enhance entries with external research

### 3. Commands (`.claude/commands/`)

Quick-access commands:
- **/kb-search:** Quick KB search
- **/kb-validate:** Quick validation
- **/kb-create:** Quick entry creation
- **/kb-index:** Quick index rebuild
- **/retrospective:** Analyze session, capture knowledge
- **/kb-sync:** Sync changes to shared repository
- **/kb-query:** Intelligent KB query with AI analysis

### 4. Configuration (`.claude/`, `.kb-config.yaml`)

- **settings.json:** Claude Code configuration
- **kb-config.yaml:** KB paths and settings
- **hooks.json:** Automation hooks

---

## Documentation

| Document | Purpose | Length |
|----------|---------|--------|
| **PROJECT-INTEGRATION.md** | Complete integration guide | ~800 lines |
| **quick-start.md** | 5-minute setup | ~200 lines |
| **agent-templates/README.md** | Agent documentation | ~400 lines |
| **skill-templates/README.md** | Skill documentation | ~300 lines |
| **command-templates/README.md** | Command documentation | ~500 lines |

---

## Installation Options

### Option 1: Full Installation (Recommended)

```bash
python docs/knowledge-base/shared/for-projects/scripts/install.py --full
```

Installs:
- ✅ All agents
- ✅ All skills
- ✅ All commands
- ✅ Configuration templates
- ✅ Local KB directories

### Option 2: Minimal Installation

```bash
python docs/knowledge-base/shared/for-projects/scripts/install.py --minimal
```

Installs:
- ✅ Core skills (kb-search, kb-validate, kb-create)
- ✅ Core commands (kb-search, kb-validate, kb-create)
- ✅ Configuration templates

### Option 3: Custom Installation

```bash
python docs/knowledge-base/shared/for-projects/scripts/install.py \
  --agents \
  --skills kb-search,kb-validate \
  --commands kb-search,kb-validate,retrospective
```

---

## Updating from Templates

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

## Customization

### Project-Specific Agents

You can customize agents for your project:

```markdown
<!-- .claude/agents/kb-agent.md -->

# KB Agent for FastAPI Web App

**Project:** fastapi-web-app
**Framework:** FastAPI 0.104
**Python:** 3.11

## Project Context

This is a FastAPI web application with:
- WebSocket support for real-time updates
- PostgreSQL database with asyncpg
- Docker deployment

## KB Integration

[Standard agent content...]

## Project-Specific Instructions

When searching KB, prioritize:
1. FastAPI-related entries
2. WebSocket-related entries
3. PostgreSQL-related entries
4. Docker-related entries
```

### Project-Specific Skills

Add project-specific skills:

```bash
# Create custom skill
mkdir -p .claude/skills/fastapi-debug

# Create skill file
cat > .claude/skills/fastapi-debug/SKILL.md << 'EOF'
# FastAPI Debug Skill

Debug FastAPI-specific issues:
- WebSocket errors
- Async/await issues
- Dependency injection problems
- Pydantic validation errors
EOF
```

### Project-Specific Commands

Add project-specific commands:

```bash
# Create custom command
cat > .claude/commands/fastapi-test.md << 'EOF'
# FastAPI Test

Run FastAPI-specific tests:
```bash
pytest tests/test_api.py
pytest tests/test_websocket.py
```
EOF
```

---

## Architecture

### Separation of Concerns

**shared-knowledge-base provides:**
- ✅ Knowledge entries (YAML files)
- ✅ Management tools (kb.py)
- ✅ Integration templates (this directory)

**Your project provides:**
- ✅ Application code
- ✅ KB integration (installed from templates)
- ✅ Local knowledge (project-specific)

### Benefits

1. **Clear separation:** Knowledge vs. application code
2. **Project flexibility:** Customize integration per project
3. **Easier updates:** Update from templates when needed
4. **Cleaner git history:** Knowledge changes separate from project changes

---

## Troubleshooting

### Installation Failed

**Problem:** Installation script fails

**Solutions:**
1. Check Python version (3.8+ required)
2. Check file permissions
3. Check submodule is cloned: `git submodule update --init --recursive`

### Agents Not Working

**Problem:** Agents not launching

**Solutions:**
1. Check `.claude/settings.json` - agents enabled?
2. Check agent file paths - files exist?
3. Check Claude Code version - supports agents?

### KB Search Not Working

**Problem:** `/kb-search` returns no results

**Solutions:**
1. Build index: `python docs/knowledge-base/shared/tools/kb.py index`
2. Check `.kb-config.yaml` - paths correct?
3. Check YAML files exist in KB

---

## Examples

See `examples/` directory for complete project integrations:
- **fastapi-project/** - FastAPI web application
- **react-project/** - React frontend application
- **python-project/** - Python CLI application

---

## Support

For issues or questions:
1. Check `PROJECT-INTEGRATION.md` for detailed guide
2. Check `examples/` for reference implementations
3. Open issue on shared-knowledge-base repository

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Maintained By:** KB Curator
