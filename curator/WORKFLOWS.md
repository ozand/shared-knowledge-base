# WORKFLOWS.md - Knowledge Base Curator Workflows

## Detailed Standard Operating Procedures

This document provides step-by-step workflows for common Knowledge Base Curator tasks.

---

## Workflow 1: Review New Contribution

**Trigger:** User submits new entry or PR

**Goal:** Validate, improve, and integrate new knowledge

### Steps

1. **Initial Validation**
   ```bash
   python tools/kb.py validate path/to/new-entry.yaml
   ```
   - Check YAML syntax
   - Verify required fields present
   - Confirm ID format (CATEGORY-NNN)
   - Ensure severity is valid level

2. **Duplicate Detection**
   ```bash
   python tools/kb.py search --tags "tag1,tag2"
   python tools/kb.py search "problem keyword"
   ```
   - Search by title keywords
   - Search by tags
   - Search by error symptoms
   - Check for semantically similar entries

3. **Scope Verification**
   - Assess if scope is correct
   - Consider: Could this be more universal?
   - Consider: Is this too specific for shared KB?
   - Verify scope hierarchy: universal → language → framework → domain → project

4. **Technical Validation**
   - Check code syntax
   - Verify imports are correct
   - Test solution if possible
   - Check API versions are current
   - Validate error messages

5. **Enhancement Research**
   - Query Perplexity: "Best practices for [problem]"
   - Check official documentation
   - Review Stack Overflow for consensus
   - Search GitHub issues for real-world cases
   - Verify against latest library version

6. **Quality Enhancement**
   - Add missing prevention guidelines
   - Include real-world examples
   - Add cross-references to related entries
   - Improve code comments
   - Expand explanation if unclear
   - Add tags for discoverability

7. **Determine Location**
   - If scope is universal (docker, universal, python, postgresql, javascript):
     - Create in: `docs/knowledge-base/shared/<scope>/errors/`
     - Plan to sync to repository
   - If scope is project-specific (project, domain, framework):
     - Create in: `docs/knowledge-base/<scope>/errors/`
     - Add metadata: `local_only: true`

8. **Integration**
   - Move file to appropriate location
   - Update any cross-references
   - Rebuild index: `python tools/kb.py index --force -v`

9. **Synchronization (if universal)**
   ```bash
   cd docs/knowledge-base/shared
   git add <file>
   git commit -m "Add ERROR-ID: Title

   - Brief description
   - Related issues
   - Real-world example

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
   git push origin main
   ```

10. **Confirmation**
    - Verify entry appears in search
    - Confirm commit in repository
    - Notify user of integration status

### Success Criteria
- ✅ Entry passes all validation checks
- ✅ No duplicates in knowledge base
- ✅ Code examples are technically correct
- ✅ Solution is based on authoritative sources
- ✅ Entry is discoverable via search
- ✅ Universal entries are synced to repository

---

## Workflow 2: Comprehensive Quality Audit

**Trigger:** Scheduled maintenance (quarterly/monthly) or after major updates

**Goal:** Assess and improve overall knowledge base quality

### Steps

1. **Establish Baseline**
   ```bash
   python tools/kb.py stats
   ```
   - Record total entries
   - Note entries by category
   - Identify largest/smallest categories
   - Document current statistics

2. **Sample Selection**
   - Select 20% of entries from each category
   - Prioritize:
     - Most frequently accessed (if usage data available)
     - High severity entries
     - Recently modified entries
     - Entries older than 1 year

3. **Duplicate Analysis**
   - Group entries by title keywords
   - Check for overlapping problem descriptions
   - Identify similar solutions
   - Create merge candidate list
   - Calculate similarity scores

4. **Technical Validation Batch**
   - Extract all code examples
   - Validate syntax for each language
   - Check for deprecated APIs
   - Verify imports exist
   - Test random sample of solutions

5. **Currency Check**
   - Identify entries with version-specific content
   - Check current versions of libraries/frameworks
   - Flag entries >6 months old for version review
   - Document breaking changes

