# METADATA_SKILLS.md - Metadata Management Skills

## Enhanced Skills for Metadata-Driven Knowledge Curation

These skills extend the base SKILLS.md with metadata-aware capabilities.

---

## Skill: `check-freshness`

**Purpose:** Detect entries needing review, updates, or version checks

**Usage:**
```bash
Please check-freshness for [scope]
```

**What it does:**
- Scans all `_meta.yaml` files in scope
- Checks `next_version_check_due` dates
- Identifies entries with `validation_status: needs_review`
- Compares tested versions with current versions
- Generates prioritized action list

**Example:**
```bash
Please check-freshness for python
```

**Output:**
```yaml
freshness_report:
  timestamp: "2026-01-05T18:00:00Z"
  scope: "python"

  critical:
    - entry_id: "IMPORT-002"
      file: "python/errors/imports.yaml"
      reason: "Version check overdue by 5 days"
      tested_versions: ["python-3.11", "python-3.12"]
      current_version: "python-3.13"
      action_required: "Test with Python 3.13 and update"
      priority: "critical"

    - entry_id: "FASTAPI-005"
      file: "framework/fastapi/errors/websocket.yaml"
      reason: "FastAPI 0.115 released with breaking changes"
      tested_version: "fastapi-0.100.0"
      current_version: "fastapi-0.115.0"
      action_required: "Review breaking changes, update examples"
      priority: "critical"

  warning:
    - entry_id: "TEST-003"
      reason: "Validation status: needs_review"
      last_reviewed: "2025-11-15"
      days_since_review: 51
      action_required: "Re-validate and update quality score"
      priority: "medium"

  upcoming:
    - entry_id: "DOCKER-024"
      next_review: "2026-02-01"
      days_until: 27
      severity: "medium"

  summary:
    total_entries: 45
    critical_actions: 2
    warning_actions: 5
    upcoming_reviews: 8
    healthy: 30

  recommendations:
    - priority: "immediate"
      action: "version_update"
      entries: ["IMPORT-002", "FASTAPI-005"]
      estimated_time: "2 hours"

    - priority: "this_week"
      action: "quality_audit"
      entries: ["TEST-003", "OLD-001"]
      estimated_time: "1 hour"
```

**Follow-up skills:**
```bash
# After freshness check
Please update-versions for IMPORT-002
Please research-enhance entry FASTAPI-005
```

---

## Skill: `track-usage`

**Purpose:** Record usage of knowledge entries for analytics

**Usage:**
```bash
Please track-usage for [ENTRY-ID] with [context]
```

**What it does:**
- Appends usage record to `.cache/usage.json`
- Records timestamp, method, query, context
- Updates access counts and statistics
- Maintains recent access history (last 100 sessions)

**Example:**
```bash
# After search returns result
Please track-usage for IMPORT-001 with context:
  method: search
  query: "circular import"
  context: error_resolution
  resolved: true
```

