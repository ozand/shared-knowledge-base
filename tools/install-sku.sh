#!/bin/bash
# install-sku.sh
#
# Universal installer for SKU (Shared Knowledge Utility)
# Downloads and installs SKU CLI from GitHub
#
# Usage:
#   curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/install-sku.sh | bash
#
# Or with custom repo:
#   SKU_REPO=https://github.com/custom/repo.git curl -sSL ... | bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="${SKU_REPO:-ozand/shared-knowledge-base}"
REPO_BASE="https://github.com/${REPO_URL}"
RAW_BASE="https://raw.githubusercontent.com/${REPO_URL}/main"
INSTALL_DIR="${SKU_INSTALL_DIR:-$HOME/.sku/bin}"

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        SKU Installer - Enterprise Knowledge Graph       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    MINGW*|MSYS*|CYGWIN*)
        MACHINE=Windows
        echo -e "${YELLOW}⚠️  Windows detected${NC}"
        echo "Please use PowerShell installer:"
        echo "  irm ${RAW_BASE}/scripts/install-sku.ps1 | iex"
        exit 1
        ;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo -e "${GREEN}✓ Detected OS:${NC} ${MACHINE}"
echo ""

# Check prerequisites
echo -e "${BLUE}🔍 Checking prerequisites...${NC}"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}⚠️  uv not found${NC}"
    echo "Installing uv..."

    # Install uv
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"

    if command -v uv &> /dev/null; then
        echo -e "${GREEN}✓ uv installed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to install uv${NC}"
        echo "Please install uv manually: https://github.com/astral-sh/uv"
        exit 1
    fi
else
    echo -e "${GREEN}✓ uv found:${NC} $(uv --version)"
fi

# Check if python is available
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python not found${NC}"
    echo "Please install Python 3.8+ first"
    exit 1
fi

PYTHON_CMD=$(command -v python3 || command -v python)
PYTHON_VERSION=$($PYTHON_CMD --version)
echo -e "${GREEN}✓ Python found:${NC} ${PYTHON_VERSION}"

echo ""

# Create install directory
echo -e "${BLUE}📁 Creating installation directory...${NC}"
mkdir -p "$INSTALL_DIR"
mkdir -p "$HOME/.sku"

echo -e "${GREEN}✓ Install directory:${NC} ${INSTALL_DIR}"
echo ""

# Download SKU CLI files
echo -e "${BLUE}⬇️  Downloading SKU CLI...${NC}"

# Create temporary directory
TMP_DIR=$(mktemp -d)
trap "rm -rf ${TMP_DIR}" EXIT

# Download pyproject.toml
curl -sSL "${RAW_BASE}/tools/skb-cli/pyproject.toml" -o "${TMP_DIR}/pyproject.toml"

# Download Python files
mkdir -p "${TMP_DIR}/sku"
for file in __init__.py cli.py catalog.py sync.py install.py publish.py update.py auth.py utils.py; do
    echo "  Downloading: ${file}"
    curl -sSL "${RAW_BASE}/tools/skb-cli/sku/${file}" -o "${TMP_DIR}/sku/${file}"
done

echo -e "${GREEN}✓ Downloaded SKU CLI files${NC}"
echo ""

# Install SKU CLI
echo -e "${BLUE}🔧 Installing SKU CLI...${NC}"

# Install using uv
cd "${TMP_DIR}"
uv pip install --target "$INSTALL_DIR" . &> /dev/null || {
    echo -e "${RED}✗ Installation failed${NC}"
    exit 1
}

# Create wrapper script
cat > "$HOME/.sku/bin/sku" <<'WRAPPER_EOF'
#!/usr/bin/env bash
# SKU wrapper script

# Set Python path
export PYTHONPATH="$HOME/.sku/bin:$PYTHONPATH"

# Run sku
python "$HOME/.sku/bin/sku/cli.py" "$@"
WRAPPER_EOF

chmod +x "$HOME/.sku/bin/sku"

echo -e "${GREEN}✓ SKU CLI installed${NC}"
echo ""

# Create configuration
echo -e "${BLUE}⚙️  Creating configuration...${NC}"

cat > "$HOME/.sku/config.yaml" <<'CONFIG_EOF'
github:
  repository: "ozand/shared-knowledge-base"
  branch: "main"

auto_update:
  policy: "smart"  # never|smart|auto
  check_interval: "daily"

paths:
  cache: "$HOME/.sku/cache"
  repo: "$HOME/.sku/repo"
  artifacts: "$HOME/.sku/artifacts"
CONFIG_EOF

echo -e "${GREEN}✓ Configuration created:${NC} $HOME/.sku/config.yaml"
echo ""

# Add to PATH
echo -e "${BLUE}🔗 Setting up PATH...${NC}"

SHELL_CONFIG=""
case "${SHELL}" in
    */zsh)
        SHELL_CONFIG="$HOME/.zshrc"
        ;;
    */bash)
        SHELL_CONFIG="$HOME/.bashrc"
        ;;
    *)
        SHELL_CONFIG="$HOME/.profile"
        ;;
esac

# Check if already in PATH
if ! grep -q "$HOME/.sku/bin" "$SHELL_CONFIG" 2>/dev/null; then
    cat >> "$SHELL_CONFIG" <<'PATH_EOF'

# SKU (Shared Knowledge Utility)
export PATH="$HOME/.sku/bin:$PATH"
PATH_EOF

    echo -e "${GREEN}✓ Added to PATH in:${NC} ${SHELL_CONFIG}"
    echo -e "${YELLOW}⚠️  Please run: source ${SHELL_CONFIG}${NC}"
else
    echo -e "${GREEN}✓ Already in PATH${NC}"
fi

echo ""

# Sync catalog
echo -e "${BLUE}📦 Syncing catalog (first time)...${NC}"

# Create catalog directory
mkdir -p "$HOME/.sku/catalog"

# Download catalog
curl -sSL "${RAW_BASE}/catalog/index.yaml" -o "$HOME/.sku/catalog/index.yaml"
curl -sSL "${RAW_BASE}/catalog/categories.yaml" -o "$HOME/.sku/catalog/categories.yaml"

echo -e "${GREEN}✓ Catalog synced${NC}"
echo ""

# Summary
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                   Installation Complete!                ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✓ SKU CLI installed successfully!${NC}"
echo ""
echo -e "${BLUE}Quick Start:${NC}"
echo "  1. Restart your shell or run: source ${SHELL_CONFIG}"
echo "  2. Authenticate:"
echo -e "     ${YELLOW}sku auth login${NC}"
echo "  3. Sync catalog:"
echo -e "     ${YELLOW}sku sync --index-only${NC}"
echo "  4. Install artifact:"
echo -e "     ${YELLOW}sku install skill testing${NC}"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo "  sku --help              Show all commands"
echo "  sku list                List available artifacts"
echo "  sku search <query>      Search artifacts"
echo "  sku status              Show installation status"
echo ""
echo -e "${BLUE}For new projects:${NC}"
echo "  cd /path/to/project"
echo "  sku init                Initialize Claude Code setup"
echo ""
echo -e "${YELLOW}⚠️  Next step:${NC} Restart your shell for PATH changes to take effect"
echo ""
