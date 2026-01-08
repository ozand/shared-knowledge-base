# Feedback Loop - Agent Learning Process

**Version:** 5.1.0
**Last Updated:** 2026-01-08

---

## Overview

The **Feedback Loop** is the cognitive process that transforms an AI agent from a simple "executor" into a "learning system". In v5.1 architecture, this process happens in the agent's "mind" (within its session) and is regulated by instructions and scripts.

---

## The Loop: 5 Stages

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1. DETECTION    →  "Something went wrong"                  │
│  2. ANALYSIS     →  "Why did it happen?"                    │
│  3. EXTRACTION   →  "Form structured knowledge"             │
│  4. ROUTING      →  "Whose knowledge is it?"                │
│  5. COMMIT       →  "Save to Project KB or Shared KB"       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Stage 1: Detection (Triggers)

The agent must continuously monitor tool outputs for triggers.

### Trigger Types

**1. Execution Errors:**
- Tool returned `exit code != 0`
- Python traceback
- Connection refused
- File not found

**2. Logical Errors:**
- Code executed but result is incorrect
- Test failed
- Wrong output format

**3. Inefficiency:**
- Solution worked but took too long
- Requires optimization
- Better approach exists

**4. Complex Success:**
- Problem required > 3 attempts to solve
- Non-obvious solution discovered
- Valuable pattern identified

### Example Triggers

```bash
# Error trigger
Traceback (most recent call last):
  File "app.py", line 42, in <module>
    raise ValueError("Invalid configuration")
ValueError: Invalid configuration

# Logical error trigger
AssertionError: Expected 200, got 403

# Success trigger
# After 4 attempts, discovered that FastAPI 0.95+ changed middleware order
```

---

## Stage 2: Analysis (Reflection)

Once triggered, the agent must pause and "think" before trying again.

### Reflection Prompt

When a trigger occurs, the agent should answer:

1. **Context:** What was I trying to do?
2. **Problem:** What exact error did I get?
3. **Root Cause:** Why did this happen?
   - Wrong library version?
   - Configuration error?
   - Network access?
   - Missing dependency?
4. **Solution:** How did I fix it?
   - Code change?
   - Configuration update?
   - Command executed?

### Internal Monologue Example

```
AGENT INTERNAL MONOLOGUE:

Context: I was trying to start the FastAPI application
Problem: Got "CORS error: 405 Method Not Allowed on OPTIONS"
Root Cause: FastAPI >= 0.95 changed the middleware registration order
Solution: Add CORSMiddleware BEFORE route registration
Attempts: This took me 3 tries to figure out
Value: This is a common issue for all FastAPI >= 0.95 projects
```

### Analysis Output

The agent should form a structured knowledge block:

```
Problem: FastAPI CORS Error: 405 Method Not Allowed on OPTIONS
Cause: In v0.95+, middleware order became critical
Solution: Register CORSMiddleware before defining routes
Attempts to solve: 3
Universality: Applies to all FastAPI >= 0.95 projects
```

---

## Stage 3: Extraction (Formalization)

Package the insight into YAML format.

### YAML Template

```yaml
version: "1.0"
category: "web-framework"
last_updated: "2026-01-08"

errors:
  - id: "FASTAPI-001"
    title: "CORS Error: 405 Method Not Allowed on OPTIONS"
    severity: "high"
    scope: "python"
    framework: "fastapi"
    problem: |
      FastAPI returns 405 Method Not Allowed for OPTIONS preflight requests
      when trying to make cross-origin requests from the browser.
    solution:
      code: |
        from fastapi.middleware.cors import CORSMiddleware

        # CRITICAL: Add middleware BEFORE defining routes
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Define routes AFTER middleware
        @app.get("/api/items")
        async def get_items():
            return {"items": []}
      explanation: |
        In FastAPI >= 0.95, the order of middleware registration matters.
        CORSMiddleware must be added BEFORE route definitions to handle
        OPTIONS preflight requests correctly.
    attempts: 3
    related_issues:
      - "https://github.com/tiangolo/fastapi/issues/1234"
```

### Quality Checklist

Before submitting, ensure:
- ✅ Problem description is clear
- ✅ Solution code is complete and runnable
- ✅ Explanation covers the "why"
- ✅ Appropriate category/scope assigned
- ✅ Severity level is correct

---

## Stage 4: Routing (Decision Matrix)

The most critical filter! Determine where knowledge belongs.

### Routing Algorithm

