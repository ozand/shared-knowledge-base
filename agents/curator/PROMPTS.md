# PROMPTS.md - Curator Prompt Templates

## Table of Contents

- [Reusable Prompt Templates for Common Tasks](#reusable-prompt-templates-for-common-tasks)
- [Category 1: Entry Analysis Prompts](#category-1-entry-analysis-prompts)
- [Category 2: Research & Enhancement Prompts](#category-2-research--enhancement-prompts)
- [Category 3: Content Creation Prompts](#category-3-content-creation-prompts)
- [Category 4: Review & Validation Prompts](#category-4-review--validation-prompts)
- [Category 5: Maintenance Prompts](#category-5-maintenance-prompts)
- [Category 6: External Research Prompts](#category-6-external-research-prompts)
- [Category 7: Specialized Prompts](#category-7-specialized-prompts)
- [Using These Templates](#using-these-templates)
- [Prompt Engineering Tips](#prompt-engineering-tips)

---

## Reusable Prompt Templates for Common Tasks

This document provides tested prompt templates for interacting with AI assistants (Claude, GPT, etc.) when performing Knowledge Base Curator tasks.

---

## Category 1: Entry Analysis Prompts

### Template: Analyze Entry Quality

```
Please analyze this knowledge base entry and provide a comprehensive quality assessment.

Entry Content:
```yaml
[PASTE YAML ENTRY HERE]
```

Please assess:

1. **Completeness**
   - Are all required fields present? (id, title, severity, scope, problem, solution)
   - Is the solution comprehensive with code examples?
   - Are prevention guidelines included?
   - Is metadata (tags, cross-references) present?

2. **Technical Accuracy**
   - Does the code example compile/run correctly?
   - Are imports and dependencies valid?
   - Is the solution technically sound?
   - Are library versions current?

3. **Clarity**
   - Is the problem clearly described?
   - Does the explanation cover *why* it works?
   - Is the code well-documented?

4. **Discoverability**
   - Is the title descriptive and searchable?
   - Are tags relevant and comprehensive?
   - Are there cross-references to related entries?

5. **Actionability**
   - Can a developer implement this immediately?
   - Are prevention guidelines specific and actionable?
   - Are there real-world examples?

Please provide:
- Overall quality score (0-100)
- List of strengths
- List of weaknesses
- Specific recommendations for improvement
- Priority ranking for improvements (high/medium/low)
```

### Template: Find Duplicates

```
I need you to find potential duplicate or near-duplicate entries in this knowledge base.

Target Entry:
```yaml
[PASTE ENTRY HERE]
```

Please search the knowledge base and identify:

1. **Exact Duplicates**
   - Same problem, same solution
   - Different ID, same content

2. **Near Duplicates**
   - Same problem, slightly different solution
   - Similar problem, same solution
   - Semantically equivalent but different wording

3. **Related but Distinct**
   - Same underlying concept, different context
   - Part of same problem pattern

For each potential match, provide:
- Matching entry ID
- Similarity score (0-100)
- Type of match (exact/near/related)
- Recommendation: merge/keep separate/cross-reference

Search in these scopes: [LIST SCOPES]
```

### Template: Validate Technical Content

```
Please validate the technical accuracy of this knowledge base entry.

Language/Framework: [SPECIFY]

Entry Content:
```yaml
[PASTE ENTRY HERE]
```

Please check:

1. **Code Correctness**
   - Does the code example have correct syntax?
   - Are all imports valid?
   - Will this code run without errors?

2. **API Validity**
   - Are the APIs used current?
   - Are any functions/methods deprecated?
   - Are parameters correct?

3. **Logic Correctness**
   - Does the solution actually solve the stated problem?
   - Are there any obvious bugs?
   - Does it handle edge cases?

4. **Best Practices**
   - Does the code follow language/framework conventions?
   - Is it idiomatic?
   - Are there better approaches?

Please provide:
- List of any errors found
- List of warnings (deprecated APIs, non-idiomatic code)
- Corrected code if needed
- Confidence level in your assessment
```

---

## Category 2: Research & Enhancement Prompts

### Template: Deep Research Enhancement

```
I need to enhance this knowledge base entry with comprehensive research.

Current Entry:
```yaml
[PASTE ENTRY HERE]
```

Please conduct deep research and provide:

1. **Latest Best Practices**
   - Current recommended approaches (2025/2026)
   - Official documentation recommendations
   - Community consensus on best approach

2. **Alternative Solutions**
   - What are other valid ways to solve this?
   - What are the trade-offs of each approach?
   - When would each alternative be preferred?

3. **Edge Cases & Nuances**
   - What are common edge cases?
   - Are there version-specific considerations?
   - Platform-specific nuances?

4. **Real-World Context**
   - How does this manifest in production?
   - What are the monitoring/debugging approaches?
   - What are the performance implications?

5. **Security & Performance**
   - Are there security considerations?
   - Are there performance implications?
   - Are there scalability concerns?

Please cite your sources:
- Official documentation URLs
- Stack Overflow top-voted answers
- GitHub issues with real examples
- Expert blog posts or articles
- Conference talks or tutorials

Output format: Provide enhanced content I can integrate into the YAML entry.
```

### Template: Version Update Research

```
I need to update this entry to be current with the latest library versions.

Current Entry:
```yaml
[PASTE ENTRY HERE]
```

Library/Framework: [NAME]
Current Version in Entry: [VERSION]
Latest Version: [VERSION]

Please research:

1. **Breaking Changes**
   - What changed between [OLD] and [NEW] versions?
   - Are the APIs used still valid?
   - Are there deprecations?

2. **Recommended Updates**
   - What's the current best practice in [NEW]?
   - Are there better approaches now?
   - What should the code example be?

3. **Migration Notes**
   - What do users need to know when upgrading?
   - Are there automated migration tools?
   - What are common migration pitfalls?

4. **Compatibility**
   - Is this backward compatible?
   - What versions are supported?
   - Are there environment-specific considerations?

Please provide:
- Updated code examples
- Migration guide if applicable
- Any version-specific notes
- Sources for your information
```

### Template: Gap Analysis Research

```
I need to identify gaps in our knowledge base coverage.

Technology/Topic: [SPECIFY]

Current entries we have:
- [LIST EXISTING ENTRY IDs AND TITLES]

Please research and identify:

1. **Common Errors Not Covered**
   - What are the most common errors developers encounter?
   - Which of these are not in our knowledge base?
   - Prioritize by frequency and impact

2. **Missing Patterns**
   - What are established best practices we haven't documented?
   - What are anti-patterns developers should avoid?

3. **Emerging Topics**
   - What are new developments in this area?
   - What upcoming changes should we prepare for?

4. **Advanced Topics**
   - What advanced concepts should experienced developers know?
   - What are the expert-level patterns?

For each gap, provide:
- Problem/pattern title
- Brief description
- Suggested scope (universal/language/framework)
- Priority (critical/high/medium/low)
- Suggested ID (e.g., PYTHON-XXX)
- Initial research sources

Please prioritize gaps that are:
- Common (affect many developers)
- High-impact (cause significant problems)
- Not well-documented elsewhere
```

---

## Category 3: Content Creation Prompts

### Template: Create Entry from Error

```
I need to create a knowledge base entry from this error/problem.

Error Description:
[PASTE ERROR MESSAGE OR DESCRIPTION]

Context:
- Language/Framework: [SPECIFY]
- What I was trying to do: [DESCRIBE]
- Full error/traceback: [PASTE IF APPLICABLE]
- Environment: [DESCRIBE]

Please help me create a complete knowledge base entry by providing:

1. **Entry Structure**
   - Suggested ID (follow CATEGORY-NNN format)
   - Title (descriptive and searchable)
   - Category
   - Severity (critical/high/medium/low)
   - Scope (universal/language/framework/domain/project)

2. **Problem Description**
   - Clear, concise description of the problem
   - Common symptoms/error messages
   - Root cause explanation

3. **Solution**
   - Working code example
   - Step-by-step explanation
   - Why this solution works
   - Alternative approaches if applicable

4. **Prevention**
   - How to avoid this problem
   - Best practices to follow
   - Early detection methods

5. **Metadata**
   - Relevant tags (3-5)
   - Related entries to cross-reference
   - Version-specific information

Please structure this as a YAML entry following our format.
```

### Template: Enhance Incomplete Entry

```
This knowledge base entry is incomplete and needs enhancement.

Current Entry:
```yaml
[PASTE INCOMPLETE ENTRY HERE]
```

What's missing:
[DESCRIBE WHAT'S LACKING]

Please enhance by providing:

1. **Missing Content**
   - [IF MISSING SOLUTION] Provide working code solution with explanation
   - [IF MISSING PREVENTION] Provide actionable prevention guidelines
   - [IF MISSING CONTEXT] Add real-world examples and context
   - [IF MISSING EXPLANATION] Explain why the problem occurs and solution works

2. **Enhancements**
   - Add alternative approaches with trade-offs
   - Include edge case handling
   - Add performance considerations
   - Note security implications if applicable

3. **Discoverability**
   - Suggest better title if current is vague
   - Add relevant tags
   - Identify related entries for cross-references

4. **Validation**
   - Verify code correctness
   - Check if APIs are current
   - Test solution if possible

Please provide the complete enhanced entry as YAML.
```

---

## Category 4: Review & Validation Prompts

### Template: Review Contribution

```
Please review this knowledge base contribution for quality and acceptance.

Contribution:
```yaml
[PASTE CONTRIBUTION HERE]
```

Contributor Context:
- [ANY CONTEXT PROVIDED BY CONTRIBUTOR]

Please assess:

1. **Validation**
   - Does it pass YAML validation?
   - Are all required fields present?
   - Is the ID format correct?

2. **Quality Assessment**
   - Score on each dimension (Completeness, Technical Accuracy, Clarity, Discoverability, Actionability)
   - Overall quality score (0-100)
   - Does it meet our quality threshold (≥75)?

3. **Duplicate Check**
   - Are there existing entries covering this?
   - Should this be merged with existing entries?
   - Is this complementary to existing knowledge?

4. **Technical Review**
   - Is the code correct?
   - Are APIs current?
   - Is the solution sound?

5. **Recommendations**
   - Specific improvements needed
   - Accept as-is?
   - Accept with minor revisions?
   - Reject with feedback?

Please provide constructive feedback for the contributor.
```

### Template: Merge Decision

```
I need to decide whether to merge these two entries.

Entry 1:
```yaml
[PASTE ENTRY 1]
```

Entry 2:
```yaml
[PASTE ENTRY 2]
```

Please analyze:

1. **Overlap Assessment**
   - What percentage overlap in problem description?
   - What percentage overlap in solution?
   - Are they solving the same problem?

2. **Unique Contributions**
   - What unique information does Entry 1 have?
   - What unique information does Entry 2 have?
   - Are the solutions distinct approaches?

3. **Merge Recommendation**
   - Should these be merged? (yes/no/partial)
   - If yes, which should be canonical?
   - What should the merged entry contain?

4. **Merge Plan**
   - [IF MERGING] Provide consolidated entry preserving all unique content
   - [IF KEEPING SEPARATE] Explain why and suggest cross-references
   - [IF PARTIAL] Explain what should be merged vs kept separate

Please provide specific rationale for your recommendation.
```

---

## Category 5: Maintenance Prompts

### Template: Deprecation Assessment

```
I need to assess if this entry should be deprecated.

Entry:
```yaml
[PASTE ENTRY]
```

Context:
- Entry age: [AGE]
- Last updated: [DATE]
- Library versions: [VERSIONS]
- Usage frequency: [HIGH/MEDIUM/LOW if known]

Please assess:

1. **Currency**
   - Are the library versions mentioned current?
   - Have there been major breaking changes?
   - Are the APIs used still recommended?

2. **Relevance**
   - Is this problem still encountered?
   - Has the problem been solved in newer versions?
   - Is there a better modern approach?

3. **Recommendation**
   - Keep as-is?
   - Update to current versions?
   - Deprecate with modern alternative?
   - Remove entirely (if obsolete)?

4. **Action Plan**
   - [IF DEPRECATING] What should replace this?
   - [IF UPDATING] What specific updates are needed?
   - [IF KEEPING] Is any refresh needed?

Please provide specific action items.
```

### Template: Usage Analysis

```
I have access to knowledge base usage data. Please help me analyze it.

Usage Data:
[PASTE USAGE STATISTICS OR SEARCH LOGS]

Current KB Stats:
- Total entries: [NUMBER]
- Entries by category: [BREAKDOWN]
- [OTHER RELEVANT STATS]

Please analyze:

1. **Usage Patterns**
   - Which entries are most accessed?
   - Which search terms are most common?
   - Are there seasonal trends?

2. **Gap Identification**
   - What are common search terms with no results?
   - What high-traffic entries need enhancement?
   - What topics are trending?

3. **Quality Focus**
   - Which high-traffic entries have low quality scores?
   - Which rarely-used entries could be candidates for deprecation?

4. **Recommendations**
   - Which entries should be prioritized for enhancement?
   - What new entries should be created based on search gaps?
   - What structural improvements would increase discoverability?

Please provide prioritized action items with impact estimates.
```

---

## Category 6: External Research Prompts

### Template: Perplexity Deep Research

```
Please use Perplexity to conduct comprehensive research on this topic.

Topic: [CLEARLY DESCRIBE TOPIC OR PROBLEM]

Current Knowledge:
[PASTE WHAT WE ALREADY KNOW IN KB]

Please research:

1. **Latest Developments** (2025-2026)
   - What's the current state-of-the-art?
   - Any recent breaking changes or updates?
   - Emerging best practices?

2. **Expert Consensus**
   - What do official documentation sources say?
   - What's the community consensus on Stack Overflow?
   - What do library authors/core contributors recommend?

3. **Real-World Experience**
   - What are common production experiences?
   - What are experts saying in blog posts and conferences?
   - What are the war stories and lessons learned?

4. **Comparison & Alternatives**
   - What are different approaches to this?
   - What are the trade-offs?
   - When would each be preferred?

Please provide:
- Summary of findings
- Key insights not in our current KB
- Specific recommendations for enhancing the entry
- Sources (URLs, citations)
```

### Template: Community Research

```
I need to research community consensus on this topic.

Topic/Problem: [DESCRIBE]

Please search and synthesize from:

1. **Stack Overflow**
   - Top-voted questions/answers on this topic
   - Questions with 100+ upvotes
   - Accepted best practices

2. **GitHub Issues**
   - Common issues in relevant repositories
   - Maintainer recommendations
   - Frequently asked questions

3. **Reddit & Forums**
   - Discussions on language/framework subreddits
   - Official forums/mailing lists
   - Community sentiment

4. **Official Documentation**
   - What do official docs say?
   - Are there official examples?
   - What's the recommended approach?

For each source, provide:
- URL/link
- Key insights
- Community consensus (if any)
- Relevance to our KB entry

Synthesize findings into:
- Consensus view
- Alternative approaches with trade-offs
- Recommendations for our KB entry
- Any gaps in our understanding
```

---

## Category 7: Specialized Prompts

### Template: Scope Promotion Assessment

```
I need to determine if this entry should be promoted to a more universal scope.

Current Entry:
```yaml
[PASTE ENTRY]
```

Current Scope: [SCOPE]
Proposed Scope: [UNIVERSAL/LANGUAGE/FRAMEWORK]

Please assess:

1. **Applicability**
   - Does this problem occur in multiple [LANGUAGES/FRAMEWORKS]?
   - Is the solution language/framework agnostic?
   - Could this benefit developers beyond the current scope?

2. **Universal Pattern**
   - Is there an underlying universal pattern here?
   - Can we extract the universal principle?
   - What would need to be abstracted?

3. **Promotion Plan**
   - [IF PROMOTING] What would the universal entry look like?
   - Should we keep the specific entry as an implementation example?
   - How should we cross-reference?

4. **Recommendation**
   - Promote to universal?
   - Promote to language (from framework)?
   - Keep at current scope?
   - Why?

Please provide rationale and proposed entry if promoting.
```

### Template: Cross-Reference Analysis

```
I need to identify and create cross-references for this entry.

Entry:
```yaml
[PASTE ENTRY]
```

Please analyze:

1. **Prerequisite Knowledge**
   - What concepts should a developer understand before this?
   - What errors might lead to this one?
   - What foundational knowledge is relevant?

2. **Related Issues**
   - What other errors are similar?
   - What other errors might a developer encountering this also face?
   - What's in the same problem domain?

3. **Follow-up Topics**
   - What might a developer want to learn next?
   - What advanced concepts build on this?
   - What are the natural next steps?

4. **Cross-Reference Plan**
   - List specific entry IDs to reference
   - For each, explain the relationship
   - Suggest bi-directional links

Please provide:
- List of related entries by ID
- Type of relationship (prerequisite/related/follow-up)
- Brief explanation of each relationship
```

---

## Using These Templates

### Best Practices

1. **Customize for Context**
   - Fill in placeholders with specific details
   - Add relevant context about your situation
   - Adjust specificity based on your needs

2. **Iterate**
   - Start with template
   - Refine based on results
   - Combine templates if needed

3. **Provide Context**
   - The more context you provide, the better the results
   - Include error messages, code snippets, environment details
   - Explain your goal and constraints

4. **Validate Results**
   - Always verify technical accuracy
   - Test code examples
   - Cross-check with official documentation

### Template Combinations

Some tasks work best with multiple prompts:

**Enhancement Workflow:**
1. Analyze Entry Quality
2. Deep Research Enhancement
3. Validate Technical Content
4. Create enhanced entry

**New Entry Workflow:**
1. Create Entry from Error
2. Validate Technical Content
3. Cross-Reference Analysis
4. Review Contribution

**Audit Workflow:**
1. Find Duplicates
2. Analyze Entry Quality (for each)
3. Merge Decision (if duplicates found)
4. Deprecation Assessment

---

## Prompt Engineering Tips

When modifying these templates:

1. **Be Specific**
   - "Analyze this Python import error" vs "Analyze this entry"
   - Specificity improves relevance

2. **Provide Examples**
   - Include code snippets
   - Show error messages
   - Share what you've tried

3. **Set Context**
   - Explain your goal
   - Note constraints
   - Define success criteria

4. **Request Structure**
   - Ask for specific output formats
   - Request sections or headings
   - Specify level of detail

5. **Iterative Refinement**
   - Start broad, then narrow
   - Follow up with clarifying questions
   - Build on previous responses
