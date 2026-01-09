# GITHUB-005: Git Push Rejected - Remote Has Work You Don't Have

## Problem

Attempting to push fails with:
```
To https://github.com/user/repo.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs
```

## Explanation

Remote repository has commits that aren't in your local branch. This happens when:
1. Someone else pushed while you were working
2. You're working on an outdated branch
3. Force push was used on remote

## Solutions

### Rebase Workflow

Rebase your commits on top of remote (recommended):

```bash
# 1. Fetch latest from remote
git fetch origin

# 2. Rebase your local commits onto origin/main
git rebase origin/main

# 3. If conflicts occur, resolve them
# Edit conflicting files
git add <resolved-files>
git rebase --continue

# 4. After rebase completes, push
git push origin main
```

**Advantages:**
- Creates linear, clean history
- Standard practice for feature branches
- Easier to understand git log

**Disadvantages:**
- Rewrites history (don't use if pushed to shared branch)
- Can be confusing for beginners

### Merge Workflow

Merge remote changes into local branch:

```bash
# 1. Pull with merge (no rebase)
git pull origin main --no-rebase

# 2. If conflicts occur, resolve them
# Edit conflicting files
git add <resolved-files>
git commit -m "Merge remote changes"

# 3. Push
git push origin main
```

**Advantages:**
- Preserves true history
- Easier to understand
- Safer for shared branches

**Disadvantages:**
- Creates merge commits
- History becomes more complex

### Force Push (DANGER!)

Force push your local version:

```bash
git push --force origin main
```

**⚠️  WARNING - ONLY use this if:**
- You are the only one working on the branch
- You know remote commits should be discarded
- You're fixing a mistake you just pushed

**NEVER force push to shared main branch!**

**Risks:**
- Loses other developers' work
- Creates inconsistent repos
- Hard to recover

## Recommendations

- **Personal projects:** Use rebase for cleaner history
- **Team projects:** Use merge to preserve everyone's work
- **Emergency only:** Force push only if absolutely necessary

## Prevention

Sync frequently to avoid large conflicts:

```bash
# Before starting work
git pull origin main

# While working (every few hours)
git fetch origin
git rebase origin/main

# Before pushing
git pull --rebase origin main
git push
```

## References

- [Git Branching and Merging](https://www.atlassian.com/git/tutorials/using-branches/merging)
- [Rebasing Safely](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase)
