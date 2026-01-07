# Architecture Analysis: Shared KB Integration Pattern

**Date:** 2026-01-07
**Issue:** Agents/Skills/Commands in wrong repository
**Status:** Analysis Complete

---

## Problem Statement

**Current State (WRONG):**
```
shared-knowledge-base/
├── .claude/
│   ├── agents/         ❌ Should NOT be here
│   ├── skills/         ❌ Should NOT be here
│   └── commands/       ❌ Should NOT be here
├── python/             ✅ Correct (knowledge)
├── docker/             ✅ Correct (knowledge)
└── tools/kb.py         ✅ Correct (management tool)
```

**Problem:**
- Agents/skills/commands are in shared-knowledge-base repository
- They should be in PROJECTS that use shared-knowledge-base
- Each project needs its own agents configured for its context
- shared-knowledge-base should only contain: knowledge + management tools

---

## Correct Architecture

### shared-knowledge-base Repository

**Purpose:** Centralized knowledge base + management tools

**Contents:**
```
shared-knowledge-base/
├── python/                    ✅ Knowledge entries
├── docker/                    ✅ Knowledge entries
├── universal/                 ✅ Knowledge entries
├── postgresql/                ✅ Knowledge entries
├── framework/                 ✅ Knowledge entries
├── tools/                     ✅ Management tools
│   ├── kb.py                 # KB search, index, validate
│   ├── kb_meta.py            # Metadata management
│   └── validate-kb.py        # Validation
├── curator/                   ✅ Curator documentation
│   ├── AGENT.md              # Curator role
│   ├── SKILLS.md             # Curator skills
│   └── QUALITY_STANDARDS.md  # Quality rubric
├── for-projects/              ✅ Integration templates (NEW)
│   ├── agent-templates/      # Agent templates for projects
│   ├── skill-templates/      # Skill templates for projects
│   ├── command-templates/    # Command templates for projects
│   ├── setup.py              # Installation script
│   └── PROJECT-INTEGRATION.md # Integration guide
├── for-claude-code/           ✅ Claude Code specific docs
└── docs/research/             ✅ Research documentation
```

**What BELONGS here:**
- ✅ Knowledge entries (YAML files)
- ✅ Management tools (kb.py, validate-kb.py)
- ✅ Curator documentation (maintaining KB quality)
- ✅ Integration templates (for projects to use)
- ✅ Documentation (how to use KB)

**What DOES NOT belong here:**
- ❌ Project-specific agents (each project has different needs)
- ❌ Project-specific skills (each project has different workflows)
- ❌ Project-specific commands (each project has different conventions)

### Working Project (e.g., my-web-app)

**Purpose:** Application code + KB integration

**Contents:**
```
my-web-app/                    # Working project
├── src/                       # Application code
├── tests/                     # Application tests
├── .claude/                   ✅ Claude Code configuration
│   ├── CLAUDE.md             # Project memory
│   ├── agents/               ✅ Project-specific agents
│   │   ├── kb-agent.md       # KB management agent
│   │   └── subagents/        # Researcher, Debugger, etc.
│   ├── skills/               ✅ Project-specific skills
│   │   ├── kb-search/        # KB search skill
│   │   ├── kb-validate/      # KB validation skill
│   │   └── kb-create/        # KB creation skill
│   ├── commands/             ✅ Project-specific commands
│   │   ├── kb-search.md
│   │   ├── kb-validate.md
│   │   ├── kb-create.md
│   │   ├── retrospective.md
│   │   ├── kb-sync.md
│   │   └── kb-query.md
│   ├── settings.json         # Claude Code settings
│   └── hooks/                # Project-specific hooks
├── docs/
│   └── knowledge-base/        ✅ Local KB (project-specific)
│       ├── shared/            ✅ Submodule to shared-knowledge-base
│       │   ├── python/
│       │   ├── docker/
│       │   └── tools/
│       └── project/           ✅ Project-specific knowledge
│           ├── errors/
│           └── patterns/
└── .kb-config.yaml           # KB configuration
```

