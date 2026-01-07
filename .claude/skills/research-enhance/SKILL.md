---
name: "research-enhance"
description: "Enhance knowledge base entries with deep research from external sources. Incorporates latest best practices, community consensus, and version-specific information"
version: "1.0"
author: "Shared KB Curator"
tags: ["research", "enhance", "update", "best-practices"]
resources:
  - "resources/research-sources.md"
  - "resources/enhancement-examples.md"
---

# Skill: Research Enhance

## What this Skill does
Enhance knowledge base entries with deep research from external sources. Incorporates latest best practices, community consensus, and version-specific information.

## Trigger
- User mentions "enhance", "research", "update entry", "add best practices"
- Entry score is low (75-84) and needs improvement
- After library/framework version updates
- During entry creation (to ensure completeness)
- Part of curator workflow

## Enhancement Workflow

### Step 1: Analyze Entry Gaps

Check current entry for:
- ✅ Problem clarity
- ✅ Solution completeness
- ⚠️ Root cause depth
- ❌ Prevention strategies (often missing)
- ❌ Best practices (often missing)
- ⚠️ Version information (may be outdated)

### Step 2: Create Research Plan

Formulate research questions based on entry topic:
1. What's new in latest versions?
2. Common pitfalls (official docs)?
3. Community best practices?
4. Performance considerations?
5. Security implications?
6. Testing strategies?

### Step 3: Conduct Research

**Research sources:**
- Official documentation
- Community knowledge (Stack Overflow)
- Best practices (style guides)
- Security advisories
- Performance guides

**📘 Detailed Research Sources:** `@resources/research-sources.md`

### Step 4: Enhance Entry

Update entry with:
- Latest version information
- Best practices from community
- Prevention strategies
- Alternative solutions
- Performance considerations
- Testing approaches
- Security implications

### Step 5: Validate & Score

Validate enhanced entry:
```bash
python tools/kb.py validate <entry>
python tools/kb.py check-quality <entry>
```

Target: 85+/100

## What Claude Can Do

### Research Latest Best Practices

```bash
# Entry: python/errors/async-timeout.yaml
# Current score: 72/100

# Research: Python 3.11+ asyncio enhancements
# Sources: Official docs, PEP discussions, community guides
# Find: TaskGroup (3.11+), improved error handling

# Update entry:
# - Add Python 3.11+ TaskGroup example
# - Include best practices from asyncio docs
# - Add prevention strategies
# - Update tested versions

# Result: Score 88/100 ✅
```

### Incorporate Community Knowledge

```bash
# Entry: docker/errors/volume-permissions.yaml
# Current: Basic solution (chmod 777)

# Research: Docker volume best practices
# Sources: Docker docs, Stack Overflow, security guides
# Find: Proper user permissions, security risks of 777

# Update entry:
# - Add security warning for 777
# - Include proper user setup
# - Add SELinux context handling
# - Reference Docker best practices

# Result: Secure, production-ready solution ✅
```

### Update with Latest Versions

```bash
# Entry: javascript/errors/promise-finally.yaml
# Current: Node.js 14 examples

# Research: Latest Node.js (20+) promise handling
# Sources: Node.js docs, TC39 proposals
# Find: Promise.withResolvers (Node 22+), async/await improvements

# Update entry:
# - Add modern promise patterns
# - Include Promise.withResolvers example
# - Update tested versions
# - Add migration notes

# Result: Up-to-date with modern JavaScript ✅
```

## Key Files to Reference

- **Entry being enhanced:** Target YAML file
- **Official docs:** Language/framework documentation
- `@standards/yaml-standards.md` - Entry format requirements
- `@standards/quality-gates.md` - Quality scoring rubric
- **Research resources:** `@resources/research-sources.md`

## Implementation Rules

1. **Always verify** information from multiple sources
2. **Prefer official docs** over community posts
3. **Check version compatibility** before suggesting new features
4. **Test code examples** in relevant environment
5. **Update metadata** with latest versions tested
6. **Cite sources** in comments or references field
7. **Balance completeness** with clarity (don't overwhelm)

## Quality Checklist

After enhancement:

- [ ] All information verified from authoritative sources
- [ ] Code examples tested and working
- [ ] Version information up-to-date
- [ ] Best practices included
- [ ] Prevention strategies added
- [ ] Quality score ≥ 85/100
- [ ] No information overload (clear, actionable)
- [ ] Entry validation passes

## Common Enhancement Patterns

### Adding Prevention Strategies

**Before (no prevention):**
```yaml
problem: "Async timeout occurs"
solution: "Use asyncio.wait_for()"
```

**After (with prevention):**
```yaml
problem: "Async timeout occurs"
solution: "Use asyncio.wait_for()"
prevention:
  - "Always set reasonable timeouts"
  - "Use TaskGroup for multiple tasks (Python 3.11+)"
  - "Log timeout events for monitoring"
```

### Updating Versions

**Before (outdated):**
```yaml
solution:
  code: |
    import asyncio  # Tested on Python 3.9
```

**After (current):**
```yaml
solution:
  code: |
    import asyncio  # Tested on Python 3.11+
    # Uses TaskGroup (Python 3.11+)
```

### Adding Best Practices

**Before (basic solution):**
```yaml
solution: "Use try/except for error handling"
```

**After (with best practices):**
```yaml
solution:
  code: |
    try:
      await operation()
    except SpecificError as e:
      logger.error(f"Specific error: {e}")
      raise
best_practices:
  - "Catch specific exceptions, not bare except"
  - "Always log with context"
  - "Re-raise after handling if needed"
```

**📘 More Examples:** `@resources/enhancement-examples.md` - Comprehensive enhancement scenarios

## Output

**Success:**
```
✅ Entry enhanced: python/errors/async-timeout.yaml
📊 Quality score: 72/100 → 88/100 (+16)
📝 Added:
  - Prevention strategies (3 items)
  - Python 3.11+ TaskGroup example
  - Best practices from community
  - Updated tested versions
✅ Validation passed
```

**No improvements found:**
```
✅ Entry review complete: python/errors/async-timeout.yaml
📊 Quality score: 89/100
💡 Entry already excellent
📝 Minor improvements:
  - Added 1 community best practice
  - Updated version info
```

## Related

- `@skills/audit-quality/SKILL.md` - Quality audit skill
- `@standards/yaml-standards.md` - Entry format standards
- `@standards/quality-gates.md` - Quality requirements
- `@resources/research-sources.md` - Detailed research sources
- `@resources/enhancement-examples.md` - Enhancement examples
