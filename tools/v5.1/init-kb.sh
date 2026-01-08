#!/bin/bash
#
# init-kb.sh - Initialize Project KB structure
#
# Creates the .kb/ directory structure for a consumer project
#
# Usage:
#   bash tools/v5.1/init-kb.sh
#
# Version: 5.1.0
#

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get project root directory
ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null)"

if [ -z "$ROOT_DIR" ]; then
    echo -e "${RED}❌ Error: Not in a git repository${NC}"
    exit 1
fi

echo -e "${BLUE}🚀 Initializing Project KB Structure${NC}"
echo ""

# Define paths
KB_DIR="$ROOT_DIR/.kb"
CONTEXT_DIR="$KB_DIR/context"
PROJECT_KB_DIR="$KB_DIR/project"
SHARED_KB_DIR="$KB_DIR/shared"

# ============================================
# 1. Create .kb/context/
# ============================================
echo -e "${BLUE}📁 Creating .kb/context/...${NC}"

mkdir -p "$CONTEXT_DIR"

if [ ! -f "$CONTEXT_DIR/PROJECT.yaml" ]; then
    cat > "$CONTEXT_DIR/PROJECT.yaml" << 'EOF'
# === Project Identity ===
meta:
  name: "My Project"
  id: "my-project"
  description: "Project description"
  type: "application"
  started: "2026-01-08"
  repository: "https://github.com/username/repo"

# === Sharing Criteria (MOST IMPORTANT!) ===
# This section controls agent behavior for knowledge submission
sharing_criteria:
  # Agents will submit to Shared KB if ANY of these conditions match
  universal_if:
    - "Solution applicable to any software project"
    - "Language or framework best practices"
    - "Open source library integration"
    - "DevOps or infrastructure patterns"

  # Agents will save to Project KB if ANY of these conditions match
  project_specific_if:
    - "Business logic or domain rules"
    - "Internal service URLs or names"
    - "Temporary workarounds or hotfixes"
    - "Environment-specific configuration"
    - "Integration secrets (use templates)"

# === Agent Instructions ===
# This section defines agent behavior and protocols
agent_instructions:
  feedback_loop:
    enabled: true
    mandatory: true
    description: "Agent must document every error solution and valuable pattern"
    triggers:
      - "Tool execution error (exit code != 0)"
      - "Test failure"
      - "Solution took > 2 attempts to discover"
      - "Non-obvious workaround or fix"
    output_format: "yaml"
    submission_required: true

  reflection_prompt: |
    When you encounter an error and successfully solve it, you MUST:

    1. ANALYZE: Answer these questions:
       - What was I trying to do?
       - What exact error occurred?
       - Root cause: Why did this happen?
       - How did I fix it?

    2. EXTRACT: Create YAML entry with:
       - Clear problem description
       - Complete solution code
       - Explanation of "why" it works
       - Appropriate category and severity

    3. ROUTE: Determine scope:
       - Secrets/business logic? → --target local
       - Universal pattern? → --target shared

    4. SUBMIT: Use kb_submit.py
       python .kb/shared/tools/v5.1/kb_submit.py \\
         --target <local|shared> \\
         --file <entry.yaml> \\
         --title "Descriptive title"

    NEVER skip this step. Every error solution is valuable knowledge.

  search_first:
    enabled: true
    description: "Always search KB before solving problems"
    command: "python .kb/shared/tools/v5.1/kb_search.py"

# === Technology Stack ===
stack:
  language: "Python"
  version: "3.11+"
  framework: "FastAPI"
  database: "PostgreSQL"
  testing: "pytest"
  deployment: "Docker"

  tools:
    - name: "FastAPI"
      version: "0.104+"
      purpose: "Web framework"
    - name: "pytest"
      version: "7.4+"
      purpose: "Testing"

# === Integration References ===
integrations:
  - name: "Shared Knowledge Base"
    type: "knowledge-base"
    docs: ".kb/shared/"
    url: "https://github.com/ozand/shared-knowledge-base"

# === Project Goals ===
goals:
  current: "Project goal description"
  priorities:
    - "Priority 1"
    - "Priority 2"

  upcoming:
    - "Upcoming feature 1"
    - "Upcoming feature 2"

