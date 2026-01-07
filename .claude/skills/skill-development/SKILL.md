---
name: "skill-development"
description: "Expert in creating Claude Code skills with auto-activation via skill-rules.json. Complete workflow from design to testing."
version: "1.0"
author: "Claude Code Expert"
tags: ["skills", "skill-rules", "auto-activation", "yaml", "development"]
resources:
  - "resources/skill-rules-schema.md"
  - "resources/500-line-rule.md"
  - "resources/yaml-frontmatter.md"
  - "resources/testing-guide.md"
  - "resources/troubleshooting.md"
related:
  - "@skills/claude-code-architecture/SKILL.md"
  - "@resources/claude-code-architecture/resources/skill-activation.md"
  - "@standards/yaml-standards.md"
---

# Skill Development

Complete guide to creating production-ready Claude Code skills with auto-activation.

---

## Quick Start

### Create a Skill in 5 Steps

```bash
# 1. Create skill directory
mkdir -p .claude/skills/my-skill/resources

# 2. Create SKILL.md with YAML frontmatter
# (see template below)

# 3. Add skill-rules.json entry
# (for auto-activation)

# 4. Test activation
# (trigger with keyword)

# 5. Integrate into project
```

**📘 Complete Workflow:** `@resources/skill-rules-schema.md`

---

## Skill Creation Workflow

### Step 1: Define Purpose (5 min)

**Ask yourself:**
1. What problem does this skill solve?
2. Who will use this skill?
3. What should Claude know when using this skill?
4. When should this skill auto-activate?

**Example:**
```
Purpose: Help developers write async/await code in Python

Users: Python developers working with async code

Claude should know:
- Async/await syntax
- Common async patterns
- Error handling in async code
- Testing async code

Auto-activate when:
- Keywords: "async", "await", "coroutine", "asyncio"
- File patterns: **/*.py with "import asyncio"
```

**📘 skill-rules.json Schema:** `@resources/skill-rules-schema.md`

---

### Step 2: Design Structure (10 min)

**Apply 500-line rule:**
- SKILL.md: 300-500 lines (core content)
- resources/: Detailed content (400-500 lines each)

**Structure template:**
```
my-skill/
├── SKILL.md (300-500 lines)
│   ├── Quick start (50 lines)
│   ├── Core concepts (100 lines)
│   ├── Common tasks (100 lines)
│   ├── Examples (50 lines)
│   └── Links to resources (10 lines)
│
└── resources/
    ├── detailed-topic-1.md (400 lines)
    ├── detailed-topic-2.md (450 lines)
    └── detailed-topic-3.md (380 lines)
```

**Content distribution:**
- **SKILL.md:** What users need 80% of the time
- **resources/:** What users need 20% of the time (details, edge cases)

**📘 500-Line Rule:** `@resources/500-line-rule.md`

---

### Step 3: Create SKILL.md (30-60 min)

**YAML Frontmatter (required):**
```yaml
---
name: "my-skill"
description: "Brief description (1-2 sentences)"
version: "1.0"
author: "Your name"
tags: ["tag1", "tag2", "tag3"]
resources:
  - "resources/detailed-topic.md"
related:
  - "@other-skill/SKILL.md"
---
```

**SKILL.md Structure:**
```markdown
# Skill Name

Brief description (1-2 sentences).

## Quick Start

### Essential Commands/P patterns

## Core Concepts

### Concept 1
Explanation with example

### Concept 2
Explanation with example

## Common Tasks

### Task 1
Step-by-step guide

### Task 2
Step-by-step guide

## Examples

### Example 1
Real-world example

## Links

**📘 Detailed:** `@resources/detailed-topic.md`
**📘 Related:** `@other-skill/SKILL.md`
```

**Best Practices:**
- Start with quick start (what users need most)
- Focus on 80/20 rule (80% of use cases)
- Provide examples for every concept
- Link to detailed content
- Keep sections concise

**📘 YAML Frontmatter Guide:** `@resources/yaml-frontmatter.md`

---

### Step 4: Create Resources (30-60 min)

**When to create resources:**
- SKILL.md exceeds 500 lines
- Topic needs detailed explanation
- Multiple examples needed
- Reference documentation needed

