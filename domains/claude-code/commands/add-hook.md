# Add Hook

Add a hook to the project for automation and workflow enhancement.

## Usage
```
/add-hook [options]
```

## Quick Examples

### Interactive Hook Creation
```
/add-hook
```
Guides through hook selection and configuration.

### Specify Event and Type
```
/add-hook --event PreToolUse --type shell
```
Creates PreToolUse shell hook with template.

### Quick Validation Hook
```
/add-hook --event PreToolUse --type shell --validate YAML
```
Creates YAML validation hook.

## What This Command Does

1. **Selects hook event** - SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop
2. **Chooses hook type** - Shell (fast) or LLM (flexible)
3. **Generates hook file** - With template code
4. **Registers in settings.json** - Adds hook configuration
5. **Provides testing guide** - How to test the hook

**📘 Complete Guide:** `@skills/hook-implementation/SKILL.md`

## Options

| Option | Description | Example |
|--------|-------------|---------|
| `--event <event>` | Hook event | `--event PreToolUse` |
| `--type <type>` | Hook type | `--type shell\|llm` |
| `--validate <what>` | Validation target | `--validate YAML` |
| `--track <tool>` | Tool to track | `--track Write` |
| `--notify` | Enable notifications | `--notify` |
| `--force` | Overwrite existing | `--force` |

## Hook Events

| Event | When Fired | Purpose | Max Duration |
|-------|-----------|---------|--------------|
| **SessionStart** | Session starts | Initial setup | 2 seconds |
| **UserPromptSubmit** | After prompt | Skill activation | 1 second |
| **PreToolUse** | Before tool call | Validation | 500ms |
| **PostToolUse** | After tool call | Tracking | 1 second |
| **Stop** | Session ends | Quality check | Non-blocking |

## Workflow

### Step 1: Choose Hook Event

Claude will help select the appropriate event:

**SessionStart** - One-time setup
- Environment validation
- Context loading
- Initialization

**UserPromptSubmit** - Prompt analysis
- Skill activation
- Prompt enhancement
- Intent analysis

**PreToolUse** - Before tool calls
- Validation
- Blocking dangerous operations
- Argument transformation

**PostToolUse** - After tool calls
- Tracking
- Formatting
- Notifications

**Stop** - Session end
- Quality validation
- Reminders
- Cleanup

### Step 2: Choose Hook Type

**Shell hooks:**
- ✅ Fast (<100ms)
- ✅ Deterministic
- ✅ Easy to test
- ❌ Limited capabilities

**Best for:** Validation, formatting, simple tracking

**LLM hooks:**
- ✅ Full context awareness
- ✅ Complex analysis
- ✅ Flexible logic
- ❌ Slower (1-3 seconds)

**Best for:** Skill activation, prompt enhancement, complex decisions

### Step 3: Generate Hook File

**Shell hook template:**
```bash
#!/bin/bash
# .claude/hooks/<Event>/hook-name.sh

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

**LLM hook template (TypeScript):**
```typescript
// .claude/hooks/<Event>/hook-name.ts

export async function hookName(args: any): Promise<any> {
  // Hook logic
  const result = await doSomething(args);

  return result;
}
```

### Step 4: Register in settings.json

```json
{
  "hooks": {
    "<Event>": [
      {
        "type": "shell|llm",
        "path": ".claude/hooks/<Event>/hook-name.ext"
      }
    ]
  }
}
```

### Step 5: Test Hook

```bash
# Test shell hook
bash .claude/hooks/<Event>/hook-name.sh arg1 arg2

# Test LLM hook (if ts-node available)
ts-node .claude/hooks/<Event>/hook-name.ts arg1
```

## Common Patterns

### Pattern 1: YAML Validation

```
/add-hook --event PreToolUse --type shell --validate YAML
```

**Creates:** `.claude/hooks/PreToolUse/yaml-validation.sh`

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

### Pattern 2: Tool Tracking

```
/add-hook --event PostToolUse --type shell --track Write
```

**Creates:** `.claude/hooks/PostToolUse/tool-tracker.sh`

```bash
#!/bin/bash
TOOL_NAME="$1"
EXIT_CODE="$2"

LOG_FILE=".claude/logs/tool-usage.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "$(date -Iseconds) | $TOOL_NAME | exit: $EXIT_CODE" >> "$LOG_FILE"

exit 0
```

### Pattern 3: Skill Activation

```
/add-hook --event UserPromptSubmit --type llm --activate-skills
```

**Creates:** `.claude/hooks/UserPromptSubmit/skill-activation.ts`

```typescript
export async function skillActivationPrompt(prompt: string): Promise<string> {
  const skills = await loadSkillRules();
  const matches = findMatchingSkills(prompt, skills);

  if (matches.length > 0) {
    return formatSuggestions(matches);
  }

  return "";
}
```

## Output

### Success

```
✅ Hook created: yaml-validation
📁 Location: .claude/hooks/PreToolUse/yaml-validation.sh
📝 Type: shell
⏱️  Target: <500ms
✅ Registered in settings.json
🔄 Next: Test with /bash "echo test" > test.yaml

