# Skill Activation System

Complete guide to the auto-activation system - BREAKTHROUGH pattern from production.

---

## Overview

**What is Auto-Activation?**

Auto-activation is the ability for skills to suggest themselves based on user intent, without manual selection.

**How it works:**

1. **skill-rules.json** - Defines trigger patterns for each skill
2. **UserPromptSubmit hook** - Analyzes user prompt
3. **Pattern matching** - Finds relevant skills
4. **Priority system** - Ranks skills by importance
5. **Suggestion format** - "Based on your request, consider using: X, Y, Z"

**Key Benefit:** Skills become context-aware and proactive, not reactive.

---

## skill-rules.json Schema

### Complete Schema

```json
{
  "skill-name": {
    "type": "domain|technical|workflow|utility",
    "enforcement": "suggest|require|optional",
    "priority": "critical|high|medium|low",
    "description": "Brief description of the skill",

    "promptTriggers": {
      "keywords": [
        "keyword1",
        "keyword2",
        "keyword3"
      ],

      "intentPatterns": [
        "regex-pattern-1",
        "regex-pattern-2"
      ],

      "fileTriggers": {
        "pathPatterns": [
          "**/*.py",
          "src/**/*.ts"
        ],

        "contentPatterns": [
          "import asyncio",
          "from fastapi",
          "useState"
        ]
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

**1. type** (required)
- `domain` - Domain-specific skills (python, docker, postgresql)
- `technical` - Technical skills (async, testing, api-design)
- `workflow` - Workflow skills (git-workflow, code-review)
- `utility` - Utility skills (kb-search, kb-validate)

**2. enforcement** (optional, default: "suggest")
- `suggest` - Suggest to user, user can decline
- `require` - Must be used for this task
- `optional` - Available but not suggested

**3. priority** (required)
- `critical` - Always suggest, highest importance
- `high` - Strongly suggest for matching tasks
- `medium` - Suggest for relevant tasks
- `low` - Only suggest if highly relevant

**4. description** (required)
- Brief description (1-2 sentences)
- Shown to user in suggestion

**5. promptTriggers** (required)
- **keywords** - Simple word matching (case-insensitive)
- **intentPatterns** - Regex patterns for intent matching
- **fileTriggers** - File-based triggers
  - **pathPatterns** - Glob patterns for file paths
  - **contentPatterns** - Regex patterns for file content

**6. context** (optional)
- **requires** - Other skills that must be active
- **incompatibleWith** - Skills that conflict
- **fileTypes** - File types this skill applies to
- **languages** - Programming languages

**7. activation** (optional)
- **autoLoad** - Automatically load without confirmation
- **userConfirmation** - Require user acceptance
- **priorityBoost** - Boost priority score

---

## Pattern Matching

### Keywords Matching

**Simple word matching:**

```json
{
  "keywords": ["python", "async", "await", "asyncio"]
}
```

**User prompt:** "How do I create an async function in python?"
**Match:** ✅ "python", "async" found
**Result:** Skill suggested

**Case-insensitive:**
- "Python" matches
- "PYTHON" matches
- "python" matches

**Partial matching:**
- "async" matches "async", "async function", "asyncio"

### Intent Patterns (Regex)

**Regex patterns for complex intent matching:**

```json
{
  "intentPatterns": [
    "(create|add|implement).*?python.*?(async|coroutine)",
    "python.*?(await|asyncio|coroutine)"
  ]
}
```

**Examples:**

**Prompt 1:** "Create an async function in python"
**Pattern:** `(create|add|implement).*?python.*?(async|coroutine)`
**Match:** ✅ "create" + "python" + "async"
**Result:** Skill suggested

**Prompt 2:** "How do I use asyncio in Python?"
**Pattern:** `python.*?(await|asyncio|coroutine)`
**Match:** ✅ "python" + "asyncio"
**Result:** Skill suggested

**Common Patterns:**

```json
{
  "intentPatterns": [
    // Create something
    "(create|add|implement|build).*?<keyword>",

    // Fix something
    "(fix|resolve|debug|solve).*?<keyword>",

    // Optimize something
    "(optimize|improve|enhance).*?<keyword>",

    // How to questions
    "how.*(to|do|can).*?<keyword>",

    // Error messages
    "(error|exception|fail).*?<keyword>"
  ]
}
```

### File Triggers

**Path Patterns (Glob):**

```json
{
  "fileTriggers": {
    "pathPatterns": [
      "**/*.py",           // All Python files
      "src/**/*.ts",       // TypeScript in src/
      "tests/**/*.test.ts" // Test files
    ]
  }
}
```

**Glob patterns:**
- `**/*.py` - All .py files (recursive)
- `src/**/*.ts` - All .ts files in src/
- `*.json` - All JSON files (root only)
- `**/*test*.py` - All Python files with "test" in name

**Content Patterns (Regex):**

```json
{
  "fileTriggers": {
    "contentPatterns": [
      "import asyncio",
      "from fastapi import",
      "useState.*React"
    ]
  }
}
```

**How it works:**
1. Reads files matching pathPatterns
2. Searches file content for contentPatterns
3. If match found, skill suggested

**Example:**

**File:** `src/api.py`
**Content:** `import asyncio\nfrom fastapi import FastAPI`

**Patterns:** `["import asyncio", "from fastapi"]`
**Match:** ✅ Both patterns found
**Result:** Skill suggested

---

## Priority System

### Priority Levels

**1. critical** (highest)
- Always suggest when relevant
- Show first in suggestions
- Use for: Essential skills (python-development, git-workflow)

**2. high**
- Strongly suggest for matching tasks
- Show near top of suggestions
- Use for: Important domain skills (docker, postgresql)

**3. medium**
- Suggest for relevant tasks
- Show in middle of suggestions
- Use for: Technical skills (async, testing)

**4. low**
- Only suggest if highly relevant
- Show at bottom of suggestions
- Use for: Utility skills (kb-search, formatting)

### Priority Scoring

**Scoring algorithm:**

```
Base priority:
  critical = 100
  high = 75
  medium = 50
  low = 25

Keyword match: +10 each
Intent pattern match: +20 each
File path match: +15 each
File content match: +15 each

Priority boost: +activation.priorityBoost

Total score = base + matches + boost
```

**Example:**

```json
{
  "python-async": {
    "priority": "high",  // Base: 75
    "promptTriggers": {
      "keywords": ["python", "async"],  // +20
      "intentPatterns": [
        "(create|add).*?python.*?async"  // +20 if match
      ],
      "fileTriggers": {
        "pathPatterns": ["**/*.py"],  // +15
        "contentPatterns": ["import asyncio"]  // +15
      }
    },
    "activation": {
      "priorityBoost": 5  // +5
    }
  }
}
```

**Scenario:** User asks "Create async function in python" with `api.py` open

**Score:**
- Base (high): 75
- Keyword "python": +10
- Keyword "async": +10
- Intent pattern match: +20
- File path match (api.py): +15
- File content match (import asyncio): +15
- Priority boost: +5
- **Total: 150** (very high)

**Result:** Skill suggested first, with high confidence

---

## UserPromptSubmit Hook

### Hook Implementation

**Type:** LLM hook (requires analysis)
**Event:** UserPromptSubmit
**Performance:** <1 second (don't block user)

**TypeScript Implementation:**

```typescript
// .claude/hooks/UserPromptSubmit/skill-activation.ts

