# Hook System

Complete guide to Claude Code hooks - deterministic automation at workflow points.

---

## Overview

**What are Hooks?**

Hooks are guaranteed executions at specific workflow points that enable automation, validation, and workflow enhancement.

**Key Characteristics:**
- **Deterministic** - Always execute when triggered
- **Event-driven** - Execute at specific points in workflow
- **Two types** - Shell (fast) and LLM (flexible)
- **Configurable** - Enable/disable per project
- **Performant** - Designed for minimal latency

**Hook Events:**
1. **SessionStart** - When Claude Code session starts
2. **UserPromptSubmit** - After user submits prompt
3. **PreToolUse** - Before any tool call
4. **PostToolUse** - After successful tool call
5. **Stop** - When Claude finishes session

---

## Hook Events

### 1. SessionStart

**When:** Immediately when Claude Code session starts

**Use Cases:**
- Initial environment setup
- Load project context
- Validate configuration
- Initialize state
- Check prerequisites

**Examples:**
```bash
# .claude/hooks/SessionStart/setup-env.sh
#!/bin/bash

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version detected"

# Check if .kb/index.db exists
if [ ! -f ".kb/index.db" ]; then
    echo "⚠️  KB index not found. Run: python tools/kb.py index -v"
fi

# Load project context
if [ -f ".claude/CONTEXT.md" ]; then
    echo "📖 Project context loaded"
fi
```

**Performance Target:** <2 seconds
**Type:** Shell or LLM
**Blocking:** No (session starts regardless)

---

### 2. UserPromptSubmit

**When:** After user submits prompt, before Claude processes it

**Use Cases:**
- **Skill activation** (BREAKTHROUGH pattern)
- Prompt enhancement
- Intent analysis
- Context gathering
- Pre-computation

**Examples:**

**TypeScript (skill activation):**
```typescript
// .claude/hooks/UserPromptSubmit/skill-activation.ts

export async function skillActivationPrompt(prompt: string) {
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

**Shell (simple keyword matching):**
```bash
# .claude/hooks/UserPromptSubmit/quick-suggestions.sh
#!/bin/bash

PROMPT="$1"

# Simple keyword matching
if echo "$PROMPT" | grep -qi "docker"; then
    echo "💡 Consider using: docker-development skill"
fi

if echo "$PROMPT" | grep -qi "python.*async"; then
    echo "💡 Consider using: async-programming skill"
fi
```

**Performance Target:** <1 second (don't block user)
**Type:** Shell (fast) or LLM (analysis)
**Blocking:** No (prompt processed regardless)

---

### 3. PreToolUse

**When:** Before any tool call (Read, Write, Bash, etc.)

**Use Cases:**
- **Validation** - Validate operation before execution
- **Blocking** - Prevent dangerous operations
- **Transformation** - Modify arguments
- **Logging** - Log all tool calls
- **Authorization** - Check permissions

**Examples:**

**Shell (YAML validation):**
```bash
# .claude/hooks/PreToolUse/yaml-validation.sh
#!/bin/bash

TOOL_NAME="$1"
FILE_PATH="$2"

# Validate YAML files before Write
if [ "$TOOL_NAME" = "Write" ]; then
    if [[ "$FILE_PATH" == *.yaml ]] || [[ "$FILE_PATH" == *.yml ]]; then
        echo "🔍 Validating YAML: $FILE_PATH"

        # Check if python tools/kb.py validate exists
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

**Shell (dangerous command blocking):**
```bash
# .claude/hooks/PreToolUse/security-check.sh
#!/bin/bash

TOOL_NAME="$1"
COMMAND="$2"

# Block dangerous Bash commands
if [ "$TOOL_NAME" = "Bash" ]; then
    DANGEROUS_PATTERNS=(
        "rm -rf /"
        "rm -rf /*"
        "mkfs"
        ":(){ :|:& };:"  # fork bomb
        "dd if=/dev/zero"
    )

    for pattern in "${DANGEROUS_PATTERNS[@]}"; do
        if echo "$COMMAND" | grep -q "$pattern"; then
            echo "❌ Dangerous command blocked: $pattern"
            exit 1  # Block the operation
        fi
    done
fi

exit 0
```

