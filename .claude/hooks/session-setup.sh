#!/bin/bash
# SessionStart Hook: Initialize Claude Code session
# Loads context, sets up environment

set -e

echo "## 📋 Shared Knowledge Base Session"
echo ""

# Show KB statistics
if [[ -f "tools/kb.py" ]] && command -v python &> /dev/null; then
  echo "### KB Statistics"
  python tools/kb.py stats 2>/dev/null || echo "  (Run 'python tools/kb.py index' first)"
  echo ""
fi

# Show recent commits
if git rev-parse --git-dir > /dev/null 2>&1; then
  echo "### Recent Activity"
  git log --oneline -5 2>/dev/null || echo "  (No git history)"
  echo ""
fi

# Show current branch
if git rev-parse --git-dir > /dev/null 2>&1; then
  BRANCH=$(git branch --show-current)
  echo "### Current Branch: $BRANCH"
  echo ""
fi

# Show pending changes
if git rev-parse --git-dir > /dev/null 2>&1; then
  if git status --porcelain | grep -q .; then
    echo "### ⚠️  Pending Changes"
    git status --short
    echo ""
  fi
fi

# Setup environment variables
if [ -n "$CLAUDE_ENV_FILE" ]; then
  # KB tools path
  echo 'export PATH="$PATH:./tools"' >> "$CLAUDE_ENV_FILE"

  # Python path if needed
  if command -v python &> /dev/null; then
    echo 'export PYTHONPATH="${PYTHONPATH}:./tools"' >> "$CLAUDE_ENV_FILE"
  fi
fi

echo "✅ Session initialized"
echo ""
echo "### Quick Commands"
echo "  Search:    python tools/kb.py search \"query\""
echo "  Validate:  python tools/kb.py validate"
echo "  Index:     python tools/kb.py index -v"
echo "  Stats:     python tools/kb.py stats"

exit 0
