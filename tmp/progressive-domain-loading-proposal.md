# Progressive Domain-Based Knowledge Loading
## Архитектурное предложение для Shared Knowledge Base v3.0

**Дата:** 2026-01-07
**Статус:** Architecture Proposal
**Автор:** Claude Code Architecture Analysis
**Версия:** 1.0

---

## Executive Summary

**Проблема:** Агенты загружают всю Knowledge Base (134 entries, ~50,000 tokens) или ничего, нет механизма выборочной загрузки по доменам.

**Решение:** Hybrid approach - Git-based progressive loading + GitHub API для discovery.

**Ключевые ограничения:**
- ❌ ЗАПРЕЩЕНО: Background скрипты, daemon processes, cron jobs, polling
- ✅ РАЗРЕШЕНО: Git native mechanisms + GitHub API + GitHub Actions

**Ожидаемые результаты:**
- Startup: ~100-500 tokens (index + metadata)
- On-demand loading доменов: ~1000-3000 tokens per domain
- Selective updates через GitHub Actions matrix
- Zero background processes

---

## Текущая Ситуация Analysis

### Что уже работает:

**1. Индексация через `kb.py index`**
- SQLite FTS5 search
- `_index.yaml` с metadata всех entries
- Token estimation через `kb.py stats`

**2. Scope hierarchy**
```
universal/    → 72 entries (cross-language)
python/       → 5 entries (language-specific)
docker/       → 12 entries (container)
framework/    → 2 entries (FastAPI, etc.)
```

**3. YAML metadata structure**
```yaml
errors:
  - id: "TEST-001"
    title: "Async Test Without @pytest.mark.asyncio"
    severity: "high"
    tags: ["async", "pytest", "decorator"]
```

### Критические Gaps:

**1. Нет domain-based organization**
- Знания организованы по `scope` (python, docker, universal)
- ❌ Нет доменов (asyncio, fastapi, websocket, testing)
- ❌ Нельзя загрузить "только asyncio знания"

**2. Нет progressive loading**
- Агент видит "все или ничего"
- ❌ Нет механизма "загрузи базовую KB → потом догрузи domains"

**3. Нет index discovery**
- Агент не знает "что доступно" без загрузки контента
- ❌ `_index.yaml` содержит 40 entries, но outdated (январь 2026)

**4. Нет selective updates**
- Нельзя обновить "только домен FastAPI"
- ❌ Все или ничего при обновлении

---

## Architecture Proposal

### Component 1: Domain-Based Metadata Schema

**Требование:** Добавить `domain` поле в YAML entries без изменения существующей структуры.

#### Решение: Backward-compatible расширение

```yaml
# Existing structure (unchanged)
version: "1.0"
category: "testing"
last_updated: "2026-01-04"

errors:
  - id: "TEST-001"
    title: "Async Test Without @pytest.mark.asyncio"
    severity: "high"
    scope: "python"  # Existing field

    # NEW: Domain classification
    domains:
      primary: "testing"           # Primary domain
      secondary: ["asyncio"]       # Related domains

    # Enhanced tags (existing field, just better usage)
    tags: ["async", "pytest", "decorator", "asyncio", "testing"]

    # NEW: Token estimation (kb.py can calculate)
    metadata:
      estimated_tokens: 450
      complexity: "medium"
      dependencies: ["pytest-asyncio"]
```

#### Domain Taxonomy

**Primary Domains** (один на entry):
- `testing` - Test patterns, pytest, unittest
- `asyncio` - Async/await, task groups, timeouts
- `fastapi` - Framework-specific
- `websocket` - WebSocket patterns
- `docker` - Container orchestration
- `postgresql` - Database operations
- `authentication` - Auth, CSRF, sessions
- `deployment` - DevOps, CI/CD
- `monitoring` - Logging, metrics
- `performance` - Optimization, profiling

**Secondary Domains** (multiple, optional):
- Cross-cutting concerns
- Related technologies
- Dependencies

#### Migration Strategy

