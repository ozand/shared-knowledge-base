# Migration Guide

**See:** @patterns/claude-code-files-organization-001.yaml

---

## From Flat Structure to Organized

### Before
```
.claude/
├── skill1.md
├── skill2.md
├── skill3.md
└── agent1.md
```

### After
```
.claude/
├── CLAUDE.md              # Create navigation hub
├── skills/
│   ├── skill1/
│   │   ├── SKILL.md
│   │   └── resources/
│   ├── skill2/
│   └── skill3/
└── agents/
    └── agent1.md
```

### Steps

1. **Create directory structure**
   ```bash
   mkdir -p .claude/{skills,agents}
   ```

2. **Move skills to subdirectories**
   ```bash
   for skill in skill1 skill2 skill3; do
     mkdir -p ".claude/skills/$skill/resources"
     mv "$skill.md" ".claude/skills/$skill/SKILL.md"
   done
   ```

3. **Split large SKILL.md files**
   If SKILL.md > 500 lines:
   1. Keep main instructions in SKILL.md
   2. Move detailed content to resources/
   3. Add @references to new files

4. **Update CLAUDE.md**
   1. Add overview section
   2. Add quick start (1 command)
   3. Add key features (bulleted)
   4. Link to skills/agents/commands/

---

## From Massive CLAUDE.md to Lean

### Before
```
CLAUDE.md: 1000+ lines
- All details inline
- Mixed concerns
- Hard to navigate
```

### After
```
CLAUDE.md: ~300 lines
- Overview (2-3 sentences)
- Quick start (1 command + link)
- Key features (bulleted)
- Documentation links (not duplication)

standards/
├── architecture.md     # Detailed architecture
├── coding-standards.md  # Detailed guidelines
└── testing-guidelines.md # Detailed testing
```

### Steps

1. **Extract standards to separate files**
   ```bash
   # Extract sections from CLAUDE.md
   # Create standards/ directory
   mkdir -p .claude/standards
   ```

2. **Create lean CLAUDE.md**
   1. Keep only overview + links
   2. Move details to standards/
   3. Add @standards/ references

3. **Update all references**
   Search for old content location
   Replace with @standards/ references
   Verify no broken links

---

## From Manual Prompts to Automated Hooks

### Before
```
User: "Please validate YAML"
User: "Please run tests"
User: "Please format code"
```

### After
```json
.claude/settings.json:
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit:*.yaml|Write:*.yaml",
      "hooks": [
        {
          "command": ".claude/hooks/validate-yaml.sh"
        },
        {
          "command": ".claude/hooks/format-yaml.sh"
        }
      ]
    }]
  }
}
```

### Steps

1. **Identify repetitive manual tasks**
   What do you repeatedly ask Claude to do?
   Validate? Format? Test? Commit?

2. **Create hook scripts**
   ```bash
   # Create .claude/hooks/validate-yaml.sh
   # Create .claude/hooks/format-yaml.sh
   ```

3. **Configure hooks in settings.json**
   Add hooks to .claude/settings.json
   Specify matchers (which tools trigger)
   Set timeouts (default 60s)

4. **Test hooks manually**
   ```bash
   echo '{"tool_name":"Write","tool_input":{"file_path":"test.yaml"}}' | \
     ./.claude/hooks/validate-yaml.sh
   echo "Exit: $?"  # 0 = allow, 2 = block
   ```
