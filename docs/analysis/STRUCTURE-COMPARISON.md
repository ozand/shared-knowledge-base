================================================================================
CURRENT vs PROPOSED STRUCTURE COMPARISON
================================================================================

CURRENT STATE (Scattered across 3 locations):
--------------------------------------------------------------------------------

📁 docs/research/claude-code/           (31 MD files, ~23,600 lines)
├── INDEX.md                            (Navigation)
├── README.md                           (Overview)
├── CLAUDE-COMPLETE-PRACTICES.md        (1,121 lines)
├── CLAUDE-COMPLETE-PRACTICES-EN.md     (~1,150 lines)
├── CLAUDE-CLAUDE-MD-GUIDE.md           (1,393 lines)
├── CLAUDE-PERMISSION-MODES-GUIDE.md    (1,298 lines)
├── CLAUDE-PERMISSION-MODES-GUIDE-EN.md (~1,325 lines)
├── CLAUDE-SLASH-COMMANDS-GUIDE.md      (1,366 lines)
├── CLAUDE-SLASH-COMMANDS-GUIDE-EN.md   (~1,390 lines)
├── CLAUDE-PROJECTS-COLLABORATION-GUIDE.md (938 lines)
├── CLAUDE-REFERENCING-CONTEXT-GUIDE.md (815 lines)
├── CLAUDE-PLANNING-WORKFLOW-GUIDE.md   (774 lines)
├── CLAUDE-MCP-GUIDE.md                 (737 lines)
├── claude-shared-architecture.md       (~1,400 lines)
├── claude-hooks-guide.md               (~1,200 lines)
├── claude-skills-guide.md              (~1,300 lines)
├── claude-agents-guide.md              (~1,100 lines)
├── claude-hooks-examples.md            (~800 lines)
├── claude-hooks-advanced.md            (~700 lines)
├── claude-templates.md                 (~600 lines)
├── claude-troubleshooting.md           (~300 lines)
├── ... (+10 more files)
├── archive/                            (Deprecated docs)
└── issues/                             (PR analysis)

