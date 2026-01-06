# Claude Code HOOKS: Production-Ready Examples & Scripts
## Копируй-вставляй готовые hooks для 10 реальных сценариев

---

## HOOK SETUP: Initial Configuration

### Step 1: Create hooks directory

```bash
mkdir -p .claude/hooks
```

### Step 2: Create settings.json template

```bash
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "PreToolUse": [],
    "PostToolUse": [],
    "SessionStart": [],
    "Stop": [],
    "UserPromptSubmit": [],
    "Notification": []
  }
}
EOF
```

### Step 3: Make hooks executable

```bash
chmod +x .claude/hooks/*.sh
chmod +x .claude/hooks/*.py
```

---

## SCENARIO 1: Quality Gate After Every Edit

### .claude/hooks/quality-gate.sh

```bash
#!/bin/bash
set -e

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only check TypeScript files
if [[ ! "$FILE" == *.ts && ! "$FILE" == *.tsx ]]; then
  exit 0
fi

echo "🔍 Running quality checks for $FILE..."

ERRORS=0

# Check 1: Prettier formatting
if ! npx prettier --check "$FILE" 2>/dev/null; then
  echo "  ❌ Prettier: File not formatted"
  ERRORS=$((ERRORS + 1))
fi

# Check 2: ESLint
if ! npx eslint "$FILE" 2>/dev/null; then
  echo "  ❌ ESLint: Linting errors found"
  ERRORS=$((ERRORS + 1))
fi

# Check 3: TypeScript type checking
if ! npx tsc --noEmit 2>/dev/null; then
  echo "  ❌ TypeScript: Type errors found"
  ERRORS=$((ERRORS + 1))
fi

if [ $ERRORS -eq 0 ]; then
  echo "✅ All quality checks passed"
  exit 0
else
  echo "❌ $ERRORS quality check(s) failed"
  exit 2
fi
```

### settings.json entry

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/quality-gate.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

---

## SCENARIO 2: Block Dangerous Commands

### .claude/hooks/security-filter.py

```python
#!/usr/bin/env python3
"""
PreToolUse hook: Block dangerous bash commands
Prevents accidental data loss and security breaches
"""

import json
import sys
import re

DANGEROUS_PATTERNS = [
    (r'rm\s+-rf\s+/', 'Recursive delete of root directory'),
    (r'sudo\s+rm', 'Sudo delete - restricted'),
    (r'chmod\s+777', 'World-writable permissions - security risk'),
    (r'DROP\s+TABLE', 'SQL table deletion - restricted'),
    (r'DELETE\s+FROM.*WHERE\s+1', 'Bulk database deletion'),
    (r'eval\s*\(', 'eval() - code injection risk'),
    (r'exec\s*\(', 'exec() - code injection risk'),
]

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

tool_name = data.get('tool_name', '')
tool_input = data.get('tool_input', {})

if tool_name != 'Bash':
    sys.exit(0)

command = tool_input.get('command', '')

# Check for dangerous patterns
for pattern, reason in DANGEROUS_PATTERNS:
    if re.search(pattern, command, re.IGNORECASE):
        output = {
            'decision': 'block',
            'reason': f'🚨 Security: {reason}\nCommand blocked: {command}',
            'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'permissionDecision': 'deny',
                'permissionDecisionReason': reason
            }
        }
        print(json.dumps(output))
        sys.exit(0)

# Check for .env file access
env_patterns = [r'\.env', r'secrets', r'password', r'api[_-]?key']
file_path = tool_input.get('file_path', '')

for pattern in env_patterns:
    if re.search(pattern, file_path, re.IGNORECASE):
        output = {
            'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'permissionDecision': 'deny',
                'permissionDecisionReason': f'Cannot access sensitive files: {file_path}'
            }
        }
        print(json.dumps(output))
        sys.exit(0)

sys.exit(0)
```

### settings.json entry

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/security-filter.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

---

## SCENARIO 3: Auto-Format Code (PostToolUse)

### .claude/hooks/auto-format.sh

