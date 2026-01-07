---
name: "claude-code-architecture"
description: "Expert knowledge of Claude Code infrastructure, components, patterns, and best practices. Deep understanding of system architecture, component interactions, and production-tested patterns."
version: "1.0"
author: "Claude Code Expert"
tags: ["claude-code", "architecture", "infrastructure", "skills", "agents", "hooks"]
resources:
  - "resources/system-overview.md"
  - "resources/skill-activation.md"
  - "resources/hook-system.md"
  - "resources/progressive-disclosure.md"
  - "resources/agent-types.md"
---

# Claude Code Architecture

Expert knowledge of Claude Code infrastructure, components, and interactions.

## Quick Overview

Claude Code is a CLI tool that extends Claude with:
- **Skills** - Reusable capabilities with auto-activation
- **Agents** - Specialized AI for specific tasks
- **Hooks** - Automation at workflow points
- **Commands** - Custom slash commands
- **Standards** - Team knowledge and workflows
- **References** - Detailed documentation

**📘 Complete System Overview:** `@resources/system-overview.md`

---

## System Components

### 1. Skills (SKILL.md)

**Purpose:** Reusable capabilities that can be auto-activated

**Location:** `.claude/skills/<skill-name>/SKILL.md`

**Key Features:**
- YAML frontmatter for discoverability
- Auto-activation via skill-rules.json
- Progressive disclosure (resources/ subdirectory)
- 500-line rule (SKILL.md < 500 lines)

**Example structure:**
```
.claude/skills/python-development/
├── SKILL.md (250-500 lines)
│   ├── Quick start
│   ├── Core patterns
│   └── Links to resources
└── resources/
    ├── async-patterns.md (400 lines)
    ├── testing.md (350 lines)
    └── error-handling.md (300 lines)
```

**📘 Complete Reference:** `@resources/skill-activation.md`

---

### 2. Agents (AGENT.md)

**Purpose:** Specialized AI agents for specific tasks

**Location:** `.claude/agents/<agent-name>.md`

**Agent Types:**
- **general-purpose** - General tasks, all tools
- **Explore** - Fast codebase exploration
- **Plan** - Software architecture planning
- **claude-code-guide** - Claude Code documentation expert
- **Specialist** - Domain-specific experts

**When to use agents:**
- Complex multi-step tasks
- Open-ended searches requiring multiple rounds
- Architecture design
- Code exploration and analysis

**Example:**
```markdown
# Claude Code Expert

**Agent Type:** Specialist
**Model:** claude-sonnet-4
**Priority:** High

## Capabilities
1. Design Claude Code infrastructure
2. Create skills with auto-activation
3. Implement production hooks
4. Optimize token efficiency
5. Troubleshoot issues
```

**📘 Complete Reference:** `@resources/agent-types.md`

---

### 3. Hooks

**Purpose:** Deterministic automation at workflow points

**Location:** `.claude/hooks/<event-name>/`

**Hook Events:**
1. **SessionStart** - Initial setup, context loading
2. **UserPromptSubmit** - Skill activation (BREAKTHROUGH)
3. **PreToolUse** - Validation, blocking, transformation
4. **PostToolUse** - Tracking, formatting, notifications
5. **Stop** - Quality validation, reminders

**Hook Types:**
- **Shell** - Execute shell scripts (fast, deterministic)
- **LLM** - Use Claude for analysis (flexible, slower)

**Example:**
```typescript
// .claude/hooks/UserPromptSubmit/skill-activation.ts
// Analyzes user prompt and suggests relevant skills
export async function skillActivationPrompt(prompt: string) {
  const skills = await loadSkillRules();
  const matches = findMatchingSkills(prompt, skills);
  return formatSuggestions(matches);
}
```

**📘 Complete Reference:** `@resources/hook-system.md`

---

### 4. Commands

**Purpose:** Custom slash commands for common workflows

