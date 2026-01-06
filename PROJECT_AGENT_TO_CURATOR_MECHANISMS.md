# Project Agent → Curator Data Transmission Analysis

**Date:** 2026-01-06
**Issue:** How does locally documented KB reach Curator?
**Pattern Gap:** AGENT-HANDOFF-001 assumes GitHub issue creation, but AGENT-ROLE-SEPARATION-001 forbids it

---

## 📊 Executive Summary

**Critical Problem:** Current patterns have CONFLICTING INSTRUCTIONS

**AGENT-HANDOFF-001 (phase_3):**
```yaml
phase_3_create_github_issue:
  steps: |
    1. Go to: https://github.com/ozand/shared-knowledge-base
    2. Click "New Issue"
    3. Fill in issue template...
```

**AGENT-ROLE-SEPARATION-001:**
```yaml
forbidden_actions:
  - action: "Create PR to shared-knowledge-base"
  - action: "Suggest or prepare Curator actions"
```

**Result:** Project Agent has NO CLEAR WAY to contribute to Shared KB!

---

## 🔍 Current Mechanisms (Actual vs Documented)

### Documented in AGENT-HANDOFF-001

**Phase 3: Create GitHub Issue in shared-knowledge-base**

Steps:
1. Go to shared-knowledge-base GitHub
2. Create issue with YAML entry
3. Curator reviews and integrates

**Problem:** This violates AGENT-ROLE-SEPARATION-001!

### Actual Mechanisms (How it REALLY works)

#### Mechanism 1: User-Mediated Handoff ✅ (PRIMARY)

**How it works:**
1. Project Agent documents in project KB (docs/knowledge-base/)
2. User notices valuable patterns during work
3. User opens Shared KB project (or Curator session)
4. User shows files to Curator Agent
5. Curator analyzes, extracts, integrates

**Example from this session:**
- User: "проанализируй сообщения в чате с последнего анализа"
- Curator: Analyzed chat, extracted 3 new patterns
- Result: KB-INDEX-001, GITHUB-006, QUALITY-PROCESS-001 created

**Pros:**
- ✅ Works reliably
- ✅ User controls timing
- ✅ Curator can prioritize

**Cons:**
- ❌ Manual process
- ❌ Requires user initiative
- ❌ Not scalable
- ❌ No documented workflow

#### Mechanism 2: GitHub Issue in Project Repository ✅ (NOT DOCUMENTED)

**How it works:**
1. Project Agent creates issue in OWN project (not shared-knowledge-base)
2. Issue tagged: `kb-contribution` or similar
3. Curator periodically reviews project repos
4. Curator discovers and integrates

**Status:** NOT mentioned in any pattern!

**Example:**
```bash
# In PARSER project (NOT shared-knowledge-base)
gh issue create \
  --repo ozand/PARSER \
  --title "KB Contribution: 5 universal patterns" \
  --label "kb-contribution,documentation" \
  --body "Extracted 5 patterns in docs/knowledge-base/"
```

**Pros:**
- ✅ No role separation violation
- ✅ Project agent owns the issue
- ✅ Curator can discover proactively

**Cons:**
- ❌ Not documented
- ❌ No discovery mechanism for Curator
- ❌ No triage process

#### Mechanism 3: Git Commit in Project Repository ✅ (POTENTIAL)

**How it works:**
1. Project Agent commits to project's docs/knowledge-base/
2. Pushed to project GitHub
3. Curator monitors project repos for updates
4. Curator analyzes new/changed KB files

**Discovery options:**
- Curator manually checks repos
- Automated webhook/project monitoring
- Periodic git pull from projects

**Pros:**
- ✅ Clean separation
- ✅ Version controlled
- ✅ Agent does normal work

**Cons:**
- ❌ No monitoring system exists
- ❌ No notification mechanism
- ❌ Scalability issues (many projects)

#### Mechanism 4: Direct GitHub Issue to shared-knowledge-base ❌ (FORBIDDEN)

