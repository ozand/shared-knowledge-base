#!/bin/bash
# setup-shared-kb-sparse.sh
#
# Setup Shared KB as submodule with sparse checkout
# This ensures only Project Agent content is loaded, excluding Curator files
#
# Usage:
#   cd /path/to/your/project
#   bash /path/to/shared-knowledge-base/scripts/setup-shared-kb-sparse.sh

set -e

echo "🔧 Setting up Shared KB with sparse checkout..."
echo ""

# Configuration
SHARED_KB_URL="https://github.com/ozand/shared-knowledge-base.git"
SHARED_KB_DIR="docs/knowledge-base/shared"

# Check if already exists
if [ -d "$SHARED_KB_DIR/.git" ]; then
    echo "⚠️  Shared KB already exists at $SHARED_KB_DIR"
    echo "   Remove it first if you want to re-setup:"
    echo "   git submodule deinit -f $SHARED_KB_DIR"
    echo "   rm -rf $SHARED_KB_DIR"
    echo "   git rm -f $SHARED_KB_DIR"
    exit 1
fi

# Create parent directory
echo "📁 Creating directory structure..."
mkdir -p "$(dirname "$SHARED_KB_DIR")"

# Add submodule
echo "📦 Adding submodule..."
git submodule add "$SHARED_KB_URL" "$SHARED_KB_DIR"

# Enable sparse checkout
echo "✂️  Enabling sparse checkout..."
cd "$SHARED_KB_DIR"
git config core.sparseCheckout true

# Create sparse-checkout file
echo "📝 Creating sparse-checkout configuration..."
cat > .git/info/sparse-checkout <<'SPARSE_EOF'
# Core documentation
README.md
GUIDE.md
QUICKSTART.md
README_INTEGRATION.md

# Agent guides
AGENT_INTEGRATION_GUIDE.md
AGENT_AUTOCONFIG_GUIDE.md
ROLE_SEPARATION_GUIDE.md
GITHUB_ATTRIBUTION_GUIDE.md

# Patterns (MAIN CONTENT)
universal/
python/
postgresql/
docker/
javascript/
vps/

# Tools
tools/
scripts/

# Base configuration
.kb-config.yaml
.gitignore.agents
SPARSE_EOF

# Pull only specified content
echo "⬇️  Pulling only specified content..."
git pull origin main

cd - > /dev/null

# Verify
echo ""
echo "✅ Setup complete!"
echo ""
echo "📊 What's loaded:"
echo "   ✅ Patterns (universal/, python/, postgresql/, docker/, javascript/)"
echo "   ✅ Documentation (README.md, GUIDE.md, agent guides)"
echo "   ✅ Tools (tools/kb.py, scripts/)"
echo ""
echo "🚫 What's EXCLUDED (not loaded):"
echo "   ❌ curator/ (Curator instructions)"
echo "   ❌ *_ANALYSIS.md (analysis documents)"
echo "   ❌ *_REPORT.md (Curator reports)"
echo "   ❌ CHAT_*.md (chat analysis)"
echo "   ❌ Generated files (.agent-config.local, _index*.yaml)"
echo ""
echo "📁 Location: $SHARED_KB_DIR"
echo ""
echo "💡 To update Shared KB:"
echo "   git submodule update --remote --merge $SHARED_KB_DIR"
echo ""
echo "💡 To check for updates:"
echo "   python $SHARED_KB_DIR/tools/kb.py check-updates"
echo ""
