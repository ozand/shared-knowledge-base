# Shared Knowledge Base - Claude Code Instructions

**Repository:** shared-knowledge-base
**Version:** 3.0 (with Phase 1-3 metadata features)
**Last Updated:** 2026-01-07

---

## Overview

This is the **Shared Knowledge Base** repository - a centralized knowledge base containing verified solutions for common software development errors across multiple languages and frameworks.

**Key characteristic:** This is a **knowledge repository**, not an executable application. The main artifact is the `kb.py` CLI tool that manages knowledge entries stored as YAML files.

---

## Quick Start

### Essential Commands

```bash
# Build search index (required after any changes)
python tools/kb.py index -v

# Search knowledge base
python tools/kb.py search "websocket"
python tools/kb.py search --category python --severity high
python tools/kb.py search --tags async pytest

# Show statistics
python tools/kb.py stats

# Validate knowledge entries
python tools/kb.py validate path/to/file.yaml
python tools/kb.py validate .  # Validate all

# Export for AI tools
python tools/kb.py export --format json --output kb.json
```

### Dependencies

```bash
# Install Python dependency
pip install pyyaml
```

---

## Repository Architecture

### Hierarchical Knowledge Organization

Knowledge is organized by scope levels (from most universal to most specific):

1. **`universal/`** - Cross-language patterns (Git, testing, architecture, filesystem)
2. **`<language>/`** - Language-specific (python, javascript, docker, postgresql)
3. **`framework/<name>/`** - Framework-specific (django, fastapi, react, vue)
4. **`project/`** - Project-specific (NOT shared, local only)

### Directory Structure

```
shared-knowledge-base/
├── python/              # Python-specific errors & patterns
│   ├── errors/
│   └── patterns/
├── javascript/          # JavaScript/Node.js
│   ├── errors/
│   └── patterns/
├── docker/              # Docker/container
│   └── errors/
├── postgresql/          # PostgreSQL
│   ├── errors/
│   ├── patterns/
│   └── tools/
├── universal/           # Cross-language
│   ├── errors/
│   ├── patterns/
│   └── agent-instructions/  # AI agent configuration
├── framework/           # Framework-specific
│   ├── django/
│   ├── fastapi/
│   ├── react/
│   └── vue/
├── tools/               # Enhanced tooling (v3.0)
│   ├── kb.py           # Main CLI tool
│   ├── kb_meta.py      # Metadata manager
│   ├── kb_usage.py     # Usage tracker
│   └── ...
├── curator/             # Knowledge Base Curator docs
├── for-claude-code/     # Claude Code integration
├── docs/research/       # Research & best practices
└── .claude/             # Claude Code configuration (this file)
```

---

## Documentation Structure

### User-Facing Documentation

| File | Purpose | Lines |
|------|---------|-------|
| **README.md** | Project overview, features, quick start | ~600 |
| **QUICKSTART.md** | 5-minute setup guide | ~300 |
| **GUIDE.md** | Implementation guide | ~600 |

### Claude Code Integration

| File | Purpose | Lines |
|------|---------|-------|
| **for-claude-code/README.md** | Complete Claude Code guide (v3.0) | ~550 |
| **for-claude-code/CLAUDE.md** | Workflow instructions | ~380 |

**📘 Start here:** `@for-claude-code/README.md` - Complete guide for using Shared KB with Claude Code

### Research & Best Practices

**Location:** `docs/research/claude-code/`

**Master Index:** `@docs/research/claude-code/INDEX.md` - Complete documentation index
**Quick Reference:** `@docs/research/claude-code/README.md` - Organized guide listing

