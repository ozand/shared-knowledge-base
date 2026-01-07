# Claude Code System Overview

Complete architecture and component interactions of Claude Code infrastructure.

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude Code CLI                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Skills     │  │   Agents     │  │  Commands    │     │
│  │              │  │              │  │              │     │
│  │ • Auto-act.  │  │ • Specialist │  │ • Slash cmd  │     │
│  │ • Progressive│  │ • General    │  │ • Workflows  │     │
│  │ • Resources  │  │ • Explore    │  │ • Quick ops  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│          │                  │                  │            │
│          └──────────────────┴──────────────────┘            │
│                            │                                │
│  ┌──────────────┐  ┌───────┴───────┐  ┌──────────────┐     │
│  │    Hooks     │  │   Standards   │  │  References  │     │
│  │              │  │               │  │              │     │
│  │ • Events     │  │ • Git workflow│  │ • CLI docs   │     │
│  │ • Automation │  │ • YAML format │  │ • Architecture│     │
│  │ • Validation │  │ • Quality     │  │ • Workflows  │     │
│  └──────────────┘  └───────────────┘  └──────────────┘     │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│                      CLAUDE.md                               │
│                   (Project Memory)                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Shared Knowledge Base                      │
│                                                              │
│  • KB entries (YAML)                                        │
│  • Patterns (universal/patterns/)                           │
│  • Documentation (docs/research/)                           │
│  • CLI tools (tools/kb.py)                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Skills System

**Purpose:** Provide reusable capabilities that can be auto-activated based on user intent.

**Location Structure:**
```
.claude/skills/
├── python-development/
│   ├── SKILL.md (300-500 lines)
│   └── resources/
│       ├── async-patterns.md
│       ├── testing.md
│       └── error-handling.md
├── fastapi-development/
│   ├── SKILL.md
│   └── resources/
└── claude-code-architecture/
    ├── SKILL.md
    └── resources/
        ├── system-overview.md (this file)
        ├── skill-activation.md
        ├── hook-system.md
        ├── progressive-disclosure.md
        └── agent-types.md
```

**Skill Lifecycle:**

1. **Session Start:**
   - Load YAML frontmatter (metadata only)
   - Token cost: ~50 tokens per skill
   - Skills become discoverable

2. **User Prompt:**
   - UserPromptSubmit hook analyzes prompt
   - skill-rules.json pattern matching
   - Relevant skills suggested
   - User accepts/rejects

3. **Skill Activation:**
   - Full SKILL.md loaded (~2,000 tokens)
   - Resources/ available on-demand
   - Knowledge applied to task

**Key Features:**
- **Auto-activation** - Suggests itself based on user intent
- **Progressive disclosure** - Metadata first, details on-demand
- **Modular** - SKILL.md + resources/ structure
- **500-line rule** - Main file <500 lines
- **YAML frontmatter** - Discoverability metadata

---

### 2. Agents System

**Purpose:** Specialized AI agents for specific types of tasks.

**Agent Types:**

**1. general-purpose**
- Description: General tasks with access to all tools
- Tools: All tools available
- Use cases: Open-ended tasks, research, multi-step operations
- Model: Any (Sonnet, Opus, Haiku)

**2. Explore**
- Description: Fast agent specialized for codebase exploration
- Tools: All tools available
- Use cases: Finding files, searching code, understanding architecture
- Thoroughness levels: quick, medium, very thorough
- Model: Prefer Haiku for speed

**3. Plan**
- Description: Software architect agent for implementation planning
- Tools: All tools available
- Use cases: Designing implementation strategies, architecture decisions
- Model: Sonnet or Opus (for complex tasks)

**4. claude-code-guide**
- Description: Expert on Claude Code features, hooks, skills, MCP servers
- Tools: Glob, Grep, Read, WebFetch, WebSearch
- Use cases: Questions about Claude Code capabilities
- Model: Any

