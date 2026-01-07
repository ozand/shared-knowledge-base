# Claude Code HOOKS: Anti-patterns & Advanced Strategies
## Типичные ошибки, решения, и production best practices

---

## PART 1: Common Mistakes & Solutions

### ❌ MISTAKE 1: Slow Hooks Block Workflow

```
PROBLEM:
  "PostToolUse": [{
    "command": "npm run full-test-suite"  # 5 minutes!
  }]

SYMPTOMS:
  • Every edit causes 5-minute pause
  • Claude gets stuck waiting
  • Workflow becomes unusable
  • Developers frustrated

ROOT CAUSE:
  Hooks run synchronously
  Claude waits for hook to complete
  Slow hooks = slow workflow
```

**SOLUTION:**

```
Separate fast checks from slow tests:

FAST HOOKS (PostToolUse):
  ├─ Prettier formatting (2 sec)
  ├─ ESLint (3 sec)
  └─ Type checking (5 sec)
  Total: <10 seconds ✅

SLOW TESTS:
  └─ Run separately via CI/CD
  └─ Don't block development
```

### ❌ MISTAKE 2: Too Broad Matchers

```
PROBLEM:
  "PreToolUse": [{
    "matcher": "*",  # ALL tools!
    "command": "heavy-validation.sh"
  }]

SYMPTOMS:
  • Every tool call gets blocked
  • Read operations trigger validation
  • Grep operations trigger validation
  • Complete workflow slowdown

ROOT CAUSE:
  Wildcard matcher applies to everything
  Validation not needed for reads
```

**SOLUTION:**

```
Use specific matchers:

"PreToolUse": [{
  "matcher": "Bash",  // Only Bash commands
  "hooks": [{
    "command": "validate-bash.sh"
  }]
}]

// Alternatively:
"matcher": "Edit|Write",  // Only modifications
"matcher": "mcp__.*__write"  // Only MCP writes
```

### ❌ MISTAKE 3: Silent Failures

```
PROBLEM:
  #!/bin/bash
  npm test
  npm run lint  # Runs even if test failed!
  
SYMPTOMS:
  • Tests fail but linting continues
  • No error feedback
  • Hard to debug

ROOT CAUSE:
  Bash continues after failed commands
  No error checking
```

**SOLUTION:**

```bash
#!/bin/bash
set -e  # Exit on first error

npm test || exit 2    # Explicit exit code
npm run lint || exit 2

# Or check manually:
if ! npm test; then
  echo "❌ Tests failed"
  exit 2
fi
```

### ❌ MISTAKE 4: Hardcoded Secrets

```
PROBLEM:
  curl https://api.example.com \
    -H "Authorization: Bearer hardcoded_token_123"

SYMPTOMS:
  • Secret in source control
  • Exposed in logs
  • Security breach
```

**SOLUTION:**

```bash
# Load from environment
TOKEN="${API_TOKEN}"
curl https://api.example.com \
  -H "Authorization: Bearer $TOKEN"

# Set via SessionStart hook:
echo 'export API_TOKEN=...' >> "$CLAUDE_ENV_FILE"
```

### ❌ MISTAKE 5: Unquoted Variables

```
PROBLEM:
  FILE=$1
  rm $FILE  # Breaks if filename has spaces!
  
  # Filename: "my file.txt"
  # Executes: rm my file.txt  ❌

SYMPTOMS:
  • Deletes wrong files
  • Data loss
  • Errors in complex paths
```

**SOLUTION:**

```bash
FILE="$1"  # Quote variables
rm "$FILE"  # Safe even with spaces

# From JSON:
FILE=$(cat | jq -r '.tool_input.file_path')
rm "$FILE"  # Properly quoted
```

### ❌ MISTAKE 6: Invalid JSON Output

```
PROBLEM:
  echo '{
    "decision": "block",
    "reason": "Invalid quote: He said "stop""  ❌ Quote not escaped!
  }'

SYMPTOMS:
  • JSON parse error
  • Hook fails silently
  • Claude doesn't get feedback
```

**SOLUTION:**

```bash
# Use jq to build valid JSON:
jq -n \
  --arg reason "He said \"stop\"" \
  '{decision: "block", reason: $reason}'

# Or escape properly in Python:
import json
output = {
  "decision": "block",
  "reason": "He said \"stop\""
}
print(json.dumps(output))
```

### ❌ MISTAKE 7: Hook Timeout Issues

```
PROBLEM:
  #!/bin/bash
  npm run build  # 2 minutes
  npm run test   # 3 minutes
  # Total: 5 minutes, but default timeout = 60 seconds
  
SYMPTOMS:
  • Hook times out
  • Process killed mid-execution
  • Incomplete results
```

**SOLUTION:**

```json
{
  "hooks": {
    "PostToolUse": [{
      "hooks": [{
        "command": "npm run full-check",
        "timeout": 300  // 5 minutes
      }]
    }]
  }
}

// Or split into parallel hooks:
"hooks": [
  {"command": "npm run build", "timeout": 120},
  {"command": "npm run test", "timeout": 180}
]
// Run in parallel, total time = max(120, 180) = 180s
```

