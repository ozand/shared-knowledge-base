# Claude Code Shared Model: Практические шаблоны и конфигурации
## Копируй-вставляй примеры для быстрого старта

---

## 1. Шаблон Root CLAUDE.md для Монорепо

```markdown
# CLAUDE.md — Shared Knowledge Model

## Project Overview
- **Type**: Full-stack Monorepo
- **Tech Stack**: [Your stack]
- **Teams**: [Team structure]
- **Updated**: [Date]

## 📍 Architecture
Team structure and architecture decisions:
→ See `@.claude/standards/architecture.md`

## 📁 Project Structure
```
packages/          # Shared packages
apps/              # Applications
services/          # Microservices
infra/             # Infrastructure
```

## 📋 Core Standards
- **Code**: `@.claude/standards/coding-standards.md`
- **Testing**: `@.claude/standards/testing-guidelines.md`
- **API**: `@.claude/standards/api-standards.md`
- **Database**: `@.claude/standards/db-schema.md`
- **Deployment**: `@.claude/standards/deployment.md`

## 🛠 Common Commands
\`\`\`bash
claude init                 # Initialize new project
claude dev                  # Start development
claude test [module]        # Run tests
claude build [app]          # Build production
claude deploy               # Deploy to staging
\`\`\`

## 🎯 Available Skills
Reusable capabilities (see `@.claude/skills/`):
- **testing** — Generate tests matching patterns
- **refactoring** — Safe code refactoring
- **docs** — Auto-generate documentation
- **migration** — Database migrations

## 🤖 Available Agents
Automated workflows (see `@.claude/agents/`):
- **code-review** — Automatic PR review
- **pr-automation** — PR workflow automation
- **deployment** — Deployment orchestration
- **testing** — Test coverage optimization

## 📖 Documentation
→ See `@docs/` for detailed guides:
- **Architecture**: System design & decisions
- **Workflows**: Feature development process
- **Runbooks**: Troubleshooting & incident response
- **Onboarding**: Setup & first tasks

## ⚡ Team Workflows
→ See `@.claude/team/`:
- **principles.md** — How we work
- **workflows.md** — Development process
- **incident-response.md** — Handling production issues

## ❓ FAQ & Troubleshooting
→ See `@.claude/team/faq.md` and `@docs/runbooks.md`

## Important Notes
1. Always reference shared standards, not personal preferences
2. Use Skills and Agents for repetitive tasks
3. Ask for help via [#engineering Slack] before starting complex work
4. Changes to shared code need code review

## Scope Hierarchy
Local (.local.md) → Project (.claude/) → User (~/.claude/) → Enterprise
```

---

## 2. Шаблон Package-specific CLAUDE.md

```markdown
# CLAUDE.md — [Package Name]

## Overview
[Brief description of what this package does]

## Architecture
[Key architectural patterns specific to this package]

See also: `@../../.claude/standards/architecture.md`

## Tech Stack
- [Primary technology]
- [Key dependencies]
- [Testing framework]

## Key Files
```
src/
├── index.ts          # Main export
├── components/       # React components
├── hooks/           # Custom hooks
└── utils/           # Utilities
```

## Patterns
See `@./patterns/` for specific patterns:
- Pattern 1
- Pattern 2
- Pattern 3

## Testing Strategy
- Unit: [Framework]
- Integration: [Framework]
- E2E: [Framework]

Testing rules: `@../../.claude/standards/testing-guidelines.md`

## Development
\`\`\`bash
# Development
npm run dev

# Testing
npm test

# Building
npm run build

# Type checking
npm run typecheck
\`\`\`

## API / Public Interface
[Document public exports]

## Important Rules
1. [Rule 1]
2. [Rule 2]
3. [Rule 3]

See `@../../.claude/standards/` for full standards.

## Deprecated
[List deprecated functions/patterns if any]

## Dependencies on Other Packages
- Package A → Used for [reason]
- Package B → Used for [reason]

This package is used by:
- App X
- App Y
```

