# Progressive Domain-Based Knowledge Loading
## Резюме архитектурного предложения (на русском)

**Дата:** 2026-01-07
**Статус:** Архитектурное предложение готово к рассмотрению

---

## 🎯 Суть предложения

**Проблема:** Агенты загружают всю Knowledge Base (134 entries, ~50,000 tokens) или ничего. Нет механизма выборочной загрузки.

**Решение:** Progressive domain-based knowledge loading - загружай metadata всех domains (~200 tokens), потом догружай нужные domains по требованию.

**Ключевые ограничения:**
- ❌ **ЗАПРЕЩЕНО:** Background скрипты, daemon processes, cron jobs, polling
- ✅ **РАЗРЕШЕНО:** Git native mechanisms + GitHub API + GitHub Actions

---

## 📊 Ожидаемые результаты

### Token Savings (токены)

| Тип проекта | Было | Стало | Экономия |
|-------------|------|-------|----------|
| **Small (1 domain)** | 50,000 | 3,700 | **92.6%** |
| **Medium (3 domains)** | 50,000 | 8,500 | **83.0%** |
| **Large (5 domains)** | 50,000 | 20,000 | **60.0%** |

### Performance (производительность)

| Метрика | Было | Стало | Улучшение |
|---------|------|-------|-----------|
| **Загрузка (1 domain)** | 5-10s | 1-2s | **3-5x быстрее** |
| **Поиск в index** | 50,000 tokens | 200 tokens | **99.6% меньше** |
| **Обновление** | 30s | 3s | **10x быстрее** |

---

## 🏗️ Архитектура: 4 Компонента

### Компонент 1: Domain-Based Metadata Schema

**Что:** Добавить `domains` поле в YAML entries.

**Пример:**
```yaml
errors:
  - id: "TEST-001"
    title: "Async Test Without @pytest.mark.asyncio"
    severity: "high"
    scope: "python"

    # НОВОЕ: Domain классификация
    domains:
      primary: "testing"       # Основной domain
      secondary: ["asyncio"]   # Связанные domains

    tags: ["async", "pytest", "testing"]
```

**Domain Taxonomy (10 domains):**
- `testing` - Тестирование (pytest, unittest)
- `asyncio` - Async/await, task groups
- `fastapi` - FastAPI framework
- `websocket` - WebSocket patterns
- `docker` - Docker containers
- `postgresql` - Database operations
- `authentication` - Auth, CSRF, sessions
- `deployment` - DevOps, CI/CD
- `monitoring` - Logging, metrics
- `performance` - Optimization, profiling

**Migration:** Автоматическая из существующих `tags`
```bash
python tools/kb_domains.py migrate --from-tags
```

---

### Компонент 2: Index-Based Discovery System

**Что:** Lightweight `_domain_index.yaml` с metadata ВСЕХ domains без полного контента.

**Пример:**
```yaml
# _domain_index.yaml (~200 tokens)
version: "2.0"
total_entries: 134
total_tokens_estimate: 52000

domains:
  testing:
    entries: 15
    token_estimate: 3500
    files:
      - "python/errors/testing.yaml"
      - "universal/patterns/testing.yaml"

  asyncio:
    entries: 22
    token_estimate: 4800
    files:
      - "python/errors/asyncio.yaml"
      - "universal/patterns/async.yaml"
```

**Генерация:**
```bash
python tools/kb_domains.py index --update
```

**Token Cost:** ~200 tokens (vs 50,000 full KB)

---

### Компонент 3: Progressive Loading Strategy

**Что:** Загружай базовую KB (~500 tokens), потом domains on-demand.

**Решение 1: Git Sparse Checkout (РЕКОМЕНДУЕТСЯ)**

**Workflow:**
```bash
# Step 1: Initial sparse setup
git clone --sparse --filter=blob:none https://github.com/ozand/shared-knowledge-base.git
cd shared-knowledge-base
git sparse-checkout init --cone
git sparse-checkout set _domain_index.yaml .claude/

# Step 2: Agent analyzes index
# Load: _domain_index.yaml (~200 tokens)
# Agent decides: "I need testing + asyncio"

# Step 3: Checkout specific domains
git sparse-checkout add python/errors/testing.yaml
git sparse-checkout add python/errors/asyncio.yaml

# Total: 200 + 3500 + 4800 = 8500 tokens (vs 50,000)
```

