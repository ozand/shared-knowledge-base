#!/usr/bin/env python3
"""
Knowledge Base Profile Manager
Manages active knowledge domains for the current project.
"""

import sys
import yaml
from pathlib import Path
from typing import List, Set

class ProfileManager:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.config_path = repo_root / ".kb" / "active-profile.yaml"
        self.domains_dir = repo_root / "domains"
        
    def _load_config(self) -> dict:
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f) or {"active_domains": ["universal"]}
        return {"active_domains": ["universal"]}

    def _save_config(self, config: dict):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

    def get_available_domains(self) -> List[str]:
        """List all available domains in shared KB."""
        return [d.name for d in self.domains_dir.iterdir() 
                if d.is_dir() and not d.name.startswith('.')]

    def get_active_domains(self) -> List[str]:
        """Get currently active domains."""
        return self._load_config().get("active_domains", ["universal"])

    def set_active_domains(self, domains: List[str]):
        """Set the list of active domains."""
        # Validate
        available = set(self.get_available_domains())
        valid = [d for d in domains if d in available or d == "universal"]
        invalid = [d for d in domains if d not in available and d != "universal"]
        
        if invalid:
            print(f"⚠️  Warning: Domains not found: {invalid}")
            
        config = {"active_domains": valid}
        self._save_config(config)
        print(f"✅ Active domains set to: {valid}")

    def add_domain(self, domain: str):
        """Add a domain to active list."""
        config = self._load_config()
        active = set(config.get("active_domains", ["universal"]))
        
        if domain not in self.get_available_domains():
            print(f"❌ Domain '{domain}' does not exist in KB.")
            return
            
        active.add(domain)
        config["active_domains"] = list(active)
        self._save_config(config)
        print(f"✅ Added '{domain}'. Active: {list(active)}")

    def remove_domain(self, domain: str):
        """Remove a domain from active list."""
        config = self._load_config()
        active = set(config.get("active_domains", ["universal"]))
        
        if domain in active:
            active.remove(domain)
            config["active_domains"] = list(active)
            self._save_config(config)
            print(f"✅ Removed '{domain}'. Active: {list(active)}")
        else:
            print(f"ℹ️  Domain '{domain}' was not active.")

    def scan_and_recommend(self):
        """Analyze project files to recommend domains."""
        # Simple heuristic scanner
        recommendations = {"universal"}
        root_files = {p.name for p in self.repo_root.iterdir()}
        
        if "package.json" in root_files:
            recommendations.add("javascript")
            recommendations.add("react") # Assumption
            
        if "requirements.txt" in root_files or "pyproject.toml" in root_files:
            recommendations.add("python")
            
        if "Dockerfile" in root_files or "docker-compose.yml" in root_files:
            recommendations.add("docker")
            
        if "Cargo.toml" in root_files:
            recommendations.add("rust")

        # Filter by what actually exists in domains/
        available = set(self.get_available_domains())
        valid_recs = recommendations.intersection(available)
        
        print(f"🔍 Recommended domains based on file scan: {list(valid_recs)}")
        return list(valid_recs)

if __name__ == "__main__":
    # Test stub
    pass
