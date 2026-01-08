# YouTube Comments MCP Server

**Version:** 1.0.0
**Project:** mcp-youtube
**Type:** MCP Server
**Published:** 2026-01-07

---

## Overview

MCP server for downloading and processing YouTube comments. Provides schema definitions, API documentation, and usage examples.

## Installation

```bash
# Install MCP artifact
uvx sku install mcp mcp-youtube/youtube-comments-mcp
```

## Usage

Once installed, Claude Code will automatically know about the YouTube Comments MCP schema and can use it without additional documentation.

### Example: Analyzing Comments

```python
# Claude Code can now:
# 1. Understand YouTube comment schema
# 2. Generate code to fetch comments
# 3. Create analysis queries
# 4. Build integrations

from youtube_mcp import fetch_comments

comments = fetch_comments(video_id="abc123")
# Returns structured data matching comment-schema.yaml
```

## Artifacts Included

- **MCP Schema** (`SCHEMA.md`) - Complete server schema
- **Usage Guide** (`USAGE.md`) - How to use the MCP server
- **API Documentation** - YouTube API integration details
- **Data Schemas** - Comment and video data structures

## Dependencies

None (standalone MCP server)

## Author

**Team:** backend-team
**Repository:** private/mcp-youtube
**License:** MIT

## Version History

- **1.0.0** (2026-01-07) - Initial release