### ❌ MISTAKE 8: Not Handling stdin

```
PROBLEM:
  #!/bin/bash
  echo "Processing..."
  # Doesn't read stdin!
  # Hook input is lost
  
SYMPTOMS:
  • Can't access tool_name, file_path, etc.
  • Hook is useless
  • Errors in downstream processing
```

**SOLUTION:**

```bash
#!/bin/bash
INPUT=$(cat)  # Read stdin first!

FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path')
TOOL=$(echo "$INPUT" | jq -r '.tool_name')

echo "Processing $FILE with $TOOL tool"
```

---

## PART 2: Advanced Patterns

### PATTERN 1: Conditional Hooks Based on File Type

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write:*.ts|Edit:*.ts",
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/ts-checks.sh"
        }]
      },
      {
        "matcher": "Write:*.py|Edit:*.py",
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/py-checks.sh"
        }]
      },
      {
        "matcher": "Write:*.md|Edit:*.md",
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/md-checks.sh"
        }]
      }
    ]
  }
}
```

### PATTERN 2: Staged Validation with Multiple Hooks

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write",
            "timeout": 10
          },
          {
            "type": "command",
            "command": "npx eslint --fix",
            "timeout": 10
          },
          {
            "type": "command",
            "command": "npx tsc --noEmit",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

Hooks run in PARALLEL, so total time = max(10, 10, 15) = 15 seconds.

### PATTERN 3: Chained Decision Making

```bash
#!/bin/bash
# Multi-level validation hook

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path')

# Level 1: Format check
if ! prettier --check "$FILE"; then
  echo "Attempting auto-fix..."
  prettier --write "$FILE"
fi

# Level 2: Lint check
if ! eslint "$FILE"; then
  echo "⚠️  Linting issues found (non-blocking)"
fi

# Level 3: Type check (blocking)
if ! tsc --noEmit; then
  echo "❌ Type errors - must fix"
  exit 2
fi

echo "✅ All checks passed"
exit 0
```

### PATTERN 4: Dynamic Matching Based on Content

```python
#!/usr/bin/env python3
"""
Analyze file content to determine validation strategy
"""

import json
import sys

try:
    data = json.load(sys.stdin)
except:
    sys.exit(0)

file_path = data.get('tool_input', {}).get('file_path', '')

# Read file to determine type
try:
    with open(file_path, 'r') as f:
        content = f.read(500)
except:
    sys.exit(0)

# Custom validation based on content
if '#!/usr/bin/env' in content:
    # It's a script - validate syntax
    import subprocess
    result = subprocess.run(['shellcheck', file_path], capture_output=True)
    if result.returncode != 0:
        print("ShellCheck errors found")
        exit(2)

elif 'import pytest' in content:
    # It's a Python test - run pytest
    import subprocess
    result = subprocess.run(['python', '-m', 'pytest', file_path], capture_output=True)
    if result.returncode != 0:
        print("Tests failed")
        exit(2)

sys.exit(0)
```

### PATTERN 5: Caching for Performance

```bash
#!/bin/bash
"""
Cache expensive operations to avoid re-computation
"""

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path')

CACHE_DIR="/tmp/claude-hooks-cache"
mkdir -p "$CACHE_DIR"

CACHE_FILE="$CACHE_DIR/$(echo $FILE | md5sum | cut -d' ' -f1)"
CACHE_TIME=300  # 5 minutes

# Check if cache is fresh
if [ -f "$CACHE_FILE" ]; then
  AGE=$(($(date +%s) - $(stat -f%m "$CACHE_FILE")))
  if [ $AGE -lt $CACHE_TIME ]; then
    echo "✅ Using cached result"
    cat "$CACHE_FILE"
    exit 0
  fi
fi

# Cache miss - do the expensive operation
RESULT=$(expensive_operation "$FILE")
echo "$RESULT" > "$CACHE_FILE"
echo "$RESULT"
exit 0
```

### PATTERN 6: Parallel Hook Execution Optimization

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "npm run type:check",
            "timeout": 20
          },
          {
            "type": "command",
            "command": "npm run lint",
            "timeout": 20
          },
          {
            "type": "command",
            "command": "npm run test",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

**Key insight:** All 3 hooks run in parallel.
- Total time = max(20, 20, 60) = 60 seconds
- Much faster than sequential (100 seconds)

### PATTERN 7: Remote vs Local Execution

```bash
#!/bin/bash
"""
Run different validations based on execution context
"""

if [ "$CLAUDE_CODE_REMOTE" = "true" ]; then
  # Running in browser/web environment
  # Can't use local tools
  echo "Running lightweight checks (web environment)"
  npm run lint  # Quick check only
else
  # Running in local CLI
  # Can use all local tools
  echo "Running comprehensive checks (local environment)"
  npm run test  # Full test suite
  npm run coverage  # Full coverage report
fi
```

---

## PART 3: Production Deployment Best Practices

### Pre-Deployment Checklist

```
□ Test all hooks locally
  └─ Create test fixtures
  └─ Test success cases
  └─ Test error cases
  └─ Test timeout scenarios

□ Performance validation
  └─ Measure hook execution time
  └─ Ensure <2 seconds for most hooks
  └─ Profile slow operations

