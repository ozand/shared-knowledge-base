# Post Tool Use Tracking Hook

Example of tracking tool usage for analytics.

---

## Overview

**Purpose:** Track all tool calls for analytics and monitoring

**Event:** PostToolUse

**Type:** Shell hook

**Location:** `.claude/hooks/PostToolUse/tool-tracker.sh`

---

## Implementation

### Complete Code

```bash
#!/bin/bash
# .claude/hooks/PostToolUse/tool-tracker.sh

TOOL_NAME="$1"
EXIT_CODE="${2:-0}"
TIMESTAMP=$(date -Iseconds)

# Configuration
LOG_DIR=".claude/logs"
LOG_FILE="$LOG_DIR/tool-usage.log"
STATS_FILE="$LOG_DIR/tool-stats.json"

# Create log directory
mkdir -p "$LOG_DIR"

# Log usage
echo "$TIMESTAMP | $TOOL_NAME | exit: $EXIT_CODE" >> "$LOG_FILE"

# Update statistics
update_stats() {
    local tool="$1"
    local stats_file="$2"

    # Initialize stats file if needed
    if [ ! -f "$stats_file" ]; then
        echo "{}" > "$stats_file"
    fi

    # Update using jq (if available)
    if command -v jq &> /dev/null; then
        jq --arg tool "$tool" '
            if has($tool) then
                .[$tool] += 1
            else
                .[$tool] = 1
            end
        ' "$stats_file" > "$stats_file.tmp"
        mv "$stats_file.tmp" "$stats_file"
    else
        # Fallback: append to JSON manually
        # Note: This is a simplified fallback
        echo "{\"$tool\": 1}" >> "$stats_file.fallback"
    fi
}

update_stats "$TOOL_NAME" "$STATS_FILE"

# Optional: Display notification
case "$TOOL_NAME" in
    Write)
        if [ "$EXIT_CODE" -eq 0 ]; then
            echo "📝 Write logged successfully"
        else
            echo "⚠️  Write failed (exit: $EXIT_CODE)"
        fi
        ;;
    Bash)
        echo "💻 Bash command logged (exit: $EXIT_CODE)"
        ;;
    Read)
        echo "📖 Read logged"
        ;;
esac

exit 0
```

---

## Enhanced Version

With session tracking and error reporting:

```bash
#!/bin/bash
# .claude/hooks/PostToolUse/tool-tracker-enhanced.sh

TOOL_NAME="$1"
EXIT_CODE="${2:-0}"
TIMESTAMP=$(date -Iseconds)
SESSION_ID="${CLAUDE_SESSION_ID:-unknown}"

LOG_DIR=".claude/logs"
LOG_FILE="$LOG_DIR/tool-usage.log"
STATS_FILE="$LOG_DIR/tool-stats.json"
ERROR_LOG="$LOG_DIR/errors.log"

mkdir -p "$LOG_DIR"

# Enhanced logging with session ID
log_entry() {
    local timestamp="$1"
    local session="$2"
    local tool="$3"
    local exit_code="$4"

    echo "$timestamp | session: $session | $tool | exit: $exit_code" >> "$LOG_FILE"
}

log_entry "$TIMESTAMP" "$SESSION_ID" "$TOOL_NAME" "$EXIT_CODE"

# Error tracking
if [ "$EXIT_CODE" -ne 0 ]; then
    echo "$TIMESTAMP | session: $SESSION_ID | $TOOL_NAME | exit: $EXIT_CODE" >> "$ERROR_LOG"
fi

# Statistics with success/failure tracking
update_enhanced_stats() {
    local tool="$1"
    local exit_code="$2"
    local stats_file="$3"

    if [ ! -f "$stats_file" ]; then
        echo "{}" > "$stats_file"
    fi

    if command -v jq &> /dev/null; then
        jq --arg tool "$tool" \
           --argjson success "$([ "$exit_code" -eq 0 ] && echo 1 || echo 0)" \
           --argjson failure "$([ "$exit_code" -ne 0 ] && echo 1 || echo 0)" '
            if has($tool) then
                .[$tool].total += 1
                .[$tool].success += $success
                .[$tool].failure += $failure
            else
                .[$tool] = {
                    "total": 1,
                    "success": $success,
                    "failure": $failure
                }
            end
        ' "$stats_file" > "$stats_file.tmp"
        mv "$stats_file.tmp" "$stats_file"
    fi
}

update_enhanced_stats "$TOOL_NAME" "$EXIT_CODE" "$STATS_FILE"

# Session summary generation
generate_session_summary() {
    local session="$1"
    local log_file="$2"

    # Count operations for this session
    local count=$(grep "session: $session" "$log_file" | wc -l)

    # Count errors
    local errors=$(grep "session: $session" "$ERROR_LOG" 2>/dev/null | wc -l)

    echo "📊 Session: $session | Operations: $count | Errors: $errors"
}

# Generate summary on Stop (when tool name is "Stop")
if [ "$TOOL_NAME" = "Stop" ]; then
    generate_session_summary "$SESSION_ID" "$LOG_FILE"
fi

exit 0
```

