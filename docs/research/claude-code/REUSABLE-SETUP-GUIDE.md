# Reusable Claude Code Configuration Guide
## How to use shared-knowledge-base Claude Code setup in your projects

**Version:** 1.0
**Last Updated:** 2026-01-07
**Source Repository:** https://github.com/ozand/shared-knowledge-base

---

## Overview

The shared-knowledge-base repository includes a production-ready Claude Code configuration with:
- **Navigation Hub** (.claude/CLAUDE.md) - Project instructions for Claude Code
- **Automated Hooks** - Quality gates, validation, auto-formatting
- **Best Practices** - Battle-tested patterns for knowledge management

This guide shows how to **reuse this configuration** in your own repositories.

---

## Quick Start

### Option 1: Copy-Paste (Fastest)

```bash
# In your project repository
git clone https://github.com/ozand/shared-knowledge-base.git /tmp/skb
cp -r /tmp/skb/.claude ./
rm -rf /tmp/skb

# Customize CLAUDE.md for your project
nano .claude/CLAUDE.md
```

### Option 2: Git Submodule (Recommended for teams)

```bash
# Add shared-knowledge-base as submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git .claude/shared

# Create symlink to CLAUDE.md
ln -s .claude/shared/.claude/CLAUDE.md .claude/CLAUDE.md

# Or copy and customize
cp .claude/shared/.claude/CLAUDE.md .claude/CLAUDE.md
```

### Option 3: NPM Package (Coming soon)

```bash
npm install --save-dev @shared-kb/claude-code-config
```

---

## File Structure

After installation, your project will have:

```
your-project/
├── .claude/
│   ├── CLAUDE.md                (customize for your project)
│   ├── settings.json            (hooks configuration)
│   └── hooks/                   (automation scripts)
│       ├── validate-yaml-before-write.sh
│       ├── quality-gate.sh
│       ├── auto-format-yaml.sh
│       ├── auto-create-metadata.sh
│       └── session-setup.sh
└── .gitignore                   (updated to exclude .local files)
```

---

## Customization Steps

### 1. Update CLAUDE.md for Your Project

Edit `.claude/CLAUDE.md` to reflect your project:

```markdown
# Your Project Name - Claude Code Instructions

**Repository:** your-org/your-project
**Version:** 1.0.0
**Last Updated:** 2026-01-07

---

## Overview

This is the [Your Project] repository - [brief description].

## Quick Start

### Essential Commands

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

## Architecture

### Tech Stack
- Frontend: React 18, TypeScript, Tailwind
- Backend: FastAPI, PostgreSQL
- Testing: Vitest, Playwright

### Directory Structure

```
your-project/
├── src/               # Source code
├── tests/             # Test files
├── docs/              # Documentation
└── scripts/           # Build scripts
```

## Common Tasks

### Adding a New Feature

1. Create feature branch
2. Implement feature
3. Add tests
4. Run quality checks
5. Submit PR

### Debugging

- Check logs: `tail -f logs/app.log`
- Run debugger: `npm run debug`
- View test coverage: `npm run test:coverage`

## Documentation

- Architecture: @docs/architecture.md
- API Reference: @docs/api.md
- Contributing: @CONTRIBUTING.md

---
```

**Key customization points:**
- Change project name and description
- Update commands (npm, python, make, etc.)
- Reflect your tech stack
- Link to your documentation

---

### 2. Adapt Hooks for Your Project

Edit `.claude/settings.json` to match your project needs:

