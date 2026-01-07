# Hook Events Reference

Complete reference for all Claude Code hook events.

---

## Event Summary

| Event | When Fired | Purpose | Max Duration | Blocking |
|-------|-----------|---------|--------------|----------|
| **SessionStart** | Session starts | Initial setup | 2 seconds | No |
| **UserPromptSubmit** | After prompt | Skill activation | 1 second | No |
| **PreToolUse** | Before tool call | Validation | 500ms | Yes |
| **PostToolUse** | After tool call | Tracking | 1 second | No |
| **Stop** | Session ends | Quality check | Non-blocking | No |

---

## 1. SessionStart

### Purpose

Initialize session, validate environment, load context.

### When Fired

Immediately when Claude Code session starts, before any user interaction.

### Arguments

None (no arguments passed)

### Return Value

None (return value ignored)

### Use Cases

1. **Environment Validation**
   - Check required tools installed
   - Verify environment variables
   - Validate configuration

2. **Context Loading**
   - Load project context
   - Initialize state
   - Set up environment

3. **Notifications**
   - Display welcome messages
   - Show setup instructions
   - Provide status information

### Example: Environment Validation

```bash
#!/bin/bash
# .claude/hooks/SessionStart/validate-env.sh

echo "🔍 Validating environment..."

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python not found"
    echo "Install Python: https://www.python.org/downloads/"
    exit 1
fi
echo "✅ Python: $(python --version)"

# Check Node
if ! command -v node &> /dev/null; then
    echo "⚠️  Node not found (optional)"
else
    echo "✅ Node: $(node --version)"
fi

# Check KB index
if [ ! -f ".kb/index.db" ]; then
    echo "⚠️  KB index not found"
    echo "Run: python tools/kb.py index -v"
fi

echo "✅ Environment ready"
```

### Example: Context Loading

```bash
#!/bin/bash
# .claude/hooks/SessionStart/load-context.sh

CONTEXT_FILE=".claude/CONTEXT.md"

if [ -f "$CONTEXT_FILE" ]; then
    echo "📖 Loading project context..."
    cat "$CONTEXT_FILE"
    echo "✅ Context loaded"
else
    echo "ℹ️  No project context found"
    echo "   Create .claude/CONTEXT.md to provide context"
fi
```

---

## 2. UserPromptSubmit

### Purpose

Analyze user prompt, suggest skills, enhance prompt.

### When Fired

After user submits prompt, before Claude processes it.

### Arguments

- `prompt: string` - User's prompt text

### Return Value

- `string` - Optional suggestion text to display to user

### Use Cases

1. **Skill Activation** (BREAKTHROUGH)
   - Analyze prompt intent
   - Match against skill rules
   - Suggest relevant skills

2. **Prompt Enhancement**
   - Add context
   - Suggest improvements
   - Fill in missing details

3. **Intent Analysis**
   - Extract user intent
   - Identify task type
   - Classify request

### Example: Skill Activation

```typescript
// .claude/hooks/UserPromptSubmit/skill-activation.ts

interface SkillRule {
  promptTriggers: {
    keywords: string[];
    intentPatterns?: string[];
  };
  description: string;
}

export async function skillActivationPrompt(prompt: string): Promise<string> {
  const skills = await loadSkillRules();
  const matches = findMatches(prompt, skills);

  if (matches.length === 0) {
    return "";
  }

  const suggestions = matches
    .slice(0, 3)
    .map(m => `• ${m.name}: ${m.description}`)
    .join("\n");

  return `\nBased on your request, consider using:\n${suggestions}`;
}

async function loadSkillRules(): Promise<Record<string, SkillRule>> {
  const fs = require('fs').promises;
  const content = await fs.readFile('.claude/skill-rules.json', 'utf-8');
  return JSON.parse(content);
}

function findMatches(prompt: string, rules: Record<string, SkillRule>) {
  const matches = [];

  for (const [name, rule] of Object.entries(rules)) {
    const keywords = rule.promptTriggers.keywords || [];
    const hasMatch = keywords.some(kw =>
      prompt.toLowerCase().includes(kw.toLowerCase())
    );

    if (hasMatch) {
      matches.push({ name, description: rule.description });
    }
  }

  return matches;
}
```

---

## 3. PreToolUse

### Purpose

Validate, block, or transform tool calls.

### When Fired

Before any tool call (Read, Write, Bash, etc.)

### Arguments

- `toolName: string` - Name of tool being called
- `args: any` - Arguments passed to tool

### Return Value

- Shell: Exit code (0 = allow, non-zero = block)
- LLM: Modified args (or original to allow)

### Use Cases

1. **Validation**
   - Validate file syntax
   - Check file permissions
   - Verify data format

2. **Blocking**
   - Prevent dangerous operations
   - Block specific commands
   - Enforce policies

3. **Transformation**
   - Modify arguments
   - Add default values
   - Normalize input

### Example: YAML Validation

```bash
#!/bin/bash
# .claude/hooks/PreToolUse/yaml-validation.sh

TOOL_NAME="$1"
FILE_PATH="$2"

if [ "$TOOL_NAME" = "Write" ]; then
    if [[ "$FILE_PATH" == *.yaml ]] || [[ "$FILE_PATH" == *.yml ]]; then
        if [ -f "tools/kb.py" ]; then
            if ! python tools/kb.py validate "$FILE_PATH" 2>&1; then
                echo "❌ YAML validation failed"
                exit 1
            fi
        fi
    fi
fi

exit 0
```

### Example: Security Check