---

## Configuration

### settings.json

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "type": "shell",
        "path": ".claude/hooks/PostToolUse/tool-tracker.sh"
      }
    ]
  }
}
```

---

## Output Examples

### Log File

```
2026-01-07T10:30:15+00:00 | Read | exit: 0
2026-01-07T10:30:18+00:00 | Write | exit: 0
2026-01-07T10:30:22+00:00 | Bash | exit: 0
2026-01-07T10:30:25+00:00 | Read | exit: 0
2026-01-07T10:30:30+00:00 | Bash | exit: 1
```

### Statistics File

```json
{
  "Read": 45,
  "Write": 23,
  "Bash": 67,
  "Grep": 12
}
```

### Enhanced Statistics

```json
{
  "Read": {
    "total": 45,
    "success": 45,
    "failure": 0
  },
  "Bash": {
    "total": 67,
    "success": 65,
    "failure": 2
  }
}
```

---

## Analytics Script

### Analyze Usage

```bash
#!/bin/bash
# .claude/scripts/analyze-usage.sh

LOG_FILE=".claude/logs/tool-usage.log"

if [ ! -f "$LOG_FILE" ]; then
    echo "No usage data found"
    exit 1
fi

echo "📊 Tool Usage Analytics"
echo ""

# Total operations
total=$(wc -l < "$LOG_FILE")
echo "Total operations: $total"

# By tool
echo ""
echo "By tool:"
awk -F '|' '{print $3}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -10

# Error rate
echo ""
echo "Error rate:"
errors=$(grep "exit: [^0]" "$LOG_FILE" | wc -l)
rate=$(echo "scale=1; $errors * 100 / $total" | bc)
echo "$errors errors ($rate%)"

# Recent activity
echo ""
echo "Recent activity:"
tail -5 "$LOG_FILE"
```

---

## Testing

### Manual Testing

```bash
# Test hook
bash .claude/hooks/PostToolUse/tool-tracker.sh "Write" "0"

# Check log
cat .claude/logs/tool-usage.log

# Check stats
cat .claude/logs/tool-stats.json | jq .
```

### Automated Testing

```python
# test_tool_tracker.py

import subprocess
import json
import time

def test_tool_tracker():
    """Test tool tracking hook"""
    # Execute hook multiple times
    tools = ["Read", "Write", "Bash"]

    for tool in tools:
        subprocess.run([
            "bash",
            ".claude/hooks/PostToolUse/tool-tracker.sh",
            tool,
            "0"
        ])

    # Check log file
    with open(".claude/logs/tool-usage.log") as f:
        log_content = f.read()
        assert "Read" in log_content
        assert "Write" in log_content
        assert "Bash" in log_content

    # Check stats file
    with open(".claude/logs/tool-stats.json") as f:
        stats = json.load(f)
        assert stats["Read"] >= 1
        assert stats["Write"] >= 1
        assert stats["Bash"] >= 1

    print("✅ Tool tracking tests passed")

if __name__ == "__main__":
    test_tool_tracker()
```

---

## Performance

**Target:** <1 second (can be async)

**Optimization:**
- Minimal shell operations
- File I/O is fast (<10ms)
- jq operations are fast (<50ms)
- No blocking operations

---

## Extensions

### 1. Performance Tracking

Track time spent in each tool:

```bash
#!/bin/bash
# Add timing information
START_TIME=$(date +%s%N)
# ... tool execution ...
END_TIME=$(date +%s%N)
ELAPSED=$((($END_TIME - $START_TIME) / 1000000))  # Convert to ms
echo "$TIMESTAMP | $TOOL_NAME | time: ${ELAPSED}ms" >> "$LOG_FILE"
```

### 2. File Size Tracking

Track file sizes for Read/Write:

```bash
#!/bin/bash
if [ "$TOOL_NAME" = "Read" ] || [ "$TOOL_NAME" = "Write" ]; then
    FILE_PATH="$3"
    if [ -f "$FILE_PATH" ]; then
        FILE_SIZE=$(wc -c < "$FILE_PATH")
        echo "$TIMESTAMP | $TOOL_NAME | size: $FILE_SIZE bytes" >> "$LOG_FILE"
    fi
fi
```

---

**Version:** 1.0
**Last Updated:** 2026-01-07
