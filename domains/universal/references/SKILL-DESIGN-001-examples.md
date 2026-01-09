# Skill Design Pattern - Real World Examples

**Extracted from:** skill-design.yaml
**Pattern ID:** SKILL-DESIGN-001

## Example 1: React Testing Skill

**Scenario:** Skill for generating React component tests

### Good Design

```yaml
---
name: react-testing-skill
description: |
  Generates tests for React components using React Testing Library.
  Covers user interactions, accessibility, and edge cases.
  Achieves 80%+ coverage with RTL best practices.

  Triggers when:
  - User asks to "test this component" or "generate tests for Button"
  - Need React Testing Library patterns
  - Must verify accessibility in tests
---

# React Testing Skill

## When to Use
- User asks: "Test this component", "Generate tests for Button"
- Need React Testing Library patterns
- Must verify accessibility

## Key Principles
1. Query by user-facing attributes (role, label)
2. NOT implementation details (class names, state)
3. Test BEHAVIOR not internals
4. Always include accessibility tests

## Common Patterns
See @resources/patterns/ for:
- Form component testing
- Async interaction testing
- Error state testing
- Accessibility testing

## Tools
- **Read**: Read component file
- **Write**: Create test file
- **Execute**: Run tests (optional)
```

### Key Points
- Specific description explains when to trigger
- SKILL.md is lean (references to resources)
- Clear principles and patterns
- Tools documented

## Example 2: Code Review Skill

**Scenario:** Skill for reviewing pull requests

### Good Design

```yaml
---
name: code-review-skill
description: |
  Reviews pull requests against architecture, performance,
  and security standards. Provides specific feedback with
  references to team guidelines.

  Triggers when:
  - User asks to "review this PR" or "check #1234"
  - Pull request needs validation
  - Code review workflow initiated
---

# Code Review Skill

## What This Reviews
1. Architecture compliance (@../../.claude/standards/architecture.md)
2. Performance implications
3. Security vulnerabilities
4. Code clarity and maintainability

## Review Process

### Step 1: Check Architecture
```bash
grep -rn "import.*from" --include="*.ts" \
  "$FILES_CHANGED" > /tmp/imports.txt
```
Compare against @resources/architecture-patterns.md

### Step 2: Check Performance
- Unnecessary re-renders in React?
- N+1 query patterns?
- Inefficient algorithms?
See @resources/performance-checklist.md

### Step 3: Check Security
```bash
grep -rn "eval\|exec\|innerHTML" "$FILES_CHANGED"
```
See @resources/security-checklist.md

### Step 4: Generate Report
Creates markdown review with:
- Summary (PASS/CONCERN/FAIL)
- Issues grouped by severity
- Specific code snippets
- Actionable suggestions
```

### Key Points
- Clear trigger conditions
- Step-by-step process
- References to team standards
- Scripts for automation
- Checklist resources

## Example 3: CSV Analyzer Skill

**Scenario:** Skill for analyzing CSV files

### Good Design

```yaml
---
name: csv-analyzer-skill
description: |
  Analyzes CSV files: generates statistics, identifies
  patterns, creates visualizations. Handles large files
  (10K+ rows) efficiently using Python pandas.

  Triggers when:
  - User asks to "analyze this CSV" or "summarize data"
  - CSV file needs statistics or visualization
  - Data exploration required
---

# CSV Analyzer Skill

## What This Skill Does
1. Reads CSV file using Python
2. Generates descriptive statistics
3. Creates summary report
4. Produces visualizations (if requested)

## Step-by-Step Instructions

### 1. Validate Input
```bash
python scripts/validate_csv.py "$FILE_PATH"
```
If validation fails, inform user and ask for correction.

### 2. Generate Statistics
```bash
python scripts/generate_stats.py "$FILE_PATH" --format json
```

### 3. Create Report
Parse JSON and create human-readable markdown report

### 4. Optional: Generate Visualizations
If user asks for charts:
```bash
python scripts/visualize.py \
  --input "$FILE_PATH" \
  --output report.png \
  --type histogram
```

## Important Notes
- Max file size: 500MB (streams larger files)
- Script handles UTF-8 encoding issues
- Missing values noted but don't fail analysis
- Error messages in console output

## Tools Required
- **Read**: For input CSV files
- **Execute**: Python script execution
- **Write**: For output report/charts
```

### Key Points
- Error handling in validation script
- Step-by-step workflow
- Optional features clearly marked
- File size limits documented
- Tools listed

## Verification Methods

### Trigger Check
**Test:** Verify skill description triggers correctly

**Method:**
1. Start new Claude Code session with skill loaded
2. Ask: "Did you load {skill-name}?"
3. If NO: Description needs to be more specific
4. If YES: Skill is discoverable

### Size Check
**Test:** Verify SKILL.md is not too large

**Method:**
```bash
wc -l .claude/skills/{skill-name}/SKILL.md
# Should be < 500 lines
# Ideally 200-400 lines
```

### Reference Check
**Test:** Verify all @references resolve

**Method:**
```bash
# Extract all @references from SKILL.md
grep -oh "@[a-zA-Z/_-]*\.md" \
  .claude/skills/{skill-name}/SKILL.md

# Verify each file exists
for ref in $(grep -oh "@[a-zA-Z/_-]*\.md" \
  .claude/skills/{skill-name}/SKILL.md); do
  file="${ref#@}"
  if [ ! -f ".claude/skills/{skill-name}/$file" ]; then
    echo "❌ Broken reference: $ref"
  fi
done
```

### Evaluation Check
**Test:** Verify skill improves performance

**Method:**
1. Create 3 evaluation scenarios
2. Run WITHOUT skill → Record baseline scores
3. Run WITH skill → Record new scores
4. Compare: improvement = new - baseline
5. If no improvement: Refine skill

## Testing Checklist

### Design Phase
- Problem clearly defined (gap analysis done)
- 3 evaluation scenarios created
- Baseline score obtained (without skill)
- Skill written (≤500 lines SKILL.md)
- Resources organized in subdirectories

### Quality Checks
- YAML frontmatter is valid
- Description is specific & clear
- Name is lowercase-kebab-case
- Instructions are sequential & clear
- Examples are minimal (1-2 per pattern)
- Error handling in scripts
- No circular references

### Testing Phase
- Tested with fresh Claude instance
- All 3 evaluations run successfully
- Score improvement measured
- Iteratively improved based on observations
- Team tested (2+ developers)

### Governance
- Code reviewed (2+ approvals)
- Added to settings.json enabled list
- Documented in .claude/CLAUDE.md
- Version number assigned
- Team notified
