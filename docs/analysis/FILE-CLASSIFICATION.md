# File Classification Analysis for Claude Code Migration

**Date:** 2026-01-08
**Purpose:** Identify what to move, what to keep, what's critical

---

## Classification Categories

### 1. KEEP in `.claude/` (Shared KB Project Technical Files)

These files are SPECIFIC to the Shared KB repository itself and should NOT be moved:

```
.claude/
├── CLAUDE.md                              ✅ KEEP - Project instructions for Shared KB
├── IMPROVEMENTS-COMPLETE.md               ✅ KEEP - Project status
├── IMPLEMENTATION-COMPLETE.md             ✅ KEEP - Project status
├── CLAUDE-CODE-EXPERNT-PLAN.md            ✅ KEEP - Project planning
├── CLAUDE-CODE-EXPERT-IMPLEMENTATION-COMPLETE.md ✅ KEEP - Project status
└── skills/                                ✅ KEEP - Shared KB technical skills
    ├── audit-quality/SKILL.md             - Quality audit for KB entries
    ├── find-duplicates/SKILL.md           - Duplicate detection
    ├── hook-implementation/SKILL.md       - Hook implementation guide
    ├── claude-code-architecture/SKILL.md  - Claude Code architecture
    ├── kb-create/SKILL.md                 - KB entry creation
    ├── kb-index/SKILL.md                  - KB indexing
    ├── kb-search/SKILL.md                 - KB search
    ├── kb-validate/SKILL.md               - KB validation
    └── research-enhance/SKILL.md          - Research enhancement
```

**Reason:** These are implementation tools FOR the Shared KB project itself.

---

### 2. MOVE to `claude-code/agents/` (Knowledge Base Content)

These are KNOWLEDGE about how to create agents, used in OTHER projects:

```
.claude/agents/  →  claude-code/agent-instructions/
├── claude-code-expert.md                  🔄 MOVE - Agent definition template
├── kb-curator.md                          🔄 MOVE - Curator agent template
└── subagents/
    ├── DEBUGGER.md                        🔄 MOVE - Subagent template
    ├── KNOWLEDGE-CURATOR.md               🔄 MOVE - Subagent template
    ├── RESEARCHER.md                      🔄 MOVE - Subagent template
    ├── VALIDATOR.md                       🔄 MOVE - Subagent template
    └── README.md                          🔄 MOVE - Subagent documentation
```

**Reason:** These are knowledge base entries about agent design, not specific to Shared KB.

**Format:** Convert `.md` to `.yaml` following KB entry schema.

---

### 3. MOVE to `claude-code/commands/` (Reference Documentation)

These are reference docs for KB commands used in OTHER projects:

```
.claude/commands/  →  claude-code/commands/
├── kb-search.md                          🔄 MOVE - Search command reference
├── kb-create.md                          🔄 MOVE - Create command reference
├── kb-index.md                           🔄 MOVE - Index command reference
├── kb-query.md                           🔄 MOVE - Query command reference
├── kb-sync.md                            🔄 MOVE - Sync command reference
├── kb-validate.md                        🔄 MOVE - Validate command reference
├── add-hook.md                           🔄 MOVE - Hook creation reference
├── create-skill.md                       🔄 MOVE - Skill creation reference
├── optimize-tokens.md                    🔄 MOVE - Token optimization reference
└── retrospective.md                      🔄 MOVE - Retrospective reference
```

**Reason:** These are documentation about using KB in projects.

**Format:** Keep as `.md` (reference documentation, not KB entries).

---

### 4. KEEP in `universal/` (Critical for Default Processes)

These patterns are AUTO-LOADED or used by DEFAULT processes:

```
universal/agent-instructions/
├── base-instructions.yaml                ✅ KEEP - Auto-loaded by ALL agents
├── README.md                             ✅ KEEP - Documentation
├── AGENT-QUICK-START.md                  ✅ KEEP - Quick start guide
└── templates/                            ✅ KEEP - Issue/PR templates
    ├── comment-template.md
    ├── issue-header.md
    ├── issue-template.md
    └── pr-template.md

universal/patterns/
├── progressive-disclosure.yaml           ✅ KEEP - Universal pattern
├── skill-design.yaml                     ✅ KEEP - Universal pattern
├── agent-handoff.yaml                    ✅ KEEP - Universal pattern
├── agent-orchestration.yaml              ✅ KEEP - Universal pattern
├── agent-accountability.yaml             ✅ KEEP - Universal pattern
├── agent-auto-configuration.yaml         ✅ KEEP - Universal pattern
└── ... (other universal patterns)
```

**Reason:** These are UNIVERSAL patterns used across all domains, not Claude Code specific.

---

### 5. MOVE to `claude-code/patterns/` (Claude Code Specific)

These patterns are SPECIFIC to Claude Code and should be in their own domain:

```
universal/patterns/  →  claude-code/patterns/
├── claude-code-files-organization-001.yaml  🔄 MOVE - Claude Code specific
├── claude-code-hooks.yaml                    🔄 MOVE - Claude Code specific
├── claude-code-shared-model.yaml             🔄 MOVE - Claude Code specific
└── CLAUDE-CODE-AUTO-ACTIVATION-001.yaml      🔄 MOVE - Claude Code specific
```

