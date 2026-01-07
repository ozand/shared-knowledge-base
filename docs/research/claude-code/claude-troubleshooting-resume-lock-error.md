# Claude Code: history.jsonl.lock Error — Troubleshooting Guide

## Problem Overview

**Error:**
```
Error: EBADF: bad file descriptor, realpath 'C:\Users\ozand\.claude\history.jsonl.lock'
    at async realpath (node:internal/fs/promises:1164:10)
```

This error occurs when Claude Code attempts to access conversation history through `--resume` or other history-related operations, but encounters a corrupted or stuck lock file.

---

## Root Cause Analysis

### When This Error Occurs

The error is **triggered specifically** when:
1. Running `claude --resume` — main trigger
2. Running `claude --continue` — also accesses history
3. Any operation that reads `~/.claude/history.jsonl`

### Why It Happens

1. **Stale Lock File** — Previous Claude Code process terminated abnormally (crash, force quit, power loss) and left `history.jsonl.lock` behind

2. **Corrupted JSON in History** — Sessions with previous 400 API errors have malformed JSON entries that cause lock acquisition failures ([GitHub Issue #2105](https://github.com/anthropics/claude-code/issues/2105))

3. **Large History File** — When `history.jsonl` contains 2000+ entries, the resume picker can fail silently ([GitHub Issue #10763](https://github.com/anthropics/claude-code/issues/10763))

4. **Multiple Instance Race** — Running multiple Claude Code instances simultaneously causes contention on shared `~/.claude/` directory ([GitHub Issue #15334](https://github.com/anthropics/claude-code/issues/15334))

### Fundamental Architecture Issue

From [GitHub Issue #14674](https://github.com/anthropics/claude-code/issues/14674):
> "The `.claude.json` architecture is fundamentally broken: **No atomic writes → file corruption on crash/interrupt**"

---

## Solutions

### Solution 1: Remove Lock File (Quick Fix)

**Windows:**
```powershell
# 1. Kill all Claude Code processes
taskkill /F /IM node.exe

# 2. Remove the lock file
del %USERPROFILE%\.claude\history.jsonl.lock

# 3. Restart Claude Code
claude
```

**Linux/macOS:**
```bash
# 1. Kill all Claude Code processes
pkill -f "claude-code"

# 2. Remove the lock file
rm -f ~/.claude/history.jsonl.lock

# 3. Restart Claude Code
claude
```

---

### Solution 2: Truncate Large History File

When `history.jsonl` is too large (2000+ entries):

**Windows PowerShell:**
```powershell
# 1. Create backup
copy %USERPROFILE%\.claude\history.jsonl %USERPROFILE%\.claude\history.jsonl.backup

# 2. Keep only last 500 entries
(Get-Content %USERPROFILE%\.claude\history.jsonl -Tail 500) | Set-Content %USERPROFILE%\.claude\history.jsonl

# 3. Remove lock
del %USERPROFILE%\.claude\history.jsonl.lock
```

**Linux/macOS:**
```bash
# 1. Create backup
cp ~/.claude/history.jsonl ~/.claude/history.jsonl.backup

# 2. Keep only last 500 entries
tail -n 500 ~/.claude/history.jsonl > ~/.claude/history.jsonl.tmp
mv ~/.claude/history.jsonl.tmp ~/.claude/history.jsonl

# 3. Remove lock
rm -f ~/.claude/history.jsonl.lock
```

---

### Solution 3: Fix Corrupted JSON (Advanced)

If the file contains malformed JSON entries:

**Using Python:**
```python
#!/usr/bin/env python3
import json
import os

history_path = os.path.expanduser('~/.claude/history.jsonl')
backup_path = os.path.expanduser('~/.claude/history.jsonl.corrupt')
output_path = os.path.expanduser('~/.claude/history.jsonl.fixed')

# Backup original
os.rename(history_path, backup_path)

# Filter valid JSON lines only
valid_lines = []
with open(backup_path, 'r', encoding='utf-8') as f:
    for line_num, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            json.loads(line)
            valid_lines.append(line)
        except json.JSONDecodeError as e:
            print(f"Skipping invalid line {line_num}: {e}")

# Write cleaned file
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(valid_lines))

print(f"Cleaned: {len(valid_lines)} valid lines (from {line_num} total)")

# Replace original
os.rename(output_path, history_path)

# Remove lock
lock_path = os.path.expanduser('~/.claude/history.jsonl.lock')
if os.path.exists(lock_path):
    os.remove(lock_path)
```

---

### Solution 4: Use --continue Instead of --resume

If `--resume` fails, try loading only the most recent session:

```bash
claude --continue
```

This bypasses the interactive picker and only loads the latest conversation.

---

### Solution 5: Nuclear Option (Complete Reset)

⚠️ **WARNING:** This deletes ALL conversation history

**Windows:**
```powershell
del %USERPROFILE%\.claude\history.jsonl
del %USERPROFILE%\.claude\history.jsonl.lock
```

**Linux/macOS:**
```bash
rm ~/.claude/history.jsonl
rm ~/.claude/history.jsonl.lock
```

---

## Prevention & Best Practices

### 1. Avoid Multiple Instances

❌ **Don't run multiple Claude Code instances simultaneously**
- No multiple terminal windows with `claude --resume`
- Close VS Code with Claude extension before using CLI

### 2. Monitor History Size

**Check history file size regularly:**

**Windows:**
```powershell
(Get-Content %USERPROFILE%\.claude\history.jsonl).Count
```

**Linux/macOS:**
```bash
wc -l ~/.claude/history.jsonl
```

If > 1000 lines, consider truncating (see Solution 2).

### 3. Graceful Shutdown

✅ **Do:**
- Exit Claude Code normally (`exit` or `Ctrl+D`)
- Let operations complete before closing terminal

❌ **Don't:**
- Force quit with `Ctrl+C` during file operations
- Kill terminal/shell while Claude Code is running
- Shut down computer while Claude Code is active

### 4. Regular Maintenance

**Set up periodic cleanup (cron/Task Scheduler):**

**Linux/macOS (crontab):**
```bash
# Run weekly: keep last 1000 entries
0 0 * * 0 tail -n 1000 ~/.claude/history.jsonl > ~/.claude/history.jsonl.tmp && mv ~/.claude/history.jsonl.tmp ~/.claude/history.jsonl
```

**Windows (Task Scheduler):**
```powershell
# Create scheduled task script: cleanup-claude-history.ps1
$count = (Get-Content $env:USERPROFILE\.claude\history.jsonl).Count
if ($count -gt 1000) {
    (Get-Content $env:USERPROFILE\.claude\history.jsonl -Tail 1000) | Set-Content $env:USERPROFILE\.claude\history.jsonl
}
```

---

## Alternative Tools

### [claude-cleaner](https://jsr.io/@tylerbu/claude-cleaner)
Tool for cleaning up bloated `history.jsonl` files.

### [claude-JSONL-browser](https://www.claude-hub.com/resource/github-cli-withLinda-claude-JSONL-browser-claude-JSONL-browser/)
Browser for inspecting and managing JSONL files.

---

## Related Issues & References

### GitHub Issues
- [[BUG] --resume does not work with a large database #10763](https://github.com/anthropics/claude-code/issues/10763)
- [Claude --resume sessions with 400 errors unusable #2105](https://github.com/anthropics/claude-code/issues/2105)
- [Support per-instance config directory for multi-agent #15334](https://github.com/anthropics/claude-code/issues/15334)
- [Bug: Multiple Claude Code instances spawning #9658](https://github.com/anthropics/claude-code/issues/9658)
- [continue broken after using claude --resume #10063](https://github.com/anthropics/claude-code/issues/10063)

### External References
- [Claude code使用老是显示history.jsonl.lock错误 (Chinese forum with fix)](https://linux.do/t/topic/1373942)
- [How to Fix the "Another Process is Currently Updating Claude" Error](https://www.ramanean.com/how-to-fix-the-another-process-is-currently-updating-claude-error-in-claude-code/)
- [How to Clean Up Local Claude Code Cache and Data](https://ctok.ai/en/claude-code-cleanup)

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│  ERROR: EBADF bad file descriptor history.jsonl.lock        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  QUICK FIX:                                                 │
│  1. Kill: taskkill /F /IM node.exe (Windows)               │
│  2. Delete lock file                                       │
│  3. Restart claude                                          │
│                                                             │
│  IF LARGE FILE (>2000 lines):                               │
│  → Keep last 500 entries only                              │
│                                                             │
│  IF CORRUPTED JSON:                                         │
│  → Filter valid JSON lines using Python/script             │
│                                                             │
│  PREVENTION:                                                │
│  → One instance at a time                                  │
│  → Check size monthly (>1000 = truncate)                   │
│  → Graceful shutdown only                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Version History

- **v1.0** (2026-01-07) — Initial documentation based on community research and GitHub issues

---

## Contributing

If you encounter variations of this error or discover new solutions, please document:
1. Exact error message
2. Claude Code version
3. OS and platform
4. What triggered the error
5. What fixed it (or didn't)

Report to: https://github.com/anthropics/claude-code/issues

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