```bash
# Phase 1: Auto-generate domains from existing tags
python tools/kb_domains.py migrate --from-tags

# Phase 2: Manual review
python tools/kb_domains.py review --scope python

# Phase 3: Commit updated entries
git add python/errors/*.yaml
git commit -m "feat: Add domain metadata to Python entries"
```

---

### Component 2: Index-Based Discovery System

**Требование:** Агент видит metadata ВСЕХ domains без загрузки полного контента (~50-100 tokens).

#### Решение: Lightweight `_domain_index.yaml`

```yaml
# T:\Code\shared-knowledge-base\_domain_index.yaml
version: "2.0"
last_updated: "2026-01-07T21:00:00Z"
total_entries: 134
total_tokens_estimate: 52000

domains:
  # Testing domain
  testing:
    entries: 15
    token_estimate: 3500
    last_updated: "2026-01-07"
    tags: ["pytest", "unittest", "mocking"]
    scopes:
      universal: 7    # Universal testing patterns
      python: 5       # Python-specific
      javascript: 3   # JS testing
    files:
      - "python/errors/testing.yaml"      # 5 entries, 1200 tokens
      - "universal/patterns/testing.yaml" # 7 entries, 1800 tokens
      - "javascript/errors/testing.yaml"  # 3 entries, 500 tokens

  # AsyncIO domain
  asyncio:
    entries: 22
    token_estimate: 4800
    last_updated: "2026-01-06"
    tags: ["async", "await", "task-group", "timeout"]
    scopes:
      python: 18
      universal: 4
    files:
      - "python/errors/asyncio.yaml"          # 12 entries, 2600 tokens
      - "python/patterns/async-patterns.yaml" # 6 entries, 1200 tokens
      - "universal/patterns/async.yaml"       # 4 entries, 1000 tokens

  # FastAPI domain
  fastapi:
    entries: 18
    token_estimate: 3200
    last_updated: "2026-01-07"
    tags: ["dependency-injection", "websocket", "routes"]
    scopes:
      framework: 18
    files:
      - "framework/fastapi/errors/deps.yaml"     # 8 entries, 1400 tokens
      - "framework/fastapi/errors/websocket.yaml" # 6 entries, 1000 tokens
      - "framework/fastapi/patterns/routes.yaml"  # 4 entries, 800 tokens

  # Docker domain
  docker:
    entries: 12
    token_estimate: 2800
    last_updated: "2026-01-05"
    tags: ["containers", "volumes", "networks"]
    scopes:
      docker: 12
    files:
      - "docker/errors/common-errors.yaml"       # 6 entries, 1400 tokens
      - "docker/errors/docker-network.yaml"      # 3 entries, 700 tokens
      - "docker/errors/docker-security.yaml"     # 3 entries, 700 tokens

# Cross-reference matrix
related_domains:
  - [testing, asyncio]    # Async testing patterns
  - [fastapi, websocket]  # FastAPI Websocket
  - [docker, postgresql]  # Docker + PostgreSQL

# Usage statistics (optional, from kb_usage.py)
usage_stats:
  last_30_days:
    testing: 45 queries
    asyncio: 38 queries
    fastapi: 22 queries
```

**Token Cost:** ~150-200 tokens (легко кэшировать)

#### Генерация Index

```bash
# Auto-generate from existing entries
python tools/kb_domains.py index --update

# Validate index integrity
python tools/kb_domains.py validate

# Export to JSON (для GitHub API consumers)
python tools/kb_domains.py export --format json --output _domain_index.json
```

---

### Component 3: Progressive Loading Strategy

**Требование:** Агент загружает базовую KB (~500 tokens), потом domains on-demand.

#### Solution 1: Git Sparse Checkout (RECOMMENDED)

**Почему Git sparse checkout?**
- ✅ Git native mechanism
- ✅ Works with submodules
- ✅ Zero background processes
- ✅ Selective checkout по path patterns

**Workflow:**

