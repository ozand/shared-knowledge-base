---
allowed-tools: Bash, Read, Write, Edit
description: Analyze chat history to extract knowledge from errors and solutions
---

## Your task
Perform a retrospective analysis of the conversation to extract valuable knowledge from errors encountered and solutions implemented.

### Step 1: Analyze the conversation
Review the conversation history and identify:
- **Errors encountered:** Error messages, exceptions, failures
- **Solutions implemented:** Code fixes, configuration changes, workarounds
- **Decisions made:** Technical choices with rationale
- **Lessons learned:** Best practices, patterns discovered
- **Context:** Framework, language, environment details

Focus on extracting:
```
1. Problem → Solution pairs
2. Code examples with explanations
3. Prevention strategies
4. Root cause analysis
```

### Step 2: For each identified knowledge item:

#### A. Check if already exists in KB
```bash
python tools/kb.py search "<error关键词或问题描述>"
```

#### B. Determine scope
Ask yourself:
- **Is this universal?** (docker, universal, python, postgresql, javascript, vps)
  - Generic pattern applicable across projects?
  - Library/framework tool issue?
  - Best practice or standard approach?

- **Or project-specific?** (project, domain, framework)
  - Business logic specific to this project?
  - Internal URLs, secrets, or infrastructure?
  - Domain-specific knowledge?

This IS the Shared KB repository, so:
- Universal patterns → add to `domains/` directly
- Project-specific (meta, development, tooling) → could document but not for distribution

### Step 3: Create knowledge entries

For each valuable knowledge item, create a YAML entry following this format:

```yaml
version: "1.0"
category: "category-name"
last_updated: "2026-01-11"

errors:
  - id: "SCOPE-NNN"  # e.g., DOCKER-024, PYTHON-123
    title: "Error Title or Problem Description"
    severity: "high"  # critical | high | medium | low
    scope: "python"   # universal | python | javascript | docker | postgresql | vps
    problem: |
      Detailed description of what went wrong.
      Include error messages, stack traces, and context.
    solution:
      code: |
        # Solution code here
        # Include imports, configuration, etc.
      explanation: |
        How the solution works.
        Why it fixes the problem.
    prevention: |
      How to prevent this issue in the future.
    tags:
      - "keyword1"
      - "keyword2"
```

### Step 4: Save entries

**For Shared KB (universal):**
```bash
# Save directly to domains/<scope>/<category>-<name>.yaml
```

**After saving:**
1. Validate: `python tools/kb.py validate domains/`
2. Rebuild index: `python tools/kb.py index --force -v`
3. Commit changes

### Step 5: Validate entries
```bash
# Validate the created entry
python tools/kb.py validate <path-to-yaml>

# Rebuild index
python tools/kb.py index --force -v
```

### Step 6: Report summary

Provide a formatted summary:

```markdown
## 📊 Retrospective Analysis Complete

### ✅ Knowledge Items Extracted: N

#### 1. [ID] Title
- **Scope:** universal/project
- **Severity:** high/medium/low
- **Saved to:** path/to/file.yaml
- **Action:** Created/Already exists

#### 2. [ID] Title
...

### 📈 Summary
- New entries created: N
- Already documented: N
- Universal patterns: N
- Repository-specific: N

### 🎯 Next Steps
1. Review created entries
2. Edit if needed: <paths>
3. Commit and push to repository
```

## Best Practices

**✅ Extract:**
- Errors with non-obvious solutions
- Solutions that required research/debugging
- Configuration patterns that work
- Best practices discovered
- Anti-patterns to avoid

**❌ Skip:**
- Trivial issues (typos, syntax errors)
- Project-specific business logic details
- Secrets, passwords, sensitive data
- Temporary workarounds
- Issues already well-documented

**💡 Tips:**
- Be specific in error descriptions
- Include complete, runnable code examples
- Explain WHY the solution works
- Add prevention strategies
- Use clear, searchable titles
- Add relevant tags for discoverability
- Check existing entries in domains/ to avoid duplicates

## Example Output

```markdown
## 📊 Retrospective Analysis Complete

### ✅ Knowledge Items Extracted: 2

#### 1. [CLAUDE-CODE-046] Plugin Bash Permission Check Error
- **Scope:** claude-code
- **Severity:** high
- **Problem:** Bash permission check failed for template expressions with `!`
- **Saved to:** domains/claude-code/errors/plugin-permission-check.yaml
- **Action:** Created

#### 2. [UNIVERSAL-089] MCP Server Integration Pattern
- **Scope:** universal
- **Severity:** medium
- **Problem:** How to integrate MCP server with Claude Desktop
- **Saved to:** domains/universal/patterns/mcp-integration-001.yaml
- **Action:** Created

### 📈 Summary
- New entries created: 2
- Already documented: 0
- Universal patterns: 2

### 🎯 Next Steps
1. Review the 2 created entries
2. Validate and rebuild index:
   ```bash
   python tools/kb.py validate domains/
   python tools/kb.py index --force -v
   ```
3. Commit and push:
   ```bash
   git add domains/
   git commit -m "Add: Plugin permission check fix and MCP integration pattern"
   git push
   ```
```

Execute these steps using the available tools. Analyze the conversation thoroughly and extract all valuable knowledge items.
