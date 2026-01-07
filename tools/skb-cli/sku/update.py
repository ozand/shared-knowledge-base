"""
Update management for SKU CLI
Handles checking for updates and updating artifacts
"""

import yaml
import requests
from pathlib import Path
from typing import List, Dict, Optional
from semver import VersionInfo
from .utils import console, error, success, info, warn


class UpdateManager:
    """Manages artifact updates"""

    def __init__(self, catalog_path: Path, state_path: Path):
        """Initialize update manager

        Args:
            catalog_path: Path to catalog directory
            state_path: Path to state file
        """
        self.catalog_path = catalog_path
        self.state_path = state_path
        self.index_file = catalog_path / "index.yaml"
        self.state_file = state_path / "state.yaml"

    def check_updates(self, artifact_type: Optional[str] = None,
                     artifact_id: Optional[str] = None,
                     remote: bool = True) -> List[Dict]:
        """Check for available updates

        Args:
            artifact_type: Filter by artifact type
            artifact_id: Filter by artifact ID
            remote: Check remote repository (default: True)

        Returns:
            List of artifacts with updates available
        """
        from .catalog import CatalogManager

        # Load catalog
        catalog = CatalogManager(self.catalog_path)
        local_index = catalog.load_index()

        # Get remote index if requested
        remote_index = None
        if remote:
            try:
                remote_index = self._fetch_remote_catalog()
            except Exception as e:
                warn(f"Could not fetch remote catalog: {e}")
                remote_index = local_index

        # Load installed state
        installed = self._load_installed()

        updates = []

        # Check for updates
        for category in ["shared_artifacts", "project_artifacts"]:
            if category not in local_index:
                continue

            if category == "shared_artifacts":
                artifacts = local_index[category]
            else:
                # Project artifacts
                for project in local_index[category]:
                    artifacts = project.get("artifacts", [])

            for artifact in artifacts:
                # Apply filters
                if artifact_type and artifact.get("type") != artifact_type:
                    continue
                if artifact_id and artifact.get("id") != artifact_id:
                    continue

                # Check if installed
                installed_key = f"{artifact.get('type')}/{artifact.get('id')}"
                if installed_key not in installed:
                    continue

                # Compare versions
                local_version = installed[installed_key].get("version")
                remote_version = artifact.get("version")

                if self._has_update(local_version, remote_version):
                    update_type = self._get_update_type(local_version, remote_version)

                    updates.append({
                        "type": artifact.get("type"),
                        "id": artifact.get("id"),
                        "path": artifact.get("path"),
                        "local_version": local_version,
                        "remote_version": remote_version,
                        "update_type": update_type,
                        "published": artifact.get("published_at"),
                        "category": category
                    })

        return updates

    def update(self, artifact_type: str, artifact_id: str,
               auto_patch: bool = True) -> bool:
        """Update an artifact

        Args:
            artifact_type: Artifact type (agent, skill, hook, mcp, etc.)
            artifact_id: Artifact ID
            auto_patch: Auto-update patch versions (default: True)

        Returns:
            True if update successful
        """
        from .sync import SyncManager
        from .install import InstallManager
        from .catalog import CatalogManager

        # Get update info
        updates = self.check_updates(artifact_type, artifact_id)

        if not updates:
            info(f"No updates available for {artifact_type}/{artifact_id}")
            return False

        update = updates[0]

        # Check if auto-update or prompt
        if auto_patch and update["update_type"] == "patch":
            info(f"Auto-updating {artifact_type}/{artifact_id}...")
        else:
            if update["update_type"] == "major":
                warn(f"⚠️  Major update available: {update['local_version']} → {update['remote_version']}")
                console.print("\nThis update may contain breaking changes.")
                console.print("Review changelog before updating:\n")

                # Show artifact details
                self._show_artifact_details(update)

                response = input("\nUpdate anyway? [y/N] ")
                if response.lower() != 'y':
                    info("Update cancelled")
                    return False

            elif update["update_type"] == "minor":
                info(f"Minor update available: {update['local_version']} → {update['remote_version']}")
                response = input("Update? [Y/n] ")
                if response.lower() == 'n':
                    info("Update cancelled")
                    return False

        # Sync from remote
        info(f"Syncing {artifact_type}/{artifact_id}...")
        sync_manager = SyncManager(self.catalog_path, Path.home() / ".sku")
        sync_manager.sync(paths=[update["path"]])

        # Reinstall
        info(f"Reinstalling {artifact_type}/{artifact_id}...")
        install_manager = InstallManager(self.catalog_path, Path.home() / ".sku")
        result = install_manager.install(artifact_type, artifact_id, force=True)

        if result:
            success(f"✓ Updated {artifact_type}/{artifact_id} to {update['remote_version']}")

            # Update state
            self._update_state(artifact_type, artifact_id, update['remote_version'])

            return True
        else:
            error(f"✗ Failed to update {artifact_type}/{artifact_id}")
            return False

    def update_all(self, auto_patch: bool = True) -> Dict[str, List]:
        """Update all artifacts

        Args:
            auto_patch: Auto-update patch versions (default: True)

        Returns:
            Dict with 'updated', 'skipped', 'failed' lists
        """
        updates = self.check_updates()

        result = {
            "updated": [],
            "skipped": [],
            "failed": []
        }

        if not updates:
            info("No updates available")
            return result

        console.print(f"\n[bold]Found {len(updates)} updates[/bold]\n")

        for update in updates:
            artifact_key = f"{update['type']}/{update['id']}"

            # Auto-update patches
            if auto_patch and update["update_type"] == "patch":
                if self.update(update["type"], update["id"], auto_patch=True):
                    result["updated"].append(artifact_key)
                else:
                    result["failed"].append(artifact_key)
            else:
                # Prompt for non-patch updates
                console.print(f"\n[bold]{artifact_key}[/bold]")
                console.print(f"  {update['local_version']} → {update['remote_version']} ({update['update_type']})")

                response = input("Update? [y/N] ")
                if response.lower() == 'y':
                    if self.update(update["type"], update["id"], auto_patch=False):
                        result["updated"].append(artifact_key)
                    else:
                        result["failed"].append(artifact_key)
                else:
                    result["skipped"].append(artifact_key)

        return result

    def _load_installed(self) -> Dict:
        """Load installed artifacts state

        Returns:
            Dict of installed artifacts
        """
        if not self.state_file.exists():
            return {}

        with open(self.state_file, 'r') as f:
            state = yaml.safe_load(f)

        return state.get("installed", {})

    def _update_state(self, artifact_type: str, artifact_id: str, version: str):
        """Update installed artifact version in state

        Args:
            artifact_type: Artifact type
            artifact_id: Artifact ID
            version: New version
        """
        state = {}

        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                state = yaml.safe_load(f)

        if "installed" not in state:
            state["installed"] = {}

        key = f"{artifact_type}/{artifact_id}"
        state["installed"][key] = {
            "version": version,
            "updated_at": self._get_timestamp()
        }

        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.state_file, 'w') as f:
            yaml.dump(state, f, default_flow_style=False)

    def _has_update(self, local: str, remote: str) -> bool:
        """Check if remote version is newer

        Args:
            local: Local version
            remote: Remote version

        Returns:
            True if remote is newer
        """
        try:
            local_ver = VersionInfo.parse(local)
            remote_ver = VersionInfo.parse(remote)
            return remote_ver > local_ver
        except:
            return False

    def _get_update_type(self, local: str, remote: str) -> str:
        """Get update type (major, minor, patch)

        Args:
            local: Local version
            remote: Remote version

        Returns:
            Update type string
        """
        try:
            local_ver = VersionInfo.parse(local)
            remote_ver = VersionInfo.parse(remote)

            if remote_ver.major > local_ver.major:
                return "major"
            elif remote_ver.minor > local_ver.minor:
                return "minor"
            else:
                return "patch"
        except:
            return "unknown"

    def _fetch_remote_catalog(self) -> Dict:
        """Fetch remote catalog from repository

        Returns:
            Remote index dict
        """
        import os

        repo_url = os.environ.get('SKU_REPO')
        if not repo_url:
            raise Exception("SKU_REPO not set")

        # Try to fetch via GitHub API
        try:
            # For now, return None - will implement GitHub API fetch
            # This would use github.com/owner/repo/raw/main/catalog/index.yaml
            return None
        except Exception as e:
            raise Exception(f"Failed to fetch remote catalog: {e}")

    def _show_artifact_details(self, update: Dict):
        """Show artifact details for update review

        Args:
            update: Update info dict
        """
        console.print(f"\n[bold cyan]Artifact:[/bold cyan] {update['type']}/{update['id']}")
        console.print(f"[bold]Versions:[/bold] {update['local_version']} → {update['remote_version']}")
        console.print(f"[bold]Type:[/bold] {update['update_type']} update")

        # Try to fetch changelog or metadata
        artifact_path = Path.home() / ".sku" / update["path"]
        metadata_file = artifact_path / "metadata.yaml"

        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = yaml.safe_load(f)

            if "changelog" in metadata:
                console.print(f"\n[bold]Changelog:[/bold]")
                for entry in metadata["changelog"][:3]:
                    console.print(f"  • {entry.get('version')}: {', '.join(entry.get('changes', []))}")

    def _get_timestamp(self) -> str:
        """Get current timestamp

        Returns:
            ISO format timestamp
        """
        from datetime import datetime
        return datetime.now().isoformat()