```bash
# Step 1: Clone with sparse checkout (initial setup)
git clone --sparse --filter=blob:none https://github.com/ozand/shared-knowledge-base.git
cd shared-knowledge-base

# Step 2: Configure sparse checkout
git sparse-checkout init --cone
git sparse-checkout set _domain_index.yaml _index.yaml .claude/

# Step 3: Agent analyzes index
# Load: _domain_index.yaml (~200 tokens)
# Agent decides: "I need testing + asyncio domains"

# Step 4: Checkout specific domains on-demand
git sparse-checkout add python/errors/testing.yaml
git sparse-checkout add python/errors/asyncio.yaml
git sparse-checkout add universal/patterns/async.yaml

# Total loaded: 200 (index) + 1200 (testing) + 2600 (asyncio) = 4000 tokens

# Step 5: Remove unused domains (optional)
git sparse-checkout disable  # Reset to full checkout if needed
```

**Для проектов через git submodule:**

```bash
# В проекте
git submodule add --sparse https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base
cd docs/knowledge-base
git sparse-checkout init --cone
git sparse-checkout set _domain_index.yaml .claude/

# Agent triggers:
git -C docs/knowledge-base sparse-checkout add python/errors/testing.yaml
```

#### Solution 2: GitHub API (FALLBACK)

**Когда использовать:** Если нет Git access, read-only access.

**Workflow:**

```python
# Agent-side code (example)
import requests

def load_domain(domain_name: str):
    # 1. Load index
    index = requests.get("https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/_domain_index.yaml")
    domain_meta = yaml.safe_load(index.content)['domains'][domain_name]

    # 2. Load specific files
    entries = []
    for file_path in domain_meta['files']:
        content = requests.get(f"https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/{file_path}")
        entries.append(yaml.safe_load(content.content))

    return entries

# Agent usage
testing_kb = load_domain('testing')  # ~3500 tokens
```

**Token Cost:** 200 (index) + domain size

#### Solution 3: Hybrid (PRODUCTION-READY)

**Best of both worlds:**

```yaml
# .kb-config.yaml (project configuration)
knowledge_base:
  type: "sparse-checkout"  # or "github-api" or "full-clone"
  repository: "https://github.com/ozand/shared-knowledge-base.git"
  path: "docs/knowledge-base"

  # Progressive loading config
  initial_load:
    - "_domain_index.yaml"    # Always load
    - "_index.yaml"           # Always load
    - ".claude/"              # Always load

  on_demand:
    mode: "sparse-checkout"   # or "github-api"

  # Domain preferences (optional)
  preferred_domains:
    - "testing"
    - "asyncio"
    - "fastapi"
```

**Agent-triggered loading:**

```bash
# Agent analyzes task
# Task: "Fix async test issue"

# Agent command:
kb load-domain testing asyncio

# kb.py internally:
# 1. Read _domain_index.yaml
# 2. Find domain files
# 3. git sparse-checkout add <files>
# 4. Return loaded entries summary
```

---

### Component 4: Selective Update Mechanism

**Требование:** Агенты обновляют только нужные domains, не всю KB.

#### Solution: GitHub Actions Matrix Strategy

**Workflow:** `.github/workflows/kb-domain-update.yml`

```yaml
name: KB Domain Update

on:
  workflow_dispatch:
    inputs:
      domain:
        description: 'Domain to update'
        required: true
        type: choice
        options:
          - testing
          - asyncio
          - fastapi
          - docker
          - all
  schedule:
    # Daily updates at 2 AM UTC
    - cron: '0 2 * * *'

jobs:
  update-domain:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        # Map domain → file paths
        domain:
          - name: testing
            paths: 'python/errors/testing.yaml,universal/patterns/testing.yaml'
          - name: asyncio
            paths: 'python/errors/asyncio.yaml,universal/patterns/async.yaml'
          - name: fastapi
            paths: 'framework/fastapi/errors/*.yaml,framework/fastapi/patterns/*.yaml'

    steps:
      - name: Checkout specific files
        uses: actions/checkout@v4
        with:
          sparse-checkout: ${{ matrix.domain.paths }}
          sparse-checkout-cone-mode: false

      - name: Update domain index
        run: |
          python tools/kb_domains.py update --domain ${{ matrix.domain.name }}

      - name: Commit changes
        run: |
          git config user.name 'KB Bot'
          git config user.email 'kb-bot@example.com'
          git add _domain_index.yaml
          git commit -m "chore: Update ${{ matrix.domain.name }} domain index" || exit 0
          git push
```

