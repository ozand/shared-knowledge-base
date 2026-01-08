# Agent Quick Start Guide
## Working with Shared Knowledge Base

**Version:** 1.0
**Last Updated:** 2026-01-06
**Applies to:** All AI Agents working with Shared KB

---

## Table of Contents

1. [Critical Rules](#critical-rules)
2. [Git Submodule Workflow](#git-submodule-workflow)
3. [Contributing to KB](#contributing-to-kb)
4. [Common Pitfalls](#common-pitfalls)
5. [Verification Checklist](#verification-checklist)

---

## Critical Rules

### ⚠️ CRITICAL: Role Separation

**If you are a Project Agent:**
- ✅ Can: Search KB, validate YAML, create GitHub issues
- ❌ CANNOT: Commit to shared-knowledge-base, create PRs, modify KB files

**If you are Curator Agent:**
- ✅ Can: Review issues, validate, commit to KB, create PRs
- ❌ Only agent who commits to KB

**Pattern:** AGENT-ROLE-SEPARATION-001

---

### ⚠️ CRITICAL: Git Submodule Access

**NEVER use direct git commands on submodule:**

```bash
# ❌ WRONG - Direct access
git -C docs/knowledge-base/shared fetch origin
cd docs/knowledge-base/shared && git pull
git -C /home/ozand/docs/knowledge-base/shared log HEAD..origin/main
```

**ALWAYS use git submodule commands:**

```bash
# ✅ CORRECT - Submodule commands from project root
git submodule status docs/knowledge-base/shared
git submodule update --remote docs/knowledge-base/shared
git submodule update --init --recursive docs/knowledge-base/shared
```

**Pattern:** AGENT-DIRECT-SUBMODULE-ACCESS-001

---

## Git Submodule Workflow

### Step 1: Check Submodule Status

```bash
git submodule status docs/knowledge-base/shared
```

**Output interpretation:**
- ` c023036...` (leading space) = ✅ Properly initialized, up to date
- `-c023036...` (minus sign) = ❌ Not initialized
- `+c023036...` (plus sign) = ⚠️ Uncommitted changes

**Pattern:** SUBMODULE-STATUS-INTERPRETATION-001

### Step 2: Update Submodule

```bash
git submodule update --remote docs/knowledge-base/shared
```

**What this does:**
- Fetches latest changes from submodule remote
- Merges them into submodule
- Updates superproject's git link to submodule
- Maintains .gitmodules synchronization

### Step 3: Verify Update

```bash
git submodule status docs/knowledge-base/shared
```

**Success indicators:**
- Commit hash changed (if updates were applied)
- No output from update command (already up to date)
- Still has leading space (properly initialized)

### Step 4: Use KB Tools

```bash
python3 docs/knowledge-base/shared/tools/kb.py stats
python3 docs/knowledge-base/shared/tools/kb.py search "query"
```

---

## Contributing to KB

### Complete Workflow

**1. Search KB First**
```bash
python3 docs/knowledge-base/shared/tools/kb.py search "pattern keywords"
```
If pattern exists, don't create duplicate.

**2. Create YAML Entry Locally**
```bash
# In your PROJECT repository (NOT shared-knowledge-base)
cat > universal/patterns/my-pattern.yaml << 'EOF'
version: "1.0"
category: "pattern-category"
last_updated: "2026-01-06"

patterns:
  - id: "PATTERN-001"
    title: "Pattern Title"
    severity: "high"
    scope: "universal"
    tags: ["tag1", "tag2", "tag3"]

    problem: |
      Detailed problem description
      with multiple paragraphs

    root_cause: |
      Explanation of root cause

    solution: |
      Step-by-step solution

    code_example: |
      ```bash
      # Code example
      command here
      ```
EOF
```

**3. Validate YAML**
```bash
python3 docs/knowledge-base/shared/tools/kb.py validate universal/patterns/my-pattern.yaml
```

Fix any errors before proceeding.

**4. Create GitHub Issue with FULL YAML**

```bash
gh issue create \
  --repo shared-knowledge-base \
  --label "agent:claude-code" \
  --label "project:YOUR_PROJECT" \
  --label "agent-type:pattern-contribution" \
  --label "kb-improvement" \
  --label "pattern-category" \
  --title "Add PATTERN-001: Pattern Title" \
  --body-file issue-template.md
```

**Critical: Issue MUST include:**
- ✅ FULL YAML content embedded (not just file path)
- ✅ All required fields
- ✅ Validation confirmation
- ✅ Proper attribution (agent, project, date)

**Pattern:** AGENT-HANDOFF-001

**5. Wait for Curator Review**
- Expected SLA: 24 hours
- Curator validates, enhances, commits to KB

**6. Pull KB Updates**
```bash
git submodule update --remote docs/knowledge-base/shared
```

---

## Common Pitfalls

### Pitfall 1: External File Reference

**❌ WRONG:**
```markdown
## Proposed Entry

**ID:** PATTERN-001
**Title:** Pattern Title

The complete YAML file is located at:
docs/knowledge-base/shared/universal/patterns/pattern.yaml

File size: 9.2KB
```

**Why wrong:** Curator cannot access your local filesystem.

**✅ CORRECT:**
```markdown
## Proposed Entry

**Full YAML content:**

```yaml
version: "1.0"
category: "pattern-category"
# ... complete 9.2KB YAML content
```
```

**Pattern:** AGENT-HANDOFF-FAILURE-001

---

### Pitfall 2: Direct Submodule Access

**❌ WRONG:**
```bash
git -C docs/knowledge-base/shared fetch origin
cd docs/knowledge-base/shared && git status
```

**Why wrong:** Breaks .gitmodules synchronization, submodule workflow integrity.

**✅ CORRECT:**
```bash
git submodule status docs/knowledge-base/shared
git submodule update --remote docs/knowledge-base/shared
```

**Pattern:** AGENT-DIRECT-SUBMODULE-ACCESS-001

---

### Pitfall 3: Stale Context

**❌ WRONG:**
```
"Waiting for Issue #11 to merge"
```

**Why wrong:** Issue #11 might already be closed from previous session.

**✅ CORRECT:**
```bash
gh issue view 11 --json state,title
# Output: {"state":"CLOSED", "title":"..."}
# Response: Issue #11 already CLOSED
```

**Pattern:** STALE-CONTEXT-001

---

### Pitfall 4: Missing YAML Validation

**❌ WRONG:**
```
Create issue without validating YAML
→ Issue closed with syntax errors
```

**✅ CORRECT:**
```bash
python3 docs/knowledge-base/shared/tools/kb.py validate pattern.yaml
# Output: ✓ Validation passed
# Then create issue
```

**Pattern:** YAML-001

---

### Pitfall 5: Assuming Issue State

**❌ WRONG:**
```
"Refer to Issue #11 for pattern details"
```

**Why wrong:** Issue state might have changed.

**✅ CORRECT:**
```bash
ISSUE_STATE=$(gh issue view 11 --json state --jq '.state')
if [ "$ISSUE_STATE" = "OPEN" ]; then
  echo "Issue #11 still open"
else
  echo "Issue #11 already $ISSUE_STATE"
fi
```

**Pattern:** STALE-CONTEXT-001

---

## Verification Checklist

### Before Creating GitHub Issue

- [ ] Searched KB for duplicates
- [ ] Created YAML in PROJECT repository (not KB)
- [ ] Validated YAML locally (`kb validate`)
- [ ] **FULL YAML embedded in issue body** (not just file path)
- [ ] All required fields present
- [ ] Proper attribution labels added

### Before Git Submodule Operations

- [ ] Checked `git submodule status` first
- [ ] Using `git submodule` commands (not `git -C` or `cd`)
- [ ] Working from project root (not inside submodule)
- [ ] Path is relative from project root

### Before Referencing GitHub Issues/PRs

- [ ] Verified current state with `gh issue view` or `gh pr view`
- [ ] Checked if still OPEN (not CLOSED/MERGED)
- [ ] Not assuming state from previous session

---

## Quick Reference Commands

### KB Operations
```bash
# Search KB
kb search "query"

# Validate YAML
kb validate pattern.yaml

# KB statistics
kb stats

# Update KB
git submodule update --remote docs/knowledge-base/shared
```

### GitHub Operations
```bash
# Check issue state
gh issue view NUMBER --json state,title

# Check PR state
gh pr view NUMBER --json state,merged,title

# Create issue
gh issue create --repo shared-knowledge-base --body-file template.md
```

### Submodule Operations
```bash
# Check status
git submodule status path/to/submodule

# Update submodule
git submodule update --remote path/to/submodule

# Initialize submodule
git submodule update --init --recursive path/to/submodule
```

---

## Related Patterns

- **AGENT-ROLE-SEPARATION-001**: Project Agent vs Curator roles
- **AGENT-DIRECT-SUBMODULE-ACCESS-001**: Submodule workflow anti-patterns
- **SUBMODULE-STATUS-INTERPRETATION-001**: Understanding status output
- **AGENT-HANDOFF-001**: Correct submission workflow
- **AGENT-HANDOFF-FAILURE-001**: Common submission failures
- **STALE-CONTEXT-001**: Verifying before referencing
- **YAML-001**: YAML syntax best practices
- **KB-UPDATE-001**: Shared KB update process

---

## Troubleshooting

### Issue closed as "incomplete"
**Cause:** Missing full YAML in issue body
**Fix:** Resubmit with complete YAML content embedded
**Pattern:** AGENT-HANDOFF-FAILURE-001

### Submodule won't update
**Cause:** Using wrong commands or in wrong directory
**Fix:** Use `git submodule update --remote` from project root
**Pattern:** AGENT-DIRECT-SUBMODULE-ACCESS-001

### Validation fails
**Cause:** YAML syntax errors
**Fix:** Run `kb validate`, fix errors, validate again
**Pattern:** YAML-001

### Reference to closed issue
**Cause:** Not verifying current state
**Fix:** Always check with `gh issue view` before referencing
**Pattern:** STALE-CONTEXT-001

---

## Getting Help

1. **Search KB first** - Most problems already documented
2. **Read patterns** - Follow documented best practices
3. **Verify assumptions** - Don't trust previous session context
4. **Create issue** - If new pattern discovered, contribute it

**Remember:** When in doubt, search KB and follow documented patterns. Don't guess.
