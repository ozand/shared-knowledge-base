# Architecture Reference Document (ARD)
# Shared Knowledge Base System v5.1

**Version:** 5.1.0
**Status:** ✅ Approved for Production
**Architecture Style:** Distributed, Git-Native, Agent-Centric
**Last Updated:** 2026-01-08

---

## 1. Executive Summary

The Shared Knowledge Base v5.1 implements a **two-tier knowledge management model** that enables secure knowledge sharing between projects through a controlled gateway (Curator) while providing Claude Code agents with clear working context.

### Key Architecture Changes from v4.0

| Feature | v4.0 | v5.1 |
|---------|------|------|
| **KB Structure** | Single-tier (Shared KB only) | **Two-tier** (Project KB + Shared KB) |
| **Submission** | Direct to Shared KB | **Project-specific or Shared via Issues** |
| **Agent Access** | Read-only to Shared KB | **RW to Project KB, Issue-submission to Shared** |
| **Integration** | Git submodules only | **Git submodules + GitHub Issues + PyGithub** |
| **Context** | Manual loading | **Automatic via SessionStart hook** |

---

## 2. High-Level Architecture

### 2.1. Scopes (Tiers)

| Component      | Scope        | Storage         | Access         | Purpose                                      |
|:---------------|:-------------|:----------------|:---------------|:---------------------------------------------|
| **Project KB** | Private      | `.kb/project/`  | RW (Direct)    | Business logic, secrets, project architecture |
| **Shared KB**  | Public/Org   | `.kb/shared/`   | RO (Submodule) | Universal patterns, languages, tooling       |
| **Submission** | Transitional | GitHub Issues   | Write-Only     | Buffer for Shared KB proposals               |

### 2.2. Technology Stack

* **Core:** Python 3.11+, Git Submodules
* **Integration:** `PyGithub` (GitHub Issues API without external binaries)
* **Storage:** YAML (structured data) + Markdown (free-form context)
* **Automation:** Claude Code Hooks (`SessionStart`, `PostToolUse`)

### 2.3. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Project Repository                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │   Project Agent  │         │   SessionStart   │             │
│  │   (Claude Code)  │────────▶│   Hook           │             │
│  └────────┬─────────┘         └────────┬─────────┘             │
│           │                            │                        │
│           │ 1. Load Context            │                        │
│           │ 2. Check sharing criteria  │                        │
│           │                            │                        │
│           ▼                            ▼                        │
│  ┌────────────────────────────────────────────────┐             │
│  │              .kb/context/                      │             │
│  │  ├── PROJECT.yaml (Structured config)          │             │
│  │  └── MEMORY.md (Free-form knowledge)           │             │
│  └────────────────────────────────────────────────┘             │
│           │                                                    │
│           │ Decision: Local vs Shared                          │
│           │                                                    │
│     ┌─────┴─────┐                                             │
│     │           │                                             │
│     ▼           ▼                                             │
│  ┌─────┐    ┌──────────────────────────────────┐              │
│  │Local│    │      kb_submit.py                │              │
│  │ KB  │    │      (PyGithub library)          │              │
│  └─────┘    └─────────────┬────────────────────┘              │
│                      │                                        │
│                      │ Create GitHub Issue                    │
│                      ▼                                        │
│  ┌─────────────────────────────────────────────────────┐      │
│  │           .kb/shared/ (Submodule)                   │      │
│  │    ├── domains/ (docker, python, postgresql)       │      │
│  │    ├── tools/ (kb_submit.py, kb_search.py)        │      │
│  │    └── _domain_index.yaml (Sparse checkout index)  │      │
│  └─────────────────────────────────────────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

                              ▲

                              │ git submodule update

                              │

┌─────────────────────────────────────────────────────────────────┐
│              Shared KB Repository (Central)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │  GitHub Issues   │────────▶│   Curator Role   │             │
│  │  (Submissions)   │         │  (Human/Agent)   │             │
│  └──────────────────┘         └────────┬─────────┘             │
│                                          │                      │
│                                          │ kb_curate.py         │
│                                          ▼                      │
│  ┌────────────────────────────────────────────────┐             │
│  │   domains/ (Validated knowledge entries)       │             │
│  │    ├── docker/                                 │             │
│  │    ├── python/                                 │             │
│  │    └── postgresql/                             │             │
│  └────────────────────────────────────────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Flow & Workflows

### 3.1. Knowledge Submission Loop

```
1. DETECTION
   Agent solves problem → Checks solution against sharing_criteria

2. DECISION
   ┌─ PROJECT-SPECIFIC ──► kb_submit.py --target local
   │                         │
   │                         └─► Direct commit to .kb/project/
   │
   └─ UNIVERSAL ──────────► kb_submit.py --target shared
                               │
                               └─► Create GitHub Issue via PyGithub

3. METADATA
   Issue body includes YAML frontmatter for machine parsing:
   - domain, type, project_source
   - agent_id, timestamp
   - Structured problem description

4. LOCAL COMMIT
   Project KB entries:
   - No validation required
   - Direct git commit
   - No curator review needed
```

