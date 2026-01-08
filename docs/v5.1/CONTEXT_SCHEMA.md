# Project Context Schema v5.1

**Version:** 5.1.0
**Last Updated:** 2026-01-08

---

## Overview

The `.kb/context/` directory contains the **project passport** - structured and free-form information that helps Claude Code agents understand the project context and make informed decisions about knowledge sharing.

**Directory Structure:**
```
.kb/context/
├── PROJECT.yaml    # Structured configuration (required)
└── MEMORY.md       # Free-form knowledge (optional)
```

---

## 1. PROJECT.yaml

This file is the **"brain"** for agent decision-making. It provides:
- Project identity and metadata
- `sharing_criteria` rules (most important!)
- Technology stack information
- Integration references
- Team information

### 1.1. Complete Schema

```yaml
# === Project Identity ===
meta:
  name: string              # Project name (required)
  id: string                # Unique project ID (required)
  description: string       # Short description (optional)
  type: string              # Project type (optional)
                            # Options: api-service, web-app, cli-tool, library, etc.
  started: string           # Start date (optional, ISO 8601)
  repository: string        # Git repository URL (optional)

# === Sharing Criteria (MOST IMPORTANT!) ===
# This section controls agent behavior for knowledge submission
sharing_criteria:
  # Agents will submit to Shared KB if ANY of these conditions match
  universal_if:
    - string                # Condition description
    - string                # Example: "Framework-agnostic solution"
    - string                # Example: "Applies to any Python project"

  # Agents will save to Project KB if ANY of these conditions match
  project_specific_if:
    - string                # Condition description
    - string                # Example: "Contains internal service names"
    - string                # Example: "Business logic specific to this project"

# === Technology Stack ===
stack:
  language: string          # Primary language (optional)
  version: string           # Language version (optional)
  framework: string         # Framework (optional)
  database: string          # Database (optional)
  orm: string              # ORM/ODM (optional)
  testing: string          # Testing framework (optional)
  deployment: string       # Deployment method (optional)

  # Additional tools (optional)
  tools:
    - name: string          # Tool name
      version: string       # Version (optional)
      purpose: string       # Purpose (optional)

# === Integration References ===
# Links to knowledge entries about integrations
integrations:
  - name: string            # Integration name
    type: string            # Type: payment, email, storage, etc.
    docs: string            # Path to docs in .kb/project/
    url: string             # External URL (optional)

# === Project Goals ===
goals:
  current: string           # Current sprint/goal (optional)
  priorities:               # Priority list (optional)
    - string
    - string

  upcoming:                 # Upcoming features (optional)
    - string

# === Team Information ===
team:
  tech_lead: string         # Tech lead name (optional)
  developers:               # Developer list (optional)
    - name: string
      role: string
  kb_curator: string        # Curator role/person (optional)

# === Development Workflow ===
workflow:
  git_branches:             # Git branching strategy (optional)
    main: string            # Main branch name
    develop: string         # Develop branch name

  testing:                  # Testing approach (optional)
    framework: string
    coverage_threshold: int # Percentage

  code_review:              # Code review process (optional)
    required: boolean
    reviewers: int          # Number of required reviewers

# === Important Paths ===
paths:
  tests: string            # Path to tests (optional)
  docs: string             # Path to docs (optional)
  configs: string          # Path to configs (optional)

# === Known Issues ===
known_issues:              # Known problems (optional)
  - description: string
    workaround: string
    status: string         # open, monitoring, resolved
```

### 1.2. Required Fields

Only these fields are **required**:
- `meta.name` - Project name
- `meta.id` - Unique project ID
- `sharing_criteria.universal_if` - At least one condition
- `sharing_criteria.project_specific_if` - At least one condition

### 1.3. Sharing Criteria Examples

**Example 1: E-Commerce Backend**
```yaml
sharing_criteria:
  universal_if:
    - "Solution applies to any FastAPI/Python project"
    - "Docker or Kubernetes configuration"
    - "PostgreSQL or Redis pattern"
    - "Generic error handling or logging"
    - "Open-source library integration"

  project_specific_if:
    - "Contains Stripe payment logic"
    - "Has product catalog business rules"
    - "References internal microservice names"
    - "Contains discount/coupon logic"
    - "Temporary workaround for specific client"
```

**Example 2: Internal CLI Tool**
```yaml
sharing_criteria:
  universal_if:
    - "Python packaging or CLI framework pattern"
    - "Cross-platform compatibility fix"
    - "Generic file processing logic"

  project_specific_if:
    - "Internal API authentication"
    - "Company-specific data formats"
    - "Internal tool orchestration"
```

**Example 3: Library Project**
```yaml
sharing_criteria:
  universal_if:
    - "Any documentation or examples"
    - "Bug fixes that apply to users"
    - "Installation or setup instructions"
    - "API design patterns"

  project_specific_if:
    - "Release management process"
    - "Internal build scripts"
    - "CI/CD pipeline configurations"
```

---

## 2. MEMORY.md

