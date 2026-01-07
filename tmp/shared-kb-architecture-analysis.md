# Shared KB Architecture Analysis: Shared vs Project-Specific Knowledge

**Date:** 2026-01-07
**Purpose:** Understanding how Shared KB separates and manages shared vs project-specific knowledge
**Language:** Russian (as requested by user)

---

## Executive Summary

Shared Knowledge Base (Shared KB) - это централизованный репозиторий знаний, который интегрируется в проекты через Git submodule. Система использует **иерархическую организацию по scope (области видимости)** для разделения знаний на общие (shared) и проектные (project-specific).

**Ключевая концепция:** Knowledge entries (записи знаний) хранятся в YAML файлах с полем `scope`, которое определяет, является ли знание общим (для всех проектов) или специфичным для конкретного проекта.

---

## 1. Иерархическая организация знаний

### Scope Levels (Уровни области видимости)

Shared KB использует 5-уровневую иерархию от самых общих к самым специфичным:

```
1. universal/     # Кросс-языковые паттерны (Git, тестирование, архитектура)
2. python/        # Специфично для Python (async, type hints, imports)
3. framework/     # Специфично для фреймворков (FastAPI, Django, React)
4. domain/        # Специфично для бизнес-домена (e-commerce, healthcare)
5. project/       # Специфично для конкретного проекта (local only)
```

### Примеры scope в YAML файлах

**Universal scope** (общее для всех):
```yaml
# File: universal/errors/redis-errors.yaml
title: Redis Configuration and Command Errors
scope: universal
severity: medium
category: redis-errors
```

**Python scope** (общее для Python-проектов):
```yaml
# File: python/errors/csrf-auth.yaml
id: "AUTH-001"
title: "Unnecessary CSRF Token Auto-Refresh Causing Failures"
scope: "python"
```

**Project scope** (локальное для проекта):
```yaml
# File: docs/knowledge-base/project/errors/app-specific.yaml
id: "APP-001"
title: "App-Specific Authentication Error"
scope: "project"
local_only: true  # Не синхронизируется в shared repository
```

---

## 2. Структура директорий Shared KB

### В центральном репозитории (T:\Code\shared-knowledge-base)

```
shared-knowledge-base/
├── universal/              # Кросс-языковые знания
│   ├── errors/            # Универсальные ошибки
│   ├── patterns/          # Универсальные паттерны
│   └── agent-instructions/  # AI agent configuration
├── python/                # Python-специфичные знания
│   ├── errors/
│   └── patterns/
├── javascript/            # JavaScript-специфичные знания
│   ├── errors/
│   └── patterns/
├── docker/                # Docker-специфичные знания
│   └── errors/
├── postgresql/            # PostgreSQL-специфичные знания
│   ├── errors/
│   ├── patterns/
│   └── tools/
├── framework/             # Фреймворк-специфичные знания
│   ├── django/
│   ├── fastapi/
│   ├── react/
│   └── vue/
├── for-claude-code/       # Документация для Claude Code
├── for-projects/          # Шаблоны интеграции для проектов
└── tools/                 # kb.py - CLI tool для управления KB
```

### В проекте клиента (после интеграции)

```
your-project/
├── docs/
│   └── knowledge-base/
│       ├── shared/        # Git submodule → shared-knowledge-base
│       │   ├── universal/
│       │   ├── python/
│       │   ├── tools/
│       │   └── for-projects/
│       └── project/       # Локальные знания проекта (local only)
│           ├── errors/
│           └── patterns/
└── .kb-config.yaml        # Конфигурация KB для этого проекта
```

---

## 3. Механизм разделения: Scope Field

### Как определяется scope

Каждая knowledge entry (запись знания) - это YAML файл с обязательным полем `scope`:

```yaml
version: "1.0"
category: "authentication-and-csrf"
last_updated: "2026-01-05"

errors:
  - id: "AUTH-001"
    title: "Unnecessary CSRF Token Auto-Refresh"
    severity: "high"
    scope: "python"  # ← Определяет тип знаний

    problem: |
      Описание проблемы...

    solution:
      code: |
        # Решение
```