**Implementation:**
```python
def track_usage(entry_id, method, query, context, resolved=False):
    usage_file = "docs/knowledge-base/.cache/usage.json"

    # Load or create
    if exists(usage_file):
        with open(usage_file) as f:
            usage_data = json.load(f)
    else:
        usage_data = {
            "version": "1.0",
            "project_id": generate_project_id(),
            "tracking_started_at": datetime.now().isoformat(),
            "entries": {},
            "search_analytics": {
                "total_searches": 0,
                "successful_searches": 0,
                "top_search_queries": []
            }
        }

    # Update entry stats
    if entry_id not in usage_data["entries"]:
        usage_data["entries"][entry_id] = {
            "access_count": 0,
            "first_accessed_at": None,
            "last_accessed_at": None,
            "access_methods": {"search": 0, "direct_id": 0, "category_browse": 0},
            "sessions": []
        }

    entry = usage_data["entries"][entry_id]
    entry["access_count"] += 1
    entry["last_accessed_at"] = datetime.now().isoformat()
    if entry["first_accessed_at"] is None:
        entry["first_accessed_at"] = entry["last_accessed_at"]
    entry["access_methods"][method] += 1

    # Add session record
    session = {
        "timestamp": datetime.now().isoformat(),
        "method": method,
        "query": query if method == "search" else None,
        "context": context,
        "resolved": resolved
    }
    entry["sessions"].append(session)

    # Keep only last 100 sessions per entry
    if len(entry["sessions"]) > 100:
        entry["sessions"] = entry["sessions"][-100:]

    # Update search analytics
    usage_data["search_analytics"]["total_searches"] += 1
    if resolved:
        usage_data["search_analytics"]["successful_searches"] += 1

    # Update query tracking
    if method == "search" and query:
        top_queries = usage_data["search_analytics"]["top_search_queries"]
        found = False
        for tq in top_queries:
            if tq["query"] == query:
                tq["count"] += 1
                found = True
                break
        if not found:
            top_queries.append({"query": query, "count": 1})
        top_queries.sort(key=lambda x: x["count"], reverse=True)
        usage_data["search_analytics"]["top_search_queries"] = top_queries[:20]

    usage_data["last_updated_at"] = datetime.now().isoformat()

    # Save
    with open(usage_file, 'w') as f:
        json.dump(usage_data, f, indent=2)

    return entry["access_count"]
```

**Automatic integration:**
Called automatically by `kb.py search` when results are accessed.

---

## Skill: `detect-changes`

**Purpose:** Efficiently detect new or modified entries since last sync

**Usage:**
```bash
Please detect-changes since [last-sync]
```

**What it does:**
- Calculates file hashes
- Compares with stored hashes in `.cache/file_hashes.json`
- Uses git diff to find changed files
- Identifies new entries, modified entries, deleted entries
- Generates prioritized analysis queue

**Example:**
```bash
Please detect-changes since last git pull
```

**Output:**
```yaml
change_detection:
  timestamp: "2026-01-05T18:30:00Z"
  last_sync: "2026-01-04T10:00:00Z"
  method: "git-diff"

  changes:
    new_entries:
      - entry_id: "REDIS-001"
        file: "universal/errors/redis-errors.yaml"
        added_at: "2026-01-05T10:15:00Z"
        action_required: "validate, assess_quality, add_metadata"
        priority: "high"

      - entry_id: "POSTGRES-015"
        file: "postgresql/errors/performance.yaml"
        added_at: "2026-01-05T11:30:00Z"
        action_required: "validate, assess_quality, add_metadata"
        priority: "medium"

    modified_entries:
      - entry_id: "IMPORT-001"
        file: "python/errors/imports.yaml"
        modified_at: "2026-01-05T14:20:00Z"
        changes:
          - "Added real-world example"
          - "Enhanced explanation"
        last_analyzed: "2026-01-04T10:00:00Z"
        action_required: "re_validate, update_metadata"
        priority: "low"

      - entry_id: "DOCKER-024"
        file: "docker/errors/best-practices.yaml"
        modified_at: "2026-01-05T15:45:00Z"
        changes:
          - "Updated to Docker 25.0"
          - "Added healthcheck section"
        action_required: "validate_new_version, update_metadata"
        priority: "high"

    deleted_entries:
      - entry_id: "OLD-001"
        was_in: "python/errors/obsolete.yaml"
        deleted_at: "2026-01-05T12:00:00Z"
        reason: "Superseded by IMPORT-005"

    metadata_updates:
      - file: "python/errors/imports_meta.yaml"
        action: "update_index"

  summary:
    total_changes: 6
    new: 2
    modified: 3
    deleted: 1
    metadata_files: 1

  analysis_queue:
    priority_high:
      - "REDIS-001 (new, validate)"
      - "DOCKER-024 (version update)"

    priority_medium:
      - "POSTGRES-015 (new, validate)"
      - "IMPORT-001 (re-validate)"

  recommended_actions:
    - action: "validate_new_entries"
      entries: ["REDIS-001", "POSTGRES-015"]
      skill: "validate-technical"

    - action: "update_version_metadata"
      entries: ["DOCKER-024"]
      skill: "update-versions"

    - action: "reindex"
      command: "python tools/kb.py index --force"
```

