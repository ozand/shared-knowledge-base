# For Claude Code: Shared Knowledge Base System

**Complete guide for Claude Code agents on the enhanced Shared Knowledge Base**

**Last Updated:** 2026-01-05
**Version:** 3.0 (with Phase 1-3 enhancements)

---

## 🎯 What's New in Version 3.0

The Shared Knowledge Base now includes:

### Phase 1: Essential Metadata ✅
- **Metadata Management** (`tools/kb_meta.py`): Track creation dates, quality scores, validation status
- **Usage Analytics** (`tools/kb_usage.py`): Track entry access, search gaps, high-usage entries
- **Change Detection** (`tools/kb_changes.py`): Hash-based detection of content changes
- **Enhanced CLI** (`tools/kb.py`): 6 new commands for metadata operations

### Phase 2: Enhanced Features ✅
- **Freshness Checking** (`tools/kb_freshness.py`): Automatic library version checks, stale entry detection
- **Git Integration** (`tools/kb_git.py`): Change detection via git, post-merge hooks
- **Automated Scripts**:
  - `scripts/daily_freshness.py`: Daily freshness checks
  - `scripts/weekly_usage.py`: Weekly usage analysis

### Phase 3: Advanced Analytics ✅
- **Version Monitoring** (`tools/kb_versions.py`): Track library versions from PyPI, npm, GitHub
- **Community Analytics** (`tools/kb_community.py`): Aggregate anonymized data across projects
- **Predictive Analytics** (`tools/kb_predictive.py`): Predict updates, assess risks, estimate quality
- **Pattern Recognition** (`tools/kb_patterns.py`): Find similar patterns, suggest universal promotions
- `scripts/monthly_community.py`: Monthly community aggregation

### New Documentation 📚
- `AGENT.md`: Knowledge Base Curator role definition
- `SKILLS.md`: 12 base skills + 8 metadata skills
- `WORKFLOWS.md`: 6 detailed workflows
- `QUALITY_STANDARDS.md`: 100-point quality rubric
- `PROMPTS.md`: 16 reusable prompt templates
- `METADATA_ARCHITECTURE.md`: Complete metadata system design
- `PHASE3_SUMMARY.md`: Phase 3 implementation details

---

## Installation for New Projects

### Unified Installation (Recommended)

**For new projects setting up Shared KB:**

```bash
# Method 1: From cloned repository
python scripts/unified-install.py --full

# Method 2: Remote download (one-line)
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/unified-install.py | python3 - --full
```

**What it does:**
- ✅ Adds submodule with sparse checkout (excludes curator/)
- ✅ Installs agents (1 main + 4 subagents)
- ✅ Installs skills (7 skills)
- ✅ Installs commands (7 commands)
- ✅ Creates configuration files
- ✅ Builds search index
- ✅ Verifies installation

**For existing projects:**
```bash
# Check for updates
python docs/knowledge-base/shared/scripts/unified-install.py --check

# Update existing installation
python docs/knowledge-base/shared/scripts/unified-install.py --update
```

### Manual Installation (Alternative)

```bash
# Add submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base/shared

# Install integration
python docs/knowledge-base/shared/for-projects/scripts/install.py --full
```

**See:** `UNIFIED-INSTALL-001` pattern for details

---

## Quick Reference for Claude Code

### Basic Commands

```bash
# Search knowledge base
python tools/kb.py search "websocket"
python tools/kb.py search --id ERROR-ID
python tools/kb.py search --scope python --tag async

# Statistics
python tools/kb.py stats

# Build index
python tools/kb.py index -v
```

### Metadata Commands (Phase 1)

```bash
# Initialize metadata for all entries
python tools/kb.py init-metadata

# Detect changes since last check
python tools/kb.py detect-changes

# Check entry freshness
python tools/kb.py check-freshness

# Analyze usage patterns
python tools/kb.py analyze-usage

# Update entry metadata
python tools/kb.py update-metadata --entry-id ERROR-ID --quality-score 85

# Reindex metadata
python tools/kb.py reindex-metadata
```

### Version Monitoring (Phase 3)

```bash
# Check specific library version
python -m tools.kb_versions check --library fastapi

# Check all libraries
python -m tools.kb_versions check --all

# Update all entries using a library
python -m tools.kb_versions update --library fastapi --version 0.128.0

# Scan KB for tested versions
python -m tools.kb_versions scan
```

### Predictive Analytics (Phase 3)

```bash
# Predict updates needed
python -m tools.kb_predictive predict-updates --days 30

# Suggest new entries based on search gaps
python -m tools.kb_predictive suggest-entries

# Estimate quality for entry
python -m tools.kb_predictive estimate-quality --entry-id ERROR-001

# Assess risk for entry
python -m tools.kb_predictive risk-assessment --entry-id ERROR-001

# Generate comprehensive report
python -m tools.kb_predictive report
```

