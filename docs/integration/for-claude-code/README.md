# For Claude Code: Shared Knowledge Base v5.1

**Complete guide for Claude Code agents on the enhanced Shared Knowledge Base**

**Last Updated:** 2026-01-07
**Version:** 4.0 (Progressive Loading + GitHub-Native Contribution + Automated Feedback Loop)

---

## 🎯 What's New in Version 4.0

### Major Features

**🚀 Progressive Domain Loading (Phase 1)**
- Load only the knowledge domains you need
- 83% token reduction for single-domain projects
- 12-domain taxonomy (docker, python, postgresql, testing, asyncio, etc.)
- Domain index optimized to ~80 tokens (99.1% reduction)

**🔗 GitHub-Native Contribution System (Phase 2)**
- Submit entries via GitHub Issues
- Zero infrastructure costs (100% GitHub Actions)
- Automated curator workflows
- Local-remote entry linking

**🔄 Automated Feedback Loop (Phase 3)**
- Curator slash commands (/approve, /request-changes, /reject, /take)
- Automatic KB updates on approval
- Complete agent-curator communication
- 100% test coverage

### Quick Stats
- **149 knowledge entries** across 12 domains
- **83% token reduction** with progressive loading
- **Zero infrastructure** - all GitHub-native
- **93.75% test coverage** (15/16 tests passed)

---

## Installation for New Projects

### Option 1: Submodule with Progressive Loading (Recommended)

**Best for:** Most projects, especially those focused on specific domains

```bash
# Add as submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared

# Configure sparse checkout for specific domains
cd .kb/shared
git sparse-checkout init
git sparse-checkout set docker postgresql universal tools _domain_index.yaml
git sparse-checkout reapply

# Initialize
cd ../..
python .kb/shared/tools/kb.py index -v
```

**Result:** Only ~1,730 tokens for docker + postgresql domains (vs ~9,750 for full KB)

### Option 2: Full Clone (For Multi-Domain Projects)

**Best for:** Projects that need all domains

```bash
# Add as submodule (full)
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared

# Initialize
cd .kb/shared
python tools/kb.py index -v
cd ..
```

**Result:** Full KB (~9,750 tokens)

### Option 3: Remote Installation Script

```bash
# One-line installation with progressive loading
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/unified-install.py | python3 - --full
```

---

## Updating from v3.x to v5.1

### Automatic Update (Recommended)

```bash
# Navigate to your Shared KB submodule
cd .kb/shared

# Pull latest changes
git fetch origin
git checkout origin/main

# Update submodule in your project
cd ../..
git submodule update --remote .kb/shared

# Rebuild index
python .kb/shared/tools/kb.py index --force -v

# Test progressive loading
python .kb/shared/tools/kb_domains.py list
```

### Manual Update

```bash
# Navigate to submodule
cd .kb/shared

# Stash any local changes
git stash

# Checkout v5.1.0 tag
git fetch origin --tags
git checkout v5.1.0

# Update in parent project
cd ../..
git add .kb/shared
git commit -m "Update Shared KB to v5.1.0

Progressive loading: 83% token reduction
GitHub-native contribution: Zero infrastructure
Automated feedback loop: Complete curator-agent communication

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Push update
git push origin main
```

---

## Quick Reference for Claude Code

### Basic Commands

```bash
# Search knowledge base
python .kb/shared/tools/kb.py search "websocket"
python .kb/shared/tools/kb.py search --scope python --tag async

# List available domains
python .kb/shared/tools/kb_domains.py list

# Load specific domain
python .kb/shared/tools/kb_domains.py load docker

# Get domain info
python .kb/shared/tools/kb_domains.py info postgresql

# Show statistics
python .kb/shared/tools/kb.py stats

# Validate entries
python .kb/shared/tools/kb.py validate .
```

### New v5.1 Commands