This file contains **free-form knowledge** that doesn't fit into structured YAML. It's a place for:
- Architectural decision history
- Lessons learned
- Onboarding tips
- Known issues and workarounds
- Project conventions

### 2.1. Suggested Structure

```markdown
# Project Memory

_Last updated: 2026-01-08_

---

## Architecture Decisions

### Database Choice (2025-01-15)
**Decision:** Use PostgreSQL instead of MySQL
**Reason:** Required JSON field support for flexible product attributes
**Impact:** Positive - JSONB queries perform well

### Authentication Strategy (2025-02-01)
**Decision:** JWT tokens with refresh token rotation
**Reason:** Better UX than session-based auth, more secure than long-lived tokens
**Implementation:** See `.kb/project/integrations/jwt-setup.yaml`

### Payment Provider (2025-03-10)
**Decision:** Stripe instead of PayPal
**Reason:** Better API documentation, webhook support
**Lessons:** Always verify webhook signatures (see lessons/stripe-webhook-security.yaml)

---

## Lessons Learned

### Performance
- **Don't use `ujson` with SQLAlchemy** (causes segfaults)
- **Use connection pooling for PostgreSQL** (min 5, max 20 connections)
- **Cache static responses with Redis** (reduces DB load by 60%)

### Security
- **Always validate webhook signatures** (Stripe, SendGrid, etc.)
- **Never commit `.env` files** (use `.env.example` template)
- **Rotate JWT secrets every 90 days** (document in `.kb/project/pending/`)

### Testing
- **Integration tests need test database** (don't use production)
- **Mock external APIs in tests** (Stripe, email, etc.)
- **Test coverage should stay above 80%** (CI blocks if lower)

### Development Workflow
- **Always run tests before committing** (`pytest -v`)
- **Use feature branches** (`feature/ticket-name`)
- **Update CHANGELOG.md** for any user-facing changes

---

## Known Issues

### Current Issues
- **Rate limiting on Stripe API** (2025-06-01)
  - **Status:** Monitoring
  - **Workaround:** Implement exponential backoff
  - **Related Issue:** #123
  - **KB Entry:** `.kb/project/lessons/stripe-rate-limit.yaml`

- **WebSocket connections drop after 30s** (2025-06-05)
  - **Status:** Investigating
  - **Workaround:** Client reconnects automatically
  - **Related Issue:** #127

### Resolved Issues
- **Memory leak in background worker** (2025-05-15)
  - **Status:** ✅ Resolved
  - **Solution:** Upgraded to Celery 5.3
  - **KB Entry:** `.kb/project/lessons/celery-memory-leak.yaml`

---

## Onboarding Tips

### For New Developers
1. **Set up environment:** Copy `.env.example` to `.env` and fill in values
2. **Run tests:** `pytest -v` to verify setup
3. **Read architecture:** Check `.kb/project/knowledge/architecture/` first
4. **Join Slack:** `#dev-team` channel for questions

### For New Agents
1. **Search KB first:** Always run `kb_search.py` before solving
2. **Check sharing criteria:** Read `.kb/context/PROJECT.yaml` before saving
3. **Verify solutions:** Test your fix before creating KB entry
4. **Provide context:** Include error messages, stack traces, and environment info

---

## Project Conventions

### Code Style
- **Python:** Follow PEP 8, use `black` for formatting
- **JavaScript:** Use ESLint with Airbnb config
- **Commits:** Conventional Commits format (`feat:`, `fix:`, `docs:`)

### File Organization
- **Models:** `src/models/` (database models)
- **API:** `src/api/` (FastAPI endpoints)
- **Services:** `src/services/` (business logic)
- **Utils:** `src/utils/` (helper functions)

### Naming Conventions
- **Files:** `kebab-case.yaml` (KB entries), `snake_case.py` (code)
- **Variables:** `snake_case` (Python), `camelCase` (JavaScript)
- **Constants:** `UPPER_SNAKE_CASE`

---

## Integration References

### Quick Links
- **Stripe Integration:** `.kb/project/integrations/stripe.yaml`
- **PostgreSQL Setup:** `.kb/project/integrations/postgresql.yaml`
- **Docker Deployment:** `.kb/project/integrations/docker-compose.yaml`

### External Docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Stripe API:** https://stripe.com/docs/api
- **PostgreSQL:** https://www.postgresql.org/docs/

---

## Environment Variables

### Required
```bash
DATABASE_URL=postgresql://user:pass@localhost/db
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
JWT_SECRET=your-jwt-secret
```

### Optional
```bash
REDIS_URL=redis://localhost:6379/0
SENTRY_DSN=https://xxx@sentry.io/xxx
LOG_LEVEL=INFO
```

---

## Glossary

- **Shared KB:** Universal knowledge base (`.kb/shared/` submodule)
- **Project KB:** Project-specific knowledge (`.kb/project/`)
- **Curator:** Role that reviews submissions to Shared KB
- **Agent:** Claude Code AI assistant
- **Submission:** GitHub Issue created to propose Shared KB entry

