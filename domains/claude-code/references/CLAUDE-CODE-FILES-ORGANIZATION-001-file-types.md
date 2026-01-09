# Complete File Type Guide

**See:** @patterns/claude-code-files-organization-001.yaml

---

## CLAUDE.md - Project Memory

**Purpose:** Navigation hub for project context
**Location:** `.claude/` (repo root) or `~/.claude/` (user)
**Size:** ~300 lines maximum
**Loading:** Always loaded at session start

### Structure
1. Overview (2-3 sentences)
2. Quick start (1 command + link)
3. Key features (bulleted list)
4. Documentation links (not duplication)
5. Recent decisions (what, why, when)

### Best Practices
- **Keep it lean (~300 lines)** - Loaded every session, token efficiency
- **Link to details, don't duplicate** - Single source of truth, progressive disclosure
- **Use WHAT, WHY, HOW framework**
  - WHAT: Project is X (technical description)
  - WHY: We chose Y (reasoning)
  - HOW: To work here, do Z (instructions)

### Anti-Patterns
- **Massive CLAUDE.md (1000+ lines)**
  - Problem: Token waste, hard to navigate
  - Solution: Split into standards/ references/
- **Duplication across files**
  - Problem: Updates missed, inconsistency
  - Solution: Single source of truth, others reference it

---

## SKILL.md - Procedural Knowledge

**Purpose:** Reusable instructions for specific tasks
**Location:** `.claude/skills/{skill-name}/`
**Size:** 200-500 lines
**Loading:** Metadata always, full content on-demand

### Structure
```yaml
---
name: skill-name              # Lowercase, kebab-case
description: |
  Does X when Y. Triggers when Z.
  Outputs A following project standards.
version: 1.0.0
---

# When to Use This Skill
- User asks for "X"
- Part of Y workflow

# What This Skill Does
1. Analyze
2. Process
3. Output

# Key Instructions
See @resources/patterns.md for details
```

### Best Practices
- **Clear description is critical**
  - Claude uses description for skill discovery
  - ✅ GOOD: "Generates unit tests with 80%+ coverage using Vitest. Triggers when user asks for tests. Outputs complete test files with edge cases."
  - ❌ BAD: "Testing skill"

- **Progressive disclosure**
  - Keep SKILL.md lean, details in resources/
  - SKILL.md (300 lines)
    - @resources/patterns.md (all patterns)
    - @resources/examples/ (full examples)

- **Consolidate related skills**
  - 5 good skills > 20 micro-skills
  - ✅ CORRECT: testing-skill/ (unit, integration, e2e)
  - ❌ WRONG: unit-test-skill/, integration-test-skill/, e2e-test-skill/

### Anti-Patterns
- **Too general description**
  - Problem: Skill never triggers or triggers inappropriately
  - Solution: Be specific: what, when, triggers, outputs

- **SKILL.md > 500 lines**
  - Problem: Loads too much content, token waste
  - Solution: Split into resources/ files

- **No resources/ organization**
  - Problem: All content inline, hard to maintain
  - Solution: Use progressive disclosure pattern

---

## AGENT.md - Autonomous Agent

**Purpose:** Independent system for long-running tasks
**Location:** `.claude/agents/` or `.claude/agents/subagents/`
**Size:** 300-800 lines
**Loading:** Explicit invocation (not auto-discovered)

### Structure
```yaml
---
name: agent-name
description: |
  Autonomous agent that performs X independently.
model: claude-opus-4  # Opus for reasoning, Sonnet for work
tools: [read, write, grep, execute]
timeout: 1h
---

# Responsibilities
- [Task 1]
- [Task 2]

# Input Format
Expect: File: requirements.md

# Output Format
MUST: File: output.md

# Decision Rules
When uncertain:
1. [Rule 1]
2. Escalate

# Success Criteria
✓ Task complete
✓ Quality met
```

### Best Practices
- **Match model to task complexity**
  - Opus 4: Planning, routing, complex reasoning
  - Sonnet 4: Coding, analysis
  - Haiku 4: Simple tasks

- **Narrow tool permissions**
  - Security, focused behavior
  - Orchestrator: [read, route]  # Minimal
  - Worker: [read, write, execute]  # Full access

- **Clear decision rules**
  - Agent knows when to escalate
  - Example:
    ```
    When uncertain:
    1. Try approach A (if pattern matches)
    2. Try approach B (if pattern matches)
    3. Escalate to orchestrator
    ```

