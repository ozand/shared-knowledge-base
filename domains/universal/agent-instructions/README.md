# Agent Instructions

**Purpose:** Auto-loaded instructions for all agents using Shared KB

**Pattern:** AGENT-AUTO-001
**Auto-discovery:** Yes - agents load these automatically on bootstrap

---

## 📁 File Structure

```
universal/agent-instructions/
├── README.md                  # This file
├── base-instructions.yaml     # Main instructions for all agents
└── templates/                 # Issue/PR/comment templates
    ├── issue-header.md       # "Created By" section
    ├── issue-template.md     # Full issue template
    ├── pr-template.md        # Full PR template
    └── comment-template.md   # Comment format
```

---

## 🎯 How It Works

### Agent Bootstrap Process

1. Agent starts → runs `tools/kb-agent-bootstrap.py`
2. Script detects context (project name, agent type)
3. Script loads this file: `base-instructions.yaml`
4. Script creates `.agent-config.local` with full configuration
5. Agent reads configuration and follows instructions automatically

### What's in base-instructions.yaml?

```yaml
instructions:
  github_attribution:
    enabled: true
    pattern: "GITHUB-ATTRIB-001"
    steps:
      - Add "Created By" at top
      - Use labels: agent:*, project:*, agent-type:*

  kb_contribution:
    enabled: true
    pattern: "AGENT-HANDOFF-001"
    steps:
      - Search KB first
      - Validate YAML
      - Create issue with attribution

  quality_standards:
    enabled: true
    pattern: "various"
    standards:
      - YAML-001: YAML syntax
      - ISOLATED-TEST-001: PR testing
      - AGENT-ACCOUNTABILITY-001: Follow own recommendations
```

---

## 🔄 Updating Instructions

### For KB Maintainers

When you want to add new agent behavior:

1. **Edit base-instructions.yaml**
   ```yaml
   instructions:
     new_feature:
       enabled: true
       pattern: "NEW-PATTERN-001"
       steps: [...]
   ```

2. **Update version**
   ```yaml
   version: "1.1"
   last_updated: "2026-01-07"
   ```

3. **Commit and push**
   ```bash
   git add universal/agent-instructions/base-instructions.yaml
   git commit -m "Update agent instructions: add NEW-PATTERN-001"
   git push
   ```

4. **All projects get updates automatically**
   - Projects run: `git pull` in KB
   - Agents detect version change
   - Agents reload instructions
   - Agents start using new pattern

### For Project Developers

**Pull KB updates:**
```bash
cd docs/knowledge-base/shared
git pull origin main
```

**Re-run bootstrap (optional):**
```bash
python tools/kb-agent-bootstrap.py
```

---

## 📝 Templates

Templates use variable substitution:

### Issue Header Template

```markdown
---
**Created By:** 🤖 {{agent_name}}
**Project:** {{project_name}}
**Agent Type:** {{agent_type}}
**Session:** {{session_id}}
**Date:** {{date}}
---
```

**Variables provided by bootstrap:**
- `{{agent_name}}` - Auto-detected from AGENT_TYPE env or .agent-config
- `{{project_name}}` - Auto-detected from git remote or config files
- `{{agent_type}}` - Task type (code-generation, debugging, etc.)
- `{{session_id}}` - Auto-generated session hash
- `{{date}}` - Current date

---

## 🎓 Examples

### Example 1: Agent Creates GitHub Issue

**Agent reads config:**
```python
config = load_json(".agent-config.local")

# Config contains:
# {
#   "project_name": "PARSER",
#   "agent_type": "claude-code",
#   "capabilities": {
#     "github_attribution": {...}
#   }
# }
```

**Agent uses template:**
```python
template = read_file("docs/knowledge-base/shared/universal/agent-instructions/templates/issue-header.md")
issue_body = render_template(template, config)

# Result:
# ---
# **Created By:** 🤖 claude-code
# **Project:** PARSER
# **Agent Type:** code-generation
# **Session:** session-20260106_143000
# **Date:** 2026-01-06
# ---
```

### Example 2: Add New Agent Capability

**Goal:** Make agents validate YAML before committing

**1. Update base-instructions.yaml:**
```yaml
instructions:
  yaml_validation:
    enabled: true
    pattern: "YAML-001"
    required_when: "creating_or_editing_yaml_files"
    steps:
      - step: "Validate YAML before committing"
        command: "python tools/kb.py validate {file}"
```

**2. Update version:**
```yaml
version: "1.1"
last_updated: "2026-01-06"
```

**3. Commit:**
```bash
git add base-instructions.yaml
git commit -m "Add YAML validation to agent instructions"
git push
```

**4. All agents start validating YAML automatically**

---

## 🔧 Configuration Priority

Agent context is determined in this order (highest to lowest priority):

1. **Environment Variables**
   - `AGENT_TYPE` - Agent type
   - `PROJECT_NAME` - Project name
   - `AGENT_SESSION` - Session ID
   - `KB_PATH` - KB path

2. **.agent-config** (Project-specific, commit to repo)
   ```json
   {
     "project_name": "PARSER",
     "agent_type": "claude-code"
   }
   ```

3. **Auto-Detection**
   - Project name: git remote → package.json → pyproject.toml → "unknown"
   - Agent type: defaults to "claude-code"
   - Session: auto-generated as "session-{timestamp}"

---

## 📚 Related Documentation

- **AGENT_AUTOCONFIG_GUIDE.md** - Complete guide to automatic system
- **tools/kb-agent-bootstrap.py** - Bootstrap script implementation
- **universal/patterns/agent-auto-configuration.yaml** - AGENT-AUTO-001 pattern
- **universal/patterns/github-agent-attribution.yaml** - GITHUB-ATTRIB-001 pattern

---

## ✅ Quality Standards

When editing these files:

- [ ] YAML syntax is valid
- [ ] Version is updated
- [ ] Templates use correct variables
- [ ] Instructions are clear and actionable
- [ ] Test with bootstrap script

**Test command:**
```bash
python tools/kb-agent-bootstrap.py --dry-run
```

---

**Maintained by:** Shared KB Curator
**Last Updated:** 2026-01-06
**Pattern:** AGENT-AUTO-001
