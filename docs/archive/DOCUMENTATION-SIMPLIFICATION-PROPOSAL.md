# Документация: Предложение по Упрощению

**Дата:** 2026-01-07
**Проблема:** 38 markdown файлов в корневой директории
**Цель:** 3-5 ключевых документов в корне, остальные в подпапках

---

## Текущая Ситуация

**Корневая директория:** 38 .md файлов

### Категории Файлов

1. **Ключевые документы** (5 файлов) - нужны пользователям
   - README.md
   - QUICKSTART.md
   - GUIDE.md
   - AGENT-QUICK-START.md
   - for-claude-code/README.md

2. **Installation guides** (6 файлов) - много дублирования
   - BOOTSTRAP-GUIDE.md (deprecated)
   - LOCAL-INSTALL-GUIDE.md
   - QUICK_SETUP_CLAUDE.md
   - QUICK_SETUP_CLAUDE_FIXED.md
   - SETUP_GUIDE_FOR_CLAUDE.md
   - HARMONIZED-INSTALLATION-GUIDE.md

3. **Analysis/Report files** (12 файлов) - временные аналитические документы
   - AGENT-INFORMATION-FLOW-*.md (3 файла)
   - FINAL-*REPORT.md (2 файла)
   - *_ANALYSIS.md (7 файлов)

4. **Specific guides** (6 файлов) - узкоспециализированные
   - AGENT_AUTOCONFIG_GUIDE.md
   - AGENT_INTEGRATION_GUIDE.md
   - GITHUB_ATTRIBUTION_GUIDE.md
   - ROLE_SEPARATION_GUIDE.md
   - PULL_REQUEST_WORKFLOW.md
   - SUBMODULE_VS_CLONE.md

5. **Obsolete/temporary** (9 файлов)
   - CHAT_ANALYSIS_RESULTS.md
   - CHAT_SESSION_ANALYSIS_*.md
   - COMPREHENSIVE-TEST-REPORT.md
   - DOCUMENTATION_AUDIT_REPORT.md
   - LABELS_INSTALLED.md
   - README_INTEGRATION.md
   - TEST_KB_CURATOR.md
   - ENTERPRISE-KNOWLEDGE-GRAPH.md

---

## Предлагаемая Структура

### В Корне (3-5 файлов)

```
shared-knowledge-base/
├── README.md                    ✅ Главный entry point (краткий!)
├── QUICKSTART.md                ✅ 5-минутный quick start
├── for-claude-code/             ✅ Документация Claude Code
│   └── README.md                ✅ Полный гайд для Claude Code
└── docs/
    ├── research/                📁 Аналитические документы
    │   └── *ANALYSIS.md
    ├── archive/                 📁 Устаревшие гайды
    │   ├── BOOTSTRAP-GUIDE.md
    │   ├── QUICK_SETUP_*.md
    │   └── OLD_*.md
    └── guides/                  📁 Узкоспециализированные гайды
        ├── installation/        📁 Installation guides
        │   └── HARMONIZED-INSTALLATION-GUIDE.md
        ├── integration/         📁 Integration guides
        │   ├── AGENT_AUTOCONFIG_GUIDE.md
        │   └── SUBMODULE_VS_CLONE.md
        └── workflows/           📁 Workflow guides
            ├── GITHUB_ATTRIBUTION_GUIDE.md
            ├── ROLE_SEPARATION_GUIDE.md
            └── PULL_REQUEST_WORKFLOW.md
```

---

## План Реорганизации

### Шаг 1: Создать структуру директорий

```bash
mkdir -p docs/research
mkdir -p docs/archive
mkdir -p docs/guides/installation
mkdir -p docs/guides/integration
mkdir -p docs/guides/workflows
```

### Шаг 2: Переместить файлы

**В docs/research/ (аналитические документы):**
- AGENT-INFORMATION-FLOW-ANALYSIS.md
- AGENT-INFORMATION-FLOW-IMPLEMENTATION.md
- AGENT-INFORMATION-FLOW-PHASE2.md
- ARCHITECTURE-ANALYSIS.md
- CHAT_SESSION_ANALYSIS_2026-01-06.md
- FINAL-ARCHITECTURE-REPORT.md
- FINAL-HARMONIZATION-REPORT.md
- PROJECT_AGENT_ROLE_CONFUSION_ANALYSIS.md
- REPOSITORY_STATE_ANALYSIS.md
- SHARED_KB_UPDATE_MECHANISMS_ANALYSIS.md
- SUBMODULE_CONTEXT_CONTAMINATION_ANALYSIS.md
- PLAIN_CLONE_PROJECT_ANALYSIS.md

