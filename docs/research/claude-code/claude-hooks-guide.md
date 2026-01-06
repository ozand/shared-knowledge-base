# Claude Code HOOKS: Полное практическое руководство
## Детерминированный контроль workflow-а через автоматизацию

---

## Оглавление

1. [Фундаментальные концепции](#фундаментальные-концепции)
2. [Hook Events: Полный справочник](#hook-events-полный-справочник)
3. [Matchers иPattern Matching](#matchers-и-pattern-matching)
4. [Hook Input/Output Format](#hook-inputoutput-format)
5. [Bash Command Hooks (type: command)](#bash-command-hooks-type-command)
6. [Prompt-Based Hooks (type: prompt)](#prompt-based-hooks-type-prompt)
7. [7 Практических паттернов](#7-практических-паттернов)
8. [Decision Control (Allow/Block)](#decision-control-allowblock)
9. [Environment Variables & Context](#environment-variables--context)
10. [Debugging & Troubleshooting](#debugging--troubleshooting)
11. [Security Best Practices](#security-best-practices)
12. [Anti-patterns & Common Mistakes](#anti-patterns--common-mistakes)

---

## Фундаментальные концепции

### Что такое HOOKS?

**Hooks** — это детерминированные автоматизированные события, которые выполняют shell-команды или запросы к LLM в специфических точках жизненного цикла Claude Code.

```
KEY DISTINCTION:

Prompts:   "Please run tests"      → Claude может забыть
Hooks:     Automatically runs tests → ГАРАНТИРОВАНО выполняется

Hooks = Promises, не suggestions
```

### Почему HOOKS важны?

```
ПРОБЛЕМА: LLM probabilistic
  - Попросили запустить тесты → Claude может забыть
  - Попросили проверить тип → Claude может пропустить
  - Попросили логировать → Claude может не сделать

РЕШЕНИЕ: Hooks = deterministic
  - Тесты ВСЕГДА запускаются после edit
  - Тип checking ВСЕГДА проверяется
  - Логирование ВСЕГДА происходит
  - Всё автоматично, без полагания на Claude
```

### Когда использовать HOOKS?

```
✅ ИСПОЛЬЗУЙ HOOKS для:
  • Автоматическая валидация (tests, linting, type checking)
  • Качество контроля (coverage, security scans)
  • Интеграция (git, CI/CD, Slack notifications)
  • Логирование и аудит
  • Блокирование опасных операций
  • Автоматическое форматирование кода
  • Модификация input перед выполнением
  • Добавление контекста в conversation

❌ НЕ ИСПОЛЬЗУЙ HOOKS для:
  • Complex decision logic (используй Prompt-based hooks)
  • Slow operations (>5sec) — замедляют workflow
  • User interaction (используй prompt instead)
  • Отключение Claude (используй Stop hook properly)
```

---

## Hook Events: Полный справочник

### Таблица всех событий

```
┌──────────────────────────────────────────────────────────────┐
│                     10 HOOK EVENTS                           │
└──────────────────────────────────────────────────────────────┘

EVENT                WHEN IT RUNS                    USE CASE
─────────────────────────────────────────────────────────────
PreToolUse           Перед любым tool call          Валидация, блокирование
                     (Before execution)             Модификация input

PostToolUse          После успешного tool call      Лinting, форматирование
                     (After execution)              Testing, logging

PermissionRequest    Когда нужна пермиссия          Auto-approve/deny
                     (Permission dialog shown)      Permission flow

UserPromptSubmit     Когда юзер сабмитит промпт    Валидация промпта
                     (Before processing)            Добавить контекст

SessionStart          При старте сессии             Setup, env setup
                     (Session initialization)       Load context, caching

SessionEnd           Когда сессия кончается        Cleanup, logging
                     (Session termination)          Save state

Stop                 Когда Claude завершил          Force continuation
                     (Agent finishes response)      Quality validation

SubagentStop         Когда subagent завершила      Task completion check
                     (Subagent finishes)            Quality validation

Notification         Когда Claude отправляет       Desktop alerts
                     уведомление                    Sound notifications
                     (Notification sent)

PreCompact           Перед context compaction      Logging, cleanup
                     (Before compact operation)     Custom preparation
```

### EVENT 1: PreToolUse

```
КОГДА: Перед execution любого tool call
ИСПОЛЬЗУЕТСЯ: Валидация, блокирование, модификация input

COMMON MATCHERS:
  Bash          → Shell commands
  Edit|Write    → File modifications
  Read          → File reading
  Grep          → Content search
  *             → All tools

DECISION OPTIONS:
  ✅ allow   → Пропустить tool call
  ❌ deny    → Блокировать tool call (feedback Claude)
  ❓ ask     → Попросить юзера confirm

ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

1. Блокировать опасные команды
   ├─ rm -rf /
   ├─ sudo rm
   └─ chmod 777

2. Валидировать edit-ы
   ├─ Проверить синтаксис
   ├─ Проверить линтер rules
   └─ Проверить format

3. Модифицировать параметры
   ├─ Сменить npm → bun
   ├─ Добавить флаги
   └─ Нормализовать paths
```

### EVENT 2: PostToolUse

```
КОГДА: Сразу после успешного tool call
ИСПОЛЬЗУЕТСЯ: Форматирование, тестирование, логирование

COMMON MATCHERS: Same as PreToolUse

DECISION OPTIONS:
  undefined     → No action (default)
  ❌ block      → Provide feedback to Claude

ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

1. Автоматическое форматирование
   ├─ prettier на .ts files
   ├─ gofmt на .go files
   └─ black на .py files

2. Запуск тестов
   ├─ npm test после edit
   ├─ Check coverage ≥80%
   └─ Block if tests fail

3. Логирование
   ├─ Log all commands
   ├─ Track changes
   └─ Audit trail
```

### EVENT 3: UserPromptSubmit

```
КОГДА: Когда юзер сабмитит промпт (перед обработкой)
ИСПОЛЬЗУЕТСЯ: Валидация, контекст injection, блокирование

DECISION OPTIONS:
  undefined     → Allow prompt
  ❌ block      → Block prompt, show reason
  (exit 0)      → Add context to conversation

ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

1. Валидировать промпт
   ├─ Проверить на secrets
   ├─ Проверить на сензитивные данные
   └─ Проверить на invalid patterns

2. Добавить контекст автоматически
   ├─ Load last commit info
   ├─ Load recent issues
   └─ Load team guidelines

3. Enforce промпт стиль
   ├─ Требовать детали
   ├─ Требовать acceptance criteria
   └─ Требовать context
```

### EVENT 4: SessionStart

```
КОГДА: При старте новой сессии
ИСПОЛЬЗУЕТСЯ: Setup, env configuration, context loading

MATCHERS:
  startup     → New session
  resume      → Resumed session
  clear       → After /clear command

ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

1. Environment setup
   ├─ nvm use 20
   ├─ source .env
   └─ Set NODE_ENV

2. Load context
   ├─ Load recent tickets
   ├─ Load team guidelines
   └─ Load project status

3. Install dependencies
   ├─ npm install
   ├─ Download required files
   └─ Setup caches

SPECIAL: CLAUDE_ENV_FILE
  Позволяет persist environment variables
  между bash commands в session
```

### EVENT 5: Stop

```
КОГДА: Когда Claude Code закончил response
ИСПОЛЬЗУЕТСЯ: Валидация completion, force continuation

DECISION OPTIONS:
  undefined     → Allow stop
  ❌ block      → Prevent stop, force continuation

ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

1. Валидировать что tasks complete
   ├─ Проверить tests passing
   ├─ Проверить coverage met
   └─ Проверить no errors

2. Require quality gates
   ├─ Must pass linting
   ├─ Must have documentation
   └─ Must have tests

TYPE: prompt-based hooks supported
  └─ LLM evaluates if work is complete
```

---

## Matchers и Pattern Matching

### Matcher Syntax

```
MATCHER TYPES:

1. EXACT MATCH
   "Bash"        → Matches ONLY Bash tool
   "Write"       → Matches ONLY Write tool
   Case-sensitive!

2. REGEX PATTERNS
   "Edit|Write"  → Matches Edit OR Write
   "Edit:*.ts"   → Matches Edit for .ts files
   "mcp__.*__write"  → Matches any MCP write operation

3. WILDCARD
   "*"           → Matches ALL tools
   ""            → Matches ALL tools (for events without matchers)

4. FILE PATTERN (PostToolUse/PreToolUse)
   "Edit:src/*"  → Matches Edit in src/
   "Read:.*\\.env" → Block .env reads

COMMON TOOL NAMES:
  Bash          Shell commands
  Read          File reading
  Write         File creation
  Edit          File modification
  Grep          Content search
  WebFetch      Web requests
  Task          Subagent execution
  * (MCP tools with special naming)
```

### Advanced Matcher Examples

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "./validate-bash.sh"
        }]
      },
      {
        "matcher": "Edit:src/auth/*|Edit:src/security/*",
        "hooks": [{
          "type": "command",
          "command": "./security-review.sh"
        }]
      },
      {
        "matcher": "mcp__memory__.*",
        "hooks": [{
          "type": "command",
          "command": "echo MCP memory operation"
        }]
      }
    ]
  }
}
```

---

## Hook Input/Output Format

### Hook Input (stdin)

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run tests"
  },
  "tool_use_id": "toolu_01ABC..."
}
```

### Hook Output (stdout/stderr)

```
TWO WAYS TO RETURN OUTPUT:

OPTION 1: Simple Exit Codes
  Exit 0       → Success (allow action)
  Exit 2       → Block (with stderr as reason)
  Exit 1/3+    → Non-blocking error (shown in verbose mode)

OPTION 2: Structured JSON Output
  JSON in stdout with exit 0
  Contains: decision, reason, metadata
```

### Structured JSON Response Format

```json
{
  "decision": "block",  // or "allow", "approve", "deny"
  "reason": "Tests failed, cannot proceed",
  "continue": true,     // Whether to continue (optional)
  "suppressOutput": false,  // Hide from transcript (optional)
  "systemMessage": "Warning message to user",
  
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Why allowed",
    "updatedInput": {
      "field_name": "new_value"  // Modify tool input
    }
  }
}
```

---

## Bash Command Hooks (type: command)

### Простейший пример

```bash
#!/bin/bash
# .claude/hooks/post-write.sh

# Run after any file write
echo "✅ File written successfully"
exit 0  # Allow the action
```

### Валидация с exit codes

```bash
#!/bin/bash
# .claude/hooks/validate-bash.sh
# PreToolUse hook for Bash commands

COMMAND="$1"

# Block dangerous commands
if echo "$COMMAND" | grep -E "(rm -rf|sudo rm|chmod 777)"; then
  echo "❌ Dangerous command blocked: $COMMAND"
  exit 2  # Exit 2 = BLOCK
fi

echo "✅ Command allowed: $COMMAND"
exit 0  # Exit 0 = ALLOW
```

### Python hook с JSON output

```python
#!/usr/bin/env python3
# .claude/hooks/smart-validator.py

import json
import sys

try:
  data = json.load(sys.stdin)
except:
  sys.exit(1)

tool_name = data.get("tool_name")
file_path = data.get("tool_input", {}).get("file_path", "")

# Auto-approve documentation reads
if tool_name == "Read" and file_path.endswith(".md"):
  output = {
    "decision": "approve",
    "reason": "Documentation file",
    "suppressOutput": True
  }
  print(json.dumps(output))
  sys.exit(0)

# Block .env modifications
if ".env" in file_path:
  output = {
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "deny",
      "permissionDecisionReason": "Cannot modify .env files"
    }
  }
  print(json.dumps(output))
  sys.exit(0)

# Allow everything else
sys.exit(0)
```

### Hook с модификацией input

```bash
#!/bin/bash
# Swap npm for bun automatically

INPUT_JSON=$(cat)

# Check if command uses npm
if echo "$INPUT_JSON" | jq -e '.tool_input.command | contains("npm")' > /dev/null; then
  # Replace npm with bun
  MODIFIED=$(echo "$INPUT_JSON" | jq '.tool_input.command |= gsub("npm"; "bun")')
  
  # Return modified input
  jq -n '{
    "decision": "allow",
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "allow",
      "updatedInput": {
        "command": "bun test"
      }
    }
  }'
  exit 0
fi

exit 0
```

---

## Prompt-Based Hooks (type: prompt)

### Когда использовать

```
Bash hooks:    Deterministic rules (syntax, patterns)
Prompt hooks:  Context-aware decisions (is task complete?)

Prompt hooks = LLM evaluation
  - Читает context
  - Понимает intent
  - Принимает intelligent decisions
```

### Configuration

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Evaluate if Claude should stop. Check if:\n1. All user-requested tasks complete\n2. No critical errors\n3. Code quality acceptable\n\nRespond with JSON: {\"decision\": \"approve\" or \"block\", \"reason\": \"explanation\"}",
        "timeout": 30
      }]
    }]
  }
}
```

### Response Schema

```json
{
  "decision": "approve",  // or "block"
  "reason": "All tasks complete, tests passing, coverage 85%",
  "continue": false,      // Stop Claude entirely (optional)
  "stopReason": "Feature complete and ready to merge",
  "systemMessage": "Note: Tests have been run successfully"
}
```

### Пример: Intelligent Stop Hook

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Analyze the conversation and determine if Claude should stop.\n\nContext: $ARGUMENTS\n\nEvaluate:\n1. Are all originally requested tasks complete?\n2. Are there any errors that need fixing?\n3. Is the code quality acceptable (tests, linting)?\n4. Are there any TODO items left?\n\nRespond with JSON containing decision (approve/block) and reason.",
        "timeout": 30
      }]
    }]
  }
}
```

---

## 7 Практических паттернов

### ПАТТЕРН 1: Code Quality Gate (PostToolUse)

```bash
#!/bin/bash
# .claude/hooks/quality-gate.sh
# Enforce tests + linting after every edit

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

# Only check TypeScript files
if [[ ! "$FILE_PATH" == *.ts ]]; then
  exit 0
fi

echo "🔍 Running quality checks..."

# Check 1: Linting
if ! npm run lint -- "$FILE_PATH"; then
  echo "❌ Linting failed"
  exit 2  # BLOCK
fi

# Check 2: Type checking
if ! npm run type:check; then
  echo "❌ Type checking failed"
  exit 2  # BLOCK
fi

# Check 3: Tests (if test file exists)
TEST_FILE="${FILE_PATH%.ts}.test.ts"
if [[ -f "$TEST_FILE" ]]; then
  if ! npm test -- "$TEST_FILE"; then
    echo "❌ Tests failed"
    exit 2  # BLOCK
  fi
fi

echo "✅ All quality checks passed"
exit 0
```

### ПАТТЕРН 2: Security Validation (PreToolUse)

```bash
#!/bin/bash
# .claude/hooks/security-check.sh
# Block dangerous operations

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

DANGEROUS_PATTERNS=(
  "rm -rf"
  "sudo rm"
  "chmod 777"
  "DROP TABLE"
  "DELETE FROM"
  "eval"
  "exec"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if [[ "$COMMAND" == *"$pattern"* ]]; then
    echo "🚨 Security violation: $pattern"
    exit 2  # BLOCK
  fi
done

# Check if modifying .env
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
if [[ "$FILE" == *".env"* ]]; then
  echo "🚨 Cannot modify .env files"
  exit 2  # BLOCK
fi

exit 0
```

### ПАТТЕРН 3: Automatic Formatting (PostToolUse)

```bash
#!/bin/bash
# .claude/hooks/auto-format.sh
# Automatically format files after edits

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

if [[ "$FILE_PATH" == *.ts || "$FILE_PATH" == *.tsx ]]; then
  npx prettier --write "$FILE_PATH"
elif [[ "$FILE_PATH" == *.go ]]; then
  gofmt -w "$FILE_PATH"
elif [[ "$FILE_PATH" == *.py ]]; then
  black "$FILE_PATH"
elif [[ "$FILE_PATH" == *.md ]]; then
  npx markdownlint --fix "$FILE_PATH"
fi

exit 0
```

### ПАТТЕРН 4: Context Injection (SessionStart)

```bash
#!/bin/bash
# .claude/hooks/load-context.sh
# Load recent issues and guidelines at session start

echo "## Recent Issues"
echo "$(gh issue list --limit 3 --json title,number,state)"

echo ""
echo "## Team Guidelines"
cat .github/CONTRIBUTING.md

echo ""
echo "## Last Commit"
git log -1 --oneline

# Persist some environment variables
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG=app:*' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

### ПАТТЕРН 5: Git Integration (Stop Hook)

```bash
#!/bin/bash
# .claude/hooks/auto-commit.sh
# Auto-commit changes when Claude finishes

if git status --porcelain | grep -q .; then
  git add -A
  
  SUMMARY=$(git diff --cached --stat | head -1)
  git commit -m "Claude Code: $SUMMARY"
  
  echo "✅ Changes committed"
fi

exit 0
```

### ПАТТЕРН 6: Notification (Notification Hook)

```bash
#!/bin/bash
# .claude/hooks/notify.sh
# Send notifications for important events

INPUT=$(cat)
MSG=$(echo "$INPUT" | jq -r '.message')
TYPE=$(echo "$INPUT" | jq -r '.notification_type')

# Desktop notification
notify-send "Claude Code" "$MSG"

# Slack notification (optional)
if [[ "$TYPE" == "permission_prompt" ]]; then
  curl -X POST $SLACK_WEBHOOK \
    -d "{'text': '🔔 Claude needs permission: $MSG'}"
fi

exit 0
```

### ПАТТЕРН 7: Coverage Check (PostToolUse)

```bash
#!/bin/bash
# .claude/hooks/coverage-check.sh
# Ensure test coverage stays ≥80%

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path')

# Only check for .test.ts files
if [[ ! "$FILE" == *.test.ts ]]; then
  exit 0
fi

COVERAGE=$(npm run coverage 2>/dev/null | grep "Statements" | grep -oP '\d+\.\d+')

if (( $(echo "$COVERAGE < 80" | bc -l) )); then
  echo "❌ Coverage $COVERAGE% < 80% minimum"
  exit 2  # BLOCK
fi

echo "✅ Coverage: $COVERAGE%"
exit 0
```

---

## Decision Control (Allow/Block)

### Decision Types & Exit Codes

```
EVENT                EXIT 0 (ALLOW)    EXIT 2 (BLOCK)
─────────────────────────────────────────────────
PreToolUse           Execute tool      Skip tool
PermissionRequest    Auto-approve      Auto-deny
PostToolUse          Continue          Feed back
UserPromptSubmit     Process prompt    Reject prompt
Stop                 Allow stop        Force continue
SubagentStop         Allow stop        Force continue
```

### JSON Decision Examples

```json
// ALLOW example
{
  "decision": "allow",
  "reason": "Command is safe",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow"
  }
}