### 3.2. Curation Loop

```
1. TRIGGER
   Tech lead runs: claude -p curator
   or
   Human runs: python tools/v5.1/kb_curate.py --mode list

2. FETCH
   Curator downloads Issues with 'kb-submission' label via GitHub API

3. VALIDATE
   ┌─ Parse YAML frontmatter
   ├─ Check Quality Score (>= 75/100)
   ├─ Check for duplicates
   └─ Verify scope appropriateness

4. DECISION
   ┌─ /approve ──► Commit to Shared KB ──► Close Issue
   ├─ /request-changes ──► Comment with feedback
   └─ /reject ──► Comment with reason ──► Close Issue
```

---

## 4. Directory Structure

```
my-project/
├── .env                      # GITHUB_TOKEN (for submissions)
├── .claude/
│   ├── hooks/
│   │   └── session-start.sh  # Context loading + update checks
│   └── settings.json         # Claude Code config
├── .kb/
│   ├── context/              # 📋 PROJECT PASSPORT
│   │   ├── PROJECT.yaml      # Config + sharing criteria
│   │   └── MEMORY.md         # History + lessons
│   ├── project/              # 📁 LOCAL KB (committed to project)
│   │   ├── integrations/     # Integration configs & docs
│   │   ├── endpoints/        # API endpoints documentation
│   │   ├── decisions/        # Architectural decisions
│   │   ├── lessons/          # Learned lessons
│   │   └── pending/          # Pending Shared KB submissions
│   └── shared/               # 🌍 SHARED KB (Git Submodule)
│       ├── domains/
│       │   ├── docker/
│       │   ├── python/
│       │   └── postgresql/
│       └── tools/
│           ├── kb_submit.py  # Submission tool (PyGithub)
│           └── kb_search.py  # Universal search
└── src/                      # Project code
```

---

## 5. Component Design

### 5.1. Project Context (`.kb/context/`)

**Purpose:** Provide agents with project-specific context and decision rules

**Files:**
- **PROJECT.yaml** - Structured configuration
  - Project metadata (name, type, stack)
  - `sharing_criteria` rules (universal vs project-specific)
  - Integration references
  - Team information

- **MEMORY.md** - Free-form knowledge
  - Architectural decisions history
  - Known issues & workarounds
  - Onboarding tips for new agents

**Loading:** Automatic via `session-start.sh` hook

### 5.2. Project KB (`.kb/project/`)

**Purpose:** Store project-specific knowledge that should NOT be shared

**Contents:**
- Business logic patterns
- Internal service URLs & names
- Temporary workarounds
- Environment-specific configs
- Integration secrets (templates)

**Access:**
- Agent: Read/Write (direct git commit)
- Curator: No access (project-private)
- Version control: Within project repository

### 5.3. Shared KB (`.kb/shared/`)

**Purpose:** Universal knowledge applicable across projects

**Contents:**
- Language patterns (python, javascript, etc.)
- Framework solutions (fastapi, react, etc.)
- DevOps patterns (docker, kubernetes, etc.)
- Database knowledge (postgresql, mongodb, etc.)

**Access:**
- Agent: Read-only (submodule)
- Submission: Write-only via GitHub Issues
- Curator: Read/Write (after review)
- Version control: Separate repository

### 5.4. Submission Gateway (GitHub Issues)

**Purpose:** Controlled buffer for Shared KB contributions

**Flow:**
```
Agent → PyGithub API → GitHub Issue → Curator → Shared KB
```

**Metadata Format:**
```yaml
---
submission_meta:
  domain: docker
  type: error-solution
  project_source: my-project-id
  agent_id: claude-session-123
  timestamp: 2026-01-08T12:00:00Z
---
```

