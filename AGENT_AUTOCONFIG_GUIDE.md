# Agent Auto-Configuration System - Complete Guide

**Date:** 2026-01-06
**Pattern:** AGENT-AUTO-001
**Purpose:** Automatic agent configuration from Shared KB

---

## 🎯 The Problem: Manual Configuration Doesn't Scale

**Before (Manual Approach):**
```
For each new project:
1. Manually edit system prompts
2. Manually configure project name
3. Manually create GitHub labels
4. Manually add attribution instructions
5. Test each agent individually

→ 30 minutes per project
→ Doesn't scale beyond 10 projects
→ Errors from manual copy-paste
```

**After (Automatic Approach):**
```
For each new project:
1. Add Shared KB as submodule
2. Run bootstrap script once
3. Agent auto-configures itself

→ 2 minutes per project
→ Scales to 100+ projects
→ Zero copy-paste errors
```

---

## 🚀 Quick Start: 3 Steps to Full Automation

### Step 1: Deploy Shared KB to Project

```bash
cd your-project/
git init

# Add Shared KB as submodule
git submodule add git@github.com:ozand/shared-knowledge-base.git docs/knowledge-base/shared

# Or clone directly
git clone git@github.com:ozand/shared-knowledge-base.git docs/knowledge-base/shared
```

### Step 2: Run Bootstrap Script (Once)

```bash
# Auto-detect everything
python docs/knowledge-base/shared/tools/kb-agent-bootstrap.py
```

**Output:**
```
🤖 Agent Bootstrap: Starting...
  → Project: PARSER
  → Agent Type: claude-code
  → Session: session-20260106_143000
  → KB Path: docs/knowledge-base/shared
  → KB Version: 1.0
✅ Bootstrap Complete
```

**Creates:** `.agent-config.local` with full configuration

### Step 3: Agent Knows Everything

Agent now automatically:
- ✅ Adds attribution to GitHub issues
- ✅ Knows project name (auto-detected)
- ✅ Follows KB contribution workflow
- ✅ Validates YAML before committing
- ✅ Uses isolated testing for PRs
- ✅ Follows all KB patterns

**Zero manual configuration needed!**

---

## 📁 How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Shared Knowledge Base                     │
│                                                               │
│  universal/agent-instructions/                               │
│  ├── base-instructions.yaml  ← Instructions for all agents  │
│  ├── context-detection.yaml    ← How to detect context      │
│  └── templates/                 ← Issue/PR templates         │
│                                                               │
│  tools/                                                       │
│  └── kb-agent-bootstrap.py    ← Bootstrap script            │
└─────────────────────────────────────────────────────────────┘
                          ↓
                          ↓ git submodule
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                      Your Project                            │
│                                                               │
│  $ python docs/knowledge-base/shared/tools/kb-agent-bootstrap.py │
│                          ↓                                   │
│  .agent-config.local  ← Auto-generated configuration        │
└─────────────────────────────────────────────────────────────┘
                          ↓
                          ↓ Agent reads .agent-config.local
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                       Agent Knows:                           │
│  • GitHub attribution (GITHUB-ATTRIB-001)                    │
│  • KB contribution workflow (AGENT-HANDOFF-001)              │
│  • Quality standards (YAML-001, ISOLATED-TEST-001)           │
│  • Project name, agent type, session ID                      │
│  • All available capabilities                                │
└─────────────────────────────────────────────────────────────┘
```

### Auto-Detection Flow

```
1. Agent starts
   ↓
2. Runs bootstrap script
   ↓
3. Detects project context:
   • project_name:
     - From git remote (git@github.com:user/PARSER.git → PARSER)
     - From package.json (name field)
     - From pyproject.toml (project.name)
     - From .agent-config (explicit override)
     - Default: "unknown"

   • agent_type:
     - From AGENT_TYPE env var
     - From .agent-config
     - Default: "claude-code"

   • session_id:
     - From AGENT_SESSION env var
     - Auto-generated: session-20260106_143000
   ↓
4. Finds Shared KB:
   - docs/knowledge-base/shared/
   - .shared-kb/
   - KB_PATH env var
   ↓
5. Loads instructions from KB
   ↓
6. Creates .agent-config.local
   ↓
7. Agent reads configuration
   ↓
