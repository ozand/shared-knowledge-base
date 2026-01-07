# skill-rules.json Schema

Complete schema reference for skill auto-activation configuration.

---

## Overview

**Purpose:** Define when and how skills should auto-activate

**Location:** `.claude/skill-rules.json`

**Integration:** Used by UserPromptSubmit hook for skill suggestion

---

## Complete Schema

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

---

## Field Definitions

### type (required)

**Values:**
- `domain` - Domain-specific skills (python, docker, postgresql)
- `technical` - Technical skills (async, testing, api-design)
- `workflow` - Workflow skills (git-workflow, code-review)
- `utility` - Utility skills (kb-search, formatting)

**Examples:**
```json
{
  "python-development": {
    "type": "domain"
  },
  "async-programming": {
    "type": "technical"
  },
  "git-workflow": {
    "type": "workflow"
  },
  "kb-search": {
    "type": "utility"
  }
}
```

---

### enforcement (optional, default: "suggest")

**Values:**
- `suggest` - Suggest to user, user can decline
- `require` - Must be used for this task
- `optional` - Available but not suggested

**Examples:**
```json
{
  "python-development": {
    "enforcement": "suggest"
  },
  "git-workflow": {
    "enforcement": "require"
  }
}
```

---

### priority (required)

**Values:**
- `critical` - Always suggest, highest importance
- `high` - Strongly suggest for matching tasks
- `medium` - Suggest for relevant tasks
- `low` - Only suggest if highly relevant

**Base scores:**
- critical = 100
- high = 75
- medium = 50
- low = 25

**Examples:**
```json
{
  "python-development": {
    "priority": "high"
  },
  "kb-search": {
    "priority": "low"
  }
}
```

---

### description (required)

**Format:** 1-2 sentences

**Content:** What the skill does, who it's for

**Examples:**
```json
{
  "python-development": {
    "description": "Python development patterns, best practices, and common workflows"
  },
  "async-programming": {
    "description": "Async/await patterns, coroutines, and event loops"
  }
}
```

---

### promptTriggers (required)

#### keywords

**Type:** Array of strings

**Purpose:** Simple word matching

**Count:** 5-10 keywords

**Matching:** Case-insensitive

**Examples:**
```json
{
  "python-development": {
    "promptTriggers": {
      "keywords": ["python", "py", "django", "flask", "fastapi"]
    }
  },
  "async-programming": {
    "promptTriggers": {
      "keywords": ["async", "await", "coroutine", "asyncio", "future"]
    }
  }
}
```

**Best practices:**
- Use specific, relevant keywords
- Include common synonyms
- Domain-specific terminology
- Test with real prompts

**Avoid:**
- Generic keywords ("code", "file")
- Too many keywords (>10)
- Full sentences

---

#### intentPatterns

**Type:** Array of regex strings

**Purpose:** Complex intent matching

**Count:** 2-5 patterns

**Matching:** Case-insensitive

**Examples:**
```json
{
  "python-async": {
    "promptTriggers": {
      "intentPatterns": [
        "(create|add|implement).*?python.*?(async|coroutine)",
        "python.*?(await|asyncio)",
        "(make|write).*?async.*?(function|method).*?python"
      ]
    }
  }
}
```

**Pattern components:**
- `(create|add|implement)` - Action words
- `.*?` - Non-greedy wildcard
- `(async|coroutine)` - Target keywords
- `python` - Domain qualifier

**Common patterns:**
```json
{
  "create": "(create|add|implement|build).*?<keyword>",
  "fix": "(fix|resolve|debug|solve).*?<keyword>",
  "optimize": "(optimize|improve|enhance).*?<keyword>",
  "how": "how.*(to|do|can).*?<keyword>",
  "error": "(error|exception|fail).*?<keyword>"
}
```

**Testing:**
- Use regex101.com
- Test with real prompts
- Make patterns case-insensitive
- Start simple, add complexity

**Avoid:**
- Overly complex patterns
- Greedy matching (`.*` vs `.*?`)
- Forgetting to escape special characters

---

#### fileTriggers (optional)

**Purpose:** Trigger based on files in workspace

