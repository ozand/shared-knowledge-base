# Autonomous Subagents System

**Version:** 1.0
**Last Updated:** 2026-01-07
**Status:** Production Ready

---

## Overview

The Autonomous Subagents System enables **multi-agent collaboration** where specialized subagents work autonomously to support primary agents in:

1. **Researching solutions** (Researcher Subagent)
2. **Analyzing errors** (Debugger Subagent)
3. **Validating fixes** (Validator Subagent)
4. **Capturing knowledge** (Knowledge Curator Subagent)

This creates a **self-improving system** where agents learn from their experiences and automatically build the Knowledge Base.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Primary Agent                         │
│              (Code Writer / Solver)                     │
│                                                         │
│  Working on task → Error encountered                   │
│         ↓                                               │
│  Launch subagents (autonomous)                          │
└─────────────────────────────────────────────────────────┘
         ↓                        ↓                    ↓
┌──────────────┐        ┌──────────────┐      ┌──────────────┐
│  Researcher  │        │   Debugger   │      │  Validator   │
│  (Parallel)  │        │  (Parallel)  │      │ (Sequential) │
│              │        │              │      │              │
│  Find        │        │  Analyze     │      │  Test        │
│  solutions   │        │  root cause  │      │  fixes       │
└──────────────┘        └──────────────┘      └──────────────┘
         ↓                        ↓                    ↓
         └────────────────────────┴────────────────────┘
                                 ↓
                    ┌──────────────────────┐
                    │ Knowledge Curator    │
                    │   (Sequential)       │
                    │                      │
                    │  Document findings   │
                    └──────────────────────┘
```

---

## Subagents

### 1. Researcher Subagent

**Role:** Web Research and Information Gathering
**File:** `.claude/agents/subagents/RESEARCHER.md`
**Execution:** Parallel (background)
**Triggers:** Error encountered, best practices needed

**Key Capabilities:**
- Web search (Stack Overflow, official docs, GitHub)
- Documentation lookup (Context7 MCP)
- Source code analysis (zread MCP)
- Multiple source correlation

**When to Use:**
- Agent encounters error and needs solution
- Best practices research
- Version compatibility checks
- Alternative solution exploration

**Example:**
```python
# Error detected - launch researcher
Task(
    subagent_type="researcher",
    prompt="Research solution for WebSocket timeout",
    context={"error": error, "urgency": "blocking"},
    run_in_background=True  # Parallel execution
)
```

---

### 2. Debugger Subagent

**Role:** Error Analysis and Root Cause Identification
**File:** `.claude/agents/subagents/DEBUGGER.md`
**Execution:** Parallel (background)
**Triggers:** Error detection, exception raised

**Key Capabilities:**
- Stack trace analysis
- Error type classification
- Root cause hierarchy (direct → systemic)
- Code context examination

**When to Use:**
- Need to understand why error occurred
- Analyze stack traces
- Examine code around error
- Identify patterns

**Example:**
```python
# Launch debugger in parallel with researcher
Task(
    subagent_type="debugger",
    prompt="Analyze this WebSocket timeout error",
    context={"stack_trace": traceback, "code": surrounding_code},
    run_in_background=True  # Parallel with researcher
)
```

---

### 3. Validator Subagent

**Role:** Solution Testing and Validation
**File:** `.claude/agents/subagents/VALIDATOR.md`
**Execution:** Sequential (blocking)
**Triggers:** Solution proposed, fix implemented

**Key Capabilities:**
- Functional testing
- Regression testing
- Code quality checks
- Performance validation
- Security checks

**When to Use:**
- Before applying fix to production
- After implementing solution
- To prevent regressions

**Example:**
```python
# Solution proposed - validate before applying
validation = Task(
    subagent_type="validator",
    prompt="Validate this WebSocket timeout fix",
    context={"solution": fix, "test_cases": tests},
    run_in_background=False  # Sequential - must wait
)

if validation.valid:
    apply_solution(fix)
else:
    research_alternative()