```bash
#!/bin/bash
"""
Auto-format files based on file type
Supports: TypeScript, Python, Go, Rust, Markdown
"""

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ -z "$FILE" ]]; then
  exit 0
fi

echo "📝 Auto-formatting $FILE..."

case "$FILE" in
  *.ts|*.tsx|*.js|*.jsx)
    npx prettier --write "$FILE" 2>/dev/null
    ;;
  *.py)
    black "$FILE" 2>/dev/null
    ;;
  *.go)
    gofmt -w "$FILE" 2>/dev/null
    ;;
  *.rs)
    rustfmt "$FILE" 2>/dev/null
    ;;
  *.md|*.mdx)
    # Fix markdown formatting
    python3 << 'PYTHON'
import re
import sys

file = "$FILE"
with open(file, 'r') as f:
    content = f.read()

# Fix code fence language tags
def fix_fence(match):
    indent, info, body, closing = match.groups()
    if not info.strip():
        lang = detect_lang(body)
        return f"{indent}```{lang}\n{body}{closing}\n"
    return match.group(0)

content = re.sub(
    r'(?ms)^([ \t]{0,3})```([^\n]*)\n(.*?)(\\n\\1```)\s*$',
    fix_fence,
    content
)

with open(file, 'w') as f:
    f.write(content)
PYTHON
    ;;
esac

echo "✅ Formatted: $FILE"
exit 0
```

### settings.json entry

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/auto-format.sh",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

---

## SCENARIO 4: Load Context at Session Start

### .claude/hooks/session-setup.sh

```bash
#!/bin/bash
"""
SessionStart hook: Load context at beginning of session
Injects recent issues, guidelines, and status
"""

set -e

echo "## 📋 Session Context"
echo ""

# Load recent git commits
if git rev-parse --git-dir > /dev/null 2>&1; then
  echo "### Recent Commits"
  git log --oneline -5
  echo ""
fi

# Load package.json scripts
if [ -f package.json ]; then
  echo "### Available Scripts"
  jq '.scripts' package.json
  echo ""
fi

# Load project status
if [ -f .github/CONTRIBUTING.md ]; then
  echo "### Contributing Guidelines"
  head -20 .github/CONTRIBUTING.md
  echo ""
fi

# Load TODO items
if [ -f TODO.md ]; then
  echo "### Active TODOs"
  cat TODO.md | head -10
  echo ""
fi

# Setup environment variables
if [ -n "$CLAUDE_ENV_FILE" ]; then
  # Node version
  if command -v nvm &> /dev/null; then
    source ~/.nvm/nvm.sh
    nvm use default > /dev/null 2>&1
    NODE_VERSION=$(node --version)
    echo "export NODE_VERSION=$NODE_VERSION" >> "$CLAUDE_ENV_FILE"
  fi
  
  # Development environment
  echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG=app:*' >> "$CLAUDE_ENV_FILE"
  
  # Add project bin to PATH
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

echo "✅ Session setup complete"
exit 0
```

### settings.json entry

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-setup.sh"
          }
        ]
      }
    ]
  }
}
```

---

## SCENARIO 5: Test Coverage Validation (PostToolUse)

### .claude/hooks/coverage-check.sh

```bash
#!/bin/bash
"""
Check test coverage after creating/modifying tests
Ensures coverage stays above threshold (default 80%)
"""

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
THRESHOLD=${COVERAGE_THRESHOLD:-80}

# Only check test files
if [[ ! "$FILE" == *.test.ts && ! "$FILE" == *.test.js ]]; then
  exit 0
fi

echo "📊 Checking test coverage..."

# Run coverage
COVERAGE_OUTPUT=$(npm run test:coverage 2>&1 || true)
COVERAGE=$(echo "$COVERAGE_OUTPUT" | grep -oP 'Statements\s*:\s*\K[\d.]+' | head -1)

if [[ -z "$COVERAGE" ]]; then
  echo "⚠️  Could not determine coverage"
  exit 0
fi

# Check if meets threshold
if (( $(echo "$COVERAGE < $THRESHOLD" | bc -l) )); then
  echo "❌ Coverage: $COVERAGE% (threshold: $THRESHOLD%)"
  echo "Please add more tests to reach $THRESHOLD% coverage"
  
  # Don't block, just warn
  exit 0
else
  echo "✅ Coverage: $COVERAGE% (threshold: $THRESHOLD%)"
  exit 0
fi
```

