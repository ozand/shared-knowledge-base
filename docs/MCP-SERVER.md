# MCP Server for Shared Knowledge Base

**Version:** 5.1.0
**Last Updated:** 2026-01-10

---

## Overview

The Shared Knowledge Base now includes an **MCP (Model Context Protocol) server** that enables AI assistants like Claude Desktop, VS Code Copilot, and Cursor to directly access knowledge entries through native tool integration.

**📘 Complete MCP Guide:** This document

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r tools/requirements-mcp.txt
```

### 2. Configure Claude Desktop

Add to `~/.config/Claude/claude_desktop_config.json` (Linux/macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "shared-kb": {
      "command": "python",
      "args": ["-m", "tools.mcp_server"],
      "cwd": "T:\\Code\\shared-knowledge-base",
      "env": {}
    }
  }
}
```

### 3. Restart Claude Desktop

The MCP server will automatically start when Claude Desktop launches.

---

## Available Tools

### kb_search

Search knowledge base for entries matching query and filters.

**Parameters:**
- `query` (string): Search query string
- `category` (string, optional): Filter by category
- `severity` (string, optional): Filter by severity (critical, high, medium, low)
- `scope` (string, optional): Filter by scope (universal, python, javascript, docker, postgresql, vps, framework, project)
- `limit` (integer, optional): Maximum results to return (default: 50, max: 500)

**Example:**
```
@shared-kb kb_search query="docker compose" severity="high" limit=10
```

---

### kb_get

Get a specific knowledge entry by ID.

**Parameters:**
- `id` (string, required): Entry ID (e.g., "DOCKER-024", "PYTHON-001")

**Example:**
```
@shared-kb kb_get id="DOCKER-024"
```

---

### kb_browse

Browse all entries in a category.

**Parameters:**
- `category` (string, required): Category name
- `limit` (integer, optional): Maximum entries to return (default: 50)

**Example:**
```
@shared-kb kb_browse category="docker-errors" limit=20
```

---

### kb_validate

Validate YAML files or directories.

**Parameters:**
- `path` (string, optional): Path to YAML file or directory (default: "domains")
- `recursive` (boolean, optional): Search recursively in directories (default: true)

**Example:**
```
@shared-kb kb_validate path="domains/docker"
```

---

### kb_stats

Get repository statistics and metrics.

**Parameters:**
- `format` (string, optional): Output format - "text" or "json" (default: "text")

**Example:**
```
@shared-kb kb_stats format="text"
```

---

### kb_health

Check knowledge base health and status.

**Parameters:** None

**Example:**
```
@shared-kb kb_health
```

---

## Architecture

### Core Modules

The MCP server is built on extracted core logic that is shared with CLI tools:

```
tools/
├── core/                 # Shared core logic
│   ├── __init__.py      # Module exports
│   ├── search.py        # KnowledgeSearch class
│   ├── metrics.py       # MetricsCalculator class
│   ├── validation.py    # KnowledgeValidator class
│   └── models.py        # Pydantic data models
├── mcp_server.py        # MCP server implementation
└── __main__.py          # Entry point
```

### Design Principles

1. **DRY Principle:** Core logic in one place, used by both CLI and MCP
2. **Type Safety:** Pydantic models for all data structures
3. **Error Handling:** Return errors as text (MCP protocol requirement)
4. **Async Support:** Native async for better performance

---

## Configuration Examples

### Claude Desktop (Windows)

```json
{
  "mcpServers": {
    "shared-kb": {
      "command": "python",
      "args": ["-m", "tools.mcp_server"],
      "cwd": "T:\\Code\\shared-knowledge-base",
      "env": {}
    }
  }
}
```

### Claude Desktop (macOS/Linux)

```json
{
  "mcpServers": {
    "shared-kb": {
      "command": "python3",
      "args": ["-m", "tools.mcp_server"],
      "cwd": "/home/user/code/shared-knowledge-base",
      "env": {}
    }
  }
}
```

### VS Code Copilot

Add to your MCP config file (`%APPDATA%\Code\User\mcp.json` on Windows):

```json
{
  "servers": {
    "shared-kb": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "tools.mcp_server"],
      "cwd": "T:\\Code\\shared-knowledge-base",
      "env": {}
    }
  }
}
```

---

## Usage Examples

### Example 1: Find Docker Compose Solutions

```
@shared-kb kb_search query="docker compose healthcheck" scope="docker"
```

**Response:**
```
## Search Results for 'docker compose healthcheck'
Found 2 entries

### Shared KB Results (2)
- **DOCKER-024**: Container becomes healthy before database is ready
  - Severity: high | Scope: docker
  - Preview: The container's healthcheck passes immediately but the DB...
```