// BLOCK example
{
  "decision": "block",
  "reason": "Security: Cannot modify production files",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Production files are protected"
  }
}

// MODIFY INPUT example
{
  "decision": "allow",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "updatedInput": {
      "command": "bun test"  // Changed from npm test
    }
  }
}
```

---

## Environment Variables & Context

### Available Variables

```bash
CLAUDE_PROJECT_DIR      Path to project root
CLAUDE_CODE_REMOTE      "true" if remote, empty if local
CLAUDE_ENV_FILE         (SessionStart only) File to persist env vars
CLAUDE_FILE_PATHS       File paths being operated on
CLAUDE_COMMAND          Command being executed (Bash tool)
```

### Using CLAUDE_PROJECT_DIR

```bash
#!/bin/bash
# Reference project files reliably

SCRIPT="$CLAUDE_PROJECT_DIR/.claude/hooks/validate.py"
CONFIG="$CLAUDE_PROJECT_DIR/.claude/config.json"

python3 "$SCRIPT" --config "$CONFIG"
```

### Persisting Environment Variables (SessionStart)

```bash
#!/bin/bash
# SessionStart hook to set up environment

# Method 1: Simple environment variables
if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG=app:*' >> "$CLAUDE_ENV_FILE"
fi

# Method 2: Complex setup (nvm, etc)
ENV_BEFORE=$(export -p | sort)

