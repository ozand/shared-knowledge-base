# Shared KB Workflows - Complete Guide

**Version:** 5.1.0
**Last Updated:** 2026-01-08

---

## Overview

The Shared Knowledge Base (Shared KB) operates on the principle of **"Centralized Library with Controlled Access"**. It stores industry standards, best practices, and tools that should be accessible across all projects in an organization.

This document details the complete lifecycle of knowledge in the Shared KB: from consumption to publication.

---

## Architecture

### Physical Structure

```
shared-knowledge-base/                 # Separate GitHub repository
├── domains/                           # Knowledge domains
│   ├── docker/                        # Docker & containers
│   ├── python/                        # Python errors & patterns
│   ├── postgresql/                    # PostgreSQL knowledge
│   ├── javascript/                    # JavaScript/Node.js
│   ├── universal/                     # Cross-language patterns
│   └── claude-code/                   # Claude Code specific
├── tools/                             # Tools for agents
│   └── v5.1/
│       ├── kb_search.py               # Search tool
│       ├── kb_submit.py               # Submission tool
│       └── kb_curate.py               # Curation tool
└── docs/v5.1/                         # Documentation
```

### Integration in Consumer Projects

```
my-project/
└── .kb/
    └── shared/                        # Git Submodule (Read-Only for agents)
        └── → symlink to shared-knowledge-base
```

**Access Control:**
- **Project Agents:** Read-Only (via submodule)
- **Curator:** Read/Write (via git)
- **Submission:** Write-Only (via GitHub Issues)

---

## Workflow 1: Read Flow (Consumption)

When an agent needs a solution, it searches the Shared KB as a local library.

### Process

1. **Agent triggers search:**
   ```bash
   python .kb/shared/tools/v5.1/kb_search.py --scope shared "docker compose healthcheck"
   ```

2. **Search mechanism:**
   - Script scans YAML files in `.kb/shared/domains/`
   - Searches content and filenames
   - Returns matching entries with previews

3. **Advantages:**
   - ✅ Instant results (no network requests)
   - ✅ Files already on disk via `git submodule`
   - ✅ Works offline

### Example Usage

```bash
# Search Shared KB only
python .kb/shared/tools/v5.1/kb_search.py "fastapi cors" --scope shared

# Search with preview
python .kb/shared/tools/v5.1/kb_search.py "postgresql" --scope shared --preview

# Show Shared KB statistics
python .kb/shared/tools/v5.1/kb_search.py --stats
```

---

## Workflow 2: Submission Flow (Proposal)

The most complex part: how can an agent add knowledge to a Read-Only repository? Through **GitHub Issues**.

### Process

1. **Agent finds a universal solution:**
   - Solves a problem applicable to any project
   - Checks `PROJECT.yaml` sharing criteria
   - Determines: *"This should be shared"*

2. **Agent creates submission:**
   ```bash
   python .kb/shared/tools/v5.1/kb_submit.py \
     --target shared \
     --file solution.yaml \
     --title "Fix for Pydantic v2 validation error"
   ```

3. **Behind the scenes:**
   - Script validates YAML content
   - Calculates quality score (>= 75 required)
   - Uses `GITHUB_TOKEN` from environment
   - Forms JSON package with metadata:
     - Author (agent_id)
     - Source project
     - Timestamp
     - Domain classification
   - Creates GitHub Issue via API

4. **Result:**
   - Issue appears in `shared-knowledge-base` repository
   - Labeled with `kb-submission`
   - Agent receives link and continues work

### Why This Design?

**Security:**
- ✅ Project agents don't need Write Access to code
- ✅ Only need permission to create Issues
- ✅ No risk of malicious commits

**Scalability:**
- ✅ No merge conflicts (10 agents = 10 Issues)
- ✅ Parallel submissions work fine
- ✅ Curator can process in any order

**Quality Control:**
- ✅ Every submission reviewed
- ✅ Feedback loop via comments
- ✅ Consistent standards enforced

### Example Submission

**Input file (`solution.yaml`):**
```yaml
version: "1.0"
category: "validation"
last_updated: "2026-01-08"

errors:
  - id: "PYDANTIC-001"
    title: "Pydantic v2 Validation Error"
    severity: "high"
    scope: "python"
    problem: |
      Validation error with Pydantic v2 models
    solution:
      code: |
        # Fix: Use model_validator
        from pydantic import model_validator

        @model_validator(mode='after')
        def validate_fields(self):
            ...
      explanation: |
        Pydantic v2 requires @model_validator decorator
```

**Command:**
```bash
python .kb/shared/tools/v5.1/kb_submit.py \
  --target shared \
  --file solution.yaml \
  --title "Pydantic v2 model validation fix" \
  --description "Fix for Pydantic v2 validation errors" \
  --domain python
```

**Created Issue:**
```markdown
---
submission_meta:
  domain: python
  type: error-solution
  project_source: my-project
  agent_id: claude-session-abc123
  timestamp: 2026-01-08T12:00:00Z
  verified: true
---

### Problem Description
Fix for Pydantic v2 validation errors

### Proposed Entry
```yaml
version: "1.0"
...
```

### Context
- **Project:** My Project
- **Problem encountered:** Fix for Pydantic v2 validation errors
- **Solution verified:** true
```

