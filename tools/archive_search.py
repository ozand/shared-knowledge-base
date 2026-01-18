#!/usr/bin/env python3
"""
Archive Search - Full-text and metadata search for condensed archive.
Provides fast discovery of relevant context files.
"""

import re
from pathlib import Path
from typing import List, Dict, Optional
from archive_index import ArchiveIndex


class ArchiveSearch:
    """Full-text and metadata search engine."""

    def __init__(self, archive_root: Path):
        """Initialize search engine."""
        self.archive_root = Path(archive_root)
        self.condensed_root = self.archive_root / "condensed"
        self.index = ArchiveIndex(archive_root)

    def search_full_text(self, query: str, file_type: Optional[str] = None) -> List[Dict]:
        """Search condensed file contents."""
        query_lower = query.lower()
        results = []

        # Get candidate files from index
        if file_type:
            candidates = self.index.get_entries_by_type(file_type)
        else:
            candidates = self.index.index_data.get("files", [])

        # Search in condensed files
        for entry in candidates:
            condensed_path = self.archive_root / entry["condensed_file"]
            if not condensed_path.exists():
                continue

            try:
                with open(condensed_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()

                # Simple keyword matching with context
                if query_lower in content:
                    matches = self._extract_context(content, query_lower, context_chars=200)
                    results.append({
                        "source_file": entry["source_file"],
                        "condensed_file": entry["condensed_file"],
                        "type": entry.get("type"),
                        "confidence": entry.get("confidence"),
                        "tags": entry.get("tags", []),
                        "matches": len(matches),
                        "preview": matches[0] if matches else ""
                    })
            except Exception as e:
                print(f"Error searching {condensed_path}: {e}")

        # Sort by match count and confidence
        results.sort(
            key=lambda x: (x["matches"], x["confidence"]),
            reverse=True
        )
        return results

    def search_by_tags(self, tags: List[str], match_all: bool = False) -> List[Dict]:
        """Search by tags."""
        results = []

        for entry in self.index.index_data.get("files", []):
            entry_tags = set(entry.get("tags", []))
            search_tags = set(tags)

            if match_all:
                if search_tags.issubset(entry_tags):
                    results.append(entry)
            else:
                if search_tags & entry_tags:
                    results.append(entry)

        return results

    def search_metadata(self, **kwargs) -> List[Dict]:
        """Search by metadata fields.

        Supported filters:
        - min_confidence: float (0-1)
        - max_confidence: float (0-1)
        - min_chunks: int
        - max_chunks: int
        - file_type: str (chat/document)
        """
        results = self.index.index_data.get("files", [])

        if "file_type" in kwargs:
            results = [f for f in results if f.get("type") == kwargs["file_type"]]

        if "min_confidence" in kwargs:
            results = [f for f in results if f.get("confidence", 0) >= kwargs["min_confidence"]]

        if "max_confidence" in kwargs:
            results = [f for f in results if f.get("confidence", 0) <= kwargs["max_confidence"]]

        if "min_chunks" in kwargs:
            results = [f for f in results if f.get("chunks", 1) >= kwargs["min_chunks"]]

        if "max_chunks" in kwargs:
            results = [f for f in results if f.get("chunks", 1) <= kwargs["max_chunks"]]

        return results

    def advanced_search(self, query: str, tags: Optional[List[str]] = None,
                       file_type: Optional[str] = None,
                       min_confidence: float = 0.0) -> List[Dict]:
        """Combined search: full-text + filters."""
        # Start with full-text results
        results = self.search_full_text(query, file_type)

        # Apply tag filter
        if tags:
            result_files = set(r["source_file"] for r in results)
            tagged = self.search_by_tags(tags, match_all=False)
            tagged_files = set(t["source_file"] for t in tagged)
            results = [r for r in results if r["source_file"] in result_files & tagged_files]

        # Apply confidence filter
        results = [r for r in results if r["confidence"] >= min_confidence]

        return results

    @staticmethod
    def _extract_context(text: str, query: str, context_chars: int = 200) -> List[str]:
        """Extract text snippets around matches."""
        matches = []
        escaped_query = re.escape(query)
        # Build regex pattern for context extraction with escaped braces
        pattern_str = "(?:.{0," + str(context_chars) + "})" + escaped_query + ".{0," + str(context_chars) + "}"
        pattern = re.compile(pattern_str, re.IGNORECASE | re.DOTALL)

        for match in pattern.finditer(text):
            snippet = match.group(0).replace('\n', ' ')
            matches.append(f"...{snippet}...")

        return matches[:3]  # Return max 3 matches

    def get_recommendations(self, source_file: str) -> List[Dict]:
        """Get related files based on tags."""
        # Find the original entry
        entry = next((f for f in self.index.index_data.get("files", [])
                     if f["source_file"] == source_file), None)

        if not entry:
            return []

        # Find files with overlapping tags
        entry_tags = set(entry.get("tags", []))
        recommendations = []

        for other in self.index.index_data.get("files", []):
            if other["source_file"] == source_file:
                continue

            other_tags = set(other.get("tags", []))
            overlap = entry_tags & other_tags

            if overlap:
                recommendations.append({
                    "source_file": other["source_file"],
                    "type": other.get("type"),
                    "shared_tags": list(overlap),
                    "overlap_count": len(overlap),
                    "confidence": other.get("confidence", 0)
                })

        # Sort by overlap count
        recommendations.sort(key=lambda x: x["overlap_count"], reverse=True)
        return recommendations[:5]  # Return top 5

    def format_search_results(self, results: List[Dict], include_preview: bool = True) -> str:
        """Format search results for display."""
        if not results:
            return "No results found."

        output = f"Found {len(results)} result(s):\n\n"

        for i, result in enumerate(results, 1):
            output += f"{i}. **{Path(result['source_file']).name}** ({result.get('type', 'unknown')})\n"
            output += f"   Confidence: {result.get('confidence', 'N/A')}\n"
            output += f"   Tags: {', '.join(result.get('tags', []))}\n"

            if include_preview and result.get("preview"):
                output += f"   Preview: {result['preview'][:150]}...\n"

            output += f"   File: `{result.get('condensed_file', 'N/A')}`\n\n"

        return output


if __name__ == "__main__":
    import sys

    archive_root = Path(".kb/project/context-archive")
    search = ArchiveSearch(archive_root)

    if len(sys.argv) < 2:
        print("Usage: python archive_search.py <query> [--type chat|document] [--tag tag1,tag2]")
        sys.exit(1)

    query = sys.argv[1]
    file_type = None
    tags = []

    if "--type" in sys.argv:
        file_type = sys.argv[sys.argv.index("--type") + 1]

    if "--tag" in sys.argv:
        tags = sys.argv[sys.argv.index("--tag") + 1].split(",")

    results = search.advanced_search(query, tags, file_type)
    print(search.format_search_results(results))
