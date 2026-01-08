# Shared Knowledge Base - Claude Code Instructions

**Repository:** shared-knowledge-base
**Version:** 5.1.0
**Last Updated:** 2026-01-08

---

## Overview

Centralized knowledge base containing verified solutions for common software development errors across multiple languages and frameworks. **v5.1 implements a two-tier architecture** with Project KB (local) and Shared KB (global) tiers, enabling secure knowledge sharing via GitHub Issues workflow.

**📘 Complete Guide:** `@for-claude-code/README.md`
**📘 v5.1 Documentation:** `@docs/v5.1/README.md`

---

## Quick Start

### Essential Commands

```bash
# Build index (required after changes)
python tools/kb.py index -v

# Search KB
python tools/kb.py search "websocket"
python tools/kb.py search --category python --severity high

# Stats & validate
python tools/kb.py stats
python tools/kb.py validate .

# Export
python tools/kb.py export --format json --output kb.json
```

**📘 Complete CLI Reference:** `@references/cli-reference.md`

### ⚠️ Shared KB Updates

**CRITICAL:** When updating Shared KB submodule (`.kb/shared/`):

1. **Read:** `@for-claude-code/AGENT-UPDATE-INSTRUCTIONS.md` (strict rules)
2. **Follow:** `@for-claude-code/KB-UPDATE-QUICK-REFERENCE.md` (quick reference)

**🚨 3 Golden Rules:**
- ⛔ **NEVER** modify files in `.kb/shared/` (submodule is read-only)
- ✅ **DATA** is source of truth (if tool breaks → tool has bug)
- ❓ **When unsure** → ASK, don't fix

**Common mistakes to avoid:**
- ❌ Don't edit `_domain_index.yaml` to "fix" format
- ❌ Don't add fields not in v4.0.0 specification
- ✅ Do check upstream if tool fails
- ✅ Do report tool bugs to Shared KB repository

**📘 Full instructions:** `@for-claude-code/AGENT-UPDATE-INSTRUCTIONS.md`

---

## Project Integration

For instructions on integrating Shared KB into your project, see **[docs/integration/BOOTSTRAP.md](docs/integration/BOOTSTRAP.md)**.

This guide covers:
- Git submodule setup
- Project context configuration (PROJECT.yaml)
- Claude Code hooks installation
- Verification and troubleshooting

---

## Architecture

### Scope Hierarchy

1. **`universal/`** - Cross-language patterns
2. **`<language>/`** - Language-specific (python, javascript, docker, postgresql)
3. **`framework/`** - Framework-specific
4. **`project/`** - Local only

**📘 Detailed Architecture:** `@references/architecture.md`

### Directory Structure

```
shared-knowledge-base/
├── domains/             # Knowledge entries by domain
│   ├── python/          # Python-specific errors/patterns
│   ├── javascript/      # JavaScript/Node.js
│   ├── docker/          # Docker/container
│   ├── postgresql/      # PostgreSQL
│   ├── universal/       # Cross-language patterns
│   ├── vps/             # VPS administration
│   └── catalog/         # Category catalog
├── tools/               # CLI tools
│   ├── kb.py            # v4.0 main CLI (index, search, stats)
│   ├── v5.1/            # v5.1 tools (kb_submit, kb_search, kb_curate)
│   └── skb-cli/         # Enterprise CLI (sku command)
├── tests/               # pytest test suite
├── docs/                # Documentation
│   ├── v5.1/            # v5.1 architecture & workflows
│   └── research/        # Research & patterns
├── agents/              # Agent configurations
└── .claude/             # This config
```

---

## Documentation

| File | Purpose |
|------|---------|
| **README.md** | Project overview |
| **QUICKSTART.md** | 5-minute setup |
| **for-claude-code/README.md** | Claude Code guide |

**Research docs:** `@docs/research/claude-code/` (23 files, ~16K lines)
- Master index: `INDEX.md`
- Hooks, Skills, Agents guides

**📘 All Docs:** `@references/architecture.md` - Complete documentation structure

---

## v5.1 Two-Tier Architecture

**New in v5.1:** Separate Project KB and Shared KB with controlled submission workflow.

### Tiers

| Tier | Scope | Storage | Access | Purpose |
|------|-------|---------|--------|---------|
| **Project KB** | Private | `.kb/project/` | RW (Direct) | Business logic, secrets, project architecture |
| **Shared KB** | Public/Org | `.kb/shared/` | RO (Submodule) | Universal patterns, languages, tooling |
| **Submission** | Transitional | GitHub Issues | Write-Only | Buffer for Shared KB proposals |

### Key Benefits

- ✅ **Safe Submission:** Project agents submit via GitHub Issues (no direct commits)
- ✅ **Auto Context:** SessionStart hook injects PROJECT.yaml context
- ✅ **Decision Criteria:** `sharing_criteria` guides local vs shared decisions
- ✅ **PyGithub Integration:** No `gh` CLI dependency

**📘 Complete Architecture:** `@docs/v5.1/ARD.md`

---

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_domain_index_validation.py

# Run with verbose output
python -m pytest -v tests/

