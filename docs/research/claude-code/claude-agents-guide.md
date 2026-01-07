# Claude Code AGENTS: Полное руководство по лучшим практикам
## Архитектура, оркестрация и production-ready паттерны

---

## Оглавление

1. [Фундаментальные концепции](#фундаментальные-концепции)
2. [AGENTS vs SKILLS vs SUBAGENTS](#agents-vs-skills-vs-subagents)
3. [Архитектура Agents системы](#архитектура-agents-системы)
4. [Orchestrator-Worker Pattern](#orchestrator-worker-pattern)
5. [Дизайн и конфигурация агентов](#дизайн-и-конфигурация-агентов)
6. [Hooks: детерминированный контроль](#hooks-детерминированный-контроль)
7. [Multi-Agent Workflows](#multi-agent-workflows)
8. [MCP & External Integration](#mcp--external-integration)
9. [Testing & Validation](#testing--validation)
10. [Типичные ошибки и Anti-patterns](#типичные-ошибки-и-anti-patterns)
11. [Production Deployment](#production-deployment)
12. [Примеры из реальных проектов](#примеры-из-реальных-проектов)

---

## Фундаментальные концепции

### Что такое AGENTS?

**AGENTS** — это автономные системы, которые действуют в цикле **gather context → plan → execute → validate → iterate**. В отличие от Skills (которые Claude вызывает на demand), Agents могут:

✅ Работать **автономно** без человеческого вмешательства  
✅ Принимать **решения** и **изменять план** на основе результатов  
✅ Взаимодействовать с **внешними системами** (MCP, APIs, databases)  
✅ Работать **параллельно** с другими агентами  
✅ Поддерживать **persistent state** между сессиями  
✅ Быть **развернуты в production** как автономные сервисы  

### Когда использовать AGENTS?

```
Используйте AGENTS когда:
✅ Задача требует АВТОНОМНОСТИ (без человека в цикле)
✅ Нужна ИТЕРАЦИЯ (план меняется на основе результатов)
✅ Требуется ПАРАЛЛЕЛЬНАЯ работа (несколько задач одновременно)
✅ Нужна ДЛИТЕЛЬНАЯ ПАМЯТЬ (сохранение state между сессиями)
✅ Интеграция с EXTERNAL SYSTEMS (API, databases, webhooks)
✅ Развертывание в PRODUCTION (как сервис, а не CLI)

НЕ используйте AGENTS когда:
❌ Одна-разовая задача (используйте Skills)
❌ Нужен ДЯМИЧЕСКИЙ контроль (используйте Commands)
❌ Задача не требует итерации (используйте Scripts)
❌ Просто нужно ЗНАНИЕ (используйте Projects/CLAUDE.md)
```

---

## AGENTS vs SKILLS vs SUBAGENTS

### Таблица сравнения

```
┌─────────────────────────────────────────────────────────────┐
│              AGENTS vs SKILLS vs SUBAGENTS                 │
└─────────────────────────────────────────────────────────────┘

FEATURE                    AGENTS         SKILLS          SUBAGENTS
────────────────────────────────────────────────────────────────
Что это?                   Автономная     Процедурные     Параллельные
                          система         знания          специалисты

Где живет?                 Production     В проекте       В Claude Code
                          (SDK/API)       (.claude/)      (Docs/Pro)

Invocation                 Explicit       Automatic       Automatic или
                          command         discovery       explicit

Context Window             Собственный    Shared          Собственный
                          (persistent)    (conversation)  (isolated)

Autonomy                   Full           Zero            Partial

Use Case                   Long-running   Quick tasks     Complex parallel
                          services       (code review)   work

Control                    Explicit       Implicit        Explicit + auto
                          (you code it)  (model decides) (delegation)

Tool Access                Full access    Restricted      Scoped per agent

State Management           Persistent     Ephemeral       Per-subagent
                          (database)      (memory)        (context)

Development               Complex        Simple          Medium
Effort                    (engineering)  (markdown)      (configuration)

Deployment                Docker/K8s      .claude/ in git VSCode/Codex
                          Production     or shared

Examples                  Content         Testing        Code review
                          moderator       generator      parallel with
                          Autonomous      Documentation  security audit
                          researcher      Refactoring

═══════════════════════════════════════════════════════════════

KEY INSIGHT:
  AGENTS = "Full independent systems"
  SKILLS = "Passive expertise, model chooses when to use"
  SUBAGENTS = "Isolated workers orchestrated by main agent"
  
  They can be COMBINED:
  Main AGENT orchestrates SKILLS + calls SUBAGENTS
```

### Когда использовать что?

```
Задача: "Generate unit tests"
→ Use SKILL (automatic discovery)
→ One-off task, no iteration

Задача: "Implement authentication system"
→ Use SUBAGENTS (parallel: design + security + testing)
→ Complex, needs isolation

Задача: "Automated content moderation service"
→ Use AGENT (continuous operation, external APIs)
→ Autonomous system

Задача: "Code review for all PRs"
→ Use AGENT + SKILL (agent orchestrates, skill does review)
→ Continuous + reusable expertise

Задача: "Team collaboration on large project"
→ Use 4 SUBAGENTS (architect, builder, validator, scribe)
→ Parallel work, clear roles
```

---

## Архитектура Agents системы

### Высокоуровневая архитектура

```
┌──────────────────────────────────────────────────────────┐
│                  PRODUCTION AGENT SYSTEM                 │
└──────────────────────────────────────────────────────────┘

┌─ External Trigger ──────────────────────────────────────┐
│ (API call, Webhook, Scheduled)                          │
└────────────────┬─────────────────────────────────────────┘
                 ↓
┌─ ORCHESTRATOR AGENT (Master) ──────────────────────────┐
│ Role: Planning, delegation, state management            │
│ Model: Claude Opus 4 (best reasoning)                   │
│ Tools: Limited (mostly read & route)                    │
│ Memory: Global state, decisions log                     │
│ Responsibilities:                                        │
│  - Understand request                                   │
│  - Break into subtasks                                  │
│  - Spawn & coordinate subagents                         │
│  - Aggregate results                                    │
│  - Handle errors & recovery                             │
└────────────────┬─────────────────────────────────────────┘
                 ↓
    ┌────────────┼────────────┐
    ↓            ↓            ↓
┌─────────┐ ┌─────────┐ ┌─────────┐
│SUBAGENT1│ │SUBAGENT2│ │SUBAGENT3│  ← Parallel execution
│(Analyst)│ │(Builder)│ │(Tester) │     Isolated contexts
└────┬────┘ └────┬────┘ └────┬────┘
     │           │           │
     └───────────┼───────────┘
                 ↓
        [External Systems]
        ├─ MCP Servers
        ├─ APIs (GitHub, Jira, etc)
        ├─ Databases
        └─ File Systems
                 ↓
        [Feedback Loop]
        Orchestrator receives results
        Validates, iterates, retries
                 ↓
        [Output & Storage]
        Results saved
        State updated
        Next trigger prepared

═══════════════════════════════════════════════════════════

KEY PRINCIPLES:
  1. Orchestrator = strategic brain (reasoning)
  2. Subagents = specialized workers (execution)
  3. Isolation = each subagent has own context
  4. Parallelization = independent tasks run simultaneously
  5. Feedback = results drive next decisions
```

### Файловая структура для Agents

```
.claude/
├── CLAUDE.md                    ← Project context
├── settings.json                ← Agent config
├── agents/                       ← AGENTS system
│   ├── orchestrator.md          ← Main orchestrator config
│   │   ├── description: "Delegates tasks to specialists"
│   │   ├── tools: [read, route] (narrow permissions!)
│   │   └── model: "claude-opus-4"
│   │
│   ├── code-review-agent.md     ← Specialist agent
│   │   ├── description: "Reviews code for quality"
│   │   ├── tools: [grep, read, comment]
│   │   └── model: "claude-sonnet-4"
│   │
│   ├── security-agent.md        ← Specialist agent
│   │   ├── description: "Audits for security issues"
│   │   ├── tools: [grep, read, report]
│   │   └── model: "claude-sonnet-4"
│   │
│   └── state.json               ← Global state
│       ├── current_task
│       ├── completed_subtasks
│       ├── pending_work
│       └── decisions
│
├── skills/                       ← Skills (called by agents)
│   ├── testing/
│   ├── documentation/
│   └── refactoring/
│
├── hooks/                        ← Lifecycle hooks
│   ├── post-agent-run.sh        ← After agent completes
│   └── error-recovery.sh        ← On agent failure
│
└── mcp/                          ← External integrations
    ├── github.server
    ├── jira.server
    └── slack.server
```

---

## Orchestrator-Worker Pattern

### Принцип работы

```
PHASE 1: REQUEST HANDLING
┌─────────────────────────────────┐
│ User/System Request             │
│ "Implement login feature"       │
└──────────────┬──────────────────┘
               ↓
┌─ ORCHESTRATOR ANALYZES ─────────┐
│ • Understand requirements       │
│ • Identify dependencies         │
│ • Plan execution phases         │
│ • Estimate effort & risks       │
└──────────────┬──────────────────┘
               ↓
PHASE 2: DELEGATION
┌──────────────────────────────────┐
│ Orchestrator spawns subagents:   │
│                                  │
│ ✓ Security Agent                │
│   Task: Design auth flows       │
│   Deadline: T+2h                │
│   Output: design-doc.md         │
│                                  │
│ ✓ Architect Agent               │
│   Task: Plan database schema    │
│   Deadline: T+3h                │
│   Output: schema.sql            │
│                                  │
│ ✓ Implementation Agent          │
│   Task: Code login endpoint     │
│   Depends on: security + arch   │
│   Output: auth-api.ts           │
│                                  │
│ ✓ Testing Agent                 │
│   Task: Write test suite        │
│   Depends on: implementation    │
│   Output: auth.test.ts          │
└──────────────┬──────────────────┘
               ↓
PHASE 3: PARALLEL EXECUTION
     [Agent 1]  [Agent 2]  [Agent 3]
     Security  Architect  Testing
     ✓ Design   ✓ Schema  ✓ Tests
       in 2h     in 3h     in 4h
               ↓
    [Orchestrator waits for all]
               ↓
PHASE 4: AGGREGATION & VALIDATION
┌──────────────────────────────────┐
│ Orchestrator checks:             │
│ ✓ All tasks completed?          │
│ ✓ Outputs meet quality bar?      │
│ ✓ Dependencies satisfied?        │
│ ✓ No conflicts?                  │
└──────────────┬──────────────────┘
               ↓
        [Issues found?]
         ↓         ↓
        NO        YES
        ↓         ↓
    SUCCESS   Re-run agents
    Done!     with feedback
              (iterate)
               ↓
            SUCCESS
            Done!

═══════════════════════════════════════════════════════════

BENEFITS:
  • Parallelization: 3 agents = ~3x faster (vs sequential)
  • Context isolation: No pollution, clean execution
  • Specialization: Each agent expert in one domain
  • Resilience: If one fails, others continue
  • Auditability: Clear task → result mapping
```

### Implementatoin примера: 4-Agent Team

```markdown
# Orchestrator Configuration

---
name: orchestrator
description: |
  Main orchestrator for feature implementation.
  
  Responsibility:
  - Understand feature requirements
  - Create detailed task breakdown
  - Spawn specialized agents
  - Aggregate and validate results
  - Handle retries and errors

---

## What This Agent Does

1. **Analyze** incoming feature request
2. **Plan** execution with phases and dependencies
3. **Delegate** to specialists (architecture, security, testing, docs)
4. **Monitor** progress and dependencies
5. **Validate** outputs meet quality standards
6. **Iterate** if issues found

## Agent Team Configuration

### 1. Architecture Agent
```
name: architecture-agent
model: claude-sonnet-4
tools: [read, write, grep]
scope: System design, data models, APIs
output: ADR (Architecture Decision Record) + schema
```

### 2. Security Agent
```
name: security-agent
model: claude-sonnet-4
tools: [read, grep, report]
scope: Security patterns, compliance, threat modeling
output: Security review + patterns
```

### 3. Implementation Agent
```
name: implementation-agent
model: claude-sonnet-4
tools: [read, write, execute]
scope: Code generation, API implementation
output: Production-ready code
```

### 4. Testing Agent
```
name: testing-agent
model: claude-sonnet-4
tools: [read, write, execute]
scope: Test generation, coverage validation
output: Comprehensive test suite
```

## Orchestration Flow

### Phase 1: Requirement Analysis
```
Orchestrator reads feature request:
- "Implement OAuth2 login"
  ├─ Security implications?
  ├─ Architecture impact?
  ├─ Testing strategy?
  └─ Documentation needs?
```

### Phase 2: Task Breakdown
```
Created MULTI_AGENT_PLAN.md:

## Feature: OAuth2 Login

### Phase 1: Security Design (Parallel)
- [ ] **Security Agent**: Review OAuth2 flows
  Input: Feature requirements
  Output: security-design.md
  Deadline: 2h

- [ ] **Architecture Agent**: Design user schema
  Input: Feature requirements
  Output: user-schema.sql
  Deadline: 2h

### Phase 2: Implementation (After Phase 1)
- [ ] **Implementation Agent**: Code endpoints
  Input: security-design.md + user-schema.sql
  Output: auth-api.ts
  Deadline: 4h

### Phase 3: Testing (After Implementation)
- [ ] **Testing Agent**: Write tests
  Input: auth-api.ts
  Output: auth.test.ts, coverage ≥80%
  Deadline: 3h

### Phase 4: Documentation (Parallel)
- [ ] **Documentation Agent**: Create docs
  Input: auth-api.ts + security-design.md
  Output: README + API docs
  Deadline: 2h
```

### Phase 3: Delegation
```
Orchestrator spawns agents with:
- Clear task description
- Input files/context
- Expected output format
- Deadline
- Success criteria
```

### Phase 4: Monitoring
```
Orchestrator checks every 30min:
- Task completion status
- Output quality
- Any blockers
- Dependencies resolved
```

### Phase 5: Validation & Aggregation
```
Results received:
✓ Security design complete
✓ Schema finalized
✓ API implemented
✓ Tests passing (85% coverage)

Orchestrator validates:
- Schema matches security requirements
- API follows security patterns
- Tests cover security edge cases
- Documentation accurate

Status: READY FOR DEPLOYMENT
```

## Error Recovery

If agent fails or produces low-quality output:

```
Option 1: Re-run with feedback
├─ Provide agent with the failure reason
├─ Add additional context/constraints
└─ Allow 1 retry

Option 2: Use different agent/model
├─ Try with better model (Claude Opus)
├─ Or escalate to human review
└─ Create issue for follow-up

Option 3: Decompose further
├─ Break task into smaller subtasks
├─ Assign to multiple agents
└─ Merge results
```

## State Management

```json
{
  "request_id": "feat-oauth2-001",
  "status": "in_progress",
  "phase": 3,
  "start_time": "2025-01-06T10:00:00Z",
  "plan": "MULTI_AGENT_PLAN.md",
  
  "agents": {
    "security": {
      "status": "completed",
      "output": "security-design.md",
      "quality_score": 9.2,
      "started": "T+0:00", 
      "completed": "T+1:45"
    },
    "architecture": {
      "status": "completed",
      "output": "user-schema.sql",
      "quality_score": 8.8,
      "started": "T+0:00",
      "completed": "T+2:15"
    },
    "implementation": {
      "status": "in_progress",
      "progress": "75%",
      "estimated_completion": "T+4:30",
      "dependencies_met": true
    },
    "testing": {
      "status": "queued",
      "prerequisites": ["implementation"],
      "estimated_start": "T+4:30"
    }
  },
  
  "decisions": [
    "Use JWT for token management (security decision)",
    "SQLite for local dev, PostgreSQL for production (arch decision)"
  ],
  
  "next_action": "Wait for implementation agent to finish"
}
```
```

---

## Дизайн и конфигурация агентов

### Каждый агент должен иметь:

```yaml
---
name: clear-kebab-case-name
description: |
  One clear sentence: What does this agent do?
  
  Input: What data/files it receives
  Output: What it produces
  Responsibilities: Specific tasks
  
model: claude-opus-4        # For orchestration/reasoning
              or claude-sonnet-4  # For specialized work
              or claude-haiku-4   # For simple tasks

tools:
  - read          # Read files
  - write         # Write files
  - grep          # Search files
  - execute       # Run scripts
  # Keep minimal! Only what's needed

memory:
  - task_state: Current progress
  - decisions: Choices made
  - blockers: What's blocking
  
timeout: 1h                 # Max execution time
max_retries: 2              # Retry attempts
---

# [Agent Name]

## Responsibilities
- [Task 1]
- [Task 2]
- [Task 3]

## Input Format
Expect to receive:
- File: requirements.md
- File: existing-code.ts
- Context: [any relevant info]

## Output Format
MUST produce:
- File: output-design.md
- File: output-code.ts
- Format: Clear, documented

## Decision Rules
When uncertain, choose:
1. [Rule 1]
2. [Rule 2]
3. Escalate to orchestrator

## Success Criteria
✓ Task completed
✓ Output meets spec
✓ Tests passing (if applicable)
✓ Documented and reviewable
```

### Моделирование выбора

```
Model Selection Strategy:

TASK COMPLEXITY         MODEL                    COST/SPEED
─────────────────────────────────────────────────────────────
Planning & routing      Claude Opus 4            $$, medium
                        (best reasoning)

Code review             Claude Sonnet 4          $, fast
Documentation

Testing                 Claude Haiku 4           tiny $, very fast
                        (simple tasks)

Heavy analysis          Claude Opus 4            $$, medium
Complex design

Total mix: Usually 10% Opus, 60% Sonnet, 30% Haiku
Result: 70% cost savings vs all-Opus while maintaining quality
```

---

## Hooks: детерминированный контроль

### Что такое Hooks?

**Hooks** — это shell scripts, которые выполняются в ключевые моменты жизненного цикла агента:

```
Lifecycle Events:
├─ post-write     → После каждого file write
├─ post-execute   → После каждого script execution
├─ pre-commit     → Перед git commit
├─ post-subagent-start  → Когда subagent запущена
├─ post-subagent-stop   → Когда subagent завершила
└─ on-error       → Когда агент встретил ошибку
```

### Control Flow с Hooks

```
Агент хочет остановиться:
  (Claude says: task complete, stopping)
           ↓
Hook: pre-stop trigger
  ├─ Запустить тесты
  ├─ Проверить coverage
  ├─ Валидировать output
           ↓
    [Тесты прошли?]
     ↓          ↓
    YES        NO
    ↓          ↓
  ALLOW    BLOCK + MESSAGE
  Stop     "Tests failed. Fix these:"
           [List failures]
           ↓
        Agent продолжает
        исправляет тесты
           ↓
        Повторяет попытку stop

═══════════════════════════════════════════════════════════

КЛЮЧЕВОЕ: Hooks = Детерминированная контроль
Вместо полагаться на агента:
  ✅ Используйте hooks для проверки фактов
  ✅ Разрешайте/блокируйте действия based on facts
  ✅ Обеспечьте автоматическое выполнение политик
```

### Пример Hook: Pre-Commit Validation

```bash
#!/bin/bash
# .claude/hooks/pre-commit.sh
# Блокирует commit если есть ошибки

set -e

echo "🔍 Running pre-commit checks..."

# Check 1: Tests pass
echo "  • Running tests..."
if ! npm test; then
  echo "❌ Tests failed. Cannot commit."
  exit 2  # Exit code 2 = BLOCK in Claude
fi

# Check 2: Coverage meets minimum
echo "  • Checking coverage..."
coverage=$(npm run coverage | grep -oP '\d+\.\d+(?=%)')
if (( $(echo "$coverage < 80" | bc -l) )); then
  echo "❌ Coverage $coverage% < 80%. Cannot commit."
  exit 2  # BLOCK
fi

# Check 3: Code quality (linting)
echo "  • Linting code..."
if ! npm run lint; then
  echo "❌ Linting failed. Cannot commit."
  exit 2  # BLOCK
fi

# Check 4: Security scan
echo "  • Security audit..."
if npm audit --audit-level=moderate; then
  echo "❌ Security vulnerabilities found. Cannot commit."
  exit 2  # BLOCK
fi

echo "✅ All checks passed. You may commit."
exit 0  # ALLOW
```

### Hook Output Format для Claude

```json
{
  "decision": "block",  // or "allow"
  "reason": "Tests failed in auth.test.ts: \n- Test 1: Expected true, got false\n- Test 2: Timeout after 5000ms",
  "next_steps": "Fix the failing tests and try again"
}
```

---

## Multi-Agent Workflows

### Паттерн 1: Параллельный поиск (Parallel Search)

```
ЗАДАЧА: Найти все уязвимости в codebase

Main Agent:
  ├─ Security Agent
  │  └─ Grep for: eval, exec, innerHTML
  │     ↓ Returns: vulnerable-lines.json
  │
  ├─ Performance Agent (параллельно)
  │  └─ Analyze: N+1 queries, large bundles
  │     ↓ Returns: perf-issues.json
  │
  └─ Dependencies Agent (параллельно)
     └─ Check: Outdated, vulnerable packages
        ↓ Returns: deps-report.json

Main Agent aggregates all → Security Report
```

### Паттерн 2: Pipeline (Sequential Dependencies)

```
ЗАДАЧА: Implement feature end-to-end

Architecture Agent → Specification
        ↓ Output: spec.md
        ↓
Security Agent (uses spec) → Security Design
        ↓ Output: security-design.md
        ↓
Implementation Agent (uses both) → Code
        ↓ Output: feature.ts
        ↓
Testing Agent (tests feature) → Tests
        ↓ Output: feature.test.ts + coverage
        ↓
Documentation Agent → Docs
        ↓ Output: README update + API docs
        ↓
DONE: Feature ready for merge
```

### Паттерн 3: Hierarchical (Team Structure)

```
PROJECT MANAGER (Lead Agent)
├─ ARCHITECT AGENT
│  ├─ Decisions: ADRs, system design
│  └─ Team liaison
│
├─ DEVELOPMENT TEAM
│  ├─ Backend Agent
│  │  ├─ API development
│  │  └─ Database work
│  │
│  └─ Frontend Agent
│     ├─ UI implementation
│     └─ State management
│
├─ QA AGENT
│  ├─ Test planning
│  ├─ Test execution
│  └─ Bug triage
│
└─ DEVOPS AGENT
   ├─ CI/CD pipeline
   ├─ Deployment
   └─ Monitoring

All agents → Project Manager (aggregation & decisions)
```

---

## MCP & External Integration

### Что такое MCP?

**Model Context Protocol (MCP)** — стандартный способ для Agents подключаться к внешним системам:

```
Claude Agent → MCP Server → External System

Примеры MCP servers:
├─ GitHub (issues, PRs, repos)
├─ Jira (tickets, projects)
├─ Slack (messages, channels)
├─ Linear (roadmap, tracking)
├─ Notion (databases, docs)
├─ PostgreSQL (data queries)
└─ Custom (your own tools)
```

### Конфигурирование MCP

```json
{
  "mcpServers": {
    "github": {
      "command": "node",
      "args": ["./tools/mcp-github.js"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}",
        "REPO": "myorg/myrepo"
      }
    },
    "jira": {
      "command": "python3",
      "args": ["./tools/mcp-jira.py"],
      "env": {
        "JIRA_URL": "https://myorg.atlassian.net",
        "JIRA_TOKEN": "${JIRA_TOKEN}"
      }
    },
    "postgres": {
      "command": "node",
      "args": ["./tools/mcp-postgres.js"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

### Использование в Agent

```yaml
---
name: issue-tracker-agent
tools:
  - read
  - write
  - mcp:github           # Access GitHub via MCP
  - mcp:jira             # Access Jira via MCP
---

# Issue Tracker Agent

When user asks to "create a bug report":
1. Read the bug description
2. Create issue in GitHub using mcp:github
   └─ POST /repos/{owner}/{repo}/issues
3. Link to Jira using mcp:jira
   └─ POST /issues
4. Post notification in Slack using mcp:slack
   └─ Send to #bugs channel
5. Update tracking spreadsheet
```

---

## Testing & Validation

### Agent Testing Framework

```
Level 1: Unit Tests
├─ Each agent behavior tested independently
├─ Mock external systems
└─ Example: "Security agent detects SQL injection"

Level 2: Integration Tests
├─ Test agents working together
├─ Use real (test) systems
└─ Example: "Orchestrator + Agents complete feature"

Level 3: End-to-End Tests
├─ Full workflow from request to deployment
├─ Production-like environment
└─ Example: "Feature request → ready in production"

Level 4: Continuous Monitoring
├─ Agent performance in production
├─ Error rates, success rates
├─ Cost tracking per agent
```

### Evaluation Framework

```
For each agent, define metrics:

COMPLETENESS:
  ├─ Did agent finish assigned task? Y/N
  ├─ Did it produce required output? Y/N
  └─ Is output in correct format? Y/N

CORRECTNESS:
  ├─ Does output match specification?
  ├─ Are there errors or incomplete parts?
  └─ Would this pass code review? Y/N

QUALITY:
  ├─ Readability (can humans understand?)
  ├─ Performance (efficient code/queries?)
  └─ Security (safe, no vulnerabilities?)

COST:
  ├─ Tokens used
  ├─ Time taken
  └─ API calls made

Track over time → identify improvements
```

---

## Типичные ошибки и Anti-patterns

### ❌ Anti-pattern 1: Too Much Autonomy

```
BAD:
"Here's the codebase. Build the whole system."
→ Agent gets lost, makes conflicting decisions
→ No checkpoints, no validation
→ Produces low-quality output

GOOD:
"Build the authentication system with these constraints:
 1. Use JWT tokens
 2. Password must be hashed with bcrypt
 3. Tests must pass before commit
 4. Get approval before merging"
→ Clear constraints
→ Validation gates
→ Quality assured
```

### ❌ Anti-pattern 2: Ignoring Agent Capabilities

```
BAD:
Use small model (Haiku) for complex reasoning task
→ Fails to understand nuances
→ Makes random decisions
→ Low quality output

GOOD:
Match model to task:
- Opus 4: Complex reasoning, planning
- Sonnet 4: Coding, analysis
- Haiku 4: Routine tasks
```

### ❌ Anti-pattern 3: Loss of Context in Long Workflows

```
BAD:
Orchestrator maintains ALL details of 5 subagents
→ Context overflow
→ Quality degrades
→ Can't track state

GOOD:
Orchestrator maintains ONLY:
- Completed ✓ Phase 1: Design (spec.md)
- In Progress → Phase 2: Implementation
- Pending ○ Phase 3: Testing

Each subagent only reads what's relevant
```

### ❌ Anti-pattern 4: No Deterministic Validation

```
BAD:
Rely on agent to self-check
"Does this look correct?"
→ Agent says yes, but it's wrong
→ No external validation

GOOD:
Use hooks for automatic validation:
- Run tests (must pass)
- Check coverage (must be ≥80%)
- Run linter (must have 0 errors)
- Security scan (must find 0 issues)
→ Deterministic, not opinion-based
```

### ❌ Anti-pattern 5: Unclear Agent Boundaries

```
BAD:
"Do whatever you think is best"
→ Overlap between agents
→ Duplicated work
→ Conflicting implementations

GOOD:
Clear boundaries:
- Security Agent: Only security decisions
- Architecture Agent: Only design decisions  
- Implementation Agent: Only coding
→ No overlap
→ Clear handoffs
```

---

## Production Deployment

### Deployment Checklist

```
PRE-DEPLOYMENT:
  [ ] All agents tested independently
  [ ] Integration tests passing
  [ ] E2E tests passing
  [ ] Load testing done (expected volume)
  [ ] Error rates acceptable (<1%)
  [ ] Cost per task estimated
  [ ] Security reviewed (MCP tokens, permissions)
  [ ] Documentation complete
  [ ] Team trained on system
  [ ] Rollback plan documented

DEPLOYMENT:
  [ ] Deploy to staging first
  [ ] Run staging for 1 week
  [ ] Monitor (errors, latency, costs)
  [ ] Fix any issues
  [ ] Schedule production deployment
  [ ] Notify stakeholders
  [ ] Deploy with feature flag (canary)

POST-DEPLOYMENT:
  [ ] Monitor 24/7 for first week
  [ ] Track:
      - Success rate (target: >99%)
      - Error rate (target: <0.1%)
      - Latency (target: <2min per task)
      - Cost per task
      - User satisfaction
  [ ] Daily review meetings
  [ ] Be ready to rollback
  [ ] After 1 week: full rollout
  [ ] Continue monitoring weekly
```

### Observability & Monitoring

```
Collect metrics for each agent:

PERFORMANCE:
- Success rate (%)
- Error rate (%)
- Average completion time
- P95, P99 latency
- Cost per execution

QUALITY:
- Output quality score (0-10)
- Rework rate (%)
- User satisfaction (1-5)
- Bug discovery rate

RESOURCES:
- Tokens per execution
- API calls per execution
- Model selection distribution
- Cost breakdown per agent

ALERTS:
- Error rate spike (>5%)
- Latency spike (>5min)
- Cost anomaly (>2x expected)
- Agent timeout
- MCP connection failure
```

---

## Примеры из реальных проектов

### Пример 1: 4-Agent Code Development Team

```
TEAM:
├─ Architect Agent (Claude Opus 4)
│  └─ Plans system design, creates ADRs
│
├─ Implementation Agent (Claude Sonnet 4)
│  └─ Codes the implementation
│
├─ Testing Agent (Claude Sonnet 4)
│  └─ Writes comprehensive tests
│
└─ Documentation Agent (Claude Haiku 4)
   └─ Creates docs and examples

WORKFLOW:
User: "Implement OAuth2 login"
  ↓
Orchestrator: 
  1. Request spec from Architect
  2. Architect creates oauth2-design.md (2h)
  3. Request implementation from Coder
  4. Coder implements auth-api.ts (4h)
  5. Request tests from Tester
  6. Tester creates auth.test.ts (3h)
  7. Request docs from Documenter
  8. Documenter creates README + API docs (2h)
  ↓
RESULT: Complete feature in ~8 hours (vs ~40h single person)

Why 3x faster?
- Architect & Tester work while Coder is working
- Each expert in their domain
- No context switching
- Parallel execution

COST:
- 1 Opus 4 (orchestrator): ~$20
- 2 Sonnet 4 (arch, code, test): ~$15
- 1 Haiku 4 (docs): ~$2
Total: ~$37 vs 40h @ $100/h = $4000 → 100x cheaper!
```

### Пример 2: Continuous Code Review System

```
AGENT SETUP:
├─ PR Watcher Agent
│  └─ Detects new PRs, triggers workflow
│
├─ Code Review Agent (parallel reviews)
│  ├─ Style & Quality Reviewer
│  ├─ Security Reviewer
│  ├─ Performance Reviewer
│  └─ Architecture Reviewer
│
└─ Aggregator Agent
   └─ Combines all reviews, posts comment

TRIGGER:
GitHub webhook → PR created
  ↓
PR Watcher detects
  ↓
Spawns 4 review agents (parallel)
  ↓
Each agent reviews for their domain:
- Style: Linting, naming, patterns
- Security: SQLi, XSS, auth issues
- Performance: N+1, large bundles, loops
- Architecture: Separation of concerns, patterns
  ↓
Aggregator collects all feedback
  ↓
Posts comprehensive review as single comment
  ↓
Developer sees all issues at once

RESULT:
- Reviews completed in 5 minutes
- No human review time wasted
- Developer gets detailed feedback
- Some issues caught automatically
```

---

## Key Takeaways

```
✅ USE AGENTS WHEN:
1. Task requires autonomy (no human in loop)
2. Need iteration (plan changes based on results)
3. Want parallelization (multiple tasks at once)
4. Require external integration (APIs, databases)
5. Long-running service (hours/days/months)

✅ ARCHITECTURE PRINCIPLES:
1. Orchestrator = strategic brain (narrow tools)
2. Subagents = specialized workers (focused tools)
3. Isolation = each agent has own context
4. Parallelization = independent work in parallel
5. Hooks = deterministic validation gates

✅ ANTI-PATTERNS TO AVOID:
❌ Too much autonomy
❌ Weak agent constraints
❌ Context overflow
❌ Relying on agent self-check
❌ Unclear boundaries
❌ No monitoring in production

✅ DEPLOYMENT SUCCESS:
1. Test thoroughly before production
2. Use staging environment
3. Monitor everything (errors, costs, latency)
4. Be ready to rollback
5. Iterate based on metrics
```

---

**Версия**: 1.0  
**Дата**: 2025-01-06  
**Статус**: Production-ready  
**Автор**: AI Research

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