# Load nvm
source ~/.nvm/nvm.sh
nvm use 20

# Capture changes
if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

---

## Debugging & Troubleshooting

### Enable Debug Mode

```bash
# Run Claude Code with debug output
claude --debug

# Shows detailed hook execution:
# [DEBUG] Executing hooks for PostToolUse:Write
# [DEBUG] Found 1 hook matchers
# [DEBUG] Executing: <command>
# [DEBUG] Exit code: 0
# [DEBUG] Stdout: <output>
```

### Common Issues & Solutions

```
ISSUE 1: Hook not executing
  └─ Check: /hooks command to verify registration
  └─ Check: JSON syntax in settings.json
  └─ Fix: Run `claude /hooks` to re-register

ISSUE 2: Hook timeout
  └─ Default: 60 seconds
  └─ Fix: Add "timeout": 30 in hook config
  └─ Or: Optimize slow operations (cache, parallel)

ISSUE 3: Hook blocking too aggressively
  └─ Check: Exit code (2 blocks, 0 allows)
  └─ Check: Matcher is correct
  └─ Fix: Use more specific matchers

ISSUE 4: Can't access variables in bash
  └─ Input comes via stdin as JSON
  └─ Use: jq to parse JSON
  └─ Example: cat | jq -r '.tool_input.command'

ISSUE 5: File paths don't work
  └─ Use: Absolute paths or $CLAUDE_PROJECT_DIR
  └─ Not: Relative paths (unsafe)
  └─ Example: "$CLAUDE_PROJECT_DIR/.claude/hooks/script.sh"
```