8. Agent follows all KB patterns automatically
```

---

## 📝 Configuration Files

### .agent-config (Optional, Commit to Git)

Override auto-detection:

```json
{
  "project_name": "PARSER",
  "agent_type": "claude-code",
  "kb_path": "docs/knowledge-base/shared",
  "auto_update": true,
  "features": {
    "github_attribution": true,
    "kb_contribution": true
  }
}
```

### .agent-config.local (Auto-Generated, Don't Commit)

Generated by bootstrap script:

```json
{
  "agent_type": "claude-code",
  "project_name": "PARSER",
  "session_id": "session-20260106_143000",
  "kb_path": "docs/knowledge-base/shared",
  "kb_version": "1.0",
  "kb_last_updated": "2026-01-06",
  "capabilities": {
    "github_attribution": {
      "pattern": "GITHUB-ATTRIB-001",
      "priority": "HIGH",
      "required_when": "creating_github_issues_or_prs",
      "steps": [
        "Add 'Created By' section at top of issue body",
        "Use labels: agent:*, project:*, agent-type:*"
      ]
    },
    "kb_contribution": {
      "pattern": "AGENT-HANDOFF-001",
      "priority": "HIGH",
      "required_when": "contributing_to_shared_kb"
    },
    "quality_standards": {
      "pattern": "various",
      "priority": "MEDIUM",
      "required_when": "always"
    }
  },
  "enabled_features": [
    "github_attribution",
    "kb_contribution",
    "quality_standards"
  ],
  "available_capabilities": {
    "github_operations": {
      "create_issue": {
        "enabled": true,
        "requires_attribution": true
      }
    },
    "kb_operations": {
      "search": {
        "enabled": true,
        "command": "kb search '{query}'"
      }
    }
  }
}
```

---

## 🔄 Update Flow: How Agents Get KB Updates

### Scenario: You Update Shared KB

**1. Add new pattern to KB:**
```bash
cd shared-knowledge-base/
# Add new pattern: universal/patterns/NEW-PATTERN.yaml
# Update base-instructions.yaml
git commit -m "Add NEW-PATTERN-001"
git push
```

**2. Projects pull updates:**
```bash
cd your-project/docs/knowledge-base/shared
git pull origin main
```

**3. Agents detect updates:**
```python
# Agent's update cycle (runs every hour)
def check_kb_updates():
    kb_path = find_knowledge_base()

    # Check git version
    current_version = read_version(kb_path)
    latest_version = get_latest_version(kb_path)

    if latest_version != current_version:
        # Pull updates
        subprocess.run(["git", "-C", kb_path, "pull"])

        # Reload instructions
        new_instructions = load_instructions(kb_path)

        # Apply new capabilities
        apply_instructions(new_instructions, detect_context())

        print("✅ KB updated. New capabilities loaded!")
```

**4. Agents start using new pattern immediately**

No manual configuration needed!

---

## 💡 Usage Examples

### Example 1: New Project Setup

**Goal:** Set up new project with full agent capabilities

**Steps:**
```bash
# 1. Create project
mkdir my-new-project
cd my-new-project

# 2. Initialize git
git init

# 3. Add Shared KB
git submodule add git@github.com:ozand/shared-knowledge-base.git docs/knowledge-base/shared

# 4. Run bootstrap (optional - agent can run it)
python docs/knowledge-base/shared/tools/kb-agent-bootstrap.py

# 5. Done! Agent knows everything
```

**Time:** 2 minutes
**Manual work:** Zero

### Example 2: Agent Creates GitHub Issue

**Before (Manual):**
```python
# Agent must know:
issue_title = "Add PYTHON-015: Async Timeout"
issue_body = "## Problem\n..."

# Agent must manually add attribution (if it remembers)
issue_body = f"---\n**Created By:** 🤖 Claude Code\n**Project:** PARSER\n---\n\n{issue_body}"

# Agent must manually add labels (if it remembers)
labels = ["agent:claude-code", "project:PARSER", "agent-type:debugging"]
```

**After (Automatic):**
```python
# Agent reads .agent-config.local
config = load_agent_config()

# Agent applies template automatically
issue_body = render_template(
    "issue-template.md",
    context=config
)

# Agent uses correct labels automatically
labels = config["capabilities"]["github_attribution"]["labels"]
```

### Example 3: Update KB with New Pattern

**Goal:** Add new quality standard to all projects

**Steps:**
```bash
# 1. Update Shared KB
cd shared-knowledge-base/

# 2. Add new pattern
cat > universal/patterns/new-standard.yaml <<EOF
pattern: NEW-STANDARD-001
enabled: true
priority: "HIGH"
EOF

# 3. Update base-instructions.yaml
# Add new-standard to instructions list

# 4. Commit and push
git add .
git commit -m "Add NEW-STANDARD-001"
git push
```

**Result:**
- All projects pull KB updates
- All agents detect new instructions
- All agents start using NEW-STANDARD-001 automatically
- Zero manual configuration

---

## 🛠️ Advanced Usage

### Custom Project Name

If auto-detection gets it wrong:

```bash
# Create .agent-config
cat > .agent-config <<EOF
{
  "project_name": "my-custom-name"
}
EOF

git add .agent-config
git commit -m "Configure agent project name"
```

### Custom Agent Type

```bash
# Export environment variable
export AGENT_TYPE="cursor-ai"

