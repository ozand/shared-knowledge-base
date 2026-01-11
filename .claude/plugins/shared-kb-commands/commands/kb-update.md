---
allowed-tools: Bash(git *), Bash(python *)
description: Update Shared Knowledge Base (this repository)
---

## Context
- Current directory: !`pwd`
- Repository: shared-knowledge-base

## Your task
Update Shared Knowledge Base repository:

### Step 1: Pull latest changes from origin
```bash
git pull origin main
```

### Step 2: Rebuild index if needed
```bash
python tools/kb.py index --force
```

### Step 3: Show update summary
```bash
git log -1 --oneline
```

Execute these steps and inform the user when complete. Note: Since this IS the Shared KB repository, we pull directly instead of updating a submodule.
