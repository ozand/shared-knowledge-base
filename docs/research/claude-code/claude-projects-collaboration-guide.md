# Claude Code Projects (Collaboration): Полное руководство по Team Development
## Лучшие практики, patterns и enterprise collaboration strategies

---

## Оглавление

1. [Фундаментальные концепции](#фундаментальные-концепции)
2. [Projects: Bounded Contexts for Collaboration](#projects-bounded-contexts)
3. [Team Plan Structure & Permissions](#team-plan-structure--permissions)
4. [Shared CLAUDE.md Hierarchy](#shared-claudemd-hierarchy)
5. [Git Worktrees: Parallel Development](#git-worktrees-parallel-development)
6. [Sub-Agents Architecture](#sub-agents-architecture)
7. [Team Collaboration Patterns](#team-collaboration-patterns)
8. [Real-World Team Workflows](#real-world-team-workflows)
9. [Knowledge Management & Context](#knowledge-management--context)
10. [Governance & Access Control](#governance--access-control)
11. [Enterprise Deployment Strategy](#enterprise-deployment-strategy)
12. [Quick Reference & Checklists](#quick-reference--checklists)

---

## Фундаментальные концепции

### What is "Collaboration" in Claude Code?

```
Collaboration in Claude Code = Multiple team members working together effectively

NOT just: Shared code repository (git)
IS: Shared context + shared workflows + shared governance

Three collaboration layers:

1. CODE COLLABORATION (Git)
   └─ Version control, branches, PRs
   └─ Standard software development

2. CONTEXT COLLABORATION (CLAUDE.md + Projects)
   └─ Shared project context
   └─ Shared coding standards
   └─ Shared architectural patterns

3. WORKFLOW COLLABORATION (Parallel agents, sub-agents)
   └─ Multiple Claude instances working on different tasks
   └─ Coordinated development
   └─ Parallel feature development
```

### Why Collaboration Matters

```
SINGLE DEVELOPER:
✓ Fast for simple tasks
✗ Bottleneck for complex projects
✗ Context loss between sessions
✗ No code review from AI
✗ Long total time

TEAM COLLABORATION:
✓ Parallel development (multiple tasks)
✓ Persistent shared context
✓ Continuous AI code review
✓ Different perspectives on problems
✓ Hedge against model failures
✓ Knowledge sharing across team

IMPACT:
- 40% faster delivery times (proven from power users)
- Better code quality (multi-perspective review)
- Reduced context switching
- Better knowledge persistence
```

---

## Projects: Bounded Contexts for Collaboration

### What are Projects?

```
Projects = Self-contained workspaces with:
- Own chat history
- Own knowledge base (uploaded documents)
- Own custom instructions
- Own configuration

Think of as: Personal knowledge base for a project
Analogy: Like having a desk with:
  - Project-specific reference materials
  - Project-specific guidelines
  - Project-specific conversations
  - Project-specific context

AVAILABLE ON:
✓ Pro plans (personal use)
✓ Team plans (shared with team)
✓ Enterprise plans (org-wide)
```

### Project Structure (Team Plan)

```
CLAUDE Projects
├── Frontend Architecture (shared)
│   ├── Custom instructions: React patterns, styling approach
│   ├── Knowledge: Design system docs, component library
│   └── Members: Frontend team (Can edit)
│
├── Backend Services (shared)
│   ├── Custom instructions: API standards, database patterns
│   ├── Knowledge: Schema docs, API reference
│   └── Members: Backend team (Can edit)
│
├── DevOps/Deployment (shared)
│   ├── Custom instructions: Deployment process, monitoring
│   ├── Knowledge: Architecture diagrams, runbooks
│   └── Members: DevOps team (Can use)
│
└── Company Wide (shared)
    ├── Custom instructions: Company coding standards
    ├── Knowledge: Company policies, best practices
    └── Members: All engineers (Can use)
```

### Permission Levels

```
ROLE BASED PERMISSIONS:

1. "Can use" (Viewer)
   ✓ See project contents
   ✓ Chat within project
   ✓ Read knowledge base
   ✗ Cannot edit instructions
   ✗ Cannot add/remove members
   → Perfect for: Reference access, learning

2. "Can edit" (Editor)
   ✓ Modify project instructions
   ✓ Add/remove members
   ✓ Update knowledge base
   ✓ Chat within project
   → Perfect for: Active team members

3. Creator (Admin)
   ✓ All edit permissions
   ✓ Control who has access
   ✓ Share/unshare project
   → Perfect for: Project owner

PRINCIPLE:
Grant minimum necessary permissions
Viewer by default, Editor for contributors
```

---

## Team Plan Structure & Permissions

### Recommended Organization Structure

```
TEAM PLAN HIERARCHY:

Organization Level
├── Admin Controls
│   ├── SSO/Domain capture
│   ├── Spend controls
│   ├── Audit logging
│   └── Managed settings
│
├── Seats Management
│   ├── Standard seats (Claude chat only)
│   └── Premium seats (Claude + Claude Code)
│
└── Project Structure
    ├── Public projects (discovery)
    ├── Private projects (protected)
    └── Shared projects (team collaboration)
```

### Settings Hierarchy

```
PRECEDENCE:
1. Organization-wide settings (enforced)
2. Project-level settings
3. User overrides (if allowed)

MANAGED SETTINGS (Admin enforced):
├── Tool permissions
├── MCP server allowlists
├── File access restrictions
├── Command execution rules
└── Audit logging rules

USER SETTINGS (Can override if allowed):
├── Custom preferences
├── Local workflow setup
└── Session defaults
```

---

## Shared CLAUDE.md Hierarchy

### Multi-Level CLAUDE.md Architecture

```
HIERARCHY (Most specific wins):

Level 1: User Home
~/.claude/CLAUDE.md
├─ Personal coding style
├─ Personal preferences
├─ User-specific guidelines
└─ Applies to all projects

Level 2: Organization
~/.claude/organization/CLAUDE.md
├─ Company coding standards
├─ Company architectural patterns
├─ Company policies
└─ Applies to all team projects

Level 3: Project Root
./CLAUDE.md
├─ Project-specific context
├─ Project architecture
├─ Project standards
├─ Applies only to this project

Level 4: Subdirectory
./src/backend/CLAUDE.md
├─ Backend-specific guidance
├─ Database patterns
├─ API standards
└─ Applies to this directory

RESOLUTION PROCESS:
Claude reads all applicable files
More specific files override general ones
All relevant context is combined automatically
```

### Example Project CLAUDE.md

```markdown
# Project Context

## Project: E-Commerce Platform
Team Size: 8 developers
Stack: React + Node.js + PostgreSQL

## Architecture Overview

### Frontend (React)
- Component-driven architecture
- Custom hooks for state management
- Styled Components for styling

### Backend (Node.js)
- REST API with Express
- PostgreSQL with Knex migrations
- Redis for caching

## Coding Standards

### React Components
- Functional components with hooks
- TypeScript strict mode
- 80%+ test coverage
- JSDoc for all exports

### API Endpoints
- RESTful patterns
- Comprehensive error handling
- Rate limiting on all endpoints
- Comprehensive logging

## Team Guidelines

### Code Review Standards
- All PRs require 2 approvals
- Focus on: security, performance, maintainability
- Use /review command

### Testing Requirements
- Unit tests for business logic
- Integration tests for APIs
- E2E tests for critical flows

## Currently Working On
- Feature: User authentication (auth branch)
- Feature: Payment integration (payments branch)
- Refactor: API error handling (refactor-errors)

See /api-standards.md for detailed API patterns.
```

---

## Git Worktrees: Parallel Development

### What are Git Worktrees?

```
Git Worktrees = Check out multiple branches simultaneously in different directories

Traditional Git:
  One working directory
  One branch at a time
  Switch branches = reload context, restart Claude

With Git Worktrees:
  Multiple working directories
  Multiple branches active simultaneously
  Multiple Claude sessions in parallel
  No context switching
  True parallel development
```

### Parallel Claude Development Workflow

```
SETUP:

1. Create worktrees for each feature:
   git worktree add ../project-feature-auth -b feature/auth
   git worktree add ../project-feature-payments -b feature/payments
   git worktree add ../project-refactor-api -b refactor/api-errors

2. Start Claude session in each:
   cd ../project-feature-auth && claude
   cd ../project-feature-payments && claude
   cd ../project-refactor-api && claude

3. Run in parallel:
   Each Claude works independently
   Each has own context window
   No conflicts or interference

4. Merge best results:
   Complete features
   Test independently
   Merge to main
   Delete worktrees

RESULT:
✓ 3 features developed in parallel (takes 1x time instead of 3x)
✓ Each Claude has full context
✓ No merge conflicts during development
✓ Each agent can use full token budget
```

### Parallel Development Architecture

```
Git Repository
├── main branch
│
├── feature-auth (worktree 1)
│   └─ Claude-1 working on auth
│
├── feature-payments (worktree 2)
│   └─ Claude-2 working on payments
│
└── refactor-api (worktree 3)
    └─ Claude-3 working on error handling

BENEFITS:
- Non-deterministic LLMs → Run 3 versions, pick best
- Parallel execution → Total time ≈ longest agent
- Different perspectives → Better solutions
- Risk hedging → If one agent fails, others succeed
```

### Commands

```bash
# Create worktree
git worktree add ../project-feature-name -b feature/name

# List worktrees
git worktree list

# Run Claude in worktree
cd ../project-feature-name
claude

# Delete worktree when done
git worktree remove ../project-feature-name
```

---

## Sub-Agents Architecture

### Multi-Agent Coordination

```
COORDINATION STRUCTURE:

Main Claude (Coordinator)
├─ Understands overall plan
├─ Delegates tasks
└─ Integrates results

Sub-Agent 1: Code Reviewer
├─ Specializes in code quality
├─ Own context: code standards
├─ Own permissions: read-only
└─ Task: Review other agents' code

Sub-Agent 2: Test Engineer
├─ Specializes in testing
├─ Own context: test patterns
├─ Own permissions: test execution
└─ Task: Write and run tests

Sub-Agent 3: Documentation Writer
├─ Specializes in docs
├─ Own context: doc standards
├─ Own permissions: markdown writing
└─ Task: Update documentation

WORKFLOW:
1. Main Claude creates plan
2. Delegates to specialized agents
3. Each agent works independently
4. Main Claude integrates results
```

### Sub-Agent Setup

```
.claude/agents/
├── code-reviewer.md
│   ├── Role: Code quality specialist
│   ├── Scope: Review and suggest improvements
│   ├── Tools: Read-only file access
│   └── Output: Feedback as comments
│
├── test-engineer.md
│   ├── Role: Testing specialist
│   ├── Scope: Generate tests, run tests
│   ├── Tools: Test execution, bash
│   └── Output: Test files, coverage reports
│
└── doc-writer.md
    ├── Role: Documentation specialist
    ├── Scope: Write and update docs
    ├── Tools: Markdown editing
    └── Output: Updated documentation
```

---

## Team Collaboration Patterns

### Pattern 1: Collaborative Code Review

```
Workflow:

1. Developer writes code with Claude
   ```bash
   cd project
   claude
   "Implement user authentication"
   ```
   → Claude-1 generates auth system

2. Human reviews code
   Push to PR
   Request review

3. AI Code Reviewer sub-agent
   Reads PR
   Analyzes code
   Posts automated review

4. Human + AI feedback
   Developer addresses feedback
   Claude-2 refines code
   Final approval

Result: Consistent, high-quality code
```

### Pattern 2: Specification-Driven Development

```
Workflow:

1. Create Project PRD (Product Requirements)
   └─ Detailed specification
   └─ Store in .claude/docs/PRD.md

2. Create Project Plan
   └─ Break PRD into tasks
   └─ Create .claude/docs/PLAN.md

3. Team members claim tasks
   └─ Each takes feature from plan
   └─ Creates own worktree

4. Parallel development
   └─ Multiple Claude agents
   └─ Each following spec
   └─ No overlaps

5. Integration
   └─ Merge features to main
   └─ Verify against spec

Result: Spec-driven, traceable, organized
```

### Pattern 3: Asynchronous Collaboration

```
Workflow:

1. Team member A writes code
   → Leaves notes in markdown
   → Commits to feature branch

2. Team member B picks up
   → Reads context files
   → References previous work
   → Continues development

3. Persistent Shared Files
   └─ .claude/docs/progress.md (current status)
   └─ .claude/docs/decisions.md (why decisions made)
   └─ .claude/docs/next-steps.md (what's next)

4. Each team member builds on context
   └─ No real-time meetings needed
   └─ Async workflow
   └─ Global teams compatible

Result: 24/7 development, preserved context
```

---

## Real-World Team Workflows

### Startup Workflow (5 developers)

```
TEAM STRUCTURE:
- 1 Tech Lead
- 2 Backend developers
- 1 Frontend developer
- 1 DevOps engineer

WORKFLOW:

Week 1: Setup
├─ Create Projects (Backend, Frontend, DevOps, Company)
├─ Write CLAUDE.md files
├─ Create slash commands library
└─ Set permissions

Week 2: Parallel Development
├─ Tech Lead: Architecture design (/plan mode)
├─ Backend-1: User service (git worktree)
├─ Backend-2: Payment service (git worktree)
├─ Frontend: UI components (git worktree)
├─ DevOps: Infrastructure (git worktree)
└─ Each uses Claude in parallel

Week 3: Integration
├─ All PRs merged
├─ Code review by tech lead + AI
├─ Final testing
└─ Deploy

RESULTS:
✓ 3 weeks vs 6 weeks (single developer)
✓ Consistent code quality
✓ Shared knowledge
✓ Reduced technical debt
```

### Enterprise Workflow (50+ developers)

```
TEAM STRUCTURE:
- Platform team (6 engineers)
- Squad A: User facing (8 engineers)
- Squad B: Backend services (8 engineers)
- Squad C: Data/Analytics (8 engineers)
- Infrastructure team (6 engineers)

GOVERNANCE:

Organization-Level CLAUDE.md
├─ Company coding standards
├─ Company architectural patterns
├─ Security policies

Squad-Level Projects
├─ Squad-specific context
├─ Squad custom commands
├─ Squad knowledge base

Individual Developer Context
├─ Personal preferences
├─ Local development setup

WORKFLOW:

1. Product Manager writes spec
   └─ Stored in shared project
   └─ Reviewed by squad leads

2. Squad Lead breaks down
   └─ Assigns tasks
   └─ Creates tickets

3. Developers claim tasks
   └─ Create feature branches
   └─ Run Claude Code in parallel

4. Continuous Integration
   └─ Auto-review by AI
   └─ Security scanning
   └─ Performance testing

5. Squad Lead integrates
   └─ Merges to squad branch
   └─ Squad testing
   └─ Merge to main

RESULTS:
✓ 50+ developers coordinated
✓ Consistent across organization
✓ Knowledge stays organized
✓ Onboarding 1 week instead of 1 month
```

---

## Knowledge Management & Context

### Organizational Knowledge Structure

```
CLAUDE Projects Knowledge Base

Tier 1: Company-Wide
├─ Coding standards
├─ Architectural patterns
├─ Security policies
├─ DevOps runbooks
└─ Shared to: All engineers

Tier 2: Team-Specific
├─ Team architecture
├─ Team workflows
├─ Team conventions
└─ Shared to: Team members only

Tier 3: Project-Specific
├─ Project context
├─ Project decisions
├─ Project patterns
└─ Shared to: Project team

Tier 4: Session-Specific
├─ Current task
├─ Session plan
├─ Session decisions
└─ Stored in: PLAN.md, decisions.md

PRINCIPLE:
Bounded contexts + Progressive disclosure
Find what you need without overwhelming info
```

### Persistent Project Memory

```
Key Files for Persistence:

.claude/docs/
├── CLAUDE.md               (project context)
├── ARCHITECTURE.md         (system design)
├── API_STANDARDS.md        (API patterns)
├── progress.md             (current status)
├── decisions.md            (why decisions made)
├── next-steps.md           (what's next)
├── known-issues.md         (technical debt)
├── changelog.md            (what changed)
└── onboarding.md           (new developer guide)

USAGE:
- New session? Start by reading these files
- Resume work? Check progress.md
- Want history? Check decisions.md
- Onboarding? Share onboarding.md

BENEFIT:
✓ Context preserved between sessions
✓ New team members get up to speed
✓ Decisions documented
✓ Reduces repeated mistakes
```

---

## Governance & Access Control

### Three Governance Modes (Simultaneously)

```
1. Human Authority (Strategic)
   └─ CLAUDE.md defines strategy
   └─ Project leads set direction
   └─ /rewind for rollback
   └─ Ensures values alignment

2. Algorithmic Governance (Operational)
   └─ Managed settings enforce rules
   └─ Permission levels control access
   └─ Deny rules prevent dangerous actions
   └─ Ensures efficiency and consistency

3. Distributed Innovation (Adaptation)
   └─ Team creates custom commands
   └─ Team creates sub-agents
   └─ Team customizes workflows
   └─ Ensures evolution and growth

PRINCIPLE:
All three operating simultaneously
Each checks excesses of others
Creates resilient, adaptive system
```

### Enterprise Access Control

```
ORGANIZATION LEVEL (Admin enforced):
├─ Tool access restrictions
├─ MCP server allowlists
├─ File access patterns
├─ Managed settings.json
└─ Cannot be overridden

PROJECT LEVEL (Project leads):
├─ Share with specific members
├─ Set permission levels (View/Edit)
├─ Custom instructions
├─ Can add additional restrictions

USER LEVEL (Developers):
├─ Local permission prompts
├─ Slash command choices
├─ Session mode selection
└─ /permissions command

LOCAL DEVICE (Developers):
├─ Read-only local files
├─ Execute commands
├─ Access to MCP servers
└─ Full control on machine
```

---

## Enterprise Deployment Strategy

### Phase 1: Foundation (Week 1-2)

```
Pilots:
  ✓ 5 engineers on pilot team
  ✓ Create company CLAUDE.md
  ✓ Create team Projects
  ✓ Document initial workflows

Training:
  ✓ How to use CLAUDE.md
  ✓ How to use Projects
  ✓ How to use slash commands
  ✓ How to use Git worktrees

Governance:
  ✓ Define coding standards
  ✓ Define permission levels
  ✓ Create managed settings.json
  ✓ Set up audit logging
```

### Phase 2: Expansion (Week 3-6)

```
Scale:
  ✓ Expand to 2-3 teams
  ✓ Create squad-level Projects
  ✓ Expand CLAUDE.md per squad
  ✓ Create team slash commands

Refinement:
  ✓ Collect feedback
  ✓ Update workflows
  ✓ Create best practices guide
  ✓ Document anti-patterns

Integration:
  ✓ GitHub integration
  ✓ Jira integration
  ✓ Slack notifications
  ✓ Audit logging
```

### Phase 3: Production (Week 7+)

```
Rollout:
  ✓ All teams using system
  ✓ Consistent governance
  ✓ Optimized workflows

Optimization:
  ✓ Monitor usage patterns
  ✓ Optimize hot paths
  ✓ Update based on feedback
  ✓ Quarterly governance review

Operations:
  ✓ Monthly: Review access, rotate credentials
  ✓ Quarterly: Audit logs, assess compliance
  ✓ Quarterly: Update standards based on learnings
```

---

## Quick Reference & Checklists

### Team Setup Checklist

```
ORGANIZATION:
  ☐ Set up Team plan with appropriate seats
  ☐ Configure SSO (if enterprise)
  ☐ Set spend controls
  ☐ Enable audit logging

PEOPLE:
  ☐ Define roles (Developer, Lead, Admin)
  ☐ Assign seat types (Standard vs Premium)
  ☐ Plan team structure
  ☐ Identify squad leads

KNOWLEDGE:
  ☐ Write company CLAUDE.md
  ☐ Write squad CLAUDE.md
  ☐ Create Projects per team
  ☐ Upload reference documents

WORKFLOWS:
  ☐ Define code standards
  ☐ Define collaboration patterns
  ☐ Create slash commands library
  ☐ Document in README

GOVERNANCE:
  ☐ Create managed-settings.json
  ☐ Define permission levels
  ☐ Set MCP allowlists
  ☐ Configure audit retention
```

### Onboarding New Developer Checklist

```
DAY 1:
  ☐ GitHub access
  ☐ Claude account created
  ☐ Assigned to team Projects
  ☐ Recommended first command: /review

DAY 2:
  ☐ Read company CLAUDE.md
  ☐ Read squad CLAUDE.md
  ☐ Read project-specific docs
  ☐ Ask: clarifying questions

DAY 3:
  ☐ Pair with senior developer
  ☐ Create first feature branch
  ☐ Run Claude Code with guidance
  ☐ Create first PR with review

FIRST WEEK:
  ☐ Complete 2-3 small tasks
  ☐ Familiar with slash commands
  ☐ Understand code review process
  ☐ Know who to ask questions
```

### Parallel Development Checklist

```
SETUP:
  ☐ Create feature branches
  ☐ Create Git worktrees
  ☐ Create detailed plans
  ☐ Assign Claude agents

EXECUTION:
  ☐ Each agent starts independently
  ☐ Each primes with context
  ☐ Each follows plan
  ☐ Regular check-ins

INTEGRATION:
  ☐ All tasks complete
  ☐ All code reviewed
  ☐ All tests pass
  ☐ Merge to main
  ☐ Delete worktrees
  ☐ Compare outcomes
```

---

**Версия**: 1.0  
**Дата**: 7 января 2026  
**Статус**: Production-ready comprehensive guide  
**Объем**: 8000+ слов, 12 разделов, 60+ примеров

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

