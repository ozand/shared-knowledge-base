# Claude Code Slash Commands: Complete Guide to Custom Automation
## Best practices, patterns, and production-ready examples

---

## Table of Contents

1. [Fundamental Concepts](#fundamental-concepts)
2. [Project vs User Scopes](#project-vs-user-scopes)
3. [Command Structure & Syntax](#command-structure--syntax)
4. [Dynamic Arguments & Interpolation](#dynamic-arguments--interpolation)
5. [Organization & Namespacing](#organization--namespacing)
6. [Real-World Command Patterns](#real-world-command-patterns)
7. [Team-Shared Commands](#team-shared-commands)
8. [Advanced Patterns & Workflows](#advanced-patterns--workflows)
9. [Integration with Other Practices](#integration-with-other-practices)
10. [Common Mistakes & Solutions](#common-mistakes--solutions)
11. [Team Deployment Strategy](#team-deployment-strategy)
12. [Quick Reference & Checklists](#quick-reference--checklists)

---

## Fundamental Concepts

### What are Slash Commands?

```
Slash Commands = Reusable prompt templates saved as Markdown files

Simple concept:
  1. Write detailed prompt in Markdown
  2. Save as .md file in .claude/commands/
  3. Invoke with /command-name
  4. Claude executes the prompt

KEY INSIGHT:
Slash Commands = Eliminate prompt repetition
                = Standardize workflows
                = Build automation engine
```

### Slash Commands vs SKILLS vs HOOKS

```
┌─────────────────┬──────────────────┬─────────────────────┐
│ Feature         │ Slash Commands   │ SKILLS              │
├─────────────────┼──────────────────┼─────────────────────┤
│ Invocation      │ Manual (/cmd)    │ Automatic discovery │
│ File location   │ .claude/cmd/     │ .claude/skills/     │
│ Use case        │ Repeatable tasks │ Rich workflows      │
│ Complexity      │ Simple-medium    │ Medium-complex      │
│ Files           │ 1 markdown       │ Multiple files      │
│ Sharing         │ Via git          │ Via plugins         │
│ Team use        │ Easy (project)   │ Structured (plugin) │
└─────────────────┴──────────────────┴─────────────────────┘

WHEN TO USE SLASH COMMANDS:
✅ Quick, frequently used prompts
✅ Simple prompt snippets (one file)
✅ Team-shared workflows (checked into git)
✅ Explicit control over invocation

WHEN TO USE SKILLS:
✅ Complex workflows (multiple files)
✅ Validation scripts & dependencies
✅ Claude should discover automatically
✅ Highly organized reference material
```

### Why Slash Commands Matter

```
PROBLEM:
  You repeat same detailed prompts constantly
  "Perform code review following our standards..."
  "Generate tests using Jest..."
  = Wasted time, inconsistent results

SOLUTION:
  Save prompt as slash command
  /review → Claude does review
  /test → Claude generates tests
  = 30 seconds instead of 2 minutes
  = Consistent results every time

IMPACT:
  1 command × 10 uses per day × 20 work days = 200 minutes saved/month
  10 commands × efficiency = 4+ hours saved per month
```

---

## Project vs User Scopes

### Scope 1: Project-Scoped Commands

```
Location:
  .claude/commands/ (in project root)

Access:
  /project:command-name (explicit prefix)
  or just /command-name (if no conflicts)

Example:
  .claude/commands/
  ├── review.md          → /review
  ├── test-coverage.md   → /test-coverage
  └── features/
      └── new.md         → /features:new

Sharing:
  ✓ Checked into git
  ✓ All team members get same commands
  ✓ Version controlled
  ✓ Easy to discover

Perfect for:
  ✓ Team workflows
  ✓ Project-specific processes
  ✓ Shared standards
  ✓ Onboarding new developers
```

### Scope 2: User-Scoped Commands

```
Location:
  ~/.claude/commands/ (in home directory)

Access:
  /user:command-name or just /command-name
  (works across ALL projects)

Example:
  ~/.claude/commands/
  ├── my-review-style.md
  ├── my-testing-approach.md
  └── personal-shortcuts/
      ├── explain.md
      └── refactor.md

Sharing:
  ✗ Personal only (not in git)
  ✗ Each developer has own
  ✓ Great for personal preferences
  ✓ Portable across projects

Perfect for:
  ✓ Personal workflow preferences
  ✓ Individual productivity hacks
  ✓ Personal coding style
  ✓ Shortcuts you use everywhere
```

### Scope Precedence

```
When you type: /my-command

Claude searches in order:

1. Local (current directory)
   .claude/commands/my-command.md
   ↓ If found, use it
   ↓ If not, continue

2. Project root
   ./CLAUDE/commands/my-command.md
   ↓ If found, use it
   ↓ If not, continue

3. User home
   ~/.claude/commands/my-command.md
   ↓ If found, use it
   ↓ If not, continue

4. Built-in
   Built-in /help, /list, etc
   ↓ Use fallback

RULE:
More specific scope wins
Local > Project > User > Built-in
```

---

## Command Structure & Syntax

### Basic Command File

```markdown
# File: .claude/commands/review.md

# Code Review

Perform comprehensive code review of the current file:

1. **Security Analysis**
   - Check for vulnerabilities
   - Verify input validation
   - Check for hardcoded secrets

2. **Performance Analysis**
   - Identify inefficient algorithms
   - Check for N+1 queries
   - Suggest optimization opportunities

3. **Code Quality**
   - Check for duplicate code
   - Verify naming conventions
   - Check for proper error handling

4. **Documentation**
   - Verify functions have JSDoc
   - Check for inline comments where needed
   - Ensure README is updated if needed

Provide structured feedback with specific examples.
```

### Advanced Command with Frontmatter

```markdown
# File: .claude/commands/optimize.md

---
description: Analyze code for performance issues
category: optimization
tags: performance, refactoring
requires-context: codebase
---

# Performance Optimization

Analyze the provided code or codebase for performance issues:

## Analysis Checklist
- [ ] Time complexity (O(n) analysis)
- [ ] Space complexity
- [ ] Database query efficiency
- [ ] API call optimization
- [ ] Memory leaks
- [ ] Unnecessary re-renders (React)
- [ ] Large bundle sizes

## Output Format

For each issue found:
1. **Issue**: Description
2. **Current**: Current implementation
3. **Problem**: Why it's inefficient
4. **Solution**: Specific optimization
5. **Benefit**: Expected improvement (e.g., 40% faster)
6. **Effort**: Effort to implement (1-3 story points)

Focus on high-impact optimizations first.
```

### Minimal Command

```markdown
# .claude/commands/test-quick.md

Run the test suite and show me only failing tests.
```

**That's it!** Simple enough to read in seconds, powerful enough to be useful.

---

## Dynamic Arguments & Interpolation

### Using $ARGUMENTS (Catch-All)

```markdown
# .claude/commands/fix-issue.md

---
argument-hint: [issue-number]
description: Fix a specific GitHub issue
---

# Fix GitHub Issue

Fix issue #$ARGUMENTS with the following approach:

1. Read the issue description carefully
2. Understand the root cause
3. Implement the minimum necessary fix
4. Add tests for the fix
5. Verify no regressions

Make clear, focused commits.
```

**Usage:**
```bash
/fix-issue 42
# Claude fixes issue #42

/fix-issue 100
# Claude fixes issue #100
```

### Using Numbered Arguments ($1, $2, etc)

```markdown
# .claude/commands/new-component.md

---
argument-hint: [component-name] [description]
description: Create a new React component
---

# Create Component: $1

Create a new React component named **$1**

## Description
$2

## Structure
Create in: `src/components/$1.tsx`

## Requirements
- Functional component with hooks
- TypeScript with strict typing
- Props interface documented
- JSDoc for component
- Default export

## Styles
Create: `src/components/$1.module.css`
- BEM naming convention
- Mobile-first responsive design

## Tests
Create: `tests/$1.test.tsx`
- Happy path tests
- Edge cases
- Error states
- Accessibility tests
- 80%+ coverage

## Export
Add to `src/components/index.ts`:
```typescript
export { $1 } from './$1';
```
```

**Usage:**
```bash
/new-component Button "A reusable button component"
# Creates Button component with description

/new-component Modal "Dialog that appears on top"
# Creates Modal component
```

### Using Square Bracket Extraction

```markdown
# .claude/commands/create-feature.md

---
argument-hint: [feature-name] [description] [story-points]
description: Create new feature structure
---

# Create Feature: $ARGUMENTS

Parse arguments:
- [featureName] = First word before space
- [description] = Text in quotes
- [storyPoints] = Number at end

Create:
1. Feature directory: `src/features/[featureName]`
2. Component file
3. Tests
4. Documentation with [storyPoints] estimate

Include [description] in component JSDoc.
```

---

## Organization & Namespacing

### Directory Structure for Large Projects

```
.claude/commands/
│
├── backend/
│   ├── db-migration.md
│   ├── api-endpoint.md
│   └── service.md
│
├── frontend/
│   ├── new-component.md
│   ├── style-update.md
│   └── state-management.md
│
├── testing/
│   ├── unit-tests.md
│   ├── e2e-tests.md
│   └── coverage-check.md
│
├── deployment/
│   ├── deploy-staging.md
│   ├── deploy-production.md
│   └── rollback.md
│
├── quality/
│   ├── code-review.md
│   ├── security-audit.md
│   └── performance-review.md
│
├── documentation/
│   ├── api-docs.md
│   └── architecture-docs.md
│
├── utilities/
│   ├── cleanup-logs.md
│   └── bulk-rename.md
│
└── quick-reference.md
```

### Naming Conventions

```
Command Names (File names):

✅ GOOD:
  new-component.md           (kebab-case)
  generate-tests.md          (verb-first)
  deploy-staging.md          (specific action)
  review-security.md         (clear purpose)

❌ BAD:
  NewComponent.md            (PascalCase - confusing)
  test.md                    (too generic)
  stuff.md                   (meaningless)
  GenerateTestsForFile.md    (too long)

PATTERN:
[verb]-[object]-[context]
- generate-tests-frontend
- deploy-to-production
- review-security-audit
```

### Invocation Patterns

```
Direct call (no conflicts):
  /review
  /new-component Button
  /deploy-staging

Scoped call (explicit):
  /project:review
  /project:quality:code-review
  /user:my-shortcuts:explain

With arguments:
  /fix-issue 42
  /new-component Button "A reusable button"
  /deploy-staging production
```

---

## Real-World Command Patterns

### Pattern 1: Code Review Command

```markdown
# .claude/commands/review.md

---
description: Comprehensive code review
category: quality
---

# Code Review

Perform a thorough code review of the changes:

## Security Checklist
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection protected (ORM used)
- [ ] XSS protection for output
- [ ] CSRF tokens for state changes
- [ ] Authentication required

## Performance Checklist
- [ ] No N+1 queries
- [ ] Algorithms use appropriate complexity
- [ ] No unnecessary re-renders (React)
- [ ] Bundle size reasonable
- [ ] Caching strategy applied

## Code Quality
- [ ] No duplicate code
- [ ] Functions have single responsibility
- [ ] Naming is clear
- [ ] No magic numbers
- [ ] Error handling complete

## Tests
- [ ] Unit tests for logic
- [ ] Integration tests for APIs
- [ ] Coverage >= 80%
- [ ] Edge cases tested

## Output Format

For each issue:
```
## Issue: [Title]
**Severity**: [Critical/High/Medium/Low]
**Type**: [Security/Performance/Quality/Testing]
**Location**: [File:Line]
**Problem**: [Detailed explanation]
**Solution**: [Specific fix]
**Example**:
```
[code example]
```
```

### Pattern 2: Test Generation Command

```markdown
# .claude/commands/generate-tests.md

---
argument-hint: [file-to-test]
description: Generate comprehensive tests
---

# Generate Tests for $ARGUMENTS

Generate comprehensive tests for: **$ARGUMENTS**

## Test Strategy
- Unit tests for each function
- Integration tests for API endpoints
- Edge cases and error conditions
- Mocking external dependencies

## Framework
- Jest for unit tests
- Supertest for API tests
- React Testing Library for components

## Coverage Target
Achieve 80%+ code coverage

## Test Structure
```typescript
describe('[Component/Function Name]', () => {
  describe('Happy Path', () => {
    // Tests for normal usage
  });

  describe('Edge Cases', () => {
    // Tests for boundary conditions
  });

  describe('Error Handling', () => {
    // Tests for error states
  });
});
```

## Output
Save tests alongside source file with .test.ts extension.
```

### Pattern 3: Git Workflow Command

```markdown
# .claude/commands/commit.md

---
description: Create conventional commit
---

# Create Commit

Create a conventional commit message for staged changes:

1. Run: `git status` and `git diff --cached`
2. Analyze changes
3. Determine commit type:
   - `feat:` New feature
   - `fix:` Bug fix
   - `refactor:` Code restructuring
   - `docs:` Documentation
   - `test:` Tests only
   - `chore:` Build, deps, tooling

4. Format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

5. Create commit with `git commit -m "..."`

Example:
```
feat(auth): add JWT token refresh

- Implement refresh token endpoint
- Add automatic token rotation
- Store refresh token in HttpOnly cookie

Closes #42
```
```

### Pattern 4: Deployment Command

```markdown
# .claude/commands/deploy-staging.md

---
description: Deploy to staging environment
requires-context: project-setup
---

# Deploy to Staging

Deploy current code to staging environment:

## Pre-Deployment Checks
- [ ] All tests passing
- [ ] No linting errors
- [ ] Code reviewed
- [ ] Database migrations ready

## Deployment Steps

1. Create deployment tag
   ```bash
   git tag staging-$(date +%Y%m%d-%H%M%S)
   git push origin --tags
   ```

2. Verify build pipeline
   ```bash
   # Check GitHub Actions status
   ```

3. Verify deployment
   ```bash
   curl https://staging.example.com/health
   ```

4. Run smoke tests
   ```bash
   npm run test:e2e:staging
   ```

5. Alert team
   - Post in #deployments Slack channel
   - Include: version, changes, status

## Rollback (if needed)
```bash
git revert <commit-hash>
git push origin main
```
```

---

## Team-Shared Commands

### Repository Structure

```
myproject/
├── .github/
│   └── workflows/
│       └── ci-cd.yml

├── docs/
│   ├── CONTRIBUTING.md
│   └── CLAUDE_COMMANDS.md    ← Document commands

├── .claude/
│   ├── CLAUDE.md             ← Project memory
│   ├── settings.json         ← Permissions
│   │
│   └── commands/
│       ├── README.md         ← How to use commands
│       │
│       ├── review.md
│       ├── commit.md
│       ├── test.md
│       │
│       ├── backend/
│       │   └── new-endpoint.md
│       │
│       └── frontend/
│           └── new-component.md

├── src/
├── tests/
├── package.json
└── README.md
```

### Command Documentation (README)

```markdown
# Claude Code Slash Commands

This project includes custom slash commands to standardize workflows.

## Available Commands

### Code Quality
- `/review` - Comprehensive code review
- `/test` - Generate tests for a file
- `/lint-fix` - Fix linting issues

### Git Workflow
- `/commit` - Create conventional commit
- `/branch-from-issue` - Create feature branch

### Development
- `/backend:new-endpoint` - Create API endpoint
- `/frontend:new-component [name] [desc]` - Create React component

### Deployment
- `/deploy-staging` - Deploy to staging
- `/deploy-prod` - Deploy to production (requires approval)

## Using Commands

### Review Code
```bash
# Current file
/review

# Specific file
# (Use in the file context)
```

### Create Component
```bash
/frontend:new-component Button "A reusable button"
```

### Deploy
```bash
/deploy-staging
```

## Creating New Commands

1. Create `.md` file in appropriate subdirectory
2. Document command purpose
3. Add to this README
4. Test with team
5. Commit to main

See `.claude/commands/` for examples.
```

### Onboarding Guide

```markdown
# New Developer: Claude Code Setup

## Step 1: Clone Repository
```bash
git clone https://github.com/yourorg/yourproject.git
cd yourproject
```

## Step 2: Install Claude Code
```bash
# Follow official instructions
```

## Step 3: Explore Project Memory
```bash
cat .claude/CLAUDE.md  # Project context
```

## Step 4: Set Up Permissions
```bash
# Copy project settings to your local setup
# Edit ~/.claude/settings.json if needed
```

## Step 5: Browse Available Commands
```bash
# List all commands
ls .claude/commands/

# Read command documentation
cat .claude/commands/README.md
```

## Step 6: Practice with Safe Commands
```bash
# These don't modify code:
/review         # Review current file
/help           # Get help

# These create commits (practice safe):
/commit         # Review before confirming
```

## Step 7: Pair Program
Ask a team member to:
- Watch your first `/new-component` command
- Review the results together
- Answer questions

## Getting Help
- Questions? Ask in #dev-help Slack
- Command bugs? File issue on GitHub
- Want to create command? See docs/CONTRIBUTING.md
```

---

## Advanced Patterns & Workflows

### Chained Commands Pattern

```markdown
# .claude/commands/feature-complete.md

---
description: Complete feature development workflow
---

# Complete Feature Development

Execute full feature development workflow:

## Step 1: Plan
1. Read feature requirements
2. Break into tasks
3. Create implementation plan

## Step 2: Implement
1. Generate files/components
2. Write business logic
3. Add error handling

## Step 3: Test
1. Generate unit tests
2. Generate integration tests
3. Verify 80%+ coverage

## Step 4: Review
1. /review (code quality)
2. /security-check (security)
3. /performance-check (performance)

## Step 5: Commit
1. Stage changes: git add .
2. /commit (create commit)
3. git push

User can call individual steps or entire workflow.
```

### Conditional Logic Commands

```markdown
# .claude/commands/smart-test.md

---
description: Generate appropriate tests
---

# Smart Test Generation

Analyze file and generate appropriate tests:

IF file is component:
  → Generate React component tests
  → Test: rendering, props, state, events
  → Use React Testing Library

ELSE IF file is service:
  → Generate unit tests
  → Test: functions, error cases
  → Use Jest mocks

ELSE IF file is API endpoint:
  → Generate integration tests
  → Test: request/response, status codes
  → Use Supertest

ELSE:
  → Generate general unit tests
  → Test: all functions, edge cases
  → Use Jest

Always aim for 80%+ coverage.
```

### Template-Based Commands

```markdown
# .claude/commands/api-endpoint.md

---
argument-hint: [method] [route] [description]
description: Create new API endpoint
---

# New API Endpoint: $ARGUMENTS

Create new API endpoint:

**Method**: $1 (GET/POST/PUT/DELETE)
**Route**: $2
**Description**: $3

## Template Structure

```typescript
// In src/api/routes/[feature].ts

router.$1('$2', async (req, res) => {
  try {
    // Extract/validate input
    const data = req.body; // or req.params

    // Call service
    const result = await [service].action(data);

    // Return response
    res.status(200).json({
      success: true,
      data: result
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});
```

## Requirements
1. Input validation
2. Error handling
3. Logging
4. Tests (integration tests for endpoint)
5. Documentation in OpenAPI

Generate all required files.
```

---

## Integration with Other Practices

### Slash Commands + HOOKS

```
Scenario: Prevent bad commits

HOOK (PreToolUse):
  Prevents: /commit with failing tests
  Error: "Tests must pass before commit"

SLASH COMMAND (/commit):
  Prompts user: "Create conventional commit"
  Verifies: Tests passing (via hook)
  Creates: Proper commit message

Result:
  Hooks enforce rules
  Commands provide easy workflow
```

### Slash Commands + CLAUDE.md

```
CLAUDE.md specifies:
  "Use conventional commits"
  "Tests required before commit"
  "Code review before merge"

Slash Commands implement:
  /commit → Conventional commit
  /test → Generate tests
  /review → Code review

Synergy:
  CLAUDE.md = Policy
  Commands = Easy execution
```

### Slash Commands + SKILLS

```
SKILL: Comprehensive testing framework
  └─ Multiple files
  └─ Validation logic
  └─ Can auto-discover

SLASH COMMAND: Quick test generation
  └─ One file
  └─ User triggers explicitly
  └─ For simple cases

Both useful:
  /test → Quick generation
  Auto-discover skill → Complex testing
```

---

## Common Mistakes & Solutions

### ❌ MISTAKE 1: Too Vague Commands

```
WRONG:
# .claude/commands/help.md

Do something helpful

PROBLEM:
  Claude doesn't know what to do
  Results inconsistent
  Not useful

RIGHT:
# .claude/commands/optimize.md

Analyze this code for performance:

1. Check time complexity O(n) analysis
2. Find N+1 query patterns
3. Identify inefficient loops
4. Suggest 3 specific optimizations
5. Show before/after examples

Provide: Issue description, problem, solution, benefit, effort
```

### ❌ MISTAKE 2: Commands Too Long

```
WRONG:
# .claude/commands/everything.md

[2000 lines of instructions]

PROBLEM:
  Hard to maintain
  Slow to load
  Confusing to read
  Overlaps multiple concerns

RIGHT:
Create specific commands:
  /test           → Test generation
  /review         → Code review
  /optimize       → Performance
  /security       → Security audit

Principle: One concern per command
```

### ❌ MISTAKE 3: No Documentation

```
WRONG:
.claude/commands/
├── review.md
├── test.md
├── deploy.md
(no documentation)

PROBLEM:
  New developers don't know commands exist
  Inconsistent usage
  Commands not adopted

RIGHT:
.claude/commands/
├── README.md           ← Overview
├── review.md           ← With description in frontmatter
├── test.md
├── deploy.md
└── EXAMPLES.md         ← Real usage examples

Plus:
  docs/CLAUDE_COMMANDS.md in repo root
  Link from main README
  Mention in CONTRIBUTING.md
```

### ❌ MISTAKE 4: Too Many Arguments

```
WRONG:
/create-thing arg1 arg2 arg3 arg4 arg5

PROBLEM:
  Hard to remember order
  Error-prone
  Confusing invocation

RIGHT:
/create-thing name "description"

Or use flags:
/create-thing --name Button --description "A button"

Principle: Max 2-3 simple arguments
```

---

## Team Deployment Strategy

### Phase 1: Foundation (Week 1)

```
Create core commands:
  .claude/commands/
  ├── README.md
  ├── review.md
  ├── test.md
  ├── commit.md
  └── quick-reference.md

Communicate:
  ✓ Announce in engineering Slack
  ✓ Link to README
  ✓ Show examples
  ✓ Invite team to test

Goal: Team discovers benefits
```

### Phase 2: Adoption (Week 2-3)

```
Expand commands:
  ├── backend/
  │   └── new-endpoint.md
  ├── frontend/
  │   └── new-component.md
  └── deployment/
      ├── deploy-staging.md
      └── deploy-prod.md

Support:
  ✓ Answer questions in Slack
  ✓ Create usage examples
  ✓ Fix commands based on feedback
  ✓ Celebrate successful usage

Goal: Regular adoption in workflows
```

### Phase 3: Standardization (Week 4+)

```
Integrate into process:
  ✓ Add to CONTRIBUTING.md
  ✓ Use in code reviews
  ✓ Reference in team guidelines
  ✓ Include in onboarding

Maintenance:
  ✓ Regular reviews (quarterly)
  ✓ Update when processes change
  ✓ Remove unused commands
  ✓ Collect team feedback

Goal: Commands are standard practice
```

### Metrics to Track

```
Adoption:
  - % of team using each command
  - Frequency of usage
  - New commands created by team

Quality:
  - Issues reported per command
  - Success rate (intended outcome achieved)
  - Team satisfaction

Efficiency:
  - Time saved per command
  - Consistency improvements
  - Onboarding time reduction
```

---

## Quick Reference & Checklists

### Command Creation Checklist

```
PLANNING:
  ☐ Define clear purpose
  ☐ Identify pain point it solves
  ☐ Estimate time saved
  ☐ Plan arguments/inputs

CREATION:
  ☐ Create .md file
  ☐ Write clear, concise instructions
  ☐ Test command works
  ☐ Add to README.md
  ☐ Document with examples

TEAM INTEGRATION:
  ☐ Get team feedback
  ☐ Refine based on feedback
  ☐ Commit to git
  ☐ Announce in Slack
  ☐ Add to onboarding docs

MAINTENANCE:
  ☐ Monitor usage
  ☐ Fix reported issues
  ☐ Update if process changes
  ☐ Remove if unused
```

### Command File Template

```markdown
# .claude/commands/[command-name].md

---
description: [One-line description]
category: [category: quality/testing/deployment/etc]
tags: [relevant, tags, separated, by, commas]
---

# [Command Title]

[One paragraph explaining what command does]

## What it does

[Detailed explanation of:
- What will be analyzed
- What will be generated
- What will be output]

## How to use

```
/[command-name] [arguments if any]
```

## Example

[Show example of running the command]

## Output

[Show example output]

## Notes

[Any important notes, prerequisites, or caveats]
```

### Invocation Quick Reference

```
Basic:
  /help              → List all commands
  /list              → List slash commands
  /review            → Run /review command

With Arguments:
  /new-component Button              → One argument
  /new-component Button "A button"   → Multiple arguments
  /fix-issue 42                       → Positional arg

Scoped:
  /project:review    → Project command explicitly
  /user:my-command   → User command explicitly
  /feature:new       → Namespaced command

Piping (if supported):
  /cmd1 | /cmd2      → Chain commands
```

---

## Pro Tips

1. **Use $ARGUMENTS for flexibility**
   ```markdown
   Fix issue #$ARGUMENTS
   ```
   Works with any issue number

2. **Organize by category**
   ```
   testing/test-unit.md
   testing/test-integration.md
   ```
   Cleaner than one big test command

3. **Document in frontmatter**
   ```markdown
   ---
   description: What this does
   tags: perf, optimization
   ---
   ```
   Helps team discover commands

4. **Create README.md**
   ```
   .claude/commands/README.md
   ```
   Show available commands and usage

5. **Version control everything**
   ```bash
   git add .claude/commands/
   git commit -m "Add new commands"
   ```
   Team gets same commands

---

**Version**: 1.0
**Date**: January 7, 2026
**Status**: Production-ready comprehensive guide
**Size**: 8,000+ words, 12 sections, 50+ examples

---

## Related Guides

### Getting Started
- [INDEX.md](INDEX.md) - Master documentation index
- [Complete Practices (Russian)](CLAUDE-SLASH-COMMANDS-GUIDE.md) - Original Russian version

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
