# Legacy Cleanup - Quick Reference Guide

**Analysis Date:** 2026-01-08
**Analyst:** Agent 4 (Legacy & Migration Analyst)

---

## TL;DR - What to Do

**Delete 97 files, Keep 30 files** → 93% line reduction, 75% space savings

---

## Phase 1: Quick Wins (2 hours) - DO THIS FIRST

### Delete These Entire Directories:

```bash
cd T:\Code\shared-knowledge-base

# 1. Legacy skills (35 files) - Replaced by tools/kb.py
rm -rf .legacy/.claude/skills/

# 2. Legacy agents (8 files) - Replaced by agents/curator/
rm -rf .legacy/.claude/agents/

# 3. Command aliases (11 files) - Use tools/kb.py directly
rm -rf .legacy/.claude/commands/

# 4. Legacy hooks (4 files) - Superseded by v5.1
rm -rf .legacy/.claude/hooks/

# 5. Migration tools (2 files) - One-time scripts, complete
rm -rf .legacy/tools/

# 6. Example projects (2 files) - Not needed
rm -rf .legacy/examples/

# 7. Obsolete schema (1 file) - Superseded by v4.0.0
rm .legacy/docs/schemas/YAML-SCHEMA-V3.1.md
```

### Delete Already-Migrated Claude Code Docs:

```bash
cd .legacy/docs/research/claude-code

# All 26 files already migrated to claude-code/ domain
# Keep 3 to extract, delete rest:
rm -f claude-agents-examples.md
rm -f claude-agents-guide.md
rm -f claude-claude-md-guide.md
rm -f CLAUDE-COMPLETE-PRACTICES-EN.md
rm -f claude-complete-practices.md
rm -f CLAUDE-COMPLETE-PRACTICES.md.backup
rm -f claude-hooks-advanced.md
rm -f claude-hooks-examples.md
rm -f claude-hooks-guide.md
rm -f claude-mcp-guide.md
rm -f CLAUDE-PERMISSION-MODES-GUIDE-EN.md
rm -f claude-permission-modes-guide.md
rm -f claude-planning-workflow-guide.md
rm -f claude-projects-collaboration-guide.md
rm -f claude-referencing-context-guide.md
rm -f CLAUDE-SLASH-COMMANDS-GUIDE-EN.md
rm -f claude-slash-commands-guide.md
rm -f claude-shared-architecture.md
rm -f claude-skills-examples.md
rm -f claude-skills-guide.md
rm -f claude-templates.md
rm -f claude-troubleshooting-resume-lock-error.md
rm -f INDEX.md
rm -f README.md
rm -rf issues/
```

### Delete Obsolete Research Analysis:

```bash
cd .legacy/docs/research

# Delete historical session analyses
rm -f AGENT-INFORMATION-FLOW-ANALYSIS.md
rm -f AGENT-INFORMATION-FLOW-IMPLEMENTATION.md
rm -f AGENT-INFORMATION-FLOW-PHASE2.md
rm -f ARCHITECTURE-ANALYSIS.md
rm -f CHAT_SESSION_ANALYSIS_2026-01-06.md
rm -f COMPLETE-SESSION-ANALYSIS.md
rm -f PLAIN_CLONE_PROJECT_ANALYSIS.md
rm -f PROJECT_AGENT_ROLE_CONFUSION_ANALYSIS.md
rm -f REORGANIZATION-COMPLETE.md
rm -f REPOSITORY_STATE_ANALYSIS.md
rm -f SESSION-ANALYSIS-2026-01-07.md
rm -f SESSION-COMPLETE.md
rm -f claude-code/archive/claude-autonomous-agent-system.md
rm -f claude-code/archive/claude-final-implementation-report.md
rm -f claude-code/archive/claude-implementation-summary.md
```

**Result:** ~82 files deleted, ~1.5MB freed, 2 hours work

---

## Phase 2: Extract & Delete (4 hours) - MEDIUM PRIORITY

### Extract These Files First (Check for Unique Patterns):

**Priority 1 - Critical:**
```bash
# 1. KB create workflow patterns
.legacy/.claude/skills/kb-create/SKILL.md
# Check for unique workflows not in tools/kb.py

# 2. Progressive disclosure pattern
.legacy/.claude/skills/claude-code-architecture/resources/progressive-disclosure.md
# Check if in claude-code domain or universal/patterns/

# 3. Hook system patterns
.legacy/.claude/skills/claude-code-architecture/resources/hook-system.md
# Check for unique hook patterns
```