```bash
# Progressive domain loading
python .kb/shared/tools/kb_domains.py list              # List all domains
python .kb/shared/tools/kb_domains.py load <domain>     # Load domain
python .kb/shared/tools/kb_domains.py info <domain>     # Domain details

# Submit entry to Shared KB (via GitHub Issues)
python .kb/shared/tools/kb_submit.py submit --entry path/to/entry.yaml
python .kb/shared/tools/kb_submit.py status --issue 123

# Test suites
python .kb/shared/tools/test_progressive_loading.py
python .kb/shared/tools/test_feedback_loop.py
```

---

## Progressive Domain Loading Guide

### What is Progressive Loading?

Instead of loading the entire KB (~9,750 tokens), you load only the domains you need:

**Example: Docker-focused project**
```bash
# Load only docker + postgresql + universal
git sparse-checkout set docker postgresql universal tools _domain_index.yaml

# Result: ~1,730 tokens (82% savings!)
```

### Domain List

Available domains in v5.1:
- `docker` (11 entries, ~1,650 tokens)
- `testing` (11 entries, ~1,650 tokens)
- `postgresql` (8 entries, ~1,200 tokens)
- `asyncio` (6 entries, ~900 tokens)
- `authentication` (6 entries, ~900 tokens)
- `api` (4 entries, ~600 tokens)
- `deployment` (4 entries, ~600 tokens)
- `fastapi` (3 entries, ~450 tokens)
- `monitoring` (4 entries, ~600 tokens)
- `performance` (4 entries, ~600 tokens)
- `security` (2 entries, ~300 tokens)
- `websocket` (2 entries, ~300 tokens)

### Setup Progressive Loading

**Step 1: Choose your domains**
```bash
# List available domains
python .kb/shared/tools/kb_domains.py list

# Output:
# docker: 11 entries, ~1650 tokens
# testing: 11 entries, ~1650 tokens
# postgresql: 8 entries, ~1200 tokens
# ...
```

**Step 2: Configure sparse checkout**
```bash
cd .kb/shared

# Initialize sparse checkout
git sparse-checkout init

# Add only the domains you need
git sparse-checkout set docker postgresql universal tools _domain_index.yaml

# Apply
git sparse-checkout reapply
```

**Step 3: Verify**
```bash
# Check what was loaded
ls -la

# Should see: docker/, postgresql/, universal/, tools/, _domain_index.yaml
# Total tokens: ~1,730 (vs ~9,750 for full KB)
```

### Adding More Domains Later

```bash
cd .kb/shared

# Add another domain
git sparse-checkout add testing

# Apply
git sparse-checkout reapply
```

---

## Submitting Entries to Shared KB (v5.1)

### GitHub-Native Contribution Workflow

**Step 1: Create entry locally**
```bash
# Create in your project's local KB
.kb/local/DOCKER-001.yaml
```

**Step 2: Submit to Shared KB**
```bash
# Use kb-submit tool
python .kb/shared/tools/kb_submit.py submit --entry .kb/local/DOCKER-001.yaml

# Output:
# 📤 Submitting entry: .kb/local/DOCKER-001.yaml
# ✅ Issue created: https://github.com/ozand/shared-knowledge-base/issues/123
# ✅ Updated .kb/local/DOCKER-001.yaml with github metadata
```

**Step 3: Wait for curator approval**

**Step 4: Automatic update**
- Curator approves → GitHub Actions trigger
- Your project receives notification
- Local KB updates automatically
- Knowledge becomes available to agents

### Manual Submission (Alternative)

If `kb-submit.py` is not available:

1. **Create GitHub Issue manually:**
   - Go to https://github.com/ozand/shared-knowledge-base/issues
   - Click "New Issue"
   - Use template for knowledge entry submission
   - Paste YAML content

