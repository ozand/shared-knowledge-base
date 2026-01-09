# KB-UPDATE-001: Update Workflows

## Git Submodule Workflow

Update when Shared KB is installed as git submodule.

### Check for Updates

**Manual:**
```bash
cd docs/knowledge-base/shared
git fetch origin
git log HEAD..origin/main --oneline
```

**Automated:**
```bash
python docs/knowledge-base/shared/tools/kb.py check-updates
```

**Auto Check on Bootstrap:**
```bash
# Automatic check when agent session starts
python tools/kb-agent-bootstrap.py
```

### Update Command

```bash
git submodule update --remote --merge docs/knowledge-base/shared
```

### What Happens

1. Fetches latest changes from remote
2. Merges changes into local submodule
3. Resolves conflicts if needed
4. Updates to latest commit

### Rollback

```bash
# If update breaks something
cd docs/knowledge-base/shared
git log --oneline -10  # Find previous commit
git checkout <previous-commit-hash>
cd ../..
git add docs/knowledge-base/shared
git commit -m "Rollback Shared KB to <commit-hash>"
```

---

## Plain Clone Workflow

Update when Shared KB is installed as plain git clone.

### Check for Updates

**Manual:**
```bash
cd docs/knowledge-base/shared
git fetch origin
git log HEAD..origin/main --oneline
```

**Automated:**
```bash
python docs/knowledge-base/shared/tools/kb.py check-updates
```

**Auto Check on Bootstrap:**
```bash
# Automatic check when agent session starts
python tools/kb-agent-bootstrap.py
```

### Update Command

```bash
cd docs/knowledge-base/shared
git pull origin main
```

### What Happens

1. Fetches latest changes from remote
2. Fast-forwards to latest commit
3. Updates working directory
4. Reports conflicts if any

### Resolve Conflicts

```bash
# If there are conflicts (rare in plain clone)
cd docs/knowledge-base/shared
git status  # See conflicted files
# Edit conflicted files
git add <resolved-files>
git commit  # Complete merge
```

### Rollback

```bash
# If update breaks something
cd docs/knowledge-base/shared
git reflog  # Find previous position
git reset --hard HEAD@{N}  # Where N is the reflog entry
# Or:
git checkout <previous-commit-hash>
```

---

## Sparse Checkout Workflow

Update with sparse checkout (excludes Curator files).

### Check for Updates

```bash
python docs/knowledge-base/shared/tools/kb.py check-updates
```

### Update Command

```bash
# Same as submodule or clone
git submodule update --remote --merge docs/knowledge-base/shared
# OR
cd docs/knowledge-base/shared && git pull origin main
```

### Verify Sparse Active

```bash
# Ensure sparse checkout still active after update
cd docs/knowledge-base/shared
git config core.sparseCheckout  # Should return "true"
ls .git/info/sparse-checkout  # Should exist
```

### If Broken

```bash
# If update loads all files (sparse checkout broken)
cd docs/knowledge-base/shared
git config core.sparseCheckout true
cat > .git/info/sparse-checkout < sparse-checkout.example
git reset --hard HEAD
git checkout
```

---

## Recommended Update Frequency

### Active Development

- Weekly during active development
- Before starting major work
- Before using critical patterns
- When encountering unfamiliar errors

### Maintenance Mode

- Monthly for maintenance projects
- Before releasing new versions
- When responding to support requests

### Always Update Before

- Using critical security patterns
- Implementing complex workflows
- Troubleshooting difficult issues
- Onboarding new team members
