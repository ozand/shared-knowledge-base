# Agent Handoff Pattern - Detailed Workflow

**Extracted from:** agent-handoff.yaml
**Pattern ID:** AGENT-HANDOFF-001

## Complete Workflow Steps

### Phase 1: Project Agent Discovers Pattern

**Role:** Project Agent (in any project using Shared KB)
**Trigger:** Encounters reusable error/solution

**Steps:**
1. Working on project task
2. Encounters error or discovers improvement
3. Searches Shared KB: `kb search "error keyword"`
4. Pattern NOT found in KB
5. Solves the problem
6. Considers: "Is this reusable for other projects?"

**Decision: Is it Reusable?**

**Questions to ask:**
- Does this apply to multiple projects/environments?
- Is this framework-agnostic or standard use case?
- Would other developers benefit?

**If YES:**
- Action: Contribute to Shared KB
- Go to Phase 2

**If NO:**
- Action: Add to project-local KB
- Steps:
  - Create entry: `docs/knowledge-base/project/errors/*.yaml`
  - Mark: `local_only: true`
  - Validate: `kb validate`
  - Commit to project repo (not shared KB)
- End

### Phase 2: Create YAML Entry

**Role:** Project Agent

**Steps:**
1. Create YAML file following KB template:

```yaml
version: "1.0"
category: "category-name"
last_updated: "2026-01-06"

errors:  # or patterns:
  - id: "CATEGORY-NNN"
    title: "Descriptive Title"
    severity: "high"
    scope: "python"  # or universal, javascript, docker, postgresql

    problem: |
      Description of problem

    root_cause: |
      Explanation

    solution:
      code: |
        # Solution code
      explanation: |
        How it works

    prevention:
      - "Prevention tip"

    tags: ["tag1", "tag2"]
```

2. Validate locally:
```bash
python tools/kb.py validate your-entry.yaml
```

3. If validation fails:
- Fix YAML syntax
- Add missing required fields
- Re-validate
- Continue until ✓ passed

### Phase 3: Create GitHub Issue

**Role:** Project Agent

**Steps:**
1. Go to: https://github.com/ozand/shared-knowledge-base
2. Click "New Issue"
3. Fill in issue template:

**Title:** "Add CATEGORY-NNN: Descriptive Title"

**Labels (IMPORTANT - for agent attribution):**
- `agent:claude-code` (or `agent:cursor-ai`, `agent:copilot`, etc.)
- `project:<PROJECT_NAME>` (e.g., `project:PARSER`)
- `agent-type:code-generation` (or `debugging`, `refactoring`, `documentation`)
- `kb-improvement`
- `enhancement` (or `bug`, `yaml-error`)
- `<language/framework>` (python, postgresql, etc.)

**Body:**
```markdown
---
**Created By:** 🤖 {{Agent Name}} (e.g., Claude Code, Cursor AI)
**Project:** {{PROJECT_NAME}}
**Agent Type:** {{task_type}} (Code Generation, Debugging, etc.)
**Session:** {{session_hash}} (optional, for tracking)
**Date:** {{YYYY-MM-DD}}
---

## Proposed KB Entry

**Type:** Error / Pattern

**Category:** language/framework name

**Entry ID:** CATEGORY-NNN

**Title:** Descriptive Title

## YAML Entry

<paste your validated YAML here>

## Validation

✅ Validated using: python tools/kb.py validate

## Real-World Example

**Project:** <your-project-name>

**Scenario:** <describe situation>

**Problem:** <what happened>

**Solution:** <how you fixed it>

## Benefit

<explain why other projects would benefit>

## Suggested Scope

**Scope:** universal / python / javascript / docker / postgresql

**Reason:** <why this scope>

## Additional Notes

<any additional context>

---

**Attribution:**
- **Created by:** 🤖 {{Agent Name}}
- **Project:** {{PROJECT_NAME}}
- **Session:** {{session_hash}}
- **Date:** {{YYYY-MM-DD}}
- **Ready for review:** ✅
```

**IMPORTANT:** The "Created By" section at the TOP makes agent attribution immediately visible in GitHub UI. The labels make it filterable.

4. Submit issue

### Phase 4: Curator Triage

**Role:** Shared KB Curator Agent (in shared-knowledge-base project)
**Trigger:** New issue with label 'kb-improvement'
**SLA:** Review within 24 hours

**Steps:**
1. Receive issue notification
2. Read issue details
3. Review YAML entry
4. Validate:
```bash
# Copy YAML to temp file
# Validate
python tools/kb.py validate temp.yaml
```

5. Check for duplicates:
```bash
kb search "title keywords"
grep -r "ID" errors/ patterns/
```

6. Assess quality:
- Problem description clear?
- Solution tested and working?
- Code examples correct?
- Appropriate scope?
- No typos, correct YAML?

7. Estimate effort:
- Small (15min): Minor edits, ready to merge
- Medium (1hr): Needs improvements, testing
- Large (2-3hr): Major rework, more examples needed

### Phase 5: Curator Enhance and Merge

**Role:** Shared KB Curator Agent

**Steps:**
1. Enhance entry if needed:
   - Improve problem description
   - Add more code examples
   - Enhance solution explanation
   - Add prevention tips
   - Fix any issues
   - Add references

2. Determine correct location:
   - Scope: universal → `universal/errors/` or `universal/patterns/`
   - Scope: python → `python/errors/` or `python/patterns/`
   - Scope: postgresql → `postgresql/errors/` or `postgresql/patterns/`
   - Scope: framework/<name> → `framework/<name>/errors/` or `patterns/`

3. Create file in appropriate location:
```bash
# Example
mv temp.yaml python/errors/async-timeout.yaml
```

4. Final validation:
```bash
python tools/kb.py validate python/errors/async-timeout.yaml
```

5. Commit to shared-knowledge-base:
```bash
git add python/errors/async-timeout.yaml
git commit -m "Add PYTHON-XXX: Async Timeout Pattern

Contributed by: <project-name>
Reviewed by: KB Curator
Validated: ✓

Pattern: Handle async timeouts correctly
Real-world: Production issue in <project-name>

🤖 Generated with Claude Code

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

6. Push to main:
```bash
git push origin main
```

7. Update index:
```bash
python tools/kb.py index --force -v
```

### Phase 6: Close Issue

**Role:** Shared KB Curator Agent

**Steps:**
1. Comment on issue:
```markdown
✅ **Merged to main!**

**Location:** `python/errors/async-timeout.yaml`

**Entry ID:** PYTHON-XXX

**Validation:** ✓ Passed

**Available in:** v5.1.1 (next release)

**Changes made:**
- <list any improvements made>

**Thank you** for your contribution! 🎉

All projects using Shared KB will benefit from this pattern.
```

2. Close issue:
```bash
gh issue close <issue-number>
```

3. (Optional) Update GitHub Release:
   - If multiple issues accumulated
   - Create release with all new entries
   - Example: "v5.1.1 - Community Contributions"

### Phase 7: Project Agent Updates

**Role:** Project Agent
**Trigger:** Issue closed by curator

**Steps:**
1. Receive notification: Issue closed
2. Read curator's comment
3. Pull latest Shared KB:
```bash
cd docs/knowledge-base/shared
git pull origin main
```

4. Update local index:
```bash
python docs/knowledge-base/tools/kb.py index --force -v
```

5. Test in project:
```bash
kb search "your pattern keywords"
# Should return your contributed entry
```

6. Update project documentation (if needed)
7. Continue using improved KB!
