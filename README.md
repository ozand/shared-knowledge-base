# Shared Knowledge Base

**Version 5.1** - Two-tier knowledge management for AI agents

🆕 **NEW: v5.1 with Two-Tier Architecture** - Separate Project KB and Shared KB with GitHub Issues workflow

Centрализованная база знаний для разработки ПО с системой метаданных, предиктивной аналитикой и распознаванием паттернов.

[English](#english) | [Русский](#russian)

---

## 🆕 What's New in v5.1?

**Two-Tier Architecture** (2026-01-08)

- ✅ **Project KB** (`.kb/project/`) - Private knowledge, direct commits
- ✅ **Shared KB** (`.kb/shared/`) - Universal patterns, GitHub Issues workflow
- ✅ **Automatic Context Loading** - SessionStart hook injects project context
- ✅ **PyGithub Integration** - No more `gh` CLI dependency
- ✅ **Decision Criteria** - Agent knows what to share via `sharing_criteria`

**Quick Links:**
- 📖 [v5.1 Documentation](docs/v5.1/README.md)
- 🚀 [v5.1 Quick Start](docs/v5.1/README.md#quick-start)
- 🔄 [Migration Guide](docs/v5.1/MIGRATION-PLAN.md)

**Backward Compatible:** ✅ v4.0 tools still work! Migrate at your own pace.

---

## <a name="english"></a>English

### Quick Start

**One-command installation:**

```bash
python scripts/unified-install.py --full
```

Or remote download:

```bash
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/unified-install.py | python3 - --full
```

**For detailed instructions:** [QUICKSTART.md](QUICKSTART.md) (5 minutes setup)

### What It Does

Shared KB provides:

- ✅ **Centralized knowledge** - Verified solutions for common errors across all languages/frameworks
- ✅ **AI-agnostic** - Works with Claude Code, GitHub Copilot, Cursor, Roo Code
- ✅ **Metadata system** - Quality scores, usage tracking, change detection
- ✅ **Auto-discovery** - Agents automatically find and use relevant patterns
- ✅ **Cross-platform** - Windows, macOS, Linux (Python-based, no emoji issues)

### Key Features

**v4.0 Features:**
- 📚 **149 knowledge entries** - Python, JavaScript, Docker, PostgreSQL, Universal patterns
- 🚀 **Progressive domain loading** - Load only what you need (83% token reduction)
- 🔗 **GitHub-native contribution** - Submit via issues, automated feedback loop
- 🤖 **AI Agent Integration** - Auto-loaded instructions, curator slash commands
- ⚡ **Zero infrastructure** - 100% GitHub Actions automation
- 📊 **Optimized indexing** - Domain index ~80 tokens (99.1% reduction)

### Documentation

**Getting Started:**
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[QUICKSTART-DOMAINS.md](QUICKSTART-DOMAINS.md)** - Progressive domain loading (v3.1)
- **[for-claude-code/README.md](for-claude-code/README.md)** - Complete Claude Code guide
- **[for-claude-code/AGENT-QUICK-START.md](for-claude-code/AGENT-QUICK-START.md)** - Quick start for AI agents

**Core Documentation:**
- **[GUIDE.md](GUIDE.md)** - Complete user guide
- **[docs/README.md](docs/README.md)** - Documentation hub
- **[docs/YAML-SCHEMA-V3.1.md](docs/YAML-SCHEMA-V3.1.md)** - YAML schema reference (v3.1)

**Integration:**
- **[docs/guides/integration/SUBMODULE_VS_CLONE.md](docs/guides/integration/SUBMODULE_VS_CLONE.md)** - Submodule vs Clone comparison
- **[docs/guides/integration/AGENT_AUTOCONFIG_GUIDE.md](docs/guides/integration/AGENT_AUTOCONFIG_GUIDE.md)** - Agent configuration

**Workflows:**
- **[docs/guides/workflows/GITHUB_ATTRIBUTION_GUIDE.md](docs/guides/workflows/GITHUB_ATTRIBUTION_GUIDE.md)** - GitHub contribution workflow
- **[docs/guides/workflows/ROLE_SEPARATION_GUIDE.md](docs/guides/workflows/ROLE_SEPARATION_GUIDE.md)** - Project Agent vs Curator roles

### ⚠️ Role-Based Access Control

**Project Agents:**
- ❌ DO NOT commit to shared-knowledge-base
- ✅ DO create GitHub issues with contributions
- ✅ Follow [AGENT-HANDOFF-001](universal/patterns/agent-handoff.yaml) workflow

**Curator Agent:**
- ✅ Review issues from project agents
- ✅ Commit approved changes
- ✅ ONLY agent who can commit to KB

**See:** [docs/guides/workflows/ROLE_SEPARATION_GUIDE.md](docs/guides/workflows/ROLE_SEPARATION_GUIDE.md)

### Architecture

```
shared-knowledge-base/
├── python/              # Python errors & patterns
├── javascript/          # JavaScript/Node.js
├── docker/              # Docker/container
├── postgresql/          # PostgreSQL
├── universal/           # Cross-language patterns
│   ├── patterns/        # Best practices
│   └── agent-instructions/  # Auto-loaded by agents
├── tools/               # kb.py CLI tool
├── for-claude-code/     # Claude Code integration
├── for-projects/        # Agent/skill/command templates
├── docs/
│   ├── research/        # Analysis & research
│   ├── archive/         # Deprecated guides
│   └── guides/          # Specialized guides
└── scripts/
    └── unified-install.py  # Cross-platform installer
```

### Usage

```bash
# Search knowledge base
python docs/knowledge-base/shared/tools/kb.py search "websocket"
python docs/knowledge-base/shared/tools/kb.py search --category python

# Statistics
python docs/knowledge-base/shared/tools/kb.py stats

# Build index
python docs/knowledge-base/shared/tools/kb.py index -v

# Check for updates
python docs/knowledge-base/shared/scripts/unified-install.py --check
```

### Contributing

**For Users:**
1. Search KB first: `python tools/kb.py search "error"`
2. If not found, document the solution in YAML
3. Validate: `python tools/kb.py validate entry.yaml`
4. Create GitHub issue with attribution
5. Wait for Curator review

**For Curators:**
- Review GitHub issues
- Validate and enhance contributions
- Commit to shared-knowledge-base
- See [curator/](curator/) for details

### Community

- **Issues:** [GitHub Issues](https://github.com/ozand/shared-knowledge-base/issues)
- **Documentation:** See [Documentation](#documentation) section above

### License

MIT License - see [LICENSE](LICENSE) for details

---

## <a name="russian"></a>Русский

### Быстрый Старт

**Установка одной командой:**

```bash
python scripts/unified-install.py --full
```

Или удаленная загрузка:

```bash
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/unified-install.py | python3 - --full
```

**Подробные инструкции:** [QUICKSTART.md](QUICKSTART.md) (настройка за 5 минут)

### Основные Возможности

- ✅ **Централизованная база знаний** - Проверенные решения для распространенных ошибок
- ✅ **AI-agnostic** - Работает с Claude Code, GitHub Copilot, Cursor, Roo Code
- ✅ **Система метаданных** - Оценка качества, отслеживание использования
- ✅ **Авто-обнаружение** - Агенты автоматически находят и используют паттерны
- ✅ **Cross-platform** - Windows, macOS, Linux (на базе Python)

### Документация

**Начало работы:**
- **[QUICKSTART.md](QUICKSTART.md)** - Гайд быстрого старта (5 минут)
- **[for-claude-code/README.md](for-claude-code/README.md)** - Полный гайд для Claude Code

**Руководства:**
- **[docs/guides/installation/HARMONIZED-INSTALLATION-GUIDE.md](docs/guides/installation/HARMONIZED-INSTALLATION-GUIDE.md)** - Установка и обновление
- **[AGENT-QUICK-START.md](AGENT-QUICK-START.md)** - Quick start для AI агентов

**См. раздел [Documentation](#documentation) выше для полного списка.**

---

**Version:** 3.2
**Last Updated:** 2026-01-07
**Repository:** https://github.com/ozand/shared-knowledge-base
