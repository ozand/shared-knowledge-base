---
allowed-tools: Bash(git *), Bash(python *)
description: Check Shared Knowledge Base repository status
---

## Context
- Current directory: !`pwd`
- Repository: shared-knowledge-base

## Your task
Check Shared Knowledge Base repository status:

### Step 1: Get version from CHANGELOG.md
```bash
head -5 CHANGELOG.md | grep -oP '(?<=\[)\d+\.\d+\.\d+(?=\])' | head -1
```

### Step 2: Get entry count
```bash
python tools/kb.py stats | grep "Total Entries:"
```

### Step 3: Get last commit
```bash
git log -1 --oneline
```

### Step 4: Check for uncommitted changes
```bash
git status --short
```

Execute these steps using the Bash tool and display the results in a formatted way. Note: Since this IS the Shared KB repository, status shows repository info, not submodule info.
