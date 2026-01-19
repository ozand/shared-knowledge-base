#!/usr/bin/env python3
"""
Release Manager Tool
Helps agents create semantic releases and broadcast them to Company OS.
"""

import os
import sys
import yaml
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

class ReleaseManager:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.passport_path = repo_root / ".kb" / "project" / "PROJECT.yaml"

    def _get_current_version(self):
        """Get version from passport."""
        if not self.passport_path.exists():
            return "0.0.0"
        with open(self.passport_path, 'r') as f:
            data = yaml.safe_load(f)
        return data.get("version", "0.0.0")

    def create_release(self, version: str, title: str, description: str):
        """Execute the Release Triad protocol."""
        print(f"🚀 Initiating Release: {version} - {title}")

        # 1. Update Passport
        if self.passport_path.exists():
            with open(self.passport_path, 'r') as f:
                data = yaml.safe_load(f)
            
            data["version"] = version
            data["latest_release"] = {
                "version": version,
                "title": title,
                "date": datetime.now().isoformat(),
                "description": description[:100] + "..." if len(description) > 100 else description
            }
            
            with open(self.passport_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
            print("✅ Updated PROJECT.yaml")
        else:
            print("❌ PROJECT.yaml not found. Run 'kb sync init-passport' first.")
            return

        # 2. Git Tag
        try:
            # Check if tag exists
            existing = subprocess.run(["git", "tag", "-l", version], capture_output=True, text=True)
            if version in existing.stdout:
                print(f"⚠️  Tag {version} already exists. Skipping git tag.")
            else:
                subprocess.run(["git", "add", ".kb/project/PROJECT.yaml"], check=True)
                subprocess.run(["git", "commit", "-m", f"release: {version} - {title}"], check=True)
                subprocess.run(["git", "tag", "-a", version, "-m", title], check=True)
                print(f"✅ Created Git Tag: {version}")
                
                # Try push
                try:
                    subprocess.run(["git", "push", "--follow-tags"], check=True)
                    print("✅ Pushed tags to remote")
                except:
                    print("⚠️  Could not push tags (remote might not be configured)")

        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
            return

        # 3. Registry Broadcast (via kb_sync)
        # We invoke the existing sync tool to push the updated passport
        kb_sync_path = self.repo_root / ".kb" / "shared" / "tools" / "kb_sync.py"
        if not kb_sync_path.exists():
             # Fallback for dev environment
             kb_sync_path = self.repo_root / "tools" / "kb_sync.py"

        if kb_sync_path.exists():
            print("📡 Broadcasting to Company OS...")
            env = os.environ.copy()
            # Ensure PYTHONPATH includes tools dir
            env["PYTHONPATH"] = str(kb_sync_path.parent.parent) 
            
            try:
                subprocess.run(
                    [sys.executable, str(kb_sync_path), "push"],
                    check=True,
                    env=env
                )
                print("✅ Release broadcasted to Registry!")
            except subprocess.CalledProcessError:
                print("❌ Failed to broadcast release to Company OS")
        else:
            print("⚠️  kb_sync.py not found, skipping broadcast.")

        # 4. Generate Announcement Template
        print("\n📨 Announcement Template (Copy & Paste):")
        print("-" * 40)
        print(f"**Release: {title} ({version})**")
        print(f"\n{description}")
        print("\n**Installation:**")
        print(f"git checkout {version}")
        print("-" * 40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project Release Manager")
    parser.add_argument("version", help="Semantic version (e.g., v1.1.0)")
    parser.add_argument("title", help="Release title")
    parser.add_argument("--desc", help="Release description", default="No description provided")
    
    args = parser.parse_args()
    
    manager = ReleaseManager(Path("."))
    manager.create_release(args.version, args.title, args.desc)
