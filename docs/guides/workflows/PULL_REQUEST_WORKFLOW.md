# Pull Request Workflow Guide

**Version:** 1.0
**Last Updated:** 2026-01-06
**Purpose:** Ensure proper PR workflow for Shared Knowledge Base contributions

---

## 🎯 Why This Matters

**Problem Identified (Repository Analysis 2026-01-06):**
- Merge success rate: **40%** (2 merged, 3 closed without merging)
- 3 PRs were **MERGEABLE** but closed without merging
- Contributor attribution lost
- PR history broken
- Non-standard workflow

**Impact:**
- Contributors lose credit for their work
- Cannot see who reviewed/approved changes
- Breaks GitHub contribution graph
- Unclear why PRs weren't merged

**Solution:**
This guide ensures **100% merge rate** for approved contributions.

---

## 📋 Standard PR Workflow

### For Contributors (Project Agents)

#### Step 1: Create Feature Branch
```bash
# From your fork or main branch
git checkout -b feature/your-feature-name

# Examples:
git checkout -b feature/postgresql-errors
git checkout -b fix/yaml-validation
git checkout -f feature/parser-project-patterns
```

**Branch Naming Convention:**
- `feature/` - New features or patterns
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring

#### Step 2: Make Your Changes
```bash
# Make changes, commit them
git add .
git commit -m "Add PostgreSQL database errors and patterns"
```

**Commit Message Guidelines:**
- Use clear, descriptive messages
- Reference issue numbers if applicable: `Fixes #16`
- Follow conventional commits: `feat:`, `fix:`, `docs:`, etc.

#### Step 3: Push to GitHub
```bash
# Push your feature branch
git push origin feature/your-feature-name
```

#### Step 4: Create Pull Request
```bash
# Using GitHub CLI
gh pr create \
  --title "Add PostgreSQL database errors and patterns" \
  --body "See description below" \
  --base main \
  --head feature/your-feature-name
```

**PR Title Format:**
- Clear description of changes
- Include pattern ID if applicable: `Add KB-UPDATE-001: Update Workflow`
- Reference issue: `Fix #16 - Add 5 universal patterns`

**PR Body Template:**
```markdown
## Description
Briefly describe what this PR adds/fixes.

## Type
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring
- [ ] Patterns (specify which ones)

## Changes
- List main changes here
- Be specific about patterns added

## Testing
- [ ] YAML validated: `py tools/kb.py validate <file>`
- [ ] Index built: `py tools/kb.py index -v`
- [ ] Search tested: `py tools/kb.py search "keyword"`
- [ ] Manual testing completed

## Related Issues
Fixes #16
Closes #15

## Checklist
- [ ] Code follows repository style guide
- [ ] YAML syntax validated
- [ ] Self-review completed
- [ ] Documentation updated (if needed)

## Additional Notes
Any additional context for reviewers.
```

#### Step 5: Wait for Review
- **DO NOT** close the PR yourself
- **DO NOT** commit directly to main
- Respond to review comments
- Make requested changes

#### Step 6: Request Merge (After Approval)
Once approved:
```bash
# Add comment requesting merge
gh pr comment "Ready to merge. All checks passed."
```

**IMPORTANT:**
- ✅ PR should be **MERGED**, not closed
- ✅ Maintain PR until Curator merges it
- ❌ **NEVER** close a mergeable PR

---

## 📋 For Curators

### Step 1: Review Incoming PRs
```bash
# List open PRs
gh pr list

# View PR details
gh pr view <pr-number>
```

### Step 2: Review Changes
```bash
# Checkout PR branch locally (for testing)
gh pr checkout <pr-number>

# Validate YAML
py tools/kb.py validate <changed-files>

# Build index
py tools/kb.py index -v

# Test search
py tools/kb.py search "test-keyword"
```

### Step 3: Approve or Request Changes
```bash
# Approve PR
gh pr review <pr-number> --approve

# OR request changes
gh pr review <pr-number> --body "Please fix the following: ..."
```

### Step 4: Merge Approved PRs ✅
```bash
# Merge PR (THIS IS CRITICAL!)
gh pr merge <pr-number> --merge --delete-branch

# Options:
# --merge: Create merge commit (recommended)
# --squash: Squash commits (if appropriate)
# --rebase: Rebase commits (rarely needed)
# --delete-branch: Delete branch after merge (recommended)
```