# Run with coverage
python -m pytest --cov=tools tests/
```

**Test requirements:** `pytest` (installed globally or via venv)

---

## v5.1 Tools

**New v5.1 tools** for two-tier KB management (in `tools/`):

### kb_submit.py
Submit knowledge entries to Project KB or Shared KB.

```bash
# Save to local Project KB (direct commit)
python tools/kb_submit.py --target local --file solution.yaml

# Submit to Shared KB via GitHub Issue
python tools/kb_submit.py \
    --target shared \
    --file solution.yaml \
    --title "Docker compose healthcheck fix" \
    --desc "Container becomes healthy before DB is ready" \
    --domain docker
```

### kb_search.py
Search knowledge entries across Project and Shared KB.

```bash
# Search all KBs
python tools/kb_search.py "docker compose"

# Search only Shared KB
python tools/kb_search.py "fastapi cors" --scope shared

# Search only Project KB
python tools/kb_search.py "stripe webhook" --scope project

# Show statistics
python tools/kb_search.py --stats
```

### kb_curate.py
Curator tool for processing GitHub Issue submissions.

```bash
# List pending submissions
python tools/kb_curate.py --mode list

# Validate specific submission
python tools/kb_curate.py --mode validate --issue 123

# Approve submission
python tools/kb_curate.py --mode approve --issue 123

# Reject submission
python tools/kb_curate.py --mode reject --issue 123 --reason "Duplicate"
```

**📘 Complete v5.1 Tools Reference:** `@docs/v5.1/README.md#tools`

---

## Knowledge Entry Format

**Minimal YAML entry:**
```yaml
version: "1.0"
category: "category-name"
last_updated: "2026-01-07"

errors:
  - id: "ERROR-001"        # CATEGORY-NNN
    title: "Error Title"
    severity: "high"       # critical | high | medium | low
    scope: "python"        # universal | python | javascript | docker | postgresql
    problem: |             # Required
      What went wrong
    solution:              # Required
      code: |
        # Solution
      explanation: |
        How it works
```

**📘 Complete YAML Standards:** `@standards/yaml-standards.md` - ID format, scope definitions, quality requirements

---

## Critical Workflows

### When User Reports an Error

1. **Search KB:** `python tools/kb.py search "error"`
2. **If not found:** Solve → Document → Determine scope
3. **Universal scope** (docker, universal, python, postgresql, javascript):
   - Validate: `python tools/kb.py validate <file>`
   - IMMEDIATELY commit & push to shared repo
   - Rebuild index: `python tools/kb.py index --force -v`
4. **Project-specific:** Keep in local KB, mark `local_only: true`

**📘 Detailed Workflows:** `@references/workflows.md` - Complete step-by-step guides

### Scope Decision

**Shared repository** if: universal scope, multi-project solution, industry standard
**Local KB** if: project/domain/framework scope, environment-specific, business logic

---

## Advanced Features

**Metadata & Analytics:**
```bash
python tools/kb.py init-metadata      # Initialize metadata
python tools/kb.py detect-changes     # Detect modifications
python tools/kb.py check-freshness    # Check staleness
python -m tools.kb_versions check --all  # Version monitoring
python -m tools.kb_predictive predict-updates --days 30  # Predictions
```

**📘 Complete Reference:** `@references/cli-reference.md` - All advanced commands

---

## Claude Code Hooks

**Deterministic automation at workflow points:**
- **PreToolUse** - Before tool calls (validation, blocking)
- **PostToolUse** - After tool calls (formatting, testing)
- **SessionStart** - Session setup
- **Stop** - Quality validation

**Current hooks:** YAML validation, quality gates, auto-formatting

**📘 Learn more:** `@docs/research/claude-code/claude-hooks-guide.md`

---

## Patterns & Best Practices

**Available Patterns:** `@universal/patterns/`
- `claude-code-files-organization-001.yaml` - .claude/ organization
- `claude-code-shared-model.yaml` - Team knowledge model
- `PROGRESSIVE-DISCLOSURE-001` - Progressive disclosure

**Best Practices:**
1. Keep CLAUDE.md lean (~300 lines) ✅
2. Progressive disclosure - load details on demand
3. Single source of truth - avoid duplication
4. Commit .claude/ to git - share with team
5. Quality gate - minimum 75/100 for shared repo

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Search no results | `python tools/kb.py index --force -v` |
| Validation fails | Check syntax: `python tools/kb.py validate <file>` |
| Hook not executing | Check `.claude/settings.json` |
| Metadata missing | `python tools/kb.py init-metadata` |

**📘 Detailed Troubleshooting:** `@references/workflows.md`

---

## Related Resources

**Internal:**
- `@for-claude-code/README.md` - Complete Claude Code guide
- `@docs/research/claude-code/` - Research & best practices
- `@references/` - CLI, architecture, workflows reference
- `@standards/` - Git, YAML, quality standards

**External:**
- [Claude Code Documentation](https://claude.com/claude-code)
- [Shared KB Repository](https://github.com/ozand/shared-knowledge-base)

---

## Agent Configuration

**Auto-loaded:** `universal/agent-instructions/base-instructions.yaml`
- Role: Knowledge Base Curator (`.curator` marker)
- GitHub attribution: GITHUB-ATTRIB-001
- Quality standards: 75/100 minimum
- Hooks configuration

**Current:** claude-code agent, Curator role

---

**Version:** 5.1.0
**Quality Score:** 90/100
