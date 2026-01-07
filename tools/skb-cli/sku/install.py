"""
Install management for SKU CLI
Handles installing and uninstalling artifacts
"""

import yaml
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List
from .utils import console, error, success

class InstallManager:
    """Manages artifact installation"""

    def __init__(self, project_path: Optional[Path] = None):
        """Initialize install manager

        Args:
            project_path: Path to current project (default: cwd)
        """
        self.project_path = project_path or Path.cwd()
        self.claude_dir = self.project_path / ".claude"
        self.state_file = self.claude_dir / "sku" / "state.yaml"

    def install(self, artifact: Dict[str, Any], force: bool = False):
        """Install artifact to project

        Args:
            artifact: Artifact dictionary from catalog
            force: Overwrite if exists
        """
        artifact_type = artifact.get('type', 'unknown')
        artifact_id = artifact.get('id', 'unknown')

        # Determine destination
        dest_map = {
            'agent': self.claude_dir / "agents" / artifact_id,
            'skill': self.claude_dir / "skills" / artifact_id,
            'hook': self.claude_dir / "hooks" / artifact_id,
            'mcp': self.claude_dir / "mcp" / artifact_id,
            'docs': self.claude_dir / "docs" / artifact_id,
            'config': self.claude_dir / "configs" / artifact_id,
        }

        dest = dest_map.get(artifact_type)
        if not dest:
            raise ValueError(f"Unknown artifact type: {artifact_type}")

        # Check if already installed
        if dest.exists() and not force:
            error(f"Artifact already installed: {artifact_type}/{artifact_id}")
            console.print("Use --force to overwrite")
            raise FileExistsError(f"Artifact exists: {dest}")

        # Download artifact from repo
        repo_path = self._get_repo_path()
        source_path = repo_path / artifact.get('path', '')

        if not source_path.exists():
            raise FileNotFoundError(f"Artifact path not found: {source_path}")

        # Copy files
        dest.mkdir(parents=True, exist_ok=True)
        self._copy_directory(source_path, dest)

        # Update state
        self._update_state(artifact)

        success(f"✓ Installed to: {dest}")

    def uninstall(self, artifact_type: str, artifact_id: str):
        """Uninstall artifact from project

        Args:
            artifact_type: Artifact type
            artifact_id: Artifact ID
        """
        dest_map = {
            'agent': self.claude_dir / "agents" / artifact_id,
            'skill': self.claude_dir / "skills" / artifact_id,
            'hook': self.claude_dir / "hooks" / artifact_id,
            'mcp': self.claude_dir / "mcp" / artifact_id,
            'docs': self.claude_dir / "docs" / artifact_id,
            'config': self.claude_dir / "configs" / artifact_id,
        }

        dest = dest_map.get(artifact_type)

        if not dest or not dest.exists():
            error(f"Artifact not installed: {artifact_type}/{artifact_id}")
            return

        # Remove files
        shutil.rmtree(dest)

        # Update state
        self._remove_from_state(artifact_type, artifact_id)

        success(f"✓ Uninstalled: {dest}")

    def list_installed(self) -> List[Dict[str, Any]]:
        """List all installed artifacts

        Returns:
            List of installed artifact info
        """
        if not self.state_file.exists():
            return []

        with open(self.state_file, 'r') as f:
            state = yaml.safe_load(f)

        return state.get('installed', [])

    def get_install_path(self, artifact: Dict[str, Any]) -> Path:
        """Get installation path for artifact

        Args:
            artifact: Artifact dictionary

        Returns:
            Installation path
        """
        artifact_type = artifact.get('type', 'unknown')
        artifact_id = artifact.get('id', 'unknown')

        dest_map = {
            'agent': self.claude_dir / "agents" / artifact_id,
            'skill': self.claude_dir / "skills" / artifact_id,
            'hook': self.claude_dir / "hooks" / artifact_id,
            'mcp': self.claude_dir / "mcp" / artifact_id,
            'docs': self.claude_dir / "docs" / artifact_id,
            'config': self.claude_dir / "configs" / artifact_id,
        }

        return dest_map.get(artifact_type, Path())

    def _get_repo_path(self) -> Path:
        """Get path to shared-knowledge-base repository

        Returns:
            Repository path
        """
        import os
        repo = os.environ.get('SKU_REPO')
        if repo:
            return Path(repo)

        # Try to find in .sku
        sku_repo = Path.home() / ".sku" / "repo"
        if sku_repo.exists():
            return sku_repo

        raise FileNotFoundError(
            "Repository not found. Run 'sku sync --index-only' first."
        )

    def _copy_directory(self, source: Path, dest: Path):
        """Copy directory contents

        Args:
            source: Source directory
            dest: Destination directory
        """
        dest.mkdir(parents=True, exist_ok=True)

        for item in source.iterdir():
            if item.is_file():
                shutil.copy2(item, dest / item.name)
            elif item.is_dir():
                self._copy_directory(item, dest / item.name)

    def _update_state(self, artifact: Dict[str, Any]):
        """Update installation state

        Args:
            artifact: Artifact dictionary
        """
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                state = yaml.safe_load(f)
        else:
            state = {'installed': []}

        # Add or update artifact
        artifact_info = {
            'type': artifact.get('type'),
            'id': artifact.get('id'),
            'version': artifact.get('version'),
            'installed_at': self._get_timestamp()
        }

        # Remove old version if exists
        state['installed'] = [
            a for a in state['installed']
            if not (a['type'] == artifact_info['type'] and a['id'] == artifact_info['id'])
        ]

        state['installed'].append(artifact_info)

        with open(self.state_file, 'w') as f:
            yaml.dump(state, f, default_flow_style=False)

    def _remove_from_state(self, artifact_type: str, artifact_id: str):
        """Remove artifact from state

        Args:
            artifact_type: Artifact type
            artifact_id: Artifact ID
        """
        if not self.state_file.exists():
            return

        with open(self.state_file, 'r') as f:
            state = yaml.safe_load(f)

        state['installed'] = [
            a for a in state.get('installed', [])
            if not (a['type'] == artifact_type and a['id'] == artifact_id)
        ]

        with open(self.state_file, 'w') as f:
            yaml.dump(state, f, default_flow_style=False)

    def _get_timestamp(self) -> str:
        """Get current timestamp

        Returns:
            ISO format timestamp
        """
        from datetime import datetime
        return datetime.now().isoformat()
