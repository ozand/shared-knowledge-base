#!/usr/bin/env python3
"""
Company OS Synchronizer
Manages the link between the local Project and the central Company OS Registry.
"""

import os
import sys
import yaml
import shutil
import subprocess
import stat
from pathlib import Path
from datetime import datetime

def on_rm_error(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.
    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.
    If the error is for another reason it re-raises the error.
    """
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise

class RegistrySync:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.passport_path = repo_root / ".kb" / "project" / "PROJECT.yaml"
        self.cache_dir = repo_root / ".kb" / "cache"
        self.registry_cache = self.cache_dir / "registry.yaml"
        
        # Configuration - ideally loaded from env or config
        self.company_os_repo = os.environ.get("COMPANY_OS_REPO", "https://github.com/ozand/company-os.git")
        self.temp_dir = repo_root / "tmp" / "company-os-sync"

    def _ensure_passport(self):
        """Ensure local project passport exists."""
        if not self.passport_path.exists():
            print(f"❌ Passport not found at {self.passport_path}")
            print("Run 'python kb.py init-passport' to create one.")
            return False
        return True

    def init_passport(self):
        """Create a template passport."""
        self.passport_path.parent.mkdir(parents=True, exist_ok=True)
        template = {
            "project_id": self.repo_root.name,
            "name": self.repo_root.name.replace('-', ' ').title(),
            "description": "Project description...",
            "repository": f"owner/{self.repo_root.name}",
            "stack": ["python"],
            "status": "active",
            "last_updated": datetime.now().isoformat()
        }
        with open(self.passport_path, 'w') as f:
            yaml.dump(template, f, default_flow_style=False)
        print(f"✅ Created passport template at {self.passport_path}")

    def fetch_registry(self):
        """Download latest registry from Company OS."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Simple implementation: git clone shallow
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, onerror=on_rm_error)
            
        try:
            print("📡 Fetching Company OS Registry...")
            subprocess.run(
                ["git", "clone", "--depth", "1", self.company_os_repo, str(self.temp_dir)],
                check=True, capture_output=True
            )
            
            # Copy registry file
            source = self.temp_dir / "registry" / "projects.yaml"
            if source.exists():
                shutil.copy2(source, self.registry_cache)
                print(f"✅ Registry cached to {self.registry_cache}")
            else:
                print("⚠️ Registry file not found in Company OS repo")
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to fetch registry: {e}")
        finally:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir, onerror=on_rm_error)

    def validate_passport(self, passport):
        """Validate passport for junk data."""
        errors = []
        
        # Check required fields
        if not passport.get("project_id") or not str(passport.get("project_id")).strip():
            errors.append("project_id is empty")
            
        # Check defaults
        if passport.get("description") == "Project description...":
            errors.append("Description is still default template")
            
        if str(passport.get("repository")).startswith("owner/"):
            errors.append("Repository is still default template (owner/...)")
            
        if not passport.get("name"):
            errors.append("Project name is empty")
            
        if errors:
            print("❌ Passport validation failed:")
            for e in errors:
                print(f"  - {e}")
            print("💡 Action: Edit .kb/project/PROJECT.yaml with real data")
            return False
        return True

    def register_project(self):
        """Register/Update this project in Company OS."""
        if not self._ensure_passport():
            return

        # Load local passport
        with open(self.passport_path, 'r') as f:
            passport = yaml.safe_load(f)

        # Validate before pushing
        if not self.validate_passport(passport):
            return

        print(f"🚀 Registering {passport['project_id']} to Company OS...")
        
        # Clone Company OS
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, onerror=on_rm_error)
            
        try:
            subprocess.run(
                ["git", "clone", self.company_os_repo, str(self.temp_dir)],
                check=True, capture_output=True
            )
            
            registry_path = self.temp_dir / "registry" / "projects.yaml"
            
            # Load existing registry
            if registry_path.exists():
                with open(registry_path, 'r') as f:
                    registry = yaml.safe_load(f) or {"projects": []}
            else:
                registry = {"projects": []}
                
            # Update or Append
            projects = registry.get("projects", [])
            existing_idx = next((i for i, p in enumerate(projects) if p.get("id") == passport["project_id"]), -1)
            
            # Map passport fields to registry schema
            entry = {
                "id": passport["project_id"],
                "name": passport.get("name"),
                "repo": passport.get("repository"),
                "description": passport.get("description"),
                "stack": passport.get("stack", []),
                "last_sync": datetime.now().isoformat()
            }
            
            if existing_idx >= 0:
                print("🔹 Updating existing entry...")
                projects[existing_idx].update(entry)
            else:
                print("🔹 Creating new entry...")
                projects.append(entry)
            
            registry["projects"] = projects
            
            # Save back
            with open(registry_path, 'w') as f:
                yaml.dump(registry, f, default_flow_style=False)
                
            # Commit and Push
            # NOTE: This requires authentication (SSH/Token) in the environment
            cwd = str(self.temp_dir)
            subprocess.run(["git", "config", "user.name", "Company OS Bot"], cwd=cwd, check=True)
            subprocess.run(["git", "config", "user.email", "bot@company-os"], cwd=cwd, check=True)
            subprocess.run(["git", "add", "."], cwd=cwd, check=True)
            
            # Check if there are changes
            status = subprocess.run(["git", "status", "--porcelain"], cwd=cwd, capture_output=True, text=True)
            if status.stdout.strip():
                subprocess.run(["git", "commit", "-m", f"Update project: {passport['project_id']}"], cwd=cwd, check=True)
                subprocess.run(["git", "push"], cwd=cwd, check=True)
                print("✅ Successfully updated Company OS!")
            else:
                print("✨ No changes to update.")
                
        except Exception as e:
            print(f"❌ Error during registration: {e}")
        finally:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir, onerror=on_rm_error)

if __name__ == "__main__":
    # Test stub
    pass
