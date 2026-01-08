# Migration Plan: v4.0 → v5.1

**Date:** 2026-01-08
**Status:** 🔄 In Progress
**Version:** 5.1.0

---

## 📊 Current State Analysis

### Existing Structure (v4.0)

```
shared-knowledge-base/
├── python/              # Domain: Python errors & patterns ✅
├── docker/              # Domain: Docker & containers ✅
├── postgresql/          # Domain: PostgreSQL ✅
├── javascript/          # Domain: JavaScript/Node.js ✅
├── universal/           # Domain: Cross-language patterns ✅
├── framework/           # Domain: Framework-specific ✅
├── vps/                 # Domain: VPS/DevOps ✅
│
├── tools/               # v4.0 CLI tools (kb.py, etc.) ✅
├── docs/                # v4.0 documentation ✅
├── for-claude-code/     # Claude Code integration ✅
├── for-projects/        # Project templates ✅
├── curator/             # Curator instructions ✅
│
├── README.md            # v4.0 main readme ⚠️ NEEDS UPDATE
├── QUICKSTART.md        # v4.0 quick start ⚠️ NEEDS UPDATE
├── CHANGELOG.md         # Version history ⚠️ NEEDS UPDATE
│
├── .kb/                 # ⚠️ NEW (only has shared/ symlink)
└── examples/            # ✅ Has v5.1 subdirectory
```

### New Structure (v5.1)

```
shared-knowledge-base/
├── [domains]            # ✅ UNCHANGED - All existing domains stay
│
├── tools/               # 🆕 NEW: v5.1 subdirectory
│   ├── v5.1/            # ✅ CREATED: New tools
│   │   ├── kb_submit.py
│   │   ├── kb_search.py
│   │   ├── kb_curate.py
│   │   └── hooks/
│   │       └── session-start.sh
│   └── [v4.0 tools]     # ✅ PRESERVED: Old tools still work
│
├── docs/                # 🆕 NEW: v5.1 subdirectory
│   ├── v5.1/            # ✅ CREATED: New documentation
│   │   ├── ARD.md
│   │   ├── WORKFLOWS.md
│   │   ├── CONTEXT_SCHEMA.md
│   │   └── README.md
│   └── [v4.0 docs]     # ✅ PRESERVED: Old docs still valid
│
├── examples/            # 🆕 NEW: v5.1 subdirectory
│   ├── v5.1/            # ✅ CREATED: New examples
│   │   ├── .env.example
│   │   ├── PROJECT.yaml.example
│   │   ├── MEMORY.md.example
│   │   └── kb-entry-example.yaml
│   └── [existing]       # ✅ PRESERVED: Old examples
│
├── .kb/                 # 🆕 NEW: Project-level KB structure
│   ├── context/         # ⚠️ TO CREATE: Project context
│   │   ├── PROJECT.yaml
│   │   └── MEMORY.md
│   ├── project/         # ⚠️ TO CREATE: Project KB
│   │   ├── integrations/
│   │   ├── endpoints/
│   │   ├── decisions/
│   │   ├── lessons/
│   │   └── pending/
│   └── shared/          # ✅ EXISTS: Symlink to repo root
│
├── for-claude-code/     # ✅ UNCHANGED
├── for-projects/        # ✅ UNCHANGED
├── curator/             # ✅ UNCHANGED
│
├── README.md            # ⚠️ TO UPDATE: Add v5.1 info
├── QUICKSTART.md        # ⚠️ TO UPDATE: Add v5.1 quick start
└── CHANGELOG.md         # ⚠️ TO UPDATE: Add v5.1 changelog
```

---

## 🎯 Migration Strategy

### Phase 1: Repository Updates (Shared KB itself)

**Status:** ✅ COMPLETED

1. ✅ Created `docs/v5.1/` with new documentation
2. ✅ Created `tools/` with new tools
3. ✅ Created `examples/v5.1/` with templates

**Remaining:**
- ⚠️ Update `README.md` to mention v5.1
- ⚠️ Update `QUICKSTART.md` with v5.1 quick start
- ⚠️ Update `CHANGELOG.md` with v5.1 release notes
- ⚠️ Create migration guide for users

### Phase 2: Project Migration (Users' projects)

**Status:** 🔄 TO BE DONE

Need to create:
1. **Migration script** (`migrate-to-v5.1.sh`)
2. **Migration guide** (`MIGRATION-GUIDE.md`)
3. **Compatibility checks** (verify v4.0 still works)

---

## 📋 Detailed Action Items

### A. Update Root Documentation

#### 1. README.md

**Changes needed:**
- Add v5.1 section to "What's New"
- Add link to `docs/v5.1/README.md`
- Update version number to 5.1.0
- Add migration warning for existing users

**Draft:**
```markdown
## 🆕 Version 5.1 (2026-01-08)

**Two-Tier Architecture** - Separate Project KB and Shared KB

- ✅ Project KB (`.kb/project/`) - Private, direct commits
- ✅ Shared KB (`.kb/shared/`) - Public, GitHub Issues workflow
- ✅ Automatic context loading via SessionStart hook
- ✅ PyGithub integration (no gh CLI dependency)

**Quick Start:**
```bash
# New projects: See docs/v5.1/README.md
# Existing projects: See docs/v5.1/MIGRATION-GUIDE.md
```

**Backward Compatibility:** ✅ v4.0 tools still work!
```

#### 2. QUICKSTART.md

**Changes needed:**
- Add "Quick Start for v5.1" section
- Link to `docs/v5.1/README.md`
- Keep v4.0 quick start for legacy users

