# AI Agent Quick Start Guide
## For agents working with Shared Knowledge Base

**Version:** 1.0
**Last Updated:** 2026-01-06
**Auto-loaded:** All agents read `universal/agent-instructions/base-instructions.yaml`

---

## CRITICAL RULES (READ FIRST)

### 1. Git Submodule Access (CRITICAL)

❌ **NEVER do this:**
```bash
# WRONG - Direct access to submodule
git -C docs/knowledge-base/shared fetch origin
cd docs/knowledge-base/shared && git pull
```

✅ **ALWAYS do this:**
```bash
# CORRECT - Use submodule commands from project root
git submodule status docs/knowledge-base/shared
git submodule update --remote docs/knowledge-base/shared
```

**Why:** Direct access breaks `.gitmodules` synchronization and submodule state.
**See:** `AGENT-DIRECT-SUBMODULE-ACCESS-001`

---

### 2. Role-Based Access Control

**Project Agents:**
- ✅ Search KB, validate YAML, create GitHub issues
- ❌ Commit to shared-knowledge-base, create PRs, modify KB files

**Curator Agent:**
- ✅ Review issues, validate, enhance, commit to KB
- 🎯 **ONLY** Curator commits to KB

**See:** `AGENT-ROLE-SEPARATION-001`

---

### 3. Verify Before Referencing (STALE CONTEXT)

❌ **NEVER assume state:**
```bash
# WRONG - Assumes Issue #11 is still open
echo "Waiting for Issue #11"
```

✅ **ALWAYS verify first:**
```bash
# CORRECT - Check current state
gh issue view 11 --json state,title
```

**Why:** Issues/PRs may close between sessions.
**See:** `STALE-CONTEXT-001`

---

## INSTALLATION (For NEW Projects)

**For agents setting up Shared KB in a new project:**

### Unified Installation (Recommended)

```bash
# Method 1: From cloned repository
python scripts/unified-install.py --full

# Method 2: Remote download (one-line)
curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/unified-install.py | python3 - --full
```

**What it does:**
- ✅ Adds submodule with sparse checkout (excludes curator/)
- ✅ Installs agents (1 main + 4 subagents)
- ✅ Installs skills (7 skills)
- ✅ Installs commands (7 commands)
- ✅ Creates configuration files
- ✅ Builds search index
- ✅ Verifies installation

**For existing projects:**
```bash
# Check for updates
python docs/knowledge-base/shared/scripts/unified-install.py --check

# Update existing installation
python docs/knowledge-base/shared/scripts/unified-install.py --update
```

**See:** `UNIFIED-INSTALL-001` pattern

### Manual Installation (Fallback)

```bash
# Add submodule
git submodule add https://github.com/ozand/shared-knowledge-base.git docs/knowledge-base/shared

# Install integration
python docs/knowledge-base/shared/for-projects/scripts/install.py --full
```

**Note:** Unified installation is preferred for cross-platform compatibility and automation.

---

## SUBMODULE STATUS REFERENCE

When you run `git submodule status`, the first character matters:

| Symbol | Meaning | Action Required |
|--------|---------|-----------------|
| ` ` (space) | ✅ Good | None |
| `-` | ❌ Not initialized | `git submodule init` |
| `+` | ⚠️ Uncommitted changes | Commit or stash |
| `U` | ❌ Merge conflict | Resolve conflict |
| `-<num>` | ⚠️ Commits ahead | Update submodule |

**Example:**
```
 c023036 docs/knowledge-base/shared (v3.0-10-gc023036)
```
Leading space = properly initialized ✅

**See:** `SUBMODULE-STATUS-INTERPRETATION-001`

---

## CORRECT SUBMODULE WORKFLOW

**Step 1: Check status**
```bash
git submodule status docs/knowledge-base/shared
```

**Step 2: Update if needed**
```bash
git submodule update --remote docs/knowledge-base/shared
```

**Step 3: Verify update**
```bash
git submodule status docs/knowledge-base/shared
```

**Step 4: Use KB tools**
```bash
python3 docs/knowledge-base/shared/tools/kb.py stats
```

**See:** `KB-UPDATE-001`

---

## CONTRIBUTING TO SHARED KB

**Project Agent workflow:**

1. Search KB first:
   ```bash
   kb search '{pattern_keywords}'
   ```

2. Create YAML locally (NOT in KB):
   ```bash
   # In YOUR project, not shared-knowledge-base
   cat > my-pattern.yaml << 'EOF'
   version: "1.0"
   category: "pattern-category"
   last_updated: "2026-01-06"
   patterns: ...
   EOF
   ```

3. Validate:
   ```bash
   python tools/kb.py validate my-pattern.yaml
   ```

4. Create GitHub issue with FULL YAML:
   ```bash
   gh issue create \
     --label "agent:claude-code" \
     --label "project:MYPROJECT" \
     --label "kb-improvement" \
     --body-file issue-template.md
   ```

