# KB Query

Query the Knowledge Base for context-aware assistance during development.

## Usage
```
/kb-query <query> [context]
```

## Examples

### Simple Query
```
/kb-query docker volume permissions
```
Searches KB and returns relevant entry with context.

### Query with Context
```
/kb-query "async error" --context "FastAPI, Python 3.11+"
```
Provides additional context for better results.

### Query with Code Snippet
```
/kb-query "TypeError" --code "print(user['name'])"
```
Analyzes code to provide more targeted solutions.

### Query by Scope
```
/kb-query "memory leak" --scope universal
```
Only searches universal patterns.

## What happens

### Step 1: Search KB
```bash
python tools/kb.py search "<query>"
```
Finds relevant entries based on keywords.

### Step 2: Analyze Results
- Reads top 3-5 matching entries
- Extracts key information:
  - Problem description
  - Solution code
  - Explanation
  - Prevention tips

### Step 3: Provide Contextual Response
Returns formatted response with:
- **Best Match:** Most relevant entry
- **Solution:** Code example with explanation
- **How it Works:** Technical details
- **Related:** Links to related entries
- **Prevention:** How to avoid this issue

### Step 4: Suggest Next Steps
- Open relevant file for viewing
- Suggest creating new entry if not found
- Recommend related documentation

## Output Format

### Simple Query
```
🔍 KB QUERY: "docker volume permissions"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Best Match: DOCKER-003 (Score: 95%)

Problem: Container cannot read/write to volume due to permissions.

Solution:
```yaml
services:
  app:
    volumes:
      - ./data:/data:rw  # Explicit permissions
    user: "${UID:-1000}:${GID:-1000}"  # Run as specific user
```

How it Works:
- Mounts volume with explicit read-write permissions
- Runs container as specific user ID (matches host user)
- Avoids permission mismatch between host and container

Prevention:
- Always specify user UID/GID when using bind mounts
- Use named volumes for simpler permission management
- Test volume access in development first

Related Entries:
- DOCKER-020: Docker Automatically Recreates Directories
- UNIVERSAL-006: Filesystem Permissions Best Practices

💡 Action: Open docker/errors/common-errors.yaml
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Query with Context
```
🔍 KB QUERY: "async error" (Context: FastAPI, Python 3.11+)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Best Match: PYTHON-018 (Score: 87%)

Problem: Improper async error handling in FastAPI endpoints.

Solution (Python 3.11+):
```python
import asyncio
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def endpoint():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(task1())
            tg.create_task(task2())
        # All exceptions automatically gathered
    except* Exception as e:
        logger.error(f"Tasks failed: {e}")
        raise
```

How it Works:
- TaskGroup (Python 3.11+) automatically awaits all tasks
- Exceptions grouped into ExceptionGroup
- No detached tasks, no lost exceptions

Prevention:
- Use TaskGroup for multiple concurrent tasks
- Never use asyncio.create_task() without await
- Enable asyncio debug mode in development

Context Applied:
- ✅ FastAPI framework confirmed
- ✅ Python 3.11+ features utilized
- ✅ Modern async error handling pattern

Related Entries:
- FASTAPI-023: FastAPI WebSocket Issues
- PYTHON-045: Async Timeout Handling

💡 Action: Open python/errors/async-errors.yaml
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### No Results Found
```
🔍 KB QUERY: "custom business logic"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ No matching entries found in Knowledge Base

💡 Suggestions:

1. Search with broader terms
   - Try: /kb-query "business logic"
   - Try: /kb-query "domain logic"

2. Check if this is project-specific
   - If yes: Consider adding to Project KB
   - Run: /kb-create --scope project

3. Consider adding to Shared KB
   - If solution is reusable: /kb-create --scope <language>
   - Run: /kb-sync to push to shared repository

4. Related Resources:
   - Check documentation: /kb-query "architecture"
   - Check patterns: /kb-query "best practices"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Options

- `--scope <scope>` - Limit search to specific scope
- `--context "<text>"` - Provide additional context
- `--code "<snippet>"` - Include code snippet for analysis
- `--open` - Automatically open best matching file
- `--create` - Create new entry if not found

## Usage Patterns

### During Development
```bash
# Before implementing feature
/kb-query "authentication pattern" --context "FastAPI, microservices"

# After encountering error
/kb-query "docker timeout" --code "docker-compose up"

# Making architectural decision
/kb-query "microservices vs monolith"
```

### During Code Review
```bash
# Check if solution follows best practices
/kb-query "async pattern" --code "await create_task()"