```
START
  │
  ├─→ Check 1: SECURITY
  │   ├─ Contains tokens, passwords, internal IPs?
  │   └─ YES → Project KB (.kb/project/)
  │
  ├─→ Check 2: BUSINESS LOGIC
  │   ├─ Contains domain rules, discount calculations?
  │   └─ YES → Project KB (.kb/project/)
  │
  ├─→ Check 3: UNIVERSALITY
  │   ├─ Would this help another project with same stack?
  │   ├─ Is this a common pattern (not a hack)?
  │   └─ YES → Shared KB (via GitHub Issue)
  │
  └─→ OTHERWISE → Project KB (.kb/project/)
```

### Decision Questions

**Question 1: Security Check**
```
Does the YAML contain:
- API keys, tokens, passwords?
- Internal server IPs?
- Database connection strings?
- Sensitive business data?

If YES → Project KB (NEVER share secrets!)
```

**Question 2: Business Logic Check**
```
Is this specific to:
- Your product's domain rules?
- Company's internal processes?
- Project-specific configurations?
- Temporary workarounds for this environment?

If YES → Project KB
```

**Question 3: Universality Check**
```
Would a developer in another project benefit from this?
- Is it a framework pattern?
- Is it a common error + fix?
- Is it a best practice?
- Is it version-specific (applies to all using that version)?

If YES → Shared KB
If NO (project-specific hack) → Project KB
```

### Examples

| Scenario | Decision | Reason |
|----------|----------|--------|
| "FastAPI CORS fix" | Shared KB | Universal pattern for FastAPI >= 0.95 |
| "Stripe webhook signature validation" | Shared KB | Standard Stripe integration pattern |
| "Discount calculation bug" | Project KB | Business logic specific to e-shop |
| "Internal API authentication" | Project KB | Contains internal service URLs |
| "Docker compose for local dev" | Project KB | Environment-specific workaround |
| "Pydantic v2 validation migration" | Shared KB | Helps all Pydantic v2 users |

---

## Stage 5: Commit (Submission)

Execute the submission using `kb_submit.py`.

### For Project KB

**When:** Security risks, business logic, project-specific

**Command:**
```bash
python .kb/shared/tools/v5.1/kb_submit.py \
  --target local \
  --file fastapi-cors-fix.yaml
```

**What happens:**
- File saved to `.kb/project/knowledge/` (or category-based subdir)
- Agent commits to project git
- Instantly available in next session
- No curator review needed

**Example output:**
```
✅ [Local] File saved: .kb/project/knowledge/fastapi-cors-fix.yaml
   Don't forget to commit to your project repository:
   git add .kb/project/knowledge/fastapi-cors-fix.yaml
   git commit -m 'Add KB entry: fastapi-cors-fix.yaml'
```

### For Shared KB

**When:** Universal patterns, framework solutions, best practices

**Command:**
```bash
python .kb/shared/tools/v5.1/kb_submit.py \
  --target shared \
  --file fastapi-cors-fix.yaml \
  --title "Fix: FastAPI CORS 405 Error on OPTIONS" \
  --description "CORS error when using FastAPI >= 0.95" \
  --domain python
```

**What happens:**
- Quality score calculated (must be >= 75)
- GitHub Issue created in `shared-knowledge-base` repo
- Issue labeled with `kb-submission`
- Agent considers task complete
- Knowledge appears after curator approval + submodule sync

**Example output:**
```
✅ Validation passed: Quality score: 85/100
   ✅ Meets quality threshold (>= 75)

✅ Created Issue #42 in shared-knowledge-base
   URL: https://github.com/ozand/shared-knowledge-base/issues/42
```

---

## Complete Example: End-to-End

### Scenario: E-Shop Project

**Context:** Agent working on e-shop, trying to run tests

**1. Detection (Trigger):**
```bash
$ pytest
ModuleNotFoundError: No module named 'myshop'
```

**2. Analysis (Reflection):**
```
What was I trying to do?
→ Run pytest test suite

What exact error?
→ ModuleNotFoundError: No module named 'myshop'

Root Cause?
→ pytest can't find the root project module
→ PYTHONPATH doesn't include current directory

How did I fix it?
→ Created pytest.ini with: pythonpath = .

How many attempts?
→ 1 (quick fix, but important pattern)
```

