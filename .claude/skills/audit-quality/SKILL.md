---
name: "audit-quality"
description: "Perform comprehensive quality audit on knowledge base entries. Analyzes completeness, accuracy, documentation quality, and adherence to best practices"
version: "1.0"
author: "Shared KB Curator"
tags: ["audit", "quality", "review", "analyze"]
---

# Skill: Audit Quality

## What this Skill does
Perform comprehensive quality audit on knowledge base entries. Analyzes completeness, accuracy, documentation quality, and adherence to best practices.

## Trigger
- User mentions "audit", "quality check", "review quality"
- Periodic KB maintenance (monthly/quarterly)
- Before major releases
- After bulk imports
- Part of curator workflow

## What Claude can do with this Skill

### 1. Audit Single Entry
```bash
# Detailed audit of one entry
python tools/kb.py validate python/errors/async-errors.yaml --audit

# Output shows:
# - Quality score breakdown
# - Missing fields
# - Improvement suggestions
# - Comparison to category average
```

### 2. Audit Category/Scope
```bash
# Audit all Python entries
python tools/kb.py audit python/errors

# Audit all high-severity entries
python tools/kb.py audit --severity high

# Audit by scope
python tools/kb.py audit --scope universal
```

### 3. Comprehensive Audit
```bash
# Audit entire KB
python tools/kb.py audit .

# Generates:
# - Overall quality report
# - Entries by score range
# - Categories needing attention
# - Improvement priorities
```

### 4. Quality Dimensions Audited

#### Dimension 1: Completeness (0-30 points)
```
✓ All required fields present (version, category, last_updated)
✓ Entry has id, title, severity, scope
✓ Problem statement clear and complete
✓ Solution has both code and explanation
✓ Prevention strategies included
✓ Tags are relevant and specific
```

#### Dimension 2: Technical Accuracy (0-30 points)
```
✓ Code examples are syntactically correct
✓ Solution actually solves the stated problem
✓ No deprecated APIs used
✓ Dependencies clearly stated
✓ Version compatibility noted
✓ Edge cases addressed
```

#### Dimension 3: Documentation (0-20 points)
```
✓ Problem description is clear
✓ Symptoms are reproducible
✓ Root cause is explained
✓ Solution explanation is thorough
✓ Real-world context provided
✓ Examples are practical
```

#### Dimension 4: Best Practices (0-20 points)
```
✓ Follows coding standards
✓ Security considerations included
✓ Performance implications noted
✓ Solution is maintainable
✓ Cross-references to related entries
✓ Prevention is actionable
```

### 5. Audit Report Format
```
📊 KB Quality Audit Report
Generated: 2026-01-07 14:45:32

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVERALL STATISTICS
───────────────────────────────────────────
Total Entries Audited: 127
Average Quality Score: 82.3/100
Score Range: 65 - 98

QUALITY DISTRIBUTION
───────────────────────────────────────────
Excellent (95-100):  12 entries (9.4%)   ⭐⭐⭐⭐⭐
Good (85-94):       45 entries (35.4%)  ⭐⭐⭐⭐
Acceptable (75-84): 48 entries (37.8%)  ⭐⭐⭐
Needs Work (65-74): 18 entries (14.2%)  ⭐⭐
Poor (<65):          4 entries (3.1%)    ⭐

BY SCOPE
───────────────────────────────────────────
universal:     85.2 avg (12 entries)  ⭐⭐⭐⭐
python:        83.1 avg (32 entries)  ⭐⭐⭐⭐
javascript:    80.5 avg (18 entries)  ⭐⭐⭐
docker:        78.9 avg (22 entries)  ⭐⭐⭐
postgresql:    84.3 avg (12 entries)  ⭐⭐⭐⭐
framework:     81.7 avg (28 entries)  ⭐⭐⭐⭐

TOP 10 ENTRIES
───────────────────────────────────────────
1. [UNIVERSAL-008] Testing Best Practices - 98/100 ⭐⭐⭐⭐⭐
2. [PYTHON-023] Async Context Managers - 96/100 ⭐⭐⭐⭐⭐
3. [DOCKER-015] Multi-stage Builds - 95/100 ⭐⭐⭐⭐⭐
... (7 more)

BOTTOM 10 ENTRIES (Need Attention)
───────────────────────────────────────────
1. [PYTHON-004] Import Errors - 65/100 ⭐
   Issues: Missing prevention, incomplete documentation
   Action: Enhance with examples and best practices

2. [DOCKER-007] Volume Mounts - 68/100 ⭐⭐
   Issues: Outdated examples, no edge cases
   Action: Update with current Docker practices

... (8 more)

IMPROVEMENT PRIORITIES
───────────────────────────────────────────
High Priority (Score < 75):
  - PYTHON-004: Import Errors (65) ⚠️
  - DOCKER-007: Volume Mounts (68) ⚠️
  - JAVASCRIPT-011: Promise Chains (70) ⚠️

Medium Priority (Score 75-84):
  - 48 entries need minor enhancements

Low Priority (Score 85-94):
  - 45 entries are good, could be excellent

RECOMMENDATIONS
───────────────────────────────────────────
1. Immediate: Improve 4 entries with score < 75
2. This Week: Enhance 18 entries in "Needs Work" range
3. This Month: Add examples to 48 "Acceptable" entries
4. Ongoing: Aim for 85+ average across all scopes

CATEGORY INSIGHTS
───────────────────────────────────────────
Strongest Categories:
  - Testing (avg: 87.3) ⭐⭐⭐⭐⭐
  - Architecture (avg: 86.1) ⭐⭐⭐⭐⭐

Weakest Categories:
  - Error Handling (avg: 76.8) ⭐⭐⭐
  - Performance (avg: 78.2) ⭐⭐⭐

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Key files to reference
- Quality rubric: `@curator/QUALITY_STANDARDS.md`
- Validation tool: `@tools/validate-kb.py`
- Entry format: `@universal/patterns/shared-kb-yaml-format.yaml`

## Implementation rules
1. **Audit systematically** - Don't skip entries
2. **Be thorough** - Check all quality dimensions
3. **Provide feedback** - Explain scores and suggestions
4. **Prioritize** - Focus on low scores first
5. **Track progress** - Re-audit after improvements

## Common commands
```bash
# Audit single entry (detailed)
python tools/kb.py validate entry.yaml --audit