**CRITICAL RULES:**
1. ✅ **ALWAYS** merge approved PRs
2. ❌ **NEVER** close mergeable PRs
3. ✅ **ALWAYS** delete branch after merging
4. ❌ **NEVER** commit PR content directly to main

**Why Merge, Not Close:**
- Merging preserves contribution history
- Contributors get proper credit
- GitHub contribution graph updated
- Clear audit trail of what was merged
- Can revert if needed

### Step 5: Close Issues
```bash
# If PR fixes an issue, close it
gh issue close <issue-number> --comment "Fixed by #<pr-number>"
```

---

## 🚫 Common Mistakes to Avoid

### Mistake 1: Closing Mergeable PRs ❌
**Problem:** PR is mergeable but closed without merging
**Impact:** Lost contributor credit, broken history
**Solution:** Always merge approved PRs

### Mistake 2: Committing Directly to Main ❌
**Problem:** PR content added via direct commits
**Impact:** Loses PR attribution, violates workflow
**Solution:** Always create PR, review, then merge

### Mistake 3: Not Deleting Branches ❌
**Problem:** Feature branches left on remote
**Impact:** Cluttered branch list, confusion
**Solution:** Always delete branches after merge

### Mistake 4: Poor PR Descriptions ❌
**Problem:** Vague title, no body, missing context
**Impact:** Hard to review, delays merge
**Solution:** Use provided template, be specific

### Mistake 5: Not Validating YAML ❌
**Problem:** PR contains YAML syntax errors
**Impact:** Blocks indexing, causes CI failures
**Solution:** Always validate before submitting

---

## ✅ Success Criteria

A successful PR workflow should have:

- [ ] **100% merge rate** for approved PRs
- [ ] **0% close rate** for mergeable PRs
- [ ] **All feature branches deleted** after merge
- [ ] **All PRs follow template**
- [ ] **All YAML validated** before submission
- [ ] **All contributors properly credited**

---

## 📊 Workflow Diagram

```
Contributor                    Curator
    |                            |
    |--[1] Create branch         |
    |                            |
    |--[2] Make changes          |
    |                            |
    |--[3] Push to GitHub        |
    |                            |
    |--[4] Create PR ---------->|
    |                            |
    |                      |--[5] Review
    |                      |--[6] Validate
    |                            |
    |<-----[7] Feedback ---------|
    |                            |
    |--[8] Make changes          |
    |                            |
    |--[9] Push updates ------->|
    |                      |--[10] Approve
    |                            |
    |                      |--[11] MERGE ✅
    |                      |--[12] Delete branch
    |                      |--[13] Close issues
    |                            |
    |<------[14] Thank you -------|
```

---

## 🔧 GitHub CLI Commands Reference

### For Contributors
```bash
# Create PR from current branch
gh pr create --title "Title" --body "Description"

# View PR status
gh pr status

# View your PRs
gh pr list --author "@me"

# Request review
gh pr edit <pr-number> --add-reviewer "username"

# Add comment
gh pr comment <pr-number> --body "Comment"

# Checkout PR for testing
gh pr checkout <pr-number>
```

### For Curators
```bash
# List open PRs
gh pr list --state open

# View PR details
gh pr view <pr-number>

# Checkout PR locally
gh pr checkout <pr-number>

# Review and approve
gh pr review <pr-number> --approve

# Review with changes
gh pr review <pr-number> --body "Please fix..."

# Merge PR (CRITICAL!)
gh pr merge <pr-number> --merge --delete-branch

# Close issue fixed by PR
gh issue close <issue-number> --comment "Fixed by #<pr-number>"

# List merged PRs
gh pr list --state merged
```

---

## 📚 Related Documentation

- **GITHUB_ATTRIBUTION_GUIDE.md** - GitHub integration and attribution
- **AGENT-HANDOFF-001** - Project Agent → Curator workflow
- **GITHUB-WORKFLOW-001** - GitHub workflow patterns (if exists)
- **GitHub Flow Documentation** - https://guides.github.com/introduction/flow/

---

## 🎓 Best Practices

### For Contributors

1. **Keep PRs Focused**
   - One PR should address one issue
   - Don't mix unrelated changes
   - Smaller PRs review faster

2. **Write Clear Commit Messages**
   - Use conventional commit format
   - Reference issue numbers
   - Explain "why" not just "what"