| File | Purpose | Lines | Language |
|------|---------|-------|----------|
| **claude-shared-architecture.md** | Shared model architecture, scope system | ~1400 | English |
| **claude-hooks-guide.md** | Complete hooks guide (10 events, patterns) | ~1200 | English |
| **claude-hooks-examples.md** | 10 production-ready hook examples | ~800 | English |
| **claude-hooks-advanced.md** | Anti-patterns & advanced strategies | ~700 | English |
| **claude-skills-guide.md** | Skills system documentation | ~1300 | English |
| **claude-agents-guide.md** | Agents system documentation | ~1100 | English |
| **claude-templates.md** | Template system | ~600 | English |
| **claude-troubleshooting.md** | Troubleshooting guide | ~300 | English |
| **CLAUDE-COMPLETE-PRACTICES.md** | Complete overview of all practices | ~1100 | Russian |
| **CLAUDE-CLAUDE-MD-GUIDE.md** | CLAUDE.md project memory guide | ~1400 | English |
| **CLAUDE-PERMISSION-MODES-GUIDE.md** | Permission modes (ALLOW, DITTO, AUTO, CONFIRM) | ~1300 | Russian |
| **CLAUDE-SLASH-COMMANDS-GUIDE.md** | Custom slash commands | ~1400 | Russian |
| **CLAUDE-MCP-GUIDE.md** | MCP (Model Context Protocol) | ~740 | Russian |
| **CLAUDE-PLANNING-WORKFLOW-GUIDE.md** | Planning mode workflow | ~770 | Russian |
| **CLAUDE-PROJECTS-COLLABORATION-GUIDE.md** | Projects & team collaboration | ~940 | Russian |
| **CLAUDE-REFERENCING-CONTEXT-GUIDE.md** | @ Referencing for context | ~820 | Russian |

**Total:** ~16,100 lines of Claude Code documentation (23 files)

**📘 For automation:** `@docs/research/claude-code/claude-hooks-guide.md` - Hooks for deterministic workflow automation
**📘 Start here:** `@docs/research/claude-code/INDEX.md` - Master documentation index

### Knowledge Base Curator Documentation

**Location:** `curator/`

