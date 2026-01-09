# Implementation Guide: Claude Code Files Organization

**See:** @patterns/claude-code-files-organization-001.yaml

---

## Phase 1: Create .claude/ Directory Structure (30 minutes)

### Step 1: Create base directories
```bash
mkdir -p .claude/{skills,agents,commands,hooks,standards,references}
chmod +x .claude/hooks/*.sh 2>/dev/null || true
```

### Step 2: Create CLAUDE.md (navigation hub)

**File:** `.claude/CLAUDE.md`

```markdown
# Project Name

## Quick Overview
One-paragraph summary

## Quick Start
One-command installation
For details: [QUICKSTART.md](QUICKSTART.md)

## Architecture
See @standards/architecture.md

## Workflow
See @standards/coding-standards.md

## Commands
- /test - Run tests
- /review - Code review

## Recent Decisions
- 2026-01-07: Adopted unified testing approach
```

### Step 3: Create settings.json

**File:** `.claude/settings.json`

```json
{
  "skills.enabled": ["testing", "code-review", "documentation"],
  "hooks": {
    "SessionStart": [{
      "command": ".claude/hooks/session-setup.sh"
    }],
    "PostToolUse": [{
      "matcher": "Edit:*.yaml|Write:*.yaml",
      "command": ".claude/hooks/validate-yaml.sh"
    }]
  }
}
```

---

## Phase 2: Create Reusable Skills (2-4 hours per skill)

### Step 1: Identify repetitive tasks
Ask yourself: "What do you repeatedly explain to Claude?
- Testing patterns?
- Code review rules?
- Documentation format?"

### Step 2: Create skill structure
```bash
mkdir -p .claude/skills/my-skill/{resources,scripts}
```

### Step 3: Write SKILL.md

**File:** `.claude/skills/my-skill/SKILL.md`

```markdown
---
name: my-skill
description: |
  Does X when Y. Triggers when user asks for Z.
  Outputs A with B format following project standards.
---

# When to Use This Skill
- User asks for "X"
- Part of Y workflow
- Need Z output

# What This Skill Does
1. Analyze input
2. Generate output
3. Validate quality

# Key Instructions
See @resources/patterns.md for detailed patterns.
Use template: @resources/template.md

# Tools Used
- **Read**: Read source files
- **Write**: Create outputs
```

### Step 4: Create resources/
- `.claude/skills/my-skill/resources/patterns.md`
- `.claude/skills/my-skill/resources/examples/`

### Step 5: Test with evaluation-driven development
1. Create 3 evaluation scenarios
2. Test baseline (without skill)
3. Test with skill
4. Measure improvement
5. Iterate based on failures

---

## Phase 3: Create Autonomous Agents (if needed, 1-2 days per agent)

### Step 1: Determine if agent is needed

**Use AGENTS when:**
- Task requires autonomy (no human in loop)
- Need iteration (plan changes based on results)
- Want parallelization (multiple tasks at once)
- Long-running service (hours/days/months)

**Use SKILLS instead for:**
- One-off tasks
- Quick workflows
- Simple procedural knowledge

### Step 2: Create agent file

**File:** `.claude/agents/my-agent.md`

```markdown
---
name: my-agent
description: |
  Autonomous agent that performs X with Y goals.
  Works independently with minimal supervision.
model: claude-opus-4  # or claude-sonnet-4 or claude-haiku-4
tools: [read, write, grep, execute]
timeout: 1h
---

# Responsibilities
- [Task 1]
- [Task 2]
- [Task 3]

# Decision Rules
When uncertain, choose:
1. [Rule 1]
2. [Rule 2]
3. Escalate to human

# Success Criteria
✓ Task completed
✓ Output meets spec
✓ Documented
```

### Step 3: Test agent thoroughly
1. Unit test: Test individual behaviors
2. Integration test: Test with other agents
3. E2E test: Full workflow
4. Monitor: Track success rate, errors, cost

---

## Phase 4: Create Slash Commands (30 minutes per command)

### Step 1: Identify repetitive workflows
- Code review workflow
- Testing workflow
- Deployment workflow

### Step 2: Create command file

**File:** `.claude/commands/my-workflow.md`

```markdown
Please perform the following workflow:

## Step 1: Analysis
Analyze the current state of $ARGUMENTS

## Step 2: Planning
Create a plan for addressing identified issues

## Step 3: Execution
Execute the plan step by step

## Step 4: Verification
Verify all changes are correct

Remember to use /testing skill for test generation.
```

### Step 3: Test command
Use Claude Code with /my-workflow command
Verify workflow executes correctly
Iterate based on results

---

## Phase 5: Create Automation Hooks (1-2 hours per hook)

### Step 1: Identify automation opportunities
- SessionStart: Check KB installation
- PostToolUse: Validate YAML
- Stop: Auto-commit changes

### Step 2: Create hook script

**File:** `.claude/hooks/my-hook.sh`

```bash
#!/bin/bash
INPUT=$(cat)

# Your validation logic here
if [[ condition ]]; then
  echo "✅ Check passed"
  exit 0  # ALLOW
else
  echo "❌ Check failed"
  exit 2  # BLOCK
fi
```

### Step 3: Make executable and configure
```bash
chmod +x .claude/hooks/my-hook.sh

# Add to .claude/settings.json hooks section
```

### Step 4: Test hook manually
```bash
echo '{"tool_name":"Bash","tool_input":{"command":"test"}}' | ./.claude/hooks/my-hook.sh
echo "Exit code: $?"  # 0 = allow, 2 = block
```
