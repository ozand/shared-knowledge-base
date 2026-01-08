#!/bin/bash
#
# migrate-to-v5.1.sh - Automated migration from v4.0 to v5.1
#
# Usage:
#   cd /path/to/your/project
#   bash .kb/shared/tools/v5.1/migrate-to-v5.1.sh
#
# Version: 5.1.0
# Last Updated: 2026-01-08

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root (detect automatically)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

# Paths
KB_SHARED="$PROJECT_ROOT/.kb/shared"
KB_CONTEXT="$PROJECT_ROOT/.kb/context"
KB_PROJECT="$PROJECT_ROOT/.kb/project"
CLAUDE_HOOKS="$PROJECT_ROOT/.claude/hooks"
EXAMPLES="$KB_SHARED/examples/v5.1"

# Backup timestamp
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$PROJECT_ROOT/.kb.backup.$BACKUP_DATE"

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Shared Knowledge Base v5.1 Migration Tool           ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Project Root:${NC} $PROJECT_ROOT"
echo -e "${BLUE}Backup Date:${NC} $BACKUP_DATE"
echo ""

# ============================================
# Pre-flight Checks
# ============================================
echo -e "${BLUE}[1/7] Pre-flight Checks${NC}"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Warning: Not in a git repository${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}❌ Migration cancelled${NC}"
        exit 1
    fi
fi

# Check if .kb/shared exists
if [ ! -d "$KB_SHARED" ]; then
    echo -e "${RED}❌ Error: .kb/shared directory not found${NC}"
    echo -e "${YELLOW}   Are you in the correct project directory?${NC}"
    exit 1
fi

echo -e "${GREEN}   ✅ In valid project directory${NC}"

# Check if v5.1 tools exist
if [ ! -d "$KB_SHARED/tools/v5.1" ]; then
    echo -e "${YELLOW}⚠️  v5.1 tools not found. Updating Shared KB...${NC}"
    cd "$KB_SHARED"
    git pull origin main
    cd "$PROJECT_ROOT"

    if [ ! -d "$KB_SHARED/tools/v5.1" ]; then
        echo -e "${RED}❌ Error: v5.1 tools still not found after update${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}   ✅ v5.1 tools available${NC}"

# Check Python
if ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Error: Python not found${NC}"
    exit 1
fi

echo -e "${GREEN}   ✅ Python available${NC}"

# Check PyGithub
if ! python -c "import github" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  PyGithub not installed. Installing...${NC}"
    pip install PyGithub
fi

echo -e "${GREEN}   ✅ PyGithub installed${NC}"
echo ""

# ============================================
# Backup Existing Files
# ============================================
echo -e "${BLUE}[2/7] Creating Backup${NC}"
echo ""

if [ -d "$PROJECT_ROOT/.kb" ]; then
    echo -e "${YELLOW}   Backing up .kb/ to $BACKUP_DIR${NC}"
    cp -r "$PROJECT_ROOT/.kb" "$BACKUP_DIR"
    echo -e "${GREEN}   ✅ Backup created${NC}"
else
    echo -e "${YELLOW}   ℹ️  No existing .kb/ directory (fresh installation)${NC}"
fi

echo ""

# ============================================
# Create Directory Structure
# ============================================
echo -e "${BLUE}[3/7] Creating Directory Structure${NC}"
echo ""

mkdir -p "$KB_CONTEXT"
mkdir -p "$KB_PROJECT"/{integrations,endpoints,decisions,lessons,pending}
mkdir -p "$CLAUDE_HOOKS"

echo -e "${GREEN}   ✅ Created .kb/context/${NC}"
echo -e "${GREEN}   ✅ Created .kb/project/ (with subdirectories)${NC}"
echo -e "${GREEN}   ✅ Created .claude/hooks/${NC}"
echo ""

# ============================================
# Copy Templates
# ============================================
echo -e "${BLUE}[4/7] Installing Templates${NC}"
echo ""

# PROJECT.yaml
if [ ! -f "$KB_CONTEXT/PROJECT.yaml" ]; then
    if [ -f "$EXAMPLES/PROJECT.yaml.example" ]; then
        cp "$EXAMPLES/PROJECT.yaml.example" "$KB_CONTEXT/PROJECT.yaml"
        echo -e "${GREEN}   ✅ Created .kb/context/PROJECT.yaml${NC}"
        echo -e "${YELLOW}      ⚠️  Edit this file with your project details!${NC}"
    else
        echo -e "${RED}   ❌ PROJECT.yaml.example not found${NC}"
    fi
else
    echo -e "${YELLOW}   ℹ️  PROJECT.yaml already exists, skipping${NC}"
fi

# MEMORY.md
if [ ! -f "$KB_CONTEXT/MEMORY.md" ]; then
    if [ -f "$EXAMPLES/MEMORY.md.example" ]; then
        cp "$EXAMPLES/MEMORY.md.example" "$KB_CONTEXT/MEMORY.md"
        echo -e "${GREEN}   ✅ Created .kb/context/MEMORY.md${NC}"
        echo -e "${YELLOW}      ⚠️  Edit this file with your project knowledge!${NC}"
    else
        echo -e "${YELLOW}   ℹ️  MEMORY.md.example not found (optional)${NC}"
    fi
else
    echo -e "${YELLOW}   ℹ️  MEMORY.md already exists, skipping${NC}"
fi

# .env.example
if [ ! -f "$PROJECT_ROOT/.env.example" ]; then
    if [ -f "$EXAMPLES/.env.example" ]; then
        cp "$EXAMPLES/.env.example" "$PROJECT_ROOT/.env.example"
        echo -e "${GREEN}   ✅ Created .env.example${NC}"
    fi
fi