**Resource structure:**
```markdown
# Detailed Topic

## In-Depth Explanation

Complete explanation (200-300 lines)

## Examples

### Example 1
Full example with context

### Example 2
Full example with context

## Edge Cases

Common edge cases and solutions

## Reference

Comprehensive reference (100-150 lines)
```

**Naming conventions:**
- Use lowercase with hyphens: `async-patterns.md`
- Descriptive names: `error-handling.md`, not `details.md`
- Group related content: `testing.md`, `advanced-testing.md`

---

### Step 5: Add skill-rules.json Entry (10 min)

**Location:** `.claude/skill-rules.json`

**Entry structure:**
```json
{
  "my-skill": {
    "type": "domain|technical|workflow|utility",
    "priority": "critical|high|medium|low",
    "description": "Brief description",
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

**Key fields:**
- **type** - Skill category (domain, technical, workflow, utility)
- **priority** - Suggestion priority (critical, high, medium, low)
- **keywords** - Simple word matching (5-10 keywords)
- **intentPatterns** - Regex patterns for intent (2-5 patterns)
- **fileTriggers** - File-based triggers (optional)

**📘 Complete Schema:** `@resources/skill-rules-schema.md`

---

### Step 6: Test Activation (10 min)

**Testing checklist:**
1. ✅ skill-rules.json valid JSON?
2. ✅ Skill name matches exactly?
3. ✅ Keywords trigger suggestion?
4. ✅ Intent patterns work?
5. ✅ File triggers work (if used)?
6. ✅ SKILL.md loads correctly?
7. ✅ Resources load correctly?

**Test prompts:**
```
# Test keyword matching
"Help me with async code in Python"

# Test intent pattern
"Create an async function"

# Test file trigger
# (open a .py file with "import asyncio")
"How do I add error handling?"
```

**Expected result:**
```
Based on your request, consider using:
• python-async: Async/await patterns and best practices
```

**📘 Testing Guide:** `@resources/testing-guide.md`

---

## skill-rules.json Schema

### Complete Schema

```json
{
  "skill-name": {
    "type": "domain|technical|workflow|utility",
    "enforcement": "suggest|require|optional",
    "priority": "critical|high|medium|low",
    "description": "Brief description (1-2 sentences)",

    "promptTriggers": {
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "intentPatterns": [
        "regex-pattern-1",
        "regex-pattern-2"
      ],
      "fileTriggers": {
        "pathPatterns": ["**/*.py", "src/**/*.ts"],
        "contentPatterns": ["import asyncio", "useState"]
      }
    },

    "context": {
      "requires": ["other-skill"],
      "incompatibleWith": ["conflicting-skill"],
      "fileTypes": ["*.py", "*.ts"],
      "languages": ["python", "typescript"]
    },

    "activation": {
      "autoLoad": false,
      "userConfirmation": true,
      "priorityBoost": 0
    }
  }
}
```

### Field Definitions

**type** (required)
- `domain` - Domain-specific (python, docker, postgresql)
- `technical` - Technical skills (async, testing, api-design)
- `workflow` - Workflow skills (git-workflow, code-review)
- `utility` - Utility skills (kb-search, formatting)

**priority** (required)
- `critical` - Essential skills (python-development, git-workflow)
- `high` - Important domain skills (docker, postgresql)
- `medium` - Technical skills (async, testing)
- `low` - Utility skills (kb-search, formatting)

**keywords** (required)
- 5-10 relevant keywords
- Case-insensitive
- Specific to domain

**intentPatterns** (optional)
- 2-5 regex patterns
- Test with regex101.com
- Use non-capturing groups: `(?:pattern)`

**fileTriggers** (optional)
- `pathPatterns` - Glob patterns for file paths
- `contentPatterns` - Regex for file content

**📘 Complete Schema:** `@resources/skill-rules-schema.md`

---

## 500-Line Rule

### What and Why

**Rule:** SKILL.md files should be <500 lines

**Why:**
1. **Token efficiency** - Load metadata first, content on-demand
2. **Maintainability** - Smaller files easier to maintain
3. **Focus** - Forces prioritization of important content
4. **Organization** - Better structure with resources/

### How to Apply

**Measure:**
```bash
wc -l .claude/skills/my-skill/SKILL.md
```

**If >500 lines:**
1. Identify large sections (>100 lines)
2. Move to resources/
3. Add link to resource
4. Add YAML frontmatter resource entry

**Example:**
```markdown
# SKILL.md (before: 650 lines)