**Status:** VIOLATES AGENT-ROLE-SEPARATION-001

**Why forbidden:**
- Bypasses Curator quality control
- Creates role confusion
- Undermines process

**Evidence:**
- PARSER PR #4: Closed (role violation)
- PARSER Issue #15: Closed (same issue)

---

## 🎯 Pattern Conflicts

### Conflict 1: AGENT-HANDOFF-001 vs AGENT-ROLE-SEPARATION-001

| Pattern | Instruction |
|---------|-------------|
| AGENT-HANDOFF-001 | "Create GitHub issue in shared-knowledge-base" |
| AGENT-ROLE-SEPARATION-001 | "DON'T create issues/PRs to shared-knowledge-base" |

**Result:** Project Agent CANNOT follow both patterns!

### Conflict 2: "Document in project KB" - Then What?

AGENT-HANDOFF-001 says:
```yaml
if_no:
  action: "Add to project-local KB"
  steps: |
    - Create entry: docs/knowledge-base/project/errors/*.yaml
    - Mark: local_only: true
    - Validate: kb validate
    - Commit to project repo (not shared KB)
    goto: "end"
```

**Problem:** No "end" workflow defined!
- Files sit in project repo
- Curator never sees them
- Knowledge not shared
- Defeats purpose of Shared KB

---

## 💡 Proposed Solutions

### Solution A: Update AGENT-HANDOFF-001 ⭐ (RECOMMENDED)

**Change Phase 3 from:**
```yaml
phase_3_create_github_issue:
  steps: |
    1. Go to: https://github.com/ozand/shared-knowledge-base
    2. Click "New Issue"
```

**To:**
```yaml
phase_3_tag_for_discovery:
  steps: |
    1. Add metadata to YAML:
       ```yaml
       proposed_for_shared_kb: true
       shared_kb_priority: high | medium | low
       ```

    2. Create GitHub issue in YOUR project:
       ```bash
       gh issue create \
         --repo $CURRENT_PROJECT \
         --title "KB Contribution: [pattern name]" \
         --label "kb-contribution,ready-for-review" \
         --body "Pattern documented at: docs/knowledge-base/..."
       ```

    3. Commit and push to project repo

    4. Notify Curator (see notification mechanism below)
```

**Add notification mechanism:**

```yaml
phase_4_curator_notification:
  options:
    option_1_user_mediated:
      description: "User shows Curator during session"
      trigger: "User opens Curator session"
      workflow: |
        User: "Check docs/knowledge-base/ in PARSER project"
        Curator: Analyzes, extracts, integrates

    option_2_github_issue_in_shared_kb:
      description: "Create issue for CURATOR to discover"
      trigger: "User or automated system"
      workflow: |
        Create issue in shared-knowledge-base:
        Title: "Review contributions from PARSER project"
        Body: |
          Project: PARSER
          Location: docs/knowledge-base/patterns/
          Patterns: 5 proposed
          Status: Ready for Curator review

        Note: This is DIFFERENT from agent creating issue with YAML.
        This is a NOTIFICATION for Curator to investigate.

    option_3_periodic_curator_review:
      description: "Curator proactively reviews projects"
      trigger: "Scheduled (weekly/monthly)"
      workflow: |
        Curator runs: scripts/review-project-contributions.sh
        Script checks:
        - New files in docs/knowledge-base/
        - Files with proposed_for_shared_kb: true
        - Issues tagged kb-contribution
```

### Solution B: Add Discovery Mechanism

**File:** `scripts/review-project-contributions.sh`

```bash
#!/bin/bash
# Curator tool: Discover project contributions

# Known projects using Shared KB
PROJECTS=(
  "ozand/PARSER"
  "ozand/APP-SW"
  "ozand/ECOMMERCE"
  # ... more projects
)

for project in "${PROJECTS[@]}"; do
  echo "Checking $project..."

  # Check for kb-contribution issues
  gh issue list \
    --repo "$project" \
    --label "kb-contribution" \
    --state open \
    --json title,url,body | jq '.'

  # Check for new KB files (if repo accessible)
  # git clone / check for new files in docs/knowledge-base/
done
```

