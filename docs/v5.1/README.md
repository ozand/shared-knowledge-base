# Shared Knowledge Base v5.1

**Two-Tier Knowledge Management System for AI Agents**

**Version:** 5.1.0
**Status:** ✅ Production Ready
**Release Date:** 2026-01-08

---

## 🌟 What's New in v5.1

### Major Changes from v4.0

- ✅ **Two-Tier Architecture**: Separate Project KB (local) and Shared KB (global)
- ✅ **GitHub Issues Workflow**: Agents submit via Issues, Curator reviews and approves
- ✅ **PyGithub Integration**: No more dependency on `gh` CLI
- ✅ **Automatic Context Loading**: SessionStart hook injects project context
- ✅ **Decision Criteria**: `sharing_criteria` in PROJECT.yaml guides agent decisions
- ✅ **Feedback Loop**: Agents learn from mistakes and accumulate knowledge
- ✅ **Cascading Search**: Project → Shared → Web priority protocol

### Key Benefits

| Feature | v4.0 | v5.1 |
|---------|------|------|
| **Submission Safety** | Direct commits (risky) | Issues workflow (safe) |
| **Project Context** | Manual loading | Automatic via hook |
| **Decision Making** | Agent guesses | Explicit criteria |
| **Integration** | gh CLI required | PyGithub library |
| **Quality Control** | Basic validation | Quality score + curation |

---

## 📋 Documentation

| Document | Description |
|----------|-------------|
| **[ARD.md](ARD.md)** | Architecture Reference Document - Complete system architecture |
| **[WORKFLOWS.md](WORKFLOWS.md)** | Agent workflows and curation protocols |
| **[CONTEXT_SCHEMA.md](CONTEXT_SCHEMA.md)** | PROJECT.yaml and MEMORY.md schemas |
| **[SHARED-KB-WORKFLOWS.md](SHARED-KB-WORKFLOWS.md)** | Shared KB lifecycle: Read → Submit → Curate → Sync |
| **[FEEDBACK-LOOP.md](FEEDBACK-LOOP.md)** | Agent learning process and knowledge extraction |
| **[INFORMATION-RETRIEVAL.md](INFORMATION-RETRIEVAL.md)** | Cascading search protocol: Project → Shared → Web |
| **[examples/feedback-loop-scenarios.md](examples/feedback-loop-scenarios.md)** | Real-world Feedback Loop examples |
| **[examples/information-retrieval-examples.md](examples/information-retrieval-examples.md)** | Cascading search examples and conflict resolution |

---

## 🚀 Quick Start

### For New Projects (Automated)

```bash
# Run the initialization script (if Shared KB is already a submodule)
bash .kb/shared/tools/init-kb.sh

# Or if adding Shared KB for the first time:
git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared
bash .kb/shared/tools/init-kb.sh

# Edit .kb/context/PROJECT.yaml with your project details
# Create .env file with GITHUB_TOKEN
# Commit to git
```

### For New Projects (Manual)

```bash
# 1. Create project structure
mkdir -p .kb/{context,project/{knowledge,integrations,endpoints,decisions,lessons,pending}}

# 2. Clone examples
cp .kb/shared/examples/v5.1/PROJECT.yaml.example .kb/context/PROJECT.yaml
cp .kb/shared/examples/v5.1/MEMORY.md.example .kb/context/MEMORY.md

# 3. Edit PROJECT.yaml
# Set your project name, ID, and sharing_criteria

# 4. Install session-start hook
cp .kb/shared/tools/hooks/session-start.sh .claude/hooks/
chmod +x .claude/hooks/session-start.sh

# 5. Configure environment
cp .kb/shared/examples/v5.1/.env.example .env
# Edit .env and add your GITHUB_TOKEN

# 6. Done! Next agent session will auto-load context
```

### For Existing Projects (Upgrade from v4.0)

```bash
# 1. Pull latest Shared KB
cd .kb/shared
git pull origin main
cd ../..

# 2. Run initialization script
bash .kb/shared/tools/init-kb.sh

# 3. Edit .kb/context/PROJECT.yaml
# Add your project-specific sharing_criteria

# 4. Create .env file
cp .kb/shared/examples/v5.1/.env.example .env
# Edit and add GITHUB_TOKEN

# 5. Commit to git
git add .kb/ .claude/hooks/ .env.example
git commit -m "feat: Upgrade to v5.1 two-tier KB architecture"

# 6. Upgrade complete!
# v4.0 tools still work, v5.1 tools available for new workflows
```

---

## 🛠️ Tools

### kb_submit.py

Submit knowledge entries to Project KB or Shared KB.

```bash
# Save to local Project KB (direct commit)
python .kb/shared/tools/kb_submit.py \
    --target local \
    --file solution.yaml

# Submit to Shared KB via GitHub Issue
python .kb/shared/tools/kb_submit.py \
    --target shared \
    --file solution.yaml \
    --title "Docker compose healthcheck fix" \
    --desc "Container becomes healthy before DB is ready" \
    --domain docker
```

### kb_search.py

Search knowledge entries across Project and Shared KB.

```bash
# Search all KBs
python .kb/shared/tools/kb_search.py "docker compose"

# Search only Shared KB
python .kb/shared/tools/kb_search.py "fastapi cors" --scope shared

# Search only Project KB
python .kb/shared/tools/kb_search.py "stripe webhook" --scope project

# Show statistics
python .kb/shared/tools/kb_search.py --stats
```

### kb_curate.py