```

---

### 4. Knowledge Curator Subagent

**Role:** Knowledge Capture and Documentation
**File:** `.claude/agents/subagents/KNOWLEDGE-CURATOR.md`
**Execution:** Sequential (blocking)
**Triggers:** Task completion, error resolved, session end

**Key Capabilities:**
- Session analysis
- Knowledge categorization (Shared KB vs Project KB)
- Entry creation (GitHub issues or YAML)
- Quality validation

**When to Use:**
- After solving a problem
- After completing a feature
- At session end (retrospective)

**Example:**
```python
# Task completed - capture knowledge
Task(
    subagent_type="knowledge-curator",
    prompt="Analyze session and capture knowledge",
    context={
        "errors_encountered": errors,
        "solutions_found": solutions,
        "decisions_made": decisions
    },
    run_in_background=False  # Sequential - document after completion
)
```

---

## Execution Modes

### Parallel Execution (Background)

**Used for:** Researcher, Debugger

```python
# Launch subagent and continue working
task = Task(
    subagent_type="researcher",
    prompt="Research solution",
    run_in_background=True  # KEY: Background execution
)

# Primary agent continues with other tasks
do_other_unblocked_tasks()

# Get result when needed
result = TaskOutput(task.task_id, block=True)
```

**Benefits:**
- Primary agent not blocked
- Multiple subagents can work simultaneously
- Faster overall execution

**When to Use:**
- Non-blocking research (can work on other things)
- Analysis while waiting (prepare error handling)
- Multiple information sources needed

### Sequential Execution (Blocking)

**Used for:** Validator, Knowledge Curator

```python
# Launch subagent and wait for result
result = Task(
    subagent_type="validator",
    prompt="Validate solution",
    run_in_background=False  # KEY: Wait for completion
)

# Only continues after validation completes
if result.valid:
    apply_solution()
```

**Benefits:**
- Guaranteed execution order
- Results available immediately
- Simpler workflow

**When to Use:**
- Must validate before proceeding
- Must document after completion
- Solution required for next steps

---

## Complete Workflow Examples

### Example 1: Error Resolution Workflow

```python
# Primary agent working on WebSocket implementation
try:
    result = implement_websocket()

except TimeoutError as error:
    print(f"❌ Error: {error}")

    # STEP 1: Launch parallel subagents (research + debug)
    research_task = Task(
        subagent_type="researcher",
        prompt=f"Research WebSocket timeout solution: {error}",
        run_in_background=True
    )

    debug_task = Task(
        subagent_type="debugger",
        prompt=f"Analyze WebSocket timeout error: {error}",
        context={"stack_trace": traceback},
        run_in_background=True
    )

    # Prepare error handling while waiting
    prepare_error_handling()

    # STEP 2: Get research and debug results
    solution = TaskOutput(research_task.task_id, block=True)
    analysis = TaskOutput(debug_task.task_id, block=True)

    print(f"📚 Research: {solution.best_solution}")
    print(f"🔍 Analysis: {analysis.root_cause}")

    # STEP 3: Implement solution
    fix = implement_fix(solution, analysis)

    # STEP 4: Validate before applying
    validation = Task(
        subagent_type="validator",
        prompt="Validate WebSocket timeout fix",
        context={"solution": fix, "test_cases": generate_tests()},
        run_in_background=False  # Sequential - must validate
    )

    if validation.valid:
        print("✅ Validation passed - applying fix")
        apply_fix(fix)
    else:
        print(f"❌ Validation failed: {validation.reason}")
        # Research alternative
        alternative = Task(subagent_type="researcher", ...)
        apply_fix(alternative)

    # STEP 5: Document after completion
    Task(
        subagent_type="knowledge-curator",
        prompt="Capture WebSocket timeout solution",
        context={
            "error": error,
            "solution": fix,
            "verified": validation.valid
        },
        run_in_background=False
    )

    print("✅ Knowledge captured to KB")
