# Agent Types

Complete guide to Claude Code agent types and their use cases.

---

## Overview

**What are Agents?**

Agents are specialized AI assistants configured for specific types of tasks. Each agent type has access to different tools and is optimized for particular workflows.

**Key Characteristics:**
- **Specialized** - Optimized for specific tasks
- **Tool access** - Different agents have different tools
- **Model selection** - Can specify Sonnet, Opus, or Haiku
- **Invocation** - Can be auto-invoked or manual
- **Resumable** - Can be resumed with agent ID

---

## Agent Types

### 1. general-purpose

**Description:** General tasks with access to all tools

**Tools:** All tools available
- Read, Write, Edit, Bash
- Glob, Grep, LSP
- Task, TodoWrite
- AskUserQuestion, EnterPlanMode
- All MCP servers

**Use Cases:**
- Open-ended tasks requiring multiple tools
- Multi-step operations
- Complex workflows
- Research requiring search and analysis
- Tasks where you don't know what tools will be needed

**Model:** Any (Sonnet recommended for balance)

**Example Invocation:**
```typescript
// Automatically invoked by Claude Code for complex tasks
```

**When to use:**
- Task is complex and open-ended
- Multiple types of operations needed (read, write, search)
- Not sure which specialist agent to use
- Task requires full tool access

---

### 2. Explore

**Description:** Fast agent specialized for codebase exploration

**Tools:** All tools available

**Thoroughness Levels:**
- **quick** - Fast search, find files quickly
- **medium** - Balanced search (default)
- **very thorough** - Comprehensive search, multiple locations

**Model:** Prefer Haiku for speed

**Use Cases:**
- Finding files by pattern (e.g., "all React components")
- Searching code for keywords
- Understanding codebase structure
- Answering "where is X used?" questions
- Finding all occurrences of a pattern

**Example Invocations:**

**Quick exploration:**
```
"Find all TypeScript files in src/"
```
→ Uses Haiku, fast search

**Medium exploration:**
```
"Search for all database connection code"
```
→ Uses Sonnet, balanced search

**Very thorough exploration:**
```
"Find every place we handle user authentication"
```
→ Uses Opus, comprehensive search across all files

**When to use:**
- Need to find files or code patterns
- Understanding codebase structure
- "Where is X used?" questions
- Don't need to modify code, just explore

**When NOT to use:**
- Need to modify files (use general-purpose)
- Need architecture planning (use Plan)
- Need Claude Code documentation (use claude-code-guide)

---

### 3. Plan

**Description:** Software architect agent for implementation planning

**Tools:** All tools available

**Specialization:**
- Architecture design
- Implementation strategy
- Step-by-step planning
- Trade-off analysis
- Dependency identification

**Model:** Sonnet or Opus (Opus for complex architecture)

**Use Cases:**
- Designing implementation strategy for a task
- Breaking down large features into steps
- Architecture decisions (e.g., "state management approach")
- Multi-file changes requiring coordination
- Tasks with multiple valid approaches

**Example Invocation:**
```
"I need to add user authentication to my app"
```
→ Plan agent analyzes codebase
→ Identifies authentication options
→ Presents trade-offs
→ Creates implementation plan
→ Waits for user approval

**Plan Output:**
```markdown
# Implementation Plan: User Authentication

## Approach Options

### Option 1: JWT Tokens
- Pros: Stateless, scalable
- Cons: Token revocation complexity
- Implementation steps: ...

### Option 2: Session-Based
- Pros: Simple, easy to revoke
- Cons: Server-side state
- Implementation steps: ...

## Recommended Approach: JWT Tokens

## Implementation Steps
1. Install dependencies
2. Create auth middleware
3. Add login endpoint
4. Protect routes
5. Add token refresh

## Files to Modify
- src/api/auth.py (new)
- src/middleware/auth.py (new)
- src/api/routes.py (modify)
```

**When to use:**
- Complex tasks requiring planning
- Multiple valid approaches exist
- Need architecture decisions
- Multi-file changes
- User asks "how should I implement X?"

**When NOT to use:**
- Simple, straightforward tasks
- Single file changes
- Clear, well-defined requirements
- Just need to execute, not plan

---

### 4. claude-code-guide

**Description:** Expert on Claude Code features, hooks, skills, MCP servers

