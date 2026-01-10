# Shared KB v5.1 Integration Protocol

**Role:** You are an AI Agent initializing a new project environment.
**Objective:** Connect this project to the Shared Knowledge Base.

---

## ⚡ Quick Alternative: Global Skill (Recommended)

If you have the **`shared-kb-bootstrap`** global skill installed, you can initialize Shared KB with a single command:

### One-Command Initialization

```
/kb-init
```

This automatically performs all 5 phases below:
- Creates `.kb/` structure
- Adds and initializes submodule
- Creates `PROJECT.yaml` template
- Installs session-start hook
- Commits changes

### Other Available Commands

```
/kb-update    # Update Shared KB to latest version
/kb-status    # Check Shared KB status and updates
```

### Installing the Global Skill

If you don't have the global skill:

1. Create directory: `C:\Users\ozand\.claude\skills\shared-kb-bootstrap\`
2. Copy files from Shared KB: `.claude/skills/shared-kb-bootstrap/`
3. Restart Claude Code
4. Skill auto-activates on KB-related keywords

**Documentation:** See `@resources/skill-installation.md` (in global skill)

### Manual Process (Below)

If you prefer manual integration or don't have the global skill, follow the 5-phase process below:

---

## 🟢 PHASE 1: File Structure

1. Check if `.kb/` exists. If not, create:
   ```bash
   mkdir -p .kb/context .kb/project/knowledge .kb/project/pending
   ```

**What this creates:**
- `.kb/context/` - Project passport (PROJECT.yaml)
- `.kb/project/knowledge/` - Local KB entries (private)
- `.kb/project/pending/` - Temporary files buffer

---

## 🟢 PHASE 2: Submodule Connection

1. Execute connection to Shared KB:
   ```bash
   git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared
   git submodule update --init --recursive
   ```

**What this does:**
- Clones Shared KB into `.kb/shared/` directory
- Creates `.gitmodules` file in project root
- Agent can read/search files but cannot modify them (read-only)

---

## 🟢 PHASE 3: Project Identity (Context)

1. Create `.kb/context/PROJECT.yaml`.

2. **ACTION:** Ask the user for:
   - `project_name` - Human-readable project name
   - `project_slug` - Short ID (e.g., "backend-v1")
   - `language` - Programming language
   - `framework` - Framework (if applicable)

3. Write the file using this template:
   ```yaml
   meta:
     name: "{PROJECT_NAME}"
     id: "{PROJECT_SLUG}"

   stack:
     language: "{LANGUAGE}"
     framework: "{FRAMEWORK}"

   sharing_criteria:
     # Send to Shared KB via GitHub Issue if matches these
     universal_if:
       - "Generic Pattern"
       - "Library Fix"
       - "Tooling"
       - "Framework-agnostic solution"

     # Keep locally in .kb/project if matches these
     project_specific_if:
       - "Business Logic"
       - "Secrets"
       - "Internal URLs"
       - "Project-specific architecture"
   ```

**Optional:** Create `.kb/context/MEMORY.md` for free-form project knowledge.

---

## 🟢 PHASE 4: Automation Hooks

1. Install the session hook to auto-load knowledge:
   ```bash
   mkdir -p .claude/hooks
   cp .kb/shared/tools/hooks/session-start.sh .claude/hooks/
   chmod +x .claude/hooks/session-start.sh
   ```

**What this does:**
- On session start: checks for updates in `.kb/shared`
- Loads `PROJECT.yaml` and `MEMORY.md` into agent's system prompt
- Agent automatically knows project context

---

## 🟢 PHASE 5: Verification

1. Run a test search to confirm integration:
   ```bash
   python .kb/shared/tools/kb_search.py --scope shared "docker"
   ```

**Expected result:** Agent finds entries in `.kb/shared/domains/docker/`

---

## 🔴 FINAL STEP

Commit the changes:
```bash
git add .kb .claude .gitmodules
git commit -m "Chore: Initialize Shared KB v5.1 integration"
```

Report to user: **"Integration complete. Shared KB is active."**

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Submodule empty | Run `git submodule update --init --recursive` |
| Hook not loading | Check `.claude/hooks/session-start.sh` exists and is executable |
| Agent can't find KB | Verify `.kb/shared/domains/` directory exists |
| Permission denied | Run `chmod +x .claude/hooks/session-start.sh` |

---

## 📚 Additional Resources

- **Complete v5.1 Documentation:** `@docs/v5.1/README.md`
- **Architecture Reference:** `@docs/v5.1/ARD.md`
- **Workflows:** `@docs/v5.1/WORKFLOWS.md`
- **Curator Guide:** `@for-claude-code/README.md`

---

**Version:** 5.1.7
**Last Updated:** 2026-01-10
