# KB Query

Query the Knowledge Base for context-aware assistance during development.

## Usage
```
/kb-query <query> [options]
```

## Quick Examples

### Simple Query
```
/kb-query docker volume permissions
```
Searches KB and returns relevant entry.

### Query with Context
```
/kb-query "async error" --context "FastAPI, Python 3.11+"
```
Provides context for better results.

### Query with Code
```
/kb-query "TypeError" --code "print(user['name'])"
```
Analyzes code for targeted solutions.

### Query by Scope
```
/kb-query "memory leak" --scope universal
```
Searches only universal patterns.

## What This Command Does

1. **Searches KB** using `python tools/kb.py search "<query>"`
2. **Analyzes Results** from top 3-5 matching entries
3. **Extracts Key Information:**
   - Problem description
   - Solution code
   - Explanation
   - Prevention tips
4. **Returns Formatted Response:**
   - **Best Match:** Most relevant entry
   - **Solution:** Code example
   - **How it Works:** Technical details
   - **Related:** Links to related entries
   - **Prevention:** How to avoid issue

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `--context` | Provide framework/version context | `--context "FastAPI, 3.11"` |
| `--code` | Include code snippet for analysis | `--code "print(user['name'])"` |
| `--scope` | Filter by scope | `--scope universal` |
| `--severity` | Filter by severity | `--severity critical` |
| `--category` | Filter by category | `--category python` |

## Common Workflows

### Debugging Errors
```
/kb-query "<error message>" --code "<problematic code>"
```

### Finding Best Practices
```
/kb-query "<practice>" --scope universal
```

### Framework-Specific Issues
```
/kb-query "<issue>" --context "<framework>, <version>"
```

### Security Issues
```
/kb-query "<security concern>" --severity critical
```

**📘 Advanced Examples:** `@references/kb-query-examples.md` - Comprehensive query patterns and scenarios

## Claude's Role

When using this command:

1. **Parse the query** and extract options
2. **Execute search** using appropriate filters
3. **Read top entries** from results
4. **Synthesize response** combining:
   - Most relevant solution
   - Code examples
   - Explanation
   - Prevention strategies
   - Related entries
5. **Suggest follow-up** queries if needed

## Quality Checks

- ✅ Always show entry ID for reference
- ✅ Include code examples when available
- ✅ Explain why the solution works
- ✅ Provide prevention strategies
- ✅ Link to related entries
- ❌ Don't truncate results
- ❌ Don't guess if not found in KB

## Related

- `@skills/kb-search/SKILL.md` - KB search skill
- `@references/cli-reference.md` - Complete CLI reference
- `@references/kb-query-examples.md` - Advanced query examples
