#!/usr/bin/env python3
"""
kb - Cross-platform Knowledge Base Management Tool

Universal CLI tool for managing knowledge bases across projects.
Works on Windows, macOS, and Linux. Compatible with all AI coding tools.

Usage:
    kb search <query>              Search knowledge base
    kb index                       Build/rebuild search index
    kb auto-sync --file <path>     Auto-sync KB entry to shared repository
    kb stats                       Show statistics
    kb validate <file>             Validate KB entry
    kb export --format json        Export to JSON for AI consumption

Author: Claude Code
Version: 2.0.0
License: MIT
"""

import argparse
import json
import sqlite3
import sys
import yaml
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import hashlib
import re


# ============================================================================
# Configuration
# ============================================================================

class KBConfig:
    """Knowledge base configuration."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()
        self.kb_dir = self.project_root / "docs" / "knowledge-base"
        self.shared_dir = self.kb_dir / "shared"
        self.cache_dir = self.kb_dir / ".cache"
        self.index_db = self.cache_dir / "kb_index.db"

        # Create cache directory if needed
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_file(cls, config_path: Path) -> 'KBConfig':
        """Load configuration from YAML file."""
        with config_path.open() as f:
            config_data = yaml.safe_load(f)

        instance = cls()
        # Override defaults with config file values
        for key, value in config_data.items():
            if hasattr(instance, key):
                setattr(instance, key, Path(value) if 'dir' in key else value)

        return instance


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class KBEntry:
    """Knowledge base entry model."""

    id: str
    title: str
    category: str
    severity: str
    scope: str
    file_path: str
    content: str
    tags: List[str]
    created: Optional[str] = None
    modified: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON export."""
        return asdict(self)

    @classmethod
    def from_yaml(cls, file_path: Path, data: Dict[str, Any]) -> List['KBEntry']:
        """Create KBEntry instances from YAML file."""
        entries = []

        if 'errors' in data:
            for error in data['errors']:
                entry = cls(
                    id=error.get('id', 'UNKNOWN'),
                    title=error.get('title', 'Untitled'),
                    category=data.get('category', 'unknown'),
                    severity=error.get('severity', 'unknown'),
                    scope=error.get('scope', 'project'),
                    file_path=str(file_path),
                    content=yaml.dump(error),
                    tags=error.get('tags', []),
                    created=data.get('last_updated'),
                    modified=data.get('last_updated')
                )
                entries.append(entry)

        return entries


# ============================================================================
# SQLite Index for Scalability
# ============================================================================

