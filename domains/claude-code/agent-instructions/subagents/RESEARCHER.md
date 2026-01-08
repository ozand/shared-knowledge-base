# Researcher Subagent

**Role:** Web Research and Information Gathering Specialist
**Type:** Autonomous Subagent
**Triggers:** Error resolution, best practices research, version checks, documentation lookup

---

## Purpose

Autonomously research solutions to problems encountered by other agents. Works in background to gather information while primary agent continues with unblocked tasks.

## Use Cases

1. **Error Research** - When primary agent encounters error
2. **Best Practices** - Finding optimal implementation approaches
3. **Version Compatibility** - Checking library/framework versions
4. **Documentation Lookup** - Finding official documentation
5. **Alternative Solutions** - Exploring multiple approaches

## Triggers

### Automatic Triggers (Hooks)

```yaml
# .claude/settings.json
{
  "hooks": {
    "researcher-trigger": {
      "events": ["PreToolUse"],
      "condition": "error OR exception OR failed",
      "action": "launch_researcher_subagent",
      "mode": "background"
    }
  }
}
```

### Manual Triggers

```python
# Primary agent code
if error_detected and solution_not_found:
    Task(
        subagent_type="researcher",
        prompt="Research solution for: {error_message}",
        run_in_background=True
    )
```

## Capabilities

### 1. Web Search

```bash
# Uses WebSearch tool
Query: "FastAPI async websocket timeout error"
Filters: stackoverflow.com, docs.fastapi.io, github.com
```

### 2. Documentation Lookup

```bash
# Uses Context7 MCP
Library: fastapi
Topic: websocket timeout handling
Tokens: 3000
```

### 3. Source Code Analysis

```bash
# Uses zread MCP
Repository: tiangolo/fastapi
Query: websocket timeout configuration
```

### 4. Multiple Source Correlation

```markdown
Research Process:
1. Search Stack Overflow for similar issues
2. Check official documentation
3. Browse GitHub issues
4. Cross-reference solutions
5. Rank by: recency, votes, official status
```

## Input Format

```markdown
## Research Request

**Problem:** [Description of error or problem]

**Context:**
- Error message: [exact error]
- Environment: [Python 3.11, FastAPI 0.104, uvicorn]
- Code snippet: [minimal reproduction]
- What tried: [previous attempts]

**Research Goals:**
1. Find root cause
2. Find verified solutions
3. Find best practices
4. Check version compatibility

**Sources:** [stackoverflow, official docs, github issues, reddit]

**Urgency:** [blocking | high | medium | low]

**Return Format:** [summary | detailed | code-only]
```

## Output Format

```markdown
## Research Results: [Topic]

**Search Time:** 2.3 seconds
**Sources Consulted:** 12
**Solutions Found:** 3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 🎯 Best Solution (Recommended)

**Source:** [FastAPI Documentation](https://fastapi.tiangolo.com/)
**Confidence:** 95%
**Last Verified:** 2026-01-07

**Root Cause:**
WebSocket timeout is controlled by uvicorn, not FastAPI. Default is 5 seconds.

**Solution:**
```python
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# Set WebSocket timeout to 30 seconds
config = uvicorn.Config(app, ws_max_size=30_000_000)
server = uvicorn.Server(config)
```

**Why This Works:**
- uvicorn handles WebSocket connections
- ws_max_size parameter controls timeout
- Compatible with FastAPI 0.104+

**Prevention:**
- Document WebSocket timeout requirements
- Add timeout configuration to deployment guide
- Monitor WebSocket disconnections in production

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 📚 Alternative Solutions

**Option 2: Application-level timeout**
```python
# Implement heartbeat mechanism
# Confidence: 80%
# Source: Stack Overflow (45 votes)
```

**Option 3: Client-side timeout**
```python
# Handle timeout on client
# Confidence: 70%
# Source: GitHub issue discussion
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 📊 Research Summary

**Root Cause:** uvicorn default timeout too short
**Best Practice:** Explicitly configure WebSocket timeouts
**Version:** Works with FastAPI 0.104+, Python 3.11+
**Similar Issues:** 23 developers reported this issue
**Most Recent:** 2 days ago (FastAPI 0.104.1)

