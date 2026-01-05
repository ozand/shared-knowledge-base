# SKILLS.md - Knowledge Base Curator Skills

## Available Skills

As the Knowledge Base Curator, you have access to these specialized skills. Each skill encapsulates a specific workflow or capability.

### Skill: `audit-quality`

**Purpose:** Perform comprehensive quality audit on knowledge base entries

**Usage:**
```
Please run audit-quality on [scope/category]
```

**What it does:**
- Scans specified entries for completeness
- Checks for duplicate detection
- Validates YAML syntax
- Verifies code examples
- Checks version currency
- Generates quality report with recommendations

**Example:**
```bash
# Audit Python errors
Please run audit-quality on python/errors

# Audit entire KB
Please run audit-quality on all
```

**Output:**
- Quality score (0-100) for each entry
- List of duplicates found
- Entries needing updates
- Code validation results
- Priority ranking for improvements

---

### Skill: `find-duplicates`

**Purpose:** Identify semantically duplicate or near-duplicate entries

**Usage:**
```
Please run find-duplicates in [scope]
```

**What it does:**
- Analyzes entry titles and descriptions
- Identifies similar problem statements
- Finds overlapping solutions
- Suggests merge candidates
- Creates consolidation plan

**Example:**
```bash
# Find duplicates in Python
Please run find-duplicates in python

# Find cross-scope duplicates
Please run find-duplicates across all scopes
```

**Output:**
- Groups of duplicate/near-duplicate entries
- Similarity scores
- Recommended canonical entry
- Merge strategy
- Cross-reference update plan

---

### Skill: `research-enhance`

**Purpose:** Enhance entry with deep research from external sources

**Usage:**
```
Please research-enhance entry [ERROR-ID]
or
Please research-enhance file [path/to/file.yaml]
```

**What it does:**
- Queries Perplexity/Gemini for latest best practices
- Searches official documentation
- Reviews community discussions (Stack Overflow, GitHub, Reddit)
- Validates current approach
- Enhances entry with:
  - Latest API versions
  - Additional context
  - Alternative solutions
  - Security/performance considerations
  - Real-world examples

**Example:**
```bash
# Enhance specific entry
Please research-enhance entry IMPORT-001

# Enhance entire file
Please research-enhance file python/errors/imports.yaml
```

**Output:**
- Enhanced YAML content with research citations
- List of sources consulted
- Summary of findings
- Recommended changes
- Confidence level for recommendations

---

### Skill: `validate-technical`

**Purpose:** Technically validate code examples and solutions

**Usage:**
```
Please validate-technical for [ERROR-ID]
```

**What it does:**
- Checks syntax of code examples
- Verifies imports and dependencies
- Tests solution if possible
- Identifies deprecated APIs
- Checks version compatibility
- Validates error messages

**Example:**
```bash
# Validate specific entry
Please validate-technical for IMPORT-001

# Validate all entries in file
Please validate-technical for python/errors/testing.yaml
```

**Output:**
- Code validation results
- Syntax errors found
- Deprecated API warnings
- Version incompatibilities
- Corrected code examples
- Test results (if applicable)

---

### Skill: `promote-scope`

**Purpose:** Promote entry from specific scope to more universal scope

**Usage:**
```
Please promote-scope for [ERROR-ID] to [target-scope]
```

**What it does:**
- Analyzes if solution is universally applicable
- Removes language-specific details
- Extracts universal pattern
- Creates new entry in target scope
- Updates cross-references
- Maintains original as specific implementation

**Example:**
```bash
# Promote Python error to Universal
Please promote-scope for PYTHON-015 to universal

# Promote framework error to language
Please promote-scope for FASTAPI-008 to python
```

**Output:**
- Analysis of applicability
- Proposed universal entry
- Mapping from specific to universal
- Cross-reference updates
- Recommendation on whether to promote

---

### Skill: `identify-gaps`

**Purpose:** Identify gaps in knowledge base coverage

**Usage:**
```
Please identify-gaps in [scope]
or
Please identify-gaps for [topic]
```

**What it does:**
- Analyzes existing entries
- Searches for common errors not covered
- Reviews industry trends
- Checks framework documentation for known issues
- Surveys community resources
- Generates prioritized list of missing entries

**Example:**
```bash
# Find gaps in Python testing
Please identify-gaps in python/testing

# Find gaps for async/await
Please identify-gaps for async patterns
```

**Output:**
- List of suggested new entries
- Priority ranking (by frequency/impact)
- Draft problem statements
- Recommended scope levels
- Sources for research

---

### Skill: `update-versions`

**Purpose:** Update entries to current library/framework versions

**Usage:**
```
Please update-versions for [ERROR-ID]
or
Please update-versions for [language/framework]
```

**What it does:**
- Checks current versions of dependencies
- Identifies affected entries
- Researches breaking changes
- Updates code examples
- Adds version-specific notes
- Marks migration paths

**Example:**
```bash
# Update specific entry
Please update-versions for IMPORT-002

# Update all FastAPI entries
Please update-versions for FastAPI
```

**Output:**
- Entries updated
- Version changelog
- Breaking changes documented
- Migration guides created
- Deprecated entries marked

