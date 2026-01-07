"""
Publish management for SKU CLI
Handles publishing project artifacts to shared-knowledge-base
"""

import yaml
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
from .utils import console, error, success, warning
from .catalog import CatalogManager

class PublishManager:
    """Manages artifact publishing"""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize publish manager

        Args:
            config_path: Path to shared-knowledge-base repository
        """
        if config_path:
            self.repo_path = config_path
        else:
            # Try to find repo in common locations
            self._find_repo()

        self.projects_dir = self.repo_path / "projects"
        self.catalog_dir = self.repo_path / "catalog"
        self.catalog_file = self.catalog_dir / "index.yaml"

    def _find_repo(self):
        """Find shared-knowledge-base repository"""
        # Try environment variable
        import os
        repo = os.environ.get('SKU_REPO')
        if repo:
            self.repo_path = Path(repo)
            return

        # Try current directory
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            if (parent / "catalog" / "index.yaml").exists():
                self.repo_path = parent
                return

        # Fallback
        self.repo_path = Path.home() / ".sku" / "repo"

    def publish(
        self,
        path: Path,
        artifact_type: str,
        version: str,
        name: Optional[str] = None,
        tags: Optional[str] = None,
        description: Optional[str] = None
    ) -> str:
        """Publish artifact to shared-knowledge-base

        Args:
            path: Path to artifact directory/files
            artifact_type: Artifact type (mcp|docs|config|schema)
            version: Artifact version (semver)
            name: Artifact name
            tags: Comma-separated tags
            description: Artifact description

        Returns:
            Published artifact ID
        """
        path = Path(path)

        # Validate inputs
        if not path.exists():
            raise ValueError(f"Path does not exist: {path}")

        # Parse tags
        tag_list = []
        if tags:
            tag_list = [t.strip() for t in tags.split(',')]

        # Get project info from config or prompt
        project_info = self._get_project_info()

        # Generate artifact ID
        artifact_id = self._generate_artifact_id(path, artifact_type)

        # Determine destination path
        dest_dir = self.projects_dir / project_info['id'] / artifact_type / artifact_id
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Copy files
        self._copy_artifact_files(path, dest_dir)

        # Create metadata.yaml
        metadata = self._create_metadata(
            artifact_id=artifact_id,
            artifact_type=artifact_type,
            version=version,
            name=name or artifact_id,
            tags=tag_list,
            description=description,
            project_info=project_info
        )

        metadata_file = dest_dir / "metadata.yaml"
        with open(metadata_file, 'w') as f:
            yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)

        success(f"✓ Artifact files copied to: {dest_dir}")

        # Update catalog index
        self._update_catalog_index(
            project_info=project_info,
            artifact_type=artifact_type,
            artifact_id=artifact_id,
            metadata=metadata
        )

        return artifact_id

    def _get_project_info(self) -> Dict[str, Any]:
        """Get project information from config or user input

        Returns:
            Project info dictionary
        """
        # Try to load from .sku/config.yaml in current project
        config_file = Path.cwd() / ".sku" / "config.yaml"
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
                return config.get('project', {})

        # Prompt user for project info
        console.print("\n[yellow]Project information required[/yellow]")

        from questionary import prompt

        answers = prompt([
            {'type': 'text', 'name': 'id', 'message': 'Project ID (e.g., mcp-youtube):'},
            {'type': 'text', 'name': 'name', 'message': 'Project name:'},
            {'type': 'text', 'name': 'repository', 'message': 'Repository (e.g., private/youtube-mcp):'},
            {'type': 'text', 'name': 'team', 'message': 'Team (e.g., backend-team):'},
        ])

        return answers

    def _generate_artifact_id(self, path: Path, artifact_type: str) -> str:
        """Generate artifact ID from path and type

        Args:
            path: Artifact path
            artifact_type: Artifact type

        Returns:
            Generated artifact ID
        """
        # Use directory name as artifact ID
        return path.name.lower().replace(' ', '-').replace('_', '-')

    def _copy_artifact_files(self, source: Path, dest: Path):
        """Copy artifact files to destination

        Args:
            source: Source directory
            dest: Destination directory
        """
        import shutil

        if source.is_dir():
            # Copy all files
            for item in source.iterdir():
                if item.is_file():
                    shutil.copy2(item, dest / item.name)
        else:
            # Copy single file
            shutil.copy2(source, dest / source.name)

        console.print(f"[dim]  Copied files from {source} to {dest}[/dim]")

    def _create_metadata(
        self,
        artifact_id: str,
        artifact_type: str,
        version: str,
        name: str,
        tags: list,
        description: Optional[str],
        project_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create metadata for artifact

        Args:
            artifact_id: Artifact ID
            artifact_type: Artifact type
            version: Version string
            name: Artifact name
            tags: List of tags
            description: Artifact description
            project_info: Project information

        Returns:
            Metadata dictionary
        """
        return {
            'artifact': {
                'id': artifact_id,
                'type': artifact_type,
                'name': name,
                'version': version,
                'description': description or f"{artifact_type} artifact from {project_info['name']}",
                'tags': tags,
            },
            'project': {
                'id': project_info['id'],
                'name': project_info['name'],
                'repository': project_info['repository'],
                'team': project_info['team'],
            },
            'publishing': {
                'published_at': datetime.now().isoformat(),
                'published_by': self._get_git_user(),
            },
            'versioning': {
                'scheme': 'semver',
                'current_version': version,
            }
        }

    def _get_git_user(self) -> str:
        """Get current git user

        Returns:
            Git username or 'unknown'
        """
        try:
            result = subprocess.run(
                ['git', 'config', 'user.name'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass

        return 'unknown'

    def _update_catalog_index(
        self,
        project_info: Dict[str, Any],
        artifact_type: str,
        artifact_id: str,
        metadata: Dict[str, Any]
    ):
        """Update catalog index with new artifact

        Args:
            project_info: Project information
            artifact_type: Artifact type
            artifact_id: Artifact ID
            metadata: Artifact metadata
        """
        # Load existing catalog
        if self.catalog_file.exists():
            with open(self.catalog_file, 'r') as f:
                catalog = yaml.safe_load(f)
        else:
            catalog = {'version': '1.0', 'last_updated': '', 'project_artifacts': []}

        # Find or create project entry
        project_entry = None
        for proj in catalog.get('project_artifacts', []):
            if proj.get('project_id') == project_info['id']:
                project_entry = proj
                break

        if not project_entry:
            project_entry = {
                'project_id': project_info['id'],
                'project_name': project_info['name'],
                'repository': project_info['repository'],
                'maintainer': project_info['team'],
                'artifacts': []
            }
            if 'project_artifacts' not in catalog:
                catalog['project_artifacts'] = []
            catalog['project_artifacts'].append(project_entry)

        # Add artifact to project
        artifact_entry = {
            'type': artifact_type,
            'id': artifact_id,
            'name': metadata['artifact']['name'],
            'version': metadata['artifact']['version'],
            'path': f"projects/{project_info['id']}/{artifact_type}/{artifact_id}/",
            'tags': metadata['artifact']['tags'],
            'description': metadata['artifact']['description']
        }

        project_entry['artifacts'].append(artifact_entry)

        # Update timestamp
        catalog['last_updated'] = datetime.now().isoformat()

        # Save catalog
        self.catalog_dir.mkdir(parents=True, exist_ok=True)
        with open(self.catalog_file, 'w') as f:
            yaml.dump(catalog, f, default_flow_style=False, sort_keys=False)

        success(f"✓ Catalog index updated")
        console.print(f"[dim]  Catalog: {self.catalog_file}[/dim]")