#### For TypeScript Projects

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write:*.ts|Edit:*.ts",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write",
            "timeout": 10
          },
          {
            "type": "command",
            "command": "npx eslint --fix",
            "timeout": 15
          },
          {
            "type": "command",
            "command": "npx tsc --noEmit",
            "timeout": 20
          }
        ]
      }
    ]
  }
}
```

#### For Python Projects

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write:*.py|Edit:*.py",
        "hooks": [
          {
            "type": "command",
            "command": "black $FILE",
            "timeout": 5
          },
          {
            "type": "command",
            "command": "pylint $FILE",
            "timeout": 10
          },
          {
            "type": "command",
            "command": "mypy $FILE",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

#### For Go Projects

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write:*.go|Edit:*.go",
        "hooks": [
          {
            "type": "command",
            "command": "gofmt -w $FILE",
            "timeout": 5
          },
          {
            "type": "command",
            "command": "go vet ./...",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

---

### 3. Update .gitignore

Ensure your `.gitignore` includes:

```gitignore
# Claude Code local configuration (team config is committed)
.claude/*.local
.claude/*.local.*
.claude/.local/

# But .claude/ itself IS committed!
```

**IMPORTANT:** Commit `.claude/` to git (except .local files)

```bash
# Correct: .claude/ is in git
git add .claude/
git commit -m "Add Claude Code configuration"

# Local overrides stay local
# .claude/settings.local.json (not committed)
```

---

## Hook Reference

### Available Events

| Event | When Fires | Use For |
|-------|-----------|---------|
| **PreToolUse** | Before tool execution | Validation, blocking, modification |
| **PostToolUse** | After tool execution | Formatting, testing, quality gates |
| **SessionStart** | When Claude starts | Context loading, environment setup |
| **Stop** | When Claude finishes | Validation, reminders, cleanup |
| **UserPromptSubmit** | When user submits prompt | Prompt validation, context enrichment |
| **Notification** | When Claude sends notification | Desktop alerts, sounds |

### Matcher Syntax

```json
{
  "matcher": "Bash"              // Only Bash commands
  "matcher": "Edit|Write"         // Edit OR Write tools
  "matcher": "Edit:*.ts"         // Only TypeScript edits
  "matcher": "Write:*.yaml"      // Only YAML file creation
  "matcher": "mcp__.*__write"    // Any MCP write operation
  "matcher": "*"                 // All tools (use carefully!)
}
```

### Hook Output

#### For PreToolUse (blocking):

```python
{
  "decision": "block",  // or "allow"
  "reason": "Security risk detected",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "updatedInput": {
      // Modified tool input (optional)
    }
  }
}
```

#### For PostToolUse (feedback):

```python
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "feedback": "Quality checks passed",
    "additionalContext": "Run tests to verify"
  }
}
```

---

## Best Practices

### ✅ DO:

1. **Keep CLAUDE.md lean** (~300 lines)
   - Acts as navigation hub
   - Links to detailed docs
   - Quick reference for commands

2. **Use specific matchers**
   - `"Edit:*.ts"` not `"*"`
   - Reduces hook execution overhead

3. **Keep hooks fast** (<2 seconds)
   - Heavy operations → CI/CD
   - Hooks are for immediate feedback

4. **Test hooks manually**
   ```bash
   echo '{"tool_input":{"file_path":"src/test.ts"}}' | \
     python .claude/hooks/quality-gate.sh
   ```

5. **Provide clear error messages**
   - What went wrong?
   - How to fix it?
   - Link to documentation

### ❌ DON'T:

1. **Don't run full test suite in hooks**
   - Tests in CI/CD, not hooks
   - Hooks should be <2 seconds

2. **Don't use wildcard matchers unnecessarily**
   - `"matcher": "*"` slows everything
   - Be specific: `"Bash"`, `"Edit|Write"`

3. **Don't hardcode secrets**
   - Use environment variables
   - Load from SessionStart hook

4. **Don't forget to commit .claude/**
   - Team shares configuration
   - Only .local files are ignored

5. **Don't make hooks too complex**
   - Start simple
   - Add complexity gradually
   - Test thoroughly

---

## Example: Complete Setup for TypeScript Project

### Step 1: Copy configuration

```bash
git clone https://github.com/ozand/shared-knowledge-base.git /tmp/skb
cp -r /tmp/skb/.claude ./
rm -rf /tmp/skb
```

### Step 2: Customize CLAUDE.md

```bash
nano .claude/CLAUDE.md
```

Replace content with your project info (see customization section above).

### Step 3: Update hooks for TypeScript

Edit `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": ".claude/hooks/security-check.sh",
          "timeout": 5
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write:*.ts|Edit:*.ts|Write:*.tsx|Edit:*.tsx",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write $FILE",
            "timeout": 10
          },
          {
            "type": "command",
            "command": "npx eslint --fix $FILE",
            "timeout": 15
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [{
          "type": "command",
          "command": ".claude/hooks/session-setup.sh",
          "timeout": 10
        }]
      }
    ]
  }
}
```

### Step 4: Create security hook

```bash
cat > .claude/hooks/security-check.sh << 'EOF'
#!/usr/bin/env python
import sys, json, re

data = json.load(sys.stdin)
if data.get('tool_name') != 'Bash':
    sys.exit(0)

cmd = data.get('tool_input', {}).get('command', '')

# Block dangerous commands
dangerous = [
    r'rm\s+-rf\s+/',
    r'sudo\s+rm',
    r'chmod\s+777'
]

for pattern in dangerous:
    if re.search(pattern, cmd, re.IGNORECASE):
        output = {
            'decision': 'block',
            'reason': f'Dangerous command blocked: {pattern}'
        }
        print(json.dumps(output))
        sys.exit(0)

sys.exit(0)
EOF

chmod +x .claude/hooks/security-check.sh
```

### Step 5: Test configuration

```bash
# Test session setup
./.claude/hooks/session-setup.sh

# Test quality gate
echo '{"tool_input":{"file_path":"src/test.ts"}}' | \
  python .claude/hooks/quality-gate.sh
```

### Step 6: Commit to git

```bash
git add .claude/
git add .gitignore
git commit -m "Add Claude Code configuration

- CLAUDE.md with project instructions
- Hooks for quality, formatting, security
- Session setup for context loading
- Updated .gitignore for local overrides

🤖 Generated with Claude Code
"
git push origin main
```

---

## Troubleshooting

### Hook not executing

**Symptom:** Hook doesn't run when expected

**Checks:**
```bash
# 1. Is hook in settings.json?
cat .claude/settings.json | jq .hooks

# 2. Is hook executable?
ls -la .claude/hooks/

# 3. Test hook manually
echo '{"tool_name":"Bash","tool_input":{"command":"test"}}' | \
  python .claude/hooks/your-hook.sh
```

**Fixes:**
- Ensure `chmod +x` on hook scripts
- Check JSON syntax in settings.json
- Verify matcher pattern matches your tool

### Hook too slow

**Symptom:** Long pauses during editing

**Diagnosis:**
```bash
# Measure hook execution time
time echo '{"tool_input":{"file_path":"test.ts"}}' | \
  python .claude/hooks/slow-hook.sh
```

**Solutions:**
- Move heavy operations to CI/CD
- Add caching
- Run checks in parallel (multiple hooks in same event)
- Increase timeout in settings.json

### Hook blocking unexpectedly

**Symptom:** Operations blocked without clear reason

**Debug:**
```bash
# Test hook with exact input
echo YOUR_INPUT | python .claude/hooks/blocking-hook.sh
echo $?  # Exit code: 0 = allow, 2 = block
```

**Fixes:**
- Check exit codes (0 = allow, 2 = block)
- Review hook logic
- Add verbose logging for debugging

---

## Advanced Patterns

### Pattern 1: Conditional Hooks

Different hooks for different file types:

```json
{
  "PostToolUse": [
    {
      "matcher": "Write:*.ts|Edit:*.ts",
      "hooks": [{"command": "npx eslint --fix"}]
    },
    {
      "matcher": "Write:*.py|Edit:*.py",
      "hooks": [{"command": "black"}]
    },
    {
      "matcher": "Write:*.go|Edit:*.go",
      "hooks": [{"command": "gofmt -w"}]
    }
  ]
}
```

### Pattern 2: Parallel Execution

Multiple hooks in same event run in parallel:

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit:*.ts",
      "hooks": [
        {"command": "npx prettier --write", "timeout": 10},
        {"command": "npx eslint --fix", "timeout": 10},
        {"command": "npx tsc --noEmit", "timeout": 15}
      ]
    }
  ]
}
```

**Total time:** max(10, 10, 15) = 15 seconds (not 35!)

### Pattern 3: Prompt-Based Decisions

Use LLM for context-aware decisions:

```json
{
  "Stop": [{
    "hooks": [{
      "type": "prompt",
      "prompt": "Evaluate if all tasks complete. Context: $ARGUMENTS\n\nRespond JSON: {\"decision\":\"approve\"|\"block\", \"reason\":\"...\"}",
      "timeout": 30
    }]
  }]
}
```

---

## Resources

### Documentation

- **Shared KB:** https://github.com/ozand/shared-knowledge-base
- **Claude Code:** https://claude.com/claude-code
- **Hooks Guide:** @docs/research/claude-code/claude-hooks-guide.md
- **Hooks Examples:** @docs/research/claude-code/claude-hooks-examples.md
- **Architecture:** @docs/research/claude-code/claude-shared-architecture.md

### Patterns

- **Shared Model:** @universal/patterns/claude-code-shared-model.yaml
- **Hooks:** @universal/patterns/claude-code-hooks.yaml
- **Agent Orchestration:** @universal/patterns/agent-orchestration.yaml

### Community

- **Issues:** https://github.com/ozand/shared-knowledge-base/issues
- **Discussions:** https://github.com/ozand/shared-knowledge-base/discussions

---

## Checklist

Before deploying to your team:

- [ ] CLAUDE.md customized for project
- [ ] Hooks tested manually
- [ ] settings.json adapted to tech stack
- [ ] .gitignore updated
- [ ] All hooks executable (`chmod +x`)
- [ ] SessionStart hook loads correct context
- [ ] Quality gates match team standards
- [ ] Team members trained on hooks
- [ ] Documentation updated
- [ ] Committed to git

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Author:** Shared KB Curator
**License:** MIT (feel free to reuse and modify)
