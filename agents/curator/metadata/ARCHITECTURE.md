# METADATA_ARCHITECTURE.md - Knowledge Base Metadata & Tracking System

## Problem Analysis

Current architecture is **distributed** with local KB copies synced via Git. This creates challenges for:
1. Tracking what has been analyzed/enhanced
2. Monitoring knowledge freshness and lifecycle
3. Collecting usage analytics without central endpoint
4. Detecting changes and new entries efficiently

## Proposed Solution: Distributed Metadata System

### Core Principles

1. **Local-First Metadata** - Each project maintains its own metadata locally
2. **Git-Synced Metadata** - Metadata files committed alongside knowledge entries
3. **Passive Analytics** - No instrumentation required, lightweight file-based tracking
4. **Privacy-Preserving** - No personal data, only aggregated statistics
5. **Merge-Safe** - Metadata must handle git merges gracefully

---

## Component 1: Entry-Level Metadata (`_meta.yaml`)

### Purpose
Track lifecycle, analysis status, and history for each knowledge entry

### Location
Alongside each YAML file (e.g., `python/errors/imports_meta.yaml`)

### Structure

```yaml
# _meta.yaml for python/errors/imports.yaml
version: "1.0"
file_metadata:
  file_id: "python-errors-imports"
  created_at: "2026-01-04T10:30:00Z"
  created_by: "claude-code"
  last_modified: "2026-01-05T15:45:00Z"
  last_modified_by: "claude-code"
  version: 3

# Entry-level tracking
entries:
  IMPORT-001:
    # Lifecycle metadata
    created_at: "2026-01-04T10:30:00Z"
    created_by: "agent-session-abc123"
    last_modified: "2026-01-05T15:45:00Z"
    last_modified_by: "curator-session-def456"

    # Analysis tracking
    last_analyzed_at: "2026-01-05T14:00:00Z"
    last_analyzed_by: "skill-validate-technical"
    analysis_version: 1

    # Quality tracking
    quality_score: 92
    quality_assessed_at: "2026-01-05T14:00:00Z"
    quality_assessed_by: "curator"

    # Research tracking
    last_researched_at: "2026-01-05T12:00:00Z"
    research_sources:
      - "official-docs"
      - "stack-overflow"
      - "perplexity"
    research_version: 2

    # Validation status
    validation_status: "validated"  # validated | needs_review | outdated | deprecated
    validated_at: "2026-01-05T14:00:00Z"
    validated_against_version: "python-3.12"

    # Version tracking
    tested_versions:
      python: "3.11, 3.12"
    requires_version_check: false
    next_version_check_due: "2026-04-05T00:00:00Z"

    # Deprecation
    is_deprecated: false
    deprecated_at: null
    deprecated_by: null
    superseded_by: null

  IMPORT-002:
    # ... similar structure ...
    quality_score: 78
    validation_status: "needs_review"
    next_version_check_due: "2026-01-10T00:00:00Z"  # Overdue!

# File-level analytics
analytics:
  total_access_count: 47
  first_accessed_at: "2026-01-04T11:00:00Z"
  last_accessed_at: "2026-01-05T16:30:00Z"
  access_history_summary:
    - date: "2026-01-04"
      count: 12
    - date: "2026-01-05"
      count: 35

# Change history
change_history:
  - timestamp: "2026-01-04T10:30:00Z"
    action: "created"
    agent: "claude-code"
    entries_affected: ["IMPORT-001", "IMPORT-002"]
    reason: "Initial import from project issues"

  - timestamp: "2026-01-05T14:00:00Z"
    action: "quality_assessed"
    agent: "curator"
    entries_affected: ["IMPORT-001"]
    changes:
      quality_score: 92
      previous_score: null

  - timestamp: "2026-01-05T15:45:00Z"
    action: "enhanced"
    agent: "curator"
    entries_affected: ["IMPORT-001"]
    reason: "Added real-world examples and cross-references"
```

### Benefits

✅ **Self-Contained** - Metadata travels with the file
✅ **Git-Friendly** - Can be merged and versioned
✅ **Queryable** - Easy to scan and analyze
✅ **No External Dependencies** - Pure YAML files

---

## Component 2: Local Usage Tracking (`.usage.json`)