**TypeScript (argument transformation):**
```typescript
// .claude/hooks/PreToolUse/arg-transformer.ts

export async function transformToolArgs(
  toolName: string,
  args: any
): Promise<any> {
  // Add line numbers to Read tool
  if (toolName === "Read" && !args.offset && !args.limit) {
    const fileSize = await getFileSize(args.file_path);

    // Only read first 200 lines for large files
    if (fileSize > 10000) {
      console.log(`📄 Large file detected, reading first 200 lines`);
      args.offset = 1;
      args.limit = 200;
    }
  }

  return args;
}

async function getFileSize(filePath: string): Promise<number> {
  const fs = require('fs').promises;
  const stats = await fs.stat(filePath);
  return stats.size;
}
```

**Performance Target:** <500ms (tool call latency)
**Type:** Shell (preferred for validation)
**Blocking:** Yes (can block tool call if returns non-zero)

---

### 4. PostToolUse

**When:** After successful tool call

**Use Cases:**
- **Tracking** - Log tool usage
- **Formatting** - Format output
- **Notifications** - Send notifications
- **Caching** - Cache results
- **Analysis** - Analyze usage patterns

**Examples:**

**Shell (tool usage tracker):**
```bash
# .claude/hooks/PostToolUsage/tool-tracker.sh
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

**Shell (auto-format on Write):**
```bash
# .claude/hooks/PostToolUse/auto-format.sh
#!/bin/bash

TOOL_NAME="$1"
FILE_PATH="$2"

# Auto-format Python files after Write
if [ "$TOOL_NAME" = "Write" ] && [[ "$FILE_PATH" == *.py ]]; then
    if command -v black &> /dev/null; then
        echo "🎨 Auto-formatting Python file..."
        black "$FILE_PATH" --quiet
        echo "✅ Formatted with black"
    fi
fi

# Auto-format JSON files after Write
if [ "$TOOL_NAME" = "Write" ] && [[ "$FILE_PATH" == *.json ]]; then
    echo "🎨 Auto-formatting JSON file..."
    jq '.' "$FILE_PATH" > "${FILE_PATH}.tmp"
    mv "${FILE_PATH}.tmp" "$FILE_PATH"
    echo "✅ Formatted JSON"
fi

exit 0
```

**Performance Target:** <1 second (can be async)
**Type:** Shell (preferred for speed)
**Blocking:** No (tool call already completed)

---

### 5. Stop

**When:** When Claude finishes session

**Use Cases:**
- **Quality validation** - Check work completed
- **Reminders** - Forgotten operations
- **Cleanup** - Temporary files
- **Summary** - Session summary
- **Notifications** - Session end notifications

**Examples:**

**TypeScript (error handling reminder):**
```typescript
// .claude/hooks/Stop/error-handling-reminder.ts

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

**Shell (cleanup):**
```bash
# .claude/hooks/Stop/cleanup.sh
#!/bin/bash

# Remove temporary files
if [ -d ".claude/tmp" ]; then
    echo "🧹 Cleaning up temporary files..."
    rm -rf .claude/tmp/*
    echo "✅ Cleanup complete"
fi

# Generate session summary
if [ -f ".claude/logs/tool-usage.log" ]; then
    echo ""
    echo "📊 Session Summary:"
    echo "   Total tool calls: $(wc -l < .claude/logs/tool-usage.log)"
    echo "   Most used tool: $(sort .claude/logs/tool-usage.log | uniq -c | sort -rn | head -1 | awk '{print $3}')"
fi

exit 0
```

**Performance Target:** Non-blocking (session ending anyway)
**Type:** Shell or LLM
**Blocking:** No (session ends regardless)

---

## Hook Types

### Shell Hooks

**File Extension:** `.sh`

**Characteristics:**
- ✅ Fast execution (<100ms typical)
- ✅ Deterministic behavior
- ✅ Easy to test
- ✅ Low resource usage
- ❌ Limited to shell capabilities
- ❌ No context awareness