```bash
#!/bin/bash
# .claude/hooks/PreToolUse/security-check.sh

TOOL_NAME="$1"
COMMAND="$2"

if [ "$TOOL_NAME" = "Bash" ]; then
    DANGEROUS=(
        "rm -rf /"
        "rm -rf /*"
        ":(){ :|:& };:"
    )

    for pattern in "${DANGEROUS[@]}"; do
        if echo "$COMMAND" | grep -q "$pattern"; then
            echo "❌ Dangerous command blocked"
            exit 1
        fi
    done
fi

exit 0
```

---

## 4. PostToolUse

### Purpose

Track, format, notify after tool calls.

### When Fired

After successful tool call

### Arguments

- `toolName: string` - Name of tool that was called
- `result: any` - Result from tool call
- `exitCode?: number` - Exit code (for Bash tool)

### Return Value

None (return value ignored)

### Use Cases

1. **Tracking**
   - Log tool usage
   - Track analytics
   - Monitor performance

2. **Formatting**
   - Auto-format output
   - Pretty-print results
   - Apply standards

3. **Notifications**
   - Send notifications
   - Update status
   - Trigger workflows

### Example: Tool Tracking

```bash
#!/bin/bash
# .claude/hooks/PostToolUse/tool-tracker.sh

TOOL_NAME="$1"
EXIT_CODE="$2"

LOG_FILE=".claude/logs/tool-usage.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "$(date -Iseconds) | $TOOL_NAME | exit: $EXIT_CODE" >> "$LOG_FILE"

case "$TOOL_NAME" in
    Write) echo "📝 Write logged" ;;
    Bash) echo "💻 Bash logged" ;;
    Read) echo "📖 Read logged" ;;
esac

exit 0
```

### Example: Auto-Format

```bash
#!/bin/bash
# .claude/hooks/PostToolUse/auto-format.sh

TOOL_NAME="$1"
FILE_PATH="$2"

if [ "$TOOL_NAME" = "Write" ]; then
    if [[ "$FILE_PATH" == *.py ]]; then
        if command -v black &> /dev/null; then
            black "$FILE_PATH" --quiet
            echo "✅ Formatted with black"
        fi
    fi

    if [[ "$FILE_PATH" == *.json ]]; then
        if command -v jq &> /dev/null; then
            jq '.' "$FILE_PATH" > "${FILE_PATH}.tmp"
            mv "${FILE_PATH}.tmp" "$FILE_PATH"
            echo "✅ Formatted JSON"
        fi
    fi
fi

exit 0
```

---

## 5. Stop

### Purpose

Quality validation, reminders, cleanup at session end.

### When Fired

When Claude finishes session (user exit or timeout)

### Arguments

- `context: SessionContext` - Session context object
  - `errorsThrown: boolean`
  - `hasUncommittedChanges: boolean`
  - `hasUnpushedCommits: boolean`

### Return Value

- `string` - Optional reminder text to display

### Use Cases

1. **Quality Validation**
   - Check work completed
   - Validate outputs
   - Review changes

2. **Reminders**
   - Forgotten pushes
   - Uncommitted changes
   - Undocumented errors

3. **Cleanup**
   - Remove temp files
   - Clear cache
   - Close connections

### Example: Error Handling Reminder

```typescript
// .claude/hooks/Stop/error-handling-reminder.ts

export async function errorHandlingReminder(
  context: {
    errorsThrown: boolean;
    hasUncommittedChanges: boolean;
    hasUnpushedCommits: boolean;
  }
): Promise<string> {
  const reminders: string[] = [];

  if (context.errorsThrown) {
    reminders.push("⚠️  Errors were thrown during this session");
    reminders.push("   Consider documenting them in the KB");
  }

  if (context.hasUncommittedChanges) {
    reminders.push("📝 You have uncommitted changes");
    reminders.push("   Don't forget to commit your work");
  }

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

### Example: Cleanup

```bash
#!/bin/bash
# .claude/hooks/Stop/cleanup.sh

# Remove temp files
if [ -d ".claude/tmp" ]; then
    rm -rf .claude/tmp/*
    echo "🧹 Cleanup complete"
fi

# Session summary
if [ -f ".claude/logs/tool-usage.log" ]; then
    echo ""
    echo "📊 Session Summary:"
    echo "   Total operations: $(wc -l < .claude/logs/tool-usage.log)"
fi

exit 0
```

---

## Hook Execution Order

### Sequence Diagram

```
Session Start
  ↓
SessionStart hooks fire
  ↓
User submits prompt
  ↓
UserPromptSubmit hooks fire
  ↓
Claude processes prompt
  ↓
Claude calls tool
  ↓
PreToolUse hooks fire
  ↓ (if all pass)
Tool executes
  ↓
PostToolUse hooks fire
  ↓
Result returned to Claude
  ↓ (repeat for more tools)
User finishes session
  ↓
Stop hooks fire
  ↓
Session ends
```

---

## Best Practices

### 1. Choose Right Event

- **SessionStart** - One-time setup
- **UserPromptSubmit** - Prompt analysis, skill activation
- **PreToolUse** - Validation, blocking
- **PostToolUse** - Tracking, formatting
- **Stop** - Quality, reminders

### 2. Respect Performance Targets

- SessionStart: <2 seconds
- UserPromptSubmit: <1 second
- PreToolUse: <500ms
- PostToolUse: <1 second
- Stop: Non-blocking

### 3. Handle Errors Gracefully

- Log errors
- Provide helpful messages
- Don't break workflow
- Exit gracefully

### 4. Test Thoroughly

- Test manually
- Test edge cases
- Test performance
- Test in production

---

**Version:** 1.0
**Last Updated:** 2026-01-07