**В docs/archive/ (устаревшие):**
- BOOTSTRAP-GUIDE.md (deprecated)
- QUICK_SETUP_CLAUDE.md
- QUICK_SETUP_CLAUDE_FIXED.md
- SETUP_GUIDE_FOR_CLAUDE.md
- LOCAL-INSTALL-GUIDE.md
- CHAT_ANALYSIS_RESULTS.md
- COMPREHENSIVE-TEST-REPORT.md
- DOCUMENTATION_AUDIT_REPORT.md
- LABELS_INSTALLED.md
- README_INTEGRATION.md
- TEST_KB_CURATOR.md
- ENTERPRISE-KNOWLEDGE-GRAPH.md
- CLEAN_STRUCTURE_PROPOSAL.md

**В docs/guides/installation/:**
- HARMONIZED-INSTALLATION-GUIDE.md (единственный installation guide)

**В docs/guides/integration/:**
- AGENT_AUTOCONFIG_GUIDE.md
- AGENT_INTEGRATION_GUIDE.md
- SUBMODULE_VS_CLONE.md

**В docs/guides/workflows/:**
- GITHUB_ATTRIBUTION_GUIDE.md
- ROLE_SEPARATION_GUIDE.md
- PULL_REQUEST_WORKFLOW.md
- PROJECT_AGENT_TO_CURATOR_MECHANISMS.md

### Шаг 3: Оставить в корне

**Только 5 файлов:**
1. **README.md** - Обзор проекта (краткий, с ссылками)
2. **QUICKSTART.md** - 5-минутный quick start
3. **AGENT-QUICK-START.md** - Quick start для агентов
4. **GUIDE.md** - Подробный гайд (можно переместить в docs/)
5. **for-claude-code/README.md** - Claude Code integration

---

## Новые Версии Ключевых Документов

### README.md (Краткий, без дублирования)

**Принципы:**
- Максimum 200 строк
- Только overview + quick start
- Ссылки на детальные гайды
- Не дублировать содержание других документов

**Структура:**
```markdown
# Shared Knowledge Base

## Overview (2-3 sentences)
## Quick Start (installation command)
## Features (bulleted list)
## Documentation (links)
## Contributing (links)
```

### QUICKSTART.md (5 минут, без дублирования)

**Принципы:**
- Maximum 150 строк
- Только installation + basic usage
- Ссылки на подробные гайды

**Структура:**
```markdown
# Quick Start (5 minutes)

## Installation (1 command)
## First Use (3 commands)
## Common Commands (list)
## Next Steps (links to detailed guides)
```

### for-claude-code/README.md (Полный, но структурированный)

**Принципы:**
- Может быть длинным (это специализируемый гайд)
- Progressive disclosure - основное upfront, детали в подпапках
- Ссылки на другие гайды, не дублирование

---

## Устранение Дублирования

### Текущее Дублирование

**Installation instructions в 6 файлах:**
1. README.md
2. QUICKSTART.md
3. AGENT-QUICK-START.md
4. for-claude-code/README.md
5. BOOTSTRAP-GUIDE.md
6. HARMONIZED-INSTALLATION-GUIDE.md

**Решение:**
- README.md → Только одна команда + ссылка на QUICKSTART
- QUICKSTART.md → Полный installation guide (150 строк)
- for-claude-code/README.md → Краткая установка + ссылка на QUICKSTART
- Остальные → В archive/ или удалить

### Submodule vs Clone в 3 файлах

**Решение:**
- SUBMODULE_VS_CLONE.md → В docs/guides/integration/
- Другие файлы → Удалить дублирующие секции

---

## Метрики Успеха

| Метрика | Сейчас | После | Цель |
|---------|--------|-------|------|
| **Файлов в корне** | 38 | 5 | 87% ↓ |
| **Installation guides** | 6 | 1 (QUICKSTART) | 83% ↓ |
| **Средний размер README** | ~600 строк | ~200 строк | 67% ↓ |
| **Дублирование** | Высокое | Минимальное | 90% ↓ |

---

## Предложение: Синхронизация

### Вариант 1: Быстрая реорганизация (1 час)

```bash
# 1. Создать структуру
mkdir -p docs/{research,archive,guides/{installation,integration,workflows}}

# 2. Переместить файлы
git mv *ANALYSIS.md docs/research/
git mv *REPORT.md docs/research/
git mv BOOTSTRAP-GUIDE.md docs/archive/
git mv QUICK_SETUP_*.md docs/archive/
# ... и т.д.

# 3. Обновить ссылки
# (заменить пути в документах)
```

### Вариант 2: Постепенная реорганизация (создать новые)

1. Создать новые краткие документы
2. Переместить старые в archive/
3. Обновить ссылки
4. Удалить archive/ через месяц

---

## Заключение

**Проблема:** 38 файлов в корне, много дублирования

**Решение:**
- 5 файлов в корне
- Остальные в docs/{research,archive,guides/}
- Краткие документы со ссылками
- Минимальное дублирование

**Следующие шаги:**
1. Создать структуру директорий
2. Переместить файлы
3. Создать новые краткие версии README.md и QUICKSTART.md
4. Обновить все ссылки

**Готов приступить?**