**Best For:**
- Validation (PreToolUse)
- Formatting (PostToolUse)
- Simple tracking
- File operations
- Environment checks

**Example:**
```bash
#!/bin/bash
# Must have shebang
# Must be executable: chmod +x hook.sh

TOOL_NAME="$1"
FILE_PATH="$2"

# Validation logic
if [ "$TOOL_NAME" = "Write" ]; then
    # Validate file
    if ! validate_file "$FILE_PATH"; then
        echo "❌ Validation failed"
        exit 1  # Block operation
    fi
fi

exit 0  # Allow operation
```

**Requirements:**
1. Shebang line (`#!/bin/bash` or `#!/bin/sh`)
2. Executable permissions (`chmod +x`)
3. Exit code 0 = allow, non-zero = block
4. POSIX-compliant (prefer `/bin/sh` over `/bin/bash`)

---

### LLM Hooks

**File Extensions:** `.ts`, `.js`, `.py`

**Characteristics:**
- ✅ Full context awareness
- ✅ Complex analysis
- ✅ Flexible logic
- ✅ Can make decisions
- ❌ Slower execution (1-3 seconds typical)
- ❌ Higher resource usage
- ❌ May require additional dependencies

**Best For:**
- Skill activation (UserPromptSubmit)
- Prompt enhancement
- Intent analysis
- Complex validation
- Context-aware decisions

**Example (TypeScript):**
```typescript
// .claude/hooks/UserPromptSubmit/skill-activation.ts

export async function skillActivationPrompt(prompt: string): Promise<string> {
  // Complex analysis
  const skills = await loadSkillRules();
  const intent = await analyzeIntent(prompt);
  const context = await gatherContext();

  const matches = findMatchingSkills(prompt, intent, context, skills);

  if (matches.length > 0) {
    return formatSuggestions(matches);
  }

  return "";
}
```

**Example (Python):**
```python
# .claude/hooks/Stop/session-summary.py

import os
import json
from datetime import datetime

def generate_session_summary():
    """Generate session summary from logs"""

    log_file = ".claude/logs/tool-usage.log"

    if not os.path.exists(log_file):
        return ""

    with open(log_file) as f:
        lines = f.readlines()

    tool_counts = {}
    for line in lines:
        tool = line.split("|")[2].strip()
        tool_counts[tool] = tool_counts.get(tool, 0) + 1

    summary = []
    summary.append("📊 Session Summary:")
    summary.append(f"   Total operations: {len(lines)}")

    for tool, count in sorted(tool_counts.items(), key=lambda x: x[1], reverse=True):
        summary.append(f"   {tool}: {count} calls")

    return "\n".join(summary)

if __name__ == "__main__":
    print(generate_session_summary())
```

**Requirements:**
1. Export async function (TypeScript/JavaScript)
2. Define function (Python)
3. Handle errors gracefully
4. Return appropriate value

---

## Configuration

### settings.json

**Location:** `.claude/settings.json`

**Structure:**
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
      }
    ],
    "PostToolUse": [
      {
        "type": "shell",
        "path": ".claude/hooks/PostToolUse/tool-tracker.sh"
      }
    ],
    "Stop": [
      {
        "type": "llm",
        "path": ".claude/hooks/Stop/error-handling-reminder.ts"
      }
    ]
  }
}
```

**Hook Properties:**
- `type` - "shell" or "llm"
- `path` - Relative path to hook file
- `enabled` (optional) - true/false (default: true)

**Multiple Hooks:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "type": "shell",
        "path": ".claude/hooks/PreToolUse/yaml-validation.sh"
      },
      {
        "type": "shell",
        "path": ".claude/hooks/PreToolUse/security-check.sh"
      }
    ]
  }
}
```
**Execution order:** As listed in array

---

## Hook Arguments

### Argument Passing

**Shell Hooks:**
```bash
#!/bin/bash
# Arguments passed as $1, $2, $3, etc.

TOOL_NAME="$1"      # PreToolUse, PostToolUse
FILE_PATH="$2"      # PreToolUse, PostToolUse
EXIT_CODE="$2"      # PostToolUse (exit code)
PROMPT="$1"         # UserPromptSubmit
```