### Scope decision criteria (Критерии принятия решения)

**Добавить в SHARED KB**, если:
- Scope: `docker`, `universal`, `python`, `postgresql`, `javascript`
- Решение применимо к множественным проектам/окружениям
- Ошибка распространена в индустрии
- Framework-agnostic или стандартный use case

**Хранить в LOCAL KB**, если:
- Scope: `project`, `domain`, `framework`
- Решение зависит от специфичной инфраструктуры
- Environment-specific или одноразовое событие
- Business logic specific

---

## 4. Конфигурация: .kb-config.yaml

### Конфигурация в Shared KB (шаблон)

```yaml
# File: shared-knowledge-base/.kb-config.yaml
version: "2.0"

# Пути (относительные к project root или абсолютные)
paths:
  kb_dir: "docs/knowledge-base"
  shared_dir: "docs/knowledge-base/shared"
  cache_dir: "docs/knowledge-base/.cache"
  index_db: "docs/knowledge-base/.cache/kb_index.db"

# Shared repositories для синхронизации
shared_sources:
  - name: "Universal Shared KB"
    url: "https://github.com/ozand/shared-knowledge-base.git"
    scopes: ["universal", "python"]
    enabled: true

# Scopes для импорта из shared repositories
import_scopes:
  - universal      # Кросс-языковые паттерны
  - python         # Python-specific
  # - javascript   # Раскомментировать если нужно
  # - docker       # Раскомментировать если нужно

# Scope levels (допустимые значения)
scope_levels:
  - universal
  - python
  - javascript
  - docker
  - postgresql
  - framework
  - domain
  - project
```

### Конфигурация в проекте клиента

```yaml
# File: your-project/.kb-config.yaml
# KB paths
shared_kb: "docs/knowledge-base/shared"
local_kb: "docs/knowledge-base"

# Search settings
search:
  ignore_case: true
  max_results: 50

# Validation settings
validation:
  min_quality_score: 75
  strict_mode: false

# Sync settings
sync:
  auto_push: false  # Не отправлять project scope в shared
  create_issues: true
```

---

## 5. Механизм доступа: Git Submodule Integration

### Установка Shared KB в проект

**Step 1: Добавление submodule**
```bash
cd your-project/
git submodule add https://github.com/ozand/shared-knowledge-base \
  docs/knowledge-base/shared
git submodule update --init --recursive
```

**Step 2: Установка интеграции**
```bash
# Полная установка (рекомендуется)
python docs/knowledge-base/shared/for-projects/scripts/install.py --full

# Или минимальная установка
python docs/knowledge-base/shared/for-projects/scripts/install.py --minimal
```

**Step 3: Конфигурация путей**
```yaml
# .kb-config.yaml
shared_kb: "docs/knowledge-base/shared"   # Submodule
local_kb: "docs/knowledge-base"           # Local knowledge
```

### Что получает проект

После установки проект имеет:

```
your-project/
├── .claude/                    # Claude Code configuration
│   ├── agents/                 # AI agents
│   │   ├── kb-agent.md        # KB management agent
│   │   └── subagents/
│   ├── skills/                 # Reusable skills
│   │   ├── kb-search/         # Search KB
│   │   ├── kb-validate/       # Validate entries
│   │   ├── kb-create/         # Create entries
│   │   └── audit-quality/     # Quality audit
│   ├── commands/               # Quick commands
│   │   ├── kb-search.md
│   │   ├── kb-validate.md
│   │   ├── retrospective.md
│   │   └── kb-sync.md
│   ├── settings.json          # Configuration
│   └── CLAUDE.md              # Project memory
├── docs/
│   └── knowledge-base/
│       ├── shared/            # Submodule → universal knowledge
│       │   ├── universal/     # Universal errors/patterns
│       │   ├── python/        # Python errors/patterns
│       │   ├── tools/         # kb.py CLI tool
│       │   └── for-projects/  # Integration templates
│       └── project/           # Local knowledge (NOT synced)
│           ├── errors/
│           └── patterns/
└── .kb-config.yaml            # KB configuration
```

