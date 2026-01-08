# Optimize Tokens

Analyze and optimize token efficiency for .claude/ organization.

## Usage
```
/optimize-tokens [options]
```

## Quick Examples

### Analyze Token Usage
```
/optimize-tokens
```
Analyzes current token efficiency.

### Apply Optimizations
```
/optimize-tokens --apply
```
Applies recommended optimizations automatically.

### Specific Component
```
/optimize-tokens --component CLAUDE.md
```
Optimizes only CLAUDE.md.

## What This Command Does

1. **Analyzes token usage** - Measures current consumption
2. **Identifies inefficiencies** - Finds oversized files, missing progressive disclosure
3. **Calculates potential savings** - Estimates token reduction
4. **Applies optimizations** - Condenses files, moves content to resources/
5. **Adds progressive disclosure** - Implements YAML frontmatter, resource links
6. **Validates improvements** - Ensures quality maintained

**Target:** 70%+ token savings at session start

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `--component <comp>` | Optimize specific component | `--component CLAUDE.md` |
| `--apply` | Apply optimizations | `--apply` |
| `--dry-run` | Show changes without applying | `--dry-run` |
| `--aggressive` | Apply aggressive optimizations | `--aggressive` |
| `--target <lines>` | Target line count | `--target 250` |

## Analysis

### Session Start Costs

**Current:**
```
CLAUDE.md: 320 lines × 7.5 tokens/line ≈ 2,400 tokens
Skills metadata: 7 skills × 50 tokens ≈ 350 tokens
Commands: 0 tokens (loaded on use) ≈ 0 tokens
──────────────────────────────────────────────────
Total: ~2,750 tokens
```

**After Optimization:**
```
CLAUDE.md: 215 lines × 7.5 tokens/line ≈ 1,610 tokens
Skills metadata: 7 skills × 50 tokens ≈ 350 tokens
Commands: 0 tokens (loaded on use) ≈ 0 tokens
──────────────────────────────────────────────────
Total: ~1,960 tokens

Savings: -790 tokens (-29%)
```

### On-Demand Loading

**When needed:**
- Full SKILL.md: ~2,000 tokens
- Resource files: ~3,000 tokens each

**Strategy:** Load only when user clicks @ reference

## Optimization Strategies

### 1. CLAUDE.md Optimization

**Before:** 320 lines
**After:** 215 lines (-33%)

**Actions:**
- Condense Documentation section (-20 lines)
- Simplify Workflows (-30 lines)
- Reduce verbose descriptions (-25 lines)
- Add links to references/ (-30 lines)

**Example transformation:**

**Before (verbose):**
```markdown
## Documentation

This repository contains comprehensive documentation covering multiple aspects:

### User Documentation
- README.md - Project overview (600 lines)
  - Installation instructions
  - Quick start guide
  - Feature descriptions
  - Configuration options
  - Troubleshooting section
  - FAQ section
  - Contributing guidelines
  - License information

- QUICKSTART.md - 5-minute setup (300 lines)
  - Prerequisites
  - Installation steps
  - First-time setup
  - Verification
  - Common issues

- GUIDE.md - Implementation guide (600 lines)
  - Architecture overview
  - Design decisions
  - Implementation steps
  - Testing strategies
  - Deployment guide
[... 47 lines total ...]
```

**After (condensed with links):**
```markdown
## Documentation

**User docs:** README.md (overview), QUICKSTART.md (5-min setup)
**Implementation:** GUIDE.md (complete guide)
**Claude Code:** for-claude-code/README.md (integration guide)
```

### 2. Skill Optimization

**Strategy:** Apply 500-line rule

**Actions:**
1. Identify sections >100 lines
2. Move to resources/
3. Add links in SKILL.md
4. Update YAML frontmatter

**Example:**