---

### Example 2: Get Python Async Entry

```
@shared-kb kb_get id="PYTHON-001"
```

**Response:**
```
## PYTHON-001: RuntimeError: Event Loop is Closed
**Category:** python-async
**Severity:** critical
**Scope:** python

### Problem
Attempting to run async operations after the event loop has been closed...

### Solution
**Code:**
```python
import asyncio

async def main():
    # Your async code here
    pass

if __name__ == "__main__":
    asyncio.run(main())
```
```

---

### Example 3: Check Repository Health

```
@shared-kb kb_health
```

**Response:**
```
## Knowledge Base Health Check
**Status:** HEALTHY
**Version:** 5.1.0
**Uptime:** 123.4 seconds

### Components
- ✅ search: healthy
- ✅ metrics: healthy
- ✅ validation: healthy
- ✅ domains: healthy

### Quick Stats
- Total Entries: 125
- Average Quality: 61.9/100
- Domains: 7
```

---

## Troubleshooting

### Server Won't Start

**Problem:** MCP server fails to start

**Solution:**
1. Verify Python path is correct in config
2. Check dependencies are installed: `pip install -r tools/requirements-mcp.txt`
3. Test manually: `python tools/mcp_server.py`
4. Check Claude Desktop logs for errors

---

### "Module Not Found" Error

**Problem:** `ModuleNotFoundError: No module named 'mcp'`

**Solution:**
```bash
pip install mcp>=1.0.0
```

---

### No Search Results

**Problem:** Search returns no results

**Solution:**
1. Verify `cwd` path in config points to repository root
2. Check `domains/` directory exists
3. Try broader query (e.g., "docker" instead of "docker compose healthcheck")
4. Use `kb_health` to check if entries are loaded

---

### ImportError in tools

**Problem:** `ImportError: cannot import name 'KnowledgeSearch'`

**Solution:**
1. Ensure you're running from repository root
2. Check Python version (requires Python 3.10+)
3. Verify `tools/core/` directory exists
4. Try reinstalling dependencies

---

## Performance

### Benchmarks

| Operation | Time | Notes |
|-----------|------|-------|
| kb_search (5 results) | ~50ms | String-based search |
| kb_get | ~10ms | Direct file lookup |
| kb_browse (20 results) | ~30ms | Category filtering |
| kb_validate (domains/) | ~200ms | Validates 80+ files |
| kb_stats | ~300ms | Full repository scan |

### Optimization Tips

1. **Limit Results:** Use `limit` parameter to reduce response size
2. **Specific Queries:** Use specific filters (category, scope) to narrow search
3. **JSON Format:** Use `format="json"` for programmatic processing

---

## Development

### Running Locally

```bash
# Run MCP server (stdio mode)
python tools/mcp_server.py

# Test with Python
python -c "from tools.core import KnowledgeSearch; ks = KnowledgeSearch(); print(ks.search('docker'))"
```

### Adding New Tools

To add a new MCP tool:

1. Add tool definition in `mcp_server.py` in `list_tools()`
2. Add handler function in `mcp_server.py` in `call_tool()`
3. Update this documentation

Example:
```python
@server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        # Existing tools...
        Tool(
            name="kb_new_tool",
            description="Description of new tool",
            inputSchema={...}
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Any):
    if name == "kb_new_tool":
        return await kb_new_tool(arguments)
```

---

## Security Considerations

### File Access

- MCP server reads from `domains/` directory
- No write operations exposed via MCP
- Validates all file paths

### Input Validation

- All parameters validated using Pydantic models
- Severity and scope checked against allowed values
- Path traversal prevented

### Environment Variables

No sensitive environment variables required. The MCP server operates entirely within the repository context.

---

## Future Enhancements

Planned features for future versions:

1. **Semantic Search:** Add vector embeddings for better search relevance
2. **Caching:** Cache frequent queries for faster response
3. **Streaming:** Stream large results instead of waiting for complete response
4. **Filters:** Add more filter options (date range, tags, author)
5. **Export:** Export search results to file

---

## Related Documentation

- **[README.md](../README.md)** - Project overview
- **[CLAUDE.md](../.claude/CLAUDE.md)** - Agent instructions
- **[docs/v5.1/README.md](v5.1/README.md)** - v5.1 architecture
- **[docs/ARD.md](ARD.md)** - Architecture reference

---

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review [MCP Protocol Documentation](https://modelcontextprotocol.io/)
3. Open issue on GitHub

---

**Version:** 5.1.0
**Quality Score:** 90/100
