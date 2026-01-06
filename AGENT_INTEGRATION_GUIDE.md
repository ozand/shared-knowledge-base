# Agent Integration Guide: How Agents Learn About Attribution

**Date:** 2026-01-06
**Pattern:** GITHUB-ATTRIB-001
**Purpose:** Practical instructions for integrating attribution into agent workflows

---

## 🎯 Key Principle

**Agents don't learn automatically - they must be explicitly instructed.**

There are **3 integration points** where you tell agents about attribution:

1. **System Prompts** (Agent instructions)
2. **Tool Definitions** (When creating issues/PRs)
3. **Templates** (Issue/PR body templates)

---

## 📝 Integration Method 1: System Prompts (RECOMMENDED)

### For Project Agents

**Add to agent's system prompt:**

```
When creating GitHub Issues or PRs to contribute to Shared Knowledge Base:

1. ALWAYS add "Created By" section at VERY TOP of issue body:
   ---
   **Created By:** 🤖 [Your Agent Name]
   **Project:** [Current Project Name]
   **Agent Type:** [Task Type: Code Generation/Debugging/Refactoring/Documentation]
   **Session:** [session-hash if available]
   **Date:** [YYYY-MM-DD]
   ---

2. ALWAYS add these GitHub labels:
   - agent:[agent-slug]
     • claude-code → for Claude Code agents
     • cursor-ai → for Cursor AI agents
     • copilot → for GitHub Copilot
     • curator → for Shared KB Curator agents

   - project:[PROJECT_SLUG]
     • PARSER, AParser, shared-kb, or your project name

   - agent-type:[type]
     • code-generation, debugging, refactoring, documentation, review

   - kb-improvement
   - [category]: python, postgresql, docker, etc.

3. Use GitHub CLI if available:
   gh issue create \
     --label "agent:claude-code" \
     --label "project:PARSER" \
     --label "agent-type:debugging" \
     --label "kb-improvement" \
     --title "Add PYTHON-XXX: Title" \
     --body-file issue-template.md

This makes agent attribution visible and filterable in GitHub!
Reference: GITHUB-ATTRIB-001 pattern in Shared KB.
```

### For Shared KB Curator Agent

**Add to Curator's system prompt:**

```
When processing GitHub issues created by project agents:

1. READ the "Created By" section at top of issue
2. NOTE the agent, project, and agent type from labels
3. When merging, preserve attribution in commit message:
   git commit -m "Add PYTHON-XXX: Pattern Name

   Contributed by: [project-name]
   Agent: [agent-name]
   Reviewed by: KB Curator

   Pattern: [description]

   🤖 Generated with Claude Code

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

4. When closing issues, thank the contributor:
   "✅ Merged to main!
   Thank you [agent-name] from [project-name] for your contribution! 🎉"

Reference: AGENT-HANDOFF-001, GITHUB-ATTRIB-001
```

---

## 🛠️ Integration Method 2: Tool/Function Definitions

### If Agent Has GitHub Issue Creation Tool

**Update tool definition:**

```python
# Example: Agent tool definition
tools = [
    {
        "name": "create_github_issue",
        "description": "Create a GitHub issue in shared-knowledge-base repository",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "body": {"type": "string"},
                "agent_name": {
                    "type": "string",
                    "description": "Must be: claude-code, cursor-ai, copilot, or curator",
                    "enum": ["claude-code", "cursor-ai", "copilot", "curator"]
                },
                "project_name": {
                    "type": "string",
                    "description": "Project name (e.g., PARSER, AParser, shared-kb)"
                },
                "agent_type": {
                    "type": "string",
                    "description": "Task type",
                    "enum": ["code-generation", "debugging", "refactoring", "documentation", "review"]
                }
            },
            "required": ["title", "body", "agent_name", "project_name", "agent_type"]
        }
    }
]
```

**Tool implementation (Python):**