6. **Completeness Assessment**
   For each sampled entry, verify:
   - Required fields present (id, title, severity, scope, problem, solution)
   - Code examples present and correct
   - Prevention guidelines included
   - Tags are accurate and useful
   - Cross-references where appropriate

7. **External Verification**
   - For high-severity entries:
     - Research current best practices
     - Verify against official docs
     - Check for community consensus
   - For old entries:
     - Confirm still relevant
     - Check for better solutions

8. **Gap Identification**
   - Analyze search logs (if available)
   - Review recent project issues
   - Check industry trends
   - Survey Stack Overflow for common errors
   - Document missing topics

9. **Prioritization Matrix**
   Create list of improvements prioritized by:
   - Impact (how many developers affected)
   - Severity (criticality of errors)
   - Effort (time to fix)
   - Value (improvement in quality)

10. **Execute Improvements**
    - Merge duplicates
    - Update outdated entries
    - Enhance incomplete entries
    - Create missing entries
    - Deprecate obsolete entries

11. **Documentation**
    - Create audit report with:
      - Entries reviewed
      - Issues found
      - Actions taken
      - Recommendations for future
      - Quality score trends

12. **Communication**
    - Share findings with team
    - Highlight critical issues found
    - Showcase improvements made
    - Suggest process changes

### Success Criteria
- ✅ 95%+ of sampled entries pass quality checks
- ✅ All duplicates identified and merged
- ✅ Outdated entries updated or deprecated
- ✅ Critical gaps filled
- ✅ Quality score improved from baseline

---

## Workflow 3: Deep Research Enhancement

**Trigger:** Important entry needs comprehensive enhancement

**Goal:** Transform basic entry into authoritative, comprehensive resource

### Steps

1. **Entry Selection**
   - Identify high-value entry (high traffic, high severity)
   - Assess current quality level
   - Determine enhancement potential
   - Confirm not already recently enhanced

2. **Initial Analysis**
   ```bash
   python tools/kb.py search --id "ERROR-ID"
   cat path/to/entry.yaml
   ```
   - Read current entry thoroughly
   - Identify weaknesses:
     - Shallow explanation?
     - Missing examples?
     - No prevention guidance?
     - Outdated information?
     - No cross-references?

3. **Research Planning**
   Create research plan covering:
   - Official documentation sources
   - Community discussion venues
   - Expert blog posts/articles
   - Academic/research papers (if applicable)
   - Related library/framework changelogs

4. **Deep Research Execution**

   **Phase 1: Authoritative Sources**
   - Read official documentation
   - Review API reference
   - Check official examples
   - Document official recommendations

   **Phase 2: Community Consensus**
   - Search Stack Overflow for top-voted answers
   - Read GitHub issues on related repos
   - Review Reddit discussions
   - Check official forums/mailing lists

   **Phase 3: Expert Perspectives**
   - Read blog posts from core contributors
   - Watch conference talks on topic
   - Review curated tutorials
   - Check open source project examples

   **Phase 4: Current Verification**
   - Query Perplexity: "[topic] best practices 2025/2026"
   - Verify against latest versions
   - Check for recent breaking changes
   - Confirm no better solutions emerged

5. **Synthesis**
   - Compile findings from all sources
   - Identify consensus vs. debate
   - Extract key insights
   - Note alternative approaches
   - Document trade-offs

6. **Entry Enhancement**

   **Structure:**
   ```yaml
   problem: |
     Enhanced with real-world context
     Add frequency indicators
     Include impact assessment

   solution:
     code: |
       # Add comprehensive, production-ready example
       # Include error handling
       # Add logging/monitoring

     explanation: |
       Expand with:
       - Why this works
       - Common pitfalls
       - Performance considerations
       - Security implications
       - Alternative approaches

   prevention: |
     Add specific, actionable guidelines
     Include automated detection
     Suggest testing strategies

   related_versions: |
     Document version-specific nuances
     Add migration guides

   real_world_example: |
     Add actual production scenario
     Include monitoring setup
     Document debugging approach
   ```

7. **Cross-Reference Enhancement**
   - Link to related entries
   - Create bidirectional references
   - Note dependencies
   - Suggest reading order