**What belongs here:**
- ✅ Application code
- ✅ Project-specific agents (configured for this project)
- ✅ Project-specific skills (project workflow)
- ✅ Project-specific commands (project conventions)
- ✅ Local KB (project-specific knowledge)
- ✅ Shared KB (submodule reference)

---

## Separation of Concerns

### shared-knowledge-base Responsibilities

1. **Store Knowledge:** Maintain YAML knowledge entries
2. **Provide Tools:** kb.py for searching, indexing, validating
3. **Quality Standards:** Define what makes a good KB entry
4. **Integration Templates:** Provide templates for projects
5. **Documentation:** How to use and maintain KB

**NOT responsible for:**
- ❌ How individual projects use the KB
- ❌ Project-specific agent configurations
- ❌ Project-specific workflows

### Working Project Responsibilities

1. **Application Code:** Build the product
2. **KB Integration:** Install agents/skills/commands from templates
3. **Configuration:** Adapt agents to project context
4. **Local Knowledge:** Maintain project-specific KB entries
5. **Synchronization:** Push shared knowledge to repository

**Responsible for:**
- ✅ How agents work in this project's context
- ✅ Project-specific workflows
- ✅ Local knowledge capture

---

## Template System

### for-projects/ Directory Structure

```
shared-knowledge-base/
└── for-projects/
    ├── README.md                      # Overview
    ├── PROJECT-INTEGRATION.md         # Complete integration guide
    ├── quick-start.md                 # 5-minute setup
    ├── agent-templates/               # Agent templates
    │   ├── README.md
    │   ├── kb-agent.md                # KB management agent
    │   └── subagents/
    │       ├── researcher.md
    │       ├── debugger.md
    │       ├── validator.md
    │       └── knowledge-curator.md
    ├── skill-templates/               # Skill templates
    │   ├── README.md
    │   ├── kb-search/
    │   │   └── SKILL.md
    │   ├── kb-validate/
    │   │   └── SKILL.md
    │   ├── kb-index/
    │   │   └── SKILL.md
    │   ├── kb-create/
    │   │   └── SKILL.md
    │   ├── audit-quality/
    │   │   └── SKILL.md
    │   ├── find-duplicates/
    │   │   └── SKILL.md
    │   └── research-enhance/
    │       └── SKILL.md
    ├── command-templates/             # Command templates
    │   ├── README.md
    │   ├── kb-search.md
    │   ├── kb-validate.md
    │   ├── kb-create.md
    │   ├── kb-index.md
    │   ├── retrospective.md
    │   ├── kb-sync.md
    │   └── kb-query.md
    ├── config-templates/              # Configuration templates
    │   ├── settings.json
    │   ├── kb-config.yaml
    │   └── hooks.json
    ├── scripts/                       # Installation scripts
    │   ├── install.py                 # Install agents/skills/commands
    │   ├── update.py                  # Update from templates
    │   └── uninstall.py               # Remove KB integration
    └── examples/                      # Example integrations
        ├── fastapi-project/
        ├── react-project/
        └── python-project/
```

---

## Installation Workflow

### Initial Setup (New Project)

```bash
# 1. In working project directory
cd my-web-app/

# 2. Clone shared-knowledge-base as submodule
git submodule add https://github.com/ozand/shared-knowledge-base \
  docs/knowledge-base/shared

# 3. Run installation script
python docs/knowledge-base/shared/for-projects/scripts/install.py

# 4. Configure for project
# Edit .claude/settings.json
# Edit .claude/CLAUDE.md
# Edit .kb-config.yaml

# 5. Test integration
# Try: /kb-search "docker"
# Try: /retrospective
```

### Installation Script

