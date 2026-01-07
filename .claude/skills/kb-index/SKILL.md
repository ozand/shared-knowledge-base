---
name: "kb-index"
description: "Rebuild the Knowledge Base search index to ensure fast and accurate search results. Indexes all YAML entries and metadata"
version: "1.0"
author: "Shared KB Curator"
tags: ["index", "search", "rebuild", "update"]
---

# Skill: KB Index

## What this Skill does
Rebuild the Knowledge Base search index to ensure fast and accurate search results. Indexes all YAML entries and metadata.

## Trigger
- User mentions "rebuild index", "update index", "kb index"
- After adding new entries
- After modifying existing entries
- Search returns no results (index may be stale)
- Called by check-index hook on session stop

## What Claude can do with this Skill

### 1. Build Index
```bash
# Build or update index
python tools/kb.py index

# Force rebuild (delete old index first)
python tools/kb.py index --force

# Verbose output (show what's being indexed)
python tools/kb.py index -v
```

### 2. What Gets Indexed

#### Content Index
- Entry IDs and titles
- Problem descriptions
- Solution descriptions
- Root causes
- Prevention strategies
- Tags and metadata

#### Metadata Index
- Categories
- Scopes
- Severity levels
- Last updated dates
- Quality scores
- Cross-references

#### Search Index Structure
```
_index_meta.yaml (SQLite database)
├── entries (table)
│   ├── id (PRIMARY KEY)
│   ├── file_path
│   ├── title
│   ├── category
│   ├── scope
│   ├── severity
│   ├── quality_score
│   ├── last_updated
│   └── tags (JSON array)
└── search_index (FULLTEXT)
    ├── content (problem + solution + root_cause)
    └── metadata (tags + category + scope)
```

### 3. Index Process
```
🔍 KB Index Building...

Step 1: Scanning for YAML files...
  Found: 45 YAML files

Step 2: Parsing entries...
  ✓ python/errors/imports.yaml (3 entries)
  ✓ universal/patterns/claude-code-hooks.yaml (1 entry)
  ... (43 more files)

Step 3: Building search index...
  Indexed: 127 total entries
  By scope:
    - universal: 15 entries
    - python: 32 entries
    - javascript: 18 entries
    - docker: 22 entries
    - postgresql: 12 entries
    - framework: 28 entries

Step 4: Metadata index...
  ✓ Categories: 12 unique
  ✓ Tags: 89 unique
  ✓ Quality scores: min 65, max 98, avg 82

✅ Index complete!
  Database: _index_meta.yaml
  Entries: 127
  Size: 156 KB
```

## Key files to reference
- Index tool: `@tools/kb.py` (index command)
- Metadata: `@_index_meta.yaml`
- Indexing pattern: `@universal/patterns/kb-indexing.yaml`

## Implementation rules
1. **Always rebuild** after batch changes
2. **Use --force** if index corrupted
3. **Check statistics** after indexing
4. **Verify search** works after rebuild
5. **Run -v** for troubleshooting

## Common commands
```bash
# Normal index (incremental update)
python tools/kb.py index

# Force complete rebuild
python tools/kb.py index --force

# Verbose mode
python tools/kb.py index -v

# Combined
python tools/kb.py index --force -v
```

## When to Rebuild

### Mandatory Rebuild
- ✅ After adding 5+ new entries
- ✅ After major restructuring
- ✅ After modifying scope/category
- ✅ If search returns no results
- ✅ After git merge with conflicts

### Optional Update
- ⚠️ After single entry change (usually auto-updated)
- ⚠️ After metadata update
- ⚠️ Periodic maintenance (weekly)

### Force Rebuild
- 🔧 Index corrupted
- 🔧 Search not working
- 🔧 Moved/renamed files
- 🔧 Changed YAML structure

## Index Maintenance

### Regular Maintenance (Weekly)
```bash
# 1. Check index health
python tools/kb.py stats

# 2. Rebuild if needed
python tools/kb.py index --force -v

# 3. Verify search
python tools/kb.py search "test query"
```

### After Major Changes
```bash
# 1. Validate all entries
python tools/kb.py validate .

# 2. Rebuild index
python tools/kb.py index --force

# 3. Check statistics
python tools/kb.py stats
```

## Index Statistics
```bash
python tools/kb.py stats
```

Output:
```
📊 KB Statistics

Total Entries: 127
├── Errors: 98
└── Patterns: 29

By Scope:
  universal:     15 (11.8%)
  python:        32 (25.2%)
  javascript:    18 (14.2%)
  docker:        22 (17.3%)
  postgresql:    12 (9.4%)
  framework:     28 (22.0%)

By Severity:
  critical:  8   (6.3%)
  high:      45  (35.4%)
  medium:    52  (40.9%)
  low:       22  (17.3%)

Quality Scores:
  Min:  65
  Max:  98
  Avg:  82.3

Index Size: 156 KB
Last Built: 2026-01-07 14:32:15
```

## Troubleshooting

### Issue: "No results found"
**Cause:** Index not built or stale
**Fix:**
```bash
python tools/kb.py index --force -v
```

### Issue: "Index corrupted"
**Symptoms:** Search errors, crashes
**Fix:**
```bash
# Delete old index
rm _index_meta.yaml

# Rebuild from scratch
python tools/kb.py index --force
```

### Issue: "Slow search"
**Cause:** Too many entries, unoptimized index
**Fix:**
```bash
# Rebuild with optimization
python tools/kb.py index --force --optimize
```

### Issue: "Missing entries"
**Check:**
```bash
# Verify file exists
ls python/errors/new-entry.yaml

# Rebuild index
python tools/kb.py index --force

# Verify entry in index
python tools/kb.py search "title from entry"
```

## Performance Tips
- Use **incremental updates** for small changes (default)
- Use **--force** only for major changes
- Run **--optimize** monthly for large KBs (>500 entries)
- Keep index under 10 MB for optimal performance

## Related Skills
- `kb-search` - Test search after indexing
- `kb-validate` - Validate entries before indexing
- `cleanup-cache` - Remove stale index files

## Automated Indexing
This skill is automatically triggered by:
- **PostToolUse hook** - After YAML file changes (check-index.sh)
- **Stop hook** - Before session ends if entries changed
- **Scheduled task** - Weekly maintenance (if configured)

---
**Version:** 1.0
**Last Updated:** 2026-01-07
**Skill Type:** Maintenance
**Index Type:** SQLite + Full-Text Search
