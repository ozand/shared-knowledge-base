# Claude Code Organization Improvement Plan

**Repository:** shared-knowledge-base
**Created:** 2026-01-07
**Status:** In Progress

---

## Executive Summary

This plan implements best practices for `.claude/` organization based on pattern `CLAUDE-CODE-FILES-ORGANIZATION-001`.

**Current Issues:**
- CLAUDE.md oversized (412 lines, target: ~300)
- 3 temporary files in root directory
- Missing standards/ and references/ directories
- 3 oversized commands (kb-query: 391, kb-sync: 367, retrospective: 319)

**Impact:** Token efficiency -30%, discoverability issues, maintenance overhead

---

## Implementation Phases

### Phase 1: Structure Cleanup (15 min)
**Goal:** Remove clutter, add missing directories

**Tasks:**
1. ✅ Analyze current structure
2. Move temporary files to `docs/research/claude-code/archive/`
3. Create `standards/` directory structure
4. Create `references/` directory structure
5. Add `.gitkeep` to maintain empty directories

**Files to move:**
```
.claude/IMPLEMENTATION-SUMMARY.md → docs/research/claude-code/archive/claude-implementation-summary.md
.claude/FINAL-IMPLEMENTATION-AND-FIX-REPORT.md → docs/research/claude-code/archive/
.claude/AUTONOMOUS-AGENT-SYSTEM.md → docs/research/claude-code/archive/
```

**New directories:**
```
.claude/
├── standards/          # Team standards and conventions
│   ├── git-workflow.md
│   ├── yaml-standards.md
│   └── quality-gates.md
├── references/         # Reference documentation
    ├── cli-reference.md
    └── api-reference.md
```

**Success criteria:**
- Root directory contains only: CLAUDE.md, settings.json
- standards/ and references/ created
- No temporary files in root

---

### Phase 2: CLAUDE.md Optimization (30 min)
**Goal:** Apply progressive disclosure, reduce to ~300 lines

**Current:** 412 lines
**Target:** ~300 lines (-27%)

**Strategy:**
1. Keep overview and quick start (always loaded)
2. Move detailed content to references/
3. Add links to detailed content
4. Maintain hierarchical structure

**Content to move:**
```yaml
Move to references/cli-reference.md:
  - Complete command reference (all kb.py commands)
  - Metadata commands (init, detect, check, analyze, update, reindex)

Move to references/architecture.md:
  - Detailed directory structure
  - Hierarchical knowledge organization

Move to references/workflows.md:
  - Critical workflows (error reporting, scope decisions)

Keep in CLAUDE.md:
  - Overview (brief)
  - Quick start (essential commands only)
  - Brief architecture overview
  - Links to detailed content
```

**New CLAUDE.md structure:**
```markdown
# Shared Knowledge Base - Claude Code Instructions

## Overview (5 lines)
## Quick Start (20 lines) - Essential commands only
## Brief Architecture (30 lines) - High-level structure
## Documentation Links (10 lines)
  - CLI Reference: @references/cli-reference.md
  - Architecture: @references/architecture.md
  - Workflows: @references/workflows.md
## Quick Reference (50 lines) - Common patterns
## Agent Configuration (20 lines)

Total: ~250-300 lines
```

**Success criteria:**
- CLAUDE.md < 300 lines
- All detailed content accessible via links
- No information loss
- Progressive disclosure applied

---

### Phase 3: Skills Optimization (1 hour)
**Goal:** Apply progressive disclosure to oversized skills

**Current analysis:**
```
✅ kb-search/SKILL.md: 121 lines (optimal)
✅ kb-validate/SKILL.md: 187 lines (optimal)
✅ kb-index/SKILL.md: 267 lines (acceptable)
⚠️  kb-create/SKILL.md: 314 lines (borderline, optimize to 250)
⚠️  audit-quality/SKILL.md: 340 lines (borderline, optimize to 280)
⚠️  find-duplicates/SKILL.md: 353 lines (borderline, optimize to 290)
⚠️  research-enhance/SKILL.md: 411 lines (oversized, optimize to 350)
```