**5. glm-plan-usage:usage-query**
- Description: Query GLM Coding Plan usage statistics
- Tools: Bash, Read, Skill, Glob, Grep
- Use cases: Usage analytics, triggered by /glm-plan-usage:usage-query

**6. Specialist Agents**
- Custom agents for specific domains
- Examples: code-architecture-reviewer, refactor-planner, documentation-architect
- Location: `.claude/agents/<agent-name>.md`

**Agent Specification:**
```markdown
# Agent Name

**Agent Type:** Specialist
**Model:** claude-sonnet-4
**Priority:** High

## Purpose
Brief description of what this agent does

## When to Use
- Trigger pattern 1
- Trigger pattern 2
- Trigger pattern 3

## Capabilities
1. Capability 1
2. Capability 2
3. Capability 3

## Knowledge Sources
- Shared KB entry 1
- Shared KB entry 2
- Official documentation

## Interaction Patterns
### Pattern 1
Description and example

## Quality Standards
- Standard 1
- Standard 2
```

**Agent Invocation:**
- Automatic based on task type
- Manual via Task tool
- Can run in background
- Can be resumed with agent ID

---

### 3. Hooks System

**Purpose:** Deterministic automation at specific workflow points.

**Hook Events:**

**1. SessionStart**
- When: When Claude Code session starts
- Use cases: Initial setup, context loading, environment checks
- Example: Load project context, validate environment
- Performance: Should complete <2 seconds