---

## Workflow 3: Curation Flow (Quality Control)

The **Curator** role (human or special agent) maintains Shared KB quality.

### Process

1. **Trigger curation:**
   ```bash
   # List pending submissions
   python tools/v5.1/kb_curate.py --mode list
   ```

2. **Fetch submissions:**
   - Curator runs in `shared-knowledge-base` repository context
   - Script queries GitHub API for Issues with `kb-submission` label
   - Downloads all pending submissions

3. **Automated Validation:**
   - ✅ Parse YAML frontmatter
   - ✅ Check syntax
   - ✅ Calculate Quality Score
   - ✅ Verify required fields
   - ⚠️  Duplicate check (manual)

4. **Decision:**

   **Option A: Approve**
   ```bash
   python tools/v5.1/kb_curate.py --mode approve --issue 123
   ```

   **Actions:**
   - Extracts YAML content from Issue
   - Determines domain from metadata
   - Creates file: `domains/{domain}/{CATEGORY}-{ID}.yaml`
   - Stages file in git: `git add`
   - Comments on Issue with file path
   - Adds `approved` label, removes `needs-review`
   - Closes Issue

   **Manual steps:**
   ```bash
   git status          # Review staged file
   git commit -m "Add python-pydantic-001.yaml"
   git push origin main
   ```

   **Option B: Reject**
   ```bash
   python tools/v5.1/kb_curate.py --mode reject --issue 456 --reason "Duplicate of #123"
   ```

   **Actions:**
   - Comments on Issue with reason
   - Adds `rejected` label
   - Closes Issue

   **Option C: Request Changes**
   - Manual comment on Issue
   - Leaves Issue open
   - Agent can update and resubmit

### Quality Gate

**Minimum Score: 75/100**

**Scoring:**
```
Basic Structure (40 points):
  version: +10
  category: +10
  last_updated: +20

Entry Quality (40 points):
  problem: +10
  solution.code: +15
  solution.explanation: +15

Metadata (20 points):
  scope: +10
  severity: +10
```

**Example:**
```
✅ Quality Score: 85/100
   ✅ Meets quality threshold (>= 75)
```

---

## Workflow 4: Sync Flow (Distribution)

How does new knowledge reach all projects?

### Process

1. **Event:** Curator pushes to `main` branch
   ```bash
   git push origin main
   ```

2. **Auto-distribution in Projects:**
   - Next Claude Code session in any project
   - SessionStart hook triggers
   - Executes: `git submodule update --remote --merge`
   - Git downloads latest changes from Shared KB

3. **Result:**
   - Knowledge submitted 5 minutes ago from Project A
   - Now available locally in Project B
   - No manual intervention needed

### Hook Implementation

**`.claude/hooks/session-start.sh`:**
```bash
# Step 1: Update Shared KB Submodule
if git submodule update --remote --merge --quiet 2>/dev/null; then
    echo "✅ Shared KB is up to date"
else
    echo "⚠️  Could not update Shared KB"
fi
```

**Timing:**
- Runs automatically on every Claude Code session start
- Runs in background (quiet mode)
- Shows summary of updates

### Update Flow Diagram

```
┌─────────────────┐
│  Project A      │
│  Agent submits  │
│  knowledge      │
└────────┬────────┘
         │ GitHub Issue
         ▼
┌─────────────────┐
│  Shared KB      │
│  Curator        │�───────┐
│  approves       │       │
└────────┬────────┘       │
         │ git push       │
         ▼                │
┌─────────────────┐       │
│  GitHub         │       │
│  main branch    │       │
└────────┬────────┘       │
         │                │
         │ submodule      │
         │ update         │
         ▼                │
┌─────────────────┐       │
│  Project B      │�───────┘
│  SessionStart   │
│  hook runs      │
│  git submodule  │
│  update         │
└─────────────────┘
```

---

## Access Control Matrix

| Actor              | Shared KB Access | Read Method              | Write Method        |
|--------------------|------------------|--------------------------|---------------------|
| **Project Agent**  | Read-Only        | Local files (fast)       | GitHub Issue (API)  |
| **Curator**        | Full             | Local files              | Git Commit (direct) |
| **Developer**      | Full             | GitHub UI / IDE          | Pull Request        |

---

## Summary: Self-Regulating Organism

The Shared KB becomes a **self-regulating system** that:

1. **Grows** through project contributions
2. **Maintains quality** via curator validation
3. **Distributes** automatically via git submodules
4. **Scales** without merge conflicts
5. **Protects** via controlled access

**Key Benefits:**

- ✅ **Single Source of Truth** for organization knowledge
- ✅ **Automatic Distribution** to all projects
- ✅ **Quality Control** via curation workflow
- ✅ **No Merge Conflicts** via Issues mechanism
- ✅ **Offline Capable** via local submodule
- ✅ **Version Controlled** via git history

---

**Related Documentation:**
- [ARD.md](../ARD.md) - Complete architecture
- [WORKFLOWS.md](WORKFLOWS.md) - Agent workflows
- [CONTEXT_SCHEMA.md](CONTEXT_SCHEMA.md) - PROJECT.yaml schema