---

## SCENARIO 6: Git Integration (Stop Hook)

### .claude/hooks/auto-commit.sh

```bash
#!/bin/bash
"""
Stop hook: Auto-commit changes when Claude finishes
Creates meaningful commit messages based on changes
"""

set -e

# Check if git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
  exit 0
fi

# Check if there are changes
if ! git status --porcelain | grep -q .; then
  echo "✅ No changes to commit"
  exit 0
fi

echo "📦 Auto-committing changes..."

# Stage all changes
git add -A

# Create meaningful commit message
if [ -f .claude/last-prompt.txt ]; then
  PROMPT=$(head -1 .claude/last-prompt.txt)
  MESSAGE="Claude: $PROMPT"
else
  # Fall back to change summary
  SUMMARY=$(git diff --cached --name-only | tr '\n' ',' | sed 's/,$//')
  MESSAGE="Claude Code: Updated $SUMMARY"
fi

# Commit
git commit -m "$MESSAGE" || echo "Nothing to commit"

echo "✅ Changes committed"
exit 0
```

---

## SCENARIO 7: Validation on Prompt Submit

### .claude/hooks/prompt-validator.py

```python
#!/usr/bin/env python3
"""
UserPromptSubmit hook: Validate and enrich user prompts
Prevents common mistakes and adds context
"""

import json
import sys
import re

try:
    data = json.load(sys.stdin)
except:
    sys.exit(0)

prompt = data.get('prompt', '')

# Check 1: Block prompts with potential secrets
SECRET_PATTERNS = [
    (r'\bpassword\s*[:=]', 'Password literal'),
    (r'\btoken\s*[:=]', 'Token literal'),
    (r'\bapi.?key\s*[:=]', 'API key literal'),
    (r'\bsecret\s*[:=]', 'Secret literal'),
]

for pattern, name in SECRET_PATTERNS:
    if re.search(pattern, prompt, re.IGNORECASE):
        output = {
            'decision': 'block',
            'reason': f'🔒 Security: {name} detected in prompt. Please remove sensitive data before submitting.'
        }
        print(json.dumps(output))
        sys.exit(0)

# Check 2: Warn about vague prompts
if len(prompt) < 10:
    context = 'Your prompt is very short. Please provide more details for better results.'
    output = {
        'hookSpecificOutput': {
            'hookEventName': 'UserPromptSubmit',
            'additionalContext': context
        }
    }
    print(json.dumps(output))
    sys.exit(0)

# Check 3: Add helpful context
context = '💡 Remember to: 1) Include acceptance criteria 2) Specify expected output format 3) Mention any constraints'
output = {
    'hookSpecificOutput': {
        'hookEventName': 'UserPromptSubmit',
        'additionalContext': context
    }
}
print(json.dumps(output))
sys.exit(0)
```

---

## SCENARIO 8: Custom Notifications

### .claude/hooks/notify.sh

```bash
#!/bin/bash
"""
Notification hook: Send desktop + Slack notifications
Alerts when Claude needs attention
"""

INPUT=$(cat)
MSG=$(echo "$INPUT" | jq -r '.message // empty')
TYPE=$(echo "$INPUT" | jq -r '.notification_type // empty')

if [[ -z "$MSG" ]]; then
  exit 0
fi

echo "🔔 $MSG"

# Desktop notification (macOS)
if command -v osascript &> /dev/null; then
  osascript -e "display notification \"$MSG\" with title \"Claude Code\""
fi

# Desktop notification (Linux)
if command -v notify-send &> /dev/null; then
  notify-send "Claude Code" "$MSG"
fi

# Slack notification (if webhook configured)
if [ -n "$SLACK_WEBHOOK_URL" ]; then
  curl -X POST "$SLACK_WEBHOOK_URL" \
    -H 'Content-Type: application/json' \
    -d "{
      \"text\": \"🤖 Claude Code: $MSG\",
      \"type\": \"$TYPE\"
    }" 2>/dev/null || true
fi

exit 0
```