---

## 6. Процесс синхронизации

### Workflow для universal scope (shared knowledge)

Когда Claude Code добавляет запись с scope: `universal`, `python`, `docker`, `postgresql`, `javascript`:

**1. Create file in SHARED KB:**
```bash
# ✅ CORRECT
T:\Code\shared-knowledge-base\universal\errors\file.yaml

# ❌ WRONG
\path\to\project\docs\knowledge-base\universal\errors\file.yaml
```

**2. Initialize metadata:**
```bash
python tools/kb.py init-metadata --verbose
# Creates file_meta.yaml with quality score, validation status, etc.
```

**3. Validate YAML:**
```bash
python tools/kb.py validate universal/errors/file.yaml
```

**4. Assess quality:**
```bash
python -m tools/kb_predictive estimate-quality --entry-id ERROR-ID
# Quality score must be ≥ 75/100
```

**5. IMMEDIATELY commit and push:**
```bash
cd T:\Code\shared-knowledge-base
git add file.yaml file_meta.yaml
git commit -m "Add ERROR-ID: Title"
git push origin main
```

**6. Rebuild index:**
```bash
python tools/kb.py index --force -v
```

**7. Confirm to user:**
```
✅ KB entry added to shared-knowledge-base repository
📝 Metadata initialized
⭐ Quality score: 85/100
📦 Committed: abc123
🚀 Pushed to: origin/main
🔍 Index rebuilt
🌐 Available at: https://github.com/ozand/shared-knowledge-base
```

### Workflow для project scope (local knowledge)

Когда Claude Code добавляет запись с scope: `project`:

**1. Create file in LOCAL KB:**
```bash
# ✅ CORRECT
\path\to\project\docs\knowledge-base\project\errors\file.yaml

# ❌ WRONG
T:\Code\shared-knowledge-base\project\errors\file.yaml
```

**2. Add metadata:**
```yaml
local_only: true  # Prevents sync to shared repository
```

**3. Validate YAML:**
```bash
python docs/knowledge-base/shared/tools/kb.py validate \
  docs/knowledge-base/project/errors/file.yaml
```

**4. Rebuild index:**
```bash
python docs/knowledge-base/shared/tools/kb.py index
```

**5. Confirm to user:**
```
✅ KB entry added to local KB (project-specific)
📝 Scope: project (local only)
🔍 Index rebuilt
```

---

## 7. Доступ к знаниям в проекте

### Поиск через CLI tool

```bash
# Поиск по ключевым словам
python docs/knowledge-base/shared/tools/kb.py search "docker volume"

# Поиск с фильтрами
python docs/knowledge-base/shared/tools/kb.py search \
  --scope python --severity high

# Поиск по тегам
python docs/knowledge-base/shared/tools/kb.py search \
  --tags async websocket
```

### Поиск через Claude Code Skills

```
# Использование skill kb-search
User: /kb-search "websocket timeout"

Claude Code:
🔍 KB SEARCH: "websocket timeout"

Found: 3 results

1. PYTHON-045: WebSocket timeout after 5 seconds (Score: 95%)
   File: shared/python/errors/websocket-timeout.yaml
   Severity: high

2. WEBSOCKET-002: Connection drops unexpectedly (Score: 82%)
   File: shared/python/errors/connection-drops.yaml
   Severity: medium

3. PROJECT-001: App-specific timeout issue (Score: 78%)
   File: project/errors/app-timeout.yaml
   Severity: low
   [LOCAL ONLY]
```

### Progressive Disclosure Pattern (Эффективная загрузка)

Shared KB использует Progressive Disclosure для оптимизации токенов:

**При старте сессии (~50 tokens):**
```yaml
# Только метаданные из *_meta.yaml файлов
- created_at: 2026-01-07
- quality_score: 85/100
- scope: universal
- tags: [docker, volumes]
```

**По требованию (полный контент):**
```bash
# Загружается полный YAML файл при необходимости
python tools/kb.py search --id DOCKER-003
```

**Результат:** 70%+ экономия токенов при старте сессии

---

## 8. Принципы разделения (Separation of Concerns)

