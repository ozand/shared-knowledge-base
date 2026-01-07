# YAML Frontmatter

Complete guide to YAML frontmatter for Claude Code skills.

---

## Overview

**Purpose:** Metadata at startup for discoverability and on-demand loading

**Location:** Top of SKILL.md files

**Token cost:** ~50 tokens at session start

**Benefits:**
- Discoverability (search, filter)
- Token efficiency (metadata only at startup)
- Resource linking (on-demand loading)
- Auto-activation (skill-rules.json integration)

---

## Schema

### Required Fields

```yaml
---
name: "skill-name"
description: "Brief description (1-2 sentences)"
version: "1.0"
---
```

### Optional Fields

```yaml
---
author: "Author name"
tags: ["tag1", "tag2", "tag3"]
resources:
  - "resources/detailed-topic.md"
  - "resources/another-topic.md"
related:
  - "@other-skill/SKILL.md"
  - "@standards/some-standard.md"
---
```

---

## Field Definitions

### name (required)

**Purpose:** Unique identifier for the skill

**Format:**
- Lowercase
- Hyphens for spaces
- Matches directory name
- Descriptive

**Examples:**
```yaml
---
name: "python-development"
name: "async-programming"
name: "docker-development"
name: "git-workflow"
---
```

**Best practices:**
- Use domain name: `python-development`, `docker`
- Use technology name: `async-programming`, `react`
- Use activity name: `git-workflow`, `code-review`
- Avoid generic names: `development`, `helper`

---

### description (required)

**Purpose:** Brief description of what the skill does

**Format:**
- 1-2 sentences
- What skill does
- Who it's for
- No markdown formatting

**Examples:**
```yaml
---
description: "Python development patterns, best practices, and common workflows"
description: "Async/await patterns, coroutines, and event loops"
description: "Docker containers, images, compose, and deployment"
description: "Git workflow conventions and best practices"
---
```

**Best practices:**
- Start with domain/technology
- Include what user will learn
- Keep concise (1-2 sentences)
- No "This skill provides..."
- Avoid: "A comprehensive guide to..."

---

### version (required)

**Purpose:** Version number for the skill

**Format:**
- Semantic versioning: `1.0`, `1.1`, `2.0`
- Or simple: `1.0`

**Examples:**
```yaml
---
version: "1.0"
version: "2.1"
version: "3.0-beta"
---
```

**Best practices:**
- Start with `1.0`
- Increment minor for updates: `1.0` → `1.1`
- Increment major for rewrites: `1.0` → `2.0`
- Use suffix for pre-releases: `1.0-beta`, `2.0-rc1`

---

### author (optional)

**Purpose:** Credit the skill author

**Format:**
- Author name or handle
- No markdown formatting

**Examples:**
```yaml
---
author: "Shared KB Curator"
author: "John Doe"
author: "@username"
---
```

**Best practices:**
- Use consistent name across skills
- Use team name for shared skills
- Use personal name for personal skills
- Include contact info optionally: `"John Doe (john@example.com)"`

---

### tags (optional)

**Purpose:** Discoverability and categorization

**Format:**
- Array of strings
- Lowercase
- 5-7 tags
- No spaces (use hyphens)

**Examples:**
```yaml
---
tags: ["python", "development", "patterns"]
tags: ["async", "await", "coroutine", "asyncio"]
tags: ["docker", "containers", "devops"]
tags: ["git", "workflow", "commit", "branch"]
---
```

**Best practices:**
- Include domain: `python`, `docker`, `git`
- Include technology: `async`, `react`, `fastapi`
- Include concepts: `testing`, `debugging`, `refactoring`
- Use specific tags: `async-programming`, not `async`
- Avoid generic tags: `code`, `development`, `help`

**Tag types:**
1. **Domain:** `python`, `docker`, `javascript`
2. **Technology:** `async`, `react`, `fastapi`
3. **Concept:** `testing`, `debugging`, `refactoring`
4. **Activity:** `git-workflow`, `code-review`

---

### resources (optional)

**Purpose:** List of resource files for on-demand loading

**Format:**
- Array of strings
- Relative paths
- Order by importance

**Examples:**
```yaml
---
resources:
  - "resources/async-patterns.md"
  - "resources/testing.md"
  - "resources/error-handling.md"
---
```

**Best practices:**
- List all resource files
- Order by importance
- Use relative paths from skill directory
- Keep in sync with actual files
- Remove if no resources (but why no resources?)

---

### related (optional)

**Purpose:** Link to related skills, standards, references

**Format:**
- Array of @ references
- Use @ syntax for internal links

**Examples:**
```yaml
---
related:
  - "@skills/claude-code-architecture/SKILL.md"
  - "@standards/yaml-standards.md"
  - "@resources/skill-activation.md"
---
```

**Best practices:**
- Link to related skills
- Link to relevant standards
- Link to useful references
- Use @ syntax (not markdown links)
- Keep list short (3-5 links)

---

## Complete Examples

### Example 1: Domain Skill

```yaml
---
name: "python-development"
description: "Python development patterns, best practices, and common workflows"
version: "1.0"
author: "Shared KB Curator"
tags: ["python", "development", "patterns", "best-practices"]
resources:
  - "resources/async-patterns.md"
  - "resources/testing.md"
  - "resources/error-handling.md"
  - "resources/decorators.md"
  - "resources/type-hints.md"
related:
  - "@skills/async-programming/SKILL.md"
  - "@skills/python-testing/SKILL.md"
  - "@standards/yaml-standards.md"
---
```

