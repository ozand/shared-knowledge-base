# Shared Knowledge Base - Claude Code Instructions

**Repository:** shared-knowledge-base
**Version:** 3.0
**Last Updated:** 2026-01-07

---

## Overview

Centralized knowledge base containing verified solutions for common software development errors across multiple languages and frameworks. Managed by `kb.py` CLI tool with YAML entries.

**📘 Complete Guide:** `@for-claude-code/README.md`

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
├── python/              # Language-specific
├── universal/           # Cross-language
├── tools/               # kb.py CLI
├── curator/             # Curator docs
├── for-claude-code/     # Claude Code integration
├── docs/research/       # Research & patterns
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

## Advanced Features (v3.0)

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

**Version:** 3.0
**Quality Score:** 90/100