### Что предоставляет Shared KB

- ✅ Knowledge entries (YAML файлы)
- ✅ Management tools (kb.py CLI)
- ✅ Integration templates (for-projects/)
- ✅ Documentation (for-claude-code/)

### Что предоставляет проект

- ✅ Application code
- ✅ KB integration (установлено из шаблонов)
- ✅ Local knowledge (project-specific)
- ✅ Project configuration (.kb-config.yaml)

### Преимущества архитектуры

1. **Clear separation:** Знания отдельно от кода приложения
2. **Project flexibility:** Кастомизация интеграции под каждый проект
3. **Easier updates:** Обновление через `git pull` в submodule
4. **Cleaner git history:** Изменения в KB отдельно от изменений в проекте
5. **Token efficiency:** Progressive Disclosure снижает расход токенов
6. **Quality control:** Метаданные и валидация обеспечивают качество

---

## 9. Decision Tree: Where to Create Entry

```
User reports error
    ↓
Search KB: python tools/kb.py search "error"
    ↓
Found? ──Yes──→ Return solution ✅
    ↓
   No
    ↓
Solve problem + Document in YAML
    ↓
Determine scope:
    ├─ Error is docker/universal/python/postgresql/javascript?
    │   ↓
    │   Create in: shared-knowledge-base/<scope>/errors/
    │   ↓
    │   Initialize metadata: python tools/kb.py init-metadata
    │   ↓
    │   Validate YAML: python tools/kb.py validate
    │   ↓
    │   Assess quality: python -m tools.kb_predictive estimate-quality
    │   ↓ (quality < 75)
    │   Enhance content
    │   ↓ (quality ≥ 75)
    │   IMMEDIATELY: git add, git commit, git push
    │   ↓ (if conflict)
    │   git pull --rebase origin main
    │   git push origin main
    │   ↓
    │   Rebuild index: python tools/kb.py index --force -v
    │   ↓
    │   Confirm: "✅ Synced to shared-knowledge-base"
    │   └→ Done ✅
    │
    └─ Error is project/domain/framework specific?
        ↓
        Create in: docs/knowledge-base/project/errors/
        ↓
        Add metadata: local_only: true
        ↓
        Validate YAML: python tools/kb.py validate
        ↓
        Rebuild index: python tools/kb.py index
        ↓
        Confirm: "✅ Added to local KB (project-specific)"
        └→ Done ✅
```

---

## 10. Примеры использования

### Example 1: Docker error (universal scope)

**Scenario:** Docker container keeps restarting with "redis: not found"

**Workflow:**
1. Search KB: `python tools/kb.py search "redis not found"`
2. Found: `REDIS-001: Redis Command Not Found in Container Logs`
3. Solution: Change `redis server` to `redis-server` in docker-compose.yml
4. Result: ✅ Fixed in 2 minutes

**Location:** `shared-knowledge-base/universal/errors/redis-errors.yaml`
**Scope:** `universal`
**Available to:** All projects

### Example 2: Python error (python scope)

**Scenario:** CSRF token auto-refresh causing failures

**Workflow:**
1. Search KB: `python tools/kb.py search "csrf token refresh"`
2. Found: `AUTH-001: Unnecessary CSRF Token Auto-Refresh Causing Failures`
3. Solution: Make auto-refresh conditional, not unconditional
4. Result: ✅ Fixed in 5 minutes

**Location:** `shared-knowledge-base/python/errors/csrf-auth.yaml`
**Scope:** `python`
**Available to:** All Python projects

### Example 3: Project-specific error (project scope)

**Scenario:** App-specific authentication timeout in fastapi-web-app

**Workflow:**
1. Search KB: `python tools/kb.py search "auth timeout"`
2. Not found in shared KB
3. Solve problem: Adjust JWT token expiration from 5min to 15min
4. Create entry: `docs/knowledge-base/project/errors/auth-timeout.yaml`
5. Add `local_only: true`
6. Result: ✅ Documented for future reference

**Location:** `fastapi-web-app/docs/knowledge-base/project/errors/auth-timeout.yaml`
**Scope:** `project`
**Available to:** Only this project

