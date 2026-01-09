#!/usr/bin/env python3
"""
kb_search.py - Search knowledge entries across Project and Shared KB

Usage:
    python tools/v5.1/kb_search.py "docker compose"
    python tools/v5.1/kb_search.py "fastapi cors" --scope shared
    python tools/v5.1/kb_search.py "stripe" --scope project

Version: 5.1.0
"""

import os
import argparse
import logging
from pathlib import Path
from typing import List, Tuple, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# When run from Shared KB repo (for curator), search in domains/
# When run from consumer project (via submodule), search in .kb/shared/domains/
if (PROJECT_ROOT / "domains").exists():
    # Running in Shared KB repository
    SHARED_KB_PATH = PROJECT_ROOT / "domains"
else:
    # Running in consumer project
    SHARED_KB_PATH = PROJECT_ROOT / ".kb" / "shared" / "domains"

PATHS = {
    "project": PROJECT_ROOT / ".kb" / "project",
    "shared": SHARED_KB_PATH
}


def search_files(root_path: Path, query: str) -> List[Path]:
    """
    Search for YAML files containing query string.

    Args:
        root_path: Root directory to search
        query: Search query string

    Returns:
        List of matching file paths
    """
    matches = []

    if not root_path.exists():
        logger.warning(f"Search path does not exist: {root_path}")
        return matches

    query_lower = query.lower()

    # Search recursively for YAML files
    for path in root_path.rglob("*.yaml"):
        # Skip index files
        if "_index" in path.name or "_index" in str(path):
            continue

        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read().lower()

                # Check if query is in content or filename
                if query_lower in content or query_lower in path.name.lower():
                    matches.append(path)

        except Exception as e:
            logger.debug(f"Could not read file {path}: {e}")
            # Skip files that can't be read
            continue

    logger.info(f"Search completed: {len(matches)} matches found in {root_path}")
    return matches


def extract_metadata(file_path: Path) -> Dict[str, Any]:
    """
    Extract metadata from YAML file for better display.

    Args:
        file_path: Path to YAML file

    Returns:
        Dictionary with title, problem, severity, etc.
    """
    try:
        import yaml
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # Extract from errors or patterns
        entries = data.get('errors', []) or data.get('patterns', [])
        if entries:
            entry = entries[0]
            return {
                'title': entry.get('title', 'No title'),
                'severity': entry.get('severity', 'unknown'),
                'category': data.get('category', 'general'),
                'scope': entry.get('scope', 'universal')
            }
    except Exception as e:
        logger.debug(f"Could not extract metadata from {file_path}: {e}")

    return {
        'title': file_path.stem,
        'severity': 'unknown',
        'category': 'unknown',
        'scope': 'unknown'
    }