8. **Validation**
   - Test all code examples
   - Verify all links work
   - Confirm version accuracy
   - Check consistency

9. **Citation**
   Add sources section:
   ```yaml
   sources:
     - "Official documentation: URL"
     - "Stack Overflow: URL (top answer)"
     - "Library author blog: URL"
     - "Perplexity research: DATE"
   ```

10. **Review & Commit**
    - Read enhanced entry end-to-end
    - Confirm it's now comprehensive
    - Commit with detailed message
    - Sync if universal scope

### Success Criteria
- ✅ Entry covers problem comprehensively
- ✅ Multiple authoritative sources cited
- ✅ Community consensus reflected
- ✅ Code examples are production-ready
- ✅ Multiple solution approaches documented
- ✅ Prevention and monitoring included
- ✅ Entry is self-contained and actionable

---

## Workflow 4: Duplicate Detection & Merge

**Trigger:** Routine maintenance or suspicion of duplicates

**Goal:** Consolidate duplicate knowledge into canonical entries

### Steps

1. **Candidate Identification**
   ```bash
   # Find potential duplicates by keywords
   python tools/kb.py search "import error"
   python tools/kb.py search --tags "circular-import"

   # Find entries with similar titles
   grep -r "circular" **/*.yaml
   ```

2. **Similarity Analysis**
   For each candidate pair:
   - Compare problem descriptions
   - Compare solutions
   - Compare scopes
   - Assess overlap percentage

3. **Classification**
   - **Exact duplicate:** Same problem, same solution → Merge
   - **Partial duplicate:** Same problem, different solutions → Keep separate, cross-reference
   - **Related but distinct:** Similar concept, different application → Keep separate, link
   - **Same problem, different scope:** Consider promoting to universal

4. **Canonical Selection**
   Choose canonical entry based on:
   - Most complete (most fields filled)
   - Most recently updated
   - Most accurate (validated)
   - Broadest applicable scope
   - Better code examples

5. **Merge Planning**
   Create merge plan documenting:
   - Which entry is canonical
   - What to preserve from each
   - How to combine code examples
   - How to merge tags
   - Which IDs to deprecate

6. **Execution**
   - Open canonical entry
   - Add unique content from other entries
   - Combine all prevention strategies
   - Merge tags (deduplicate)
   - Add alternative solutions if distinct
   - Expand examples with all variations
   - Document deprecation of old IDs

7. **Deprecation**
   For each merged (non-canonical) entry:
   ```yaml
   deprecated: true
   deprecated_by: "CANONICAL-ID"
   deprecated_reason: "Merged into CANONICAL-ID"
   migration_guide: |
     This entry has been merged into CANONICAL-ID.
     All content has been preserved and enhanced.
   ```

8. **Cross-Reference Updates**
   - Find all entries referencing deprecated IDs
   - Update to reference canonical ID
   - Search codebase for mentions (if applicable)

9. **Index Rebuild**
   ```bash
   python tools/kb.py index --force -v
   ```

10. **Verification**
    - Search for old IDs, should show deprecation notice
    - Search for canonical ID, should show merged content
    - Confirm no information lost

### Success Criteria
- ✅ No duplicate content remains
- ✅ All unique information preserved
- ✅ Clear migration path from deprecated entries
- ✅ Search returns canonical entry
- ✅ Cross-references updated

---

## Workflow 5: Knowledge Gap Analysis

**Trigger:** Strategic planning or after completing audit

**Goal:** Identify and prioritize missing knowledge

### Steps

1. **Data Collection**
   - Gather available search logs
   - Collect recent project issues
   - Review error tracking (Sentry, etc.)
   - Survey team members
   - Monitor relevant forums/communities

2. **Pattern Analysis**
   - Identify recurring error patterns
   - Note frequently asked questions
   - Find common stumbling blocks
   - Detect complex topics with sparse documentation

3. **External Research**
   - Stack Overflow: Common questions for technologies used
   - GitHub: Open issues in popular repos
   - Reddit: r/learnprogramming, language-specific subreddits
   - Official docs: Known issues or FAQ sections
   - Google Trends: Rising search queries

