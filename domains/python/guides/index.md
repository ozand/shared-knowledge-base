---
title: "Python Project Guidelines Index"
version: "1.0.0"
last_updated: "2025-01-01"
purpose: "Navigation hub for AI agents"
priority: critical
agent_usage: "Read this first to understand guideline structure"
---

# Python Project Guidelines - Navigation Index

## 📋 Quick Reference for AI Agents

### Document Priority Levels
- **🔴 Critical** - Must read for every task
- **🟡 Contextual** - Read when relevant to task type
- **🔵 Reference** - Consult when needed

---

## Universal Guidelines (Apply to all Python projects)

| Document | Priority | When to Use | Key Topics |
|----------|----------|-------------|------------|
| [00-core-principles.md](00-core-principles.md) | 🔴 Critical | Always | DRY, SOLID, architecture patterns |
| [01-project-structure.md](01-project-structure.md) | 🔴 Critical | Project setup, file organization | Directory layout, src/tests separation |
| [02-code-quality.md](02-code-quality.md) | 🟡 Contextual | Code changes, refactoring | Ruff, mypy, pre-commit hooks |
| [03-testing-strategy.md](03-testing-strategy.md) | 🟡 Contextual | Writing/running tests | Unit, integration, E2E testing |
| [04-ddd-guideline.md](04-ddd-guideline.md) | 🟡 Contextual | Domain modeling, context boundaries | Bounded Contexts, Entities, Aggregates |

---

## Task-Based Navigation

### "I need to set up a new project"
→ Read: `00-core-principles.md`, `01-project-structure.md`, `02-code-quality.md`

### "I need to write/modify code"
→ Read: `00-core-principles.md`, `02-code-quality.md`

### "I need to write tests"
→ Read: `03-testing-strategy.md`, `01-project-structure.md` (test directory layout)

### "I need to refactor existing code"
→ Read: `00-core-principles.md`, `02-code-quality.md` (refactoring process)
