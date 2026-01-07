# Progressive Loading: Implementation Details
## Техническая спецификация и примеры кода

**Дата:** 2026-01-07
**Связанный документ:** `progressive-domain-loading-proposal.md`
**Статус:** Technical Specification

---

## Component 1: `tools/kb_domains.py` - Domain Management Tool

### Функциональность

```python
#!/usr/bin/env python3
"""
kb_domains - Domain-based knowledge base management

Commands:
    migrate      Add domain metadata to existing entries
    index        Generate/update _domain_index.yaml
    validate     Check domain metadata consistency
    load         Load specific domain (sparse checkout)
    sync         Synchronize specific domain
    list         List all domains with metadata
"""

import argparse
import yaml
from pathlib import Path
from collections import defaultdict
import sys
import subprocess
from typing import Dict, List, Any

# Domain taxonomy definition
DOMAIN_TAXONOMY = {
    'testing': {
        'description': 'Test patterns, pytest, unittest, mocking',
        'keywords': ['test', 'pytest', 'unittest', 'mock', 'fixture'],
        'related': ['asyncio']
    },
    'asyncio': {
        'description': 'Async/await, task groups, timeouts, cancellation',
        'keywords': ['async', 'await', 'asyncio', 'task', 'coroutine'],
        'related': ['testing']
    },
    'fastapi': {
        'description': 'FastAPI framework patterns',
        'keywords': ['fastapi', 'dependency', 'route', 'websocket'],
        'related': ['websocket', 'authentication']
    },
    'websocket': {
        'description': 'WebSocket patterns and implementations',
        'keywords': ['websocket', 'ws', 'connection'],
        'related': ['fastapi', 'asyncio']
    },
    'docker': {
        'description': 'Docker containers, volumes, networks',
        'keywords': ['docker', 'container', 'volume', 'network'],
        'related': ['deployment']
    },
    'postgresql': {
        'description': 'PostgreSQL database operations',
        'keywords': ['postgres', 'sql', 'database', 'query'],
        'related': ['docker']
    },
    'authentication': {
        'description': 'Auth, CSRF, sessions, JWT',
        'keywords': ['auth', 'csrf', 'jwt', 'session', 'login'],
        'related': ['fastapi']
    },
    'deployment': {
        'description': 'DevOps, CI/CD, deployment',
        'keywords': ['deploy', 'ci', 'cd', 'production'],
        'related': ['docker']
    },
    'monitoring': {
        'description': 'Logging, metrics, observability',
        'keywords': ['log', 'metric', 'monitor', 'trace'],
        'related': []
    },
    'performance': {
        'description': 'Optimization, profiling, performance',
        'keywords': ['optimize', 'performance', 'profile', 'cache'],
        'related': ['asyncio']
    }
}


class DomainManager:
    """Manage domain-based knowledge organization."""

    def __init__(self, kb_dir: Path):
        self.kb_dir = kb_dir
        self.domain_index_path = kb_dir / "_domain_index.yaml"

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
        for yaml_file in self.kb_dir.rglob("*.yaml"):
            if '_meta' in yaml_file.name or yaml_file.name == '_domain_index.yaml':
                continue

            with open(yaml_file, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)

            if not content or 'errors' not in content and 'patterns' not in content:
                continue

            entries = content.get('errors', []) or content.get('patterns', [])
            file_updated = False

            for entry in entries:
                if 'domains' in entry:
                    continue  # Already has domains

                tags = entry.get('tags', [])
                domains = self._infer_domains_from_tags(tags)

                if domains:
                    entry['domains'] = domains
                    file_updated = True
                    print(f"  ✓ {entry['id']}: {domains['primary']}")

            if file_updated:
                updated_count += 1
                if not dry_run:
                    with open(yaml_file, 'w', encoding='utf-8') as f:
                        yaml.safe_dump(content, f, allow_unicode=True, sort_keys=False)

        if dry_run:
            print(f"\n📊 Dry run: Would update {updated_count} files")
        else:
            print(f"\n✅ Updated {updated_count} files with domain metadata")

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

        for domain_name, domain_info in DOMAIN_TAXONOMY.items():
            score = 0
            for keyword in domain_info['keywords']:
                for tag in tags:
                    if keyword.lower() in tag.lower():
                        score += 1
            if score > 0:
                scores[domain_name] = score

        if not scores:
            return {}

        # Primary domain = highest score
        primary_domain = max(scores, key=scores.get)

        # Secondary domains = related domains
        secondary_domains = [
            DOMAIN_TAXONOMY[primary_domain]['related']
        ]

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
            'files': set(),
            'tags': set(),
            'scopes': defaultdict(int),
            'token_estimate': 0
        })

        total_entries = 0
        total_tokens = 0

        for yaml_file in self.kb_dir.rglob("*.yaml"):
            if '_meta' in yaml_file.name or yaml_file.name in ['_index.yaml', '_domain_index.yaml']:
                continue

            with open(yaml_file, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)

            if not content:
                continue

            entries = content.get('errors', []) or content.get('patterns', [])
            scope = self._infer_scope_from_path(yaml_file)

            for entry in entries:
                if 'domains' not in entry:
                    continue

                domain_name = entry['domains']['primary']
                domains_data[domain_name]['entries'].append(entry['id'])
                domains_data[domain_name]['files'].add(str(yaml_file.relative_to(self.kb_dir)))
                domains_data[domain_name]['scopes'][scope] += 1

                # Extract tags
                for tag in entry.get('tags', []):
                    domains_data[domain_name]['tags'].add(tag)

                # Estimate tokens (rough estimate: 100 tokens per entry)
                domains_data[domain_name]['token_estimate'] += 100
                total_tokens += 100
                total_entries += 1

        # Convert to final format
        index = {
            'version': '2.0',
            'last_updated': datetime.now().isoformat(),
            'total_entries': total_entries,
            'total_tokens_estimate': total_tokens,
            'domains': {}
        }

        for domain_name, data in domains_data.items():
            index['domains'][domain_name] = {
                'entries': len(data['entries']),
                'token_estimate': data['token_estimate'],
                'last_updated': datetime.now().strftime('%Y-%m-%d'),
                'tags': sorted(list(data['tags']))[:10],  # Top 10 tags
                'scopes': dict(data['scopes']),
                'files': sorted(list(data['files']))
            }

        # Add cross-reference matrix
        index['related_domains'] = self._generate_related_domains()

        # Write index
        with open(self.domain_index_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(index, f, allow_unicode=True, sort_keys=False)

        print(f"✅ Generated _domain_index.yaml ({total_entries} entries, ~{total_tokens} tokens)")

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
                if [domain_name, related_domain] not in related:
                    related.append([domain_name, related_domain])
        return related

    def load_domain(self, domain_name: str):
        """
        Load specific domain using Git sparse checkout.

        Command: git sparse-checkout add <files>
        """
        print(f"📦 Loading domain: {domain_name}")

        # Load index
        with open(self.domain_index_path, 'r') as f:
            index = yaml.safe_load(f)

        if domain_name not in index['domains']:
            print(f"❌ Domain not found: {domain_name}")
            return

        domain_data = index['domains'][domain_name]
        files = domain_data['files']

        print(f"  Files: {len(files)}")
        print(f"  Entries: {domain_data['entries']}")
        print(f"  Tokens: ~{domain_data['token_estimate']}")

        # Execute git sparse-checkout
        for file_path in files:
            try:
                subprocess.run(
                    ['git', 'sparse-checkout', 'add', file_path],
                    cwd=self.kb_dir,
                    check=True,
                    capture_output=True
                )
                print(f"  ✓ {file_path}")
            except subprocess.CalledProcessError as e:
                print(f"  ❌ Failed to load {file_path}: {e}")

        print(f"\n✅ Loaded domain '{domain_name}' (~{domain_data['token_estimate']} tokens)")

    def sync_domain(self, domain_name: str):
        """
        Synchronize specific domain from remote.

        Uses GitHub API to fetch latest domain files.
        """
        print(f"🔄 Syncing domain: {domain_name}")

        # Implementation uses GitHub API
        # (detailed in Component 3 below)
        pass

    def list_domains(self):
        """List all domains with metadata."""
        with open(self.domain_index_path, 'r') as f:
            index = yaml.safe_load(f)

        print(f"\n📚 Knowledge Base Domains ({index['total_entries']} entries, ~{index['total_tokens_estimate']} tokens)\n")

        for domain_name, data in sorted(index['domains'].items()):
            print(f"  {domain_name:20} {data['entries']:3} entries, ~{data['token_estimate']:4} tokens")
            print(f"  {'':20} Tags: {', '.join(data['tags'][:5])}")
            print()


def main():
    parser = argparse.ArgumentParser(description='Domain-based KB management')
    parser.add_argument('--kb-dir', type=Path, default=Path.cwd(), help='KB directory')

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

    # Sync command
    parser_sync = subparsers.add_parser('sync', help='Sync domain from remote')
    parser_sync.add_argument('domain', help='Domain name')

    # List command
    subparsers.add_parser('list', help='List all domains')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = DomainManager(args.kb_dir)

    if args.command == 'migrate':
        if args.from_tags:
            manager.migrate_from_tags(dry_run=args.dry_run)

    elif args.command == 'index':
        manager.generate_index()

    elif args.command == 'load':
        manager.load_domain(args.domain)

    elif args.command == 'sync':
        manager.sync_domain(args.domain)

    elif args.command == 'list':
        manager.list_domains()


if __name__ == '__main__':
    main()
```

