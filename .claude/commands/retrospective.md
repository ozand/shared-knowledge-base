# Retrospective

Analyze the current Claude Code session to extract valuable knowledge and add it to the Knowledge Base.

## Usage
```
/retrospective [option]
```

## Quick Examples

### Full Session Analysis
```
/retrospective
```
Analyzes entire conversation history for knowledge extraction.

### Last Retrospective Only
```
/retrospective --last
```
Analyzes conversation since the last retrospective marker.

### Errors Only
```
/retrospective --errors
```
Focus only on errors and their solutions.

### Patterns Only
```
/retrospective --patterns
```
Extract best practices and patterns discovered.

## What This Command Does

1. **Scans conversation history** for:
   - Errors encountered and solved
   - Best practices discovered
   - New patterns identified
   - Lessons learned

2. **Extracts knowledge:**
   - Problem → Solution pairs
   - Code examples with explanations
   - Prevention strategies
   - Related patterns

3. **Validates and creates entries:**
   - Checks if entry already exists in KB
   - Validates new entry quality (≥75/100)
   - Determines appropriate scope
   - Creates YAML entry with proper format

4. **Suggests next steps:**
   - Review created entries
   - Sync to shared repository (if universal scope)
   - Update related entries

## Options

| Option | Description |
|--------|-------------|
| None | Full session analysis |
| `--last` | Analyze since last retrospective |
| `--errors` | Focus on errors only |
| `--patterns` | Extract patterns only |
| `--scope <scope>` | Set scope for new entries |

## Workflow

### Step 1: Analyze Conversation
Extract:
- Error messages and stack traces
- Solutions implemented
- Code snippets
- Decision rationale
- Lessons learned

### Step 2: Check for Duplicates
```bash
python tools/kb.py search "<potential error>"
```
If exists → update existing entry
If not → create new entry

### Step 3: Determine Scope
Ask:
- Is this error universal? (docker, universal, python, postgresql, javascript)
- Or project-specific? (project, domain, framework)

### Step 4: Create Entry
Use `/kb-create` to create validated entry.

### Step 5: Review and Sync
- Review created entries
- Edit if needed
- Sync to shared repository if universal scope

## Best Practices

**✅ Do:**
- Run retrospective after complex debugging sessions
- Include context and error messages
- Add code examples
- Document prevention strategies
- Review before syncing to shared repository

**❌ Don't:**
- Create entries for trivial issues
- Duplicate existing entries
- Forget to validate quality
- Mix multiple problems in one entry

## Output

**Success:**
```
✅ Retrospective complete
📝 Created 3 new entries:
  - PYTHON-123: Async timeout in FastAPI
  - DOCKER-045: Volume permission issue
  - universal/patterns/session-management-001

Next steps:
1. Review entries: /kb-query PYTHON-123
2. Sync to shared repo: /kb-sync
```

**No new knowledge:**
```
✅ Retrospective complete
💡 No new knowledge to extract
📝 All issues already documented in KB
```

## Common Workflows

### After Debugging Session
```
# 1. Run retrospective
/retrospective

# 2. Review created entries
/retrospective --last

# 3. Sync if applicable
/kb-sync python/errors/
```

### Weekly Knowledge Capture
```
# 1. Review week's sessions
/retrospective --last

# 2. Extract patterns
/retrospective --patterns

# 3. Sync best practices
/kb-sync universal/patterns/
```

## Related

- `@skills/kb-create/SKILL.md` - Create KB entries
- `@skills/audit-quality/SKILL.md` - Quality audit
- `@commands/kb-sync.md` - Sync to shared repository
- `@references/workflows.md` - Complete workflow guide
