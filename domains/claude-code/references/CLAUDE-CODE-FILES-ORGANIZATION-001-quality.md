# Quality Metrics and Verification

**See:** @patterns/claude-code-files-organization-001.yaml

---

## Token Efficiency

### Metric: Token Usage per Session

| Level | Tokens | Assessment |
|-------|--------|------------|
| Poor | >10000 | Too much context loaded |
| Acceptable | 5000-10000 | Room for improvement |
| Excellent | <5000 | Optimal loading |

### Calculation

**Session Start:**
- CLAUDE.md: ~300 tokens
- Skill metadata (10 skills × 50 tokens): 500 tokens
- **Total startup: ~800 tokens**

**When Skill Triggers:**
- Full SKILL.md: 500-2000 tokens
- Referenced resources: 400-1000 tokens
- **Total per skill: 1000-3000 tokens**

**Goal:** Minimal metadata, load details on-demand

---

## Discoverability

### Metric: Skill Discovery Rate

| Level | Rate | Assessment |
|-------|------|------------|
| Poor | <50% | Skills not found when needed |
| Acceptable | 50-80% | Moderate success |
| Excellent | >80% | Optimal discovery |

### Measurement
Track how often Claude uses the right skill:
- Log skill activation
- Compare against expected usage
- Improve descriptions based on misses

---

## Maintainability

### Metric: File Organization Score

| Level | Characteristics |
|-------|-----------------|
| Poor | Flat structure, mixed concerns |
| Acceptable | Organized by type, some duplication |
| Excellent | Clear separation, single source of truth |

### Checklist
- ✓ No duplication across files
- ✓ One source of truth per topic
- ✓ Progressive disclosure used
- ✓ Clear naming conventions
- ✓ Easy to navigate

---

## Organization Verification Checklist

### Setup
- [ ] **.claude/ directory exists**
  - Command: `ls -la .claude/`
  - Expected: Directory with subdirectories

- [ ] **CLAUDE.md ≤ 300 lines**
  - Command: `wc -l .claude/CLAUDE.md`
  - Expected: Less than 400 lines

- [ ] **settings.json valid JSON**
  - Command: `jq empty .claude/settings.json`
  - Expected: No syntax errors

- [ ] **Skills have YAML frontmatter**
  - Command: `grep -l '^name:' .claude/skills/*/SKILL.md`
  - Expected: All skills have name field

- [ ] **Hooks are executable**
  - Command: `ls -la .claude/hooks/*.sh`
  - Expected: Executable bit set

### Skills
- [ ] **Description is specific**
  - Verification: Read description, ask: Is it clear when to use?
  - Expected: Yes, includes what/when/triggers

- [ ] **SKILL.md ≤ 500 lines**
  - Command: `wc -l .claude/skills/*/SKILL.md`
  - Expected: All under 500 lines

- [ ] **Resources organized**
  - Verification: Check resources/ subdirectories exist
  - Expected: patterns/, examples/, templates/

- [ ] **No circular references**
  - Verification: Trace @references, check for loops
  - Expected: No circular dependencies

- [ ] **Tested with real usage**
  - Verification: Confirm skill tested in actual workflow
  - Expected: At least 3 evaluation scenarios run

### Agents
- [ ] **Model matches task complexity**
  - Verification: Review agent model choice
  - Expected: Opus for reasoning, Sonnet for work, Haiku for simple

- [ ] **Tool permissions minimal**
  - Verification: Check tools list in agent file
  - Expected: Only necessary tools, no blanket permissions

- [ ] **Decision rules defined**
  - Verification: Read agent file for decision rules section
  - Expected: Clear escalation path defined

- [ ] **Success criteria specified**
  - Verification: Check for measurable success criteria
  - Expected: Specific outputs, validation steps

### Hooks
- [ ] **Hooks execute in <2 seconds**
  - Command: `time .claude/hooks/*.sh`
  - Expected: All hooks complete in <2 seconds

- [ ] **Exit codes are correct**
  - Verification: Test hook with valid/invalid input
  - Expected: 0 = allow, 2 = block

- [ ] **Variables are quoted**
  - Verification: Check shell scripts for quoted variables
  - Expected: All "$VAR" properly quoted

- [ ] **Error handling present**
  - Verification: Review scripts for error handling
  - Expected: try/except or set -e or || exit 2

### Standards
- [ ] **No duplication across files**
  - Verification: Search for same rule in multiple files
  - Expected: Each rule has single source of truth

- [ ] **CLAUDE.md references standards**
  - Verification: Check for @standards/ references
  - Expected: Links to detailed standards, not duplication

- [ ] **Team reviewed (if applicable)**
  - Verification: Confirm team approved standards
  - Expected: Documented approval date