**Before (research-enhance: 510 lines):**
```markdown
# Research Enhance

## Enhancement Workflow
[100 lines]

## What Claude Can Do
[150 lines - detailed]

## Implementation Rules
[80 lines]

## Research Sources
[120 lines - detailed with links]

## Enhancement Examples
[60 lines - minimal]
```

**After (SKILL.md: 280 lines):**
```markdown
# Research Enhance

## Enhancement Workflow
[100 lines - condensed]

## What Claude Can Do
[50 lines - examples only]

**📘 Complete Capabilities:** `@resources/claude-capabilities.md`

## Implementation Rules
[80 lines]

## Quality Checklist
[30 lines]

**📘 Research Sources:** `@resources/research-sources.md`
**📘 Enhancement Examples:** `@resources/enhancement-examples.md`
```

**resources/ created:**
- `claude-capabilities.md` (150 lines)
- `research-sources.md` (120 lines)
- `enhancement-examples.md` (100 lines)

### 3. Command Optimization

**Target:** <200 lines per command

**Actions:**
1. Remove verbose descriptions (-30 lines)
2. Simplify examples (-20 lines)
3. Extract to references/ (-25 lines)
4. Add reference links (-5 lines)

**Example:**

**Before (kb-query.md: 215 lines):**
```markdown
# KB Query

Search the Shared Knowledge Base for error solutions, patterns, and best practices.

## Usage
```
/kb-query [options]
```

## Detailed Description (40 lines)
[Verbose description of all features...]

## What This Command Does (30 lines)
[Detailed explanation of each step...]

## Complete Workflow (60 lines)
[Step-by-step with extensive examples...]

## All Options (50 lines)
[Every option with detailed explanation...]
```

**After (kb-query.md: 115 lines):**
```markdown
# KB Query

Search the Shared Knowledge Base for error solutions and patterns.

## Usage
```
/kb-query [options]
```

## Quick Examples
[Concise examples]

## What This Command Does
[Brief description]

**📘 Complete Workflow:** `@references/workflows.md`

## Options
[Essential options table]

**📘 CLI Reference:** `@references/cli-reference.md`
```

## Output

### Analysis Report

```
📊 Token Efficiency Analysis

────────────────────────────────
CURRENT STATE
────────────────────────────────

Session Start: ~2,750 tokens
- CLAUDE.md: 2,400 tokens (320 lines)
- Skills metadata: 350 tokens (7 skills)

Progressive Disclosure: 57% (4/7 skills)

Issues:
⚠️  CLAUDE.md exceeds target (320 > 300)
⚠️  3 skills missing progressive disclosure
⚠️  2 commands oversized (>200 lines)

────────────────────────────────
OPTIMIZATION POTENTIAL
────────────────────────────────

Component: CLAUDE.md
- Current: 320 lines (~2,400 tokens)
- Target: 215 lines (~1,610 tokens)
- Savings: -790 tokens (-33%)

Component: Skills
- research-enhance: 510 → 280 lines
  - Move to resources/: -150 lines
  - Add progressive disclosure
  - Savings: -1,125 tokens at startup

Component: Commands
- kb-query.md: 215 → 115 lines (-100 lines)
- retrospective.md: 210 → 145 lines (-65 lines)
- Savings: -1,235 tokens total

────────────────────────────────
RECOMMENDED ACTIONS
────────────────────────────────

Priority 1: CLAUDE.md
1. Condense Documentation section (-20 lines)
2. Simplify Workflows section (-30 lines)
3. Reduce verbose descriptions (-25 lines)
4. Add links to references/ (-30 lines)
Expected: -790 tokens (-33%)

Priority 2: research-enhance skill
1. Split into SKILL.md (280 lines) + resources/
2. Move detailed content to resources/ (-150 lines)
3. Add YAML frontmatter resources
Expected: -1,125 tokens at startup (-98%)

Priority 3: Oversized commands
1. Optimize kb-query.md (215 → 115 lines)
2. Optimize retrospective.md (210 → 145 lines)
3. Move examples to references/
Expected: -1,235 tokens (-56%)

────────────────────────────────
EXPECTED RESULTS
────────────────────────────────

Session Start:
- Before: ~2,750 tokens
- After: ~1,100 tokens
- Savings: -1,650 tokens (-60%)

Progressive Disclosure:
- Before: 57% (4/7 skills)
- After: 100% (7/7 skills)

Quality:
- Content: Maintained ✅
- Links: Added ✅
- Accessibility: Improved ✅

────────────────────────────────
NEXT STEPS
────────────────────────────────

1. Review recommendations
2. Run: /optimize-tokens --apply
3. Restart Claude Code
4. Verify improvements

💡 Use --dry-run to preview changes
```

