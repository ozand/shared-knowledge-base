# Skill Design Pattern - Implementation Guide

**Extracted from:** skill-design.yaml
**Pattern ID:** SKILL-DESIGN-001

## YAML Frontmatter

### Required Fields

Every SKILL.md MUST start with YAML frontmatter:

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
---
```

### Naming Rules

- **name:** lowercase, kebab-case, ≤64 chars, unique
- **description:** Plain text (not markdown), ≤1024 chars
- **CRITICAL:** Description must explain WHEN to use
- Use bullet points in description (helps Claude)

### Description Examples

**BAD:**
```yaml
description: "Testing skill"
```
**Problem:** Too vague, Claude doesn't know when to trigger

**GOOD:**
```yaml
description: |
  Generates unit tests for functions using Vitest, matching
  project coverage targets and assertion patterns.

  Triggers when:
  - User asks to "write tests" or "generate tests"
  - Testing function or API endpoint
  - Part of code review or deployment validation

  Outputs complete test files with 80%+ coverage.
```

## Skill Structure

### Recommended Outline

```markdown
---
name: skill-name
description: Specific description of when to use
---

# Skill Title

## When to Use This Skill
- User asks to "X", "Y", "Z"
- Part of workflow W
- When condition C is met

## What This Skill Does
1. Step one
2. Step two
3. Step three

## Key Instructions

### Step 1: Action
- Detail 1
- Detail 2
- See @resources/patterns.md for patterns

### Step 2: Action
- Detail 1
- Detail 2
- Use @resources/template.ts

## Common Patterns

### Pattern: Name
[Brief example]
See @resources/pattern-name.md for more

## Tools Used
- **Read**: For reading source files
- **Write**: For creating new files

## Important Notes
- Critical note 1
- Critical note 2
- Refer to project CLAUDE.md: @../../CLAUDE.md

## Examples
See @resources/examples/ for complete examples
```

### Size Guidelines

- **SKILL.md:** 200-500 lines max (prefer 300)
- **resources/patterns.md:** 100-500 lines
- **resources/examples/:** 1-20 files
- **Full skill folder:** Typically 500KB-5MB
- **If >10MB:** Refactor!

## Progressive Disclosure

### Architecture

Load information in layers:

```
Layer 1: Metadata (ALWAYS loaded)
├─ name: "testing-skill"
├─ description: "Generates unit tests..."
└─ Size: ~30-50 tokens per skill

Layer 2: SKILL.md (loaded when TRIGGERED)
├─ Main instructions (200-500 lines)
├─ Brief examples (1-2 per pattern)
└─ Size: ~500-2000 tokens

Layer 3: Resources (loaded ON DEMAND)
├─ @resources/patterns.md (detailed patterns)
├─ @resources/examples/ (full examples)
├─ @resources/template.ts (templates)
└─ Size: Depends on usage
```

### Implementation

```
SKILL.md (300 lines - core only)
├── When to use
├── Key instructions
├── Brief examples
└── @references to resources

resources/
├── patterns.md (200 lines - complete patterns)
├── examples/
│   ├── simple.ts (50 lines)
│   └── complex.ts (150 lines)
├── assertions.md (100 lines)
└── template.ts (30 lines)

IMPORTANT: All @references are WITHIN skill directory
WRONG: @../../../standards/testing.md (goes up!)
RIGHT: @resources/patterns.md or @./resources/patterns.md
```

## Best Practices

1. **Use evaluation-driven development**
   - Guideline: Define gap → Create evaluations → Write minimal skill → Test with Claude B
   - Reason: Observations > Assumptions. Skills based on real usage work better.

2. **Write crystal-clear descriptions**
   - Guideline: Spend 80% of time on description. Explain WHEN to use, not WHAT.
   - Reason: Description determines when skill triggers. Vague = never triggers.

3. **Keep SKILL.md lean**
   - Guideline: 200-500 lines max. Move details to resources/ with @references.
   - Reason: Faster loading, less tokens, easier maintenance.

4. **Consolidate related skills**
   - Guideline: One skill for testing, not 10 micro-skills (unit, integration, e2e...)
   - Reason: Less confusion, easier for Claude to choose, less metadata overhead.

5. **Add error handling to scripts**
   - Guideline: Scripts MUST NOT crash. Return helpful error messages.
   - Reason: Claude needs to know what went wrong to help user.

6. **Use specific descriptions**
   - Guideline: BAD: "Code review" → GOOD: "Reviews PRs for security and performance issues"
   - Reason: Specific descriptions prevent false positives.

7. **Test with fresh Claude instance**
   - Guideline: Use Claude A to build, Claude B to test. Never test in isolation.
   - Reason: Real usage reveals problems that theoretical testing misses.

8. **Version your skills**
   - Guideline: Use semantic versioning: 1.0.0 → 1.0.1 (bugs), 1.1.0 (features), 2.0.0 (breaking)
   - Reason: Track changes, enable rollbacks, communicate impact.