**Structure:**
```json
{
  "fileTriggers": {
    "pathPatterns": ["**/*.py", "src/**/*.ts"],
    "contentPatterns": ["import asyncio", "useState"]
  }
}
```

**pathPatterns:**
- Type: Array of glob patterns
- Purpose: Match file paths
- Examples:
  - `**/*.py` - All Python files
  - `src/**/*.ts` - TypeScript in src/
  - `**/*test*.py` - Test files

**contentPatterns:**
- Type: Array of regex patterns
- Purpose: Match file content
- Examples:
  - `import asyncio`
  - `from fastapi import`
  - `useState.*React`

**How it works:**
1. Reads files matching pathPatterns
2. Searches file content for contentPatterns
3. If match found, skill suggested

**Examples:**
```json
{
  "python-development": {
    "fileTriggers": {
      "pathPatterns": ["**/*.py", "**/requirements.txt"],
      "contentPatterns": ["import ", "from ", "#!/usr/bin/env python"]
    }
  },
  "react-development": {
    "fileTriggers": {
      "pathPatterns": ["**/*.jsx", "**/*.tsx"],
      "contentPatterns": ["import React", "useState", "useEffect"]
    }
  }
}
```

**Performance:**
- Limit files scanned (open files only if possible)
- Specific patterns (not `**/*`)
- Cache results when possible

---

### context (optional)

**Purpose:** Define skill relationships and requirements

**Structure:**
```json
{
  "context": {
    "requires": ["other-skill"],
    "incompatibleWith": ["conflicting-skill"],
    "fileTypes": ["*.py", "*.ts"],
    "languages": ["python", "typescript"]
  }
}
```

**requires:**
- Skills that must be active
- Array of skill names
- Auto-activate required skills

**incompatibleWith:**
- Skills that conflict
- Array of skill names
- Don't suggest if incompatible skill active

**fileTypes:**
- File types this skill applies to
- Array of glob patterns
- Used for filtering

**languages:**
- Programming languages
- Array of language names
- Used for filtering

**Examples:**
```json
{
  "fastapi-development": {
    "context": {
      "requires": ["python-development"],
      "fileTypes": ["*.py"],
      "languages": ["python"]
    }
  }
}
```

---

### activation (optional)

**Purpose:** Control activation behavior

**Structure:**
```json
{
  "activation": {
    "autoLoad": false,
    "userConfirmation": true,
    "priorityBoost": 5
  }
}
```

**autoLoad:**
- Type: Boolean
- Default: false
- If true, load without confirmation

**userConfirmation:**
- Type: Boolean
- Default: true
- If false, don't ask user

**priorityBoost:**
- Type: Integer
- Default: 0
- Boost priority score by this amount

**Examples:**
```json
{
  "python-development": {
    "activation": {
      "autoLoad": false,
      "userConfirmation": true
    }
  },
  "critical-skill": {
    "activation": {
      "autoLoad": true,
      "priorityBoost": 10
    }
  }
}
```

---

## Complete Example

```json
{
  "python-async": {
    "type": "technical",
    "enforcement": "suggest",
    "priority": "high",
    "description": "Python async/await patterns, coroutines, and event loops",

    "promptTriggers": {
      "keywords": [
        "async",
        "await",
        "coroutine",
        "asyncio",
        "future"
      ],

      "intentPatterns": [
        "(create|add|implement).*?python.*?(async|coroutine)",
        "python.*?(await|asyncio|coroutine)",
        "(make|write).*?async.*?(function|method).*?python"
      ],

      "fileTriggers": {
        "pathPatterns": [
          "**/*.py",
          "**/requirements.txt"
        ],

        "contentPatterns": [
          "import asyncio",
          "from asyncio import",
          "async def",
          "await "
        ]
      }
    },

    "context": {
      "requires": ["python-development"],
      "fileTypes": ["*.py"],
      "languages": ["python"]
    },

    "activation": {
      "autoLoad": false,
      "userConfirmation": true,
      "priorityBoost": 0
    }
  }
}
```

---

## Priority Scoring

### Algorithm

