# SKU - Shared Knowledge Utility

**Enterprise Knowledge Graph CLI for Claude Code Artifacts**

## Overview

SKU (Shared Knowledge Utility) is a CLI tool for managing Claude Code artifacts across your organization's projects. It enables:

- **Lazy loading** of artifacts (index always synced, artifacts on demand)
- **Cross-project knowledge sharing** (projects publish, others consume)
- **Versioned artifacts** with semantic versioning
- **Smart updates** (auto for patches, prompt for breaking changes)

## Installation

```bash
# Using uv (recommended)
uv pip install uvx

# Install from local repository
uv pip install -e tools/skb-cli/

# Or run directly with uvx
uvx sku --help
```

## Quick Start

```bash
# 1. Authenticate with private repository
uvx sku auth login

# 2. Sync catalog (fast, metadata only)
uvx sku sync --index-only

# 3. Search for artifacts
uvx sku search --tag testing
uvx sku list --category agents

# 4. Install artifact
uvx sku install skill testing

# 5. Publish project artifact
uvx sku publish project my-mcp --type mcp
```

## Commands

### Sync

```bash
# Sync catalog only (fast, recommended)
uvx sku sync --index-only

# Sync specific category
uvx sku sync --category agents

# Sync all artifacts (slow)
uvx sku sync --all
```

### Search & List

```bash
# List all artifacts
uvx sku list

# Filter by category
uvx sku list --category agents
uvx sku list --category projects

# Search by tags
uvx sku search --tag youtube
uvx sku search --tag docker

# Show artifact details
uvx sku info agent code-review
uvx sku info project mcp-youtube/mcp
```

### Install

```bash
# Install shared artifact
uvx sku install agent code-review
uvx sku install skill testing
uvx sku install hook typescript-quality

# Install project artifact
uvx sku install mcp mcp-youtube/youtube-comments-mcp
uvx sku install docs mcp-youtube/youtube-api-docs

# Install with dependencies
uvx sku install template typescript-starter  # includes agents + skills + hooks
```

### Publish

```bash
# Publish project artifact
uvx sku publish project mcp-youtube --type mcp --version 1.0.0

# Publish documentation
uvx sku publish project data-pipeline --type docs --version 2.0.0

# Publish with custom metadata
uvx sku publish project analytics-dashboard \
  --type metrics \
  --version 1.5.0 \
  --tags "analytics,business,kpi"
```

### Update

```bash
# Check for updates
uvx sku check-updates

# Update specific artifact
uvx sku update agent code-review

# Update all installed artifacts
uvx sku update --all
```

### Uninstall

```bash
# Remove artifact
uvx sku uninstall agent code-review

# Remove project artifact
uvx sku uninstall mcp mcp-youtube/youtube-comments-mcp
```

## Configuration

Config file: `~/.sku/config.yaml`

```yaml
github:
  repository: "your-team/shared-knowledge-base"
  branch: "main"
  auth_method: "token"  # token|ssh|github-app
  token: "ghp_xxxxxxxxxxxx"  # or use env var: GITHUB_TOKEN

auto_update:
  policy: "smart"  # never|smart|auto
  check_interval: "daily"  # daily|weekly|never

paths:
  cache: "~/.sku/cache"
  repo: "~/.sku/repo"
  artifacts: "~/.sku/artifacts"

project:
  # Current project context (for publishing)
  id: "my-project"
  name: "My Project"
  team: "backend-team"
```

## Environment Variables

```bash
# GitHub authentication
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
export SKU_REPO="your-team/shared-knowledge-base"

# Cache location
export SKU_CACHE_DIR="~/.sku/cache"

# Debug mode
export SKU_DEBUG=1
```

## Examples

### Example 1: YouTube MCP Project

```bash
# In mcp-youtube project directory

# Publish MCP documentation
uvx sku publish . \
  --type mcp \
  --name "YouTube Comments MCP" \
  --version 1.0.0 \
  --tags "youtube,comments,api"

# In analytics-dashboard project

# Install YouTube MCP docs
uvx sku install mcp mcp-youtube/youtube-comments-mcp

# Now Claude Code knows about YouTube MCP
# without manual documentation sharing!
```

### Example 2: Team Setup

```bash
# One-time setup for team member

# 1. Clone shared-knowledge-base with auth
git clone https://github.com/your-team/shared-knowledge-base.git

# 2. Install sku CLI
cd shared-knowledge-base
uv pip install -e tools/skb-cli/

# 3. Authenticate
sku auth login

# 4. Sync catalog
sku sync --index-only

# 5. Install common artifacts
sku install agent code-review
sku install skill testing
sku install hook typescript-quality
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   shared-knowledge-base                  │
│                                                          │
│  catalog/index.yaml (5KB) ← Always synced              │
│                                                          │
│  claude-code-artifacts/ ← Lazy load                    │
│    ├── agents/                                         │
│    ├── skills/                                         │
│    └── hooks/                                          │
│                                                          │
│  projects/ ← Lazy load                                 │
│    ├── mcp-youtube/                                     │
│    ├── data-pipeline/                                  │
│    └── analytics-dashboard/                            │
└─────────────────────────────────────────────────────────┘

         ↑ sync index           ↑ install artifact           ↑ publish
┌──────────────┐            ┌──────────────┐            ┌──────────────┐
│  Project A   │            │  Project B   │            │  Project C   │
│  (Creator)   │            │  (Consumer)  │            │  (Publisher) │
└──────────────┘            └──────────────┘            └──────────────┘
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black sku/
ruff check sku/

# Type check
mypy sku/
```

## License

MIT License - see LICENSE file for details