```python
import subprocess
from datetime import datetime

def create_github_issue(title, body, agent_name, project_name, agent_type):
    """
    Create GitHub issue with agent attribution (GITHUB-ATTRIB-001)
    """
    session_hash = os.getenv('AGENT_SESSION', 'unknown')

    # Add "Created By" section at TOP
    attribution_header = f"""---
**Created By:** 🤖 {agent_name}
**Project:** {project_name}
**Agent Type:** {agent_type}
**Session:** {session_hash}
**Date:** {datetime.now().strftime('%Y-%m-%d')}
---

"""

    full_body = attribution_header + body

    # Create issue with labels
    cmd = [
        "gh", "issue", "create",
        "--label", f"agent:{agent_name}",
        "--label", f"project:{project_name}",
        "--label", f"agent-type:{agent_type}",
        "--label", "kb-improvement",
        "--title", title,
        "--body", full_body
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout
```

---

## 📋 Integration Method 3: Issue/PR Templates

### Provide Templates to Agents

**Template 1: KB Entry Contribution**

```markdown
---
**Created By:** 🤖 {{agent_name}}
**Project:** {{project_name}}
**Agent Type:** {{agent_type}}
**Session:** {{session_hash}}
**Date:** {{date}}
---

## Proposed KB Entry

**Type:** Error / Pattern

**Category:** {{category}}

**Entry ID:** {{entry_id}}

**Title:** {{title}}

## YAML Entry

```yaml
{{yaml_content}}
```

## Validation

✅ Validated using: python tools/kb.py validate

## Real-World Example

**Project:** {{project_name}}

**Scenario:** {{scenario}}

**Problem:** {{problem}}

**Solution:** {{solution}}

## Benefit

{{why_other_projects_benefit}}

## Suggested Scope

**Scope:** {{universal/python/javascript/etc}}

**Reason:** {{scope_reason}}

## Additional Notes

{{additional_context}}

---

**Attribution:**
- **Created by:** 🤖 {{agent_name}}
- **Project:** {{project_name}}
- **Session:** {{session_hash}}
- **Date:** {{date}}
- **Status:** Ready for review ✅
```

**Tell agents:**
> "Use this template when creating GitHub issues. Replace {{variables}} with actual values."

---

## 🤖 Integration Method 4: Agent Instructions File

### Create `.agent-instructions.md` in Project Root

**Example for PARSER project:**

```markdown
# Agent Instructions for PARSER Project

## When Contributing to Shared Knowledge Base

This project uses Shared KB for error patterns and best practices.

### When You Discover Reusable Patterns:

1. **Search KB first:**
   ```bash
   cd docs/knowledge-base/shared
   kb search "error keyword"
   ```

2. **If pattern not found:**
   - Create YAML entry in `/tmp/`
   - Validate: `python tools/kb.py validate /tmp/entry.yaml`
   - Create GitHub issue with attribution

3. **Required attribution format:**
   - Add "Created By" section at TOP (see template below)
   - Use labels: agent:claude-code, project:PARSER, agent-type:debugging
   - Follow GITHUB-ATTRIB-001 pattern

4. **Issue template:**
   [Paste Template 1 from above]

### Your Agent Identity:

- **Agent Name:** claude-code
- **Project:** PARSER
- **Session:** Use session hash if available
- **Agent Type:** Choose based on task:
  - code-generation → Writing new code
  - debugging → Fixing bugs
  - refactoring → Restructuring code
  - documentation → Writing docs

### References:

- GITHUB-ATTRIB-001: Full attribution pattern
- AGENT-HANDOFF-001: Contribution workflow
- Shared KB location: docs/knowledge-base/shared/
```

**Tell agents:**
> "Read .agent-instructions.md before contributing to Shared KB."

---

## 📚 Method 5: Integration in Code Comments

### For Code-Generating Agents

**Add to project README or CONTRIBUTING.md:**