**Использование:**

```bash
# Manual trigger через GitHub CLI
gh workflow run kb-domain-update.yml -f domain=testing

# Или агент триггерит (в проекте)
kb sync --domain testing
```

#### Solution 2: Git Tags per Domain

**Версионирование domains:**

```bash
# Когда domain обновляется
git tag -a testing-v1.2.0 -m "Testing domain: Add pytest-asyncio patterns"
git push origin testing-v1.2.0

# Проект pinned на конкретную версию
cd docs/knowledge-base
git fetch --tags
git checkout testing-v1.2.0
```

**Конфигурация в проекте:**

```yaml
# .kb-config.yaml
domains:
  testing:
    version: "v1.2.0"
    auto_update: true  # Check daily via GitHub API
  asyncio:
    version: "v2.1.0"
    auto_update: false  # Pinned
```

#### Solution 3: GitHub Releases (OPTIONAL)

**Domain-specific releases:**

```bash
# Создать release для domain
gh release create testing-v1.2.0 \
  --title "Testing Domain v1.2.0" \
  --notes "Added pytest-asyncio patterns" \
  python/errors/testing.yaml \
  universal/patterns/testing.yaml
```

**Проект загружает release:**

```python
# Agent-side
import requests

def get_domain_release(domain: str, version: str):
    url = f"https://api.github.com/repos/ozand/shared-knowledge-base/releases/tags/{domain}-{version}"
    release = requests.get(url).json()

    # Download assets
    for asset in release['assets']:
        content = requests.get(asset['browser_download_url'])
        # Save to local KB

    return release
```

---

## Implementation Plan

### Phase 1: Domain Metadata (1-2 days)

**Tasks:**
1. ✅ Добавить `domains` поле в YAML schema
2. ✅ Создать `tools/kb_domains.py` для migration
3. ✅ Auto-migrate существующие entries (based on tags)
4. ✅ Manual review и корректировка

**Deliverables:**
- `tools/kb_domains.py` - Domain management CLI
- `_domain_index.yaml` - Initial index
- Updated YAML entries с domain metadata

**Acceptance Criteria:**
- Все 134 entries имеют `domains` поле
- `_domain_index.yaml` содержит все 10+ domains
- `python tools/kb_domains.py validate` passes

---

### Phase 2: Index-Based Discovery (2-3 days)

**Tasks:**
1. ✅ Implement `_domain_index.yaml` generator
2. ✅ Add `kb.py index --domains` command
3. ✅ Calculate token estimates per domain
4. ✅ Create cross-reference matrix

**Deliverables:**
- `_domain_index.yaml` (< 200 tokens)
- `tools/kb_domains.py index` command
- Updated `kb.py` с domain-aware search

**Acceptance Criteria:**
- `_domain_index.yaml` < 200 tokens
- Agent может load index за 1 request
- Index auto-updates при изменении entries

---

### Phase 3: Progressive Loading (3-4 days)

**Tasks:**
1. ✅ Implement Git sparse checkout integration
2. ✅ Add `kb.py load-domain` command
3. ✅ Create GitHub API fallback
4. ✅ Update `.kb-config.yaml` с progressive config

**Deliverables:**
- `tools/kb_domains.py load` command
- `for-projects/kb-sparse-setup.sh` script
- Updated documentation

**Acceptance Criteria:**
- `kb load-domain testing` работает
- Token reduced с 50,000 → 5,000 для single-domain project
- Fallback на GitHub API если нет Git access

---

### Phase 4: Selective Updates (2-3 days)

**Tasks:**
1. ✅ Create GitHub Actions workflow для domain updates
2. ✅ Implement Git tags per domain
3. ✅ Add `kb.py sync --domain` command
4. ✅ Create release automation (optional)

