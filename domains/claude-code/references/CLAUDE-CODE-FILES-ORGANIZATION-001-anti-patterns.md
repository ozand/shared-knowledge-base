# Anti-Patterns and Solutions

**See:** @patterns/claude-code-files-organization-001.yaml

---

## Anti-Pattern 1: Massive CLAUDE.md (1000+ lines)

### Problem
- Token waste (loaded every session)
- Hard to navigate
- Mixed concerns (overview + details + everything)
- Difficult to maintain

### Solution
Keep CLAUDE.md ≤ 300 lines:
- Overview (2-3 sentences)
- Quick start (1 command)
- Key features (bulleted)
- Links to details (not duplication)
- Recent decisions

Move details to:
- @standards/architecture.md
- @standards/coding-standards.md
- @references/

**Reference:** PROGRESSIVE-DISCLOSURE-001

---

## Anti-Pattern 2: Too Many Micro-Skills

### Problem
```
.claude/skills/
├── unit-test-skill/
├── integration-test-skill/
├── e2e-test-skill/
├── snapshot-test-skill/
├── performance-test-skill/
└── ... (10+ skills for one topic)
```

- Claude confused about which to use
- Might not find the right one
- 300+ tokens metadata overhead
- Hard to manage

### Solution
Consolidate into one skill:
```
.claude/skills/
└── testing-skill/
    ├── SKILL.md (main)
    └── resources/
        ├── patterns-unit.md
        ├── patterns-integration.md
        ├── patterns-e2e.md
        └── patterns-performance.md
```

**Reference:** claude-skills-guide.md:1119-1157

---

## Anti-Pattern 3: Using Prompts Instead of Hooks

### Problem
Relying on prompts for critical tasks:
- "Please validate YAML" → Claude might forget
- "Check coverage" → Claude might skip
- "Run tests" → Claude might not do it

### Solution
Use hooks for deterministic automation:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit:*.yaml|Write:*.yaml",
      "command": ".claude/hooks/validate-yaml.sh"
    }]
  }
}
```

**Hooks = Guaranteed execution**
**Prompts = Probabilistic (might happen)**

**Reference:** claude-code-hooks.yaml:15-36

---

## Anti-Pattern 4: Duplication Across Files

### Problem
Error handling rules in:
- CLAUDE.md
- standards/error-handling.md
- docs/best-practices.md
- patterns/error-handling-001.yaml

→ Updates missed, inconsistency spreads

### Solution
Single source of truth:
```
standards/error-handling.md (authoritative)
```

All others reference it:
```
CLAUDE.md: "See @standards/error-handling.md"
SKILL.md: "Follow @standards/error-handling.md"
AGENT.md: "Refer to @standards/error-handling.md"
```

**Reference:** claude-code-shared-model.yaml:97-106

---

## Anti-Pattern 5: Wrong Model for Agent Task

### Problem
Using Haiku (fast, simple) for complex reasoning
→ Fails to understand nuances
→ Makes random decisions
→ Low quality output

### Solution
Match model to task complexity:
- **Opus 4:** Planning, routing, complex reasoning
- **Sonnet 4:** Coding, analysis, debugging
- **Haiku 4:** Simple, routine tasks

Example breakdown:
- 10% Opus (orchestrator)
- 60% Sonnet (workers)
- 30% Haiku (simple tasks)

**Result:** 70% cost savings, quality maintained

**Reference:** claude-agents-guide.md:614-634

---

## Anti-Pattern 6: Using Agents for Simple Tasks

### Problem
Creating agent for one-off task:
- Over-engineering
- Complex setup for simple need
- Wasted development time

### Solution
**Use SKILL instead when:**
- Task is one-off or rare
- No iteration needed
- No autonomy required
- Quick workflow

**Use AGENT when:**
- Task requires autonomy
- Need iteration (plan changes)
- Long-running service
- External integration

**Reference:** claude-agents-guide.md:36-52

---

## Anti-Pattern 7: Deeply Nested References

### Problem
```
SKILL.md
  └─ @resources/main.md
      └─ @../standards/testing.md
          └─ @../../team/guidelines.md
              └─ @../../../../best-practices.md
```

- Claude may partially read
- Files not found (wrong paths)
- Hard to track dependencies

### Solution
Keep references one level deep from SKILL.md:
```
SKILL.md
  ├─ @resources/patterns.md (direct)
  ├─ @resources/examples.md (direct)
  └─ @../../standards/architecture.md (max 1 up)
```

**Reference:** claude-skills-guide.md:1197-1223

---

## Anti-Pattern 8: Scripts Without Error Handling

### Problem
```python
def analyze_csv(path):
    df = pd.read_csv(path)  # Crashes if file missing
    return df.describe()
```

- Script crashes silently
- Claude doesn't know why
- Poor user experience

### Solution
```python
def analyze_csv(path):
    try:
        if not os.path.exists(path):
            print(f"ERROR: File not found: {path}")
            return None

        df = pd.read_csv(path)
        if df.empty:
            print(f"ERROR: CSV is empty")
            return None

        return df.describe()

    except Exception as e:
        print(f"ERROR: {e}")
        return None
```

- Graceful degradation
- Helpful error messages
- Claude can react properly

**Reference:** claude-skills-guide.md:1159-1195