### Pattern Recognition (Phase 3)

```bash
# Find similar patterns
python -m tools.kb_patterns link-related --min-similarity 0.5

# Analyze specific pattern
python -m tools.kb_patterns analyze-pattern --entry-id ERROR-001

# Find universal pattern candidates
python -m tools.kb_patterns find-universal

# Generate pattern report
python -m tools.kb_patterns report
```

### Community Analytics (Phase 3)

```bash
# Export local analytics (for sharing)
python -m tools.kb_community export-analytics --project-name "MyApp" --project-type web

# Generate community report
python -m tools.kb_community report
```

---

## 🚨 Agent Behavior Rules - CRITICAL

### MANDATORY WORKFLOW FOR UNIVERSAL ERRORS

**When adding KB entries with these scopes:**
- **docker**
- **universal**
- **python**
- **postgresql**
- **javascript**

**YOU MUST:**

#### 1. Create file in SHARED KB (NOT local!)

```bash
# ✅ CORRECT: Create here
T:\Code\shared-knowledge-base\<scope>\errors\<filename>.yaml

# ❌ WRONG: NOT in project-specific KB
\path\to\project\docs\knowledge-base\<scope>\errors\<filename>.yaml
```

#### 2. Initialize Metadata

```bash
python tools/kb.py init-metadata --verbose
```

This creates `*_meta.yaml` files alongside YAML files with:
- `created_at`: Creation timestamp
- `last_analyzed_at`: Last review date
- `quality_score`: 0-100 (based on 5 dimensions)
- `validation_status`: validated/pending/needs_review
- `tested_versions`: Library versions tested
- `next_version_check_due`: When to check library versions

#### 3. Validate YAML

```bash
python tools/kb.py validate
```

#### 4. Assess Quality

```bash
python -m tools.kb_predictive estimate-quality --entry-id ERROR-001
```

Ensure quality score ≥ 75 before committing to shared repository.

#### 5. IMMEDIATELY commit and push

```bash
git add <file> *_meta.yaml
git commit -m "Add ERROR-ID: Error Title

- Brief description
- Related issues
- Real-world example
- Quality score: X/100

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

git push origin main

# If push fails with conflicts:
git pull --rebase origin main
git push origin main
```

#### 6. Rebuild index

```bash
python tools/kb.py index --force -v
```

#### 7. Confirm to user

```
✅ KB entry added to shared-knowledge-base repository
📝 Metadata initialized
⭐ Quality score: X/100
📦 Committed: <commit-hash>
🚀 Pushed to: origin/main
🔍 Index rebuilt
🌐 Available at: https://github.com/ozand/shared-knowledge-base
```

---

## Quick Decision Tree (Enhanced)

```
User reports error
    ↓
Search KB: python tools/kb.py search "error"
    ↓
Found? ──Yes──→ Return solution ✅
    ↓
   No
    ↓
Solve problem + Document in YAML
    ↓
Initialize metadata: python tools/kb.py init-metadata
    ↓
Assess quality: python -m tools.kb_predictive estimate-quality
    ↓
Quality ≥ 75? ──No──→ Enhance content
    ↓Yes
Determine scope:
    ├─ docker, universal, python, postgresql, javascript?
    │   ↓
    │   Create in shared-knowledge-base/<scope>/
    │   ↓
    │   Validate YAML
    │   ↓
    │   git add <file> *_meta.yaml
    │   git commit -m "Add ERROR-ID: Title"
    │   git push origin main
    │   ↓ (if conflict)
    │   git pull --rebase origin main
    │   git push origin main
    │   ↓
    │   Rebuild index
    │   ↓
    │   Confirm: "✅ Synced to shared-knowledge-base"
    │   └→ Done ✅
    │
    └─ project, domain, framework?
        ↓
        Create in project's local KB
        ↓
        Add metadata: local_only: true
        ↓
        Validate YAML
        ↓
        Rebuild index
        ↓
        Confirm: "✅ Added to local KB (project-specific)"
        └→ Done ✅
```

---

## Automated Scripts (Schedule with cron/Task Scheduler)

### Daily Freshness Check

```bash
# Run daily at 2 AM
0 2 * * * python T:\Code\shared-knowledge-base\scripts\daily_freshness.py
```

Checks:
- Library version updates (via `tools/kb_versions.py`)
- Entries needing review (based on `last_analyzed_at`)
- Stale entries (>6 months since last update)

### Weekly Usage Analysis

```bash
# Run weekly on Monday at 10 AM
0 10 * * 1 python T:\Code\shared-knowledge-base\scripts\weekly_usage.py --days 7
```

Analyzes:
- Top accessed entries
- Search gaps (failed searches)
- High-access, low-quality entries
- Usage trends

