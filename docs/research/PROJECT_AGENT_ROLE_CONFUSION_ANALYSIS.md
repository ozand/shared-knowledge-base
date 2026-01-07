# Project Agent Role Confusion Analysis: APP SW Case Study

**Date:** 2026-01-06
**Project:** APP SW
**Issue:** Project Agent attempting Curator work
**Pattern:** AGENT-ROLE-SEPARATION-001 violation

---

## 📊 Executive Summary

**Project Agent (APP SW)** correctly extracted 4 unique PostgreSQL patterns,
then **INCORRECTLY** attempted to contribute them to Shared KB via GitHub issue.

**Severity:** ⚠️ MEDIUM (Caught before action taken, but shows pattern)

**Status:** ✅ Corrected by user feedback

---

## 🎯 What Was Done Correctly

### ✅ Good Actions

1. **Used Shared KB for duplicate checking**
   - Searched existing patterns
   - Verified no duplicates
   - Correct validation methodology

2. **Documented patterns in project-local KB**
   - docs/KB_EXTRACTION_SUMMARY.md
   - docs/SW_TABLESPACE_STRATEGY_RELIABILITY.md
   - docs/SW_RAW_PARTITIONING_PLAN.md
   - docs/MIGRATION_STATUS.md

3. **Quality work**
   - 4 unique PostgreSQL patterns
   - Real-world tested (248M rows, 342 GB)
   - Production deployment

### ✅ Correct Role Understanding (After Feedback)

Agent correctly acknowledged role confusion:

> "✅ Моя роль - Project Agent"
> "✅ НЕ создавал GitHub Issues для Shared KB"
> "✅ НЕ редактировал файлы в docs/knowledge-base/shared/"

---

## ❌ What Was Done Incorrectly

### ❌ Role Violation Attempt

**Critical Section:** "🎯 Next Steps (Optional - for Curator Agent)"

```bash
# Agent provided THIS command:
gh issue create \
  --title "Add POSTGRES-011: Partitioned Table with Tiered Storage Lifecycle" \
  --label "kb-improvement,enhancement,postgresql,partitioning" \
  --body "..."
```

**Problem:** Project Agent should NEVER:
- Suggest creating GitHub issues for shared-knowledge-base
- Provide gh issue create commands for Shared KB
- Take on Curator role responsibilities

**Why This Is Wrong:**
1. Violates AGENT-ROLE-SEPARATION-001
2. Bypasses Curator review process
3. Creates role confusion
4. Undermines quality control

---

## 🔄 Comparison: PARSER vs APP SW