### Purpose
Track which entries are accessed locally without central endpoint

### Location
Project-level: `docs/knowledge-base/.cache/usage.json`

### Structure

```json
{
  "version": "1.0",
  "project_id": "project-xyz-abc",
  "tracking_started_at": "2026-01-01T00:00:00Z",
  "last_updated_at": "2026-01-05T18:00:00Z",

  "entries": {
    "IMPORT-001": {
      "access_count": 23,
      "first_accessed_at": "2026-01-03T10:15:00Z",
      "last_accessed_at": "2026-01-05T14:30:00Z",
      "access_methods": {
        "search": 18,
        "direct_id": 5,
        "category_browse": 0
      },
      "access_context": {
        "error_resolution": 20,
        "prevention": 2,
        "learning": 1
      },
      "sessions": [
        {
          "timestamp": "2026-01-05T14:30:00Z",
          "agent": "claude-code",
          "method": "search",
          "query": "circular import",
          "context": "error_resolution",
          "resolved": true
        }
      ]
    },

    "DOCKER-001": {
      "access_count": 5,
      "first_accessed_at": "2026-01-04T09:00:00Z",
      "last_accessed_at": "2026-01-04T16:45:00Z",
      "access_methods": {
        "search": 5,
        "direct_id": 0,
        "category_browse": 0
      }
    }
  },

  "search_analytics": {
    "total_searches": 156,
    "successful_searches": 142,
    "no_results_searches": 14,
    "top_search_queries": [
      {"query": "circular import", "count": 12},
      {"query": "websocket timeout", "count": 8},
      {"query": "port already in use", "count": 7}
    ],
    "no_results_queries": [
      {"query": "fastapi websockets", "count": 3},
      {"query": "pytest async fixture", "count": 2}
    ]
  },

  "gap_signals": {
    "repeated_no_results": [
      {
        "query": "fastapi websockets",
        "count": 3,
        "first_seen": "2026-01-03",
        "last_seen": "2026-01-05",
        "priority": "high"
      }
    ],
    "high_access_low_quality": [
      {
        "entry_id": "OLD-001",
        "access_count": 15,
        "quality_score": 45,
        "suggestion": "enhance"
      }
    ]
  }
}
```

### Privacy Note

⚠️ **This file stays LOCAL** - NOT committed to Git
- Contains project-specific usage patterns
- Should be in `.gitignore`
- Used for local gap analysis and prioritization
- Can be aggregated (manually) if needed

---

## Component 3: Global Metadata Index (`_index.yaml`)

### Purpose
Repository-wide catalog of all entries with cross-references

### Location
Repository root: `docs/knowledge-base/shared/_index.yaml`

### Structure

```yaml
version: "1.0"
last_updated: "2026-01-05T18:00:00Z"
total_entries: 127

# Catalog by entry ID
entry_catalog:
  IMPORT-001:
    file: "python/errors/imports.yaml"
    scope: "python"
    category: "imports"
    severity: "high"
    created_at: "2026-01-04T10:30:00Z"
    last_modified: "2026-01-05T15:45:00Z"
    quality_score: 92
    validation_status: "validated"
    next_review_date: "2026-04-05T00:00:00Z"

  DOCKER-024:
    file: "docker/errors/best-practices.yaml"
    scope: "docker"
    category: "best-practices"
    severity: "medium"
    created_at: "2026-01-03T14:00:00Z"
    last_modified: "2026-01-03T14:00:00Z"
    quality_score: 85
    validation_status: "validated"
    next_review_date: "2026-04-03T00:00:00Z"

# Catalog by file
file_catalog:
  python/errors/imports.yaml:
    entries: ["IMPORT-001", "IMPORT-002", "IMPORT-003"]
    total_entries: 3
    last_modified: "2026-01-05T15:45:00Z"
    metadata_file: "python/errors/imports_meta.yaml"

# Statistics
statistics:
  by_scope:
    python: 45
    javascript: 12
    docker: 18
    universal: 22
    postgresql: 15
    framework: 15

  by_severity:
    critical: 8
    high: 45
    medium: 52
    low: 22

  by_quality:
    excellent_90_plus: 38
    good_75_89: 72
    acceptable_60_74: 15
    needs_improvement: 2

  by_validation_status:
    validated: 110
    needs_review: 12
    outdated: 3
    deprecated: 2

# Alerts
alerts:
  overdue_review:
    - entry_id: "IMPORT-002"
      reason: "Version check overdue"
      due_date: "2026-01-10T00:00:00Z"

  low_quality_high_usage:
    - entry_id: "OLD-001"
      quality_score: 45
      access_count: 15
      suggestion: "Priority enhancement"

  gaps_detected:
    - topic: "FastAPI websockets"
      signal_count: 3
      priority: "high"
      suggested_entry_id: "FASTAPI-WS-001"
```