3. **Test Before Submitting**
   - Validate all YAML
   - Build index
   - Test search
   - Manual verification

4. **Be Responsive**
   - Address review feedback promptly
   - Ask questions if unclear
   - Update PR as requested

### For Curators

1. **Review Promptly**
   - Try to review within 24-48 hours
   - Communicate delays if busy
   - Set expectations with contributors

2. **Provide Clear Feedback**
   - Explain what needs fixing
   - Provide examples
   - Be constructive, not critical

3. **Merge Approved PRs Quickly**
   - Don't leave approved PRs open
   - Merge within 24 hours of approval
   - Delete branches after merge

4. **Maintain Standards**
   - Enforce YAML validation
   - Ensure pattern quality
   - Check documentation completeness

---

## 🔄 Integration with Existing Workflows

### AGENT-HANDOFF-001 Workflow

**Project Agent:**
1. Creates patterns locally
2. Validates YAML syntax
3. Creates GitHub issue (via AGENT-HANDOFF-001)
4. Waits for Curator review

**Curator Agent:**
1. Reviews issue
2. Provides feedback
3. If approved: Creates PR from issue
4. Merges PR (doesn't close!)
5. Closes issue

**Key Point:** Curator creates PR from issue, merges it, doesn't close it.

---

## 🚨 Troubleshooting

### Problem: PR Shows "Merge Conflict"
**Solution:**
```bash
# Update your branch with latest main
git checkout main
git pull origin main
git checkout feature/your-branch
git rebase main
# Fix conflicts
git push origin feature/your-branch --force
```

### Problem: Curator Closed PR Without Merging
**Solution:**
1. Reopen PR: `gh pr reopen <pr-number>`
2. Verify it's mergeable: `gh pr view <pr-number>`
3. If mergeable: Request merge again
4. If not mergeable: Fix conflicts, update PR

### Problem: Branch Not Deleted After Merge
**Solution:**
```bash
# Delete local branch
git branch -d feature/your-branch

# Delete remote branch
git push origin --delete feature/your-branch
```

---

## 📈 Measuring Success

Track these metrics:

| Metric | Current | Target | How to Measure |
|--------|---------|--------|----------------|
| Merge Rate | 40% | 100% | `gh pr list --state merged | wc -l` / total PRs |
| Close Rate | 60% | 0% | `gh pr list --state closed | wc -l` / total PRs |
| Avg Time to Merge | TBD | < 7 days | Track PR creation vs merge dates |
| Stale Branches | 3 | 0 | `git branch -r | grep -v HEAD | wc -l` - 1 |

---

## ✅ Checklist

### Before Creating PR
- [ ] Changes committed to feature branch
- [ ] YAML validated: `py tools/kb.py validate`
- [ ] Index tested: `py tools/kb.py index -v`
- [ ] Search tested: `py tools/kb.py search "keyword"`
- [ ] PR description follows template
- [ ] Related issues referenced

### Before Merging PR (Curators)
- [ ] Changes reviewed
- [ ] YAML validated
- [ ] Tests passed
- [ ] Documentation complete
- [ ] Approved for merge

### After Merging PR
- [ ] PR merged (not closed!)
- [ ] Branch deleted
- [ ] Issues closed
- [ ] Contributors thanked
- [ ] Metrics updated

---

**Document Version:** 1.0
**Created:** 2026-01-06
**Author:** Shared KB Curator Agent
**Purpose:** Ensure 100% merge rate for approved contributions
**Next Review:** After 10 PRs processed or 2026-02-01

---

## 🎯 Quick Reference

### Contributors: Do's and Don'ts

✅ **DO:**
- Create feature branches
- Validate YAML before submitting
- Use PR template
- Respond to feedback promptly
- Wait for merge, don't close PR

❌ **DON'T:**
- Commit directly to main
- Close mergeable PRs
- Submit unvalidated YAML
- Ignore feedback
- Leave PRs abandoned

### Curators: Do's and Don'ts

✅ **DO:**
- Review PRs promptly
- Provide clear feedback
- **Merge approved PRs** (critical!)
- Delete branches after merge
- Close related issues

❌ **DON'T:**
- Close mergeable PRs
- Commit PR content directly to main
- Leave branches undeleted
- Delay merges unnecessarily
- Lose contributor attribution
