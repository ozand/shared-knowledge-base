# Progressive Domain-Based Loading: Visual Guide
## Диаграммы, схемы и примеры конфигураций

**Дата:** 2026-01-07
**Связанные документы:**
- `progressive-domain-loading-proposal.md` - Architecture proposal
- `progressive-loading-implementation-guide.md` - Technical implementation

---

## Architecture Overview

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Claude Code Agent                           │
│                                                                      │
│  Task: "Fix async test error in FastAPI WebSocket"                  │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Progressive Loading Engine                        │
│                                                                      │
│  1. Analyze Task → Extract Keywords: async, test, websocket        │
│  2. Load Index → _domain_index.yaml (200 tokens)                    │
│  3. Match Domains → testing, asyncio, websocket                     │
│  4. Load Domains → Git sparse checkout / GitHub API                 │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌────────────────┐  ┌─────────────────┐  ┌──────────────────┐
│ Testing Domain │  │ AsyncIO Domain  │  │ WebSocket Domain │
│                │  │                 │  │                  │
│ • 15 entries   │  │ • 22 entries    │  │ • 8 entries      │
│ • 3,500 tokens │  │ • 4,800 tokens  │  │ • 1,200 tokens   │
└────────────────┘  └─────────────────┘  └──────────────────┘

         Total: 9,500 tokens (vs 50,000 full KB)
         Time: ~2-3 seconds
```

---

## Data Flow Diagram

### Workflow 1: Initial Setup

```
┌──────────────┐
│ New Project  │
└──────┬───────┘
       │
       │ git submodule add --sparse <repo> docs/kb
       ▼
┌──────────────────────────┐
│ Sparse Checkout Setup    │
│                          │
│ ✓ _domain_index.yaml     │ ← 200 tokens
│ ✓ _index.yaml            │ ← 50 tokens
│ ✓ .claude/               │ ← 100 tokens
└──────────┬───────────────┘
           │
           │ Total: ~350 tokens (vs 50,000)
           ▼
┌──────────────────────────┐
│ Agent Starts             │
│                          │
│ 1. Load index            │
│ 2. Analyze task          │
│ 3. Decide domains        │
└──────────────────────────┘
```

### Workflow 2: Progressive Domain Loading

```
┌──────────────────────────────┐
│ Agent Receives Task          │
│                              │
│ "Help me fix async test"     │
└──────┬───────────────────────┘
       │
       │ Keywords: async, test
       ▼
┌──────────────────────────────┐
│ Load Domain Index            │
│                              │
│ _domain_index.yaml           │
│                              │
│ domains:                     │
│   testing: 3,500 tokens      │ ← Match!
│   asyncio: 4,800 tokens      │ ← Match!
│   fastapi: 3,200 tokens      │
└──────┬───────────────────────┘
       │
       │ Decision: Load testing + asyncio
       ▼
