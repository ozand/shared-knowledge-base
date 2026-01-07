# Hook Implementation Patterns

Production-tested patterns for common hook implementations.

---

## Pattern 1: Validation Hook

### Purpose

Validate operations before execution

### Event

PreToolUse (blocking)

### Implementation

```bash
#!/bin/bash
# .claude/hooks/PreToolUse/validate-yaml.sh

TOOL_NAME="$1"
FILE_PATH="$2"

# Validate YAML files before Write
if [ "$TOOL_NAME" = "Write" ]; then
    if [[ "$FILE_PATH" == *.yaml ]] || [[ "$FILE_PATH" == *.yml ]]; then
        if [ -f "tools/kb.py" ]; then
            if ! python tools/kb.py validate "$FILE_PATH" 2>&1; then
                echo "❌ YAML validation failed"
                exit 1  # Block operation
            fi
        fi
    fi
fi

exit 0
```

### Key Points

- Returns non-zero to block operation
- Returns zero to allow operation
- Fast shell execution
- Clear error messages

---

## Pattern 2: Enhancement Hook

### Purpose

Enhance user prompt with context

### Event

UserPromptSubmit (non-blocking)

### Implementation

```typescript
// .claude/hooks/UserPromptSubmit/enhance-prompt.ts

export async function enhancePrompt(prompt: string): Promise<string> {
  const context = await gatherContext();

  // Add context if not present
  if (!prompt.includes("context") && context) {
    return `${prompt}\n\nContext: ${context}`;
  }

  return prompt;
}

async function gatherContext(): Promise<string> {
  // Gather relevant context
  const fs = require('fs').promises;

  if (await fs.access('.claude/CONTEXT.md').then(() => true).catch(() => false)) {
    const context = await fs.readFile('.claude/CONTEXT.md', 'utf-8');
    return context.slice(0, 500);  // First 500 chars
  }

  return "";
}
```

### Key Points

- Returns enhanced prompt (or empty string)
- Non-blocking (user can ignore)
- Adds value without changing intent
- Respects user's original prompt

---

## Pattern 3: Tracking Hook

### Purpose

Track tool usage for analytics

### Event

PostToolUse (non-blocking)

### Implementation

```bash
#!/bin/bash
# .claude/hooks/PostToolUse/track-usage.sh

TOOL_NAME="$1"
EXIT_CODE="$2"

LOG_FILE=".claude/logs/tool-usage.log"
mkdir -p "$(dirname "$LOG_FILE")"

# Log usage
echo "$(date -Iseconds) | $TOOL_NAME | exit: $EXIT_CODE" >> "$LOG_FILE"

# Update statistics
STATS_FILE=".claude/logs/tool-stats.json"
if [ ! -f "$STATS_FILE" ]; then
  echo "{}" > "$STATS_FILE"
fi

# Update stats (requires jq)
if command -v jq &> /dev/null; then
  jq --arg tool "$TOOL_NAME" '
    if has($tool) then
      .[$tool] += 1
    else
      .[$tool] = 1
    end
  ' "$STATS_FILE" > "$STATS_FILE.tmp"
  mv "$STATS_FILE.tmp" "$STATS_FILE"
fi

exit 0
```

### Key Points

- Non-blocking (operation already completed)
- Logs to file for later analysis
- Updates statistics
- Handles missing files gracefully

---

## Pattern 4: Notification Hook

### Purpose

Send notifications on events

### Event

PostToolUse or Stop

### Implementation

```bash
#!/bin/bash
# .claude/hooks/PostToolUse/notify.sh

TOOL_NAME="$1"

# Send desktop notification (Linux)
if command -v notify-send &> /dev/null; then
    case "$TOOL_NAME" in
        Write)
            notify-send "Claude Code" "File written"
            ;;
        Bash)
            notify-send "Claude Code" "Command executed"
            ;;
    esac
fi

exit 0
```

### Key Points

- Optional functionality
- Checks if command available
- Graceful degradation
- User-friendly notifications

---

## Pattern 5: Transformation Hook

### Purpose

Transform tool arguments before execution

### Event

PreToolUse

### Implementation

```typescript
// .claude/hooks/PreToolUse/transform-args.ts

export async function transformArgs(
  toolName: string,
  args: any
): Promise<any> {
  // Add line numbers to Read tool for large files
  if (toolName === "Read") {
    if (!args.offset && !args.limit) {
      const fileSize = await getFileSize(args.file_path);

      if (fileSize > 10000) {  # >10KB
        console.log("📄 Large file, reading first 200 lines");
        args.offset = 1;
        args.limit = 200;
      }
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

### Key Points

- Modifies arguments before tool execution
- Adds smart defaults
- Preserves original behavior
- Transparent to user

---

## Pattern 6: Cleanup Hook

### Purpose

Clean up resources at session end

### Event

Stop

### Implementation

```bash
#!/bin/bash
# .claude/hooks/Stop/cleanup.sh

# Remove temporary files
if [ -d ".claude/tmp" ]; then
    rm -rf .claude/tmp/*
    echo "🧹 Cleanup complete"
fi

# Rotate logs
LOG_FILE=".claude/logs/tool-usage.log"
if [ -f "$LOG_FILE" ]; then
    LINES=$(wc -l < "$LOG_FILE")
    if [ $LINES -gt 1000 ]; then
        # Keep last 1000 lines
        tail -n 1000 "$LOG_FILE" > "$LOG_FILE.tmp"
        mv "$LOG_FILE.tmp" "$LOG_FILE"
        echo "📋 Logs rotated"
    fi
fi

exit 0
```

### Key Points

- Non-blocking (session ending)
- Handles resource cleanup
- Log rotation
- Prevents disk space issues

---

## Pattern Selection Guide

| Pattern | Event | Type | Use When |
|---------|-------|------|----------|
| **Validation** | PreToolUse | Shell | Need to block operation |
| **Enhancement** | UserPromptSubmit | LLM | Add context to prompt |
| **Tracking** | PostToolUse | Shell | Log tool usage |
| **Notification** | PostToolUse | Shell | Send notifications |
| **Transformation** | PreToolUse | LLM | Modify arguments |
| **Cleanup** | Stop | Shell | Clean up resources |

---

## Best Practices

1. **Choose right event** for your use case
2. **Respect performance targets**
3. **Handle errors gracefully**
4. **Test thoroughly**
5. **Provide clear feedback**

---

**Version:** 1.0
**Last Updated:** 2026-01-07