4. **Gap Categorization**
   For each potential gap:
   - **Scope:** Universal, language, framework, domain?
   - **Frequency:** How often does this occur?
   - **Impact:** How severe is the problem?
   - **Complexity:** How difficult to solve/understand?
   - **Availability:** Is this well-documented elsewhere?

5. **Prioritization Matrix**
   Create list scoring each gap on:
   - Frequency × Impact = Priority Score
   - Consider:
     - High frequency + high impact = CRITICAL
     - High frequency + low impact = HIGH
     - Low frequency + high impact = MEDIUM
     - Low frequency + low impact = LOW

6. **Entry Planning**
   For high-priority gaps:
   - Draft problem statement
   - Determine appropriate scope
   - Identify needed research
   - Estimate effort to create
   - Assign suggested ID

7. **Drafting & Research**
   For top N gaps (start with 5-10):
   - Research best practices
   - Create draft entries
   - Validate technical accuracy
   - Add comprehensive examples
   - Test solutions

8. **Review & Refine**
   - Validate drafts with team
   - Test with real scenarios if possible
   - Refine based on feedback
   - Add cross-references

9. **Integration**
   - Add to knowledge base
   - Rebuild index
   - Sync to repository if universal
   - Monitor usage

10. **Iterative Improvement**
    - Track which gaps get most use
    - Refine based on feedback
    - Continue filling lower-priority gaps
    - Re-assess periodically

### Success Criteria
- ✅ High-priority gaps filled
- ✅ New entries validated and tested
- ✅ Search gaps reduced
- ✅ Team feedback positive

---

## Workflow 6: Currency Update Cycle

**Trigger:** Scheduled (monthly) or after major dependency updates

**Goal:** Keep knowledge base current with latest versions

### Steps

1. **Version Inventory**
   - List all libraries/frameworks mentioned in KB
   - Note current versions in entries
   - Check latest released versions
   - Identify version gaps

2. **Changelog Review**
   For each outdated library:
   - Review changelog for breaking changes
   - Note deprecations
   - Identify new recommended approaches
   - Document version-specific nuances

3. **Affected Entry Identification**
   ```bash
   grep -r "fastapi" **/*.yaml
   grep -r "0.100" **/*.yaml
   ```
   - Find all entries mentioning outdated versions
   - Tag entries for review

4. **Update Strategy**
   For each affected entry:
   - **Minor version bump:** May not need update
   - **Major version bump:** Likely needs update
   - **Deprecated features:** Must update
   - **Breaking changes:** Must update

5. **Execution**
   - Update version-specific code examples
   - Add migration notes
   - Update related_versions field
   - Add "Upgraded from X to Y" notes
   - Test with new versions

6. **Deprecation Handling**
   For entries about deprecated features:
   ```yaml
   deprecated_approach: true
   modern_alternative: "NEW-ERROR-ID"
   migration_guide: |
     This approach is deprecated as of version X.
     See MODERN-ALTERNATIVE for current approach.
   ```

7. **Documentation**
   - Document all updates made
   - Note any breaking changes encountered
   - Record version compatibility matrix
   - Update GUIDE.md if needed

8. **Communication**
   - Notify team of major updates
   - Highlight breaking changes
   - Suggest migration projects review KB

### Success Criteria
- ✅ All critical version gaps addressed
- ✅ Code examples work with current versions
- ✅ Deprecated approaches clearly marked
- ✅ Migration paths documented

---

## Workflow 7: Pull Request Review

**Trigger:** New PR opened in Shared Knowledge Base repository

**Goal:** Thoroughly review PR before merge to ensure quality, prevent duplicates, and maintain standards

### Steps

1. **Access PR Details**
   ```bash
   # Get PR overview
   gh pr view <number> --json title,body,additions,deletions,files,author,state

   # List changed files
   gh pr diff <number> --name-only

   # Get full description
   gh pr view <number> --json body --jq .body
   ```