### With --apply

```
✅ Optimizations Applied

CLAUDE.md:
  Before: 320 lines
  After: 215 lines
  Savings: -105 lines (-33%)

Skills:
  research-enhance:
    Before: 510 lines
    After: 280 lines (SKILL.md) + 230 lines (resources/)
    Savings: -230 tokens at startup (-98%)

Commands:
  kb-query.md: 215 → 115 lines (-100)
  retrospective.md: 210 → 145 lines (-65)

Total Savings:
  Session start: -1,650 tokens (-60%)
  Progressive disclosure: 57% → 100%

✅ Quality maintained
✅ Links added
✅ References created

🔄 Restart Claude Code to apply changes
```

## Best Practices

### 1. Progressive Disclosure

**Apply to all components:**
- CLAUDE.md → essentials only
- Skills → SKILL.md + resources/
- Commands → concise + links

**Result:** 70%+ token savings

### 2. Content Distribution

**Root files (always loaded):**
- Essentials only
- Quick reference
- Links to details

**Resources/ (on-demand):**
- Detailed explanations
- Comprehensive examples
- Reference documentation

### 3. Link Strategy

**Use @ references:**
```markdown
**📘 Complete Guide:** `@references/workflows.md`
**📘 YAML Standards:** `@standards/yaml-standards.md`
```

**Benefits:**
- Single source of truth
- No duplication
- Easy to maintain

## Quality Assurance

### Before Optimizing

**Verify:**
- Content is accurate
- Links work
- No critical information lost

### After Optimizing

**Verify:**
- All @ links resolve
- Quality maintained
- No broken references
- YAML frontmatter valid

### Testing

**Test session start:**
```bash
# Measure token usage
# Before and after optimization
```

**Test links:**
```bash
# Click each @ reference
# Verify file loads
```

**Test activation:**
```bash
# Restart Claude Code
# Verify skills activate
# Test resources load
```

## Claude's Role

When using this command, Claude will:

1. **Analyze current state** - Measure file sizes, token usage
2. **Identify inefficiencies** - Find oversized files, missing progressive disclosure
3. **Calculate savings** - Estimate token reduction potential
4. **Propose optimizations** - Specific actions with line counts
5. **Apply changes** - If --apply specified
6. **Maintain quality** - Ensure no content lost
7. **Add links** - Create references/ where needed
8. **Validate results** - Verify improvements

## Examples

### Example 1: Analysis Only

```
/optimize-tokens
```

Output: Analysis report with recommendations

### Example 2: Apply Optimizations

```
/optimize-tokens --apply
```

Output: Applies all recommended optimizations

### Example 3: Specific Component

```
/optimize-tokens --component CLAUDE.md --apply
```

Output: Optimizes only CLAUDE.md

### Example 4: Dry Run

```
/optimize-tokens --dry-run
```

Output: Shows what would change without applying

## Related

- `@commands/review-claude-setup.md` - Setup review
- `@skills/claude-code-architecture/SKILL.md` - Architecture
- `@resources/claude-code-architecture/resources/progressive-disclosure.md` - Progressive disclosure
- `@standards/quality-gates.md` - Quality requirements

---

**Version:** 1.0
**Last Updated:** 2026-01-07