### Manual Hook Testing

```bash
# Test a hook manually without Claude Code

# Create fake input
INPUT='{"tool_name":"Bash","tool_input":{"command":"npm test"}}'

# Pipe to hook
echo "$INPUT" | ./hooks/validate.sh

# Check exit code
echo $?  # 0 = allow, 2 = block
```

---

## Security Best Practices

### DANGER: Arbitrary Command Execution

```
⚠️  HOOKS EXECUTE ARBITRARY SHELL COMMANDS
    Only use hooks from trusted sources
    Review all hooks before enabling
    Test in safe environment first
```

### Security Checklist

```
✅ DO:
  • Use absolute paths
  • Quote all variables: "$VAR" not $VAR
  • Validate/sanitize inputs
  • Test hooks in sandbox first
  • Use static analysis (shellcheck)
  • Log hook execution
  • Review exit codes carefully
  
❌ DON'T:
  • Use hooks from untrusted sources
  • Hardcode secrets in hooks
  • Use unquoted variables
  • Run heavy operations (>5sec)
  • Ignore error handling
  • Store passwords in code
```

### Input Validation Example

```bash
#!/bin/bash
# Validate input safely

INPUT=$(cat)

# Extract values safely
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Validate file path (prevent traversal)
if [[ "$FILE" == *".."* ]]; then
  echo "❌ Path traversal detected"
  exit 2
fi

# Validate command (whitelist)
if ! echo "$CMD" | grep -E '^(npm|git|ls|cat|grep)'; then
  echo "❌ Command not whitelisted"
  exit 2
fi

# Safe to proceed
exit 0
```