**Location:** `.claude/commands/<command-name>.md`

**Usage:**
```
/command-name [options]
```

**Best practices:**
- Keep commands <200 lines
- Focus on specific workflows
- Link to detailed references
- Provide examples

**Example:**
```markdown
# KB Create

Create new knowledge base entries.

## Usage
```
/kb-create [options]
```

## Quick Examples
```
/kb-create --scope python --category async
```

**📘 Complete Workflow:** `@references/workflows.md`
```

---

### 5. Standards

**Purpose:** Single source of truth for team standards

**Location:** `.claude/standards/`

**Common Standards:**
- `git-workflow.md` - Commit conventions, branching
- `yaml-standards.md` - Entry format, ID structure
- `quality-gates.md` - Validation requirements

**Key principle:** Reference standards from multiple locations, don't duplicate.

---

### 6. References

**Purpose:** Detailed documentation on-demand

**Location:** `.claude/references/`

**Common References:**
- `cli-reference.md` - Complete CLI documentation
- `architecture.md` - System architecture details
- `workflows.md` - Critical workflows

**Key principle:** Progressive disclosure - link from SKILL.md, commands, CLAUDE.md.

---

## Component Interactions

### How Components Work Together

**1. Session Start Flow:**
```
Claude starts
  → Loads CLAUDE.md (always loaded)
  → Loads skill YAML frontmatter (metadata only)
  → Triggers SessionStart hooks
  → Loads agent instructions (if agent specified)
```

**2. User Prompt Flow:**
```
User submits prompt
  → Triggers UserPromptSubmit hooks
  → skill-activation hook analyzes prompt
  → Suggests relevant skills (based on skill-rules.json)
  → Claude accepts/rejects suggestions
  → Full skill content loaded on acceptance
```

**3. Tool Use Flow:**
```
Claude calls tool (Read, Write, Bash, etc.)
  → Triggers PreToolUse hooks
    → Validation, blocking, transformation
  → Tool executes
  → Triggers PostToolUse hooks
    → Formatting, tracking, notifications
```

**4. Session End Flow:**
```
User finishes session
  → Triggers Stop hooks
  → Quality validation
  → Reminders (forgotten pushes, etc.)
  → Session ends
```

**📘 Complete System Overview:** `@resources/system-overview.md`

---

## Auto-Activation System

### BREAKTHROUGH Pattern from Production

**Key innovation:** Skills can suggest themselves based on user intent.

**How it works:**

1. **skill-rules.json** - Defines trigger patterns
2. **UserPromptSubmit hook** - Analyzes user prompt
3. **Pattern matching** - Finds relevant skills
4. **Priority system** - critical → high → medium → low
5. **Suggestion format** - "Based on your request, consider using: X, Y, Z"

**skill-rules.json Schema:**
```json
{
  "python-development": {
    "type": "domain",
    "priority": "high",
    "description": "Python development patterns",
    "promptTriggers": {
      "keywords": ["python", "async", "pytest"],
      "intentPatterns": [
        "(create|add).*?python.*?(function|class)",
        "python.*?(async|await|decorator)"
      ],
      "fileTriggers": {
        "pathPatterns": ["**/*.py"],
        "contentPatterns": ["import asyncio", "from fastapi"]
      }
    }
  }
}
```

**📘 Complete Auto-Activation Guide:** `@resources/skill-activation.md`

---

## Progressive Disclosure Pattern

### Token Efficiency Strategy

**Problem:** Loading all documentation at startup is expensive.

**Solution:** Load metadata at startup, full content on-demand.

**Implementation:**

**At Session Start (metadata only):**
```yaml
---
name: "python-development"
description: "Python patterns and best practices"
version: "1.0"
tags: ["python", "async", "testing"]
resources:
  - "resources/async.md"
  - "resources/testing.md"
---
```
**Token cost:** ~50 tokens per skill

