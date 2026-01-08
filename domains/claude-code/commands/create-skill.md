# Create Skill

Interactive skill creation with auto-activation via skill-rules.json.

## Usage
```
/create-skill [options]
```

## Quick Examples

### Interactive Creation
```
/create-skill
```
Guides through all required fields.

### Quick Skill with Options
```
/create-skill --name "my-skill" --type domain --priority high
```
Generates template with pre-filled fields.

### From Prompt
```
/create-skill --prompt "Create a skill for FastAPI development"
```
Infers configuration from prompt.

## What This Command Does

1. **Gathers requirements** - Skill name, purpose, domain
2. **Creates directory structure** - SKILL.md + resources/
3. **Generates YAML frontmatter** - With metadata
4. **Creates skill-rules.json entry** - For auto-activation
5. **Generates templates** - SKILL.md and resource files
6. **Provides testing guide** - How to test activation

**📘 Complete Guide:** `@skills/skill-development/SKILL.md`

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `--name <name>` | Skill name | `--name "python-async"` |
| `--type <type>` | Skill type | `--type domain\|technical\|workflow` |
| `--priority <prio>` | Priority level | `--priority high` |
| `--description <desc>` | Skill description | `--description "Async patterns"` |
| `--prompt <text>` | Infer from prompt | `--prompt "Create React skill"` |
| `--with-resources` | Create resources/ | `--with-resources` |
| `--force` | Overwrite existing | `--force` |

## Workflow

### Step 1: Define Skill Purpose

Claude will ask:
1. **What is the skill name?** (e.g., "python-async")
2. **What does this skill do?** (1-2 sentences)
3. **Who will use this skill?** (e.g., "Python developers")
4. **When should it activate?** (keywords, patterns)

### Step 2: Choose Type and Priority

**Skill types:**
- `domain` - Domain-specific (python, docker, postgresql)
- `technical` - Technical skills (async, testing, api-design)
- `workflow` - Workflow skills (git-workflow, code-review)
- `utility` - Utility skills (kb-search, formatting)

**Priority levels:**
- `critical` - Always suggest (python-development, git-workflow)
- `high` - Strongly suggest (docker, postgresql)
- `medium` - Suggest for relevant (async, testing)
- `low` - Only if highly relevant (kb-search)

### Step 3: Generate Structure

Creates:
```
.claude/skills/<skill-name>/
├── SKILL.md
└── resources/
    ├── topic-1.md
    ├── topic-2.md
    └── topic-3.md
```

### Step 4: Configure Auto-Activation

Adds entry to `.claude/skill-rules.json`:
```json
{
  "<skill-name>": {
    "type": "domain",
    "priority": "high",
    "description": "<description>",
    "promptTriggers": {
      "keywords": ["keyword1", "keyword2"],
      "intentPatterns": ["(create|add).*?pattern"],
      "fileTriggers": {
        "pathPatterns": ["**/*.py"],
        "contentPatterns": ["import asyncio"]
      }
    }
  }
}
```

### Step 5: Create Templates

**SKILL.md template:**
```yaml
---
name: "skill-name"
description: "Brief description"
version: "1.0"
author: "Your name"
tags: ["tag1", "tag2", "tag3"]
resources:
  - "resources/topic-1.md"
  - "resources/topic-2.md"
related:
  - "@other-skill/SKILL.md"
---

# Skill Name

Brief description.

## Quick Start

Essential commands and patterns.

## Core Concepts

Main concepts and explanations.

## Common Tasks

Frequently used workflows.

## Examples

Real-world examples.

**📘 Detailed:** `@resources/topic-1.md`
```

### Step 6: Test Activation

1. Restart Claude Code
2. Submit prompt with keyword
3. Verify skill suggested
4. Test skill activation
5. Validate resources load

## Output

### Success

```
✅ Skill created: python-async
📁 Location: .claude/skills/python-async/
📄 Files:
   - SKILL.md (280 lines)
   - resources/async-patterns.md (400 lines)
   - resources/error-handling.md (350 lines)
✅ skill-rules.json updated
🔄 Next: Restart Claude Code and test activation

Test with: "Help with async code in Python"
```

