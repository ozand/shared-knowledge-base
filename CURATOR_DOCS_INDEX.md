# 📚 Knowledge Base Curator Documentation Index

This directory contains comprehensive documentation for the **Knowledge Base Curator** role - enabling systematic maintenance, enhancement, and evolution of the Shared Knowledge Base.

---

## 🎯 What is the Knowledge Base Curator?

The Curator is a specialized agent role responsible for ensuring the knowledge base remains:
- **Accurate** - Technically validated and tested
- **Comprehensive** - Covers common problems and patterns
- **Current** - Up-to-date with latest versions
- **Actionable** - Clear solutions and prevention
- **Universal** - Promoting broadly applicable patterns

---

## 📖 Documentation Map

### For New Curators
Start here: **[README_CURATOR.md](README_CURATOR.md)**
- Quick start guide (30 minutes)
- Typical curator sessions
- Essential commands and tools
- Common curator tasks

### Core Reference Documents

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[AGENT.md](AGENT.md)** | Role definition & responsibilities | Understanding the curator mission |
| **[SKILLS.md](SKILLS.md)** | Available skills & capabilities | Finding the right tool for the job |
| **[WORKFLOWS.md](WORKFLOWS.md)** | Standard operating procedures | Step-by-step task execution |
| **[QUALITY_STANDARDS.md](QUALITY_STANDARDS.md)** | Entry quality rubric | Assessing entry quality (0-100) |
| **[PROMPTS.md](PROMPTS.md)** | AI prompt templates | Researching and enhancing entries |
| **[CLAUDE.md](CLAUDE.md)** | Repository guide for Claude Code | Understanding KB architecture |

---

## 🚀 Quick Start (5 Minutes)

### 1. Understand the Role
Read **[AGENT.md](AGENT.md)** - Sections:
- Role: Knowledge Base Curator
- Core Responsibilities
- Core Principles

### 2. Learn Key Skills
Browse **[SKILLS.md](SKILLS.md)** for:
- `validate-technical` - Verify code correctness
- `find-duplicates` - Find and merge duplicates
- `research-enhance` - Deep research improvement
- `audit-quality` - Comprehensive quality checks

### 3. Master Quality Standards
Review **[QUALITY_STANDARDS.md](QUALITY_STANDARDS.md)**:
- 5 quality dimensions (100 points total)
- Quality gate checklist
- Target: ≥ 75 points before syncing to repository

### 4. Practice Workflows
Pick one workflow from **[WORKFLOWS.md](WORKFLOWS.md)**:
- Review New Contribution (start here)
- Comprehensive Quality Audit
- Deep Research Enhancement

### 5. Use Prompt Templates
Bookmark **[PROMPTS.md](PROMPTS.md)**:
- Category 1: Entry Analysis
- Category 2: Research & Enhancement
- Category 3: Content Creation

---

## 🎨 Curator Workflow Examples

### Example 1: Reviewing New Entry
```
1. User submits new entry
2. Please review-contribution path/to/entry.yaml
3. Validate YAML: kb validate entry.yaml
4. Check duplicates: kb search --tags "tag1,tag2"
5. Please validate-technical for ENTRY-ID
6. Please research-enhance entry ENTRY-ID
7. Assess quality: Score on 5 dimensions (QUALITY_STANDARDS.md)
8. Provide feedback or approve
9. If universal scope: Sync to repository
10. Rebuild index: kb index --force -v
```

### Example 2: Quality Audit
```
1. Please run audit-quality on python
2. Review audit report
3. For low-scoring entries (< 75):
   a. Please research-enhance entry ID
   b. Please validate-technical for ID
   c. Apply improvements
4. For duplicates:
   a. Please merge-entries ID1 and ID2
5. Document findings
6. Rebuild index
```

### Example 3: Gap Analysis
```
1. Please identify-gaps in "FastAPI websockets"
2. Prioritize gaps by impact
3. For top 5 gaps:
   a. Research best practices
   b. Please create-entry for [problem]
   c. Validate and enhance
   d. Integrate into KB
4. Monitor usage of new entries
```

---

## 🛠️ Essential Tools

### KB Tool (kb.py)
```bash
# Search
python tools/kb.py search "keyword"

# Validate
python tools/kb.py validate path/to/file.yaml

# Statistics
python tools/kb.py stats

# Index
python tools/kb.py index -v

# Export
python tools/kb.py export --format json
```

### External Research
- **Perplexity AI** - Deep research on topics
- **Gemini Deep Research** - Comprehensive analysis
- **Official Documentation** - Authoritative sources
- **Stack Overflow** - Community consensus
- **GitHub Issues** - Real-world problems

