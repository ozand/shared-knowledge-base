# Sprint Plan: Repository Optimization Roadmap

**Timeline:** 10 weeks (98 hours total)
**Start Date:** 2026-01-08
**Target Quality:** 98/100 (Excellent)
**Target Token Reduction:** 31% (109,400 tokens)

---

## Sprint Overview

| Sprint | Duration | Focus | Hours | Impact |
|--------|----------|-------|-------|--------|
| **Sprint 0** | 1 day | Critical Fixes | 0.5 | CRITICAL |
| **Sprint 1** | 1 week | Quick Wins | 8 | HIGH |
| **Sprint 2** | 1 week | High Priority | 14 | HIGH |
| **Sprint 3** | 2 weeks | Medium Priority | 30 | MEDIUM |
| **Sprint 4** | 4 weeks | Polish & Excellence | 20 | LOW |
| **Buffer** | 2 weeks | Unplanned work | 25.5 | - |
| **TOTAL** | **10 weeks** | **All phases** | **98** | **MAX** |

---

## Sprint 0: Critical Fixes (Day 1)

**Goal:** Fix all CRITICAL issues
**Duration:** 0.5 hours (27 minutes)
**Priority:** CRITICAL

### Task List

#### Task 0.1: Fix GitHub Actions Syntax (5 min) ⭐ CRITICAL
**Files:**
- `.github/workflows/curator-commands.yml`
- `.github/workflows/enhanced-notification.yml`

**Issue:** `runs-"on"` should be `runs-on` (lines 18, 23 and 23, 174)

**Commands:**
```bash
cd T:\Code\shared-knowledge-base
sed -i 's/runs-"on"/runs-on/g' .github/workflows/curator-commands.yml
sed -i 's/runs-"on"/runs-on/g' .github/workflows/enhanced-notification.yml
```

**Verification:**
```bash
git diff .github/workflows/
```

**Commit:**
```bash
git add .github/workflows/
git commit -m "fix: Correct critical syntax errors in GitHub Actions workflows

- Fix runs-\"on\" typo in curator-commands.yml (lines 18, 23)
- Fix runs-\"on\" typo in enhanced-notification.yml (lines 23, 174)
- Restores CI/CD functionality

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

#### Task 0.2: Fix kb-curator.yaml Metadata (20 min) ⭐ CRITICAL
**File:** `domains/claude-code/agent-instructions/kb-curator.yaml`

**Issue:** Missing `version`, `category`, `last_updated` fields

**Fix:**
```yaml
version: "5.1"
category: "claude-code-agent"
last_updated: "2026-01-08"
```

**Commands:**
```bash
# Edit file
nano domains/claude-code/agent-instructions/kb-curator.yaml

# Validate
python tools/kb.py validate domains/claude-code/agent-instructions/kb-curator.yaml

# Rebuild index
python tools/kb.py index -v
```

**Commit:**
```bash
git add domains/claude-code/agent-instructions/kb-curator.yaml
git commit -m "fix: Add missing metadata to kb-curator.yaml

- Add version: 5.1
- Add category: claude-code-agent
- Add last_updated: 2026-01-08
- Fixes core agent configuration

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

#### Task 0.3: Delete Temporary File (2 min) ⭐ HIGH
**File:** `2026-01-08-caveat-the-messages-below-were-generated-by-the-u.txt`

**Issue:** 2,700-line conversation dump wasting 12,000 tokens

**Command:**
```bash
rm 2026-01-08-caveat-the-messages-below-were-generated-by-the-u.txt
```

**Commit:**
```bash
git add 2026-01-08-caveat-the-messages-below-were-generated-by-the-u.txt
git commit -m "chore: Remove temporary conversation dump file

- Delete 2,700-line temp file (12,000 tokens)
- File was accidentally committed
- Improves repository hygiene

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

### Success Criteria
- [ ] GitHub Actions workflows syntax-correct
- [ ] kb-curator.yaml has all required fields
- [ ] Temporary file deleted
- [ ] All changes committed and pushed
- [ ] Zero breaking changes

**Completion Time:** Day 1 (27 minutes)

---

## Sprint 1: Quick Wins (Week 1)

**Goal:** Execute high-impact, low-effort optimizations
**Duration:** 1 week (8 hours)
**Priority:** HIGH

### Task List

#### Task 1.1: Execute DELETE_DUPLICATES.sh (15 min)
**Script:** `DELETE_DUPLICATES.sh`
**Impact:** Delete 27 duplicate files (10,000 lines)

**Commands:**
```bash
# Dry run first
bash DELETE_DUPLICATES.sh --dry-run