### Monthly Community Aggregation

```bash
# Run monthly on 1st day at midnight
0 0 1 * * python T:\Code\shared-knowledge-base\scripts\monthly_community.py
```

Aggregates:
- Community-wide usage patterns
- Universal patterns (used in ≥3 projects)
- Community search gaps
- Quality trends

---

## Quality Standards (100-Point Rubric)

### Dimensions (20 points each)

1. **Completeness** (20 points)
   - Problem description: 5 points
   - Root cause analysis: 5 points
   - Multiple solutions: 5 points
   - Prevention tips: 5 points

2. **Technical Accuracy** (20 points)
   - Code examples work: 10 points
   - Information current: 5 points
   - No factual errors: 5 points

3. **Clarity** (20 points)
   - Clear title: 5 points
   - Structured content: 5 points
   - Examples explained: 5 points
   - Language simple: 5 points

4. **Discoverability** (20 points)
   - Descriptive ID: 5 points
   - Relevant tags: 5 points
   - Good summary: 5 points
   - Links to related entries: 5 points

5. **Actionability** (20 points)
   - Step-by-step solution: 10 points
   - Copy-pasteable code: 5 points
   - Test verification: 5 points

### Quality Thresholds

- **90-100**: Excellent ⭐⭐⭐ (ready for shared KB)
- **75-89**: Good ⭐⭐ (acceptable for shared KB)
- **60-74**: Acceptable ⭐ (needs improvement)
- **<60**: Needs Improvement (not ready for shared KB)

**Quality Gate**: Minimum score 75 required before committing to shared repository.

---

## File Structure (Updated)

```
shared-knowledge-base/
├── tools/                      # Python tools
│   ├── kb.py                  # Main CLI (enhanced with 6 new commands)
│   ├── kb_config.py           # Configuration management
│   ├── kb_meta.py             # Metadata manager (Phase 1)
│   ├── kb_usage.py            # Usage tracker (Phase 1)
│   ├── kb_changes.py          # Change detector (Phase 1)
│   ├── kb_freshness.py        # Freshness checker (Phase 2)
│   ├── kb_git.py              # Git integration (Phase 2)
│   ├── kb_versions.py         # Version monitor (Phase 3)
│   ├── kb_community.py        # Community analytics (Phase 3)
│   ├── kb_predictive.py       # Predictive analytics (Phase 3)
│   └── kb_patterns.py         # Pattern recognizer (Phase 3)
├── scripts/                   # Automation scripts
│   ├── init_metadata.py       # Initialize metadata
│   ├── daily_freshness.py     # Daily freshness checks
│   ├── weekly_usage.py        # Weekly usage analysis
│   └── monthly_community.py   # Monthly community aggregation
├── .cache/                    # Local cache (NOT git-synced)
│   ├── usage.json             # Usage analytics
│   ├── file_hashes.json       # Hash cache for change detection
│   ├── versions.json          # Version cache
│   └── community/             # Community data
├── _index.yaml                # Global index (auto-generated, NOT git-synced)
├── *_meta.yaml                # Metadata files (git-synced) ✓
├── .gitignore                 # Updated to exclude cache, include metadata
├── .kb-config.yaml            # KB configuration
│
├── 📚 Documentation (New):
│   ├── AGENT.md               # Curator role definition
│   ├── SKILLS.md              # 12 base + 8 metadata skills
│   ├── WORKFLOWS.md           # 6 detailed workflows
│   ├── QUALITY_STANDARDS.md   # 100-point quality rubric
│   ├── PROMPTS.md             # 16 prompt templates
│   ├── METADATA_ARCHITECTURE.md  # Metadata system design
│   ├── METADATA_SKILLS.md     # 8 metadata-driven skills
│   ├── IMPLEMENTATION_GUIDE.md # Python implementation details
│   ├── METADATA_SUMMARY.md    # Executive summary
│   ├── PHASE3_SUMMARY.md      # Phase 3 details
│   └── FOR_CLAUDE_CODE.md     # This file
│
└── 📦 Knowledge Content:
    ├── universal/             # Universal errors & patterns
    ├── python/                # Python-specific
    ├── javascript/            # JavaScript/Node.js
    ├── postgresql/            # PostgreSQL
    ├── docker/                # Docker/container
    └── framework/             # Framework-specific (FastAPI, React, etc.)
```

**Legend:**
- ✓ Git-synced (committed to repository)
- ✗ Local only (NOT committed)

---

## Updating Existing Projects

### Step 1: Pull Latest Changes

```bash
cd T:\Code\shared-knowledge-base
git pull origin main
```

### Step 2: Update Documentation

Ask the user to read the updated documentation:

```
📚 Shared Knowledge Base has been updated to version 3.0!

New features:
- ✅ Metadata management (quality scores, usage tracking)
- ✅ Freshness checking (library version monitoring)
- ✅ Predictive analytics (update predictions, risk assessment)
- ✅ Pattern recognition (find similar patterns)
- ✅ Community analytics (aggregate data across projects)

Please read:
- FOR_CLAUDE_CODE.md (this file) - Updated guide
- PHASE3_SUMMARY.md - Phase 3 details
- METADATA_ARCHITECTURE.md - Metadata system design

Recommended actions:
1. Initialize metadata: python tools/kb.py init-metadata
2. Run freshness check: python tools/kb.py check-freshness
3. Schedule automated scripts (see below)
```

### Step 3: Initialize Metadata (First Time Only)

```bash
cd T:\Code\shared-knowledge-base
python tools/kb.py init-metadata --verbose
```

This creates `*_meta.yaml` files for all entries.

### Step 4: Schedule Automated Scripts

**Linux/macOS (cron):**

```bash
# Edit crontab
crontab -e

# Add these lines:
0 2 * * * cd /path/to/shared-knowledge-base && python scripts/daily_freshness.py
0 10 * * 1 cd /path/to/shared-knowledge-base && python scripts/weekly_usage.py --days 7
0 0 1 * * cd /path/to/shared-knowledge-base && python scripts/monthly_community.py
```

**Windows (Task Scheduler):**

Create tasks that run:
```
python T:\Code\shared-knowledge-base\scripts\daily_freshness.py
python T:\Code\shared-knowledge-base\scripts\weekly_usage.py --days 7
python T:\Code\shared-knowledge-base\scripts\monthly_community.py
```

---

## Troubleshooting (Updated)

### Import Errors for New Tools

```python
# Add tools directory to path
import sys
from pathlib import Path
tools_dir = Path(__file__).parent / "tools"
sys.path.insert(0, str(tools_dir))

# Now import
from kb_meta import MetadataManager
from kb_predictive import PredictiveAnalytics
```

### No Usage Data Yet

Predictive features require usage data accumulation:

```bash
# Use KB regularly (search, view entries)
# Wait 1-2 weeks for data accumulation
# Check progress:
python tools/kb.py analyze-usage
```

### API Rate Limiting (Version Checks)

Some version checks may fail due to API rate limiting:
- GitHub API: 60 requests/hour (unauthenticated)
- PyPI: No rate limit
- npm: No rate limit

**Solution**: Use cached versions or add authentication.

---

## Verification Checklist (Updated)

After updating to version 3.0, verify:

- [ ] `tools/kb_meta.py` exists
- [ ] `tools/kb_usage.py` exists
- [ ] `tools/kb_freshness.py` exists
- [ ] `tools/kb_versions.py` exists
- [ ] `tools/kb_predictive.py` exists
- [ ] `tools/kb_patterns.py` exists
- [ ] `tools/kb_community.py` exists
- [ ] `scripts/` directory contains automation scripts
- [ ] Metadata files (`*_meta.yaml`) created
- [ ] `tools/kb.py` has 6 new commands
- [ ] Automated scripts scheduled (optional)
- [ ] Documentation files exist (AGENT.md, SKILLS.md, etc.)

---

## Summary for Claude Code

**When user says "update knowledge base":**

1. Pull latest changes: `git pull origin main`
2. Initialize metadata: `python tools/kb.py init-metadata`
3. Run freshness check: `python tools/kb.py check-freshness`
4. Check for updates: `python -m tools.kb_versions check --all`
5. Generate predictions: `python -m tools.kb_predictive report`
6. Schedule automated scripts (optional)

**New capabilities available:**
- Track entry quality (0-100 scale)
- Monitor library versions automatically
- Predict which entries need updates
- Find similar patterns across projects
- Aggregate analytics across community

**Estimated setup time:** 10-15 minutes

---

## Additional Resources

### Internal Documentation
- `AGENT.md`: Knowledge Base Curator role
- `SKILLS.md`: All available skills
- `WORKFLOWS.md`: Step-by-step procedures
- `QUALITY_STANDARDS.md`: Quality rubric
- `PROMPTS.md`: Prompt templates

### Technical Documentation
- `METADATA_ARCHITECTURE.md`: System architecture
- `IMPLEMENTATION_GUIDE.md`: Code examples
- `PHASE3_SUMMARY.md`: Phase 3 details
- `README.md`: Project overview

### External Resources
- [Claude Code Documentation](https://claude.com/claude-code)
- [Shared KB Repository](https://github.com/ozand/shared-knowledge-base)

---

**Version:** 3.0
**Last Updated:** 2026-01-05
**Maintained By:** Development Team & Claude Code
**Issues?** See: [GitHub Issues](https://github.com/ozand/shared-knowledge-base/issues)