---

## 📊 Quality Thresholds

| Score Range | Quality Level | Action |
|-------------|---------------|--------|
| 90-100 | ⭐⭐⭐ Excellent | Canonical example, minimal improvement needed |
| 75-89 | ⭐⭐ Good | Meets standards, minor improvements optional |
| 60-74 | ⭐ Acceptable | Functional but needs improvement |
| 40-59 | Needs Improvement | Significant issues, prioritize for update |
| 0-39 | Incomplete | Requires major rework or completion |

**Minimum for Shared Repository:** ≥ 75 points

---

## 🔄 Typical Curator Tasks

### Daily (5-10 min)
- Review new contributions
- Validate recent entries
- Check for obvious duplicates

### Weekly (1-2 hours)
- Quality audit of 5-10 entries
- Enhance 1-2 high-value entries
- Update versions if needed

### Monthly (3-5 hours)
- Comprehensive audit (20% of entries)
- Bulk duplicate detection
- Version update cycle
- Gap analysis

### Quarterly (1 day)
- Full knowledge base audit
- Strategic planning
- Process improvement
- Major enhancements

---

## 📋 Quick Decision Guide

### Should I accept this entry?
✅ Yes - if score ≥ 75, validates, no duplicates, technically accurate
⚠️ Revise - if score 60-74, fixable issues
❌ No - if score < 60, critical errors, duplicate

### Should I merge these entries?
✅ Yes - if same problem/solution, overlap > 70%
⚠️ Cross-reference - if same problem, different solutions
❌ No - if different problems, minimal overlap

### Should I promote scope?
✅ To universal - if works across languages, architectural pattern
✅ To language - if framework-specific → language-wide
❌ Keep current - if truly framework-specific

---

## 🎓 Learning Path

### Week 1: Foundations
- Read AGENT.md completely
- Learn key skills from SKILLS.md
- Study quality rubric in QUALITY_STANDARDS.md
- Practice "Review New Contribution" workflow

### Week 2: Practice
- Review 5-10 real entries
- Practice using prompt templates
- Conduct mini quality audit
- Enhance 2-3 entries

### Week 3: Advanced
- Lead full quality audit
- Conduct gap analysis
- Handle complex merges
- Create new entries from scratch

### Week 4: Mastery
- Improve curator processes
- Create new prompt templates
- Mentor new curators
- Contribute to documentation

---

## 💡 Curator Principles

1. **Quality Over Quantity** - One excellent entry > ten mediocre ones
2. **Research Thoroughly** - Verify claims, check authoritative sources
3. **Be Collaborative** - Provide constructive feedback, welcome discussion
4. **Think Long-Term** - How will this age? Is it future-proof?
5. **Maintain Standards** - Don't lower bar for convenience

---

## 📞 Getting Help

### Step 1: Check Documentation
- [AGENT.md](AGENT.md) - Role and responsibilities
- [WORKFLOWS.md](WORKFLOWS.md) - Step-by-step procedures
- [QUALITY_STANDARDS.md](QUALITY_STANDARDS.md) - Quality assessment
- [PROMPTS.md](PROMPTS.md) - Research templates

### Step 2: Use Tools
- KB tool: `python tools/kb.py help`
- Prompt templates from PROMPTS.md
- External research services

### Step 3: Collaborate
- Discuss with other curators
- Get feedback from contributors
- Consult community resources

---

## 🎯 Success Indicators

You're successful when:
- ✅ Average entry score ≥ 80
- ✅ < 5% of entries score < 75
- ✅ No critical technical errors
- ✅ High-impact topics covered
- ✅ Common errors documented
- ✅ Versions updated within 1 month of release
- ✅ Duplicates consolidated
- ✅ Gaps identified and prioritized
- ✅ Contributor satisfaction high

---

## 📝 Documentation Version

**Version:** 1.0
**Last Updated:** 2026-01-05
**Maintained By:** Knowledge Base Curator Community

---

## 🚀 Start Now

1. Read [README_CURATOR.md](README_CURATOR.md) - 5 min
2. Browse [AGENT.md](AGENT.md) - 10 min
3. Skim [SKILLS.md](SKILLS.md) - 10 min
4. Review [QUALITY_STANDARDS.md](QUALITY_STANDARDS.md) - 15 min
5. Practice one workflow from [WORKFLOWS.md](WORKFLOWS.md) - 30 min

**Total Investment:** ~70 minutes to become a productive Knowledge Base Curator

---

**Remember:** The knowledge base serves developers and AI assistants. Everything you do should make it more useful, reliable, and comprehensive. **Quality is your north star.** ⭐
