# Retrospective

Analyze the current Claude Code session to extract valuable knowledge and add it to the Knowledge Base.

## Usage
```
/retrospective [option]
```

## Examples

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

### Specific Analysis Type
```
/retrospective --errors
```
Focus only on errors and their solutions.

### Scope Selection
```
/retrospective --scope universal
```
Only look for universal/shared knowledge.

## What happens

### Phase 1: Conversation Analysis
1. Scans conversation from start (or last retrospective)
2. Identifies key moments:
   - Errors encountered
   - Solutions implemented
   - Decisions made
   - Patterns discovered
   - Best practices used

### Phase 2: Knowledge Extraction
For each key moment, extracts:
- **Problem:** What went wrong or question asked
- **Solution:** How it was resolved
- **Context:** Language/framework/environment
- **Tags:** Relevant keywords
- **Scope:** universal, python, javascript, docker, postgresql, project, domain

### Phase 3: Categorization
Determines where knowledge should go:

**Shared KB (requires GitHub issue):**
- ✅ Universal patterns (docker, universal scope)
- ✅ Language-specific best practices (python, javascript, postgresql)
- ✅ Cross-cutting concerns (git, testing, architecture)
- ✅ Framework-agnostic solutions

**Project KB (direct addition):**
- ✅ Project-specific logic
- ✅ Domain knowledge
- ✅ Environment-specific configurations
- ✅ Business rules

### Phase 4: Output Generation

**For Shared KB entries:**
Creates GitHub issue template:
```markdown
## Add to Shared KB: [Title]

**Scope:** [universal/python/docker/etc]
**Category:** [category-name]
**Severity:** [critical/high/medium/low]

### Problem
[Description]

### Solution
```yaml
[code solution]
```

### Tags
[tag1, tag2, tag3]

### Context
[Additional context about when this occurred, project details, etc.]

**Discovered by:** Claude Code retrospective analysis
**Date:** [timestamp]
```

**For Project KB entries:**
Creates ready-to-use YAML entry:
```yaml
version: "1.0"
category: "[category]"
last_updated: "[date]"

errors:
  - id: "PROJECT-[NNN]"
    title: "[Title]"
    severity: "medium"
    scope: "project"

    problem: |
      [Description]

    solution:
      code: |
        [Solution code]

    tags: ["tag1", "tag2"]
```

## Options

- `--last` - Analyze only since last retrospective (not implemented yet)
- `--errors` - Focus on errors only (not implemented yet)
- `--scope <scope>` - Filter by scope (universal, python, docker, etc.)
- `--project` - Target project KB instead of shared KB
- `--dry-run` - Show what would be extracted without creating issues/entries

## Output Examples

### Example 1: Error Discovered
```
🔍 RETROSPECTIVE ANALYSIS

Session Duration: 45 minutes
Key Moments Found: 3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY MOMENT #1: Docker Volume Permission Error

Problem: Docker container failed with permission denied on volume mount
Context: Docker Compose, Linux host, development environment
Solution: Changed volume mount from relative to absolute path, added user UID
Scope: docker
Severity: medium
Tags: [docker, volumes, permissions, linux]

🎯 RECOMMENDATION: Add to Shared KB

✅ GitHub issue created: https://github.com/ozand/shared-knowledge-base/issues/[number]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Example 2: Pattern Discovered
```
🔍 RETROSPECTIVE ANALYSIS

Session Duration: 1 hour 20 minutes
Key Moments Found: 5

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY MOMENT #3: Async Context Manager Pattern

Pattern: Using async with TaskGroup for error handling in Python 3.11+
Context: FastAPI application, async endpoints
Benefit: Automatic exception gathering, cleaner code
Scope: python
Severity: low (optimization)
Tags: [async, python-3.11, taskgroup, fastapi]

🎯 RECOMMENDATION: Add to Shared KB (as pattern)

✅ GitHub issue created: https://github.com/ozand/shared-knowledge-base/issues/[number]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Example 3: Project-Specific Knowledge
```
🔍 RETROSPECTIVE ANALYSIS

Session Duration: 30 minutes
Key Moments Found: 2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEY MOMENT #2: Authentication Flow Decision

Decision: Chose JWT over session-based auth
Reasoning: Better for microservices, stateless, scalable
Context: User service architecture
Project-specific: YES

🎯 RECOMMENDATION: Add to Project KB

✅ YAML entry created: docs/knowledge-base/project/auth-flow.yaml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## When to Use

Run `/retrospective`:
- ✅ After solving a complex problem
- ✅ At end of work session (to capture knowledge)
- ✅ Before completing a feature (to ensure nothing was missed)
- ✅ After debugging session (to document solutions)
- ✅ Periodically (every 1-2 hours of work)

## Best Practices

### For Teams
- Run retrospective at least once per feature
- Review and triage GitHub issues weekly
- Add valuable discoveries to KB
- Document decisions and their rationale

### For Solo Developers
- Run retrospective before pushing code
- Create issues for shared knowledge immediately
- Add project-specific patterns to local KB
- Build up personal knowledge base over time

### Retrospective Frequency
- **After each bug fix:** Document the solution
- **After each feature:** Document decisions and patterns
- **Weekly:** Review all retrospectives, categorize and prioritize
- **Monthly:** Triage GitHub issues, add to KB

## Integration with Workflows

### Part of Development Cycle
```
1. Start task
2. Work → Encounter problem → Solve problem
3. /retrospective (analyze session)
4. Categorize findings:
   - Shared KB? → Create GitHub issue
   - Project KB? → Create YAML entry
5. Continue work or end session
```

### Part of Code Review
```
1. PR submitted
2. /retrospective (analyze PR development)
3. Add findings to KB
4. Include KB entries in PR review
5. Merge PR
```

## Related Commands
- `/kb-search` - Search KB before solving (avoid duplicates)
- `/kb-create` - Create entry from retrospective output
- `/kb-validate` - Validate entry before committing

## Troubleshooting

**"No key moments found"?**
- Session was too short or routine
- Try broader analysis scope
- Consider whether knowledge is worth capturing

**"Too many results"?**
- Use filters: --errors, --scope
- Focus on most valuable/complex solutions
- Consider running retrospective more frequently

**"Can't determine scope"?**
- Default to project scope if unsure
- Document as universal during triage
- Let curator decide on final scope

## Advanced Features

### Retrospective Markers
You can insert markers in conversation to split analysis:

```
🔄 RETROSPECTIVE COMPLETE
```

This allows running `/retrospective --last` to analyze only since last marker.

### Automatic Triggers
Can be configured to run automatically:
- On session end
- Every N messages
- When keywords detected ("error", "fixed", "decided")

### Integration with GitHub
- Automatically creates issues in shared-knowledge-base repo
- Uses template for consistency
- Tags issues by scope and category

## Tips

- **Be specific** in problem descriptions for better future search
- **Include context** - what were you trying to do?
- **Document decisions** - why did you choose X over Y?
- **Add examples** - code snippets, commands, configurations
- **Think future** - what would help future-you (or others)?

## See Also
- Skill: `research-enhance` - Enhance entries with research
- Agent: `kb-curator` - Automated KB curation
- Guide: `@for-claude-code/README.md` - Project integration guide
- Workflow: Retrospective-driven knowledge capture

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Skill Type:** Knowledge Extraction
**Integration:** GitHub API (for shared KB issues)
