# Shared Knowledge Base Integration Guide

**Version 3.0 - Updated with Clean Structure**

For agents integrating Shared Knowledge Base into new projects or handling major version updates.

---

## 🎯 Two Main Scenarios

### Scenario 1: New Project Integration
**When:** Starting a new project that wants to use Shared Knowledge Base

### Scenario 2: Major Architecture Updates
**When:** Shared KB has breaking changes (e.g., v2 → v3 migration)

---

## 📖 Scenario 1: New Project Integration

### Quick Reference for Agents

**Integration Document:** [for-claude-code/README.md](for-claude-code/README.md)

**Old location (before clean structure):** `FOR_CLAUDE_CODE.md` (root)

**New location (after clean structure):** `for-claude-code/README.md`

### Step-by-Step Integration

#### For the Integration Agent (in NEW project)

**Step 1: Reference the Integration Guide**

```bash
# In your new project, read this FIRST:
curl -o /tmp/kb-integration.md \
  https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-claude-code/README.md

# Or access via GitHub web UI:
# https://github.com/ozand/shared-knowledge-base/blob/main/for-claude-code/README.md
```

**What this file contains:**
- Complete integration workflow
- Directory structure setup
- Configuration examples
- Usage patterns for Claude Code
- AI-agnostic integration (Copilot, Cursor, etc.)

**Step 2: Clone or Add as Submodule**

```bash
# RECOMMENDED: Add as submodule
cd /path/to/your/project
git submodule add https://github.com/ozand/shared-knowledge-base.git \
  docs/knowledge-base/shared

# OR for quick testing: Clone directly
git clone https://github.com/ozand/shared-knowledge-base.git \
  docs/knowledge-base/shared
```

**Step 3: Copy kb.py Tool**

```bash
# Copy tool to project location
cp docs/knowledge-base/shared/tools/kb.py \
  docs/knowledge-base/tools/kb.py

# Make executable (Unix/Mac)
chmod +x docs/knowledge-base/tools/kb.py
```

**Step 4: Install Dependencies**

```bash
pip install pyyaml
```

**Step 5: Initialize Knowledge Base**

```bash
# Build search index
python docs/knowledge-base/tools/kb.py index -v

# Test search
python docs/knowledge-base/tools/kb.py search "async"
```

**Step 6: Create Project-Specific KB (Optional)**

```bash
# Create local KB entries (project scope)
# Example: docs/knowledge-base/project/errors/my-project-error.yaml
```

---

## 🔄 Scenario 2: Major Architecture Updates

### Example: v2 → v3 Migration

**Background:**
- Shared KB v3.0 introduced major changes (metadata system, clean structure)
- Existing projects using v2 need to update
- Breaking changes affect directory structure, tools, workflows

### For the Project Agent (in EXISTING project)

**Step 1: Check Current Version**

```bash
cd docs/knowledge-base/shared
git tag --contains HEAD
# Shows: v2.0, v2.1, etc.

# Check available updates
git fetch origin
git log HEAD..origin/main --oneline
# See what's new
```

**Step 2: Review Breaking Changes**

```bash
# Read migration guide
cat FOR_MIGRATION.md  # If exists
# Or check GitHub Releases
gh release view v3.0

# Check clean structure changes
cat CLEAN_STRUCTURE_PROPOSAL.md
```

**Step 3: Update Submodule**

```bash
# Option A: Update to latest
git submodule update --remote --merge docs/knowledge-base/shared

# Option B: Update to specific version
cd docs/knowledge-base/shared
git checkout v3.0
cd ../..
git add docs/knowledge-base/shared
git commit -m "Update Shared KB to v3.0"
```

**Step 4: Handle Breaking Changes**

**Directory Structure Changes:**
```diff
- FOR_CLAUDE_CODE.md (root)
+ for-claude-code/README.md

- CURATOR_DOCS_INDEX.md (root)
+ curator/INDEX.md

- AGENT.md (root)
+ curator/AGENT.md
```

**What to do:**
1. Update any hardcoded references in your project
2. Update documentation links
3. Re-run initialization scripts

**New Tools in v3.0:**
```bash
# v2 had: kb.py (basic)
# v3 added: kb_meta.py, kb_usage.py, kb_freshness.py, etc.

# Update your integration if using advanced features:
python -m tools.kb_meta init-all
python -m tools.kb_freshness check-all
```

**Step 5: Re-initialize**

```bash
# Rebuild index with new structure
python docs/knowledge-base/tools/kb.py index --force -v

# Initialize metadata (v3.0 feature)
python docs/knowledge-base/shared/scripts/init_metadata.py
```

**Step 6: Test Integration**

```bash
# Search should still work
python docs/knowledge-base/tools/kb.py search "async"

# New v3.0 features
python docs/knowledge-base/tools/kb.py stats
python docs/knowledge-base/tools/kb.py check-freshness
```

**Step 7: Handle Customizations**

If you have project-specific KB entries:

```yaml
# Before (v2):
version: "1.0"
category: "project"
# ... rest of entry

# After (v3) - add metadata:
version: "1.0"
category: "project"
local_only: true  # Don't sync to shared KB
# ... rest of entry
```

---

## 🤝 Agent Handoff Workflow

### Role Clarification

**Project Agents** (in projects USING Shared KB):
- Integrate Shared KB into project
- Use Shared KB for error solving
- **NOT responsible for maintaining Shared KB itself**
- Report issues to Shared KB repository

**Shared KB Curator Agent** (in shared-knowledge-base project):
- Maintains Shared KB repository
- Fixes reported issues
- Validates entries
- Manages metadata
- Handles migrations

### Issue Reporting Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                     PROJECT AGENT                                │
│                  (in your-app project)                          │
│                                                                  │
│  1. Working on project task                                     │
│  2. Encounters error or improvement opportunity                │
│  3. Searches Shared KB: kb search "error"                      │
│  4. If NOT found → Solves problem                              │
│  5. Determines: "Is this reusable pattern?"                    │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ IF YES (reusable pattern):                            │     │
│  │   → Create YAML entry                                 │     │
│  │   → Validate: kb validate entry.yaml                  │     │
│  │   → Create GitHub issue in Shared KB repo             │     │
│  │   → Include: error details, fix, validation result    │     │
│  │   → Assign labels: kb-improvement, bug, enhancement   │     │
│  │   → DONE (curator will handle it)                     │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ IF NO (project-specific):                             │     │
│  │   → Add to project's local KB                         │     │
│  │   → Mark: local_only: true                           │     │
│  │   → DONE                                              │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ GitHub Issue
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│              SHARED KB CURATOR AGENT                             │
│             (in shared-knowledge-base project)                  │
│                                                                  │
│  1. Monitors GitHub issues (daily/weekly)                      │
│  2. Sees new issue from project agent                           │
│  3. Triage: priority, scope, effort                             │
│  4. Reviews YAML entry provided by agent                       │
│  5. Edits/validates if needed                                   │
│  6. Moves to appropriate directory                             │
│  7. Commits to shared-knowledge-base repo                       │
│  8. Comments on issue: "Merged, available in v3.0.1"          │
│  9. Closes issue                                                │
│                                                                  │
│  Result: Improvement available to ALL projects using Shared KB  │
└─────────────────────────────────────────────────────────────────┘
```

### Example: Issue Creation

**Project Agent (in my-app project):**

```bash
# 1. Found error pattern in PostgreSQL
cd docs/knowledge-base/shared

# 2. Created YAML entry: postgresql/errors/deadlock-detection.yaml

# 3. Validated
python tools/kb.py validate postgresql/errors/deadlock-detection.yaml
# ✓ Validation passed

# 4. Create GitHub issue
gh issue create \
  --repo ozand/shared-knowledge-base \
  --title "Add POSTGRES-001: Deadlock Detection Pattern" \
  --label "kb-improvement,enhancement,postgresql" \
  --body "## Proposed Entry

**File:** postgresql/errors/deadlock-detection.yaml

**Pattern:** Deadlock detection and prevention in PostgreSQL

**Validation:** ✓ Passed

**Real-world example:** Encountered in my-app project, solved by...

**Benefit:** Reusable across all projects using PostgreSQL

**Suggested scope:** postgresql

**Curator action:** Please review and merge to shared KB.

---

Created by: Project Agent (my-app)
Date: 2026-01-06"
```

**Shared KB Curator Agent (in shared-knowledge-base):**

```bash
# 1. See issue notification

# 2. Review the entry
cat postgresql/errors/deadlock-detection.yaml

# 3. Enhance if needed
# - Add missing fields
# - Improve code examples
# - Add references

# 4. Re-validate
python tools/kb.py validate postgresql/errors/deadlock-detection.yaml

# 5. Commit
git add postgresql/errors/deadlock-detection.yaml
git commit -m "Add POSTGRES-001: Deadlock Detection Pattern

Contributed by: my-app project
Reviewed by: KB Curator
Validated: ✓

Pattern: Detect and prevent PostgreSQL deadlocks
Real-world: Production issue in my-app"

# 6. Push
git push origin main

# 7. Comment and close issue
gh issue comment <issue-number> \
  --body "✅ Merged to main!

Available in: postgresql/errors/deadlock-detection.yaml
Validation: ✓ Passed
Next KB version: v3.0.1

Thank you for the contribution!"

