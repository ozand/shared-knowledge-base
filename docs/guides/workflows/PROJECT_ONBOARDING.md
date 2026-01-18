# Project Onboarding Guide for Agents

Use this prompt to onboard any project into the Company OS ecosystem.

## The Activation Prompt

Paste this into your agent's chat window (Claude Code, Cursor, etc.):

```markdown
@sys_instruction
# Project Activation Protocol

You are tasked with integrating this project into the **Company OS** ecosystem.
Follow these steps autonomously:

**Step 1: Install Knowledge Base (v5.1)**
Check if `.kb/shared` exists.
- If NO: Run `curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/unified-install.py | python3 - --full`
- If YES: Run `python3 .kb/shared/scripts/unified-install.py --full` to update structure.

**Step 2: Profile Initialization**
Run `python3 .kb/shared/tools/kb.py profile init` to auto-detect the tech stack and activate relevant knowledge domains (e.g., Python, React, Docker).

**Step 3: Capability Harvesting**
Scan the project for existing scripts, prompts, or tools (check `.claude/`, `scripts/`, `.github/`).
- If you find reusable tools, ARCHIVE them to the Project KB:
  `python3 .kb/shared/tools/kb.py archive <file> --type <skills|agents|hooks> --scope project`

**Step 4: Company OS Registration**
Initialize the project passport and sync with the registry:
1. Run `python3 .kb/shared/tools/kb.py sync init-passport`
2. Review/Edit the generated `.kb/project/PROJECT.yaml`
3. Run `python3 .kb/shared/tools/kb.py sync push` (if auth available) OR present the passport content to the user for manual registration.

**Step 5: Context Archiving**
If there is existing documentation or context files, run `/context-condense` (or `python .kb/shared/tools/kb.py archive-context`) to index them.

Report completion when all steps are done.
```

## What Happens Next?

1.  **Shared KB** is installed/updated.
2.  **Profile** is set (e.g., "Active domains: Python, AWS").
3.  **Local Tools** are preserved in `.kb/project`.
4.  **Project** is registered in Company OS (visibility).
