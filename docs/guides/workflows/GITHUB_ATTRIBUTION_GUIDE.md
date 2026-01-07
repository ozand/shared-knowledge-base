# GitHub Agent Attribution - Implementation Guide

**Date:** 2026-01-06
**Pattern:** GITHUB-ATTRIB-001
**Purpose:** Make agents and projects visible in GitHub Issues and PRs

---

## 🎯 Проблема

**Сейчас:**
- GitHub показывает: `ozand opened this issue 2 hours ago`
- Нет информации о том, какой агент создал issue
- Нет информации о проекте-источнике
- attribution скрыто внизу issue body

**Хочется:**
- Сразу видеть: "Создано Claude Code из проекта PARSER"
- Фильтровать issues по агенту
- Фильтровать issues по проекту
- Отслеживать активность агентов

---

## ✅ Решение

### 4-слойная система атрибуции:

**Layer 1: "Created By" секция в ВЕРХНЕЙ части issue**
```markdown
---
**Created By:** 🤖 Claude Code (Sonnet 4.5)
**Project:** PARSER
**Agent Type:** Debugging
**Session:** session-abc123
**Date:** 2026-01-06
---
```

**Layer 2: GitHub Labels**
```bash
agent:claude-code
project:PARSER
agent-type:debugging
kb-improvement
python
```

**Layer 3: Детальная метадата**
```markdown
## Agent Metadata

**Agent:** Claude Code (Sonnet 4.5)
**Agent ID:** claude-sonnet-4-5-20251101
**Session:** session-abc123def456
**Project:** PARSER
**Project Type:** Python Web Scraping
```

**Layer 4: Формат комментариев**
```markdown
**_Comment by 🤖 Claude Code (PARSER project)_**
```

---

## 📝 Практическая реализация

### Вариант 1: Через GitHub Web UI

1. Создай issue
2. Добавь labels:
   - `agent:claude-code`
   - `project:PARSER`
   - `agent-type:code-generation`
3. В тело issue (САМОЕ ПЕРВОЕ):
```markdown
---
**Created By:** 🤖 Claude Code (Sonnet 4.5)
**Project:** PARSER
**Agent Type:** Code Generation
**Session:** <session-hash>
**Date:** 2026-01-06
---

# Add PYTHON-015: Async Timeout Error
```

### Вариант 2: Через GitHub CLI (Рекомендуется)

```bash
gh issue create \
  --label "agent:claude-code" \
  --label "project:PARSER" \
  --label "agent-type:debugging" \
  --label "kb-improvement" \
  --title "Add PYTHON-015: Async Timeout Error" \
  --body-file issue-template.md
```

**issue-template.md:**
```markdown
---
**Created By:** 🤖 Claude Code (Sonnet 4.5)
**Project:** PARSER
**Agent Type:** Debugging
**Session:** session-abc123
**Date:** 2026-01-06
---

## Proposed KB Entry
... (остальное содержимое)
```

---

## 🎨 Настройка Labels (One-time setup)

```bash
# Agent labels
gh label create "agent:claude-code" --color "0366d6" --description "Created by Claude Code agent"
gh label create "agent:cursor-ai" --color "fbca04" --description "Created by Cursor AI agent"
gh label create "agent:copilot" --color "1d76db" --description "Created by GitHub Copilot"
gh label create "agent:curator" --color "e99695" --description "Created by Shared KB Curator"

# Project labels (создавай по мере необходимости)
gh label create "project:PARSER" --color "d4c5f9" --description "From PARSER project"
gh label create "project:APARSER" --color "d4c5f9" --description "From AParser project"

# Agent type labels
gh label create "agent-type:code-generation" --color "5319e7" --description "Code generation task"
gh label create "agent-type:debugging" --color "5319e7" --description "Debugging task"
gh label create "agent-type:refactoring" --color "5319e7" --description "Refactoring task"
gh label create "agent-type:documentation" --color "5319e7" --description "Documentation task"
```

---

## 🔍 Фильтрация и Аналитика

**Фильтр по агенту:**
```bash
gh issue list --label "agent:claude-code" --state all
```

**Фильтр по проекту:**
```bash
gh issue list --label "project:PARSER" --state all
```

**Фильтр по типу агента:**
```bash
gh issue list --label "agent-type:debugging" --state all
```

**Комбинированный фильтр:**
```bash
gh issue list --label "agent:claude-code" --label "project:PARSER" --state all
```

**Активность агента:**
```bash
gh issue list --state all --json agent,labels,createdAt | \
  jq -r '.[] | "\(.labels[]) - \(.createdAt)"' | \
  grep "agent:" | sort | uniq -c
```

---

## 📊 Пример

**ДО (без атрибуции):**
```
GitHub UI: ozand opened this issue 2 hours ago

Тело issue:
## Proposed KB Entry
... (много текста) ...
Created by: Project Agent (PARSER)  [в самом низу]
```

**ПОСЛЕ (с атрибуцией):**
```
GitHub UI: ozand opened this issue 2 hours ago

Labels: agent:claude-code, project:PARSER, agent-type:debugging

Тело issue (ПЕРВАЯ СТРОКА):
---
**Created By:** 🤖 Claude Code (Sonnet 4.5)
**Project:** PARSER
**Agent Type:** Debugging
**Session:** session-abc123
**Date:** 2026-01-06
---

## Proposed KB Entry
...
```

**Результат:**
- ✅ Агент виден сразу (первая строка issue)
- ✅ Labels видны в списке issues
- ✅ Можно фильтровать по агенту/проекту
- ✅ Можно отслеживать активность

---

## 🚀 Для Agents (Интеграция в промпты)

**Добавьте в систему промпт агента:**

```
When creating GitHub Issues or PRs:

1. ALWAYS add "Created By" section at VERY TOP of body:
   ---
   **Created By:** 🤖 {{your_agent_name}}
   **Project:** {{project_name}}
   **Agent Type:** {{task_type}}
   **Date:** {{date}}
   ---

2. ALWAYS add these labels:
   - agent:{{agent_slug}} (claude-code, cursor-ai, copilot, curator)
   - project:{{project_slug}} (PARSER, AParser, etc.)
   - agent-type:{{type}} (code-generation, debugging, refactoring, documentation)

3. Use GitHub CLI if possible:
   gh issue create --label "agent:claude-code" --label "project:PARSER" ...

This makes agent attribution visible and filterable!
```

---

## 📋 Checklist для создания Issue

- [ ] "Created By" секция в САМОМ НАЧАЛЕ issue body
- [ ] 🤖 emoji для агента
- [ ] Указано название проекта
- [ ] Указан тип агента (code-generation, debugging, etc.)
- [ ] Добавлен label: agent:claude-code
- [ ] Добавлен label: project:PROJECT_NAME
- [ ] Добавлен label: agent-type:TYPE
- [ ] (Опционально) Session hash для отслеживания

---

## 📚 Связанные паттерны

- **GITHUB-ATTRIB-001:** GitHub Agent and Project Attribution
- **AGENT-HANDOFF-001:** Cross-Repository Agent Collaboration (обновлен)
- **AGENT-ACCOUNTABILITY-001:** Agent Self-Accountability

---

**Дата:** 2026-01-06
**Паттерн:** GITHUB-ATTRIB-001
**Статус:** ✅ Ready to use
