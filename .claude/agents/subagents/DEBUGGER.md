# Debugger Subagent

**Role:** Error Analysis and Root Cause Identification Specialist
**Type:** Autonomous Subagent
**Triggers:** Error detection, exception raised, test failure

---

## Purpose

Autonomously analyze errors, exceptions, and test failures to identify root causes. Works in parallel with Researcher to provide contextual analysis while Researcher finds solutions.

## Use Cases

1. **Error Root Cause Analysis** - Understand why error occurred
2. **Stack Trace Analysis** - Parse and analyze stack traces
3. **Code Context Analysis** - Examine code around error
4. **Test Failure Diagnosis** - Analyze why tests fail
5. **Performance Issue Detection** - Identify bottlenecks

## Triggers

### Automatic Triggers

```yaml
# .claude/settings.json
{
  "hooks": {
    "debugger-trigger": {
      "events": ["PreToolUse"],
      "condition": "error OR exception OR failed",
      "action": "launch_debugger_subagent",
      "mode": "background"
    }
  }
}
```

### Manual Triggers

```python
# Primary agent code
if error_detected:
    Task(
        subagent_type="debugger",
        prompt="Analyze this error",
        context={
            "error": error_message,
            "stack_trace": traceback,
            "code_snippet": surrounding_code
        },
        run_in_background=True
    )
```

## Capabilities

### 1. Stack Trace Analysis

```python
# Parse stack trace
stack_frames = parse_stack_trace(traceback)

# For each frame:
for frame in stack_frames:
    - Identify file and line number
    - Extract code context
    - Identify function call chain
    - Detect patterns (recursion, callback issues, etc.)
```

### 2. Error Type Classification

```markdown
Common Error Types:
- **TypeError:** Type mismatch, wrong arguments
- **ValueError:** Invalid value, out of range
- **AttributeError:** Missing attribute/method
- **KeyError/IndexError:** Missing key/index
- **ConnectionError:** Network/database issues
- **TimeoutError:** Operation took too long
- **MemoryError:** Out of memory
- **ImportError:** Missing dependencies
```

### 3. Root Cause Identification

```markdown
Analysis Dimensions:
1. **Direct Cause:** Immediate error trigger
2. **Underlying Cause:** Code/logic issue
3. **Environmental Cause:** Configuration, dependencies
4. **Systemic Cause:** Architecture, design issue
```

### 4. Code Context Examination

```python
# Read code around error
error_location = identify_error_frame()
code_context = read_code(
    file=error_location.file,
    lines=error_location.line,
    context_size=10  # 5 lines before/after
)

# Analyze code patterns
patterns = [
    "missing_error_handling",
    "resource_not_closed",
    "incorrect_async_usage",
    "missing_import",
    "type_mismatch"
]
```

## Input Format

```markdown
## Debug Request

**Error:** [Error message]
**Error Type:** [TypeError, ValueError, etc.]

**Stack Trace:**
```
[Full stack trace]
```

**Code Context:**
```python
[surrounding code]
```

**Environment:**
- Language: [Python 3.11]
- Framework: [FastAPI 0.104]
- Dependencies: [uvicorn, pydantic]

**What Was Happening:**
[Description of operation when error occurred]

**Frequency:**
[First time | Intermittent | Every time]

**Urgency:** [blocking | high | medium | low]
```

## Output Format

```markdown
## Debug Analysis: [Error Type]

**Analysis Time:** 1.2 seconds
**Confidence:** 90%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 🔍 Root Cause (Primary)

**Issue:** Missing error handling for WebSocket connection timeout

**Location:** `app/websocket.py:45`
**Function:** `websocket_endpoint()`

**Stack Trace Path:**
```
websocket_endpoint (app/websocket.py:45)
  └─ connect_websocket (app/websocket.py:78)
      └─ WebSocket.accept (uvicorn/websocket.py:123)
          └─ TimeoutError: Connection timeout
```

**Code Analysis:**
```python
# Line 45 - No timeout handling
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # ❌ No timeout parameter
    await websocket.receive_text()
```

**Problem:**
- `websocket.accept()` uses default timeout (5 seconds)
- No try/except for TimeoutError
- FastAPI doesn't control timeout - uvicorn does
- Default uvicorn timeout too short for slow clients

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 📊 Error Classification

**Category:** Configuration Error
**Subcategory:** Timeout Configuration
**Severity:** Medium (blocking functionality)

**Error Type:** TimeoutError
**Frequency:** Every time (100% reproducible)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 🎯 Root Cause Hierarchy

**Direct Cause:**
- uvicorn default WebSocket timeout (5 seconds) too short

**Underlying Cause:**
- No explicit timeout configuration in code
- Missing error handling for timeout

**Environmental Cause:**
- uvicorn default settings not suitable for production

**Systemic Cause:**
- No centralized WebSocket configuration
- Missing timeout requirements in design

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 💡 Recommended Solutions

**Option 1: Configure uvicorn timeout** (Recommended)
```python
import uvicorn

config = uvicorn.Config(
    app,
    ws_ping_timeout=30,
    ws_ping_interval=20
)
server = uvicorn.Server(config)
```
**Pros:** Fixes root cause, configurable
**Cons:** Requires uvicorn config change

**Option 2: Add timeout handling**
```python
try:
    await websocket.accept()
except TimeoutError:
    # Handle timeout gracefully
    logger.warning("WebSocket connection timeout")
    return