# Audit category
python tools/kb.py audit python/errors

# Audit by severity
python tools/kb.py audit --severity high

# Audit entire KB
python tools/kb.py audit .

# Audit with verbose output
python tools/kb.py audit . --verbose

# Export audit report
python tools/kb.py audit . --output audit-report.md
```

## Audit Workflow

### Weekly Spot Checks
```bash
# Audit 5 random entries from each scope
python tools/kb.py audit --random 5 --all-scopes

# Focus on recent additions
python tools/kb.py audit --since "2026-01-01"
```

### Monthly Comprehensive Audit
```bash
# Full KB audit
python tools/kb.py audit . --output monthly-audit-$(date +%Y%m).md

# Review and plan improvements
# Prioritize entries < 75 score
```

### Quarterly Deep Dive
```bash
# Complete audit + action plan
python tools/kb.py audit . --full-report

# Includes:
# - Quality trends over time
# - Category comparisons
# - Improvement tracking
# - Best practice identification
```

## Quality Improvement Process

### For Low-Scoring Entries (< 75)
1. **Identify gaps** using audit report
2. **Research** best practices (research-enhance skill)
3. **Add content** to address gaps
4. **Re-validate** to confirm improvement
5. **Track** progress in metadata

### For Mid-Range Entries (75-84)
1. **Polish documentation**
2. **Add real-world examples**
3. **Include edge cases**
4. **Add performance notes**
5. **Cross-reference** related entries

### For High-Scoring Entries (85+)
1. **Consider for promotion** to universal scope
2. **Use as examples** for new entries
3. **Identify patterns** for reuse
4. **Share** in team updates

## Score Analysis

### Score Trends
```bash
# Track score changes over time
python tools/kb.py audit . --trend

# Compare to previous audit
python tools/kb.py audit . --compare previous-audit.md
```

### Category Benchmarks
```
Excellent Categories (avg 85+):
  - Testing (87.3)
  - Architecture (86.1)
  - Security (85.8)

Target Categories (avg 80-84):
  - Async/Await (83.1)
  - Database (84.3)
  - CLI Tools (82.5)

Needs Improvement (avg < 80):
  - Error Handling (76.8) ← Focus here
  - Performance (78.2) ← Focus here
  - File I/O (79.1) ← Focus here
```

## Related Skills
- `kb-validate` - Quick validation check
- `find-duplicates` - Check for duplicate content
- `research-enhance` - Enhance entries with research
- `update-versions` - Update outdated entries
- `identify-gaps` - Find missing content

## Automation
Schedule automatic audits:
```bash
# Weekly: Audit recent entries
0 9 * * 1 cd /path/to/kb && python tools/kb.py audit --since "1 week ago" --output weekly-audit.md

# Monthly: Full audit
0 9 1 * * cd /path/to/kb && python tools/kb.py audit . --output monthly-audit-$(date +\%Y\%m).md
```

## Troubleshooting

### Issue: "Audit takes too long"
**Fix:**
```bash
# Audit smaller scope
python tools/kb.py audit python/errors

# Parallelize by scope
for scope in python javascript docker; do
  python tools/kb.py audit $scope &
done
```

### Issue: "Scores seem wrong"
**Check:**
- Review quality rubric
- Verify validation rules
- Check for updated standards
- Re-run audit after changes

### Issue: "Too many low scores"
**Strategy:**
1. Prioritize by severity (critical > high > medium)
2. Focus on frequently accessed entries
3. Batch improvements by category
4. Track and celebrate progress

---
**Version:** 1.0
**Last Updated:** 2026-01-07
**Skill Type:** Quality Assurance
**Target Score:** 85/100 (average)