**Deliverables:**
- `.github/workflows/kb-domain-update.yml`
- `tools/kb_domains.py sync` command
- Versioning documentation

**Acceptance Criteria:**
- `gh workflow run kb-domain-update.yml -f domain=testing` работает
- Git tags создаются автоматически
- Projects могут pin domain versions

---

### Phase 5: Testing & Documentation (2-3 days)

**Tasks:**
1. ✅ Create test entries для всех domains
2. ✅ Test progressive loading в реальном проекте
3. ✅ Document workflow в `GUIDE.md`
4. ✅ Update `for-claude-code/README.md`

**Deliverables:**
- Test suite
- Updated documentation
- Migration guide для существующих projects

**Acceptance Criteria:**
- Все integration tests pass
- Documentation complete
- Migration path documented

---

## Migration Guide для Projects

### Before (Current):

```bash
# Project setup
git submodule add https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base
cd docs/knowledge-base
git pull origin main  # Loads ALL entries: ~50,000 tokens
```

### After (Progressive):

```bash
# Step 1: Initial sparse setup
git submodule add --sparse https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base
cd docs/knowledge-base
git sparse-checkout init --cone
git sparse-checkout set _domain_index.yaml _index.yaml .claude/

# Step 2: Configure preferred domains
cat > .kb-config.yaml <<EOF
knowledge_base:
  type: "sparse-checkout"
  initial_load:
    - "_domain_index.yaml"
    - ".claude/"
  preferred_domains:
    - "testing"
    - "asyncio"
EOF

# Step 3: Agent loads domains on-demand
kb load-domain testing asyncio
# Total: ~200 (index) + 3500 (testing) + 4800 (asyncio) = ~8500 tokens

# Step 4: Selective updates
kb sync --domain testing  # Only update testing domain
```

---

## Expected Results

### Token Savings

| Scenario | Before | After | Savings |
|----------|--------|-------|---------|
| Small project (1 domain) | 50,000 | 5,000 | 90% |
| Medium project (3 domains) | 50,000 | 12,000 | 76% |
| Large project (5 domains) | 50,000 | 20,000 | 60% |

### Performance Improvements

- **Startup time:** 5s → 1s (sparse checkout)
- **Index search:** 50,000 tokens → 200 tokens (index only)
- **Update time:** 30s → 3s (single domain)

### Developer Experience

- Agent говорит: "Loading testing domain..." → User видит progress
- Agent использует 85% меньше tokens
- Faster context loading

---

## Technical Considerations

### 1. Backward Compatibility

**✅ Fully backward compatible**

```yaml
# Old entries (without domains) still work
errors:
  - id: "TEST-001"
    tags: ["async", "pytest"]  # kb_domains.py migrates automatically
```

Migration tool auto-generates `domains` from `tags`.

### 2. Git Sparse Checkout Limitations

**Known limitations:**
- Windows Git < 2.25: Not supported (rare now)
- Submodule sparse checkout: Requires Git 2.35+

**Mitigation:**
- Fallback на GitHub API
- Documentation minimum versions

### 3. GitHub API Rate Limits

**Rate limit:** 60 requests/hour (unauthenticated)

**Solution:**
- Cache `_domain_index.yaml` locally
- Use authenticated requests (5000 requests/hour)
- Prefer Git sparse checkout over API

### 4. Index Synchronization

**Problem:** `_domain_index.yaml` может устаревать

**Solutions:**
1. **GitHub Actions:** Auto-update index hourly
2. **Git pre-commit hook:** Update index on commits
3. **Agent-side:** Check index age before loading

**Recommended:** Pre-commit hook

```bash
# .git/hooks/pre-commit
python tools/kb_domains.py index --update
git add _domain_index.yaml
```

---

## Alternatives Considered

### Alternative 1: Git Submodules per Domain

**Idea:** Отдельный submodule для каждого domain.

**Pros:**
- Максимальная granularность
- Независимое versioning

