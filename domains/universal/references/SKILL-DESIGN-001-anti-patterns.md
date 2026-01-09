# Skill Design Pattern - Anti-Patterns

**Extracted from:** skill-design.yaml
**Pattern ID:** SKILL-DESIGN-001

## Anti-Pattern 1: Vague Description

**Wrong:**
```yaml
description: "Testing helper"
```

**Consequence:** Skill never triggers when needed. Claude doesn't understand when to use it.

**Correct:**
```yaml
description: |
  Generates unit tests with 80%+ coverage using Vitest.

  Triggers when:
  - User asks to "write tests" or "generate tests"
  - Testing function or component
  - Part of code review process

  Outputs complete test files with edge cases and assertions.
```

## Anti-Pattern 2: Monolithic SKILL.md

**Wrong:** SKILL.md with 2000+ lines including all patterns, examples, docs

**Consequence:** Loads everything every time. Wastes 1500+ tokens. Slow. Hard to update.

**Correct:**
```
SKILL.md (300 lines - core instructions + @references)
resources/
├── patterns.md (all patterns, loaded on demand)
├── examples/ (full examples, loaded on demand)
└── template.ts (template, loaded on demand)
```

## Anti-Pattern 3: Too Many Micro-Skills

**Wrong:** 10 skills for one domain (unit-test-skill, integration-test-skill, e2e-skill...)

**Consequence:** Claude confused by choice. 300+ tokens metadata. Hard to manage.

**Correct:**
```
One testing-skill/
├── SKILL.md (unified instructions)
└── resources/
    ├── patterns-unit.md
    ├── patterns-integration.md
    └── patterns-e2e.md
```

## Anti-Pattern 4: Scripts Without Error Handling

**Wrong:**
```python
def analyze_csv(path):
    df = pd.read_csv(path)  # Crashes if file missing!
    return df.describe()
```

**Consequence:** Script crashes. Claude doesn't know why. Bad user experience.

**Correct:**
```python
def analyze_csv(path):
    try:
        if not os.path.exists(path):
            print(f"ERROR: File not found: {path}")
            return None
        df = pd.read_csv(path)
        if df.empty:
            print(f"ERROR: CSV is empty: {path}")
            return None
        return df.describe()
    except Exception as e:
        print(f"ERROR: Failed to analyze CSV: {e}")
        return None
```

## Anti-Pattern 5: Deep Nested References

**Wrong:**
```
SKILL.md
  └─ @resources/main.md
      └─ @../standards/testing.md
          └─ @../../team/guidelines.md
```

**Consequence:** Claude loses context. Files not found. Hard to track.

**Correct:**
```
SKILL.md
  ├─ @resources/patterns.md (direct)
  ├─ @resources/examples.md (direct)
  └─ Reference: @../../CLAUDE.md (max 1 level up)
```

## Key Takeaways

1. **Description = 80% of success**
   - Be specific about WHEN to use
   - List trigger conditions
   - Explain output clearly

2. **Progressive disclosure is mandatory**
   - Keep SKILL.md lean (200-500 lines)
   - Use @resources/ for details
   - Load on demand

3. **Consolidate, don't fragment**
   - One skill per domain
   - Use subdirectories for organization
   - Reduce Claude's decision burden

4. **Error handling is not optional**
   - Validate inputs
   - Return helpful errors
   - Fail gracefully

5. **Keep references local**
   - All @refs within skill directory
   - Max 1 level up to CLAUDE.md
   - Avoid deep nesting