**Priority 2 - High Value:**
```bash
# 4. Claude Code agent mistakes (valuable lessons)
.legacy/docs/research/CLAUDE-CODE-AGENT-MISTAKES-ANALYSIS.md
# Extract lessons about Claude Code pattern violations

# 5. Reusable setup guide
.legacy/docs/research/claude-code/REUSABLE-SETUP-GUIDE.md
# Extract unique setup patterns

# 6. Submodule context contamination (unique insights)
.legacy/docs/research/SUBMODULE_CONTEXT_CONTAMINATION_ANALYSIS.md
# Extract lessons learned about submodules
```

**Priority 3 - Medium Value:**
```bash
# 7. 500-line rule pattern
.legacy/.claude/skills/skill-development/resources/500-line-rule.md
# Check if relevant to universal/patterns/

# 8. Unique workflows
.legacy/.claude/references/workflows.md
# Check for workflows not in docs/

# 9. Installation lessons
.legacy/docs/research/claude-code/INSTALLATION-LESSONS.md
# Extract best practices

# 10. Installation analysis
.legacy/docs/research/claude-code/INSTALLATION-ANALYSIS.md
# Extract lessons learned
```

**Process for Each:**
1. Read file thoroughly
2. Search active KB for similar patterns: `python tools/kb.py search "keywords"`
3. If unique → Extract to appropriate location:
   - Universal pattern → `universal/patterns/`
   - Domain-specific → `domains/<domain>/`
   - Documentation → `docs/`
4. If duplicate → Delete immediately
5. Update any references

**Expected Result:** 5-10 files have unique patterns, 5-10 files deletable as-is

---

## Phase 3: Archive Cleanup (1 hour) - LOW PRIORITY

### Organize Remaining Archive Files:

```bash
cd T:\Code\shared-knowledge-base\.legacy

# Create archive structure
mkdir -p archive/implementation
mkdir -p archive/migration
mkdir -p archive/version-history
mkdir -p archive/project-history

# Move implementation history (4 files)
mv docs/implementation/IMPLEMENTATION-SUMMARY.md archive/implementation/
mv docs/implementation/PHASE3-COMPLETION-REPORT.md archive/implementation/
mv docs/implementation/STRUCTURE-ANALYSIS.md archive/implementation/
mv docs/implementation/STRUCTURE-OPTIMIZATION-REPORT.md archive/implementation/

# Move migration history (5 files)
mv docs/analysis/MIGRATION-COMPLETE-REPORT.md archive/migration/
mv docs/analysis/CLAUDE-CODE-DOMAIN-MIGRATION.md archive/migration/
mv docs/analysis/FILE-CLASSIFICATION.md archive/migration/
mv docs/analysis/PROJECT-UPDATE-ISSUES.md archive/migration/
mv docs/analysis/V4.0.1-IMPLEMENTATION-SUMMARY.md archive/migration/

# Move version history (2 files)
mv docs/migrations/UPGRADE-4.0.md archive/version-history/
mv docs/research/FINAL-ARCHITECTURE-REPORT.md archive/version-history/
mv docs/research/FINAL-HARMONIZATION-REPORT.md archive/version-history/

# Move project history (4 files - keep docs/legacy/GUIDE.md for extraction)
mv docs/analysis/ archive/project-history/

# Clean up empty directories
rm -rf docs/implementation/
rm -rf docs/analysis/
rm -rf docs/migrations/
rm -rf docs/research/  # after extraction complete
rm -rf docs/legacy/    # after extraction complete
rm -rf docs/schemas/

# Keep archive README
mv README.md archive/
```

### Create Archive README:

```bash
cat > archive/README.md << 'EOF'
# Legacy Archive

**Archived:** 2026-01-08
**Reason:** Historical reference only
**Status:** Read-only archive

## Contents

### implementation/ (4 files)
Historical implementation tracking and phase completion reports.

### migration/ (5 files)
Migration documentation and structure analysis history.

### version-history/ (3 files)
Version upgrade history and architecture evolution.

### project-history/ (4 files)
Project update issues and file classification history.

## Usage

This archive is preserved for historical reference only.
Do not modify these files.

For current documentation, see:
- Project root: README.md
- Integration: docs/integration/
- Architecture: docs/v5.1/ARD.md
EOF
```

**Result:** Organized archive, 15 files preserved

---

## Phase 4: Split Agent Files (2 hours) - QUALITY IMPROVEMENT