# Execute cleanup
bash DELETE_DUPLICATES.sh

# Verify
git status
git diff --stat
```

**Commit:** Use commit template from script

#### Task 1.2: Delete Migration Scripts (10 min)
**Files:**
- `.legacy/tools/migrate-to-v5.1.sh` (10,715 lines)
- `.legacy/tools/init-kb.sh` (11,868 lines)

**Commands:**
```bash
rm -rf .legacy/tools/
git add .legacy/tools/
git commit -m "chore: Remove completed migration scripts

- Delete migrate-to-v5.1.sh (10,715 lines)
- Delete init-kb.sh (11,868 lines)
- Migration complete, scripts no longer needed
- Saves 3,400 tokens

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

#### Task 1.3: Archive Analysis Reports (10 min)
**Files:** 7 legacy analysis reports in `.legacy/docs/analysis/`

**Action:** Move to deeper archive or delete

**Command:**
```bash
rm -rf .legacy/docs/analysis/
git add .legacy/docs/analysis/
git commit -m "chore: Archive historical analysis reports

- Remove 7 legacy analysis reports
- Migration complete, no longer needed
- Historical value minimal
- Saves 2,200 lines

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

#### Task 1.4: Update Version References (1 hr)
**Files:** 262 occurrences of v3.x/v4.0
**Action:** Replace with v5.1

**Command:**
```bash
# Find outdated references
grep -r "v3\." . --exclude-dir=.git --exclude-dir=.legacy --exclude-dir=.claude-code | wc -l
grep -r "v4\.0" . --exclude-dir=.git --exclude-dir=.legacy --exclude-dir=.claude-code | wc -l

# Update versions (manual review required)
# Use IDE find/replace or sed with caution
```

**Commit:** Group changes by file/directory

#### Task 1.5: Consolidate SKILLS.md (15 min)
**Files:** 2 duplicate SKILLS.md files
**Action:** Merge and consolidate

**Command:**
```bash
# Review duplicates
diff agents/curator/metadata/SKILLS.md domains/claude-code/SKILLS.md

# Consolidate (manual process)
# Keep agents/curator version, delete other if duplicate
```

#### Task 1.6: Add Missing last_updated (2 hrs)
**Files:** 43 YAML files missing last_updated
**Action:** Add "2026-01-08" to all

**Command:**
```bash
# Find files missing last_updated
grep -rL "last_updated:" domains/

# Add to each file (manual or script)
for file in $(grep -rL "last_updated:" domains/); do
  # Add after version field
  sed -i '/version:/a last_updated: "2026-01-08"' "$file"
done
```

#### Task 1.7: Clean Root Directory (30 min)
**Files:** Various root-level cleanup
**Action:** Remove obsolete files, organize

**Command:**
```bash
# Review root files
ls -la | grep -v "^\." | grep -v "\.git"

# Remove obsolete (case by case)
```

#### Task 1.8: Validate and Rebuild (30 min)
**Action:** Ensure all changes valid

**Commands:**
```bash
# Validate YAML
python tools/kb.py validate domains/

# Rebuild index
python tools/kb.py index --force -v

# Search test
python tools/kb.py search "docker"

# Check for broken links
grep -rh "@.*\.md" . --exclude-dir=.git --exclude-dir=.legacy | while read ref; do
  path=$(echo "$ref" | sed 's/@//')
  if [ ! -f "$path" ]; then
    echo "Broken: $ref"
  fi
done
```

### Success Criteria
- [ ] 30,000+ tokens saved
- [ ] Duplicate ratio < 2%
- [ ] Version consistency > 95%
- [ ] All validation checks pass
- [ ] Zero breaking changes

**Completion Time:** Week 1 (8 hours)

---

## Sprint 2: High Priority Cleanup (Week 2)

**Goal:** Maximum impact cleanup
**Duration:** 1 week (14 hours)
**Priority:** HIGH

### Task List

#### Task 2.1: Delete Low-Quality KB Entries (4.5 hrs)
**Files:** 49 YAML entries (quality < 40/100)
**Action:** Remove poor quality entries

**Process:**
1. Review `analysis_agent2_domains.csv`
2. Filter by Quality Score < 40
3. Verify safe to delete
4. Delete in batches by domain

**Commands:**
```bash
# Find low-quality files
awk -F, '$6 < 40' analysis_agent2_domains.csv