**Benefits:**
- ✅ No merge conflicts (agents don't commit directly)
- ✅ Audit trail (Issue history)
- ✅ Feedback loop (comments before approval)
- ✅ Quality control (curator validation)

### 5.5. Curator Role

**Purpose:** Gatekeeper for Shared KB quality

**Implementation:**
- Can be human or agent
- Runs on-demand (not a service)
- Works in Shared KB repository context

**Tools:**
- `kb_curate.py` - Process submissions
- Quality validation (score >= 75)
- Duplicate detection
- Domain categorization

**Commands:**
```bash
kb_curate.py --mode list                    # List pending submissions
kb_curate.py --validate <issue_id>          # Validate submission
kb_curate.py --approve <issue_id>           # Approve & commit
kb_curate.py --reject <issue_id> --reason   # Reject with feedback
```

---

## 6. Security Model

### 6.1. Access Control

| Actor          | Project KB | Shared KB | GitHub Issues |
|:---------------|:-----------|:----------|:--------------|
| **Agent**      | RW         | RO        | Create only   |
| **Curator**    | None       | RW        | RW            |
| **Developer**  | RW         | RO        | RW            |

### 6.2. Token Management

**GITHUB_TOKEN** required for:
- Creating submissions (`kb_submit.py --target shared`)
- Curating submissions (`kb_curate.py`)

**Scopes:**
- Public repo: `public_repo`
- Private repo: `repo` + `issues`

**Storage:**
- `.env` file (gitignored)
- Never committed to repository

### 6.3. Content Security

**Project KB:**
- May contain secrets (use templates, not actual values)
- Committed to project repo (access controlled by project)
- No curator access

**Shared KB:**
- Must NOT contain secrets
- Public repository (or org-scoped)
- Curator validation required

---

## 7. Scalability Considerations

### 7.1. Token Optimization

**Progressive Loading:**
- Sparse checkout for Shared KB domains
- Load only relevant project context
- Search via `kb_search.py` before loading full files

**SessionStart Hook:**
- Updates Shared KB submodule (background)
- Loads PROJECT.yaml into agent context
- Minimal overhead on session start

### 7.2. Submission Scaling

**Volume Handling:**
- GitHub Issues scale to thousands of submissions
- Labels for categorization (`kb-submission`, `needs-review`)
- Curator can batch-process submissions

**Quality Gate:**
- Automated validation (quality score)
- Duplicate detection before curator review
- Auto-approve high-quality submissions (optional)

### 7.3. Multi-Project Support

**Isolation:**
- Each Project KB is independent
- Shared KB is common reference
- No cross-project interference

**Knowledge Flow:**
```
Project A ──┐
             ├──► Shared KB ◄── Curator ◄── GitHub Issues
Project B ──┘
```

---

## 8. Integration with Claude Code

### 8.1. Hooks

**SessionStart Hook** (`.claude/hooks/session-start.sh`):
```bash
# 1. Update Shared KB submodule
git submodule update --remote --merge --quiet

# 2. Load project context
cat .kb/context/PROJECT.yaml
cat .kb/context/MEMORY.md

# 3. Check token availability
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  GITHUB_TOKEN not set"
fi
```

**PostToolUse Hook** (optional):
- Auto-submit after certain tools
- Validate submissions before creating Issue

### 8.2. Agent Instructions

**Project Agent** (`.claude/agents/backend-dev.md`):
```markdown
## Knowledge Sharing Rules

1. Always search Shared KB first: `kb_search.py "query"`
2. Check `sharing_criteria` in PROJECT.yaml before saving
3. Use `kb_submit.py --target local` for project-specific
4. Use `kb_submit.py --target shared` for universal patterns
5. Never commit secrets to Shared KB
```

---

## 9. Migration Path from v4.0

### 9.1. Breaking Changes

- ❌ v4.0 agents can't submit to Shared KB directly
- ✅ v5.1 agents use Issues for submissions
- ✅ Backward compatible for reading Shared KB

### 9.2. Migration Steps

1. **Install Dependencies:**
   ```bash
   pip install PyGithub
   ```

2. **Create Project Structure:**
   ```bash
   mkdir -p .kb/{context,project/{integrations,endpoints,decisions,lessons,pending}}
   ```

3. **Create PROJECT.yaml:**
   ```yaml
   meta:
     name: "My Project"
     id: "my-project"
   sharing_criteria:
     universal_if:
       - "Framework-agnostic solution"
     project_specific_if:
       - "Contains business logic"
   ```

4. **Install SessionStart Hook:**
   ```bash
   cp .kb/shared/tools/v5.1/hooks/session-start.sh .claude/hooks/
   chmod +x .claude/hooks/session-start.sh
   ```

5. **Configure Token:**
   ```bash
   echo "GITHUB_TOKEN=ghp_xxx" >> .env
   echo ".env" >> .gitignore
   ```

---

## 10. Troubleshooting

| Issue | Solution |
|-------|----------|
| `kb_submit.py` fails with "No GITHUB_TOKEN" | Add token to `.env` file |
| Submodule not updating | Run `git submodule update --remote` manually |
| Issue created but not showing | Check GitHub repo URL in environment |
| Quality score too low | Improve YAML completeness (add all required fields) |
| Duplicate entries | Use `kb_search.py` before submitting |

---

## 11. Version History

| Version | Date | Changes |
|---------|------|---------|
| **5.1.0** | 2026-01-08 | Two-tier architecture, PyGithub integration, Issues workflow |
| **4.0.1** | 2026-01-07 | Bug fixes, performance improvements |
| **4.0.0** | 2026-01-05 | Quality scoring, metadata system |

---

**Document Status:** ✅ Approved
**Next Review:** 2026-02-01
**Maintainer:** Knowledge Base Curator