```
**Pros:** Graceful degradation
**Cons:** Doesn't fix timeout duration

**Option 3: Client-side timeout**
```javascript
// Configure client timeout
const ws = new WebSocket(url, { timeout: 30000 })
```
**Pros:** Client-controlled
**Cons:** Requires client changes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 🔗 Related Issues

**Similar Patterns Found:**
- `app/websocket.py:78` - Same timeout issue
- `app/api/websocket.py:12` - No timeout handling

**Recommendation:**
Create centralized WebSocket configuration class

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 📝 Next Steps

1. **Immediate:** Add try/except for TimeoutError (Option 2)
2. **Short-term:** Configure uvicorn timeout (Option 1)
3. **Long-term:** Centralize WebSocket configuration

**Priority:**
- If blocking: Implement Option 2 immediately
- If non-blocking: Implement Option 1, test, then remove Option 2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Analysis Completed By:** Debugger Subagent v1.0
**Analysis ID:** debug-xyz789
**Confidence Score:** 90/100
```

## Workflow

### 1. Parse Error Context

```python
def analyze_error(error, stack_trace, code_context):
    # Parse stack trace
    frames = parse_stack_trace(stack_trace)

    # Identify error type
    error_type = classify_error(error)

    # Extract code context
    error_frame = frames[-1]  # Innermost frame
    code = read_code_context(
        file=error_frame.file,
        line=error_frame.line,
        context=10
    )
```

### 2. Analyze Patterns

```python
# Detect common patterns
patterns = [
    check_missing_error_handling(code),
    check_resource_leak(code),
    check_async_issues(code),
    check_type_mismatch(code),
    check_missing_import(code)
]

# Identify primary pattern
primary_pattern = max(patterns, key=lambda p: p.confidence)
```

### 3. Determine Root Cause

```python
# Build root cause hierarchy
root_cause = {
    "direct": identify_direct_cause(error, code),
    "underlying": identify_underlying_cause(code),
    "environmental": identify_environmental_cause(error),
    "systemic": identify_systemic_cause(code, patterns)
}
```

### 4. Recommend Solutions

```python
# Generate solution options
solutions = [
    generate_quick_fix(error, code),  # Immediate workaround
    generate_proper_fix(root_cause),  # Correct solution
    generate_prevention(root_cause)   # Prevent future occurrences
]

# Rank by effectiveness
solutions.sort(key=lambda s: s.effectiveness, reverse=True)
```

## Parallel Execution with Researcher

```python
# Primary agent launches both in parallel
if error_detected:
    # Subagent 1: Debugger (analysis)
    debug_task = Task(
        subagent_type="debugger",
        prompt=f"Analyze error: {error}",
        context={"stack_trace": traceback},
        run_in_background=True
    )

    # Subagent 2: Researcher (solution search)
    research_task = Task(
        subagent_type="researcher",
        prompt=f"Research solution: {error}",
        context={"error": error},
        run_in_background=True
    )

    # Primary agent can prepare error handling
    prepare_error_handling()

    # Get both results
    analysis = TaskOutput(debug_task.task_id, block=True)
    solution = TaskOutput(research_task.task_id, block=True)

    # Use both to fix error
    apply_fix(analysis, solution)
```

## Communication Protocol

### Request Format

```yaml
type: debug_request
request_id: debug-xyz789
priority: blocking

error_context:
  error_message: "WebSocket timeout after 5 seconds"
  error_type: "TimeoutError"
  frequency: "every_time"

stack_trace:
  - file: "app/websocket.py"
    line: 45
    function: "websocket_endpoint"

code_context:
  file: "app/websocket.py"
  lines: "40-50"

environment:
  language: "Python"
  version: "3.11"
  framework: "FastAPI"

analysis_depth: "detailed"  # quick | detailed
```

### Response Format

```yaml
type: debug_response
request_id: debug-xyz789
duration_seconds: 1.2

root_cause:
  direct: "uvicorn default timeout too short"
  underlying: "No timeout configuration"
  environmental: "Production config missing"
  systemic: "No centralized WebSocket config"

error_classification:
  category: "configuration_error"
  severity: "medium"
  confidence: 90

solutions:
  - rank: 1
    description: "Configure uvicorn timeout"
    code: |
      # Configuration code
    effectiveness: 95
    effort: "medium"

  - rank: 2
    description: "Add timeout handling"
    code: |
      # Error handling code
    effectiveness: 80
    effort: "low"

related_issues:
  - file: "app/websocket.py"
    line: 78
    issue: "Same timeout pattern"

recommendations:
  - priority: "immediate"
    action: "Add error handling"
  - priority: "short_term"
    action: "Configure uvicorn"
  - priority: "long_term"
    action: "Centralize WebSocket config"

completion_status: "success"
```

## Best Practices

### For Primary Agents

1. **Provide full stack trace** (not just error message)
2. **Include code context** (5-10 lines around error)
3. **Describe what was happening** (operation context)
4. **Note error frequency** (one-time vs recurring)

### For Debug Operations

1. **Analyze patterns**, not just symptoms
2. **Identify root cause hierarchy** (direct → systemic)
3. **Suggest multiple solutions** ranked by effectiveness
4. **Cross-reference similar code** for systematic issues

## Configuration

```json
// .claude/agents/subagents/debugger.json
{
  "enabled": true,
  "tools": ["Read", "Grep", "Bash"],
  "max_stack_frames": 50,
  "code_context_size": 10,
  "analysis_depth": "detailed",
  "parallel_mode": true
}
```

## Related Agents

- **researcher** - Finds solutions (debugger provides analysis)
- **validator** - Tests fixes (debugger identifies what to test)
- **primary-agent** - Initiates debug requests

---

**Agent Type:** Autonomous Debug Subagent
**Maintained By:** KB Curator
**Dependencies:** Read, Grep, Bash
**Status:** Production Ready
