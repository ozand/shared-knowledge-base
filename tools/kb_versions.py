#!/usr/bin/env python3
"""
kb_versions.py - Library Version Monitor

Monitors library versions and alerts when knowledge base entries
need updates due to new releases.

Supports:
- Python (PyPI)
- Node.js (npm)
- Docker
- PostgreSQL
- GitHub releases

Author: Knowledge Base Curator
Version: 1.0.0
License: MIT
"""

import requests
import yaml
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class VersionInfo:
    """Version information for a library."""
    library: str
    current_version: str
    tested_versions: List[str]
    entry_ids: List[str]
    needs_update: bool
    release_date: Optional[str] = None
    release_url: Optional[str] = None
    breaking_changes: bool = False
    changelog: Optional[str] = None


class VersionChecker:
    """Monitor library versions and check for updates."""

    def __init__(self, kb_root: Optional[Path] = None):
        """
        Initialize VersionChecker.

        Args:
            kb_root: Root directory of knowledge base
        """
        self.kb_root = kb_root or Path.cwd()
        self.cache_dir = self.kb_root / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Version cache file
        self.version_cache_file = self.cache_dir / "versions.json"

        # Cache duration (in hours)
        self.cache_duration = 24

    def get_cached_versions(self) -> Dict:
        """Get cached version information."""
        if self.version_cache_file.exists():
            try:
                with open(self.version_cache_file, 'r') as f:
                    data = json.load(f)

                # Check if cache is still valid
                cache_time = datetime.fromisoformat(data.get('cached_at', ''))
                if datetime.now() - cache_time < timedelta(hours=self.cache_duration):
                    return data
            except:
                pass

        return {}

    def save_cached_versions(self, versions: Dict):
        """Save version information to cache."""
        versions['cached_at'] = datetime.now().isoformat()
        versions['cache_duration_hours'] = self.cache_duration

        with open(self.version_cache_file, 'w') as f:
            json.dump(versions, f, indent=2)

    def get_python_version(self, package: str = "python") -> Optional[Dict]:
        """
        Get latest Python version from PyPI.

        Args:
            package: Package name on PyPI

        Returns:
            Version information dictionary
        """
        try:
            url = f"https://pypi.org/pypi/{package}/json"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            info = data['info']
            return {
                'library': package,
                'current_version': info['version'],
                'release_date': None,  # PyPI doesn't provide release date in simple format
                'release_url': f"https://pypi.org/project/{package}/",
                'project_url': info.get('project_url'),
                'requires_python': info.get('requires_python')
            }
        except Exception as e:
            print(f"✗ Error getting {package} version: {e}")
            return None

    def get_node_version(self) -> Optional[Dict]:
        """Get latest Node.js version."""
        try:
            url = "https://nodejs.org/dist/index.json"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            return {
                'library': 'node',
                'current_version': data.get('version'),
                'release_date': data.get('date'),
                'release_url': f"https://nodejs.org/dist/{data['version']}/",
                'files_url': f"https://nodejs.org/dist/{data['version']}/"
            }
        except Exception as e:
            print(f"✗ Error getting node version: {e}")
            return None

    def get_npm_version(self, package: str) -> Optional[Dict]:
        """
        Get latest npm package version.

        Args:
            package: npm package name

        Returns:
            Version information dictionary
        """
        try:
            url = f"https://registry.npmjs.org/{package}/latest"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            return {
                'library': package,
                'current_version': data['version'],
                'release_date': None,
                'release_url': f"https://www.npmjs.com/package/{package}",
                'homepage': data.get('homepage'),
                'repository': data.get('repository', {}).get('url')
            }
        except Exception as e:
            print(f"✗ Error getting {package} version: {e}")
            return None

    def get_docker_version(self) -> Optional[Dict]:
        """Get latest Docker version (simplified - from GitHub releases)."""
        try:
            url = "https://api.github.com/repos/docker/docker-ce/releases/latest"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            # Extract version from tag name (e.g., "v20.10.0" -> "20.10.0")
            tag = data.get('tag_name', '')
            version = tag.lstrip('v')

            return {
                'library': 'docker',
                'current_version': version,
                'release_date': data.get('published_at'),
                'release_url': f"https://github.com/docker/docker-ce/releases/tag/{tag}",
                'changelog': data.get('body')
            }
        except Exception as e:
            print(f"✗ Error getting docker version: {e}")
            return None

    def get_postgres_version(self) -> Optional[Dict]:
        """Get latest PostgreSQL version."""
        try:
            url = "https://api.github.com/repos/postgres/postgres/releases/latest"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            tag = data.get('tag_name', '')
            version = re.sub(r'^REL_', '', tag).replace('_', '.')

            return {
                'library': 'postgresql',
                'current_version': version,
                'release_date': data.get('published_at'),
                'release_url': f"https://github.com/postgres/postgres/releases/tag/{tag}",
                'changelog': data.get('body')
            }
        except Exception as e:
            print(f"✗ Error getting postgres version: {e}")
            return None

    def get_fastapi_version(self) -> Optional[Dict]:
        """Get latest FastAPI version."""
        return self.get_python_version('fastapi')

    def get_django_version(self) -> Optional[Dict]:
        """Get latest Django version."""
        return self.get_python_version('django')

    def get_react_version(self) -> Optional[Dict]:
        """Get latest React version."""
        return self.get_npm_version('react')

    def get_vue_version(self) -> Optional[Dict]:
        """Get latest Vue.js version."""
        return self.get_npm_version('vue')

    def check_library_versions(self, libraries: List[str]) -> List[VersionInfo]:
        """
        Check versions for multiple libraries.

        Args:
            libraries: List of library names (python, node, docker, postgresql, etc.)

        Returns:
            List of VersionInfo objects
        """
        versions = []

        for library in libraries:
            version_info = None

            # Map library name to checker function
            checkers = {
                'python': self.get_python_version,
                'node': self.get_node_version,
                'docker': self.get_docker_version,
                'postgresql': self.get_postgres_version,
                'fastapi': self.get_fastapi_version,
                'django': self.get_django_version,
                'react': self.get_react_version,
                'vue': self.get_vue_version,
            }

            checker = checkers.get(library)
            if checker:
                version_info = checker()

            if version_info:
                versions.append(VersionInfo(
                    library=library,
                    current_version=version_info['current_version'],
                    tested_versions=[],
                    entry_ids=[],
                    needs_update=False,
                    release_date=version_info.get('release_date'),
                    release_url=version_info.get('release_url'),
                    changelog=version_info.get('changelog')
                ))

        return versions

    def scan_kb_for_versions(self) -> Dict[str, List[str]]:
        """
        Scan knowledge base for tested versions.

        Returns:
            Dictionary mapping library -> list of tested versions
        """
        library_versions = {}

        # Find all metadata files
        meta_files = list(self.kb_root.rglob("*_meta.yaml"))

        for meta_file in meta_files:
            try:
                with open(meta_file, 'r') as f:
                    meta = yaml.safe_load(f)

                for entry_id, entry_meta in meta.get('entries', {}).items():
                    tested = entry_meta.get('tested_versions', {})

                    for library, version in tested.items():
                        if library not in library_versions:
                            library_versions[library] = set()
                        library_versions[library].add(version)

            except Exception as e:
                print(f"✗ Error reading {meta_file}: {e}")

        # Convert sets to sorted lists
        return {k: sorted(list(v)) for k, v in library_versions.items()}

    def compare_versions(self, current: str, tested: str) -> Tuple[bool, str]:
        """
        Compare two version strings.

        Args:
            current: Current version string
            tested: Tested version string

        Returns:
            Tuple of (is_newer, comparison_result)
        """
        try:
            # Split version numbers
            current_parts = [int(x) for x in current.split('.')[:2]]
            tested_parts = [int(x) for x in tested.split('.')[:2]]

            if current_parts > tested_parts:
                return True, f"{tested} → {current}"
            elif current_parts == tested_parts:
                return False, "equal"
            else:
                return False, f"{tested} (newer: {current})"
        except:
            return False, "unknown"

    def check_updates_needed(self) -> List[VersionInfo]:
        """
        Check which libraries need version updates.

        Returns:
            List of VersionInfo objects with updates needed
        """
        updates_needed = []

        # Scan KB for tested versions
        tested_versions = self.scan_kb_for_versions()

        if not tested_versions:
            print("ℹ️  No tested versions found in knowledge base")
            return []

        # Get current versions
        libraries = list(tested_versions.keys())
        current_versions = self.check_library_versions(libraries)

        # Create version info for each library
        for lib_info in current_versions:
            library = lib_info.library
            tested = tested_versions.get(library, [])

            if tested:
                lib_info.tested_versions = tested

                # Check if any tested version is outdated
                for tested_ver in tested:
                    is_newer, comparison = self.compare_versions(
                        lib_info.current_version,
                        tested_ver
                    )

                    if is_newer:
                        lib_info.needs_update = True
                        break

                # Collect entries that use this library
                if lib_info.needs_update:
                    lib_info.entry_ids = self._find_entries_using_library(library)
                    updates_needed.append(lib_info)

        return updates_needed

    def _find_entries_using_library(self, library: str) -> List[str]:
        """
        Find knowledge base entries that use a specific library.

        Args:
            library: Library name

        Returns:
            List of entry IDs
        """
        entry_ids = []

        # Find all YAML files
        yaml_files = []
        for ext in ['*.yaml', '*.yml']:
            yaml_files.extend(self.kb_root.rglob(ext))

        yaml_files = [f for f in yaml_files if '_meta.yaml' not in str(f)]

        for yaml_file in yaml_files:
            try:
                with open(yaml_file, 'r') as f:
                    content = f.read()

                # Simple search for library mentions
                if library.lower() in content.lower():
                    # Extract entry IDs
                    data = yaml.safe_load(content)
                    if 'errors' in data:
                        for error in data['errors']:
                            entry_ids.append(error.get('id'))
                    elif 'patterns' in data:
                        for pattern in data['patterns']:
                            entry_ids.append(pattern.get('id'))

            except Exception:
                pass

        return list(set(entry_ids))

    def generate_version_report(self) -> str:
        """
        Generate version check report.

        Returns:
            Formatted report string
        """
        print("🔍 Checking library versions...")

        updates_needed = self.check_updates_needed()

        report = f"""
📚 Library Version Report
Generated: {datetime.now().isoformat()}

"""

        if updates_needed:
            report += f"⚠️  Updates Available: {len(updates_needed)} libraries\n\n"

            for lib_info in updates_needed:
                report += f"📦 {lib_info.library.upper()}\n"
                report += f"   Current: {lib_info.current_version}\n"
                report += f"   Tested: {', '.join(lib_info.tested_versions)}\n"
                report += f"   Status: NEEDS UPDATE\n"

                if lib_info.release_url:
                    report += f"   URL: {lib_info.release_url}\n"

                if lib_info.entry_ids:
                    report += f"   Affected entries: {', '.join(lib_info.entry_ids[:5])}"
                    if len(lib_info.entry_ids) > 5:
                        report += f" (+{len(lib_info.entry_ids) - 5} more)"
                    report += "\n"

                report += "\n"

            report += "💡 Recommendations:\n"
            report += "   1. Test with new library versions\n"
            report += "   2. Update knowledge base entries with new versions\n"
            report += "   3. Update tested_versions in metadata\n"

        else:
            report += "✅ All tested versions are up to date!\n"

        return report

    def update_entry_versions(self, library: str, new_version: str) -> int:
        """
        Update tested versions for all entries using a library.

        Args:
            library: Library name
            new_version: New version to set as tested

        Returns:
            Number of entries updated
        """
        from kb_meta import MetadataManager

        manager = MetadataManager(self.kb_root)
        updated = 0

        # Find all metadata files
        meta_files = list(self.kb_root.rglob("*_meta.yaml"))

        for meta_file in meta_files:
            try:
                with open(meta_file, 'r') as f:
                    meta = yaml.safe_load(f)

                for entry_id, entry_meta in meta.get('entries', {}).items():
                    tested_versions = entry_meta.get('tested_versions', {})

                    if library in tested_versions:
                        # Update version
                        tested_versions[library] = new_version

                        yaml_file = meta_file.parent / meta_file.stem.replace('_meta', '.yaml')

                        manager.update_entry_metadata(
                            yaml_file,
                            entry_id,
                            {
                                'tested_versions': tested_versions,
                                'validation_status': 'validated'
                            },
                            agent='version-checker',
                            reason=f"Updated {library} to {new_version}"
                        )

                        updated += 1

            except Exception as e:
                print(f"✗ Error updating {meta_file}: {e}")

        return updated