**2. UserPromptSubmit**
- When: After user submits prompt, before Claude processes it
- Use cases: **Skill activation** (BREAKTHROUGH), prompt enhancement
- Example: skill-activation-prompt hook suggests relevant skills
- Performance: Should complete <1 second (don't block user)

**3. PreToolUse**
- When: Before any tool call (Read, Write, Bash, etc.)
- Use cases: Validation, blocking, transformation
- Example: Validate YAML before Write operation, block dangerous commands
- Performance: Should complete <500ms (tool call latency)

**4. PostToolUse**
- When: After successful tool call
- Use cases: Tracking, formatting, notifications
- Example: Track tool usage, format output, send notifications
- Performance: Should complete <1 second (async preferred)

**5. Stop**
- When: When Claude finishes session
- Use cases: Quality validation, reminders
- Example: error-handling-reminder checks for unresolved errors
- Performance: Non-blocking, can take longer

**Hook Types:**

**1. Shell Hooks**
- File extension: `.sh`
- Permissions: Must be executable (`chmod +x`)
- Advantages: Fast, deterministic, predictable
- Best for: Validation, formatting, simple transformations
- Example:
  ```bash
  #!/bin/bash
  # .claude/hooks/PreToolUse/yaml-validation.sh
  FILE_PATH="$1"
  if [[ "$FILE_PATH" == *.yaml ]]; then
    python tools/kb.py validate "$FILE_PATH"
  fi
  ```

**2. LLM Hooks**
- File extension: `.ts`, `.js`, `.py`
- Advantages: Flexible, can analyze context, make decisions
- Best for: Skill activation, prompt enhancement, complex analysis
- Example:
  ```typescript
  // .claude/hooks/UserPromptSubmit/skill-activation.ts
  export async function skillActivationPrompt(prompt: string) {
    const skills = await loadSkillRules();
    const matches = findMatchingSkills(prompt, skills);
    return formatSuggestions(matches);
  }
  ```

**Hook Configuration:**
```json
// .claude/settings.json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "shell",
        "path": ".claude/hooks/SessionStart/setup-env.sh"
      }
    ],
    "UserPromptSubmit": [
      {
        "type": "llm",
        "path": ".claude/hooks/UserPromptSubmit/skill-activation.ts"
      }
    ],
    "PreToolUse": [
      {
        "type": "shell",
        "path": ".claude/hooks/PreToolUse/yaml-validation.sh"
      }
    ],
    "PostToolUse": [
      {
        "type": "shell",
        "path": ".claude/hooks/PostToolUse/tool-tracker.sh"
      }
    ],
    "Stop": [
      {
        "type": "llm",
        "path": ".claude/hooks/Stop/error-handling-reminder.ts"
      }
    ]
  }
}
```

**Best Practices:**
1. Keep hooks fast (<2 seconds for SessionStart, <1 second for others)
2. Handle errors gracefully (don't break workflow)
3. Test thoroughly before deploying
4. Use shell hooks for simple, fast operations
5. Use LLM hooks for complex analysis requiring context

---

### 4. Commands System

**Purpose:** Custom slash commands for common workflows.

**Location:** `.claude/commands/<command-name>.md`

**Command Structure:**
```markdown
# Command Name

Brief description (1-2 sentences).

## Usage
```
/command-name [options]
```

## Quick Examples

### Example 1
```
/command-name --option value
```
Description

### Example 2
```
/command-name
```
Description

## What This Command Does

1. Step 1
2. Step 2
3. Step 3

**📘 Detailed Guide:** `@references/some-reference.md`

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `--opt` | Description | `--opt value` |

## Workflow

### Step 1: Name
Description

### Step 2: Name
Description

## Output

**Success:**
```
✅ Success message
```

**Error:**
```
❌ Error message
```

## Common Patterns

### Pattern 1
```
/command-name pattern
```

## Related
- `@skills/some-skill/SKILL.md`
- `@standards/some-standard.md`
```

**Best Practices:**
- Keep commands <200 lines
- Focus on specific workflows
- Provide quick examples
- Link to detailed references
- Clear success/error output

**Command Discovery:**
- Commands listed in `/help`
- Can be invoked with `/command-name`
- Auto-complete support
- Can have options and arguments

---

### 5. Standards System

**Purpose:** Single source of truth for team standards and workflows.

**Location:** `.claude/standards/`

**Common Standards:**

**1. git-workflow.md**
- Commit message format (GITHUB-ATTRIB-001)
- Branching strategy
- Pull request guidelines
- Code review standards

**2. yaml-standards.md**
- Entry structure and format
- ID format (CATEGORY-NNN)
- Required vs optional fields
- Code example standards
- Quality requirements

**3. quality-gates.md**
- Minimum quality score (75/100)
- Validation requirements
- Testing standards
- Documentation requirements

**4. workflow-standards.md**
- Error reporting workflow
- Scope decision criteria
- Synchronization process
- Troubleshooting procedures

**Key Principle:**
- Define standards once
- Reference from multiple locations (skills, commands, CLAUDE.md)
- No duplication
- Single source of truth

**Example Usage:**
```markdown
In SKILL.md:
**📘 YAML Standards:** `@standards/yaml-standards.md`

In command:
**📘 Complete Workflow:** `@standards/workflow-standards.md`

In CLAUDE.md:
**📘 Git Workflow:** `@standards/git-workflow.md`
```

---

### 6. References System

**Purpose:** Detailed documentation available on-demand.

**Location:** `.claude/references/`

**Common References:**

**1. cli-reference.md**
- Complete CLI command documentation
- All `kb.py` commands with options
- Metadata commands
- Version monitoring
- Predictive analytics
- Usage examples

**2. architecture.md**
- Hierarchical knowledge organization
- Directory structure
- Search technology (SQLite FTS5)
- Metadata architecture
- Component interactions

**3. workflows.md**
- Error reporting workflow
- Scope decision criteria
- Quality validation workflow
- Synchronization workflow
- Troubleshooting procedures

**4. hooks-reference.md**
- All hook events documented
- Hook patterns and examples
- Performance considerations
- Best practices

**5. skills-reference.md**
- Skill development guide
- Auto-activation system
- Progressive disclosure patterns
- Resource organization

**Key Principle:**
- Comprehensive documentation
- Linked from skills, commands, CLAUDE.md
- Progressive disclosure (details on-demand)
- Maintainable and updatable

---

## Component Interactions

### Session Start Flow

```
1. Claude Code starts
   ↓
2. Load CLAUDE.md (always loaded, ~300 lines, ~2,000 tokens)
   ↓
3. Scan .claude/skills/ for YAML frontmatter
   → Load metadata only (~50 tokens per skill)
   → SKILL.md not loaded yet
   ↓
4. Execute SessionStart hooks
   → Setup environment
   → Load initial context
   → Validate configuration
   ↓
5. Ready for user input

Total token cost: ~2,000 + (N × 50) tokens
For 10 skills: ~2,500 tokens
```

### User Prompt Flow

```
1. User submits prompt
   ↓
2. Trigger UserPromptSubmit hooks
   ↓
3. skill-activation hook (LLM)
   → Load skill-rules.json
   → Analyze user prompt
   → Match against trigger patterns:
     • Keywords
     • Intent patterns (regex)
     • File path patterns
     • File content patterns
   ↓
4. Rank matches by priority
   → critical > high > medium > low
   ↓
5. Format suggestions
   → "Based on your request, consider using: X, Y, Z"
   ↓
6. User accepts/rejects suggestions
   ↓
7. If accepted, load full SKILL.md (~2,000 tokens)
   → Resources/ available on-demand
   ↓
8. Claude processes prompt with skill knowledge
```

### Tool Use Flow

```
1. Claude decides to use tool (Read, Write, Bash, etc.)
   ↓
2. Trigger PreToolUse hooks
   ↓
3. Validation hook (shell)
   → Check file type
   → Validate syntax
   → Potentially block operation
   ↓
4. Tool executes
   ↓
5. Trigger PostToolUse hooks
   ↓
6. Tracking hook (shell)
   → Log tool usage
   → Format output
   → Send notifications
   ↓
7. Return result to Claude
```

### Session End Flow

```
1. User finishes session (or timeout)
   ↓
2. Trigger Stop hooks
   ↓
3. Quality validation hook (LLM)
   → Check for unresolved errors
   → Validate work completed
   → Check for forgotten operations
   ↓
4. Reminder hook (LLM)
   → "You forgot to push changes"
   → "Uncommitted changes detected"
   → "Consider creating KB entry"
   ↓
5. Session cleanup
   ↓
6. Session ends
```

---

## Data Flow

### Knowledge Flow

```
Shared KB (YAML entries)
    ↓
  Claude learns
    ↓
  Claude applies to task
    ↓
  Claude validates solution
    ↓
  Claude documents in YAML
    ↓
  Claude validates entry (kb.py validate)
    ↓
  Claude commits to git
    ↓
  Knowledge added to Shared KB
```

### Skill Activation Flow

```
User intent (prompt)
    ↓
  UserPromptSubmit hook
    ↓
  skill-rules.json (pattern matching)
    ↓
  Relevant skills identified
    ↓
  Ranked by priority
    ↓
  Suggestions presented
    ↓
  User acceptance
    ↓
  Full skill loaded
    ↓
  Knowledge applied
```

### Progressive Disclosure Flow

```
Session Start
    ↓
  Load YAML frontmatter (metadata)
    ↓
  Low token cost (~50 tokens/skill)
    ↓
  User triggers task
    ↓
  Load full SKILL.md (~2,000 tokens)
    ↓
  User needs details
    ↓
  Load resource files (~3,000 tokens each)
    ↓
  Complete knowledge available
```

---

## Performance Considerations

### Token Efficiency Targets

**Session Start:**
- CLAUDE.md: ~2,000 tokens (~300 lines)
- Skills metadata: ~50 tokens per skill
- Total for 10 skills: ~2,500 tokens
- **Target: <3,000 tokens**

**On-Demand Loading:**
- Full SKILL.md: ~2,000 tokens
- Resource file: ~3,000 tokens each
- Loaded only when needed
- **Savings: 70%+ vs loading everything**

### Hook Performance

**Critical Performance Requirements:**

| Hook Event | Max Duration | Reason |
|------------|--------------|---------|
| **SessionStart** | 2 seconds | Session startup latency |
| **UserPromptSubmit** | 1 second | Don't block user input |
| **PreToolUse** | 500ms | Tool call latency |
| **PostToolUse** | 1 second | Can be async |
| **Stop** | Non-blocking | Session ending anyway |

**Optimization Strategies:**
1. Use shell hooks for fast, deterministic operations
2. Use LLM hooks only when necessary (complex analysis)
3. Cache expensive operations
4. Implement timeouts
5. Handle errors gracefully

---

## Best Practices

### 1. Progressive Disclosure

**Always apply:**
- SKILL.md <500 lines
- resources/ for detailed content
- YAML frontmatter for metadata
- Links to references

**Benefits:**
- 70%+ token savings
- Faster session start
- Better organization
- Improved discoverability

### 2. Auto-Activation

**Implement:**
- skill-rules.json configuration
- UserPromptSubmit hook
- Pattern matching (keywords, intent, files, content)
- Priority system

**Benefits:**
- Skills suggest themselves
- Better user experience
- Reduced manual skill selection
- Context-aware assistance

### 3. Single Source of Truth

**Apply:**
- Standards in standards/
- References in references/
- Link from multiple locations
- No duplication

**Benefits:**
- Easier maintenance
- Consistent information
- Single place to update
- Reduced confusion

### 4. Token Optimization

**Targets:**
- CLAUDE.md: ~300 lines
- Commands: <200 lines
- Skills: 300-500 lines (SKILL.md only)
- Resources: Unlimited (on-demand)

**Benefits:**
- Faster performance
- Lower costs
- Better user experience
- Scalable to large projects

---

## Quality Metrics

### Token Efficiency

**Good:**
- Session start <3,000 tokens
- Progressive disclosure applied
- Skills <500 lines
- Commands <200 lines

**Needs Improvement:**
- Session start >5,000 tokens
- No progressive disclosure
- Large skills (>600 lines)
- Oversized commands (>300 lines)

### Organization Quality

**Good:**
- Clear directory structure
- Standards and references separated
- Progressive disclosure throughout
- YAML frontmatter on all skills

**Needs Improvement:**
- Mixed file types in directories
- Duplication of content
- No YAML frontmatter
- Everything loaded at startup

---

## Troubleshooting

### Issue: High Token Usage

**Symptoms:**
- Session start >5,000 tokens
- Context limits hit frequently

**Solutions:**
1. Apply progressive disclosure
2. Move content to resources/
3. Link to references/
4. Reduce CLAUDE.md size
5. Optimize oversized commands

### Issue: Skills Not Activating

**Symptoms:**
- Skills don't suggest themselves
- Auto-activation not working

**Solutions:**
1. Check skill-rules.json exists
2. Verify JSON syntax
3. Check skill name matches
4. Verify UserPromptSubmit hook registered
5. Test trigger patterns

### Issue: Hooks Not Firing

**Symptoms:**
- Hooks not executing
- No automation happening

**Solutions:**
1. Check hook permissions (executable)
2. Verify hook registered in settings.json
3. Test hook manually
4. Check console for errors
5. Verify correct event selected

---

## Related Resources

**Internal:**
- `@resources/skill-activation.md` - Auto-activation deep dive
- `@resources/hook-system.md` - Hook events and patterns
- `@resources/progressive-disclosure.md` - Progressive disclosure patterns
- `@resources/agent-types.md` - Agent types and use cases

**Shared KB:**
- `universal/patterns/claude-code-files-organization-001.yaml` - Organization guide
- `universal/patterns/claude-code-hooks.yaml` - Hooks pattern

**External:**
- [Claude Code Documentation](https://claude.com/claude-code)
- [Claude Agent SDK](https://docs.anthropic.com/claude-agent-sdk)

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** diet103 Claude Code Infrastructure Showcase
