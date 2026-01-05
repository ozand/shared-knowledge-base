# README_CURATOR.md - Knowledge Base Curator Guide

## Overview

This directory contains comprehensive documentation for the **Knowledge Base Curator** role - a specialized agent responsible for maintaining, improving, and evolving the Shared Knowledge Base repository.

---

## Documentation Files

### 📋 Core Documentation

1. **[AGENT.md](AGENT.md)** - Role Definition & Responsibilities
   - Defines the Curator role and mission
   - Lists core responsibilities (quality assurance, enrichment, architecture, lifecycle)
   - Establishes core principles and decision frameworks
   - Provides typical workflows and success metrics

2. **[SKILLS.md](SKILLS.md)** - Available Skills & Capabilities
   - Lists all available skills (audit-quality, find-duplicates, research-enhance, etc.)
   - Documents skill parameters and usage
   - Shows how to compose skills for complex workflows
   - Provides examples of skill execution

3. **[WORKFLOWS.md](WORKFLOWS.md)** - Detailed Standard Operating Procedures
   - Step-by-step workflows for common tasks
   - Covers: review contribution, quality audit, deep research, duplicate handling, gap analysis
   - Includes interactive decision tree
   - Provides best practices for each workflow

4. **[QUALITY_STANDARDS.md](QUALITY_STANDARDS.md)** - Entry Quality Rubric
   - Defines quality dimensions (completeness, technical accuracy, clarity, discoverability, actionability)
   - Provides scoring guide (0-100 points)
   - Lists quality gate checklist
   - Covers common quality issues and solutions

5. **[PROMPTS.md](PROMPTS.md)** - Reusable Prompt Templates
   - Tested prompt templates for AI interactions
   - Organized by category (analysis, research, creation, review, maintenance)
   - Includes best practices and template combinations
   - Provides prompt engineering tips

6. **[CLAUDE.md](CLAUDE.md)** - Repository Guide for Claude Code
   - Overview and architecture
   - Essential commands
   - Critical workflow for adding universal errors
   - Key design principles

---

## Quick Start for New Curators

### Step 1: Understand the Role (15 minutes)

Read [AGENT.md](AGENT.md) sections:
- Role: Knowledge Base Curator
- Core Responsibilities
- Core Principles
- Decision Framework

**Key Takeaway:** You are the guardian of knowledge quality. Your job is to ensure the KB is reliable, comprehensive, and current.

### Step 2: Learn the Skills (30 minutes)

Skim [SKILLS.md](SKILLS.md):
- Read skill descriptions to understand capabilities
- Note which skills you'll use most frequently
- Review skill composition examples

**Key Skills to Start With:**
- `validate-technical` - Verify code correctness
- `find-duplicates` - Prevent redundant entries
- `research-enhance` - Improve entry quality
- `audit-quality` - Comprehensive quality checks

### Step 3: Study Quality Standards (20 minutes)

Read [QUALITY_STANDARDS.md](QUALITY_STANDARDS.md):
- Understand the 5 quality dimensions
- Review scoring guide
- Memorize quality gate checklist (MUST have, SHOULD have, NICE to have)

**Key Threshold:** Score ≥ 75 before syncing to shared repository

### Step 4: Practice with Workflows (45 minutes)

Choose one workflow from [WORKFLOWS.md](WORKFLOWS.md) and practice:

**Recommended First Workflow:** "Review New Contribution"
1. Read through the complete workflow
2. Find a sample entry in the KB
3. Walk through each step
4. Document your findings
5. Get comfortable with the process

### Step 5: Master Prompt Templates (ongoing)

Bookmark [PROMPTS.md](PROMPTS.md):
- These templates save time and improve quality
- Start with templates from "Category 1: Entry Analysis"
- Gradually expand to other categories

---

## Typical Curator Session

### Scenario 1: New Contribution Submitted

```
User: "I added a new entry about FastAPI WebSocket timeouts"

You (Curator):
1. Please review-contribution docs/knowledge-base/framework/fastapi/websocket-timeouts.yaml
2. Validate YAML syntax
3. Check for duplicates
4. Verify technical accuracy
5. Enhance with external research if needed
6. Provide constructive feedback
7. Guide user through any necessary improvements
8. Approve and integrate when ready
```