# Delete (manual review first)
# Commit by domain for safety
```

**Impact:** Quality score +10 points (47 → 57)

#### Task 2.2: Extract & Delete Legacy Research (2 hrs)
**Files:** 48 research docs in `.legacy/docs/research/claude-code/`
**Action:** Extract unique patterns, then delete

**Process:**
1. Review 26 migrated guides
2. Verify all content in YAML
3. Check for unique insights
4. Extract if valuable
5. Delete duplicates

**Commands:**
```bash
# List migrated guides
ls -la .legacy/docs/research/claude-code/

# Compare with YAML versions
diff .legacy/docs/research/claude-code/claude-hooks-guide.md \
     domains/claude-code/patterns/claude-code-hooks.yaml

# Extract value if unique, then delete
rm -rf .legacy/docs/research/claude-code/
```

**Impact:** 15,000 lines removed

#### Task 2.3: Merge Duplicate Documentation (3 hrs)
**Files:** 12 overlapping documentation files
**Action:** Consolidate into single sources

**Pairs to Merge:**
1. `LOCAL-INSTALL-GUIDE.md` + `HARMONIZED-INSTALLATION-GUIDE.md`
2. `SETUP_GUIDE_FOR_CLAUDE.md` + `for-claude-code/README.md`
3. `BOOTSTRAP-GUIDE.md` + `BOOTSTRAP.md`

**Process:**
1. Compare files side-by-side
2. Identify unique content
3. Merge into authoritative version
4. Delete duplicates
5. Update references

**Impact:** 3,000 lines removed, single source of truth

#### Task 2.4: Split Large Agent Documentation (2 hrs)
**Files:** 3 large agent files (>700 lines)
**Action:** Split into topic-specific files

**Files:**
1. `agents/curator/PROMPTS.md` (774 lines) → 7 files
2. `agents/curator/metadata/IMPLEMENTATION.md` (1,026 lines) → 8 files
3. `agents/curator/metadata/SKILLS.md` (932 lines) → 4 files

**Process:**
1. Read file structure
2. Identify logical sections
3. Extract each section to new file
4. Add @references in main file
5. Test navigation

**Impact:** Better progressive disclosure

#### Task 2.5: Delete Obsolete Archive Files (1 hr)
**Files:** Remaining obsolete files in `docs/archive/`
**Action:** Remove superseded documentation

**Files:**
- `SETUP_GUIDE_FOR_CLAUDE.md` (superseded by v5.1)
- `BOOTSTRAP-GUIDE.md` (superseded)
- `README_INTEGRATION.md` (duplicate)
- `TEST_KB_CURATOR.md` (superseded)
- `QUICK_SETUP_CLAUDE*.md` (obsolete)

**Commands:**
```bash
cd docs/archive/
rm SETUP_GUIDE_FOR_CLAUDE.md BOOTSTRAP-GUIDE.md README_INTEGRATION.md
rm TEST_KB_CURATOR.md QUICK_SETUP_CLAUDE*.md
git add .
git commit -m "chore: Remove obsolete archive files

- Delete 5 superseded documentation files
- Replaced by v5.1 architecture
- Improves clarity

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

#### Task 2.6: Add TOCs to Long Files (1.5 hrs)
**Files:** 22 files >500 lines without TOCs
**Action:** Generate and add tables of contents

**Process:**
1. Identify long files
2. Generate TOC from headers
3. Add to file top
4. Update links

**Tool:** Manual or automated TOC generator

### Success Criteria
- [ ] 50,000+ tokens saved total
- [ ] Quality score > 75/100
- [ ] Documentation consolidated
- [ ] All large files split
- [ ] Archive cleanup 90% complete

**Completion Time:** Week 2 (14 hours)

---

## Sprint 3: Medium Priority (Weeks 3-4)

**Goal:** Quality improvements
**Duration:** 2 weeks (30 hours)
**Priority:** MEDIUM