---

### Skill: `merge-entries`

**Purpose:** Merge duplicate or related entries

**Usage:**
```
Please merge-entries [ERROR-ID-1] and [ERROR-ID-2]
```

**What it does:**
- Analyzes both entries
- Identifies unique contributions
- Creates consolidated entry
- Preserves all valuable information
- Updates cross-references
- Marks old entries as deprecated

**Example:**
```bash
# Merge two entries
Please merge-entries IMPORT-001 and IMPORT-005
```

**Output:**
- Merged entry content
- Summary of what was preserved
- Cross-reference updates needed
- Deprecation notices for old entries

---

### Skill: `analyze-usage`

**Purpose:** Analyze knowledge base usage patterns (if logs available)

**Usage:**
```
Please analyze-usage for [time-period]
```

**What it does:**
- Reviews search logs
- Identifies most accessed entries
- Finds search terms with no results
- Detects trending topics
- Suggests entries to feature/improve
- Recommends entries to deprecate

**Example:**
```bash
# Analyze last month
Please analyze-usage for last-30-days

# Analyze all time
Please analyze-usage for all-time
```

**Output:**
- Top accessed entries
- Search gap analysis
- Trending topics
- Underutilized entries
- Improvement recommendations

---

### Skill: `review-contribution`

**Purpose:** Review user-submitted knowledge base entry

**Usage:**
```
Please review-contribution [path/to/file.yaml]
```

**What it does:**
- Validates YAML syntax
- Checks for duplicates
- Verifies technical accuracy
- Tests code examples
- Researches best practices
- Provides constructive feedback
- Suggests improvements

**Example:**
```bash
# Review new contribution
Please review-contribution docs/knowledge-base/errors/new-entry.yaml
```

**Output:**
- Validation results
- Duplicate analysis
- Technical assessment
- Improvement suggestions
- Approval/rejection rationale
- Recommended changes

---

### Skill: `create-entry`

**Purpose:** Create new knowledge base entry from scratch

**Usage:**
```
Please create-entry for [problem description]
```

**What it does:**
- Analyzes problem description
- Researches best practices
- Determines appropriate scope
- Creates structured YAML entry
- Validates format
- Suggests related entries
- Generates draft ID

**Example:**
```bash
# Create entry from error
Please create-entry for "TypeError: 'NoneType' object is not subscriptable in FastAPI dependency"
```

**Output:**
- Draft YAML entry
- Recommended scope and category
- Related entries found
- Research sources
- Validation results
- Next steps for completion

---

### Skill: `export-for-ai`

**Purpose:** Export knowledge base in AI-optimized format

**Usage:**
```
Please export-for-ai in [format] for [ai-tool]
```

**What it does:**
- Converts KB to specified format
- Optimizes for AI tool consumption
- Includes metadata for matching
- Filters by scope/tags if requested
- Generates export summary

**Example:**
```bash
# Export for Claude Code
Please export-for-ai in markdown for claude-code

# Export JSON for Copilot
Please export-for-ai in json for github-copilot
```

**Output:**
- Exported file(s)
- Format specifications
- Entry count
- Metadata included
- Usage instructions for AI tool

---

### Skill: `cleanup-cache`

**Purpose:** Clean and rebuild knowledge base index

**Usage:**
```
Please cleanup-cache and rebuild
```

**What it does:**
- Removes old index files
- Clears stale cache
- Validates all entries
- Rebuilds SQLite index
- Verifies search functionality
- Generates statistics

**Example:**
```bash
Please cleanup-cache and rebuild
```

**Output:**
- Cache cleanup summary
- Validation results
- Index build statistics
- Search verification
- Final KB statistics

---

## Skill Composition

Skills can be combined for complex workflows:

### Example: Comprehensive Entry Enhancement
```
1. Please validate-technical for IMPORT-001
2. Please research-enhance entry IMPORT-001
3. Please find-duplicates in python for IMPORT-001
4. If duplicates found: Please merge-entries IMPORT-001 and DUPLICATE-ID
```

### Example: New Entry Creation
```
1. Please identify-gaps for "FastAPI websocket errors"
2. Please create-entry for [identified gap]
3. Please research-enhance entry [NEW-ID]
4. Please validate-technical for [NEW-ID]
```

### Example: Scheduled Maintenance
```
1. Please analyze-usage for last-30-days
2. Please update-versions for python
3. Please audit-quality on high-use entries
4. Please cleanup-cache and rebuild
```

## Skill Parameters

All skills support optional parameters:

- `--verbose` - Detailed output
- `--dry-run` - Show what would happen without making changes
- `--scope=` - Filter by scope
- `--severity=` - Filter by severity level
- `--tags=` - Filter by tags
- `--limit=` - Limit number of entries processed

## Custom Skills

New skills can be created on-demand based on recurring needs. Suggest new skills when you identify patterns that could be automated.

## Skill Execution

When you request a skill:
1. Skill validates prerequisites (e.g., kb.py available)
2. Skill performs its core function
3. Skill generates structured output
4. Skill suggests next steps or related skills

Skills are designed to be **idempotent** - can be run multiple times safely without side effects (unless they explicitly modify data).