### Split Large Agent Files:

```bash
cd T:\Code\shared-knowledge-base\agents\curator

# 1. Split PROMPTS.md (774 lines)
mkdir -p prompts
# Split into:
# - prompts/analysis-prompts.md
# - prompts/research-prompts.md
# - prompts/creation-prompts.md
# - prompts/review-prompts.md
# - prompts/maintenance-prompts.md

# 2. Split metadata/IMPLEMENTATION.md (1,026 lines)
mkdir -p metadata/implementation
# Split into:
# - metadata/implementation/phases.md
# - metadata/implementation/decisions.md
# - metadata/implementation/challenges.md
# - metadata/implementation/solutions.md

# 3. Split metadata/SKILLS.md (932 lines)
mkdir -p metadata/skills
# Split into:
# - metadata/skills/audit-skills.md
# - metadata/skills/research-skills.md
# - metadata/skills/creation-skills.md
# - metadata/skills/validation-skills.md
```

**Note:** Use manual editing to ensure proper organization and cross-references.

**Result:** Better progressive disclosure, improved navigation

---

## Verification Steps

After each phase, verify:

```bash
# Check remaining files
find .legacy -type f | wc -l  # Should decrease significantly

# Check agents/
find agents -type f | wc -l    # Should increase after splitting

# Verify no broken references
grep -r "TODO" .legacy/         # Should be minimal

# Check git status
git status                      # Review changes before commit
```

---

## Commit Strategy

### After Phase 1 (Quick Wins):
```bash
git add .legacy/
git commit -m "chore: Delete 82 obsolete legacy files

- Remove .claude/skills/ (35 files) - replaced by tools/kb.py
- Remove .claude/agents/ (8 files) - replaced by agents/curator/
- Remove .claude/commands/ (11 files) - use tools/kb.py directly
- Remove .claude/hooks/ (4 files) - superseded by v5.1
- Remove 26 Claude Code docs - already migrated to claude-code/ domain
- Remove 13 research analyses - historical session analyses
- Remove tools/ (2 files) - one-time migration scripts
- Remove examples/ (2 files) - example projects not needed
- Remove docs/schemas/YAML-SCHEMA-V3.1.md - superseded by v4.0.0

Impact: ~82 files deleted, ~1.5MB freed, ~50,000 lines removed

Related: Agent 4 Legacy & Migration Analysis"
```

### After Phase 2 (Extract & Delete):
```bash
git add .legacy/ domains/ universal/patterns/ docs/
git commit -m "chore: Extract valuable patterns from legacy, delete remainder

- Extract X unique patterns from legacy files
- Delete 15 legacy files after extraction
- Update references as needed

See ANALYSIS-AGENT4-SUMMARY.md for extraction details"
```

### After Phase 3 (Archive):
```bash
git add .legacy/
git commit -m "chore: Organize legacy archive

- Create .legacy/archive/ structure
- Move 15 historical files to archive
- Add archive/README.md
- Clean up empty directories

Preserved: implementation history, migration docs, version history"
```

### After Phase 4 (Split Agent Files):
```bash
git add agents/curator/
git commit -m "docs: Split large agent files for better organization

- Split PROMPTS.md into 5 topic-specific files
- Split metadata/IMPLEMENTATION.md into 4 component files
- Split metadata/SKILLS.md into 4 category files
- Update cross-references

Improves progressive disclosure and navigation"
```

---

## Summary

### Before Cleanup:
- `.legacy/`: 2.0MB, 127 files (~70,158 lines)
- `agents/`: 261KB, 14 files

### After Cleanup:
- `.legacy/`: ~500KB, 15 files (~5,158 lines)
- `agents/`: 261KB, 26 files (after splitting)

### Total Impact:
- **Files Deleted:** 97 out of 127 (76%)
- **Lines Removed:** ~65,000 out of 70,158 (93%)
- **Space Freed:** ~1.5MB out of 2.0MB (75%)
- **Time Required:** ~9 hours total
  - Phase 1: 2 hours (quick wins)
  - Phase 2: 4 hours (extraction)
  - Phase 3: 1 hour (archive)
  - Phase 4: 2 hours (splitting)

### Recommendation:
**Start with Phase 1** for immediate token savings (2 hours, 82 files deleted)

---

**See Also:**
- `analysis_agent4_legacy.csv` - Detailed file-by-file analysis
- `ANALYSIS-AGENT4-SUMMARY.md` - Comprehensive analysis report
