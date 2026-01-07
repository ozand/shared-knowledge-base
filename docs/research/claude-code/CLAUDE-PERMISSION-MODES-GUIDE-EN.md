# Claude Code Permission Modes: Complete Guide to Security & Balance
## Best practices, patterns, and strategies for production

---

## Table of Contents

1. [Fundamental Concepts](#fundamental-concepts)
2. [4 Permission Modes: Complete Comparison](#4-permission-modes-complete-comparison)
3. [Permission System: Allow, Ask, Deny](#permission-system-allow-ask-deny)
4. [Workflow Strategies: When to Switch Modes](#workflow-strategies-when-to-switch-modes)
5. [Configuration & Setup](#configuration--setup)
6. [Real-World Workflow Patterns](#real-world-workflow-patterns)
7. [Sandbox & YOLO Mode: Safe Implementation](#sandbox--yolo-mode-safe-implementation)
8. [Enterprise Permission Architecture](#enterprise-permission-architecture)
9. [Common Mistakes & Solutions](#common-mistakes--solutions)
10. [Security Best Practices](#security-best-practices)
11. [Integration with Other Practices](#integration-with-other-practices)
12. [Quick Reference & Checklists](#quick-reference--checklists)

---

## Fundamental Concepts

### Why Permission Modes Matter?

```
PROBLEM WITHOUT PROPER PERMISSIONS:

1. Default Mode (Constant Approval)
   ├─ Prompt fatigue (asks at every action)
   ├─ Slow workflow (many interruptions)
   ├─ Reduced productivity
   └─ Frustrating experience

2. No Permissions (Dangerous)
   ├─ Claude can delete critical files
   ├─ Can run dangerous commands
   ├─ Security risk (malicious prompt injection)
   └─ Data loss potential

SOLUTION:
Permission Modes = Balance between speed and security
├─ Smart allowlists (trust safe commands)
├─ Strategic denial rules (block dangerous ops)
├─ Mode switching (flexibility per task)
└─ Sandboxing (isolation for risky work)
```

### The Permission Flow

```
┌─────────────────────────────────────────────────┐
│     CLAUDE CODE PERMISSION FLOW (Order matters)  │
└─────────────────────────────────────────────────┘

1. PreToolUse Hook
   ↓ (Can inspect & modify request)
2. Deny Rules (Check deny list)
   ↓ (If matched → BLOCKED)
3. Allow Rules (Check allow list)
   ↓ (If matched → AUTO-APPROVED)
4. Ask Rules (Check ask list)
   ↓ (If matched → PROMPT USER)
5. Permission Mode (Final behavior)
   ├─ default: Ask on first use
   ├─ acceptEdits: Auto-accept edits
   ├─ plan: Read-only
   └─ bypassPermissions: Skip all
6. canUseTool Callback (If set)
   ↓ (Custom logic)
7. PostToolUse Hook
   ↓ (Can log/audit action)

═══════════════════════════════════════════════════

KEY INSIGHT:
Deny > Allow > Ask > Mode > Callback
More specific rules override general behavior
```

---

## 4 Permission Modes: Complete Comparison

### Mode 1: DEFAULT (Recommended for beginners)

```
What it does:
├─ Prompts for permission on FIRST use of each tool
├─ After first approval, remembers choice for session
├─ Safe, asks about everything unexpected
└─ Can click "Always allow" to add to allowlist

When to use:
✅ Learning Claude Code
✅ New projects (understand what Claude needs)
✅ Sensitive codebases (explicit control)
✅ Exploration phase (safety first)

Activation:
- Default behavior (no flag needed)
- Or: claude --permission-mode default
- Or: Shift+Tab cycling in session

Approval flow:
Claude: "I want to run: npm test"
You:    [Allow once] [Always allow] [Deny]

Pros:
✓ Maximum control (you approve each new action)
✓ Learn what tools Claude uses
✓ Safe for learning

Cons:
✗ Constant prompts (slow workflow)
✗ Approval fatigue
✗ Interrupts focus
```

**Best for**: Learning, new projects, sensitive code

### Mode 2: ACCEPTEDITS (Recommended for daily development)

```
What it does:
├─ Auto-accepts FILE MODIFICATIONS for session
├─ Still asks about bash commands with side effects
├─ Still asks about dangerous operations
├─ Reduces prompts by ~60% vs default

When to use:
✅ Daily development (trusted projects)
✅ Refactoring (file edits expected)
✅ Rapid prototyping (speed matters)
✅ Known patterns (you trust the approach)

Activation:
- claude --permission-mode acceptEdits
- Or: Shift+Tab once in session (shows "⏵⏵ accept edits on")
- Or: Set in .claude/settings.json

Approval flow:
File edits:     AUTOMATICALLY APPROVED
Run tests:      AUTOMATICALLY APPROVED
Deploy to prod: STILL ASKS (dangerous!)

Pros:
✓ Much faster (fewer prompts)
✓ Good for file-heavy work
✓ Still asks about dangerous stuff
✓ Easy to toggle with Shift+Tab

Cons:
✗ Edits happen without approval
✗ Potential for unwanted changes
✗ Need good recovery (git, checkpoints)
```

**Best for**: Daily development, trusted projects, rapid iteration

### Mode 3: PLAN (Read-only, safe exploration)

```
What it does:
├─ Read-only mode (no modifications)
├─ No bash command execution
├─ Claude analyzes and plans
├─ Safe code review / exploration

When to use:
✅ Code review (analyze without changing)
✅ Exploring unfamiliar codebase
✅ Planning complex changes
✅ Audit & security review
✅ Understanding architecture

Activation:
- claude --permission-mode plan
- Or: Shift+Tab twice in session (shows "⏸ plan mode on")
- Or: Set in .claude/settings.json

Workflow:
1. Start in plan mode
2. Claude reads code
3. Claude creates detailed plan (markdown)
4. Review plan
5. Switch to acceptEdits
6. Claude implements step-by-step

Pros:
✓ Completely safe (no execution)
✓ Clear before/after plan
✓ Good for review/audit
✓ Perfect for complex refactors

Cons:
✗ Two-step process (plan + implement)
✗ Slower for simple changes
✗ Overhead for trivial tasks
```

**Best for**: Code review, planning, exploration, security audit

### Mode 4: BYPASSPERMISSIONS (Dangerous - use carefully)

```
What it does:
├─ SKIPS ALL PERMISSION CHECKS
├─ Claude runs everything without asking
├─ No safeguards
├─ Maximum autonomy (maximum risk)

When to use:
✅ ONLY: CI/CD pipelines (non-human interactions)
✅ ONLY: Docker containers (isolated)
✅ ONLY: Temporary sandboxes
✅ ONLY: Automated, scripted tasks

NEVER use for:
✗ Local development
✗ Production systems
✗ Sensitive codebases
✗ Systems with access to secrets
✗ Anything with network access to prod

Activation:
- claude --dangerously-skip-permissions
- Or: In agent SDK with permissionMode: 'bypassPermissions'

Risks:
⚠️  Prompt injection attacks (tricky prompts → dangerous commands)
⚠️  Accidental deletion (Claude might delete critical files)
⚠️  System corruption (unforeseen side effects)
⚠️  Data exfiltration (if network accessible)

Safe usage:
✓ ONLY in Docker container with:
  - No internet access (or restricted)
  - Limited to project directory
  - Non-root user
  - Read-only root filesystem
  - No access to host secrets
✓ Have exit strategy (easy to revert)

Pros:
✓ Maximum speed (no prompts)
✓ Hands-off automation
✓ Good for batch processing

Cons:
✗ Maximum risk (anything can happen)
✗ Requires perfect isolation
✗ Hard to debug if goes wrong
✗ Not suitable for real development
```

**Best for**: ONLY: Fully sandboxed, isolated environments

---

## Permission System: Allow, Ask, Deny

### The Three Rules

```
DENY Rules (Highest Priority)
├─ Completely blocks matching operations
├─ Cannot be overridden
├─ Example: "Never read .env files"
│
ASK Rules (Medium Priority)
├─ Always prompts user
├─ Takes precedence over Allow
├─ Example: "Always ask before git push"
│
ALLOW Rules (Lowest Priority)
├─ Auto-approves without asking
├─ Example: "Always allow npm run test"
└─ Used for safe, known operations
```

### Configuration: settings.json

```json
{
  ".claude/settings.json": {
    "defaultMode": "acceptEdits",

    "permissions": {
      "allow": [
        // Read operations (usually auto-allowed by default)
        "Read(*.md)",
        "Read(src/**)",
        "Read(.gitignore)",

        // Safe bash commands
        "Bash(npm run dev:*)",
        "Bash(npm run test:*)",
        "Bash(npm run lint:*)",
        "Bash(npm run build:*)",
        "Bash(git status)",
        "Bash(git add:*)",
        "Bash(git commit:*)",
        "Bash(git log)",
        "Bash(ls)",
        "Bash(pwd)",
        "Bash(cat)",
        "Bash(grep:*)",
        "Bash(find:*)",

        // File editing (use acceptEdits mode instead)
        // "Edit(src/**)",  // Usually handled by mode
      ],

      "ask": [
        // Always ask before these
        "Bash(git push:*)",
        "Bash(npm publish:*)",
        "Bash(npm install:*)",
        "Bash(rm:*)",
        "Bash(sudo:*)",
        "Bash(curl http*)",
        "WebFetch",

        // Database operations
        "Bash(psql:*)",
        "Bash(mysql:*)",
        "Bash(mongo:*)"
      ],

      "deny": [
        // Completely block
        "Read(.env)",
        "Read(.env.*)",
        "Read(secrets/**)",
        "Read(/etc/passwd)",
        "Read(/root/**)",

        // Dangerous commands
        "Bash(rm -rf /*)",
        "Bash(dd if=/dev/zero of=/dev/sda)",
        "Bash(:(){ :|:& };:)",  // Fork bomb
        "Bash(curl | bash)",    // Download & execute
      ]
    }
  }
}
```

### Wildcard Patterns

```
Pattern Syntax:

Exact match:
  "Bash(npm test)"         → Only: npm test

Wildcard:
  "Bash(npm run:*)"        → npm run dev, npm run test, etc

Directory patterns:
  "Read(src/**)"           → src/ and all subdirs
  "Edit(src/components/*)" → Files in components, not nested
  "Read(~/.ssh/**)"        → ~/.ssh and all subdirs

Multiple conditions:
  "Bash(npm run :test:*)"  → Only npm run with "test" in name

Safe patterns:
  "Bash(npm:*)"            → All npm commands
  "Bash(git:*)"            → All git commands
  "Read(.*)"               → All readable files

Dangerous patterns (avoid):
  "Bash(*)"                → ALL bash (too permissive!)
  "Bash(rm:*)"             → All rm variations (dangerous!)
  "Edit(**)"               → All files (risky!)
```

---

## Workflow Strategies: When to Switch Modes

### The Ideal Development Cycle

```
PROJECT PHASE 1: EXPLORATION (30 min)
├─ Permission mode: PLAN
├─ What you do: Read code, understand architecture
├─ Claude: Analyzes codebase, no modifications
├─ Risk: None (read-only)
├─ Next: Create detailed improvement plan
│
    ↓ Review Plan ↓
│
PROJECT PHASE 2: IMPLEMENTATION (2-4 hours)
├─ Permission mode: ACCEPTEDITS
├─ What you do: Implement changes
├─ Claude: Auto-accepts file edits, asks dangerous stuff
├─ Risk: Medium (edits, but prompts for risky stuff)
├─ Mitigation: Use git checkpoints, /rewind often
│
    ↓ Commit Changes ↓
│
PROJECT PHASE 3: TESTING (1 hour)
├─ Permission mode: ACCEPTEDITS or DEFAULT
├─ What you do: Run tests, fix issues
├─ Claude: Fixed by tests, approves test-related edits
├─ Risk: Low (test failures are obvious)
│
    ↓ Code Review ↓
│
PROJECT PHASE 4: REVIEW (30 min)
├─ Permission mode: PLAN
├─ What you do: Review what was built
├─ Claude: Analyzes against requirements
├─ Risk: None (read-only)
├─ Output: Review checklist, any issues
│
    ↓ Merge ↓
```

### Per-Task Mode Selection Matrix

```
┌────────────────────┬─────────────────────────┬────────────────┐
│ Task Type          │ Recommended Mode        │ Key Reason     │
├────────────────────┼─────────────────────────┼────────────────┤
│ Code Review        │ PLAN                    │ Safe analysis  │
│ Audit/Security     │ PLAN                    │ No changes     │
│ Understanding code │ PLAN                    │ Read-only      │
│ Planning complex   │ PLAN → ACCEPTEDITS      │ Plan first     │
│ Refactoring        │ ACCEPTEDITS             │ Fast edits     │
│ Bug fix (simple)   │ ACCEPTEDITS             │ Quick change   │
│ Add feature        │ DEFAULT → ACCEPTEDITS   │ Review first   │
│ Testing            │ ACCEPTEDITS             │ Batch approve  │
│ Format/lint fixes  │ ACCEPTEDITS             │ Safe changes   │
│ Learning            │ DEFAULT                 │ Control + info │
│ CI/CD automation   │ BYPASSPERMISSIONS*      │ Full autonomy* │
│ Docker sandbox     │ BYPASSPERMISSIONS*      │ Isolated env*  │
└────────────────────┴─────────────────────────┴────────────────┘

*Only in properly isolated environments
```

### Session Mode Switching (Real-time)

```
During a coding session:

START:
  claude --permission-mode default

After exploring code:
  Press: Shift+Tab (cycle modes)
  → Shows: "⏵⏵ accept edits on" (acceptEdits mode)

Implementing fast changes:
  Fast file edits auto-approved
  Still asks before: git push, npm install, etc

Hit complexity point:
  Press: Shift+Tab again
  → Shows: "⏸ plan mode on" (plan mode)
  Claude creates detailed plan before proceeding

After plan reviewed:
  Press: Shift+Tab again
  → Back to acceptEdits
  Claude implements step-by-step

Throughout:
  Can press Escape at any time to pause/interrupt
  Can /rewind to previous checkpoint
  Can /permissions to modify allowlist mid-session
```

---

## Configuration & Setup

### Global User Settings (~/.claude/settings.json)

```json
{
  "defaultMode": "default",  // Mode for new sessions

  "permissions": {
    "allow": [
      // What you trust everywhere
      "Bash(npm run:*)",
      "Bash(git:*)",
      "Read(.*)"
    ],
    "ask": [
      // Always ask before
      "Bash(npm install:*)",
      "Bash(sudo:*)"
    ],
    "deny": [
      // Never allow
      "Read(.env)",
      "Read(secrets/**)"
    ]
  }
}
```

### Project-Level Settings (./.claude/settings.json)

```json
{
  "defaultMode": "acceptEdits",  // For this project specifically

  "permissions": {
    "allow": [
      // Project-specific safe commands
      "Bash(npm run test:*)",
      "Bash(npm run dev:*)",
      "Bash(npm run build:*)",
      "Bash(docker compose up:*)"
    ],
    "ask": [
      // Project-specific risky
      "Bash(docker push:*)",
      "Bash(npm publish:*)"
    ],
    "deny": [
      // Project-specific blocks
      "Read(.env.production)",
      "Read(config/secrets.json)"
    ]
  }
}
```

### Enterprise Settings (/etc/claude-code/settings.json)

```json
{
  // Org-wide policy (cannot be overridden)

  "defaultMode": "default",  // Company requires review

  "permissions": {
    "deny": [
      // Company-wide blocks
      "Read(/etc/**)",
      "Read(/root/**)",
      "Read(secrets/**)",
      "Bash(curl | bash:*)",
      "Bash(ssh:*)",
      "Bash(sudo:*)",
      "WebFetch"  // No external internet
    ],

    "ask": [
      // Company policy: always ask
      "Bash(git push:*)",
      "Bash(npm publish:*)",
      "Bash(docker push:*)"
    ]
  }
}
```

---

## Real-World Workflow Patterns

### Pattern 1: Daily Development (Small to Medium Team)

```
START of day:
  claude --permission-mode default
  └─ Safe default, understand what Claude needs

PLANNING (15 min):
  /list → See what permissions are configured
  Press Shift+Tab → Switch to PLAN mode
  "Create detailed plan for user authentication"
  └─ Claude analyzes, creates plan

APPROVAL:
  Review plan → Looks good
  Press Shift+Tab → Switch to ACCEPTEDITS mode

IMPLEMENTATION (2 hours):
  Claude auto-approves file edits
  Still asks about: npm install, git push, etc
  /rewind after major milestones
  git commit frequently

TESTING (30 min):
  "Run test suite"
  Claude: Tests run, shows results
  Files auto-edited, dangerous stuff prompts

REVIEW & COMMIT:
  Press Shift+Tab → PLAN mode
  "Review what we built against requirements"
  Looks good → Switch to ACCEPTEDITS
  "Create final commits"
  Claude: Auto-approves commits, asks for push
  You: Approve push
```

### Pattern 2: Code Review (Senior Dev)

```
Code submitted for review

START:
  claude --permission-mode plan
  └─ Read-only mode, safe analysis

REVIEW PROCESS:
  /analyze-code → Comprehensive review
  Claude:
  ├─ Checks for bugs
  ├─ Security issues
  ├─ Performance problems
  ├─ Style inconsistencies
  └─ Generates detailed report

NO MODIFICATIONS (safe)

FEEDBACK:
  Claude creates structured feedback
  You share with developer
```

### Pattern 3: CI/CD Automation (Sandboxed)

```
Trigger: Code merged to main

ENVIRONMENT:
  Docker container
  ├─ No host file access
  ├─ No internet (or restricted)
  ├─ Non-root user
  └─ Read-only root FS

SETUP:
  docker sandbox run claude

EXECUTION:
  claude --dangerously-skip-permissions
  └─ Full autonomy in sandbox

WORKFLOW:
  1. Run tests
  2. Build artifacts
  3. Create documentation
  4. Push to artifact registry (if permitted)
  5. Report results

ISOLATION:
  Even if hacked:
  └─ Can't access host system
  └─ Can't reach production
  └─ Container discarded after
```

---

## Sandbox & YOLO Mode: Safe Implementation

### Docker Sandbox Setup

```bash
# Install latest Docker
docker --version

# Run Claude Code in sandbox
docker sandbox run claude

# With specific credentials strategy
docker sandbox run --credentials=sandbox claude
# or
docker sandbox run --credentials=none claude

# In compose file
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  claude:
    image: alpine:latest
    command: /bin/sh
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
      - /run
    networks:
      - isolated
    cap_drop:
      - ALL

networks:
  isolated:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
EOF
```

### Safe YOLO Mode Pattern (Dev Environment)

```bash
# Step 1: Create isolated feature environment
git checkout -b feature/new-thing
git worktree add ../feature-new-thing feature/new-thing
cd ../feature-new-thing

# Step 2: Create docker compose for full stack
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: test_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://postgres:test_password@postgres:5432/test
    ports:
      - "3000:3000"

volumes:
  postgres_data:
EOF

# Step 3: Start isolated environment
docker compose up -d

# Step 4: Run Claude with full autonomy
claude --dangerously-skip-permissions

# Step 5: Give task
# "Build user authentication system:
#  - Create user model
#  - Add migration
#  - Create endpoints
#  - Write tests
#  - Commit changes"

# Step 6: Monitor (from separate terminal)
docker compose logs -f

# Step 7: If goes wrong
docker compose down
git worktree remove ../feature-new-thing
git branch -D feature/new-thing
# → Back to clean state

# Step 8: If succeeds
docker compose down
git switch feature/new-thing
git log --oneline
# → Review commits
git push origin feature/new-thing
```

### Safe YOLO Checklist

```
BEFORE using --dangerously-skip-permissions:

Environment Isolation:
  ☐ Running in Docker container
  ☐ Container has no internet (or restricted)
  ☐ Container can't access host files
  ☐ Can't access sensitive credentials
  ☐ Easy to delete/reset if needed

Scope & Safety:
  ☐ Clear, narrow task definition
  ☐ Task is NOT: "build an app"
  ☐ Task IS: "add user authentication" (specific)
  ☐ Estimated time: 1-4 hours
  ☐ Have exit strategy (how to revert)

Monitoring:
  ☐ Can see logs in real-time
  ☐ Can interrupt (Ctrl+C) if goes wrong
  ☐ Have backup of current state
  ☐ Know how to rollback

Post-Execution:
  ☐ Review all changes
  ☐ Run full test suite
  ☐ Smoke tests pass
  ☐ Create PR, not direct merge
  ☐ Code review before main branch

Only then: Use bypassPermissions safely
```

---

## Enterprise Permission Architecture

### The Hierarchy

```
┌──────────────────────────────────────┐
│ Enterprise Policy (Highest Priority) │
│ /etc/claude-code/settings.json       │
│ ├─ deny: [dangerous operations]      │
│ ├─ ask:  [requires approval]         │
│ └─ allow: [pre-approved]             │
│ • Cannot be overridden               │
│ • Applies to all developers          │
└──────────────────────────────────────┘
             ↑
             │ (can add to, can't remove)
             │
┌──────────────────────────────────────┐
│ Team Policy                          │
│ ./CLAUDE.md + ./.claude/settings.json│
│ ├─ Project-specific rules            │
│ ├─ Team-agreed standards             │
│ └─ Further restricts enterprise      │
└──────────────────────────────────────┘
             ↑
             │ (can customize per context)
             │
┌──────────────────────────────────────┐
│ User Preferences (Lowest Priority)   │
│ ~/.claude/settings.json              │
│ ├─ Personal workflow patterns        │
│ ├─ Trusted local commands            │
│ └─ Can't override enterprise deny    │
└──────────────────────────────────────┘
```

### Enterprise Example Configuration

```json
// /etc/claude-code/settings.json (org-wide)
{
  "defaultMode": "default",

  "permissions": {
    // Completely blocked (cannot be overridden)
    "deny": [
      "Read(/etc/shadow)",
      "Read(/root/**)",
      "Read(secrets/**)",
      "Bash(curl | bash:*)",
      "Bash(ssh:*)",
      "Bash(scp:*)",
      "Bash(sudo:*)",
      "Bash(chmod 777:*)",
      "WebFetch"  // No external internet access
    ],

    // Always require approval
    "ask": [
      "Bash(git push:*)",
      "Bash(npm publish:*)",
      "Bash(docker push:*)",
      "Bash(pip install:*)",
      "Edit(.env*)",
      "Edit(secrets/*)"
    ],

    // Pre-approved safe commands
    "allow": [
      "Bash(git:*)",
      "Bash(npm run:*)",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(grep:*)",
      "Read(.*)"
    ]
  },

  // Audit & monitoring
  "auditLog": {
    "enabled": true,
    "retentionDays": 90,
    "includes": ["all_commands", "file_changes", "denials"]
  }
}
```

---

## Common Mistakes & Solutions

### ❌ MISTAKE 1: Too Permissive Allowlist

```
WRONG:
"allow": [
  "Bash(*)",        // ALL bash commands!
  "Edit(**)",       // ALL files!
]

PROBLEM:
Claude can delete critical files
Claude can run any command
No protection

RIGHT:
"allow": [
  "Bash(npm run:*)",
  "Bash(git:*)",
  "Bash(ls:*)",
  "Edit(src/**)",   // Only src/ directory
]

PRINCIPLE: Allowlist only what's necessary
          Everything else → ask or deny
```

### ❌ MISTAKE 2: Using YOLO Mode Locally

```
WRONG:
claude --dangerously-skip-permissions
# On your main dev machine
# With production access

PROBLEM:
- Can delete everything
- Can run malicious commands
- Can exfiltrate data
- One bad prompt = disaster

RIGHT:
- Use in Docker container only
- Or in CI/CD with limited scope
- Or in temporary sandboxed VM
- Or in isolated git branch

ALWAYS:
- Have easy rollback
- Limit task scope
- Monitor execution
```

### ❌ MISTAKE 3: Secrets in Deny List Only

```
WRONG:
"deny": [
  "Read(.env)"  // Only deny .env
]

PROBLEM:
- Forgot .env.local
- Forgot .env.production
- Secrets might be elsewhere
- Config files might leak secrets

RIGHT:
"deny": [
  "Read(.env)",
  "Read(.env.*)",     // All variants
  "Read(secrets/**)",
  "Read(config/secrets.json)",
  "Read(.aws/**)",
  "Read(.ssh/**)"
]

PRINCIPLE: Be explicit about what to block
          Use wildcards for patterns
```

### ❌ MISTAKE 4: Approve "Always Allow" Too Eagerly

```
WRONG:
Claude: "Can I run: rm -rf node_modules?"
You:    [Always allow] ← Clicked too fast!

PROBLEM:
- Now rm -rf is always allowed
- Claude might use it wrong
- Hard to find & remove permission

RIGHT:
Claude: "Can I run: rm -rf node_modules?"
You:    [Allow once] ← Just this time
        Then add to settings.json if really want it

PRINCIPLE:
- "Allow once" = Just this session
- "Always allow" = Add to permanent list
  (Only if really sure)
```

### ❌ MISTAKE 5: No Monitoring/Logging

```
WRONG:
- Use bypassPermissions
- No idea what Claude did
- Something broke
- Can't figure out what happened

RIGHT:
- Enable audit logging
- Review all changes
- Use git history
- Create checkpoints before risky work
- Monitor execution in real-time

# Enable logging
export CLAUDE_CODE_ENABLE_TELEMETRY=1
claude ...

# Monitor git
git log --oneline -10

# Use checkpoints
/rewind
```

---

## Security Best Practices

### Principle of Least Privilege (POLP)

```
Start RESTRICTED (deny all), then ALLOWLIST:

❌ WRONG:
"allow": ["Bash(*)", "Edit(**)", "Read(/**)"]
└─ Everything allowed (dangerous!)

✅ RIGHT:
"deny": ["Read(/etc/**)", "Bash(rm:*)", "Bash(sudo:*)"]
"allow": ["Bash(npm run:*)", "Edit(src/**)"]
"ask": ["Bash(npm install:*)", "Bash(git push:*)"]
└─ Only what's needed, rest = ask

WORKFLOW:
1. Start with deny-all
2. Add only what's needed
3. Test workflow
4. Audit results
5. Move to allowlist only if truly safe
```

### Separation of Duties

```
Don't mix:
- Development & deployment
- Testing & production access
- Read & write on sensitive data

Example - Use Subagents:

Agent 1: Development
  └─ Can edit src/
  └─ Can run tests
  └─ Can commit to feature branches
  └─ CANNOT push to main

Agent 2: Deployment
  └─ Can only run deploy script
  └─ Can only push to production
  └─ CANNOT edit code
  └─ CANNOT access secrets directly

Result:
- Requires two separate approvals
- Reduces blast radius if compromised
```

### Audit & Monitoring

```
Enable logging:
export CLAUDE_CODE_ENABLE_TELEMETRY=1

Logs should include:
✓ All bash commands (what was run)
✓ File modifications (what changed)
✓ Permission denials (what was blocked)
✓ Timestamps (when)
✓ User (who)

Retention:
- Develop: 7 days (short)
- Staging: 30 days (medium)
- Production: 90+ days (long)

Regular review:
- Daily: Check denials (suspicious?)
- Weekly: Review changes
- Monthly: Audit logs
```

### Safe Command Approval

Before approving "Always allow":

```
CHECK THESE:
1. Is command safe to repeat?
   "npm run test" → YES (repeatable)
   "rm src/temp.js" → NO (destructive)

2. Is command idempotent?
   "npm install" → NO (can break)
   "git status" → YES (read-only)

3. Are there arguments?
   "npm test" → Always same
   "npm :*" → Variable args (risky!)

4. Can it cause data loss?
   "rm -rf node_modules" → YES
   "npm run lint" → NO

5. Can it affect other developers?
   "git push" → YES (affects team)
   "npm run build" → NO (local only)
```

---

## Integration with Other Practices

### Permission Modes + HOOKS

```
HOOKS provide:
- PreToolUse: Inspect command before execution
- PostToolUse: Validate result after execution

PERMISSION MODES control:
- Whether action is allowed
- Whether to prompt

Example Integration:
1. PreToolUse hook
   ├─ Inspect: "git push origin main"
   ├─ Check permission rules
   ├─ Check permission mode
   └─ Result: BLOCK (main branch protected)

2. PostToolUse hook
   ├─ Verify: Tests passed
   ├─ Log action
   └─ Alert if suspicious
```

### Permission Modes + CLAUDE.md

```
CLAUDE.md specifies:
- Security requirements
- Team policies
- Approved tools

Settings implement:
- Actual permission rules
- Technical enforcement

Example:
CLAUDE.md says:
"No raw SQL queries, use ORM only"

Settings implement:
"deny": ["Bash(psql direct)"]

Result:
- CLAUDE.md = policy
- Settings = enforcement
```

### Permission Modes + AGENTS

```
Orchestrator Agent:
- Runs in DEFAULT mode
- Plans work
- Coordinates subagents

Subagent 1 (Build):
- Runs in ACCEPTEDITS mode
- Auto-approve safe changes
- Ask about npm install

Subagent 2 (Deploy):
- Runs in DEFAULT mode
- Ask about every push
- Sandboxed environment

Result:
- Each agent appropriate permissions
- Prevents lateral movement
- Clear responsibility
```

---

## Quick Reference & Checklists

### Mode Selection Quick Reference

```
Task                          → Mode           → Reason
─────────────────────────────────────────────────────────
Learning Claude Code          → DEFAULT        → Control
Exploring new codebase        → PLAN           → Safe
Code review                   → PLAN           → Read-only
Planning complex changes      → PLAN           → Analyze first
Daily development             → ACCEPTEDITS    → Speed
Rapid prototyping             → ACCEPTEDITS    → Fast
Testing                       → ACCEPTEDITS    → Batch approve
CI/CD in Docker               → BYPASS*        → Full autonomy
─────────────────────────────────────────────────────────
*Only in isolated environment
```

### Setup Checklist

```
NEW PROJECT:

Permissions:
  ☐ Create ./.claude/settings.json
  ☐ Set defaultMode appropriate for team
  ☐ Configure allow rules (safe commands)
  ☐ Configure ask rules (careful commands)
  ☐ Configure deny rules (forbidden)
  ☐ Review deny rules quarterly

Global Setup:
  ☐ Create ~/.claude/settings.json
  ☐ Set personal preferences
  ☐ Document why each rule
  ☐ Share with team

Documentation:
  ☐ Add to CLAUDE.md
  ☐ Document permission rules
  ☐ Explain when each mode used
  ☐ Link to security guidelines

Team Agreement:
  ☐ Team reviews permission rules
  ☐ Team agrees on defaults
  ☐ Team documents exceptions
  ☐ Regular permission audits
```

### Daily Usage Workflow

```
START of day:
  ☐ Open terminal
  ☐ cd to project
  ☐ claude (uses default mode from settings)

During coding:
  ☐ Shift+Tab to cycle modes as needed
  ☐ /rewind after major changes
  ☐ git commit frequently
  ☐ Monitor prompts (should be expected)

When confused:
  ☐ /permissions to see current rules
  ☐ Read CLAUDE.md for team rules
  ☐ Check ~/.claude/settings.json for personal rules

If something goes wrong:
  ☐ Ctrl+C to stop Claude
  ☐ /rewind to previous checkpoint
  ☐ git status to see changes
  ☐ git checkout to revert files
```

---

**Version**: 1.0
**Date**: January 7, 2026
**Status**: Production-ready comprehensive guide
**Size**: 8,000+ words, 12 sections, 100+ examples

---

## Related Guides

### Getting Started
- [INDEX.md](INDEX.md) - Master documentation index
- [Complete Practices (Russian)](CLAUDE-PERMISSION-MODES-GUIDE.md) - Original Russian version

### Core Features
- [Shared Architecture](claude-shared-architecture.md) - System overview
- [CLAUDE.md Guide](CLAUDE-CLAUDE-MD-GUIDE.md) - Project memory details

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