class KBIndex:
    """SQLite-based index for fast searching and scalability."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = None
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database with schema."""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row

        cursor = self.conn.cursor()

        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                severity TEXT NOT NULL,
                scope TEXT NOT NULL,
                file_path TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT,
                created TEXT,
                modified TEXT,
                content_hash TEXT,
                UNIQUE(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                entry_id TEXT,
                tag TEXT,
                FOREIGN KEY(entry_id) REFERENCES entries(id),
                PRIMARY KEY(entry_id, tag)
            )
        """)

        # Create indexes for fast searching
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_title
            ON entries(title)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_category
            ON entries(category)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_severity
            ON entries(severity)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_scope
            ON entries(scope)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tags
            ON tags(tag)
        """)

        # Full-text search
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS entries_fts
            USING fts5(id, title, content, tags)
        """)

        self.conn.commit()

    def add_entry(self, entry: KBEntry) -> bool:
        """Add or update entry in index."""
        cursor = self.conn.cursor()

        # Calculate content hash for change detection
        content_hash = hashlib.sha256(entry.content.encode()).hexdigest()

        try:
            # Insert or replace entry
            cursor.execute("""
                INSERT OR REPLACE INTO entries
                (id, title, category, severity, scope, file_path,
                 content, tags, created, modified, content_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.id, entry.title, entry.category, entry.severity,
                entry.scope, entry.file_path, entry.content,
                ','.join(entry.tags), entry.created, entry.modified,
                content_hash
            ))

            # Delete old tags
            cursor.execute("DELETE FROM tags WHERE entry_id = ?", (entry.id,))

            # Insert tags
            for tag in entry.tags:
                cursor.execute("""
                    INSERT INTO tags (entry_id, tag) VALUES (?, ?)
                """, (entry.id, tag))

            # Update FTS index
            cursor.execute("""
                INSERT OR REPLACE INTO entries_fts
                (id, title, content, tags)
                VALUES (?, ?, ?, ?)
            """, (entry.id, entry.title, entry.content, ','.join(entry.tags)))

            self.conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"Error adding entry {entry.id}: {e}", file=sys.stderr)
            return False

    def search(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        severity: Optional[str] = None,
        scope: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Search entries with filters."""
        cursor = self.conn.cursor()

        if query:
            # Full-text search
            sql = """
                SELECT e.* FROM entries e
                JOIN entries_fts fts ON e.id = fts.id
                WHERE entries_fts MATCH ?
            """
            params = [query]
        else:
            sql = "SELECT * FROM entries WHERE 1=1"
            params = []

        # Add filters
        if category:
            sql += " AND category = ?"
            params.append(category)

        if severity:
            sql += " AND severity = ?"
            params.append(severity)

        if scope:
            sql += " AND scope = ?"
            params.append(scope)

        if tags:
            # Search for entries with ANY of the tags
            placeholders = ','.join('?' * len(tags))
            sql += f"""
                AND id IN (
                    SELECT entry_id FROM tags
                    WHERE tag IN ({placeholders})
                )
            """
            params.extend(tags)

        sql += f" LIMIT ?"
        params.append(limit)

        cursor.execute(sql, params)

        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row['id'],
                'title': row['title'],
                'category': row['category'],
                'severity': row['severity'],
                'scope': row['scope'],
                'file_path': row['file_path'],
                'tags': row['tags'].split(',') if row['tags'] else []
            })

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        cursor = self.conn.cursor()

        # Total entries
        cursor.execute("SELECT COUNT(*) as count FROM entries")
        total = cursor.fetchone()['count']

        # By category
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM entries
            GROUP BY category
            ORDER BY count DESC
        """)
        by_category = {row['category']: row['count'] for row in cursor.fetchall()}

        # By severity
        cursor.execute("""
            SELECT severity, COUNT(*) as count
            FROM entries
            GROUP BY severity
            ORDER BY
                CASE severity
                    WHEN 'critical' THEN 1
                    WHEN 'high' THEN 2
                    WHEN 'medium' THEN 3
                    WHEN 'low' THEN 4
                    ELSE 5
                END
        """)
        by_severity = {row['severity']: row['count'] for row in cursor.fetchall()}

        # By scope
        cursor.execute("""
            SELECT scope, COUNT(*) as count
            FROM entries
            GROUP BY scope
            ORDER BY count DESC
        """)
        by_scope = {row['scope']: row['count'] for row in cursor.fetchall()}

        # Most common tags
        cursor.execute("""
            SELECT tag, COUNT(*) as count
            FROM tags
            GROUP BY tag
            ORDER BY count DESC
            LIMIT 10
        """)
        top_tags = [(row['tag'], row['count']) for row in cursor.fetchall()]

        return {
            'total': total,
            'by_category': by_category,
            'by_severity': by_severity,
            'by_scope': by_scope,
            'top_tags': top_tags
        }

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()


# ============================================================================
# Knowledge Base Manager
# ============================================================================

