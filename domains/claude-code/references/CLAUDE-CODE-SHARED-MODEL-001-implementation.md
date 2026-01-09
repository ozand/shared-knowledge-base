# Claude Code Shared Model - Implementation Guide

**Extracted from:** claude-code-shared-model.yaml
**Pattern ID:** CLAUDE-CODE-SHARED-MODEL-001

## Phase 1: Foundation Setup

**Title:** Setup Root Configuration
**Effort:** 2-4 hours

### Step 1: Create root .claude/ structure

**Files to create:**

#### .claude/CLAUDE.md
- **Purpose:** Navigation hub
- **Size:** ~300 lines

#### .claude/settings.json
- **Purpose:** Feature enablement
- **Content:**
```json
{
  "skills.enabled": ["testing", "refactoring"],
  "agents.enabled": ["code-review"]
}
```

### Step 2: Create standards directory

**Files:**
- `.claude/standards/architecture.md`
- `.claude/standards/coding-standards.md`
- `.claude/standards/testing-guidelines.md`
- `.claude/standards/api-standards.md`
- `.claude/standards/deployment.md`

### Step 3: Create CLAUDE.md with references

**Template:**
```markdown
# Project Knowledge

## Architecture
See @standards/architecture.md

## Coding Standards
See @standards/coding-standards.md

## Testing
See @standards/testing-guidelines.md
Use /testing skill to generate tests
```

### Step 4: Commit to git

```bash
git add .claude/
git commit -m "Add shared Claude Code configuration"
```

## Phase 2: Create Reusable SKILLS

**Title:** Create Reusable SKILLS
**Effort:** 4-8 hours

### Step 1: Create testing skill

**Structure:**
```
.claude/skills/testing/
├── SKILL.md          (Skill definition)
├── templates/        (Test templates)
└── patterns.md       (Test patterns)
```

### Step 2: Document in SKILL.md

**Sections:**
- What this skill does
- When to use it
- Examples
- Patterns to follow

### Step 3: Enable in settings.json

**Config:**
```json
{
  "skills.enabled": ["testing"]
}
```

## Phase 3: Add AGENTS for Automation

**Title:** Add AGENTS for Automation
**Effort:** 1-2 days

### Step 1: Create code-review agent

**File:** `.claude/agents/code-review-agent.md`
**Purpose:** Automate PR review

**Workflow:**
1. **Trigger:** GitHub webhook on PR
2. **Actions:**
   - Load standards from .claude/standards/
   - Review PR for violations
   - Post comments with @standard references
   - Link specific rules violated

### Step 2: Start simple, iterate

**Advice:**
- Begin with 1-2 specific agents
- Test thoroughly
- Monitor feedback
- Improve iteratively

## Team Size Scaling Guide

### Team: 1-3 Developers

**Structure:** Single repo, simple .claude/
**Setup:** 2-4 hours
**Maintenance:** 1 hour/month

**Config:**
```
.claude/
├── CLAUDE.md (200 lines)
├── standards/ (all-in-one file)
└── skills/ (1-2 basic)
```

### Team: 3-10 Developers

**Structure:** Monorepo with shared root
**Setup:** 1-2 days
**Maintenance:** 4-6 hours/month

**Config:**
```
.claude/ (root)
├── CLAUDE.md (300 lines)
├── standards/ (split by domain)
├── skills/ (testing, refactoring, docs)
├── agents/ (code review)
└── team/ (workflows, faq)

packages/*/.claude/ (specific)
```

### Team: 10-30 Developers

**Structure:** Monorepo + services
**Setup:** 1 week
**Maintenance:** 8-12 hours/month

**Config:**
```
.claude/ (core)
├── CLAUDE.md (250 lines - lean!)
├── standards/ (comprehensive)
├── skills/ (10+ skills)
├── agents/ (automation everywhere)
├── references/ (APIs, schemas)
└── team/ (comprehensive docs)
```

### Team: 30-100 Developers

**Structure:** Multi-service platform with MCP
**Setup:** 2 weeks + MCP implementation
**Maintenance:** 20-30 hours/month

**Config:**
```
.claude/ (minimal - 150 lines!)
├── CLAUDE.md (navigation only)
├── standards/ (strict requirements)
├── shared-skills/ (company-wide)
├── shared-agents/ (automation)
└── references/ (via MCP)

domain-specific .claude/ (FE, BE, platform)
knowledge-base/ (MCP-powered)
```

**Insight:**
> Root CLAUDE.md gets SMALLER as team grows!
> Standards live in separate files
> MCP provides dynamic context loading
> Result: No token waste, infinite scale
