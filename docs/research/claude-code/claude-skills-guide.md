# Claude Code SKILLS: Полное руководство по лучшим практикам
## Архитектура, дизайн и реальные примеры для production

---

## Оглавление

1. [Фундаментальные концепции](#фундаментальные-концепции)
2. [Архитектура Skills системы](#архитектура-skills-системы)
3. [Дизайн и структура SKILL.md](#дизайн-и-структура-skillmd)
4. [Процесс разработки Skills](#процесс-разработки-skills)
5. [Практические паттерны](#практические-паттерны)
6. [Testing и валидация](#testing-и-валидация)
7. [Performance & Optimization](#performance--optimization)
8. [Типичные ошибки (Anti-patterns)](#типичные-ошибки-anti-patterns)
9. [Примеры из реальных проектов](#примеры-из-реальных-проектов)
10. [Checklist для production](#checklist-для-production)

---

## Фундаментальные концепции

### Что такое Skills?

**Skills** — это переиспользуемые единицы знания и инструкций, которые Claude загружает **на demand** для выполнения специфичных задач. Ключевая особенность: они не вызываются явно (как команды), а **автоматически обнаруживаются и загружаются** Claude когда он понимает, что они релевантны.

### Как Skills отличаются от других инструментов?

```
┌─────────────────────────────────────────────────────────┐
│  SKILLS vs Projects vs MCP vs Prompts                  │
└─────────────────────────────────────────────────────────┘

SKILLS
├─ Что это: Процедурные знания ("как делать")
├─ Область: Переиспользуемые workflow'ы
├─ Видимость: Portable (работает везде)
├─ Загрузка: На demand (только при необходимости)
├─ Жизненный цикл: Persistent (проживают боевые сессии)
└─ Когда использовать: Повторяющиеся задачи

PROJECTS
├─ Что это: Контекстное знание ("что нужно знать")
├─ Область: Специфичный проект/задача
├─ Видимость: Локально для этого проекта
├─ Загрузка: Всегда (полная загрузка в контекст)
├─ Жизненный цикл: Persistent (в рамках проекта)
└─ Когда использовать: Долгосрочные проекты

MCP
├─ Что это: Интеграция с инструментами ("где найти")
├─ Область: Доступ к данным и сервисам
├─ Видимость: Как API/инструмент
├─ Загрузка: Инициализируется на старте
├─ Жизненный цикл: Рантайм-зависимый
└─ Когда использовать: Внешние данные и сервисы

PROMPTS
├─ Что это: One-time инструкции ("сделай сейчас")
├─ Область: Текущая конверсация
├─ Видимость: Локально для этого сообщения
├─ Загрузка: Inline с запросом
├─ Жизненный цикл: Ephemeral (забывается после)
└─ Когда использовать: Немедленные, специфичные задачи

═══════════════════════════════════════════════════════════

ПРАВИЛО: Skills + Projects + MCP + Prompts работают ВМЕСТЕ
Пример:
  1. Project загружает контекст о компании
  2. Skill учит Claude как анализировать рынок
  3. MCP подает данные о конкурентах
  4. Prompt уточняет: "Фокусируйся на healthcare"
```

### Автоматическое обнаружение и загрузка

Skills используют **progressive disclosure** (прогрессивное раскрытие информации):

```
Уровень 1: Metadata (ВСЕГДА загружена)
├─ name: "testing-skill"
├─ description: "Generates unit tests with 80%+ coverage..."
└─ Размер: ~30-50 токенов per skill

Уровень 2: Instructions (загружена когда TRIGGERED)
├─ Основные инструкции (200-500 строк)
├─ Примеры использования
└─ Размер: ~500-2000 токенов

Уровень 3: Resources (загружены ПО ТРЕБОВАНИЮ)
├─ reference.md (детальная информация)
├─ examples.md (полные примеры)
├─ templates/ (шаблоны)
├─ scripts/ (исполняемые скрипты)
└─ Размер: зависит от использования

═══════════════════════════════════════════════════════════

КЛЮЧЕВОЕ ПОНИМАНИЕ:
  Когда Claude Code стартует, загружаются ТОЛЬКО
  metadata (~50 токенов за skill).
  
  Полная инструкция загружается ТОЛЬКО если Claude
  решит что skill релевантна.
  
  Файлы из resources/ загружаются только когда
  Claude их явно читает.
  
  → Результат: Огромная экономия токенов!
```

### Как Claude решает КОГДА использовать Skill?

```
User: "Generate unit tests for this API handler"
                ↓
Claude получает запрос + список всех Skills с описаниями
                ↓
Claude анализирует: 
  - "testing-skill" с description: 
    "Generates unit tests matching project patterns"
    → Матчится! (пользователь просит тесты)
                ↓
Claude ЗАГРУЖАЕТ полный текст testing-skill SKILL.md
                ↓
SKILL.md содержит:
  1. Инструкции как генерировать тесты
  2. Паттерны из проекта (@resources/test-patterns.md)
  3. Примеры
  4. Ссылки на tools (Grep, Read, Write)
                ↓
Claude выполняет skill используя эти инструкции
                ↓
Result: Тесты сгенерированы по паттернам проекта

═══════════════════════════════════════════════════════════

ВНИМАНИЕ: Описание (description) — САМОЕ ВАЖНОЕ!
Если описание неясное → Skill не загружается когда нужно
Если описание слишком общее → Skill загружается ВЕЗДЕ
```

---

## Архитектура Skills системы

### Структура файлов

```
.claude/
├── CLAUDE.md                          ← Главная навигация
├── settings.json                      ← Что Skills enabled
└── skills/                            ← Хранилище Skills
    ├── testing/
    │   ├── SKILL.md                   ← Метаданные + инструкции
    │   ├── resources/
    │   │   ├── patterns.md            ← Test patterns
    │   │   ├── examples.md            ← Full examples
    │   │   └── assertions.md          ← Common assertions
    │   └── scripts/
    │       └── generate_tests.py      ← Optional automation
    │
    ├── code-review/
    │   ├── SKILL.md
    │   ├── resources/
    │   │   ├── checklist.md
    │   │   └── rules/
    │   │       ├── architecture.md
    │   │       ├── performance.md
    │   │       └── security.md
    │   └── scripts/
    │
    ├── documentation/
    │   ├── SKILL.md
    │   ├── resources/
    │   │   ├── templates/
    │   │   └── examples/
    │   └── scripts/
    │
    └── refactoring/
        ├── SKILL.md
        └── resources/
            └── patterns/

Total size guidelines:
- .claude/skills/ : 50-500 MB (все Skills вместе)
- Один skill: 1-50 MB (обычно 100KB-5MB)
- SKILL.md: 200-500 строк (максимум!)
- resource файлы: 100-2000 строк (OK)
```

### Иерархия Skills в разных контекстах

```
Global Skills (~/.claude/skills/)
├─ Доступны во ВСЕХ проектах
├─ Личные Skills разработчика
├─ Примеры: Personal coding style, Brand guidelines
└─ Загружаются для всех сессий

Project Skills (.claude/skills/ в репо)
├─ Доступны ТОЛЬКО в этом проекте
├─ Разделяются со всей командой
├─ Примеры: Test generation, Code review rules
└─ Наследуются всеми разработчиками

Package Skills (packages/*/claude/skills/)
├─ Доступны для этого package
├─ Специфичны для пакета
└─ Наследуют project-level skills

Scope resolution (как с CLAUDE.md):
Local (.local) → Package → Project → Global → (none)
```

### Как Skills загружаются (Discovery & Loading)

```
PHASE 1: Startup (~100ms)
┌──────────────────────────────────────┐
│ Claude Code инициализируется         │
│ 1. Сканирует ~/.claude/skills/       │
│ 2. Сканирует .claude/skills/         │
│ 3. Сканирует packages/*/claude/skills│
│ 4. Читает settings.json (enabled?)   │
│ 5. Собирает metadata (name + desc)   │
│ 6. Встраивает в System Prompt        │
└──────────────────────────────────────┘

PHASE 2: User Request (Per-message)
┌──────────────────────────────────────┐
│ Пользователь: "Generate tests"       │
│ 1. Claude получает request           │
│ 2. Claude видит testing-skill в list │
│ 3. Claude решает: "Это релевантно"   │
│ 4. Загружает FULL текст SKILL.md     │
│ 5. Загружает @resources/ файлы       │
│ 6. Выполняет skill                   │
└──────────────────────────────────────┘

PHASE 3: Execution (Variable length)
┌──────────────────────────────────────┐
│ Skill выполняется с tools:           │
│ - Может читать файлы (Read)          │
│ - Может писать файлы (Write)         │
│ - Может искать (Grep)                │
│ - Может выполнять скрипты (Execute)  │
│ - Может вызывать МCP                 │
│ 6. Возвращает результаты             │
└──────────────────────────────────────┘
```

---

## Дизайн и структура SKILL.md

### YAML Frontmatter (обязательно!)

```yaml
---
name: testing-skill
description: |
  Generates unit tests matching project patterns.
  
  Triggers when:
  - User asks for "test", "write tests", "add coverage"
  - Testing is part of code review workflow
  - Part of deployment validation
  
  Outputs complete test files with examples,
  edge cases, and assertions following project standards.

version: 1.0.0
created: 2025-01-06

# OPTIONAL metadata:
keywords: ["testing", "vitest", "coverage"]
author: "engineering-team"
---
```

**Правила для YAML:**
- `name`: Lowercase, kebab-case, ≤64 chars, уникален
- `description`: Плаинтекст (не markdown), ≤1024 chars
  - **КРИТИЧНО**: Должна точно описывать КОГДА использовать
  - **ПЛОХО**: "Testing skill" (слишком общая)
  - **ХОРОШО**: "Generates unit tests for functions using Vitest, matching project coverage targets and assertion patterns"
- Используйте bullet points в description (помогает Claude)

### Структура основного контента

```markdown
---
name: testing-skill
description: Generates unit tests...
---

# Skill Title

## When to Use This Skill
- User asks to "write tests", "generate tests", "test this"
- Testing is part of code review workflow
- User wants to increase code coverage
- Part of deployment checklist

## What This Skill Does
1. Analyzes function signatures and logic
2. Identifies edge cases and error scenarios
3. Generates test file matching project patterns
4. Includes examples and assertions
5. Achieves 80%+ code coverage

## Key Instructions

### Step 1: Analyze Target Code
- Read the file user wants to test
- Identify function signatures
- Note any external dependencies
- See @resources/test-patterns.md for patterns

### Step 2: Generate Test File
- Use test template from @resources/template.ts
- Follow assertion style from @resources/assertions.md
- See full examples: @resources/examples/
- Match indentation and naming conventions

### Step 3: Validate Coverage
```bash
npx vitest --coverage
```
- Target: 80%+ coverage
- Review uncovered lines
- If <80%: add missing edge case tests

## Common Patterns

### Pattern: Testing Error Handling
```typescript
describe("error handling", () => {
  it("throws when input is invalid", () => {
    expect(() => fn(null)).toThrow();
  });
});
```
See @resources/patterns-errors.md for more patterns.

### Pattern: Async Testing
[Similar structure...]

## Tools Used
- **Read**: Read source files and patterns
- **Write**: Create test files
- **Execute**: Run tests and coverage

## Important Notes
- Tests are in __tests__/ directory
- Never modify production code for testing
- Always run coverage check before commit
- Refer to project CLAUDE.md for more context: @../../CLAUDE.md

## Examples
See @resources/examples/ for complete examples of:
- Unit tests for React components
- API endpoint tests
- Database integration tests
- Error handling tests
```

### Размер и организация

```
RULE: SKILL.md должен быть ≤500 строк (обычно 200-400)

Если SKILL.md становится больше → SPLIT НА ЧАСТИ:

SKILL.md (300 строк)
├─ Основные инструкции
├─ Ссылки на @resources/
└─ Примеры (краткие, 1-2 на каждый паттерн)

resources/
├─ patterns.md (200 строк) — Полное описание паттернов
├─ examples/
│  ├─ simple.ts (50 строк)
│  ├─ complex.ts (150 строк)
│  └─ README.md (описание каждого примера)
├─ assertions.md (100 строк) — Все типы assertions
├─ template.ts (30 строк) — Шаблон нового теста
└─ edge-cases.md (150 строк) — Как тестировать edge cases

ВАЖНО: Все @ссылки в SKILL.md указывают ВНУТРИ skill директории
НЕПРАВИЛЬНО: @../../../standards/testing.md (идет вверх!)
ПРАВИЛЬНО: @resources/patterns.md или @./resources/patterns.md
```

---

## Процесс разработки Skills

### Phase 1: Discovery — Что это вообще такое?

**Начните с наблюдения**, а не с предположений:

```
1. Работайте над задачей БЕЗ Skill
   - Используйте обычный prompt Claude
   - Заметьте что вы повторяете
   
2. Выпишите паттерны
   - "Я всегда объясняю тестирование"
   - "Я копирую одни и те же примеры"
   - "Я переписываю одни и те же rules"
   
3. Оцените: "Будет ли это использоваться повторно?"
   - YES → Candidate для skill
   - NO → Просто оставьте как prompt

ТЕСТ: Если вы используете одинаковый контекст >3 раз → Skill time!
```

### Phase 2: Evaluation-Driven Development (EDDDF)

**КРИТИЧНОЕ отличие**: Сначала пишите tests, потом skill!

```
TRADITIONAL (Неправильно):
1. Пишите большую SKILL.md с предположениями
2. Проверяете если это работает
3. Много итераций на переписывание

EVALUATION-DRIVEN (Правильно):
1. Определяете GAP (где Claude fails без skill)
2. Пишите 3 evaluation scenarios
3. Базовый score (без skill)
4. Пишите MINIMAL skill (только для closing gap)
5. Итерируете на основе observations
```

**Пример с Testing Skill:**

```
STEP 1: Define the Gap
"When I ask Claude to write tests without context,
they don't follow our patterns:
- Wrong assertion style (Mocha vs Vitest)
- Missing edge case testing
- Coverage too low (40% vs needed 80%)"

STEP 2: Create Evaluations
Eval 1: "Generate tests for login function"
├─ Metrics:
│  ├─ Uses Vitest describe/it syntax? Y/N
│  ├─ Covers error cases? Y/N
│  ├─ Achieves 80%+ coverage? Y/N
│  └─ Matches project patterns? Y/N
├─ Baseline (without skill): 1/4 ✗
└─ Target: 4/4 ✓

Eval 2: "Generate tests for async API call"
├─ Metrics:
│  ├─ Uses async/await correctly? Y/N
│  ├─ Tests both success and error? Y/N
│  ├─ Mocks dependencies properly? Y/N
│  └─ Has timeout handling? Y/N
├─ Baseline (without skill): 2/4 ✗
└─ Target: 4/4 ✓

Eval 3: "Generate tests for React component"
├─ Metrics:
│  ├─ Uses React Testing Library? Y/N
│  ├─ Tests user interactions? Y/N
│  ├─ Covers accessibility? Y/N
│  └─ No implementation details tested? Y/N
├─ Baseline (without skill): 1/4 ✗
└─ Target: 4/4 ✓

STEP 3: Write Minimal Skill
(Only the MINIMUM to close these gaps)

## When to Use This Skill
- Generating unit tests
- Need Vitest patterns
- Must achieve 80%+ coverage

## Key Instructions
1. Analyze function
2. Use Vitest describe/it pattern
3. Cover error cases and edge cases
4. Check coverage meets 80%

(That's it! No more.)

STEP 4: Test with Claude B (Fresh instance with skill loaded)
Run Eval 1, 2, 3 → Score each

STEP 5: Observe and Iterate
If Eval 1 score = 4/4: ✓ Skill works for basic tests
If Eval 2 score = 2/4: ✗ Need to improve async handling
  → Update SKILL.md with async patterns

If Eval 3 score = 3/4: △ Missing accessibility aspect
  → Add accessibility testing section
```

### Phase 3: Iterative Refinement

**Pattern: Claude A (Builder) ↔ Claude B (Tester)**

```
ITERATION CYCLE:

1. Claude B uses skill on real task
   → "Generate tests for login API"

2. You observe Claude B's output
   → "Good, but forgot to test rate limiting"

3. You return to Claude A (builder)
   → "I noticed Claude forgot rate limiting.
      Should we add that to skill?"

4. Claude A refines SKILL.md
   → Adds rate limiting section

5. Back to Claude B with updated skill
   → Test again: "Generate tests for login API"
   → Better! Now includes rate limiting

6. Repeat until observations show skill works well

═════════════════════════════════════════════════════════════

KEY INSIGHT:
Never write a skill in isolation.
Always iterate on REAL usage with Claude B.
Your observations → Claude A improvements.
```

### Phase 4: Team Feedback & Governance

```
Before deploying skill to team:

1. Code Review
   - Minimum 2 approvals on SKILL.md
   - Check for security issues
   - Validate tool permissions

2. Documentation
   - Update CLAUDE.md with skill reference
   - Document when/why to use
   - Link to resources/examples

3. Testing
   - Run evaluations again with team perspective
   - Gather feedback from 2-3 team members
   - Iterate based on feedback

4. Publishing
   - Add to settings.json enabled list
   - Communicate in team channel
   - Create "how to use" guide if complex

5. Maintenance
   - Monitor usage (Claude will show when it triggers)
   - Quarterly reviews
   - Update based on feedback
```

---

## Практические паттерны

### Паттерн 1: Markdown-only (Simple)

**Когда использовать**: Инструкции, гайдлайны, форматирование

```markdown
---
name: brand-guidelines-skill
description: |
  Formats content following company brand guidelines.
  Applies tone, style, visual elements to documents.
---

# Brand Guidelines Skill

## When to Use
- Creating marketing materials
- Writing copy for external audience
- Formatting brand-aligned documents

## Key Guidelines

### Tone
- Professional yet approachable
- No jargon without explanation
- Active voice preferred

### Visual Style
- Headings: Title Case, Blue (#0066CC)
- Lists: Bullet points for features
- Emphasis: Bold for key terms

## Formatting Rules
1. Headers use ### (h3 minimum)
2. Lists have bullets or numbers
3. Links in Markdown format [text](url)
4. Images use ![alt](path) syntax

## Common Sections
See @resources/templates/ for complete templates:
- @resources/templates/article.md
- @resources/templates/product-page.md
- @resources/templates/email.md
```

**Плюсы:**
- ✅ Быстро написать
- ✅ Легко обновлять
- ✅ Нет зависимостей
- ✅ Работает везде

**Минусы:**
- ❌ Не автоматизирует сложные операции
- ❌ Зависит от Claude compliance

---

### Паттерн 2: Script Automation (Complex)

**Когда использовать**: Детерминированные операции, требующие вычислений

```markdown
---
name: csv-analyzer-skill
description: |
  Analyzes CSV files: generates statistics, identifies
  patterns, creates visualizations. Handles large files
  (10K+ rows) efficiently.
---

# CSV Analyzer Skill

## What This Skill Does
1. Reads CSV file using Python
2. Generates descriptive statistics
3. Creates summary report
4. Produces visualizations (if requested)

## How to Use
```bash
User: "Analyze this customer data"
Claude: Runs analyze_csv.py
Result: Summary + charts
```

## Step-by-Step Instructions

### 1. Validate Input
```bash
python scripts/validate_csv.py "$FILE_PATH"
```

If validation fails, inform user and ask for correction.

### 2. Generate Statistics
```bash
python scripts/generate_stats.py "$FILE_PATH" --format json
```

Output format: JSON with:
```json
{
  "row_count": 10000,
  "columns": ["name", "email", "signup_date"],
  "missing_values": { "email": 5 },
  "data_types": { "signup_date": "datetime" }
}
```

### 3. Create Report
Parse JSON statistics and create human-readable report:
```markdown
# CSV Analysis Report

## Overview
- Rows: 10,000
- Columns: 3
- Missing values: 5 (0.05%)

## Column Analysis
- **name**: Text, no missing values
- **email**: Text, 5 missing values
- **signup_date**: DateTime, complete
```

### 4. Optional: Generate Visualizations
If user asks for charts, use Matplotlib:
```bash
python scripts/visualize.py \
  --input "$FILE_PATH" \
  --output report.png \
  --type histogram
```

## Important Notes
- Max file size: 500MB (streams larger files)
- Script handles UTF-8 encoding issues
- Missing values are noted but don't fail analysis
- Error handling: See error messages in console output

## Tools Required
- **Read**: For input CSV files
- **Execute**: Python script execution
- **Write**: For output report/charts
```

**Плюсы:**
- ✅ Автоматизирует скучные операции
- ✅ Обрабатывает большие файлы эффективно
- ✅ Детерминированные результаты

**Минусы:**
- ❌ Зависимости должны быть установлены
- ❌ Сложнее дебажить
- ❌ Требует error handling

---

### Паттерн 3: Search-Analyze-Report

**Когда использовать**: Поиск по кодовой базе, анализ, отчеты

```markdown
---
name: security-audit-skill
description: |
  Audits codebase for common security issues:
  SQL injection risks, hardcoded secrets, unsafe
  deserialization. Generates comprehensive report.
---

# Security Audit Skill

## What This Skill Does
1. Search codebase for security patterns
2. Analyze each finding for severity
3. Generate detailed audit report

## Step-by-Step

### 1. Search for Vulnerability Patterns

```bash
# SQL Injection risks
grep -rn "SELECT.*\$" src/ > /tmp/sql_risks.txt

# Hardcoded secrets
grep -rn "(password|api_key|secret)" src/ > /tmp/secrets.txt

# Unsafe deserialization
grep -rn "pickle\|eval\|exec" src/ > /tmp/unsafe.txt
```

### 2. Analyze Each Finding

For each grep match:
1. Read the file around the match
2. Assess severity: CRITICAL, HIGH, MEDIUM, LOW
3. Note the risk type
4. Suggest mitigation

Example analysis:
```python
# File: src/api.py, Line 42
query = f"SELECT * FROM users WHERE id = {user_id}"

Risk: HIGH (SQL Injection)
Issue: User input directly in SQL query
Mitigation: Use parameterized queries

Before:
  query = f"SELECT * FROM users WHERE id = {user_id}"

After:
  cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### 3. Generate Report

Create report.md with:
- Executive summary
- Grouped by severity (CRITICAL first)
- Each finding with code snippet + fix
- Recommendations

```markdown
# Security Audit Report

## Executive Summary
- Total Issues: 12
- CRITICAL: 1 (SQL Injection)
- HIGH: 3 (Hardcoded secrets)
- MEDIUM: 5 (Missing validation)
- LOW: 3 (Code quality)

## CRITICAL Issues

### 1. SQL Injection in user lookup
**File**: src/api.py:42
**Risk**: Attackers can manipulate database queries
**Code**:
\`\`\`python
query = f"SELECT * FROM users WHERE id = {user_id}"
\`\`\`
**Fix**: Use parameterized queries
\`\`\`python
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
\`\`\`

[Similar for other issues...]

## Recommendations
1. Immediately fix CRITICAL issues
2. Create tickets for HIGH issues
3. Code review process for security
```

## Tools Required
- **Grep**: Find vulnerable patterns
- **Read**: Read and analyze matches
- **Write**: Generate final report
```

**Плюсы:**
- ✅ Масштабируемо (работает на 1M+ строк кода)
- ✅ Составной (search + analyze + report)
- ✅ Информативно

**Минусы:**
- ❌ Может быть шумно (false positives)
- ❌ Требует post-processing
- ❌ Зависит от хороших паттернов поиска

---

## Testing и валидация

### Evaluation-Driven Development (повторение важное!)

```
ПЕРЕД написанием skills:

1. Определите GAP
   "Где Claude fails без этого skill?"

2. Создайте 3 evaluation scenarios
   Eval 1: Базовый случай
   Eval 2: Средний случай
   Eval 3: Сложный случай

3. Запустите базовую оценку (без skill)
   baseline = score('test 1') + score('test 2') + score('test 3')

4. Пишите МИНИМАЛЬНЫЙ skill
   Только что нужно для закрытия gap

5. Используйте с Claude B (fresh instance)
   Run evaluations → Получите новые scores

6. Сравните: baseline vs с skill
   improvement = new_score - baseline_score

7. Итерируйте на основе failures
```

### Testing Checklist

```
SKILL Development:
- [ ] Created 3 evaluation scenarios
- [ ] Ran baseline (without skill)
- [ ] SKILL.md is ≤500 lines
- [ ] Description is clear and specific
- [ ] All @references to resources are valid
- [ ] Tested with fresh Claude instance
- [ ] Iteratively improved based on observations

SKILL Content:
- [ ] YAML frontmatter is valid
- [ ] Name is lowercase, kebab-case
- [ ] Description explains when to use
- [ ] Instructions are clear and sequential
- [ ] Examples are concise but complete
- [ ] All required tools are documented
- [ ] Error cases are handled

TEAM READINESS:
- [ ] Code reviewed (2+ approvals)
- [ ] Security team reviewed (if needed)
- [ ] Added to settings.json
- [ ] Documented in CLAUDE.md
- [ ] Shared with team
- [ ] Team feedback incorporated
```

### Common Testing Mistakes

```
❌ MISTAKE 1: Testing in isolation
   "Does skill work theoretically?"
   
✅ SOLUTION: Test with REAL USAGE
   "Does skill work when Claude naturally uses it?"

───────────────────────────────────────────

❌ MISTAKE 2: Assuming skill will trigger
   "I built a great testing skill"
   
✅ SOLUTION: Verify trigger conditions
   Ask Claude: "Did you use testing-skill?"
   If NO → Description needs work

───────────────────────────────────────────

❌ MISTAKE 3: Over-engineering
   "Let me add every possible testing pattern"
   
✅ SOLUTION: Minimal viable skill
   Add ONLY what's needed for gap closure
   Expand based on REAL feedback

───────────────────────────────────────────

❌ MISTAKE 4: Not handling errors
   Script fails and Claude doesn't know why
   
✅ SOLUTION: Explicit error handling
   Script SHOULD NOT crash
   Should return helpful error messages
```

---

## Performance & Optimization

### Token Usage

```
Breakdown when using Skills:

Session Start:
├─ Each skill metadata (name + description): 30-50 tokens
├─ Total with 5 skills: ~200 tokens
├─ IMPORTANT: These are ALWAYS loaded
└─ → Keep descriptions concise!

When Skill Triggers:
├─ Full SKILL.md content: 500-2000 tokens
├─ Referenced resources: loaded on demand
├─ Scripts: NOT counted (executed, not as tokens)
└─ → Only loaded when skill is used!

Total Cost Example:
1. Session start with 10 skills: +300 tokens
2. Trigger testing skill: +1200 tokens
3. Reference patterns.md: +400 tokens
4. Run script: +0 tokens (executed, not tokens)
────────────────────────────────
Total: ~1900 tokens (reasonable!)

WITHOUT skill (using only prompts):
└─ Each request: Re-explain testing requirements
└─ ~2000 tokens EVERY TIME
└─ Over 10 requests: 20,000 tokens!

SAVINGS: Skills save tokens on repeated usage!
```

### Optimization Strategies

```
1. Keep SKILL.md ≤500 lines
   - Move detailed content to resources/
   - Use @references
   - Keep examples minimal (1-2 per pattern)

2. Break large content across files
   SKILL.md (300 lines - core)
   └─ resources/
      ├─ patterns.md (200 lines)
      ├─ examples/ (folder)
      └─ templates/ (folder)
      
3. Use specific descriptions
   - Vague: "Code review"
   - Specific: "Reviews PRs for security and performance issues"
   - Result: Only triggers when appropriate

4. Avoid dependency bloat
   - Don't require 10 packages if 1 works
   - Shell scripts > Python for simple tasks
   - Use built-in tools (Grep, Read, Write)

5. Cache expensive operations
   - If analyzing large codebase: save results
   - Reuse between requests
   - Example: Save security audit findings

6. Consolidate related skills
   DON'T: 10 micro-skills
   DO: 3-5 well-designed skills
   
   ✅ one-testing-skill (all test patterns)
   ❌ unit-test-skill, e2e-skill, integration-test-skill...
```

### Размеры файлов (рекомендации)

```
Целевые размеры:

SKILL.md:              200-500 lines
resources/patterns.md: 100-500 lines
resources/examples/:   1-20 files, 20-200 lines каждый
scripts/:              1-10 files, 50-500 lines каждый
resources/:            Total ≤5MB per skill

Full skill folder:     Typical 500KB-5MB
All skills together:   Typical 10-100MB

Если skill > 10MB → Слишком большой, рефакторите!
```

---

## Типичные ошибки (Anti-patterns)

### ❌ Anti-pattern 1: Слишком общее описание

```
BAD:
---
name: testing-skill
description: "Helps with testing"
---

Проблема:
- Claude не понимает КОГДА использовать
- Может срабатывать на неправильные запросы
- Не найдёт skill когда нужно

GOOD:
---
name: testing-skill
description: |
  Generates unit tests with 80%+ coverage using Vitest.
  
  Triggers when:
  - User asks to "write tests" or "generate tests"
  - Testing function or component
  - Part of code review process
  
  Outputs complete test files with edge cases,
  error handling, and assertions following
  project-specific Vitest patterns.
---

Почему better:
- Ясно когда использовать
- Claude найдёт когда уместно
- Конкретные выходные данные
```

### ❌ Anti-pattern 2: SKILL.md слишком большой

```
BAD:
---
name: testing-skill
---
# Testing Skill

[2000 строк всего контента inline]
- Все паттерны
- Все примеры
- Все документация
- Все шаблоны

Проблема:
- Claude загружает ВСЕ при каждом использовании
- Много токенов потрачено
- Трудно обновлять

GOOD:
---
name: testing-skill
---
# Testing Skill

[300 строк основного контента]
- Когда использовать
- Основные инструкции
- Ссылки на детали: @resources/patterns.md
- Ссылки на примеры: @resources/examples/
- Ссылки на шаблоны: @resources/template.ts

resources/
├─ patterns.md (все паттерны)
├─ examples/ (примеры)
└─ template.ts (шаблон)

Почему better:
- SKILL.md 300 строк (быстро загружается)
- Детальное содержание загружается on-demand
- Легче обновлять отдельные части
```

### ❌ Anti-pattern 3: Слишком много micro-skills

```
BAD:
~/.claude/skills/
├─ unit-test-skill/
├─ integration-test-skill/
├─ e2e-test-skill/
├─ snapshot-test-skill/
├─ performance-test-skill/
└─ ... (10 skills для одной темы)

Проблема:
- Claude путается между ними
- Может не найти нужный
- Много metadata в памяти (300+ токенов)
- Сложно управлять

GOOD:
~/.claude/skills/
├─ testing-skill/
│  ├─ SKILL.md (основное)
│  └─ resources/
│     ├─ patterns-unit.md
│     ├─ patterns-integration.md
│     ├─ patterns-e2e.md
│     ├─ patterns-performance.md
│     └─ examples/

Почему better:
- Одна clearly defined skill
- Claude легче выбирать
- Меньше metadata overhead
- Проще обновлять все вместе
```

### ❌ Anti-pattern 4: Scripts без обработки ошибок

```
BAD:
def analyze_csv(path):
    # Если файл не существует → crash!
    df = pd.read_csv(path)
    return df.describe()

Проблема:
- Script падает
- Claude не знает почему
- Плохой пользовательский опыт

GOOD:
def analyze_csv(path):
    try:
        if not os.path.exists(path):
            print(f"ERROR: File not found: {path}")
            return None
        
        df = pd.read_csv(path)
        if df.empty:
            print(f"ERROR: CSV is empty: {path}")
            return None
        
        return df.describe()
    
    except Exception as e:
        print(f"ERROR: Failed to analyze CSV: {e}")
        return None

Почему better:
- Graceful degradation
- Helpful error messages
- Claude может отреагировать правильно
```

### ❌ Anti-pattern 5: Глубокие nested references

```
BAD:
SKILL.md
  └─ @resources/main.md
      └─ @../standards/testing.md
          └─ @../../team/guidelines.md
              └─ @../../../../best-practices.md

Проблема:
- Claude может потерять контекст
- Файлы не найдены (неправильные пути)
- Сложно отследить

GOOD:
SKILL.md
  ├─ @resources/patterns.md (direct)
  ├─ @resources/examples.md (direct)
  ├─ @resources/assertions.md (direct)
  └─ Reference: @../../CLAUDE.md (project level)

Почему better:
- Максимум 1 уровень вверх от skill/
- Все resources в одной директории
- Ясная структура
```

---

## Примеры из реальных проектов

### Пример 1: Testing Skill для React компонентов

(Минимизированный пример)

```markdown
---
name: react-testing-skill
description: |
  Generates tests for React components using React Testing Library.
  Covers user interactions, accessibility, and edge cases.
  Achieves 80%+ coverage with RTL best practices.
---

# React Testing Skill

## When to Use
- User asks: "Test this component", "Generate tests for Button"
- Need React Testing Library patterns
- Must verify accessibility

## Quick Start

```typescript
import { render, screen } from '@testing-library/react';
import Button from './Button';

describe('Button', () => {
  it('renders with label', () => {
    render(<Button label="Click me" />);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });
});
```

## Key Principles
1. Query by user-facing attributes (role, label)
2. NOT implementation details (class names, state)
3. Test BEHAVIOR not internals
4. Always include accessibility tests

## Common Patterns
See @resources/patterns/ for:
- Form component testing
- Async interaction testing
- Error state testing
- Accessibility testing

## Tools
- **Read**: Read component file
- **Write**: Create test file
- **Execute**: Run tests (optional)
```

### Пример 2: Code Review Skill

```markdown
---
name: code-review-skill
description: |
  Reviews pull requests against architecture, performance,
  and security standards. Provides specific feedback with
  references to team guidelines.
---

# Code Review Skill

## What This Reviews
1. Architecture compliance (patterns from @../../.claude/standards/architecture.md)
2. Performance implications
3. Security vulnerabilities
4. Code clarity and maintainability

## Review Process

### Step 1: Check Architecture
```bash
grep -rn "import.*from" --include="*.ts" \
  "$FILES_CHANGED" > /tmp/imports.txt
```
Compare against allowed patterns in @resources/architecture-patterns.md

### Step 2: Check Performance
- Unnecessary re-renders in React?
- N+1 query patterns?
- Inefficient algorithms?

See @resources/performance-checklist.md

### Step 3: Check Security
Search for common vulnerabilities:
```bash
grep -rn "eval\|exec\|innerHTML" "$FILES_CHANGED"
```

See @resources/security-checklist.md

### Step 4: Generate Review Report
```markdown
# Code Review: #1234

## Summary
- Architecture: ✅ PASS
- Performance: ⚠️ CONCERN (1 issue)
- Security: ✅ PASS
- Overall: APPROVE with suggestions

## Issues
### 1. Performance: Potential N+1 Query
**File**: src/api.ts:42
**Issue**: Loop calls database query
**Suggestion**: Use batch query

[Full details...]
```

## Tools
- **Grep**: Find problematic patterns
- **Read**: Analyze implementation
- **Reference**: Check against standards
```

---

## Checklist для production

### Pre-Deployment Checklist

```
SKILL DESIGN:
  [ ] Problem clearly defined (gap analysis done)
  [ ] 3 evaluation scenarios created
  [ ] Baseline score obtained (without skill)
  [ ] Skill written (≤500 lines SKILL.md)
  [ ] Resources organized in subdirectories
  [ ] All @references are valid
  [ ] No circular references
  
SKILL QUALITY:
  [ ] YAML frontmatter valid
  [ ] Description is specific & clear
  [ ] Name is lowercase-kebab-case
  [ ] Instructions are sequential & clear
  [ ] Examples are minimal (1-2 per pattern)
  [ ] Error handling in scripts
  [ ] No hardcoded paths (use forward slashes)
  [ ] Comments explain non-obvious logic
  
TESTING:
  [ ] Tested with fresh Claude instance
  [ ] All 3 evaluations run successfully
  [ ] Score improvement measured
  [ ] Iteratively improved based on observations
  [ ] Team tested (2+ developers)
  [ ] No regressions from previous skills
  
SECURITY:
  [ ] No sensitive data in skill
  [ ] Scripts don't execute arbitrary code
  [ ] Paths are validated
  [ ] External API calls are safe
  [ ] Security team reviewed (if applicable)
  
GOVERNANCE:
  [ ] Code reviewed (2+ approvals)
  [ ] Added to settings.json "enabled" list
  [ ] Documented in .claude/CLAUDE.md
  [ ] Version number assigned
  [ ] Changelog entry created
  [ ] Team notified
  
DOCUMENTATION:
  [ ] README in skill folder
  [ ] Examples are comprehensive
  [ ] Common use cases documented
  [ ] Troubleshooting guide written
  [ ] Links to related skills
  
MAINTENANCE:
  [ ] Owner assigned (who maintains?)
  [ ] Review cycle scheduled (quarterly)
  [ ] Deprecation policy clear
  [ ] Version management planned
```

### Post-Deployment Monitoring

```
FIRST WEEK:
  [ ] Monitor skill usage (does Claude trigger it?)
  [ ] Collect team feedback
  [ ] Fix any unexpected behaviors
  [ ] Update docs if unclear
  
FIRST MONTH:
  [ ] Measure productivity improvement
  [ ] Check for false positives (unwanted triggers)
  [ ] Refine trigger description if needed
  [ ] Add new patterns based on feedback
  
QUARTERLY REVIEW:
  [ ] Still solving the original problem?
  [ ] Any better alternatives?
  [ ] Dependencies still maintained?
  [ ] Performance acceptable?
  [ ] Should we expand or deprecate?
```

---

## Практические советы от опыта

```
TIP 1: Описание — это 80% успеха
Потратьте время на кристально ясное описание.
Если skill не срабатывает → всегда виновато описание.

TIP 2: Начните с простого
Markdown-only skills > Scripts с зависимостями
Усложняйте только когда необходимо.

TIP 3: Используйте evaluation-driven development
Не пишите предположения → Пишите на основе наблюдений.
Observations > Assumptions ВСЕГДА.

TIP 4: Консолидируйте skills
5 хороших skills > 20 плохих
Лучше один крепкий skill для тестирования,
чем 5 micro-skills.

TIP 5: Дебажьте с Claude A
Используйте Claude A (builder mode) для улучшения.
Затем тестируйте с Claude B (fresh instance).
Это РАБОТАЕТ лучше чем самостоятельная итерация.

TIP 6: Мониторьте использование
Если skill не срабатывает → Description не соответствует
Если срабатывает неправильно → Description слишком общая
Наблюдайте за реальным использованием и итерируйте.

TIP 7: Версионируйте корректно
Семантическое версионирование:
- 1.0.0 → 1.0.1: bug fixes
- 1.0.0 → 1.1.0: new patterns/features
- 1.0.0 → 2.0.0: breaking changes
```

---

**Дата:** 2025-01-06  
**Статус:** Production-ready  
**Версия:** 1.0

---

## Related Guides

### Getting Started
- [INDEX.md](INDEX.md) - Master documentation index
- [Complete Practices](CLAUDE-COMPLETE-PRACTICES.md) - Overview of all features (Russian)

### Core Features
- [Shared Architecture](claude-shared-architecture.md) - System overview
- [CLAUDE.md Guide](CLAUDE-CLAUDE-MD-GUIDE.md) - Project memory (English)

### Automation
- [Hooks Guide](claude-hooks-guide.md) - Workflow automation
- [Hooks Examples](claude-hooks-examples.md) - Production examples
- [Hooks Advanced](claude-hooks-advanced.md) - Advanced patterns

### Custom Capabilities
- [Skills Guide](claude-skills-guide.md) - Custom skills
- [Agents Guide](claude-agents-guide.md) - Agent system
- [Templates](claude-templates.md) - Template system

### Reference
- [Troubleshooting](claude-troubleshooting.md) - Common issues

