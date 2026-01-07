#!/usr/bin/env python3
"""
kb_domains - Domain-based knowledge base management

Commands:
    migrate      Add domain metadata to existing entries
    index        Generate/update _domain_index.yaml
    validate     Check domain metadata consistency
    load         Load specific domain (sparse checkout)
    list         List all domains with metadata

Usage:
    python tools/kb_domains.py migrate --from-tags
    python tools/kb_domains.py index --update
    python tools/kb_domains.py list
"""

import argparse
import yaml
import re
from pathlib import Path
from collections import defaultdict
import sys
import subprocess
from typing import Dict, List, Any, Optional
from datetime import datetime

# Domain taxonomy definition
DOMAIN_TAXONOMY = {
    'testing': {
        'description': 'Test patterns, pytest, unittest, mocking',
        'keywords': ['test', 'pytest', 'unittest', 'mock', 'fixture', 'assert', 'suite'],
        'related': ['asyncio']
    },
    'asyncio': {
        'description': 'Async/await, task groups, timeouts, cancellation',
        'keywords': ['async', 'await', 'asyncio', 'task', 'coroutine', 'future', 'timeout', 'event-loop'],
        'related': ['testing']
    },
    'fastapi': {
        'description': 'FastAPI framework patterns',
        'keywords': ['fastapi', 'dependency', 'route', 'websocket', 'api-router', 'middleware'],
        'related': ['websocket', 'authentication']
    },
    'websocket': {
        'description': 'WebSocket patterns and implementations',
        'keywords': ['websocket', 'ws', 'connection', 'socket'],
        'related': ['fastapi', 'asyncio']
    },
    'docker': {
        'description': 'Docker containers, volumes, networks',
        'keywords': ['docker', 'container', 'volume', 'network', 'dockerfile', 'compose'],
        'related': ['deployment']
    },
    'postgresql': {
        'description': 'PostgreSQL database operations',
        'keywords': ['postgres', 'postgresql', 'sql', 'database', 'query', 'psycopg'],
        'related': ['docker']
    },
    'authentication': {
        'description': 'Auth, CSRF, sessions, JWT',
        'keywords': ['auth', 'csrf', 'jwt', 'session', 'login', 'oauth', 'token'],
        'related': ['fastapi']
    },
    'deployment': {
        'description': 'DevOps, CI/CD, deployment',
        'keywords': ['deploy', 'ci', 'cd', 'production', 'release', 'kubernetes'],
        'related': ['docker']
    },
    'monitoring': {
        'description': 'Logging, metrics, observability',
        'keywords': ['log', 'metric', 'monitor', 'trace', 'observability', 'prometheus'],
        'related': []
    },
    'performance': {
        'description': 'Optimization, profiling, performance',
        'keywords': ['optimize', 'performance', 'profile', 'cache', 'memory', 'cpu'],
        'related': ['asyncio']
    },
    'security': {
        'description': 'Security patterns and best practices',
        'keywords': ['security', 'vulnerability', 'xss', 'injection', 'encryption'],
        'related': ['authentication']
    },
    'api': {
        'description': 'API design and REST patterns',
        'keywords': ['api', 'rest', 'http', 'endpoint', 'json', 'response'],
        'related': ['fastapi']
    }
}