---

## SCENARIO 9: Intelligent Stop Hook (Prompt-Based)

### settings.json

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop working.\n\nContext from conversation: $ARGUMENTS\n\nDecide based on:\n1. Are all initially requested tasks complete?\n2. Are there any errors or failures?\n3. Is code quality acceptable (tests pass, linting passes)?\n4. Are there any TODOs or incomplete items?\n5. Should Claude continue for follow-up work?\n\nRespond with JSON:\n{\"decision\": \"approve\" or \"block\", \"reason\": \"brief explanation\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

---

## SCENARIO 10: Input Modification (PreToolUse)

### .claude/hooks/smart-modify.py

```python
#!/usr/bin/env python3
"""
PreToolUse hook: Intelligently modify tool inputs
Example: Replace npm with bun, add common flags, etc.
"""

import json
import sys

try:
    data = json.load(sys.stdin)
except:
    sys.exit(0)

tool_name = data.get('tool_name', '')
tool_input = data.get('tool_input', {})

# Rule 1: Use bun instead of npm for package management
if tool_name == 'Bash':
    command = tool_input.get('command', '')
    
    # npm test → bun test
    if 'npm test' in command:
        modified_command = command.replace('npm test', 'bun test')
        output = {
            'decision': 'allow',
            'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'permissionDecision': 'allow',
                'updatedInput': {
                    'command': modified_command
                }
            }
        }
        print(json.dumps(output))
        sys.exit(0)
    
    # npm run → bun run
    if 'npm run' in command:
        modified_command = command.replace('npm run', 'bun run')
        output = {
            'decision': 'allow',
            'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'permissionDecision': 'allow',
                'updatedInput': {
                    'command': modified_command
                }
            }
        }
        print(json.dumps(output))
        sys.exit(0)

sys.exit(0)
```

---

## Configuration Template: All 10 Scenarios

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/security-filter.py",
            "timeout": 5
          },
          {
            "type": "command",
            "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/smart-modify.py",
            "timeout": 5
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
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/quality-gate.sh",
            "timeout": 30
          },
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/auto-format.sh",
            "timeout": 15
          },
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/coverage-check.sh",
            "timeout": 60
          }
        ]
      }
    ],
    
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-setup.sh"
          }
        ]
      }
    ],
    
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/auto-commit.sh"
          },
          {
            "type": "prompt",
            "prompt": "Evaluate if all tasks complete. Consider: task completion, code quality, errors. Respond with JSON: {\"decision\": \"approve\" or \"block\", \"reason\": \"...\"}"
          }
        ]
      }
    ],
    
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 $CLAUDE_PROJECT_DIR/.claude/hooks/prompt-validator.py"
          }
        ]
      }
    ],
    
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/notify.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Debugging Helper Scripts

### .claude/hooks/debug-input.sh

```bash
#!/bin/bash
# Debug hook: Print hook input for troubleshooting

cat | jq . > /tmp/claude-hook-input.json
cat /tmp/claude-hook-input.json
echo "💾 Hook input saved to /tmp/claude-hook-input.json"
exit 0
```

### .claude/hooks/test-hooks.sh

```bash
#!/bin/bash
# Test all hooks manually

echo "Testing PreToolUse hooks..."
echo '{"tool_name":"Bash","tool_input":{"command":"npm test"}}' | \
  python3 .claude/hooks/security-filter.py

echo "Testing PostToolUse hooks..."
echo '{"tool_input":{"file_path":"src/test.ts"}}' | \
  bash .claude/hooks/quality-gate.sh

echo "✅ Hook testing complete"
```

---

**Используй эти scripts как основу для своих hooks**

---

**Версия**: 1.0  
**Дата**: 2025-01-07  
**Статус**: Production-ready  
**Копируй-вставляй готовые hooks для быстрого старта**
