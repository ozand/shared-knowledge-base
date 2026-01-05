#!/usr/bin/env python3
"""
kb_meta.py - Knowledge Base Metadata Manager

Manages metadata files for knowledge base entries.
Creates and updates _meta.yaml files alongside knowledge entries.

Author: Knowledge Base Curator
Version: 1.0.0
License: MIT
"""

import yaml
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import hashlib


class MetadataManager:
    """Manage knowledge base metadata files."""

    def __init__(self, kb_root: Optional[Path] = None):
        """
        Initialize MetadataManager.

        Args:
            kb_root: Root directory of knowledge base (defaults to cwd)
        """
        self.kb_root = kb_root or Path.cwd()
        self.cache_dir = self.kb_root / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _generate_file_id(self, yaml_file: Path) -> str:
        """
        Generate unique file ID from path.

        Args:
            yaml_file: Path to YAML file

        Returns:
            Unique file identifier
        """
        try:
            rel_path = yaml_file.relative_to(self.kb_root)
        except ValueError:
            # File is not under kb_root, use absolute path
            rel_path = yaml_file

        return str(rel_path).replace('/', '-').replace('\\', '-').replace('.yaml', '')

    def _calculate_entry_hash(self, entry_data: Dict) -> str:
        """
        Calculate hash of entry content for change detection.

        Args:
            entry_data: Entry dictionary

        Returns:
            SHA256 hash of entry content
        """
        # Serialize entry content deterministically
        content = json.dumps(entry_data, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def _create_entry_metadata(self, entry_id: str, entry_data: Dict) -> Dict:
        """
        Create initial metadata for an entry.

        Args:
            entry_id: Entry identifier (e.g., IMPORT-001)
            entry_data: Entry data from YAML

        Returns:
            Metadata dictionary for entry
        """
        now = datetime.now().isoformat() + "Z"
        entry_hash = self._calculate_entry_hash(entry_data)

        return {
            # Basic info
            "entry_id": entry_id,
            "content_hash": entry_hash,

            # Creation tracking
            "created_at": now,
            "created_by": "unknown",

            # Modification tracking
            "last_modified": now,
            "last_modified_by": "unknown",

            # Analysis tracking
            "last_analyzed_at": None,
            "last_analyzed_by": None,
            "analysis_version": 0,

            # Quality tracking
            "quality_score": None,
            "quality_assessed_at": None,
            "quality_assessed_by": None,
            "quality_dimensions": {},

            # Research tracking
            "last_researched_at": None,
            "research_sources": [],
            "research_version": 0,

            # Validation status
            "validation_status": "needs_review",  # needs_review | validated | outdated | deprecated
            "validated_at": None,
            "validated_against_version": None,

            # Version tracking
            "tested_versions": {},
            "requires_version_check": True,
            "next_version_check_due": (datetime.now() + timedelta(days=90)).isoformat() + "Z",

            # Deprecation
            "is_deprecated": False,
            "deprecated_at": None,
            "deprecated_by": None,
            "superseded_by": None
        }

    def create_meta_file(self, yaml_file: Path) -> Path:
        """
        Create _meta.yaml file alongside a YAML file.

        Args:
            yaml_file: Path to knowledge entry YAML file

        Returns:
            Path to created metadata file
        """
        meta_file = yaml_file.parent / f"{yaml_file.stem}_meta.yaml"

        # Check if already exists
        if meta_file.exists():
            print(f"✓ Metadata already exists: {meta_file.relative_to(self.kb_root)}")
            return meta_file

        # Load the YAML file to extract entries
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"✗ Error reading {yaml_file}: {e}")
            return None

        # Create metadata structure
        now = datetime.now().isoformat() + "Z"
        entry_ids = []

        if 'errors' in data:
            entry_ids = [error.get('id') for error in data['errors'] if error.get('id')]
        elif 'patterns' in data:
            entry_ids = [pattern.get('id') for pattern in data['patterns'] if pattern.get('id')]

        meta = {
            "version": "1.0",
            "file_metadata": {
                "file_id": self._generate_file_id(yaml_file),
                "created_at": now,
                "created_by": "kb-meta-tool",
                "last_modified": now,
                "last_modified_by": "kb-meta-tool",
                "version": 1,
                "entry_count": len(entry_ids)
            },
            "entries": {},
            "analytics": {
                "total_access_count": 0,
                "first_accessed_at": None,
                "last_accessed_at": None,
                "access_history_summary": []
            },
            "change_history": [
                {
                    "timestamp": now,
                    "action": "created",
                    "agent": "kb-meta-tool",
                    "entries_affected": entry_ids,
                    "reason": "Initial metadata creation"
                }
            ]
        }

        # Initialize entry metadata
        if 'errors' in data:
            for error in data['errors']:
                entry_id = error.get('id')
                if entry_id:
                    meta['entries'][entry_id] = self._create_entry_metadata(entry_id, error)

        if 'patterns' in data:
            for pattern in data['patterns']:
                entry_id = pattern.get('id')
                if entry_id:
                    meta['entries'][entry_id] = self._create_entry_metadata(entry_id, pattern)

        # Write metadata file
        try:
            with open(meta_file, 'w', encoding='utf-8') as f:
                yaml.dump(meta, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

            print(f"✓ Created metadata: {meta_file.relative_to(self.kb_root)} ({len(entry_ids)} entries)")
            return meta_file

        except Exception as e:
            print(f"✗ Error writing {meta_file}: {e}")
            return None

    def load_meta_file(self, yaml_file: Path) -> Optional[Dict]:
        """
        Load metadata file for a YAML file.

        Args:
            yaml_file: Path to knowledge entry YAML file

        Returns:
            Metadata dictionary or None if not found
        """
        meta_file = yaml_file.parent / f"{yaml_file.stem}_meta.yaml"

        if not meta_file.exists():
            return None

        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"✗ Error loading {meta_file}: {e}")
            return None

    def update_entry_metadata(
        self,
        yaml_file: Path,
        entry_id: str,
        updates: Dict[str, Any],
        agent: str = "unknown",
        reason: str = ""
    ) -> Optional[Dict]:
        """
        Update metadata for a specific entry.

        Args:
            yaml_file: Path to knowledge entry YAML file
            entry_id: Entry identifier
            updates: Dictionary of fields to update
            agent: Agent making the update
            reason: Reason for update

        Returns:
            Updated entry metadata or None on error
        """
        meta_file = yaml_file.parent / f"{yaml_file.stem}_meta.yaml"

        # Create metadata if doesn't exist
        if not meta_file.exists():
            self.create_meta_file(yaml_file)

        # Load metadata
        with open(meta_file, 'r', encoding='utf-8') as f:
            meta = yaml.safe_load(f)

        if entry_id not in meta['entries']:
            print(f"✗ Entry {entry_id} not found in metadata")
            return None

        # Apply updates
        entry_meta = meta['entries'][entry_id]
        now = datetime.now().isoformat() + "Z"

        # Update last_modified
        entry_meta['last_modified'] = now
        entry_meta['last_modified_by'] = agent

        # Apply specific updates
        for key, value in updates.items():
            entry_meta[key] = value

        # Update file metadata
        meta['file_metadata']['last_modified'] = now
        meta['file_metadata']['last_modified_by'] = agent
        meta['file_metadata']['version'] += 1

        # Add to change history
        change_entry = {
            "timestamp": now,
            "action": updates.get('action', 'updated'),
            "agent": agent,
            "entries_affected": [entry_id],
            "reason": reason
        }

        # Add details if available
        if 'quality_score' in updates:
            change_entry['quality_score'] = updates['quality_score']
        if 'validation_status' in updates:
            change_entry['validation_status'] = updates['validation_status']

        meta['change_history'].append(change_entry)

        # Write back
        try:
            with open(meta_file, 'w', encoding='utf-8') as f:
                yaml.dump(meta, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

            return entry_meta

        except Exception as e:
            print(f"✗ Error writing {meta_file}: {e}")
            return None

    def get_entry_metadata(self, yaml_file: Path, entry_id: str) -> Optional[Dict]:
        """
        Get metadata for a specific entry.

        Args:
            yaml_file: Path to knowledge entry YAML file
            entry_id: Entry identifier

        Returns:
            Entry metadata dictionary or None if not found
        """
        meta = self.load_meta_file(yaml_file)

        if not meta:
            return None

        return meta['entries'].get(entry_id)

    def find_all_meta_files(self) -> List[Path]:
        """
        Find all metadata files in knowledge base.

        Returns:
            List of paths to _meta.yaml files
        """
        return list(self.kb_root.rglob("*_meta.yaml"))

    def get_all_entries_metadata(self) -> Dict[str, Dict]:
        """
        Load metadata for all entries in the knowledge base.

        Returns:
            Dictionary mapping entry_id to metadata with file info
        """
        all_entries = {}

        for meta_file in self.find_all_meta_files():
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta = yaml.safe_load(f)

                yaml_file = meta_file.parent / meta_file.stem.replace('_meta', '.yaml')

                for entry_id, entry_meta in meta.get('entries', {}).items():
                    all_entries[entry_id] = {
                        'metadata': entry_meta,
                        'file': str(yaml_file.relative_to(self.kb_root)),
                        'meta_file': str(meta_file.relative_to(self.kb_root))
                    }

            except Exception as e:
                print(f"✗ Error loading {meta_file}: {e}")

        return all_entries


def main():
    """CLI interface for metadata management."""
    import argparse

    parser = argparse.ArgumentParser(description="Knowledge Base Metadata Manager")
    parser.add_argument('action', choices=['init', 'list', 'update'],
                       help='Action to perform')
    parser.add_argument('--kb-root', type=Path, default=Path.cwd(),
                       help='Knowledge base root directory')
    parser.add_argument('--file', type=Path,
                       help='Specific YAML file to process')
    parser.add_argument('--entry-id',
                       help='Entry ID to update')
    parser.add_argument('--field',
                       help='Field to update')
    parser.add_argument('--value',
                       help='Value to set')

    args = parser.parse_args()
    manager = MetadataManager(args.kb_root)

    if args.action == 'init':
        if args.file:
            # Initialize metadata for specific file
            manager.create_meta_file(args.file)
        else:
            # Initialize metadata for all YAML files
            print("Initializing metadata for all YAML files...")
            yaml_files = []
            for ext in ['*.yaml', '*.yml']:
                yaml_files.extend(args.kb_root.rglob(ext))

            # Skip meta files and cache
            yaml_files = [f for f in yaml_files
                         if '_meta.yaml' not in str(f)
                         and '.cache' not in str(f)]

            for yaml_file in yaml_files:
                manager.create_meta_file(yaml_file)

            print(f"\n✓ Processed {len(yaml_files)} files")

    elif args.action == 'list':
        all_entries = manager.get_all_entries_metadata()
        print(f"\n📊 Total entries: {len(all_entries)}\n")

        # Group by validation status
        by_status = {}
        for entry_id, data in all_entries.items():
            status = data['metadata'].get('validation_status', 'unknown')
            by_status.setdefault(status, [])
            by_status[status].append(entry_id)

        for status, entries in sorted(by_status.items()):
            print(f"{status}: {len(entries)}")

    elif args.action == 'update':
        if not args.file or not args.entry_id or not args.field:
            print("--file, --entry-id, and --field required for update")
            return

        updates = {args.field: args.value}
        result = manager.update_entry_metadata(
            args.file,
            args.entry_id,
            updates,
            agent="cli",
            reason="Manual update"
        )

        if result:
            print(f"✓ Updated {args.entry_id}: {args.field} = {args.value}")
        else:
            print(f"✗ Update failed")


if __name__ == '__main__':
    main()