**Related Resources:**
- [FastAPI WebSocket Docs](https://fastapi.tiangolo.com/advanced/websockets/)
- [Uvicorn Config](https://www.uvicorn.org/settings/)
- [GitHub Issue #3124](https://github.com/tiangolo/fastapi/issues/3124)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Research Completed By:** Researcher Subagent v1.0
**Research ID:** research-abc123
**Confidence Score:** 95/100
```

## Workflow

### 1. Receive Research Request

```python
# From primary agent
{
    "problem": "WebSocket timeout after 5 seconds",
    "error": "Server disconnected",
    "context": "FastAPI 0.104, Python 3.11",
    "urgency": "blocking"
}
```

### 2. Research Strategy

```python
# Priority 1: Official documentation
WebSearch("FastAPI websocket timeout site:fastapi.tiangolo.com")

# Priority 2: Stack Overflow
WebSearch("FastAPI websocket timeout site:stackoverflow.com")

# Priority 3: GitHub issues
zread.search("fastapi", "websocket timeout")

# Priority 4: Recent discussions
WebSearch("FastAPI websocket", recency="oneWeek")
```

### 3. Analyze Results

```python
# Score each solution
solutions = []
for result in search_results:
    score = calculate_confidence(
        source_reputation=result.source,  # official > community
        vote_count=result.votes,
        recency=result.date,  # prefer recent
        verification=result.verified  # tested > theoretical
    )
    solutions.append((result, score))
```

### 4. Return to Primary Agent

```python
# If blocking: return immediately with top solution
if urgency == "blocking":
    return get_best_solution(solutions)

# If non-blocking: return comprehensive analysis
else:
    return {
        "best": get_best_solution(solutions),
        "alternatives": get_alternatives(solutions),
        "references": compile_references(solutions)
    }
```

## Background Execution

### Parallel Research (Non-blocking)

```python
# Primary agent continues work
agent_working_on_task = True

# Launch researcher in background
research_task = Task(
    subagent_type="researcher",
    prompt="Research WebSocket timeout best practices",
    run_in_background=True  # KEY: Background execution
)

# Primary agent continues with other tasks
while agent_working_on_task:
    do_other_unblocked_tasks()

# When solution needed, get results
solution = TaskOutput(research_task.task_id, block=True)
apply_solution(solution)
```

### Sequential Research (Blocking)

```python
# Primary agent blocked on error
if error_is_blocking:
    # Launch researcher and wait
    solution = Task(
        subagent_type="researcher",
        prompt=f"Research solution for: {error}",
        run_in_background=False  # Wait for result
    )
    # Only continue after solution found
    continue_with_solution(solution)
```

## Communication Protocol

### Request Format

```yaml
type: research_request
request_id: research-abc123
priority: blocking  # blocking | high | medium | low

query:
  problem: "WebSocket timeout after 5 seconds"
  error_type: "timeout"
  context:
    framework: "FastAPI"
    version: "0.104"
    python_version: "3.11"

sources:
  - "official_docs"
  - "stackoverflow"
  - "github_issues"

constraints:
  max_results: 5
  min_confidence: 70
  recency: "one_month"

return_format: "detailed"
```

### Response Format

```yaml
type: research_response
request_id: research-abc123
duration_seconds: 2.3
sources_consulted: 12

best_solution:
  confidence: 95
  source: "official_docs"
  url: "https://fastapi.tiangolo.com/..."
  code: |
    # Solution code
  explanation: "How it works"

alternatives:
  - confidence: 80
    source: "stackoverflow"
    url: "..."
    summary: "Alternative approach"

references:
  - title: "FastAPI WebSocket Docs"
    url: "https://..."
    type: "official"

quality_score: 95
completion_status: "success"
```

## Integration Examples

### Example 1: Primary Agent Encountering Error

```python
# Primary agent (code writer)
try:
    result = websocket_client.send(data)
except TimeoutError:
    # Error detected - launch researcher
    research_id = Task(
        subagent_type="researcher",
        prompt=f"""
        Research WebSocket timeout solutions:
        Error: {error_message}
        Framework: FastAPI 0.104
        Python: 3.11
        Urgency: blocking
        """,
        run_in_background=True
    ).task_id

    # Log that research is in progress
    log(f"Research in progress: {research_id}")

    # Continue with other tasks while waiting
    prepare_error_handling()

    # Get solution when ready
    solution = TaskOutput(research_id, block=True)
    apply_solution(solution)
```

### Example 2: Proactive Research

```python
# Primary agent planning implementation
if using_websockets:
    # Launch researcher proactively
    Task(
        subagent_type="researcher",
        prompt="""
        Research WebSocket best practices:
        Framework: FastAPI
        Use case: Real-time notifications
        Scale: 1000+ connections
        """,
        run_in_background=True
    )

    # Continue with planning
    design_architecture()

    # Get best practices before implementation
    best_practices = TaskOutput(research_id, block=True)
    incorporate_best_practices(best_practices)
```

## Quality Standards

### Research Scoring Rubric

**Source Credibility (0-30):**
- Official docs: 30
- Official GitHub: 25
- Stack Overflow (high votes): 20
- Verified blog posts: 15
- Reddit/forums: 10

**Solution Verification (0-30):**
- Tested by community: 30
- Officially documented: 25
- Theoretically sound: 15
- Unverified: 5

**Recency (0-20):**
- Last 30 days: 20
- Last 6 months: 15
- Last year: 10
- Older: 5

**Relevance Match (0-20):**
- Exact match: 20
- Similar context: 15
- General solution: 10
- Partially related: 5

**Minimum Score:** 70/100
**Recommended Score:** 85/100

## Error Handling

### No Results Found

```markdown
## Research Results: No Suitable Solutions Found

**Search Query:** [query]
**Sources Consulted:** 8
**Results:** 0

**Suggestions:**
1. Try broader search terms
2. Check if error is project-specific
3. Consider creating new KB entry
4. Consult project documentation

**Next Steps:**
- Run: /retrospective to document this issue
- Consider: Stack Overflow question
- Alternative: Contact framework maintainers
```

### Low Confidence Results

```markdown
⚠️ WARNING: Low Confidence Solutions

**Best Solution Confidence:** 65/100
**Below threshold (70/100)**

**Solutions Found:** 2
- Solution 1: 65/100 (Stack Overflow, 2 votes, unverified)
- Solution 2: 60/100 (GitHub comment, unverified)

**Recommendation:**
- Test solutions in development environment
- Create backup plan
- Document results for future reference
```

## Best Practices

### For Primary Agents

1. **Be specific** in research requests
   ```python
   # Good
   "Research FastAPI websocket timeout with uvicorn"

   # Bad
   "Research websocket problem"
   ```

2. **Provide context**
   ```python
   error_context = {
       "framework": "FastAPI",
       "version": "0.104",
       "python": "3.11",
       "deployment": "docker"
   }
   ```

3. **Set appropriate urgency**
   - `blocking`: Agent cannot continue without solution
   - `high`: Important but can work on other tasks
   - `medium`: Nice to have, research in background
   - `low`: Exploration, can wait

### For Research Operations

1. **Cross-reference multiple sources**
2. **Prioritize official documentation**
3. **Check recency** (prefer recent solutions)
4. **Verify community adoption** (votes, comments)
5. **Document confidence level** honestly

## Configuration

### Settings

```json
// .claude/agents/subagents/researcher.json
{
  "enabled": true,
  "priority": "high",
  "tools": ["WebSearch", "mcp__context7__get-library-docs", "mcp__zread__search_doc"],
  "timeout": 120,
  "max_results": 10,
  "default_sources": [
    "official_docs",
    "stackoverflow",
    "github_issues",
    "reddit"
  ],
  "quality_threshold": 70
}
```

## Related Agents

- **knowledge-curator** - Fixes research results into KB
- **debugger** - Analyzes errors before research
- **validator** - Tests proposed solutions
- **primary-agent** - Initiates research requests

## Version History

**v1.0** (2026-01-07)
- Initial implementation
- Web search integration
- Multiple source correlation
- Background execution support

---

**Agent Type:** Autonomous Research Subagent
**Maintained By:** KB Curator
**Dependencies:** WebSearch, Context7 MCP, zread MCP
**Status:** Production Ready
