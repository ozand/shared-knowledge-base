# Review Claude Setup

Review .claude/ organization and provide recommendations for improvement.

## Usage
```
/review-claude-setup [options]
```

## Quick Examples

### Basic Review
```
/review-claude-setup
```
Reviews entire .claude/ organization.

### Specific Component
```
/review-claude-setup --component skills
```
Reviews only skills organization.

### Detailed Analysis
```
/review-claude-setup --detailed
```
Provides detailed analysis with recommendations.

## What This Command Does

1. **Analyzes structure** - Checks .claude/ directory organization
2. **Validates configuration** - Verifies settings.json and skill-rules.json
3. **Checks token efficiency** - Measures file sizes and progressive disclosure
4. **Reviews compliance** - Checks against best practices
5. **Provides recommendations** - Suggests improvements
6. **Generates report** - Detailed analysis with scores

**📘 Standards:** `@standards/quality-gates.md`

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `--component <comp>` | Review specific component | `--component skills` |
| `--detailed` | Provide detailed analysis | `--detailed` |
| `--fix` | Apply fixes automatically | `--fix` |
| `--output <file>` | Save report to file | `--output report.md` |

## Components Reviewed

### 1. Directory Structure

**Checks:**
- ✅ .claude/ directory exists
- ✅ Standard subdirectories present (skills/, agents/, commands/, hooks/)
- ✅ No files in root (should be organized)
- ✅ Proper naming conventions

**Standard structure:**
```
.claude/
├── CLAUDE.md
├── settings.json
├── skill-rules.json
├── skills/
├── agents/
├── commands/
├── hooks/
├── standards/
└── references/
```

### 2. CLAUDE.md

**Checks:**
- ✅ File exists
- ✅ Size <300 lines (target)
- ✅ Contains essential sections
- ✅ Links to detailed documentation
- ✅ Progressive disclosure applied

**Metrics:**
- Line count
- Token estimate
- Link coverage
- Section completeness

### 3. Skills

**Checks:**
- ✅ All skills have YAML frontmatter
- ✅ SKILL.md <500 lines
- ✅ resources/ directory for large skills
- ✅ skill-rules.json entries exist
- ✅ Names match across files

**Metrics:**
- Number of skills
- Average size
- YAML coverage (%)
- Progressive disclosure (%)

### 4. Commands

**Checks:**
- ✅ All commands <200 lines
- ✅ Proper usage examples
- ✅ Links to references
- ✅ Clear descriptions

**Metrics:**
- Number of commands
- Average size
- Oversized commands count
- Link coverage

### 5. Hooks

**Checks:**
- ✅ Hooks registered in settings.json
- ✅ Hook files exist
- ✅ Shell hooks executable
- ✅ Performance targets met

**Metrics:**
- Number of hooks
- Events covered
- Shell vs LLM ratio
- Performance compliance

### 6. Standards and References

**Checks:**
- ✅ standards/ directory exists
- ✅ references/ directory exists
- ✅ Single source of truth
- ✅ No content duplication

**Metrics:**
- Number of standards
- Number of references
- Duplication score
- Link density

## Output

### Summary Report

```
📊 Claude Code Setup Review

Overall Score: 85/100 ✅ Good

Structure:       90/100 ✅ Excellent
Token Efficiency: 80/100 ✅ Good
Compliance:      85/100 ✅ Good
Progressive Disclosure: 75/100 ⚠️ Needs improvement

✅ Strengths:
   - Well-organized directory structure
   - All skills have YAML frontmatter
   - Good use of references/

⚠️  Issues Found:
   - CLAUDE.md exceeds 300 lines (320 lines)
   - 2 commands oversized (>200 lines)
   - 3 skills missing progressive disclosure

💡 Recommendations:
   1. Optimize CLAUDE.md to ~250 lines
   2. Apply progressive disclosure to 3 skills
   3. Optimize 2 oversized commands

📝 Detailed report: /review-claude-setup-report.md
```

