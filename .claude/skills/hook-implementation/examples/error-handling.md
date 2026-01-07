# Error Handling Reminder Hook

Example of reminding users to document errors and complete work.

---

## Overview

**Purpose:** Remind user to document errors, commit changes, push commits

**Event:** Stop

**Type:** LLM hook (TypeScript)

**Location:** `.claude/hooks/Stop/error-handling-reminder.ts`

---

## Implementation

### Complete Code

```typescript
// .claude/hooks/Stop/error-handling-reminder.ts

interface SessionContext {
  errorsThrown: boolean;
  hasUncommittedChanges: boolean;
  hasUnpushedCommits: boolean;
  hasOpenFiles?: boolean;
  sessionDuration?: number;
}

export async function errorHandlingReminder(
  context: SessionContext
): Promise<string> {
  const reminders: string[] = [];

  // Check for errors thrown
  if (context.errorsThrown) {
    reminders.push("⚠️  Errors were thrown during this session");
    reminders.push("   Consider documenting them in the KB");

    // Suggest workflow
    reminders.push("");
    reminders.push("   💡 Workflow:");
    reminders.push("      1. Review error messages");
    reminders.push("      2. Identify root cause");
    reminders.push("      3. Document in YAML format");
    reminders.push("      4. Validate: python tools/kb.py validate <file>");
    reminders.push("      5. Commit and push");
  }

  // Check for uncommitted changes
  if (context.hasUncommittedChanges) {
    if (reminders.length > 0) {
      reminders.push("");
    }
    reminders.push("📝 You have uncommitted changes");
    reminders.push("   Don't forget to commit your work");

    // Suggest git workflow
    reminders.push("");
    reminders.push("   💡 Workflow:");
    reminders.push("      git status");
    reminders.push("      git add <files>");
    reminders.push('      git commit -m "Add: Description"');
    reminders.push("      git push");
  }

  // Check for unpushed commits
  if (context.hasUnpushedCommits) {
    if (reminders.length > 0 && !context.hasUncommittedChanges) {
      reminders.push("");
    }
    reminders.push("⬆️  You have unpushed commits");
    reminders.push("   Consider pushing to remote");

    // Suggest push command
    reminders.push("");
    reminders.push("   💡 Command:");
    reminders.push("      git push origin <branch>");
  }

  // Session duration (optional)
  if (context.sessionDuration && context.sessionDuration > 3600000) {  # >1 hour
    if (reminders.length > 0) {
      reminders.push("");
    }
    const duration = Math.round(context.sessionDuration / 60000);  # minutes
    reminders.push(`⏱️  Session duration: ${duration} minutes`);
    reminders.push("   Consider taking a break");
  }

  // Format output
  if (reminders.length > 0) {
    return "\n" + reminders.join("\n");
  }

  return "";
}

// Helper function to detect errors
export async function detectErrors(): Promise<boolean> {
  const fs = require('fs').promises;

  try {
    // Check for error logs
    const errorLog = '.claude/logs/errors.log';
    if (await fs.access(errorLog).then(() => true).catch(() => false)) {
      const content = await fs.readFile(errorLog, 'utf-8');
      const recentErrors = content.split('\n').filter(line => {
        const timestamp = line.split('|')[0];
        const errorTime = new Date(timestamp);
        const hourAgo = new Date(Date.now() - 3600000);
        return errorTime > hourAgo;
      });

      return recentErrors.length > 0;
    }

    return false;
  } catch (error) {
    return false;
  }
}

// Helper function to check git status
export async function checkGitStatus(): Promise<{
  hasUncommittedChanges: boolean;
  hasUnpushedCommits: boolean;
}> {
  const { execSync } = require('child_process');

  try {
    // Check for uncommitted changes
    const status = execSync('git status --porcelain', {
      encoding: 'utf-8',
      cwd: process.cwd()
    });
    const hasUncommittedChanges = status.trim().length > 0;

    // Check for unpushed commits
    const log = execSync('git log @{u}.. --oneline', {
      encoding: 'utf-8',
      cwd: process.cwd()
    });
    const hasUnpushedCommits = log.trim().length > 0;

    return { hasUncommittedChanges, hasUnpushedCommits };
  } catch (error) {
    // Not a git repository or git not available
    return { hasUncommittedChanges: false, hasUnpushedCommits: false };
  }
}
```

---

## Simplified Version

For quick implementation:

```typescript
// .claude/hooks/Stop/error-handling-reminder-simple.ts

export async function errorHandlingReminder(
  context: {
    errorsThrown: boolean;
    hasUncommittedChanges: boolean;
    hasUnpushedCommits: boolean;
  }
): Promise<string> {
  const reminders: string[] = [];

  if (context.errorsThrown) {
    reminders.push("⚠️  Errors were thrown - document in KB");
  }

  if (context.hasUncommittedChanges) {
    reminders.push("📝 Uncommitted changes - don't forget to commit");
  }

  if (context.hasUnpushedCommits) {
    reminders.push("⬆️  Unpushed commits - consider pushing");
  }

  if (reminders.length > 0) {
    return "\n" + reminders.join("\n");
  }

  return "";
}
```