```markdown
## Agent Contribution Guidelines

AI agents working on this project should follow GITHUB-ATTRIB-001
when creating GitHub Issues or PRs.

**Required:**
- "Created By" section at top of issue/PR body
- Labels: agent:*, project:*, agent-type:*
- Session tracking

See: [Shared KB]/GITHUB_ATTRIBUTION_GUIDE.md
```

---

## 🎯 Practical Implementation: Which Method to Use?

| Method | Best For | Effort | Reliability |
|--------|----------|--------|-------------|
| **System Prompts** | All agents | High | ⭐⭐⭐⭐⭐ |
| **Tool Definitions** | Agents with custom tools | Medium | ⭐⭐⭐⭐ |
| **Templates** | Manual/supervised creation | Low | ⭐⭐⭐ |
| **Agent Instructions File** | Project-specific agents | Low | ⭐⭐⭐ |
| **Code Comments** | Reminders only | Very Low | ⭐⭐ |

### RECOMMENDED Approach:

**For Maximum Compliance:**
1. **System Prompts** - Add attribution instructions to agent's system prompt
2. **Tool Wrappers** - If agent has GitHub tools, wrap them to add labels automatically
3. **Validation** - Curator checks for attribution on received issues

---

## 🔄 Example: Full Workflow

### Agent Side (Project Agent)

```
1. [User asks agent to fix error]

2. [Agent searches KB]
   kb search "asyncio timeout"
   → Not found

3. [Agent creates YAML]
   → Validated successfully

4. [Agent creates GitHub issue]
   gh issue create \
     --label "agent:claude-code" \
     --label "project:PARSER" \
     --label "agent-type:debugging" \
     --label "kb-improvement" \
     --label "python" \
     --title "Add PYTHON-015: Async Timeout Error" \
     --body-file issue-with-attribution.md

5. [Issue created with:]
   - "Created By" at top ✅
   - All labels ✅
   - Session hash ✅
```

### Curator Side (Shared KB)

```
1. [Receive issue notification]

2. [Read issue]
   → See: "Created By: 🤖 Claude Code - PARSER project"
   → See: agent:claude-code, project:PARSER labels

3. [Process issue]
   → Validate YAML
   → Enhance entry
   → Commit with attribution

4. [Close issue]
   "✅ Merged! Thank you Claude Code from PARSER project! 🎉"
```

---

## ✅ Checklist: Is Your Agent Configured?

- [ ] Agent system prompt includes attribution instructions
- [ ] Agent knows its identity (agent_name, project_name)
- [ ] Agent has access to attribution template
- [ ] Agent knows which labels to use
- [ ] Agent validates YAML before creating issue
- [ ] Agent uses GitHub CLI or API with labels
- [ ] Curator knows to check for attribution
- [ ] Curator preserves attribution in commits

---

## 🚀 Quick Start: 3 Steps

### Step 1: Add to Agent System Prompt
```
When creating GitHub issues, follow GITHUB-ATTRIB-001:
- Add "Created By" section at top
- Use labels: agent:*, project:*, agent-type:*
- See GITHUB_ATTRIBUTION_GUIDE.md for details
```

### Step 2: Tell Agent Its Identity
```
You are:
- Agent Name: claude-code
- Project: [PROJECT_NAME]
- Session Hash: [session_id if available]
```

### Step 3: Provide Template
```
Use this template for GitHub issues:
[Paste Template 1]
```

---

## 📖 References

- **GITHUB_ATTRIBUTION_GUIDE.md** - Full implementation guide (Russian)
- **universal/patterns/github-agent-attribution.yaml** - GITHUB-ATTRIB-001 pattern
- **universal/patterns/agent-handoff.yaml** - AGENT-HANDOFF-001 workflow
- **LABELS_INSTALLED.md** - List of installed labels

---

**Status:** ✅ Ready for integration
**Last Updated:** 2026-01-06
**Pattern:** GITHUB-ATTRIB-001
