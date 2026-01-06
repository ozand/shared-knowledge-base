#!/bin/bash
# Migration Script: Clean Directory Structure
# Moves files from cluttered root to organized structure
#
# Before: 21 .md files in root
# After: 7 .md files in root (67% reduction)

set -e  # Exit on error

echo "=========================================================================="
echo "  Shared Knowledge Base - Clean Structure Migration"
echo "=========================================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Backup and prepare
echo -e "${BLUE}Step 1: Creating backup branch...${NC}"
git checkout -b clean-structure-backup 2>/dev/null || git checkout clean-structure-backup
echo "✓ Working in backup branch: clean-structure-backup"
echo ""

# Step 2: Create directory structure
echo -e "${BLUE}Step 2: Creating directory structure...${NC}"
mkdir -p curator/metadata
mkdir -p for-claude-code
mkdir -p .archive
echo "✓ Created directories: curator/, curator/metadata/, for-claude-code/, .archive/"
echo ""

# Step 3: Move curator documentation
echo -e "${BLUE}Step 3: Moving curator documentation...${NC}"
mv CURATOR_DOCS_INDEX.md curator/INDEX.md && echo "  ✓ CURATOR_DOCS_INDEX.md → curator/INDEX.md"
mv README_CURATOR.md curator/README.md && echo "  ✓ README_CURATOR.md → curator/README.md"
mv AGENT.md curator/AGENT.md && echo "  ✓ AGENT.md → curator/AGENT.md"
mv SKILLS.md curator/SKILLS.md && echo "  ✓ SKILLS.md → curator/SKILLS.md"
mv WORKFLOWS.md curator/WORKFLOWS.md && echo "  ✓ WORKFLOWS.md → curator/WORKFLOWS.md"
mv QUALITY_STANDARDS.md curator/QUALITY_STANDARDS.md && echo "  ✓ QUALITY_STANDARDS.md → curator/QUALITY_STANDARDS.md"
mv PROMPTS.md curator/PROMPTS.md && echo "  ✓ PROMPTS.md → curator/PROMPTS.md"
mv DEPLOYMENT_GUIDE.md curator/DEPLOYMENT.md && echo "  ✓ DEPLOYMENT_GUIDE.md → curator/DEPLOYMENT.md"
echo ""

# Step 4: Move metadata documentation
echo -e "${BLUE}Step 4: Moving metadata documentation...${NC}"
mv METADATA_ARCHITECTURE.md curator/metadata/ARCHITECTURE.md && echo "  ✓ METADATA_ARCHITECTURE.md → curator/metadata/ARCHITECTURE.md"
mv METADATA_SKILLS.md curator/metadata/SKILLS.md && echo "  ✓ METADATA_SKILLS.md → curator/metadata/SKILLS.md"
mv METADATA_SUMMARY.md curator/metadata/SUMMARY.md && echo "  ✓ METADATA_SUMMARY.md → curator/metadata/SUMMARY.md"
mv IMPLEMENTATION_GUIDE.md curator/metadata/IMPLEMENTATION.md && echo "  ✓ IMPLEMENTATION_GUIDE.md → curator/metadata/IMPLEMENTATION.md"
mv PHASE3_SUMMARY.md curator/metadata/PHASE3.md && echo "  ✓ PHASE3_SUMMARY.md → curator/metadata/PHASE3.md"
echo ""

# Step 5: Move AI tool documentation
echo -e "${BLUE}Step 5: Moving AI tool documentation...${NC}"
mv FOR_CLAUDE_CODE.md for-claude-code/README.md && echo "  ✓ FOR_CLAUDE_CODE.md → for-claude-code/README.md"
mv CLAUDE.md for-claude-code/CLAUDE.md && echo "  ✓ CLAUDE.md → for-claude-code/CLAUDE.md"
echo ""

# Step 6: Handle project-specific files
echo -e "${BLUE}Step 6: Handling project-specific files...${NC}"
if [ -f "VPS_README.md" ]; then
    mv VPS_README.md vps/README.md && echo "  ✓ VPS_README.md → vps/README.md"
fi
if [ -f "MIGRATION_TO_HYBRID_RU.md" ]; then
    mv MIGRATION_TO_HYBRID_RU.md .archive/ && echo "  ✓ MIGRATION_TO_HYBRID_RU.md → .archive/ (legacy)"
fi
echo ""

