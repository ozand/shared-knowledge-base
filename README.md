# Shared Knowledge Base

**Version 2.0 - Hybrid Approach** 🚀

Централизованная база знаний для разработки ПО. Содержит проверенные решения типовых ошибок для множества языков и фреймворков.

[English](#english) | [Русский](#russian)

---

## <a name="english"></a>English

### What's New in v2.0

- ✅ **Cross-platform Python CLI** (`kb.py`) - works on Windows/Mac/Linux
- ✅ **SQLite indexing** - fast search with 1M+ entries
- ✅ **AI-agnostic** - works with Claude Code, GitHub Copilot, Cursor, Roo Code
- ✅ **Multi-language** - Python, JavaScript, Docker, and more
- ✅ **JSON export** - programmatic access for AI tools

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
└── tools/
    ├── kb.py           # Main CLI tool (v2.0) ⭐
    ├── search-kb.py    # Legacy search
    ├── sync-knowledge.py
    └── validate-kb.py
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

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[GUIDE.md](GUIDE.md)** - Implementation guide
- **Repository:** https://github.com/ozand/shared-knowledge-base

### License

MIT License - Free to use in any project.

---

## <a name="russian"></a>Русский

### Что нового в v2.0

- ✅ **Кросс-платформенный Python CLI** (`kb.py`) - работает на Windows/Mac/Linux
- ✅ **SQLite индексация** - быстрый поиск до 1М+ записей
- ✅ **AI-агностичность** - работает с Claude Code, GitHub Copilot, Cursor, Roo Code
- ✅ **Многоязычность** - Python, JavaScript, Docker и др.
- ✅ **JSON экспорт** - программный доступ для AI инструментов

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

- **[QUICKSTART.md](QUICKSTART.md)** - Установка за 5 минут
- **[GUIDE.md](GUIDE.md)** - Руководство по использованию
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