### Benefits

✅ **Global View** - See entire KB state at once
✅ **Queryable** - Find entries needing attention
✅ **Alerts** - Automatic detection of issues
✅ **Git-Synced** - Propagates to all projects

---

## Component 4: Change Detection System

### Purpose
Efficiently detect new/modified entries without full re-scans

### Mechanism 1: File Hash Tracking

```yaml
# .cache/file_hashes.json
{
  "version": "1.0",
  "last_scan": "2026-01-05T18:00:00Z",

  "file_hashes": {
    "python/errors/imports.yaml": "a1b2c3d4e5f6",
    "docker/errors/common.yaml": "f6e5d4c3b2a1"
  },

  "entry_hashes": {
    "IMPORT-001": "hash-of-import-001-content",
    "DOCKER-001": "hash-of-docker-001-content"
  }
}
```

**Algorithm:**
```python
def detect_changes():
    # Calculate current hashes
    current_hashes = calculate_all_hashes()

    # Compare with stored
    changes = []
    for entry_id, old_hash in stored_hashes['entry_hashes'].items():
        if old_hash != current_hashes['entry_hashes'][entry_id]:
            changes.append({
                'entry_id': entry_id,
                'type': 'modified',
                'needs_reanalysis': True
            })

    # Find new entries
    for entry_id in current_hashes['entry_hashes']:
        if entry_id not in stored_hashes['entry_hashes']:
            changes.append({
                'entry_id': entry_id,
                'type': 'new',
                'needs_analysis': True
            })

    return changes
```

### Mechanism 2: Git-Based Detection

```bash
# Since last sync
git diff --name-only HEAD@{1} HEAD | grep '\.yaml$'

# Find entries modified in last N days
git log --since="7 days ago" --name-only --pretty=format: | grep '\.yaml$' | sort -u
```

---

## Component 5: Automated Analysis Workflow

### Skill: `check-freshness`

```bash
Please check-freshness for all entries
```

**What it does:**

1. Scan all `_meta.yaml` files
2. Check `next_version_check_due` dates
3. Check `validation_status`
4. Compare with current library versions
5. Generate report:

```yaml
freshness_report:
  timestamp: "2026-01-05T18:00:00Z"

  overdue:
    - entry_id: "IMPORT-002"
      reason: "Version check overdue since 2026-01-10"
      current_python_version: "3.13"
      tested_versions: ["3.11", "3.12"]
      action_required: "Test with Python 3.13"

    - entry_id: "FASTAPI-005"
      reason: "FastAPI 0.115 released, breaking changes"
      current_fastapi_version: "0.115.0"
      tested_version: "0.100.0"
      action_required: "Check for breaking changes"

  upcoming_reviews:
    - entry_id: "DOCKER-024"
      next_review: "2026-02-01"
      days_until: 27

  recommendations:
    - action: "version_update"
      entries: ["IMPORT-002", "FASTAPI-005"]
      priority: "high"

    - action: "quality_audit"
      entries: ["OLD-001"]
      reason: "Low quality score (45) with high usage"
```

---

## Component 6: Usage Analytics Aggregation (Manual)

### Purpose
Periodically aggregate insights across projects (opt-in, manual)

### Process

1. **Each project** (optionally) runs:
```bash
python tools/kb.py export-analytics --output analytics-2026-01.json
```

2. **Anonymized output**:
```json
{
  "project_type": "web-api",
  "period": "2026-01",
  "entries_used": ["IMPORT-001", "DOCKER-024"],
  "top_gaps": ["fastapi websockets"],
  "total_searches": 156,
  "success_rate": 0.91
}
```