2. **Categorize PR Type**
   - **Bug Fix:** Resolves error or issue
   - **New Pattern:** Adds new knowledge entry
   - **Tool Update:** Modifies kb*.py tools
   - **Documentation:** Updates README, guides
   - **Refactoring:** Code reorganization

3. **Clone & Isolate PR Branch**
   ```bash
   cd /tmp
   rm -rf pr-test
   mkdir pr-test && cd pr-test
   git clone git@github.com:ozand/shared-knowledge-base.git .
   git fetch origin pull/<number>/head:pr-branch
   git checkout pr-branch
   ```

4. **Validate YAML Syntax (if applicable)**
   ```bash
   # Validate all changed YAML files
   for file in $(gh pr diff <number> --name-only | grep '\.yaml$'); do
     python tools/kb.py validate "$file"
   done
   ```

5. **Check for Duplicates (CRITICAL for new patterns)**
   ```bash
   # Extract keywords from PR title/description
   # Search for similar entries
   python tools/kb.py search "<keyword1>"
   python tools/kb.py search "<keyword2>"
   python tools/kb.py search "<keyword3>"
   ```

6. **Test Affected Tools**
   ```bash
   # Test all v3.0 tools if code changes
   python tools/kb_patterns.py find-universal --kb-root /tmp/pr-test
   python tools/kb_community.py report --kb-root /tmp/pr-test
   python tools/kb_predictive.py suggest-entries --kb-root /tmp/pr-test
   python tools/kb_issues.py scan --kb-root /tmp/pr-test
   ```

7. **Code Quality Review**
   - **PEP 8 Compliance:** Check formatting, naming
   - **Type Hints:** Verify proper typing
   - **Documentation:** Check docstrings, comments
   - **Error Handling:** Verify exception handling
   - **Testing:** Check if tests exist/work

8. **Verify No Breaking Changes**
   ```bash
   # Run existing tests
   python -m pytest tools/tests/ 2>/dev/null || echo "No test suite"

   # Test basic KB operations
   python tools/kb.py validate .
   python tools/kb.py search "test"
   python tools/kb.py index -v
   ```

9. **Assess Completeness**
   - ✅ Problem clearly defined
   - ✅ Solution tested and working
   - ✅ Examples provided
   - ✅ Cross-references added
   - ✅ Documentation updated
   - ✅ Tags appropriate

10. **Create Review Document**
    - Create file: `PR<NUMBER>_REVIEW.md` in repository root
    - Include sections:
      - Executive Summary (rating, decision)
      - Problem Analysis
      - Testing Results
      - Code Quality Review
      - Issues Found (if any)
      - Recommendation

11. **Post Review on GitHub**
    ```bash
    # Post review comment
    gh pr comment <number> --body "<review summary>"

    # Official review decision
    gh pr review <number> --approve --body "<detailed review>"
    # OR
    gh pr review <number> --request-changes --body "<blocking issues>"
    ```

**Review Template:**
```markdown
## PR Review: #[number] - [PR Title]

**Date:** YYYY-MM-DD
**Reviewer:** Shared KB Curator Agent
**PR Author:** @username
**PR URL:** https://github.com/ozand/shared-knowledge-base/pull/<number>

---

### 📊 Executive Summary

**Decision:** [APPROVE / APPROVE WITH SUGGESTIONS / REQUEST CHANGES]

**Rating:** ⭐⭐⭐⭐⭐ (X/5)

---

### 🎯 Problem Analysis

[Describe the problem PR is solving]

---

### 🧪 Testing Results

**Before PR:**
```bash
[Test results showing issue]
```

**After PR:**
```bash
[Test results showing fix]
```

---

### ⭐ Code Quality

- ✅ PEP 8 compliant
- ✅ Type hints used
- ✅ Well documented
- ✅ No breaking changes

---

### ✅ Review Checklist

- ✅ Problem clearly defined
- ✅ Solution tested
- ✅ Code quality meets standards
- ✅ No breaking changes
- ✅ No duplicates (if new pattern)
- ✅ YAML validation passes
- ✅ All tools work
- ✅ Cross-references added
- ✅ Documentation updated

---

### 🎯 Decision

**[MERGE / CHANGE / DISCUSS]**

[Detailed reasoning]

---

**Review Date:** YYYY-MM-DD
**Reviewer:** Shared KB Curator Agent
```

