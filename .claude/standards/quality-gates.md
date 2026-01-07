# Quality Gates

**Quality requirements and validation standards for Shared Knowledge Base entries**

---

## Minimum Quality Score: 75/100

Entries must score **75/100 or higher** before committing to shared repository.

---

## Quality Scoring Rubric

### Completeness (40 points)

**All required fields present (10 points):**
- [ ] `id` - Unique identifier
- [ ] `title` - Human-readable title
- [ ] `severity` - Impact level
- [ ] `scope` - Applicability
- [ ] `problem` - Problem description
- [ ] `solution` - Solution with code

**Detailed problem description (10 points):**
- [ ] Clear what went wrong
- [ ] Context provided
- [ ] Impact explained

**Comprehensive solution (10 points):**
- [ ] Tested code example
- [ ] Explanation provided
- [ ] Addresses root cause

**Prevention strategies (10 points):**
- [ ] How to avoid issue
- [ ] Best practices included
- [ ] Related patterns referenced

---

### Accuracy (30 points)

**Tested code examples (15 points):**
- [ ] Code runs without errors
- [ ] Produces expected output
- [ ] Tested in relevant environment

**Correct root cause (15 points):**
- [ ] Root cause identified correctly
- [ ] Explanation accurate
- [ ] Solution addresses root cause

---

### Usability (20 points)

**Clear explanation (10 points):**
- [ ] Language accessible
- [ ] Technical terms explained
- [ ] Step-by-step when needed

**Actionable solution (10 points):**
- [ ] Can implement directly
- [ ] No ambiguity
- [ ] Complete instructions

---

### Maintainability (10 points)

**Up-to-date versions (5 points):**
- [ ] Library versions specified
- [ ] Tested on current version
- [ ] Version compatibility noted

**Fresh content (5 points):**
- [ ] Last updated < 180 days
- [ ] Still relevant
- [ ] No deprecated patterns

---

## Quality Checklist

### Before Creating Entry

```bash
# 1. Validate YAML syntax
python tools/kb.py validate <file>

# 2. Check quality score
python tools/kb.py check-quality <file>

# Expected: Quality score ≥ 75/100
```

---

### Manual Review Checklist

**Completeness:**
- [ ] All required fields present
- [ ] Problem clearly described
- [ ] Solution comprehensive
- [ ] Prevention strategies included

**Accuracy:**
- [ ] Code examples tested
- [ ] Root cause correct
- [ ] Solution tested and verified

**Usability:**
- [ ] Explanation clear
- [ ] Solution actionable
- [ ] No ambiguity

**Maintainability:**
- [ ] Versions specified
- [ ] Content fresh (< 180 days)
- [ ] No deprecated patterns

---

## Quality Gates Workflow

### Gate 1: YAML Validation

```bash
python tools/kb.py validate <file>
```

**Pass:** No syntax errors
**Fail:** Fix syntax errors before proceeding

---

### Gate 2: Quality Score

```bash
python tools/kb.py check-quality <file>
```

**Pass:** Score ≥ 75/100
**Fail:** Improve entry before committing

**Common improvements:**
- Add missing fields
- Improve code examples
- Add prevention strategies
- Update with latest versions
- Clarify explanations

---

### Gate 3: Duplicate Check

```bash
python tools/kb.py search "<keywords>"
```

**Pass:** No duplicate found
**Fail:** Update existing entry OR justify new entry

---

### Gate 4: Scope Verification

**Question:** Is this entry universal or project-specific?

**Universal scopes** (push to shared repository):
- ✅ docker
- ✅ universal
- ✅ python
- ✅ postgresql
- ✅ javascript

**Project-specific scopes** (keep local):
- ❌ framework
- ❌ domain
- ❌ project

---

### Gate 5: Code Testing

**Test code examples:**
```bash
# Copy code from solution.code
# Run in relevant environment
# Verify expected output
```

**Pass:** Code works as described
**Fail:** Fix code example before committing

---

## Auto-Quality Gates (Hooks)

### Pre-Commit Validation

**Hook:** `validate-yaml-before-commit.yaml`

**Validates:**
- YAML syntax
- Required fields
- ID format
- Quality score ≥ 75/100

**Blocks commit if:**
- Validation fails
- Quality score < 75/100
- Duplicate ID found

---

### Post-Format Quality Check

**Hook:** `quality-gate.yaml`

**Checks:**
- YAML formatting
- Field completeness
- Code example quality

**Warns if:**
- Quality score between 50-74
- Missing optional fields
- Code examples incomplete

---

## Quality Improvement

### Low Quality Score (< 75)

**Common issues:**
1. Missing required fields
2. Untested code examples
3. Vague problem description
4. Incomplete solution
5. No prevention strategies

**Improvement steps:**
1. Add missing fields
2. Test all code examples
3. Clarify problem description
4. Complete solution details
5. Add prevention strategies

---

### Medium Quality Score (75-84)

**Good but can improve:**
1. Add more examples
2. Improve explanation clarity
3. Add related patterns
4. Update versions
5. Enhance prevention strategies

**Improvement steps:**
1. Review against rubric
2. Add missing optional fields
3. Test on multiple versions
4. Add real-world examples
5. Reference related entries

---

### High Quality Score (85-100)

**Excellent quality!**

Maintain by:
1. Keeping content fresh
2. Updating with new versions
3. Adding examples from real use
4. Refining based on feedback

---

## Quality Metrics

### Repository Targets

**Average quality score:** ≥ 85/100
**Entries below 75:** < 5%
**Entries above 90:** > 30%

### Monitoring

```bash
# Check repository quality
python tools/kb.py analyze-quality

# Find low-quality entries
python tools/kb.py find-low-quality --threshold 75

# Quality by category
python tools/kb.py quality-by-category
```

---

## Quality Enforcement

### Shared Repository

**Mandatory:**
- Quality score ≥ 75/100
- All fields validated
- Code tested
- No duplicates

**Blockers:**
- Quality score < 75/100
- Validation failures
- Duplicate IDs
- Untested code examples

### Local Knowledge Base

**Recommended:**
- Quality score ≥ 70/100
- Most fields complete
- Code tested

**Flexible:**
- Project-specific contexts
- Environment-specific solutions
- Temporary workarounds

---

## Related

- `@standards/yaml-standards.md` - YAML format requirements
- `@standards/git-workflow.md` - Commit and push standards
- `@skills/audit-quality/SKILL.md` - Quality audit skill
- `@references/cli-reference.md` - Quality commands

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Minimum Score:** 75/100