---

## Component 2: GitHub API Fallback Implementation

### `tools/kb_github_api.py`

```python
#!/usr/bin/env python3
"""
kb_github_api - GitHub API-based domain loader

Use when Git sparse checkout is not available.
"""

import requests
import yaml
from pathlib import Path
from typing import Dict, List, Any

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/ozand/shared-knowledge-base/main"
GITHUB_API_BASE = "https://api.github.com/repos/ozand/shared-knowledge-base"


class GitHubDomainLoader:
    """Load domains via GitHub API (fallback)."""

    def __init__(self):
        self.raw_base = GITHUB_RAW_BASE
        self.api_base = GITHUB_API_BASE

    def load_domain_index(self) -> Dict:
        """Load _domain_index.yaml from GitHub."""
        url = f"{self.raw_base}/_domain_index.yaml"
        response = requests.get(url)
        response.raise_for_status()
        return yaml.safe_load(response.content)

    def load_domain(self, domain_name: str) -> List[Dict]:
        """
        Load all entries for specific domain.

        Returns:
            List of YAML entries (parsed)
        """
        index = self.load_domain_index()

        if domain_name not in index['domains']:
            raise ValueError(f"Domain not found: {domain_name}")

        domain_data = index['domains'][domain_name]
        entries = []

        for file_path in domain_data['files']:
            # Download file
            url = f"{self.raw_base}/{file_path}"
            response = requests.get(url)
            response.raise_for_status()

            # Parse YAML
            content = yaml.safe_load(response.content)

            # Extract entries
            if content:
                entries_list = content.get('errors', []) or content.get('patterns', [])
                entries.extend(entries_list)

        return entries

    def get_domain_file(self, file_path: str) -> Dict:
        """Get specific file from GitHub."""
        url = f"{self.raw_base}/{file_path}"
        response = requests.get(url)
        response.raise_for_status()
        return yaml.safe_load(response.content)

    def save_domain_locally(self, domain_name: str, output_dir: Path):
        """
        Download and save domain files locally.

        Useful for offline access or caching.
        """
        index = self.load_domain_index()
        domain_data = index['domains'][domain_name]

        output_dir.mkdir(parents=True, exist_ok=True)

        for file_path in domain_data['files']:
            content = self.get_domain_file(file_path)

            local_path = output_dir / Path(file_path).name
            with open(local_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(content, f, allow_unicode=True)

            print(f"  ✓ Saved: {local_path}")

        print(f"\n✅ Saved {len(domain_data['files'])} files to {output_dir}")
```