class DomainManager:
    """Manage domain-based knowledge organization."""

    def __init__(self, kb_dir: Optional[Path] = None):
        self.kb_dir = kb_dir or Path.cwd()
        self.domain_index_path = self.kb_dir / "_domain_index.yaml"

    def migrate_from_tags(self, dry_run: bool = False):
        """
        Auto-generate domain metadata from existing tags.

        Strategy:
        1. Read all YAML entries
        2. Extract tags from each entry
        3. Match tags to domain keywords
        4. Assign primary domain (best match)
        5. Assign secondary domains (related matches)
        """
        print("🔍 Scanning entries for domain migration...")

        updated_count = 0
        reviewed_count = 0

        for yaml_file in self.kb_dir.rglob("*.yaml"):
            # Skip index files and meta files
            if any(x in yaml_file.name for x in ['_meta', '_index', '_domain']):
                continue

            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    content = yaml.safe_load(f)

                if not content:
                    continue

                # Handle both errors and patterns
                entries = content.get('errors', []) or content.get('patterns', [])
                if not entries:
                    continue

                file_updated = False

                for entry in entries:
                    if 'domains' in entry:
                        continue  # Already has domains

                    tags = entry.get('tags', [])
                    if not tags:
                        continue

                    domains = self._infer_domains_from_tags(tags)

                    if domains:
                        entry['domains'] = domains
                        file_updated = True
                        reviewed_count += 1
                        print(f"  ✓ {entry['id']}: {domains['primary']}" +
                              (f" (+{len(domains['secondary'])} secondary)" if domains['secondary'] else ""))

                if file_updated:
                    updated_count += 1
                    if not dry_run:
                        with open(yaml_file, 'w', encoding='utf-8') as f:
                            yaml.safe_dump(content, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

            except Exception as e:
                print(f"  ⚠ Error processing {yaml_file.name}: {e}")
                continue

        if dry_run:
            print(f"\n📊 Dry run: Would update {updated_count} files ({reviewed_count} entries)")
        else:
            print(f"\n✅ Updated {updated_count} files ({reviewed_count} entries) with domain metadata")

    def _infer_domains_from_tags(self, tags: List[str]) -> Dict[str, Any]:
        """
        Infer domain from tags using keyword matching.

        Returns:
            {
                'primary': 'domain_name',
                'secondary': ['related_domain1', 'related_domain2']
            }
        """
        scores = {}

        # Score each domain based on tag matches
        for domain_name, domain_info in DOMAIN_TAXONOMY.items():
            score = 0
            matched_keywords = []

            for keyword in domain_info['keywords']:
                for tag in tags:
                    if keyword.lower() in tag.lower():
                        score += 1
                        if keyword not in matched_keywords:
                            matched_keywords.append(keyword)

            if score > 0:
                scores[domain_name] = {'score': score, 'keywords': matched_keywords}

        if not scores:
            return {}

        # Primary domain = highest score
        primary_domain = max(scores, key=lambda x: scores[x]['score'])

        # Secondary domains = related domains that also have matches
        secondary_domains = []
        for related_domain in DOMAIN_TAXONOMY[primary_domain]['related']:
            if related_domain in scores:
                secondary_domains.append(related_domain)

        return {
            'primary': primary_domain,
            'secondary': secondary_domains
        }

    def generate_index(self):
        """
        Generate _domain_index.yaml from all entries.

        Process:
        1. Scan all YAML files
        2. Extract domain metadata
        3. Calculate token estimates
        4. Generate cross-reference matrix
        5. Write _domain_index.yaml
        """
        print("📊 Generating domain index...")

        domains_data = defaultdict(lambda: {
            'entries': [],
            'entry_ids': [],
            'files': set(),
            'tags': set(),
            'scopes': defaultdict(int),
            'token_estimate': 0
        })

        total_entries = 0
        total_tokens = 0
        entries_with_domains = 0

        for yaml_file in self.kb_dir.rglob("*.yaml"):
            # Skip index and meta files
            if any(x in yaml_file.name for x in ['_meta', '_index', '_domain']):
                continue

            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    content = yaml.safe_load(f)

                if not content:
                    continue

                entries = content.get('errors', []) or content.get('patterns', [])
                if not entries:
                    continue

                scope = self._infer_scope_from_path(yaml_file)
                file_token_estimate = 0

                for entry in entries:
                    # Count all entries
                    total_entries += 1

                    if 'domains' not in entry:
                        continue

                    entries_with_domains += 1
                    domain_name = entry['domains']['primary']

                    # Add entry info
                    domains_data[domain_name]['entries'].append({
                        'id': entry['id'],
                        'title': entry.get('title', ''),
                        'severity': entry.get('severity', 'unknown')
                    })
                    domains_data[domain_name]['entry_ids'].append(entry['id'])
                    domains_data[domain_name]['files'].add(str(yaml_file.relative_to(self.kb_dir)))
                    domains_data[domain_name]['scopes'][scope] += 1

                    # Extract tags
                    for tag in entry.get('tags', []):
                        domains_data[domain_name]['tags'].add(tag)

                    # Estimate tokens (rough estimate: 150 tokens per entry)
                    token_estimate = 150
                    domains_data[domain_name]['token_estimate'] += token_estimate
                    file_token_estimate += token_estimate
                    total_tokens += token_estimate

            except Exception as e:
                print(f"  ⚠ Error indexing {yaml_file.name}: {e}")
                continue

        # Convert to final format
        index = {
            'version': '2.0',
            'last_updated': datetime.now().isoformat(),
            'total_entries': total_entries,
            'entries_with_domains': entries_with_domains,
            'coverage_percentage': round((entries_with_domains / total_entries * 100) if total_entries > 0 else 0, 1),
            'total_tokens_estimate': total_tokens,
            'domains': {}
        }

        for domain_name, data in sorted(domains_data.items()):
            index['domains'][domain_name] = {
                'entries': len(data['entries']),
                'entry_ids': sorted(list(set(data['entry_ids']))),
                'token_estimate': data['token_estimate'],
                'last_updated': datetime.now().strftime('%Y-%m-%d'),
                'tags': sorted(list(data['tags']))[:15],  # Top 15 tags
                'scopes': dict(data['scopes']),
                'files': sorted(list(data['files']))
            }

        # Add cross-reference matrix
        index['related_domains'] = self._generate_related_domains()

        # Write index
        with open(self.domain_index_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(index, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

        print(f"✅ Generated _domain_index.yaml")
        print(f"   Total entries: {total_entries}")
        print(f"   With domains: {entries_with_domains} ({index['coverage_percentage']}%)")
        print(f"   Total domains: {len(index['domains'])}")
        print(f"   Total tokens: ~{total_tokens}")

    def _infer_scope_from_path(self, file_path: Path) -> str:
        """Infer scope from file path."""
        path_str = str(file_path)

        if 'universal' in path_str:
            return 'universal'
        elif 'python' in path_str:
            return 'python'
        elif 'javascript' in path_str:
            return 'javascript'
        elif 'docker' in path_str:
            return 'docker'
        elif 'postgresql' in path_str:
            return 'postgresql'
        elif 'framework' in path_str:
            return 'framework'
        else:
            return 'project'

    def _generate_related_domains(self) -> List[List[str]]:
        """Generate cross-domain relationship matrix."""
        related = []
        for domain_name, domain_info in DOMAIN_TAXONOMY.items():
            for related_domain in domain_info['related']:
                if [domain_name, related_domain] not in related and [related_domain, domain_name] not in related:
                    related.append([domain_name, related_domain])
        return related

    def validate(self):
        """Validate domain metadata consistency."""
        print("🔍 Validating domain metadata...")

        errors = []
        warnings = []

        # Check if index exists
        if not self.domain_index_path.exists():
            errors.append("_domain_index.yaml does not exist. Run 'index' command first.")
            return False

        # Load index
        with open(self.domain_index_path, 'r') as f:
            index = yaml.safe_load(f)

        # Validate domains
        for domain_name in index.get('domains', {}):
            if domain_name not in DOMAIN_TAXONOMY:
                warnings.append(f"Domain '{domain_name}' not in DOMAIN_TAXONOMY")

        # Check entries without domains
        total = index.get('total_entries', 0)
        with_domains = index.get('entries_with_domains', 0)
        without_domains = total - with_domains

        if without_domains > 0:
            warnings.append(f"{without_domains} entries without domain metadata ({without_domains/total*100:.1f}%)")

        # Print results
        if errors:
            print(f"❌ Validation failed with {len(errors)} errors:")
            for error in errors:
                print(f"   - {error}")
            return False

        print(f"✅ Validation passed")
        if warnings:
            print(f"⚠ {len(warnings)} warnings:")
            for warning in warnings:
                print(f"   - {warning}")

        print(f"   Domains: {len(index.get('domains', {}))}")
        print(f"   Entries: {with_domains}/{total} ({index.get('coverage_percentage', 0)}%)")

        return True

    def list_domains(self):
        """List all domains with metadata."""
        if not self.domain_index_path.exists():
            print("❌ _domain_index.yaml not found. Run 'index' command first.")
            return

        with open(self.domain_index_path, 'r') as f:
            index = yaml.safe_load(f)

        print(f"\n📚 Knowledge Base Domains")
        print(f"   Total entries: {index.get('total_entries', 0)}")
        print(f"   With domains: {index.get('entries_with_domains', 0)} ({index.get('coverage_percentage', 0)}%)")
        print(f"   Total tokens: ~{index.get('total_tokens_estimate', 0)}")
        print()

        for domain_name, data in sorted(index.get('domains', {}).items(),
                                       key=lambda x: x[1] if isinstance(x[1], int) else x[1].get('entries', 0),
                                       reverse=True):
            # Support both flat format (int) and nested format (dict) for compatibility
            if isinstance(data, int):
                # Flat format (v4.0.0 standard)
                entry_count = data
                token_count = 0  # Not available in flat format
                tags = []
            else:
                # Nested format (future compatibility)
                entry_count = data.get('entries', 0)
                token_count = data.get('token_estimate', 0)
                tags = data.get('tags', [])

            print(f"  {domain_name:20} {entry_count:3} entries", end='')
            if token_count > 0:
                print(f", ~{token_count:4} tokens", end='')
            print()

            if tags:
                print(f"  {'':20} Tags: {', '.join(tags[:5])}")
            print()

    def load_domain(self, domain_name: str):
        """
        Load specific domain using Git sparse checkout.

        Command: git sparse-checkout add <files>
        """
        print(f"📦 Loading domain: {domain_name}")

        # Load index
        if not self.domain_index_path.exists():
            print("❌ _domain_index.yaml not found. Run 'index' command first.")
            return

        with open(self.domain_index_path, 'r') as f:
            index = yaml.safe_load(f)

        if domain_name not in index.get('domains', {}):
            print(f"❌ Domain not found: {domain_name}")
            print(f"   Available domains: {', '.join(index.get('domains', {}).keys())}")
            return

        domain_data = index['domains'][domain_name]
        files = domain_data['files']

        print(f"  Files: {len(files)}")
        print(f"  Entries: {domain_data['entries']}")
        print(f"  Tokens: ~{domain_data['token_estimate']}")

        # Check if in git repository
        if not (self.kb_dir / '.git').exists():
            print("❌ Not in a git repository. Cannot use sparse checkout.")
            print("   Use GitHub API fallback instead.")
            return

        # Execute git sparse-checkout
        loaded_count = 0
        for file_path in files:
            try:
                result = subprocess.run(
                    ['git', 'sparse-checkout', 'add', file_path],
                    cwd=self.kb_dir,
                    check=True,
                    capture_output=True,
                    text=True
                )
                loaded_count += 1
                if loaded_count <= 5:  # Show first 5
                    print(f"  ✓ {file_path}")
            except subprocess.CalledProcessError as e:
                print(f"  ⚠ Failed to load {file_path}: {e.stderr.strip()}")

        if loaded_count > 5:
            print(f"  ... and {loaded_count - 5} more files")

        print(f"\n✅ Loaded domain '{domain_name}' (~{domain_data['token_estimate']} tokens, {loaded_count} files)")


def main():
    parser = argparse.ArgumentParser(
        description='Domain-based KB management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Migrate entries from tags
  python tools/kb_domains.py migrate --from-tags

  # Generate domain index
  python tools/kb_domains.py index --update

  # List all domains
  python tools/kb_domains.py list

  # Load specific domain
  python tools/kb_domains.py load testing
        """
    )

    parser.add_argument('--kb-dir', type=Path, default=Path.cwd(), help='KB directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    subparsers = parser.add_subparsers(dest='command', help='Command')

    # Migrate command
    parser_migrate = subparsers.add_parser('migrate', help='Add domain metadata')
    parser_migrate.add_argument('--from-tags', action='store_true', help='Infer from tags')
    parser_migrate.add_argument('--dry-run', action='store_true', help='Preview changes')

    # Index command
    parser_index = subparsers.add_parser('index', help='Generate domain index')
    parser_index.add_argument('--update', action='store_true', help='Update existing index')

    # Load command
    parser_load = subparsers.add_parser('load', help='Load specific domain')
    parser_load.add_argument('domain', help='Domain name')

    # List command
    subparsers.add_parser('list', help='List all domains')

    # Validate command
    subparsers.add_parser('validate', help='Validate domain metadata')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = DomainManager(args.kb_dir)

    if args.command == 'migrate':
        if args.from_tags:
            manager.migrate_from_tags(dry_run=args.dry_run)
        else:
            parser.error("Specify --from-tags or use --help")

    elif args.command == 'index':
        manager.generate_index()

    elif args.command == 'load':
        manager.load_domain(args.domain)

    elif args.command == 'list':
        manager.list_domains()

    elif args.command == 'validate':
        manager.validate()


if __name__ == '__main__':
    main()
