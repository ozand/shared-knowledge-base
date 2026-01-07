# install-sku.ps1
#
# Universal installer for SKU (Shared Knowledge Utility) - Windows PowerShell
# Downloads and installs SKU CLI from GitHub
#
# Usage:
#   irm https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/install-sku.ps1 | iex
#
# Or with custom repo:
#   $env:SKU_REPO="custom/repo"; irm ... | iex

$ErrorActionPreference = "Stop"

# Configuration
$RepoUrl = if ($env:SKU_REPO) { $env:SKU_REPO } else { "ozand/shared-knowledge-base" }
$RepoBase = "https://github.com/${RepoUrl}"
$RawBase = "https://raw.githubusercontent.com/${RepoUrl}/main"
$InstallDir = if ($env:SKU_INSTALL_DIR) { $env:SKU_INSTALL_DIR } else { "$env:USERPROFILE\.sku\bin" }

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║        SKU Installer - Enterprise Knowledge Graph       ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Blue

# Check if uv is installed
$uvFound = $false
try {
    $uvVersion = uv --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $uvFound = $true
        Write-Host "✓ uv found: $uvVersion" -ForegroundColor Green
    }
} catch {
    # uv not found
}

if (-not $uvFound) {
    Write-Host "⚠️  uv not found" -ForegroundColor Yellow
    Write-Host "Installing uv..."

    # Install uv using PowerShell
    irm https://astral.sh/uv/install.ps1 | iex

    # Check again
    $uvVersion = uv --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ uv installed successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to install uv" -ForegroundColor Red
        Write-Host "Please install uv manually: https://github.com/astral-sh/uv"
        exit 1
    }
}

# Check if python is available
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Host "✗ Python not found" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ first"
    exit 1
}

$pythonVersion = & $pythonCmd --version
Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Create install directory
Write-Host "📁 Creating installation directory..." -ForegroundColor Blue
New-Item -ItemType Directory -Force -Path "$InstallDir" | Out-Null
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.sku" | Out-Null

Write-Host "✓ Install directory: $InstallDir" -ForegroundColor Green
Write-Host ""

# Download SKU CLI files
Write-Host "⬇️  Downloading SKU CLI..." -ForegroundColor Blue

# Create temporary directory
$tmpDir = Join-Path $env:TEMP "sku-install-$([GUID]::NewGuid())"
New-Item -ItemType Directory -Force -Path $tmpDir | Out-Null

try {
    # Download pyproject.toml
    Invoke-WebRequest -Uri "$RawBase/tools/skb-cli/pyproject.toml" -OutFile "$tmpDir\pyproject.toml" -UseBasicParsing

    # Download Python files
    New-Item -ItemType Directory -Force -Path "$tmpDir\sku" | Out-Null

    $files = @("__init__.py", "cli.py", "catalog.py", "sync.py", "install.py", "publish.py", "update.py", "auth.py", "utils.py")
    foreach ($file in $files) {
        Write-Host "  Downloading: $file"
        Invoke-WebRequest -Uri "$RawBase/tools/skb-cli/sku/$file" -OutFile "$tmpDir\sku\$file" -UseBasicParsing
    }

    Write-Host "✓ Downloaded SKU CLI files" -ForegroundColor Green
    Write-Host ""

    # Install SKU CLI
    Write-Host "🔧 Installing SKU CLI..." -ForegroundColor Blue

    # Install using uv
    Push-Location $tmpDir
    uv pip install --target $InstallDir . 2>&1 | Out-Null
    Pop-Location

    if ($LASTEXITCODE -ne 0) {
        throw "Installation failed"
    }

    # Create wrapper script
    $skuWrapper = @"
#!/usr/bin/env python
import sys
import os

# Set Python path
sys.path.insert(0, r'$InstallDir')

# Run sku
from sku import cli
sys.exit(cli.main())
"@

    $skuWrapper | Out-File "$InstallDir\sku.py" -Encoding UTF8

    # Create batch wrapper
    @"
@echo off
python "$InstallDir\sku.py" %*
"@ | Out-File "$env:USERPROFILE\.sku\bin\sku.cmd" -Encoding ASCII

    Write-Host "✓ SKU CLI installed" -ForegroundColor Green
    Write-Host ""

    # Create configuration
    Write-Host "⚙️  Creating configuration..." -ForegroundColor Blue

    $configContent = @"
github:
  repository: "ozand/shared-knowledge-base"
  branch: "main"

auto_update:
  policy: "smart"
  check_interval: "daily"

paths:
  cache: "$env:USERPROFILE\.sku\cache"
  repo: "$env:USERPROFILE\.sku\repo"
  artifacts: "$env:USERPROFILE\.sku\artifacts"
"@

    $configContent | Out-File "$env:USERPROFILE\.sku\config.yaml" -Encoding UTF8

    Write-Host "✓ Configuration created: $env:USERPROFILE\.sku\config.yaml" -ForegroundColor Green
    Write-Host ""

    # Sync catalog
    Write-Host "📦 Syncing catalog (first time)..." -ForegroundColor Blue

    New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.sku\catalog" | Out-Null

    Invoke-WebRequest -Uri "$RawBase/catalog/index.yaml" -OutFile "$env:USERPROFILE\.sku\catalog\index.yaml" -UseBasicParsing
    Invoke-WebRequest -Uri "$RawBase/catalog/categories.yaml" -OutFile "$env:USERPROFILE\.sku\catalog\categories.yaml" -UseBasicParsing

    Write-Host "✓ Catalog synced" -ForegroundColor Green
    Write-Host ""

    # Add to PATH
    Write-Host "🔗 Setting up PATH..." -ForegroundColor Blue

    $skuPath = "$env:USERPROFILE\.sku\bin"
    $pathInProfile = [Environment]::GetEnvironmentVariable("Path", "User") -split ";" | Where-Object { $_ -eq $skuPath }

    if (-not $pathInProfile) {
        # Add to user PATH
        $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$skuPath", "User")

        Write-Host "✓ Added to user PATH" -ForegroundColor Green
        Write-Host "⚠️  Please restart your terminal for PATH changes to take effect" -ForegroundColor Yellow
    } else {
        Write-Host "✓ Already in PATH" -ForegroundColor Green
    }

    Write-Host ""

    # Summary
    Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                   Installation Complete!                ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "✓ SKU CLI installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Quick Start:" -ForegroundColor Cyan
    Write-Host "  1. Restart your terminal"
    Write-Host "  2. Authenticate:"
    Write-Host "     sku auth login" -ForegroundColor Yellow
    Write-Host "  3. Sync catalog:"
    Write-Host "     sku sync --index-only" -ForegroundColor Yellow
    Write-Host "  4. Install artifact:"
    Write-Host "     sku install skill testing" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Useful Commands:" -ForegroundColor Cyan
    Write-Host "  sku --help              Show all commands"
    Write-Host "  sku list                List available artifacts"
    Write-Host "  sku search <query>      Search artifacts"
    Write-Host "  sku status              Show installation status"
    Write-Host ""
    Write-Host "For new projects:" -ForegroundColor Cyan
    Write-Host "  cd C:\path\to\project"
    Write-Host "  sku init                Initialize Claude Code setup"
    Write-Host ""

} finally {
    # Cleanup
    Remove-Item -Recurse -Force $tmpDir -ErrorAction SilentlyContinue
}