**Optimization strategy:**
1. Add YAML frontmatter (if missing)
2. Move detailed examples to resources/
3. Keep core logic in SKILL.md
4. Add links to detailed resources

**Example: research-enhance/SKILL.md (411 → 350 lines)**
```yaml
---
name: "research-enhance"
description: "Enhance KB entries with research and cross-references"
version: "1.0"
---

# Research Enhancement Skill

## Overview (5 lines)
## Quick Start (10 lines)
## Core Workflow (100 lines)
## Examples (20 lines)
→ See: resources/complex-research-example.md
## Testing (15 lines)

Total: ~150 lines in SKILL.md
Detailed content: resources/research-patterns.md (200+ lines)
```

**Tasks:**
1. Add YAML frontmatter to all skills
2. Create resources/ subdirectories for oversized skills
3. Move detailed examples to resources/
4. Add progressive disclosure links
5. Test each skill after optimization

**Success criteria:**
- All SKILL.md files < 350 lines
- All skills have YAML frontmatter
- resources/ directories created where needed
- Skills tested and functional

---

### Phase 4: Commands Optimization (45 min)
**Goal:** Reduce oversized commands to 50-200 lines

**Current analysis:**
```
✅ kb-search.md: 107 lines (optimal)
✅ kb-validate.md: 155 lines (optimal)
⚠️  kb-create.md: 202 lines (borderline, optimize to 180)
⚠️  kb-index.md: 249 lines (oversized, optimize to 180)
❌ retrospective.md: 319 lines (oversized, optimize to 150)
❌ kb-sync.md: 367 lines (oversized, optimize to 180)
❌ kb-query.md: 391 lines (oversized, optimize to 200)
```

**Optimization strategy:**
1. Simplify prompt templates
2. Move examples to references/
3. Focus on core workflow
4. Add links to detailed guides

**Example: kb-query.md (391 → 200 lines)**
```markdown
# kb-query: Advanced Knowledge Base Query

## Purpose (5 lines)
## Usage (10 lines)
## Quick Example (20 lines)
→ See: @references/kb-query-examples.md for advanced patterns
## Parameters (30 lines)
## Workflow (50 lines)

Total: ~115 lines
Detailed examples: references/kb-query-examples.md
```

**Tasks:**
1. Analyze each oversized command
2. Extract detailed examples
3. Simplify prompt templates
4. Create reference documentation
5. Test commands after optimization

**Success criteria:**
- All commands < 200 lines
- Detailed examples in references/
- Commands tested and functional
- No functionality loss

---

### Phase 5: Standards Creation (30 min)
**Goal:** Create team standards in standards/ directory

**Standards to create:**

1. **standards/git-workflow.md** (100 lines)
   ```yaml
   - Commit message conventions
   - Branch naming patterns
   - Pull request requirements
   - GITHUB-ATTRIB-001 pattern
   ```

2. **standards/yaml-standards.md** (150 lines)
   ```yaml
   - YAML syntax requirements
   - KB entry structure
   - Validation rules
   - Quality gates (75/100 minimum)
   ```

3. **standards/quality-gates.md** (100 lines)
   ```yaml
   - Quality scoring rubric
   - Entry validation checklist
   - Testing requirements
   - Metadata standards
   ```

**Success criteria:**
- 3 standards documents created
- Each < 200 lines
- Referenced from CLAUDE.md
- Referenced from relevant skills/commands

---

### Phase 6: References Creation (30 min)
**Goal:** Create reference documentation in references/ directory

**References to create:**

1. **references/cli-reference.md** (200 lines)
   ```yaml
   - All kb.py commands (index, search, stats, validate)
   - Metadata commands (init, detect, check, analyze, update)
   - Version monitoring commands
   - Predictive analytics commands
   - Usage examples for each command
   ```

2. **references/architecture.md** (150 lines)
   ```yaml
   - Hierarchical knowledge organization
   - Directory structure details
   - Scope system (universal → project)
   - Metadata architecture
   - Search technology (SQLite FTS5)
   ```

3. **references/workflows.md** (200 lines)
   ```yaml
   - Error reporting workflow
   - Scope decision criteria
   - Commit & push workflow
   - Validation workflow
   - Quality validation process
   ```