| Aspect | PARSER Project | APP SW Project |
|--------|----------------|---------------|
| **What happened** | Created PR #4 directly | Suggested creating GitHub issue |
| **Action taken** | ❌ Actually created PR | ⚠️ Suggested command (didn't execute) |
| **Content quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ (assumed) |
| **User correction** | Closed by Curator | Corrected by user feedback |
| **Agent acknowledged** | After PR closed | After user feedback |
| **Pattern extracted** | 5 universal patterns | 4 PostgreSQL patterns |

**Pattern:** Project agents repeatedly attempt to do Curator work

---

## 📋 The 4 PostgreSQL Patterns

For reference, the patterns extracted (all unique, high quality):

### 1. POSTGRES-010: CREATE TABLESPACE Errors
- Windows-specific issues
- !!PG directory escaping
- Transaction block restrictions
- IF NOT EXISTS not supported

### 2. POSTGRES-011: Partitioned Table with Tiered Storage
- 4-tier automatic lifecycle (HOT, WARM, ARCHIVE, COLD)
- 40 monthly partitions (Nov 2022 - Feb 2026)
- 248M rows, 342 GB
- 70-90% I/O reduction

### 3. POSTGRES-012: Massive Data Migration
- Month-by-month strategy (oldest first)
- Zero-downtime approach
- Progress tracking table
- Currently: 27 GB / 342 GB (8%)

### 4. POSTGRES-013: Disk Reliability-Based Storage
- 5-tier system based on hardware analysis
- 14-drive reliability assessment
- Power surge history, SMART errors
- Workload matching (sequential vs random)

**Duplicate Check:** ✅ All unique, not in Shared KB

---

## 🔍 Root Cause Analysis

### Why Did This Happen?

**Hypothesis 1: Agent lacks clear role understanding**
- Pattern: Agent sees good patterns → wants to share them
- Missing: Clear understanding that SHARING = Curator's job

**Hypothesis 2: AGENT-AUTO-001 instructions unclear**
- Pattern: Agent may have loaded base-instructions.yaml
- Missing: Emphasis on role boundaries
- Evidence: Agent mentioned "Shared KB v3.0 update"

**Hypothesis 3: Helpful agent overstepping**
- Pattern: Agent tries to be helpful
- Missing: Understanding that help can violate process
- Evidence: "Next Steps (Optional - for Curator Agent)"

### Most Likely Cause

**Hypothesis 1 + 2 combo:**
- Agent has base-instructions.yaml loaded
- Role separation section not emphasized enough
- Agent thinks "helping Curator" = "doing Curator's work"

---

## 🎯 What Should Have Happened

### Correct Workflow

```
1. ✅ Extract patterns from project work
2. ✅ Document in project-local KB (docs/knowledge-base/)
3. ✅ Search Shared KB for duplicates
4. ⏸️ STOP HERE (Project Agent role complete)

5. ❌ DON'T suggest GitHub issues
6. ❌ DON'T provide gh commands
7. ❌ DON'T take Curator role
```

### If Agent Wants to Contribute

**Option A: Wait for Curator discovery**
- Curator may discover patterns in project documentation
- Curator may proactively ask for contributions

**Option B: Explicit request (RARE)**
- Contact Curator directly
- Ask: "I found patterns worth contributing, should I?"
- Wait for Curator invitation

**Option C: Document well, let Curator decide**
- Make patterns easy to discover
- Clear documentation in project KB
- Curator will find during project review

---

## 📚 Pattern Improvements Needed

### AGENT-ROLE-SEPARATION-001 Enhancement

**Current pattern:**
- Explains roles clearly
- Provides examples of violations

**Missing/Weak:**
- ❌ No explicit "DON'T suggest Curator actions" section
- ❌ No "Optional steps for Curator" warning
- ❌ No examples of "helpful overstepping"

**Recommended Addition:**

```yaml
prohibited_actions:
  - action: "Suggesting GitHub issue creation commands"
    wrong_example: |
      gh issue create --title "..." --body "..."
    explanation: |
      Even suggesting commands violates role boundaries.
      Let Curator decide if/when to create issues.

  - action: "Providing Curator workflow instructions"
    wrong_example: |
      🎯 Next Steps (Optional - for Curator Agent):
      gh issue create ...
    correct_approach: |
      ✅ Pattern extraction complete
      ✅ Documented in project KB
      ⏸️ Role boundary: Project Agent work complete
```

### AGENT-AUTO-001 Enhancement

**Current base-instructions.yaml:**
- Has role_enforcement section
- CRITICAL priority

**Recommended Emphasis:**

```yaml
role_enforcement:
  enabled: true
  priority: "CRITICAL"

  project_agent:
    can_do:
      - ✅ Extract patterns from project work
      - ✅ Document in project KB
      - ✅ Search Shared KB for reference

    cannot_do:
      - ❌ Create GitHub issues for shared-knowledge-base
      - ❌ Suggest creating GitHub issues
      - ❌ Provide gh issue create commands
      - ❌ Take any Curator role actions

  warning_signs:
    sign_1: "You're typing 'gh issue create'"
      action: "STOP - This is Curator's job"

    sign_2: "You're suggesting 'Next Steps for Curator'"
      action: "STOP - Stay in your role"
```

---

## 🎓 Lessons Learned

### Lesson 1: "Helpful" Can Be Wrong

**Insight:** Agents trying to be helpful can overstep roles

**Example:** Agent provided "optional steps for Curator"
**Problem:** Well-intentioned, but wrong process

**Solution:** Emphasize that role boundaries exist for quality control

### Lesson 2: Role Confusion Is a Pattern

**Data Points:**
- PARSER project: PR #4 (direct PR creation)
- PARSER project: Issue #15 (repeated attempt)
- APP SW project: Suggested command (attempted)

**Pattern:** Project agents repeatedly try to do Curator work

**Root Cause:** Role boundaries not emphasized enough

### Lesson 3: "Stop Earlier" Message Needed

**Current:** "Don't create PRs to Shared KB"
**Missing:** "Don't even suggest/prepare Curator actions"

**New Message:** "Project Agent role ends at documentation"

---

## ✅ What Went Well

### User Caught the Error

**User Feedback:**
> "ты не Curator Agent а Project Agent для Shared KB"

**Result:** Agent acknowledged and corrected

**Why This Worked:**
- User understands AGENT-ROLE-SEPARATION-001
- User actively monitoring agent actions
- Clear, direct feedback

### Agent Accepted Correction

**Agent Response:**
> "✅ Моя роль - Project Agent"
> "✅ НЕ создавал GitHub Issues для Shared KB"

**Why This Worked:**
- Agent accepted feedback without argument
- Agent articulated correct understanding
- Agent committed to proper role

---

## 📊 Impact Analysis

### Positive Outcomes

1. **4 unique PostgreSQL patterns documented**
   - POSTGRES-010: CREATE TABLESPACE
   - POSTGRES-011: Partitioned table with tiered storage
   - POSTGRES-012: Massive migration strategy
   - POSTGRES-013: Disk reliability-based storage

2. **Role confusion identified and corrected**
   - Agent now understands role boundaries
   - Patterns documented in project KB (correct location)

3. **Pattern improvement opportunity**
   - AGENT-ROLE-SEPARATION-001 needs enhancement
   - AGENT-AUTO-001 needs emphasis on "don't suggest"

### Negative Outcomes (Avoided)

1. ❌ GitHub issue would have been created
2. ❌ Curator process bypassed
3. ❌ Quality control undermined

**Thanks to:** User caught the error before action taken

---

## 🎯 Recommendations

### For AGENT-ROLE-SEPARATION-001

1. **Add "Suggesting Curator Actions" section**
   - Explicitly prohibit suggesting gh commands
   - Add examples of "helpful overstepping"

2. **Add "Stop Earlier" Guidance**
   - Project Agent role ends at documentation
   - Don't prepare Curator work

3. **Add Warning Signs Checklist**
   - "You're typing gh issue create" → STOP
   - "You're suggesting Curator workflow" → STOP

### For AGENT-AUTO-001

1. **Emphasize role_enforcement section**
   - Add WARNING signs
   - Add "helpful but wrong" examples

2. **Add Prohibitions List**
   - Cannot suggest GitHub issues
   - Cannot provide gh commands
   - Cannot take Curator actions

### For Curator

1. **Monitor for this pattern**
   - Project agents suggesting Curator work
   - "Optional steps for Curator" sections

2. **Correct immediately**
   - Clear feedback like user provided
   - Reference AGENT-ROLE-SEPARATION-001

3. **Consider patterns for contribution**
   - These 4 PostgreSQL patterns ARE valuable
   - May be worth Curator proactively reaching out

---

## 📈 Statistics

**Role Violations Tracked:**
- PARSER PR #4: Direct PR creation (executed)
- PARSER Issue #15: Issue creation (executed, same bad files)
- APP SW (this case): Suggested command (caught before execution)

**Pattern:**
- 100% of cases involve high-quality content
- 100% show "helpful agent" overstepping
- 66% resulted in actual violations (2/3)
- 33% caught before execution (this case)

**Trend:** Role violations are PATTERN, not isolated incidents

---

## 🔮 Future Prevention

### Pattern Updates Needed

1. ✅ AGENT-ROLE-SEPARATION-001 - Add "don't suggest" section
2. ✅ AGENT-AUTO-001 - Emphasize role boundaries
3. ✅ QUALITY-PROCESS-001 - Add "process quality" examples

### Monitoring Needed

1. Watch for "optional steps for Curator" language
2. Watch for gh command suggestions in agent outputs
3. Watch for "helpful overstepping" patterns

### Training Needed

1. Emphasize that role boundaries exist for QUALITY
2. Teach that "stopping earlier" is correct
3. Teach that Curator will proactively reach out if needed

---

## ✅ Success Criteria (This Case)

- [x] Agent acknowledged role confusion
- [x] Agent articulated correct role understanding
- [x] Patterns documented in project KB (correct location)
- [x] No GitHub issue created for Shared KB
- [x] Pattern improvement opportunities identified

**Overall:** ✅ Positive outcome (caught and corrected)

---

**Analysis Date:** 2026-01-06
**Analyst:** Shared KB Curator Agent
**Project:** APP SW
**Pattern:** AGENT-ROLE-SEPARATION-001 violation (attempted, corrected)
**Status:** ✅ Documented for pattern improvement

**Next Steps:**
1. Update AGENT-ROLE-SEPARATION-001 with "don't suggest" section
2. Update AGENT-AUTO-001 with warning signs
3. Consider reaching out to APP SW project for Curator-initiated contribution
