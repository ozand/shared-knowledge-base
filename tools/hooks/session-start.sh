#!/bin/bash
#
# session-start.sh - Claude Code SessionStart Hook
#
# Purpose:
#   1. Update Shared KB submodule
#   2. Load project context into agent memory
#   3. Validate environment configuration
#
# Version: 5.1.0
#

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get project root directory
ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null)"

if [ -z "$ROOT_DIR" ]; then
    echo -e "${RED}❌ Error: Not in a git repository${NC}"
    exit 1
fi

# Define paths
KB_SHARED="$ROOT_DIR/.kb/shared"
CONTEXT_DIR="$ROOT_DIR/.kb/context"
PROJECT_YAML="$CONTEXT_DIR/PROJECT.yaml"
MEMORY_MD="$CONTEXT_DIR/MEMORY.md"

echo -e "${BLUE}🤖 KB System Initialization v5.1${NC}"
echo ""

# ============================================
# 1. Update Shared KB Submodule
# ============================================
echo -e "${BLUE}🔄 Step 1: Checking Shared KB updates...${NC}"

if [ -d "$KB_SHARED" ]; then
    # Try to update submodule (quiet mode)
    if git submodule update --remote --merge --quiet 2>/dev/null; then
        echo -e "${GREEN}   ✅ Shared KB is up to date${NC}"
    else
        echo -e "${YELLOW}   ⚠️  Could not update Shared KB${NC}"
        echo -e "${YELLOW}      (Check network or run: git submodule update --remote --merge)${NC}"
    fi
else
    echo -e "${YELLOW}   ⚠️  Shared KB submodule not found at .kb/shared${NC}"
    echo -e "${YELLOW}      Initialize with: git submodule add <repo-url> .kb/shared${NC}"
fi

echo ""

# ============================================
# 2. Load Project Context
# ============================================
echo -e "${BLUE}📥 Step 2: Loading Project Context...${NC}"

if [ -f "$PROJECT_YAML" ]; then
    echo -e "${GREEN}   ✅ PROJECT.yaml found${NC}"
    echo ""
    echo "=== PROJECT IDENTITY ==="
    cat "$PROJECT_YAML"
    echo ""
    echo "========================"
else
    echo -e "${YELLOW}   ⚠️  PROJECT.yaml not found${NC}"
    echo -e "${YELLOW}      Agent will run without specific project instructions${NC}"
    echo -e "${YELLOW}      Create: .kb/context/PROJECT.yaml${NC}"
fi

echo ""

if [ -f "$MEMORY_MD" ]; then
    echo -e "${GREEN}   ✅ MEMORY.md found${NC}"
    echo ""
    echo "=== PROJECT MEMORY ==="
    cat "$MEMORY_MD"
    echo ""
    echo "======================="
else
    echo -e "${YELLOW}   ℹ️  MEMORY.md not found (optional)${NC}"
fi

echo ""

# ============================================
# 3. Validate Environment Configuration
# ============================================
echo -e "${BLUE}🔐 Step 3: Validating Environment...${NC}"

# Check GITHUB_TOKEN
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}   ⚠️  GITHUB_TOKEN not set${NC}"
    echo -e "${YELLOW}      'kb_submit.py --target shared' will fail${NC}"
    echo -e "${YELLOW}      Set it: export GITHUB_TOKEN=ghp_your_token${NC}"
else
    echo -e "${GREEN}   ✅ GITHUB_TOKEN is set${NC}"
fi

# Check SHARED_KB_REPO
if [ -z "$SHARED_KB_REPO" ]; then
    echo -e "${YELLOW}   ℹ️  SHARED_KB_REPO not set (using default)${NC}"
else
    echo -e "${GREEN}   ✅ SHARED_KB_REPO: $SHARED_KB_REPO${NC}"
fi

echo ""

# ============================================
# 4. Display KB Statistics
# ============================================
echo -e "${BLUE}📊 Step 4: KB Statistics${NC}"

PROJECT_KB="$ROOT_DIR/.kb/project"

if [ -d "$PROJECT_KB" ]; then
    PROJECT_ENTRIES=$(find "$PROJECT_KB" -name "*.yaml" -not -name "_index*" 2>/dev/null | wc -l)
    echo -e "${GREEN}   ✅ Project KB: $PROJECT_ENTRIES entries${NC}"
else
    echo -e "${YELLOW}   ℹ️  Project KB: Not found at .kb/project${NC}"
fi

if [ -d "$KB_SHARED" ]; then
    # Search in domains/ subdirectory (v5.1 structure)
    SHARED_ENTRIES=$(find "$KB_SHARED/domains" -name "*.yaml" -not -name "_index*" 2>/dev/null | wc -l)
    echo -e "${GREEN}   ✅ Shared KB: $SHARED_ENTRIES entries${NC}"
fi

echo ""

# ============================================
# 5. Display Quick Reference
# ============================================
echo -e "${BLUE}📚 Quick Reference:${NC}"
echo "   Search:     python .kb/shared/tools/v5.1/kb_search.py \"<query>\""
echo "   Local:      python .kb/shared/tools/v5.1/kb_submit.py --target local --file <entry.yaml>"
echo "   Shared:     python .kb/shared/tools/v5.1/kb_submit.py --target shared --file <entry.yaml> --title \"<title>\""
echo ""

# ============================================
# 6. Ready
# ============================================
echo -e "${GREEN}🚀 Ready! Agent has full context.${NC}"
