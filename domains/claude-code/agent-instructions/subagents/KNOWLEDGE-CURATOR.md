# Knowledge Curator Subagent

> **Progressive Disclosure:** This file is large (732 lines). Load specific sections on demand using `@references` below instead of reading entire file.

**Role:** Knowledge Capture and Documentation Specialist
**Type:** Autonomous Subagent
**Triggers:** Task completion, error resolution, retrospective request

---

## Table of Contents

- [Purpose](#purpose)
- [Use Cases](#use-cases)
- [Triggers](#triggers)
- [Capabilities](#capabilities)
- [Input Format](#input-format)
- [Knowledge Capture Request](#knowledge-capture-request)
- [Output Format](#output-format)
- [Add to Shared KB: [Title]](#add-to-shared-kb-title)
- [Workflow](#workflow)
- [Communication Protocol](#communication-protocol)
- [Integration Examples](#integration-examples)
- [Quality Standards](#quality-standards)
- [Best Practices](#best-practices)
- [Error Handling](#error-handling)
- [Configuration](#configuration)
- [Integration with Other Subagents](#integration-with-other-subagents)
- [Related Agents](#related-agents)
- [Version History](#version-history)

---

## Purpose

Autonomously capture, document, and synchronize knowledge from agent activities. Analyzes what happened during task execution and creates appropriate KB entries (Project KB or Shared KB).

## Use Cases

1. **Post-Implementation Documentation** - After solving a problem
2. **Error Solution Capture** - After fixing an error
3. **Best Practice Discovery** - After finding better approach
4. **Decision Documentation** - After architectural/technical decision
5. **Retrospective Analysis** - Session/feature completion

## Triggers

### Automatic Triggers

```yaml
# .claude/settings.json
{
  "hooks": {
    "knowledge-capture": {
      "events": ["Stop", "SessionEnd"],
      "action": "launch_knowledge_curator",
      "mode": "sequential"
    }
  }
}
```

### Manual Triggers

```python
# Primary agent code
if task_completed and knowledge_worth_capturing:
    Task(
        subagent_type="knowledge-curator",
        prompt="Analyze session and capture knowledge",
        context={
            "task": description,
            "errors_encountered": errors,
            "solutions_found": solutions,
            "decisions_made": decisions
        }
    )
```

## Capabilities

### 1. Session Analysis

```markdown
Analyzes conversation history to identify:
- Errors encountered and their solutions
- Decisions made with rationale
- Patterns discovered
- Best practices used
- Anti-patterns to avoid
```

### 2. Knowledge Categorization

```markdown
Determines appropriate KB scope:

Shared KB (requires GitHub issue):
✅ docker, universal, python, postgresql, javascript
✅ Cross-project relevance
✅ Industry-standard solutions
✅ Framework-agnostic patterns

Project KB (direct YAML creation):
✅ Project-specific logic
✅ Domain knowledge
✅ Environment-specific configs
✅ One-time occurrences
```

### 3. Entry Creation

```yaml
# For Shared KB
Creates GitHub issue with template:
- Problem description
- Solution code
- Context and tags
- Severity and scope

# For Project KB
Creates ready-to-use YAML:
- All required fields
- Quality score ≥75/100
- Proper ID format
- Metadata initialized
```

### 4. Quality Validation

```python
# Automatic quality scoring
quality_score = calculate_quality(
    completeness=has_all_required_fields,
    technical_accuracy=code_works,
    documentation=clear_explanation,
    best_practices=follows_standards
)

# Minimum threshold: 75/100
if quality_score < 75:
    enhance_entry()
```

## Input Format

```markdown
## Knowledge Capture Request

**Session Summary:**
- Duration: 45 minutes
- Task: [description]
- Status: [success | partial | failed]

**Errors Encountered:**
1. Error: [message]
   Context: [what happened]
   Solution: [how fixed]
   Verification: [tested | not tested]

**Decisions Made:**
1. Decision: [what decided]
   Rationale: [why this choice]
   Alternatives considered: [list]
   Impact: [consequences]

**Discoveries:**
- Patterns: [found patterns]
- Best practices: [what worked well]
- Anti-patterns: [what to avoid]

**Context:**
- Project: [project name]
- Framework: [FastAPI, React, etc.]
- Environment: [development, production]
- Team: [team size, expertise]

**Capture Options:**
- Auto-categorize: [true | false]
- Create issues: [true | false]
- Validate quality: [true | false]
```

## Output Format

### Shared KB Entry (GitHub Issue)

```markdown
## Add to Shared KB: [Title]

**Scope:** [python | docker | universal | postgresql | javascript]
**Category:** [category-name]
**Severity:** [critical | high | medium | low]
**Quality Score:** 85/100

### Problem
[Clear description of what went wrong]

**Error Message:**
```
[exact error if applicable]
```

**Context:**
- Framework: [FastAPI 0.104]
- Environment: [Docker, production]
- Triggered by: [what action caused this]

### Solution
```yaml
# [language]
[working solution code]
```

**Explanation:**
[How the solution works, why it fixes the problem]

### Prevention
- [ ] [Prevention tip 1]
- [ ] [Prevention tip 2]

### Tags
[tag1, tag2, tag3]

### Additional Context
**Project:** [project-name]
**Discovery Date:** [date]
**Tested:** [yes | no]
**Verified By:** [agent name, human]

**Related Entries:**
- [Link to related KB entries]

**Metadata:**
- **Last Occurrence:** [date]
- **Frequency:** [how often this happens]
- **Impact:** [development time lost, user impact]

**Discovered by:** Knowledge Curator Subagent
**Date:** [timestamp]
**Session Context:** [brief context]

---

**Curator Notes:**
- Verified solution: ✅
- Cross-referenced: [similar entries]
- Confidence: [high | medium | low]
- Suggested next steps: [if any]
```

### Project KB Entry (YAML)

```yaml
version: "1.0"
category: "category-name"
last_updated: "2026-01-07"

errors:
  - id: "PROJECT-001"
    title: "[Title]"
    severity: "medium"
    scope: "project"
    local_only: true  # Marks as project-specific

    problem: |
      [Clear description of what went wrong]

    symptoms:
      - "[Error message or symptom]"

    root_cause: |
      [Explanation of why it happens]

    solution:
      code: |
        [Working solution code]

      explanation: |
        [How the solution works]

    prevention:
      - "[How to avoid this error]"

    tags: ["tag1", "tag2"]

    metadata:
      project: "[project-name]"
      discovered_by: "knowledge-curator-subagent"
      date_discovered: "2026-01-07"
      tested: true
      verified: true
      frequency: "occasional"
```

## Workflow

### 1. Analyze Session

```python
# Scan conversation for key moments
key_moments = analyze_conversation(history)

# Categorize findings
errors = [m for m in key_moments if m.type == "error"]
decisions = [m for m in key_moments if m.type == "decision"]
patterns = [m for m in key_moments if m.type == "pattern"]
```

### 2. Determine Scope

```python
# Decision tree for KB scope
def determine_scope(knowledge):
    # Check if universal/shared
    if knowledge.scope in ["docker", "python", "postgresql", "javascript", "universal"]:
        if is_cross_project_relevant(knowledge):
            return "shared_kb"
    # Otherwise project-specific
    return "project_kb"
```

### 3. Create Entry

```python
if scope == "shared_kb":
    # Create GitHub issue
    issue = create_github_issue(knowledge)
    notify_user(f"📝 GitHub issue created: {issue.url}")
else:
    # Create YAML file
    yaml_file = create_yaml_entry(knowledge)
    validate(yaml_file)
    notify_user(f"✅ Project KB entry created: {yaml_file}")
```

### 4. Validate Quality

```python
# Quality scoring
score = calculate_quality_score(entry)

if score >= 75:
    commit_entry(entry)
    notify_user(f"✅ Entry committed (score: {score}/100)")
else:
    enhance_entry(entry)
    notify_user(f"⚠️ Entry enhanced (score: {score} → {new_score}/100)")
```

## Communication Protocol

### Request Format

```yaml
type: knowledge_capture_request
request_id: capture-xyz789

session_context:
  duration_minutes: 45
  task_description: "Implement WebSocket notifications"
  task_status: "success"

findings:
  errors:
    - error: "WebSocket timeout after 5 seconds"
      solution: "Configure uvicorn ws_max_size"
      verified: true

  decisions:
    - decision: "Use WebSocket over polling"
      rationale: "Real-time requirements, better UX"
      alternatives: ["Long-polling", "Server-sent events"]

  patterns:
    - pattern: "Centralized WebSocket management"
      description: "Single connection manager class"

capture_options:
  auto_categorize: true
  create_github_issues: true
  validate_quality: true
  min_quality_score: 75

output_format: "both"  # github_issue + yaml
```

### Response Format

```yaml
type: knowledge_capture_response
request_id: capture-xyz789

analysis:
  key_moments_found: 3
  errors_captured: 1
  decisions_documented: 1
  patterns_identified: 1

entries_created:
  - type: "github_issue"
    scope: "shared_kb"
    url: "https://github.com/ozand/shared-knowledge-base/issues/123"
    status: "created"

  - type: "yaml_file"
    scope: "project_kb"
    path: "docs/knowledge-base/project/websocket-timeout.yaml"
    status: "created"

quality_metrics:
  average_score: 82
  min_score: 75
  max_score: 89

recommendations:
  - "Consider adding WebSocket monitoring to operations"
  - "Document connection lifecycle for new developers"

completion_status: "success"
duration_seconds: 3.7
```

## Integration Examples

### Example 1: Post-Error Capture

```python
# Primary agent just fixed an error
if error_fixed:
    Task(
        subagent_type="knowledge-curator",
        prompt="""
        Capture this error resolution:

        Error: WebSocket timeout after 5 seconds
        Context: FastAPI 0.104, uvicorn default
        Solution: Set ws_max_size in uvicorn.Config
        Verified: Tested locally, works in dev

        Please determine if this should be:
        - Shared KB (seems like common FastAPI issue)
        - Project KB (specific to our setup)

        Create appropriate entry and notify me.
        """
    )

    # Continue with next task
    # Knowledge capture happens in background
```

### Example 2: Feature Completion Retrospective

```python
# Primary agent completed feature
if feature_complete:
    # Launch knowledge curator
    result = Task(
        subagent_type="knowledge-curator",
        prompt=f"""
        Analyze feature implementation for knowledge:

        Feature: Real-time notifications
        Duration: {session_duration}
        Status: Complete

        Key moments:
        - Researched WebSocket vs polling (chose WebSocket)
        - Fixed timeout issue (configured uvicorn)
        - Implemented connection manager pattern
        - Added reconnection logic

        Capture:
        1. Error solutions
        2. Decisions made
        3. Patterns discovered
        4. Best practices

        Auto-categorize scope (shared vs project KB)
        Create GitHub issues for shared knowledge
        """,
        run_in_background=False  # Wait for completion
    )

    # Review what was captured
    print(f"✅ Created {result.entries_created} KB entries")
    print(f"📊 Average quality: {result.quality_metrics.average_score}/100")
```

### Example 3: Session End Retrospective

```python
# Automatic trigger at session end
# Hook configured in settings.json

# Knowledge curator analyzes entire session
# Creates entries for all discovered knowledge
# Reports summary to user

# Output:
"""
🔍 SESSION RETROSPECTIVE

Session Duration: 2 hours 15 minutes
Key Moments Found: 7

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Captured Knowledge:

✅ Shared KB Entries (GitHub Issues):
1. FastAPI WebSocket timeout configuration (Issue #123)
2. Docker Compose service dependency pattern (Issue #124)

✅ Project KB Entries (YAML):
1. Authentication flow decision (PROJECT-042)
2. Database migration strategy (PROJECT-043)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Quality Metrics:
- Average Score: 84/100
- All entries ≥75 threshold ✅

💡 Next Steps:
1. Review GitHub issues
2. Approve or enhance entries
3. Sync to shared repository

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
```

## Quality Standards

### Knowledge Worth Capturing

**Capture if:**
✅ Error took >5 minutes to resolve
✅ Solution is reusable
✅ Decision has architectural impact
✅ Pattern is best practice
✅ Finding is counter-intuitive

**Skip if:**
❌ Trivial fix (typo, obvious error)
❌ Project-specific one-liner
❌ Temporary workaround
❌ Already documented in KB

### Quality Scoring Rubric

**Completeness (0-30):**
- All required fields: 30
- Missing 1-2 fields: 20
- Missing 3+ fields: 10

**Technical Accuracy (0-30):**
- Tested solution: 30
- Code compiles/runs: 20
- Theoretical: 10

**Documentation (0-20):**
- Clear problem: 10
- Good explanation: 10

**Best Practices (0-20):**
- Follows standards: 10
- Has prevention tips: 10

**Minimum:** 75/100
**Target:** 85/100

## Best Practices

### For Primary Agents

1. **Provide context** when triggering knowledge capture
2. **Mark verified** solutions appropriately
3. **Include alternatives** considered
4. **Note impact** of decisions

### For Knowledge Capture

1. **Be specific** in problem descriptions
2. **Include code examples** for solutions
3. **Add prevention tips** for errors
4. **Cross-reference** related entries
5. **Honest quality scores** - don't inflate

## Error Handling

### Low Quality Score

```markdown
⚠️ WARNING: Entry Quality Below Threshold

**Score:** 68/100
**Threshold:** 75/100

**Issues:**
- Missing root_cause field (-10)
- No prevention tips (-10)
- Code not verified (-12)

**Auto-Enhancement Applied:**
✅ Added root_cause based on solution
✅ Suggested 2 prevention tips
⚠️ Code verification required - please test

**New Score:** 78/100
**Status:** Ready for review

**Please verify:**
- [ ] Code works as documented
- [ ] Explanation is clear
- [ ] Prevention tips are relevant
```

### Uncertain Scope

```markdown
❓ UNCERTAIN: Shared KB vs Project KB

**Knowledge:** FastAPI WebSocket timeout configuration

**Analysis:**
- **Shared KB indicators:**
  ✅ Common FastAPI issue
  ✅ Framework-agnostic solution
  ✅ Reusable across projects

- **Project KB indicators:**
  ⚠️ Specific to our uvicorn version
  ⚠️ Custom configuration

**Recommendation:** Shared KB
**Confidence:** 80%

**Rationale:**
While configuration details are specific to our setup, the core issue (WebSocket timeout) and solution (uvicorn configuration) are common across FastAPI projects.

**Created:** GitHub Issue (you can move to Project KB if needed)
```

## Configuration

### Settings

```json
// .claude/agents/subagents/knowledge-curator.json
{
  "enabled": true,
  "triggers": {
    "on_error_resolved": true,
    "on_task_complete": true,
    "on_session_end": true
  },
  "quality_threshold": 75,
  "auto_enhance": true,
  "create_github_issues": true,
  "default_scope": "auto",
  "tools": [
    "Grep",
    "Read",
    "Write",
    "GitHubCreateIssue"
  ]
}
```

## Integration with Other Subagents

### Researcher → Knowledge Curator

```python
# Researcher found solution
# Pass to knowledge curator for documentation

research_result = Task(subagent_type="researcher", ...)

if research_result.confidence >= 85:
    # High confidence - auto-capture
    Task(
        subagent_type="knowledge-curator",
        prompt=f"Capture research result: {research_result}",
        context={"auto_approve": True}
    )
else:
    # Low confidence - ask user first
    notify_user(f"Research found solution (confidence: {research_result.confidence}%). Capture to KB?")
```

### Primary Agent → Knowledge Curator

```python
# Primary agent completed task
# Trigger knowledge capture automatically

if task_completed:
    Task(
        subagent_type="knowledge-curator",
        prompt="Analyze task completion for knowledge",
        context={
            "task": current_task,
            "errors": encountered_errors,
            "solutions": implemented_solutions
        }
    )
```

## Related Agents

- **researcher** - Finds solutions (knowledge curator documents them)
- **primary-agent** - Initiates knowledge capture
- **kb-curator** - Reviews KB entries (different from capture)
- **validator** - Tests solutions before documentation

## Version History

**v1.0** (2026-01-07)
- Initial implementation
- Session analysis
- Automatic scope detection
- GitHub issue creation
- Project KB YAML generation

---

**Agent Type:** Autonomous Knowledge Capture Subagent
**Maintained By:** KB Curator
**Dependencies:** Grep, Read, Write, GitHub API
**Status:** Production Ready
## @references (Progressive Disclosure)

**Load specific sections on demand to reduce token usage:**

- **Role Definition:** `@KNOWLEDGE-CURATOR.md#role-definition` (Lines 9-80)
- **Trigger Conditions:** `@KNOWLEDGE-CURATOR.md#trigger-conditions` (Lines 82-140)
- **Capture Workflow:** `@KNOWLEDGE-CURATOR.md#capture-workflow` (Lines 142-280)
- **Documentation Standards:** `@KNOWLEDGE-CURATOR.md#documentation-standards` (Lines 282-400)
- **Quality Assurance:** `@KNOWLEDGE-CURATOR.md#quality-assurance` (Lines 402-540)
- **Integration Points:** `@KNOWLEDGE-CURATOR.md#integration-points` (Lines 542-660)

**Related Documentation:**
- `@../AGENT.md` - Main Curator agent
- `@../../../../../agents/curator/AGENT.md` - Curator role
