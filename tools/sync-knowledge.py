#!/usr/bin/env python3
"""
Knowledge Base Sync Tool

Sync shared knowledge from other projects based on scope.

Usage:
    python sync-knowledge.py --config sync-config.yaml
    python sync-knowledge.py --source /path/to/project --scope python universal
    python sync-knowledge.py --list-sources
"""

import argparse
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class KnowledgeSync:
    """Sync knowledge base from multiple projects."""

    def __init__(self, target_path: Path):
        self.target_path = target_path
        self.shared_path = target_path / "shared"
        self.shared_path.mkdir(exist_ok=True)

    def sync_from_project(
        self,
        source_project: Path,
        scopes: List[str],
        dry_run: bool = False
    ) -> Dict[str, int]:
        """Sync knowledge from a source project."""
        stats = {"errors": 0, "patterns": 0, "files": 0}

        source_kb = source_project / "docs/knowledge-base"
        if not source_kb.exists():
            print(f"Warning: No knowledge base found in {source_project}")
            return stats

        # Process each YAML file
        for yaml_file in source_kb.rglob("*.yaml"):
            # Skip shared directory to avoid recursion
            if "shared" in yaml_file.parts:
                continue

            with yaml_file.open(encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    print(f"Warning: Failed to parse {yaml_file}: {e}")
                    continue

            # Filter errors by scope
            filtered_errors = []
            if "errors" in data:
                for error in data["errors"]:
                    error_scope = error.get("scope", "project")
                    if error_scope in scopes:
                        filtered_errors.append(error)
                        stats["errors"] += 1

            # Filter patterns by scope
            filtered_patterns = []
            if "patterns" in data:
                for pattern in data["patterns"]:
                    pattern_scope = pattern.get("scope", "project")
                    if pattern_scope in scopes:
                        filtered_patterns.append(pattern)
                        stats["patterns"] += 1

            # Write filtered content if not dry run
            if (filtered_errors or filtered_patterns) and not dry_run:
                category = data.get("category", "unknown")
                output_file = self.shared_path / f"{category}-shared.yaml"

                output_data = {
                    "version": data.get("version", "1.0"),
                    "category": category,
                    "source": "shared",
                    "source_project": source_project.name,
                    "synced_at": datetime.now().isoformat(),
                    "scopes": scopes,
                }

                if filtered_errors:
                    output_data["errors"] = filtered_errors
                if filtered_patterns:
                    output_data["patterns"] = filtered_patterns

                with output_file.open("w", encoding="utf-8") as f:
                    yaml.dump(output_data, f, default_flow_style=False, allow_unicode=True)

                stats["files"] += 1

                print(f"✓ Synced {category} from {source_project.name}")

        return stats

    def sync_from_config(self, config_path: Path, dry_run: bool = False):
        """Sync from configuration file."""
        with config_path.open(encoding="utf-8") as f:
            config = yaml.safe_load(f)

        sources = config.get("sources", [])
        scopes = config.get("scopes", ["universal", "python"])

        total_stats = {"errors": 0, "patterns": 0, "files": 0}

        for source_config in sources:
            source_path = Path(source_config["path"]).expanduser()
            source_scopes = source_config.get("scopes", scopes)

            print(f"\nSyncing from: {source_path}")
            print(f"Scopes: {', '.join(source_scopes)}")

            stats = self.sync_from_project(source_path, source_scopes, dry_run)

            for key in total_stats:
                total_stats[key] += stats[key]

        return total_stats


def create_sample_config(output_path: Path):
    """Create sample sync configuration file."""
    config = {
        "sources": [
            {
                "name": "Project A",
                "path": "/path/to/project-a",
                "scopes": ["universal", "python", "fastapi"]
            },
            {
                "name": "Project B",
                "path": "/path/to/project-b",
                "scopes": ["universal", "python", "docker"]
            }
        ],
        "scopes": ["universal", "python"],
        "exclude_tags": ["project-specific"],
    }

    with output_path.open("w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False)

    print(f"Created sample config: {output_path}")


def list_sources(config_path: Path):
    """List configured sources."""
    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        return

    with config_path.open(encoding="utf-8") as f:
        config = yaml.safe_load(f)

    sources = config.get("sources", [])

    print("\nConfigured Knowledge Sources:\n")
    for i, source in enumerate(sources, 1):
        print(f"{i}. {source.get('name', 'Unknown')}")
        print(f"   Path: {source.get('path')}")
        print(f"   Scopes: {', '.join(source.get('scopes', []))}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Sync shared knowledge from other projects"
    )
    parser.add_argument("--config", type=Path,
                       default="docs/knowledge-base/sync-config.yaml",
                       help="Path to sync configuration file")
    parser.add_argument("--source", type=Path,
                       help="Source project path (alternative to config)")
    parser.add_argument("--scope", nargs="+",
                       default=["universal", "python"],
                       help="Scopes to sync")
    parser.add_argument("--target", type=Path,
                       default="docs/knowledge-base",
                       help="Target knowledge base path")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be synced without writing")
    parser.add_argument("--create-config", action="store_true",
                       help="Create sample configuration file")
    parser.add_argument("--list-sources", action="store_true",
                       help="List configured sources")

    args = parser.parse_args()

    # Create sample config if requested
    if args.create_config:
        create_sample_config(args.config)
        return

    # List sources if requested
    if args.list_sources:
        list_sources(args.config)
        return

    # Initialize syncer
    syncer = KnowledgeSync(args.target)

    # Sync from single source or config
    if args.source:
        print(f"Syncing from: {args.source}")
        print(f"Scopes: {', '.join(args.scope)}")
        if args.dry_run:
            print("(Dry run - no files will be written)\n")

        stats = syncer.sync_from_project(args.source, args.scope, args.dry_run)

        print(f"\n{'='*50}")
        print(f"Sync Summary:")
        print(f"  Errors synced: {stats['errors']}")
        print(f"  Patterns synced: {stats['patterns']}")
        print(f"  Files created: {stats['files']}")

    elif args.config.exists():
        if args.dry_run:
            print("(Dry run - no files will be written)\n")

        stats = syncer.sync_from_config(args.config, args.dry_run)

        print(f"\n{'='*50}")
        print(f"Sync Summary:")
        print(f"  Errors synced: {stats['errors']}")
        print(f"  Patterns synced: {stats['patterns']}")
        print(f"  Files created: {stats['files']}")

    else:
        print(f"Error: Config file not found: {args.config}")
        print(f"Use --create-config to create a sample configuration")
        sys.exit(1)


if __name__ == "__main__":
    main()
