# Claude Code Shared Model - Real World Examples

**Extracted from:** claude-code-shared-model.yaml
**Pattern ID:** CLAUDE-CODE-SHARED-MODEL-001

## Example 1: Monorepo with Frontend and Backend Teams

**Scenario:** Monorepo with Frontend and Backend teams

**Structure:**
```
.claude/ (shared core)
├── standards/
│   ├── architecture.md
│   ├── coding-standards.md
│   └── testing-guidelines.md
├── skills/
│   └── testing/SKILL.md
└── agents/
    └── code-review-agent.md

packages/frontend/.claude/
└── CLAUDE.md (FE-specific: "Use React + TypeScript")

services/backend/.claude/
└── CLAUDE.md (BE-specific: "Use FastAPI + Pydantic")
```

**Workflow:**
1. Frontend dev: Uses shared standards + FE CLAUDE.md
2. Backend dev: Uses shared standards + BE CLAUDE.md
3. Both: Use same testing Skill → consistent test style
4. PR review: code-review-agent enforces shared standards

**Results:**
- Onboarding: Days → Hours
- Code review: 5 cycles → 1-2 cycles
- Test coverage: 30% → 80%+
- Consistency: No → Yes

## Example 2: New Developer Onboarding

**Scenario:** New developer joins team

### Without Shared Model

- Asks: "How do we structure components?"
- Gets 3 different answers from 3 people
- Confused, inconsistent code
- Onboarding: **1 week**

### With Shared Model

- Reads CLAUDE.md (5 min)
- Reads architecture standard (30 min)
- Ready to code!
- Onboarding: **1 hour**

**Lesson:**
> Shared knowledge reduces onboarding from 1 week to 1 hour.
> Everyone gets same answer from same source of truth.

## Example 3: Feature Development Workflow

**Scenario:** 5-day feature development

### Day 1: Planning
- Developer checks CLAUDE.md
- Reads @standards/architecture.md
- Creates PLAN.md following patterns

### Day 2-3: Development
- Uses /testing skill to generate tests
- Code matches standards automatically
- Consistent structure

### Day 4: Testing
- Testing Skill generates matching tests
- 80%+ coverage achieved
- Follows team test patterns

### Day 5: Code Review
- code-review agent checks standards
- Only real issues discussed
- Each comment links to @standard
- Approved in 1-2 cycles

### Day 6: Deploy
- deployment agent orchestrates
- Following deployment.md standard
- Automated validation & deployment

**Result:**
> Same workflow, ANY developer, ANY project.
> Standards ensure consistency.
> Skills speed up repetitive tasks.
> Agents automate the boring stuff.

## Example 4: Common Mistakes and Solutions

### Mistake 1: Everything in Root CLAUDE.md

**Wrong:** 2000 lines in CLAUDE.md with all details
**Consequence:** 2000 lines loaded every session (wasteful!)
**Correct:** Keep root ~300 lines, link to details

**Pattern:**
```
CLAUDE.md (300 lines) → @standards/ (detailed)
Only referenced files loaded on demand
```

### Mistake 2: Duplicating Rules

**Wrong:** Same rule in CLAUDE.md, standards/, docs/
**Consequence:** Updates missed, inconsistency spreads
**Correct:** Single source of truth, others reference it

**Pattern:**
```
error-handling.md (authoritative)
All others: @standards/error-handling.md
```

### Mistake 3: Deep Nested References

**Wrong:** CLAUDE.md → ref1.md → ref2.md → ref3.md
**Consequence:** Claude partially reads, loses context
**Correct:** One level deep from CLAUDE.md

**Pattern:**
```
CLAUDE.md → reference files (direct)
reference files → other references OK
```

### Mistake 4: Not Committing .claude

**Wrong:** .claude/ in .gitignore
**Consequence:** Each dev has different standards!
**Correct:** Commit standards, exclude .local files

**Gitignore:**
```
.claude/         → IN GIT (shared)
.claude/*.local  → .gitignore (personal)
```

### Mistake 5: Unused Skills

**Wrong:** 10 skills created, nobody uses them
**Consequence:** Manual work continues, skills ignored
**Correct:** Start with 1-2 essential skills, document usage

**Examples:**
- testing skill first
- Expand based on feedback
- Document how to use each skill

### Mistake 6: Unreliable Agents

**Wrong:** code-review agent comments wrong issues
**Consequence:** Developers disable it, lose automation
**Correct:** Start simple, test thoroughly, monitor feedback

**Advice:**
- First agent: Very specific task
- Test thoroughly before deploying
- Monitor and fix issues quickly

### Mistake 7: Ignoring Feedback

**Wrong:** Standards created by leadership, dev team says "too strict"
**Consequence:** Team ignores standards, works around them
**Correct:** Feedback loop, iterate based on real problems

**Pattern:**
- Monthly reviews
- "This standard doesn't work because..."
- Show team they matter
- Update based on feedback

### Mistake 8: Not Maintaining

**Wrong:** Standards written 6 months ago, reality changed
**Consequence:** Standards outdated, ignored
**Correct:** Quarterly updates

**Pattern:**
- Review standards each quarter
- Update based on new tools/patterns
- Remove obsolete rules
- Add lessons learned
