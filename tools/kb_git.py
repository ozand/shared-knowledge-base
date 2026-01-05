#!/usr/bin/env python3
"""
kb_git.py - Git-based Change Detection

Detects changes in knowledge base using git commands.
Provides integration with git version control for automatic change detection.

Author: Knowledge Base Curator
Version: 1.0.0
License: MIT
"""

import subprocess
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple


class GitChangeDetector:
    """Detect changes using git commands."""

    def __init__(self, kb_root: Optional[Path] = None):
        """
        Initialize GitChangeDetector.

        Args:
            kb_root: Root directory of knowledge base (must be a git repo)
        """
        self.kb_root = kb_root or Path.cwd()
        self.git_dir = self.kb_root / ".git"

        if not self.git_dir.exists():
            print("⚠️  Not a git repository")
            self.is_git_repo = False
        else:
            self.is_git_repo = True

    def has_git(self) -> bool:
        """Check if directory is a git repository."""
        return self.is_git_repo

    def _run_git(self, args: List[str]) -> subprocess.CompletedProcess:
        """
        Run git command.

        Args:
            args: Git command arguments

        Returns:
            CompletedProcess result
        """
        full_cmd = ["git"] + args
        return subprocess.run(
            full_cmd,
            cwd=self.kb_root,
            capture_output=True,
            text=True
        )

    def get_changed_files_since(self, ref: str = "HEAD@{1}") -> List[str]:
        """
        Get list of changed files since git ref.

        Args:
            ref: Git reference (default: HEAD@{1} for last state)

        Returns:
            List of changed file paths
        """
        if not self.has_git():
            return []

        try:
            result = self._run_git(["diff", "--name-only", ref, "HEAD"])

            if result.returncode == 0:
                files = result.stdout.strip().split('\n')
                return [f for f in files if f.endswith('.yaml')]

        except Exception as e:
            print(f"✗ Git error: {e}")

        return []

    def get_changed_entries_since_last_pull(self) -> List[Dict]:
        """
        Get entries changed since last git pull.

        Returns:
            List of changed entry dictionaries
        """
        files = self.get_changed_files_since("HEAD@{1}")
        entries = []

        for file_path in files:
            # Extract entry IDs from file
            full_path = self.kb_root / file_path
            if full_path.exists() and "_meta.yaml" not in str(full_path):
                entry_ids = self._extract_entry_ids(full_path)
                entries.extend([{
                    "entry_id": entry_id,
                    "file": file_path,
                    "action": "modified"
                } for entry_id in entry_ids])

        return entries

    def _extract_entry_ids(self, yaml_file: Path) -> List[str]:
        """
        Extract entry IDs from YAML file.

        Args:
            yaml_file: Path to YAML file

        Returns:
            List of entry IDs
        """
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            entry_ids = []
            if 'errors' in data:
                for error in data['errors']:
                    entry_ids.append(error.get('id'))
            elif 'patterns' in data:
                for pattern in data['patterns']:
                    entry_ids.append(pattern.get('id'))

            return [eid for eid in entry_ids if eid]

        except Exception as e:
            print(f"✗ Error reading {yaml_file}: {e}")
            return []

    def get_files_modified_in_period(self, days: int = 7) -> List[str]:
        """
        Get files modified in the last N days.

        Args:
            days: Number of days to look back

        Returns:
            List of modified file paths
        """
        if not self.has_git():
            return []

        try:
            since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            result = self._run_git([
                "log",
                f"--since={since_date}",
                "--name-only",
                "--pretty=format:"
            ])

            if result.returncode == 0:
                files = result.stdout.strip().split('\n')
                yaml_files = [f for f in files if f.endswith('.yaml')]
                return list(set(yaml_files))  # Deduplicate

        except Exception as e:
            print(f"✗ Git error: {e}")

        return []

    def get_last_commit_date(self) -> Optional[datetime]:
        """
        Get date of last commit.

        Returns:
            Last commit datetime or None
        """
        if not self.has_git():
            return None

        try:
            result = self._run_git(["log", "-1", "--format=%ci"])
            if result.returncode == 0:
                timestamp = result.stdout.strip()
                return datetime.fromisoformat(timestamp)

        except Exception as e:
            print(f"✗ Git error: {e}")

        return None

    def get_commit_history(self, file_path: str, limit: int = 10) -> List[Dict]:
        """
        Get commit history for a file.

        Args:
            file_path: Path to file
            limit: Maximum number of commits to return

        Returns:
            List of commit dictionaries
        """
        if not self.has_git():
            return []

        try:
            result = self._run_git([
                "log",
                f"--max-count={limit}",
                "--format=%ci|%H|%s",
                "--",
                file_path
            ])

            if result.returncode == 0:
                commits = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('|', 2)
                        if len(parts) == 3:
                            commits.append({
                                "date": parts[0],
                                "hash": parts[1],
                                "message": parts[2]
                            })
                return commits

        except Exception as e:
            print(f"✗ Git error: {e}")

        return []

    def get_branch(self) -> Optional[str]:
        """
        Get current git branch.

        Returns:
            Branch name or None
        """
        if not self.has_git():
            return None

        try:
            result = self._run_git(["rev-parse", "--abbrev-ref", "HEAD"])
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception as e:
            print(f"✗ Git error: {e}")

        return None

    def is_clean_working_dir(self) -> bool:
        """
        Check if working directory is clean (no uncommitted changes).

        Returns:
            True if working directory is clean
        """
        if not self.has_git():
            return True

        try:
            result = self._run_git(["status", "--porcelain"])
            return result.stdout.strip() == ""
        except:
            return True

    def stage_file(self, file_path: str) -> bool:
        """
        Stage a file for commit.

        Args:
            file_path: Path to file

        Returns:
            True if successful
        """
        if not self.has_git():
            return False

        try:
            result = self._run_git(["add", file_path])
            return result.returncode == 0
        except Exception as e:
            print(f"✗ Git error: {e}")
            return False

    def unstage_file(self, file_path: str) -> bool:
        """
        Unstage a file.

        Args:
            file_path: Path to file

        Returns:
            True if successful
        """
        if not self.has_git():
            return False

        try:
            result = self._run_git(["reset", "HEAD", "--", file_path])
            return result.returncode == 0
        except Exception as e:
            print(f"✗ Git error: {e}")
            return False


