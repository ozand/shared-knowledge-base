# YAML Schema Enhancement v3.1
## GitHub Integration Metadata

**Version:** 3.1
**Last Updated:** 2026-01-07

---

## Overview

Shared Knowledge Base v3.1 extends the YAML schema with two new optional sections:

1. **`domains`** - Domain classification for progressive loading
2. **`github`** - GitHub integration metadata for issue-based contributions

---

## Complete YAML Schema

### Minimal Entry (v2.0 compatible)

```yaml
version: "1.0"
category: "category-name"
last_updated: "2026-01-07"

errors:
  - id: "ERROR-001"
    title: "Error Title"
    severity: "high"
    scope: "python"

    problem: |
      Description of what went wrong

    solution:
      code: |
        # Solution code
      explanation: |
        How it works
```

---

### Enhanced Entry (v3.1 with domains + github)

```yaml
version: "1.0"
category: "category-name"
last_updated: "2026-01-07"

errors:
  - id: "ERROR-001"
    title: "Error Title"
    severity: "high"
    scope: "python"

    # NEW: Domain classification (v3.1)
    domains:
      primary: "testing"
      secondary: ["asyncio"]

    # NEW: GitHub integration metadata (v3.1)
    github:
      issue_number: 123
      issue_url: "https://github.com/ozand/shared-knowledge-base/issues/123"
      issue_status: "approved"
      contribution_date: "2026-01-07"
      merged_by: "curator"
      merge_commit: "abc123def456"
      agent_attribution:
        agent_type: "claude-code"
        agent_version: "4.5"
        source_repository: "mycompany/myproject"
        local_kb_path: ".kb/local/ERROR-001.yaml"

    problem: |
      Description of what went wrong

    symptoms:
      - "Error message or symptom"

    solution:
      code: |
        # Solution code
      explanation: |
        How it works

    prevention:
      - "How to avoid this error"

    tags: ["tag1", "tag2", "tag3"]
```

---

## Field Specifications

### 1. `domains` Section

**Purpose:** Classify entry into knowledge domains for progressive loading.

**Structure:**

```yaml
domains:
  primary: "domain-name"        # Required, single domain
  secondary: ["domain-name"]    # Optional, array of related domains
```

**Available Primary Domains:**

- `testing` - Test patterns, pytest, unittest
- `asyncio` - Async/await, task groups
- `fastapi` - FastAPI framework
- `websocket` - WebSocket patterns
- `docker` - Containers, volumes, networks
- `postgresql` - Database operations
- `authentication` - Auth, JWT, sessions
- `deployment` - DevOps, CI/CD
- `monitoring` - Logging, metrics
- `security` - Security patterns
- `api` - REST API patterns
- `performance` - Optimization

**Examples:**

```yaml
# Single domain
domains:
  primary: "testing"

# Multiple related domains
domains:
  primary: "testing"
  secondary: ["asyncio"]
```

---

### 2. `github` Section

**Purpose:** Track GitHub issue-based contribution workflow.

**Structure:**

```yaml
github:
  # Required fields (populated after issue creation)
  issue_number: 123                    # Issue number in Shared KB repo
  issue_url: "https://..."             # Full issue URL
  issue_status: "pending"              # Current status
  contribution_date: "2026-01-07"      # When submitted

  # Optional fields (populated after approval)
  merged_by: "curator-username"         # Who approved/merged
  merge_commit: "abc123def"            # Merge commit hash

  # Agent attribution (for agent-submitted entries)
  agent_attribution:
    agent_type: "claude-code"          # Agent type
    agent_version: "4.5"               # Agent version
    source_repository: "org/repo"      # Source repository
    local_kb_path: ".kb/local/..."     # Local file path
```

**Status Values:**

- `pending` - Initial submission, awaiting review
- `reviewing` - Curator is reviewing
- `approved` - Approved for merge
- `rejected` - Rejected with feedback
- `changes_requested` - Changes needed before approval

---

## Examples

### Example 1: Local-Only Entry (Before Submission)

```yaml
version: "1.0"
category: "testing"
last_updated: "2026-01-07"

errors:
  - id: "LOCAL-TEST-001"
    title: "Local Test Issue"
    severity: "medium"
    scope: "project"

    domains:
      primary: "testing"

    # No github section yet (not submitted)
    local_only: true

    problem: |
      Project-specific test issue

    solution:
      code: |
        # Local solution
```

---

### Example 2: Submitted Entry (Pending Review)

