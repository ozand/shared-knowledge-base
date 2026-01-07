"""
Catalog management for SKU CLI
Handles loading and querying the artifact catalog
"""

import yaml
from pathlib import Path
from typing import List, Dict, Optional, Any
from .utils import console, error

class CatalogManager:
    """Manages the artifact catalog"""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize catalog manager

        Args:
            config_path: Path to catalog directory (default: repo/catalog/)
        """
        if config_path:
            self.catalog_dir = config_path
        else:
            # Try to find catalog in repo
            self._find_catalog()

        self.index_file = self.catalog_dir / "index.yaml"
        self.categories_file = self.catalog_dir / "categories.yaml"
        self._index = None
        self._categories = None

    def _find_catalog(self):
        """Find catalog directory in repository"""
        # Try current directory
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            catalog = parent / "catalog"
            if catalog.exists() and (catalog / "index.yaml").exists():
                self.catalog_dir = catalog
                return

        # Fallback to default
        self.catalog_dir = Path.home() / ".sku" / "repo" / "catalog"

    def load_index(self) -> Dict[str, Any]:
        """Load catalog index

        Returns:
            Catalog index dictionary
        """
        if self._index is not None:
            return self._index

        if not self.index_file.exists():
            error("Catalog index not found. Run 'sku sync --index-only' first.")
            return {}

        try:
            with open(self.index_file, 'r') as f:
                self._index = yaml.safe_load(f)
            return self._index
        except Exception as e:
            error(f"Failed to load catalog: {e}")
            return {}

    def load_categories(self) -> Dict[str, Any]:
        """Load category definitions

        Returns:
            Categories dictionary
        """
        if self._categories is not None:
            return self._categories

        if not self.categories_file.exists():
            return {}

        try:
            with open(self.categories_file, 'r') as f:
                self._categories = yaml.safe_load(f)
            return self._categories
        except Exception as e:
            error(f"Failed to load categories: {e}")
            return {}

    def list_artifacts(
        self,
        type: Optional[str] = None,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        project: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List artifacts with filters

        Args:
            type: Filter by artifact type
            category: Filter by category
            tag: Filter by tag
            project: Filter by project
            search: Search in name/description

        Returns:
            List of artifact dictionaries
        """
        index = self.load_index()
        artifacts = []

        # Add shared artifacts
        for category_name, category_data in index.get('shared_artifacts', {}).items():
            for artifact in category_data.get('artifacts', []):
                artifact['category'] = 'shared'
                artifact['type'] = category_name.rstrip('s')  # agents -> agent
                artifacts.append(artifact)

        # Add project artifacts
        for project_data in index.get('project_artifacts', []):
            for artifact in project_data.get('artifacts', []):
                artifact['category'] = 'project'
                artifact['project'] = project_data.get('project_id')
                artifacts.append(artifact)

        # Apply filters
        if type:
            artifacts = [a for a in artifacts if a.get('type') == type]

        if category:
            artifacts = [a for a in artifacts if a.get('category') == category]

        if tag:
            artifacts = [a for a in artifacts if tag in a.get('tags', [])]

        if project:
            artifacts = [a for a in artifacts if a.get('project') == project]

        if search:
            search_lower = search.lower()
            artifacts = [
                a for a in artifacts
                if search_lower in a.get('name', '').lower() or
                   search_lower in a.get('description', '').lower() or
                   search_lower in a.get('id', '').lower()
            ]

        return artifacts

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search artifacts by query

        Args:
            query: Search query

        Returns:
            List of matching artifacts
        """
        return self.list_artifacts(search=query)

    def get_artifact(self, artifact_type: str, artifact_id: str) -> Optional[Dict[str, Any]]:
        """Get specific artifact by type and ID

        Args:
            artifact_type: Artifact type (agent|skill|hook|mcp|docs|config)
            artifact_id: Artifact ID

        Returns:
            Artifact dictionary or None
        """
        artifacts = self.list_artifacts(type=artifact_type)
        for artifact in artifacts:
            if artifact.get('id') == artifact_id:
                return artifact
        return None

    def get_status(self) -> Dict[str, Any]:
        """Get catalog status information

        Returns:
            Status dictionary with version, last_updated, etc.
        """
        index = self.load_index()
        return {
            'version': index.get('version'),
            'last_updated': index.get('last_updated'),
            'total_artifacts': index.get('statistics', {}).get('total_artifacts', 0),
            'shared_artifacts': index.get('statistics', {}).get('shared_artifacts', 0),
            'project_artifacts': index.get('statistics', {}).get('project_artifacts', 0)
        }