**Использование:**

```python
# Agent-side usage
from tools.kb_github_api import GitHubDomainLoader

loader = GitHubDomainLoader()

# Load domain index (cached)
index = loader.load_domain_index()

# Load specific domain
testing_entries = loader.load_domain('testing')
print(f"Loaded {len(testing_entries)} entries")

# Save locally for offline use
loader.save_domain_locally('testing', Path('cache/testing'))
```

---

## Component 3: Integration с `kb.py`

### Добавление domain-aware commands

```python
# В tools/kb.py

def cmd_load_domain(args):
    """Load specific domain using progressive loading."""
    from kb_domains import DomainManager

    manager = DomainManager(config.kb_dir)

    if args.domain == 'all':
        # Load all domains (full checkout)
        print("Loading all domains...")
        subprocess.run(['git', 'sparse-checkout', 'disable'], cwd=config.kb_dir)
    else:
        # Load specific domain
        manager.load_domain(args.domain)

def cmd_sync_domain(args):
    """Synchronize specific domain from remote."""
    from kb_domains import DomainManager
    from kb_github_api import GitHubDomainLoader

    # Try Git sparse checkout first
    try:
        manager = DomainManager(config.kb_dir)
        manager.sync_domain(args.domain)
    except Exception:
        # Fallback to GitHub API
        print("Falling back to GitHub API...")
        loader = GitHubDomainLoader()
        entries = loader.load_domain(args.domain)
        loader.save_domain_locally(args.domain, config.cache_dir / args.domain)

def cmd_list_domains(args):
    """List all available domains."""
    from kb_domains import DomainManager

    manager = DomainManager(config.kb_dir)
    manager.list_domains()

# Add to argparse subparsers
parser_load = subparsers.add_parser('load-domain', help='Load specific domain')
parser_load.add_argument('domain', help='Domain name (or "all")')
parser_load.set_defaults(func=cmd_load_domain)

parser_sync = subparsers.add_parser('sync', help='Sync domain from remote')
parser_sync.add_argument('domain', help='Domain name (or "all")')
parser_sync.set_defaults(func=cmd_sync_domain)

parser_list = subparsers.add_parser('list-domains', help='List all domains')
parser_list.set_defaults(func=cmd_list_domains)
```

---

## Component 4: Git Pre-Commit Hook

### `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Auto-update _domain_index.yaml on commit