**Tools:**
- Glob (find files)
- Grep (search files)
- Read (read files)
- WebFetch (fetch documentation)
- WebSearch (search web)

**Specialization:**
- Claude Code CLI features
- Hooks system (events, implementation)
- Skills system (auto-activation, progressive disclosure)
- Agents system (types, invocation)
- MCP servers (installation, configuration)
- Commands (creation, usage)

**Use Cases:**
- "How do I create a skill?"
- "What are hooks in Claude Code?"
- "How do I set up auto-activation?"
- "What's the difference between agents?"
- "How do I install an MCP server?"

**Example Invocation:**
```
"How do I create a skill with auto-activation?"
```
→ Explains skill creation process
→ Provides skill-rules.json example
→ Shows YAML frontmatter format
→ Links to documentation

**When to use:**
- Questions about Claude Code capabilities
- Need help with Claude Code configuration
- "Can Claude Code do X?"
- How-to questions about Claude Code

**When NOT to use:**
- Working on non-Claude-Code tasks
- Need to modify files (use general-purpose)
- Need to search codebase (use Explore)

---

### 5. glm-plan-usage:usage-query

**Description:** Query GLM Coding Plan usage statistics

**Tools:**
- Bash (execute commands)
- Read (read files)
- Skill (invoke skills)
- Glob (find files)
- Grep (search files)

**Specialization:**
- Usage analytics for GLM Coding Plan
- Account usage information
- Triggered by command: `/glm-plan-usage:usage-query`

**Use Cases:**
- Check current usage statistics
- Query account limits
- Monitor token consumption
- Usage reporting

**Example Invocation:**
```
/glm-plan-usage:usage-query
```
→ Returns current usage statistics
→ Shows remaining quota
→ Displays usage trends

**When to use:**
- Need to check GLM Coding Plan usage
- Monitoring token consumption
- Usage reporting

**When NOT to use:**
- Not using GLM Coding Plan
- General usage questions

---

### 6. Specialist Agents

**Description:** Custom agents for specific domains

**Location:** `.claude/agents/<agent-name>.md`

**Examples from Production:**

**code-architecture-reviewer**
- Reviews code architecture
- Identifies design patterns
- Suggests improvements
- Tools: All tools
- Model: Sonnet or Opus

**refactor-planner**
- Plans refactoring strategies
- Identifies code smells
- Suggests refactoring steps
- Tools: All tools
- Model: Sonnet

**documentation-architect**
- Designs documentation structure
- Creates documentation plans
- Suggests documentation tools
- Tools: Read, Glob, Grep, WebFetch, WebSearch
- Model: Sonnet

**auto-error-resolver**
- Resolves errors automatically
- Searches KB for solutions
- Applies fixes
- Tools: All tools
- Model: Sonnet

**plan-reviewer**
- Reviews implementation plans
- Identifies missing steps
- Suggests improvements
- Tools: All tools
- Model: Opus

**frontend-error-fixer**
- Fixes frontend errors
- Debugs React, Vue, Angular issues
- Tools: All tools
- Model: Sonnet

**Creating Specialist Agents:**

See `.claude/agents/claude-code-expert.md` for complete agent specification template.

---

## Agent Selection Guide

### Decision Tree

```
Start
  │
  ├─ Question about Claude Code?
  │   └─ YES → Use claude-code-guide
  │
  ├─ Need to explore codebase?
  │   └─ YES → Use Explore
  │       │
  │       ├─ Quick search needed?
  │       │   └─ YES → Use Explore with thoroughness: quick
  │       │
  │       └─ Comprehensive search?
  │           └─ YES → Use Explore with thoroughness: very thorough
  │
  ├─ Complex task requiring planning?
  │   └─ YES → Use Plan
  │
  ├─ GLM usage query?
  │   └─ YES → Use glm-plan-usage:usage-query
  │
  └─ General task?
      └─ YES → Use general-purpose
```

### Use Case Matrix

| Task | Best Agent | Alternative |
|------|-----------|-------------|
| Find all files matching pattern | Explore | general-purpose |
| Search code for keyword | Explore | general-purpose |
| Understand codebase structure | Explore | - |
| Design implementation strategy | Plan | general-purpose |
| Architecture decisions | Plan | - |
| Create Claude Code skill | claude-code-guide | - |
| Understand hooks | claude-code-guide | - |
| Multi-step complex task | general-purpose | Plan |
| Single file edit | general-purpose | - |
| Code review | code-architecture-reviewer | general-purpose |
| Refactoring | refactor-planner | general-purpose |
| Documentation planning | documentation-architect | general-purpose |
| Error resolution | auto-error-resolver | general-purpose |

