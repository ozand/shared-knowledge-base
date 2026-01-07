# Shared Knowledge Base Documentation

**Version:** 3.1+ | **Last Updated:** 2026-01-07

---

## Quick Links

### Getting Started 🚀
- [Quick Start](../QUICKSTART.md) - 5-minute setup guide
- [Progressive Domain Loading](../QUICKSTART-DOMAINS.md) - Load only domains you need (v3.1)
- [Complete User Guide](../GUIDE.md) - Full documentation

### For Claude Code Users 🤖
- [Claude Code Integration](../for-claude-code/README.md) - Complete guide
- [Agent Quick Start](../for-claude-code/AGENT-QUICK-START.md) - AI agent setup

### Reference Documentation 📚
- [YAML Schema v3.1](YAML-SCHEMA-V3.1.md) - Entry structure and metadata
- [Domain Management](../QUICKSTART-DOMAINS.md) - Progressive loading guide

---

## Implementation Documentation (v3.1)

### Phase 1: Progressive Domain Loading
- **[Implementation Summary](implementation/IMPLEMENTATION-SUMMARY.md)** - All phases overview
- **Key Achievement:** 83.1% token reduction for single-domain projects
- **Domain Index:** Optimized to ~80 tokens (99.1% reduction)

### Phase 2: GitHub-Native Contribution
- **[Implementation Summary](implementation/IMPLEMENTATION-SUMMARY.md)** - Phase 2 details
- **Key Achievement:** Zero-infrastructure contribution system
- **Tools:** `kb-submit.py` for issue-based submissions

### Phase 3: Automated Feedback Loop
- **[Phase 3 Completion Report](implementation/PHASE3-COMPLETION-REPORT.md)** - Complete feedback loop
- **Key Achievement:** 100% test coverage (10/10 tests)
- **Features:** Curator slash commands, auto-update workflows

### Repository Structure
- **[Structure Analysis](implementation/STRUCTURE-ANALYSIS.md)** - Complete structure review
- **Optimization:** Index reduced from 8,829 to ~80 tokens

---

## Integration Guides

### Submodule vs Clone
- **[Submodule vs Clone Comparison](guides/integration/SUBMODULE_VS_CLONE.md)** - Choose your integration method
- **Recommendation:** Submodule for progressive loading

### Agent Configuration
- **[Agent Auto-Config Guide](guides/integration/AGENT_AUTOCONFIG_GUIDE.md)** - Automatic setup
- **Role-Based Access:** [Project Agent vs Curator](guides/workflows/ROLE_SEPARATION_GUIDE.md)

---

## Workflow Documentation

### Contribution Workflow
- **[GitHub Attribution Guide](guides/workflows/GITHUB_ATTRIBUTION_GUIDE.md)** - Submitting entries
- **Curator Workflows:** Review and approve contributions

### Role Separation
- **[Role Separation Guide](guides/workflows/ROLE_SEPARATION_GUIDE.md)** - Agent responsibilities
- **Project Agent:** Submit via GitHub Issues
- **Curator Agent:** Review and commit to shared KB

---

## Research & Analysis

### Research Papers
- **[Research Directory](research/)** - Architecture analysis and best practices
- **Claude Code Research:** [research/claude-code/](research/claude-code/)

### Implementation Reports
- Phase 1: Progressive Loading (see Implementation Summary)
- Phase 2: GitHub-Native Contribution (see Implementation Summary)
- Phase 3: Automated Feedback Loop (see Phase 3 Report)

---

## Tools & Utilities

### Domain Management (v3.1)
```bash
# List all domains
python ../tools/kb_domains.py list

# Load specific domain
python ../tools/kb_domains.py load docker

# Get domain info
python ../tools/kb_domains.py info postgresql
```

### Submission Tool (v3.1)
```bash
# Submit entry to Shared KB
python ../tools/kb_submit.py submit --entry path/to/entry.yaml

# Dry run
python ../tools/kb_submit.py submit --entry path/to/entry.yaml --dry-run
```

### Testing
```bash
# Test progressive loading
python ../tools/test_progressive_loading.py

# Test feedback loop
python ../tools/test_feedback_loop.py
```

---

## File Structure

### Root Files (for quick access)
- `README.md` - Project overview
- `QUICKSTART.md` - 5-minute setup
- `QUICKSTART-DOMAINS.md` - Progressive loading
- `_index.yaml` - Main search index
- `_domain_index.yaml` - Domain metadata (optimized, ~80 tokens)

### Documentation (this directory)
- `YAML-SCHEMA-V3.1.md` - Entry schema reference
- `implementation/` - Implementation reports
- `guides/` - Integration and workflow guides
- `research/` - Research and analysis

### Curator Resources
- `curator/` - Curator documentation and workflows
- `.github/workflows/` - Shared KB automation

### Project Resources
- `for-claude-code/` - Claude Code integration
- `for-projects/` - Project workflows and templates

---

## Domain Structure

### Knowledge Domains (Git Sparse Checkout)
```
shared-knowledge-base/
├── docker/          # Docker & containers
├── javascript/      # JavaScript & Node.js
├── postgresql/      # PostgreSQL database
├── python/          # Python language
├── universal/       # Cross-language patterns
└── framework/       # Framework-specific
```

### Progressive Loading
```bash
# Load only specific domains
git sparse-checkout set docker postgresql universal tools _domain_index.yaml

# Result: ~80 tokens for index + selected domains only
# Savings: Up to 83% compared to full KB
```

---

## Key Metrics

### Token Efficiency
- **Full KB:** ~9,750 tokens
- **Domain Index:** ~80 tokens (optimized from 8,829)
- **Single Domain:** ~1,650 tokens
- **Savings:** 83.1% for single-domain projects

### Coverage
- **Total Entries:** 149
- **With Domain Metadata:** 65 (43.6%)
- **Domains:** 12 classified

### Test Coverage
- **Progressive Loading:** 5/6 tests passed
- **Feedback Loop:** 10/10 tests passed (100%)

---

## Version Information

**Current Version:** 3.1
**Release Date:** 2026-01-07
**Status:** Production Ready ✅

### Features by Version
- **v3.1:** Progressive loading, GitHub-native contribution, automated feedback loop
- **v3.0:** Metadata system, usage tracking, predictive analytics
- **v2.0:** SQLite search, FTS5 indexing
- **v1.0:** Initial YAML-based knowledge base

---

## Support & Contribution

### Getting Help
- **Quick Issues:** Check [GUIDE.md](../GUIDE.md)
- **Integration:** See [Integration Guides](#integration-guides)
- **Curator Support:** See [curator/](../curator/)

### Contributing
1. **Project Agents:** Submit via GitHub Issues (use `kb-submit.py`)
2. **Curators:** Review and approve via slash commands
3. **Documentation:** Update docs in this directory

### Contribution Workflow
1. Create entry locally
2. Submit via `python tools/kb_submit.py submit`
3. Curator reviews and uses `/approve` or `/request-changes`
4. Auto-update to project repositories on approval

---

**Navigation:**
- [Back to Root](../README.md)
- [Claude Code Guide](../for-claude-code/README.md)
- [Implementation Reports](implementation/)