---

## Anti-patterns & Common Mistakes

### ❌ ANTI-PATTERN 1: Slow Hooks

```
BAD:
"PostToolUse": [{
  "command": "npm run full-test-suite"  # Takes 5 minutes!
}]

Result: Every edit pauses workflow for 5 minutes
→ Terrible UX, Claude gets stuck

GOOD:
"PostToolUse": [{
  "command": "npm run quick-check"  # Takes 2 seconds
}]

// Run full suite separately via /hooks command
```

### ❌ ANTI-PATTERN 2: Too Broad Matchers

```
BAD:
"PreToolUse": [{
  "matcher": "*",  # ALL tools
  "hooks": [{
    "command": "heavy-validation.sh"
  }]
}]

Result: Every tool call gets blocked for validation
→ Workflow becomes unusable

GOOD:
"PreToolUse": [{
  "matcher": "Bash",  // Only bash commands
  "hooks": [{
    "command": "validate-bash.sh"
  }]
}]
```

### ❌ ANTI-PATTERN 3: Unquoted Variables

```
BAD:
#!/bin/bash
FILE=$1  # If filename has spaces, breaks
rm $FILE

GOOD:
#!/bin/bash
FILE="$1"  # Properly quoted
rm "$FILE"

EVEN BETTER:
FILE=$(cat | jq -r '.tool_input.file_path')
rm "$FILE"  # Quoted, extracted safely
```

