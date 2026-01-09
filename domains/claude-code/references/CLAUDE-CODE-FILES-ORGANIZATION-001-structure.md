# Complete Directory Structure

**See:** @patterns/claude-code-files-organization-001.yaml

---

## Production-ready .claude/ directory structure

```
.claude/                              # Project-level configuration (git)
├── CLAUDE.md                        # Navigation hub (~300 lines)
│   ├── Overview (2-3 sentences)
│   ├── Quick start (1 command)
│   ├── Key features (bulleted)
│   ├── Documentation links
│   └── Recent decisions
│
├── settings.json                    # Feature flags, enabled skills/agents
│   ├── skills.enabled: ["testing", "code-review"]
│   └── hooks: {SessionStart, PostToolUse, Stop}
│
├── skills/                          # Procedural knowledge (auto-discovered)
│   ├── testing/
│   │   ├── SKILL.md                # Metadata + instructions (200-500 lines)
│   │   │   ├── YAML frontmatter (name, description)
│   │   │   ├── When to use
│   │   │   ├── What it does
│   │   │   ├── Key instructions
│   │   │   └── @resources/ references
│   │   ├── resources/
│   │   │   ├── patterns.md        # Detailed patterns (100-500 lines)
│   │   │   ├── examples/          # Concrete examples
│   │   │   │   ├── templates/     # Code templates
│   │   │   │   └── assertions.md  # Assertion patterns
│   │   └── scripts/               # Optional automation
│   │       └── generate_tests.py
│   │
│   ├── code-review/
│   │   ├── SKILL.md
│   │   └── resources/
│   │       ├── checklist.md
│   │       └── rules/
│   │
│   └── documentation/
│       ├── SKILL.md
│       └── resources/
│           └── templates/
│
├── agents/                          # Autonomous agents (explicit invocation)
│   ├── orchestrator.md             # Main coordinator (Opus 4)
│   ├── code-review-agent.md        # Specialist (Sonnet 4)
│   ├── security-agent.md
│   └── subagents/                  # Isolated workers
│       ├── researcher.md
│       ├── debugger.md
│       ├── validator.md
│       └── knowledge-curator.md
│
├── commands/                        # Slash commands (prompt templates)
│   ├── test.md                     # /project:test
│   ├── review.md                   # /project:review
│   ├── deploy.md                   # /project:deploy
│   └── debug.md                    # /project:debug
│
├── hooks/                           # Lifecycle automation (deterministic)
│   ├── session-setup.sh            # SessionStart: Environment setup
│   ├── validate-yaml.sh            # PreToolUse: Block invalid YAML
│   ├── quality-gate.sh             # PostToolUse: Check quality
│   ├── auto-format.sh              # PostToolUse: Format code
│   └── auto-commit.sh              # Stop: Auto-commit changes
│
├── standards/                       # Team standards (single source of truth)
│   ├── architecture.md             # System design patterns
│   ├── coding-standards.md         # Style guidelines
│   ├── testing-guidelines.md       # Test patterns
│   └── api-standards.md            # API design rules
│
├── references/                      # Reference documentation (progressive)
│   ├── patterns/                   # Design patterns
│   ├── apis/                       # API documentation
│   └── troubleshooting.md          # Common issues
│
└── memory/                          # Persistent memory (optional)
    ├── project-state.json          # Decisions, context
    └── session-history.json        # Cross-session memory
```

## User-level structure

```
~/.claude/                           # User-level configuration (personal)
├── CLAUDE.md                        # Personal preferences
├── skills/                          # Personal skills
│   ├── my-coding-style/
│   └── brand-guidelines/
└── settings.json                    # User-level config
```