---

## Agent Invocation

### Automatic Invocation

Claude Code automatically selects appropriate agent based on task:

**Explore agent auto-invoked when:**
- Task is primarily search/exploration
- User asks "find all X", "where is X used?"
- No modifications needed

**Plan agent auto-invoked when:**
- User enters plan mode (EnterPlanMode tool)
- Task requires implementation strategy
- Multiple valid approaches exist

**general-purpose agent auto-invoked when:**
- Default for most tasks
- Complex multi-step operations
- Unclear which specialist to use

### Manual Invocation

Using Task tool:
```typescript
Task(
  subagent_type: "Explore",
  prompt: "Find all React components",
  model: "haiku"  // Optional
)
```

**Available subagent_type values:**
- "general-purpose"
- "Explore"
- "Plan"
- "claude-code-guide"
- "glm-plan-usage:usage-query"
- Specialist agent names

### Agent Resumption

After agent completes, you can resume with agent ID:
```typescript
Task(
  resume: "agent-id-from-previous-call",
  prompt: "Continue with next step"
)
```

---

## Agent Configuration

### Agent Specification

**Location:** `.claude/agents/<agent-name>.md`

**Template:**
```markdown
# Agent Name

Brief description (1-2 sentences).

**Agent Type:** Specialist
**Model:** claude-sonnet-4
**Priority:** High

## Purpose

Detailed description of what this agent does.

## When to Use

Trigger patterns:
- Pattern 1
- Pattern 2
- Pattern 3

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

**User:** "Example request"

**Agent response:**
1. Step 1
2. Step 2
3. Step 3

## Quality Standards

- Standard 1
- Standard 2
- Standard 3

## Related Resources

- Internal resource 1
- Internal resource 2
- External resource 3

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Quality Score:** 95/100
```

### Example: Claude Code Expert Agent

```markdown
# Claude Code Expert

Expert agent for Claude Code infrastructure, patterns, and best practices.

**Agent Type:** Specialist
**Model:** claude-sonnet-4 (primary), claude-opus-4 (complex tasks)
**Priority:** High

## Purpose

Deep knowledge of Claude Code infrastructure with integration to Shared Knowledge Base.

## When to Use

- User mentions "Claude Code", "skills", "hooks", "agents"
- Need to design .claude/ organization
- Creating skills with auto-activation
- Implementing hooks for automation
- Optimizing token efficiency
- Troubleshooting Claude Code issues
- Reviewing Claude Code setup

## Capabilities

1. **Design Claude Code Infrastructure**
   - Analyze project needs
   - Recommend .claude/ structure
   - Suggest skills, hooks, agents
   - Design skill-rules.json

2. **Create Skills with Auto-Activation**
   - Apply 500-line rule
   - Add YAML frontmatter
   - Create skill-rules.json entry
   - Implement resources/

3. **Implement Hooks**
   - Choose hook event
   - Implement shell/LLM hooks
   - Optimize performance
   - Test thoroughly

4. **Optimize Token Efficiency**
   - Analyze token usage
   - Apply progressive disclosure
   - Optimize file sizes
   - Achieve 70%+ savings

5. **Troubleshoot Issues**
   - Debug skill activation
   - Fix hook problems
   - Resolve token bloat

## Knowledge Sources

**Shared KB:**
- `claude-code-files-organization-001.yaml`
- `claude-code-hooks.yaml`
- `claude-code-shared-model.yaml`

**Standards:**
- `git-workflow.md`
- `yaml-standards.md`
- `quality-gates.md`

**Production Patterns:**
- diet103 showcase (6 months production)
- Auto-activation system
- 500-line rule
- Progressive disclosure

## Interaction Patterns

### Pattern 1: Infrastructure Design

**User:** "I need to set up Claude Code for my Python project"

**Agent response:**
1. Ask about project structure
2. Analyze tech stack
3. Recommend .claude/ organization
4. Suggest relevant skills (python, testing, async)
5. Propose useful hooks (validation, indexing)
6. Create implementation plan

### Pattern 2: Skill Creation

**User:** "Create a skill for FastAPI development"

**Agent response:**
1. Gather requirements
2. Check Shared KB for patterns
3. Create skill structure
4. Add YAML frontmatter
5. Create skill-rules.json entry
6. Implement auto-activation
7. Test activation

### Pattern 3: Troubleshooting

**User:** "My skills aren't activating"

**Agent response:**
1. Check skill-rules.json exists
2. Validate JSON syntax
3. Verify skill name matches
4. Check hook registered
5. Test trigger patterns
6. Provide fix

## Quality Standards

- Base solutions on Shared KB
- Reference showcase patterns
- Explain trade-offs
- Provide real examples
- Test recommendations
- Consider context

## Related Resources

- `@resources/system-overview.md`
- `@resources/skill-activation.md`
- `@resources/hook-system.md`
- `@resources/progressive-disclosure.md`

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** diet103 Claude Code Infrastructure Showcase
**Shared KB Integration:** Yes
```

