# Domain-Based Knowledge Base: Quick Start

**Version:** 3.1
**Last Updated:** 2026-01-07

---

## Overview

Shared Knowledge Base v3.1 introduces **progressive domain-based loading**, allowing you to load only the knowledge domains you need, reducing token usage by **70-90%**.

---

## Quick Start

### 1. List Available Domains

```bash
# See all domains with metadata
python tools/kb_domains.py --kb-dir .kb/shared list
```

**Output:**
```
📚 Knowledge Base Domains
   Total entries: 149
   With domains: 65 (43.6%)
   Total tokens: ~9750

  docker                11 entries, ~1650 tokens
  testing               11 entries, ~1650 tokens
  postgresql             8 entries, ~1200 tokens
  asyncio                6 entries, ~900 tokens
  ...
```

---

### 2. Load Specific Domain

```bash
# Load testing domain using Git sparse checkout
python tools/kb_domains.py load testing
```

**What happens:**
1. Checks `_domain_index.yaml` for domain files
2. Runs `git sparse-checkout add` for domain files
3. Loads only testing domain (~1,650 tokens vs 9,750 total)

**Output:**
```
📦 Loading domain: testing
  Files: 3
  Entries: 11
  Tokens: ~1650
  ✓ python/errors/testing.yaml
  ✓ universal/patterns/testing.yaml
  ✓ javascript/errors/testing.yaml

✅ Loaded domain 'testing' (~1650 tokens, 3 files)
```

---

### 3. Migrate Entries with Domain Metadata

```bash
# Add domain metadata to entries (from existing tags)
python tools/kb_domains.py migrate --from-tags

# Preview changes first
python tools/kb_domains.py migrate --from-tags --dry-run
```

---

### 4. Generate/Update Domain Index

```bash
# Generate _domain_index.yaml from all entries
python tools/kb_domains.py index --update
```

---

### 5. Validate Domain Metadata

```bash
# Check domain metadata consistency
python tools/kb_domains.py validate
```

---

## GitHub API Fallback

If Git sparse checkout is not available, use GitHub API:

```python
# Load domain via GitHub API
python tools/kb_github_api.py load testing

# Save domain locally for offline use
python tools/kb_github_api.py save testing --output ./cache

# Check API rate limit
python tools/kb_github_api.py rate-limit
```

---

## Domain Taxonomy

Available domains (12 total):

| Domain | Description | Entries | Tokens |
|--------|-------------|---------|--------|
| **testing** | Test patterns, pytest, unittest | 11 | ~1,650 |
| **docker** | Containers, volumes, networks | 11 | ~1,650 |
| **postgresql** | Database operations | 8 | ~1,200 |
| **asyncio** | Async/await, task groups | 6 | ~900 |
| **authentication** | Auth, JWT, sessions | 6 | ~900 |
| **deployment** | DevOps, CI/CD | 6 | ~900 |
| **api** | REST API patterns | 4 | ~600 |
| **fastapi** | FastAPI framework | 3 | ~450 |
| **monitoring** | Logging, metrics | 3 | ~450 |
| **security** | Security patterns | 3 | ~450 |
| **performance** | Optimization | 2 | ~300 |
| **websocket** | WebSocket patterns | 2 | ~300 |

---

## Token Savings

### Before (Monolithic Loading)
```
Full KB: 9,750 tokens
├─ All domains loaded
└─ 5-10 seconds load time
```

### After (Progressive Loading)
```
Small Project (1 domain):
  Domain Index: 200 tokens
  + Testing Domain: 1,650 tokens
  = Total: 1,850 tokens (81% reduction!)

Medium Project (3 domains):
  Domain Index: 200 tokens
  + Testing + AsyncIO + Docker: 4,200 tokens
  = Total: 4,400 tokens (55% reduction!)

Large Project (5 domains):
  Domain Index: 200 tokens
  + 5 major domains: 6,600 tokens
  = Total: 6,800 tokens (30% reduction!)
```

---

## Usage Examples

### Example 1: New Project Setup

