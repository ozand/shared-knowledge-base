# KB Index

Rebuild the Knowledge Base search index to ensure fast and accurate search results.

## Usage
```
/kb-index [options]
```

## Examples

### Update Index (Incremental)
```
/kb-index
```
Updates index with recent changes

### Force Rebuild
```
/kb-index --force
```
Deletes old index and rebuilds from scratch

### Verbose Rebuild
```
/kb-index --force -v
```
Shows detailed progress during rebuild

## What happens

### Step 1: Scan for YAML Files
```
Scanning: . (recursive)
Found: 45 YAML files
```

### Step 2: Parse Entries
```
Parsing entries...
  ✓ python/errors/imports.yaml (3 entries)
  ✓ claude-code/patterns/claude-code-hooks.yaml (1 entry)
  ... (43 more files)
Total: 127 entries
```

### Step 3: Build Search Index
```
Building search index...
  By scope:
    - universal: 15 entries
    - python: 32 entries
    - javascript: 18 entries
    - docker: 22 entries
    - postgresql: 12 entries
    - framework: 28 entries

  By severity:
    - critical: 8 entries
    - high: 45 entries
    - medium: 52 entries
    - low: 22 entries
```

### Step 4: Statistics
```
✅ Index complete!
  Database: _index_meta.yaml
  Entries: 127
  Size: 156 KB
  Time: 2.3 seconds
```

## Options

- `--force` - Delete old index and rebuild completely
- `--verbose` or `-v` - Show detailed progress
- `--optimize` - Optimize index for better performance

## When to Rebuild

### Mandatory Rebuild
✅ After adding 5+ new entries
✅ After major restructuring
✅ After modifying scope/category
✅ If search returns no results
✅ After git merge with conflicts

### Optional Update
⚠️ After single entry change (usually auto-updated)
⚠️ After metadata update
⚠️ Periodic maintenance (weekly)

### Force Rebuild
🔧 Index corrupted
🔧 Search not working
🔧 Moved/renamed files
🔧 Changed YAML structure

## Index Statistics

```bash
# Check statistics
/kb-stats
```

Shows:
- Total entries (errors + patterns)
- Entries by scope
- Entries by severity
- Quality score distribution
- Index size and last build time

## Output Format

### Normal Update
```
🔍 Updating KB index...

Scanning for YAML files...
  Found: 45 files

Parsing entries...
  ✓ Parsed 127 entries

Updating index...
  ✓ Indexed 127 entries
  ✓ Categories: 12
  ✓ Tags: 89

✅ Index updated successfully
```

### Force Rebuild (Verbose)
```
🔍 Rebuilding KB index (--force -v)...

Step 1: Deleting old index...
  ✓ Removed: _index_meta.yaml

Step 2: Scanning for YAML files...
  Scanning: . (recursive)
  ✓ Found: 45 YAML files

Step 3: Parsing entries...
  ✓ python/errors/imports.yaml (3 entries)
  ✓ universal/patterns/claude-code-hooks.yaml (1 entry)
  ✓ python/errors/testing.yaml (5 entries)
  ... (42 more files)
  Total: 127 entries

Step 4: Building search index...
  Creating tables...
  ✓ entries (127 rows)
  ✓ search_index (FULLTEXT)

  Indexing by scope:
    - universal: 15 entries (11.8%)
    - python: 32 entries (25.2%)
    - javascript: 18 entries (14.2%)
    - docker: 22 entries (17.3%)
    - postgresql: 12 entries (9.4%)
    - framework: 28 entries (22.0%)

  Indexing by severity:
    - critical: 8 entries (6.3%)
    - high: 45 entries (35.4%)
    - medium: 52 entries (40.9%)
    - low: 22 entries (17.3%)

Step 5: Metadata...
  ✓ Categories: 12 unique
  ✓ Tags: 89 unique
  ✓ Quality: min 65, max 98, avg 82.3

✅ Index rebuild complete!
  Database: _index_meta.yaml
  Entries: 127
  Size: 156 KB
  Time: 2.3 seconds
```

## Tips

- **Use --force sparingly** - Only for major changes
- **Run after edits** - Keep index current
- **Check statistics** - Verify index health
- **Monitor size** - Index should stay under 10 MB

## Maintenance Schedule

### Daily
- Index updates automatically via hooks
- No manual action needed

### Weekly
- Check index statistics
- Force rebuild if needed

### Monthly
- Force rebuild with --optimize
- Verify search functionality
- Check index size

## Related Commands
- `/kb-search` - Test search after indexing
- `/kb-validate` - Validate entries before indexing
- `/kb-stats` - Show index statistics

## Troubleshooting

### Issue: "No results found"
**Cause:** Index not built or stale
**Fix:**
```bash
/kb-index --force -v
```

### Issue: "Index corrupted"
**Symptoms:** Search errors, crashes
**Fix:**
```bash
/kb-index --force
```

### Issue: "Slow search"
**Cause:** Too many entries, unoptimized index
**Fix:**
```bash
/kb-index --force --optimize
```

### Issue: "Missing entries"
**Check:**
```bash
# Verify file exists
ls python/errors/new-entry.yaml

# Rebuild index
/kb-index --force

# Verify entry in index
/kb-search "title from entry"
```

## See Also
- Skill: `kb-index` - Full indexing documentation
- Index Tool: `@tools/kb.py` (index command)
- Indexing Pattern: `@universal/patterns/kb-indexing.yaml`
