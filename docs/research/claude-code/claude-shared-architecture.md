# Архитектура Claude Code для Shared моделей знаний
## Лучшие практики организации SKILLS, AGENTS, MEMORY для нескольких проектов

---

## Оглавление

1. [Концепция Shared Model](#концепция-shared-model)
2. [Уровни конфигурации (Scope System)](#уровни-конфигурации-scope-system)
3. [Структура служебных файлов](#структура-служебных-файлов)
4. [CLAUDE.md: Иерархия и организация](#claudemd-иерархия-и-организация)
5. [SKILLS и AGENTS для повторного использования](#skills-и-agents-для-повторного-использования)
6. [MEMORY: Управление контекстом](#memory-управление-контекстом)
7. [HOOKS: Детерминированная автоматизация](#hooks-детерминированная-автоматизация)
8. [Shared архитектура для команд](#shared-архитектура-для-команд)
9. [Практические примеры структур](#практические-примеры-структур)
10. [Checklist для внедрения](#checklist-для-внедрения)

---

## Концепция Shared Model

### Что такое Shared Model?

**Shared Model** — это единая система знаний, контекста и инструкций, которые используются:
- Несколько проектов (в монорепо или отдельных репозиториях)
- Несколько пользователей/разработчиков в команде
- Разные версии одного продукта (frontend, backend, mobile)

### Ключевые преимущества:

✅ **Консистентность** — все проекты следуют одним стандартам  
✅ **Масштабируемость** — новые проекты наследуют знания старых  
✅ **Экономия токенов** — переиспользование контекста вместо дублирования  
✅ **Онбординг** — новые разработчики получают полный context сразу  
✅ **Maintenance** — изменения в стандартах применяются ко всем сразу  
✅ **Colab** — команда работает с единой версией правды  

---

## Уровни конфигурации (Scope System)

Claude Code поддерживает **4 уровня конфигурации** с четкой иерархией приоритета:

### 1. **Enterprise Scope** (IT-управляемый)
```
/etc/claude/managed-settings.json  (Linux/Mac)
C:\ProgramData\Claude\...          (Windows)
```
- Применяется ко всем пользователям машины
- Управляется IT для corporate policies
- Наиболее низкий приоритет

### 2. **User Scope** (Личный)
```
~/.claude/
├── CLAUDE.md              # Глобальные инструкции
├── settings.json          # Глобальные настройки
└── .mcp.json             # MCP серверы
```
- Применяется ко всем проектам пользователя
- НЕ коммитится в git
- Личные предпочтения

### 3. **Project Scope** (Командный — ★ для Shared Models)
```
<project-root>/
└── .claude/
    ├── CLAUDE.md                    # Проект-специфичные инструкции
    ├── settings.json                # Проект-специфичные настройки
    ├── .mcp.json                   # MCP серверы проекта
    ├── hooks.json                  # Git hooks
    └── plugins.json                # Плагины
```
- **КОММИТИТСЯ В GIT** ✨
- Применяется ко всем разработчикам проекта
- Переопределяет user scope

### 4. **Local Scope** (Временный)
```
.claude/
├── CLAUDE.local.md        # Личные переопределения
├── settings.local.json    # Личные настройки
└── .mcp.local.json       # Личные MCP серверы
```
- Игнорируется в git (.gitignore)
- Только для текущей машины/сессии
- Самый высокий приоритет

### Приоритет разрешения конфликтов:
```
Local Scope (最高) 
    ↓
Project Scope (команда)
    ↓
User Scope (личное)
    ↓
Enterprise Scope (корпоративное,最低)
```

---

## Структура служебных файлов

### Рекомендуемая структура для Shared Model:

```
monorepo/
├── .claude/                           ← SHARED (Git-tracked)
│   ├── CLAUDE.md                      ← Глобальные инструкции монорепо
│   ├── settings.json                  ← Глобальные настройки
│   ├── .mcp.json                      ← Общие MCP серверы
│   ├── hooks.json                     ← Общие Git hooks
│   │
│   ├── skills/                        ← ★ Переиспользуемые SKILLS
│   │   ├── SKILL.md
│   │   ├── testing/
│   │   ├── deployment/
│   │   ├── documentation/
│   │   └── refactoring/
│   │
│   ├── agents/                        ← ★ Агенты для автоматизации
│   │   ├── code-review-agent.md
│   │   ├── pr-automation.md
│   │   ├── testing-agent.md
│   │   └── deployment-orchestrator.md
│   │
│   ├── standards/                     ← Единые стандарты
│   │   ├── architecture.md            ← Архитектурные решения
│   │   ├── coding-standards.md        ← Стандарты кода
│   │   ├── naming-conventions.md      ← Соглашения об именовании
│   │   ├── error-handling.md          ← Обработка ошибок
│   │   └── testing-guidelines.md      ← Гайдлайны тестирования
│   │
│   ├── references/                    ← Справочные материалы
│   │   ├── project-map.md             ← Карта проектов
│   │   ├── stack.md                   ← Tech stack
│   │   ├── apis.md                    ← API docs
│   │   └── database-schema.md         ← DB schema
│   │
│   └── team/                          ← Информация о команде
│       ├── principles.md              ← Командные принципы
│       ├── workflows.md               ← Рабочие процессы
│       ├── runbooks.md                ← Runbooks
│       └── faq.md                     ← Часто задаваемые вопросы
│
├── packages/
│   ├── ui/
│   │   └── .claude/
│   │       ├── CLAUDE.md              ← Package-специфичные инструкции
│   │       └── standards/
│   │           ├── component-patterns.md
│   │           └── a11y-guidelines.md
│   │
│   └── api/
│       └── .claude/
│           ├── CLAUDE.md              ← Package-специфичные инструкции
│           └── standards/
│               ├── endpoint-patterns.md
│               └── error-responses.md
│
├── apps/
│   ├── web/
│   │   └── .claude/
│   │       ├── CLAUDE.md              ← App-специфичные инструкции
│   │       └── specs/
│   │           ├── features.md
│   │           └── migrations.md
│   │
│   └── mobile/
│       └── .claude/
│           ├── CLAUDE.md              ← App-специфичные инструкции
│           └── specs/
│               └── platform-specific.md
│
└── docs/
    ├── shared-knowledge/              ← Документация для всех
    │   ├── onboarding.md
    │   ├── deployment-process.md
    │   ├── incident-response.md
    │   └── security.md
    │
    └── architecture/                  ← Архитектурные описания
        ├── system-overview.md
        ├── data-flow.md
        └── decisions/
            ├── adr-001-...md
            └── adr-002-...md
```

---

## CLAUDE.md: Иерархия и организация

### Принцип прогрессивного раскрытия

Claude.md работает **как система навигации**, не загружая весь контекст сразу:

```
CLAUDE.md (главный)
├── [Краткое резюме проекта]
├── [Ссылки на детали]
│   ├── @.claude/standards/architecture.md
│   ├── @.claude/standards/coding-standards.md
│   └── @docs/shared-knowledge/deployment-process.md
└── [Специфичные для этого уровня инструкции]
```

### Структура главного CLAUDE.md (Root монорепо)

```markdown
# CLAUDE.md — Shared Knowledge Model v1.0

## Project Summary
- **Type**: Monorepo (Full-stack application)
- **Tech Stack**: Next.js, Node.js, TypeScript, PostgreSQL
- **Teams**: 5-10 разработчиков
- **Last Updated**: 2025-01-06

## Architecture Overview
See `@.claude/standards/architecture.md` for detailed architecture decisions.

### Directory Map
```
packages/          # Shared packages (UI, utils)
apps/              # Applications (web, mobile)
services/          # Microservices (API, auth)
infra/             # Infrastructure & deployment
docs/              # Documentation
```

## Core Standards & Rules
- **Code**: See `@.claude/standards/coding-standards.md`
- **Architecture**: See `@.claude/standards/architecture.md`
- **Testing**: See `@.claude/standards/testing-guidelines.md`
- **Naming**: See `@.claude/standards/naming-conventions.md`

## Tech Stack Details
See `@.claude/references/stack.md` for full tech stack details.

## Common Commands
```bash
claude dev          # Start development
claude test         # Run tests
claude build        # Production build
claude deploy       # Deploy to staging
claude pr-check     # Pre-PR checks
```

## Workflows
See `@.claude/team/workflows.md` for detailed team workflows.

## Team Principles
See `@.claude/team/principles.md` for how we work together.

## Quick Refs
- **API Docs**: `@.claude/references/apis.md`
- **Database**: `@.claude/references/database-schema.md`
- **Troubleshooting**: `@.claude/team/runbooks.md`
- **FAQ**: `@.claude/team/faq.md`

## Skills Available
See `@.claude/skills/` for reusable Skills:
- Testing automation
- Code review
- Documentation
- Refactoring patterns

## Agents Available
See `@.claude/agents/` for automated agents:
- Code review agent
- PR automation
- Deployment orchestrator
- Testing agent

## Important Notes
- Always check for existing patterns before creating new
- Reference shared standards, not personal preferences
- Use Skills and Agents instead of manual prompts
- Keep this file under 500 lines (link to details)

## Version History
- v1.0 (2025-01-06) — Initial shared model setup
```

### Специфичные CLAUDE.md для package'а (packages/ui/.claude/CLAUDE.md)

```markdown
# CLAUDE.md — UI Package Standards

## Overview
This is a shared React component library used by web and mobile apps.

## Architecture
- **Pattern**: Component-driven with Storybook
- **State**: Zustand for complex components
- **Styling**: Tailwind CSS + CSS Modules
- **See also**: `@../../.claude/standards/architecture.md`

## Component Patterns
See `@./standards/component-patterns.md` for:
- Composability principles
- Props interfaces
- Render optimization
- Accessibility requirements

## Accessibility (A11y)
- All interactive elements must be keyboard navigable
- Color contrast: WCAG AA minimum
- See `@./standards/a11y-guidelines.md` for details

## Testing
- Unit tests: Vitest (for logic)
- Visual tests: Storybook
- Integration: No (test in consuming app)

## Naming Conventions
- Components: PascalCase (Button, Dialog)
- Exports: named exports only
- Props: camelCase with JSDoc

## Common Tasks
```bash
claude dev           # Storybook in development
claude build         # Build package
claude test          # Run unit tests
claude check-a11y    # Accessibility audit
```

## Links
- Global standards: `@../../.claude/standards/`
- Storybook docs: See README.md

## No changes without:
1. Matching existing component patterns
2. Updating Storybook stories
3. Adding/updating tests
4. A11y review (axe-core automated + manual)
```

---

## SKILLS и AGENTS для повторного использования

### SKILL.md: Структура для shared умений

**Skills** — это модульные возможности, которые Claude может вызывать автоматически.

#### Пример: Testing Skill

```
.claude/skills/testing/
├── SKILL.md                          ← Метаданные и инструкции
├── test-templates/                   ← Шаблоны тестов
│   ├── unit-test.template.ts
│   ├── integration-test.template.ts
│   └── e2e-test.template.ts
├── test-patterns.md                  ← Распространенные паттерны
├── common-assertions.md              ← Полезные assertions
└── generate-tests.sh                 ← Скрипт для генерации тестов
```

**SKILL.md содержит:**

```markdown
# Skill: Automated Testing

## What this Skill does
Generates tests that match your codebase patterns and runs test suites.

## Trigger
- User mentions "test", "testing", "write tests", "add coverage"
- Part of PR automation workflow
- Called by testing-agent

## What Claude can do with this Skill
- Generate unit tests matching your patterns
- Generate integration tests
- Generate E2E tests
- Run test suite and report coverage
- Suggest improvements based on coverage gaps

## Key files to reference
- Test patterns: `@test-patterns.md`
- Templates: Use `@test-templates/` for examples
- Assertions: `@common-assertions.md`

## Implementation rules (see references below)
1. Match existing test structure
2. Use describe/it pattern (Vitest)
3. Test behavior, not implementation
4. Reference related tests
5. Update snapshots carefully

## Common commands
```bash
claude test [filename]          # Generate tests for file
claude test --coverage          # Full coverage report
claude test --fix-coverage      # Suggest coverage fixes
```

See `@../../.claude/standards/testing-guidelines.md` for detailed rules.
```

#### Пример: Code Review Agent

```
.claude/agents/code-review-agent.md

# Agent: Code Review

## Purpose
Automatically reviews pull requests for code quality, architecture, and standards compliance.

## Trigger
- GitHub webhook on PR created/updated
- Manual invocation: `claude review [branch]`
- Pre-merge check

## Capabilities
- Architecture compliance (uses `@../../.claude/standards/architecture.md`)
- Code standards (uses `@../../.claude/standards/coding-standards.md`)
- Performance issues
- Security concerns
- Test coverage
- Documentation completeness

## Output format
Comments on GitHub PR with:
- Category (architecture, performance, security, etc.)
- Severity (critical, major, minor)
- Suggested fix
- Relevant standard reference

## How to use
```bash
claude review                    # Review current branch
claude review --strict           # Strict mode (fail on warnings)
claude review --standards-only   # Only standard violations
```

## Implementation
Uses shell script to:
1. Get PR files changed
2. For each file: `@test-review.sh`
3. Post results as comments

See `@../../.claude/agents/` for other agents.
```

### Как регистрировать Skills

Добавить в `.claude/settings.json`:

```json
{
  "skills": {
    "paths": [
      "./.claude/skills",
      "./packages/*/claude/skills"
    ],
    "enabled": ["testing", "refactoring", "documentation"],
    "auto_discover": true
  },
  "agents": {
    "paths": ["./.claude/agents"],
    "enabled": ["code-review", "pr-automation", "deployment"]
  }
}
```

---

## MEMORY: Управление контекстом

### Стратегия управления памятью для Shared Model

⚠️ **Критично**: Большой CLAUDE.md загружается в каждой сессии. Оптимизируйте!

### ✅ ДА — Положить в CLAUDE.md:
- Инструкции, которые используются в **КАЖДОЙ** сессии
- Project-специфичные правила
- Ссылки на другие документы
- Краткие резюме (5-10 строк max)

### ❌ НЕТ — Не класть в CLAUDE.md:
- Детальную документацию (ссылайтесь вместо этого)
- API документацию (используйте `@docs/`)
- Большие примеры (в отдельных файлах)
- Историческую информацию (в git commits)
- Никогда не повторяйте правила (разделите на parts)

### Рекомендуемые размеры:

| Файл | Максимум | Примечание |
|------|----------|-----------|
| Root CLAUDE.md | **500 строк** | Просто ссылки, краткие резюме |
| Package CLAUDE.md | **300 строк** | Специфичные для package инструкции |
| Reference файлы | **1000+ строк** | OK, загружаются по запросу |
| SKILL.md | **200 строк** | Короткие, сфокусированные |

### Паттерн: Reference с Table of Contents

Для больших справочных файлов добавить оглавление (Claude видит даже при partial read):

```markdown
# API Reference

## Table of Contents
- [Authentication](#authentication)
- [Users Endpoint](#users-endpoint)
- [Posts Endpoint](#posts-endpoint)
- [Comments Endpoint](#comments-endpoint)
- [Error Codes](#error-codes)

## Authentication
[details...]

## Users Endpoint
[details...]

## Posts Endpoint
[details...]

## Comments Endpoint
[details...]

## Error Codes
[details...]
```

### Компакция памяти (контролируемо)

**Не** использовать `/compact` после каждого сообщения (теряется контекст).

Вместо этого:
```bash
# Закончить одну задачу
/clear                          # Очистить память для новой задачи

# После нескольких сессий (если контекст стал огромным)
/compact                        # Только когда действительно нужно
```

---

## HOOKS: Детерминированная автоматизация

### Что такое HOOKS?

**Hooks** — это гарантированное выполнение shell-команд или LLM-запросов в специфических точках workflow Claude Code.

```
KEY DISTINCTION:

Prompts:   "Please run tests"      → Claude может забыть
Hooks:     Automatically runs tests → ГАРАНТИРОВАНО выполняется

Hooks = Deterministic automation, не suggestions
```

### Зачем нужны HOOKS?

```
ПРОБЛЕМА: LLM probabilistic
  - Попросили запустить тесты → Claude может забыть
  - Попросили проверить тип → Claude может пропустить
  - Попросили логировать → Claude может не сделать

РЕШЕНИЕ: Hooks = deterministic
  - Тесты ВСЕГДА запускаются после edit
  - Тип checking ВСЕГДА проверяется
  - Логирование ВСЕГДА происходит
  - Всё автоматично, без полагания на Claude
```

### Hook Events

| Event | Когда выполняется | Использование |
|-------|------------------|---------------|
| **PreToolUse** | Перед любым tool call | Валидация, блокирование, модификация input |
| **PostToolUse** | После успешного tool call | Лinting, форматирование, тестирование |
| **SessionStart** | При старте сессии | Setup, env configuration, загрузка контекста |
| **Stop** | Когда Claude завершил | Валидация completion, force continuation |
| **UserPromptSubmit** | Когда юзер сабмитит промпт | Валидация промпта, добавление контекста |
| **Notification** | Когда Claude отправляет уведомление | Desktop alerts, звуковые уведомления |

### Пример конфигурации

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/security-filter.py",
          "timeout": 5
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/quality-gate.sh",
            "timeout": 30
          },
          {
            "type": "command",
            "command": "npx prettier --write",
            "timeout": 10
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-setup.sh"
        }]
      }
    ]
  }
}
```

### Matcher Syntax

- `"Bash"` → Только Bash команды
- `"Edit|Write"` → Edit OR Write инструменты
- `"Edit:*.ts"` → Только TypeScript edit-ы
- `"mcp__.*__write"` → Любые MCP write операции
- `"*"` → Все инструменты (использовать осторожно!)

### Decision Control

| Event | Exit 0 (ALLOW) | Exit 2 (BLOCK) |
|-------|----------------|----------------|
| PreToolUse | Execute tool | Skip tool |
| PostToolUse | Continue | Feed back to Claude |
| Stop | Allow stop | Force continuation |

### Best Practices

✅ **DO:**
- Keep hooks FAST (<2 seconds)
- Use specific matchers (not `"*"`)
- Quote all variables: `"$VAR"`
- Test hooks manually before deploying
- Use `set -e` in bash scripts
- Provide clear error messages

❌ **DON'T:**
- Run full test suite in hooks (>5 sec) → Use CI/CD instead
- Use wildcard matchers → Too slow
- Forget to test → Debug in production
- Hardcode secrets → Use environment variables

### Примеры Hooks

#### 1. Quality Gate (PostToolUse)

```bash
#!/bin/bash
# .claude/hooks/quality-gate.sh

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path')

# Only check TypeScript files
if [[ ! "$FILE" == *.ts ]]; then
  exit 0
fi

echo "🔍 Quality checks for $FILE..."

# Prettier
if ! npx prettier --check "$FILE"; then
  echo "  ❌ Prettier: Not formatted"
  exit 2
fi

# ESLint
if ! npx eslint "$FILE"; then
  echo "  ❌ ESLint: Linting errors"
  exit 2
fi

echo "✅ All checks passed"
exit 0
```

#### 2. Security Filter (PreToolUse)

```python
#!/usr/bin/env python3
# .claude/hooks/security-filter.py

import json, sys, re

DANGEROUS = [
    (r'rm\s+-rf\s+/', 'Recursive root delete'),
    (r'sudo\s+rm', 'Sudo delete'),
    (r'chmod\s+777', 'World-writable permissions'),
]

data = json.load(sys.stdin)
if data.get('tool_name') != 'Bash':
    sys.exit(0)

command = data.get('tool_input', {}).get('command', '')

for pattern, reason in DANGEROUS:
    if re.search(pattern, command, re.IGNORECASE):
        output = {
            'decision': 'block',
            'reason': f'🚨 Security: {reason}'
        }
        print(json.dumps(output))
        sys.exit(0)

sys.exit(0)
```

### Дополнительные ресурсы

- **Полное руководство:** `claude-hooks-guide.md`
- **Production примеры:** `claude-hooks-examples.md`
- **Анти-паттерны:** `claude-hooks-advanced.md`
- **Pattern:** `universal/patterns/claude-code-hooks.yaml`

---

## Shared архитектура для команд

### Сценарий 1: Маленькая команда (2-5 человека)

```
myapp/
├── .claude/                    ← Все в одном месте
│   ├── CLAUDE.md               ← 200 строк, все основное
│   ├── settings.json
│   ├── skills/
│   │   └── common/
│   │       ├── testing.md
│   │       ├── refactoring.md
│   │       └── docs.md
│   └── standards/
│       ├── coding-standards.md
│       ├── architecture.md
│       └── workflow.md
├── src/
└── docs/

# Workflow:
# 1. Все читают главный CLAUDE.md
# 2. Используют Skills из .claude/skills/
# 3. Reference документы в docs/
```

### Сценарий 2: Средняя команда (5-15 человек) в Монорепо

```
monorepo/
├── .claude/                    ← Глобальные + shared
│   ├── CLAUDE.md               ← Карта + ссылки (300 строк)
│   ├── settings.json
│   ├── skills/                 ← Переиспользуемые
│   ├── agents/                 ← Автоматизированные workflow'ы
│   ├── standards/              ← Единые стандарты
│   └── team/                   ← Процессы команды
│
├── packages/
│   ├── ui/.claude/
│   │   ├── CLAUDE.md           ← UI-специфичные (200 строк)
│   │   └── standards/
│   │
│   ├── utils/.claude/
│   │   ├── CLAUDE.md           ← Utils-специфичные
│   │   └── patterns/
│   │
│   └── api/.claude/
│       ├── CLAUDE.md           ← API-специфичные
│       └── patterns/
│
├── apps/
│   ├── web/.claude/
│   │   └── CLAUDE.md           ← Web app-специфичные
│   │
│   └── mobile/.claude/
│       └── CLAUDE.md           ← Mobile app-специфичные
│
└── docs/
    └── shared-knowledge/

# Workflow:
# 1. Глобальный CLAUDE.md — начальная ориентация
# 2. Package .claude/CLAUDE.md — при работе с package
# 3. Skills/Agents — выполнение повторных задач
# 4. Standards — проверка соответствия
```

### Сценарий 3: Большая команда (15+ человек) с микросервисами

```
services-platform/
├── .claude/                    ← Самое критичное для всех
│   ├── CLAUDE.md               ← Минимально (200 строк)
│   ├── shared-skills/          ← Кроссервисные Skills
│   │   ├── deployment/
│   │   ├── testing/
│   │   └── monitoring/
│   ├── standards/
│   │   ├── api-standards.md
│   │   ├── data-model.md
│   │   ├── error-handling.md
│   │   └── security.md
│   └── team/
│       ├── architecture-review-process.md
│       ├── deployment-process.md
│       └── incident-response.md
│
├── services/
│   ├── user-service/
│   │   └── .claude/
│   │       ├── CLAUDE.md       ← Service-специфичные (150 строк)
│   │       ├── api-schema.md
│   │       └── db-schema.md
│   │
│   ├── auth-service/
│   │   └── .claude/
│   │       ├── CLAUDE.md
│   │       ├── auth-flows.md
│   │       └── security.md
│   │
│   ├── notification-service/
│   │   └── .claude/
│   │       └── CLAUDE.md
│   │
│   └── payment-service/
│       └── .claude/
│           ├── CLAUDE.md
│           └── payment-flows.md
│
├── libs/
│   ├── shared-types/.claude/CLAUDE.md
│   └── shared-utils/.claude/CLAUDE.md
│
├── infra/
│   └── .claude/
│       ├── CLAUDE.md           ← Infrastructure automation
│       ├── deployment-pipeline.md
│       └── monitoring-setup.md
│
└── docs/
    └── architecture/

# Workflow:
# 1. Новый сервис наследует глобальные standards
# 2. Свой CLAUDE.md для service-специфичного
# 3. Кроссервисные Skills в shared-skills/
# 4. Architecture reviews используют shared standards
# 5. Deployment agents автоматизируют процессы
```

### MCP (Model Context Protocol) для Shared Model

Использовать MCP для динамического загрузки контекста:

```json
{
  ".mcp.json": {
    "mcpServers": {
      "knowledge-loader": {
        "command": "node",
        "args": ["./tools/mcp-knowledge-loader.js"],
        "env": {
          "KNOWLEDGE_BASE": "./.claude/standards",
          "CONTEXT_TYPE": "project"
        }
      },
      "schema-validator": {
        "command": "python3",
        "args": ["./tools/mcp-schema-validator.py"],
        "env": {
          "SCHEMAS_PATH": "./.claude/references"
        }
      }
    }
  }
}
```

Пример MCP script (knowledge-loader.js):

```javascript
// Dynamically loads only needed standards based on context
const stdio = require('stdio');

const handlers = {
  'get_standards': (params) => {
    const { type } = params;  // 'architecture', 'coding', 'testing'
    // Load only the requested standard
    return loadStandard(type);
  },
  
  'get_pattern': (params) => {
    const { domain } = params;  // 'ui-components', 'api-endpoints'
    return getPattern(domain);
  }
};
```

---

## Практические примеры структур

### Пример 1: React Monorepo с Shared Components

```
project-react/
├── .claude/
│   ├── CLAUDE.md
│   │   ## Architecture
│   │   Monorepo с shared UI components. See `@.claude/standards/architecture.md`
│   │   
│   │   ## Tech Stack
│   │   React 18, TypeScript, Tailwind, Vitest
│   │   
│   │   ## Common Tasks
│   │   `claude dev` — Start dev server + Storybook
│   │   `claude test` — Run test suite
│   │   See `@.claude/skills/testing/` for test generation
│   │
│   ├── settings.json
│   │   {
│   │     "skills": {
│   │       "enabled": ["testing", "component-gen", "refactoring"]
│   │     },
│   │     "agents": {
│   │       "enabled": ["pr-review", "accessibility-check"]
│   │     }
│   │   }
│   │
│   ├── skills/
│   │   ├── component-gen/
│   │   │   └── SKILL.md
│   │   ├── testing/
│   │   │   ├── SKILL.md
│   │   │   └── test-templates/
│   │   └── refactoring/
│   │       └── SKILL.md
│   │
│   ├── standards/
│   │   ├── component-architecture.md
│   │   ├── a11y-guidelines.md
│   │   ├── testing-strategy.md
│   │   └── performance-budget.md
│   │
│   └── references/
│       ├── component-inventory.md
│       └── storybook-patterns.md
│
├── packages/
│   ├── ui/
│   │   ├── .claude/
│   │   │   └── CLAUDE.md
│   │   │       ## Component Library
│   │   │       Exports: Button, Dialog, Form, Layout components
│   │   │       See global `@../../.claude/standards/`
│   │   │
│   │   ├── src/
│   │   │   ├── components/
│   │   │   └── __stories__/
│   │   │
│   │   └── package.json
│   │
│   ├── hooks/
│   │   ├── .claude/
│   │   │   └── CLAUDE.md
│   │   │
│   │   ├── src/
│   │   │   ├── useForm.ts
│   │   │   ├── useLocalStorage.ts
│   │   │   └── useFetch.ts
│   │   │
│   │   └── package.json
│   │
│   └── utils/
│       ├── .claude/
│       │   └── CLAUDE.md
│       │
│       └── src/
│
├── apps/
│   ├── web/
│   │   ├── .claude/
│   │   │   └── CLAUDE.md
│   │   │       ## Web Application
│   │   │       Next.js + Vercel
│   │   │       See package standards in `@../../packages/*/`
│   │   │
│   │   ├── src/
│   │   │   ├── pages/
│   │   │   ├── components/
│   │   │   └── utils/
│   │   │
│   │   └── next.config.js
│   │
│   ├── admin/
│   │   └── .claude/
│   │       └── CLAUDE.md
│   │
│   └── mobile/
│       └── .claude/
│           └── CLAUDE.md
│
└── docs/
    ├── architecture/
    │   ├── system-overview.md
    │   ├── component-hierarchy.md
    │   └── data-flow.md
    │
    ├── workflows/
    │   ├── component-development.md
    │   ├── release-process.md
    │   └── incident-response.md
    │
    └── onboarding/
        ├── setup.md
        ├── first-component.md
        └── faq.md
```

---

### Пример 2: Backend + Frontend в одном Monorepo

```
full-stack-app/
├── .claude/
│   ├── CLAUDE.md
│   │   # Full-Stack Application
│   │   ## Architecture
│   │   Frontend: Next.js
│   │   Backend: Node.js/Express
│   │   Database: PostgreSQL
│   │   Infrastructure: Docker + Kubernetes
│   │   See `@.claude/standards/architecture.md`
│   │
│   │   ## Shared Standards
│   │   - API contracts: `@.claude/standards/api-standards.md`
│   │   - Database: `@.claude/standards/db-schema.md`
│   │   - Testing: `@.claude/standards/testing-strategy.md`
│   │   - Error handling: `@.claude/standards/errors.md`
│   │
│   │   ## Teams
│   │   Frontend: 3 people
│   │   Backend: 3 people
│   │   DevOps/Infra: 1 person
│   │
│   ├── settings.json
│   ├── .mcp.json
│   │
│   ├── standards/
│   │   ├── architecture.md      # System design
│   │   ├── api-standards.md     # REST API contracts
│   │   ├── db-schema.md         # Database schema
│   │   ├── testing-strategy.md  # Test approach
│   │   ├── error-handling.md    # Error codes & handling
│   │   ├── security.md          # Security practices
│   │   └── deployment.md        # CI/CD pipeline
│   │
│   ├── skills/
│   │   ├── api-generation/      # Auto-generate API routes
│   │   ├── migration-gen/       # Database migrations
│   │   ├── testing/
│   │   ├── e2e-testing/
│   │   └── deployment/
│   │
│   ├── agents/
│   │   ├── pr-review.md
│   │   ├── api-contract-check.md
│   │   ├── database-review.md
│   │   └── deployment-orchestrator.md
│   │
│   └── team/
│       ├── principles.md
│       ├── workflows.md
│       ├── incident-response.md
│       └── runbooks.md
│
├── frontend/
│   ├── .claude/
│   │   └── CLAUDE.md
│   │       ## Frontend Specifics
│   │       Framework: Next.js 14
│   │       State: Redux Toolkit
│   │       API client: TanStack Query
│   │       UI: shadcn/ui + Tailwind
│   │
│   │       ## Standards
│   │       See `@../../.claude/standards/`
│   │       Component patterns: `@./standards/component-patterns.md`
│   │       Testing: `@../../.claude/standards/testing-strategy.md`
│   │
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/api.ts   # Generated from backend schema
│   │   └── store/
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   │
│   └── package.json
│
├── backend/
│   ├── .claude/
│   │   └── CLAUDE.md
│   │       ## Backend Specifics
│   │       Framework: Express.js
│   │       Database: PostgreSQL + Prisma ORM
│   │       Queue: Redis + Bull
│   │       Cache: Redis
│   │
│   │       ## Standards
│   │       API: `@../../.claude/standards/api-standards.md`
│   │       Database: `@../../.claude/standards/db-schema.md`
│   │       See `@../../.claude/standards/` for all
│   │
│   ├── src/
│   │   ├── routes/
│   │   │   ├── auth.ts
│   │   │   ├── users.ts
│   │   │   └── posts.ts
│   │   ├── middleware/
│   │   ├── services/
│   │   ├── models/
│   │   └── utils/
│   │
│   ├── prisma/
│   │   ├── schema.prisma
│   │   └── migrations/
│   │
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── e2e/
│   │
│   └── package.json
│
├── infra/
│   ├── .claude/
│   │   └── CLAUDE.md
│   │       ## Infrastructure
│   │       Container runtime: Docker
│   │       Orchestration: Kubernetes
│   │       CI/CD: GitHub Actions
│   │       See `@../../.claude/standards/deployment.md`
│   │
│   ├── docker/
│   │   ├── Dockerfile.frontend
│   │   └── Dockerfile.backend
│   │
│   ├── k8s/
│   │   ├── frontend-deployment.yaml
│   │   ├── backend-deployment.yaml
│   │   ├── postgres-statefulset.yaml
│   │   └── redis-cache.yaml
│   │
│   └── github-actions/
│       ├── test.yaml
│       ├── build.yaml
│       └── deploy.yaml
│
└── docs/
    ├── architecture/
    │   ├── system-overview.md
    │   ├── api-design.md
    │   ├── database-design.md
    │   └── deployment-strategy.md
    │
    ├── workflows/
    │   ├── feature-development.md
    │   ├── api-contract-process.md
    │   ├── database-migrations.md
    │   └── deployment-process.md
    │
    └── onboarding/
        ├── backend-setup.md
        ├── frontend-setup.md
        ├── full-stack-first-task.md
        └── faq.md
```

---

## Checklist для внедрения

### Phase 1: Planning (День 1-2)

- [ ] Определить текущее состояние
  - [ ] Сколько проектов?
  - [ ] Сколько разработчиков?
  - [ ] Какие стандарты уже существуют?

- [ ] Определить structure
  - [ ] Монорепо vs несколько репо?
  - [ ] Какие shared component'ы?
  - [ ] Какие shared standards?

- [ ] Выбрать файлы для shared
  - [ ] Какие стандарты нужны?
  - [ ] Какие Skills?
  - [ ] Какие Agents?

### Phase 2: Structure (День 3-5)

- [ ] Создать .claude/ директорию в root
  ```bash
  mkdir -p .claude/{skills,agents,standards,references,team}
  ```

- [ ] Создать основной CLAUDE.md
  - [ ] Резюме проекта
  - [ ] Ссылки на детали
  - [ ] Краткие инструкции

- [ ] Создать settings.json
  - [ ] Enabled Skills
  - [ ] Enabled Agents
  - [ ] MCP servers (если нужны)

- [ ] Создать standards/
  - [ ] architecture.md
  - [ ] coding-standards.md
  - [ ] naming-conventions.md
  - [ ] testing-guidelines.md

### Phase 3: Implementation (Неделя 1-2)

- [ ] Мигрировать существующие инструкции
  - [ ] Найти старые CLAUDE.md
  - [ ] Консолидировать в shared standards
  - [ ] Обновить ссылки

- [ ] Создать первые Skills
  - [ ] Testing
  - [ ] Code review
  - [ ] Documentation

- [ ] Создать первые Agents
  - [ ] PR review
  - [ ] Deployment
  - [ ] Monitoring

- [ ] Документировать workflows
  - [ ] Feature development
  - [ ] Code review process
  - [ ] Deployment process
  - [ ] Incident response

### Phase 4: Team Adoption (Неделя 2-3)

- [ ] Провести presentation для команды
  - [ ] Объяснить structure
  - [ ] Показать примеры использования
  - [ ] Ответить на вопросы

- [ ] Коммитить в git
  - [ ] .claude/ directory
  - [ ] Обновить README
  - [ ] Добавить ссылку в wiki

- [ ] Обучение
  - [ ] Документировать общие use cases
  - [ ] Создать FAQ
  - [ ] Записать видео примеры

- [ ] Feedback loop (неделя 3)
  - [ ] Собрать feedback от команды
  - [ ] Улучшить документацию
  - [ ] Добавить missing standards

### Phase 5: Optimization (Месяц 1+)

- [ ] Мониторить использование
  - [ ] Какие Skills используются?
  - [ ] Какие standards нарушаются?
  - [ ] Где пробелы?

- [ ] Итеративно улучшать
  - [ ] Добавлять новые Skills
  - [ ] Расширять standards
  - [ ] Optimizing CLAUDE.md size

- [ ] Регулярные обновления
  - [ ] Quarterly reviews
  - [ ] Add new decisions
  - [ ] Remove obsolete content

---

## Лучшие практики & Ошибки

### ✅ DO (Делать)

✅ **Ссылайтесь на детали, не дублируйте**
```
Good: "See `@.claude/standards/architecture.md` for details"
Bad: "Our architecture is ... [full explanation]"
```

✅ **Разделите большие файлы**
```
Good: CLAUDE.md (ссылок) → standards/ (детали)
Bad: Все в одном CLAUDE.md файле (1000+ строк)
```

✅ **Используйте иерархию для specificity**
```
Good: root CLAUDE.md → package CLAUDE.md → local overrides
Bad: Одна конфигурация на все
```

✅ **Регулярно обновляйте standards**
```
Good: Встроить обновление standards в code review process
Bad: Standards "написаны один раз и забыты"
```

### ❌ DON'T (Не делать)

❌ **Не дублируйте инструкции в нескольких местах**
```
Bad:
- CLAUDE.md: "Use functional components"
- .claude/standards/coding-standards.md: "Use functional components"
- docs/: "Use functional components"

Good: CLAUDE.md ссылается на standards/coding-standards.md
```

❌ **Не создавайте углубленные ссылки (nested references)**
```
Bad: reference1.md → reference2.md → reference3.md
Claude может прочитать partial, потеряв контекст

Good: reference1.md, reference2.md, reference3.md
Все ссылаются из CLAUDE.md (один уровень)
```

❌ **Не смешивайте все in one CLAUDE.md**
```
Bad: CLAUDE.md с架構 + coding rules + API docs + примерами
Claude читает 50KB every session (много токенов)

Good: CLAUDE.md (300 строк) + separate files
```

❌ **Не используйте absolute paths**
```
Bad: "/home/user/project/.claude/standards.md"
Bad: "C:\Users\project\.claude\standards.md"

Good: "@.claude/standards.md"
Good: "@../shared/standards.md"
```

❌ **Не забывайте коммитить .claude/ в git**
```
Bad: .claude/ in .gitignore
→ Другие разработчики не получают standards

Good: .claude/ в git (except .local.* files)
```

---

## Инструменты & Интеграции

### Автоматизация синхронизации standards

```bash
#!/bin/bash
# sync-standards.sh — синхронизировать standards между проектами

SHARED_STANDARDS="./shared/.claude/standards"

for project in ./projects/*/; do
  echo "Syncing standards to $project"
  cp "$SHARED_STANDARDS"/*.md "$project/.claude/standards/"
done

echo "Running validation..."
# Опционально: проверить что все стандарты соответствуют
```

### GitHub Actions для validation

```yaml
# .github/workflows/claude-standards.yaml

name: Claude Standards Check

on: [pull_request]

jobs:
  check-standards:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate CLAUDE.md
        run: |
          # Check CLAUDE.md size < 500 lines
          lines=$(wc -l < .claude/CLAUDE.md)
          if [ $lines -gt 500 ]; then
            echo "ERROR: CLAUDE.md > 500 lines ($lines)"
            exit 1
          fi
          echo "✓ CLAUDE.md size OK"
      
      - name: Check references
        run: |
          # Ensure all @references exist
          grep -o "@[^[:space:]]*" .claude/CLAUDE.md | sort -u > /tmp/refs.txt
          while read ref; do
            path="${ref/@/.}"
            if [ ! -f "$path" ]; then
              echo "ERROR: Reference not found: $path"
              exit 1
            fi
          done < /tmp/refs.txt
          echo "✓ All references valid"
```

### IDE Integrations

**VS Code Extensions:**
- Claude Code (official)
- Better Comments (highlighting references)
- Markdown Preview Enhanced (для preview)

---

## Материалы для дальнейшего изучения

1. **Официальная документация Claude**
   - https://claude.com/docs (CLAUDE.md best practices)
   - https://code.claude.com/docs (Claude Code Skills)

2. **Гайды по架構**
   - "Using CLAUDE.md files" — Anthropic blog
   - "Claude Code Best Practices" — Anthropic Engineering

3. **Community примеры**
   - GitHub: awesome-claude-code
   - Reddit: r/ClaudeCode
   - Dev.to: Claude Code tutorials

4. **Свои опасности & решения**
   - Token optimization strategies
   - MCP implementation patterns
   - Monorepo scaling strategies

---

## Заключение

Эффективная **Shared Model** требует:

1. **Правильной структуры** — ясная иерархия файлов
2. **Оптимизации контекста** — ссылки вместо дублирования
3. **Team alignment** — регулярное обновление standards
4. **Итеративного улучшения** — feedback loop с командой
5. **Документации** — примеры использования Skills & Agents

Invest в setup сейчас = экономия времени + улучшение качества в долгосрочной перспективе.

---

**Версия:** 1.0  
**Дата:** 2025-01-06  
**Автор:** AI Research  
**Статус:** Production-ready