#### 3. CHANGELOG.md

**Add new entry:**
```markdown
## [5.1.0] - 2026-01-08

### Added
- Two-tier knowledge management (Project KB + Shared KB)
- GitHub Issues workflow for shared submissions
- PyGithub integration for issue creation
- Automatic context loading (session-start.sh hook)
- Decision criteria system (sharing_criteria in PROJECT.yaml)
- v5.1 tools (kb_submit.py, kb_search.py, kb_curate.py)
- Complete v5.1 documentation (ARD, WORKFLOWS, CONTEXT_SCHEMA)

### Changed
- Tools directory: Added v5.1 subdirectory
- Docs directory: Added v5.1 subdirectory
- Examples directory: Added v5.1 subdirectory

### Deprecated
- gh CLI dependency (use PyGithub instead)

### Fixed
- Fixed kb_submit.py code blocks
- Fixed Issue body YAML formatting
- Added validation to kb_submit.py

### Backward Compatibility
- ✅ v4.0 tools still work
- ✅ v4.0 documentation still valid
- ✅ Existing projects can migrate at their own pace
```

### B. Create Migration Guide

**File:** `docs/v5.1/MIGRATION-GUIDE.md`

**Sections:**
1. Overview of changes
2. Pre-migration checklist
3. Step-by-step migration
4. Post-migration verification
5. Rollback instructions
6. Troubleshooting

### C. Create Migration Script

**File:** `tools/migrate-to-v5.1.sh`

**Features:**
- Backup existing `.kb/` directory
- Create new directory structure
- Copy templates from `examples/v5.1/`
- Preserve existing configurations
- Run validation checks

---

## 🔍 Compatibility Matrix

| Feature | v4.0 | v5.1 | Migration Path |
|---------|------|------|----------------|
| **KB Storage** | Single-tier | Two-tier | Optional upgrade |
| **Submission** | Direct/Issues | Issues only | Recommended |
| **Tools** | tools/*.py | tools/*.py | Both work |
| **Documentation** | docs/* | docs/v5.1/* | Both valid |
| **Context Loading** | Manual | Automatic | Optional |
| **Dependency** | gh CLI | PyGithub | Recommended |
| **Project KB** | No | Yes | New feature |

---

## 📊 Impact Assessment

### Low Impact Changes
- ✅ New documentation in separate directories
- ✅ New tools in v5.1 subdirectory
- ✅ New examples in v5.1 subdirectory

### Medium Impact Changes
- ⚠️ README.md updates (informational only)
- ⚠️ QUICKSTART.md updates (informational only)
- ⚠️ CHANGELOG.md updates (informational only)

### High Impact Changes
- 🔴 Project structure changes (`.kb/` directory)
- 🔴 Tool usage changes (new commands)
- 🔴 Workflow changes (Issues instead of direct commits)

### No Breaking Changes
- ✅ All v4.0 features still work
- ✅ Existing domains unchanged
- ✅ v4.0 tools still functional
- ✅ No forced migration

---

## ✅ Migration Checklist

### Repository Level (shared-knowledge-base)

- [x] Create docs/v5.1/ directory
- [x] Create tools/ directory
- [x] Create examples/v5.1/ directory
- [x] Write ARD.md
- [x] Write WORKFLOWS.md
- [x] Write CONTEXT_SCHEMA.md
- [x] Write README.md (v5.1)
- [ ] Update main README.md
- [ ] Update QUICKSTART.md
- [ ] Update CHANGELOG.md
- [ ] Create MIGRATION-GUIDE.md
- [ ] Create migration script
- [ ] Test migration script
- [ ] Update website/docs (if applicable)

### User Project Level

For each user project:

- [ ] Backup existing `.kb/` directory
- [ ] Run migration script
- [ ] Create PROJECT.yaml
- [ ] Create MEMORY.md
- [ ] Install session-start.sh hook
- [ ] Configure GITHUB_TOKEN
- [ ] Test kb_search.py
- [ ] Test kb_submit.py (local)
- [ ] Test kb_submit.py (shared)
- [ ] Verify context loading
- [ ] Update team documentation

---

## 🚀 Recommended Rollout

### Week 1: Soft Launch
- Announce v5.1 availability
- Update documentation
- Create migration guide
- Gather feedback from early adopters

### Week 2: Testing
- Test migration script
- Test new tools
- Test workflows
- Fix bugs

### Week 3: Documentation
- Write migration guide
- Update tutorials
- Create video demos
- Publish examples

### Week 4: Public Launch
- Announce stable release
- Mark v4.0 as legacy
- Encourage migration
- Monitor issues

---

## 📝 Next Steps

1. **Update README.md** - Add v5.1 section (5 minutes)
2. **Update QUICKSTART.md** - Add v5.1 quick start (10 minutes)
3. **Update CHANGELOG.md** - Add v5.1 release notes (5 minutes)
4. **Create MIGRATION-GUIDE.md** - User migration guide (30 minutes)
5. **Create migration script** - Automate project migration (20 minutes)
6. **Test everything** - Verify all changes work (15 minutes)

**Total estimated time:** 1.5 hours

---

## 🔗 Related Documents

- **[ARD.md](ARD.md)** - Complete v5.1 architecture
- **[WORKFLOWS.md](WORKFLOWS.md)** - Agent and curator workflows
- **[CONTEXT_SCHEMA.md](CONTEXT_SCHEMA.md)** - PROJECT.yaml schema
- **[README.md](README.md)** - v5.1 overview

---

**Status:** 🔄 Plan created, execution pending
**Next Action:** Update main README.md