**Follow-up workflow:**
```bash
# After detecting changes
For each new entry:
  1. Please validate-technical for [ENTRY-ID]
  2. Please assess-quality for [ENTRY-ID]
  3. Please create-metadata for [ENTRY-ID]

# Rebuild index
python tools/kb.py index --force
```

---

## Skill: `analyze-usage`

**Purpose:** Analyze local usage patterns to identify gaps and improvement opportunities

**Usage:**
```bash
Please analyze-usage for [time-period]
```

**What it does:**
- Reads `.cache/usage.json`
- Identifies most accessed entries
- Finds search terms with no results (gaps)
- Detects high-access, low-quality entries
- Suggests new entries to create
- Recommends entries to enhance

**Example:**
```bash
Please analyze-usage for last-30-days
```

**Output:**
```yaml
usage_analysis:
  period: "2025-12-06 to 2026-01-05"
  total_searches: 342
  successful_searches: 298
  success_rate: 0.87  # 87%

  top_accessed_entries:
    - entry_id: "IMPORT-001"
      access_count: 47
      file: "python/errors/imports.yaml"
      quality_score: 92
      status: "excellent"
      last_accessed: "2026-01-05T16:30:00Z"

    - entry_id: "DOCKER-024"
      access_count: 35
      file: "docker/errors/best-practices.yaml"
      quality_score: 85
      status: "good"
      last_accessed: "2026-01-05T14:20:00Z"

    - entry_id: "OLD-001"
      access_count: 28
      file: "python/errors/legacy.yaml"
      quality_score: 45
      status: "needs_improvement"
      last_accessed: "2026-01-04T11:15:00Z"
      recommendation: "Priority enhancement - high usage, low quality"

  search_gaps:
    critical:
      - query: "fastapi websocket timeout"
        count: 12
        first_seen: "2025-12-20"
        last_seen: "2026-01-05"
        suggested_category: "framework/fastapi"
        suggested_entry_id: "FASTAPI-WS-001"
        estimated_priority: "critical"
        rationale: "Frequent searches, no results, common error"

    - query: "pytest async fixture loop"
        count: 8
        first_seen: "2025-12-25"
        last_seen: "2026-01-04"
        suggested_category: "python/errors"
        suggested_entry_id: "PYTEST-003"
        estimated_priority: "high"

    medium:
      - query: "docker compose override file"
        count: 5
        suggested_category: "docker/patterns"
        estimated_priority: "medium"

  quality_opportunities:
    - entry_id: "OLD-001"
      access_count: 28
      quality_score: 45
      gap: 47  # 83% improvement needed
      estimated_effort: "2 hours"
      expected_impact: "high"

    - entry_id: "MEDIUM-002"
      access_count: 15
      quality_score: 68
      gap: 7
      estimated_effort: "30 minutes"
      expected_impact: "medium"

  category_insights:
    python:
      total_accesses: 156
      top_entries: ["IMPORT-001", "TEST-003", "OLD-001"]
      gap_topics: ["pytest async", "type hints union"]
      health_score: 78

    docker:
      total_accesses: 89
      top_entries: ["DOCKER-024", "DOCKER-001"]
      gap_topics: ["compose override", "multi-stage build"]
      health_score: 85

  recommendations:
    immediate:
      - action: "create_entry"
        topic: "FastAPI WebSocket Timeout"
        priority: "critical"
        rationale: "12 failed searches in 30 days"

      - action: "enhance_entry"
        entry_id: "OLD-001"
        target_score: 75
        priority: "high"
        rationale: "28 accesses but quality score only 45"

    this_week:
      - action: "create_entry"
        topic: "Pytest Async Fixture Event Loop"
        priority: "high"

      - action: "enhance_entry"
        entry_id: "MEDIUM-002"
        target_score: 75
        priority: "medium"

    backlog:
      - action: "create_entry"
        topic: "Docker Compose Override Files"
        priority: "low"
```

