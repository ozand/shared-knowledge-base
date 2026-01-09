# KB-UPDATE-001: Agent Commands for Shared KB Updates

⚠️ **FOR AI AGENTS UPDATING SHARED KB:**

When updating Shared Knowledge Base, AI agents MUST follow this workflow:

## CRITICAL RULES

1. ✅ Always use `git submodule` commands (NEVER direct access)
2. ✅ Verify state before referencing (check issues/PRs first)
3. ✅ Interpret status output correctly
4. ❌ Never use `git -C` or `cd` into submodule

## Complete Agent Workflow

### Step 1: Check submodule status (ALWAYS FIRST)

```bash
git submodule status docs/knowledge-base/shared
# Output:  c023036 docs/knowledge-base/shared (v5.1-10-gc023036)
#          ^ Leading space = properly initialized ✅
```

### Step 2: Verify before referencing resources

```bash
# Example: Check if Issue #11 is still open
gh issue view 11 --json state,title
# If CLOSED: Don't reference it (STALE-CONTEXT-001)
```

### Step 3: Update submodule

```bash
git submodule update --remote docs/knowledge-base/shared
# No output = already up to date (this is GOOD!)
# Output with commits = update applied
```

### Step 4: Verify update succeeded

```bash
git submodule status docs/knowledge-base/shared
# Compare commit hash: if different = updated, if same = was already latest
```

### Step 5: Use KB tools

```bash
python3 docs/knowledge-base/shared/tools/kb.py stats
```

## Verification Checklist

- [ ] First command: `git submodule status` (not `git -C` or `cd`)
- [ ] Verified issue/PR state before referencing
- [ ] Interpreted status symbols correctly (space=good, -=bad, +=warning)
- [ ] Working from project root (not inside submodule)
- [ ] Used relative paths (not absolute)

## Forbidden Patterns (NEVER do these)

```bash
# ❌ WRONG - Direct access
git -C docs/knowledge-base/shared fetch origin
cd docs/knowledge-base/shared && git pull

# ❌ WRONG - Not verifying first
echo "Waiting for Issue #11"  # Issue might be closed!

# ❌ WRONG - Assuming state
gh pr view 12  # Might be merged or closed
```

## Required Patterns (ALWAYS do these)

```bash
# ✅ CORRECT - Submodule commands
git submodule status docs/knowledge-base/shared
git submodule update --remote docs/knowledge-base/shared

# ✅ CORRECT - Verify first
ISSUE_STATE=$(gh issue view 11 --json state --jq '.state')
[ "$ISSUE_STATE" = "OPEN" ] && echo "Issue #11 open" || echo "Issue #11 closed"

# ✅ CORRECT - Check actual state
gh pr view 12 --json state,merged
```

## Interpreting Status Output

See SUBMODULE-STATUS-INTERPRETATION-001 for complete reference:

- ` c023036` (leading space) = ✅ Properly initialized
- `-c023036` (minus sign) = ❌ Not initialized
- `+c023036` (plus sign) = ⚠️ Uncommitted changes
- `-U c023036` (U suffix) = ❌ Merge conflict

## What "No output" Means

```bash
git submodule update --remote docs/knowledge-base/shared
# No output = Already up to date ✅ (This is GOOD!)
```

## Real-World Examples

### Example 1: Correct workflow

```bash
# User asks: "обнови статус Share KB используя git submodule commands"

# Agent responds:
git submodule status docs/knowledge-base/shared
# Output:  c023036 docs/knowledge-base/shared (v5.1-10-gc023036)

git submodule update --remote docs/knowledge-base/shared
# No output (already up to date)

git submodule status docs/knowledge-base/shared
# Output:  c023036 docs/knowledge-base/shared (v5.1-10-gc023036)
# Same commit = confirmed already was at latest

python3 docs/knowledge-base/shared/tools/kb.py stats
# Output: Shared KB v5.1-10-gc023036, 95 entries indexed
```

### Example 2: Stale context prevented

```bash
# Agent wants to reference Issue #11

# CORRECT - Verify first
gh issue view 11 --json state,title
# Output: state: "closed", title: "..."

# Result: Don't reference Issue #11, it's closed
# Prevented: "Waiting for Issue #11" mistake
```

### Example 3: Status interpretation

```bash
git submodule status docs/knowledge-base/shared
# Output:  c023036 docs/knowledge-base/shared (v5.1-10-gc023036)

# Agent interpretation:
# - Leading space = properly initialized ✅
# - c023036 = current commit hash
# - v5.1-10-gc023036 = 10 commits ahead of v5.1 tag (effectively v5.1)
# - No + symbol = no uncommitted changes ✅
# - Status: Healthy, ready for update
```

## Related Patterns

- **AGENT-DIRECT-SUBMODULE-ACCESS-001** - Why direct access is forbidden
- **SUBMODULE-STATUS-INTERPRETATION-001** - Understanding status symbols
- **STALE-CONTEXT-001** - Verify before referencing
- **AGENT-QUICK-START.md** - Complete agent quick reference
