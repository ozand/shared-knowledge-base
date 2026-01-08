# Upgrade Guide: Shared Knowledge Base v4.0

**Complete guide for upgrading from v3.x to v4.0**

**Last Updated:** 2026-01-07
**Target Version:** 4.0.0

---

## 📋 What's New in v4.0?

### Major Features

**🚀 Progressive Domain Loading (Phase 1)**
- 83% token reduction for single-domain projects
- 12-domain taxonomy
- Domain index: ~80 tokens (99.1% reduction from 8,829)

**🔗 GitHub-Native Contribution System (Phase 2)**
- Submit entries via GitHub Issues
- Zero infrastructure costs
- Automated curator workflows

**🔄 Automated Feedback Loop (Phase 3)**
- Curator slash commands
- Automatic KB updates
- Complete agent-curator communication

### Compatibility

**Backward Compatible:** ✅ Yes
- All v3.x tools work unchanged
- Existing entries compatible
- Progressive loading is optional

---

## 🔧 Preparation

### Before You Upgrade

**1. Check current version:**
```bash
cd .kb/shared
git log --oneline -1
grep version .kb-version
```

**2. Backup current installation:**
```bash
# Stash any local changes
cd .kb/shared
git stash

# Or backup entire directory
cp -r .kb/shared .kb/shared.backup
```

**3. Check for uncommitted changes:**
```bash
git status
```

---

## ⚡ Upgrade Methods

### Method 1: Automatic Update (Recommended)

**For most users:**

```bash
# 1. Navigate to submodule
cd .kb/shared

# 2. Fetch latest changes
git fetch origin

# 3. Checkout latest main branch
git checkout origin/main

# 4. Return to project root
cd ../..

# 5. Update submodule reference
git submodule update --remote .kb/shared

# 6. Rebuild index
python .kb/shared/tools/kb.py index -v

# 7. Test new features
python .kb/shared/tools/kb_domains.py --kb-dir .kb/shared list
```

### Method 2: Tag-Based Update

**For specific version control:**

```bash
# 1. Navigate to submodule
cd .kb/shared

# 2. Fetch tags
git fetch origin --tags

# 3. Checkout v4.0.0 tag
git checkout v4.0.0

# 4. Return to project root
cd ../..

# 5. Update submodule reference
git add .kb/shared
git commit -m "Update Shared KB to v4.0.0

Progressive loading: 83% token reduction
GitHub-native contribution: Zero infrastructure
Automated feedback loop: Complete curator-agent communication

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# 6. Push
git push origin main

# 7. Rebuild index
python .kb/shared/tools/kb.py index -v
```

### Method 3: Fresh Installation

**If you want to start fresh:**

```bash
# 1. Remove old submodule
git submodule deinit -f .kb/shared
git rm -f .kb/shared
rm -rf .git/modules/.kb/shared

# 2. Add new submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared

# 3. Configure progressive loading
cd .kb/shared
git sparse-checkout init
git sparse-checkout set docker postgresql universal tools _domain_index.yaml
git sparse-checkout reapply

# 4. Initialize
cd ../..
python .kb/shared/tools/kb.py index -v
```

---

## 🆕 After Upgrade

### Enable Progressive Loading (Optional but Recommended)

```bash
# 1. Navigate to submodule
cd .kb/shared

# 2. Initialize sparse checkout
git sparse-checkout init

# 3. Choose your domains
git sparse-checkout set docker postgresql universal tools _domain_index.yaml

# 4. Apply
git sparse-checkout reapply

# 5. Verify
ls -la
# Should see only: docker/, postgresql/, universal/, tools/, _domain_index.yaml
```

### Test New Features

**1. Test progressive loading:**
```bash
python .kb/shared/tools/kb_domains.py --kb-dir .kb/shared list
python .kb/shared/tools/kb_domains.py info docker
```

**2. Test search:**
```bash
python .kb/shared/tools/kb.py search "docker"
```

**3. Test submission tool (optional):**
```bash
python .kb/shared/tools/kb_submit.py submit --help
```