5. Wait for Curator (24h SLA)

6. Pull updates after merge:
   ```bash
   cd docs/knowledge-base/shared && git pull
   ```

**See:** `AGENT-HANDOFF-001`

---

## COMMON MISTAKES TO AVOID

### ❌ Mistake 1: External File References

**Wrong:**
```
The complete YAML file is located at:
docs/knowledge-base/shared/universal/patterns/pattern.yaml
```

**Correct:**
```markdown
## Full YAML content:

```yaml
version: "1.0"
category: "pattern-category"
# ... complete YAML content ...
```
```

**Why:** Curator cannot access your local filesystem.
**See:** `AGENT-HANDOFF-FAILURE-001`

---

### ❌ Mistake 2: Not Being Explicit

**Vague request:**
```
"Update Shared KB status"
→ Agent chooses direct access (simpler but wrong)
```

**Explicit request:**
```
"Update Shared KB status using git submodule commands"
→ Agent uses correct workflow
```

**Why:** Agents choose path of least resistance. Be explicit.

---

### ❌ Mistake 3: Assuming Previous Context

**Wrong:**
```bash
# Assume Issue #11 still pending from previous session
gh issue view 11
```

**Correct:**
```bash
# Verify current state first
gh issue view 11 --json state
# Output: "state": "closed" → Don't reference it
```

**Why:** Sessions don't share state. Always verify.
**See:** `STALE-CONTEXT-001`

---

## VERIFICATION CHECKLIST

Before acting, verify:

- [ ] Checked `git submodule status` before submodule operations
- [ ] Using `git submodule` commands (not `git -C` or `cd`)
- [ ] Verified issue/PR state before referencing
- [ ] Searched KB for existing patterns before creating new ones
- [ ] Validated YAML before creating GitHub issue
- [ ] Using relative paths from project root
- [ ] Never committing to shared-knowledge-base (unless Curator)

---

## QUICK REFERENCE COMMANDS

### Submodule Operations
```bash
# Check status
git submodule status docs/knowledge-base/shared

# Update submodule
git submodule update --remote docs/knowledge-base/shared

# Initialize if needed
git submodule update --init --recursive docs/knowledge-base/shared
```

### GitHub Operations
```bash
# Check issue state
gh issue view NUMBER --json state,title

# Create issue with attribution
gh issue create \
  --label "agent:claude-code" \
  --label "project:MYPROJECT" \
  --label "kb-improvement" \
  --title "Add PATTERN-XXX: Pattern Name" \
  --body-file issue-template.md

# Check PR state
gh pr view NUMBER --json state,merged
```

### KB Operations
```bash
# Search KB
kb search '{query}'

# Validate YAML
python tools/kb.py validate pattern.yaml

# KB statistics
python tools/kb.py stats
```

---

## RELATED PATTERNS

| Pattern ID | Title | Priority |
|------------|-------|----------|
| AGENT-DIRECT-SUBMODULE-ACCESS-001 | Direct Submodule Access Anti-Pattern | CRITICAL |
| AGENT-ROLE-SEPARATION-001 | Project Agent vs Curator Roles | CRITICAL |
| STALE-CONTEXT-001 | Verify Before Referencing | HIGH |
| SUBMODULE-STATUS-INTERPRETATION-001 | Understanding Status Output | MEDIUM |
| KB-UPDATE-001 | Shared KB Update Process | HIGH |
| AGENT-HANDOFF-001 | Contribution Workflow | HIGH |
| AGENT-HANDOFF-FAILURE-001 | Common Submission Failures | HIGH |
| CURATOR-ISSUE-TRIAGE-001 | Issue Triage Workflow | HIGH |

---

## TROUBLESHOOTING

### Problem: Agent uses direct git commands
**Solution:** Re-read user request, add "using git submodule commands"

### Problem: "Waiting for Issue #XXX" but issue already closed
**Solution:** Run `gh issue view NUMBER --json state` to verify

### Problem: Submodule always shows `-` prefix
**Solution:** Run `git submodule init` then `git submodule update`

### Problem: Can't tell if submodule update succeeded
**Solution:** Compare hashes before/after:
```bash
BEFORE=$(git submodule status | awk '{print $1}')
git submodule update --remote docs/knowledge-base/shared
AFTER=$(git submodule status | awk '{print $1}')
[ "$BEFORE" = "$AFTER" ] && echo "No change" || echo "Updated"
```

### Problem: Issue closed as "incomplete"
**Solution:** Resubmit with FULL YAML embedded in issue body (not file path)

---

## ATTRIBUTION

**Created By:** Shared KB Curator
**Pattern Source:** Analysis of agent workflows (2026-01-06)
**Related Issues:** #11-16

**For full details, see patterns in `universal/patterns/`**