```python
# docs/knowledge-base/shared/for-projects/scripts/install.py

import os
import shutil
from pathlib import Path

def install_kb_integration():
    """Install Claude Code KB integration into current project."""

    project_root = Path.cwd()
    shared_kb_root = Path(__file__).parent.parent.parent

    # Create .claude directory structure
    claude_dir = project_root / ".claude"
    claude_dir.mkdir(exist_ok=True)

    # Copy agent templates
    agents_src = shared_kb_root / "for-projects/agent-templates"
    agents_dst = claude_dir / "agents"
    if agents_src.exists():
        shutil.copytree(agents_src, agents_dst, dirs_exist_ok=True)
        print("✅ Agents installed")

    # Copy skill templates
    skills_src = shared_kb_root / "for-projects/skill-templates"
    skills_dst = claude_dir / "skills"
    if skills_src.exists():
        shutil.copytree(skills_src, skills_dst, dirs_exist_ok=True)
        print("✅ Skills installed")

    # Copy command templates
    commands_src = shared_kb_root / "for-projects/command-templates"
    commands_dst = claude_dir / "commands"
    if commands_src.exists():
        shutil.copytree(commands_src, commands_dst, dirs_exist_ok=True)
        print("✅ Commands installed")

    # Copy config templates
    settings_src = shared_kb_root / "for-projects/config-templates/settings.json"
    settings_dst = claude_dir / "settings.json"
    if settings_src.exists() and not settings_dst.exists():
        shutil.copy(settings_src, settings_dst)
        print("✅ Settings configured")

    kb_config_src = shared_kb_root / "for-projects/config-templates/kb-config.yaml"
    kb_config_dst = project_root / ".kb-config.yaml"
    if kb_config_src.exists() and not kb_config_dst.exists():
        shutil.copy(kb_config_src, kb_config_dst)
        print("✅ KB configuration created")

    # Create local KB directories
    local_kb = project_root / "docs/knowledge-base"
    local_kb.mkdir(parents=True, exist_ok=True)

    (local_kb / "project/errors").mkdir(parents=True, exist_ok=True)
    (local_kb / "project/patterns").mkdir(parents=True, exist_ok=True)

    print("✅ Local KB directories created")

    print("\n🎉 Installation complete!")
    print("\nNext steps:")
    print("1. Edit .claude/settings.json for your project")
    print("2. Edit .claude/CLAUDE.md with project context")
    print("3. Edit .kb-config.yaml with KB paths")
    print("4. Run: python docs/knowledge-base/shared/tools/kb.py index")

if __name__ == "__main__":
    install_kb_integration()
```

---

## Update Workflow

### Updating from Templates

```bash
# When shared-knowledge-base templates are updated

# 1. Pull latest changes
cd docs/knowledge-base/shared
git pull origin main

# 2. Run update script
cd ../../..
python docs/knowledge-base/shared/for-projects/scripts/update.py

# 3. Review changes
# The script will show what changed
# You can accept or reject each change
```

### Update Script

```python
# docs/knowledge-base/shared/for-projects/scripts/update.py

import os
import shutil
from pathlib import Path
import difflib

def update_from_templates():
    """Update agents/skills/commands from templates."""

    project_root = Path.cwd()
    shared_kb_root = Path(__file__).parent.parent.parent

    # Compare and update agents
    update_directory(
        src=shared_kb_root / "for-projects/agent-templates",
        dst=project_root / ".claude/agents",
        name="Agents"
    )

    # Compare and update skills
    update_directory(
        src=shared_kb_root / "for-projects/skill-templates",
        dst=project_root / ".claude/skills",
        name="Skills"
    )

    # Compare and update commands
    update_directory(
        src=shared_kb_root / "for-projects/command-templates",
        dst=project_root / ".claude/commands",
        name="Commands"
    )

    print("\n✅ Update complete!")

def update_directory(src, dst, name):
    """Update directory from template, showing diffs."""

    if not src.exists():
        print(f"⚠️  {name} template not found")
        return

    for src_file in src.rglob("*"):
        if src_file.is_file():
            relative_path = src_file.relative_to(src)
            dst_file = dst / relative_path

            if dst_file.exists():
                # Show diff
                show_diff(src_file, dst_file)
                # Ask user
                if input(f"Update {relative_path}? [y/N] ").lower() == 'y':
                    shutil.copy(src_file, dst_file)
                    print(f"✅ Updated {relative_path}")
            else:
                # New file
                shutil.copy(src_file, dst_file)
                print(f"✅ Added {relative_path}")

def show_diff(file1, file2):
    """Show diff between two files."""

    with open(file1) as f1, open(file2) as f2:
        diff = difflib.unified_diff(
            f2.readlines(),
            f1.readlines(),
            fromfile=str(file2),
            tofile=str(file1),
            lineterm=""
        )
        print("\n".join(list(diff)[:20]))  # Show first 20 lines
        print("...")

if __name__ == "__main__":
    update_from_templates()
```

