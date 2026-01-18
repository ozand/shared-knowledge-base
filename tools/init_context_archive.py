#!/usr/bin/env python3
"""
Initialize Context Archive structure and configuration.
Sets up directories, config files, and templates.
"""

import sys
from pathlib import Path
from datetime import datetime
import yaml


def initialize_archive(archive_root: Path | None = None) -> bool:
    """Initialize context archive structure."""
    if archive_root is None:
        archive_root = Path(".kb/project/context-archive")
    else:
        archive_root = Path(archive_root)

    # Create directory structure
    directories = [
        archive_root / "sources" / "chats",
        archive_root / "sources" / "documents",
        archive_root / "condensed" / "chats",
        archive_root / "condensed" / "documents",
        archive_root / "index",
        archive_root / "metadata"
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {directory}")

    # Create initial config
    config = {
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "archive_root": str(archive_root),
        "settings": {
            "condensing_model": "claude-opus-4-5-20251101",
            "chunk_size": 12000,
            "confidence_threshold": 0.6,
            "auto_tagging": True
        },
        "retention": {
            "keep_source_files": True,
            "keep_processing_logs": True,
            "archive_old_condensed_after_days": 365
        }
    }

    config_file = archive_root / "archive-config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    print(f"✓ Created: {config_file}")

    # Create README
    readme = """# Context Archive

This directory contains condensed summaries of large files and chat logs for quick context retrieval.

## Structure

- **sources/**: Original files (read-only or linked)
  - chats/: Exported chat sessions
  - documents/: Large documentation files
- **condensed/**: AI-generated summaries
  - chats/: Condensed chat summaries
  - documents/: Condensed document summaries
- **index/**: Archive catalog and search index
- **metadata/**: Processing logs and statistics

## Quick Commands

```bash
# Search condensed files
python tools/archive_search.py "query"

# Condense a new file (runs in background)
/context-condense path/to/file.txt

# View archive statistics
python tools/archive_index.py

# Search by tags
python tools/archive_search.py "query" --tag tag1,tag2
```

## File Naming Convention

- Condensed files: `{original_name}.condensed.md`
- Example: `2026-01-18-feature-discussion.txt` → `2026-01-18-feature-discussion.condensed.md`

## Metadata Format

Each condensed file includes YAML frontmatter with:
- `source_file`: Original file path
- `processed_at`: Timestamp
- `chunks_processed`: Number of chunks analyzed
- `confidence_score`: 0-1 confidence in summary
- `tags`: Auto-extracted topics
- `file_hash`: Source file hash (for change detection)

## Search Features

1. **Full-text search**: `archive_search.py "keyword"`
2. **Tag-based search**: `archive_search.py "" --tag authentication,security`
3. **Metadata filters**: Search by confidence, type, chunk count
4. **Recommendations**: Find related files by tags

## Workflow

1. Run `/context-condense file.txt` (or provide via UI)
2. Background agent processes file in chunks
3. Claude creates local summaries for each chunk
4. Summaries are merged and deduplicated
5. Index is updated automatically
6. Condensed file is saved with metadata
7. You can now search/reference in future conversations
"""

    readme_file = archive_root / "README.md"
    with open(readme_file, 'w') as f:
        f.write(readme)
    print(f"✓ Created: {readme_file}")

    # Create .gitignore for sources (keep them out of git)
    gitignore = """# Large source files - keep these locally only
sources/
*.orig
*.bak
*.tmp

# Keep condensed files in git
!condensed/
!index/
!metadata/
"""

    gitignore_file = archive_root / ".gitignore"
    with open(gitignore_file, 'w') as f:
        f.write(gitignore)
    print(f"✓ Created: {gitignore_file}")

    # Create sample links file
    links_sample = """# External File References
# Use this file to link to files that shouldn't be copied into the archive
# Format: source_file: file_path_or_url

# Example:
# production_logs: /var/log/app.log
# api_docs: https://docs.example.com/api
"""

    links_file = archive_root / "sources" / "links.yaml"
    with open(links_file, 'w') as f:
        f.write(links_sample)
    print(f"✓ Created: {links_file}")

    print(f"\n✓ Archive initialized at: {archive_root}")
    print(f"\nNext steps:")
    print(f"1. Add source files to: {archive_root}/sources/")
    print(f"2. Run: /context-condense <file>")
    print(f"3. Search with: python tools/archive_search.py 'query'")

    return True


if __name__ == "__main__":
    archive_path = Path(".kb/project/context-archive")
    if len(sys.argv) > 1:
        archive_path = Path(sys.argv[1])

    try:
        initialize_archive(archive_path)
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