---

## 11. Техническая реализация

### KB Search Index (SQLite FTS5)

```bash
# Index database location
docs/knowledge-base/shared/.cache/kb_index.db

# Build index
python tools/kb.py index -v

# Index features:
- Full-text search with FTS5
- Sub-second search for 1M+ entries
- Cross-platform (Windows/Mac/Linux)
- Automatic indexing on changes
```

### Metadata System

```bash
# Metadata files (*_meta.yaml)
- created_at: 2026-01-07
- last_analyzed_at: 2026-01-07
- quality_score: 85/100 (5 dimensions × 20 points)
- validation_status: validated/pending/needs_review
- tested_versions: fastapi@0.104.0, python@3.11
- next_version_check_due: 2026-02-07
- local_only: false (if project-specific)
```

### Quality Assessment (100-point rubric)

```yaml
# Dimensions (20 points each)
1. Completeness (20 points)
   - Problem description: 5 points
   - Root cause analysis: 5 points
   - Multiple solutions: 5 points
   - Prevention tips: 5 points

2. Technical Accuracy (20 points)
   - Code examples work: 10 points
   - Information current: 5 points
   - No factual errors: 5 points

3. Clarity (20 points)
   - Clear title: 5 points
   - Structured content: 5 points
   - Examples explained: 5 points
   - Language simple: 5 points

4. Discoverability (20 points)
   - Descriptive ID: 5 points
   - Relevant tags: 5 points
   - Good summary: 5 points
   - Links to related entries: 5 points

5. Actionability (20 points)
   - Step-by-step solution: 10 points
   - Copy-pasteable code: 5 points
   - Test verification: 5 points

# Quality thresholds
- 90-100: Excellent ⭐⭐⭐ (ready for shared KB)
- 75-89: Good ⭐⭐ (acceptable for shared KB)
- 60-74: Acceptable ⭐ (needs improvement)
- <60: Needs Improvement (not ready for shared KB)

# Quality gate: Minimum 75 required before committing to shared repository
```

---

## 12. Summary

### Ключевые механизмы разделения

1. **Scope field в YAML:** Определяет тип знаний (universal/python/project)
2. **Git Submodule:** Раздельные репозитории (shared vs local)
3. **Directory structure:** universal/ + python/ (shared) vs project/ (local)
4. **Configuration:** .kb-config.yaml определяет пути к shared и local KB
5. **Sync workflow:** Universal scope → push to shared, project scope → local only
6. **Access patterns:** CLI tool + Claude Code skills + Progressive Disclosure

### Как проект получает доступ

1. **Git submodule:** `git submodule add shared-knowledge-base docs/knowledge-base/shared`
2. **Installation script:** `python for-projects/scripts/install.py --full`
3. **Configuration:** .kb-config.yaml + .claude/settings.json
4. **Index building:** `python tools/kb.py index`
5. **Search access:** CLI tool + Claude Code skills

### Преимущества

- ✅ **Token efficiency:** 70%+ экономия через Progressive Disclosure
- ✅ **Quality control:** Метаданные + валидация + оценка качества (75+ баллов)
- ✅ **Easy updates:** `git pull` в submodule для обновления
- ✅ **Clear separation:** Shared knowledge отдельно от project-specific
- ✅ **Flexible integration:** Кастомизация под каждый проект
- ✅ **Cross-project sharing:** Universal знания доступны всем проектам

---

**Version:** 1.0
**Date:** 2026-01-07
**Author:** Claude Code (Sonnet 4.5)
**Language:** Russian (as requested)

---

## Дополнительные ресурсы

### Внутренняя документация
- `for-claude-code/README.md` - Полный гайд по Claude Code
- `for-projects/README.md` - Шаблоны интеграции для проектов
- `for-projects/quick-start.md` - 5-минутная установка
- `.claude/CLAUDE.md` - Project instructions для Claude Code

### Внешние ресурсы
- [Shared KB Repository](https://github.com/ozand/shared-knowledge-base)
- [Claude Code Documentation](https://claude.com/claude-code)
