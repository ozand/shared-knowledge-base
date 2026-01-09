# Real-World Examples

**See:** @patterns/claude-code-files-organization-001.yaml

---

## Example 1: Shared Knowledge Base - Production Example

Real .claude/ structure from shared-knowledge-base repo

```
.claude/
├── CLAUDE.md                    # Project memory (300 lines)
├── settings.json                # Configuration
│
├── skills/                      # 7 KB skills
│   ├── kb-index/               # Search KB
│   ├── kb-create/              # Create entries
│   ├── kb-validate/            # Validate YAML
│   ├── audit-quality/          # Quality assessment
│   ├── find-duplicates/        # Find similar entries
│   ├── research-enhance/       # Research patterns
│   └── kb-search/              # Quick search
│
├── commands/                    # 7 slash commands
│   ├── kb-validate.md
│   ├── kb-create.md
│   ├── kb-index.md
│   ├── kb-search.md
│   ├── kb-sync.md
│   ├── kb-query.md
│   └── retrospective.md
│
├── agents/                      # Agent system
│   ├── kb-curator.md           # Main curator agent
│   └── subagents/              # 4 specialist subagents
│       ├── researcher.md
│       ├── debugger.md
│       ├── validator.md
│       └── knowledge-curator.md
│
└── hooks/                       # 9 automation hooks
    ├── session-setup.sh
    ├── validate-yaml-before-edit.sh
    ├── validate-yaml-before-write.sh
    ├── auto-create-metadata.sh
    ├── auto-format-yaml.sh
    ├── quality-gate.sh
    ├── check-index.sh
    ├── validate-metadata.sh
    └── check-artifact-updates.py
```

### Results
- 7 skills auto-discovered by Claude
- 7 commands available via / menu
- 5 agent specialists coordinated
- 9 hooks for automation
- **Estimated token savings: 60% vs prompts**

---

## Example 2: Monorepo with Multiple Teams

How to organize .claude/ for large teams

```
company-monorepo/
├── .claude/                      # Shared by all teams
│   ├── CLAUDE.md               # Company-wide standards
│   ├── standards/
│   │   ├── architecture.md     # System design
│   │   ├── security.md         # Security policies
│   │   └── compliance.md       # Legal requirements
│   └── skills/
│       ├── code-review/        # Shared code review skill
│       └── testing/            # Shared testing skill
│
├── frontend/.claude/            # Frontend team only
│   ├── CLAUDE.md               # React + TypeScript specific
│   ├── skills/
│   │   ├── component-library/
│   │   └── state-management/
│   └── standards/
│       └── react-patterns.md
│
└── backend/.claude/             # Backend team only
    ├── CLAUDE.md               # FastAPI + Python specific
    ├── skills/
    │   ├── api-design/
    │   └── database-migration/
    └── standards/
        └── python-patterns.md
```

### Hierarchy
```
Local (.local) → Package → Project → Global → (none)
Most specific → Least specific
```

### Benefits
- Company standards inherited by all teams
- Team-specific overrides where needed
- Clear separation of concerns
- Scalable to 100+ developers

---

## Example 3: Personal Developer Setup

User-level Claude Code configuration

```
~/.claude/
├── CLAUDE.md                   # Personal preferences
│   ## My Coding Style
│   - Use TypeScript strict mode
│   - Prefer functional over OOP
│   - Test coverage ≥ 80%
│
├── skills/                     # Personal skills
│   ├── my-coding-style/
│   │   └── SKILL.md
│   └── brand-guidelines/
│       └── SKILL.md
│
└── settings.json               # User config
    {
      "skills.enabled": ["my-coding-style", "brand-guidelines"]
    }
```

### Benefits
- Available in ALL projects
- Personal preferences preserved
- Not shared with team (in .gitignore)
