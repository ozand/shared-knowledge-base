#!/usr/bin/env python3
"""
kb_changes.py - Knowledge Base Change Detector

Detects changes in knowledge base entries using hash-based comparison.
Identifies new, modified, and deleted entries.

Author: Knowledge Base Curator
Version: 1.0.0
License: MIT
"""

import yaml
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class ChangeDetector:
    """Detect changes in knowledge base entries."""

    def __init__(self, kb_root: Optional[Path] = None, cache_dir: Optional[Path] = None):
        """
        Initialize ChangeDetector.

        Args:
            kb_root: Root directory of knowledge base
            cache_dir: Cache directory for hash storage
        """
        self.kb_root = kb_root or Path.cwd()
        self.cache_dir = cache_dir or self.kb_root / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.hash_file = self.cache_dir / "file_hashes.json"

    def calculate_entry_hash(self, yaml_file: Path, entry_id: str) -> Optional[str]:
        """
        Calculate hash of entry content.

        Args:
            yaml_file: Path to YAML file
            entry_id: Entry identifier

        Returns:
            SHA256 hash or None if entry not found
        """
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if 'errors' in data:
                for error in data['errors']:
                    if error.get('id') == entry_id:
                        # Serialize entry content deterministically
                        content = json.dumps(error, sort_keys=True)
                        return hashlib.sha256(content.encode()).hexdigest()

            elif 'patterns' in data:
                for pattern in data['patterns']:
                    if pattern.get('id') == entry_id:
                        content = json.dumps(pattern, sort_keys=True)
                        return hashlib.sha256(content.encode()).hexdigest()

        except Exception as e:
            print(f"✗ Error hashing {entry_id} from {yaml_file}: {e}")

        return None

    def calculate_file_hash(self, yaml_file: Path) -> str:
        """
        Calculate hash of entire YAML file.

        Args:
            yaml_file: Path to YAML file

        Returns:
            SHA256 hash of file contents
        """
        try:
            with open(yaml_file, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            print(f"✗ Error hashing file {yaml_file}: {e}")
            return ""

    def scan_all_entries(self) -> Dict:
        """
        Scan all entries and calculate hashes.

        Returns:
            Dictionary with entry_hashes and file_hashes
        """
        hashes = {
            "entry_hashes": {},
            "file_hashes": {}
        }

        # Find all YAML files
        yaml_files = []
        for ext in ['*.yaml', '*.yml']:
            yaml_files.extend(self.kb_root.rglob(ext))

        # Skip meta files and cache
        yaml_files = [
            f for f in yaml_files
            if '_meta.yaml' not in str(f)
            and '.cache' not in str(f)
        ]

        for yaml_file in yaml_files:
            # Calculate file hash
            file_hash = self.calculate_file_hash(yaml_file)
            rel_path = str(yaml_file.relative_to(self.kb_root))
            hashes["file_hashes"][rel_path] = file_hash

            # Calculate entry hashes
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                if 'errors' in data:
                    for error in data['errors']:
                        entry_id = error.get('id')
                        if entry_id:
                            entry_hash = self.calculate_entry_hash(yaml_file, entry_id)
                            if entry_hash:
                                hashes["entry_hashes"][entry_id] = {
                                    "hash": entry_hash,
                                    "file": rel_path
                                }

                elif 'patterns' in data:
                    for pattern in data['patterns']:
                        entry_id = pattern.get('id')
                        if entry_id:
                            entry_hash = self.calculate_entry_hash(yaml_file, entry_id)
                            if entry_hash:
                                hashes["entry_hashes"][entry_id] = {
                                    "hash": entry_hash,
                                    "file": rel_path
                                }

            except Exception as e:
                print(f"✗ Error processing {yaml_file}: {e}")

        return hashes

    def save_hashes(self, hashes: Dict):
        """
        Save hashes to cache file.

        Args:
            hashes: Hash dictionary from scan_all_entries
        """
        hashes["last_scan"] = datetime.now().isoformat() + "Z"
        hashes["version"] = "1.0"

        with open(self.hash_file, 'w', encoding='utf-8') as f:
            json.dump(hashes, f, indent=2)

    def load_hashes(self) -> Optional[Dict]:
        """
        Load hashes from cache file.

        Returns:
            Hash dictionary or None if file doesn't exist
        """
        if not self.hash_file.exists():
            return None

        try:
            with open(self.hash_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"✗ Error loading hashes: {e}")
            return None

    def detect_changes(self) -> Dict:
        """
        Detect changes since last scan.

        Returns:
            Dictionary with new_entries, modified_entries, deleted_entries
        """
        old_hashes = self.load_hashes()

        if old_hashes is None:
            # First scan - save current state and return initial scan info
            print("🔍 Initial scan - no previous hash data")
            current_hashes = self.scan_all_entries()
            self.save_hashes(current_hashes)

            return {
                "type": "initial_scan",
                "timestamp": datetime.now().isoformat() + "Z",
                "total_entries": len(current_hashes["entry_hashes"]),
                "total_files": len(current_hashes["file_hashes"]),
                "entries": list(current_hashes["entry_hashes"].keys())
            }

        # Scan current state
        current_hashes = self.scan_all_entries()

        changes = {
            "type": "changes_detected",
            "timestamp": datetime.now().isoformat() + "Z",
            "new_entries": [],
            "modified_entries": [],
            "deleted_entries": [],
            "new_files": [],
            "modified_files": []
        }

        # Detect new and modified entries
        for entry_id, current_data in current_hashes["entry_hashes"].items():
            if entry_id not in old_hashes["entry_hashes"]:
                changes["new_entries"].append({
                    "entry_id": entry_id,
                    "file": current_data["file"],
                    "hash": current_data["hash"]
                })
            elif old_hashes["entry_hashes"][entry_id]["hash"] != current_data["hash"]:
                changes["modified_entries"].append({
                    "entry_id": entry_id,
                    "file": current_data["file"],
                    "old_hash": old_hashes["entry_hashes"][entry_id]["hash"],
                    "new_hash": current_data["hash"]
                })

        # Detect deleted entries
        for entry_id in old_hashes["entry_hashes"]:
            if entry_id not in current_hashes["entry_hashes"]:
                changes["deleted_entries"].append({
                    "entry_id": entry_id,
                    "was_in": old_hashes["entry_hashes"][entry_id]["file"]
                })

        # Detect new and modified files
        for file_path, file_hash in current_hashes["file_hashes"].items():
            if file_path not in old_hashes["file_hashes"]:
                changes["new_files"].append({
                    "file": file_path,
                    "hash": file_hash
                })
            elif old_hashes["file_hashes"][file_path] != file_hash:
                changes["modified_files"].append({
                    "file": file_path,
                    "old_hash": old_hashes["file_hashes"][file_path],
                    "new_hash": file_hash
                })

        # Save current hashes
        self.save_hashes(current_hashes)

        return changes

    def get_changes_summary(self, changes: Dict) -> str:
        """
        Get human-readable summary of changes.

        Args:
            changes: Changes dictionary from detect_changes

        Returns:
            Formatted summary string
        """
        if changes["type"] == "initial_scan":
            return f"""
📊 Initial Scan Results
   Timestamp: {changes['timestamp']}
   Total entries: {changes['total_entries']}
   Total files: {changes['total_files']}
"""

        summary = f"""
🔄 Changes Detected
   Timestamp: {changes['timestamp']}

📈 Summary:
   New entries: {len(changes['new_entries'])}
   Modified entries: {len(changes['modified_entries'])}
   Deleted entries: {len(changes['deleted_entries'])}
   New files: {len(changes['new_files'])}
   Modified files: {len(changes['modified_files'])}
"""

        if changes['new_entries']:
            summary += "\n✅ New Entries:\n"
            for item in changes['new_entries']:
                summary += f"   - {item['entry_id']} in {item['file']}\n"

        if changes['modified_entries']:
            summary += "\n📝 Modified Entries:\n"
            for item in changes['modified_entries']:
                summary += f"   - {item['entry_id']} in {item['file']}\n"

        if changes['deleted_entries']:
            summary += "\n🗑️  Deleted Entries:\n"
            for item in changes['deleted_entries']:
                summary += f"   - {item['entry_id']} (was in {item['was_in']})\n"

        return summary

    def force_rescan(self):
        """Force a fresh scan by deleting hash cache."""
        if self.hash_file.exists():
            self.hash_file.unlink()
            print("✓ Hash cache deleted - next scan will be a fresh scan")
        else:
            print("✓ No hash cache found")


def main():
    """CLI interface for change detection."""
    import argparse

    parser = argparse.ArgumentParser(description="Knowledge Base Change Detector")
    parser.add_argument('action', choices=['detect', 'scan', 'rescan', 'status'],
                       help='Action to perform')
    parser.add_argument('--kb-root', type=Path, default=Path.cwd(),
                       help='Knowledge base root directory')
    parser.add_argument('--cache-dir', type=Path,
                       help='Cache directory path')
    parser.add_argument('--json', action='store_true',
                       help='Output in JSON format')

    args = parser.parse_args()

    if args.cache_dir:
        cache_dir = args.cache_dir
    else:
        cache_dir = args.kb_root / ".cache"

    detector = ChangeDetector(args.kb_root, cache_dir)

    if args.action == 'detect':
        changes = detector.detect_changes()

        if args.json:
            print(json.dumps(changes, indent=2))
        else:
            print(detector.get_changes_summary(changes))

    elif args.action == 'scan':
        print("🔍 Scanning all entries...")
        hashes = detector.scan_all_entries()
        detector.save_hashes(hashes)

        print(f"\n✓ Scan complete")
        print(f"  Total entries: {len(hashes['entry_hashes'])}")
        print(f"  Total files: {len(hashes['file_hashes'])}")

    elif args.action == 'rescan':
        detector.force_rescan()
        print("\n💡 Run 'detect' to perform a fresh scan")

    elif args.action == 'status':
        hashes = detector.load_hashes()

        if hashes is None:
            print("📊 No previous scan found")
            print("   Run 'scan' or 'detect' to create baseline")
        else:
            print(f"📊 Last Scan: {hashes.get('last_scan', 'unknown')}")
            print(f"   Entries: {len(hashes['entry_hashes'])}")
            print(f"   Files: {len(hashes['file_hashes'])}")


if __name__ == '__main__':
    main()
