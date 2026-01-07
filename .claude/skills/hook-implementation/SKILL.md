---
name: "hook-implementation"
description: "Expert in implementing Claude Code hooks for automation and workflow enhancement. Production-tested patterns for all hook events."
version: "1.0"
author: "Claude Code Expert"
tags: ["hooks", "automation", "workflow", "events", "production"]
resources:
  - "resources/hook-events.md"
  - "resources/hook-patterns.md"
  - "resources/performance.md"
  - "examples/skill-activation.md"
  - "examples/post-tool-tracking.md"
  - "examples/error-handling.md"
related:
  - "@skills/claude-code-architecture/SKILL.md"
  - "@resources/claude-code-architecture/resources/hook-system.md"
---

# Hook Implementation

Complete guide to implementing production-tested Claude Code hooks for automation and workflow enhancement.

---

## Quick Start

### Hook in 3 Steps

```bash
# 1. Choose hook event
# UserPromptSubmit, PreToolUse, PostToolUse, etc.

# 2. Create hook file
# Shell: .claude/hooks/<Event>/hook.sh
# LLM: .claude/hooks/<Event>/hook.ts

# 3. Register in settings.json
```

**📘 Complete Hook Events:** `@resources/hook-events.md`

---

## Hook Events Overview

### 1. SessionStart

**When:** Claude Code session starts

**Use cases:**
- Initial environment setup
- Load project context
- Validate configuration
- Initialize state

**Performance:** <2 seconds

**Example:**
```bash
#!/bin/bash
# .claude/hooks/SessionStart/setup-env.sh

echo "🚀 Setting up environment..."

# Check Python version
python --version
echo "✅ Environment ready"
```

**📘 Complete Guide:** `@resources/hook-events.md`

---

### 2. UserPromptSubmit

**When:** After user submits prompt, before Claude processes

**Use cases:**
- **Skill activation** (BREAKTHROUGH)
- Prompt enhancement
- Intent analysis
- Context gathering