---

### Example 2: Technical Skill

```yaml
---
name: "async-programming"
description: "Async/await patterns, coroutines, event loops, and concurrent programming"
version: "1.0"
author: "Shared KB Curator"
tags: ["async", "await", "coroutine", "asyncio", "concurrency"]
resources:
  - "resources/async-patterns.md"
  - "resources/error-handling.md"
  - "resources/testing.md"
related:
  - "@skills/python-development/SKILL.md"
  - "@skills/testing/SKILL.md"
---
```

---

### Example 3: Workflow Skill

```yaml
---
name: "git-workflow"
description: "Git workflow conventions, commit patterns, and branching strategies"
version: "1.0"
author: "Shared KB Curator"
tags: ["git", "workflow", "commit", "branch", "merge"]
resources:
  - "resources/commit-patterns.md"
  - "resources/branching.md"
  - "resources/code-review.md"
related:
  - "@standards/git-workflow.md"
---
```

---

### Example 4: Minimal Skill

```yaml
---
name: "kb-search"
description: "Search the Shared Knowledge Base for error solutions and patterns"
version: "1.0"
tags: ["search", "kb", "query", "lookup"]
---
```

---

## Integration with skill-rules.json

### Matching Names

**Important:** Skill name must match exactly

**skill-rules.json:**
```json
{
  "python-development": {
    "type": "domain",
    "priority": "high",
    "description": "Python development patterns"
  }
}
```

**YAML frontmatter:**
```yaml
---
name: "python-development"  # ← Must match
---
```

**Directory name:**
```
.claude/skills/python-development/  # ← Must match
```

---

## Token Efficiency

### Metadata-Only Loading

**At session start:**
```yaml
---
name: "python-development"
description: "Python development patterns"
version: "1.0"
tags: ["python", "development"]
resources:
  - "resources/async.md"
---
```
**Token cost:** ~50 tokens

**On-demand (when skill activated):**
- Full SKILL.md: ~2,000 tokens
- Resources: ~3,000 tokens each

**Savings:** 98% at session start (50 vs 2,000+ tokens)

---

## Best Practices

### 1. Naming

**DO:**
- Use lowercase
- Hyphens for spaces
- Descriptive names
- Match directory name

**DON'T:**
- Use uppercase: `Python-Development`
- Use underscores: `python_development`
- Use generic names: `helper`, `tool`
- Mismatch directory name

---

### 2. Description

**DO:**
- 1-2 sentences
- Start with domain/technology
- Describe what user learns
- Keep concise

**DON'T:**
- Write paragraphs
- Start with "This skill..."
- Be vague: "A helpful skill"
- Use markdown: `**bold**`, `*italic*`

---

### 3. Tags

**DO:**
- 5-7 relevant tags
- Lowercase
- Domain, technology, concepts
- Use hyphens for multi-word: `async-programming`

**DON'T:**
- Too many tags (>10)
- Too few tags (<3)
- Generic tags: `code`, `development`
- Uppercase: `Python`, `Async`

---

### 4. Resources

**DO:**
- List all resource files
- Order by importance
- Relative paths
- Keep in sync

**DON'T:**
- Forget to update list
- Use absolute paths
- List non-existent files
- Order randomly

---

## Quality Checklist

**Before releasing:**

- [ ] name matches directory name
- [ ] name is lowercase with hyphens
- [ ] description is 1-2 sentences
- [ ] description starts with domain/technology
- [ ] version is set
- [ ] tags are 5-7 relevant keywords
- [ ] tags are lowercase
- [ ] resources list matches actual files
- [ ] related links use @ syntax
- [ ] No markdown formatting in fields
- [ ] No YAML syntax errors

**Test YAML syntax:**
```bash
# Parse YAML (if yq available)
yq eval '.' .claude/skills/my-skill/SKILL.md

# Or validate manually
# YAML frontmatter must be valid YAML
```

---

## Troubleshooting

### Issue: YAML Not Recognized

**Symptoms:** Frontmatter not parsed

**Check:**
1. Starts with `---`?
2. Ends with `---`?
3. Valid YAML syntax?
4. No extra spaces?

**Fix:**
```yaml
---  # Must start with ---
name: "skill-name"
description: "Description"
version: "1.0"
---  # Must end with ---
```

---

### Issue: Name Mismatch

**Symptoms:** Skill not activating

**Check:**
```bash
# Directory name
ls .claude/skills/

# YAML frontmatter
grep "name:" .claude/skills/my-skill/SKILL.md

# skill-rules.json
grep "my-skill" .claude/skill-rules.json
```

**Fix:** Ensure all three match exactly

---

### Issue: Invalid YAML

**Symptoms:** Parse errors

**Common errors:**
- Missing quotes: `name: python-development` ❌
- Extra spaces: `name:  "python-development"` ❌
- Missing colon: `name "python-development"` ❌

**Fix:**
```yaml
name: "python-development"  # ✅ Correct
```

---

## Related Resources

**Internal:**
- `@resources/500-line-rule.md` - Modular skill pattern
- `@resources/skill-rules-schema.md` - skill-rules.json schema
- `@resources/testing-guide.md` - Testing skills

**Related Skills:**
- `@skills/claude-code-architecture/SKILL.md` - System overview

**Shared KB:**
- `universal/patterns/claude-code-files-organization-001.yaml` - Organization guide

---

**Version:** 1.0
**Last Updated:** 2026-01-07