### Detailed Report (--detailed)

```
================================
Claude Code Setup Review Report
================================

Generated: 2026-01-07
Repository: shared-knowledge-base

────────────────────────────────
1. DIRECTORY STRUCTURE
────────────────────────────────

Score: 90/100 ✅ Excellent

Structure:
✅ .claude/ exists
✅ Standard subdirectories present
⚠️  Found: 3 files in root (should be in subdirectories)

Recommendations:
- Move tmp/ files to archive/

────────────────────────────────
2. CLAUDE.md
────────────────────────────────

Score: 75/100 ⚠️ Needs improvement

Metrics:
- Lines: 320 (target: ~300)
- Estimated tokens: ~2,400
- Link coverage: 85%
- Progressive disclosure: Partial

Issues:
⚠️  Exceeds target by 20 lines
⚠️  Some sections verbose (Documentation, Workflows)

Recommendations:
1. Condense Documentation section (-10 lines)
2. Move detailed workflows to references/ (-15 lines)
3. Target: ~250 lines

────────────────────────────────
3. SKILLS (7 skills)
────────────────────────────────

Score: 80/100 ✅ Good

Metrics:
- Total skills: 7
- Average size: 325 lines
- YAML coverage: 100% ✅
- Progressive disclosure: 57% (4/7)

Issues:
⚠️  3 skills missing progressive disclosure
⚠️  1 skill exceeds 500 lines (research-enhance: 510 lines)

Recommendations:
1. Split research-enhance skill (move to resources/)
2. Add YAML frontmatter resources to all skills
3. Target: 100% progressive disclosure

────────────────────────────────
4. COMMANDS (7 commands)
────────────────────────────────

Score: 70/100 ⚠️ Needs improvement

Metrics:
- Total commands: 7
- Average size: 160 lines
- Oversized commands: 2/7 (28%)
- Link coverage: 85%

Issues:
❌ kb-query.md: 215 lines (limit: 200)
❌ retrospective.md: 210 lines (limit: 200)

Recommendations:
1. Optimize kb-query.md (target: <150 lines)
2. Optimize retrospective.md (target: <150 lines)
3. Move verbose examples to references/

────────────────────────────────
5. HOOKS (4 hooks)
────────────────────────────────

Score: 95/100 ✅ Excellent

Metrics:
- Total hooks: 4
- Events covered: 3/5 (60%)
- Shell vs LLM: 3 shell, 1 LLM
- Performance compliance: 100%

Strengths:
✅ All hooks registered in settings.json
✅ Shell hooks executable
✅ Performance targets met

Recommendations:
- Consider adding SessionStart hook
- Consider adding Stop hook

────────────────────────────────
6. STANDARDS & REFERENCES
────────────────────────────────

Score: 90/100 ✅ Excellent

Metrics:
- Standards: 3 files
- References: 3 files
- Duplication score: Low ✅
- Link density: High ✅

Strengths:
✅ Single source of truth
✅ No content duplication
✅ Comprehensive references

────────────────────────────────
7. TOKEN EFFICIENCY
────────────────────────────────

Score: 75/100 ⚠️ Needs improvement

Session Start Costs:
- CLAUDE.md: ~2,400 tokens (target: ~2,000)
- Skills metadata: ~350 tokens ✅
- Commands: 0 tokens (loaded on use) ✅
- Total: ~2,750 tokens (target: <3,000)

Savings Achieved: 30%
Potential Savings: +15% (with improvements)

────────────────────────────────
8. COMPLIANCE
────────────────────────────────

Best Practices Compliance: 85%

✅ Follows naming conventions
✅ YAML frontmatter on all skills
✅ Single source of truth
⚠️  Progressive disclosure partial
⚠️  Some oversized files

────────────────────────────────
SUMMARY
────────────────────────────────

Overall Score: 85/100 ✅ Good

Strengths:
- Well-organized structure
- Comprehensive standards and references
- Good use of YAML frontmatter
- Single source of truth

Areas for Improvement:
1. Apply progressive disclosure to all skills
2. Optimize oversized commands
3. Reduce CLAUDE.md size

Priority Actions:
1. Split research-enhance skill (-150 lines)
2. Optimize kb-query and retrospective (-130 lines)
3. Reduce CLAUDE.md to ~250 lines (-70 lines)

Expected Results:
- Token efficiency: +15% improvement
- Progressive disclosure: 100% coverage
- All files within size limits

────────────────────────────────
Next Steps
────────────────────────────────

1. Review recommendations
2. Implement changes
3. Run /optimize-tokens
4. Re-review setup

💡 Use /optimize-tokens --apply to auto-fix issues
================================
```