# Or add to .agent-config
cat > .agent-config <<EOF
{
  "agent_type": "cursor-ai"
}
EOF
```

### Disable Specific Features

```bash
cat > .agent-config <<EOF
{
  "features": {
    "github_attribution": true,
    "kb_contribution": false  // Disable KB contribution
  }
}
EOF
```

### Run Bootstrap in CI/CD

```yaml
# .github/workflows/agent-setup.yml
name: Agent Setup

steps:
  - name: Bootstrap Agent
    run: |
      python docs/knowledge-base/shared/tools/kb-agent-bootstrap.py

  - name: Verify Configuration
    run: |
      cat .agent-config.local
      test -f .agent-config.local
```

---

## 🎯 Best Practices

### For Shared KB Maintainers

1. **Version instructions properly**
   ```yaml
   version: "1.0"
   last_updated: "2026-01-06"
   ```

2. **Test bootstrap script**
   ```bash
   python tools/kb-agent-bootstrap.py --dry-run
   ```

3. **Document breaking changes**
   ```yaml
   backward_compatible: false
   deprecation_notice: "Migrate to new format by 2026-02-01"
   ```

4. **Keep templates updated**
   - When updating patterns, update templates too
   - Test templates with real examples

### For Project Developers

1. **Keep Shared KB as submodule**
   ```bash
   git submodule add <kb-url> docs/knowledge-base/shared
   # Don't clone directly
   ```

2. **Commit .agent-config, ignore .agent-config.local**
   ```bash
   echo ".agent-config.local" >> .gitignore
   git add .agent-config
   ```

3. **Update KB regularly**
   ```bash
   # Add to git hooks or CI
   cd docs/knowledge-base/shared && git pull
   ```

4. **Don't edit KB files directly**
   - Contribute patterns via GitHub issues
   - Follow AGENT-HANDOFF-001 workflow

### For Agent Developers

1. **Run bootstrap on startup**
   ```python
   def initialize_agent():
       bootstrap_agent()
       config = load_agent_config()
       return config
   ```

2. **Check for updates periodically**
   ```python
   while True:
       check_kb_updates()
       time.sleep(3600)  # Every hour
   ```

3. **Use templates from KB**
   ```python
   template = load_template("issue-template.md")
   issue_body = render_template(template, config)
   ```

---

## 📊 Comparison: Manual vs Automatic

| Feature | Manual | Automatic |
|---------|--------|-----------|
| **Setup time** | 30 min | 2 min |
| **Scalability** | ~10 projects | Unlimited |
| **Updates** | Reconfigure each project | Update KB once |
| **Error rate** | High (copy-paste) | Zero |
| **Maintenance** | High | Low |
| **New patterns** | Manual distribution | Auto-distributed |
| **Project names** | Manual config | Auto-detected |
| **Consistency** | Variable | Guaranteed |

---

## ✅ Checklist

### For New Projects

- [ ] Add Shared KB as submodule
- [ ] Run bootstrap script once
- [ ] Verify .agent-config.local created
- [ ] Test agent capabilities
- [ ] Add .agent-config.local to .gitignore

### For KB Updates

- [ ] Update base-instructions.yaml
- [ ] Version the update
- [ ] Test bootstrap script
- [ ] Commit and push to main
- [ ] Notify projects to pull updates

### For Agent Integration

- [ ] Call bootstrap on startup
- [ ] Load .agent.config.local
- [ ] Use KB templates
- [ ] Check for updates periodically
- [ ] Follow KB patterns

---

## 🔧 Troubleshooting

### Problem: Bootstrap can't find KB

**Solution:**
```bash
# Set KB_PATH explicitly
export KB_PATH="/path/to/kb"
python tools/kb-agent-bootstrap.py
```

### Problem: Wrong project name detected

**Solution:**
```bash
# Create .agent-config with explicit name
cat > .agent-config <<EOF
{"project_name": "correct-name"}
EOF
```

### Problem: Agent not using new KB pattern

**Solution:**
```bash
# Pull KB updates
cd docs/knowledge-base/shared && git pull

# Re-run bootstrap
python tools/kb-agent-bootstrap.py
```

### Problem: PyYAML not installed

**Solution:**
```bash
pip install pyyaml
# Or script uses basic parser (limited functionality)
```

---

## 📚 References

- **AGENT-AUTO-001:** Full pattern documentation
- **universal/agent-instructions/base-instructions.yaml:** Agent instructions
- **tools/kb-agent-bootstrap.py:** Bootstrap script
- **GITHUB-ATTRIB-001:** GitHub attribution pattern
- **AGENT-HANDOFF-001:** KB contribution workflow

---

**Status:** ✅ Production Ready
**Last Updated:** 2026-01-06
**Pattern:** AGENT-AUTO-001
**Version:** 1.0