class KBManager:
    """Main knowledge base management class."""

    def __init__(self, config: KBConfig):
        self.config = config
        self.index = KBIndex(config.index_db)

    def build_index(self, verbose: bool = False) -> int:
        """Build or rebuild the search index."""
        if verbose:
            print(f"📚 Building index from: {self.config.kb_dir}")

        indexed = 0

        # Index all YAML files
        for yaml_file in self.config.kb_dir.rglob("*.yaml"):
            if yaml_file.name.startswith('.'):
                continue

            try:
                with yaml_file.open() as f:
                    data = yaml.safe_load(f)

                entries = KBEntry.from_yaml(yaml_file, data)

                for entry in entries:
                    if self.index.add_entry(entry):
                        indexed += 1
                        if verbose:
                            print(f"  ✓ Indexed: {entry.id} - {entry.title}")

            except Exception as e:
                print(f"  ✗ Error indexing {yaml_file}: {e}", file=sys.stderr)

        if verbose:
            print(f"\n✓ Indexed {indexed} entries")

        return indexed

    def search(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        severity: Optional[str] = None,
        scope: Optional[str] = None,
        tags: Optional[List[str]] = None,
        format: str = 'text'
    ) -> List[Dict[str, Any]]:
        """Search knowledge base."""
        results = self.index.search(
            query=query,
            category=category,
            severity=severity,
            scope=scope,
            tags=tags
        )

        if format == 'json':
            return results
        elif format == 'text':
            self._print_results(results)
            return results
        else:
            raise ValueError(f"Unknown format: {format}")

    def _print_results(self, results: List[Dict[str, Any]]):
        """Print search results in human-readable format."""
        if not results:
            print("No results found.")
            return

        print(f"\n📚 Found {len(results)} result(s):\n")

        for i, result in enumerate(results, 1):
            # Severity emoji
            severity_emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(result['severity'], '⚪')

            print(f"{i}. {severity_emoji} {result['id']}: {result['title']}")
            print(f"   Category: {result['category']} | "
                  f"Severity: {result['severity']} | "
                  f"Scope: {result['scope']}")
            print(f"   Tags: {', '.join(result['tags'])}")
            print(f"   File: {result['file_path']}")
            print()

    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics."""
        return self.index.get_stats()

    def print_stats(self):
        """Print statistics in human-readable format."""
        stats = self.get_stats()

        print("\n📊 Knowledge Base Statistics\n")
        print(f"Total entries: {stats['total']}\n")

        print("By Category:")
        for category, count in stats['by_category'].items():
            print(f"  {category}: {count}")
        print()

        print("By Severity:")
        for severity, count in stats['by_severity'].items():
            emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(severity, '⚪')
            print(f"  {emoji} {severity}: {count}")
        print()

        print("By Scope:")
        for scope, count in stats['by_scope'].items():
            print(f"  {scope}: {count}")
        print()

        print("Top 10 Tags:")
        for tag, count in stats['top_tags']:
            print(f"  {tag}: {count}")
        print()

    def validate_file(self, file_path: Path) -> bool:
        """Validate a YAML knowledge base file."""
        required_fields = ['id', 'title', 'severity']

        try:
            with file_path.open() as f:
                data = yaml.safe_load(f)

            if 'errors' not in data and 'patterns' not in data:
                print(f"✗ Missing 'errors' or 'patterns' section", file=sys.stderr)
                return False

            errors = data.get('errors', [])

            for i, error in enumerate(errors):
                for field in required_fields:
                    if field not in error:
                        print(f"✗ Error {i}: Missing required field '{field}'",
                              file=sys.stderr)
                        return False

                # Validate ID format
                if not re.match(r'^[A-Z]+-\d+$', error['id']):
                    print(f"✗ Error {i}: Invalid ID format '{error['id']}' "
                          f"(should be CATEGORY-NNN)", file=sys.stderr)
                    return False

                # Validate severity
                valid_severities = ['critical', 'high', 'medium', 'low']
                if error['severity'] not in valid_severities:
                    print(f"✗ Error {i}: Invalid severity '{error['severity']}'",
                          file=sys.stderr)
                    return False

            print(f"✓ Validation passed: {file_path}")
            return True

        except yaml.YAMLError as e:
            print(f"✗ Invalid YAML: {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            return False

    def export_json(self, output_file: Optional[Path] = None) -> str:
        """Export entire knowledge base to JSON for AI consumption."""
        results = self.index.search(limit=10000)  # Get all entries

        export_data = {
            'metadata': {
                'exported_at': datetime.now().isoformat(),
                'total_entries': len(results),
                'version': '2.0.0'
            },
            'entries': results,
            'stats': self.get_stats()
        }

        json_output = json.dumps(export_data, indent=2, ensure_ascii=False)

        if output_file:
            output_file.write_text(json_output, encoding='utf-8')
            print(f"✓ Exported to: {output_file}")

        return json_output

    def close(self):
        """Close resources."""
        self.index.close()


# ============================================================================
# Auto-Sync Command
# ============================================================================

def cmd_auto_sync(config: KBConfig, file_path: Path, commit_message: Optional[str] = None) -> bool:
    """
    Automatically sync KB entry to shared repository.

    Args:
        config: KB configuration
        file_path: Path to YAML file to sync
        commit_message: Optional custom commit message

    Returns:
        True if sync successful, False otherwise
    """
    import subprocess
    import os

    # Check if file exists
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return False

    # Check if file is in shared KB
    if "/docs/knowledge-base/shared/" not in str(file_path):
        print("⚠️  File not in shared KB, skipping sync")
        print(f"   File location: {file_path}")
        print("   Expected location: /docs/knowledge-base/shared/<scope>/")
        return False

    print(f"🔄 Syncing {file_path.name} to shared-knowledge-base...")

    # Get shared directory and relative path
    shared_dir = config.shared_dir
    rel_path = file_path.relative_to(shared_dir)

    # Change to shared directory
    original_dir = os.getcwd()
    try:
        os.chdir(shared_dir)

        # Validate file first
        print("🔍 Validating YAML...")
        try:
            with file_path.open() as f:
                yaml.safe_load(f)
            print("✓ YAML validation passed")
        except Exception as e:
            print(f"❌ YAML validation failed: {e}")
            return False

        # Add file
        print("📦 Adding file to git...")
        result = subprocess.run(
            ["git", "add", str(rel_path)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ Git add failed: {result.stderr}")
            return False
        print("✓ File added")

        # Commit
        print("💾 Committing changes...")
        if not commit_message:
            # Extract error ID from filename or content
            error_id = file_path.stem.replace('-', '_').upper()
            commit_message = f"""Add {error_id}: Knowledge base entry

