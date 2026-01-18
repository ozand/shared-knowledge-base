#!/usr/bin/env python3
"""
Archive Index Manager - Maintains catalog of condensed files.
Provides fast lookups and metadata tracking.
"""

import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class ArchiveIndex:
    """Manages the archive index (catalog of condensed files)."""

    def __init__(self, archive_root: Path):
        """Initialize index manager."""
        self.archive_root = Path(archive_root)
        self.index_file = self.archive_root / "index" / "archive-index.yaml"
        self.metadata_file = self.archive_root / "metadata" / "processing-log.yaml"
        self.index_data = self._load_index()

    def _load_index(self) -> Dict:
        """Load existing index or create new."""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                return yaml.safe_load(f) or {"files": [], "last_updated": None}
        return {"files": [], "last_updated": None}

    def _save_index(self):
        """Save index to disk."""
        self.index_file.parent.mkdir(parents=True, exist_ok=True)
        self.index_data["last_updated"] = datetime.now().isoformat()
        with open(self.index_file, 'w') as f:
            yaml.dump(self.index_data, f, default_flow_style=False)

    def add_entry(self, source_file: str, condensed_file: str, metadata: Dict):
        """Add condensed file to index."""
        entry = {
            "source_file": source_file,
            "condensed_file": condensed_file,
            "source_size_kb": metadata.get("source_size_bytes", 0) / 1024,
            "processed_at": metadata.get("processed_at"),
            "chunks": metadata.get("chunks_processed", 1),
            "confidence": metadata.get("confidence_score", 0),
            "tags": metadata.get("tags", []),
            "file_hash": metadata.get("file_hash"),
            "type": metadata.get("source_type", "chat")
        }

        # Check if already exists and update
        existing = next((f for f in self.index_data["files"]
                        if f["source_file"] == source_file), None)
        if existing:
            self.index_data["files"].remove(existing)

        self.index_data["files"].append(entry)
        self._save_index()

    def get_entries_by_tag(self, tag: str) -> List[Dict]:
        """Get all entries with specific tag."""
        return [f for f in self.index_data["files"] if tag in f.get("tags", [])]

    def get_entries_by_type(self, file_type: str) -> List[Dict]:
        """Get all entries of specific type (chat/document)."""
        return [f for f in self.index_data["files"] if f.get("type") == file_type]

    def search_entries(self, query: str) -> List[Dict]:
        """Search entries by various fields."""
        query_lower = query.lower()
        results = []
        for entry in self.index_data["files"]:
            if (query_lower in entry.get("source_file", "").lower() or
                query_lower in " ".join(entry.get("tags", "")).lower()):
                results.append(entry)
        return results

    def get_all_tags(self) -> List[str]:
        """Get all unique tags in archive."""
        tags = set()
        for entry in self.index_data["files"]:
            tags.update(entry.get("tags", []))
        return sorted(list(tags))

    def get_stats(self) -> Dict:
        """Get archive statistics."""
        return {
            "total_files": len(self.index_data["files"]),
            "chat_files": len(self.get_entries_by_type("chat")),
            "document_files": len(self.get_entries_by_type("document")),
            "total_size_kb": sum(f.get("source_size_kb", 0)
                                for f in self.index_data["files"]),
            "avg_confidence": (sum(f.get("confidence", 0)
                                   for f in self.index_data["files"]) /
                             len(self.index_data["files"])
                             if self.index_data["files"] else 0),
            "unique_tags": len(self.get_all_tags()),
            "last_updated": self.index_data.get("last_updated")
        }

    def get_index_summary(self) -> str:
        """Get human-readable index summary."""
        stats = self.get_stats()
        tags = self.get_all_tags()

        summary = f"""
# Archive Index Summary

**Statistics:**
- Total Files: {stats['total_files']}
- Chat Files: {stats['chat_files']}
- Documents: {stats['document_files']}
- Total Size: {stats['total_size_kb']:.1f} KB
- Avg Confidence: {stats['avg_confidence']:.2f}
- Unique Tags: {stats['unique_tags']}
- Last Updated: {stats['last_updated']}

**All Tags:**
{', '.join(f'`{tag}`' for tag in tags)}

**Recent Files:**
"""
        # Sort by processed date, show last 5
        sorted_files = sorted(self.index_data["files"],
                            key=lambda f: f.get("processed_at", ""),
                            reverse=True)[:5]

        for f in sorted_files:
            summary += f"\n- **{Path(f['source_file']).name}** ({f['type']}) - {f['processed_at']}"

        return summary


class ProcessingLog:
    """Tracks processing history."""

    def __init__(self, log_file: Path):
        """Initialize log."""
        self.log_file = log_file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.entries = self._load_log()

    def _load_log(self) -> List[Dict]:
        """Load existing log or create new."""
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                return yaml.safe_load(f) or []
        return []

    def _save_log(self):
        """Save log to disk."""
        with open(self.log_file, 'w') as f:
            yaml.dump(self.entries, f, default_flow_style=False)

    def log_processing(self, source_file: str, result: Dict):
        """Log a processing event."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "source_file": source_file,
            "status": "success",
            "chunks_processed": result.get("chunks_processed"),
            "tokens_used": result.get("tokens_used"),
            "confidence": result.get("confidence_score"),
            "file_hash": result.get("file_hash")
        }
        self.entries.append(entry)
        self._save_log()

    def log_error(self, source_file: str, error: str):
        """Log a processing error."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "source_file": source_file,
            "status": "error",
            "error": error
        }
        self.entries.append(entry)
        self._save_log()

    def get_recent_entries(self, count: int = 10) -> List[Dict]:
        """Get recent log entries."""
        return self.entries[-count:]

    def get_stats(self) -> Dict:
        """Get processing statistics."""
        successful = [e for e in self.entries if e.get("status") == "success"]
        failed = [e for e in self.entries if e.get("status") == "error"]

        total_tokens = sum(e.get("tokens_used", 0) for e in successful)

        return {
            "total_processed": len(self.entries),
            "successful": len(successful),
            "failed": len(failed),
            "total_tokens_used": total_tokens,
            "avg_confidence": (sum(e.get("confidence", 0) for e in successful) /
                             len(successful) if successful else 0),
            "success_rate": (len(successful) / len(self.entries) * 100
                           if self.entries else 0)
        }


if __name__ == "__main__":
    # CLI interface
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Archive Index Manager")
    parser.add_argument("--register", help="Register a condensed file manually")
    parser.add_argument("--source", help="Original source file path (required for register)")
    parser.add_argument("--root", default=".kb/project/context-archive", help="Archive root")
    
    args = parser.parse_args()
    
    archive_root = Path(args.root)
    index = ArchiveIndex(archive_root)

    if args.register:
        if not args.source:
            print("❌ Error: --source is required when registering a file")
            sys.exit(1)
            
        condensed_path = Path(args.register)
        if not condensed_path.exists():
            print(f"❌ Error: Condensed file not found: {condensed_path}")
            sys.exit(1)
            
        # Try to read metadata from frontmatter
        import re
        with open(condensed_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Very basic frontmatter parsing
        metadata = {}
        fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            try:
                metadata = yaml.safe_load(fm_match.group(1))
            except:
                pass
        
        # Fallback/Override
        metadata["source_file"] = args.source
        
        index.add_entry(args.source, str(condensed_path), metadata)
        print(f"✅ Registered {condensed_path.name} in index")
        
    else:
        print(index.get_index_summary())