## Async Patterns (400 lines) ⚠️ Too large
Detailed async patterns...
```

```markdown
# SKILL.md (after: 280 lines)

## Async Patterns
Quick overview of async patterns...

**📘 Complete Patterns:** `@resources/async-patterns.md`
```

**resources/async-patterns.md (400 lines)**
```markdown
# Async Patterns

Complete async patterns...
```

**📘 500-Line Rule Guide:** `@resources/500-line-rule.md`

---

## YAML Frontmatter

### Purpose

Two purposes:
1. **Metadata** - Skill discoverability at startup (~50 tokens)
2. **Resource list** - On-demand loading links

### Schema

**Required fields:**
```yaml
---
name: "skill-name"
description: "Brief description (1-2 sentences)"
version: "1.0"
---
```

**Optional fields:**
```yaml
---
author: "Author name"
tags: ["tag1", "tag2", "tag3"]
resources:
  - "resources/topic.md"
related:
  - "@other-skill/SKILL.md"
---
```

### Best Practices

**name:**
- Matches directory name
- Lowercase with hyphens
- Descriptive

**description:**
- 1-2 sentences
- What skill does
- Who it's for

**tags:**
- 5-7 relevant tags
- Lowercase
- Include domain, technology

**resources:**
- List all resource files
- Relative paths
- Order by importance

**📘 Complete Guide:** `@resources/yaml-frontmatter.md`

---

## Testing Skills

### Manual Testing

**Test 1: Keyword activation**
```
Prompt: "Help with async code"
Expected: Skill suggested
```

**Test 2: Intent pattern**
```
Prompt: "Create async function"
Expected: Skill suggested
```

**Test 3: File trigger**
```
File: test.py with "import asyncio"
Prompt: "Add error handling"
Expected: Skill suggested
```

**Test 4: Resource loading**
```
Click link: @resources/async-patterns.md
Expected: Resource file loads
```

### Automated Testing

**Test script:**
```python
# test_skill_activation.py

import json
import re

def test_skill_rules():
    with open('.claude/skill-rules.json') as f:
        rules = json.load(f)

    test_cases = [
        {
            "prompt": "Create async function",
            "expected": ["python-async"]
        }
    ]

    for test in test_cases:
        skills = match_skills(test["prompt"], rules)
        assert set(skills) >= set(test["expected"])

def match_skills(prompt, rules):
    matched = []
    for name, rule in rules.items():
        for keyword in rule["promptTriggers"]["keywords"]:
            if keyword.lower() in prompt.lower():
                matched.append(name)
                break
    return matched

if __name__ == "__main__":
    test_skill_rules()
    print("✅ All tests passed")
```

**📘 Complete Testing Guide:** `@resources/testing-guide.md`

---

## Common Patterns

### Pattern 1: Domain Skill

**Example: python-development**

```yaml
---
name: "python-development"
description: "Python development patterns, best practices, and common workflows"
tags: ["python", "development", "patterns"]
resources:
  - "resources/async.md"
  - "resources/testing.md"
  - "resources/decorators.md"
---
```

```json
{
  "python-development": {
    "type": "domain",
    "priority": "high",
    "promptTriggers": {
      "keywords": ["python", "py", "django", "flask"],
      "fileTriggers": {
        "pathPatterns": ["**/*.py"]
      }
    }
  }
}
```

### Pattern 2: Technical Skill

**Example: async-programming**

```yaml
---
name: "async-programming"
description: "Async/await patterns, coroutines, event loops"
tags: ["async", "await", "coroutine", "asyncio"]
resources:
  - "resources/async-patterns.md"
  - "resources/error-handling.md"
---
```

```json
{
  "async-programming": {
    "type": "technical",
    "priority": "medium",
    "promptTriggers": {
      "keywords": ["async", "await", "coroutine"],
      "intentPatterns": ["(create|make).*?async.*?(function|method)"],
      "fileTriggers": {
        "contentPatterns": ["import asyncio", "async def"]
      }
    }
  }
}
```

### Pattern 3: Workflow Skill

**Example: git-workflow**

```yaml
---
name: "git-workflow"
description: "Git workflow conventions and best practices"
tags: ["git", "workflow", "commit", "branch"]
resources:
  - "resources/commit-patterns.md"
  - "resources/branching.md"