### ❌ ANTI-PATTERN 4: Ignoring Exit Codes

```
BAD:
#!/bin/bash
npm test
npm run lint  # Runs even if tests failed!

GOOD:
#!/bin/bash
npm test || exit 2  # Exit 2 if test fails
npm run lint || exit 2  # Exit 2 if lint fails
exit 0
```

### ❌ ANTI-PATTERN 5: Hardcoding Secrets

```
BAD:
#!/bin/bash
curl https://api.example.com \
  -H "Authorization: Bearer abc123secret"

GOOD:
#!/bin/bash
curl https://api.example.com \
  -H "Authorization: Bearer ${API_TOKEN}"

# Set via environment or SessionStart hook
```

### ❌ ANTI-PATTERN 6: Not Handling Errors

```
BAD:
#!/bin/bash
jq '.tool_input.command'  # What if JSON is invalid?

GOOD:
#!/bin/bash
if ! jq -e '.tool_input.command' < /dev/stdin > /dev/null 2>&1; then
  echo "Invalid JSON input"
  exit 1
fi
```

### ❌ ANTI-PATTERN 7: Blocking Without Reason

```
BAD:
echo "❌ BLOCKED"
exit 2

GOOD:
echo "❌ Cannot modify production files - use staging environment instead"
exit 2

// Claude gets meaningful feedback for retry
```