interface SkillRule {
  type: string;
  priority: string;
  description: string;
  promptTriggers: {
    keywords: string[];
    intentPatterns: string[];
    fileTriggers: {
      pathPatterns: string[];
      contentPatterns: string[];
    };
  };
  activation?: {
    userConfirmation: boolean;
    priorityBoost: number;
  };
}

interface SkillRules {
  [skillName: string]: SkillRule;
}

export async function skillActivationPrompt(
  prompt: string,
  context: {
    openFiles: string[];
    fileContents: Map<string, string>;
  }
): Promise<string> {
  // Load skill rules
  const skillRules: SkillRules = await loadSkillRules();

  // Calculate scores
  const scoredSkills = [];

  for (const [skillName, rule] of Object.entries(skillRules)) {
    const score = calculateSkillScore(prompt, context, rule);
    if (score > 0) {
      scoredSkills.push({ skillName, score, rule });
    }
  }

  // Sort by score (descending)
  scoredSkills.sort((a, b) => b.score - a.score);

  // Filter top skills
  const topSkills = scoredSkills.slice(0, 3);

  // Format suggestions
  return formatSuggestions(topSkills);
}

function calculateSkillScore(
  prompt: string,
  context: any,
  rule: SkillRule
): number {
  let score = 0;

  // Base priority
  const priorityScores = {
    critical: 100,
    high: 75,
    medium: 50,
    low: 25
  };
  score += priorityScores[rule.priority] || 50;

  // Keyword matching
  const lowerPrompt = prompt.toLowerCase();
  for (const keyword of rule.promptTriggers.keywords) {
    if (lowerPrompt.includes(keyword.toLowerCase())) {
      score += 10;
    }
  }

  // Intent pattern matching
  for (const pattern of rule.promptTriggers.intentPatterns) {
    try {
      const regex = new RegExp(pattern, 'i');
      if (regex.test(prompt)) {
        score += 20;
        break; // Only count first match
      }
    } catch (e) {
      console.error(`Invalid regex: ${pattern}`);
    }
  }

  // File triggers
  if (rule.promptTriggers.fileTriggers) {
    score += scoreFileTriggers(context, rule.promptTriggers.fileTriggers);
  }

  // Priority boost
  if (rule.activation?.priorityBoost) {
    score += rule.activation.priorityBoost;
  }

  return score;
}

