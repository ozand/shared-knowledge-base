# Shared Knowledge Base

**Version 3.0 - Complete Metadata System** 🚀

Централизованная база знаний для разработки ПО с продвинутой системой метаданных, предиктивной аналитикой и распознаванием паттернов.

[English](#english) | [Русский](#russian)

---

## <a name="english"></a>English

### What's New in v3.0

- ✅ **Metadata Management** - Quality scores (0-100), usage tracking, change detection
- ✅ **Freshness Checking** - Automatic library version monitoring (PyPI, npm, GitHub)
- ✅ **Predictive Analytics** - Update predictions, risk assessment, quality estimation
- ✅ **Pattern Recognition** - Find similar patterns across projects
- ✅ **Community Analytics** - Privacy-first aggregation across projects
- ✅ **Automated Scripts** - Daily/weekly/monthly maintenance automation
- ✅ **GitHub Issues Integration** - Automatic issue creation for migration errors (NEW)

**v2.0 Features:**
- ✅ Cross-platform Python CLI (`kb.py`) - works on Windows/Mac/Linux
- ✅ SQLite indexing - fast search with 1M+ entries
- ✅ AI-agnostic - works with Claude Code, GitHub Copilot, Cursor, Roo Code
- ✅ Multi-language - Python, JavaScript, Docker, and more
- ✅ JSON export - programmatic access for AI tools

### Quick Start

```bash
# 1. Clone or add as submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base/shared

# 2. Copy kb.py tool
cp docs/knowledge-base/shared/tools/kb.py docs/knowledge-base/tools/

# 3. Install dependencies
pip install pyyaml

# 4. Build index
python docs/knowledge-base/tools/kb.py index -v

# 5. Search!
python docs/knowledge-base/tools/kb.py search "async"
```

**See [QUICKSTART.md](QUICKSTART.md) for detailed setup.**

### 📚 For Knowledge Base Curators

**Are you maintaining this knowledge base?** See the [Curator Documentation Index](CURATOR_DOCS_INDEX.md) for:

- 🎯 **[AGENT.md](AGENT.md)** - Curator role definition and responsibilities
- 🛠️ **[SKILLS.md](SKILLS.md)** - Available skills (audit-quality, find-duplicates, research-enhance, etc.)
- 📋 **[WORKFLOWS.md](WORKFLOWS.md)** - Standard operating procedures
- ⭐ **[QUALITY_STANDARDS.md](QUALITY_STANDARDS.md)** - Entry quality rubric (0-100)
- 💬 **[PROMPTS.md](PROMPTS.md)** - Reusable AI prompt templates
- 🚀 **[README_CURATOR.md](README_CURATOR.md)** - Quick start guide for curators

**Key capabilities:**
- Quality assurance and validation
- Duplicate detection and merging
- Deep research enhancement (Perplexity, Gemini, etc.)
- Gap analysis and knowledge expansion
- Version updates and deprecation
- Cross-reference optimization

### What's Inside

**Supported Languages:**
- 🐍 **Python** - imports, type checking, async, testing
- 🟨 **JavaScript** - async/await, Promises, event loop
- 🐳 **Docker** - networking, volumes, ports
- 🌍 **Universal** - Git workflows, Clean Architecture

**Content:**
- **Errors** - Common mistakes with solutions
- **Patterns** - Best practices and proven patterns
- **Tools** - Automation scripts and utilities

### Project Structure

```
shared-knowledge-base/
├── python/              # Python-specific
│   ├── errors/
│   └── patterns/
├── javascript/          # JavaScript-specific
│   ├── errors/
│   └── patterns/
├── docker/              # Docker-specific
│   ├── errors/
│   └── patterns/
├── universal/           # Cross-language
│   ├── errors/
│   └── patterns/
├── framework/           # Framework-specific
│   ├── django/
│   ├── fastapi/
│   ├── react/
│   └── vue/
├── tools/               # Enhanced tooling (v3.0) ⭐
│   ├── kb.py           # Main CLI tool (enhanced with 6 new commands)
│   ├── kb_meta.py      # Metadata manager
│   ├── kb_usage.py     # Usage tracker
│   ├── kb_changes.py   # Change detector
│   ├── kb_freshness.py # Freshness checker
│   ├── kb_git.py       # Git integration
│   ├── kb_versions.py  # Version monitor
│   ├── kb_community.py # Community analytics
│   ├── kb_predictive.py # Predictive analytics
│   ├── kb_patterns.py  # Pattern recognizer
│   └── kb_issues.py    # GitHub issues integration (NEW)
├── scripts/             # Automation scripts (NEW in v3.0)
│   ├── init_metadata.py
│   ├── daily_freshness.py
│   ├── weekly_usage.py
│   └── monthly_community.py
└── *_meta.yaml         # Metadata files (git-synced)
```

### Using kb.py

```bash
# Search
kb search "keyword"
kb search --category python --severity high
kb search --tags async pytest

# Statistics
kb stats

# Validate
kb validate path/to/file.yaml

# Export for AI tools
kb export --format json --output kb.json
```

**New in v3.0 - Metadata Commands:**

```bash
# Initialize metadata for all entries
kb init-metadata

# Detect changes since last check
kb detect-changes

# Check entry freshness
kb check-freshness

# Analyze usage patterns
kb analyze-usage

# Update entry metadata
kb update-metadata --entry-id ERROR-ID --quality-score 85

# Reindex metadata
kb reindex-metadata
```

**New in v3.0 - Advanced Analytics:**

```bash
# Check library versions
python -m tools.kb_versions check --library fastapi

# Predict updates needed
python -m tools.kb_predictive predict-updates --days 30

# Find similar patterns
python -m tools.kb_patterns report

# Export community analytics
python -m tools.kb_community export-analytics --project-name "MyApp"
```

**New in v3.0 - GitHub Issues Integration:**

```bash
# Scan for issues and create GitHub tickets automatically
python -m tools.kb_issues scan --type all

# Create issues for specific problem types
python -m tools.kb_issues scan --type yaml-errors
python -m tools.kb_issues scan --type quality-issues
python -m tools.kb_issues scan --type missing-metadata

# Manually create issue for specific error
python -m tools.kb_issues create \
  --type yaml-errors \
  --file postgresql/errors.yaml \
  --reason "Mapping value error at line 410"
```

**Use Case:** When migrating KB to new projects, automatically create GitHub issues for any YAML errors or quality problems. A separate KB Curator agent then fixes these issues, and you sync back the corrections.

### Scope Levels

Knowledge is organized hierarchically:

1. **universal** - Cross-language (Git, testing, architecture)
2. **python, javascript, etc.** - Language-specific
3. **django, react, etc.** - Framework-specific
4. **project** - Project-specific (not shared)

### Contributing

We welcome contributions!

1. Fork this repository
2. Add your error/pattern with proper scope
3. Validate: `kb validate your-file.yaml`
4. Submit Pull Request

**See [GUIDE.md](GUIDE.md) for detailed guidelines.**

### Integration with AI Tools

**Claude Code:**
```bash
kb search "error description"
```

**GitHub Copilot / Cursor / Roo Code:**
```bash
kb export --format json --output kb-snapshot.json
# AI tools can consume this JSON
```

### Scalability

| Entries | Search Time |
|---------|-------------|
| 1,000 | < 10ms |
| 10,000 | < 50ms |
| 100,000 | < 200ms |
| 1,000,000 | < 1s |

Powered by SQLite FTS5.

### Documentation

**Getting Started:**
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[FOR_CLAUDE_CODE.md](FOR_CLAUDE_CODE.md)** - Complete guide for Claude Code (v3.0)
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deployment instructions

**For Curators:**
- **[CURATOR_DOCS_INDEX.md](CURATOR_DOCS_INDEX.md)** - Documentation index
- **[AGENT.md](AGENT.md)** - Curator role definition
- **[SKILLS.md](SKILLS.md)** - All available skills
- **[WORKFLOWS.md](WORKFLOWS.md)** - Standard procedures
- **[QUALITY_STANDARDS.md](QUALITY_STANDARDS.md)** - Quality rubric (0-100)
- **[PROMPTS.md](PROMPTS.md)** - Reusable AI prompts

**Technical:**
- **[METADATA_ARCHITECTURE.md](METADATA_ARCHITECTURE.md)** - Metadata system design
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Implementation details
- **[PHASE3_SUMMARY.md](PHASE3_SUMMARY.md)** - Phase 3 features
- **Repository:** https://github.com/ozand/shared-knowledge-base

### License

MIT License - Free to use in any project.

---

## <a name="russian"></a>Русский

### Что нового в v3.0

- ✅ **Управление метаданными** - Quality scores (0-100), трекинг использования, детекция изменений
- ✅ **Проверка актуальности** - Автоматический мониторинг версий библиотек (PyPI, npm, GitHub)
- ✅ **Предиктивная аналитика** - Прогнозирование обновлений, оценка рисков, оценка качества
- ✅ **Распознавание паттернов** - Поиск похожих паттернов между проектами
- ✅ **Аналитика сообщества** - Приватная агрегация данных между проектами
- ✅ **Автоматизация** - Daily/weekly/monthly скрипты обслуживания

**Возможности v2.0:**
- ✅ Кросс-платформенный Python CLI (`kb.py`) - работает на Windows/Mac/Linux
- ✅ SQLite индексация - быстрый поиск до 1М+ записей
- ✅ AI-агностичность - работает с Claude Code, GitHub Copilot, Cursor, Roo Code
- ✅ Многоязычность - Python, JavaScript, Docker и др.
- ✅ JSON экспорт - программный доступ для AI инструментов

### Быстрый старт

```bash
# 1. Клонировать или добавить как submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base/shared

# 2. Скопировать kb.py
cp docs/knowledge-base/shared/tools/kb.py docs/knowledge-base/tools/

# 3. Установить зависимости
pip install pyyaml

# 4. Построить индекс
python docs/knowledge-base/tools/kb.py index -v

# 5. Искать!
python docs/knowledge-base/tools/kb.py search "async"
```

**См. [QUICKSTART.md](QUICKSTART.md) для подробной настройки.**

### Что внутри

**Поддерживаемые языки:**
- 🐍 **Python** - импорты, типизация, async, тестирование
- 🟨 **JavaScript** - async/await, Promises, event loop
- 🐳 **Docker** - сети, volumes, порты
- 🌍 **Universal** - Git workflows, Clean Architecture

**Содержимое:**
- **Errors** - Типовые ошибки с решениями
- **Patterns** - Best practices и проверенные паттерны
- **Tools** - Скрипты автоматизации

### Использование kb.py

```bash
# Поиск
kb search "ключевое слово"
kb search --category python --severity high
kb search --tags async pytest

# Статистика
kb stats

# Валидация
kb validate путь/к/файлу.yaml

# Экспорт для AI
kb export --format json --output kb.json
```

### Уровни Scope

Знания организованы иерархически:

1. **universal** - Кросс-языковые (Git, тестирование, архитектура)
2. **python, javascript, и т.д.** - Специфичные для языка
3. **django, react, и т.д.** - Специфичные для фреймворка
4. **project** - Специфичные для проекта (не публикуются)

### Вклад

Приветствуем вклад в базу знаний!

1. Fork этого репозитория
2. Добавьте свою ошибку/паттерн с правильным scope
3. Валидируйте: `kb validate ваш-файл.yaml`
4. Создайте Pull Request

**См. [GUIDE.md](GUIDE.md) для подробных инструкций.**

### Интеграция с AI инструментами

**Claude Code:**
```bash
kb search "описание ошибки"
```

**GitHub Copilot / Cursor / Roo Code:**
```bash
kb export --format json --output kb-snapshot.json
# AI инструменты могут использовать этот JSON
```

### Масштабируемость

| Записей | Время поиска |
|---------|--------------|
| 1,000 | < 10ms |
| 10,000 | < 50ms |
| 100,000 | < 200ms |
| 1,000,000 | < 1s |

На базе SQLite FTS5.

### Документация

**Начало работы:**
- **[QUICKSTART.md](QUICKSTART.md)** - Установка за 5 минут
- **[FOR_CLAUDE_CODE.md](FOR_CLAUDE_CODE.md)** - Полный гайд для Claude Code (v3.0)
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Инструкции по деплою

**Для кураторов:**
- **[CURATOR_DOCS_INDEX.md](CURATOR_DOCS_INDEX.md)** - Индекс документации
- **[AGENT.md](AGENT.md)** - Определение роли куратора
- **[SKILLS.md](SKILLS.md)** - Все доступные навыки
- **[WORKFLOWS.md](WORKFLOWS.md)** - Стандартные процедуры
- **[QUALITY_STANDARDS.md](QUALITY_STANDARDS.md)** - Рубрика качества (0-100)
- **[PROMPTS.md](PROMPTS.md)** - Переиспользуемые AI промпты

**Техническая документация:**
- **[METADATA_ARCHITECTURE.md](METADATA_ARCHITECTURE.md)** - Архитектура метасистемы
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Детали реализации
- **[PHASE3_SUMMARY.md](PHASE3_SUMMARY.md)** - Возможности Phase 3
- **Репозиторий:** https://github.com/ozand/shared-knowledge-base

### Лицензия

MIT License - Свободно для использования в любых проектах.

---

## Statistics

**Current Knowledge Base:**
- Python: 12+ errors, 3+ patterns
- JavaScript: 3+ errors
- Docker: 3+ errors
- Universal: 5+ patterns

**Continuously growing** - contributions welcome!

---

**Start using now:** See [QUICKSTART.md](QUICKSTART.md) 🚀