**Follow-up actions:**
```bash
# Address critical gaps
Please create-entry for "FastAPI WebSocket Timeout"
Please research-enhance entry OLD-001
```

---

## Skill: `update-metadata`

**Purpose:** Create or update metadata for an entry after analysis/enhancement

**Usage:**
```bash
Please update-metadata for [ENTRY-ID]
```

**What it does:**
- Creates `_meta.yaml` if doesn't exist
- Updates analysis timestamps
- Records quality score
- Sets next review date
- Tracks changes made

**Example:**
```bash
# After validating and enhancing IMPORT-001
Please update-metadata for IMPORT-001 with:
  quality_score: 92
  validation_status: validated
  tested_versions: ["python-3.12", "python-3.13"]
  next_review: "2026-04-05"
  changes_made: "Added real-world example, enhanced explanation"
```

**Output:**
```yaml
metadata_updated:
  entry_id: "IMPORT-001"
  file: "python/errors/imports_meta.yaml"

  updated_fields:
    last_analyzed_at: "2026-01-05T18:00:00Z"
    last_analyzed_by: "skill-validate-technical"
    quality_score: 92
    quality_assessed_at: "2026-01-05T18:00:00Z"
    validation_status: "validated"
    validated_at: "2026-01-05T18:00:00Z"
    validated_against_version: "python-3.13"
    tested_versions:
      python: "3.12, 3.13"
    next_version_check_due: "2026-04-05T00:00:00Z"

  change_history_entry:
    timestamp: "2026-01-05T18:00:00Z"
    action: "enhanced"
    agent: "curator"
    reason: "Added real-world example, enhanced explanation"
    quality_improvement:
      from: 78
      to: 92

  summary:
    status: "success"
    next_review: "2026-04-05"
    days_until_review: 90
```

**Metadata file created/updated:**
```yaml
# python/errors/imports_meta.yaml
version: "1.0"
file_metadata:
  file_id: "python-errors-imports"
  created_at: "2026-01-04T10:30:00Z"
  last_modified: "2026-01-05T18:00:00Z"
  version: 3

entries:
  IMPORT-001:
    # ... existing metadata ...
    last_analyzed_at: "2026-01-05T18:00:00Z"
    last_analyzed_by: "skill-validate-technical"
    quality_score: 92
    quality_assessed_at: "2026-01-05T18:00:00Z"
    validation_status: "validated"
    validated_at: "2026-01-05T18:00:00Z"
    validated_against_version: "python-3.13"
    tested_versions:
      python: "3.12, 3.13"
    next_version_check_due: "2026-04-05T00:00:00Z"

change_history:
  # ... existing history ...
  - timestamp: "2026-01-05T18:00:00Z"
    action: "enhanced"
    agent: "curator"
    entries_affected: ["IMPORT-001"]
    reason: "Added real-world example, enhanced explanation"
    changes:
      quality_score:
        from: 78
        to: 92
```

---

## Skill: `assess-quality`

**Purpose:** Comprehensive quality assessment using rubric from QUALITY_STANDARDS.md

**Usage:**
```bash
Please assess-quality for [ENTRY-ID]
```

**What it does:**
- Evaluates entry on 5 dimensions (100 points total)
- Generates detailed scoring report
- Identifies specific weaknesses
- Recommends improvements
- Updates metadata with score

**Example:**
```bash
Please assess-quality for IMPORT-001
```

