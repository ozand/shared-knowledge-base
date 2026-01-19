---
title: "Core Software Design Principles"
version: "1.0.0"
last_updated: "2025-01-01"
category: "architecture"
priority: critical
applies_to: ["all_projects"]
agent_usage: "Read before any design or implementation task"
keywords: ["DRY", "SOLID", "architecture", "design_patterns", "abstractions"]
related_docs: ["01-project-structure.md", "02-code-quality.md"]
---

# Core Software Design Principles

> Universal principles for any software project. These are non-negotiable fundamentals.

## Universal Principles

### DRY (Don't Repeat Yourself)
- Eliminate duplicated logic across the codebase
- Extract shared utilities into reusable functions/classes
- Apply to code, tests, documentation, and configuration

### Single Responsibility Principle (SRP)
- One module/class/function = one reason to change
- Each component should do one thing well
- Easier to test, maintain, and understand

### Separation of Concerns
- Each module handles one type of responsibility
- Business logic ≠ data access ≠ presentation ≠ infrastructure
- Example: separate API routes, business logic, and database queries

### YAGNI & KISS
- **YAGNI (You Ain't Gonna Need It):** Build only what's needed now
- **KISS (Keep It Simple, Stupid):** Choose the simplest solution that works
- Avoid premature optimization and over-engineering

---

## Architecture Guidelines

### Dependency Inversion Principle
- High-level modules depend on abstractions, not concrete implementations
- Use interfaces/protocols to define contracts
- Example: depend on `PaymentProcessor` interface, not `StripePayment` class

### Import Strategy
- **Absolute imports only** - forbid relative imports
```python
# ✅ Good
from src.my_project.payments import process_payment

# ❌ Bad
from ..payments import process_payment
```

### Clear Boundaries
- Keep core business logic independent from:
  - I/O operations (file, network, database)
  - UI/presentation layer
  - Framework-specific code
  - External services
- This enables easier testing and framework migration

### Low Coupling, High Cohesion
- **Low coupling:** Minimize dependencies between modules
- **High cohesion:** Keep related functionality together
- Modules should be independently deployable and testable

---

## Code Organization Principles

### Explicit Over Implicit
- Code should be self-documenting
- Clear variable and function names
- Avoid "magic" values and hidden assumptions

### Determinism
- Prefer pure functions for business logic
- Same input → same output (no hidden state)
- Side effects isolated to boundaries (I/O layer)

### Idempotency
- Critical operations should be safely repeatable
- Examples: API calls, database migrations, deployments
- Use unique identifiers to prevent duplicate processing

---

## When to Apply These Principles

| Principle | Apply When | Skip When |
|-----------|-----------|-----------|
| DRY | Logic repeated 2+ times | Single use, prototype code |
| SRP | Module becoming complex | Trivial scripts (<50 lines) |
| Abstraction | Multiple implementations needed | Only one implementation will ever exist |
| Idempotency | Network/IO operations | Pure computation |

---

## Anti-Patterns to Avoid

- ❌ God objects (classes that do everything)
- ❌ Circular dependencies between modules
- ❌ Tight coupling to frameworks
- ❌ Business logic in controllers/views
- ❌ Hidden global state
- ❌ Copy-paste programming
