# Deployment Guide: Shared Knowledge Base v5.1

## Overview

This document explains how to deploy Shared Knowledge Base v5.1 to GitHub and update existing projects.

---

## 1. Deployment to GitHub

### Files to Commit

#### ✅ DO Commit These Files:

**Core Tools:**
```
tools/kb.py                    # Main CLI (modified)
tools/kb_config.py            # Configuration (existing)
tools/kb_meta.py              # Metadata manager (new)
tools/kb_usage.py             # Usage tracker (new)
tools/kb_changes.py           # Change detector (new)
tools/kb_freshness.py         # Freshness checker (new)
tools/kb_git.py               # Git integration (new)
tools/kb_versions.py          # Version monitor (new)
tools/kb_community.py         # Community analytics (new)
tools/kb_predictive.py        # Predictive analytics (new)
tools/kb_patterns.py          # Pattern recognizer (new)
```

**Automation Scripts:**
```
scripts/init_metadata.py      # Initialize metadata (new)
scripts/daily_freshness.py    # Daily freshness checks (new)
scripts/weekly_usage.py       # Weekly usage analysis (new)
scripts/monthly_community.py  # Monthly community aggregation (new)
```

**Documentation:**
```
AGENT.md                       # Curator role definition (new)
SKILLS.md                      # 12 base + 8 metadata skills (new)
WORKFLOWS.md                   # 6 detailed workflows (new)
QUALITY_STANDARDS.md           # 100-point quality rubric (new)
PROMPTS.md                     # 16 prompt templates (new)
METADATA_ARCHITECTURE.md       # Metadata system design (new)
METADATA_SKILLS.md             # 8 metadata-driven skills (new)
IMPLEMENTATION_GUIDE.md        # Python implementation details (new)
METADATA_SUMMARY.md            # Executive summary (new)
PHASE3_SUMMARY.md              # Phase 3 implementation details (new)
FOR_CLAUDE_CODE.md             # Updated guide (modified)
README.md                      # Project overview (modified)
CLAUDE.md                      # Quick start (new)
CURATOR_DOCS_INDEX.md          # Documentation index (new)
README_CURATOR.md              # Curator quick start (new)
```

**Configuration:**
```
.gitignore                     # Updated (modified)
```

**Example Metadata (Optional):**
```
*_meta.yaml                    # Example metadata files (new)
```

#### ❌ DO NOT Commit These Files:

**Generated/Cache:**
```
.cache/                        # Local cache directory
_index.yaml                    # Auto-generated index
.kb-config-local.yaml          # Local configuration
kb-export.json                 # Exported JSON
kb-snapshot.json               # Snapshot JSON
```

**Generated Documentation:**
```
docs/                          # Generated docs directory
```

### Commit Steps

```bash
cd T:\Code\shared-knowledge-base

# Add all tools
git add tools/kb*.py

# Add scripts
git add scripts/

# Add documentation
git add *.md

# Add updated .gitignore
git add .gitignore

# Add example metadata (optional - shows users format)
# Uncomment if you want to include:
# git add *_meta.yaml

# Check what will be committed
git status

# Commit
git commit -m "Release v5.1: Phase 1-3 Complete

Phase 1: Essential Metadata
- Metadata management (kb_meta.py)
- Usage analytics (kb_usage.py)
- Change detection (kb_changes.py)
- Enhanced CLI with 6 new commands

Phase 2: Enhanced Features
- Freshness checking (kb_freshness.py)
- Git integration (kb_git.py)
- Automated scripts (daily/weekly)

Phase 3: Advanced Analytics
- Version monitoring (kb_versions.py)
- Community analytics (kb_community.py)
- Predictive analytics (kb_predictive.py)
- Pattern recognition (kb_patterns.py)
- Monthly community aggregation

Documentation:
- Complete metadata system docs
- Quality standards (100-point rubric)
- Agent skills and workflows
- Deployment guide

Features:
- Track entry quality (0-100 scale)
- Monitor library versions automatically
- Predict which entries need updates
- Find similar patterns across projects
- Aggregate analytics across community
- Privacy-first design (SHA256 anonymization)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Push to GitHub
git push origin main
```

---

## 2. Updating Existing Projects

### For Projects Using Shared KB

When users update their Shared KB submodule, they should:

1. **Update the submodule:**
   ```bash
   cd /path/to/project
   git submodule update --remote docs/knowledge-base/shared
   # Or if not using submodule:
   cd docs/knowledge-base/shared
   git pull origin main
   ```

2. **Read the updated documentation:**
   - `FOR_CLAUDE_CODE.md` - Updated guide
   - `PHASE3_SUMMARY.md` - Phase 3 details
   - `METADATA_ARCHITECTURE.md` - Metadata system

3. **Initialize metadata (first time only):**
   ```bash
   cd docs/knowledge-base/shared
   python tools/kb.py init-metadata --verbose
   ```

4. **Schedule automated scripts (optional):**
   ```bash
   # Add to crontab or Task Scheduler
   # Daily: scripts/daily_freshness.py
   # Weekly: scripts/weekly_usage.py --days 7
   # Monthly: scripts/monthly_community.py
   ```

5. **Test new features:**
   ```bash
   # Check library versions
   python -m tools.kb_versions check --library fastapi

   # Generate predictions
   python -m tools.kb_predictive report

   # Find similar patterns
   python -m tools.kb_patterns report
   ```