gh issue close <issue-number>
```

---

## 📁 File Location Reference (Post Clean Structure)

### For New Project Integration

**Read this first:**
```
for-claude-code/README.md
```

**Old vs New locations:**

| Old Location (before clean structure) | New Location (after clean structure) |
|---------------------------------------|--------------------------------------|
| `FOR_CLAUDE_CODE.md` | `for-claude-code/README.md` |
| `CLAUDE.md` | `for-claude-code/CLAUDE.md` |
| `CURATOR_DOCS_INDEX.md` | `curator/INDEX.md` |
| `README_CURATOR.md` | `curator/README.md` |
| `AGENT.md` | `curator/AGENT.md` |
| `SKILLS.md` | `curator/SKILLS.md` |
| `WORKFLOWS.md` | `curator/WORKFLOWS.md` |
| `QUALITY_STANDARDS.md` | `curator/QUALITY_STANDARDS.md` |
| `PROMPTS.md` | `curator/PROMPTS.md` |
| `DEPLOYMENT_GUIDE.md` | `curator/DEPLOYMENT.md` |
| `METADATA_ARCHITECTURE.md` | `curator/metadata/ARCHITECTURE.md` |
| `METADATA_SKILLS.md` | `curator/metadata/SKILLS.md` |
| `METADATA_SUMMARY.md` | `curator/metadata/SUMMARY.md` |
| `IMPLEMENTATION_GUIDE.md` | `curator/metadata/IMPLEMENTATION.md` |
| `PHASE3_SUMMARY.md` | `curator/metadata/PHASE3.md` |

**Unchanged (still in root):**
- `README.md`
- `LICENSE`
- `GUIDE.md`
- `QUICKSTART.md`
- `SUBMODULE_VS_CLONE.md`

---

## 🔄 Version Update Detection

### For Project Agents

**Check for Updates:**

```bash
# In your project
cd docs/knowledge-base/shared

# See current version
git describe --tags

# Check for new commits
git fetch origin
git log HEAD..origin/main --oneline

# Check GitHub Releases
gh release list --limit 5
```

**Major Version Change Detected:**

```bash
# Example: See v3.0 announcement
gh release view v3.0

# Read breaking changes
# Look for:
# - "BREAKING CHANGE:" in commit messages
# - Migration guides
# - Directory structure changes

# Update following Scenario 2 above
```

---

## 📋 Integration Checklist

### New Project Integration

- [ ] Read `for-claude-code/README.md`
- [ ] Clone or add as submodule
- [ ] Copy kb.py to project
- [ ] Install dependencies (pyyaml)
- [ ] Initialize: `kb.py index -v`
- [ ] Test search: `kb.py search "test"`
- [ ] Create project-specific KB (if needed)
- [ ] Document integration in project README

### Major Version Update

- [ ] Check current version: `git describe --tags`
- [ ] Read release notes: `gh release view vX.Y.Z`
- [ ] Review breaking changes
- [ ] Update submodule: `git submodule update --remote`
- [ ] Update file references (if structure changed)
- [ ] Re-initialize: `kb.py index --force -v`
- [ ] Test all KB commands
- [ ] Update project documentation
- [ ] Test search functionality
- [ ] Verify metadata (v3.0+)

### Issue Reporting (Project Agent)

- [ ] Search KB first
- [ ] Determine if reusable
- [ ] Create YAML entry
- [ ] Validate: `kb.py validate`
- [ ] Create GitHub issue with full details
- [ ] Add appropriate labels
- [ ] Wait for curator to merge

---

## 🎓 Summary

### For New Projects

**One-time setup:**
```bash
git submodule add https://github.com/ozand/shared-knowledge-base.git \
  docs/knowledge-base/shared
cp docs/knowledge-base/shared/tools/kb.py docs/knowledge-base/tools/
pip install pyyaml
python docs/knowledge-base/tools/kb.py index -v
```

**Reference:** `for-claude-code/README.md`

### For Version Updates

**Detect:**
```bash
cd docs/knowledge-base/shared
git fetch origin
git log HEAD..origin/main --oneline
```

**Update:**
```bash
git submodule update --remote --merge
python docs/knowledge-base/tools/kb.py index --force -v
```

### For Issue Reporting

**Project Agent:**
- Find improvement → Create YAML → Validate → Create GitHub issue

**Shared KB Curator:**
- Review issue → Enhance entry → Commit → Close issue

---

## 📖 Documentation Index

**For Integration:**
- [for-claude-code/README.md](for-claude-code/README.md) - Main integration guide
- [for-claude-code/CLAUDE.md](for-claude-code/CLAUDE.md) - Agent instructions

**For Curators:**
- [curator/INDEX.md](curator/INDEX.md) - Curator documentation index
- [curator/AGENT.md](curator/AGENT.md) - Curator role

**For Users:**
- [README.md](README.md) - Project overview
- [GUIDE.md](GUIDE.md) - User guide
- [QUICKSTART.md](QUICKSTART.md) - 5-minute setup

**For Deployment:**
- [SUBMODULE_VS_CLONE.md](SUBMODULE_VS_CLONE.md) - Deployment decision
- [CLEAN_STRUCTURE_PROPOSAL.md](CLEAN_STRUCTURE_PROPOSAL.md) - Architecture decisions

---

**Last Updated:** 2026-01-06
**Version:** 3.0 (Clean Structure)
