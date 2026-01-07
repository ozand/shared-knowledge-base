# CLI Reference - kb.py Commands

**Complete reference for all kb.py CLI commands**

---

## Core Commands

### Build Search Index

```bash
# Build index (required after any changes)
python tools/kb.py index -v

# Force rebuild (drop and recreate)
python tools/kb.py index --force -v
```

**When to use:**
- After adding/modifying YAML entries
- After initial setup
- If search returns no results

---

### Search Knowledge Base

```bash
# Simple search
python tools/kb.py search "websocket"

# Filter by category
python tools/kb.py search --category python

# Filter by severity
python tools/kb.py search --severity high

# Filter by tags
python tools/kb.py search --tags async pytest

# Combined filters
python tools/kb.py search --category python --severity high --tags async
```

**Output:**
- Matching entries with ID, title, severity
- File paths to matching entries
- Search statistics (results count, search time)

---

### Show Statistics

```bash
# Overall statistics
python tools/kb.py stats

# Output includes:
# - Total entries count
# - Entries by category
# - Entries by severity
# - Entries by scope
# - Index size and status
```

---

### Validate Knowledge Entries

```bash
# Validate specific file
python tools/kb.py validate path/to/file.yaml

# Validate all entries in directory
python tools/kb.py validate python/errors/

# Validate all entries in repository
python tools/kb.py validate .

# Validation checks:
# - YAML syntax correctness
# - Required fields presence
# - ID format compliance (CATEGORY-NNN)
# - Duplicate detection
```

---

### Export for AI Tools

```bash
# Export to JSON
python tools/kb.py export --format json --output kb.json

# Export to Markdown
python tools/kb.py export --format markdown --output kb.md

# Export specific category
python tools/kb.py export --category python --output python-kb.json
```

---

## Metadata Commands (v3.0)

### Initialize Metadata

```bash
# Initialize metadata for all entries
python tools/kb.py init-metadata

# Creates *_meta.yaml files for all entries
# Extracts: quality_score, usage_count, last_used, tested_versions
```

**When to use:**
- First-time metadata setup
- After adding new entries without metadata

---

### Detect Changes

```bash
# Detect file changes since last check
python tools/kb.py detect-changes

# Output:
# - Modified entries (need reindex)
# - New entries (need metadata init)
# - Deleted entries (need cleanup)
```

---

### Check Freshness

```bash
# Check all entries for freshness
python tools/kb.py check-freshness

# Check specific entry
python tools/kb.py check-freshness --entry-id ERROR-001

# Output:
# - Entries needing updates (age > 180 days)
# - Entries with version mismatches
# - Entries with declining usage
```

---

### Analyze Usage Patterns

```bash
# Analyze usage across all entries
python tools/kb.py analyze-usage

# Most accessed entries
# Least accessed entries
# Search term frequency
# Category usage distribution
```

---

### Update Entry Metadata

```bash
# Update quality score
python tools/kb.py update-metadata --entry-id ERROR-001 --quality-score 85

# Update tested versions
python tools/kb.py update-metadata --entry-id ERROR-001 --tested-version "2.0.0"

# Mark as reviewed
python tools/kb.py update-metadata --entry-id ERROR-001 --reviewed
```

---

### Reindex Metadata

```bash
# Rebuild metadata index
python tools/kb.py reindex-metadata

# When to use:
# - After bulk metadata updates
# - If metadata queries are slow
# - After merging metadata conflicts
```

---

## Version Monitoring

### Check Library Versions

```bash
# Check specific library
python -m tools.kb_versions check --library fastapi

# Check all libraries
python -m tools.kb_versions check --all

# Output:
# - Latest version available
# - Versions tested in KB
# - Version gaps (need testing)
```

---

### Scan for Tested Versions

```bash
# Scan KB for tested versions
python -m tools.kb_versions scan

# Extracts version info from:
# - solution.code examples
# - tested_versions metadata
# - examples sections

# Updates *_meta.yaml with version info
```

---

## Predictive Analytics

### Predict Updates Needed

```bash
# Predict entries needing updates (30-day window)
python -m tools.kb_predictive predict-updates --days 30

# Output:
# - Entries with old libraries (version gaps)
# - Entries with declining quality
# - Entries with low usage (consider deprecation)
```

---

### Suggest New Entries

```bash
# Suggest entries based on search gaps
python -m tools.kb_predictive suggest-entries

# Analyzes:
# - Frequent searches with no results
# - Search term combinations
# - Emerging technology trends

# Outputs suggested entry topics
```

---

### Estimate Entry Quality

```bash
# Estimate quality score for entry
python -m tools.kb_predictive estimate-quality --entry-id ERROR-001

# Quality factors:
# - Completeness (all required fields)
# - Code examples quality
# - Testing coverage
# - Usage frequency
# - Freshness (last updated)

# Outputs: 0-100 score
```

---

## Common Workflows

### Initial Setup

```bash
# 1. Install dependencies
pip install pyyaml

# 2. Build search index
python tools/kb.py index -v

# 3. Validate all entries
python tools/kb.py validate .

# 4. Initialize metadata
python tools/kb.py init-metadata
```

---

### After Modifying Entries

```bash
# 1. Validate changes
python tools/kb.py validate path/to/modified.yaml

# 2. Rebuild index
python tools/kb.py index --force -v

# 3. Update metadata
python tools/kb.py update-metadata --entry-id ERROR-ID --reviewed
```

---

### Regular Maintenance

```bash
# Weekly: Check freshness
python tools/kb.py check-freshness

# Monthly: Analyze usage
python tools/kb.py analyze-usage

# Quarterly: Predict updates
python -m tools.kb_predictive predict-updates --days 90
```

---

## Troubleshooting

### Search Returns No Results

**Symptom:** `python tools/kb.py search "query"` returns nothing

**Solutions:**
1. Rebuild index: `python tools/kb.py index --force -v`
2. Check query syntax (avoid special characters)
3. Verify entries exist: `python tools/kb.py stats`

---

### Validation Fails

**Symptom:** `python tools/kb.py validate` reports errors

**Common errors:**
- **YAML syntax error:** Check indentation, quotes
- **Missing required field:** Add id, title, severity, scope, problem, solution
- **Invalid ID format:** Use CATEGORY-NNN (e.g., ERROR-001)
- **Duplicate ID:** Change ID to unique value

---

### Metadata Not Working

**Symptom:** Metadata commands return errors

**Solutions:**
1. Initialize metadata: `python tools/kb.py init-metadata`
2. Check *_meta.yaml files exist
3. Verify metadata YAML syntax

---

**Version:** 3.0
**Last Updated:** 2026-01-07