---

## 3. Шаблон settings.json для Shared Конфигурации

```json
{
  "comment": "Claude Code settings — shared across team",
  
  "skills": {
    "paths": [
      "./.claude/skills",
      "./packages/*/claude/skills"
    ],
    "enabled": [
      "testing",
      "documentation",
      "refactoring",
      "migration"
    ],
    "auto_discover": true
  },

  "agents": {
    "paths": ["./.claude/agents"],
    "enabled": [
      "code-review",
      "pr-automation",
      "deployment",
      "testing"
    ]
  },

  "commands": {
    "dev": {
      "description": "Start development environment",
      "runner": "npm run dev"
    },
    "test": {
      "description": "Run test suite",
      "runner": "npm test",
      "args": ["--coverage"]
    },
    "build": {
      "description": "Production build",
      "runner": "npm run build"
    },
    "deploy": {
      "description": "Deploy to staging",
      "runner": "npm run deploy:staging"
    },
    "lint": {
      "description": "Lint code",
      "runner": "npm run lint --fix"
    }
  },

  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "commands": [
          "echo 'Claude Code session started'",
          "git status"
        ]
      }
    ]
  },

  "permissions": {
    "dangerous_commands": {
      "delete_files": "require_approval",
      "database_migration": "require_approval",
      "production_deploy": "require_approval"
    }
  },

  "context_limits": {
    "max_tokens_per_session": 100000,
    "auto_cleanup_frequency": "hourly"
  }
}
```

---

## 4. Шаблон .mcp.json для Model Context Protocol

```json
{
  "mcpServers": {
    "knowledge-base": {
      "command": "node",
      "args": ["./tools/mcp-knowledge-loader.js"],
      "description": "Load project knowledge dynamically",
      "env": {
        "KNOWLEDGE_PATH": "./.claude/standards",
        "CACHE_ENABLED": "true"
      }
    },

    "schema-validator": {
      "command": "python3",
      "args": ["./tools/mcp-schema-validator.py"],
      "description": "Validate against project schemas",
      "env": {
        "SCHEMAS_PATH": "./.claude/references/schemas"
      }
    },

    "test-runner": {
      "command": "node",
      "args": ["./tools/mcp-test-runner.js"],
      "description": "Run tests with detailed feedback"
    },

    "linter": {
      "command": "node",
      "args": ["./node_modules/.bin/eslint"],
      "description": "Lint code with ESLint"
    }
  }
}
```

---

## 5. Шаблон SKILL.md

```markdown
# Skill: [Skill Name]

## Purpose
[What does this Skill do?]

## When to Use
Claude will automatically trigger this Skill when:
- User mentions [keywords]
- As part of [workflow]
- Called by [agents]

## What Claude Can Do
- Capability 1
- Capability 2
- Capability 3

## Key References
→ `@./templates/` for code templates
→ `@./patterns.md` for patterns
→ `@../../.claude/standards/` for standards

## Rules & Constraints
1. [Rule 1]
2. [Rule 2]
3. [Rule 3]

## How to Trigger Manually
\`\`\`bash
claude [skill-name] [options]
# Example:
claude test --coverage
claude refactor --strict
\`\`\`

## Examples
### Example 1
[Describe scenario and output]

### Example 2
[Describe scenario and output]

## Output Format
[What kind of output should user expect]

## Advanced Options
- `--strict`: Enforce all rules strictly
- `--fast`: Quick version (less thorough)
- `--debug`: Verbose output

## Troubleshooting
- **Issue 1**: Solution
- **Issue 2**: Solution

## Implementation Details
[Technical details for advanced users]
```

---

## 6. Шаблон Architecture Standard

