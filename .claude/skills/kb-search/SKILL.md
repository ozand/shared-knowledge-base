# Skill: KB Search

## What this Skill does
Search the Shared Knowledge Base for error solutions, patterns, and best practices across multiple languages and frameworks.

## Trigger
- User mentions "search kb", "find error", "look up solution", "kb search"
- User asks about specific errors or patterns
- Called by other agents when troubleshooting

## What Claude can do with this Skill

### 1. Basic Search
Search by query string:
```bash
python tools/kb.py search "websocket timeout"
```

### 2. Filtered Search
Search with filters:
```bash
# By category
python tools/kb.py search --category python

# By severity
python tools/kb.py search --severity high

# By scope
python tools/kb.py search --scope universal

# By tags
python tools/kb.py search --tags async pytest

# Combined filters
python tools/kb.py search --category python --severity high --tags async
```

### 3. Display Results
- Show matching entries with ID, title, severity
- Display file paths for easy access
- Show relevance ranking
- Suggest related entries

## Key files to reference
- Main CLI: `@tools/kb.py`
- Search implementation: `tools/search-kb.py`
- Index: `_index_meta.yaml`

## Implementation rules
1. Always show full results, don't truncate
2. Display file paths for easy navigation
3. Include severity and scope in results
4. If no results, suggest alternative search terms
5. Offer to open relevant files

## Common commands
```bash
# Basic search
python tools/kb.py search "error message"

# Search with filters
python tools/kb.py search --category python --severity high

# Search in specific scope
python tools/kb.py search --scope docker "volume"

# Note: Use search query to filter results
# First 50 results are displayed by default
```

## Search Strategy
1. **Broad first** - Start with general terms
2. **Filter down** - Use category/severity/scope filters
3. **Check synonyms** - Try related terms
4. **Look cross-scope** - Check universal patterns too

## Output format
```
🔍 Search Results for "websocket timeout"

Found 3 matches:

1. [PYTHON-045] WebSocket Timeout Error (high)
   📁 python/errors/websocket.yaml
   📝 WebSocket connections timing out after 30 seconds...
   🏷️  Tags: async, websocket, timeout

2. [UNIVERSAL-012] Timeout Patterns (medium)
   📁 universal/patterns/timeout-handling.yaml
   📝 Generic timeout handling patterns across languages...
   🏷️  Tags: timeout, patterns, best-practices

3. [FASTAPI-023] FastAPI WebSocket Issues (high)
   📁 framework/fastapi/errors/websocket.yaml
   📝 FastAPI-specific WebSocket connection problems...
   🏷️  Tags: fastapi, websocket, async

💡 Suggest opening: python/errors/websocket.yaml
```

## Related Skills
- `kb-validate` - Validate entries after search
- `kb-create` - Create new entry if not found
- `find-duplicates` - Check for similar entries

## Troubleshooting
- **No results**: Try broader search terms or different scope
- **Too many results**: Add filters (--category, --severity, --scope)
- **Index outdated**: Run `python tools/kb.py index --force -v`

## Quality Check
Before using search results:
- Verify the solution applies to your context
- Check the scope (universal vs language-specific)
- Look for version-specific notes
- Consider related entries

---
**Version:** 1.0
**Last Updated:** 2026-01-07
**Skill Type:** Search & Retrieval
