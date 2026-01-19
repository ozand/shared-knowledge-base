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

    def _setup_git_auth(self, cwd: str):
        """Configure git authentication for subprocess."""
        # 1. Check if GITHUB_TOKEN is in environment
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            # Configure git credential helper to use the token
            # This is a bit hacky for a subprocess, better to use the token in the URL
            return

    def _get_authenticated_url(self) -> str:
        """Inject token into URL if available."""
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            # Fallback: check if 'gh' CLI is authenticated
            try:
                subprocess.run(["gh", "auth", "status"], check=True, capture_output=True)
                # If gh is authed, we can use the https URL directly if git-credential-manager is set up
                # Or we can use gh to get the token
                proc = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
                if proc.returncode == 0:
                    token = proc.stdout.strip()
            except Exception:
                pass

        if token:
            # Convert https://github.com/org/repo.git -> https://token@github.com/org/repo.git
            if self.company_os_repo.startswith("https://"):
                return self.company_os_repo.replace("https://", f"https://x-access-token:{token}@", 1)
        
        return self.company_os_repo

    def fetch_registry(self):
        """Download latest registry from Company OS."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Simple implementation: git clone shallow
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, onerror=on_rm_error)
            
        try:
            print("📡 Fetching Company OS Registry...")
            # Use authenticated URL
            repo_url = self._get_authenticated_url()
            
            subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, str(self.temp_dir)],
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
            repo_url = self._get_authenticated_url()
            subprocess.run(
                ["git", "clone", repo_url, str(self.temp_dir)],
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
                "version": passport.get("version", "0.0.0"),
                "latest_release": passport.get("latest_release", {}),
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

    def check_updates(self):
        """Check for updates in dependencies."""
        if not self.passport_path.exists():
            print("❌ PROJECT.yaml not found.")
            return

        # 1. Fetch latest registry
        self.fetch_registry()
        
        if not self.registry_cache.exists():
            print("❌ Could not load registry cache.")
            return

        with open(self.passport_path, 'r') as f:
            passport = yaml.safe_load(f)
            
        with open(self.registry_cache, 'r') as f:
            registry = yaml.safe_load(f)
            
        dependencies = passport.get("dependencies", [])
        projects = {p["id"]: p for p in registry.get("projects", [])}
        
        print("\n🔍 Checking dependencies...")
        updates_found = False
        
        for dep in dependencies:
            pid = dep.get("project_id")
            current_version = dep.get("version", "0.0.0")
            
            if pid in projects:
                remote_proj = projects[pid]
                # Check for latest_release field (added in Release Protocol)
                latest_release = remote_proj.get("latest_release", {})
                remote_version = latest_release.get("version") or remote_proj.get("version")
                
                if remote_version and remote_version != "0.0.0" and remote_version != current_version:
                    print(f"  👉 Update available for {pid}: {current_version} -> {remote_version}")
                    print(f"     Title: {latest_release.get('title', 'No title')}")
                    updates_found = True
                else:
                    print(f"  ✅ {pid} is up to date ({current_version})")
            else:
                print(f"  ⚠️  Dependency not found in registry: {pid}")
                
        if not updates_found:
            print("\n✨ All dependencies are up to date.")
        else:
            print("\n💡 Action: Update your dependencies and run tests.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Company OS Synchronizer")
    parser.add_argument("action", choices=["init-passport", "pull", "push", "check-updates"], help="Action to perform")
    
    args = parser.parse_args()
    
    sync = RegistrySync(Path("."))
    
    if args.action == "init-passport":
        sync.init_passport()
    elif args.action == "pull":
        sync.fetch_registry()
    elif args.action == "push":
        sync.register_project()
    elif args.action == "check-updates":
        sync.check_updates()