📁 .claude/                             (~6,478 lines)
├── agents/
│   ├── claude-code-expert.md
│   ├── kb-curator.md
│   └── subagents/
│       ├── DEBUGGER.md
│       ├── KNOWLEDGE-CURATOR.md
│       ├── RESEARCHER.md
│       └── VALIDATOR.md
├── commands/
│   ├── kb-search.md
│   ├── kb-create.md
│   ├── kb-index.md
│   ├── kb-query.md
│   ├── kb-sync.md
│   ├── kb-validate.md
│   ├── add-hook.md
│   ├── create-skill.md
│   ├── optimize-tokens.md
│   └── retrospective.md
├── CLAUDE.md                           (This project's instructions)
└── errors/                             (Empty)

📁 universal/patterns/                  (4 existing YAML files)
├── claude-code-files-organization-001.yaml (51,996 lines - MASSIVE!)
├── claude-code-hooks.yaml              (15,795 lines)
├── claude-code-shared-model.yaml       (22,254 lines)
└── CLAUDE-CODE-AUTO-ACTIVATION-001.yaml (8,469 lines)

📊 TOTAL: ~128,588 lines across 3 locations
🔍 SEARCHABLE: Partially (only YAML patterns via kb.py)
⚡ PROGRESSIVE LOADING: No


================================================================================
PROPOSED STATE (Option B: Minimal Domain)
--------------------------------------------------------------------------------

📁 claude-code/                          (NEW DOMAIN)
├── .curator-only                       (Access control)
├── agent-instructions/
│   ├── claude-code-expert.yaml         (Moved from .claude/agents/)
│   ├── kb-curator.yaml                 (Moved from .claude/agents/)
│   └── subagents/
│       ├── DEBUGGER.yaml               (Moved from .claude/agents/)
│       ├── KNOWLEDGE-CURATOR.yaml
│       ├── RESEARCHER.yaml
│       └── VALIDATOR.yaml
├── errors/                             (Converted from MD guides)
│   ├── CLAUDE-MD-001.yaml              (From CLAUDE-CLAUDE-MD-GUIDE.md)
│   ├── HOOKS-GUIDE-002.yaml            (From claude-hooks-guide.md)
│   ├── SKILLS-GUIDE-003.yaml           (From claude-skills-guide.md)
│   ├── AGENTS-GUIDE-004.yaml           (From claude-agents-guide.md)
│   └── PERMISSION-MODES-005.yaml       (From permission guides)
├── patterns/                           (From universal/patterns/)
│   ├── claude-code-files-organization-001.yaml (Moved)
│   ├── claude-code-hooks.yaml          (Moved)
│   ├── claude-code-shared-model.yaml   (Moved)
│   └── CLAUDE-CODE-AUTO-ACTIVATION-001.yaml (Moved)
└── commands/                           (Reference docs - keep as MD)
    ├── kb-search.md                    (Moved from .claude/commands/)
    ├── kb-create.md
    ├── ... (10 more)

📁 docs/research/claude-code/           (KEPT - Reference only)
├── INDEX.md                            (Navigation)
├── README.md                           (Overview)
├── archive/                            (Deprecated docs)
└── issues/                             (PR analysis)

📁 .claude/                             (KEPT - Project-specific)
├── CLAUDE.md                           (This project's instructions)
└── errors/                             (Empty placeholder)

📊 TOTAL: ~5,000 lines in claude-code/ domain
🔍 SEARCHABLE: Yes (all via kb.py search)
⚡ PROGRESSIVE LOADING: Yes (git sparse-checkout)
💾 TOKEN SAVINGS: 75% (~2,500 vs ~10,000)


================================================================================
PROPOSED STATE (Option A: Full Domain)
--------------------------------------------------------------------------------

📁 claude-code/
├── .curator-only
├── agent-instructions/                 (4 agents + 4 subagents)
├── errors/                             (~15 entries from MD)
│   ├── CLAUDE-MD-001.yaml
│   ├── HOOKS-GUIDE-002.yaml
│   ├── SKILLS-GUIDE-003.yaml
│   ├── AGENTS-GUIDE-004.yaml
│   ├── PERMISSION-MODES-005.yaml
│   ├── SLASH-COMMANDS-006.yaml
│   ├── PROJECTS-COLLAB-007.yaml
│   ├── REFERENCING-008.yaml
│   ├── PLANNING-009.yaml
│   ├── MCP-INTEGRATION-010.yaml
│   ├── SHARED-ARCHITECTURE-011.yaml
│   ├── HOOKS-EXAMPLES-012.yaml
│   ├── HOOKS-ADVANCED-013.yaml
│   ├── TEMPLATES-014.yaml
│   └── TROUBLESHOOTING-015.yaml
├── patterns/                           (~20 entries)
│   ├── claude-code-files-organization-001.yaml
│   ├── claude-code-hooks.yaml
│   ├── claude-code-shared-model.yaml
│   ├── CLAUDE-CODE-AUTO-ACTIVATION-001.yaml
│   ├── progressive-disclosure.yaml     (From universal/)
│   ├── skill-design.yaml               (From universal/)
│   ├── agent-handoff.yaml              (From universal/)
│   ├── agent-orchestration.yaml        (From universal/)
│   ├── ... (12 more patterns)
└── commands/                           (12 reference MD files)

📊 TOTAL: ~9,500 lines in claude-code/ domain
🔍 SEARCHABLE: Yes (all via kb.py search)
⚡ PROGRESSIVE LOADING: Yes
💾 TOKEN SAVINGS: 5% (~9,500 vs ~10,000)
📈 COVERAGE: Complete (all features)


================================================================================
COMPARISON TABLE
--------------------------------------------------------------------------------

Aspect                 | Current       | Option A (Full) | Option B (Minimal)
-----------------------|---------------|-----------------|-------------------
Locations              | 3 scattered   | 1 organized     | 1 organized
Searchable             | Partially     | Fully           | Fully
Progressive Loading    | No            | Yes             | Yes
Token Cost             | ~10,000       | ~9,500 (5%)     | ~2,500 (75%)
Format Consistency     | No (MD+YAML)  | Yes (YAML)      | Yes (YAML)
Coverage               | Complete      | Complete        | Core only
Migration Effort       | -             | 12-17 hours     | 4-6 hours
Maintainability        | Poor          | Excellent       | Good


================================================================================
KEY BENEFITS
--------------------------------------------------------------------------------

✅ Unified structure - Same as other domains (docker, postgresql, etc.)
✅ Searchable - All entries via kb.py search
✅ Progressively loadable - Can load just claude-code domain
✅ Consistent format - All YAML, standardized schema
✅ Better discoverability - Clear domain in _domain_index.yaml
✅ Token efficient - 75% savings with Option B
✅ Scalable - Easy to add new entries
✅ Maintainable - Single location for all Claude Code knowledge


================================================================================
RECOMMENDATION
--------------------------------------------------------------------------------

Start with Option B (Minimal):
- Convert top 5 most-used guides
- Move existing 4 YAML patterns
- Test progressive loading
- Measure token savings

Expand to Option A if needed:
- Add more entries based on usage patterns
- Keep comprehensive coverage
- Maintain searchability

================================================================================