---

## Migration Plan

### Step 1: Reorganize shared-knowledge-base

```bash
# Move agents/skills/commands to for-projects/
mkdir -p for-projects/agent-templates
mkdir -p for-projects/skill-templates
mkdir -p for-projects/command-templates

mv .claude/agents/* for-projects/agent-templates/
mv .claude/skills/* for-projects/skill-templates/
mv .claude/commands/* for-projects/command-templates/

# Keep only documentation in .claude/
# .claude/ should only have: CLAUDE.md, settings.json, hooks/
```

### Step 2: Create Installation System

```bash
# Create scripts
for-projects/scripts/install.py
for-projects/scripts/update.py
for-projects/scripts/uninstall.py

# Create documentation
for-projects/PROJECT-INTEGRATION.md
for-projects/quick-start.md
for-projects/README.md
```

### Step 3: Update Documentation

```bash
# Update for-claude-code/README.md
# Add: "How to install in your project"

# Update for-claude-code/CLAUDE.md
# Add: "Installation instructions"

# Create for-projects/examples/
# Show example integrations
```

---

## Benefits of This Architecture

### 1. Clear Separation of Concerns

- **shared-knowledge-base:** Knowledge + tools + templates
- **Projects:** Application + KB integration + local knowledge

### 2. Project Flexibility

- Each project can customize agents
- Each project can add project-specific skills
- Each project can have different workflows

### 3. Easier Updates

- Templates live in one place (shared-knowledge-base)
- Projects update from templates when needed
- Projects can customize without affecting templates

### 4. Better Git History

- shared-knowledge-base: Only knowledge changes
- Projects: Only application + integration changes
- Cleaner git logs, easier to understand

### 5. Scalability

- New projects: Install from templates
- Template updates: All projects can update
- Project customization: Doesn't affect other projects

---

## Example: FastAPI Project Integration

```
fastapi-web-app/
├── app/                        # FastAPI application
├── tests/
├── .claude/                    ✅ Installed from templates
│   ├── agents/
│   │   ├── kb-agent.md        # Configured for FastAPI
│   │   └── subagents/
│   ├── skills/
│   │   ├── kb-search/         # KB search skill
│   │   ├── fastapi-debug/     # FastAPI-specific (custom)
│   │   └── kb-create/
│   ├── commands/
│   │   ├── kb-search.md
│   │   ├── retrospective.md
│   │   └── fastapi-test.md    # FastAPI-specific (custom)
│   └── settings.json          # Configured for FastAPI
├── docs/
│   └── knowledge-base/
│       ├── shared/            ✅ Submodule
│       │   ├── python/
│       │   ├── docker/
│       │   └── for-projects/  # Templates for updates
│       └── project/           ✅ Local KB
│           └── errors/
│               └── fastapi-websocket-timeout.yaml
└── .kb-config.yaml            # Configured paths
```

---

## Summary

**Problem:** Agents/skills/commands in wrong repository
**Solution:** Template-based installation system
**Benefits:** Clear separation, project flexibility, easier updates

**Next Steps:**
1. Move agents/skills/commands to for-projects/
2. Create installation scripts
3. Create integration documentation
4. Provide example integrations

---

**Status:** Analysis Complete
**Recommendation:** Implement template-based system
**Priority:** High (architectural issue)