```yaml
version: "1.0"
category: "testing"
last_updated: "2026-01-07"

errors:
  - id: "TEST-001"
    title: "Async Test Without Decorator"
    severity: "high"
    scope: "python"

    domains:
      primary: "testing"
      secondary: ["asyncio"]

    github:
      issue_number: 123
      issue_url: "https://github.com/ozand/shared-knowledge-base/issues/123"
      issue_status: "pending"
      contribution_date: "2026-01-07"
      agent_attribution:
        agent_type: "claude-code"
        agent_version: "4.5"
        source_repository: "mycompany/myproject"
        local_kb_path: ".kb/local/TEST-001.yaml"

    problem: |
      Async test missing @pytest.mark.asyncio

    solution:
      code: |
        @pytest.mark.asyncio
        async def test_my_async_func():
            assert True
```

---

### Example 3: Approved Entry (Merged to Shared KB)

```yaml
version: "1.0"
category: "testing"
last_updated: "2026-01-07"

errors:
  - id: "TEST-001"
    title: "Async Test Without Decorator"
    severity: "high"
    scope: "python"

    domains:
      primary: "testing"
      secondary: ["asyncio"]

    github:
      issue_number: 123
      issue_url: "https://github.com/ozand/shared-knowledge-base/issues/123"
      issue_status: "approved"
      contribution_date: "2026-01-07"
      merged_by: "kb-curator"
      merge_commit: "abc123def456"
      agent_attribution:
        agent_type: "claude-code"
        agent_version: "4.5"
        source_repository: "mycompany/myproject"
        local_kb_path: ".kb/local/TEST-001.yaml"

    problem: |
      Async test missing @pytest.mark.asyncio

    solution:
      code: |
        @pytest.mark.asyncio
        async def test_my_async_func():
            assert True
```

---

## Migration Guide

### For Existing Entries (v2.0 → v3.1)

**Step 1: Add domain metadata**

```bash
# Automatic migration from tags
python tools/kb_domains.py migrate --from-tags
```

**Step 2: Submit to Shared KB (optional)**

```bash
# Submit via GitHub Issues
python tools/kb.py submit --entry path/to/entry.yaml
```

**Step 3: Update local YAML with github metadata**

After issue creation, the YAML will be automatically updated with:

```yaml
github:
  issue_number: 123
  issue_url: "https://..."
  issue_status: "pending"
  contribution_date: "2026-01-07"
```

---

### For New Entries

Start with enhanced schema from the beginning:

```yaml
version: "1.0"
category: "category-name"
last_updated: "2026-01-07"

errors:
  - id: "CATEGORY-NNN"
    title: "Title"
    severity: "high"
    scope: "python"

    # Add domains immediately
    domains:
      primary: "testing"
      secondary: ["asyncio"]

    # github section will be added after submission
    # (don't add manually)

    problem: |
      Description

    solution:
      code: |
        # Solution
```

---

## Validation

### Check YAML Syntax

```bash
# Validate entry
python tools/kb.py validate path/to/entry.yaml
```

### Check Domain Metadata

```bash
# Validate domains
python tools/kb_domains.py validate
```

### Check GitHub Metadata (Coming Soon)

```bash
# Validate GitHub metadata
python tools/kb.py validate-github path/to/entry.yaml
```

---

## Backward Compatibility

✅ **Fully backward compatible with v2.0**

- Old entries without `domains` or `github` sections still work
- These sections are **optional**
- All existing tools continue to function
- Progressive loading gracefully handles entries without domains

---

## Best Practices

### 1. Domain Selection

**Choose primary domain based on:**
- Main topic of the error/pattern
- Technology stack involved
- Typical use case

**Example:**
- Async test error → `testing` (not `asyncio`)
- Docker volume error → `docker`
- FastAPI dependency issue → `fastapi`

### 2. GitHub Metadata

**Don't add manually** - let `kb submit` populate it.

**Exception:** If manually creating issue in GitHub, you can add:

```yaml
github:
  issue_number: 123
  issue_url: "https://..."
  issue_status: "pending"
```

### 3. Local-Only Entries

Mark project-specific entries:

```yaml
domains:
  primary: "project"  # or your custom domain

github: {}  # Empty or omit entirely (no GitHub submission)
local_only: true
```

---

## Related Documentation

- **`QUICKSTART-DOMAINS.md`** - Progressive loading guide
- **`tmp/integrated-improvement-roadmap.md`** - Complete roadmap
- **`for-projects/.github/workflows/`** - GitHub Actions templates

---

**Version:** 3.1
**Status:** YAML Schema Enhanced
**Backward Compatible:** Yes