```

### Example 2: Proactive Research Workflow

```python
# Primary agent planning feature implementation
if feature_requires_websockets:
    # Launch researcher proactively (before implementation)
    research_task = Task(
        subagent_type="researcher",
        prompt="""
        Research WebSocket best practices:
        Framework: FastAPI
        Use case: Real-time notifications
        Scale: 1000+ concurrent connections
        """,
        run_in_background=True
    )

    # Continue with architecture design
    architecture = design_feature_architecture()

    # Get research results before implementation
    best_practices = TaskOutput(research_task.task_id, block=True)

    print(f"📚 Best Practices Found:")
    for practice in best_practices.recommendations:
        print(f"  - {practice}")

    # Incorporate best practices into design
    architecture = apply_best_practices(architecture, best_practices)

    # Implement with best practices already incorporated
    implementation = implement_feature(architecture)

    # Validate implementation
    validation = Task(
        subagent_type="validator",
        prompt="Validate WebSocket implementation",
        context={"implementation": implementation}
    )

    if validation.valid:
        # Document learning
        Task(
            subagent_type="knowledge-curator",
            prompt="Document WebSocket implementation learnings",
            context={"best_practices": best_practices}
        )
```

### Example 3: Session End Retrospective

```python
# Automatic trigger at session end (via hook)
# Configured in .claude/settings.json

# Knowledge curator analyzes entire session
result = Task(
    subagent_type="knowledge-curator",
    prompt="""
    Analyze entire session for knowledge capture:

    Session Duration: 2 hours
    Tasks Completed: 3
    Errors Encountered: 2
    Solutions Implemented: 2
    Decisions Made: 5

    Capture:
    1. All error solutions
    2. All decisions with rationale
    3. Patterns discovered
    4. Best practices found

    Auto-categorize (Shared KB vs Project KB)
    Create GitHub issues for shared knowledge
    """,
    run_in_background=False
)

# Output summary
print(f"""
🔍 SESSION RETROSPECTIVE COMPLETE

Key Moments Found: {result.key_moments}

Captured Knowledge:
✅ Shared KB: {result.shared_entries} GitHub issues
✅ Project KB: {result.project_entries} YAML files

📊 Quality Metrics:
  - Average Score: {result.quality_score}/100
  - All entries ≥75 threshold: {'✅' if result.all_passed else '❌'}

💡 Next Steps:
1. Review GitHub issues
2. Approve or enhance entries
3. Sync to shared repository
""")
```

---

## Configuration

### Settings

```json
// .claude/settings.json
{
  "agents": {
    "paths": [".claude/agents", ".claude/agents/subagents"],
    "enabled": [
      "kb-curator",
      "researcher",
      "debugger",
      "validator",
      "knowledge-curator"
    ],
    "auto_discover": true
  },
  "hooks": {
    "error-handling": {
      "events": ["PreToolUse"],
      "condition": "error OR exception",
      "action": "launch_parallel_subagents",
      "subagents": ["researcher", "debugger"],
      "mode": "background"
    },
    "validation-required": {
      "events": ["PostToolUse"],
      "condition": "code_modified OR fix_applied",
      "action": "launch_validator",
      "mode": "sequential"
    },
    "knowledge-capture": {
      "events": ["Stop", "SessionEnd"],
      "action": "launch_knowledge_curator",
      "mode": "sequential"
    }
  }
}
```

---

## Communication Protocols

### Request Format

```yaml
type: subagent_request
request_id: "<uuid>"
subagent_type: "<subagent_name>"
priority: "blocking | high | medium | low"

context:
  task: "<task description>"
  error: "<error message if applicable>"
  stack_trace: "<stack trace if applicable>"
  code_snippet: "<relevant code>"
  environment:
    framework: "<FastAPI, React, etc.>"
    version: "<version number>"
    language: "<Python, JavaScript, etc.>"

requirements:
  urgency: "<blocking | high | medium | low>"
  return_format: "<summary | detailed | code_only>"
  constraints:
    max_time: <seconds>
    quality_threshold: <score>

execution:
  mode: "<background | sequential>"
  timeout: <seconds>
```

### Response Format

```yaml
type: subagent_response
request_id: "<uuid>"
duration_seconds: <float>
completion_status: "<success | failed | partial>"

results:
  # Subagent-specific results

quality_metrics:
  confidence_score: <0-100>
  completeness: <percentage>

recommendations:
  - "<next step 1>"
  - "<next step 2>"

next_actions:
  - action: "<action name>"
    agent: "<agent type>"
    reason: "<why this action>"
