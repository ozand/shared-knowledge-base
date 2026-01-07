# Shared KB Architecture Reference

**Detailed architecture and structure documentation**

---

## Hierarchical Knowledge Organization

Knowledge is organized by **scope levels** (from most universal to most specific):

### Scope Hierarchy

```
1. universal/      (Most universal)
   ↓
2. <language>/     (Language-specific)
   ↓
3. framework/      (Framework-specific)
   ↓
4. project/        (Most specific, NOT shared)
```

### Scope Definitions

| Scope | Description | Examples | Shared? |
|-------|-------------|----------|---------|
| **universal** | Cross-language patterns | Git, testing, architecture, filesystem | ✅ Yes |
| **python** | Python-specific | asyncio, pytest, django-agnostic | ✅ Yes |
| **javascript** | JavaScript/Node.js | npm, async/await, ES6 | ✅ Yes |
| **docker** | Docker/container | Dockerfile, docker-compose | ✅ Yes |
| **postgresql** | PostgreSQL | SQL, indexing, replication | ✅ Yes |
| **framework** | Framework-specific | Django, FastAPI, React | ❌ No |
| **domain** | Domain-specific | Business logic, industry-specific | ❌ No |
| **project** | Project-specific | Local infrastructure, one-off | ❌ No |

**Key Rule:** If scope is **universal**, **docker**, **python**, **postgresql**, or **javascript** → MUST be pushed to shared repository immediately.

---

## Directory Structure

```
shared-knowledge-base/
├── python/                    # Python-specific errors & patterns
│   ├── errors/
│   │   ├── async/
│   │   ├── testing/
│   │   └── yaml-001.yaml
│   └── patterns/
│       ├── async/
│       └── testing/
│
├── javascript/                # JavaScript/Node.js
│   ├── errors/
│   └── patterns/
│
├── docker/                    # Docker/container
│   └── errors/
│       ├── encoding/
│       └── emoji-encoding-powershell.yaml
│
├── postgresql/                # PostgreSQL
│   ├── errors/
│   ├── patterns/
│   └── tools/
│
├── universal/                 # Cross-language
│   ├── errors/
│   │   ├── git/
│   │   └── documentation/
│   ├── patterns/
│   │   ├── claude-code-files-organization-001.yaml
│   │   ├── claude-code-hooks.yaml
│   │   └── progressive-disclosure-001.yaml
│   └── agent-instructions/    # AI agent configuration
│       └── base-instructions.yaml
│
├── framework/                 # Framework-specific
│   ├── django/
│   ├── fastapi/
│   ├── react/
│   └── vue/
│
├── tools/                     # Enhanced tooling (v3.0)
│   ├── kb.py                 # Main CLI tool
│   ├── kb_meta.py            # Metadata manager
│   ├── kb_usage.py           # Usage tracker
│   ├── kb_versions.py        # Version monitoring
│   ├── kb_predictive.py      # Predictive analytics
│   ├── search-kb.py          # Legacy search (deprecated)
│   ├── sync-knowledge.py     # Sync tool
│   └── validate-kb.py        # Validation tool
│
├── curator/                   # Knowledge Base Curator docs
│   ├── AGENT.md              # Curator role definition
│   ├── SKILLS.md             # Available skills
│   ├── WORKFLOWS.md          # Standard procedures
│   ├── QUALITY_STANDARDS.md  # Quality rubric (0-100)
│   ├── PROMPTS.md            # Reusable prompts
│   └── metadata/             # Metadata system docs
│       ├── ARCHITECTURE.md
│       ├── IMPLEMENTATION.md
│       └── SUMMARY.md
│
├── for-claude-code/           # Claude Code integration
│   ├── README.md             # Complete guide (v3.0)
│   └── CLAUDE.md             # Workflow instructions
│
├── docs/                      # Documentation
│   ├── research/             # Research & best practices
│   │   └── claude-code/      # Claude Code research
│   │       ├── INDEX.md      # Master index
│   │       ├── README.md     # Quick reference
│   │       ├── claude-hooks-guide.md
│   │       ├── claude-skills-guide.md
│   │       └── archive/      # Archived docs
│   ├── archive/              # Deprecated/obsolete
│   └── guides/               # Detailed guides
│
├── .claude/                   # Claude Code configuration
│   ├── CLAUDE.md             # Project memory (~300 lines)
│   ├── settings.json         # Configuration
│   ├── skills/               # Procedural knowledge
│   ├── commands/             # Slash commands
│   ├── hooks/                # Lifecycle automation
│   ├── agents/               # Autonomous agents
│   ├── standards/            # Team standards
│   └── references/           # Reference docs
│
├── .kb-config.yaml            # Configuration template
├── README.md                  # User-facing overview
├── QUICKSTART.md              # 5-minute setup guide
└── GUIDE.md                   # Implementation guide
```

---

## Documentation Structure

### User-Facing Documentation

| File | Purpose | Lines | Audience |
|------|---------|-------|----------|
| **README.md** | Project overview, features, quick start | ~600 | All users |
| **QUICKSTART.md** | 5-minute setup guide | ~300 | New users |
| **GUIDE.md** | Implementation guide | ~600 | Implementers |

### Claude Code Integration

| File | Purpose | Lines | Audience |
|------|---------|-------|----------|
| **for-claude-code/README.md** | Complete Claude Code guide (v3.0) | ~550 | Claude Code users |
| **for-claude-code/CLAUDE.md** | Workflow instructions | ~380 | Claude Code users |

**📘 Start here:** `@for-claude-code/README.md`

### Research & Best Practices

**Location:** `docs/research/claude-code/`