```markdown
# Architecture Standards

## System Overview
[High-level system description]

## Core Principles
1. **Principle 1** — Explanation
2. **Principle 2** — Explanation
3. **Principle 3** — Explanation

## Architectural Decisions

### ADR-001: [Decision Name]
- **Context**: [Why was this decision made?]
- **Decision**: [What was decided?]
- **Consequences**: [What are the implications?]
- **Date**: YYYY-MM-DD
- **Status**: [Accepted/Deprecated/Superseded]

### ADR-002: [Decision Name]
- **Context**: ...
- **Decision**: ...
- **Consequences**: ...

## Layer Structure

### Presentation Layer
- Components
- Pages/Views
- Routing

### Business Logic Layer
- Services
- State management
- Validation

### Data Layer
- API clients
- Database access
- Caching

### Infrastructure Layer
- Logging
- Monitoring
- Error tracking

## Technology Stack
| Layer | Technology | Version | Why |
|-------|-----------|---------|-----|
| Frontend | React | 18+ | Component library |
| Backend | Node.js | 18+ | Server runtime |
| DB | PostgreSQL | 14+ | Relational DB |
| Cache | Redis | 6+ | Session/cache |
| Queue | Bull | 4+ | Job queue |

## Code Organization

### Frontend
```
src/
├── components/      # Reusable components
├── pages/          # Page components
├── hooks/          # Custom hooks
├── services/       # API & business logic
├── store/          # State management
├── utils/          # Utilities
├── types/          # TypeScript types
└── styles/         # Global styles
```

### Backend
```
src/
├── routes/         # API routes
├── middleware/     # Express middleware
├── services/       # Business logic
├── models/         # Database models
├── utils/          # Utilities
├── types/          # TypeScript types
└── config/         # Configuration
```

## Data Flow
[Describe request/response flow]

## State Management
- **Frontend**: [Tool]
- **Backend**: [Pattern]
- **Caching**: [Strategy]

## Integration Points
- **External APIs**: [List]
- **Third-party Services**: [List]
- **Microservices**: [List]

## Security Considerations
- Authentication: [Method]
- Authorization: [Method]
- Data Encryption: [Method]
- CSRF Protection: [Method]

## Performance Targets
- Page Load Time: [X]ms
- API Response Time: [Y]ms
- Database Query Time: [Z]ms

## Scaling Strategy
- Horizontal: [Method]
- Vertical: [Method]
- Caching: [Strategy]

## Monitoring & Observability
- Logging: [Service]
- Metrics: [Service]
- Tracing: [Service]
- Error Tracking: [Service]

## Disaster Recovery
- Backup Strategy: [Method]
- Recovery Time Objective: [X] hours
- Recovery Point Objective: [Y] minutes

## Migration Paths
[Future architecture considerations]
```

---

## 7. Шаблон Coding Standards