```

---

## Best Practices

### For Primary Agents

1. **Set appropriate execution mode**
   - Use `background=True` for research/debug (parallel)
   - Use `background=False` for validation/documentation (sequential)

2. **Provide clear context**
   - Always include error message
   - Include stack trace for debugging
   - Describe what you were trying to do

3. **Set urgency correctly**
   - `blocking`: Agent cannot continue without result
   - `high`: Important but can work on other tasks
   - `medium`: Nice to have, research in background
   - `low`: Exploration, can wait

4. **Handle subagent failures**
   - Research failed: Try broader search terms
   - Validation failed: Research alternative solution
   - Curator failed: Manual KB entry creation

### For Subagent Development

1. **Be autonomous** - Work independently, minimal human intervention
2. **Communicate clearly** - Structured requests/responses
3. **Report confidence** - Honest confidence scores
4. **Suggest next steps** - Guide primary agent on what to do next

---

## Integration with Existing System

### With KB Curator Agent

```python
# KB Curator (main agent) can use subagents
# Example: Automated PR review

# Subagent: Validate entry quality
validation = Task(
    subagent_type="validator",
    prompt="Validate this KB entry",
    context={"entry": pr_entry}
)

# Subagent: Research similar entries
similar = Task(
    subagent_type="researcher",
    prompt="Find similar KB entries",
    context={"query": entry.problem}
)

# Use both for comprehensive review
review = generate_pr_review(validation, similar)
```

### With Skills

```python
# Skills can trigger subagents
# Example: kb-create skill

# After creating entry, validate it
validation = Task(
    subagent_type="validator",
    prompt="Validate newly created KB entry",
    context={"entry": new_entry}
)

if validation.valid:
    # Sync to repository
    sync_entry(new_entry)
```

### With Slash Commands

```bash
# /retrospective command uses knowledge-curator subagent
/retrospective
# → Launches knowledge-curator subagent
# → Analyzes session
# → Creates KB entries

# /kb-query command can trigger researcher subagent
/kb-query "unknown error"
# → If not found in KB, launch researcher
# → Research web for solution
# → Return results + offer to add to KB
```

---

## Troubleshooting

### Subagent Not Launching

**Problem:** Subagent not starting when triggered

**Solutions:**
1. Check `.claude/settings.json` - subagent enabled?
2. Check file path - subagent file exists?
3. Check syntax - YAML/JSON valid?
4. Check permissions - file readable?

### Subagent Hanging

**Problem:** Subagent not returning results

**Solutions:**
1. Check timeout setting - increase if needed
2. Check dependencies - tools available?
3. Check network - web search working?
4. Manual test - run subagent independently

### Poor Quality Results

**Problem:** Subagent returns low-quality solutions

**Solutions:**
1. Provide more context in request
2. Set higher quality_threshold
3. Check confidence scores
4. Verify sources being consulted

---

## Performance Metrics

### Expected Performance

| Subagent | Avg Response | Success Rate | Quality |
|----------|--------------|--------------|---------|
| Researcher | 2-5 seconds | 95% | 85/100 |
| Debugger | 1-2 seconds | 98% | 90/100 |
| Validator | 3-10 seconds | 92% | 95/100 |
| Knowledge Curator | 2-4 seconds | 97% | 82/100 |

### Optimization Tips

1. **Use parallel execution** when possible (researcher + debugger)
2. **Set appropriate timeouts** (don't wait forever)
3. **Cache research results** (same query multiple times)
4. **Limit search scope** (be specific in queries)

---

## Future Enhancements

### Planned Subagents

1. **Performance Profiler** - Analyze performance bottlenecks
2. **Security Auditor** - Check for security vulnerabilities
3. **Documentation Generator** - Auto-generate code docs
4. **Test Generator** - Generate test cases for code

### Planned Features

1. **Subagent chaining** - Researcher → Debugger → Validator
2. **Result caching** - Cache research results
3. **Learning system** - Subagents learn from past results
4. **Collaboration** - Subagents share information

---

## Related Documentation

- **Pattern:** `universal/patterns/agent-collaboration-workflow.yaml`
- **Subagent Details:** `.claude/agents/subagents/*.md`
- **Main Agent:** `.claude/agents/kb-curator.md`
- **Skills:** `.claude/skills/*/SKILL.md`

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Maintained By:** KB Curator
**Status:** Production Ready ✅