# Step 7: Remove local files from git
echo -e "${BLUE}Step 7: Removing local files from git tracking...${NC}"
if git ls-files | grep -q ".kb-config-local.yaml"; then
    git rm --cached .kb-config-local.yaml && echo "  ✓ Removed .kb-config-local.yaml from git"
fi
if git ls-files | grep -q ".kb-config-local_meta.yaml"; then
    git rm --cached .kb-config-local_meta.yaml && echo "  ✓ Removed .kb-config-local_meta.yaml from git"
fi
echo ""

# Step 8: Show current state
echo -e "${BLUE}Step 8: Current root directory state...${NC}"
echo ""
echo "Markdown files in root:"
ls -1 *.md 2>/dev/null | wc -l | xargs echo "  Total:"
ls -1 *.md 2>/dev/null | sed 's/^/    - /'
echo ""
echo "Config files in root:"
ls -1 .kb*.{yaml,yml} 2>/dev/null | sed 's/^/    - /'
echo ""

# Step 9: Ask for confirmation
echo -e "${YELLOW}=========================================================================="
echo "  MIGRATION PREVIEW"
echo "==========================================================================${NC}"
echo ""
echo "Files moved:"
echo "  - Curator docs: 8 files → curator/"
echo "  - Metadata docs: 5 files → curator/metadata/"
echo "  - AI tool docs: 2 files → for-claude-code/"
echo "  - Project-specific: 1-2 files to proper locations"
echo "  - Local files: Removed from git tracking"
echo ""
echo -e "${GREEN}Expected result:${NC}"
echo "  - Root .md files: 21 → 7 (67% reduction)"
echo "  - Clean separation: users, curators, AI tools"
echo "  - No local files in git"
echo ""
echo -e "${YELLOW}Ready to commit? [y/N]${NC}"
read -r response

if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo -e "${RED}Migration cancelled. Changes are staged but not committed.${NC}"
    echo "To undo: git reset --hard HEAD"
    exit 1
fi

# Step 10: Commit changes
echo ""
echo -e "${BLUE}Step 10: Committing migration...${NC}"
git add .
git commit -m "Refactor: Implement clean directory structure

BREAKING CHANGE: Documentation reorganized

Directory structure changes:
- Move 8 curator docs to curator/
- Move 5 metadata docs to curator/metadata/
- Move 2 AI tool docs to for-claude-code/
- Move VPS_README.md to vps/
- Archive legacy docs to .archive/

Root directory cleanup:
- Markdown files: 21 → 7 (67% reduction)
- Local files removed from git (.kb-config-local.*)

Benefits:
- Clear separation: users vs curators vs AI tools
- Professional structure
- Easy navigation
- Clean git history

Migration guide:
- CURATOR_DOCS_INDEX.md → curator/INDEX.md
- README_CURATOR.md → curator/README.md
- AGENT.md → curator/AGENT.md
- SKILLS.md → curator/SKILLS.md
- WORKFLOWS.md → curator/WORKFLOWS.md
- QUALITY_STANDARDS.md → curator/QUALITY_STANDARDS.md
- PROMPTS.md → curator/PROMPTS.md
- DEPLOYMENT_GUIDE.md → curator/DEPLOYMENT.md
- METADATA_ARCHITECTURE.md → curator/metadata/ARCHITECTURE.md
- METADATA_SKILLS.md → curator/metadata/SKILLS.md
- METADATA_SUMMARY.md → curator/metadata/SUMMARY.md
- IMPLEMENTATION_GUIDE.md → curator/metadata/IMPLEMENTATION.md
- PHASE3_SUMMARY.md → curator/metadata/PHASE3.md
- FOR_CLAUDE_CODE.md → for-claude-code/README.md
- CLAUDE.md → for-claude-code/CLAUDE.md
- VPS_README.md → vps/README.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

echo ""
echo -e "${GREEN}✓ Migration committed successfully!${NC}"
echo ""

# Step 11: Show summary
echo "=========================================================================="
echo "  MIGRATION COMPLETE"
echo "=========================================================================="
echo ""
echo "Commit created in branch: clean-structure-backup"
echo ""
echo "Next steps:"
echo "  1. Review changes: git log -1 --stat"
echo "  2. Test documentation links"
echo "  3. If satisfied, merge to main:"
echo "     git checkout main"
echo "     git merge clean-structure-backup"
echo "     git push origin main"
echo ""
echo "  4. If problems, reset:"
echo "     git reset --hard main"
echo ""
echo -e "${GREEN}Root directory files (should be 7 .md):${NC}"
ls -1 *.md 2>/dev/null
echo ""
echo "=========================================================================="
