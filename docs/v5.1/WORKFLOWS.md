# Agent Workflows & Protocols v5.1

**Version:** 5.1.0
**Last Updated:** 2026-01-08

---

## Table of Contents

1. [Project Agent Protocol](#1-project-agent-protocol)
   - [Initialization](#a-initialization)
   - [Decision Matrix](#b-decision-matrix)
   - [Commands](#c-commands)
2. [Submission Templates](#2-submission-templates)
   - [Shared KB Issue Format](#shared-kb-issue-format)
3. [Curator Protocol](#3-curator-protocol)
4. [Common Workflows](#4-common-workflows)

---

## 1. Project Agent Protocol

### A. Initialization

When a Claude Code agent session starts, the `session-start.sh` hook automatically:

1. **Updates Shared KB:**
   ```bash
   git submodule update --remote --merge --quiet
   ```

2. **Loads Project Context:**
   - Reads `.kb/context/PROJECT.yaml` (structured config)
   - Reads `.kb/context/MEMORY.md` (free-form knowledge)
   - Injects content into agent context

3. **Validates Environment:**
   - Checks if `GITHUB_TOKEN` is set
   - Warns if token missing (submissions will fail)

**Agent Checklist:**
- ✅ Read PROJECT.yaml to understand project stack
- ✅ Check `sharing_criteria` before saving knowledge
- ✅ Ensure GITHUB_TOKEN is available for Shared KB submissions

---

### B. Decision Matrix

Agents must check `sharing_criteria` in `.kb/context/PROJECT.yaml` before saving knowledge.

**Decision Flow:**

```
Agent solves problem
       │
       ▼
Check sharing_criteria in PROJECT.yaml
       │
       ├── Meets "project_specific_if" criteria?
       │   │
       │   └── YES → Save to .kb/project/ (direct commit)
       │              - Business logic
       │              - Internal service names
       │              - Temporary workarounds
       │              - Environment-specific configs
       │
       └── Meets "universal_if" criteria?
           │
           └── YES → Submit to Shared KB via Issue
                      - Framework-agnostic patterns
                      - Language-specific solutions
                      - DevOps configurations
                      - Industry best practices
```

**Examples:**

| Scenario | Target | Reason |
|----------|--------|--------|
| Fixed FastAPI CORS error for specific endpoint | **Project KB** | Contains business logic (endpoint-specific) |
| Docker compose healthcheck pattern | **Shared KB** | Universal Docker pattern |
| Stripe webhook signature validation | **Project KB** | Contains business logic (payment flow) |
| Poetry dependency resolution error | **Shared KB** | Universal Python/ Poetry issue |
| Internal microservice authentication | **Project KB** | Internal service names/URLs |
| PostgreSQL connection pooling in FastAPI | **Shared KB** | Framework-agnostic database pattern |

---

### C. Commands

Agents use Python scripts from the Shared KB submodule:

#### 1. Search (Always First Step)

```bash
# Search both Project and Shared KB
python .kb/shared/tools/v5.1/kb_search.py "fastapi cors error"

# Search only Shared KB
python .kb/shared/tools/v5.1/kb_search.py "docker compose" --scope shared

# Search only Project KB
python .kb/shared/tools/v5.1/kb_search.py "stripe webhook" --scope project
```

**Output:**
```
🔍 Поиск: 'fastapi cors error' | Найдено: 2

--- SHARED KB ---
📄 .kb/shared/shared/python/fastapi-cors-001.yaml

--- PROJECT KB ---
📄 .kb/project/knowledge/cors-fix-2025-01-08.yaml
```

#### 2. Local Save (Project KB)

```bash
# Save to project KB (direct commit)
python .kb/shared/tools/v5.1/kb_submit.py \
    --target local \
    --file solution.yaml

# Output:
# ✅ [Local] Файл сохранен: .kb/project/knowledge/solution.yaml
#    Не забудьте сделать git add/commit в репозитории проекта!
```

**When to use:**
- ✅ Project-specific business logic
- ✅ Internal service integrations
- ✅ Temporary workarounds
- ✅ Environment-specific configs

**No validation required** - direct git commit to project repo.

#### 3. Shared Submission (Shared KB)

```bash
# Submit to Shared KB via GitHub Issue
python .kb/shared/tools/v5.1/kb_submit.py \
    --target shared \
    --file solution.yaml \
    --title "Docker compose healthcheck for PostgreSQL" \
    --desc "Container becomes healthy before DB is ready" \
    --domain docker

# Output:
# ✅ [Shared] Создан Issue #123: https://github.com/org/shared-kb/issues/123
#    Куратор проверит предложение в ближайшее время.
```

**Requirements:**
- ⚠️ **GITHUB_TOKEN** must be set in `.env`
- ⚠️ **--title** is required for shared submissions
- ⚠️ **--domain** helps curator categorize

**When to use:**
- ✅ Framework-agnostic solutions
- ✅ Language-specific patterns
- ✅ DevOps configurations
- ✅ Industry best practices

---

## 2. Submission Templates

### Shared KB Issue Format

When `kb_submit.py --target shared` creates an Issue, it uses this format:

```markdown
---
submission_meta:
  domain: docker
  type: error-solution
  project_source: my-ecommerce-backend
  agent_id: claude-session-abc123
  timestamp: 2026-01-08T15:30:00Z
  verified: true
  reproducible: true
---

### Problem Description
Docker Compose healthcheck passes immediately, but application fails because PostgreSQL database is still initializing.

### Proposed Entry

```yaml
version: "1.0"
category: "docker-compose"
last_updated: "2026-01-08"

errors:
  - id: "DC-HEALTH-001"
    title: "Docker Compose healthcheck race condition with PostgreSQL"
    severity: "high"
    scope: "docker"
    problem: |
      Docker Compose healthcheck passes immediately but application
      fails to connect because PostgreSQL is still initializing.
    solution:
      code: |
        services:
          postgres:
            image: postgres:15
            healthcheck:
              test: ["CMD-SHELL", "pg_isready -U postgres"]
              interval: 5s
              timeout: 5s
              retries: 5
              start_period: 10s

          app:
            depends_on:
              postgres:
                condition: service_healthy
      explanation: |
        Add `start_period` to healthcheck and use `condition: service_healthy`
        in depends_on to ensure PostgreSQL is fully ready before app starts.
```

### Context
- **Project:** my-ecommerce-backend
- **Reproducible:** Yes
- **Tested on:** Docker Compose v2.20.0, PostgreSQL 15
- **Similar issues:** None found in Shared KB
```

**Metadata Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `domain` | string | ✅ | docker, python, postgresql, javascript, etc. |
| `type` | string | ✅ | error-solution, pattern, integration |
| `project_source` | string | ✅ | Project ID from PROJECT.yaml |
| `agent_id` | string | ✅ | Claude session ID (auto-detected) |
| `timestamp` | string | ✅ | ISO 8601 datetime (auto-generated) |
| `verified` | boolean | ⚠️ | Has agent tested the solution? |
| `reproducible` | boolean | ⚠️ | Can issue be reproduced? |

---

## 3. Curator Protocol

The Curator is a **role**, not a service. It can be:
- Human (tech lead, developer)
- Agent (Claude Code with curator prompt)

### Triggering Curation

**Option 1: Human Command**
```bash
# List pending submissions
python .kb/shared/tools/v5.1/kb_curate.py --mode list

# Validate specific submission
python .kb/shared/tools/v5.1/kb_curate.py --mode validate --issue 123

# Approve submission
python .kb/shared/tools/v5.1/kb_curate.py --mode approve --issue 123

# Reject submission
python .kb/shared/tools/v5.1/kb_curate.py --mode reject \
    --issue 123 \
    --reason "Duplicate of existing entry DC-HEALTH-001"
```

**Option 2: Claude Code Agent**
```bash
# Start curator agent
claude -p curator

# Agent will:
# 1. Fetch open Issues with 'kb-submission' label
# 2. Parse YAML metadata from each Issue
# 3. Validate quality score (>= 75)
# 4. Check for duplicates
# 5. Ask for approve/reject decision
```

### Curation Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    Curator Workflow                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. FETCH                                                       │
│     ├── Get Issues with label: 'kb-submission'                 │
│     └── Filter by status: 'open'                               │
│                                                                 │
│  2. PARSE                                                       │
│     ├── Extract YAML frontmatter                               │
│     ├── Load submission metadata                               │
│     └── Parse YAML entry content                               │
│                                                                 │
│  3. VALIDATE                                                    │
│     ├── Check required fields                                  │
│     ├── Calculate quality score                                │
│     ├── Search for duplicates                                  │
│     └── Verify domain categorization                           │
│                                                                 │
│  4. DECIDE                                                     │
│     ├── /approve → Commit to Shared KB → Close Issue           │
│     ├── /request-changes → Comment with feedback               │
│     └── /reject → Comment with reason → Close Issue            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Validation Checklist

Curator must verify:

- [ ] **YAML Syntax**: Valid YAML, no parsing errors
- [ ] **Required Fields**: All mandatory fields present
- [ ] **Quality Score**: Score >= 75/100
- [ ] **No Duplicates**: Search for similar entries
- [ ] **Scope Appropriate**: Not project-specific
- [ ] **No Secrets**: No API keys, passwords, tokens
- [ ] **Tested**: Agent has verified solution works
- [ ] **Domain**: Correct domain categorization

### Quality Score Calculation

```python
def calculate_quality_score(entry):
    score = 0

    # Required fields (20 points each)
    if 'version' in entry: score += 20
    if 'category' in entry: score += 20
    if 'last_updated' in entry: score += 20

    # Content quality (40 points)
    errors = entry.get('errors', [])
    if errors:
        error = errors[0]
        if error.get('problem'): score += 10
        if error.get('solution', {}).get('code'): score += 15
        if error.get('solution', {}).get('explanation'): score += 15

    # Metadata (20 points)
    if 'domains' in errors[0]: score += 10
    if 'scope' in errors[0]: score += 10

    return score  # Max: 100
```

**Thresholds:**
- **< 50**: Reject (insufficient information)
- **50-74**: Request changes (needs improvement)
- **>= 75**: Approve (meets quality standards)

---

## 4. Common Workflows

### Workflow 1: Agent Debugs Error

```bash
# 1. Search for existing solution
python .kb/shared/tools/v5.1/kb_search.py "fastapi cors error"

# 2. If found in Shared KB, apply solution
# → Done!

# 3. If not found, solve the problem
# → Agent implements fix

# 4. Decide where to save
# → Check PROJECT.yaml sharing_criteria

# 5a. If project-specific
python .kb/shared/tools/v5.1/kb_submit.py \
    --target local \
    --file fastapi-cors-fix.yaml

# 5b. If universal
python .kb/shared/tools/v5.1/kb_submit.py \
    --target shared \
    --file fastapi-cors-fix.yaml \
    --title "FastAPI CORS error with OPTIONS preflight" \
    --domain python

# 6. If shared, track Issue URL
# → Wait for curator approval
```

### Workflow 2: New Agent Onboarding

```bash
# 1. Agent session starts
# → session-start.sh hook runs automatically

# 2. Agent reads injected context
# → PROJECT.yaml loaded into memory
# → MEMORY.md loaded into memory

# 3. Agent searches before working
python .kb/shared/tools/v5.1/kb_search.py "authentication"
python .kb/shared/tools/v5.1/kb_search.py "database"

# 4. Agent checks project structure
python .kb/shared/tools/v5.1/kb_search.py "architecture" --scope project

# 5. Agent understands context and starts working
# → Ready!
```

### Workflow 3: Curator Batch Processing

```bash
# 1. Morning: Check for new submissions
python .kb/shared/tools/v5.1/kb_curate.py --mode list

# Output:
# Issue #123: Docker compose healthcheck
# Issue #124: Poetry dependency conflict
# Issue #125: FastAPI WebSocket timeout

# 2. Process each submission
for issue in 123 124 125; do
    python .kb/shared/tools/v5.1/kb_curate.py \
        --mode validate \
        --issue $issue

    # Review output, then decide
    # python .kb/shared/tools/v5.1/kb_curate.py \
    #     --mode approve --issue $issue
done

# 3. End of day: All processed
# → Shared KB updated
# → Issues closed
```

### Workflow 4: Project Setup

```bash
# 1. Initialize Shared KB submodule
git submodule add https://github.com/org/shared-kb.git .kb/shared
git submodule update --init --recursive

# 2. Create Project KB structure
mkdir -p .kb/{context,project/{integrations,endpoints,decisions,lessons,pending}}

# 3. Create PROJECT.yaml
cat > .kb/context/PROJECT.yaml << 'EOF'
meta:
  name: "My Project"
  id: "my-project"
sharing_criteria:
  universal_if:
    - "Framework-agnostic solution"
  project_specific_if:
    - "Contains business logic"
EOF

# 4. Create MEMORY.md
cat > .kb/context/MEMORY.md << 'EOF'
# Project Memory

## Architecture Decisions
- (add decisions here)

## Lessons Learned
- (add lessons here)
EOF

# 5. Install session-start hook
cp .kb/shared/tools/v5.1/hooks/session-start.sh .claude/hooks/
chmod +x .claude/hooks/session-start.sh

# 6. Configure GitHub token
echo "GITHUB_TOKEN=ghp_your_token" > .env
echo ".env" >> .gitignore

# 7. Done!
# → Next agent session will auto-load context
```

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `No GITHUB_TOKEN found` | Token not in environment | Add `GITHUB_TOKEN=xxx` to `.env` file |
| `PyGithub not installed` | Missing dependency | Run `pip install PyGithub` |
| `Issue creation failed` | Invalid repo URL or token | Check `SHARED_KB_REPO` in environment |
| `Quality score too low` | Incomplete YAML entry | Add missing fields (problem, solution, explanation) |
| `Duplicate entry found` | Similar entry exists | Search KB, update existing instead |
| `Submodule not updating` | Network or git config | Run `git submodule update --remote --merge` |

---

**Document Status:** ✅ Ready for Use
**Next Review:** 2026-02-01