**LLM Hooks (TypeScript):**
```typescript
// UserPromptSubmit hook
export async function userPromptSubmitHook(prompt: string): Promise<string> {
  // prompt: user's prompt text
  // Return: optional suggestion text
}

// PreToolUse hook
export async function preToolUseHook(
  toolName: string,
  args: any
): Promise<any> {
  // toolName: name of tool being called
  // args: arguments passed to tool
  // Return: modified args (or original to allow)
}

// PostToolUse hook
export async function postToolUseHook(
  toolName: string,
  result: any
): Promise<void> {
  // toolName: name of tool that was called
  // result: result from tool call
}

// Stop hook
export async function stopHook(
  context: SessionContext
): Promise<string> {
  // context: session context object
  // Return: optional reminder text
}
```

---

## Best Practices

### 1. Performance

**Target Times:**
- **SessionStart:** <2 seconds
- **UserPromptSubmit:** <1 second
- **PreToolUse:** <500ms
- **PostToolUse:** <1 second (can be async)
- **Stop:** Non-blocking

**Optimization Strategies:**

1. **Use shell hooks** for fast, deterministic operations
2. **Cache expensive operations** (load files once, cache in memory)
3. **Limit file scanning** (only scan necessary files)
4. **Use compiled regex** (pre-compile regex patterns)
5. **Break early** (return as soon as result determined)

**Example:**
```bash
#!/bin/bash
# ❌ BAD: Scans entire codebase
find . -name "*.py" -exec grep "TODO" {} \;

# ✅ GOOD: Only scans open files
for file in "$OPEN_FILES"; do
    grep "TODO" "$file"
done
```

---

### 2. Error Handling

**Always handle errors gracefully:**

```bash
#!/bin/bash
# ✅ GOOD: Handle errors

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Trap errors
trap 'echo "❌ Hook failed at line $LINENO"; exit 1' ERR

# Validate command exists
if ! command -v python &> /dev/null; then
    echo "⚠️  Python not found, skipping validation"
    exit 0  # Don't block, just skip
fi

# Try validation
if ! python tools/kb.py validate "$FILE" 2>&1; then
    echo "❌ Validation failed"
    exit 1  # Block the operation
fi

echo "✅ Validation passed"
exit 0
```

**Never break workflow:**
- Log errors
- Provide helpful error messages
- Exit gracefully
- Don't leave system in bad state

---

### 3. Testing

**Test hooks manually before deploying:**

```bash
# Test shell hook
bash .claude/hooks/PreToolUse/yaml-validation.sh "Write" "test.yaml"

# Test with actual file
bash .claude/hooks/PreToolUse/yaml-validation.sh "Write" "python/errors/test.yaml"
```

**Test edge cases:**
- Missing files
- Invalid input
- Empty input
- Large files
- Network failures

---

### 4. Security

**Security considerations:**

1. **Validate all input**
2. **Sanitize file paths**
3. **Don't execute user input directly**
4. **Check file permissions**
5. **Use absolute paths**

**Example:**
```bash
#!/bin/bash
# ❌ BAD: Executes user input
eval "$USER_COMMAND"

# ✅ GOOD: Validates and sanitizes
if [[ "$USER_COMMAND" =~ ^[a-zA-Z0-9_\-]+$ ]]; then
    "./$USER_COMMAND"
else
    echo "❌ Invalid command"
    exit 1
fi
```

---

### 5. Logging

**Log hook execution for debugging:**

```bash
#!/bin/bash

LOG_DIR=".claude/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/hooks.log"

log() {
    echo "$(date -Iseconds) | $1" >> "$LOG_FILE"
}

log "PreToolUse hook started"
log "Tool: $TOOL_NAME"
log "File: $FILE_PATH"

# ... hook logic ...

log "PreToolUse hook completed"
```

**Useful for:**
- Debugging hook issues
- Performance analysis
- Usage tracking
- Audit trail

---

## Production Examples

### Example 1: Complete skill-activation system