---

## Model Selection

### Claude Sonnet 4

**Best for:**
- Most general-purpose tasks
- Complex reasoning
- Good balance of speed and intelligence
- Can handle multiple documentation sources

**Use when:**
- Default choice
- Need complex analysis
- Multiple sources to synthesize
- Balanced speed/intelligence

### Claude Opus 4

**Best for:**
- Most complex architecture tasks
- Deep analysis required
- Slower but more thorough
- Critical decisions

**Use when:**
- Sonnet struggles with task
- Most complex architecture
- Deep reasoning required
- Time permits slower execution

### Claude Haiku

**Best for:**
- Quick tasks
- Simple operations
- Fast response needed
- Explore agent (quick mode)

**Use when:**
- Simple, straightforward tasks
- Speed is critical
- Limited complexity
- Exploration tasks

---

## Best Practices

### 1. Agent Selection

**DO:**
- Use appropriate agent for task
- Consider task complexity
- Think about tools needed
- Use Explore for codebase searches
- Use Plan for architecture decisions

**DON'T:**
- Use general-purpose for everything (inefficient)
- Use Plan for simple tasks (overkill)
- Use Explore for modifications (wrong tool)
- Use claude-code-guide for non-Claude-Code tasks

### 2. Agent Configuration

**DO:**
- Specify agent purpose clearly
- Define when to use agent
- List knowledge sources
- Provide interaction patterns
- Include quality standards

**DON'T:**
- Create vague agent descriptions
- Forget to specify model
- Leave out use cases
- Omit knowledge sources

### 3. Agent Invocation

**DO:**
- Let Claude auto-select when appropriate
- Use manual invocation for specific needs
- Resume agents when possible
- Provide clear prompts

**DON'T:**
- Over-specify agent (let Claude decide)
- Invoke wrong agent for task
- Forget agent resumption capability
- Provide vague prompts

---

## Troubleshooting

### Issue: Wrong Agent Selected

**Symptoms:**
- Agent not suited for task
- Agent lacks necessary tools
- Task takes too long

**Solutions:**
1. Manually invoke correct agent
2. Be more specific in prompt
3. Use Task tool with subagent_type
4. Check agent capabilities

### Issue: Agent Not Available

**Symptoms:**
- Agent invocation fails
- "Agent not found" error

**Solutions:**
1. Check agent file exists
2. Verify agent name spelling
3. Check agent file syntax
4. Restart Claude Code

### Issue: Agent Performance Issues

**Symptoms:**
- Agent takes too long
- Agent doesn't complete task

**Solutions:**
1. Try different model (Haiku for speed)
2. Simplify task prompt
3. Break into smaller tasks
4. Use more appropriate agent

---

## Related Resources

**Internal:**
- `@resources/system-overview.md` - Complete system architecture
- `@resources/skill-activation.md` - Skill auto-activation
- `@resources/hook-system.md` - Hook implementation

**Shared KB:**
- `universal/patterns/claude-code-files-organization-001.yaml` - Organization guide

**External:**
- [Claude Code Documentation](https://claude.com/claude-code)
- [Claude Agent SDK](https://docs.anthropic.com/claude-agent-sdk)

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** diet103 Claude Code Infrastructure Showcase
