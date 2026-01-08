# KB Search

Search the Knowledge Base for error solutions, patterns, and best practices.

## Usage
```
/kb-search <query> [options]
```

## Examples

### Basic Search
```
/kb-search websocket timeout
```
Searches all entries for "websocket timeout"

### Filtered Search
```
/kb-search async error --category python --severity high
```
Search Python errors with high severity about async errors

### Search by Tags
```
/kb-search --tags websocket,async
```
Find entries tagged with websocket and async

### Search by Scope
```
/kb-search timeout --scope universal
```
Search universal patterns for timeout issues

## What happens

1. **Search Execution**
   ```bash
   python tools/kb.py search "<query>"
   ```

2. **Results Display**
   - Matching entries with ID and title
   - File paths for easy navigation
   - Severity and scope information
   - Relevant tags

3. **Suggestions**
   - Top related entries
   - Alternative search terms if no results
   - Option to open relevant files

## Options

- `--category <name>` - Filter by category (python, javascript, docker, etc.)
- `--severity <level>` - Filter by severity (critical, high, medium, low)
- `--scope <scope>` - Filter by scope (universal, language, framework, etc.)
- `--tags <tags>` - Filter by comma-separated tags

**Note:** First 50 results are displayed. Use specific filters to narrow results.

## Output Format
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

💡 Suggest opening: python/errors/websocket.yaml
```

## Tips

- **Broad first** - Start with general terms, then add filters
- **Check synonyms** - Try related terms if no results
- **Look cross-scope** - Check universal patterns too
- **Use tags** - Filter by relevant tags for precision

## Related Commands
- `/kb-validate` - Validate entries after search
- `/kb-create` - Create new entry if not found

## Troubleshooting

**No results found?**
- Try broader search terms
- Remove filters
- Check different scope (universal vs language-specific)

**Too many results?**
- Add filters (--category, --severity, --scope)
- Use more specific search terms
- Filter by tags

## See Also
- Skill: `kb-search` - Full search documentation
- Guide: `@tools/kb.py` - Main CLI reference
