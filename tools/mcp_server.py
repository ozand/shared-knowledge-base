"""
MCP Server for Shared Knowledge Base.

Provides stdio-based MCP server with tools for searching, browsing,
validating, and monitoring the knowledge base.

Based on ayga-mcp-client architecture.
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, List
from datetime import datetime

# Try importing mcp, provide helpful error if not available
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("Error: mcp package not installed. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Import core modules
from core import (
    KnowledgeSearch,
    MetricsCalculator,
    KnowledgeValidator,
    SearchFilter,
    HealthStatus
)

# Create MCP server instance
server = Server("shared-knowledge-base")

# Initialize core components
repo_path = Path.cwd()
search_engine = KnowledgeSearch()
metrics_calculator = MetricsCalculator(str(repo_path))
validator = KnowledgeValidator(str(repo_path))

# Track server start time for health checks
server_start_time = datetime.now()


@server.list_tools()
async def list_tools() -> List[Tool]:
    """
    List available MCP tools.

    Returns:
        List of Tool objects describing available tools
    """
    return [
        Tool(
            name="kb_search",
            description="Search knowledge base for entries matching query and filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query string"
                    },
                    "category": {
                        "type": "string",
                        "description": "Filter by category (e.g., 'docker-errors', 'python-async')"
                    },
                    "severity": {
                        "type": "string",
                        "enum": ["critical", "high", "medium", "low"],
                        "description": "Filter by severity level"
                    },
                    "scope": {
                        "type": "string",
                        "enum": ["universal", "python", "javascript", "docker", "postgresql", "vps", "framework", "project"],
                        "description": "Filter by scope"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 50, max: 500)",
                        "default": 50,
                        "minimum": 1,
                        "maximum": 500
                    }
                }
            }
        ),
        Tool(
            name="kb_get",
            description="Get a specific knowledge entry by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "Entry ID (e.g., 'DOCKER-024', 'PYTHON-001')"
                    }
                },
                "required": ["id"]
            }
        ),
        Tool(
            name="kb_browse",
            description="Browse all entries in a category",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Category name (e.g., 'docker-errors', 'python-async')"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum entries to return (default: 50)",
                        "default": 50,
                        "minimum": 1,
                        "maximum": 500
                    }
                },
                "required": ["category"]
            }
        ),
        Tool(
            name="kb_validate",
            description="Validate YAML files or directories",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to YAML file or directory (default: domains/)"
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Search recursively in directories (default: true)",
                        "default": True
                    }
                }
            }
        ),
        Tool(
            name="kb_stats",
            description="Get repository statistics and metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "format": {
                        "type": "string",
                        "enum": ["text", "json"],
                        "description": "Output format (default: text)",
                        "default": "text"
                    }
                }
            }
        ),
        Tool(
            name="kb_health",
            description="Check knowledge base health and status",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """
    Handle MCP tool calls.

    Args:
        name: Tool name
        arguments: Tool arguments

    Returns:
        List of TextContent with results or errors
    """
    try:
        if name == "kb_search":
            return await kb_search(arguments)
        elif name == "kb_get":
            return await kb_get(arguments)
        elif name == "kb_browse":
            return await kb_browse(arguments)
        elif name == "kb_validate":
            return await kb_validate(arguments)
        elif name == "kb_stats":
            return await kb_stats(arguments)
        elif name == "kb_health":
            return await kb_health(arguments)
        else:
            return [TextContent(
                type="text",
                text=f"Error: Unknown tool '{name}'"
            )]

    except Exception as e:
        # Return error as text (MCP protocol requirement)
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def kb_search(arguments: dict) -> List[TextContent]:
    """Search knowledge base"""
    query = arguments.get("query", "")
    category = arguments.get("category")
    severity = arguments.get("severity")
    scope = arguments.get("scope")
    limit = arguments.get("limit", 50)

    # Perform search
    results = search_engine.search(
        query=query,
        category=category,
        severity=severity,
        scope=scope,
        limit=limit,
        include_project=True,
        include_shared=True
    )

    # Format results
    output = []
    output.append(f"## Search Results for '{query}'")
    output.append(f"Found {results.total} entries")

    if results.project_results:
        output.append(f"\n### Project KB Results ({len(results.project_results)})")
        for result in results.project_results[:10]:
            meta = result.metadata
            output.append(f"- **{meta.id}**: {meta.title}")
            output.append(f"  - Severity: {meta.severity} | Scope: {meta.scope}")
            if result.preview:
                output.append(f"  - Preview: {result.preview[:100]}...")

    if results.shared_results:
        output.append(f"\n### Shared KB Results ({len(results.shared_results)})")
        for result in results.shared_results[:10]:
            meta = result.metadata
            output.append(f"- **{meta.id}**: {meta.title}")
            output.append(f"  - Severity: {meta.severity} | Scope: {meta.scope}")
            if result.preview:
                output.append(f"  - Preview: {result.preview[:100]}...")

    if results.execution_time_ms:
        output.append(f"\nExecution time: {results.execution_time_ms:.1f}ms")

    return [TextContent(type="text", text="\n".join(output))]


async def kb_get(arguments: dict) -> List[TextContent]:
    """Get entry by ID"""
    entry_id = arguments.get("id")

    if not entry_id:
        return [TextContent(type="text", text="Error: 'id' parameter is required")]

    result = search_engine.get_by_id(entry_id)

    if not result:
        return [TextContent(type="text", text=f"Error: Entry '{entry_id}' not found")]

    entry = result["entry"]
    category = result["category"]
    file_path = result["file_path"]

    # Format entry
    output = []
    output.append(f"## {entry.get('id', 'UNKNOWN')}: {entry.get('title', 'Untitled')}")
    output.append(f"**Category:** {category}")
    output.append(f"**Severity:** {entry.get('severity', 'unknown')}")
    output.append(f"**Scope:** {entry.get('scope', 'unknown')}")
    output.append(f"**Source:** {file_path}")

    if entry.get('symptoms'):
        output.append(f"\n### Symptoms")
        output.append(entry['symptoms'])

    if entry.get('root_cause'):
        output.append(f"\n### Root Cause")
        output.append(entry['root_cause'])

    if entry.get('problem'):
        output.append(f"\n### Problem")
        output.append(entry['problem'])

    if entry.get('solution'):
        output.append(f"\n### Solution")
        solution = entry['solution']
        if isinstance(solution, dict):
            if solution.get('code'):
                output.append(f"\n**Code:**")
                output.append(f"```")
                output.append(solution['code'])
                output.append(f"```")
            if solution.get('explanation'):
                output.append(f"\n**Explanation:**")
                output.append(solution['explanation'])
        else:
            output.append(str(solution))

    if entry.get('prevention'):
        output.append(f"\n### Prevention")
        output.append(entry['prevention'])

    return [TextContent(type="text", text="\n".join(output))]


async def kb_browse(arguments: dict) -> List[TextContent]:
    """Browse entries by category"""
    category = arguments.get("category")
    limit = arguments.get("limit", 50)

    if not category:
        return [TextContent(type="text", text="Error: 'category' parameter is required")]

    results = search_engine.browse_by_category(category, limit=limit)

    output = []
    output.append(f"## Browsing Category: {category}")
    output.append(f"Found {len(results)} entries")

    for result in results[:20]:
        meta = result.metadata
        output.append(f"\n### {meta.id}: {meta.title}")
        output.append(f"- **Severity:** {meta.severity}")
        output.append(f"- **Scope:** {meta.scope}")
        if result.preview:
            output.append(f"- **Preview:** {result.preview[:150]}...")

    return [TextContent(type="text", text="\n".join(output))]


async def kb_validate(arguments: dict) -> List[TextContent]:
    """Validate YAML files"""
    path_str = arguments.get("path", "domains")
    recursive = arguments.get("recursive", True)

    path = Path(path_str)

    if not path.is_absolute():
        path = Path.cwd() / path

    if not path.exists():
        return [TextContent(type="text", text=f"Error: Path not found: {path}")]

    # Validate
    if path.is_file():
        result = validator.validate_file(path)
    else:
        result = validator.validate_directory(path, recursive=recursive)

    # Format results
    output = []
    output.append(f"## Validation Results")
    output.append(f"**Files Checked:** {result.files_checked}")
    output.append(f"**Status:** {'✅ Valid' if result.is_valid else '❌ Invalid'}")

    if result.execution_time_ms:
        output.append(f"**Execution Time:** {result.execution_time_ms:.1f}ms")

    if result.errors:
        output.append(f"\n### Errors ({len(result.errors)})")
        for error in result.errors[:10]:
            output.append(f"- **{error.file_path}**")
            output.append(f"  - {error.error_type}: {error.message}")
            if error.field_path:
                output.append(f"  - Field: {error.field_path}")

    if result.warnings:
        output.append(f"\n### Warnings ({len(result.warnings)})")
        for warning in result.warnings[:10]:
            output.append(f"- **{warning.file_path}**")
            output.append(f"  - {warning.error_type}: {warning.message}")
            if warning.field_path:
                output.append(f"  - Field: {warning.field_path}")

    if len(result.errors) > 10:
        output.append(f"\n_... and {len(result.errors) - 10} more errors_")

    if len(result.warnings) > 10:
        output.append(f"\n_... and {len(result.warnings) - 10} more warnings_")

    return [TextContent(type="text", text="\n".join(output))]


async def kb_stats(arguments: dict) -> List[TextContent]:
    """Get repository statistics"""
    format_type = arguments.get("format", "text")

    # Calculate metrics
    metrics = metrics_calculator.calculate_all()

    if format_type == "json":
        return [TextContent(
            type="text",
            text=json.dumps(metrics.model_dump(), indent=2, default=str)
        )]

    # Format as text
    output = []
    output.append("## Shared Knowledge Base Statistics")
    output.append(f"**Generated:** {metrics.timestamp}")

    output.append("\n### Repository Statistics")
    rs = metrics.repository_stats
    output.append(f"- Total Files: {rs.total_files:,}")
    output.append(f"- Total Lines: {rs.total_lines:,}")
    output.append(f"- Total Size: {rs.total_size_kb:.1f} KB")
    output.append(f"- YAML Files: {rs.yaml_files}")
    output.append(f"- Markdown Files: {rs.markdown_files}")
    output.append(f"- Python Files: {rs.python_files}")

    output.append("\n### YAML Entry Statistics")
    ys = metrics.yaml_files
    output.append(f"- Total Entries: {ys.total_entries}")
    output.append(f"- Errors: {ys.errors}")
    output.append(f"- Patterns: {ys.patterns}")
    output.append(f"- Avg Entry Size: {ys.avg_entry_size_lines:.1f} lines")

    output.append("\n### Domain Distribution")
    for domain, count in list(metrics.domain_distribution.items())[:10]:
        output.append(f"- {domain}: {count} entries")

    output.append("\n### Quality Scores")
    qs = metrics.quality_scores
    output.append(f"- Total Entries: {qs.total_entries}")
    output.append(f"- Average Score: {qs.avg_score:.1f}/100")
    output.append(f"- Excellent (90-100): {qs.excellent} ({qs.excellent/qs.total_entries*100:.1f}%)" if qs.total_entries > 0 else "")
    output.append(f"- Good (75-89): {qs.good} ({qs.good/qs.total_entries*100:.1f}%)" if qs.total_entries > 0 else "")
    output.append(f"- Acceptable (60-74): {qs.acceptable} ({qs.acceptable/qs.total_entries*100:.1f}%)" if qs.total_entries > 0 else "")
    output.append(f"- Poor (40-59): {qs.poor} ({qs.poor/qs.total_entries*100:.1f}%)" if qs.total_entries > 0 else "")
    output.append(f"- Critical (0-39): {qs.critical} ({qs.critical/qs.total_entries*100:.1f}%)" if qs.total_entries > 0 else "")

    output.append(f"\n### Overall Health: {metrics.health_status.upper()}")

    return [TextContent(type="text", text="\n".join(output))]


async def kb_health(arguments: dict) -> List[TextContent]:
    """Check knowledge base health"""
    uptime = (datetime.now() - server_start_time).total_seconds()

    # Calculate metrics for health status
    metrics = metrics_calculator.calculate_all()

    # Determine component health
    components = {
        "search": "healthy",
        "metrics": "healthy",
        "validation": "healthy",
        "domains": "healthy" if metrics.domain_distribution else "unhealthy"
    }

    issues = []
    if metrics.yaml_files.total_entries == 0:
        issues.append("No knowledge entries found")
        components["domains"] = "unhealthy"

    if metrics.quality_scores.avg_score < 60:
        issues.append(f"Low average quality score: {metrics.quality_scores.avg_score:.1f}/100")
        components["quality"] = "degraded"

    # Overall health
    if any(c == "unhealthy" for c in components.values()):
        overall_health = "unhealthy"
    elif any(c == "degraded" for c in components.values()):
        overall_health = "degraded"
    else:
        overall_health = "healthy"

    # Format response
    output = []
    output.append("## Knowledge Base Health Check")
    output.append(f"**Status:** {overall_health.upper()}")
    output.append(f"**Version:** 5.1.0")
    output.append(f"**Uptime:** {uptime:.1f} seconds")
    output.append(f"**Timestamp:** {datetime.now().isoformat()}")

    output.append("\n### Components")
    for component, status in components.items():
        emoji = "✅" if status == "healthy" else ("⚠️" if status == "degraded" else "❌")
        output.append(f"- {emoji} **{component}**: {status}")

    if issues:
        output.append("\n### Issues")
        for issue in issues:
            output.append(f"- ❌ {issue}")

    if metrics.yaml_files.total_entries > 0:
        output.append(f"\n### Quick Stats")
        output.append(f"- Total Entries: {metrics.yaml_files.total_entries}")
        output.append(f"- Average Quality: {metrics.quality_scores.avg_score:.1f}/100")
        output.append(f"- Domains: {len(metrics.domain_distribution)}")

    return [TextContent(type="text", text="\n".join(output))]


async def main():
    """Main entry point for MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