**On Demand (when needed):**
- SKILL.md: ~2,000 tokens
- Resources: ~3,000 tokens each

**Benefits:**
- Session start: <500 tokens (vs 5,000+)
- Load full content only when needed
- **Savings: 70%+ vs loading everything**

**📘 Complete Progressive Disclosure Guide:** `@resources/progressive-disclosure.md`

---

## Quick Reference

### File Locations

| Component | Location | Purpose |
|-----------|----------|---------|
| **CLAUDE.md** | `.claude/CLAUDE.md` | Project memory (always loaded) |
| **Skills** | `.claude/skills/<name>/SKILL.md` | Reusable capabilities |
| **Agents** | `.claude/agents/<name>.md` | Specialized AI |
| **Hooks** | `.claude/hooks/<event>/` | Automation |
| **Commands** | `.claude/commands/<name>.md` | Slash commands |
| **Standards** | `.claude/standards/` | Team standards |
| **References** | `.claude/references/` | Detailed docs |

### Best Practices

1. **SKILL.md < 500 lines** - Move details to resources/
2. **Commands < 200 lines** - Link to references/
3. **CLAUDE.md ~300 lines** - Navigation hub only
4. **YAML frontmatter on all skills** - Discoverability
5. **Single source of truth** - Reference standards, don't duplicate
6. **Progressive disclosure** - Metadata at startup, full content on-demand
7. **Auto-activation** - Use skill-rules.json for skill suggestions

### Common Patterns

**Modular Skill Pattern:**
```
skill-name/
├── SKILL.md (300-500 lines)
│   ├── Quick start
│   ├── Core patterns
│   ├── Essential examples
│   └── Links to resources
└── resources/
    ├── detailed-topic-1.md (400 lines)
    ├── detailed-topic-2.md (350 lines)
    └── detailed-topic-3.md (450 lines)
```

**Token Efficiency:**
- Metadata at startup: ~50 tokens
- SKILL.md on-demand: ~2,000 tokens
- Resources on-demand: ~3,000 tokens each

---

## Production-Tested Patterns

**From diet103 showcase (6 months, 50K+ lines TypeScript):**

1. **Auto-Activation System** - skill-rules.json + UserPromptSubmit hook
2. **500-Line Rule** - Modular skills with resources/
3. **Progressive Disclosure** - 70%+ token savings
4. **Hook Automation** - Deterministic workflow enhancement
5. **Specialized Agents** - Domain-specific expertise
6. **Token Optimization** - <500 tokens at session start

**📘 Complete System Overview:** `@resources/system-overview.md`

---

## Related Resources

**Internal:**
- `@resources/system-overview.md` - Complete Claude Code architecture
- `@resources/skill-activation.md` - Auto-activation deep dive
- `@resources/hook-system.md` - Hook events and patterns
- `@resources/progressive-disclosure.md` - Progressive disclosure patterns
- `@resources/agent-types.md` - Different agent types and use cases

**Shared KB:**
- `universal/patterns/claude-code-files-organization-001.yaml` - Complete organization guide
- `universal/patterns/claude-code-hooks.yaml` - Hooks pattern
- `universal/patterns/claude-code-shared-model.yaml` - Team knowledge model

**External:**
- [Claude Code Documentation](https://claude.com/claude-code)
- [Claude Agent SDK](https://docs.anthropic.com/claude-agent-sdk)

---

## Quality Checklist

**When creating Claude Code architecture:**

- [ ] Applied progressive disclosure (metadata at startup)
- [ ] SKILL.md < 500 lines
- [ ] Commands < 200 lines
- [ ] YAML frontmatter on all skills
- [ ] skill-rules.json for auto-activation
- [ ] Single source of truth (standards/, references/)
- [ ] Token efficiency <500 tokens at session start
- [ ] Hooks for workflow automation
- [ ] Integration with Shared KB

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** diet103 Claude Code Infrastructure Showcase
**Quality Score:** 95/100