Curator tool for processing GitHub Issue submissions.

```bash
# List pending submissions
python .kb/shared/tools/kb_curate.py --mode list

# Validate specific submission
python .kb/shared/tools/kb_curate.py --mode validate --issue 123

# Approve submission
python .kb/shared/tools/kb_curate.py --mode approve --issue 123

# Reject submission
python .kb/shared/tools/kb_curate.py \
    --mode reject \
    --issue 123 \
    --reason "Duplicate of existing entry"
```

---

## 📁 Project Structure

```
my-project/
├── .env                      # GitHub token (gitignored)
├── .claude/
│   ├── hooks/
│   │   └── session-start.sh  # Auto-loads context on session start
│   └── agents/               # Agent configurations
├── .kb/
│   ├── context/              # 📋 Project Passport
│   │   ├── PROJECT.yaml      # Structured config + sharing criteria
│   │   └── MEMORY.md         # Free-form knowledge
│   ├── project/              # 📁 Local KB (private)
│   │   ├── integrations/     # Integration docs
│   │   ├── endpoints/        # API endpoints
│   │   ├── decisions/        # Architectural decisions
│   │   ├── lessons/          # Learned lessons
│   │   └── pending/          # Pending submissions
│   └── shared/               # 🌍 Shared KB (submodule)
│       ├── domains/          # docker, python, postgresql, etc.
│       └── tools/
│           └── v5.1/         # v5.1 tools
│               ├── kb_submit.py
│               ├── kb_search.py
│               ├── kb_curate.py
│               └── hooks/
│                   └── session-start.sh
└── src/                      # Your project code
```

---

## 🔄 Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Workflow                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Session Start                                          │
│     └─► session-start.sh loads PROJECT.yaml + MEMORY.md    │
│                                                             │
│  2. Agent Solves Problem                                   │
│     └─► Searches KB first: kb_search.py "query"            │
│                                                             │
│  3. Agent Checks sharing_criteria in PROJECT.yaml          │
│     │                                                       │
│     ├──► Project-specific? → kb_submit.py --target local   │
│     │                         └─► Direct commit           │
│     │                                                       │
│     └──► Universal? → kb_submit.py --target shared         │
│                         └─► GitHub Issue                  │
│                                                             │
│  4. Curator Review (for shared submissions)               │
│     └─► kb_curate.py --mode validate --issue 123           │
│         ├──► Approve → Commit to Shared KB                 │
│         └──► Reject → Close with feedback                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Requirements

### System Requirements
- Python 3.11+
- Git
- GitHub account (for Shared KB submissions)

### Python Dependencies
```bash
# Required for v5.1 tools
pip install PyGithub pyyaml
```

### Environment Variables
```bash
# Required for shared submissions
GITHUB_TOKEN=ghp_your_token_here
SHARED_KB_REPO=ozand/shared-knowledge-base

# Optional
CLAUDE_SESSION_ID=auto-detected
```

---

## 📚 Examples

See the `examples/v5.1/` directory for templates:

- **`.env.example`** - Environment variables template
- **`PROJECT.yaml.example`** - Complete project configuration
- **`MEMORY.md.example`** - Project memory template
- **`kb-entry-example.yaml`** - Proper KB entry format

---

## 🤝 Contributing

### For Agents

1. **Search First**: Always check if solution already exists
2. **Check Criteria**: Use `sharing_criteria` to decide local vs shared
3. **Verify Solutions**: Test before submitting
4. **Provide Context**: Include error messages, stack traces, environment

### For Curators

1. **Validate Submissions**: Use `kb_curate.py --mode validate`
2. **Check Quality**: Ensure score >= 75
3. **Find Duplicates**: Search KB before approving
4. **Provide Feedback**: Be constructive when requesting changes

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `kb_submit.py` fails "No GITHUB_TOKEN" | Add `GITHUB_TOKEN=xxx` to `.env` |
| Submodule not updating | Run `git submodule update --remote --merge` |
| Issue created but not showing | Check `SHARED_KB_REPO` environment variable |
| Quality score too low | Add missing fields to YAML entry |
| Duplicate entries | Use `kb_search.py` before submitting |
| Context not loading | Check `.claude/hooks/session-start.sh` exists |
| PyGithub import error | Run `pip install PyGithub` |

---

## 📖 Further Reading

- **Architecture**: See [ARD.md](ARD.md) for complete architecture
- **Workflows**: See [WORKFLOWS.md](WORKFLOWS.md) for detailed protocols
- **Schemas**: See [CONTEXT_SCHEMA.md](CONTEXT_SCHEMA.md) for YAML schemas
- **v4.0 Docs**: See parent directory for v4.0 documentation (still compatible)

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| **5.1.0** | 2026-01-08 | Two-tier architecture, Issues workflow, PyGithub |
| **4.0.1** | 2026-01-07 | Bug fixes, performance improvements |
| **4.0.0** | 2026-01-05 | Quality scoring, metadata system |

---

**Status**: ✅ Production Ready
**Maintainer**: Knowledge Base Curator
**License**: MIT

---

## 🎯 Next Steps

1. **Read the Architecture**: [ARD.md](ARD.md)
2. **Set Up Your Project**: Follow Quick Start above
3. **Customize Criteria**: Edit `sharing_criteria` in PROJECT.yaml
4. **Train Your Team**: Share WORKFLOWS.md with developers
5. **Start Curating**: Set up regular curation schedule

**Welcome to v5.1! 🚀**