# .env (if doesn't exist)
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    if [ -f "$EXAMPLES/.env.example" ]; then
        cp "$EXAMPLES/.env.example" "$PROJECT_ROOT/.env"
        echo -e "${GREEN}   ✅ Created .env${NC}"
        echo -e "${YELLOW}      ⚠️  Edit .env and add your GITHUB_TOKEN!${NC}"
    fi
else
    echo -e "${YELLOW}   ℹ️  .env already exists, skipping${NC}"
fi

echo ""

# ============================================
# Install SessionStart Hook
# ============================================
echo -e "${BLUE}[5/7] Installing SessionStart Hook${NC}"
echo ""

HOOK_SOURCE="$KB_SHARED/tools/v5.1/hooks/session-start.sh"
HOOK_DEST="$CLAUDE_HOOKS/session-start.sh"

if [ -f "$HOOK_SOURCE" ]; then
    cp "$HOOK_SOURCE" "$HOOK_DEST"
    chmod +x "$HOOK_DEST"
    echo -e "${GREEN}   ✅ Installed .claude/hooks/session-start.sh${NC}"
else
    echo -e "${RED}   ❌ session-start.sh not found at $HOOK_SOURCE${NC}"
fi

echo ""

# ============================================
# Verification Checks
# ============================================
echo -e "${BLUE}[6/7] Running Verification Checks${NC}"
echo ""

# Check directory structure
echo -e "   Checking directories..."
if [ -d "$KB_CONTEXT" ] && [ -d "$KB_PROJECT" ] && [ -d "$CLAUDE_HOOKS" ]; then
    echo -e "${GREEN}   ✅ Directory structure OK${NC}"
else
    echo -e "${RED}   ❌ Directory structure incomplete${NC}"
fi

# Check configuration files
echo -e "   Checking configuration files..."
if [ -f "$KB_CONTEXT/PROJECT.yaml" ]; then
    if python -c "import yaml; yaml.safe_load(open('$KB_CONTEXT/PROJECT.yaml'))" 2>/dev/null; then
        echo -e "${GREEN}   ✅ PROJECT.yaml valid${NC}"
    else
        echo -e "${YELLOW}   ⚠️  PROJECT.yaml has syntax errors${NC}"
    fi
else
    echo -e "${YELLOW}   ⚠️  PROJECT.yaml not found${NC}"
fi

# Check .env
if [ -f "$PROJECT_ROOT/.env" ]; then
    if grep -q "GITHUB_TOKEN=" "$PROJECT_ROOT/.env"; then
        # Check if token is set (not just placeholder)
        if grep "GITHUB_TOKEN=ghp_" "$PROJECT_ROOT/.env" > /dev/null; then
            echo -e "${GREEN}   ✅ GITHUB_TOKEN configured${NC}"
        else
            echo -e "${YELLOW}   ⚠️  GITHUB_TOKEN needs to be set in .env${NC}"
        fi
    else
        echo -e "${YELLOW}   ⚠️  GITHUB_TOKEN not found in .env${NC}"
    fi
else
    echo -e "${YELLOW}   ⚠️  .env file not found${NC}"
fi

# Test v5.1 tools
echo -e "   Testing v5.1 tools..."
if python "$KB_SHARED/tools/v5.1/kb_search.py" --stats > /dev/null 2>&1; then
    echo -e "${GREEN}   ✅ kb_search.py works${NC}"
else
    echo -e "${YELLOW}   ⚠️  kb_search.py has issues${NC}"
fi

echo ""

# ============================================
# Summary and Next Steps
# ============================================
echo -e "${BLUE}[7/7] Migration Complete!${NC}"
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  ✅ MIGRATION SUCCESSFUL                 ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}What's Next?${NC}"
echo ""
echo -e "1. ${YELLOW}Edit .kb/context/PROJECT.yaml${NC}"
echo -e "   - Set your project name and ID"
echo -e "   - Configure sharing_criteria"
echo -e "   - Document your tech stack"
echo ""
echo -e "2. ${YELLOW}Edit .env and add your GITHUB_TOKEN${NC}"
echo -e "   - Get token from: https://github.com/settings/tokens"
echo -e "   - Required for 'shared' submissions"
echo ""
echo -e "3. ${YELLOW}Edit .kb/context/MEMORY.md (optional)${NC}"
echo -e "   - Document architectural decisions"
echo -e "   - Add lessons learned"
echo -e "   - Include onboarding tips"
echo ""
echo -e "4. ${YELLOW}Test the new tools${NC}"
echo -e "   python .kb/shared/tools/v5.1/kb_search.py \"docker\""
echo -e "   bash .claude/hooks/session-start.sh"
echo ""
echo -e "5. ${YELLOW}Commit changes to git${NC}"
echo -e "   git add .kb/ .claude/hooks/ .env.example"
echo -e "   git commit -m \"Migrate to KB v5.1\""
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo -e "  - Quick Start:  docs/v5.1/README.md"
echo -e "  - Full Guide:   docs/v5.1/MIGRATION-GUIDE.md"
echo -e "  - Architecture: docs/v5.1/ARD.md"
echo ""
echo -e "${BLUE}Backup Location:${NC}"
echo -e "  $BACKUP_DIR"
echo ""
echo -e "${BLUE}Rollback (if needed):${NC}"
echo -e "  rm -rf .kb/context .kb/project .claude/hooks/session-start.sh"
echo -e "  cp -r $BACKUP_DIR/* .kb/"
echo ""

# Ask if user wants to test hook now
read -p "Test SessionStart hook now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${BLUE}Testing SessionStart Hook...${NC}"
    bash "$CLAUDE_HOOKS/session-start.sh"
fi

echo ""
echo -e "${GREEN}🚀 Ready to use KB v5.1!${NC}"