**3. Extraction (YAML):**
```yaml
version: "1.0"
category: "testing"
last_updated: "2026-01-08"

errors:
  - id: "PYTEST-001"
    title: "ModuleNotFoundError when running pytest"
    severity: "medium"
    scope: "python"
    framework: "pytest"
    problem: |
      pytest fails with ModuleNotFoundError when tests import
      application modules from the project root.
    solution:
      code: |
        # Create pytest.ini in project root
        [pytest]
        pythonpath = .
        testpaths = tests
        python_files = test_*.py
      explanation: |
        pytest doesn't automatically add the current directory to PYTHONPATH.
        This causes import errors when tests try to import modules from the
        project root. Adding pythonpath = . to pytest.ini fixes this.
```

**4. Routing (Decision):**
```
Security Check: No secrets ✅
Business Logic: Not domain-specific ✅
Universality: Helps all pytest projects ✅

Decision: SHARED KB
```

**5. Commit (Submission):**
```bash
python .kb/shared/tools/v5.1/kb_submit.py \
  --target shared \
  --file pytest-module-not-found.yaml \
  --title "Fix: pytest ModuleNotFoundError" \
  --description "pytest can't find project modules" \
  --domain python
```

**Result:**
```
✅ Quality score: 78/100
✅ Created Issue #43 in shared-knowledge-base
```

---

## Implementation: How to Enforce

### Method 1: System Prompt (Recommended)

Add to `.claude/agents/<agent-name>.md` or `CLAUDE.md`:

```markdown
## Feedback Loop Protocol

**MANDATORY:** When you encounter an error and successfully solve it:

1. **Create Knowledge Entry:**
   - Format the solution as YAML
   - Include problem, solution code, explanation
   - Assign appropriate category and severity

2. **Determine Scope:**
   - Check `.kb/context/PROJECT.yaml` sharing_criteria
   - Secrets/business logic → `--target local`
   - Universal patterns → `--target shared`

3. **Submit Entry:**
   ```bash
   python .kb/shared/tools/v5.1/kb_submit.py \
     --target <local|shared> \
     --file <entry.yaml> \
     --title "Descriptive title"
   ```

**Never skip this step.** Every error you solve is valuable knowledge.
```

### Method 2: PROJECT.yaml Instructions

Add to `.kb/context/PROJECT.yaml`:

```yaml
agent_instructions:
  feedback_loop:
    enabled: true
    mandatory: true
    triggers:
      - "Error with exit code != 0"
      - "Test failure"
      - "Solution took > 2 attempts"
    output_format: "yaml"
    submission_required: true
```

### Method 3: PostToolUse Hook (Advanced)

Create `.claude/hooks/post-tool-use.sh`:

```bash
#!/bin/bash
# Check if last command failed
if [ $LAST_EXIT_CODE -ne 0 ]; then
    echo "⚠️  Tool failed! Remember to document the solution."
    echo "   Use kb_submit.py after you fix it."
fi
```

---

## Benefits

### For the Agent

**Learning:**
- Never makes the same mistake twice
- Builds institutional memory
- Accelerates problem-solving

**Efficiency:**
- Quick access to previous solutions
- Patterns become reusable
- Reduces trial-and-error

### For the Team

**Knowledge Sharing:**
- Solutions preserved across sessions
- Onboarding becomes faster
- Consistent problem-solving approaches

**Quality:**
- Vetted solutions via curator
- Standardized documentation
- Searchable knowledge base

### For the Organization

**Scalability:**
- Knowledge compounds over time
- New projects benefit instantly
- Reduces duplicate work

**Continuity:**
- Knowledge survives agent sessions
- Survives team member turnover
- Builds organizational intelligence

---

## Summary

The Feedback Loop transforms agents from reactive executors to proactive learners:

1. ✅ **Detects** errors and valuable patterns
2. ✅ **Analyzes** root causes
3. ✅ **Extracts** structured knowledge
4. ✅ **Routes** to appropriate KB (Project vs Shared)
5. ✅ **Commits** for future use

**Key Principle:** This is not magic code — it's **agent discipline** reinforced by:
- Clear instructions
- Convenient tools
- Automated workflows
- Quality validation

**Result:** A self-improving AI system that learns from every mistake and success.

---

**Related Documentation:**
- [SHARED-KB-WORKFLOWS.md](SHARED-KB-WORKFLOWS.md) - Shared KB workflows
- [WORKFLOWS.md](WORKFLOWS.md) - Agent workflows
- [CONTEXT_SCHEMA.md](CONTEXT_SCHEMA.md) - PROJECT.yaml schema