# === Team Information ===
team:
  tech_lead: "Tech Lead Name"
  kb_curator: "tech-lead"

# === Development Workflow ===
workflow:
  git_branches:
    main: "main"
    develop: "develop"

  testing:
    framework: "pytest"
    coverage_threshold: 80

  code_review:
    required: true
    reviewers: 1

# === Important Paths ===
paths:
  src: "src/"
  tests: "tests/"
  docs: "docs/"

# === Known Issues ===
known_issues:
  - description: "Example issue"
    workaround: "Example workaround"
    status: "active"
EOF
    echo -e "${GREEN}   ✅ Created PROJECT.yaml${NC}"
else
    echo -e "${YELLOW}   ⚠️  PROJECT.yaml already exists${NC}"
fi

if [ ! -f "$CONTEXT_DIR/MEMORY.md" ]; then
    cat > "$CONTEXT_DIR/MEMORY.md" << 'EOF'
# Project Memory

_Last updated: 2026-01-08_

---

## Architecture Decisions

### Decision Title (YYYY-MM-DD)
**Decision:** Description of architectural decision
**Reason:**
- Reason 1
- Reason 2
**Impact:** Impact on the project

---

## Lessons Learned

### Category

**What we learned:**
- Lesson 1
- Lesson 2

**How to apply:**
- Application 1
- Application 2

---

## Known Issues

### Current Issues
- **Issue description** (YYYY-MM-DD)
  - **Status:** Active | Resolved | Workaround exists
  - **Plan:** Plan to resolve

---

## Onboarding Tips

### For New Contributors
1. **Read existing docs** - Start with README.md
2. **Setup environment** - Follow setup instructions
3. **Run tests** - Ensure everything works

### For New Agents
1. **Search KB first** - Use `kb_search.py "query"`
2. **Check sharing criteria** - Read PROJECT.yaml
3. **Follow conventions** - Code style, patterns

---

## Project Conventions

### Code Style
- **Language:** Python
- **Formatter:** black
- **Linter:** flake8
- **Type hints:** Required

### Git Workflow
- **Branch naming:** feature/description, fix/description
- **Commit messages:** Conventional Commits
- **PR review:** Required

---

_This file is automatically loaded by Claude Code via session-start.sh hook_
EOF
    echo -e "${GREEN}   ✅ Created MEMORY.md${NC}"
else
    echo -e "${YELLOW}   ⚠️  MEMORY.md already exists${NC}"
fi

echo ""

# ============================================
# 2. Create .kb/project/
# ============================================
echo -e "${BLUE}📁 Creating .kb/project/...${NC}"

mkdir -p "$PROJECT_KB_DIR"/{integrations,endpoints,decisions,lessons,pending}

echo -e "${GREEN}   ✅ Created .kb/project/ integrations/${NC}"
echo -e "${GREEN}   ✅ Created .kb/project/ endpoints/${NC}"
echo -e "${GREEN}   ✅ Created .kb/project/ decisions/${NC}"
echo -e "${GREEN}   ✅ Created .kb/project/ lessons/${NC}"
echo -e "${GREEN}   ✅ Created .kb/project/ pending/${NC}"

# Add README to explain structure
cat > "$PROJECT_KB_DIR/README.md" << 'EOF'
# Project Knowledge Base

This directory contains project-specific knowledge that should NOT be shared with the Shared KB.

## Directory Structure

### `integrations/`
Integration configurations and documentation:
- External service integrations
- API client configurations
- Webhook setups

### `endpoints/`
API endpoints documentation:
- Internal endpoints
- External endpoints used
- Rate limiting info

### `decisions/`
Architectural decisions:
- ADR (Architecture Decision Records)
- Technical choices
- Trade-off analysis

### `lessons/`
Lessons learned:
- Bugs and fixes
- Performance optimizations
- Refactoring insights

### `pending/`
Temporary storage:
- Draft knowledge entries
- Work-in-progress documentation
- Pending Shared KB submissions

## Access Rules

- **Agents:** Read/Write (direct commit)
- **Curator:** No access (project-private)
- **Version control:** Within project repository

## Important

⚠️ **Never commit secrets!** Use templates instead:
- ❌ `api_key: "sk_live_12345"`
- ✅ `api_key_template: "sk_live_{ENVIRONMENT}_PROJECT"`