**Reason:** These are explicitly Claude Code patterns, not universal.

**Verification:** Check if any project auto-loads these by ID pattern match.

---

### 6. CONVERT to `claude-code/errors/` (From MD Guides)

Convert top MD guides to searchable YAML entries:

```
docs/research/claude-code/  →  claude-code/errors/
├── CLAUDE-CLAUDE-MD-GUIDE.md          →  CLAUDE-MD-001.yaml
├── claude-hooks-guide.md              →  HOOKS-GUIDE-002.yaml
├── claude-skills-guide.md             →  SKILLS-GUIDE-003.yaml
├── claude-agents-guide.md             →  AGENTS-GUIDE-004.yaml
├── CLAUDE-PERMISSION-MODES-GUIDE.md   →  PERMISSION-MODES-005.yaml
├── CLAUDE-SLASH-COMMANDS-GUIDE.md     →  SLASH-COMMANDS-006.yaml
├── CLAUDE-PROJECTS-COLLABORATION-GUIDE.md  →  PROJECTS-COLLAB-007.yaml
├── CLAUDE-REFERENCING-CONTEXT-GUIDE.md    →  REFERENCING-008.yaml
└── CLAUDE-MCP-GUIDE.md                →  MCP-INTEGRATION-009.yaml
```

**Keep as MD in `docs/research/claude-code/`:**
- INDEX.md (navigation)
- README.md (overview)
- archive/ (deprecated docs)
- issues/ (PR analysis)

---

## Verification Steps

### Check Auto-Load References

Before moving patterns from `universal/`, verify they're not auto-loaded:

```bash
# Search for references to these patterns
grep -r "claude-code-files-organization-001" --include="*.yaml" --include="*.md"
grep -r "claude-code-hooks" --include="*.yaml" --include="*.md"
grep -r "claude-code-shared-model" --include="*.yaml" --include="*.md"
grep -r "CLAUDE-CODE-AUTO-ACTIVATION" --include="*.yaml" --include="*.md"
```

**Results:** If no references found, safe to move.

---

### Check base-instructions.yaml Dependencies

Verify what depends on `universal/agent-instructions/base-instructions.yaml`:

```bash
grep -r "agent-instructions/base-instructions" --include="*.yaml" --include="*.md"
```

**Expected:** Many references - this is auto-loaded by design, do NOT move.

---

## Migration Order

### Phase 1: Create Domain Structure
```bash
mkdir -p claude-code/agent-instructions/subagents
mkdir -p claude-code/errors
mkdir -p claude-code/patterns
mkdir -p claude-code/commands
touch claude-code/.curator-only
```

### Phase 2: Move Agent Instructions
```bash
# Convert .md to .yaml
mv .claude/agents/claude-code-expert.md claude-code/agent-instructions/claude-code-expert.yaml
mv .claude/agents/kb-curator.md claude-code/agent-instructions/kb-curator.yaml
mv .claude/agents/subagents/*.md claude-code/agent-instructions/subagents/
```

### Phase 3: Move Patterns
```bash
# Move only Claude Code specific patterns
mv universal/patterns/claude-code-*.yaml claude-code/patterns/
mv universal/patterns/CLAUDE-CODE-*.yaml claude-code/patterns/
```

### Phase 4: Move Commands
```bash
# Keep as MD (reference docs)
mv .claude/commands/* claude-code/commands/
```

### Phase 5: Convert MD to YAML
```bash
# Convert top guides to YAML entries
# (Detailed conversion plan in next section)
```

### Phase 6: Clean Up
```bash
# Remove empty directories
rmdir .claude/agents/subagents
rmdir .claude/agents
rmdir .claude/commands
```

---

## Risk Assessment

### Low Risk ✅
- Moving patterns from `universal/` to `claude-code/patterns/`
- Moving commands from `.claude/` to `claude-code/commands/`
- Converting MD guides to YAML

### Medium Risk ⚠️
- Moving agents from `.claude/agents/` to `claude-code/agent-instructions/`
- Need to verify no auto-load by ID

### High Risk ❌
- Moving `universal/agent-instructions/base-instructions.yaml`
- **DO NOT MOVE** - Critical for all agents

---

## Success Criteria

1. ✅ All Claude Code knowledge in `claude-code/` domain
2. ✅ Searchable via `kb.py search --scope claude-code`
3. ✅ Progressively loadable via `git sparse-checkout`
4. ✅ No broken auto-loads
5. ✅ All existing functionality preserved
6. ✅ `.claude/` contains only Shared KB project files

---

## Post-Migration Validation

### 1. Test Search
```bash
python tools/kb.py search "claude code hooks"
python tools/kb.py search --scope claude-code --tag skills
```

### 2. Test Progressive Loading
```bash
git sparse-checkout set claude-code
python tools/kb_domains.py info claude-code
```

### 3. Test Auto-Load
```bash
# Verify base-instructions still loads
grep -r "GITHUB-ATTRIB-001" --include="*.yaml"
```

### 4. Verify Domain Index
```bash
grep "claude-code:" _domain_index.yaml
python tools/kb_domains.py list
```

---

**Status:** Ready for migration
**Estimated Time:** 4-6 hours
**Risk Level:** Low (with verification steps)