```markdown
# Coding Standards

## Language: [JavaScript/TypeScript/Python/etc]

## Code Organization

### File Structure
\`\`\`
src/
├── modules/
│   └── [feature-name]/
│       ├── index.ts            # Export public API
│       ├── [feature].service.ts # Business logic
│       ├── [feature].model.ts   # Data models
│       ├── [feature].types.ts   # TypeScript types
│       ├── __tests__/           # Tests
│       └── README.md            # Module docs
\`\`\`

### Module Exports
- Export only public API
- Use index.ts as barrel file
- Avoid circular dependencies

## Naming Conventions

### Files
- Components: PascalCase (Button.tsx)
- Services: camelCase.service.ts (user.service.ts)
- Models: camelCase.model.ts (user.model.ts)
- Utils: descriptive names (formatDate.ts)

### Variables & Functions
- Functions: camelCase (getUserById)
- Classes: PascalCase (UserService)
- Constants: UPPER_SNAKE_CASE (MAX_RETRIES)
- Booleans: is/has prefix (isActive, hasError)

### Component Props
- Use TypeScript interfaces
- Name: ComponentProps
- Example: ButtonProps

## Code Style

### Formatting
- Indentation: 2 spaces
- Line length: 100 characters max
- Trailing commas: Always
- Semicolons: Required

### Comments
\`\`\`typescript
// Single-line comments for brief explanations

/**
 * JSDoc for functions/classes
 * @param x Description
 * @returns Description
 */
function example(x: number): string {
  return String(x);
}
\`\`\`

### Error Handling
- Use typed errors
- Provide context in messages
- Log errors with context
- Don't swallow errors

\`\`\`typescript
try {
  await riskyOperation();
} catch (error) {
  const message = `Operation failed: ${error.message}`;
  logger.error(message, { context: { error } });
  throw new CustomError(message, error);
}
\`\`\`

## Testing Requirements
- Unit test coverage: 80%+
- Integration tests: For critical paths
- E2E tests: User workflows
- No test skips (.skip, .only) in main

## Performance Requirements
- Tree-shaking: Explicit exports
- Code splitting: By route
- Bundle size: Track in CI
- Runtime: Profile hot paths

## Accessibility
- Semantic HTML
- ARIA labels where needed
- Keyboard navigation
- Color contrast: WCAG AA

## Type Safety
\`\`\`typescript
// ✅ DO: Explicit types
function getUserById(id: string): Promise<User> {
  ...
}

// ❌ DON'T: Use 'any'
function getUserById(id: any): any {
  ...
}
\`\`\`

## Async/Await
- Always handle errors
- Use async/await, not .then()
- Use Promise.all() for parallel
- Avoid fire-and-forget promises

## Dependencies
- Add to package.json only
- Document why new dependency
- Keep count reasonable
- Use peer dependencies when appropriate

## Review Checklist
- [ ] Passes linter
- [ ] 80%+ test coverage
- [ ] No console.log() in production
- [ ] Error handling in place
- [ ] Performance acceptable
- [ ] Documentation updated
- [ ] No breaking changes without discussion
```

---

## 8. Быстрый чекlistый для team onboarding

```markdown
# New Developer Onboarding Checklist

## Day 1: Setup
- [ ] Clone repository
- [ ] Follow setup in `@docs/onboarding/setup.md`
- [ ] Verify `claude /init` runs without errors
- [ ] Read this file: `@.claude/CLAUDE.md`

## Day 2: Understand Standards
- [ ] Read `@.claude/standards/architecture.md` (30 min)
- [ ] Read `@.claude/standards/coding-standards.md` (20 min)
- [ ] Read `@.claude/standards/testing-guidelines.md` (20 min)
- [ ] Skim `@docs/architecture/system-overview.md` (30 min)

## Day 3: First Task
- [ ] Pick a "good first issue" from GitHub
- [ ] Use relevant Skill: \`claude [skill-name] [issue]\`
- [ ] Follow patterns from `@.claude/standards/`
- [ ] Submit PR for review
- [ ] Incorporate feedback

## Week 1: Deeper Learning
- [ ] Pair with senior dev (2-3 hours)
- [ ] Review 3 existing PRs to learn patterns
- [ ] Complete 2-3 small tasks
- [ ] Ask questions in #engineering channel
- [ ] Update team if docs are unclear

## Week 2: Independence
- [ ] Complete first medium task independently
- [ ] Understand CI/CD pipeline (see `@.claude/standards/deployment.md`)
- [ ] Know how to escalate production issues
- [ ] Read incident response playbook: `@.claude/team/incident-response.md`

## Ongoing
- [ ] Weekly: Sync with team on blockers
- [ ] Monthly: Review own code for improvements
- [ ] Quarterly: Help review others' onboarding
- [ ] Always: Ask for help when unsure

## Key People
- **Architecture Q's**: [Name]
- **DevOps Q's**: [Name]
- **Product Q's**: [Name]
- **General Q's**: [Slack Channel]

## Common Commands to Know
\`\`\`bash
claude dev              # Start developing
claude test             # Run tests
claude build            # Build production
npm run lint --fix      # Fix linting issues
git log --oneline       # See recent commits
\`\`\`

## Important Links
- GitHub Issues: [Link]
- Slack: [Link]
- Wiki: [Link]
- Architecture Decisions: [Link]
- Runbooks: [Link]
```