### Update Configuration Files

**Update .kb/.kb-config.yaml:**
```yaml
version: "4.0"
paths:
  shared: ".kb/shared"
  local: ".kb/local"

shared_repository:
  url: "https://github.com/ozand/shared-knowledge-base.git"
  branch: "main"
  tag: "v4.0.0"

domains:
  enabled: true
  progressive_loading: true
  loaded_domains:
    - docker
    - postgresql
    - universal
```

**Update .claude/settings.json:**
```json
{
  "contextSearch": true,
  "contextPaths": [
    ".kb/shared/**/*.{md,yaml,py}",
    ".kb/shared/_domain_index.yaml"
  ],
  "hooks": [
    {
      "name": "kb-index-check",
      "events": ["SessionStart"],
      "command": "python .kb/shared/tools/kb.py index --check"
    }
  ]
}
```

---

## 🔍 Verification

### Verify Upgrade Success

**1. Check version:**
```bash
cd .kb/shared
git describe --tags
# Should show: v4.0.0
grep version ../.kb-version
# Should show: 4.0
```

**2. Check files:**
```bash
# New tools in v4.0
ls tools/kb_domains.py
ls tools/kb_submit.py
ls tools/test_feedback_loop.py
ls tools/test_progressive_loading.py

# New documentation
ls docs/implementation/
ls docs/YAML-SCHEMA-V3.1.md
ls CHANGELOG.md
```

**3. Test functionality:**
```bash
# Test search
python .kb/shared/tools/kb.py search "test"

# Test domain loading
python .kb/shared/tools/kb_domains.py --kb-dir .kb/shared list

# Test submission
python .kb/shared/tools/kb_submit.py submit --help
```

---

## 🐛 Troubleshooting

### Issue: Submodule Update Failed

**Solution:**
```bash
# Force update
cd .kb/shared
git fetch origin
git checkout origin/main
cd ../..
git submodule update --remote --merge .kb/shared
```

### Issue: Index Build Failed

**Solution:**
```bash
# Force rebuild
python .kb/shared/tools/kb.py index -v

# If still fails, check dependencies
pip install pyyaml
```

### Issue: Progressive Loading Not Working

**Solution:**
```bash
cd .kb/shared

# Reinitialize
git sparse-checkout disable
git sparse-checkout init
git sparse-checkout set docker postgresql universal tools _domain_index.yaml
git sparse-checkout reapply
```

### Issue: Missing New Tools

**Solution:**
```bash
# Verify you're on v4.0.0
cd .kb/shared
git checkout v4.0.0

# Verify files exist
ls tools/kb_domains.py
ls tools/kb_submit.py
```

---

## 📊 What Changed?

### New Tools

| Tool | Purpose | Lines |
|------|---------|-------|
| `tools/kb_domains.py` | Domain management | 373 |
| `tools/kb_github_api.py` | GitHub API fallback | 254 |
| `tools/kb_submit.py` | Submit entries | 296 |
| `tools/test_progressive_loading.py` | Test progressive loading | 398 |
| `tools/test_feedback_loop.py` | Test feedback loop | 398 |

### New Documentation

| Document | Purpose |
|----------|---------|
| `CHANGELOG.md` | Version history |
| `docs/README.md` | Documentation hub |
| `docs/YAML-SCHEMA-V3.1.md` | YAML schema |
| `docs/implementation/` | Implementation reports |
| `QUICKSTART-DOMAINS.md` | Progressive loading guide |

### New Features

1. **Progressive Domain Loading**
   - Load only needed domains
   - 83% token reduction
   - 12-domain taxonomy

2. **GitHub-Native Contribution**
   - Submit via GitHub Issues
   - Automated workflows
   - Zero infrastructure

3. **Automated Feedback Loop**
   - Curator slash commands
   - Auto-update on approval
   - Complete communication

---

## 🤖 For Agents: Critical Instructions

### ⚠️ READ THIS BEFORE UPDATING

**If you are an AI agent updating Shared KB:**