### Update Notification Template

Send this message to users/projects:

```
📚 Shared Knowledge Base updated to v5.1!

New capabilities:
- ✅ Metadata management (quality scores, usage tracking)
- ✅ Freshness checking (library version monitoring)
- ✅ Predictive analytics (update predictions, risk assessment)
- ✅ Pattern recognition (find similar patterns)
- ✅ Community analytics (aggregate data across projects)

Update instructions:
1. git pull origin main (in shared-knowledge-base)
2. Read FOR_CLAUDE_CODE.md (updated guide)
3. Run: python tools/kb.py init-metadata
4. Schedule automated scripts (optional)

Documentation:
- FOR_CLAUDE_CODE.md - Complete guide
- PHASE3_SUMMARY.md - Phase 3 details
- METADATA_ARCHITECTURE.md - System design

Breaking changes: None (backward compatible)
Estimated setup time: 10-15 minutes
```

---

## 3. File Structure Verification

### After Deployment, Verify This Structure:

```
shared-knowledge-base/
├── tools/                          # ✓ Should exist
│   ├── kb.py                      # ✓ Modified
│   ├── kb_config.py               # ✓ Existing
│   ├── kb_meta.py                 # ✓ NEW (Phase 1)
│   ├── kb_usage.py                # ✓ NEW (Phase 1)
│   ├── kb_changes.py              # ✓ NEW (Phase 1)
│   ├── kb_freshness.py            # ✓ NEW (Phase 2)
│   ├── kb_git.py                  # ✓ NEW (Phase 2)
│   ├── kb_versions.py             # ✓ NEW (Phase 3)
│   ├── kb_community.py            # ✓ NEW (Phase 3)
│   ├── kb_predictive.py           # ✓ NEW (Phase 3)
│   └── kb_patterns.py             # ✓ NEW (Phase 3)
├── scripts/                        # ✓ Should exist (NEW)
│   ├── init_metadata.py
│   ├── daily_freshness.py
│   ├── weekly_usage.py
│   └── monthly_community.py
├── .cache/                         # ✗ Should be ignored (local only)
├── _index.yaml                     # ✗ Should be ignored (auto-generated)
├── .gitignore                      # ✓ Modified
├── AGENT.md                        # ✓ NEW
├── SKILLS.md                       # ✓ NEW
├── WORKFLOWS.md                    # ✓ NEW
├── QUALITY_STANDARDS.md            # ✓ NEW
├── PROMPTS.md                      # ✓ NEW
├── METADATA_ARCHITECTURE.md        # ✓ NEW
├── METADATA_SKILLS.md              # ✓ NEW
├── IMPLEMENTATION_GUIDE.md         # ✓ NEW
├── METADATA_SUMMARY.md             # ✓ NEW
├── PHASE3_SUMMARY.md               # ✓ NEW
├── FOR_CLAUDE_CODE.md              # ✓ Modified
├── README.md                       # ✓ Modified
├── CLAUDE.md                       # ✓ NEW
├── CURATOR_DOCS_INDEX.md           # ✓ NEW
└── README_CURATOR.md               # ✓ NEW
```

**Legend:**
- ✓ Should be committed to git
- ✗ Should NOT be committed to git

---

## 4. Testing After Deployment

### Basic Functionality Tests

```bash
cd T:\Code\shared-knowledge-base

# Test 1: Basic search
python tools/kb.py search "websocket"

# Test 2: Metadata initialization
python tools/kb.py init-metadata --verbose

# Test 3: Version check
python -m tools.kb_versions check --library fastapi

# Test 4: Predictive analytics
python -m tools.kb_predictive report

# Test 5: Pattern recognition
python -m tools.kb_patterns report
```

### Expected Results

✅ All commands should execute without errors
✅ Metadata files should be created
✅ Reports should be generated
✅ No import errors

---

## 5. Rollback Plan (If Needed)

If something goes wrong:

```bash
# Revert to previous commit
git revert HEAD

# Or reset to specific commit
git reset --hard <commit-hash>

# Push rollback
git push origin main --force
```

---

## 6. Maintenance

### Regular Tasks

**Daily (Automated):**
- Freshness checks (`scripts/daily_freshness.py`)

**Weekly (Automated):**
- Usage analysis (`scripts/weekly_usage.py`)

**Monthly (Automated):**
- Community aggregation (`scripts/monthly_community.py`)

**Quarterly (Manual):**
- Review quality scores
- Update low-quality entries
- Review universal pattern candidates

**As Needed:**
- Add new entries (with metadata)
- Update library versions
- Review and merge duplicate patterns

---

## 7. Support

### Documentation

- `FOR_CLAUDE_CODE.md` - Main guide for Claude Code
- `AGENT.md` - Curator role definition
- `SKILLS.md` - All available skills
- `WORKFLOWS.md` - Step-by-step procedures
- `METADATA_ARCHITECTURE.md` - System architecture
- `PHASE3_SUMMARY.md` - Phase 3 implementation

### Troubleshooting

See `FOR_CLAUDE_CODE.md` → "Troubleshooting" section

### Issues

Report issues at: https://github.com/ozand/shared-knowledge-base/issues

---

**Deployment Version:** 3.0
**Date:** 2026-01-05
**Status:** Ready for Deployment ✅
