# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the **Shared Knowledge Base** repository - a centralized, version 2.0 "Hybrid Approach" knowledge base containing verified solutions for common software development errors across multiple languages and frameworks. It's designed as a standalone repository that other projects can integrate via git submodules or direct cloning.

**Key characteristic:** This is a **knowledge repository**, not an executable application. The main artifact is the `kb.py` CLI tool that manages knowledge entries stored as YAML files.

## Architecture

### Hierarchical Knowledge Organization

Knowledge is organized by scope levels (from most universal to most specific):

1. **`universal/`** - Cross-language patterns (Git, testing, architecture, filesystem)
2. **`<language>/`** - Language-specific (python, javascript, docker, postgresql)
3. **`framework/<name>/`** - Framework-specific (django, fastapi, react, vue)
4. **`project/`** - Project-specific (NOT shared, local only)

### Directory Structure

```
shared-knowledge-base/
├── python/
│   ├── errors/          # Python error patterns
│   └── patterns/        # Python best practices
├── javascript/
│   ├── errors/
│   └── patterns/
├── docker/
│   └── errors/
├── postgresql/
│   ├── errors/
│   ├── patterns/
│   └── tools/
├── universal/
│   ├── errors/
│   └── patterns/
├── framework/
│   ├── django/
│   ├── fastapi/
│   ├── react/
│   └── vue/
├── tools/
│   ├── kb.py           # Main CLI tool (v2.0)
│   ├── search-kb.py    # Legacy search
│   ├── sync-knowledge.py
│   └── validate-kb.py
├── .kb-config.yaml     # Configuration template
├── README.md           # User documentation
├── QUICKSTART.md       # Setup guide
└── FOR_CLAUDE_CODE.md  # Claude Code workflow instructions
```

## Essential Commands

### Build/Run/Search

```bash
# Build search index (required after any changes)
python tools/kb.py index -v

# Search knowledge base
python tools/kb.py search "keyword"
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

# Or with uv
uv add pyyaml --optional dev
```

## Knowledge Entry Format

Each entry is a YAML file with this structure:

```yaml
version: "1.0"
category: "category-name"
last_updated: "2026-01-05"

errors:
  - id: "ERROR-001"           # Unique ID: CATEGORY-NNN
    title: "Error Title"
    severity: "high"          # critical | high | medium | low
    scope: "python"           # universal | python | javascript | docker | postgresql | framework | domain | project

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

## Critical Workflow: Adding Universal Errors

When adding knowledge entries with these scopes: **docker, universal, python, postgresql, javascript**

**YOU MUST:**

1. **Create file in SHARED KB** (not local):
   ```bash
   # ✅ CORRECT
   path/to/project/docs/knowledge-base/shared/<scope>/errors/<file>.yaml

   # ❌ WRONG
   path/to/project/docs/knowledge-base/<scope>/errors/<file>.yaml
   ```

2. **Validate the YAML:**
   ```bash
   python3 path/to/project/docs/knowledge-base/tools/kb.py validate path/to/project/docs/knowledge-base/shared/
   ```

3. **IMMEDIATELY commit and push to shared repository:**
   ```bash
   cd path/to/project/docs/knowledge-base/shared
   git add <file>
   git commit -m "Add ERROR-ID: Error Title

   - Brief description
   - Related issues
   - Real-world example

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

   git push origin main

   # If push fails with conflicts:
   git pull --rebase origin main
   git push origin main
   ```

4. **Rebuild index:**
   ```bash
   python3 path/to/project/docs/knowledge-base/tools/kb.py index --force -v
   ```

5. **Confirm to user:**
   ```
   ✅ KB entry added to shared-knowledge-base repository
   📦 Committed: <commit-hash>
   🚀 Pushed to: origin/main
   🔍 Index rebuilt
   🌐 Available at: https://github.com/ozand/shared-knowledge-base
   ```

**For project-specific errors** (scope: project, domain, framework):
- Create in local KB: `docs/knowledge-base/<scope>/errors/`
- Add metadata: `local_only: true`
- Do NOT push to shared repository

## Search Technology

The knowledge base uses **SQLite FTS5 (Full-Text Search)** for scalability:
- Handles 1M+ entries with sub-second search times
- Automatic indexing on `kb.py index`
- Cross-platform compatible (Windows/Mac/Linux)

## Key Design Principles

1. **AI-agnostic:** Works with Claude Code, GitHub Copilot, Cursor, Roo Code
2. **Hierarchical scoping:** Universal → Language → Framework → Domain → Project
3. **Validation-first:** All entries must validate before committing
4. **Immediate synchronization:** Universal errors must be pushed to shared repo immediately
5. **Git-based distribution:** Designed for git submodule integration

## Testing Infrastructure

No formal test suite exists. Validation is done through `kb.py validate` which checks:
- YAML syntax correctness
- Required fields presence
- ID format compliance (CATEGORY-NNN)
- Duplicate detection

## Configuration

The `.kb-config.yaml` file controls:
- Paths to KB directories
- Shared repository sources
- Import scopes (which scopes to sync)
- Search settings
- AI tool integration preferences

Default location: `docs/knowledge-base/.kb-config.yaml`

## Common Patterns

### When User Reports an Error

1. Search KB first: `python tools/kb.py search "error message"`
2. If found → Return solution
3. If not found → Solve problem, document in YAML, determine scope
4. **CRITICAL:** If scope is universal (docker, universal, python, postgresql, javascript):
   - Create in `/docs/knowledge-base/shared/<scope>/`
   - Validate YAML
   - IMMEDIATELY `git add`, `git commit`, `git push` to shared repo
   - Rebuild index
   - Confirm sync status to user
5. If scope is project-specific:
   - Create in `/docs/knowledge-base/<scope>/`
   - Mark with `local_only: true`
   - Rebuild index
   - Inform user it's local only

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

## Documentation Files

- **README.md** - User-facing overview
- **QUICKSTART.md** - 5-minute setup guide
- **FOR_CLAUDE_CODE.md** - Detailed Claude Code workflow instructions (CRITICAL)
- **GUIDE.md** - Implementation guide
- **MIGRATION_TO_HYBRID_RU.md** - Migration documentation

## Important Notes

- This repository is meant to be integrated as a **git submodule** in other projects
- The `kb.py` tool is the primary interface for managing knowledge
- Always rebuild index after modifying YAML files
- Universal scope entries **must** be synchronized to the shared repository immediately
- Never use `git push --force` to resolve conflicts - use `git pull --rebase`