1. **READ FIRST:**
   - `for-claude-code/AGENT-UPDATE-INSTRUCTIONS.md` (full instructions)
   - `for-claude-code/KB-UPDATE-QUICK-REFERENCE.md` (quick reference)

2. **3 GOLDEN RULES:**
   - ⛔ **NEVER** modify files in `.kb/shared/` (submodule is READ-ONLY)
   - ✅ **DATA** is source of truth (if tool breaks → tool has bug)
   - ❓ **When unsure** → ASK, don't fix

3. **COMMON MISTAKES TO AVOID:**
   - ❌ Don't edit `_domain_index.yaml` to "fix" format
   - ❌ Don't add fields not in v4.0.0 specification
   - ❌ Don't modify tool code in `.kb/shared/tools/`
   - ✅ Do check upstream if tool fails
   - ✅ Do report tool bugs to Shared KB repository

4. **IF TOOL FAILS:**
   ```
   Check: T:\Code\shared-knowledge-base\_domain_index.yaml
   Compare: Is format the same?

   If YES → Tool has bug, report it
   If NO → Incomplete update, retry checkout
   ```

**Example from real case (tmp/tmp1.txt):**
- ❌ Agent: "Error in _domain_index.yaml format" → Edited file
- ✅ Correct: "Error in kb_domains.py line 415" → Tool incompatible with data

**Full documentation:** `@for-claude-code/AGENT-UPDATE-INSTRUCTIONS.md`

---

## 🎓 Next Steps

### Learn Progressive Loading

```bash
# Read the guide
cat .kb/shared/QUICKSTART-DOMAINS.md

# List available domains
python .kb/shared/tools/kb_domains.py --kb-dir .kb/shared list

# Load specific domain
python .kb/shared/tools/kb_domains.py load docker
```

### Learn Contribution Workflow

```bash
# Read the guide
cat .kb/shared/for-claude-code/README.md

# Submit test entry
python .kb/shared/tools/kb_submit.py submit --help
```

### Explore New Features

```bash
# Run test suites
python .kb/shared/tools/test_progressive_loading.py
python .kb/shared/tools/test_feedback_loop.py

# Check domain info
python .kb/shared/tools/kb_domains.py info postgresql
```

---

## 📞 Support

### Documentation

- **[README.md](../README.md)** - Project overview
- **[CHANGELOG.md](../CHANGELOG.md)** - Version history
- **[docs/README.md](../docs/README.md)** - Documentation hub
- **[docs/implementation/](../docs/implementation/)** - Implementation details

### Troubleshooting

- **[for-claude-code/README.md](../for-claude-code/README.md)** - Claude Code guide
- **[AGENT-QUICK-START.md](../for-claude-code/AGENT-QUICK-START.md)** - Agent quick start

### Issues

- **GitHub Issues:** https://github.com/ozand/shared-knowledge-base/issues
- **Check existing issues first**

---

## ✅ Upgrade Checklist

- [ ] Backup current installation
- [ ] Update submodule to v4.0.0
- [ ] Rebuild index
- [ ] Test search functionality
- [ ] Test domain loading
- [ ] Update configuration files
- [ ] Enable progressive loading (optional)
- [ ] Test submission tool (optional)
- [ ] Read new documentation
- [ ] Verify all tests pass

---

## 🎉 Congratulations!

You've successfully upgraded to Shared Knowledge Base v4.0!

### What You Get

- ✅ Progressive domain loading (83% token savings)
- ✅ GitHub-native contribution (zero infrastructure)
- ✅ Automated feedback loop (complete automation)
- ✅ 149 knowledge entries across 12 domains
- ✅ Comprehensive documentation
- ✅ 93.75% test coverage

### Next Steps

1. **Enable progressive loading** - Load only domains you need
2. **Explore new features** - Try kb_submit.py, kb_domains.py
3. **Read documentation** - Check out docs/README.md
4. **Submit knowledge** - Contribute back to Shared KB

---

**Version:** 4.0.0
**Release Date:** 2026-01-07
**Backward Compatible:** Yes ✅

Happy coding with v4.0! 🚀