┌──────────────────────────────┐
│ Git Sparse Checkout          │
│                              │
│ git sparse-checkout add      │
│   python/errors/testing.yaml │
│   python/errors/asyncio.yaml │
│   universal/patterns/*.yaml  │
└──────┬───────────────────────┘
       │
       │ Loaded: 8,300 tokens
       ▼
┌──────────────────────────────┐
│ Agent Works with Knowledge   │
│                              │
│ ✓ Test patterns              │
│ ✓ Async patterns             │
│ ✓ Examples                   │
└──────────────────────────────┘
```

### Workflow 3: Selective Update

```
┌──────────────────────────────┐
│ Domain Updated in Shared KB  │
│                              │
│ testing.yaml: +3 new entries │
└──────┬───────────────────────┘
       │
       │ GitHub Actions Trigger
       ▼
┌──────────────────────────────┐
│ Project: kb sync --domain    │
│                              │
│ 1. Check _domain_index.yaml  │
│ 2. Compare versions          │
│ 3. Download changed files    │
└──────┬───────────────────────┘
       │
       │ Updated: 300 new tokens
       ▼
┌──────────────────────────────┐
│ Local KB Updated             │
│                              │
│ ✓ testing.yaml refreshed     │
│ ✓ Index updated              │
│ ✓ Ready for use              │
└──────────────────────────────┘
```

---

## File Structure Comparison

### Before (Monolithic)

```
shared-knowledge-base/
├── python/
│   ├── errors/
│   │   ├── testing.yaml           ← 5 entries, 1,200 tokens
│   │   ├── asyncio.yaml           ← 12 entries, 2,600 tokens
│   │   ├── imports.yaml           ← 4 entries, 800 tokens
│   │   └── type-checking.yaml     ← 4 entries, 700 tokens
│   └── patterns/
│       ├── async-patterns.yaml    ← 6 entries, 1,200 tokens
│       └── testing-patterns.yaml  ← 7 entries, 1,800 tokens
├── docker/
│   └── errors/
│       ├── common-errors.yaml     ← 6 entries, 1,400 tokens
│       └── network-errors.yaml    ← 3 entries, 700 tokens
└── _index.yaml                    ← 40 entries, 50 tokens

Total: 134 entries, ~50,000 tokens (when loaded fully)
```

### After (Domain-Organized)

```
shared-knowledge-base/
├── _domain_index.yaml             ← NEW: 200 tokens, all domains metadata
├── python/
│   ├── errors/
│   │   ├── testing.yaml           ← Enhanced with domain metadata
│   │   │   └── errors:
│   │   │       - domains:
│   │   │           primary: "testing"
│   │   │           secondary: ["asyncio"]
│   │   ├── asyncio.yaml           ← Enhanced with domain metadata
│   │   │   └── errors:
│   │   │       - domains:
│   │   │           primary: "asyncio"
│   │   │           secondary: ["testing"]
│   │   └── ...
│   └── patterns/
│       └── ...
├── tools/
│   ├── kb_domains.py              ← NEW: Domain management
│   └── kb_github_api.py           ← NEW: GitHub API fallback
└── .github/
    └── workflows/
        └── kb-domain-update.yml   ← NEW: Selective updates

Progressive loading:
├── Step 1: Load _domain_index.yaml (200 tokens)
├── Step 2: Analyze task → Need "testing" domain
└── Step 3: Load testing domain (3,500 tokens)

Total: 3,700 tokens (vs 50,000)
```

---

## Configuration Examples

### Example 1: Minimal Project Configuration

**`.kb-config.yaml`** - Small project (single domain)

```yaml
# Minimal config: Only testing domain
knowledge_base:
  type: "sparse-checkout"
  repository: "https://github.com/ozand/shared-knowledge-base.git"
  path: "docs/kb"

  initial_load:
    - "_domain_index.yaml"
    - ".claude/"

  preferred_domains:
    - "testing"

  on_demand:
    mode: "sparse-checkout"

  updates:
    mode: "manual"  # Agent decides when to sync
```

**Result:** ~3,700 tokens on startup

---

### Example 2: Medium Project Configuration

**`.kb-config.yaml`** - Multiple domains

```yaml
# Medium config: 3 domains
knowledge_base:
  type: "sparse-checkout"
  repository: "https://github.com/ozand/shared-knowledge-base.git"
  path: "docs/knowledge-base"

  initial_load:
    - "_domain_index.yaml"
    - "_index.yaml"
    - ".claude/"

  preferred_domains:
    - "testing"      # Load immediately
    - "asyncio"      # Load immediately
    - "fastapi"      # Load on-demand

  on_demand:
    mode: "sparse-checkout"
    fallback: "github-api"  # Use API if sparse checkout fails

  updates:
    mode: "scheduled"  # Auto-sync daily
    time: "02:00"      # 2 AM UTC
    domains:
      - "testing"
      - "asyncio"

  versioning:
    testing: "v1.2.0"      # Pinned version
    asyncio: "latest"      # Always latest
```

**Result:** ~8,500 tokens on startup

---

### Example 3: Large Project Configuration

**`.kb-config.yaml`** - All domains

```yaml
# Large config: All domains, versioned
knowledge_base:
  type: "full-clone"  # Clone everything
  repository: "https://github.com/ozand/shared-knowledge-base.git"
  path: "docs/knowledge-base"

  initial_load:
    - "_domain_index.yaml"
    - ".claude/"

  preferred_domains:
    - "testing"
    - "asyncio"
    - "fastapi"
    - "websocket"
    - "docker"
    - "postgresql"

  on_demand:
    mode: "full-clone"  # All domains available

  updates:
    mode: "selective"  # Update domains independently
    strategy: "git-tags"  # Use Git tags for versioning

  versioning:
    testing: "v1.2.0"
    asyncio: "v2.1.0"
    fastapi: "v1.0.5"
    websocket: "latest"
    docker: "v1.3.0"
    postgresql: "latest"

  cache:
    enabled: true
    path: ".cache/kb-domains"
    ttl: 86400  # 24 hours
```

**Result:** ~20,000 tokens on startup (vs 50,000 monolithic)

---

## Domain Metadata Examples

### Example 1: Single-Domain Entry

**`python/errors/testing.yaml`**

```yaml
version: "1.0"
category: "testing"
last_updated: "2026-01-07"

errors:
  - id: "TEST-001"
    title: "Async Test Without @pytest.mark.asyncio"
    severity: "high"
    scope: "python"

    # NEW: Domain classification
    domains:
      primary: "testing"
      secondary: []  # No secondary domains

    problem: |
      Async test functions fail if missing @pytest.mark.asyncio decorator.

    symptoms:
      - "RuntimeWarning: coroutine was never awaited"

    solution:
      code: |
        @pytest.mark.asyncio
        async def test_websocket():
            assert True

    tags: ["async", "pytest", "testing"]
```

---

### Example 2: Cross-Domain Entry

**`python/errors/async-testing.yaml`**

```yaml
version: "1.0"
category: "testing"
last_updated: "2026-01-07"

errors:
  - id: "ASYNC-TEST-001"
    title: "Async Test Timeout in Event Loop"
    severity: "high"
    scope: "python"

    # NEW: Multiple domains
    domains:
      primary: "testing"          # Primary: It's a test error
      secondary: ["asyncio"]      # Secondary: Involves asyncio

    problem: |
      Async test times out when event loop is blocked.

    symptoms:
      - "asyncio.TimeoutError"
      - Test hangs >30 seconds

    solution:
      code: |
        @pytest.mark.asyncio
        async def test_with_timeout():
            async with asyncio.timeout(5):
                await slow_operation()

    tags: ["async", "testing", "timeout", "asyncio", "event-loop"]

    # NEW: Cross-references
    related_entries:
      - "TEST-002"  # AsyncMock pattern
      - "ASYNC-001"  # Async timeout pattern
```

---

## Token Usage Comparison

### Scenario 1: Small Project (FastAPI + Testing)

**Before (Monolithic):**
```
Full KB: 50,000 tokens
├─ All Python entries: 5,000 tokens
├─ All Docker entries: 12,000 tokens
├─ All FastAPI entries: 3,200 tokens
├─ All testing entries: 3,500 tokens
├─ All asyncio entries: 4,800 tokens
└─ All other entries: 21,500 tokens (unused!)

Context overflow risk: HIGH
```

**After (Progressive):**
```
Domain Index: 200 tokens
├─ See all domains metadata
└─ Decide what to load

Testing Domain: 3,500 tokens
├─ python/errors/testing.yaml
├─ universal/patterns/testing.yaml
└─ javascript/errors/testing.yaml

AsyncIO Domain: 4,800 tokens
├─ python/errors/asyncio.yaml
├─ universal/patterns/async.yaml
└─ framework/fastapi/errors/async.yaml

Total: 8,500 tokens (83% reduction!)
Context overflow risk: LOW
```

---

### Scenario 2: Medium Project (Multi-Domain)

**Project:** Django backend with PostgreSQL, Docker, Redis

**Before:**
```
Full KB: 50,000 tokens
Context loading: 5-10 seconds
Token budget: 50% of context window
```

**After:**
```
Domain Index: 200 tokens
PostgreSQL Domain: 2,800 tokens
Docker Domain: 2,800 tokens
Django Domain: 3,200 tokens

Total: 9,000 tokens (82% reduction!)
Context loading: 2-3 seconds
Token budget: 9% of context window
```

---

## Command Examples

### Basic Commands

```bash
# Domain management
kb list-domains                    # List all domains
kb load-domain testing             # Load testing domain
kb unload-domain docker            # Unload docker domain
kb sync --domain testing           # Sync testing domain

# Multiple domains
kb load-domain testing asyncio fastapi

# All domains
kb load-domain all                 # Full checkout
kb unload-domain all               # Reset to sparse

# Status
kb status                          # Show loaded domains
kb info testing                    # Show domain metadata
```

### Advanced Commands

```bash
# Version management
kb pin testing v1.2.0              # Pin domain version
kb unpin testing                   # Use latest version
kb list-versions testing           # Show available versions

# Cache management
kb cache clear                     # Clear domain cache
kb cache status                    # Show cache stats

# Migration
kb migrate --from-tags             # Auto-generate domains
kb validate-domains                # Check consistency
```

---

## Integration Examples

### Example 1: Claude Code Agent Workflow

```python
# Agent-side progressive loading
from tools.kb_domains import DomainManager

def agent_task_handler(task: str):
    """Handle agent task with progressive loading."""

    # 1. Analyze task
    keywords = extract_keywords(task)
    # ['async', 'test', 'fastapi']

    # 2. Load index (lightweight)
    manager = DomainManager(kb_dir)
    index = manager.load_index()  # 200 tokens

    # 3. Match domains
    domains_needed = match_domains(index, keywords)
    # ['testing', 'asyncio', 'fastapi']

    # 4. Load domains progressively
    for domain in domains_needed:
        manager.load_domain(domain)

    # 5. Work with knowledge
    relevant_kb = search_domains(domains_needed, task)

    return relevant_kb
```

---

### Example 2: GitHub Actions Integration

**`.github/workflows/kb-sync.yml`**

```yaml
name: Sync Knowledge Base

on:
  workflow_dispatch:
    inputs:
      domain:
        description: 'Domain to sync'
        required: true
        type: choice
        options:
          - testing
          - asyncio
          - fastapi
          - docker
          - all

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout KB
        uses: actions/checkout@v4
        with:
          repository: 'ozand/shared-knowledge-base'
          path: 'kb'

      - name: Sync domain
        run: |
          cd kb
          python tools/kb_domains.py sync ${{ inputs.domain }}

      - name: Update project KB
        run: |
          kb sync --from kb --domain ${{ inputs.domain }}
```

---

## Performance Visualization

### Loading Time Comparison

```
Monolithic (Before):
████████████████████████████████████████ 10 seconds
50,000 tokens

Progressive (After):
███ 2 seconds
8,500 tokens

Speedup: 5x faster
```

### Token Usage Comparison

```
Small Project (1 domain):
Before: ████████████████████████████████████████████████ 50,000 tokens
After:  ████████ 3,700 tokens
Savings: 92.6%

Medium Project (3 domains):
Before: ████████████████████████████████████████████████ 50,000 tokens
After:  ███████████████ 8,500 tokens
Savings: 83.0%

Large Project (5 domains):
Before: ████████████████████████████████████████████████ 50,000 tokens
After:  █████████████████████ 20,000 tokens
Savings: 60.0%
```

---

## Migration Path

### Step-by-Step Migration

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Prepare Shared KB                                   │
│                                                              │
│ ✓ Add domain metadata to entries                            │
│ ✓ Generate _domain_index.yaml                               │
│ ✓ Test domain commands (kb load-domain)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 2: Migrate Projects                                    │
│                                                              │
│ ✓ Update .kb-config.yaml                                    │
│ ✓ Run: kb setup --sparse                                    │
│ ✓ Load preferred domains                                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 3: Optimize                                           │
│                                                              │
│ ✓ Monitor token usage                                       │
│ ✓ Adjust preferred domains                                 │
│ ✓ Configure selective updates                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Troubleshooting Scenarios

### Scenario 1: Sparse Checkout Not Working

**Problem:** `git sparse-checkout` fails on Windows

**Solution:**
```bash
# Check Git version
git --version  # Should be >= 2.25

# Fallback to GitHub API
kb config set on_demand.mode github-api
kb load-domain testing
```

---

### Scenario 2: Index Out of Sync

**Problem:** `_domain_index.yaml` outdated

**Solution:**
```bash
# Force index update
kb index --force

# Or use pre-commit hook
cd shared-knowledge-base
git hooks install pre-commit
```

---

### Scenario 3: Domain Not Found

**Problem:** `kb load-domain xxx` fails

**Solution:**
```bash
# List available domains
kb list-domains

# Search for similar domains
kb search-domain "test"  # Returns: testing

# Use correct name
kb load-domain testing
```

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Status:** Visual Guide Complete