**Преимущества:**
- ✅ Git native mechanism
- ✅ Работает с submodules
- ✅ Zero background processes
- ✅ Selective checkout по path patterns

**Решение 2: GitHub API (FALLBACK)**

**Когда использовать:** Если нет Git access, read-only access

**Workflow:**
```python
# Agent-side code
from tools.kb_github_api import GitHubDomainLoader

loader = GitHubDomainLoader()
testing_entries = loader.load_domain('testing')
# Returns: ~3500 tokens
```

**Решение 3: Hybrid (PRODUCTION-READY)**

**Конфигурация:**
```yaml
# .kb-config.yaml
knowledge_base:
  type: "sparse-checkout"
  repository: "https://github.com/ozand/shared-knowledge-base.git"

  initial_load:
    - "_domain_index.yaml"
    - ".claude/"

  preferred_domains:
    - "testing"
    - "asyncio"

  on_demand:
    mode: "sparse-checkout"   # or "github-api"
```

---

### Компонент 4: Selective Update Mechanism

**Что:** Обновляй только нужные domains, не всю KB.

**Решение 1: GitHub Actions Matrix Strategy**

**Workflow:**
```yaml
# .github/workflows/kb-domain-update.yml
on:
  workflow_dispatch:
    inputs:
      domain:
        options: [testing, asyncio, fastapi, docker, all]

jobs:
  update-domain:
    strategy:
      matrix:
        domain:
          - name: testing
            paths: 'python/errors/testing.yaml'
    steps:
      - uses: actions/checkout@v4
        with:
          sparse-checkout: ${{ matrix.domain.paths }}
```

**Использование:**
```bash
gh workflow run kb-domain-update.yml -f domain=testing
```

**Решение 2: Git Tags per Domain**

**Версионирование:**
```bash
git tag -a testing-v1.2.0 -m "Testing domain v1.2.0"
git push origin testing-v1.2.0

# Проект pinned на конкретную версию
git checkout testing-v1.2.0
```

---

## 📅 План внедрения: 8 недель

### Phase 1: Foundation (Weeks 1-4)

**Week 1: Domain Metadata & Migration**
- ✅ Создать `tools/kb_domains.py`
- ✅ Migrate существующие entries (auto из tags)
- ✅ Manual review

**Week 2: Domain Index & Discovery**
- ✅ Generate `_domain_index.yaml`
- ✅ Implement index-based discovery
- ✅ Test token estimates

**Week 3: Progressive Loading (Git Sparse Checkout)**
- ✅ Implement Git sparse checkout integration
- ✅ Add `kb load-domain` command
- ✅ Test with real projects

**Week 4: GitHub API Fallback**
- ✅ Implement GitHub API fallback
- ✅ Test offline scenarios
- ✅ Document fallback behavior

---

### Phase 2: Production Readiness (Weeks 5-8)

**Week 5: Selective Updates**
- ✅ GitHub Actions matrix workflow
- ✅ Git tags per domain
- ✅ `kb sync` command

**Week 6: Project Migration Tools**
- ✅ Setup scripts для projects
- ✅ Update `for-projects/` templates
- ✅ Migration guide

**Week 7: Testing & Quality Assurance**
- ✅ Comprehensive test suite
- ✅ Performance benchmarks
- ✅ Security audit

**Week 8: Documentation & Launch**
- ✅ Complete documentation
- ✅ Example projects
- ✅ v3.1.0 release

---

## 🎓 Примеры использования

### Example 1: New Project Setup

```bash
# В новом проекте
git submodule add --sparse https://github.com/ozand/shared-knowledge-base.git docs/kb
cd docs/kb
git sparse-checkout init --cone
git sparse-checkout set _domain_index.yaml .claude/

# Agent работает
kb load-domain testing asyncio
# Total: ~8,500 tokens (vs 50,000)
```

---

### Example 2: Agent Workflow

```python
# Agent-side decision making
def load_relevant_domains(task_description: str):
    """Анализируй задачу и загружай нужные domains."""

    # 1. Load index (lightweight)
    index = kb.load_domain_index()  # 200 tokens

    # 2. Analyze task
    if 'test' in task_description.lower():
        kb.load_domain('testing')  # 3,500 tokens

    if 'async' in task_description.lower():
        kb.load_domain('asyncio')  # 4,800 tokens

    # Total: 200 + 3500 + 4800 = 8500 tokens
```