## Scoring System

### Overall Score

**90-100:** ✅ Excellent
**80-89:** ✅ Good
**70-79:** ⚠️ Needs improvement
**<70:** ❌ Poor

### Component Scores

**Structure (25%):**
- Directory organization
- File placement
- Naming conventions

**Token Efficiency (25%):**
- CLAUDE.md size
- Skill sizes
- Progressive disclosure

**Compliance (25%):**
- Best practices
- Standards adherence
- YAML frontmatter

**Quality (25%):**
- Content quality
- Link coverage
- Documentation

## Best Practices

### 1. Progressive Disclosure

**Target:** 100% coverage

**Current:** 57% (4/7 skills)

**Action Required:**
- Add resources/ to 3 skills
- Move detailed content from SKILL.md
- Add resource links to YAML frontmatter

### 2. File Sizes

**Targets:**
- CLAUDE.md: ~250 lines
- Commands: <200 lines
- Skills: <500 lines

**Current Issues:**
- CLAUDE.md: 320 lines (+20%)
- 2 commands: >200 lines
- 1 skill: >500 lines

### 3. Token Efficiency

**Target:** <3,000 tokens at session start

**Current:** ~2,750 tokens ✅

**Potential:** ~2,300 tokens (with improvements)

## Claude's Role

When using this command, Claude will:

1. **Analyze directory structure** - Check organization
2. **Measure file sizes** - Count lines, estimate tokens
3. **Validate YAML** - Check syntax and compliance
4. **Review progressive disclosure** - Check coverage
5. **Identify issues** - Find oversized files, missing metadata
6. **Calculate scores** - Component and overall scores
7. **Provide recommendations** - Specific improvements
8. **Generate report** - Detailed analysis document

## Examples

### Example 1: Quick Review

```
/review-claude-setup
```

Output:
```
📊 Claude Code Setup Review

Overall Score: 85/100 ✅ Good

Strengths:
✅ Well-organized structure
✅ All skills have YAML frontmatter
✅ Good use of references/

Issues:
⚠️  3 skills missing progressive disclosure
⚠️  2 commands oversized

Recommendations:
1. Apply progressive disclosure to 3 skills
2. Optimize 2 oversized commands
```

### Example 2: Skills Only

```
/review-claude-setup --component skills
```

Output:
```
📊 Skills Review

Score: 80/100 ✅ Good

Total Skills: 7
Average Size: 325 lines
YAML Coverage: 100%
Progressive Disclosure: 57%

Issues:
⚠️  research-enhance exceeds 500 lines
⚠️  3 skills missing resources/

Recommendations:
1. Split research-enhance (move to resources/)
2. Add resources/ to 3 skills
```

### Example 3: With Auto-Fix

```
/review-claude-setup --fix
```

Actions:
1. Splits oversized skills
2. Optimizes commands
3. Adds progressive disclosure
4. Updates YAML frontmatter
5. Generates optimized versions

## Related

- `@standards/quality-gates.md` - Quality requirements
- `@commands/optimize-tokens.md` - Token optimization
- `@skills/claude-code-architecture/SKILL.md` - Architecture review
- `universal/patterns/claude-code-files-organization-001.yaml` - Organization guide

---

**Version:** 1.0
**Last Updated:** 2026-01-07