### Solution C: Update AGENT-ROLE-SEPARATION-001

**Clarify what IS allowed:**

```yaml
permitted_actions:
  - action: "Create kb-contribution issue in OWN project"
    example: |
      gh issue create \
        --repo ozand/PARSER \
        --label "kb-contribution" \
        --body "Pattern at: docs/knowledge-base/pattern-x.yaml"

  - action: "Tag YAML files for discovery"
    metadata:
      proposed_for_shared_kb: true
      shared_kb_priority: high
      ready_for_review: true
```

---

## 📋 Recommended Implementation

### Phase 1: Immediate (Pattern Updates)

1. **Update AGENT-HANDOFF-001:**
   - Remove "create issue in shared-knowledge-base"
   - Add "create issue in own project with kb-contribution label"
   - Add "tag YAML files with proposed_for_shared_kb"

2. **Update AGENT-ROLE-SEPARATION-001:**
   - Add permitted_actions section
   - Explicitly allow project repo issues
   - Clarify notification vs contribution

### Phase 2: Short-term (Discovery Tools)

1. **Create curator review script:**
   - `scripts/review-project-contributions.sh`
   - Checks project repos for contributions
   - Generates summary report

2. **Add project registry:**
   - `curator/projects.yaml` - list of known projects
   - Auto-discoverable via GitHub org

### Phase 3: Long-term (Automated Discovery)

1. **GitHub Actions integration:**
   - Webhook on project repo changes
   - Auto-notifies Curator repo
   - Creates triage issues

2. **Curator dashboard:**
   - View all project contributions
   - Prioritize review queue
   - Track integration status

---

## 🎓 Current Real-World Workflow

### How it ACTUALLY works today:

```
1. Project Agent documents in: docs/knowledge-base/
2. Files sit in project repo
3. User notices during work
4. User asks Curator: "проанализируй сообщения в чате"
5. Curator analyzes chat
6. Curator extracts patterns
7. Curator integrates into Shared KB
```

**Problems:**
- ❌ Ad-hoc, manual
- ❌ Relies on user noticing
- ❌ Not documented
- ❌ Not scalable
- ❌ Pattern conflicts confuse agents

---

## ✅ Success Criteria

After implementation:

- [ ] AGENT-HANDOFF-001 updated with correct workflow
- [ ] AGENT-ROLE-SEPARATION-001 permits project repo issues
- [ ] Discovery mechanism created
- [ ] Review script functional
- [ ] Project registry established
- [ ] Pattern conflicts resolved
- [ ] Clear path from project → Curator

---

## 📊 Comparison Table

| Mechanism | Documented | Scalable | Automatic | No Role Violation |
|-----------|------------|----------|-----------|-------------------|
| User-mediated handoff | ❌ | ❌ | ❌ | ✅ |
| Project repo issue | ❌ | ⚠️ | ❌ | ✅ |
| Git commit monitoring | ❌ | ⚠️ | ✅ | ✅ |
| Direct Shared KB issue | ✅ | ✅ | ❌ | ❌ |
| **Proposed solution** | ✅ | ✅ | ✅ | ✅ |

---

## 🚀 Next Steps

1. **Immediate:**
   - Document current workflow (user-mediated)
   - Add to AGENT-HANDOFF-001 as phase_3_alt

2. **Short-term:**
   - Create discovery script
   - Update patterns to resolve conflicts

3. **Long-term:**
   - Implement automated notifications
   - Build Curator dashboard

---

**Analysis Date:** 2026-01-06
**Analyst:** Shared KB Curator Agent
**Pattern Gaps Identified:** 2 critical conflicts
**Recommendation:** Update AGENT-HANDOFF-001 + create discovery mechanism