# Verify if error handling is correct
/kb-query "exception handling" --context "Python, asyncio"
```

### During Debugging
```bash
# Get solution for specific error
/kb-query "port already in use" --context "Docker, port 3000"

# Understand root cause
/kb-query "permission denied" --scope docker
```

## Related Commands
- `/kb-search` - Direct search (no AI analysis)
- `/kb-create` - Create new entry from query
- `/retrospective` - Find KB-worthy moments in session
- `/kb-sync` - Sync new entries to repository

## Comparison: kb-query vs kb-search

### /kb-search (Direct Search)
- Returns raw search results
- Lists all matches
- Shows file paths
- No analysis or interpretation

**Use when:**
- You know exactly what you're looking for
- Want to see all options
- Need file paths for navigation

### /kb-query (Intelligent Query)
- Analyzes best match
- Extracts key information
- Provides formatted response
- Offers contextualized solution

**Use when:**
- You need understanding, not just results
- Want the best solution highlighted
- Need explanation of how it works
- Want prevention tips

## Advanced Features

### Code Analysis
When using `--code` option:
1. Parses code snippet
2. Identifies patterns, keywords, issues
3. Searches KB for relevant entries
4. Provides targeted solution

### Context-Aware Search
When using `--context` option:
1. Weights results by context relevance
2. Filters by applicable frameworks/versions
3. Provides solution optimized for context
4. Notes if context differs from entry

### Automatic Entry Creation
With `--create` option:
1. If no exact match found
2. Creates draft entry using query + context + code
3. Validates entry (quality score)
4. Opens editor for refinement
5. Suggests appropriate scope

## Best Practices

### Effective Queries
- ✅ Be specific: "docker volume permission denied" not "docker problem"
- ✅ Include context: Framework, version, environment
- ✅ Use code snippets: Show actual problematic code
- ❌ Avoid too broad: "error" (too many results)
- ❌ Avoid too specific: Exact error message (might not match)

### Iterative Querying
1. Start broad: `/kb-query "async error"`
2. Add context: `/kb-query "async error" --context "FastAPI"`
3. Add code: `/kb-query "async error" --code "<snippet>"`
4. Narrow scope: `/kb-query "async" --scope python`

### When No Results
1. Try broader search terms
2. Check different scope
3. Consider if knowledge doesn't exist yet
4. Think about creating new entry
5. Run `/retrospective` first to capture solution

## Integration with Workflows

### Before Implementation
```bash
# Check for existing patterns
/kb-query "authentication JWT" --context "FastAPI, microservices"

# Use findings to inform implementation
# Avoid reinventing the wheel
```

### After Error Resolution
```bash
# Find best practice solution
/kb-query "docker compose timeout" --code "<docker-compose.yml>"

# Document solution in KB
/kb-create --scope docker --category timeouts

# Sync to shared repository
/kb-sync docker/errors/compose-timeout.yaml
```

### During Code Review
```bash
# Verify implementation follows best practices
/kb-query "error handling pattern" --context "Python, asyncio"

# Suggest improvements if suboptimal
# Check for existing solutions before suggesting new approaches
```

## Troubleshooting

**"Too many results"?**
- Add more specific keywords
- Use `--scope` to narrow down
- Provide context to filter
- Use code snippet to target exact issue

**"No results found"?**
- Try broader terms
- Check different scope
- Consider creating new entry
- Run `/retrospective` to capture current solution

**"Solution doesn't match context"?**
- Add more context with `--context`
- Include code snippet with `--code`
- Specify scope with `--scope`
- Consider creating project-specific entry

## Examples by Scenario

### Scenario 1: Docker Development
```bash
/kb-query "container restart policy" --context "production, docker-compose"
```
Returns: Best practice for restart policies in production.

### Scenario 2: Python Development
```bash
/kb-query "import error relative path" --code "from utils.helper import func"
```
Returns: Solution for relative import issues with explanation.

### Scenario 3: Debugging Session
```bash
/kb-query "database connection pool" --context "PostgreSQL, asyncpg"
```
Returns: Connection pool configuration best practices.

### Scenario 4: Code Review
```bash
/kb-query "async exception handling" --code "<async function>"
```
Returns: Whether exception handling follows best practices.

## See Also
- `/kb-search` - Direct search without AI analysis
- `/kb-create` - Create new KB entry
- `/retrospective` - Find KB-worthy content in session
- Guide: `@for-claude-code/README.md` - Project integration

---

**Version:** 1.0
**Last Updated:** 202-26-01-07
**Command Type:** Intelligent Search
**AI-Enhanced:** Yes (analyzes and formats results)