---

## Shell Version

Alternative implementation in bash:

```bash
#!/bin/bash
# .claude/hooks/Stop/error-handling-reminder.sh

reminders=()

# Check for errors
if [ -f ".claude/logs/errors.log" ]; then
    recent_errors=$(grep "$(date -Iminutes | cut -d'+' -f1)" .claude/logs/errors.log)
    if [ -n "$recent_errors" ]; then
        reminders+=("⚠️  Errors were thrown - document in KB")
    fi
fi

# Check git status
if git rev-parse --git-dir > /dev/null 2>&1; then
    # Uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        reminders+=("📝 Uncommitted changes")
    fi

    # Unpushed commits
    unpushed=$(git log @{u}.. --oneline 2>/dev/null)
    if [ -n "$unpushed" ]; then
        reminders+=("⬆️  Unpushed commits")
    fi
fi

# Print reminders
if [ ${#reminders[@]} -gt 0 ]; then
    echo ""
    for reminder in "${reminders[@]}"; do
        echo "$reminder"
    done
fi

exit 0
```

---

## Configuration

### settings.json

```json
{
  "hooks": {
    "Stop": [
      {
        "type": "llm",
        "path": ".claude/hooks/Stop/error-handling-reminder.ts"
      }
    ]
  }
}
```

---

## Context Integration

### How Context is Provided

The context object is populated by Claude Code:

```typescript
interface SessionContext {
  errorsThrown: boolean;          // Were any errors thrown?
  hasUncommittedChanges: boolean;  // Are there uncommitted git changes?
  hasUnpushedCommits: boolean;     // Are there unpushed git commits?
  hasOpenFiles: boolean;           // Are there open files?
  sessionDuration: number;         // Session duration in milliseconds
}
```

---

## Testing

### Manual Testing

```bash
# Test with ts-node (if available)
ts-node .claude/hooks/Stop/error-handling-reminder.ts << 'EOF'
{
  "errorsThrown": true,
  "hasUncommittedChanges": true,
  "hasUnpushedCommits": false
}
EOF

# Expected output:
# ⚠️  Errors were thrown during this session
#    Consider documenting them in the KB
#
# 📝 You have uncommitted changes
#    Don't forget to commit your work
```

### Automated Testing

```python
# test_error_reminder.py

import subprocess
import json

def test_error_reminder():
    """Test error handling reminder"""
    test_contexts = [
        {
            "errorsThrown": True,
            "hasUncommittedChanges": False,
            "hasUnpushedCommits": False
        },
        {
            "errorsThrown": False,
            "hasUncommittedChanges": True,
            "hasUnpushedCommits": True
        },
        {
            "errorsThrown": False,
            "hasUncommittedChanges": False,
            "hasUnpushedCommits": False
        }
    ]

    for i, context in enumerate(test_contexts):
        print(f"\nTest {i + 1}: {context}")

        # Execute hook
        result = subprocess.run(
            ["ts-node", ".claude/hooks/Stop/error-handling-reminder.ts"],
            input=json.dumps(context),
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()

        # Verify output
        if context["errorsThrown"]:
            assert "Errors were thrown" in output
        if context["hasUncommittedChanges"]:
            assert "Uncommitted changes" in output
        if context["hasUnpushedCommits"]:
            assert "Unpushed commits" in output

        print(f"Output:\n{output}")

    print("\n✅ All tests passed")

if __name__ == "__main__":
    test_error_reminder()
```

---

## Output Examples

### Example 1: Errors Only

```
⚠️  Errors were thrown during this session
   Consider documenting them in the KB

   💡 Workflow:
      1. Review error messages
      2. Identify root cause
      3. Document in YAML format
      4. Validate: python tools/kb.py validate <file>
      5. Commit and push
```

### Example 2: Git Issues Only

```
📝 You have uncommitted changes
   Don't forget to commit your work

   💡 Workflow:
      git status
      git add <files>
      git commit -m "Add: Description"
      git push
```

### Example 3: Multiple Issues

```
⚠️  Errors were thrown during this session
   Consider documenting them in the KB

📝 You have uncommitted changes
   Don't forget to commit your work

⬆️  You have unpushed commits
   Consider pushing to remote
```

### Example 4: No Issues

```
(No output - clean session!)
```

---

## Performance

**Target:** Non-blocking (session ending anyway)

**Optimization:**
- Minimal processing
- Fast git checks (<500ms)
- No network calls
- Caches git status

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** diet103 Claude Code Infrastructure Showcase