### Task List

#### Task 3.1: Standardize YAML Schema (2.5 hrs)
**Files:** 80 YAML files using old versions
**Action:** Update to version "5.1"

**Commands:**
```bash
# Find files using old versions
grep -r 'version: "1.0"' domains/
grep -r 'version: "4.0"' domains/

# Update (manual or scripted)
find domains/ -name "*.yaml" -exec sed -i 's/version: "1.0"/version: "5.1"/' {} \;
find domains/ -name "*.yaml" -exec sed -i 's/version: "4.0"/version: "5.1"/' {} \;
```

**Commit:** Bulk update with validation

#### Task 3.2: Fix ID Formats (1 hr)
**Files:** 8 YAML files with non-standard IDs
**Action:** Fix to CATEGORY-NNN format

**Process:**
1. Review `analysis_agent6_consistency.csv`
2. Filter by ID format issues
3. Fix each ID
4. Update references

#### Task 3.3: Merge Similar KB Entries (8 hrs)
**Files:** 38 YAML entries with similar problems
**Action:** Consolidate related entries

**Process:**
1. Group by problem type
2. Identify overlaps
3. Merge into single entries
4. Delete duplicates
5. Rebuild index

**Impact:** Cleaner KB, less redundancy

#### Task 3.4: Expand KB Entries with Prevention (6 hrs)
**Files:** 47 entries missing prevention steps
**Action:** Add best practices

**Process:**
1. Identify entries without prevention
2. Add prevention field
3. Write best practices
4. Validate

**Impact:** Higher quality KB entries

#### Task 3.5: Add Progressive Disclosure (3 hrs)
**Files:** 12 files without @references
**Action:** Implement progressive disclosure

**Process:**
1. Summarize long sections
2. Add @references to details
3. Test navigation
4. Validate links

#### Task 3.6: Split Large Pattern Files (3 hrs)
**Files:** 10 pattern files >500 lines
**Action:** Split into focused files

**Files:**
- `domains/universal/patterns/kb-update.yaml` (1,186 lines)
- Other large patterns

**Process:**
1. Identify sub-patterns
2. Extract to separate files
3. Add cross-references
4. Update IDs

#### Task 3.7: Add Type Hints to Python Tools (1 hr)
**Files:** 3 Python scripts (kb_submit.py, kb_search.py, kb_curate.py)
**Action:** Add type annotations

**Process:**
1. Review current code
2. Add function signatures with types
3. Add parameter types
4. Add return types
5. Test

#### Task 3.8: Implement Logging Framework (1 hr)
**Files:** 3 Python scripts
**Action:** Replace print() with logging

**Process:**
1. Import logging module
2. Configure logger
3. Replace print() with logger.info/debug/error
4. Test

#### Task 3.9: Add Test Coverage (4 hrs)
**Files:** Python tools and critical functions
**Action:** Write unit tests

**Process:**
1. Identify test gaps
2. Write test cases
3. Add pytest fixtures
4. Run tests
5. Achieve >50% coverage

### Success Criteria
- [ ] Quality score > 85/100
- [ ] 100% schema compliance
- [ ] Progressive disclosure implemented
- [ ] Test coverage > 50%
- [ ] Logging framework in place

**Completion Time:** Weeks 3-4 (30 hours)

---

## Sprint 4: Polish & Excellence (Weeks 5-8)

**Goal:** Achieve excellence (98/100)
**Duration:** 4 weeks (20 hours)
**Priority:** LOW

### Task List

#### Task 4.1: Final Legacy Cleanup (2 hrs)
**Files:** Remaining 15 legacy files
**Action:** Final extraction or deletion

#### Task 4.2: Quality Validation (3 hrs)
**Action:** Comprehensive quality checks

**Process:**
1. Run all validation scripts
2. Fix remaining issues
3. Verify consistency
4. Check links

#### Task 4.3: Documentation Optimization (3 hrs)
**Action:** Polish all documentation

**Process:**
1. Review all MD files
2. Improve formatting
3. Add missing examples
4. Update screenshots

#### Task 4.4: Performance Optimization (2 hrs)
**Action:** Token and performance improvements

**Process:**
1. Review large files
2. Optimize further
3. Compress where possible
4. Measure impact

#### Task 4.5: Automated Validation Setup (3 hrs)
**Action:** CI/CD checks

