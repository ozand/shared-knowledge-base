"""
Shared Knowledge Base - MCP Server Entry Point

Run the MCP server using: python -m tools

This starts the stdio-based MCP server that can be integrated with
Claude Desktop, VS Code Copilot, and other MCP-compatible clients.

Usage:
    python -m tools
    REDIS_API_KEY=your_key python -m tools

For configuration details, see docs/MCP-SERVER.md
"""

import asyncio
import sys
from pathlib import Path

# Add repository root to path for imports
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

# Import the MCP server
from tools.mcp_server import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMCP server stopped", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error starting MCP server: {e}", file=sys.stderr)
        sys.exit(1)
