# Claude Code CLAUDE.md: Complete Project Memory Guide
## Best Practices, Architecture, and Advanced Patterns

---

## Table of Contents

1. [Fundamental Concepts](#fundamental-concepts)
2. [Hierarchical Memory Architecture](#hierarchical-memory-architecture)
3. [Structuring CLAUDE.md](#structuring-claudemd)
4. [WHAT, WHY, HOW Framework](#what-why-how-framework)
5. [Progressive Disclosure Pattern](#progressive-disclosure-pattern)
6. [Structural Patterns](#structural-patterns)
7. [Anti-patterns & Common Mistakes](#anti-patterns--common-mistakes)
8. [Context Optimization Strategies](#context-optimization-strategies)
9. [Team & Enterprise Patterns](#team--enterprise-patterns)
10. [Integration with Other Practices](#integration-with-other-practices)
11. [Migration and Evolution](#migration-and-evolution)
12. [Real-World Examples](#real-world-examples)

---

## Fundamental Concepts

### What is CLAUDE.md?

**CLAUDE.md** is a special Markdown file containing **persistent project memory** for Claude Code.

```
KEY PRINCIPLE:
CLAUDE.md = Cheat sheet for Claude about your project
Automatically loaded at the start of each session
= Solves the "Tell me about the project" problem in every session
```

### Why is CLAUDE.md Important?

**WITHOUT CLAUDE.md:**
- Every session → need to explain project context
- Tokens wasted on re-explanation
- Inconsistent behavior (Claude forgets details)
- Friction in workflow

**WITH CLAUDE.md:**
- Context loaded automatically
- Consistent behavior (set once, always applies)
- Tokens saved (context already loaded)
- Smooth workflow

### Where Does CLAUDE.md Live?

```
Hierarchy (priority from bottom to top):

┌─ Enterprise-level
│  /etc/claude-code/CLAUDE.md (or equivalent)
│  ↑ All developers in org
│
├─ Team-level
│  ~/.claude/CLAUDE.md
│  ↑ All projects of this user
│
└─ Project-level
   ./CLAUDE.md (in repo root)
   ↑ Only this project

Claude reads ALL applicable files in hierarchy
More specific files override general ones
```

### When Does Claude Read CLAUDE.md?

```
TIMING:

Session Start:
  1. Claude starts
  2. Reads all CLAUDE.md files in hierarchy
  3. Loads context
  4. Uses in conversation

Between Turns:
  • CLAUDE.md is NOT reloaded between turns
  • But can be overridden in conversation

After /compact:
  • Context is compressed
  • CLAUDE.md remains active
```

---

## Hierarchical Memory Architecture

### 4 Memory Levels

```
┌──────────────────────────────────────────────┐
│     CLAUDE.md Hierarchy (Priority Order)    │
└──────────────────────────────────────────────┘

LEVEL 1: ENTERPRISE (Highest Priority)
  /etc/claude-code/CLAUDE.md
  - Company-wide policies
  - Security guidelines
  - Compliance requirements
  - Global coding standards
  Shared by: All developers in organization

LEVEL 2: USER (Project-independent)
  ~/.claude/CLAUDE.md
  - Personal preferences
  - Favorite tools & libraries
  - Personal workflow patterns
  - Credentials & APIs
  Shared by: All projects of this user

LEVEL 3: PROJECT (Project-specific)
  ./CLAUDE.md (repo root)
  - Architecture overview
  - Team standards
  - Project-specific patterns
  - Build/test commands
  Shared by: All team members on this project

LEVEL 4: LOCAL (Deprecated but supported)
  .claude/CLAUDE.md or src/CLAUDE.md
  - Directory-specific context
  - Nested overrides
  - Local customizations
  Used by: Specific directories when Claude works there

═══════════════════════════════════════════════════════

RULE: More specific files override general ones
      Nested CLAUDE.md > Project CLAUDE.md > User > Enterprise
```

### Example: How Loading Works

```
Project: ~/projects/myapp/

Files present:
  /etc/claude-code/CLAUDE.md           ← Enterprise
  ~/.claude/CLAUDE.md                  ← User
  ~/projects/myapp/CLAUDE.md           ← Project
  ~/projects/myapp/src/CLAUDE.md       ← Local

Claude reads (in order):
  1. Enterprise CLAUDE.md (company policies)
  2. User CLAUDE.md (personal preferences) — overrides enterprise
  3. Project CLAUDE.md (team standards) — overrides user
  4. Local CLAUDE.md (directory context) — overrides project

If running in src/:
  Also loads ~/projects/myapp/src/CLAUDE.md
  = Most specific file

RESULT:
  Merged context with project-level > user-level > enterprise-level
```

---

## Structuring CLAUDE.md

### Basic Structure

```markdown
# Project Name

## Quick Overview
One-paragraph summary of what this project does

## Key Files & Structure
Show important directories and key files

## Workflow
How to work on this project

## Important Rules
Must-follow guidelines

## Commands
Common commands you use

## Recent Decisions
Architecture decisions and why

## Questions?
How to get help
```

### Production-Ready Template

See the full file for comprehensive production-ready template with WHAT, WHY, HOW framework.

---

## WHAT, WHY, HOW Framework

### Core Concept

Structure CLAUDE.md around three questions:

```
WHAT:   Describe the project technically
        - Architecture, stack, structure
        - "Here's what we're building"

WHY:    Explain the reasoning
        - Goals, principles, decisions
        - "Why did we choose this"

HOW:    Provide instructions for working
        - Workflow, standards, commands
        - "Here's how to work here"
```

---

## Progressive Disclosure Pattern

### What is Progressive Disclosure?

**Progressive Disclosure** = Show what exists and how to access it, let Claude fetch details on demand.

```
Instead of:
  ❌ Dumping entire 500-line CLAUDE.md

Do:
  ✅ Show overview + references to detailed docs
  ✅ Let Claude fetch what's needed
```

### Two-Layer Structure

```
Layer 1: CLAUDE.md (Concise)
├─ Core principles (must follow)
├─ Pointers to where details live
├─ Quick reference commands
└─ Recent decisions with links

Layer 2: Detailed References
├─ ~/.claude/references/architecture.md
├─ ~/.claude/references/api-standards.md
├─ ~/.claude/references/deployment.md
└─ ~/.claude/references/troubleshooting.md
```

---

## Integration with Other Practices

### CLAUDE.md + SKILLS

CLAUDE.md establishes requirements, SKILL.md implements them.

### CLAUDE.md + HOOKS

CLAUDE.md = intent & rules, HOOKS = automated enforcement.

### CLAUDE.md + AGENTS

CLAUDE.md frames entire agent team with project context.

### CLAUDE.md + Commands

Commands use CLAUDE.md context, CLAUDE.md references commands.

---

**Version**: 1.0  
**Date**: January 7, 2026  
**Status**: Production-ready comprehensive guide  
**Size**: 8,000+ words, 12 sections, 50+ examples

**Note:** This is a condensed English version of the original Russian guide. For the complete detailed version with all examples, templates, and anti-patterns, refer to the full guide structure above.

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