□ Security review
  └─ No hardcoded secrets
  └─ Proper input validation
  └─ Safe use of shell features
  └─ Check for injection risks

□ Documentation
  └─ Document what each hook does
  └─ Document failure modes
  └─ Document recovery steps

□ Team review
  └─ Code review of all hooks
  └─ Security review
  └─ Performance sign-off
  └─ Cross-team alignment
```

### Staging Environment Testing

```bash
# Test hooks in staging before production

# 1. Test individual hooks
echo '{"tool_name":"Bash","tool_input":{"command":"npm test"}}' | \
  ./.claude/hooks/my-hook.sh

# 2. Test with real files
STAGING_FILES="src/__staging__/*"
for file in $STAGING_FILES; do
  ./.claude/hooks/validate.sh "$file" || exit 1
done

# 3. Load test
for i in {1..100}; do
  ./.claude/hooks/fast-hook.sh || exit 1
done

echo "✅ All tests passed"
```

### Monitoring & Logging

```bash
#!/bin/bash
"""
Production hook with logging & monitoring
"""

set -e

HOOK_NAME="my-quality-hook"
LOG_FILE="/var/log/claude-hooks.log"
METRICS_FILE="/var/log/claude-hooks-metrics.log"

START_TIME=$(date +%s%N)

echo "[$(date)] HOOK_START: $HOOK_NAME" >> "$LOG_FILE"

# Run validation
if npm run quality-checks; then
  RESULT="SUCCESS"
else
  RESULT="FAILURE"
fi

END_TIME=$(date +%s%N)
DURATION_MS=$(( (END_TIME - START_TIME) / 1000000 ))

# Log metrics
echo "$(date +%s) $HOOK_NAME $RESULT $DURATION_MS" >> "$METRICS_FILE"

# Alert if slow
if [ $DURATION_MS -gt 5000 ]; then
  echo "⚠️  SLOW_HOOK: $HOOK_NAME took ${DURATION_MS}ms" >> "$LOG_FILE"
fi

if [ "$RESULT" = "SUCCESS" ]; then
  echo "[$(date)] HOOK_END: $HOOK_NAME (${DURATION_MS}ms)" >> "$LOG_FILE"
  exit 0
else
  echo "[$(date)] HOOK_FAILED: $HOOK_NAME (${DURATION_MS}ms)" >> "$LOG_FILE"
  exit 2
fi
```

### Rollback Strategy

```json
{
  "hooks": {
    "_comment": "Hooks can be quickly disabled by moving entries",
    
    "PreToolUse_DISABLED": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Hook disabled for rollback'"
          }
        ]
      }
    ]
  }
}
```

To rollback: Rename `PreToolUse` → `PreToolUse_DISABLED`

---

## PART 4: Troubleshooting Guide

### Hook Not Executing

```bash
# Check 1: Is hook registered?
cat .claude/settings.json | jq .hooks

# Check 2: Run with debug mode
claude --debug

# Check 3: Test hook directly
cat input.json | ./my-hook.sh
echo $?  # Should be 0 (allow) or 2 (block)

# Check 4: Check JSON validity
jq . .claude/settings.json || echo "Invalid JSON"

# Check 5: Check file permissions
ls -la .claude/hooks/
chmod +x .claude/hooks/*.sh
```

### Hook Blocking Unexpectedly

```bash
# Test the exact input causing issues
echo "$INPUT_JSON" | ./hook.sh
echo $?  # Check exit code

# Debug the hook
bash -x ./hook.sh 2>&1  # Verbose mode

# Check conditionals
if [[ "$FILE" == *.ts ]]; then
  echo "Condition matched: $FILE is TypeScript"
fi
```

### Hook Timeout

```bash
# Measure actual execution time
time ./my-hook.sh

# If >60 seconds, increase timeout:
{
  "type": "command",
  "command": "...",
  "timeout": 120  // 2 minutes
}

# Or optimize the hook:
- Cache results
- Run in parallel
- Remove unnecessary operations
```

---

**Версия**: 1.0  
**Дата**: 2025-01-07  
**Статус**: Reference guide for production use  
**Используй это руководство перед развертыванием в production**

---

## Related Guides

### Getting Started
- [INDEX.md](INDEX.md) - Master documentation index
- [Complete Practices](CLAUDE-COMPLETE-PRACTICES.md) - Overview of all features (Russian)

### Core Features
- [Shared Architecture](claude-shared-architecture.md) - System overview
- [CLAUDE.md Guide](CLAUDE-CLAUDE-MD-GUIDE.md) - Project memory (English)

### Automation
- [Hooks Guide](claude-hooks-guide.md) - Workflow automation
- [Hooks Examples](claude-hooks-examples.md) - Production examples
- [Hooks Advanced](claude-hooks-advanced.md) - Advanced patterns

### Custom Capabilities
- [Skills Guide](claude-skills-guide.md) - Custom skills
- [Agents Guide](claude-agents-guide.md) - Agent system
- [Templates](claude-templates.md) - Template system

### Reference
- [Troubleshooting](claude-troubleshooting.md) - Common issues

