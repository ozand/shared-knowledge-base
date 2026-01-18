#!/usr/bin/env python3
"""
Capability Management Tool - Archive and Install capabilities (Agents, Skills, Hooks)
"""

import sys
import shutil
import argparse
from pathlib import Path
from typing import Optional
import yaml
import hashlib

def get_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of file content."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

class CapabilityManager:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.shared_dir = repo_root / "domains" / "claude-code"
        self.project_dir = repo_root / ".kb" / "project" / "domains" / "claude-code"
        self.local_dir = Path(".claude") # Standard location for active capabilities

    def archive(self, file_path: Path, cap_type: str, scope: str = "project", 
               name: Optional[str] = None, description: str = "Imported capability"):
        """Archive a local file into the capability store."""
        
        file_path = Path(file_path).resolve()
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return False

        if not name:
            name = file_path.stem

        # Determine destination
        base_dir = self.project_dir if scope == "project" else self.shared_dir
        dest_dir = base_dir / cap_type
        
        # Determine wrapper path
        wrapper_path = dest_dir / f"{name}.yaml"
        
        # Ensure destination directory exists
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Create wrapper content
        wrapper_data = {
            "version": "1.0",
            "type": cap_type.rstrip('s'), # skill, agent, hook
            "id": f"{cap_type.upper().rstrip('S')}-{name.upper()}-001",
            "metadata": {
                "name": name,
                "description": description,
                "tags": [cap_type.rstrip('s'), scope],
                "created_at": "2026-01-18", # In real usage, use datetime.now()
                "source_hash": get_hash(file_path)
            },
            "implementation": {
                "type": "file",
                "source": file_path.name,
                "language": file_path.suffix.lstrip('.') or "unknown"
            }
        }

        # 1. Copy source file
        dest_source_path = dest_dir / file_path.name
        shutil.copy2(file_path, dest_source_path)
        print(f"✓ Copied source to: {dest_source_path}")

        # 2. Write YAML wrapper
        with open(wrapper_path, 'w') as f:
            yaml.dump(wrapper_data, f, default_flow_style=False)
        print(f"✓ Created wrapper: {wrapper_path}")
        
        return True

    def install(self, name: str, cap_type: str):
        """Install a capability from the store to the local environment."""
        
        # Search in project then shared
        candidates = [
            self.project_dir / cap_type / f"{name}.yaml",
            self.shared_dir / cap_type / f"{name}.yaml"
        ]
        
        found_wrapper = None
        for cand in candidates:
            if cand.exists():
                found_wrapper = cand
                break
        
        if not found_wrapper:
            print(f"❌ Capability not found: {name} (checked project & shared tiers)")
            return False
            
        # Parse wrapper to find source
        with open(found_wrapper, 'r') as f:
            data = yaml.safe_load(f)
            
        source_name = data.get("implementation", {}).get("source")
        if not source_name:
            print(f"❌ Invalid wrapper: missing implementation source in {found_wrapper}")
            return False
            
        source_path = found_wrapper.parent / source_name
        if not source_path.exists():
            print(f"❌ Source file missing in store: {source_path}")
            return False
            
        # Determine install destination
        # .claude/skills, .claude/agents, etc.
        install_dir = self.local_dir / cap_type
        install_dir.mkdir(parents=True, exist_ok=True)
        
        dest_path = install_dir / source_name
        
        shutil.copy2(source_path, dest_path)
        print(f"✅ Installed {name} to {dest_path}")
        return True

if __name__ == "__main__":
    # Test stub
    pass