echo "🔄 Updating domain index..."

# Run index update
python tools/kb_domains.py index --update

# Add index to commit if changed
if git diff --quiet _domain_index.yaml; then
    echo "✓ Index unchanged"
else
    echo "✓ Index updated, adding to commit..."
    git add _domain_index.yaml
fi
```

**Installation:**

```bash
# Symlink to .git/hooks
ln -s ../../tools/git-hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

---

## Component 5: Project Setup Script

### `for-projects/kb-sparse-setup.sh`

```bash
#!/bin/bash
# Setup Shared KB with progressive loading

set -e

REPO_URL="https://github.com/ozand/shared-knowledge-base.git"
KB_PATH="docs/knowledge-base"

echo "📦 Setting up Shared Knowledge Base (progressive mode)..."

# Step 1: Add submodule (sparse)
git submodule add --sparse "$REPO_URL" "$KB_PATH"
cd "$KB_PATH"

# Step 2: Configure sparse checkout
git sparse-checkout init --cone
git sparse-checkout set _domain_index.yaml _index.yaml .claude/

# Step 3: Create config
cat > .kb-config.yaml <<EOF
knowledge_base:
  type: "sparse-checkout"
  repository: "$REPO_URL"
  path: "$KB_PATH"

  initial_load:
    - "_domain_index.yaml"
    - "_index.yaml"
    - ".claude/"

  preferred_domains:
    - "testing"
    - "asyncio"
    - "fastapi"

  on_demand:
    mode: "sparse-checkout"
EOF

# Step 4: Load initial domains
echo "📚 Loading preferred domains..."
kb load-domain testing
kb load-domain asyncio

# Step 5: Show status
echo ""
echo "✅ Setup complete!"
echo ""
kb list-domains
echo ""
echo "Next steps:"
echo "  kb load-domain <domain>    Load specific domain"
echo "  kb list-domains            Show all domains"
echo "  kb sync --domain <name>    Sync specific domain"
```

---

## Usage Examples

### Example 1: New Project Setup

```bash
# В новом проекте
git init
git submodule add --sparse https://github.com/ozand/shared-knowledge-base.git docs/kb
cd docs/kb
git sparse-checkout init --cone
git sparse-checkout set _domain_index.yaml .claude/

# Agent работает
kb load-domain testing asyncio
```

### Example 2: Agent Domain Loading

```python
# Agent-side decision making
def load_relevant_domains(task_description: str):
    """Analyze task and load relevant domains."""

    # Load index (lightweight)
    index = kb.load_domain_index()

    # Analyze task
    if 'test' in task_description.lower():
        kb.load_domain('testing')
    if 'async' in task_description.lower():
        kb.load_domain('asyncio')
    if 'docker' in task_description.lower():
        kb.load_domain('docker')

    # Total: ~200 (index) + 3500 (testing) + 4800 (asyncio) = 8500 tokens
    # vs 50,000 tokens (full KB)
```

### Example 3: Selective Updates

```bash
# Update only testing domain
kb sync --domain testing

# Update multiple domains
kb sync --domain testing asyncio

# Update all
kb sync --all
```

---

## Testing Strategy

### Unit Tests

```python
# tests/test_kb_domains.py

def test_infer_domains_from_tags():
    manager = DomainManager(kb_dir)

    # Test 1: Async test
    domains = manager._infer_domains_from_tags(['async', 'pytest', 'testing'])
    assert domains['primary'] == 'testing'
    assert 'asyncio' in domains['secondary']

    # Test 2: Docker
    domains = manager._infer_domains_from_tags(['docker', 'container', 'volume'])
    assert domains['primary'] == 'docker'

def test_generate_index():
    manager = DomainManager(kb_dir)
    manager.generate_index()

    index_path = kb_dir / "_domain_index.yaml"
    assert index_path.exists()

    with open(index_path) as f:
        index = yaml.safe_load(f)

    assert 'domains' in index
    assert index['total_entries'] > 0
```

### Integration Tests

```bash
# Test progressive loading
test_progressive_loading() {
    # Setup sparse checkout
    git sparse-checkout init --cone
    git sparse-checkout set _domain_index.yaml

    # Load domain
    kb load-domain testing

    # Verify files loaded
    assert_exists python/errors/testing.yaml
    assert_token_count 3500  # Approximate
}
```

---

## Performance Benchmarks

### Expected Performance

| Operation | Time | Tokens |
|-----------|------|--------|
| Load index | 0.5s | 200 |
| Load domain (testing) | 1s | 3500 |
| Load domain (asyncio) | 1.5s | 4800 |
| Sync domain | 2s | - |
| Full checkout | 5s | 50000 |

### Memory Usage

- Index: <1 MB
- Single domain: ~2-5 MB
- Full KB: ~30 MB

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Status:** Implementation Ready