---

## Best Practices Checklist

```
HOOK DESIGN:
  [ ] Keep hooks FAST (<2sec)
  [ ] Be SPECIFIC with matchers
  [ ] Write CLEAR error messages
  [ ] Test BEFORE deploying
  [ ] Document WHAT and WHY
  [ ] Handle ERRORS gracefully

SECURITY:
  [ ] Quote all variables
  [ ] Validate all inputs
  [ ] Use absolute paths
  [ ] Review from trusted sources
  [ ] No hardcoded secrets
  [ ] Minimal permissions needed

DEBUGGING:
  [ ] Use `--debug` flag
  [ ] Test hooks manually
  [ ] Check exit codes
  [ ] Log important events
  [ ] Monitor hook execution
  [ ] Have escape hatch

MAINTENANCE:
  [ ] Keep hooks simple
  [ ] One hook = one concern
  [ ] Version your hooks
  [ ] Document changes
  [ ] Test regularly
  [ ] Get team feedback
```

---

## Quick Reference: Hook Configuration Template

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/validate-bash.sh",
            "timeout": 10
          }
        ]
      }
    ],
    
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write",
            "timeout": 30
          }
        ]
      }
    ],
    
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/setup.sh"
          }
        ]
      }
    ],
    
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks complete. $ARGUMENTS",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

---

**Версия**: 1.0  
**Дата**: 2025-01-07  
**Статус**: Production-ready  
**Источник**: Anthropic Claude Code docs + real-world patterns
