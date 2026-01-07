#!/bin/bash

# Shared KB Update Checker
# This script checks if .kb/shared submodule needs updating
# Usage: Add to .claude/hooks/session-setup.sh

set -e

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in a project with Shared KB submodule
if [ ! -d ".kb/shared" ]; then
    # Silent exit if not using Shared KB
    exit 0
fi

if [ ! -d ".kb/shared/.git" ]; then
    echo -e "${YELLOW}⚠️  .kb/shared/ exists but is not a git submodule${NC}"
    echo "   Initialize with: git submodule add https://github.com/ozand/shared-knowledge-base.git .kb/shared"
    exit 0
fi

echo -e "${BLUE}📦 Checking Shared KB updates...${NC}"

# Navigate to submodule
cd .kb/shared

# Fetch latest changes
git fetch origin > /dev/null 2>&1

# Get current version
CURRENT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
CURRENT_COMMIT=$(git rev-parse HEAD)

# Get latest version
LATEST_VERSION=$(git tag -l | sort -V | tail -n1)
LATEST_COMMIT=$(git rev-parse origin/main)

# Check if we're on main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${YELLOW}⚠️  .kb/shared/ is on branch '$CURRENT_BRANCH' instead of 'main'${NC}"
    echo -e "   Fix: ${GREEN}git checkout main${NC}"
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${RED}🚨 CRITICAL: .kb/shared/ has uncommitted changes!${NC}"
    echo -e "   This should NEVER happen - .kb/shared/ must be read-only"
    echo ""
    echo "   Status:"
    git status --short
    echo ""
    echo -e "   To fix: ${YELLOW}git reset --hard HEAD && git checkout main${NC}"
    echo -e "   Then: ${YELLOW}git pull origin main${NC}"
    cd ../..
    exit 1
fi

# Check if updates are available
if [ "$CURRENT_COMMIT" != "$LATEST_COMMIT" ]; then
    echo -e "${YELLOW}⚠️  Shared KB update available!${NC}"
    echo -e "   Current: ${BLUE}$CURRENT_VERSION${NC} ($CURRENT_COMMIT)"
    echo -e "   Latest:  ${GREEN}$LATEST_VERSION${NC} ($LATEST_COMMIT)"
    echo ""
    echo -e "📝 Recent changes:"
    git log --oneline HEAD..origin/main | head -n5 | sed 's/^/   /'
    echo ""
    echo -e "To update:"
    echo -e "   ${GREEN}cd .kb/shared && git pull origin main && cd ../..${NC}"
    echo -e "   ${GREEN}python tools/kb.py index --force -v${NC}"
    echo ""
    echo -e "Read update instructions: ${BLUE}@for-projects/UPDATE-SHARED-KB.md${NC}"
else
    echo -e "${GREEN}✅ Shared KB is up to date (${CURRENT_VERSION})${NC}"
fi

# Check notification file
NOTIFICATION_FILE=".kb-version-notification.md"
if [ -f "$NOTIFICATION_FILE" ]; then
    echo ""
    echo -e "${BLUE}📖 Version notification available:${NC}"
    echo -e "   ${BLUE}@.kb/shared/.kb-version-notification.md${NC}"
fi

cd ../..
