# Shared Knowledge Base - Project Memory

_Last updated: 2026-01-08_

---

## Architecture Decisions

### Two-Tier Architecture (2026-01-08)
**Decision:** Separate Project KB (private) and Shared KB (public) with GitHub Issues workflow
**Reason:**
- Prevents agents from directly modifying Shared KB
- Enables quality control via curation
- Clear separation of project-specific vs universal knowledge
**Impact:** Positive - Safer contribution model, better quality control
**Implementation:** v5.1 tools in `tools/v5.1/`
**KB Entry:** `docs/v5.1/ARD.md`

### PyGithub vs gh CLI (2026-01-08)
**Decision:** Use PyGithub library instead of gh CLI for submissions
**Reason:**
- Easier Python integration
- No external binary dependency
- Better error handling
**Impact:** Positive - Simpler installation, more reliable
**Implementation:** `tools/v5.1/kb_submit.py`

### SessionStart Hook (2026-01-08)
**Decision:** Automatic context loading via session-start.sh
**Reason:**
- Agents need project context before making decisions
- Manual loading is error-prone
- Submodule updates need to happen automatically
**Impact:** Positive - Seamless agent experience
**Implementation:** `.claude/hooks/session-start.sh`

---

## Lessons Learned

### Architecture
- **Two-tier model works well** - Clear separation prevents confusion
- **Issues workflow is safer** than direct commits for multi-agent systems
- **Decision criteria must be explicit** - Agents can't guess what to share
- **Context loading is critical** - Without it, agents make poor decisions

### Development
- **Backward compatibility is essential** - v4.0 users need time to migrate
- **Documentation is as important as code** - Without guides, users won't migrate
- **Migration automation reduces friction** - Scripts work better than manual steps
- **Quality scoring prevents low-quality submissions** - 75/100 threshold works well

### Tool Design
- **PyGithub integration is cleaner** than gh CLI subprocess calls
- **Validation should happen early** - Before creating GitHub Issues
- **Error messages must be actionable** - Tell users exactly what to fix
- **Progress feedback is important** - Users need to know what's happening

### Security
- **GITHUB_TOKEN in .env** - Never commit tokens
- **Project KB for secrets** - Use templates, not actual values
- **Shared KB must remain generic** - No project-specific data
- **Curator role is essential** - Final gatekeeper for quality

---

## Known Issues

### Current Issues
- **v5.1 tools need real-world testing** (2026-01-08)
  - **Status:** Monitoring
  - **Workaround:** Use v4.0 tools as fallback
  - **Related:** Need more user feedback

- **Documentation needs translation** (2026-01-08)
  - **Status:** Planned
  - **Workaround:** Use auto-translation tools
  - **Priority:** Medium

### Resolved Issues
- **gh CLI dependency** (2025-12-15)
  - **Status:** ✅ Resolved in v5.1
  - **Solution:** Replaced with PyGithub library

- **Direct commits to Shared KB** (2025-12-10)
  - **Status:** ✅ Resolved in v5.1
  - **Solution:** GitHub Issues workflow with curator

- **Manual context loading** (2025-12-05)
  - **Status:** ✅ Resolved in v5.1
  - **Solution:** SessionStart hook

---

## Development Workflow

### Repository Structure
```
shared-knowledge-base/
├── [domains]/          # python/, docker/, postgresql/, etc.
├── docs/               # All documentation
│   ├── v5.1/          # New v5.1 docs
│   └── [v4.0 docs]    # Legacy docs
├── tools/              # All tools
│   ├── v5.1/          # New v5.1 tools
│   └── [v4.0 tools]   # Legacy tools
├── examples/           # Templates and examples
│   ├── v5.1/          # New v5.1 examples
│   └── [legacy]       # Old examples
├── for-claude-code/    # Claude Code integration
├── for-projects/       # Project templates
└── curator/            # Curator instructions
```

### Version Management
- **v4.0:** Single-tier architecture, direct submissions
- **v5.1:** Two-tier architecture, Issues workflow
- **Backward compatible:** v4.0 tools still work

### Release Process
1. Update version numbers in docs
2. Add CHANGELOG.md entry
3. Update README.md
4. Tag release: `git tag v5.1.0`
5. Push: `git push origin v5.1.0`