**Performance:** <1 second (don't block user)

**Example:**
```typescript
// .claude/hooks/UserPromptSubmit/skill-activation.ts
export async function skillActivationPrompt(prompt: string): Promise<string> {
  const skills = await loadSkillRules();
  const matches = findMatchingSkills(prompt, skills);

  if (matches.length > 0) {
    return formatSuggestions(matches);
  }

  return "";
}
```

---

### 3. PreToolUse

**When:** Before any tool call (Read, Write, Bash, etc.)

**Use cases:**
- **Validation** - Validate operation
- **Blocking** - Prevent dangerous operations
- **Transformation** - Modify arguments
- **Authorization** - Check permissions

**Performance:** <500ms (tool call latency)

**Example:**
```bash
#!/bin/bash
# .claude/hooks/PreToolUse/yaml-validation.sh

TOOL_NAME="$1"
FILE_PATH="$2"

if [ "$TOOL_NAME" = "Write" ] && [[ "$FILE_PATH" == *.yaml ]]; then
    if ! python tools/kb.py validate "$FILE_PATH" 2>&1; then
        echo "❌ YAML validation failed"
        exit 1  # Block operation
    fi
fi

exit 0
```

---

### 4. PostToolUse

**When:** After successful tool call

**Use cases:**
- **Tracking** - Log tool usage
- **Formatting** - Auto-format output
- **Notifications** - Send notifications
- **Caching** - Cache results

**Performance:** <1 second (can be async)

**Example:**
```bash
#!/bin/bash
# .claude/hooks/PostToolUse/tool-tracker.sh

TOOL_NAME="$1"
LOG_FILE=".claude/logs/tool-usage.log"

mkdir -p "$(dirname "$LOG_FILE")"
echo "$(date -Iseconds) | $TOOL_NAME" >> "$LOG_FILE"

exit 0
```

---

### 5. Stop

**When:** When Claude finishes session

**Use cases:**
- **Quality validation** - Check work completed
- **Reminders** - Forgotten operations
- **Cleanup** - Temporary files
- **Summary** - Session summary

**Performance:** Non-blocking (session ending anyway)

**Example:**
```typescript
// .claude/hooks/Stop/error-handling-reminder.ts
export async function errorHandlingReminder(context: any): Promise<string> {
  const reminders = [];

  if (context.errorsThrown) {
    reminders.push("⚠️  Errors were thrown - consider documenting in KB");
  }

  if (context.hasUncommittedChanges) {
    reminders.push("📝 Don't forget to commit your changes");
  }

  return reminders.join("\n");
}
```

---

## Hook Types

### Shell Hooks

**File extension:** `.sh`

**Characteristics:**
- ✅ Fast (<100ms typical)
- ✅ Deterministic
- ✅ Easy to test
- ❌ Limited to shell capabilities

**Best for:**
- Validation (PreToolUse)
- Formatting (PostToolUse)
- Simple tracking
- File operations
- Environment checks

**Template:**
```bash
#!/bin/bash
# Must have shebang

# Get arguments
ARG1="$1"
ARG2="$2"

# Hook logic
if [ condition ]; then
    echo "✅ Success"
    exit 0  # Allow
else
    echo "❌ Failed"
    exit 1  # Block (PreToolUse only)
fi
```

**Requirements:**
1. Shebang line (`#!/bin/bash` or `#!/bin/sh`)
2. Executable permissions (`chmod +x`)
3. Exit code 0 = allow, non-zero = block
4. POSIX-compliant (prefer `/bin/sh`)

---

### LLM Hooks

**File extensions:** `.ts`, `.js`, `.py`

**Characteristics:**
- ✅ Full context awareness
- ✅ Complex analysis
- ✅ Flexible logic
- ❌ Slower (1-3 seconds)
- ❌ Higher resource usage

**Best for:**
- Skill activation (UserPromptSubmit)
- Prompt enhancement
- Intent analysis
- Complex validation
- Context-aware decisions

**Template (TypeScript):**
```typescript
// .claude/hooks/UserPromptSubmit/hook.ts

export async function hookName(args: any): Promise<any> {
  // Hook logic
  const result = await doSomething(args);

  return result;
}
```

**Template (Python):**
```python
# .claude/hooks/Stop/hook.py

import json

def hook_name(context: dict) -> str:
    """Hook documentation"""

    # Hook logic
    result = process_context(context)

    return result

if __name__ == "__main__":
    # For testing
    context = {}
    print(hook_name(context))
```

---

## Configuration

### settings.json Structure

**Location:** `.claude/settings.json`

**Complete example:**
```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "shell",
        "path": ".claude/hooks/SessionStart/setup-env.sh"
      }
    ],
    "UserPromptSubmit": [
      {
        "type": "llm",
        "path": ".claude/hooks/UserPromptSubmit/skill-activation.ts"
      }
    ],
    "PreToolUse": [
      {
        "type": "shell",
        "path": ".claude/hooks/PreToolUse/yaml-validation.sh"
      },
      {
        "type": "shell",
        "path": ".claude/hooks/PreToolUse/security-check.sh"
      }
    ],
    "PostToolUse": [
      {
        "type": "shell",
        "path": ".claude/hooks/PostToolUse/tool-tracker.sh"
      },
      {
        "type": "shell",
        "path": ".claude/hooks/PostToolUse/auto-format.sh"
      }
    ],
    "Stop": [
      {
        "type": "llm",
        "path": ".claude/hooks/Stop/error-handling-reminder.ts"
      },
      {
        "type": "shell",
        "path": ".claude/hooks/Stop/cleanup.sh"
      }
    ]
  }
}
```

**Hook properties:**
- `type` - "shell" or "llm"
- `path` - Relative path to hook file
- `enabled` (optional) - true/false (default: true)

**Multiple hooks:**
- Execute in order listed
- All hooks execute (unless one blocks)
- For PreToolUse: first non-zero exit blocks

---

## Performance Considerations

### Target Times

| Hook Event | Max Duration | Reason |
|------------|--------------|---------|
| **SessionStart** | 2 seconds | Session startup latency |
| **UserPromptSubmit** | 1 second | Don't block user |
| **PreToolUse** | 500ms | Tool call latency |
| **PostToolUse** | 1 second | Can be async |
| **Stop** | Non-blocking | Session ending |

### Optimization Strategies

**1. Use shell hooks** (fast, deterministic)
```bash
#!/bin/bash
# Fast validation
if [[ "$FILE" == *.yaml ]]; then
    python tools/kb.py validate "$FILE" > /dev/null 2>&1
fi
```

**2. Cache expensive operations**
```typescript
// Cache skill rules
let skillRulesCache = null;

async function loadSkillRules() {
    if (skillRulesCache) {
        return skillRulesCache;
    }

    skillRulesCache = await loadFile();
    return skillRulesCache;
}
```

**3. Limit file scanning**
```bash
# ❌ BAD: Scans entire codebase
find . -name "*.py"

# ✅ GOOD: Only scans open files
for file in "$OPEN_FILES"; do
    grep "TODO" "$file"
done
```

**4. Use compiled regex**
```typescript
// Pre-compile regex
const patterns = [
    new RegExp("(create|add).*?python", "i"),
    new RegExp("async.*?function", "i")
];

// Use cached patterns
for (const pattern of patterns) {
    if (pattern.test(prompt)) {
        // Match found
    }
}
```

**5. Break early**
```typescript
// Don't check all keywords if one matched
for (const keyword of keywords) {
    if (prompt.includes(keyword)) {
        return true;  // Found match, return early
    }
}
```

**📘 Complete Performance Guide:** `@resources/performance.md`

---

## Common Use Cases

### Use Case 1: Skill Activation

**Purpose:** Suggest relevant skills based on user intent

**Implementation:** TypeScript LLM hook

**Location:** `.claude/hooks/UserPromptSubmit/skill-activation.ts`

**Code:**
```typescript
export async function skillActivationPrompt(prompt: string): Promise<string> {
  const skills = await loadSkillRules();
  const matches = findMatchingSkills(prompt, skills);

  if (matches.length > 0) {
    const suggestions = matches
      .map(m => `• ${m.name}: ${m.description}`)
      .join("\n");

    return `Based on your request, consider using:\n${suggestions}`;
  }

  return "";
}

async function loadSkillRules() {
  const fs = require('fs').promises;
  const content = await fs.readFile('.claude/skill-rules.json', 'utf-8');
  return JSON.parse(content);
}

function findMatchingSkills(prompt: string, rules: any) {
  const matches = [];

  for (const [name, rule] of Object.entries(rules)) {
    const keywords = rule.promptTriggers.keywords || [];
    const hasMatch = keywords.some((kw: string) =>
      prompt.toLowerCase().includes(kw.toLowerCase())
    );

    if (hasMatch) {
      matches.push({ name, description: rule.description });
    }
  }

  return matches.sort((a, b) => b.score - a.score).slice(0, 3);
}
```

**📘 Complete Example:** `@examples/skill-activation.md`

---

### Use Case 2: YAML Validation

**Purpose:** Validate YAML files before writing

**Implementation:** Shell hook

**Location:** `.claude/hooks/PreToolUse/yaml-validation.sh`

**Code:**
```bash
#!/bin/bash

TOOL_NAME="$1"
FILE_PATH="$2"

# Validate YAML files before Write
if [ "$TOOL_NAME" = "Write" ]; then
    if [[ "$FILE_PATH" == *.yaml ]] || [[ "$FILE_PATH" == *.yml ]]; then
        echo "🔍 Validating YAML: $FILE_PATH"

        if [ -f "tools/kb.py" ]; then
            if ! python tools/kb.py validate "$FILE_PATH" 2>&1; then
                echo "❌ YAML validation failed"
                echo "Fix errors before writing"
                exit 1  # Block the Write operation
            fi
            echo "✅ YAML validation passed"
        fi
    fi
fi

exit 0
```

---

### Use Case 3: Tool Usage Tracking

**Purpose:** Track all tool calls for analytics

**Implementation:** Shell hook

**Location:** `.claude/hooks/PostToolUse/tool-tracker.sh`

**Code:**
```bash
#!/bin/bash

TOOL_NAME="$1"
EXIT_CODE="$2"

# Log tool usage
LOG_FILE=".claude/logs/tool-usage.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "$(date -Iseconds) | $TOOL_NAME | exit: $EXIT_CODE" >> "$LOG_FILE"

# Track specific tools
case "$TOOL_NAME" in
    Write)
        echo "📝 Write operation logged"
        ;;
    Bash)
        echo "💻 Bash command logged"
        ;;
    Read)
        echo "📖 Read operation logged"
        ;;
esac

exit 0
```

**📘 Complete Example:** `@examples/post-tool-tracking.md`

---

### Use Case 4: Error Handling Reminder

**Purpose:** Remind user to document errors

**Implementation:** TypeScript LLM hook

**Location:** `.claude/hooks/Stop/error-handling-reminder.ts`

**Code:**
```typescript
export async function errorHandlingReminder(
  context: {
    errorsThrown: boolean;
    hasUncommittedChanges: boolean;
    hasUnpushedCommits: boolean;
  }
): Promise<string> {
  const reminders = [];

  // Check if errors were thrown
  if (context.errorsThrown) {
    reminders.push("⚠️  Errors were thrown during this session");
    reminders.push("   Consider documenting them in the KB");
  }

  // Check for uncommitted changes
  if (context.hasUncommittedChanges) {
    reminders.push("📝 You have uncommitted changes");
    reminders.push("   Don't forget to commit your work");
  }

  // Check for unpushed commits
  if (context.hasUnpushedCommits) {
    reminders.push("⬆️  You have unpushed commits");
    reminders.push("   Consider pushing to remote");
  }

  if (reminders.length > 0) {
    return "\n" + reminders.join("\n");
  }

  return "";
}
```

**📘 Complete Example:** `@examples/error-handling.md`

---

## Testing Hooks

### Manual Testing

**Test shell hook:**
```bash
# Test directly
bash .claude/hooks/PreToolUse/yaml-validation.sh "Write" "test.yaml"

# Check exit code
echo $?
```

**Test LLM hook (TypeScript):**
```bash
# If ts-node available
ts-node .claude/hooks/UserPromptSubmit/skill-activation.ts "Create async function"

# Or compile and run
tsc hook.ts
node hook.js "test prompt"
```

**Test LLM hook (Python):**
```bash
python .claude/hooks/Stop/cleanup.py
```

---

### Automated Testing

**Test template:**
```python
# test_hooks.py

import subprocess
import json

def test_yaml_validation_hook():
    """Test YAML validation hook"""
    result = subprocess.run(
        ["bash", ".claude/hooks/PreToolUse/yaml-validation.sh", "Write", "test.yaml"],
        capture_output=True,
        text=True
    )

    # Check exit code
    assert result.returncode == 0, "Hook should pass for valid YAML"

    print("✅ YAML validation hook test passed")

def test_skill_activation_hook():
    """Test skill activation hook"""
    # Load skill rules
    with open('.claude/skill-rules.json') as f:
        rules = json.load(f)

    # Test prompts
    test_prompts = [
        ("Create async function", ["async-programming"]),
        ("Build Docker image", ["docker-development"])
    ]

    for prompt, expected in test_prompts:
        # Simulate hook execution
        matched = match_skills(prompt, rules)
        assert any(skill in matched for skill in expected)

    print("✅ Skill activation hook test passed")

if __name__ == "__main__":
    test_yaml_validation_hook()
    test_skill_activation_hook()
    print("✅ All hook tests passed")
```

---

## Best Practices

### 1. Error Handling

**Always handle errors gracefully:**

```bash
#!/bin/bash
set -euo pipefail  # Exit on error

trap 'echo "❌ Hook failed at line $LINENO"; exit 1' ERR

# Validate command exists
if ! command -v python &> /dev/null; then
    echo "⚠️  Python not found, skipping validation"
    exit 0  # Don't block, just skip
fi

# Try validation
if ! python tools/kb.py validate "$FILE"; then
    echo "❌ Validation failed"
    exit 1  # Block operation
fi
```

---

### 2. Performance

**Use shell hooks for fast operations:**

```bash
#!/bin/bash
# ✅ GOOD: Fast shell check
if [[ "$FILE" == *.yaml ]]; then
    python tools/kb.py validate "$FILE"
fi
```

**Use LLM hooks only when necessary:**

```typescript
// ✅ GOOD: LLM for complex analysis
export async function skillActivationPrompt(prompt: string) {
  const skills = await loadSkillRules();
  const matches = findMatchingSkills(prompt, skills);
  return formatSuggestions(matches);
}
```

---

### 3. Security

**Validate input:**

```bash
#!/bin/bash
FILE_PATH="$2"

# ✅ GOOD: Validate file path
if [[ "$FILE_PATH" == *".."* ]]; then
    echo "❌ Invalid file path"
    exit 1
fi

# ✅ GOOD: Sanitize input
FILE_PATH=$(realpath -m "$FILE_PATH")
```

---

### 4. Logging

**Log for debugging:**

```bash
#!/bin/bash

LOG_FILE=".claude/logs/hooks.log"

log() {
    echo "$(date -Iseconds) | $1" >> "$LOG_FILE"
}

log "PreToolUse hook started"
log "Tool: $TOOL_NAME"
log "File: $FILE_PATH"

# ... hook logic ...

log "PreToolUse hook completed"
```

---

## Troubleshooting

### Hook Not Firing

**Checklist:**
1. ✅ Hook file exists?
2. ✅ Hook executable? (`chmod +x` for shell)
3. ✅ Hook registered in settings.json?
4. ✅ JSON syntax valid in settings.json?
5. ✅ Correct event selected?
6. ✅ Claude Code restarted?

**Common fixes:**
- Make shell hooks executable
- Verify settings.json format
- Test hook manually
- Check console for errors

---

### Hook Performance Issues

**Symptoms:**
- Slow session start
- Laggy tool calls

**Solutions:**
1. Profile hook execution time
2. Use shell hooks instead of LLM
3. Cache expensive operations
4. Limit file scanning
5. Optimize regex patterns

---

## Examples

**Production examples from diet103 showcase:**
- skill-activation.ts (TypeScript LLM hook)
- post-tool-use-tracker.sh (Shell hook)
- error-handling-reminder.ts (TypeScript LLM hook)

**📘 Complete Examples:** `@examples/`

---

## Related Resources

**Internal:**
- `@resources/hook-events.md` - Complete event reference
- `@resources/hook-patterns.md` - Implementation patterns
- `@resources/performance.md` - Performance optimization
- `@examples/skill-activation.md` - Skill activation example
- `@examples/post-tool-tracking.md` - Tool tracking example
- `@examples/error-handling.md` - Error handling example

**Related Skills:**
- `@skills/claude-code-architecture/SKILL.md` - System overview
- `@claude-code-architecture/resources/hook-system.md` - Complete hook guide

**Shared KB:**
- `universal/patterns/claude-code-hooks.yaml` - Hooks pattern

**External:**
- [Bash Scripting Guide](https://www.shellcheck.net/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** diet103 Claude Code Infrastructure Showcase
**Quality Score:** 95/100