⚠️ **Never share business logic!** Keep project-specific knowledge here.
EOF

echo ""

# ============================================
# 3. Check Shared KB Submodule
# ============================================
echo -e "${BLUE}📁 Checking Shared KB submodule...${NC}"

if [ -d "$SHARED_KB_DIR" ]; then
    echo -e "${GREEN}   ✅ Shared KB submodule exists${NC}"
else
    echo -e "${YELLOW}   ⚠️  Shared KB submodule not found${NC}"
    echo -e "${YELLOW}      Initialize with:${NC}"
    echo -e "${YELLOW}      git submodule add https://github.com/ozand/shared-knowledge-base .kb/shared${NC}"
fi

echo ""

# ============================================
# 4. Create .env.example
# ============================================
echo -e "${BLUE}📁 Creating .env.example...${NC}"

if [ ! -f "$ROOT_DIR/.env.example" ]; then
    cat > "$ROOT_DIR/.env.example" << 'EOF'
# GitHub Token for Shared KB Submissions
# Required for: kb_submit.py --target shared
# Get token from: https://github.com/settings/tokens
# Permissions: repo (for private repos) or public_repo (for public repos)
GITHUB_TOKEN=ghp_your_token_here

# Shared Knowledge Base Repository
# Default: ozand/shared-knowledge-base
# Only change if you're using a fork
SHARED_KB_REPO=ozand/shared-knowledge-base

# Debug Mode (optional)
# Set to 1 for verbose output
DEBUG=0
EOF
    echo -e "${GREEN}   ✅ Created .env.example${NC}"
    echo -e "${YELLOW}   ⚠️  Remember to create .env file with actual values${NC}"
else
    echo -e "${YELLOW}   ⚠️  .env.example already exists${NC}"
fi

echo ""

# ============================================
# 5. Install SessionStart Hook
# ============================================
echo -e "${BLUE}📁 Installing SessionStart hook...${NC}"

HOOKS_DIR="$ROOT_DIR/.claude/hooks"
HOOK_FILE="$HOOKS_DIR/session-start.sh"

if [ -f "$SHARED_KB_DIR/tools/v5.1/hooks/session-start.sh" ]; then
    mkdir -p "$HOOKS_DIR"
    cp "$SHARED_KB_DIR/tools/v5.1/hooks/session-start.sh" "$HOOK_FILE"
    chmod +x "$HOOK_FILE"
    echo -e "${GREEN}   ✅ Installed session-start.sh hook${NC}"
else
    echo -e "${YELLOW}   ⚠️  Could not install hook (Shared KB not found)${NC}"
fi

echo ""

# ============================================
# 6. Update .gitignore
# ============================================
echo -e "${BLUE}📁 Updating .gitignore...${NC}"

if ! grep -q "^\.env$" "$ROOT_DIR/.gitignore" 2>/dev/null; then
    echo "" >> "$ROOT_DIR/.gitignore"
    echo "# Knowledge Base" >> "$ROOT_DIR/.gitignore"
    echo ".env" >> "$ROOT_DIR/.gitignore"
    echo ".env.local" >> "$ROOT_DIR/.gitignore"
    echo -e "${GREEN}   ✅ Updated .gitignore${NC}"
else
    echo -e "${YELLOW}   ⚠️  .gitignore already configured${NC}"
fi

echo ""

# ============================================
# 7. Summary
# ============================================
echo -e "${GREEN}✅ Project KB initialization complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "   1. Review and customize .kb/context/PROJECT.yaml"
echo "   2. Create .env file: cp .env.example .env"
echo "   3. Add GITHUB_TOKEN to .env"
echo "   4. Commit to git:"
echo "      git add .kb/ .env.example .claude/hooks/session-start.sh"
echo "      git commit -m 'feat: Initialize Project KB structure'"
echo ""
echo -e "${BLUE}📚 Documentation:${NC}"
echo "   - Architecture: .kb/shared/ARD.md"
echo "   - Workflows: .kb/shared/docs/v5.1/WORKFLOWS.md"
echo "   - Context Schema: .kb/shared/docs/v5.1/CONTEXT_SCHEMA.md"
echo ""