---

## Onboarding Tips

### For New Maintainers
1. **Read architecture first:** `docs/v5.1/ARD.md`
2. **Understand workflows:** `docs/v5.1/WORKFLOWS.md`
3. **Review issues regularly:** Check for kb-submission label
4. **Test new tools:** Use them yourself before recommending
5. **Keep v4.0 working:** Don't break backward compatibility

### For Contributors
1. **Search before submitting:** Use kb_search.py
2. **Check quality score:** Ensure >= 75/100
3. **Use examples:** See `examples/v5.1/` for templates
4. **Test your solutions:** Verify code works
5. **Be patient:** Curator review takes time

### For New Users
1. **Start with README:** `docs/v5.1/README.md`
2. **Use migration script:** `tools/v5.1/migrate-to-v5.1.sh`
3. **Configure PROJECT.yaml:** Set sharing_criteria
4. **Install hook:** `.claude/hooks/session-start.sh`
5. **Test locally:** Use `--target local` first

---

## Project Conventions

### Code Style
- **Python:** PEP 8, type hints where useful
- **Bash:** POSIX-compliant, error handling with set -e
- **YAML:** 2-space indentation, comments for complex logic

### File Organization
- **Documentation:** docs/v5.1/
- **Tools:** tools/v5.1/
- **Examples:** examples/v5.1/
- **Domains:** python/, docker/, postgresql/, etc.

### Naming Conventions
- **KB entries:** kebab-case.yaml (DC-HEALTH-001.yaml)
- **Tools:** kb_<action>.py (kb_search.py)
- **Hooks:** <event>-<target>.sh (session-start.sh)
- **Documentation:** TITLE-case.md (MIGRATION-GUIDE.md)

### Git Conventions
- **Commits:** Conventional Commits (feat:, fix:, docs:)
- **Branches:** feature/, fix/, hotfix/
- **Tags:** v<major>.<minor>.<patch>

---

## Integration References

### Quick Links
- **v5.1 Architecture:** docs/v5.1/ARD.md
- **Migration Guide:** docs/v5.1/MIGRATION-GUIDE.md
- **Tool Reference:** docs/v5.1/WORKFLOWS.md
- **Schema Reference:** docs/v5.1/CONTEXT_SCHEMA.md

### External Docs
- **Claude Code:** https://claude.com/claude-code
- **PyGithub:** https://pygithub.readthedocs.io/
- **PyYAML:** https://pyyaml.org/wiki/PyYAMLDocumentation

---

## Environment Variables

### Required
```bash
# For v5.1 submissions to Shared KB
GITHUB_TOKEN=ghp_your_token_here

# Repository (optional, has default)
SHARED_KB_REPO=ozand/shared-knowledge-base
```

### Optional
```bash
# Session tracking
CLAUDE_SESSION_ID=auto-detected

# Debug mode
DEBUG=1
```

---

## Glossary

- **Shared KB:** Universal knowledge repository (this repo)
- **Project KB:** Private knowledge in user's project (.kb/project/)
- **Curator:** Role that reviews GitHub Issues and commits to Shared KB
- **Agent:** Claude Code AI assistant
- **Submission:** GitHub Issue proposing Shared KB entry
- **Sharing Criteria:** Rules in PROJECT.yaml that guide agent decisions
- **Two-Tier:** Architecture separating Project KB and Shared KB
- **SessionStart Hook:** Script that runs when Claude Code session starts

---

## Milestones

### v5.1 Release (2026-01-08)
- ✅ Two-tier architecture implemented
- ✅ GitHub Issues workflow working
- ✅ PyGithub integration complete
- ✅ Automatic context loading functional
- ✅ Complete documentation suite
- ✅ Migration script tested
- ⏭️ User feedback gathering
- ⏭️ Real-world testing

### Future Plans
- **v5.2:** Enhanced quality scoring
- **v5.3:** Automated duplicate detection
- **v5.4:** Multi-language support
- **v6.0:** Web UI for curation

---

_Last updated by: Claude Code Agent (Sonnet 4.5)_
_Update frequency: After major architectural decisions_
_Maintainer: Ozand_
