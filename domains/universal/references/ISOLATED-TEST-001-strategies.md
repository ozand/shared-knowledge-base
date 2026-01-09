# Isolated Testing Pattern - Complete Strategies

**Extracted from:** isolated-testing.yaml
**Pattern ID:** ISOLATED-TEST-001

## Strategy 1: Temporary Clone (RECOMMENDED) 🌟

**Best for:** PR review, one-off testing, quick validation

### Process

```bash
# 1. Create temporary directory
cd /tmp
rm -rf pr-test
mkdir pr-test && cd pr-test

# 2. Clone repository (clean copy)
git clone git@github.com:user/repo.git .
# Note: '.' puts contents directly in pr-test, not pr-test/repo

# 3. Fetch PR branch
git fetch origin pull/<number>/head:pr-branch
git checkout pr-branch

# 4. Run tests
python tools/kb.py validate .
python tools/kb_patterns.py find-universal
# ... more tests

# 5. Delete entire directory when done
cd /tmp
rm -rf pr-test
```

### Advantages
- ✅ Complete isolation from main repo
- ✅ Easy cleanup (delete directory)
- ✅ No git contamination
- ✅ Can test destructive operations
- ✅ Fresh clone every time
- ✅ Parallel testing (multiple /tmp/pr-test-2, etc.)

### Disadvantages
- ⚠️ Requires cloning (network time for large repos)
- ⚠️ Uses disk space (temporary)

### Example: PR Review

```bash
cd /tmp && rm -rf pr-6-test && mkdir pr-6-test && cd pr-6-test
git clone git@github.com:ozand/shared-knowledge-base.git .
git fetch origin pull/6/head:pr6-branch
git checkout pr6-branch

# Test changes
python tools/kb_patterns.py find-universal
python tools/kb_community.py report
python tools/kb_predictive.py suggest-entries
python tools/kb_issues.py scan

# All passed, can cleanup
cd /tmp && rm -rf pr-6-test
```

## Strategy 2: Git Worktree

**Best for:** Frequent testing, multiple branches, development

### Process

```bash
# 1. Create worktree (linked to main repo)
git worktree add ../repo-pr-test pr-branch

# 2. Work in isolated directory
cd ../repo-pr-test

# 3. Run tests
python tools/test.py

# 4. When done, remove worktree
cd ../repo
git worktree remove ../repo-pr-test
```

### Advantages
- ✅ No full clone needed (shares .git objects)
- ✅ Faster than clone for large repos
- ✅ Still isolated from main work
- ✅ Easy to remove

### Disadvantages
- ⚠️ Still shares git database
- ⚠️ More complex git commands

## Strategy 3: Docker Container

**Best for:** Complete isolation, environment-specific testing

### Process

```bash
# 1. Mount repo as volume
docker run -v $(pwd):/app -w /app python:3.11 bash

# 2. Inside container, make changes and test
git checkout pr-branch
python test.py

# 3. Exit container (changes discarded)
exit
```

### Advantages
- ✅ Complete environment isolation
- ✅ No host contamination
- ✅ Reproducible environment
- ✅ Easy cleanup (docker rm)

### Disadvantages
- ⚠️ Requires Docker
- ⚠️ Heavier than just git clone

## Strategy 4: Git Stash (For Small Tests)

**Best for:** Quick tests in current repo, minimal changes

### Process

```bash
# 1. Stash current work
git stash push -u -m "Work before testing PR"

# 2. Checkout PR branch
git checkout pr-branch

# 3. Run tests
python test.py

# 4. Checkout main branch
git checkout main

# 5. Restore work
git stash pop

# OR if tests broke things, just discard:
# git checkout -f main
# git stash drop
```

### Advantages
- ✅ Fast for small tests
- ✅ No cloning needed

### Disadvantages
- ❌ Risk of accidental commits
- ❌ Still modifies main repo git state
- ❌ Not truly isolated
- ❌ Dangerous if forget stash pop/drop

**Recommendation:** Only use Strategy 1 (Temporary Clone) for safety

## Comparison Table

| Strategy | Isolation | Speed | Cleanup | Safety | Use Case |
|----------|-----------|-------|---------|--------|----------|
| **Temporary Clone** | ⭐⭐⭐⭐⭐ | Medium | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **PR Review (RECOMMENDED)** |
| **Git Worktree** | ⭐⭐⭐⭐ | Fast | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Frequent testing |
| **Docker** | ⭐⭐⭐⭐⭐ | Slow | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Environment-specific |
| **Git Stash** | ⭐⭐ | Fastest | ⭐⭐ | ⭐⭐ | Quick tests only |

## Best Practices

1. **Always use isolated environment for PR review**
   - Reason: Complete safety, easy cleanup

2. **Use /tmp for temporary clones**
   - Reason: Automatically cleaned on reboot

3. **Delete test directory immediately after testing**
   - Reason: No leftover artifacts

4. **Test destructive operations in clone**
   - Reason: Can't break main repo

5. **Use descriptive directory names**
   - Reason: Easy to identify (pr-6-test, pr-4-test)

6. **Parallel testing with separate directories**
   - Reason: Test multiple PRs simultaneously

## Anti-Patterns

### Anti-Pattern 1: Testing Directly in Main Repository

**Risks:**
- Accidental commits
- Git history pollution
- Difficult cleanup
- Build artifacts in repo
- Lost work if stash messed up

### Anti-Pattern 2: Using Master Branch for Experiments

**Risks:**
- Mix experimental with production
- Hard to undo
- Git state confusion

### Anti-Pattern 3: Forgetting Which Repo You're In

**Risks:**
- Modifying wrong repository
- Commits in wrong branch
- Lost work

## Workflow Checklist

1. **Create temporary directory**
   - Location: /tmp
   - Command: `cd /tmp && mkdir pr-test && cd pr-test`

2. **Clone repository**
   - Command: `git clone git@github.com:user/repo.git .`
   - Note: Period at end clones into current dir

3. **Fetch and checkout PR branch**
   - Commands:
     - `git fetch origin pull/<number>/head:pr-branch`
     - `git checkout pr-branch`

4. **Run tests**
   - Example:
     ```bash
     python tools/kb.py validate .
     python tools/kb_patterns.py find-universal
     # ... more tests
     ```

5. **Verify results**
   - Question: All tests passed?

6. **Cleanup**
   - Commands:
     - `cd /tmp`
     - `rm -rf pr-test`
   - Note: Complete cleanup, no traces

## Parallel Testing

**Scenario:** Testing multiple PRs simultaneously

**Process:**
```bash
cd /tmp

# PR #6
mkdir pr-6-test && cd pr-6-test
git clone git@github.com:user/repo.git .
git fetch origin pull/6/head:pr6 && git checkout pr6

# In another terminal
cd /tmp

# PR #4
mkdir pr-4-test && cd pr-4-test
git clone git@github.com:user/repo.git .
git fetch origin pull/4/head:pr4 && git checkout pr4

# Test both independently
```

**Advantage:** No interference between PRs