```
Base priority:
  critical = 100
  high = 75
  medium = 50
  low = 25

+ Keyword match: +10 each
+ Intent pattern match: +20 each
+ File path match: +15 each
+ File content match: +15 each
+ Priority boost: +activation.priorityBoost

= Total score
```

### Example Calculation

**Scenario:** User asks "Create async function in python" with `api.py` open

**Rule:**
```json
{
  "priority": "high",  // 75
  "keywords": ["python", "async"],  // +20
  "intentPatterns": ["(create).*?python.*?async"],  // +20 if match
  "fileTriggers": {
    "pathPatterns": ["**/*.py"],  // +15
    "contentPatterns": ["import asyncio"]  // +15
  },
  "activation": {
    "priorityBoost": 5  // +5
  }
}
```

**Score:**
- Base (high): 75
- Keyword "python": +10
- Keyword "async": +10
- Intent pattern: +20
- File path (api.py): +15
- File content (import asyncio): +15
- Priority boost: +5
- **Total: 150** (very high)

---

## Testing

### Manual Testing

```bash
# Test 1: Keywords
Prompt: "Help with async code"
Expected: Skill suggested

# Test 2: Intent pattern
Prompt: "Create async function"
Expected: Skill suggested

# Test 3: File trigger
File: test.py with "import asyncio"
Prompt: "Add error handling"
Expected: Skill suggested
```

### Automated Testing

```python
# test_skill_rules.py

import json
import re

def test_skill_rules():
    with open('.claude/skill-rules.json') as f:
        rules = json.load(f)

    test_cases = [
        {
            "prompt": "Create async function in python",
            "open_files": ["api.py"],
            "file_contents": {"api.py": "import asyncio"},
            "expected": ["python-async"]
        }
    ]

    for test in test_cases:
        skills = match_skills(test, rules)
        print(f"Prompt: {test['prompt']}")
        print(f"Expected: {test['expected']}")
        print(f"Got: {skills}")
        assert set(skills) >= set(test['expected'])

def match_skills(test, rules):
    matched = []
    for name, rule in rules.items():
        score = calculate_score(test, rule)
        if score > 50:  # Threshold
            matched.append((name, score))
    return [m[0] for m in sorted(matched, key=lambda x: x[1], reverse=True)]

def calculate_score(test, rule):
    score = {"critical": 100, "high": 75, "medium": 50, "low": 25}.get(rule["priority"], 50)

    # Keywords
    for kw in rule["promptTriggers"]["keywords"]:
        if kw.lower() in test["prompt"].lower():
            score += 10

    # Intent patterns
    for pattern in rule["promptTriggers"].get("intentPatterns", []):
        if re.search(pattern, test["prompt"], re.I):
            score += 20
            break

    # File triggers
    if "fileTriggers" in rule["promptTriggers"]:
        # ... file trigger logic
        pass

    return score

if __name__ == "__main__":
    test_skill_rules()
    print("✅ All tests passed")
```

---

## Troubleshooting

### Issue: JSON Syntax Error

**Error:** `Expecting ',' delimiter`

**Fix:**
```bash
# Validate JSON
jq . .claude/skill-rules.json

# Or
python -m json.tool .claude/skill-rules.json
```

### Issue: Skill Not Activating

**Symptoms:** Skill doesn't suggest itself

**Checklist:**
1. ✅ skill-rules.json exists?
2. ✅ JSON syntax valid?
3. ✅ Skill name matches exactly?
4. ✅ Keywords in prompt?
5. ✅ Intent patterns work?
6. ✅ Hook registered?

### Issue: Wrong Skills Suggested

**Symptoms:** Irrelevant skills suggested

**Solutions:**
1. Refine intent patterns
2. Remove generic keywords
3. Adjust priority scores
4. Test with real prompts

---

## Best Practices

1. **Start simple** - Keywords first, add intent patterns later
2. **Test thoroughly** - Test with real prompts
3. **Use specific keywords** - Not "code" but "python", "async"
4. **Test regex** - Use regex101.com
5. **Appropriate priority** - Not everything high/critical
6. **Consider performance** - Limit file scanning

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** diet103 Claude Code Infrastructure Showcase