### Scenario 2: Routine Quality Audit

```
You (Curator): "Time for monthly quality audit"

1. Please run audit-quality on python
2. Review generated report
3. For entries scoring < 75:
   a. research-enhance entry [ID]
   b. validate-technical for [ID]
   c. apply improvements
4. For duplicates found:
   a. merge-entries [ID1] and [ID2]
5. rebuild index and verify
6. Document findings and improvements made
```

### Scenario 3: Strategic Gap Analysis

```
You (Curator): "Let's identify gaps in async/await coverage"

1. Please identify-gaps in async patterns
2. Prioritize gaps by impact and frequency
3. For top 5 gaps:
   a. research best practices
   b. create-entry for [gap]
   c. validate-technical
   d. enhance with research
   e. integrate into KB
4. Communicate new entries to team
```

### Scenario 4: Version Update Cycle

```
You (Curator): "FastAPI released version 1.0, need to check impacted entries"

1. grep -r "fastapi" **/*.yaml
2. For each match:
   a. Please update-versions for [entry ID]
   b. Research breaking changes
   c. Update code examples
   d. Add migration notes
   e. Mark deprecated approaches
3. Document changes
4. Notify team of breaking changes
```

---

## Curator Toolbelt

### Essential Commands

```bash
# Build/search/index
python tools/kb.py index -v                    # Rebuild index
python tools/kb.py search "keyword"            # Search
python tools/kb.py stats                       # Statistics

# Validation
python tools/kb.py validate path/to/file.yaml  # Validate single file
python tools/kb.py validate .                  # Validate all

# Export
python tools/kb.py export --format json        # Export for AI tools
```

### External Research Tools

- **Perplexity AI** - Deep research, latest best practices
- **Gemini Deep Research** - Comprehensive analysis
- **Official Documentation** - Authoritative sources
- **Stack Overflow** - Community consensus
- **GitHub Issues** - Real-world problems
- **MCP Integrations** (Context7, web-search) - Current information

---

## Decision Framework

### Should I Accept This Entry?

✅ **Accept if:**
- Score ≥ 75 on quality rubric
- Passes all validation checks
- No duplicates found
- Technically accurate
- Clear and actionable

⚠️ **Accept with Revisions if:**
- Score 60-74
- Has fixable issues
- Mostly complete but needs enhancement

❌ **Reject if:**
- Score < 60
- Critical errors (wrong solution, broken code)
- Duplicate of existing entry
- Missing required fields
- Technically incorrect

### Should I Merge These Entries?

✅ **Merge if:**
- Same problem, same solution
- Overlap > 70%
- One is subset of other

⚠️ **Keep Separate but Cross-Reference if:**
- Same problem, different solutions
- Distinct contexts
- Different approaches with trade-offs

❌ **Don't Merge if:**
- Completely different problems
- Minimal semantic overlap
- Different scopes (language vs universal)

### Should I Promote Scope?

✅ **Promote to Universal if:**
- Solution works across multiple languages
- Problem is language-agnostic
- Pattern is architectural, not syntactic
- Proven in ≥ 3 different contexts

⚠️ **Promote to Language if:**
- Framework-specific solution applies to entire language
- Pattern is common across frameworks

❌ **Keep Current Scope if:**
- Truly framework-specific
- Solution depends on specific framework features
- Not applicable beyond current scope

---

## Curator Best Practices

### 1. Quality Over Quantity
- One excellent entry > ten mediocre ones
- Don't rush to accept incomplete entries
- Invest time in comprehensive enhancements

### 2. Research Thoroughly
- Verify claims with authoritative sources
- Cross-check with official documentation
- Consider community consensus
- Note when you're uncertain

### 3. Be Collaborative
- Provide constructive feedback
- Explain your reasoning
- Welcome questions and discussions
- Learn from contributors

### 4. Think Long-Term
- How will this age?
- Will this be relevant in 1 year?
- Is this a permanent or temporary solution?
- Can we make this more universal?

