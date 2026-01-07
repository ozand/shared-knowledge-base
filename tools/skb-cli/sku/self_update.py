"""
Self-update management for SKU CLI
Handles updating SKU CLI itself
"""

import os
import sys
import requests
import shutil
import subprocess
from pathlib import Path
from typing import Optional
from .utils import console, error, success, info, warn


class SelfUpdateManager:
    """Manages SKU CLI self-updates"""

    def __init__(self):
        """Initialize self-update manager"""
        self.repo_url = os.environ.get('SKU_REPO', 'ozand/shared-knowledge-base')
        self.raw_base = f"https://raw.githubusercontent.com/{self.repo_url}/main"
        self.install_dir = Path.home() / ".sku" / "bin"

    def check_update(self) -> Optional[dict]:
        """Check if SKU CLI update is available

        Returns:
            Dict with update info or None if up to date
        """
        # Get current version
        try:
            from . import __version__
            current_version = __version__.__version__
        except:
            current_version = "1.0.0"

        # Fetch remote version
        try:
            response = requests.get(
                f"{self.raw_base}/tools/skb-cli/sku/__init__.py",
                timeout=10
            )
            response.raise_for_status()

            # Parse version from remote __init__.py
            remote_content = response.text
            for line in remote_content.split('\n'):
                if line.startswith('__version__'):
                    remote_version = line.split('=')[1].strip().strip('"\'')
                    break
            else:
                remote_version = "1.0.0"

        except Exception as e:
            warn(f"Could not check for updates: {e}")
            return None

        # Compare versions
        if self._has_update(current_version, remote_version):
            return {
                'current': current_version,
                'remote': remote_version,
                'update_type': self._get_update_type(current_version, remote_version)
            }

        return None

    def update(self, auto_patch: bool = True) -> bool:
        """Update SKU CLI to latest version

        Args:
            auto_patch: Auto-update patch versions (default: True)

        Returns:
            True if update successful
        """
        # Check for updates
        update_info = self.check_update()

        if not update_info:
            info("SKU CLI is already up to date")
            return True

        # Check if auto-update or prompt
        if auto_patch and update_info['update_type'] == 'patch':
            info(f"Auto-updating SKU CLI: {update_info['current']} → {update_info['remote']}")
        else:
            if update_info['update_type'] == 'major':
                warn(f"⚠️  Major update available: {update_info['current']} → {update_info['remote']}")
                console.print("\nThis update may contain breaking changes.")
                response = input("\nUpdate anyway? [y/N] ")
                if response.lower() != 'y':
                    info("Update cancelled")
                    return False

            elif update_info['update_type'] == 'minor':
                info(f"Minor update available: {update_info['current']} → {update_info['remote']}")
                response = input("Update? [Y/n] ")
                if response.lower() == 'n':
                    info("Update cancelled")
                    return False

        # Perform update
        console.print("\n[dim]Updating SKU CLI...[/dim]")

        try:
            # Create backup
            backup_dir = self.install_dir / "backup"
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            shutil.copytree(self.install_dir, backup_dir)

            # Download new files
            tmp_dir = Path("/tmp/sku-update")
            if tmp_dir.exists():
                shutil.rmtree(tmp_dir)
            tmp_dir.mkdir()

            # Download Python files
            sku_dir = tmp_dir / "sku"
            sku_dir.mkdir()

            files = [
                "__init__.py", "cli.py", "catalog.py", "sync.py",
                "install.py", "publish.py", "update.py", "auth.py",
                "utils.py", "self_update.py"
            ]

            for file in files:
                console.print(f"  Downloading: {file}")
                response = requests.get(f"{self.raw_base}/tools/skb-cli/sku/{file}", timeout=10)
                response.raise_for_status()

                (sku_dir / file).write_text(response.text)

            # Install new version
            console.print("\n  [dim]Installing new version...[/dim]")

            # Use uv to install
            subprocess.run(
                ["uv", "pip", "install", "--target", str(self.install_dir), str(tmp_dir)],
                check=True,
                capture_output=True
            )

            # Cleanup
            shutil.rmtree(tmp_dir)
            shutil.rmtree(backup_dir)

            success(f"✓ Updated SKU CLI to {update_info['remote']}")
            return True

        except Exception as e:
            error(f"✗ Update failed: {e}")

            # Restore backup
            if backup_dir.exists():
                warn("Restoring backup...")
                try:
                    if self.install_dir.exists():
                        shutil.rmtree(self.install_dir)
                    shutil.copytree(backup_dir, self.install_dir)
                    shutil.rmtree(backup_dir)
                    success("✓ Backup restored")
                except:
                    error("✗ Failed to restore backup")

            return False

    def _has_update(self, local: str, remote: str) -> bool:
        """Check if remote version is newer

        Args:
            local: Local version
            remote: Remote version

        Returns:
            True if remote is newer
        """
        try:
            from semver import VersionInfo
            local_ver = VersionInfo.parse(local)
            remote_ver = VersionInfo.parse(remote)
            return remote_ver > local_ver
        except:
            # Simple string comparison if semver fails
            return remote > local

    def _get_update_type(self, local: str, remote: str) -> str:
        """Get update type (major, minor, patch)

        Args:
            local: Local version
            remote: Remote version

        Returns:
            Update type string
        """
        try:
            from semver import VersionInfo
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