---

### Example 3: Selective Updates

```bash
# Обнови только testing domain
kb sync --domain testing

# Обнови несколько domains
kb sync --domain testing asyncio

# Обнови все
kb sync --all
```

---

## ⚠️ Risk Assessment

### High Priority Risks

**Risk 1: Git Sparse Checkout Compatibility**
- **Impact:** High (пользователи со старыми версиями Git)
- **Probability:** Medium (~20% users)
- **Mitigation:**
  - Document minimum Git version (2.25+)
  - Provide GitHub API fallback
  - Add version check к setup script

**Risk 2: Migration Breaking Changes**
- **Impact:** Critical (существующие projects сломаются)
- **Probability:** Low (<5%)
- **Mitigation:**
  - 100% backward compatibility requirement
  - Extensive testing перед release
  - Rollback plan ready

### Medium Priority Risks

**Risk 3: GitHub API Rate Limits**
- **Impact:** Medium (нельзя загрузить domains)
- **Probability:** Low (<10%)
- **Mitigation:**
  - Implement caching
  - Prefer Git sparse checkout
  - Use authenticated requests

---

## 🚀 Next Steps

### Immediate Actions

**1. Review Proposal**
```bash
# Полное архитектурное предложение
cat tmp/progressive-domain-loading-proposal.md

# Технические детали
cat tmp/progressive-loading-implementation-guide.md

# Визуальные схемы
cat tmp/progressive-loading-visual-guide.md
```

**2. Decide on Timeline**
```yaml
Options:
  A: Aggressive - 4 weeks (Phase 1 only)
  B: Standard - 8 weeks (Phase 1 + 2)
  C: Conservative - 12 weeks (with buffer)
```

**3. Start Implementation**
```bash
# Week 1: Domain metadata
python tools/kb_domains.py migrate --from-tags
python tools/kb_domains.py index --update
```

---

## 📚 Документация

### Created Documents

1. **PROGRESSIVE-DOMAIN-LOADING-INDEX.md** - Этот файл (навигация)
2. **progressive-domain-loading-proposal.md** - Полная архитектура (~1000 строк)
3. **progressive-loading-implementation-guide.md** - Техническая реализация (~800 строк)
4. **progressive-loading-visual-guide.md** - Визуальные схемы (~900 строк)
5. **progressive-loading-adoption-plan.md** - План внедрения (~700 строк)

**Total:** ~4,100 строк документации

---

## ✅ Success Criteria

### Phase 1 (Weeks 1-4)
- ✅ Domain metadata добавлена ко всем entries
- ✅ `_domain_index.yaml` сгенерирован (<200 tokens)
- ✅ `kb load-domain` command работает
- ✅ GitHub API fallback functional

### Phase 2 (Weeks 5-8)
- ✅ Selective updates через GitHub Actions
- ✅ Migration tools протестированы
- ✅ Documentation complete
- ✅ v3.1.0 released

### Post-Launch (Weeks 9-12)
- ✅ Token reduction >70% (измерено)
- ✅ Load time <3s (измерено)
- ✅ Adoption rate >50% (измерено)
- ✅ No critical bugs (monitored)

---

## 🎉 Заключение

**Progressive Domain-Based Knowledge Loading** - это:

✅ **Low Risk** - Backward compatible, fallback mechanisms
✅ **High Value** - 70-90% token reduction, 3x faster loading
✅ **Quick Win** - 8-week timeline, zero cost
✅ **Scalable** - Foundation для future improvements

**Recommendation:** Proceed с implementation немедленно.

**Готов начать?** Начни с `progressive-domain-loading-proposal.md`.

---

## 📞 Questions & Feedback

**Для вопросов:**
- GitHub Issue: label `progressive-loading`
- GitHub Discussions
- Email: support@example.com

**Для feedback:**
- Создать GitHub issue с предложениями
- Комментарии к документации
- Code review при implementation

---

**Версия:** 1.0
**Последнее обновление:** 2026-01-07
**Статус:** Архитектурное предложение готово к рассмотрению
**Следующий шаг:** Team review & decision