2. **Update local YAML with github metadata:**
```yaml
github:
  issue_number: 123
  issue_url: "https://github.com/ozand/shared-knowledge-base/issues/123"
  issue_status: "pending"
  contribution_date: "2026-01-07"
  agent_attribution:
    agent_type: "claude-code"
    source_repository: "your-org/your-repo"
    local_kb_path: ".kb/local/"
```

---

## Curator Interaction

### Understanding the Feedback Loop

```
Agent → Submit Entry → GitHub Issue → Curator Reviews → Agent Notified → Local KB Updated
```

### Curator Commands

Curators use slash commands in GitHub Issues:

- `/approve [reason]` - Entry approved, will be merged
- `/request-changes [reason]` - Changes needed before approval
- `/reject [reason]` - Entry rejected
- `/take` - Curator took ownership for review

### Receiving Feedback

**When curator requests changes:**
1. Feedback saved to `.kb/feedback/issue-{number}.md`
2. Agent notified via GitHub Actions
3. Update entry based on feedback
4. Resubmit via issue comment

**When curator approves:**
1. Local KB metadata updated automatically
2. Shared KB submodule updated
3. Knowledge available to agents

---

## Configuration Files

### .kb/.kb-config.yaml (Local Config)

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

search:
  engine: "sqlite"
  index_path: ".kb/_index.yaml"
```

---

## Common Workflows

### Workflow 1: Search for Solution

```bash
# 1. Search KB
python .kb/shared/tools/kb.py search "docker build error"

# 2. If found, return solution
# 3. If not found, create entry

# Create in .kb/local/
# Determine scope (docker, python, universal, etc.)

# 4. If scope is universal → submit to Shared KB
python .kb/shared/tools/kb_submit.py submit --entry .kb/local/ENTRY-001.yaml
```

### Workflow 2: Update Shared KB

```bash
# 1. Check for updates
cd .kb/shared
git fetch origin
git log HEAD..origin/main --oneline

# 2. Update if needed
git pull origin main

# 3. In parent project
cd ../..
git submodule update --remote .kb/shared

# 4. Rebuild index
python .kb/shared/tools/kb.py index --force -v
```

### Workflow 3: Add New Domain

```bash
# 1. Add domain to sparse checkout
cd .kb/shared
git sparse-checkout add testing
git sparse-checkout reapply

# 2. Verify
python tools/kb_domains.py list

# 3. Update .kb/.kb-config.yaml
# Add 'testing' to loaded_domains
```

---

## Troubleshooting

### Issue: Submodule not updating

```bash
# Solution: Force update
cd .kb/shared
git fetch origin
git checkout origin/main
cd ../..
git submodule update --remote .kb/shared
```

### Issue: Index not found

```bash
# Solution: Rebuild index
python .kb/shared/tools/kb.py index --force -v
```

### Issue: Progressive loading not working

```bash
# Solution: Reinitialize sparse checkout
cd .kb/shared
git sparse-checkout disable
git sparse-checkout init
git sparse-checkout set docker postgresql universal tools _domain_index.yaml
git sparse-checkout reapply
```

### Issue: Submit failed

```bash
# Solution: Check gh CLI
gh auth status

# If not authenticated:
gh auth login
```

---

## Documentation

- **[AGENT-QUICK-START.md](AGENT-QUICK-START.md)** - Quick start for agents
- **[CLAUDE.md](CLAUDE.md)** - Claude Code workflow instructions
- **[../QUICKSTART-DOMAINS.md](../QUICKSTART-DOMAINS.md)** - Progressive loading guide
- **[../docs/README.md](../docs/README.md)** - Documentation hub
- **[../CHANGELOG.md](../CHANGELOG.md)** - Version history

---

## Version Information

**Current Version:** 4.0.0
**Release Date:** 2026-01-07
**Backward Compatible:** Yes ✅

See [CHANGELOG.md](../CHANGELOG.md) for complete version history.

---

## Support

- **Documentation:** [docs/README.md](../docs/README.md)
- **Issues:** https://github.com/ozand/shared-knowledge-base/issues