**Files:**
- `.claude/hooks/UserPromptSubmit/skill-activation.ts`
- `.claude/skill-rules.json`
- `.claude/settings.json`

**Implementation:** See `@resources/skill-activation.md`

---

### Example 2: Complete validation system

**Files:**
- `.claude/hooks/PreToolUse/yaml-validation.sh`
- `.claude/hooks/PreToolUse/python-syntax.sh`
- `.claude/hooks/PreToolUse/json-validation.sh`

**yaml-validation.sh:**
```bash
#!/bin/bash
TOOL_NAME="$1"
FILE_PATH="$2"

if [ "$TOOL_NAME" = "Write" ] && [[ "$FILE_PATH" == *.yaml ]]; then
    if [ -f "tools/kb.py" ]; then
        if ! python tools/kb.py validate "$FILE_PATH" 2>&1; then
            echo "❌ YAML validation failed"
            exit 1
        fi
    fi
fi

exit 0
```

**python-syntax.sh:**
```bash
#!/bin/bash
TOOL_NAME="$1"
FILE_PATH="$2"

if [ "$TOOL_NAME" = "Write" ] && [[ "$FILE_PATH" == *.py ]]; then
    if ! python -m py_compile "$FILE_PATH" 2>&1; then
        echo "❌ Python syntax error"
        exit 1
    fi
fi

exit 0
```

**json-validation.sh:**
```bash
#!/bin/bash
TOOL_NAME="$1"
FILE_PATH="$2"

if [ "$TOOL_NAME" = "Write" ] && [[ "$FILE_PATH" == *.json ]]; then
    if ! jq empty "$FILE_PATH" 2>&1; then
        echo "❌ Invalid JSON"
        exit 1
    fi
fi

exit 0
```

---

### Example 3: Complete tracking system

**Files:**
- `.claude/hooks/PostToolUse/tool-tracker.sh`
- `.claude/hooks/Stop/session-summary.sh`

**tool-tracker.sh:**
```bash
#!/bin/bash
TOOL_NAME="$1"
RESULT="$2"

LOG_FILE=".claude/logs/tool-usage.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "$(date -Iseconds) | $TOOL_NAME" >> "$LOG_FILE"
```

**session-summary.sh:**
```bash
#!/bin/bash
LOG_FILE=".claude/logs/tool-usage.log"

if [ ! -f "$LOG_FILE" ]; then
    exit 0
fi

echo ""
echo "📊 Session Summary:"
echo "   Total operations: $(wc -l < "$LOG_FILE")"
echo "   Most used tool:"
    sort "$LOG_FILE" | uniq -c | sort -rn | head -1 | \
    awk '{print "     " $2 " (" $1 " calls)"}'
```

---

## Troubleshooting

### Hook Not Firing

**Checklist:**
1. ✅ Hook file exists?
2. ✅ Hook executable? (`chmod +x`)
3. ✅ Hook registered in settings.json?
4. ✅ JSON syntax valid in settings.json?
5. ✅ Correct event selected?
6. ✅ Claude Code restarted?

**Common fixes:**
- Make shell hooks executable
- Verify settings.json syntax
- Restart Claude Code after changes
- Check hook file permissions
- Test hook manually

---

### Hook Performance Issues

**Symptoms:**
- Slow session start
- Laggy tool calls
- Unresponsive UI

**Solutions:**
1. Profile hook execution time
2. Optimize expensive operations
3. Use shell hooks instead of LLM
4. Cache results
5. Limit file scanning

---

### Hook Blocking Operations

**Problem:** Hook blocks valid operations

**Solutions:**
1. Review hook logic
2. Add more specific validation
3. Add debug logging
4. Test edge cases
5. Use `enabled: false` temporarily

---

## Related Resources

**Internal:**
- `@resources/system-overview.md` - Complete system architecture
- `@resources/skill-activation.md` - Skill activation implementation

**Shared KB:**
- `universal/patterns/claude-code-hooks.yaml` - Hooks pattern

**External:**
- [Bash Scripting Guide](https://www.shellcheck.net/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** diet103 Claude Code Infrastructure Showcase (6 months production)
