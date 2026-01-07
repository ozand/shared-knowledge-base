"""
Sync management for SKU CLI
Handles syncing catalog and artifacts from repository
"""

import subprocess
from pathlib import Path
from typing import Optional
from .utils import console, error, success

class SyncManager:
    """Manages repository sync operations"""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize sync manager"""
        if config_path:
            self.repo_path = config_path
        else:
            self._find_repo()

        self.catalog_dir = self.repo_path / "catalog"
        self.catalog_file = self.catalog_dir / "index.yaml"

    def _find_repo(self):
        """Find repository path"""
        import os
        repo = os.environ.get('SKU_REPO')
        if repo:
            self.repo_path = Path(repo)
        else:
            self.repo_path = Path.home() / ".sku" / "repo"

    def sync_index(self, force: bool = False):
        """Sync catalog index only (fast)

        Args:
            force: Force re-download even if cached
        """
        console.print("Syncing catalog index...")

        # Initialize sparse checkout if needed
        if not (self.repo_path / ".git").exists():
            self._init_sparse_checkout()

        # Pull latest changes
        self._git_pull()

    def sync_category(self, category: str, force: bool = False):
        """Sync specific category

        Args:
            category: Category to sync
            force: Force re-download
        """
        console.print(f"Syncing category: {category}...")
        # TODO: Implement category sync

    def sync_all(self, force: bool = False):
        """Sync all artifacts

        Args:
            force: Force re-download
        """
        console.print("Syncing all artifacts...")
        # TODO: Implement full sync

    def sync_installed(self, force: bool = False):
        """Sync installed artifacts only

        Args:
            force: Force re-download
        """
        console.print("Syncing installed artifacts...")
        # TODO: Implement installed sync

    def _init_sparse_checkout(self):
        """Initialize git sparse checkout"""
        console.print("Initializing repository...")

        # Clone with filter
        subprocess.run([
            'git', 'clone',
            '--filter=blob:none',
            '--sparse',
            subprocess.getenv('SKU_REPO', 'https://github.com/your-team/shared-knowledge-base.git'),
            str(self.repo_path)
        ], check=True)

        # Configure sparse checkout
        sparse_checkout = self.repo_path / ".git" / "info" / "sparse-checkout"
        sparse_checkout.parent.mkdir(parents=True, exist_ok=True)

        with open(sparse_checkout, 'w') as f:
            f.write("catalog/\n")  # Always need catalog

        subprocess.run([
            'git', '-C', str(self.repo_path),
            'sparse-checkout', 'set'
        ], check=True)

        success("✓ Repository initialized")

    def _git_pull(self):
        """Pull latest changes from repository"""
        try:
            subprocess.run([
                'git', '-C', str(self.repo_path),
                'pull', 'origin', 'main'
            ], check=True, capture_output=True)
            success("✓ Repository synced")
        except subprocess.CalledProcessError as e:
            error(f"✗ Git pull failed: {e}")

    def get_artifact_count(self) -> int:
        """Get total artifact count from catalog

        Returns:
            Total number of artifacts
        """
        import yaml

        if not self.catalog_file.exists():
            return 0

        with open(self.catalog_file, 'r') as f:
            catalog = yaml.safe_load(f)

        return catalog.get('statistics', {}).get('total_artifacts', 0)