function scoreFileTriggers(
  context: any,
  fileTriggers: any
): number {
  let score = 0;

  // Path patterns
  for (const openFile of context.openFiles) {
    for (const pattern of fileTriggers.pathPatterns) {
      if (matchPathPattern(openFile, pattern)) {
        score += 15;
        break;
      }
    }
  }

  // Content patterns
  for (const [file, content] of context.fileContents) {
    for (const pattern of fileTriggers.contentPatterns) {
      if (content.includes(pattern)) {
        score += 15;
        break;
      }
    }
  }

  return score;
}

function formatSuggestions(skills: any[]): string {
  if (skills.length === 0) {
    return "";
  }

  const suggestions = skills
    .map(s => `• ${s.skillName}: ${s.rule.description}`)
    .join("\n");

  return `Based on your request, consider using these skills:\n${suggestions}`;
}

async function loadSkillRules(): Promise<SkillRules> {
  const fs = require('fs').promises;
  const content = await fs.readFile('.claude/skill-rules.json', 'utf-8');
  return JSON.parse(content);
}

function matchPathPattern(filePath: string, pattern: string): boolean {
  // Simplified glob matching
  const regexPattern = pattern
    .replace(/\*\*/g, '.*')
    .replace(/\*/g, '[^/]*')
    .replace(/\?/g, '.');
  const regex = new RegExp(`^${regexPattern}$`);
  return regex.test(filePath);
}
```

**Shell Implementation (Alternative):**

```bash
#!/bin/bash
# .claude/hooks/UserPromptSubmit/skill-activation.sh

PROMPT="$1"
OPEN_FILES="$2"

# Load skill rules
SKILL_RULES=$(cat .claude/skill-rules.json)