```bash
# 1. Initialize domain index
python tools/kb_domains.py index --update

# 2. List available domains
python tools/kb_domains.py --kb-dir .kb/shared list

# 3. Load relevant domains
python tools/kb_domains.py load testing
python tools/kb_domains.py load asyncio

# 4. Verify loaded domains
ls -la python/errors/testing.yaml
ls -la python/errors/asyncio.yaml
```

---

### Example 2: Agent Workflow

```python
# Agent-side decision making
from tools.kb_domains import DomainManager

def agent_task_handler(task: str):
    """Handle agent task with progressive loading."""

    # 1. Analyze task
    keywords = extract_keywords(task)
    # ['async', 'test', 'fastapi']

    # 2. Load index (lightweight)
    manager = DomainManager(kb_dir)
    # Load _domain_index.yaml (~200 tokens)

    # 3. Match domains
    domains_needed = match_domains(keywords)
    # ['testing', 'asyncio']

    # 4. Load domains progressively
    for domain in domains_needed:
        manager.load_domain(domain)
    # Total: ~2,550 tokens (vs 9,750)

    # 5. Work with knowledge
    relevant_kb = search_domains(domains_needed, task)

    return relevant_kb
```

---

### Example 3: GitHub API Fallback

```python
# When Git sparse checkout is not available
from tools.kb_github_api import GitHubDomainLoader

loader = GitHubDomainLoader(token=os.getenv('GITHUB_TOKEN'))

# Load domain index
index = loader.load_domain_index()

# Load specific domain
testing_entries = loader.load_domain('testing')
print(f"Loaded {len(testing_entries)} entries")

# Save locally for offline use
loader.save_domain_locally('testing', Path('./cache'))
```

---

## Advanced Usage

### Selective Updates (Future)

```bash
# Update only specific domain
python tools/kb_domains.py sync --domain testing

# Update multiple domains
python tools/kb_domains.py sync testing asyncio

# Update all
python tools/kb_domains.py sync --all
```

### Domain Versioning (Future)

```bash
# Pin domain to specific version
python tools/kb_domains.py pin testing v1.2.0

# Check available versions
python tools/kb_domains.py --kb-dir .kb/shared list-versions testing

# Use latest version
python tools/kb_domains.py unpin testing
```

---

## Troubleshooting

### Issue: Domain not found

```
❌ Domain not found: xxx
```

**Solution:**
```bash
# List available domains
python tools/kb_domains.py --kb-dir .kb/shared list

# Use correct domain name
python tools/kb_domains.py load testing  # not 'test'
```

---

### Issue: Git sparse checkout fails

**Error:** `fatal: this operation must be run in a git repository`

**Solution:**
```bash
# Use GitHub API fallback instead
python tools/kb_github_api.py load testing
```

---

### Issue: Index out of sync

**Error:** `⚠ 84 entries without domain metadata`

**Solution:**
```bash
# Re-run migration
python tools/kb_domains.py migrate --from-tags

# Re-generate index
python tools/kb_domains.py index --update

# Validate
python tools/kb_domains.py validate
```

---

## Integration with Existing Workflow

### Current Commands (Still Work)

```bash
# Search still works as before
python tools/kb.py search "websocket"

# Validate still works
python tools/kb.py validate path/to/file.yaml

# Stats still works
python tools/kb.py stats
```

### New Domain Commands

```bash
# Domain management (NEW)
python tools/kb_domains.py --kb-dir .kb/shared list
python tools/kb_domains.py load testing
python tools/kb_domains.py migrate --from-tags
python tools/kb_domains.py index --update
python tools/kb_domains.py validate
```

---

## Next Steps

1. **Phase 1 Complete:** Domain metadata + index + loading ✅
2. **Phase 2 (Next):** GitHub-native contribution system
3. **Phase 3 (Future):** Automated feedback loop

---

## Related Documentation

- **`tmp/progressive-domain-loading-proposal.md`** - Architecture proposal
- **`tmp/progressive-loading-implementation-guide.md`** - Technical implementation
- **`tmp/progressive-loading-visual-guide.md`** - Visual diagrams
- **`tmp/integrated-improvement-roadmap.md`** - Complete 12-week roadmap

---

**Version:** 3.1
**Status:** Phase 1 Complete
**Next:** Phase 2 - GitHub-Native Contribution System
