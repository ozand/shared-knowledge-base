# Agent Quick Start Guide - Shared Knowledge Base v4.0

**5-minute setup guide for Claude Code agents**

**Last Updated:** 2026-01-07
**Version:** 4.0

---

## ⚡ Quick Setup (5 Minutes)

### Step 1: Add Shared KB to Your Project (2 minutes)

```bash
# Add as submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared

# Configure progressive loading (load only what you need)
cd .kb/shared
git sparse-checkout init
git sparse-checkout set docker postgresql universal tools _domain_index.yaml
git sparse-checkout reapply

# Initialize search
cd ../..
python .kb/shared/tools/kb.py index -v
```

**Result:** Shared KB ready with ~1,730 tokens (82% savings!)

### Step 2: Test Search (1 minute)

```bash
# Search for solution
python .kb/shared/tools/kb.py search "docker build error"

# List available domains
python .kb/shared/tools/kb_domains.py list
```

### Step 3: Configure Your Agent (2 minutes)

Create `.claude/settings.json`:
```json
{
  "contextSearch": true,
  "contextPaths": [
    ".kb/shared/**/*.{md,yaml,py}",
    ".kb/shared/_domain_index.yaml"
  ],
  "hooks": [
    {
      "name": "kb-search",
      "events": ["SessionStart"],
      "command": "python .kb/shared/tools/kb.py index --check"
    }
  ]
}
```

**Done!** Your agent now has access to Shared KB v4.0.

---

## 🎯 For New Projects

### Option A: Progressive Loading (Recommended)

**Best for:** Focused projects (e.g., only use Docker + PostgreSQL)

```bash
# 1. Add submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared

# 2. Choose your domains
cd .kb/shared
git sparse-checkout init

# 3. Load only what you need (example: docker + postgresql)
git sparse-checkout set docker postgresql universal tools _domain_index.yaml
git sparse-checkout reapply

# 4. Initialize
cd ../..
python .kb/shared/tools/kb.py index -v
```

**Token cost:** ~1,730 tokens (vs ~9,750 for full KB)

### Option B: Full KB (For Multi-Domain Projects)

**Best for:** Projects that need everything

```bash
# Add submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared

# Initialize
cd .kb/shared
python tools/kb.py index -v
cd ..
```

**Token cost:** ~9,750 tokens

---

## 🔄 Updating from v3.x to v4.0

### Automatic Update (Recommended)

```bash
# 1. Navigate to submodule
cd .kb/shared

# 2. Pull latest changes
git fetch origin
git checkout origin/main

# 3. Update in your project
cd ../..
git submodule update --remote .kb/shared

# 4. Rebuild index
python .kb/shared/tools/kb.py index --force -v

# 5. Test new features
python .kb/shared/tools/kb_domains.py list
```

### Manual Update to Specific Version

```bash
# 1. Navigate to submodule
cd .kb/shared

# 2. Checkout v4.0.0 tag
git fetch origin --tags
git checkout v4.0.0

# 3. Update in parent project
cd ../..
git add .kb/shared
git commit -m "Update Shared KB to v4.0.0"

# 4. Push
git push origin main
```

---

## 📚 Key Commands Reference

### Search Commands

```bash
# Basic search
python .kb/shared/tools/kb.py search "keyword"

# Advanced search
python .kb/shared/tools/kb.py search --scope python --tag async
python .kb/shared/tools/kb.py search --severity high

# Show statistics
python .kb/shared/tools/kb.py stats

# Validate entries
python .kb/shared/tools/kb.py validate .
```

### Progressive Loading Commands (NEW in v4.0)

```bash
# List all available domains
python .kb/shared/tools/kb_domains.py list

# Load specific domain
python .kb/shared/tools/kb_domains.py load docker

# Get domain details
python .kb/shared/tools/kb_domains.py info postgresql

# Migrate entries to domains
python .kb/shared/tools/kb_domains.py migrate --from-tags

# Validate domain metadata
python .kb/shared/tools/kb_domains.py validate
```

### Submission Commands (NEW in v4.0)

```bash
# Submit entry to Shared KB (via GitHub Issue)
python .kb/shared/tools/kb_submit.py submit --entry path/to/entry.yaml

# Dry run (preview)
python .kb/shared/tools/kb_submit.py submit --entry path/to/entry.yaml --dry-run

# Check issue status
python .kb/shared/tools/kb_submit.py status --issue 123
```

---

## 🎓 Common Workflows

### Workflow 1: Find Solution

```bash
# When user reports error

# 1. Search KB
python .kb/shared/tools/kb.py search "error message"

# 2. If found → Return solution
# 3. If not found → Create entry in .kb/local/

# 4. If universal scope → Submit to Shared KB
python .kb/shared/tools/kb_submit.py submit --entry .kb/local/NEW-ENTRY.yaml
```

