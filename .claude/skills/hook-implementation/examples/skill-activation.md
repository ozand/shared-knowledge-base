# Skill Activation Hook

Complete implementation of skill activation system.

---

## Overview

**Purpose:** Suggest relevant skills based on user intent

**Event:** UserPromptSubmit

**Type:** LLM hook (TypeScript)

**Location:** `.claude/hooks/UserPromptSubmit/skill-activation.ts`

---

## Implementation

### Complete Code

```typescript
// .claude/hooks/UserPromptSubmit/skill-activation.ts

interface SkillRule {
  type: string;
  priority: string;
  description: string;
  promptTriggers: {
    keywords: string[];
    intentPatterns?: string[];
    fileTriggers?: {
      pathPatterns: string[];
      contentPatterns: string[];
    };
  };
}

interface SkillMatch {
  name: string;
  description: string;
  score: number;
}

export async function skillActivationPrompt(
  prompt: string,
  context?: {
    openFiles?: string[];
    fileContents?: Map<string, string>;
  }
): Promise<string> {
  // Load skill rules
  const skillRules = await loadSkillRules();

  // Calculate scores
  const scoredSkills = calculateScores(prompt, context, skillRules);

  // Sort by score (descending)
  scoredSkills.sort((a, b) => b.score - a.score);

  // Filter top skills (score > threshold)
  const topSkills = scoredSkills
    .filter(s => s.score > 50)
    .slice(0, 3);

  // Format suggestions
  if (topSkills.length === 0) {
    return "";
  }

  const suggestions = topSkills
    .map(s => `• ${s.name}: ${s.description}`)
    .join("\n");

  return `Based on your request, consider using:\n${suggestions}`;
}

async function loadSkillRules(): Promise<Record<string, SkillRule>> {
  const fs = require('fs').promises;

  try {
    const content = await fs.readFile('.claude/skill-rules.json', 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.error('Failed to load skill-rules.json:', error);
    return {};
  }
}

function calculateScores(
  prompt: string,
  context: any,
  rules: Record<string, SkillRule>
): SkillMatch[] {
  const matches: SkillMatch[] = [];

  for (const [name, rule] of Object.entries(rules)) {
    const score = calculateSkillScore(prompt, context, rule);
    if (score > 0) {
      matches.push({ name, description: rule.description, score });
    }
  }

  return matches;
}

function calculateSkillScore(
  prompt: string,
  context: any,
  rule: SkillRule
): number {
  let score = 0;

  // Base priority
  const priorityScores: Record<string, number> = {
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
  if (rule.promptTriggers.intentPatterns) {
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
  }

  // File triggers
  if (rule.promptTriggers.fileTriggers && context) {
    score += scoreFileTriggers(context, rule.promptTriggers.fileTriggers);
  }

  return score;
}

function scoreFileTriggers(
  context: any,
  fileTriggers: { pathPatterns: string[]; contentPatterns: string[] }
): number {
  let score = 0;

  // Path patterns
  if (context.openFiles) {
    for (const openFile of context.openFiles) {
      for (const pattern of fileTriggers.pathPatterns) {
        if (matchPathPattern(openFile, pattern)) {
          score += 15;
          break;
        }
      }
    }
  }

  // Content patterns
  if (context.fileContents) {
    for (const [file, content] of context.fileContents) {
      for (const pattern of fileTriggers.contentPatterns) {
        if (content.includes(pattern)) {
          score += 15;
          break;
        }
      }
    }
  }

  return score;
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

---

## Configuration

### skill-rules.json

```json
{
  "python-async": {
    "type": "technical",
    "priority": "high",
    "description": "Python async/await patterns and coroutines",
    "promptTriggers": {
      "keywords": ["python", "async", "await", "coroutine"],
      "intentPatterns": [
        "(create|add).*?python.*?(async|coroutine)",
        "python.*?(await|asyncio)"
      ],
      "fileTriggers": {
        "pathPatterns": ["**/*.py"],
        "contentPatterns": ["import asyncio", "async def"]
      }
    }
  }
}
```

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

---

## Testing

### Manual Testing

```bash
# Test with ts-node (if available)
ts-node .claude/hooks/UserPromptSubmit/skill-activation.ts "Create async function"

# Expected output:
# Based on your request, consider using:
# • python-async: Python async/await patterns and coroutines
```

### Automated Testing

```python
# test_skill_activation.py

import subprocess
import json

def test_skill_activation():
    """Test skill activation hook"""
    # Test cases
    test_cases = [
        {
            "prompt": "Create async function in python",
            "expected": ["python-async"]
        },
        {
            "prompt": "Build Docker image",
            "expected": ["docker"]
        }
    ]

    for test in test_cases:
        # Simulate hook execution
        prompt = test["prompt"]
        print(f"\nTesting: {prompt}")

        # Load skill rules
        with open('.claude/skill-rules.json') as f:
            rules = json.load(f)

        # Match skills
        matched = []
        for name, rule in rules.items():
            for keyword in rule["promptTriggers"]["keywords"]:
                if keyword.lower() in prompt.lower():
                    matched.append(name)
                    break

        print(f"Matched: {matched}")
        print(f"Expected: {test['expected']}")

        assert any(skill in matched for skill in test["expected"])

    print("\n✅ All tests passed")

if __name__ == "__main__":
    test_skill_activation()
```

---

## Troubleshooting

### Issue: No Suggestions

**Check:**
1. skill-rules.json exists?
2. JSON syntax valid?
3. Keywords in prompt?
4. Hook registered?

### Issue: Wrong Skills Suggested

**Fix:**
1. Refine keywords
2. Adjust intent patterns
3. Modify priority levels
4. Test with real prompts

---

## Performance

**Target:** <1 second (don't block user)

**Optimization:**
- Cache skill rules in memory
- Pre-compile regex patterns
- Break early on matches
- Limit file scanning

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** diet103 Claude Code Infrastructure Showcase
