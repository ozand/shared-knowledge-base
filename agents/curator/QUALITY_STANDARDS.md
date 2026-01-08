# QUALITY_STANDARDS.md - Knowledge Base Quality Standards

## Entry Quality Rubric

Every knowledge base entry is evaluated on these dimensions. Use this rubric when reviewing entries or assessing quality during audits.

---

## Dimension 1: Completeness (25 points)

### Required Fields (5 points)
- ✅ `id` present and follows CATEGORY-NNN format
- ✅ `title` is clear and descriptive
- ✅ `severity` is one of: critical, high, medium, low
- ✅ `scope` is valid (universal, python, javascript, docker, postgresql, framework, domain, project)
- ✅ `problem` field describes the issue

### Solution Quality (10 points)
**10 points (Excellent):**
- Solution includes working code example
- Explanation covers *why* it works
- Alternative approaches discussed
- Trade-offs documented

**7 points (Good):**
- Working code example provided
- Basic explanation included
- Solves the stated problem

**4 points (Acceptable):**
- Code example present but minimal
- Explanation unclear or missing
- Solution works but not well-explained

**0 points (Incomplete):**
- No code example
- Or code doesn't solve stated problem
- Or solution section missing

### Prevention & Context (5 points)
**5 points:** Comprehensive prevention guidelines + real-world context
**3 points:** Basic prevention guidelines
**1 point:** Minimal or generic prevention
**0 points:** No prevention guidelines

### Metadata (5 points)
**5 points:**
- Relevant tags present (3+)
- Cross-references to related entries
- Version-specific information when applicable
- Sources cited

**3 points:**
- Some tags present
- Minimal cross-references

**0 points:**
- No tags or cross-references

---

## Dimension 2: Technical Accuracy (25 points)

### Code Correctness (10 points)
**10 points:**
- Code compiles/runs without errors
- All imports are valid
- Syntax is correct for language
- Code follows language best practices
- No obvious bugs

**5 points:**
- Code has minor issues
- Or imports not verified
- Or doesn't follow idiomatic style

**0 points:**
- Code has syntax errors
- Or missing imports
- Or clearly incorrect

### Version Currency (8 points)
**8 points:**
- Uses current library/framework versions
- Tested with current versions
- Notes if version-specific
- No deprecated APIs used

**4 points:**
- Versions not specified but likely current
- Or minor version lag (within last 6 months)

**0 points:**
- Uses deprecated APIs
- Or versions clearly outdated
- Or incompatible with current versions

### Solution Effectiveness (7 points)
**7 points:**
- Solution directly solves stated problem
- Tested in real scenarios
- Handles edge cases
- No unintended side effects

**4 points:**
- Solution solves basic problem
- May not handle edge cases
- Not verified in production

**0 points:**
- Solution doesn't solve problem
- Or introduces new problems
- Or is theoretical/untested

---

## Dimension 3: Clarity & Comprehensibility (20 points)

### Problem Description (5 points)
**5 points:**
- Clear, concise description
- Includes symptoms/error messages
- Context is obvious
- Root cause explained

**3 points:**
- Problem described but unclear
- Or missing context
- Or symptoms not listed

**0 points:**
- Problem not described
- Or description is confusing

### Explanation Quality (10 points)
**10 points:**
- Explains *why* problem occurs
- Explains *why* solution works
- Uses appropriate technical depth
- Avoids jargon without explanation
- Flows logically

**6 points:**
- Basic explanation provided
- Some gaps in reasoning
- Or too technical/simplistic

**3 points:**
- Minimal explanation
- Or explanation is unclear
- Or misses key points

**0 points:**
- No explanation provided

### Code Documentation (5 points)
**5 points:**
- Code has helpful comments
- Variable names are self-documenting
- Complex logic explained inline
- Example usage clear

**3 points:**
- Some comments present
- Variable names mostly clear

**0 points:**
- No comments
- Or variables poorly named
- Or code is cryptic

---

## Dimension 4: Discoverability (15 points)

### Title Quality (5 points)
**5 points:**
- Title is descriptive and specific
- Uses searchable keywords
- Clearly indicates error type
- Matches how developers would search