### Workflow 2: Add New Domain

```bash
# When project needs new domain

# 1. Add domain to sparse checkout
cd .kb/shared
git sparse-checkout add testing
git sparse-checkout reapply

# 2. Verify
python tools/kb_domains.py list
```

### Workflow 3: Submit Knowledge

```bash
# When you create new knowledge entry

# 1. Create entry in .kb/local/
# 2. Validate YAML
python .kb/shared/tools/kb.py validate .kb/local/NEW-ENTRY.yaml

# 3. Submit to Shared KB
python .kb/shared/tools/kb_submit.py submit --entry .kb/local/NEW-ENTRY.yaml

# 4. Wait for curator approval
# 5. Automatic update when approved
```

---

## 🔧 Configuration Files

### .kb/.kb-config.yaml

```yaml
version: "4.0"
paths:
  shared: ".kb/shared"
  local: ".kb/local"

shared_repository:
  url: "https://github.com/ozand/shared-knowledge-base.git"
  branch: "main"

domains:
  enabled: true
  progressive_loading: true
  loaded_domains:
    - docker
    - postgresql
    - universal
```

### .claude/settings.json (Claude Code)

```json
{
  "contextSearch": true,
  "contextPaths": [
    ".kb/shared/**/*.{md,yaml,py}",
    ".kb/shared/_domain_index.yaml"
  ]
}
```

---

## 📊 Domain Reference

Available domains in v4.0:

| Domain | Entries | Tokens | Description |
|--------|---------|--------|-------------|
| docker | 11 | ~1,650 | Docker & containers |
| testing | 11 | ~1,650 | Testing frameworks |
| postgresql | 8 | ~1,200 | PostgreSQL database |
| asyncio | 6 | ~900 | Async/await patterns |
| authentication | 6 | ~900 | Auth & security |
| api | 4 | ~600 | API design |
| deployment | 4 | ~600 | Deployment strategies |
| fastapi | 3 | ~450 | FastAPI framework |
| monitoring | 4 | ~600 | Logging & monitoring |
| performance | 4 | ~600 | Optimization |
| security | 2 | ~300 | Security practices |
| websocket | 2 | ~300 | WebSocket |

**Total entries:** 149
**Total domains:** 12

---

## ❓ FAQ

### Q: Should I use progressive loading?

**A:** Yes, if your project focuses on specific domains. Benefits:
- 83% token reduction
- Faster context loading
- Clearer knowledge boundaries

### Q: How do I add more domains later?

**A:** Easy:
```bash
cd .kb/shared
git sparse-checkout add testing
git sparse-checkout reapply
```

### Q: What if I need all domains?

**A:** Use full clone:
```bash
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared
```

### Q: How do I submit new knowledge?

**A:** Use kb-submit tool:
```bash
python .kb/shared/tools/kb_submit.py submit --entry .kb/local/NEW-ENTRY.yaml
```

### Q: What happens after I submit?

**A:**
1. GitHub Issue created automatically
2. Curator reviews
3. Curator uses `/approve` or `/request-changes`
4. You're notified via GitHub Actions
5. If approved, local KB updates automatically

### Q: Is v4.0 backward compatible?

**A:** Yes! All v3.x tools work unchanged.

---

## 🆘 Troubleshooting

### Problem: Submodule not updating

**Solution:**
```bash
cd .kb/shared
git fetch origin
git checkout origin/main
cd ../..
git submodule update --remote .kb/shared
```

### Problem: Index not found

**Solution:**
```bash
python .kb/shared/tools/kb.py index --force -v
```

### Problem: Progressive loading not working

**Solution:**
```bash
cd .kb/shared
git sparse-checkout disable
git sparse-checkout init
git sparse-checkout set docker postgresql universal tools _domain_index.yaml
git sparse-checkout reapply
```

---

## 📖 Next Steps

- **Full Guide:** [../README.md](../README.md)
- **Progressive Loading:** [../QUICKSTART-DOMAINS.md](../QUICKSTART-DOMAINS.md)
- **Implementation:** [../docs/implementation/](../docs/implementation/)
- **Change Log:** [../CHANGELOG.md](../CHANGELOG.md)

---

## 🎉 You're Ready!

Your agent now has access to:
- ✅ Shared Knowledge Base v4.0
- ✅ Progressive domain loading
- ✅ GitHub-native contribution
- ✅ Automated feedback loop

**Token cost:** ~1,730 tokens (with progressive loading)
**Savings:** 82% compared to full KB

Happy coding! 🚀