---

## 9. Шаблон Deployment Standard

```markdown
# Deployment Standards

## Deployment Environments

### Development
- Deployed from: main branch
- Auto-deploy on merge
- Retention: 30 days logs

### Staging
- Deployed from: release/* branches
- Manual trigger via:
  \`claude deploy --staging\`
- QA testing environment

### Production
- Deployed from: tags v*.*.*
- Manual approval required
- Zero-downtime deployment
- Automatic rollback on failure

## Deployment Checklist
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Database migrations tested
- [ ] Environment variables configured
- [ ] Feature flags set correctly
- [ ] Monitoring alerts working
- [ ] Rollback plan documented

## Deployment Process

### 1. Pre-deployment
\`\`\`bash
# Create release
git tag v1.2.3
git push --tags

# Verify deployment
claude deploy --staging --dry-run
\`\`\`

### 2. Deploy to Staging
\`\`\`bash
claude deploy --staging
# Wait for health checks
# Run smoke tests
# Test critical flows
\`\`\`

### 3. Approval & Production Deploy
\`\`\`bash
# After staging sign-off:
claude deploy --production
\`\`\`

### 4. Post-deployment
- Monitor error rates
- Check performance metrics
- Verify all features working
- Notify stakeholders

## Rollback Procedure

If issues detected:
\`\`\`bash
# Check logs
claude logs --tail 100 --production

# Rollback to previous version
claude rollback v1.2.2 --production

# Notify team
#incident-response Slack channel
\`\`\`

## Database Migrations
- Must be reversible
- Test on staging first
- No data loss
- Can run in parallel with deploy

## Monitoring During Deploy
- Error rate: < 0.1%
- Response time: < 200ms p99
- CPU usage: < 70%
- Memory usage: < 80%

## Communication
1. Announce deployment start
2. Deploy to staging
3. Deploy to production
4. Monitor for 30 min
5. Announce deployment complete
```

---

## 10. GitHub Workflow для синхронизации standards

```yaml
# .github/workflows/sync-standards.yaml

name: Sync Claude Standards

on:
  push:
    paths:
      - '.claude/standards/**'
      - '.github/workflows/sync-standards.yaml'
    branches: [main]

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate standards
        run: |
          # Проверить что все standards скомпилированы
          for file in .claude/standards/*.md; do
            if [ ! -f "$file" ]; then
              echo "❌ Missing standard: $file"
              exit 1
            fi
          done
          echo "✅ All standards validated"
      
      - name: Sync to packages
        run: |
          # Опционально: синхронизировать standards в пакеты
          for pkg in packages/*/; do
            if [ -d "$pkg/.claude" ]; then
              echo "Updating $pkg"
              cp .claude/standards/* "$pkg/.claude/standards/" || true
            fi
          done
      
      - name: Create PR if changed
        uses: peter-evans/create-pull-request@v4
        with:
          commit-message: 'chore: sync claude standards'
          title: 'Sync Claude standards to packages'
          body: 'Standards have been updated in root .claude/'
          branch: standards-sync/${{ github.ref }}
```

---

## Чит-лист команде при внедрении

### Week 1
- [ ] Create `.claude/` directory
- [ ] Write root CLAUDE.md
- [ ] Create settings.json
- [ ] Commit to git

### Week 2
- [ ] Create standards/ files
- [ ] Create skills/testing
- [ ] Create agents/code-review
- [ ] Present to team

### Week 3
- [ ] Team uses new structure
- [ ] Collect feedback
- [ ] Update based on feedback
- [ ] Document learnings

### Month 2
- [ ] Add more Skills
- [ ] Expand standards
- [ ] Integrate with CI/CD
- [ ] Monitor adoption

---

**Готово к использованию!** Копируйте нужные части в свой проект.

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

