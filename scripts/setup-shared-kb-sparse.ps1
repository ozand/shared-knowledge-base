# setup-shared-kb-sparse.ps1
#
# Setup Shared KB as submodule with sparse checkout (Windows version)
# This ensures only Project Agent content is loaded, excluding Curator files
#
# Usage:
#   cd C:\path\to\your\project
#   powershell -ExecutionPolicy Bypass -File C:\path\to\shared-knowledge-base\scripts\setup-shared-kb-sparse.ps1

$ErrorActionPreference = "Stop"

Write-Host "🔧 Setting up Shared KB with sparse checkout..." -ForegroundColor Cyan
Write-Host ""

# Configuration
$SHARED_KB_URL = "https://github.com/ozand/shared-knowledge-base.git"
$SHARED_KB_DIR = "docs/knowledge-base/shared"

# Check if already exists
if (Test-Path "$SHARED_KB_DIR/.git") {
    Write-Host "⚠️  Shared KB already exists at $SHARED_KB_DIR" -ForegroundColor Yellow
    Write-Host "   Remove it first if you want to re-setup:"
    Write-Host "   git submodule deinit -f $SHARED_KB_DIR"
    Write-Host "   Remove-Item -Recurse -Force $SHARED_KB_DIR"
    Write-Host "   git rm -f $SHARED_KB_DIR"
    exit 1
}

# Create parent directory
Write-Host "📁 Creating directory structure..." -ForegroundColor Green
$parentDir = Split-Path -Parent $SHARED_KB_DIR
if (-not (Test-Path $parentDir)) {
    New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
}

# Add submodule
Write-Host "📦 Adding submodule..." -ForegroundColor Green
git submodule add $SHARED_KB_URL $SHARED_KB_DIR

# Enable sparse checkout
Write-Host "✂️  Enabling sparse checkout..." -ForegroundColor Green
Push-Location $SHARED_KB_DIR
git config core.sparseCheckout true

# Create sparse-checkout directory
$sparseCheckoutDir = ".git/info"
if (-not (Test-Path $sparseCheckoutDir)) {
    New-Item -ItemType Directory -Path $sparseCheckoutDir -Force | Out-Null
}

# Create sparse-checkout file
Write-Host "📝 Creating sparse-checkout configuration..." -ForegroundColor Green
$sparseCheckoutContent = @"
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
.kb-version
"@

Set-Content -Path "$sparseCheckoutDir/sparse-checkout" -Value $sparseCheckoutContent -NoNewline

# Pull only specified content
Write-Host "⬇️  Pulling only specified content..." -ForegroundColor Green
git pull origin main

Pop-Location

# Verify
Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 What's loaded:"
Write-Host "   ✅ Patterns (universal/, python/, postgresql/, docker/, javascript/)"
Write-Host "   ✅ Documentation (README.md, GUIDE.md, agent guides)"
Write-Host "   ✅ Tools (tools/kb.py, scripts/)"
Write-Host ""
Write-Host "🚫 What's EXCLUDED (not loaded):"
Write-Host "   ❌ curator/ (Curator instructions)"
Write-Host "   ❌ *_ANALYSIS.md (analysis documents)"
Write-Host "   ❌ *_REPORT.md (Curator reports)"
Write-Host "   ❌ CHAT_*.md (chat analysis)"
Write-Host "   ❌ Generated files (.agent-config.local, _index*.yaml)"
Write-Host ""
Write-Host "📁 Location: $SHARED_KB_DIR"
Write-Host ""
Write-Host "💡 To update Shared KB:"
Write-Host "   git submodule update --remote --merge $SHARED_KB_DIR"
Write-Host ""
Write-Host "💡 To check for updates:"
Write-Host "   python $SHARED_KB_DIR/tools/kb.py check-updates"
Write-Host ""