Test command:
  bash .claude/hooks/PreToolUse/yaml-validation.sh "Write" "test.yaml"
```

### Already Exists

```
⚠️  Hook already exists: PreToolUse/yaml-validation.sh
💡 Use --force to overwrite
```

## Best Practices

### 1. Event Selection

**SessionStart** - Use for setup, not validation
**UserPromptSubmit** - Use for analysis, not blocking
**PreToolUse** - Use for validation, blocking
**PostToolUse** - Use for tracking, formatting
**Stop** - Use for reminders, cleanup

### 2. Performance

**Shell hooks:** <100ms typical
**LLM hooks:** 1-3 seconds typical

**Respect targets:**
- SessionStart: <2 seconds
- UserPromptSubmit: <1 second
- PreToolUse: <500ms
- PostToolUse: <1 second
- Stop: Non-blocking

### 3. Error Handling

**Always handle errors gracefully:**

```bash
#!/bin/bash
set -euo pipefail  # Exit on error

trap 'echo "❌ Hook failed at line $LINENO"; exit 1' ERR

# Validate command exists
if ! command -v python &> /dev/null; then
    echo "⚠️  Python not found, skipping"
    exit 0  # Don't block
fi

# Try validation
if ! python tools/kb.py validate "$FILE"; then
    echo "❌ Validation failed"
    exit 1  # Block operation
fi
```

### 4. Testing

**Test manually before trusting:**

```bash
# Test shell hook
bash .claude/hooks/PreToolUse/hook.sh "Write" "test.yaml"
echo "Exit code: $?"

# Test LLM hook
ts-node .claude/hooks/UserPromptSubmit/hook.ts "test prompt"
```

## Claude's Role

When using this command, Claude will:

1. **Ask for hook event** (if not specified)
2. **Suggest hook type** based on use case
3. **Generate hook file** with appropriate template
4. **Register in settings.json** with correct configuration
5. **Make hook executable** (for shell hooks)
6. **Provide testing commands** for validation
7. **Suggest performance optimizations**

## Examples

### Example 1: Environment Validation

```
/add-hook --event SessionStart --type shell
```

**Purpose:** Validate environment on session start

**Created:** `.claude/hooks/SessionStart/validate-env.sh`

```bash
#!/bin/bash
echo "🔍 Validating environment..."

if ! command -v python &> /dev/null; then
    echo "❌ Python not found"
    exit 1
fi
echo "✅ Python: $(python --version)"

if [ ! -f ".kb/index.db" ]; then
    echo "⚠️  KB index missing"
    echo "   Run: python tools/kb.py index -v"
fi

echo "✅ Environment ready"
```

### Example 2: Auto-Format

```
/add-hook --event PostToolUse --type shell --format
```

**Purpose:** Auto-format files after writing

**Created:** `.claude/hooks/PostToolUse/auto-format.sh`

```bash
#!/bin/bash
TOOL_NAME="$1"
FILE_PATH="$2"

if [ "$TOOL_NAME" = "Write" ]; then
    if [[ "$FILE_PATH" == *.py ]] && command -v black &> /dev/null; then
        black "$FILE_PATH" --quiet
        echo "✅ Formatted with black"
    fi

    if [[ "$FILE_PATH" == *.json ]] && command -v jq &> /dev/null; then
        jq '.' "$FILE_PATH" > "${FILE_PATH}.tmp"
        mv "${FILE_PATH}.tmp" "$FILE_PATH"
        echo "✅ Formatted JSON"
    fi
fi

exit 0
```

### Example 3: Error Reminder

```
/add-hook --event Stop --type llm --remind-errors
```

**Purpose:** Remind to document errors at session end

**Created:** `.claude/hooks/Stop/error-handling-reminder.ts`

```typescript
export async function errorHandlingReminder(context: any): Promise<string> {
  if (context.errorsThrown) {
    return "⚠️  Errors were thrown - consider documenting in KB";
  }
  return "";
}
```

## Related

- `@skills/hook-implementation/SKILL.md` - Complete hook implementation guide
- `@skills/hook-implementation/resources/hook-events.md` - Hook events reference
- `@skills/hook-implementation/resources/hook-patterns.md` - Implementation patterns
- `@skills/claude-code-architecture/SKILL.md` - Claude Code architecture

## Troubleshooting

### Hook Not Firing

**Check:**
1. ✅ Hook file exists?
2. ✅ Hook executable? (`chmod +x` for shell)
3. ✅ Hook registered in settings.json?
4. ✅ JSON syntax valid?
5. ✅ Claude Code restarted?

**Fix:** Restart Claude Code after adding hook

### Hook Performance Issues

**Symptoms:** Slow session start, laggy tool calls

**Solutions:**
1. Use shell hooks instead of LLM
2. Cache expensive operations
3. Limit file scanning
4. Optimize regex patterns
5. Profile execution time

### Shell Hook Permission Denied

**Symptom:** Hook doesn't execute

**Fix:**
```bash
chmod +x .claude/hooks/<Event>/hook.sh
```

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** hook-implementation skill