def main():
    """CLI interface for version monitoring."""
    import argparse

    parser = argparse.ArgumentParser(description="Library Version Monitor")
    parser.add_argument('action', choices=['check', 'update', 'scan'],
                       help='Action to perform')
    parser.add_argument('--kb-root', type=Path, default=Path.cwd(),
                       help='Knowledge base root directory')
    parser.add_argument('--library',
                       help='Specific library to check/update')
    parser.add_argument('--version',
                       help='Version to update to')
    parser.add_argument('--all', action='store_true',
                       help='Check all libraries')
    parser.add_argument('--cache', action='store_true',
                       help='Use cached version data')

    args = parser.parse_args()
    checker = VersionChecker(args.kb_root)

    if args.action == 'check':
        if args.library:
            # Check specific library
            versions = checker.check_library_versions([args.library])
            if versions:
                v = versions[0]
                print(f"\n📦 {args.library.upper()}")
                print(f"Current version: {v.current_version}")
                print(f"Release URL: {v.release_url}")
            else:
                print(f"✗ Unknown library: {args.library}")
        else:
            # Check all and generate report
            report = checker.generate_version_report()
            print(report)

    elif args.action == 'update':
        if not args.library or not args.version:
            print("--library and --version required for update action")
            return 1

        updated = checker.update_entry_versions(args.library, args.version)
        print(f"✓ Updated {updated} entries to {args.library} {args.version}")

    elif args.action == 'scan':
        tested = checker.scan_kb_for_versions()

        print(f"\n📚 Tested Versions in Knowledge Base\n")
        for library, versions in tested.items():
            print(f"{library}: {', '.join(versions)}")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