---

_Last updated by: Agent claude-code-session-abc123_
_Update frequency: After major architectural decisions or lessons learned_
```

### 2.2. Best Practices

**DO:**
- ✅ Update after architectural decisions
- ✅ Document lessons learned (positive and negative)
- ✅ Include dates for decisions
- ✅ Link to KB entries where applicable
- ✅ Keep it organized with clear sections

**DON'T:**
- ❌ Duplicate information from PROJECT.yaml
- ❌ Include sensitive data (passwords, tokens)
- ❌ Make it too long (> 500 lines)
- ❌ Use vague descriptions ("fixed a bug")
- ❌ Forget to update it (stale memory is useless)

---

## 3. Example Files

### 3.1. Minimal PROJECT.yaml

```yaml
meta:
  name: "My Project"
  id: "my-project"

sharing_criteria:
  universal_if:
    - "Generic solution applicable to other projects"
  project_specific_if:
    - "Business logic specific to this project"
```

### 3.2. Complete PROJECT.yaml

```yaml
meta:
  name: "E-Commerce Backend"
  id: "ecom-backend-v2"
  description: "FastAPI-based e-commerce platform"
  type: "api-service"
  started: "2025-01-15"
  repository: "https://github.com/company/ecom-backend"

sharing_criteria:
  universal_if:
    - "Solution applies to any FastAPI/Python project"
    - "Docker, PostgreSQL, or Redis patterns"
    - "Open-source library integrations"
    - "Generic error handling or logging"

  project_specific_if:
    - "Contains Stripe payment logic"
    - "Product catalog business rules"
    - "Internal microservice names"
    - "Discount/coupon logic"
    - "Client-specific workarounds"

stack:
  language: "Python"
  version: "3.11"
  framework: "FastAPI"
  database: "PostgreSQL 15"
  orm: "SQLAlchemy 2.0"
  testing: "pytest"
  deployment: "Docker Compose"

  tools:
    - name: "Redis"
      version: "7.0"
      purpose: "Caching and sessions"
    - name: "Celery"
      version: "5.3"
      purpose: "Background tasks"

integrations:
  - name: "Stripe"
    type: "payment"
    docs: ".kb/project/integrations/stripe.yaml"
    url: "https://stripe.com/docs"
  - name: "SendGrid"
    type: "email"
    docs: ".kb/project/integrations/sendgrid.yaml"

goals:
  current: "Implementing subscription billing"
  priorities:
    - "Security audit"
    - "Performance optimization"
    - "API v2 documentation"

  upcoming:
    - "Multi-currency support"
    - "Advanced analytics"

team:
  tech_lead: "Jane Smith"
  developers:
    - name: "John Doe"
      role: "Backend Developer"
    - name: "Alice Johnson"
      role: "DevOps Engineer"
  kb_curator: "tech-lead"

workflow:
  git_branches:
    main: "main"
    develop: "develop"

  testing:
    framework: "pytest"
    coverage_threshold: 80

  code_review:
    required: true
    reviewers: 1

paths:
  tests: "tests/"
  docs: "docs/"
  configs: "config/"

known_issues:
  - description: "Stripe rate limiting on peak hours"
    workaround: "Implement exponential backoff"
    status: "monitoring"
```

### 3.3. Minimal MEMORY.md

```markdown
# Project Memory

## Architecture Decisions
- (add decisions here)

## Lessons Learned
- (add lessons here)

## Onboarding Tips
1. Copy `.env.example` to `.env`
2. Run `pytest -v` to verify setup
3. Search KB before solving problems
```

---

## 4. Validation

### 4.1. PROJECT.yaml Validation

The `kb_validate.py` tool checks:
- ✅ Required fields present
- ✅ `sharing_criteria` has both sections
- ✅ Valid YAML syntax
- ✅ No duplicate keys

### 4.2. MEMORY.md Validation

The tool checks:
- ✅ File exists (optional)
- ✅ Valid Markdown (if present)
- ✅ Size < 100 KB (prevent bloated files)

---

## 5. Usage in Agents

### 5.1. Automatic Loading

The `session-start.sh` hook automatically injects context:

```bash
# Loads PROJECT.yaml into agent context
cat .kb/context/PROJECT.yaml

# Loads MEMORY.md into agent context
cat .kb/context/MEMORY.md
```

### 5.2. Agent Decision Making

Agents use `sharing_criteria` to decide:

```python
# Pseudo-code for agent decision
def decide_where_to_save(knowledge, project_context):
    criteria = project_context['sharing_criteria']

    # Check project-specific criteria
    for condition in criteria['project_specific_if']:
        if matches_condition(knowledge, condition):
            return 'project'

    # Check universal criteria
    for condition in criteria['universal_if']:
        if matches_condition(knowledge, condition):
            return 'shared'

    # Default: ask user
    return 'ask'
```

---

**Document Status:** ✅ Ready for Use
**Next Review:** 2026-02-01