# Simple keyword matching (shell script)
MATCHING_SKILLS=$(echo "$SKILL_RULES" | jq -r '
  to_entries[] |
  select(.value.promptTriggers.keywords // [] | inside(env.PROMPT | ascii_downcase)) |
  "\(.key): \(.value.description)"
')

if [ -n "$MATCHING_SKILLS" ]; then
  echo "Based on your request, consider using these skills:"
  echo "$MATCHING_SKILLS"
fi
```

---

## Configuration

### settings.json

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "type": "llm",
        "path": ".claude/hooks/UserPromptSubmit/skill-activation.ts"
      }
    ]
  }
}
```

### skill-rules.json Location

**Location:** `.claude/skill-rules.json`

**Required:** Yes (for auto-activation to work)

**Structure:**
```json
{
  "skill-1": { /* rule */ },
  "skill-2": { /* rule */ },
  "skill-3": { /* rule */ }
}
```

---

## Examples

### Example 1: Python Development Skill

```json
{
  "python-development": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",
    "description": "Python development patterns, best practices, and common workflows",

    "promptTriggers": {
      "keywords": [
        "python",
        "py",
        "django",
        "flask",
        "fastapi"
      ],

      "intentPatterns": [
        "(create|add|implement).*?python.*?(class|function|module)",
        "python.*?(class|function|module).*?(best.practice|pattern)",
        "(import|from).*?python"
      ],

      "fileTriggers": {
        "pathPatterns": [
          "**/*.py",
          "**/requirements.txt",
          "**/pyproject.toml"
        ],

        "contentPatterns": [
          "import ",
          "from ",
          "#!/usr/bin/env python"
        ]
      }
    },

    "context": {
      "fileTypes": ["*.py", "*.pyx", "*.pyi"],
      "languages": ["python"]
    },

    "activation": {
      "autoLoad": false,
      "userConfirmation": true
    }
  }
}
```

**Triggers on:**
- Prompt: "Create a Python class for user management"
- Prompt: "How do I import modules in Python?"
- File: `src/models.py` open
- File: `requirements.txt` with `django` in content

### Example 2: Async Programming Skill

```json
{
  "async-programming": {
    "type": "technical",
    "enforcement": "suggest",
    "priority": "medium",
    "description": "Async/await patterns, coroutines, event loops",

    "promptTriggers": {
      "keywords": [
        "async",
        "await",
        "coroutine",
        "asyncio",
        "future",
        "promise"
      ],

      "intentPatterns": [
        "(create|make).*?async.*?(function|method)",
        "how.*(use|implement).*?(async|await)",
        "(async|await).*(pattern|best.practice)"
      ],

      "fileTriggers": {
        "pathPatterns": ["**/*.py", "**/*.ts", "**/*.js"],

        "contentPatterns": [
          "import asyncio",
          "from asyncio import",
          "async def",
          "await ",
          "async function",
          "Promise"
        ]
      }
    },

    "context": {
      "fileTypes": ["*.py", "*.ts", "*.js"],
      "languages": ["python", "typescript", "javascript"]
    }
  }
}
```

**Triggers on:**
- Prompt: "Create async function for API calls"
- Prompt: "How do I use asyncio in Python?"
- File: `src/api.py` with `import asyncio`
- File: `src/api.ts` with `async function`

### Example 3: Docker Skill

```json
{
  "docker-development": {
    "type": "domain",
    "enforcement": "suggest",
    "priority": "high",
    "description": "Docker containers, images, compose, and deployment",

    "promptTriggers": {
      "keywords": [
        "docker",
        "container",
        "dockerfile",
        "compose",
        "kubernetes",
        "k8s"
      ],

      "intentPatterns": [
        "(create|build).*?docker.*?(image|container)",
        "docker.*?(compose|file|deploy)",
        "(container|docker).*(network|volume|mount)"
      ],

      "fileTriggers": {
        "pathPatterns": [
          "**/Dockerfile",
          "**/docker-compose.yml",
          "**/.dockerignore"
        ],

        "contentPatterns": [
          "FROM ",
          "docker-compose",
          "docker build"
        ]
      }
    },

    "context": {
      "fileTypes": ["Dockerfile", "docker-compose.yml", "*.dockerfile"]
    }
  }
}
```

**Triggers on:**
- Prompt: "Create a Dockerfile for Python app"
- Prompt: "How do I use docker-compose?"
- File: `Dockerfile` open
- File: `docker-compose.yml` open

---

## Best Practices

### 1. Keyword Selection

**DO:**
- Use specific, relevant keywords
- Include common synonyms
- Use domain-specific terminology
- Test with real prompts

**DON'T:**
- Use overly generic keywords ("code", "file")
- Use too many keywords (>10)
- Forget case-insensitivity
- Use full sentences

### 2. Intent Patterns

**DO:**
- Test regex patterns thoroughly
- Use non-capturing groups `(?:...)`
- Make patterns case-insensitive `/i`
- Start simple, add complexity gradually

**DON'T:**
- Create overly complex regex
- Forget to escape special characters
- Use greedy matching `.*` (use `.*?` instead)
- Create patterns that match everything

### 3. File Triggers

**DO:**
- Use specific path patterns
- Test content patterns on real files
- Combine path and content patterns
- Consider performance (don't scan too many files)

**DON'T:**
- Use `**/*` (matches everything)
- Create expensive content checks
- Forget to handle file read errors
- Trigger on common code (e.g., "import")

### 4. Priority Assignment

**DO:**
- Reserve `critical` for essential skills
- Use `high` for domain skills
- Use `medium` for technical skills
- Use `low` for utility skills

**DON'T:**
- Make everything `high` or `critical`
- Use `low` for important skills
- Forget to test priority order
- Ignore priority boost feature

---

## Troubleshooting

### Skill Not Suggesting Itself

**Checklist:**
1. ✅ skill-rules.json exists?
2. ✅ JSON syntax valid? (`jq . skill-rules.json`)
3. ✅ Skill name matches exactly?
4. ✅ Keywords in user prompt?
5. ✅ Intent patterns match?
6. ✅ File triggers match?
7. ✅ UserPromptSubmit hook registered?
8. ✅ Hook file executable (if shell)?

**Common Fixes:**
- Add more keywords
- Simplify intent patterns
- Broaden path patterns
- Fix JSON syntax errors
- Match skill name exactly (SKILL.md ↔ skill-rules.json)

### Too Many Suggestions

**Problem:** All skills suggesting themselves

**Solutions:**
1. Reduce priority levels
2. Make trigger patterns more specific
3. Remove overly generic keywords
4. Use `enforcement: "optional"`
5. Adjust priority boost values

### Wrong Skills Suggested

**Problem:** Irrelevant skills suggested

**Solutions:**
1. Refine intent patterns (be more specific)
2. Remove generic keywords
3. Add negative patterns (if supported)
4. Adjust priority scores
5. Test with real prompts

---

## Performance

### Hook Performance

**Target:** <1 second (don't block user)

**Optimization Strategies:**

1. **Load skill rules once** (cache in memory)
2. **Use efficient pattern matching**
   - Keywords: Simple string search (fast)
   - Intent: Compiled regex (cache)
   - Files: Limit files scanned
3. **Score efficiently** (break early if score low)
4. **Limit suggestions** (top 3-5 skills)
5. **Use shell hooks** (faster than LLM for simple matching)

### Bottlenecks

**Common bottlenecks:**
1. Reading too many files for content patterns
2. Complex regex patterns
3. LLM hook (vs shell hook)
4. Not caching compiled regex
5. Scanning entire codebase

**Solutions:**
1. Limit file scanning (open files only)
2. Pre-compile regex patterns
3. Use shell hook for simple matching
4. Cache skill rules in memory
5. Optimize glob patterns

---

## Testing

### Manual Testing

**Test 1: Keyword matching**
```
Prompt: "Create async function in python"
Expected: python-development, async-programming suggested
```

**Test 2: Intent pattern matching**
```
Prompt: "How do I optimize Docker image size?"
Expected: docker-development suggested
```

**Test 3: File triggers**
```
Files open: src/api.py (with "import asyncio")
Prompt: "Add error handling"
Expected: async-programming suggested (due to file content)
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
            "prompt": "Create async function in python",
            "open_files": ["src/api.py"],
            "file_contents": {
                "src/api.py": "import asyncio\nfrom fastapi import FastAPI"
            },
            "expected": ["python-development", "async-programming"]
        },
        {
            "prompt": "Build Docker image for Node.js app",
            "open_files": ["Dockerfile"],
            "file_contents": {
                "Dockerfile": "FROM node:18\nCOPY . ."
            },
            "expected": ["docker-development"]
        }
    ]

    for test in test_cases:
        skills = suggest_skills(
            test["prompt"],
            test["open_files"],
            test["file_contents"],
            rules
        )
        print(f"Prompt: {test['prompt']}")
        print(f"Expected: {test['expected']}")
        print(f"Got: {skills}")
        assert set(skills) >= set(test["expected"])

def suggest_skills(prompt, open_files, file_contents, rules):
    # Simplified suggestion logic
    suggested = []
    for skill_name, rule in rules.items():
        # Check keywords
        for keyword in rule["promptTriggers"]["keywords"]:
            if keyword.lower() in prompt.lower():
                suggested.append(skill_name)
                break
    return suggested

if __name__ == "__main__":
    test_skill_rules()
    print("All tests passed!")
```

---

## Related Resources

**Internal:**
- `@resources/system-overview.md` - Complete system architecture
- `@resources/hook-system.md` - Hook implementation details
- `@resources/progressive-disclosure.md` - Progressive disclosure patterns

**Shared KB:**
- `universal/patterns/claude-code-files-organization-001.yaml` - Organization guide

**External:**
- [Claude Code Documentation](https://claude.com/claude-code)
- [Regex Testing](https://regex101.com/)

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** diet103 Claude Code Infrastructure Showcase (6 months production)