3. **Manual submission** to shared repo (PR or issue):
```yaml
# analytics/community/2026-01/project-xyz.json
```

4. **Aggregated insights** in `_index.yaml`:
```yaml
community_insights:
  most_accessed_entries_2026_01:
    - entry_id: "IMPORT-001"
      access_count: 234
      project_count: 12

  common_gaps_2026_01:
    - topic: "FastAPI websockets"
      projects_reporting: 8
      priority: "critical"
```

**Privacy:** Only aggregated statistics, no project identification

---

## Complete Workflow Examples

### Scenario 1: New Agent Joins Project

```
1. Clone/fetch shared KB
   git pull origin main

2. Detect changes since last sync
   python tools/kb.py detect-changes

3. Output: 3 new entries, 2 modified entries

4. Update local index
   python tools/kb.py index --force

5. Check what needs analysis
   python tools/kb.py check-freshness

6. Analyze only new/changed entries
   For each new entry:
     - validate-technical
     - assess quality
     - add to _meta.yaml
```

### Scenario 2: Curator Performs Quality Audit

```
1. Check freshness
   python tools/kb.py check-freshness

2. Identify entries needing attention
   - 2 overdue for version check
   - 1 low quality + high usage
   - 5 need review

3. For each priority entry:
   a. research-enhance entry ID
   b. validate-technical for ID
   c. update _meta.yaml with:
      - last_analyzed_at
      - quality_score
      - next_version_check_due

4. Commit changes
   git add _meta.yaml
   git commit -m "Update metadata for IMPORT-002, FASTAPI-005"
```

### Scenario 3: Local Usage Analysis

```
1. Analyze local usage patterns
   python tools/kb.py analyze-usage

2. Output:
   - Top accessed entries
   - Search terms with no results (gaps)
   - High-access, low-quality entries

3. Address gaps:
   For each "no results" query:
     - identify-gaps for "topic"
     - create-entry for "topic"
     - validate and enhance

4. Improve quality:
   For high-access, low-quality:
     - research-enhance entry ID
     - Target: improve score to ≥ 75
```

---

## Implementation Priority

### Phase 1: Essential (Immediate)
✅ **Entry `_meta.yaml` files** - Track analysis status
✅ **Local `.usage.json`** - Usage tracking
✅ **`check-freshness` skill** - Detect outdated entries
✅ **Hash-based change detection** - Efficient scanning

### Phase 2: Enhanced (1-2 weeks)
✅ **Global `_index.yaml`** - Repository-wide catalog
✅ **Automated alerts** - Overdue reviews, quality issues
✅ **Usage analysis skill** - Gap detection
✅ **Git-based change detection** - Integration with version control

### Phase 3: Advanced (1 month)
✅ **Community analytics aggregation** - Opt-in sharing
✅ **Predictive gap detection** - ML-based suggestions
✅ **Automated version monitoring** - Check for library updates
✅ **Cross-project pattern recognition** - Identify universal patterns

---

## Technical Implementation Notes

### File Operations

All metadata files should be:
- **Atomic writes** - Write to temp, then rename
- **Merge-safe** - Use list-based structures, avoid deep nesting conflicts
- **Backward compatible** - Include version field, handle old formats

### Performance

For large knowledge bases (1000+ entries):
- **Incremental updates** - Only scan changed files
- **Lazy loading** - Load metadata on demand
- **Index caching** - Keep parsed index in memory

### Concurrency

Multiple agents/curlers working simultaneously:
- **Optimistic locking** - Check file hash before writing
- **Merge resolution** - Git handles conflicts
- **Last-write-wins acceptable** - Metadata can be recalculated

---

## Summary

This distributed metadata system provides:

✅ **Change Detection** - Hash-based and git-based
✅ **Analysis Tracking** - What's been analyzed, what hasn't
✅ **Lifecycle Management** - Creation, modification, review dates
✅ **Usage Analytics** - Local tracking, optional community aggregation
✅ **No Central Endpoint** - Fully distributed, Git-synced
✅ **Privacy-Preserving** - Local analytics optional to share
✅ **Scalable** - Works with 10 or 10,000 entries

**Key Innovation:** Metadata travels with knowledge, propagates through Git, and enables intelligent curation without central infrastructure.
