# YAML Standards

**YAML entry format and structure standards for Shared Knowledge Base**

---

## Entry Structure

### Required Top-Level Fields

```yaml
version: "1.0"           # YAML format version
category: "category-name" # Category for grouping entries
last_updated: "YYYY-MM-DD" # Last update date
```

**Rules:**
- `version` must be "1.0"
- `category` should be descriptive (e.g., "async", "testing", "encoding")
- `last_updated` must be ISO 8601 format (YYYY-MM-DD)

---

## Entry Fields

### Required Fields

Every entry MUST have:

```yaml
errors:
  - id: "ERROR-001"           # Unique ID: CATEGORY-NNN
    title: "Error Title"       # Human-readable title
    severity: "high"           # critical | high | medium | low
    scope: "python"            # universal | python | javascript | docker | postgresql | framework
    problem: |                 # Description of problem
      Problem description
    solution:                  # Solution details
      code: |
        # Code example
      explanation: |
        How it works
```

### Optional Fields

```yaml
    symptoms:                  # List of symptoms
      - "Error message"
      - "Another symptom"
    root_cause: |              # Explanation of why it happens
      Root cause analysis
    prevention:                # Prevention strategies
      - "How to avoid"
      - "Another strategy"
    tags: ["tag1", "tag2"]     # Searchable tags
    local_only: true           # For project-specific entries
```

---

## ID Format

### Pattern: `CATEGORY-NNN`

**Examples:**
- `PYTHON-001` - Python error
- `DOCKER-045` - Docker error
- `ASYNC-123` - Async pattern
- `UNIVERSAL-001` - Universal pattern

**Rules:**
- Category must be uppercase
- Use hyphen separator
- Three-digit number (001-999)
- Unique within repository

**Finding next ID:**
```bash
# Search for existing IDs in category
grep -r "PYTHON-" python/errors/ | grep "id:" | sort | tail -1
```

---

## Severity Levels

### Critical
- Security vulnerabilities
- Data loss potential
- Complete system failure

### High
- Major functionality broken
- Significant performance impact
- Difficult workaround

### Medium
- Partial functionality broken
- Moderate performance impact
- Easy workaround

### Low
- Minor issues
- Cosmetic problems
- Nice-to-have improvements

---

## Scope Definitions

### Universal
**Definition:** Cross-language patterns, applies to all projects

**Examples:**
- Git workflows
- Testing patterns
- Architecture patterns
- Filesystem operations

**Push:** ✅ Always push to shared repository

---

### Language-Specific
**python, javascript, docker, postgresql**

**Definition:** Specific to language/technology

**Examples:**
- Python async patterns
- Docker container errors
- PostgreSQL indexing

**Push:** ✅ Always push to shared repository

---

### Framework-Specific
**framework**

**Definition:** Specific to frameworks (Django, FastAPI, React)

**Examples:**
- Django ORM patterns
- FastAPI dependency injection
- React hooks issues

**Push:** ❌ Keep in local KB

---

### Domain-Specific
**domain**

**Definition:** Business logic or industry-specific

**Examples:**
- Payment processing
- User authentication flows
- Industry regulations

**Push:** ❌ Keep in local KB

---

### Project-Specific
**project**

**Definition:** One-time or environment-specific

**Examples:**
- Local infrastructure issues
- Project-specific workarounds
- Temporary solutions

**Push:** ❌ Keep in local KB

---

## Code Examples

### Requirements

**✅ DO:**
- Use proper indentation (2 spaces)
- Include comments for clarity
- Show complete, runnable examples
- Follow language style guides
- Test examples before committing

**❌ DON'T:**
- Use tabs (use spaces)
- Include incomplete snippets
- Forget error handling
- Use obscure syntax without explanation

### Example Format

```yaml
    solution:
      code: |
        # ✅ GOOD: Complete, commented example
        import asyncio

        async def fetch_with_timeout(url, timeout=5.0):
            """Fetch URL with timeout handling."""
            try:
                return await asyncio.wait_for(
                    fetch(url),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                logger.error(f"Timeout fetching {url}")
                return None

        # ❌ BAD: Incomplete, no context
        await asyncio.wait_for(fetch(url), 5)
```

---

## Multiline Strings

### Use Literal Block Scalar (|)

```yaml
problem: |
      This is a multiline string.
      Preserves newlines.
      Good for code examples.
```

### Use Folded Block Scalar (>)

```yaml
explanation: >
      This is a folded string.
      Newlines become spaces.
      Good for paragraphs.
```

---

## Tags

### Purpose
Improve discoverability through search

### Guidelines

**✅ Good tags:**
- Specific: `["async", "timeout", "fastapi"]`
- Relevant: Match entry content
- Lowercase: Consistency
- Hyphenated: `["error-handling", "type-hints"]`

**❌ Bad tags:**
- Too vague: `["error", "problem"]`
- Too generic: `["code", "programming"]`
- Mixed case: `["Async", "Timeout"]`
- Spaces: `["error handling"]`

### Tag Examples

**Python async entry:**
```yaml
tags: ["async", "await", "event-loop", "coroutine", "timeout"]
```

**Docker entry:**
```yaml
tags: ["docker", "permissions", "volumes", "containers"]
```

**Testing entry:**
```yaml
tags: ["pytest", "testing", "fixtures", "assertions"]
```

---

## Quality Requirements

### Minimum Quality Score: 75/100

**Breakdown:**
- Completeness (40 points): All required fields
- Accuracy (30 points): Tested, correct solutions
- Usability (20 points): Clear, actionable
- Maintainability (10 points): Up-to-date, fresh

**Validation:**
```bash
python tools/kb.py validate <file>
python tools/kb.py check-quality <file>
```

---

## Common YAML Issues

### Issue: Indentation Errors

**❌ WRONG:**
```yaml
errors:
- id: "ERROR-001"  # Missing indentation
  title: "Error"
```

**✅ CORRECT:**
```yaml
errors:
  - id: "ERROR-001"  # Proper indentation (2 spaces)
    title: "Error"
```

---

### Issue: Missing Quotation Marks

**❌ WRONG:**
```yaml
tags: [async, timeout]  # Missing quotes
```

**✅ CORRECT:**
```yaml
tags: ["async", "timeout"]  # Proper quotes
```

---

### Issue: Invalid Multiline Strings

**❌ WRONG:**
```yaml
problem: This is a long string that should
use multiline syntax but doesn't
```

**✅ CORRECT:**
```yaml
problem: |
  This is a long string that
  properly uses multiline syntax
```

---

## Validation Checklist

Before committing:

- [ ] All required fields present
- [ ] ID format correct (CATEGORY-NNN)
- [ ] Severity level appropriate
- [ ] Scope correctly identified
- [ ] Code examples tested
- [ ] YAML syntax valid
- [ ] Tags relevant and formatted
- [ ] Quality score ≥ 75/100
- [ ] No duplicate IDs
- [ ] Last updated date current

---

## Related

- `@standards/quality-gates.md` - Quality requirements
- `@standards/git-workflow.md` - Commit standards
- `@references/cli-reference.md` - Validation commands

---

**Version:** 1.0
**Last Updated:** 2026-01-07
