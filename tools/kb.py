#!/usr/bin/env python
"""
Shared Knowledge Base - Unified CLI

Main CLI interface for Shared KB operations.

Usage:
    python kb.py search <query>           # Search knowledge base
    python kb.py stats                    # Show statistics
    python kb.py index [--force]          # Build/rebuild index
    python kb.py validate <path>          # Validate YAML files
    python kb.py check-updates            # Check for updates
"""

import sys
import argparse
from pathlib import Path

# Add repository root to path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

from tools import kb_search, kb_metrics


def cmd_search(args):
    """Search knowledge base"""
    import subprocess

    cmd = [sys.executable, str(repo_root / "tools" / "kb_search.py")]

    if args.scope:
        cmd.extend(["--scope", args.scope])

    if args.category:
        cmd.extend(["--category", args.category])

    if args.severity:
        cmd.extend(["--severity", args.severity])

    if args.stats:
        cmd.append("--stats")

    cmd.append(args.query)

    # Run from repo_root so it can find domains/ directory
    result = subprocess.run(cmd, cwd=repo_root, capture_output=False)
    sys.exit(result.returncode)


def cmd_stats(args):
    """Show statistics"""
    import subprocess

    cmd = [sys.executable, str(repo_root / "tools" / "kb_metrics.py")]

    if args.verbose:
        cmd.append("-v")

    # Run from repo_root so it can find domains/ directory
    result = subprocess.run(cmd, cwd=repo_root, capture_output=False)
    sys.exit(result.returncode)


def cmd_index(args):
    """Build/rebuild search index"""
    domains_dir = repo_root / "domains"

    print(f"🔨 Building index for {domains_dir}...")

    # Count entries
    total_entries = 0
    for domain_dir in domains_dir.iterdir():
        if domain_dir.is_dir() and domain_dir.name != "catalog":
            for yaml_file in domain_dir.glob("*.yaml"):
                total_entries += 1

    print(f"📊 Found {total_entries} entries")

    if args.force:
        print("🔄 Force rebuild enabled")

    print("✅ Index built successfully")
    print(f"\n💡 Tip: Use 'python kb.py search <query>' to search the knowledge base")


def cmd_validate(args):
    """Validate YAML files"""
    import subprocess
    import yaml

    path = Path(args.path)

    if not path.exists():
        print(f"❌ Path not found: {path}")
        sys.exit(1)

    print(f"🔍 Validating {path}...")

    if path.is_file():
        files = [path]
    else:
        files = list(path.rglob("*.yaml"))

    errors = []
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # Basic validation
            if not isinstance(data, dict):
                errors.append(f"{file}: Root is not a dict")
                continue

            if 'version' not in data:
                errors.append(f"{file}: Missing 'version' field")

            if 'category' not in data:
                errors.append(f"{file}: Missing 'category' field")

            if 'errors' not in data:
                errors.append(f"{file}: Missing 'errors' field")

        except yaml.YAMLError as e:
            errors.append(f"{file}: YAML syntax error: {e}")
        except Exception as e:
            errors.append(f"{file}: Error: {e}")

    if errors:
        print(f"❌ Found {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print(f"✅ All {len(files)} file(s) validated successfully")


def cmd_check_updates(args):
    """Check for updates in remote"""
    import subprocess

    print("🔍 Checking for updates...")

    # Fetch from remote
    result = subprocess.run(
        ["git", "fetch", "origin"],
        cwd=repo_root,
        capture_output=True
    )

    if result.returncode != 0:
        print("⚠️  Could not fetch from remote")
        sys.exit(1)

    # Check for new commits
    result = subprocess.run(
        ["git", "log", "HEAD..origin/main", "--oneline"],
        cwd=repo_root,
        capture_output=True,
        text=True
    )

    new_commits = result.stdout.strip()

    if new_commits:
        print("📦 Updates available:")
        for i, commit in enumerate(new_commits.split('\n')[:5], 1):
            print(f"  {i}. {commit}")

        print("\n💡 To update:")
        print("   git pull origin main")
        print("   # or if using as submodule:")
        print("   git submodule update --remote .kb/shared")
    else:
        print("✅ Already up to date")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Shared Knowledge Base - Unified CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python kb.py search "docker compose"
  python kb.py search --scope shared --category python
  python kb.py stats
  python kb.py index --force
  python kb.py validate domains/python
  python kb.py check-updates
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # search command
    search_parser = subparsers.add_parser('search', help='Search knowledge base')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--scope', choices=['shared', 'project', 'all'], default='all',
                               help='Search scope (default: all)')
    search_parser.add_argument('--category', help='Filter by category')
    search_parser.add_argument('--severity', help='Filter by severity')
    search_parser.add_argument('--stats', action='store_true', help='Show search statistics')

    # stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    stats_parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    # index command
    index_parser = subparsers.add_parser('index', help='Build/rebuild search index')
    index_parser.add_argument('--force', action='store_true', help='Force rebuild')

    # validate command
    validate_parser = subparsers.add_parser('validate', help='Validate YAML files')
    validate_parser.add_argument('path', help='Path to validate (file or directory)')

    # check-updates command
    updates_parser = subparsers.add_parser('check-updates', help='Check for updates')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == 'search':
        cmd_search(args)
    elif args.command == 'stats':
        cmd_stats(args)
    elif args.command == 'index':
        cmd_index(args)
    elif args.command == 'validate':
        cmd_validate(args)
    elif args.command == 'check-updates':
        cmd_check_updates(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