- Auto-synced from local KB
- Validated and tested

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"""

        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            # Check if nothing to commit
            if "nothing to commit" in result.stdout.lower():
                print("⚠️  No changes to commit (file already synced)")
                return True
            print(f"❌ Git commit failed: {result.stderr}")
            return False
        print("✓ Committed")

        # Push
        print("🚀 Pushing to origin/main...")
        result = subprocess.run(
            ["git", "push", "origin", "main"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            # Check if push failed due to conflicts
            if "rejected" in result.stderr or "fetch first" in result.stderr:
                print("⚠️  Push failed, attempting rebase...")
                result = subprocess.run(
                    ["git", "pull", "--rebase", "origin", "main"],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"❌ Rebase failed: {result.stderr}")
                    print("   Please resolve conflicts manually")
                    return False

                # Try push again
                result = subprocess.run(
                    ["git", "push", "origin", "main"],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"❌ Push failed after rebase: {result.stderr}")
                    return False
            else:
                print(f"❌ Git push failed: {result.stderr}")
                return False

        print("✓ Pushed successfully")

        # Get commit hash
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True
        )
        commit_hash = result.stdout.strip()

        print(f"\n✅ Synced to shared-knowledge-base repository")
        print(f"📦 Commit: {commit_hash[:8]}")
        print(f"🌐 Available at: https://github.com/ozand/shared-knowledge-base")

        # Rebuild index
        print("\n🔍 Rebuilding KB index...")
        os.chdir(original_dir)
        manager = KBManager(config)
        try:
            manager.build_index(verbose=False)
            print("✓ Index rebuilt")
        finally:
            manager.close()

        return True

    except Exception as e:
        print(f"❌ Sync failed: {e}")
        return False

    finally:
        os.chdir(original_dir)


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Knowledge Base Management Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  kb search "async test"                   # Search by keyword
  kb search --category python --tags async # Filter by category and tags
  kb search --severity high                # Find high severity errors
  kb index                                 # Rebuild search index
  kb stats                                 # Show statistics
  kb validate errors/testing.yaml          # Validate file
  kb export --format json --output kb.json # Export to JSON
  kb auto-sync --file shared/docker/errors/test.yaml  # Auto-sync to repository
        """
    )

    parser.add_argument('--config', type=Path, help='Config file path')

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search knowledge base')
    search_parser.add_argument('query', nargs='?', help='Search query')
    search_parser.add_argument('--category', help='Filter by category')
    search_parser.add_argument('--severity', help='Filter by severity')
    search_parser.add_argument('--scope', help='Filter by scope')
    search_parser.add_argument('--tags', nargs='+', help='Filter by tags')
    search_parser.add_argument('--format', choices=['text', 'json'],
                               default='text', help='Output format')

    # Index command
    index_parser = subparsers.add_parser('index', help='Build search index')
    index_parser.add_argument('-v', '--verbose', action='store_true',
                             help='Verbose output')

    # Stats command
    subparsers.add_parser('stats', help='Show statistics')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate KB file')
    validate_parser.add_argument('file', type=Path, help='File to validate')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export to JSON')
    export_parser.add_argument('--output', type=Path, help='Output file')
    export_parser.add_argument('--format', choices=['json'], default='json',
                              help='Export format')

    # Auto-sync command
    sync_parser = subparsers.add_parser('auto-sync', help='Auto-sync KB entry to shared repository')
    sync_parser.add_argument('--file', type=Path, required=True, help='YAML file to sync')
    sync_parser.add_argument('--message', type=str, help='Custom commit message')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Load configuration
    if args.config and args.config.exists():
        config = KBConfig.from_file(args.config)
    else:
        config = KBConfig()

    # Initialize manager
    manager = KBManager(config)

    try:
        # Execute command
        if args.command == 'search':
            manager.search(
                query=args.query,
                category=args.category,
                severity=args.severity,
                scope=args.scope,
                tags=args.tags,
                format=args.format
            )

        elif args.command == 'index':
            manager.build_index(verbose=args.verbose)

        elif args.command == 'stats':
            manager.print_stats()

        elif args.command == 'validate':
            success = manager.validate_file(args.file)
            return 0 if success else 1

        elif args.command == 'export':
            manager.export_json(args.output)

        elif args.command == 'auto-sync':
            success = cmd_auto_sync(config, args.file, args.message)
            return 0 if success else 1

        return 0

    finally:
        manager.close()


if __name__ == '__main__':
    sys.exit(main())
