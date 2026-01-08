# How to Give Instructions to Agents

**Problem:** Agent in another project doesn't know about Shared KB and doesn't have access to local files.

**Solution:** Use one of these methods:

---

## Method 1: Copy-Paste Prompt (Quickest)

**When to use:** Agent needs quick setup, you know what they need

**Steps:**
1. Copy content from `AGENT-PROMPT.md` (above)
2. Paste to agent
3. Agent has all commands and rules

**Example:**
```
You said: "I need to set up Shared KB"

I paste:
[Copy from AGENT-PROMPT.md]

Agent: Reads and executes commands → Done!
```

**Time:** 30 seconds to copy, 3-5 minutes for agent to execute

---

## Method 2: GitHub URL (Best for Documentation)

**When to use:** Agent needs to understand Shared KB, read full docs

**URL to give:**
```
https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md
```

**Agent can:**
- Read the file via WebFetch tool
- Access all linked documentation
- Get full context

**Example prompt to agent:**
```
"Your project uses Shared Knowledge Base. Read this:
https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md

Then follow Step 1 (New Project) or Step 2 (Update Project) depending on your situation."
```

**Time:** 1 minute to explain, 5-10 minutes for agent to read + execute

---

## Method 3: Local Path (If Agent Has Access)

**When to use:** Agent is working in project that already has `.kb/shared/` submodule

**Agent can read:**
```
.kb/shared/for-projects/START-HERE.md
```

**Check if agent has access:**
```bash
# Ask agent to check
ls .kb/shared/for-projects/
```

**If files exist:**
```
"Read .kb/shared/for-projects/START-HERE.md and follow the steps"
```

**Time:** 30 seconds to explain, 3-5 minutes to execute

---

## Method 4: Zero-Context Prompt (Agent Knows Nothing)

**When to use:** Agent has no idea what Shared KB is

**Prompt to agent:**
```
"Your project uses Shared Knowledge Base - a centralized error/solution database.

Here's what to do:

1. Add it as submodule:
   git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared

2. Copy tools:
   cp .kb/shared/tools/kb.py tools/
   cp .kb/shared/tools/kb_domains.py tools/

3. Build index:
   python tools/kb.py index -v

Critical rules:
- NEVER modify files in .kb/shared/
- If tool breaks, tool has bug (not data)
- Read docs: https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md

That's it! Let me know if you need help."
```

**Time:** 1 minute to write, 5 minutes for agent to execute

---

## Comparison

| Method | Best For | Time | Agent Understanding |
|--------|----------|------|---------------------|
| **1. Copy-Paste** | Quick setup, known scenario | 30s | Minimal (just commands) |
| **2. GitHub URL** | Full context, documentation | 1min | Complete (reads docs) |
| **3. Local Path** | Agent has .kb/shared/ | 30s | Good (local access) |
| **4. Zero-Context** | Agent knows nothing | 1min | Basic (needs follow-up) |

---

## Real-World Examples

### Example 1: Fresh Project, Agent Knows Nothing

**You:**
```
"Set up Shared KB for this project. Read:
https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md

Follow Step 1: New Project Setup"
```

**Agent:**
1. WebFetch the URL
2. Reads instructions
3. Executes commands
4. Asks questions if needed

---

### Example 2: Update Existing Project

**You:**
```
"Update Shared KB to latest version. Read:
https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md

Follow Step 2: Update Existing Project"
```

**Agent:**
1. Reads Step 2
2. Checks current version
3. Updates submodule
4. Rebuilds index

---

### Example 3: Quick Setup (No GitHub Access)

**You:**
```
[paste AGENT-PROMPT.md content]

Follow option A) New Project Setup"
```

**Agent:**
1. Has all commands in paste
2. Executes directly
3. Done in 3 minutes

---

### Example 4: Agent Has .kb/shared/ Already

**You:**
```
"Update Shared KB. Check:
.kb/shared/for-projects/START-HERE.md

Follow Step 2"
```

**Agent:**
1. Reads local file
2. Executes update commands
3. Done

---

## Key URLs for Agents

**Main Entry Point:**
- https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md

**Agent Instructions:**
- https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/AGENT-INSTRUCTIONS.md

**Update Guide:**
- https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/UPDATE-SHARED-KB.md

**Repository:**
- https://github.com/ozand/shared-knowledge-base

---

## Pro Tips

1. **Always mention the URL** - Agent can fetch it with WebFetch
2. **Specify which Step** - "Follow Step 1" or "Follow Step 2"
3. **Include critical rules** - "NEVER modify .kb/shared/"
4. **Offer help** - "Let me know if you need help"

---

## Template Library

**Quick Setup (30s):**
```markdown
"Set up Shared KB:
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared
cp .kb/shared/tools/kb.py tools/
cp .kb/shared/tools/kb_domains.py tools/
python tools/kb.py index -v

Docs: https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md
NEVER modify .kb/shared/"
```

**Update (30s):**
```markdown
"Update Shared KB:
cd .kb/shared && git pull origin main && cd ../..
python tools/kb.py index -v
Docs: https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md
```

**Full Context (1min):**
```markdown
"Your project uses Shared KB. Read this:
https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md

Follow Step 1 (new) or Step 2 (update). NEVER modify .kb/shared/ files.
"
```

---

**Last Updated:** 2026-01-08
**Shared KB Version:** 4.0.1