### Anti-Patterns
- **Too much autonomy**
  - Problem: Agent gets lost, makes bad decisions
  - Solution: Clear constraints, validation gates

- **Wrong model for task**
  - Problem: Haiku for complex reasoning → Fails
  - Solution: Match model to complexity

- **No error handling**
  - Problem: Agent crashes, no recovery
  - Solution: Try/retry logic, escalation paths

---

## COMMAND.md - Slash Command

**Purpose:** Prompt template for quick workflows
**Location:** `.claude/commands/`
**Size:** 50-200 lines
**Invocation:** Typing / in Claude Code

### Structure
```markdown
Please perform the following workflow:

## Step 1: Analysis
Analyze $ARGUMENTS

## Step 2: Planning
Create plan for addressing issues

## Step 3: Execution
Execute plan step by step

## Step 4: Verification
Verify changes
```

### Best Practices
- **Use $ARGUMENTS for parameters**
  - Makes commands flexible
  - Example: `/fix-issue 1234`
  - Command receives: `$ARGUMENTS = "1234"`

- **Clear sequential steps**
  - Easy to follow, predictable
  - Guideline: Number each step 1-10

- **Reference skills/agents**
  - Reuse existing capabilities
  - Example: Use /testing skill for test generation

### Anti-Patterns
- **Vague instructions**
  - Problem: Unpredictable behavior
  - Solution: Specific steps, clear outputs

- **Too long (>200 lines)**
  - Problem: Hard to maintain, complex
  - Solution: Split into smaller commands

---

## Hooks - Lifecycle Automation

**Purpose:** Deterministic automation at key points
**Location:** `.claude/hooks/`
**Size:** <100 lines (fast execution)

### Events

#### SessionStart
- **Trigger:** When Claude session starts
- **Uses:** Environment setup, context loading
- **Example:** `.claude/hooks/session-setup.sh`

#### PreToolUse
- **Trigger:** Before any tool call
- **Uses:** Validation, security filtering, blocking
- **Example:** `.claude/hooks/validate-yaml.sh`

#### PostToolUse
- **Trigger:** After successful tool call
- **Uses:** Quality checks, auto-formatting, logging
- **Example:** `.claude/hooks/quality-gate.sh`

#### Stop
- **Trigger:** When Claude finishes response
- **Uses:** Quality validation, auto-commit
- **Example:** `.claude/hooks/auto-commit.sh`

### Best Practices
- **Keep hooks FAST (<2 seconds)**
  - Run synchronously, block workflow
  - Guideline: Heavy operations → CI/CD, not hooks

- **Exit codes matter**
  - Exit 0: ALLOW (continue)
  - Exit 2: BLOCK (stop action, show reason)

- **Quote all variables**
  - Prevent injection, handle spaces
  - Example: `FILE="$1"; rm "$FILE"`

- **Test hooks manually**
  ```bash
  echo '{"tool_name":"Bash","tool_input":{"command":"test"}}' | ./hook.sh
  echo "Exit: $?"  # 0 = allow, 2 = block
  ```

### Anti-Patterns
- **Slow hooks (>5 seconds)**
  - Problem: Every edit pauses workflow
  - Solution: Quick checks in hooks, heavy in CI/CD

- **Broad matchers**
  - Problem: `"matcher": "*"` runs on EVERY tool call
  - Solution: Specific matchers: 'Bash', 'Edit|Write'

- **Silent failures**
  - Problem: No error feedback, hard to debug
  - Solution: `set -e` or explicit `|| exit 2`

---

## Standards - Team Knowledge

**Purpose:** Single source of truth for team rules
**Location:** `.claude/standards/`
**Size:** 100-500 lines each
**Loading:** Referenced from CLAUDE.md, SKILL.md, AGENT.md

### Best Practices
- **One authoritative file per topic**
  - Avoid duplication, prevent inconsistency
  - Example:
    ```
    standards/testing.md (authoritative)
    All others: @standards/testing.md
    ```

- **Clear structure**
  - Guideline: Principles → Patterns → Examples

- **Version control**
  - Track changes, maintain history

### Anti-Patterns
- **Duplication across files**
  - Problem: Updates missed, inconsistency spreads
  - Solution: Single source of truth

- **Mixed concerns in one file**
  - Problem: Hard to find, hard to maintain
  - Solution: One topic per file