| File | Purpose |
|------|---------|
| **AGENT.md** | Curator role definition and responsibilities |
| **SKILLS.md** | Available curators skills |
| **WORKFLOWS.md** | Standard operating procedures |
| **QUALITY_STANDARDS.md** | Entry quality rubric (0-100) |
| **PROMPTS.md** | Reusable AI prompt templates |
| **metadata/** | Metadata system architecture |

---

## Knowledge Entry Format

Each entry is a YAML file with this structure:

```yaml
version: "1.0"
category: "category-name"
last_updated: "2026-01-07"

errors:
  - id: "ERROR-001"           # Unique ID: CATEGORY-NNN
    title: "Error Title"
    severity: "high"          # critical | high | medium | low
    scope: "python"           # universal | python | javascript | docker | postgresql | framework

    problem: |
      Description of what went wrong

    symptoms:
      - "Error message or symptom"

    root_cause: |
      Explanation of why it happens

    solution:
      code: |
        # Correct code example

      explanation: |
        How the solution works

    prevention:
      - "How to avoid this error"

    tags: ["tag1", "tag2"]
```

**Required fields:** `id`, `title`, `severity`, `scope`, `problem`, `solution`

---

## Critical Workflows

### When User Reports an Error

1. **Search KB first:**
   ```bash
   python tools/kb.py search "error message"
   ```

2. **If found:** Return solution ✅

3. **If not found:**
   - Solve problem
   - Document in YAML
   - Determine scope (see below)

4. **If scope is universal** (docker, universal, python, postgresql, javascript):
   - Create in `shared-knowledge-base/<scope>/errors/`
   - Validate: `python tools/kb.py validate <file>`
   - Initialize metadata: `python tools/kb.py init-metadata`
   - **IMMEDIATELY commit and push:**
     ```bash
     git add <file> *_meta.yaml
     git commit -m "Add ERROR-ID: Title"
     git push origin main
     ```
   - Rebuild index: `python tools/kb.py index --force -v`

5. **If scope is project-specific:**
   - Create in local KB
   - Mark with `local_only: true`
   - Do NOT push to shared repository

### Scope Decision Criteria

**Add to SHARED KB if:**
- Error is: docker, universal, python, postgresql, javascript scope
- Solution applies to multiple projects/environments
- Error is common across industry
- Framework-agnostic or standard use case

**Keep in LOCAL KB if:**
- Error is: project, domain, framework scope
- Solution depends on specific infrastructure
- Environment-specific or one-time occurrence
- Business logic specific

---

## Advanced Features (v3.0)

### Metadata Commands

```bash
# Initialize metadata for all entries
python tools/kb.py init-metadata

# Detect changes since last check
python tools/kb.py detect-changes

# Check entry freshness
python tools/kb.py check-freshness

# Analyze usage patterns
python tools/kb.py analyze-usage

# Update entry metadata
python tools/kb.py update-metadata --entry-id ERROR-ID --quality-score 85

# Reindex metadata
python tools/kb.py reindex-metadata
```

### Version Monitoring

```bash
# Check specific library version
python -m tools.kb_versions check --library fastapi

# Check all libraries
python -m tools.kb_versions check --all

# Scan KB for tested versions
python -m tools.kb_versions scan
```

### Predictive Analytics

```bash
# Predict updates needed
python -m tools.kb_predictive predict-updates --days 30

# Suggest new entries based on search gaps
python -m tools.kb_predictive suggest-entries

# Estimate quality for entry
python -m tools.kb_predictive estimate-quality --entry-id ERROR-001
```

---

## Claude Code Hooks (NEW!)

This repository uses **Claude Code Hooks** for deterministic workflow automation.

### What are Hooks?

Hooks are guaranteed shell/LLM executions at specific workflow points:
- **PreToolUse** - Before any tool call (validation, blocking)
- **PostToolUse** - After successful tool call (formatting, testing)
- **SessionStart** - When session starts (setup, context loading)
- **Stop** - When Claude finishes (quality validation)

### Current Hooks Configuration

See `.claude/settings.json` for active hooks:
- **YAML Validation** - Automatic validation before commits
- **Quality Gates** - Ensure entry quality standards
- **Auto-formatting** - Consistent YAML formatting

### Hooks Documentation

**📘 Learn more:** `@docs/research/claude-code/claude-hooks-guide.md` - Complete hooks reference
**📘 Examples:** `@docs/research/claude-code/claude-hooks-examples.md` - Production-ready scripts
**📘 Pattern:** `@universal/patterns/claude-code-hooks.yaml` - Integration pattern

---

## Patterns & Best Practices

### Available Patterns

**Location:** `universal/patterns/`

| Pattern | Purpose |
|---------|---------|
| **claude-code-shared-model.yaml** | Shared knowledge model for teams |
| **claude-code-hooks.yaml** | Hooks automation pattern |
| **agent-role-separation.yaml** | Project Agent vs Curator roles |
| **agent-handoff.yaml** | Cross-repository collaboration |
| **yaml-syntax.yaml** | YAML best practices |

### Key Best Practices

1. **Keep root CLAUDE.md lean** (~300 lines) - Acts as navigation hub
2. **Use progressive disclosure** - Load details on demand
3. **Single source of truth** - Avoid duplication
4. **Commit .claude/ to git** - Share configuration with team
5. **Quality gate** - Minimum score 75/100 before committing to shared repository

---

## Troubleshooting

### Common Issues

**Issue:** Search returns no results
- **Fix:** Rebuild index: `python tools/kb.py index --force -v`

**Issue:** YAML validation fails
- **Fix:** Check syntax: `python tools/kb.py validate <file>`

**Issue:** Hook not executing
- **Fix:** Check `.claude/settings.json` syntax, test hook manually

**Issue:** Metadata not initialized
- **Fix:** Run: `python tools/kb.py init-metadata`

---

## Related Resources

### Internal Documentation
- `for-claude-code/README.md` - Complete Claude Code guide
- `docs/research/claude-code/` - Research & best practices
- `curator/AGENT.md` - Curator role definition

### External Resources
- [Claude Code Documentation](https://claude.com/claude-code)
- [Shared KB Repository](https://github.com/ozand/shared-knowledge-base)

---

## Agent Configuration

**Auto-loaded instructions:** `universal/agent-instructions/base-instructions.yaml`
- Role-based access control (Project Agent vs Curator)
- GitHub attribution requirements (GITHUB-ATTRIB-001)
- Quality standards and workflows
- Hooks configuration rules

**Current agent type:** claude-code
**Current role:** Knowledge Base Curator (`.curator` marker exists)

---

**Version:** 3.0
**Last Updated:** 2026-01-07
**Maintained By:** Development Team & Claude Code
**Quality Score:** 90/100