4. **references/kb-query-examples.md** (150 lines)
   ```yaml
   - Simple queries
   - Complex filters
   - Category-based search
   - Tag-based search
   - Advanced patterns
   ```

**Success criteria:**
- 4 reference documents created
- Each < 250 lines
- Linked from CLAUDE.md
- Linked from relevant commands

---

### Phase 7: Validation & Testing (30 min)
**Goal:** Validate all changes, test functionality

**Validation checklist:**
```yaml
Structure:
  - [ ] Root .claude/ contains only CLAUDE.md and settings.json
  - [ ] standards/ directory exists with 3 files
  - [ ] references/ directory exists with 4 files
  - [ ] No temporary files in root

CLAUDE.md:
  - [ ] File size < 300 lines
  - [ ] All links valid
  - [ ] Progressive disclosure applied
  - [ ] No information loss

Skills:
  - [ ] All SKILL.md < 350 lines
  - [ ] All have YAML frontmatter
  - [ ] All resources/ created where needed
  - [ ] All skills tested and functional

Commands:
  - [ ] All commands < 200 lines
  - [ ] All tested and functional
  - [ ] Examples in references/

Standards:
  - [ ] All standards < 200 lines
  - [ ] Referenced from CLAUDE.md
  - [ ] Content accurate and complete

References:
  - [ ] All references < 250 lines
  - [ ] All links valid
  - [ ] Content accurate and complete
```

**Testing:**
```bash
# Test KB operations
python tools/kb.py stats
python tools/kb.py search "test"
python tools/kb.py validate .

# Test skills (manually)
# Test commands (manually)
# Test hooks (manually)

# Verify no broken links
grep -r "@references/" .claude/ | grep -v "Binary"
```

**Success criteria:**
- All validation checks pass
- All functionality tested
- No broken links
- No regressions

---

## Timeline Summary

| Phase | Duration | Tasks | Value |
|-------|----------|-------|-------|
| Phase 1: Structure Cleanup | 15 min | 5 tasks | Remove clutter |
| Phase 2: CLAUDE.md Optimization | 30 min | 4 tasks | Token efficiency +27% |
| Phase 3: Skills Optimization | 1 hour | 5 tasks | Improved discoverability |
| Phase 4: Commands Optimization | 45 min | 5 tasks | Better usability |
| Phase 5: Standards Creation | 30 min | 3 tasks | Team alignment |
| Phase 6: References Creation | 30 min | 4 tasks | Better navigation |
| Phase 7: Validation & Testing | 30 min | 2 tasks | Quality assurance |

**Total Time:** ~4 hours

---

## Expected Outcomes

**Quantitative:**
- CLAUDE.md: 412 → ~300 lines (-27%)
- Commands avg: 391 → ~150 lines (-62%)
- Token efficiency: +30%
- Discoverability: 95% find content in <30s

**Qualitative:**
- Progressive disclosure applied throughout
- Single source of truth for standards
- Clear separation of concerns
- Better maintainability
- Improved onboarding for new users

---

## Risk Mitigation

**Risk 1: Breaking links during refactoring**
- **Mitigation:** Use search to find all references before moving
- **Validation:** Test all links after each phase

**Risk 2: Information loss during optimization**
- **Mitigation:** Move content, don't delete
- **Validation:** Compare line counts, verify content exists

**Risk 3: Functionality regression**
- **Mitigation:** Test after each phase
- **Validation:** Comprehensive test suite in Phase 7

---

## Rollback Plan

If critical issues arise:
1. Stop current phase
2. Git revert changes for that phase
3. Fix issues in pattern document
4. Resume from last successful phase

```bash
# Rollback specific phase
git revert HEAD --no-edit
git push origin main
```

---

## Next Steps

1. ✅ Review and approve this plan
2. ⏳ Execute Phase 1: Structure Cleanup
3. ⏳ Execute Phase 2-7 sequentially
4. ⏳ Final validation and testing

---

**Status:** Ready for execution
**Last Updated:** 2026-01-07