**Output:**
```yaml
quality_assessment:
  entry_id: "IMPORT-001"
  file: "python/errors/imports.yaml"
  assessed_at: "2026-01-05T18:00:00Z"
  assessor: "curator"

  dimensions:
    completeness:
      score: 24/25
      breakdown:
        required_fields: 5/5
        solution_quality: 9/10
        prevention_context: 5/5
        metadata: 5/5
      strengths:
        - All required fields present
        - Comprehensive solution with code
        - Excellent prevention guidelines
      weaknesses:
        - "Solution could show alternative approach"
      improvement_potential: "+1 point"

    technical_accuracy:
      score: 23/25
      breakdown:
        code_correctness: 10/10
        version_currency: 8/8
        solution_effectiveness: 5/7
      strengths:
        - Code compiles and runs correctly
        - Tested with Python 3.12 and 3.13
        - Solves the stated problem
      weaknesses:
        - "Solution not tested in production context"
        - "Edge cases not documented"
      improvement_potential: "+2 points"

    clarity:
      score: 18/20
      breakdown:
        problem_description: 5/5
        explanation_quality: 9/10
        code_documentation: 4/5
      strengths:
        - Problem clearly described
        - Good explanation of why it works
      weaknesses:
        - "Could explain TYPE_CHECKING mechanism in more detail"
      improvement_potential: "+2 points"

    discoverability:
      score: 13/15
      breakdown:
        title_quality: 5/5
        tag_relevance: 4/5
        cross_references: 4/5
      strengths:
        - Descriptive, searchable title
        - Relevant tags
      weaknesses:
        - "Could add 'import-cycle' tag"
        - "Cross-references to related patterns could be expanded"
      improvement_potential: "+2 points"

    actionability:
      score: 14/15
      breakdown:
        solution_immediacy: 5/5
        prevention_actionability: 4/5
        examples_context: 5/5
      strengths:
        - Immediately implementable
        - Real-world example included
      weaknesses:
        - "Prevention could include automated testing strategy"
      improvement_potential: "+1 point"

  total_score: 92/100

  quality_level: "excellent"
  threshold: "≥ 90 (⭐⭐⭐)"

  status: "ready_for_shared_repository"

  improvement_plan:
    to_reach_95:
      - priority: "low"
        action: "Add alternative solution approach"
        dimension: "completeness"
        potential_gain: "+1 point"

      - priority: "low"
        action: "Document edge cases and production testing"
        dimension: "technical_accuracy"
        potential_gain: "+2 points"

    to_reach_100:
      - priority: "medium"
        action: "Expand TYPE_CHECKING explanation"
        dimension: "clarity"
        potential_gain: "+2 points"

      - priority: "low"
        action: "Add 'import-cycle' tag"
        dimension: "discoverability"
        potential_gain: "+1 point"

      - priority: "low"
        action: "Include automated testing in prevention"
        dimension: "actionability"
        potential_gain: "+1 point"

  recommended_actions:
    immediate: []  # No critical issues
    optional:
      - "Test solution in production context"
      - "Add edge case documentation"
      - "Expand cross-references"

  metadata_updates:
    quality_score: 92
    quality_assessed_at: "2026-01-05T18:00:00Z"
    quality_assessed_by: "curator"
    validation_status: "validated"
```

**Follow-up:**
```bash
# Apply optional improvements
Please enhance-entry IMPORT-001 with:
  - "Add production testing notes"
  - "Document edge cases"
```

---

## Skill: `reindex-metadata`

**Purpose:** Rebuild global metadata index from all `_meta.yaml` files

**Usage:**
```bash
Please reindex-metadata
```

**What it does:**
- Scans all `_meta.yaml` files
- Aggregates entry metadata
- Updates `_index.yaml`
- Generates statistics
- Detects alerts and issues

**Example:**
```bash
Please reindex-metadata
```