**Process:**
1. Create validation scripts
2. Add pre-commit hooks
3. Add CI checks
4. Configure notifications

#### Task 4.6: Create Metrics Dashboard (2 hrs)
**Action:** Track quality metrics

**Process:**
1. Define metrics
2. Create dashboard
3. Setup reporting
4. Track trends

#### Task 4.7: Documentation of Improvements (3 hrs)
**Action:** Document changes

**Process:**
1. Write CHANGELOG entry
2. Update README
3. Create migration guide
4. Update standards

#### Task 4.8: Final Review & Testing (2 hrs)
**Action:** Comprehensive testing

**Process:**
1. End-to-end testing
2. User acceptance testing
3. Performance testing
4. Security review

### Success Criteria
- [ ] Quality score 98/100
- [ ] 100% consistency
- [ ] Zero critical issues
- [ ] Automated validation in place
- [ ] Documentation complete

**Completion Time:** Weeks 5-8 (20 hours)

---

## Buffer Weeks (Weeks 9-10)

**Goal:** Handle unplanned work, delays, additional improvements
**Duration:** 2 weeks (25.5 hours)

**Use Cases:**
- Tasks took longer than estimated
- Additional issues discovered
- Team member availability
- Testing and validation
- Stakeholder feedback

---

## Weekly Status Report Template

```markdown
# Week N Status Report

**Date:** YYYY-MM-DD
**Sprint:** N
**Completed Tasks:**
- [ ] Task N.X (Y hours)
- [ ] Task N.Y (Z hours)

**Metrics:**
- Quality Score: XX/100
- Tokens Saved: XX,XXX
- Files Deleted: XX
- Time Spent: XX hours

**Issues:**
- Issue description
- Resolution/Plan

**Next Week:**
- Planned tasks
- Estimated hours

**Risks:**
- Risk description
- Mitigation
```

---

## Success Metrics Summary

### Week 1 (Sprint 0 + 1)
- Quality: 71 → 78 (+7)
- Tokens: -30,000 (-9%)
- Files: -40 (-10%)

### Week 2 (Sprint 2)
- Quality: 78 → 82 (+4)
- Tokens: -20,000 (-6%)
- Files: -30 (-7%)

### Weeks 3-4 (Sprint 3)
- Quality: 82 → 90 (+8)
- Tokens: -15,000 (-4%)
- Files: -20 (-5%)

### Weeks 5-8 (Sprint 4)
- Quality: 90 → 98 (+8)
- Tokens: -14,400 (-4%)
- Files: +10 (+3% due to splits)

### Final State
- **Quality Score:** 98/100 ✅
- **Total Tokens Saved:** 109,400 (-31%) ✅
- **Total Files:** 350 (-16%) ✅
- **Critical Issues:** 0 ✅
- **Duplicate Content:** 0% ✅

---

## Git Commit Strategy

### Commit Frequency
- **After each task** (if small)
- **After each sprint phase** (if large)
- **Always** before pushing

### Commit Message Format
```
type(scope): brief description

- Detailed bullet points
- Of changes made
- Impact described

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### Types
- `fix` - Bug fixes, critical issues
- `chore` - Cleanup, optimization
- `docs` - Documentation changes
- `refactor` - Code restructuring
- `test` - Test additions
- `style` - Formatting, style changes

---

## Risk Management

### Weekly Review
- Assess progress
- Identify blockers
- Adjust timeline
- Re-prioritize if needed

### Rollback Plan
- Git revert available
- Each sprint is独立
- Can stop after any sprint

### Quality Gates
- Validation must pass
- Tests must pass
- Manual review for deletions
- Zero breaking changes

---

## Conclusion

This sprint plan provides a **structured, phased approach** to repository optimization over **10 weeks**. By following this plan, we will achieve **excellence (98/100 quality score)** while saving **31% in tokens** and creating a **maintainable, professional-grade** knowledge base.

**Recommendation:** Begin immediately with Sprint 0 (27 minutes critical fixes), then proceed through sprints sequentially.

**Next Step:** Execute Sprint 0 tasks TODAY.

---

**Plan Status:** ✅ READY FOR EXECUTION
**Start Date:** 2026-01-08
**End Date:** 2026-03-18
**Total Duration:** 10 weeks
