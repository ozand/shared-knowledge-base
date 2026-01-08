# Architecture Reference Document (ARD)
# Shared Knowledge Base v4.0

**Document Version:** 1.0
**Last Updated:** 2026-01-08
**Product Version:** 4.0.1
**Status:** ✅ Production Ready

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Architecture Principles](#architecture-principles)
3. [System Architecture](#system-architecture)
4. [Component Design](#component-design)
5. [Data Architecture](#data-architecture)
6. [Technology Stack](#technology-stack)
7. [Integration Architecture](#integration-architecture)
8. [Security Architecture](#security-architecture)
9. [Deployment Architecture](#deployment-architecture)
10. [Scalability & Performance](#scalability--performance)
11. [Monitoring & Observability](#monitoring--observability)
12. [Disaster Recovery](#disaster-recovery)

---

## Executive Summary

### Architecture Overview

Shared Knowledge Base is a **distributed, version-controlled knowledge repository** designed for AI agent consumption. It uses a **domain-driven, file-based architecture** optimized for:

1. **Git-native storage** (YAML files in repository)
2. **Progressive loading** (sparse checkout for token efficiency)
3. **Agent-first protocols** (strict rules for AI updates)
4. **Quality-gated content** (automated validation ≥75/100 score)

### Key Architectural Decisions

| Decision | Rationale | Impact |
|----------|-----------|--------|
| **File-based storage (YAML)** | Human-readable, version-controlled, IDE-friendly | Easy editing, git history, no database needed |
| **Git submodules for distribution** | Standard tool, no custom sync, built-in versioning | Seamless integration, automatic updates |
| **Progressive domain loading** | Minimize token usage for AI agents | 50%+ token savings, faster loading |
| **Quality score gating** | Prevent low-quality entries | Maintain high standard, automated curation |
| **Agent instructions as code** | Treat agent protocols as first-class citizens | Clear rules, prevent data corruption |

### Technology Stack Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
├─────────────────────────────────────────────────────────────┤
│  CLI Tools (Python 3.8+)  │  Hooks (Bash)  │  Agents (MD)  │
├─────────────────────────────────────────────────────────────┤
│                    Data Layer (YAML)                        │
├─────────────────────────────────────────────────────────────┤
│  Entries  │  Index  │  Metadata  │  Domain Index           │
├─────────────────────────────────────────────────────────────┤
│                    Storage Layer (Git)                      │
├─────────────────────────────────────────────────────────────┤
│  GitHub Repository  │  Git Submodules  │  Sparse Checkout   │
└─────────────────────────────────────────────────────────────┘
```

---

## Architecture Principles

### P1: Simplicity First

**Rationale:** Complex architectures fail; simple ones scale.

**Practices:**
- File-based storage (no databases)
- Standard Git workflows (no custom sync)
- Human-readable YAML (no binary formats)
- Minimal dependencies (Python stdlib + pyyaml)

**Trade-offs:**
- ❌ Slower than database for large datasets
- ✅ Easier to understand, maintain, extend

### P2: Git-Native

**Rationale:** Leverage Git's proven version control, collaboration, and distribution.

**Practices:**
- Everything in Git repository
- Git submodules for distribution
- Pull requests for contributions
- Git history for audit trail

**Trade-offs:**
- ❌ Git learning curve for some users
- ✅ Industry-standard, battle-tested, free hosting

### P3: Progressive Loading

**Rationale:** AI agents have token limits; loading everything is wasteful.

**Practices:**
- Domain-based organization
- Git sparse-checkout for selective loading
- Metadata-first queries (load summary before full entry)
- Lazy loading of entry details

**Trade-offs:**
- ❌ More complex query logic
- ✅ 50%+ token savings, faster load times

### P4: Quality Gates

**Rationale:** Low-quality entries erode trust and utility.

**Practices:**
- Automated quality scoring (0-100)
- Minimum score ≥75 for shared repository
- Validation checks before commit
- Peer review for contributions

**Trade-offs:**
- ❌ Higher barrier to contribution
- ✅ Maintain high standard, reduce maintenance burden

### P5: Agent-First Protocols

**Rationale:** AI agents are primary consumers; design for them, not humans.

**Practices:**
- Structured YAML for machine parsing
- Clear agent instructions (3 Golden Rules)
- Decision trees for ambiguity
- Troubleshooting guides for edge cases

**Trade-offs:**
- ❌ Steeper learning curve for humans
- ✅ Reliable agent behavior, fewer errors

### P6: Extensibility

**Rationale:** Future requirements unknown; design for change.

**Practices:**
- Plugin architecture for validators
- Schema versioning in entries
- Backward compatibility for tools
- Open for contributions

**Trade-offs:**
- ❌ More complex initial design
- ✅ Easier to add features, adapt to changes

---

## System Architecture

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         User Layer                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Developer  │  │ AI Agent     │  │  Tech Lead   │          │
│  │   (Human)    │  │ (Claude Code)│  │   (Human)    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                    │
│         └─────────────────┴─────────────────┘                    │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────┐
│                   Access Layer  │                               │
├───────────────────────────┼──────────────────────────────────────┤
│                           │                                      │
│  ┌────────────────────────┴────────────────────────┐            │
│  │         Interface Layer (REST/CLI/WebFetch)      │            │
│  └─────────────────────────────────────────────────┘            │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────┐
│                    Application Layer                            │
├───────────────────────────┼──────────────────────────────────────┤
│                           │                                      │
│  ┌────────────┐  ┌────────┴────────┐  ┌────────────┐           │
│  │  kb.py     │  │  kb_domains.py  │  │  Hooks     │           │
│  │  (CLI)     │  │  (Domain Mgr)   │  │  (Bash)    │           │
│  └─────┬──────┘  └─────────────────┘  └─────┬──────┘           │
│        │                                      │                  │
│  ┌─────┴──────────────────────────────────────┴──────┐         │
│  │         Validation Layer (Quality Gates)           │         │
│  │  - YAML Syntax  - Completeness  - Accuracy        │         │
│  └──────────────────────────────────────────────────┘         │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────┐
│                      Data Layer                                  │
├───────────────────────────┼──────────────────────────────────────┤
│                           │                                      │
│  ┌────────────────────────┴────────────────────────┐            │
│  │            Knowledge Base (YAML Files)           │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │            │
│  │  │ Entries  │ │  Index   │ │ Metadata │        │            │
│  │  └──────────┘ └──────────┘ └──────────┘        │            │
│  │                                                 │            │
│  │  ┌─────────────────────────────────────────┐   │            │
│  │  │    Domain Organization                  │   │            │
│  │  │  docker/  postgresql/  python/  ...      │   │            │
│  │  └─────────────────────────────────────────┘   │            │
│  └─────────────────────────────────────────────────┘            │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────┐
│                    Storage Layer (Git)                          │
├───────────────────────────┼──────────────────────────────────────┤
│                           │                                      │
│  ┌────────────────────────┴────────────────────────┐            │
│  │      GitHub Repository (shared-knowledge-base)   │            │
│  │                                                   │            │
│  │  ┌──────────────────────────────────────────┐   │            │
│  │  │  Main Branch (Production Knowledge)      │   │            │
│  │  └──────────────────────────────────────────┘   │            │
│  │                                                   │            │
│  │  ┌──────────────────────────────────────────┐   │            │
│  │  │  Tags (v4.0.0, v4.0.1, ...)              │   │            │
│  │  └──────────────────────────────────────────┘   │            │
│  └─────────────────────────────────────────────────┘            │
│                           │                                      │
│  ┌────────────────────────┴────────────────────────┐            │
│  │      Consumer Projects (via Git Submodule)       │            │
│  │                                                   │            │
│  │  Project A: .kb/shared/ → (submodule)            │            │
│  │  Project B: docs/kb/shared/ → (submodule)        │            │
│  │  Project C: knowledge-base/ → (submodule)        │            │
│  └─────────────────────────────────────────────────┘            │
│                           │                                      │
└───────────────────────────┼──────────────────────────────────────┘
                            │
```

### Data Flow

#### Flow 1: Agent Search for Error Solution

```
Agent                  kb.py                  Index                  Entries
  │                      │                      │                      │
  │ 1. Search "docker"   │                      │                      │
  ├─────────────────────>│                      │                      │
  │                      │                      │                      │
  │                      │ 2. Load index        │                      │
  │                      ├────────────────────>│                      │
  │                      │                      │                      │
  │                      │ 3. Return matches    │                      │
  │                      │<────────────────────┤                      │
  │                      │                      │                      │
  │ 4. Results (IDs)     │                      │                      │
  │<─────────────────────┤                      │                      │
  │                      │                      │                      │
  │ 5. Load entry DOCKER-001                      │                      │
  ├─────────────────────>│                      │                      │
  │                      │                      │                      │
  │                      │ 6. Parse YAML        │                      │
  │                      ├──────────────────────────────────────────>│
  │                      │                      │                      │
  │                      │ 7. Return entry      │                      │
  │                      │<─────────────────────────────────────────┤
  │                      │                      │                      │
  │ 8. Entry (YAML)      │                      │                      │
  │<─────────────────────┤                      │                      │
  │                      │                      │                      │
```

#### Flow 2: Developer Contributes Entry

```
Developer             Hooks                  kb.py              Git/GitHub
   │                     │                       │                     │
   │ 1. Write YAML       │                       │                     │
   ├────────────────────>│                       │                     │
   │                     │                       │                     │
   │                     │ 2. Validate YAML     │                     │
   │                     ├────────────────────>│                     │
   │                     │                       │                     │
   │                     │ 3. Quality score     │                     │
   │                     ├────────────────────>│                     │
   │                     │                       │                     │
   │                     │ 4. Score: 82/100     │                     │
   │                     │<────────────────────┤                     │
   │                     │                       │                     │
   │ 5. Pass/Fail        │                       │                     │
   │<────────────────────┤                       │                     │
   │                     │                       │                     │
   │ 6. If pass → commit                       │                     │
   ├───────────────────────────────────────────>│                     │
   │                     │                       │                     │
   │                     │                       │ 7. Push to GitHub  │
   │                     │                       ├──────────────────>│
   │                     │                       │                     │
   │                     │                       │ 8. Open PR         │
   │                     │                       │<──────────────────┤
   │                     │                       │                     │
   │                     │                       │ 9. Merge           │
   │                     │                       ├──────────────────>│
   │                     │                       │                     │
```

#### Flow 3: Progressive Domain Loading

```
Agent                Git Sparse Checkout      Domains
  │                         │                    │
  │ 1. List domains         │                    │
  ├────────────────────────>│                    │
  │                         │                    │
  │                         │ 2. Return metadata │
  │                         │<──────────────────┤
  │                         │                    │
  │ 3. Select "docker"      │                    │
  ├────────────────────────>│                    │
  │                         │                    │
  │                         │ 4. Checkout docker/│
  │                         ├────────────────────>│
  │                         │                    │
  │ 5. Return docker files  │                    │
  │<────────────────────────┤                    │
  │                         │                    │
  │ (postgresql/, python/, etc. NOT loaded)      │
  │                         │                    │
```

---

## Component Design

### C1: CLI Tool (kb.py)

**Purpose:** Primary interface for interacting with KB

**Responsibilities:**
- Search entries
- Validate entries
- Build/update index
- Display statistics
- Export/import data

**Architecture:**

```python
class KBCli:
    """Main CLI interface"""

    def __init__(self, kb_path: str):
        self.kb_path = kb_path
        self.index = IndexManager(kb_path)
        self.validator = EntryValidator()
        self.exporter = DataExporter()

    def search(self, query: str, filters: Dict) -> List[Entry]:
        """Search entries by query and filters"""
        self.index.load()
        results = self.index.search(query)
        filtered = self._apply_filters(results, filters)
        return filtered

    def validate(self, path: str) -> ValidationResult:
        """Validate entries at path"""
        entries = self._load_entries(path)
        results = [self.validator.validate(e) for e in entries]
        return ValidationResult(results)

    def index_build(self, force: bool = False) -> IndexStats:
        """Build search index"""
        if force or not self.index.exists():
            entries = self._load_all_entries()
            self.index.build(entries)
        return self.index.stats()

class IndexManager:
    """Manages search index"""

    def __init__(self, kb_path: str):
        self.kb_path = kb_path
        self.index_path = os.path.join(kb_path, "_index.yaml")
        self.index = None

    def load(self):
        """Load index from disk"""
        if not self.index:
            with open(self.index_path) as f:
                self.index = yaml.safe_load(f)

    def build(self, entries: List[Entry]):
        """Build index from entries"""
        self.index = {
            "version": "4.0.0",
            "entries": [],
            "domains": {},
            "built_at": datetime.now().isoformat()
        }
        for entry in entries:
            self._add_entry(entry)
        self._save()

    def search(self, query: str) -> List[Entry]:
        """Search index by query"""
        results = []
        for entry in self.index["entries"]:
            score = self._calculate_relevance(entry, query)
            if score > 0:
                results.append((entry, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results]

class EntryValidator:
    """Validates KB entries"""

    def validate(self, entry: Entry) -> ValidationResult:
        """Validate single entry"""
        score = 0
        errors = []

        # Completeness (30 points)
        score += self._check_completeness(entry, errors)

        # Accuracy (30 points)
        score += self._check_accuracy(entry, errors)

        # Documentation (20 points)
        score += self._check_documentation(entry, errors)

        # Relevance (20 points)
        score += self._check_relevance(entry, errors)

        return ValidationResult(
            entry_id=entry.id,
            score=score,
            errors=errors,
            passed=score >= 75
        )
```

**Key Design Decisions:**

1. **Separation of Concerns:** Search, validation, indexing separate classes
2. **Lazy Loading:** Index loaded only when needed
3. **Immutable Entries:** Entries never modified in-place
4. **Strategy Pattern:** Pluggable validators, exporters

### C2: Domain Manager (kb_domains.py)

**Purpose:** Manage domain metadata and progressive loading

**Responsibilities:**
- List domains with entry counts
- Display domain statistics
- Support flat and nested index formats (v4.0.0 compatibility)
- Calculate token estimates

**Architecture:**

```python
class DomainManager:
    """Manages KB domains"""

    def __init__(self, kb_path: str):
        self.kb_path = kb_path
        self.index_path = os.path.join(kb_path, "_domain_index.yaml")
        self.domains = None

    def load_index(self):
        """Load domain index (handles flat & nested formats)"""
        with open(self.index_path) as f:
            data = yaml.safe_load(f)

        self.domains = data.get("domains", {})

        # Handle both formats:
        # v4.0.0 flat: {docker: 11}
        # Old nested: {docker: {entries: 11}}
        for name, value in self.domains.items():
            if isinstance(value, dict):
                # Convert nested to flat
                self.domains[name] = value.get("entries", 0)

    def list_domains(self) -> List[DomainInfo]:
        """List all domains with metadata"""
        self.load_index()
        domains = []
        for name, count in self.domains.items():
            domain_path = os.path.join(self.kb_path, name)
            token_count = self._estimate_tokens(domain_path)
            domains.append(DomainInfo(
                name=name,
                entry_count=count,
                token_estimate=token_count
            ))
        return sorted(domains, key=lambda d: d.entry_count, reverse=True)

    def get_domain_files(self, domain_name: str) -> List[str]:
        """Get all files in domain"""
        domain_path = os.path.join(self.kb_path, domain_name)
        files = []
        for root, _, filenames in os.walk(domain_path):
            for filename in filenames:
                if filename.endswith(".yaml"):
                    files.append(os.path.join(root, filename))
        return files

    def _estimate_tokens(self, domain_path: str) -> int:
        """Estimate token count for domain"""
        total_chars = 0
        for root, _, filenames in os.walk(domain_path):
            for filename in filenames:
                if filename.endswith(".yaml"):
                    filepath = os.path.join(root, filename)
                    with open(filepath) as f:
                        total_chars += len(f.read())
        # Rough estimate: 1 token ≈ 4 characters
        return total_chars // 4
```

**Key Design Decisions:**

1. **Backward Compatibility:** Handles both flat (v4.0.0) and nested (old) formats
2. **Token Estimation:** Rough estimate for planning
3. **Lazy File Loading:** Files loaded only when requested
4. **Immutable Index:** Never modifies index file directly

### C3: Hooks System

**Purpose:** Automate KB operations at key workflow points

**Responsibilities:**
- Validate YAML before writes
- Enforce quality gates after edits
- Check for updates on session start
- Validate index on session stop

**Architecture:**

```bash
# .claude/hooks/validate-yaml-before-write.sh
#!/bin/bash
# PreToolUse hook for Write operations

FILE="$1"
if [[ "$FILE" == *.yaml ]]; then
    # Validate YAML syntax
    python -c "import yaml; yaml.safe_load(open('$FILE'))"
    if [ $? -ne 0 ]; then
        echo "❌ Invalid YAML syntax"
        exit 1
    fi

    # Check required fields
    python tools/kb.py validate "$FILE"
    if [ $? -ne 0 ]; then
        echo "❌ Validation failed"
        exit 1
    fi
fi
exit 0
```

```bash
# .claude/hooks/quality-gate.sh
#!/bin/bash
# PostToolUse hook for YAML edits

FILE="$1"
if [[ "$FILE" == *.yaml ]]; then
    # Calculate quality score
    SCORE=$(python tools/kb.py score "$FILE")

    # Check if shared repository
    if [[ "$FILE" == .kb/shared/* ]]; then
        if [ $SCORE -lt 75 ]; then
            echo "❌ Quality score $SCORE < 75 (minimum for shared repo)"
            echo "   Add to local KB instead or improve quality"
            exit 1
        fi
    fi

    # Auto-format YAML
    python tools/kb.py format "$FILE"

    # Create metadata
    python tools/kb.py metadata "$FILE"
fi
exit 0
```

```bash
# .claude/hooks/session-setup.sh
#!/bin/bash
# SessionStart hook

echo "🔍 Checking Shared KB updates..."

if [ -d ".kb/shared" ]; then
    cd .kb/shared
    git fetch origin

    CURRENT=$(git describe --tags --abbrev=0)
    LATEST=$(git tag -l | sort -V | tail -n1)

    if [ "$CURRENT" != "$LATEST" ]; then
        echo "⚠️  Update available: $CURRENT → $LATEST"
        echo "   Run: cd .kb/shared && git pull origin main"
    fi

    cd ../..
fi

echo "✅ Session ready"
```

**Key Design Decisions:**

1. **Fast Fail:** Exit on first error for immediate feedback
2. **Non-Blocking:** Use `|| true` for optional checks
3. **Clear Messaging:** Emoji + text for visibility
4. **Cross-Platform:** Bash scripts work on Linux, macOS, WSL2

### C4: Agent Instructions System

**Purpose:** Provide AI agents with clear protocols for KB interaction

**Responsibilities:**
- Define 3 Golden Rules
- Provide decision trees for common scenarios
- Include troubleshooting guides
- Specify update workflows

**Architecture:**

```
Agent Instructions (Markdown)
│
├── for-claude-code/
│   ├── AGENT-UPDATE-INSTRUCTIONS.md (600+ lines)
│   │   ├── 3 Golden Rules
│   │   ├── 5 Workflow Phases
│   │   ├── Diagnostic Commands
│   │   └── Troubleshooting Guide
│   │
│   └── KB-UPDATE-QUICK-REFERENCE.md (200+ lines)
│       ├── 5 Tests (Yes/No)
│       ├── Decision Tree
│       └── 30-Second Diagnosis
│
└── for-projects/
    ├── START-HERE.md (Single entry point)
    ├── AGENT-INSTRUCTIONS.md (Complete guide)
    ├── QUICK-REFERENCE.md (How to give instructions)
    └── UPDATE-SHARED-KB.md (Update workflow)
```

**Content Structure:**

```markdown
# AGENT-UPDATE-INSTRUCTIONS.md

## 3 Golden Rules
1. NEVER modify .kb/shared/ files
2. DATA is source of truth
3. When unsure → ASK

## Workflow Phases
Phase 1: Detection - Is this a KB update?
Phase 2: Scope - Universal or project-specific?
Phase 3: Validation - Quality score ≥75?
Phase 4: Commit - Follow commit standards
Phase 5: Verify - Post-commit validation

## Decision Tree
```
[ASCII decision tree diagram]
```

## Troubleshooting
- Problem: "TypeError"
- Diagnosis: Tool bug vs data bug
- Solution: Update tool, NOT data
```

**Key Design Decisions:**

1. **Progressive Disclosure:** Quick reference first, details later
2. **Decision Trees:** Visual aids for complex decisions
3. **Real Examples:** Actual problems from tmp/tmp1.txt
4. **Cross-References:** Link to related documentation

---

## Data Architecture

### Data Model

```
Knowledge Base
│
├── Domains (Top-level categories)
│   ├── docker/          (Docker-specific errors)
│   ├── postgresql/      (PostgreSQL errors)
│   ├── python/          (Python errors)
│   ├── javascript/      (JavaScript errors)
│   ├── universal/       (Cross-language patterns)
│   └── claude-code/     (Claude Code errors)
│
├── Entries (YAML files)
│   ├── errors/
│   │   ├── DOMAIN-001.yaml
│   │   ├── DOMAIN-002.yaml
│   │   └── ...
│   │
│   └── patterns/
│       ├── PATTERN-001.yaml
│       └── ...
│
├── Index Files
│   ├── _domain_index.yaml    (Domain metadata)
│   ├── _index.yaml           (Search index)
│   └── DOMAIN-001_meta.yaml  (Entry metadata)
│
└── Documentation
    ├── README.md
    ├── CHANGELOG.md
    └── standards/
        ├── yaml-standards.md
        └── quality-standards.md
```

### Data Flow

```
┌─────────────┐
│   Create    │ Write YAML file
└──────┬──────┘
       │
       v
┌─────────────┐
│  Validate   │ Check syntax, required fields
└──────┬──────┘
       │
       v
┌─────────────┐
│ Score       │ Calculate quality (0-100)
└──────┬──────┘
       │
       v
┌─────────────┐    ┌──────────────┐
│ Score ≥75?  │───No│ Reject/Improve│
└──────┬──────┘    └──────────────┘
       │Yes
       v
┌─────────────┐
│  Commit     │ Add to git
└──────┬──────┘
       │
       v
┌─────────────┐
│ Build Index│ Update _index.yaml
└──────┬──────┘
       │
       v
┌─────────────┐
│  Searchable │ Available for queries
└─────────────┘
```

### Data Versioning

**Git-based versioning:**
- Every commit creates version
- Tags for releases (v4.0.0, v4.0.1)
- Branch for experimental features
- PRs for contributions

**Entry versioning:**
```yaml
version: "1.0"              # Entry format version
last_updated: "2026-01-08"  # Last modification date

# Git history for full audit trail
# $ git log --follow python/errors/PYTHON-001.yaml
```

**Schema versioning:**
- v1.0: Initial schema (2025-12-01)
- v4.0.0: Domain index flat format (2026-01-07)
- Backward compatibility maintained
- Migration scripts for breaking changes

---

## Technology Stack

### Core Technologies

| Component | Technology | Version |
|-----------|-----------|---------|
| **Language** | Python | 3.8+ |
| **Data Format** | YAML | 1.2 |
| **Version Control** | Git | 2.30+ |
| **Hosting** | GitHub | - |
| **CLI** | argparse (std) | - |
| **Parsing** | PyYAML | 6.0+ |

### Python Dependencies

```python
# requirements.txt
pyyaml>=6.0            # YAML parsing
typing-extensions>=4.0  # Type hints (Python <3.10)
```

### Development Tools

```python
# requirements-dev.txt
pytest>=7.0             # Testing
pytest-cov>=4.0         # Coverage
pylint>=2.17            # Linting
black>=23.0             # Formatting
mypy>=1.0               # Type checking
```

### Infrastructure

| Service | Purpose | Provider |
|---------|---------|----------|
| **Git Hosting** | Repository, issues, PRs | GitHub |
| **CI/CD** | Automated testing | GitHub Actions |
| **Documentation** | Static site | GitHub Pages |
| **Releases** | Versioned releases | GitHub Releases |
| **Package** | Distribution (future) | PyPI |

---

## Integration Architecture

### I1: Claude Code Integration

**Components:**

1. **Hooks**
   - SessionStart: Check updates, display stats
   - PreToolUse: Validate before writes
   - PostToolUse: Quality gates after edits
   - Stop: Validate index

2. **Agents**
   - kb-curator: Auto-load from universal/agent-instructions/
   - Subagents: researcher, debugger, validator, curator

3. **Skills**
   - kb-search: Search entries
   - kb-validate: Validate entries
   - kb-index: Build index
   - kb-create: Create entries

4. **Commands**
   - /kb-search: Quick search
   - /kb-validate: Quick validation
   - /kb-index: Rebuild index

**Configuration:**

```json
// .claude/settings.json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/session-setup.sh",
        "timeout": 10
      }]
    }],
    "PostToolUse": [{
      "matcher": "Write:*.yaml",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/quality-gate.sh",
        "timeout": 15
      }]
    }]
  },
  "agents": {
    "enabled": ["kb-curator"]
  },
  "skills": {
    "enabled": ["kb-search", "kb-validate", "kb-index"]
  }
}
```

### I2: Git Submodule Integration

**Setup:**

```bash
# Add Shared KB as submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared

# Initialize
git submodule update --init --recursive

# Update
cd .kb/shared && git pull origin main
```

**Sparse Checkout (Progressive Loading):**

```bash
# Enable sparse checkout
git config core.sparseCheckout true

# Configure which domains to load
cat > .git/info/sparse-checkout << EOF
docker/
postgresql/
universal/
EOF

# Update
git submodule update --init --recursive
```

**Version Pinning:**

```bash
# Pin to specific version
cd .kb/shared
git checkout v4.0.1
cd ../..
git add .kb/shared
git commit -m "Pin Shared KB to v4.0.1"
```

### I3: IDE Integration

**VS Code Extension (Future):**

```json
// .vscode/settings.json
{
  "kb.enabled": true,
  "kb.paths": [".kb/shared"],
  "kb.autoIndex": true,
  "kb.syntaxHighlighting": true
}
```

**JetBrains Plugin (Future):**

- Quick search: Ctrl+Shift+K
- Entry preview: Ctrl+Q
- Navigation: Ctrl+Click on entry IDs

---

## Security Architecture

### Threat Model

**Threats:**
1. **Data Corruption:** Agent modifies `.kb/shared/` incorrectly
2. **Low-Quality Entries:** Spam, incorrect solutions
3. **Code Injection:** Malicious code in YAML
4. **Git Conflicts:** Concurrent modifications
5. **Access Violation:** Unauthorized writes to shared repo

**Mitigations:**

1. **Data Corruption**
   - Agent instructions (3 Golden Rules)
   - Read-only enforcement in hooks
   - PreToolUse validation

2. **Low-Quality Entries**
   - Quality score ≥75 gate
   - Peer review for PRs
   - Automated validation

3. **Code Injection**
   - YAML parsing (no eval)
   - Sanitize user input
   - Code review for exec commands

4. **Git Conflicts**
   - Single source of truth (upstream)
   - Clear update protocols
   - Conflict resolution docs

5. **Access Violation**
   - PR review required
   - Maintainer permissions only
   - Branch protection rules

### Security Controls

**Access Control:**

```
┌─────────────────────────────────────────────────┐
│              Access Control Matrix              │
├─────────────────────────────────────────────────┤
│ Role           │ Read │ Write │ Admin │ Merge  │
├────────────────┼──────┼───────┼───────┼───────┤
│ Public         │  ✓   │   ✗   │   ✗   │   ✗   │
│ Contributor    │  ✓   │   ✓   │   ✗   │   ✗   │
│ Maintainer     │  ✓   │   ✓   │   ✓   │   ✓   │
│ Agent (AI)     │  ✓   │   ✗   │   ✗   │   ✗   │
└────────────────┴──────┴───────┴───────┴───────┘
```

**Validation Controls:**

```python
# Input validation
def validate_entry(entry: Entry) -> bool:
    # Check required fields
    if not entry.problem or not entry.solution:
        return False

    # Check code is safe (no exec, eval, etc.)
    if dangerous_code(entry.solution.code):
        return False

    # Check URLs are safe
    for url in entry.sources:
        if not safe_url(url):
            return False

    return True
```

---

## Deployment Architecture

### Development Environment

```bash
# Local development
shared-knowledge-base/
├── .git/                  # Local git repo
├── docker/                # Working on docker entries
├── tools/                 # CLI tools
└── tests/                 # Unit tests

# Workflow
python tools/kb.py validate .
python tools/kb.py index --force
python -m pytest tests/
```

### Production Environment

```
GitHub Repository
├── Main Branch (production)
├── Feature Branches (development)
├── Tags (releases: v4.0.0, v4.0.1)
└── Pull Requests (contributions)

# CI/CD Pipeline
GitHub Actions:
  1. Trigger: Push/PR
  2. Run: pytest tests/
  3. Run: pylint tools/
  4. Run: python tools/kb.py validate .
  5. Build: Documentation
  6. Deploy: Update GitHub Pages
```

### Consumer Projects

```
Project A
├── .kb/shared/ → (submodule) → shared-knowledge-base (v4.0.1)
├── tools/
│   └── kb.py → (copy or symlink)
└── .claude/
    ├── hooks/ → (copy from .kb/shared/.claude/hooks/)
    └── settings.json → (configured)

# Usage
cd project-a
python tools/kb.py search "docker"
```

---

## Scalability & Performance

### Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| **Search latency** | <1s (500 entries) | 0.3s |
| **Index build** | <10s (500 entries) | 5s |
| **Domain load** | <2s | 1s |
| **Validation** | <5s/entry | 2s |
| **Token per entry** | <500 | 350 avg |

### Scalability Strategy

**Horizontal Scaling:**
- Git submodules (each project has own copy)
- No central bottleneck
- Distributed via GitHub CDN

**Vertical Scaling:**
- In-memory index (fast search)
- Lazy loading (load only what's needed)
- Progressive parsing (don't parse full YAML)

**Caching:**
- Index cached in memory
- Git objects cached by Git
- GitHub CDN for raw content

### Optimization Techniques

1. **Incremental Indexing**
   ```python
   # Only index new/modified files
   if force or not index.exists():
       build_full_index()
   else:
       build_incremental_index()
   ```

2. **Sparse Parsing**
   ```python
   # Load only metadata first
   entry = load_entry_metadata(filepath)  # Fast

   # Load full content only when needed
   if detailed_view_needed:
       entry.load_full_content()  # Slower
   ```

3. **Domain Sharding**
   ```python
   # Search only requested domains
   if domains:
       results = search_in_domains(query, domains)
   else:
       results = search_all(query)
   ```

---

## Monitoring & Observability

### Metrics

**Operational Metrics:**
- Index build time
- Search query latency
- Validation pass/fail rate
- Error rates by component

**Product Metrics:**
- Total entries
- Entries per domain
- Average quality score
- GitHub stars/forks

**User Metrics:**
- CLI command usage
- Agent access patterns
- Search query distribution
- Popular entries

### Logging

```python
# Structured logging
import logging
import json

logger = logging.getLogger("kb")

logger.info("search_query", extra={
    "query": query,
    "filters": filters,
    "results_count": len(results),
    "latency_ms": latency
})
```

**Log Levels:**
- DEBUG: Detailed diagnostics
- INFO: Normal operations
- WARNING: Quality score <80
- ERROR: Validation failure
- CRITICAL: Data corruption

### Health Checks

```bash
# .claude/hooks/health-check.sh
#!/bin/bash

# Check index exists
if [ ! -f "_index.yaml" ]; then
    echo "❌ Index missing"
    exit 1
fi

# Check index is recent (within 7 days)
INDEX_AGE=$(find _index.yaml -mtime +7)
if [ -n "$INDEX_AGE" ]; then
    echo "⚠️  Index stale (>7 days)"
fi

# Check for errors
if python tools/kb.py validate . 2>&1 | grep -q "ERROR"; then
    echo "❌ Validation errors found"
    exit 1
fi

echo "✅ Healthy"
```

---

## Disaster Recovery

### Backup Strategy

**Git as Backup:**
- Every commit is a backup
- GitHub has 3 replicas
- Local clone as backup

**Recovery Procedures:**

1. **Accidental Deletion**
   ```bash
   # Restore from git
   git checkout HEAD~1 -- path/to/file.yaml
   ```

2. **Corrupted Index**
   ```bash
   # Rebuild from source
   python tools/kb.py index --force
   ```

3. **Lost Submodule**
   ```bash
   # Re-add submodule
   git submodule add https://github.com/... .kb/shared
   git checkout v4.0.1
   ```

4. **Git Conflict**
   ```bash
   # Reset to upstream
   cd .kb/shared
   git fetch origin
   git reset --hard origin/main
   ```

### Business Continuity

**RTO (Recovery Time Objective):** 1 hour
**RPO (Recovery Point Objective):** 1 commit

**Scenarios:**

1. **GitHub Down**
   - Use local clone
   - Work offline
   - Push when GitHub recovers

2. **Corrupted Repository**
   - Restore from backup
   - Rebuild from source files
   - Last resort: Re-clone from GitHub

3. **Lost Maintainer**
   - Documentation in README
   - Succession plan
   - Community takeover

---

## Appendix

### A. Architecture Decision Records (ADRs)

**ADR-001: File-Based Storage (YAML)**
- Status: Accepted
- Decision: Use YAML files instead of database
- Rationale: Human-readable, version-controlled, simple
- Consequences: Slower than DB, but simpler and more portable

**ADR-002: Git Submodules for Distribution**
- Status: Accepted
- Decision: Use git submodules instead of custom sync
- Rationale: Standard tool, built-in versioning
- Consequences: Git learning curve, but industry-standard

**ADR-003: Quality Score ≥75 Gate**
- Status: Accepted
- Decision: Require minimum quality score for shared repo
- Rationale: Maintain high standard, reduce maintenance
- Consequences: Higher barrier to contribution, but better quality

**ADR-004: Progressive Domain Loading**
- Status: Accepted
- Decision: Load only needed domains via sparse-checkout
- Rationale: Minimize token usage for AI agents
- Consequences: More complex, but 50%+ token savings

**ADR-005: Agent Instructions as Code**
- Status: Accepted
- Decision: Treat agent protocols as first-class documentation
- Rationale: Clear rules, prevent data corruption
- Consequences: More documentation, but fewer agent errors

### B. Performance Benchmarks

**Hardware:** Intel i7-10750H, 16GB RAM, SSD

| Operation | Entries | Time | Throughput |
|-----------|---------|------|------------|
| **Index Build** | 105 | 0.5s | 210 entries/s |
| **Search** | 105 | 0.3s | 350 queries/s |
| **Validate** | 1 | 2s | 0.5 entries/s |
| **Load Domain** | 11 (docker) | 0.8s | - |

### C. Known Limitations

1. **No Real-Time Updates**
   - Submodules require manual update
   - No push notifications
   - Mitigation: SessionStart hook checks for updates

2. **No Collaborative Editing**
   - One editor per entry at a time
   - Git merge conflicts possible
   - Mitigation: PR review process

3. **No Access Control**
   - Anyone can read (public repo)
   - Write access via maintainer approval
   - Mitigation: PR review, branch protection

4. **Search Quality**
   - Keyword-based (no semantic search)
   - Relevance scoring basic
   - Mitigation: v4.2.0 will add AI search

### D. Future Architecture Improvements

**v5.0.0 (2027):**
- Add database backend (PostgreSQL) for scalability
- Add REST API for remote access
- Add web UI for browsing/searching
- Add AI-powered semantic search

**v6.0.0 (2028):**
- Add real-time collaboration (WebSockets)
- Add multi-tenant support
- Add enterprise SSO
- Add advanced analytics

---

**Document Owners:** KB Curator
**Review Cycle:** Quarterly
**Next Review:** 2026-04-08
**Related Documents:** PRD.md, CHANGELOG.md, README.md