def main():
    """CLI interface for git change detection."""
    import argparse

    parser = argparse.ArgumentParser(description="Git-based Change Detection")
    parser.add_argument('action', choices=['changes', 'files', 'history', 'status'],
                       help='Action to perform')
    parser.add_argument('--kb-root', type=Path, default=Path.cwd(),
                       help='Knowledge base root directory')
    parser.add_argument('--ref', default='HEAD@{1}',
                       help='Git reference for comparison')
    parser.add_argument('--days', type=int, default=7,
                       help='Number of days for period search')
    parser.add_argument('--file',
                       help='File to get history for')
    parser.add_argument('--limit', type=int, default=10,
                       help='Limit for history')

    args = parser.parse_args()
    detector = GitChangeDetector(args.kb_root)

    if not detector.has_git():
        print("❌ Not a git repository")
        return 1

    if args.action == 'changes':
        print("🔍 Detecting changes since last state...\n")

        # Get changed files
        files = detector.get_changed_files_since(args.ref)

        print(f"📝 Changed files: {len(files)}")
        for f in files:
            print(f"  - {f}")

        # Get changed entries
        entries = detector.get_changed_entries_since_last_pull()
        print(f"\n📚 Changed entries: {len(entries)}")
        for entry in entries:
            print(f"  - {entry['entry_id']} in {entry['file']}")

    elif args.action == 'files':
        print(f"🔍 Files modified in last {args.days} days:\n")

        files = detector.get_files_modified_in_period(args.days)
        print(f"Total: {len(files)} files\n")

        for f in files:
            print(f"  - {f}")

    elif args.action == 'history':
        if not args.file:
            print("--file required for history action")
            return 1

        print(f"📜 Commit history for {args.file}:\n")

        commits = detector.get_commit_history(args.file, args.limit)
        for i, commit in enumerate(commits, 1):
            print(f"{i}. {commit['date']}")
            print(f"   {commit['hash'][:8]} - {commit['message']}")
            print()

    elif args.action == 'status':
        print("📊 Git Status\n")

        branch = detector.get_branch()
        print(f"Branch: {branch or 'unknown'}")

        last_commit = detector.get_last_commit_date()
        print(f"Last commit: {last_commit or 'unknown'}")

        clean = detector.is_clean_working_dir()
        print(f"Working dir: {'clean' if clean else 'has uncommitted changes'}")

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
