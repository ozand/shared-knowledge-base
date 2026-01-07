# 🎯 Quick Reference: Giving Instructions to Agents

## 🚀 The ONE Thing You Need to Know

**Give agent this URL:**
```
https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md
```

Agent will use WebFetch to read it and get all instructions.

---

## 📝 Example Prompts to Agents

### Scenario 1: New Project (Agent Knows Nothing)

```
"Your project uses Shared Knowledge Base. Read this:
https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md

Follow Step 1: New Project Setup. Let me know if you need help."
```

---

### Scenario 2: Update Existing Project

```
"Update Shared KB to latest version. Read:
https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md

Follow Step 2: Update Existing Project."
```

---

### Scenario 3: Quick Commands (No Documentation Reading)

```
"Set up Shared KB:

git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared
cp .kb/shared/tools/kb.py tools/
cp .kb/shared/tools/kb_domains.py tools/
python tools/kb.py index --force -v

Critical rule: NEVER modify files in .kb/shared/"
```

---

## 🔗 Key URLs

| Purpose | URL |
|---------|-----|
| **Main Start Guide** | https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md |
| **Agent Instructions** | https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/AGENT-INSTRUCTIONS.md |
| **Update Guide** | https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/UPDATE-SHARED-KB.md |
| **How to Give Instructions** | https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/HOW-TO-GIVE-INSTRUCTIONS.md |

---

## ⚡ Quick Copy-Paste Templates

### For New Project
```markdown
"Set up Shared KB. Read:
https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md

Follow Step 1. NEVER modify .kb/shared/ files."
```

### For Update
```markdown
"Update Shared KB. Read:
https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md

Follow Step 2."
```

### Zero Context (Everything Included)
```markdown
"Your project uses Shared KB - centralized error/solution database.

Setup:
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared
cp .kb/shared/tools/kb.py tools/
cp .kb/shared/tools/kb_domains.py tools/
python tools/kb.py index --force -v

Critical: NEVER modify .kb/shared/ files. Read more:
https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md"
```

---

## 🎓 How It Works

### Agent's Perspective:

1. **Receives GitHub URL** from you
2. **Uses WebFetch tool** to read the file
3. **Sees two paths:**
   - Step 1: New Project Setup
   - Step 2: Update Existing Project
4. **Follows the commands** for their path
5. **Has links** to more documentation if needed

### Your Perspective:

- **Give ONE URL** - agent gets everything
- **Specify which Step** - "Follow Step 1" or "Follow Step 2"
- **Mention critical rule** - "NEVER modify .kb/shared/"
- **Offer help** - "Let me know if you need help"

---

## 📚 File Structure (For Reference)

```
for-projects/
├── START-HERE.md                   ⭐ MAIN FILE - give this URL
├── AGENT-INSTRUCTIONS.md           📖 Complete guide
├── UPDATE-SHARED-KB.md             📝 Update details
├── HOW-TO-GIVE-INSTRUCTIONS.md     🎓 This file
├── AGENT-PROMPT.md                 📋 Copy-paste templates
└── VERSION-NOTIFICATION.md         🔔 Version updates
```

---

## ✅ Checklist

Before giving instructions to agent:

- [ ] Decide: New project or Update?
- [ ] Copy the URL: https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/START-HERE.md
- [ ] Add prompt: "Follow Step 1" or "Follow Step 2"
- [ ] Add critical rule: "NEVER modify .kb/shared/"
- [ ] Offer help: "Let me know if you need help"

---

## 🆘 If Agent Gets Stuck

**Common issues:**

1. **"I don't have access to the file"**
   → Agent should use WebFetch tool with the GitHub URL

2. **"Should I modify .kb/shared/?"**
   → NO! NEVER modify .kb/shared/ files

3. **"Tool shows TypeError"**
   → Copy tools from .kb/shared/: `cp .kb/shared/tools/kb_domains.py tools/`

4. **"Where do I get more info?"**
   → Point to: https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/for-projects/AGENT-INSTRUCTIONS.md

---

**That's it!** One URL, clear instructions, agent is set up in 3-5 minutes.

**Version:** 4.0.1
**Last Updated:** 2026-01-08