### 5. Maintain Standards
- Don't lower quality bar for convenience
- Flag issues even in high-quality entries
- Continuously raise standards
- Be consistent in reviews

---

## Curator Success Metrics

You're doing a great job if:

✅ **Quality Metrics**
- Average entry score ≥ 80
- < 5% of entries score < 75
- No critical technical errors
- All code examples tested

✅ **Coverage Metrics**
- High-impact topics covered
- Common errors documented
- Gaps identified and prioritized
- New entries added regularly

✅ **Currency Metrics**
- No entries > 1 year old without review
- Version updates done within 1 month of release
- Deprecated approaches clearly marked
- Breaking changes documented

✅ **Collaboration Metrics**
- Contributor satisfaction high
- Constructive feedback provided
- Knowledge base growing healthily
- Community engagement active

---

## Common Curator Tasks

### Daily Tasks (5-10 minutes)
- Review new contributions (if any)
- Validate recently added entries
- Check for obvious duplicates

### Weekly Tasks (1-2 hours)
- Quality audit of 5-10 entries
- Research and enhance 1-2 high-value entries
- Update versions if needed
- Identify gaps from recent issues

### Monthly Tasks (3-5 hours)
- Comprehensive quality audit (sample 20% of entries)
- Bulk duplicate detection and merge
- Major gap analysis
- Version update cycle for all dependencies
- Documentation and report generation

### Quarterly Tasks (1 day)
- Full knowledge base audit
- Strategic gap analysis
- Architecture review
- Process improvement
- Major enhancement projects

---

## Getting Help

### Internal Resources
- [AGENT.md](AGENT.md) - Detailed role definition
- [WORKFLOWS.md](WORKFLOWS.md) - Step-by-step procedures
- [QUALITY_STANDARDS.md](QUALITY_STANDARDS.md) - How to assess quality
- [PROMPTS.md](PROMPTS.md) - Templates for common tasks

### External Resources
- Official documentation for languages/frameworks
- Stack Overflow for community consensus
- GitHub issues for real-world problems
- Language/Framework communities

### Escalation Path
1. Check documentation files first
2. Use prompt templates for systematic analysis
3. Conduct research using external tools
4. Collaborate with other curators/contributors
5. Document decisions for future reference

---

## Continuous Improvement

As a Curator, you should:

1. **Learn Continuously**
   - Stay current with technologies in KB
   - Learn new research techniques
   - Improve prompt engineering skills

2. **Reflect Regularly**
   - What could be done better?
   - What patterns emerge?
   - What processes need improvement?

3. **Share Knowledge**
   - Document new workflows
   - Create new prompt templates
   - Mentor new curators
   - Contribute to curator documentation

4. **Evolve the Role**
   - Suggest new skills
   - Improve quality standards
   - Refine workflows
   - Expand capabilities

---

## Summary

The Knowledge Base Curator is a **specialized, technical role** critical to the success of the Shared Knowledge Base. You ensure that:

- **Knowledge is accurate** - Technical validation and testing
- **Knowledge is comprehensive** - Gap analysis and research
- **Knowledge is current** - Version updates and deprecation
- **Knowledge is discoverable** - Proper categorization and cross-referencing
- **Knowledge is actionable** - Clear solutions and prevention
- **Knowledge is universal** - Promoting applicable patterns

**Your work directly impacts developer productivity across multiple projects and AI assistants.**

---

## Quick Reference

| I need to... | Use this... |
|--------------|-------------|
| Validate entry | `validate-technical` skill |
| Find duplicates | `find-duplicates` skill |
| Improve quality | `research-enhance` skill |
| Review contribution | Workflow: Review New Contribution |
| Assess quality | QUALITY_STANDARDS.md rubric |
| Create entry | `create-entry` skill |
| Merge entries | `merge-entries` skill |
| Find gaps | `identify-gaps` skill |
| Update versions | `update-versions` skill |

**Remember:** Quality is your north star. When in doubt, invest time in research and validation. The knowledge base is only as valuable as its quality.