**3 points:**
- Title is somewhat descriptive
- Could be more specific
- Or uses uncommon terminology

**0 points:**
- Title is vague or generic
- Or doesn't match problem

### Tag Relevance (5 points)
**5 points:**
- 3-5 relevant tags
- Tags cover problem, solution, technologies
- Tags are searchable/common terms
- No redundant tags

**3 points:**
- 1-2 tags present
- Or tags not comprehensive
- Or tags too specific/rare

**0 points:**
- No tags
- Or irrelevant tags

### Cross-References (5 points)
**5 points:**
- Links to related entries
- References common prerequisite issues
- Links to follow-up patterns
- Bi-directional references

**3 points:**
- Some cross-references
- Or one-directional only

**0 points:**
- No cross-references

---

## Dimension 5: Actionability (15 points)

### Solution Immediacy (5 points)
**5 points:**
- Developer can implement immediately
- No external dependencies (or clearly specified)
- No ambiguity in steps
- Copy-pasteable code

**3 points:**
- Solution implementable with research
- Or some steps unclear
- Or requires significant adaptation

**0 points:**
- Solution is theoretical
- Or requires significant setup
- Or not actionable without more info

### Prevention Actionability (5 points)
**5 points:**
- Prevention guidelines are specific actions
- Includes automated detection if applicable
- Testing strategies provided
- Monitoring recommendations included

**3 points:**
- General prevention guidelines
- Or some actions not specific

**0 points:**
- Prevention is generic
- Or no prevention provided

### Examples & Context (5 points)
**5 points:**
- Multiple concrete examples
- Real-world scenario included
- Production context provided
- Common variations covered

**3 points:**
- Single basic example
- Or minimal context

**0 points:**
- No examples
- Or purely theoretical

---

## Scoring Guide

**Total Points: 100**

### Quality Levels

**90-100: Excellent ⭐⭐⭐**
- Ready for production use
- Can be used as canonical example
- Minimal improvements possible
- Exemplary entry

**75-89: Good ⭐⭐**
- High quality, useful entry
- Minor improvements would make it excellent
- Meets all critical standards

**60-74: Acceptable ⭐**
- Entry is functional and useful
- Has noticeable gaps or weaknesses
- Should be improved in next review cycle

**40-59: Needs Improvement**
- Entry has significant issues
- Should be enhanced before relying on it
- Priority for next update

**0-39: Incomplete/Problematic**
- Entry should not be used
- Requires major rework or completion
- Should be flagged for immediate attention

---

## Quality Gate Checklist

Before syncing to shared repository, entry MUST:

### Must Have (Non-negotiable)
- [ ] All required fields present and valid
- [ ] Code example compiles/runs without errors
- [ ] Solution solves stated problem
- [ ] Problem is clearly described
- [ ] Title is descriptive
- [ ] No duplicates in knowledge base
- [ ] Passes `kb.py validate`

### Should Have (High priority)
- [ ] Score ≥ 75 on quality rubric
- [ ] Prevention guidelines included
- [ ] At least 3 relevant tags
- [ ] Cross-references to related entries
- [ ] Uses current library versions
- [ ] Explains *why* solution works

### Nice to Have (Enhances quality)
- [ ] Multiple code examples
- [ ] Real-world production scenario
- [ ] Alternative approaches discussed
- [ ] Performance considerations
- [ ] Security implications noted
- [ ] Sources cited
- [ ] Version compatibility matrix

---

## Common Quality Issues

### Issue: Vague Title
**Bad:** "Import Error"
**Good:** "Circular Import Between ETL Modules"
**Why:** Specific titles are searchable and indicate scope

### Issue: No Prevention
**Bad:** Only shows how to fix current problem
**Good:** Includes guidelines to prevent recurrence
**Why:** Knowledge base should prevent problems, not just solve them

### Issue: Untested Code
**Bad:** Code looks right but unverified
**Good:** Code tested with current version
**Why:** Typos and minor errors damage credibility

### Issue: Missing Context
**Bad:** Just shows code fix
**Good:** Explains why problem occurred
**Why:** Understanding prevents similar issues

### Issue: Overly Specific
**Bad:** "FastAPI 0.98.2 WebSocket timeout on Tuesdays"
**Good:** "WebSocket Timeout in FastAPI"
**Why:** Overly specific entries don't scale across versions

