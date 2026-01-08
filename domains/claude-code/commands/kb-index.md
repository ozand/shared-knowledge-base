# KB Index

Rebuild the Knowledge Base search index for fast and accurate search results.

## Usage
```
/kb-index [options]
```

## Quick Examples

### Update Index
```
/kb-index
```
Updates index with recent changes.

### Force Rebuild
```
/kb-index --force -v
```
Complete rebuild from scratch with verbose output.

## What This Command Does

1. **Scans** for all YAML files in KB
2. **Parses** entries (extracts id, title, problem, solution)
3. **Builds** SQLite FTS5 search index
4. **Reports** statistics (entry count, size, time)

**Output:**
```
✅ Index complete!
  Entries: 127
  Size: 156 KB
  Time: 2.3 seconds
```

## Options

| Option | Description |
|--------|-------------|
| `--force` | Delete old index, rebuild from scratch |
| `--verbose` or `-v` | Show detailed progress |
| `--optimize` | Optimize index for better performance |

## When to Rebuild

### Required After:
- ✅ Adding new entries
- ✅ Modifying existing entries
- ✅ Deleting entries
- ✅ Changing metadata

### Recommended:
- Weekly (if active development)
- Before major searches
- After bulk imports

### Troubleshooting:
```bash
# Search returns no results
/kb-index --force -v
```

**📘 CLI Reference:** `@references/cli-reference.md` - Complete index command documentation

## Claude's Role

When using this command:

1. **Check if index exists** (`_index_meta.yaml`)
2. **Determine rebuild type:**
   - Recent changes → Incremental update
   - Search issues → Force rebuild
3. **Execute appropriate command**
4. **Verify completion** (check entry count)
5. **Report statistics** to user

## Quality Checks

- ✅ Always rebuild after YAML modifications
- ✅ Use `--force` if search returns no results
- ✅ Verify entry count after rebuild
- ❌ Don't skip rebuild after changes

## Related

- `@skills/kb-index/SKILL.md` - KB index skill
- `@references/cli-reference.md` - Complete CLI reference
- `@references/workflows.md` - Index maintenance workflows