### Success Criteria
- ✅ All validation checks pass
- ✅ No duplicates introduced
- ✅ Code quality meets standards
- ✅ No breaking changes
- ✅ All v3.0 tools work correctly
- ✅ Review document created
- ✅ GitHub comment posted

### Common Issues to Flag

**For New Patterns:**
- Duplicate or near-duplicate content
- Missing required YAML fields
- Incorrect scope classification
- Lack of real-world examples
- Missing cross-references

**For Bug Fixes:**
- Fix not thoroughly tested
- Breaking changes introduced
- No regression testing
- Missing test cases

**For Tool Updates:**
- Backward compatibility broken
- Import errors
- Missing error handling
- No documentation update

**For Documentation:**
- Outdated information
- Inaccurate examples
- Missing critical details
- Unclear instructions

### Output Artifacts

1. **PR#_REVIEW.md** - Comprehensive review document
2. **GitHub Comment** - Summary posted on PR
3. **Official Review** - Via `gh pr review` command
4. **Follow-up Issues** (if needed) - For non-blocking improvements

### Examples

- **PR #6:** PR6_REVIEW.md - kb_config.py fix (APPROVED ⭐⭐⭐⭐½)
- **PR #4:** PARSER_PROJECT_AGENT_ANALYSIS.md - 5 new patterns (APPROVED ⭐⭐⭐⭐)

---

## Workflow: Interactive Decision Tree

Use this flow when unsure which workflow to apply:

```
                    ┌─────────────────┐
                    │  What's the     │
                    │  situation?     │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌────▼────┐         ┌────▼────┐
   │  New    │         │ Problem │         │ Routine │
   │  entry  │         │ with    │         │ task    │
   │  added  │         │ existing│         │         │
   └────┬────┘         └────┬────┘         └────┬────┘
        │                   │                   │
        │              ┌────▼────┐              │
        │              │ Quality │              │
        │              │ issues? │              │
        │              └────┬────┘              │
        │                   │                   │
        │              ┌────┴────┐              │
        │           ┌───┴───┐  ┌───┴───┐        │
        │           │  Yes  │  │  No   │        │
        │           └───┬───┘  └───┬───┘        │
        │               │          │            │
        │               │     ┌────▼────┐        │
        │               │     │ Duplicate?│      │
        │               │     └────┬────┘        │
        │               │          │            │
        │               │     ┌────┴────┐       │
        │               │  ┌───┴───┐  ┌──┴───┐   │
        │               │  │  Yes  │  │  No  │   │
        │               │  └───┬───┘  └──┬───┘   │
        │               │       │         │      │
        │               │       │    ┌────▼────┐ │
        │               │       │    │ Need    │ │
        │               │       │    │ research?│
        │               │       │    └────┬────┘
        │               │       │         │
        │               │       │    ┌────┴────┐
        │               │       │ ┌───┴───┐  ┌──┴───┐
        │               │       │ │  Yes  │  │  No  │
        │               │       │ └───┬───┘  └──┬───┘
        │               │       │     │        │
        ▼               ▼       ▼     ▼        ▼
┌──────────────┐ ┌──────────┐ ┌──────┐ ┌──────────┐ ┌──────────┐
│Review        │ │Quality   │ │Merge │ │Deep      │ │Scheduled │
│Contribution  │ │Audit     │ │Entry │ │Research  │ │Update    │
│              │ │          │ │      │ │Enhance   │ │Cycle     │
└──────────────┘ └──────────┘ └──────┘ └──────────┘ └──────────┘
```

## Best Practices

- **Always validate** before making changes
- **Research thoroughly** before enhancing
- **Communicate clearly** about changes
- **Document decisions** for future reference
- **Test assumptions** when possible
- **Preserve information** during merges
- **Think universally** when categorizing
- **Be conservative** with deprecation
- **Iterate** rather than perfect immediately
- **Collaborate** on major changes