def extract_preview(file_path: Path, query: str, max_lines: int = 3) -> str:
    """
    Extract lines containing query for preview.

    Args:
        file_path: Path to file
        query: Search query
        max_lines: Maximum lines to show

    Returns:
        String preview with matching lines highlighted
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        query_lower = query.lower()
        matching_lines = []

        for i, line in enumerate(lines):
            if query_lower in line.lower():
                # Show context (line number + content)
                matching_lines.append(f"  L{i+1}: {line.rstrip()}")
                if len(matching_lines) >= max_lines:
                    break

        return "\n".join(matching_lines) if matching_lines else "  (No preview available)"

    except Exception:
        return "  (Error reading file)"


def display_results(results: Dict[str, Any], query: str, show_preview: bool = False) -> None:
    """
    Display search results in a formatted way with priority ordering.

    Args:
        results: Dictionary with source -> list of paths
        query: Original search query
        show_preview: Whether to show content preview
    """
    total = sum(len(paths) for paths in results.values())

    if total == 0:
        logger.info(f"Search '{query}' returned 0 results")
        print(f"🔍 Search: '{query}' | Found: 0")
        print("\n❌ No matches found. Try:")
        print("   - Different search terms")
        print("   - Broader query (fewer words)")
        print("   - Check if KB directories exist")
        print("\n💡 Tip: If no local results, consider web search")
        return

    logger.info(f"Search '{query}' returned {total} results")
    print(f"🔍 Search: '{query}' | Found: {total}\n")

    # Priority order: PROJECT → SHARED
    # Project KB always shown first as it overrides Shared KB
    priority_order = ["PROJECT", "SHARED"]

    # Display results in priority order
    for source in priority_order:
        if source not in results or not results[source]:
            continue

        paths = results[source]
        icon = "⭐" if source == "PROJECT" else "📚"
        priority_hint = " [HIGHEST PRIORITY - Overrides Shared KB]" if source == "PROJECT" else ""

        print(f"--- {source} KB ({len(paths)} entries){priority_hint} ---\n")

        for path in paths:
            try:
                # Get relative path from project root
                rel_path = path.relative_to(PROJECT_ROOT)
                metadata = extract_metadata(path)

                print(f"{icon} {rel_path}")
                print(f"   Title: {metadata['title']}")
                print(f"   Severity: {metadata['severity']} | Category: {metadata['category']} | Scope: {metadata['scope']}")

                # Show preview if requested
                if show_preview:
                    preview = extract_preview(path, query)
                    print(f"\n{preview}\n")
                else:
                    print()  # Spacing between entries

            except ValueError:
                # If can't get relative path, show absolute
                print(f"📄 {path}\n")

    # Conflict resolution hint if both sources have results
    if "PROJECT" in results and "SHARED" in results:
        if results["PROJECT"] and results["SHARED"]:
            print("⚠️  NOTE: Project KB entries take precedence over Shared KB")
            print("   Always follow project-specific patterns over general standards\n")


def get_kb_stats() -> Dict[str, Any]:
    """
    Get statistics about KB directories.

    Returns:
        Dictionary with stats for each KB
    """
    stats = {}

    for source, path in PATHS.items():
        if path.exists():
            yaml_files = list(path.rglob("*.yaml"))
            # Filter out index files
            yaml_files = [f for f in yaml_files if "_index" not in f.name]

            stats[source] = {
                "exists": True,
                "path": path,
                "entries": len(yaml_files)
            }
            logger.debug(f"{source} KB: {len(yaml_files)} entries at {path}")
        else:
            stats[source] = {
                "exists": False,
                "path": path,
                "entries": 0
            }
            logger.debug(f"{source} KB: path does not exist: {path}")

    return stats


def main() -> None:
    """CLI interface"""
    parser = argparse.ArgumentParser(
        description="Knowledge Base Search Tool v5.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search all KBs
  python tools/v5.1/kb_search.py "docker compose"

  # Search only Shared KB
  python tools/v5.1/kb_search.py "fastapi cors" --scope shared

  # Search only Project KB
  python tools/v5.1/kb_search.py "stripe webhook" --scope project

  # Search with preview
  python tools/v5.1/kb_search.py "postgresql" --preview

  # Show KB statistics
  python tools/v5.1/kb_search.py --stats
        """
    )

    parser.add_argument(
        "query",
        nargs="?",
        help="Search query (text to search for in YAML files)"
    )

    parser.add_argument(
        "--scope",
        choices=["project", "shared", "all"],
        default="all",
        help="Where to search: 'project', 'shared', or 'all' (default: all)"
    )

    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show content preview with matching lines"
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show KB statistics instead of searching"
    )

    args = parser.parse_args()

    # Show statistics if requested
    if args.stats:
        stats = get_kb_stats()

        logger.info("Displaying KB statistics")
        print("📊 Knowledge Base Statistics\n")
        for source, stat in stats.items():
            if stat["exists"]:
                print(f"✅ {source.upper()} KB: {stat['entries']} entries")
                print(f"   Path: {stat['path']}")
            else:
                print(f"❌ {source.upper()} KB: Not found")
                print(f"   Expected: {stat['path']}")

            print()

        return 0

    # Require query if not showing stats
    if not args.query:
        parser.print_help()
        return 1

    # Search in requested scopes
    results = {}
    scopes = []

    if args.scope in ["project", "all"]:
        scopes.append("project")
        results["PROJECT"] = search_files(PATHS["project"], args.query)

    if args.scope in ["shared", "all"]:
        scopes.append("shared")
        results["SHARED"] = search_files(PATHS["shared"], args.query)

    logger.info(f"Searching in scopes: {', '.join(scopes)}")
    # Display results
    display_results(results, args.query, show_preview=args.preview)

    return 0


if __name__ == "__main__":
    exit(main())