### Issue: No Alternatives
**Bad:** Only one solution presented
**Good:** Notes alternative approaches with trade-offs
**Why:** Real-world solutions vary by context

### Issue: Generic Prevention
**Bad:** "Write better code" or "Be careful"
**Good:** "Use TYPE_CHECKING guard for circular imports"
**Why:** Prevention must be actionable

### Issue: Outdated Versions
**Bad:** Uses library from 3 years ago
**Good:** Tested with current version
**Why:** Outdated solutions may not work or may be deprecated

---

## Entry Lifecycle Quality Standards

### New Entry
- **Target score:** ≥ 75 (Good)
- **Minimum score:** ≥ 60 (Acceptable)
- **Required:** Pass validation, no duplicates

### Existing Entry - Routine Review
- **Maintain score:** ≥ 75
- **Improve if:** Score < 75 or outdated
- **Deprecate if:** No longer applicable or superseded

### High-Traffic Entry
- **Target score:** ≥ 90 (Excellent)
- **Review frequency:** Quarterly
- **Priority for enhancement**

### Critical Severity Entry
- **Target score:** ≥ 85 (Good-Excellent)
- **Validation:** Must be tested
- **Review frequency:** After major version updates

---

## Automated Quality Checks

These checks are performed by `kb.py validate`:

```yaml
required_fields:
  - id
  - title
  - severity
  - scope
  - problem
  - solution

id_pattern: "^[A-Z]+-\\d+$"

severity_levels:
  - critical
  - high
  - medium
  - low

scope_levels:
  - universal
  - python
  - javascript
  - typescript
  - docker
  - postgresql
  - framework
  - domain
  - project
```

Manual checks required:
- Code syntax verification
- Version currency
- Duplicate detection (semantic)
- Explanation clarity
- Prevention actionability
- Cross-reference accuracy

---

## Quality Improvement Priorities

When multiple entries need improvement, prioritize in this order:

1. **Critical severity + Low quality** (safety/impact)
2. **High traffic + Low quality** (affects many users)
3. **High severity + Medium quality** (important but usable)
4. **Medium traffic + Medium quality** (incremental improvement)
5. **All others** (backlog for gradual improvement)

---

## Example: Scoring an Entry

### Entry: IMPORT-001 (Circular Import)

**Completeness: 24/25**
- Required fields: 5/5 ✅
- Solution quality: 9/10 (excellent but could show alternative)
- Prevention: 5/5 ✅
- Metadata: 5/5 ✅

**Technical Accuracy: 23/25**
- Code correctness: 10/10 ✅
- Version currency: 8/8 ✅
- Solution effectiveness: 5/7 (works but not tested in production context)

**Clarity: 18/20**
- Problem description: 5/5 ✅
- Explanation quality: 9/10 (clear but could be more detailed on TYPE_CHECKING)
- Code documentation: 4/5 (good variable names, minimal comments)

**Discoverability: 13/15**
- Title quality: 5/5 ✅
- Tag relevance: 4/5 (good tags, could add "import-cycle")
- Cross-references: 4/5 (some but could be more)

**Actionability: 14/15**
- Solution immediacy: 5/5 ✅
- Prevention actionability: 4/5 (specific but could include testing)
- Examples: 5/5 ✅

**Total: 92/100 - Excellent ⭐⭐⭐**

This entry is production-ready and can serve as a model for other entries.

---

## Using This Rubric

### For Reviewing New Entries
1. Score entry on each dimension
2. Calculate total
3. If score < 75, request improvements
4. If score ≥ 75, approve with optional suggestions

### For Quality Audits
1. Sample entries from each category
2. Score each sampled entry
3. Identify patterns of weakness
4. Prioritize improvements by score × traffic

### For Self-Assessment
1. Before submitting entry, score yourself
2. Address low-scoring dimensions
3. Aim for ≥ 75 on all new entries
4. Strive for ≥ 90 on important topics

---

Remember: **Quality is more important than quantity.** One excellent entry helps developers more than ten mediocre ones. When in doubt, invest time in making an entry comprehensive and authoritative.