---
```

```json
{
  "git-workflow": {
    "type": "workflow",
    "priority": "high",
    "promptTriggers": {
      "keywords": ["git", "commit", "branch", "merge"],
      "intentPatterns": ["(commit|push|merge).*?changes"]
    }
  }
}
```

---

## Best Practices

### 1. Skill Design

**DO:**
- Focus on specific domain/problem
- Keep scope narrow
- Target 80% of use cases
- Provide examples
- Link to detailed content

**DON'T:**
- Create overly broad skills
- Mix multiple domains
- Include edge cases in SKILL.md
- Forget examples
- Duplicate content

### 2. skill-rules.json

**DO:**
- Use 5-10 specific keywords
- Test regex patterns thoroughly
- Set appropriate priority
- Use file triggers for domain skills
- Match skill name exactly

**DON'T:**
- Use generic keywords ("code", "file")
- Create overly complex regex
- Make everything high priority
- Forget to test file triggers
- Misspell skill names

### 3. File Organization

**DO:**
- Keep SKILL.md <500 lines
- Move details to resources/
- Add YAML frontmatter
- Use descriptive names
- Link with @ syntax

**DON'T:**
- Let SKILL.md grow beyond 500 lines
- Put everything in one file
- Forget YAML frontmatter
- Use vague names
- Duplicate content

### 4. Testing

**DO:**
- Test keyword matching
- Test intent patterns
- Test file triggers
- Test resource loading
- Test with real prompts

**DON'T:**
- Skip testing
- Assume it works
- Test only one scenario
- Forget edge cases
- Release without validation

---

## Quality Checklist

**Before releasing:**

- [ ] Skill purpose clearly defined
- [ ] SKILL.md <500 lines
- [ ] YAML frontmatter complete
- [ ] skill-rules.json entry added
- [ ] Keywords tested
- [ ] Intent patterns tested
- [ ] File triggers tested (if used)
- [ ] Resources load correctly
- [ ] Links work
- [ ] Tested with real prompts
- [ ] Token efficiency verified

**📘 Troubleshooting:** `@resources/troubleshooting.md`

---

## Troubleshooting

### Skill Not Activating

**Checklist:**
1. ✅ skill-rules.json exists?
2. ✅ JSON syntax valid? (`jq . skill-rules.json`)
3. ✅ Skill name matches exactly?
4. ✅ Keywords in prompt?
5. ✅ Hook registered?

**Common fixes:**
- Add more keywords
- Fix JSON syntax
- Match skill name (SKILL.md ↔ skill-rules.json)
- Register UserPromptSubmit hook

### SKILL.md Too Large

**Solutions:**
1. Identify large sections (>100 lines)
2. Move to resources/
3. Add links
4. Apply progressive disclosure

### Links Not Working

**Solutions:**
1. Verify file paths
2. Use @ syntax
3. Check file extensions
4. Test links

**📘 Complete Guide:** `@resources/troubleshooting.md`

---

## Related Resources

**Internal:**
- `@resources/skill-rules-schema.md` - Complete JSON schema
- `@resources/500-line-rule.md` - Modular skill pattern
- `@resources/yaml-frontmatter.md` - Frontmatter examples
- `@resources/testing-guide.md` - How to test skills
- `@resources/troubleshooting.md` - Common issues and fixes

**Related Skills:**
- `@skills/claude-code-architecture/SKILL.md` - System overview
- `@claude-code-architecture/resources/skill-activation.md` - Auto-activation deep dive

**Shared KB:**
- `universal/patterns/claude-code-files-organization-001.yaml` - Organization guide

**External:**
- [Claude Code Documentation](https://claude.com/claude-code)
- [Regex Testing](https://regex101.com/)

---

## Example Skills

**Production examples from diet103 showcase:**
- python-development (325 lines + 3 resources)
- async-programming (280 lines + 2 resources)
- docker-development (295 lines + 2 resources)
- fastapi-development (310 lines + 3 resources)

**Each follows:**
- 500-line rule
- YAML frontmatter
- skill-rules.json entry
- Progressive disclosure
- Auto-activation

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** diet103 Claude Code Infrastructure Showcase
**Quality Score:** 95/100