### Already Exists

```
⚠️  Skill already exists: python-async
💡 Use --force to overwrite
```

## Examples

### Example 1: Domain Skill

```
/create-skill --name "python-async" --type domain --priority high
```

Creates Python async programming skill with:
- Keywords: python, async, await, coroutine
- File triggers: **/*.py with "import asyncio"
- Resources: async-patterns.md, error-handling.md, testing.md

### Example 2: Technical Skill

```
/create-skill --name "docker-optimization" --type technical --priority medium
```

Creates Docker optimization skill with:
- Keywords: docker, optimize, image, multi-stage
- File triggers: Dockerfile, docker-compose.yml
- Resources: multi-stage-builds.md, caching.md, best-practices.md

### Example 3: Workflow Skill

```
/create-skill --name "code-review" --type workflow --priority high
```

Creates code review workflow skill with:
- Keywords: review, refactor, improve, optimize
- No file triggers (workflow skill)
- Resources: review-checklist.md, patterns.md, examples.md

## Best Practices

### 1. Skill Naming

**DO:**
- Use lowercase with hyphens: `python-async`
- Be descriptive: `docker-optimization`
- Match domain: `python-testing`

**DON'T:**
- Use uppercase: `Python-Async`
- Use underscores: `python_async`
- Be vague: `helper`, `tool`

### 2. Type Selection

**domain** - For language/framework skills
**technical** - For specific techniques/patterns
**workflow** - For processes/workflows
**utility** - For helper utilities

### 3. Priority Assignment

**critical** - Essential skills (python-development)
**high** - Important domains (docker, postgresql)
**medium** - Specific techniques (async, testing)
**low** - Utilities (kb-search)

### 4. Keywords

**Choose 5-10 relevant keywords:**
- Domain-specific: python, docker, react
- Technology-specific: async, await, hooks
- Task-specific: testing, debugging, refactor

**Avoid generic keywords:** code, file, help, tool

## Claude's Role

When using this command, Claude will:

1. **Ask for skill details** (if not provided)
2. **Suggest type and priority** based on description
3. **Generate appropriate keywords** from domain/technology
4. **Create directory structure** with SKILL.md and resources/
5. **Generate YAML frontmatter** with proper metadata
6. **Create skill-rules.json entry** with triggers
7. **Provide next steps** for testing

## Testing Guide

After skill creation:

1. **Restart Claude Code** (reload configuration)

2. **Test keyword activation:**
   ```
   Prompt: "Help with <keyword>"
   Expected: Skill suggested
   ```

3. **Test file activation** (if configured):
   ```
   Open: <matching file>
   Prompt: "Add feature"
   Expected: Skill suggested
   ```

4. **Test skill loading:**
   ```
   Accept suggestion
   Verify: SKILL.md loads
   Click: @resources link
   Verify: Resource loads
   ```

5. **Test in real scenario:**
   ```
   Use skill for actual task
   Verify: Content helpful
   Note: Improvements needed
   ```

## Related

- `@skills/skill-development/SKILL.md` - Complete skill development guide
- `@skills/skill-development/resources/skill-rules-schema.md` - skill-rules.json schema
- `@skills/skill-development/resources/yaml-frontmatter.md` - YAML frontmatter format
- `@skills/claude-code-architecture/SKILL.md` - Claude Code architecture

## Troubleshooting

### Skill Not Activating

**Check:**
1. ✅ skill-rules.json exists?
2. ✅ JSON syntax valid?
3. ✅ Skill name matches?
4. ✅ Keywords in prompt?
5. ✅ Claude Code restarted?

**Fix:** Restart Claude Code after creating skill

### YAML Frontmatter Not Recognized

**Check:**
1. ✅ Starts with `---`?
2. ✅ Ends with `---`?
3. ✅ Valid YAML syntax?

**Fix:** Ensure proper YAML format

### Resources Not Loading

**Check:**
1. ✅ Resource files exist?
2. ✅ Listed in YAML frontmatter?
3. ✅ File paths correct?

**Fix:** Verify resource paths in YAML frontmatter

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** skill-development skill