**Cons:**
- ❌ Too many submodules (10+)
- ❌ Complex management
- ❌ Slow `git submodule update`

**Decision:** ❌ Rejected (over-engineering)

### Alternative 2: Git LFS for Index

**Idea:** Store index в Git LFS для fast loading.

**Pros:**
- Fast downloads
- Separation from repo

**Cons:**
- ❌ Requires LFS setup
- ❌ Not all Git hosts support LFS
- ❌ Overkill для <200 tokens

**Decision:** ❌ Rejected (unnecessary complexity)

### Alternative 3: External Index Service

**Idea:** Separate index server/API.

**Pros:**
- Centralized updates
- Real-time stats

**Cons:**
- ❌ **External dependency** (violates constraints)
- ❌ Requires background process
- ❌ Single point of failure

**Decision:** ❌ Rejected (violates "no background scripts" constraint)

---

## Success Metrics

### Quantitative

- **Token reduction:** >70% для single-domain projects
- **Index size:** <200 tokens
- **Load time:** <2s для single domain
- **Update time:** <5s для single domain

### Qualitative

- **Developer feedback:** "Easier to find relevant knowledge"
- **Agent performance:** "Faster context loading"
- **Maintainability:** "Simple Git-based workflow"

---

## Open Questions

### Q1: Should domains be hierarchical?

**Example:** `python.asyncio` vs `asyncio`

**Recommendation:** Flat domains (не hierarchical)
- Simpler implementation
- Easier search
- Cross-domain references already supported

### Q2: How to handle overlapping domains?

**Example:** Entry belongs to both `testing` AND `asyncio`

**Recommendation:**
```yaml
domains:
  primary: "testing"
  secondary: ["asyncio"]
```

- Appears in both domain indexes
- Token counted towards primary
- Cross-referenced in related matrix

### Q3: Should we use Git submodules or direct clone?

**Recommendation:** Hybrid
- Default: Git submodule (для проектов)
- Option: Direct clone (для standalone usage)
- Fallback: GitHub API (read-only)

---

## Next Steps

### Immediate Actions

1. **Review proposal** с командой
2. **Create tracking issue** в GitHub
3. **Assign Phases 1-2** для initial implementation
4. **Set up milestone** для v3.1 release

### Timeline Estimate

- **Phase 1-2:** 1 week (domain metadata + index)
- **Phase 3-4:** 1 week (progressive loading + updates)
- **Phase 5:** 3 days (testing + docs)

**Total:** ~2-3 weeks для MVP

---

## Conclusion

**Progressive Domain-Based Knowledge Loading** позволит:

1. ✅ **Reduce token usage** на 70-90% для single-domain projects
2. ✅ **Improve performance** (1-2s load vs 5-10s)
3. ✅ **Enable selective updates** (update only what changed)
4. ✅ **Maintain simplicity** (Git-based, no background processes)
5. ✅ **Stay backward compatible** (existing entries work)

**Ключевое решение:** Git sparse checkout + GitHub API fallback = zero infrastructure, maximum compatibility.

---

**Appendix A: Example Commands**

```bash
# Domain management
python tools/kb_domains.py migrate --from-tags
python tools/kb_domains.py index --update
python tools/kb_domains.py validate

# Progressive loading
kb load-domain testing asyncio
kb unload-domain docker
kb list-domains

# Selective updates
kb sync --domain testing
kb sync --all
kb status
```

**Appendix B: File Structure**

```
shared-knowledge-base/
├── _domain_index.yaml          # NEW: Domain metadata index
├── _index.yaml                  # Existing: Entry catalog
├── tools/
│   ├── kb.py                    # Existing: Main CLI
│   ├── kb_domains.py            # NEW: Domain management
│   └── kb_progressive.py        # NEW: Progressive loading
├── .github/workflows/
│   └── kb-domain-update.yml     # NEW: Selective updates
└── for-projects/
    └── kb-sparse-setup.sh       # NEW: Setup script
```

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Status:** Ready for Review
**Next Review:** After team feedback
