#!/usr/bin/env python3
"""
Template Manager - Safe installation and updates for project guidelines.
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

class TemplateManager:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.domains_dir = repo_root / "domains"
        # Where templates are installed in the project
        self.target_dir = repo_root / "docs" / "guidelines"
        # Hash storage
        self.hash_file = repo_root / ".kb" / "project" / ".template_hashes.json"

    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file content."""
        if not file_path.exists():
            return ""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _load_hashes(self) -> dict:
        """Load stored template hashes."""
        if self.hash_file.exists():
            with open(self.hash_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_hashes(self, hashes: dict):
        """Save template hashes."""
        self.hash_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.hash_file, 'w') as f:
            json.dump(hashes, f, indent=2)

    def install_template(self, domain: str):
        """Install guidelines from a specific domain."""
        source_dir = self.domains_dir / domain / "guides"
        if not source_dir.exists():
            print(f"❌ Domain guidelines not found: {domain}")
            return

        print(f"📦 Installing guidelines from {domain}...")
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        stored_hashes = self._load_hashes()
        new_hashes = stored_hashes.copy()
        
        stats = {"added": 0, "updated": 0, "skipped": 0, "errors": 0}

        for source_file in source_dir.glob("**/*.md"):
            rel_path = source_file.relative_to(source_dir)
            target_file = self.target_dir / rel_path
            
            # Ensure target subdir exists
            target_file.parent.mkdir(parents=True, exist_ok=True)

            current_source_hash = self._calculate_hash(source_file)
            
            # Case 1: New file
            if not target_file.exists():
                shutil.copy2(source_file, target_file)
                new_hashes[str(rel_path)] = current_source_hash
                print(f"  ✅ Added: {rel_path}")
                stats["added"] += 1
                continue

            # Case 2: Existing file
            current_target_hash = self._calculate_hash(target_file)
            stored_hash = stored_hashes.get(str(rel_path))

            if current_target_hash == stored_hash:
                # File hasn't been modified by user, safe to update
                if current_target_hash != current_source_hash:
                    shutil.copy2(source_file, target_file)
                    new_hashes[str(rel_path)] = current_source_hash
                    print(f"  🔄 Updated: {rel_path}")
                    stats["updated"] += 1
                else:
                    # Already up to date
                    pass
            else:
                # User modified the file
                if current_target_hash != current_source_hash:
                    print(f"  ⏭️  Skipped (User Modified): {rel_path}")
                    stats["skipped"] += 1
                    
                    # Create .new version for reference
                    new_file = target_file.with_suffix(".md.new")
                    shutil.copy2(source_file, new_file)
                    print(f"     -> Saved update as {new_file.name}")

        self._save_hashes(new_hashes)
        
        print("\n📊 Update Summary:")
        print(f"   ✅ Added: {stats['added']}")
        print(f"   🔄 Updated: {stats['updated']}")
        print(f"   ⏭️  Skipped: {stats['skipped']}")

if __name__ == "__main__":
    # Test stub
    pass