**Output:**
```yaml
metadata_reindex:
  timestamp: "2026-01-05T19:00:00Z"
  duration_seconds: 2.3

  scan_results:
    meta_files_scanned: 18
    entries_cataloged: 127
    files_processed: 45

  index_created: "_index.yaml"
  size_bytes: 15234

  statistics:
    by_scope:
      universal: 22
      python: 45
      javascript: 12
      docker: 18
      postgresql: 15
      framework: 15

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

  alerts_generated:
    overdue_reviews:
      - entry_id: "IMPORT-002"
        due: "2026-01-10"
        overdue_by: "5 days"
        priority: "critical"

    low_quality_high_usage:
      - entry_id: "OLD-001"
        quality_score: 45
        access_count: 28
        priority: "high"

    version_updates_available:
      - entry_id: "FASTAPI-005"
        tested: "0.100.0"
        current: "0.115.0"
        priority: "high"

  summary:
    status: "success"
    total_alerts: 4
    critical_actions: 3
    next_reindex_recommended: "2026-01-12"
```

---

## Skill: `export-analytics`

**Purpose:** Export anonymized usage analytics for community aggregation (opt-in)

**Usage:**
```bash
Please export-analytics for [period] to [output-file]
```

**What it does:**
- Reads `.cache/usage.json`
- Aggregates statistics
- Anonymizes data (removes project IDs, timestamps, etc.)
- Generates shareable analytics file
- Preserves privacy

**Example:**
```bash
Please export-analytics for 2026-01 to analytics-community-2026-01.json
```

**Output:**
```json
{
  "version": "1.0",
  "period": "2026-01",
  "project_type": "web-api",
  "anonymized": true,

  "usage_summary": {
    "total_searches": 342,
    "successful_searches": 298,
    "unique_entries_accessed": 34,
    "success_rate": 0.87
  },

  "top_accessed_entries": [
    {"entry_id": "IMPORT-001", "access_count": 47},
    {"entry_id": "DOCKER-024", "access_count": 35},
    {"entry_id": "TEST-003", "access_count": 28}
  ],

  "search_gaps": [
    {"query": "fastapi websocket timeout", "count": 12},
    {"query": "pytest async fixture loop", "count": 8}
  ],

  "category_usage": {
    "python": 156,
    "docker": 89,
    "javascript": 45,
    "postgresql": 34
  },

  "quality_opportunities": [
    {
      "entry_id": "OLD-001",
      "access_count": 28,
      "quality_score": 45,
      "improvement_needed": 30
    }
  ]
}
```

**Privacy Note:**
- No project identification
- No exact timestamps (only period)
- No session details
- Only aggregated statistics
- Opt-in (manual execution)

---

## Workflow Integration

### Complete Metadata-Driven Workflow

```bash
# 1. Detect changes after git pull
Please detect-changes since last sync

# 2. Check freshness of existing entries
Please check-freshness for all

# 3. Analyze local usage to find gaps
Please analyze-usage for last-30-days

# 4. Process analysis queue
For each new/modified entry:
  a. Please validate-technical for [ENTRY-ID]
  b. Please assess-quality for [ENTRY-ID]
  c. Please update-metadata for [ENTRY-ID]

# 5. Address critical gaps
For each high-priority gap:
  a. Please create-entry for [topic]
  b. Please research-enhance entry [NEW-ID]
  c. Please update-metadata for [NEW-ID]

# 6. Rebuild metadata index
Please reindex-metadata

# 7. Rebuild search index
python tools/kb.py index --force

# 8. (Optional) Export analytics
Please export-analytics for 2026-01 to analytics-2026-01.json
```

---

## Skills Summary

| Skill | Purpose | Output | Updates Metadata |
|-------|---------|--------|------------------|
| `check-freshness` | Find outdated entries | Action list | No |
| `track-usage` | Record entry access | Usage log | Yes (`.usage.json`) |
| `detect-changes` | Find new/modified entries | Change queue | No |
| `analyze-usage` | Identify gaps & improvements | Analysis report | No |
| `update-metadata` | Create/update `_meta.yaml` | Confirmation | Yes |
| `assess-quality` | Score entry quality | Quality report | Yes |
| `reindex-metadata` | Rebuild global index | Statistics | Yes (`_index.yaml`) |
| `export-analytics` | Export anonymized data | Analytics file | No |

These metadata-driven skills enable systematic, trackable knowledge curation without central infrastructure.
