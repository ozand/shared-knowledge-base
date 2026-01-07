#!/usr/bin/env python3
"""
kb_github_api - GitHub API-based domain loader

Use when Git sparse checkout is not available.

Usage:
    from tools.kb_github_api import GitHubDomainLoader

    loader = GitHubDomainLoader()
    index = loader.load_domain_index()
    entries = loader.load_domain('testing')
"""

import requests
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import time

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/ozand/shared-knowledge-base/main"
GITHUB_API_BASE = "https://api.github.com/repos/ozand/shared-knowledge-base"


class GitHubDomainLoader:
    """Load domains via GitHub API (fallback)."""

    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub API loader.

        Args:
            token: Optional GitHub personal access token for authenticated requests
                   (increases rate limit from 60 to 5000 requests/hour)
        """
        self.raw_base = GITHUB_RAW_BASE
        self.api_base = GITHUB_API_BASE
        self.token = token
        self.session = requests.Session()

        if token:
            self.session.headers.update({
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            })

    def load_domain_index(self) -> Dict:
        """
        Load _domain_index.yaml from GitHub.

        Returns:
            Domain index dictionary

        Raises:
            requests.RequestException: If download fails
        """
        url = f"{self.raw_base}/_domain_index.yaml"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()

        return yaml.safe_load(response.content)

    def load_domain(self, domain_name: str) -> List[Dict]:
        """
        Load all entries for specific domain.

        Args:
            domain_name: Name of domain to load (e.g., 'testing', 'asyncio')

        Returns:
            List of YAML entries (parsed)

        Raises:
            ValueError: If domain not found
            requests.RequestException: If download fails
        """
        index = self.load_domain_index()

        if domain_name not in index.get('domains', {}):
            available = ', '.join(index.get('domains', {}).keys())
            raise ValueError(f"Domain '{domain_name}' not found. Available: {available}")

        domain_data = index['domains'][domain_name]
        entries = []

        print(f"Loading domain '{domain_name}' from GitHub...")
        print(f"  Files: {len(domain_data['files'])}")

        for i, file_path in enumerate(domain_data['files'], 1):
            try:
                # Download file
                url = f"{self.raw_base}/{file_path}"
                response = self.session.get(url, timeout=30)
                response.raise_for_status()

                # Parse YAML
                content = yaml.safe_load(response.content)

                if not content:
                    continue

                # Extract entries (errors or patterns)
                entries_list = content.get('errors', []) or content.get('patterns', [])
                entries.extend(entries_list)

                print(f"  [{i}/{len(domain_data['files'])}] ✓ {file_path}")

                # Rate limiting: sleep between requests
                if i < len(domain_data['files']):
                    time.sleep(0.5)

            except Exception as e:
                print(f"  [{i}/{len(domain_data['files'])}] ✗ {file_path}: {e}")
                continue

        print(f"\n✅ Loaded {len(entries)} entries from '{domain_name}' domain")

        return entries

    def get_domain_file(self, file_path: str) -> Optional[Dict]:
        """
        Get specific file from GitHub.

        Args:
            file_path: Path relative to repository root

        Returns:
            Parsed YAML content or None if error
        """
        try:
            url = f"{self.raw_base}/{file_path}"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return yaml.safe_load(response.content)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None

    def save_domain_locally(self, domain_name: str, output_dir: Path, index: Optional[Dict] = None):
        """
        Download and save domain files locally.

        Useful for offline access or caching.

        Args:
            domain_name: Domain to download
            output_dir: Directory to save files
            index: Optional domain index (will load if not provided)
        """
        if index is None:
            index = self.load_domain_index()

        if domain_name not in index.get('domains', {}):
            raise ValueError(f"Domain '{domain_name}' not found")

        domain_data = index['domains'][domain_name]
        output_dir = Path(output_dir) / domain_name
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"Saving domain '{domain_name}' to {output_dir}")

        for file_path in domain_data['files']:
            content = self.get_domain_file(file_path)

            if content:
                # Preserve filename
                local_path = output_dir / Path(file_path).name

                with open(local_path, 'w', encoding='utf-8') as f:
                    yaml.safe_dump(content, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

                print(f"  ✓ {local_path}")

        print(f"\n✅ Saved {len(domain_data['files'])} files to {output_dir}")

    def search_entries(self, query: str, domain: Optional[str] = None) -> List[Dict]:
        """
        Search entries by query string.

        Args:
            query: Search query (matches against title, problem, solution)
            domain: Optional domain to limit search

        Returns:
            List of matching entries
        """
        index = self.load_domain_index()
        results = []

        domains_to_search = [domain] if domain else index.get('domains', {}).keys()

        for domain_name in domains_to_search:
            if domain_name not in index.get('domains', {}):
                continue

            domain_data = index['domains'][domain_name]

            for entry_id in domain_data.get('entry_ids', []):
                # Load entry details
                # For simplicity, just return matching IDs
                if query.lower() in entry_id.lower():
                    results.append({
                        'id': entry_id,
                        'domain': domain_name
                    })

        return results

    def get_rate_limit_status(self) -> Dict:
        """
        Check GitHub API rate limit status.

        Returns:
            Rate limit information
        """
        try:
            response = self.session.get(f"{self.api_base}/rate_limit", timeout=10)
            response.raise_for_status()
            data = response.json()

            core = data.get('resources', {}).get('core', {})

            return {
                'limit': core.get('limit'),
                'remaining': core.get('remaining'),
                'reset': core.get('reset'),
                'authenticated': self.token is not None
            }
        except Exception as e:
            return {'error': str(e)}


def main():
    """CLI interface for kb_github_api."""
    import argparse

    parser = argparse.ArgumentParser(
        description='GitHub API-based domain loader',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Load domain index
  python tools/kb_github_api.py index

  # Load specific domain
  python tools/kb_github_api.py load testing

  # Save domain locally
  python tools/kb_github_api.py save testing --output ./cache

  # Check rate limit
  python tools/kb_github_api.py rate-limit
        """
    )

    parser.add_argument('--token', help='GitHub personal access token')
    parser.add_argument('--repo', default='ozand/shared-knowledge-base', help='Repository')

    subparsers = parser.add_subparsers(dest='command', help='Command')

    # Index command
    subparsers.add_parser('index', help='Load domain index')

    # Load command
    parser_load = subparsers.add_parser('load', help='Load domain entries')
    parser_load.add_argument('domain', help='Domain name')
    parser_load.add_argument('--format', choices=['yaml', 'json'], default='yaml', help='Output format')

    # Save command
    parser_save = subparsers.add_parser('save', help='Save domain locally')
    parser_save.add_argument('domain', help='Domain name')
    parser_save.add_argument('--output', '-o', default='./cache', help='Output directory')

    # Rate limit command
    subparsers.add_parser('rate-limit', help='Check API rate limit')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    loader = GitHubDomainLoader(token=args.token)

    try:
        if args.command == 'index':
            index = loader.load_domain_index()
            print(yaml.safe_dump(index, allow_unicode=True, sort_keys=False))

        elif args.command == 'load':
            entries = loader.load_domain(args.domain)

            if args.format == 'yaml':
                print(yaml.safe_dump(entries, allow_unicode=True, sort_keys=False))
            else:
                print(json.dumps(entries, indent=2))

        elif args.command == 'save':
            loader.save_domain_locally(args.domain, args.output)

        elif args.command == 'rate-limit':
            status = loader.get_rate_limit_status()

            if 'error' in status:
                print(f"Error: {status['error']}")
                return 1

            print(f"Rate Limit Status:")
            print(f"  Authenticated: {status['authenticated']}")
            print(f"  Limit: {status['limit']} requests/hour")
            print(f"  Remaining: {status['remaining']} requests")
            print(f"  Resets at: {status['reset']}")

        return 0

    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