**Master Index:** `@docs/research/claude-code/INDEX.md`
**Quick Reference:** `@docs/research/claude-code/README.md`

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

**📘 For automation:** `@docs/research/claude-code/claude-hooks-guide.md`
**📘 Start here:** `@docs/research/claude-code/INDEX.md`

### Knowledge Base Curator Documentation

**Location:** `curator/`

| File | Purpose | Lines |
|------|---------|-------|
| **AGENT.md** | Curator role definition and responsibilities | ~400 |
| **SKILLS.md** | Available curators skills | ~500 |
| **WORKFLOWS.md** | Standard operating procedures | ~600 |
| **QUALITY_STANDARDS.md** | Entry quality rubric (0-100) | ~300 |
| **PROMPTS.md** | Reusable AI prompt templates | ~400 |
| **metadata/** | Metadata system architecture | ~800 |

---

## Search Technology

### SQLite FTS5 (Full-Text Search)

**Why SQLite FTS5?**
- Handles 1M+ entries with sub-second search times
- Automatic indexing on `kb.py index`
- Cross-platform compatible (Windows/Mac/Linux)
- Zero external dependencies

**Index Structure:**
```sql
CREATE VIRTUAL TABLE kb_search USING fts5(
    entry_id,
    title,
    category,
    scope,
    severity,
    problem,
    solution,
    tags,
    file_path
);
```

**Search Features:**
- Full-text search across all fields
- Boolean queries (AND, OR, NOT)
- Phrase queries ("exact phrase")
- Proximity searches ("query" NEAR/10 "other")
- Filter by category, severity, scope, tags

---

## Metadata Architecture (v3.0)

### Metadata Files

Each YAML entry has a corresponding `*_meta.yaml` file:

```yaml
# python/errors/async/await-in-event-loop.yaml_meta.yaml

entry_id: "ASYNC-001"
file_path: "python/errors/async/await-in-event-loop.yaml"
metadata:
  quality_score: 85              # 0-100
  usage_count: 42                # Times accessed
  last_used: "2026-01-07"
  created_at: "2025-06-15"
  last_updated: "2026-01-07"
  tested_versions:               # Library versions tested
    - library: "python"
      version: "3.11+"
  review_status: "reviewed"      # reviewed | needs_review | outdated
  freshness_days: 215            # Days since last update
  indexed: true                  # In search index
```

### Metadata Operations

**Initialize:**
```bash
python tools/kb.py init-metadata
```

**Update:**
```bash
python tools/kb.py update-metadata --entry-id ERROR-001 --quality-score 85
```

**Analyze:**
```bash
python tools/kb.py analyze-usage
```

---

## Version Control Strategy

### Git Integration

**Shared Repository:**
- Remote: `https://github.com/ozand/shared-knowledge-base`
- Branch: `main`
- Protection: No force push, require PR review

**Commit Workflow:**
```bash
# 1. Validate changes
python tools/kb.py validate .

# 2. Rebuild index
python tools/kb.py index --force -v

# 3. Commit with conventional format
git add <files>
git commit -m "Add ERROR-ID: Title

- Brief description
- Related issues
- Real-world example

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# 4. Push immediately for universal scopes
git push origin main

# 5. If conflicts:
git pull --rebase origin main
git push origin main
```

### Git Submodule Integration

**Add to project:**
```bash
cd your-project
git submodule add https://github.com/ozand/shared-knowledge-base docs/knowledge-base/shared
cd docs/knowledge-base/shared
git submodule update --init --recursive
```

**Update submodule:**
```bash
# In parent project
git submodule update --remote docs/knowledge-base/shared
```

**Commit submodule update:**
```bash
git add docs/knowledge-base/shared
git commit -m "Update shared-knowledge-base to latest"
```

---

## Quality Architecture

### Quality Scoring Rubric (0-100)

**Completeness (40 points):**
- All required fields present: 10 points
- Detailed problem description: 10 points
- Comprehensive solution: 10 points
- Prevention strategies: 10 points

**Accuracy (30 points):**
- Code examples tested: 15 points
- Root cause correct: 15 points

**Usability (20 points):**
- Clear explanation: 10 points
- Actionable solution: 10 points

**Maintainability (10 points):**
- Up-to-date versions: 5 points
- Fresh content (<180 days): 5 points

**Minimum score for shared repository:** 75/100

---

## Claude Code Integration Architecture

### .claude/ Directory Structure

```
.claude/
├── CLAUDE.md                  # Project memory (~300 lines)
├── settings.json              # Configuration
├── skills/                    # Procedural knowledge
│   └── {skill-name}/
│       ├── SKILL.md          # 200-500 lines
│       ├── resources/        # Detailed content
│       └── scripts/          # Optional automation
├── agents/                    # Autonomous agents
│   ├── {agent-name}.md
│   └── subagents/
├── commands/                  # Slash commands
├── hooks/                     # Lifecycle automation
├── standards/                 # Team standards
├── references/                # Reference docs
└── memory/                    # Persistent memory
```

### Progressive Disclosure Pattern

**Metadata at startup:** ~30-50 tokens per skill
**Full content on-demand:** 500-2000 tokens when relevant

**Example:**
```yaml
---
name: "kb-search"
description: "Search knowledge base for entries"
version: "1.0"
---

# KB Search Skill

## Quick Start (10 lines)
## Core Workflow (50 lines)
→ See: @resources/advanced-search-patterns.md

Total SKILL.md: ~150 lines
Detailed resources/: 500+ lines (loaded on demand)
```

**Token efficiency:** 60%+ reduction vs loading all content

---

**Version:** 3.0
**Last Updated:** 2026-01-07
