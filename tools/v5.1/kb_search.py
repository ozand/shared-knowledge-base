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
from pathlib import Path
from typing import List, Tuple

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
            # Skip files that can't be read
            continue

    return matches


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


def display_results(results: dict, query: str, show_preview: bool = False):
    """
    Display search results in a formatted way.

    Args:
        results: Dictionary with source -> list of paths
        query: Original search query
        show_preview: Whether to show content preview
    """
    total = sum(len(paths) for paths in results.values())

    if total == 0:
        print(f"🔍 Search: '{query}' | Found: 0")
        print("\n❌ No matches found. Try:")
        print("   - Different search terms")
        print("   - Broader query (fewer words)")
        print("   - Check if KB directories exist")
        return

    print(f"🔍 Search: '{query}' | Found: {total}\n")

    # Display results by source
    for source, paths in results.items():
        if paths:
            print(f"--- {source} KB ({len(paths)} entries) ---")

            for path in paths:
                try:
                    # Get relative path from project root
                    rel_path = path.relative_to(PROJECT_ROOT)
                    print(f"\n📄 {rel_path}")

                    # Show preview if requested
                    if show_preview:
                        preview = extract_preview(path, query)
                        print(f"\n{preview}\n")

                except ValueError:
                    # If can't get relative path, show absolute
                    print(f"📄 {path}")

            print()  # Blank line between sources


def get_kb_stats() -> dict:
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
        else:
            stats[source] = {
                "exists": False,
                "path": path,
                "entries": 0
            }

    return stats


def main():
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

    if args.scope in ["project", "all"]:
        results["PROJECT"] = search_files(PATHS["project"], args.query)

    if args.scope in ["shared", "all"]:
        results["SHARED"] = search_files(PATHS["shared"], args.query)

    # Display results
    display_results(results, args.query, show_preview=args.preview)

    return 0


if __name__ == "__main__":
    exit(main())
