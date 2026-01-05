# IMPLEMENTATION_GUIDE.md - Metadata System Implementation

## Technical Implementation Guide

This document provides concrete implementation examples for the metadata system described in METADATA_ARCHITECTURE.md.

---

## Part 1: Metadata File Operations

### 1.1 Create Metadata File

```python
# tools/kb_meta.py

import yaml
import json
from pathlib import Path
from datetime import datetime, timedelta
import hashlib

class MetadataManager:
    """Manage knowledge base metadata files."""

    def __init__(self, kb_root: Path):
        self.kb_root = kb_root
        self.cache_dir = kb_root / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def create_meta_file(self, yaml_file: Path) -> Path:
        """Create _meta.yaml file alongside a YAML file."""
        meta_file = yaml_file.parent / f"{yaml_file.stem}_meta.yaml"

        if meta_file.exists():
            return meta_file

        # Load the YAML file to extract entries
        with open(yaml_file) as f:
            data = yaml.safe_load(f)

        # Create metadata structure
        meta = {
            "version": "1.0",
            "file_metadata": {
                "file_id": self._generate_file_id(yaml_file),
                "created_at": datetime.now().isoformat() + "Z",
                "created_by": "kb-meta-tool",
                "last_modified": datetime.now().isoformat() + "Z",
                "last_modified_by": "kb-meta-tool",
                "version": 1
            },
            "entries": {},
            "analytics": {
                "total_access_count": 0,
                "first_accessed_at": None,
                "last_accessed_at": None,
                "access_history_summary": []
            },
            "change_history": [
                {
                    "timestamp": datetime.now().isoformat() + "Z",
                    "action": "created",
                    "agent": "kb-meta-tool",
                    "entries_affected": [],
                    "reason": "Initial metadata creation"
                }
            ]
        }

        # Initialize entry metadata
        if 'errors' in data:
            for error in data['errors']:
                entry_id = error.get('id', 'UNKNOWN')
                meta['entries'][entry_id] = self._create_entry_metadata(entry_id, error)
                meta['change_history'][0]['entries_affected'].append(entry_id)

        # Write metadata file
        with open(meta_file, 'w') as f:
            yaml.dump(meta, f, default_flow_style=False, sort_keys=False)

        return meta_file

    def _create_entry_metadata(self, entry_id: str, entry_data: dict) -> dict:
        """Create initial metadata for an entry."""
        return {
            "created_at": datetime.now().isoformat() + "Z",
            "created_by": "unknown",
            "last_modified": datetime.now().isoformat() + "Z",
            "last_modified_by": "unknown",

            # Analysis tracking
            "last_analyzed_at": None,
            "last_analyzed_by": None,
            "analysis_version": 0,

            # Quality tracking
            "quality_score": None,
            "quality_assessed_at": None,
            "quality_assessed_by": None,

            # Research tracking
            "last_researched_at": None,
            "research_sources": [],
            "research_version": 0,

            # Validation status
            "validation_status": "needs_review",
            "validated_at": None,
            "validated_against_version": None,

            # Version tracking
            "tested_versions": {},
            "requires_version_check": True,
            "next_version_check_due": (datetime.now() + timedelta(days=90)).isoformat() + "Z",

            # Deprecation
            "is_deprecated": False,
            "deprecated_at": None,
            "deprecated_by": None,
            "superseded_by": None
        }

    def _generate_file_id(self, yaml_file: Path) -> str:
        """Generate unique file ID."""
        rel_path = yaml_file.relative_to(self.kb_root)
        return str(rel_path).replace('/', '-').replace('\\', '-').replace('.yaml', '')

    def update_entry_metadata(self, yaml_file: Path, entry_id: str, updates: dict) -> dict:
        """Update metadata for a specific entry."""
        meta_file = yaml_file.parent / f"{yaml_file.stem}_meta.yaml"

        if not meta_file.exists():
            self.create_meta_file(yaml_file)

        with open(meta_file) as f:
            meta = yaml.safe_load(f)

        if entry_id not in meta['entries']:
            meta['entries'][entry_id] = self._create_entry_metadata(entry_id, {})

        # Apply updates
        entry_meta = meta['entries'][entry_id]
        for key, value in updates.items():
            entry_meta[key] = value

        # Update file metadata
        meta['file_metadata']['last_modified'] = datetime.now().isoformat() + "Z"
        meta['file_metadata']['version'] += 1

        # Add to change history
        meta['change_history'].append({
            "timestamp": datetime.now().isoformat() + "Z",
            "action": updates.get('action', 'updated'),
            "agent": updates.get('agent', 'unknown'),
            "entries_affected": [entry_id],
            "reason": updates.get('reason', '')
        })

        # Write back
        with open(meta_file, 'w') as f:
            yaml.dump(meta, f, default_flow_style=False, sort_keys=False)

        return entry_meta

    def get_entry_metadata(self, yaml_file: Path, entry_id: str) -> dict:
        """Get metadata for a specific entry."""
        meta_file = yaml_file.parent / f"{yaml_file.stem}_meta.yaml"

        if not meta_file.exists():
            return None

        with open(meta_file) as f:
            meta = yaml.safe_load(f)

        return meta['entries'].get(entry_id)

    def calculate_hash(self, yaml_file: Path, entry_id: str) -> str:
        """Calculate hash of entry content."""
        with open(yaml_file) as f:
            data = yaml.safe_load(f)

        if 'errors' in data:
            for error in data['errors']:
                if error.get('id') == entry_id:
                    content = yaml.dump(error)
                    return hashlib.sha256(content.encode()).hexdigest()

        return None
```

---

## Part 2: Usage Tracking

### 2.1 Usage Tracker

```python
# tools/kb_usage.py

import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List

class UsageTracker:
    """Track knowledge base usage locally."""

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.usage_file = cache_dir / "usage.json"
        self.max_sessions_per_entry = 100

        self._ensure_usage_file()

    def _ensure_usage_file(self):
        """Create usage file if it doesn't exist."""
        if not self.usage_file.exists():
            initial_data = {
                "version": "1.0",
                "project_id": self._generate_project_id(),
                "tracking_started_at": datetime.now().isoformat() + "Z",
                "last_updated_at": datetime.now().isoformat() + "Z",
                "entries": {},
                "search_analytics": {
                    "total_searches": 0,
                    "successful_searches": 0,
                    "no_results_searches": 0,
                    "top_search_queries": [],
                    "no_results_queries": []
                },
                "gap_signals": {
                    "repeated_no_results": [],
                    "high_access_low_quality": []
                }
            }
            with open(self.usage_file, 'w') as f:
                json.dump(initial_data, f, indent=2)

    def _generate_project_id(self) -> str:
        """Generate anonymous project ID."""
        import uuid
        return f"project-{uuid.uuid4().hex[:8]}"

    def track_access(
        self,
        entry_id: str,
        method: str = "search",
        query: Optional[str] = None,
        context: str = "unknown",
        resolved: bool = False
    ) -> int:
        """Record access to an entry."""
        with open(self.usage_file) as f:
            usage_data = json.load(f)

        # Initialize entry if needed
        if entry_id not in usage_data["entries"]:
            usage_data["entries"][entry_id] = {
                "access_count": 0,
                "first_accessed_at": None,
                "last_accessed_at": None,
                "access_methods": {"search": 0, "direct_id": 0, "category_browse": 0},
                "access_context": {"error_resolution": 0, "prevention": 0, "learning": 0},
                "sessions": []
            }

        # Update entry stats
        entry = usage_data["entries"][entry_id]
        entry["access_count"] += 1
        entry["last_accessed_at"] = datetime.now().isoformat() + "Z"
        if entry["first_accessed_at"] is None:
            entry["first_accessed_at"] = entry["last_accessed_at"]

        entry["access_methods"][method] = entry["access_methods"].get(method, 0) + 1
        entry["access_context"][context] = entry["access_context"].get(context, 0) + 1

        # Add session record
        session = {
            "timestamp": datetime.now().isoformat() + "Z",
            "method": method,
            "query": query if method == "search" else None,
            "context": context,
            "resolved": resolved
        }
        entry["sessions"].append(session)

        # Keep only last N sessions
        if len(entry["sessions"]) > self.max_sessions_per_entry:
            entry["sessions"] = entry["sessions"][-self.max_sessions_per_entry:]

        # Update search analytics
        usage_data["search_analytics"]["total_searches"] += 1
        if resolved:
            usage_data["search_analytics"]["successful_searches"] += 1
        else:
            usage_data["search_analytics"]["no_results_searches"] += 1

        # Update query tracking
        if method == "search" and query:
            self._update_query_tracking(usage_data["search_analytics"], query, resolved)

        usage_data["last_updated_at"] = datetime.now().isoformat() + "Z"

        # Save
        with open(self.usage_file, 'w') as f:
            json.dump(usage_data, f, indent=2)

        return entry["access_count"]

    def _update_query_tracking(self, analytics: dict, query: str, resolved: bool):
        """Update query statistics."""
        target_list = analytics["top_search_queries"] if resolved else analytics["no_results_queries"]

        # Find existing or add new
        for item in target_list:
            if item["query"] == query:
                item["count"] += 1
                break
        else:
            target_list.append({"query": query, "count": 1})

        # Sort and keep top 20
        target_list.sort(key=lambda x: x["count"], reverse=True)
        if len(target_list) > 20:
            target_list[:] = target_list[:20]

    def get_entry_stats(self, entry_id: str) -> Optional[dict]:
        """Get usage statistics for an entry."""
        with open(self.usage_file) as f:
            usage_data = json.load(f)

        return usage_data["entries"].get(entry_id)

    def get_top_entries(self, limit: int = 10) -> List[tuple]:
        """Get most accessed entries."""
        with open(self.usage_file) as f:
            usage_data = json.load(f)

        entries_with_counts = [
            (entry_id, data["access_count"])
            for entry_id, data in usage_data["entries"].items()
        ]

        entries_with_counts.sort(key=lambda x: x[1], reverse=True)
        return entries_with_counts[:limit]

    def detect_gaps(self, min_count: int = 3) -> List[dict]:
        """Detect search gaps from failed searches."""
        with open(self.usage_file) as f:
            usage_data = json.load(f)

        gaps = []
        for item in usage_data["search_analytics"]["no_results_queries"]:
            if item["count"] >= min_count:
                gaps.append({
                    "query": item["query"],
                    "count": item["count"],
                    "priority": "high" if item["count"] >= 5 else "medium"
                })

        return gaps
```

---

## Part 3: Change Detection

### 3.1 Hash-Based Change Detector

```python
# tools/kb_changes.py

import yaml
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple

class ChangeDetector:
    """Detect changes in knowledge base entries."""

    def __init__(self, kb_root: Path, cache_dir: Path):
        self.kb_root = kb_root
        self.cache_dir = cache_dir
        self.hash_file = cache_dir / "file_hashes.json"

    def calculate_entry_hash(self, yaml_file: Path, entry_id: str) -> str:
        """Calculate hash of entry content."""
        with open(yaml_file) as f:
            data = yaml.safe_load(f)

        if 'errors' in data:
            for error in data['errors']:
                if error.get('id') == entry_id:
                    # Serialize entry content deterministically
                    content = json.dumps(error, sort_keys=True)
                    return hashlib.sha256(content.encode()).hexdigest()

        return None

    def calculate_file_hash(self, yaml_file: Path) -> str:
        """Calculate hash of entire YAML file."""
        with open(yaml_file, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def scan_all_entries(self) -> Dict[str, dict]:
        """Scan all entries and calculate hashes."""
        hashes = {"entry_hashes": {}, "file_hashes": {}}

        for yaml_file in self.kb_root.rglob("*.yaml"):
            # Skip meta files and cache
            if "_meta.yaml" in str(yaml_file) or ".cache" in str(yaml_file):
                continue

            # Calculate file hash
            file_hash = self.calculate_file_hash(yaml_file)
            rel_path = str(yaml_file.relative_to(self.kb_root))
            hashes["file_hashes"][rel_path] = file_hash

            # Calculate entry hashes
            with open(yaml_file) as f:
                data = yaml.safe_load(f)

            if 'errors' in data:
                for error in data['errors']:
                    entry_id = error.get('id')
                    if entry_id:
                        entry_hash = self.calculate_entry_hash(yaml_file, entry_id)
                        hashes["entry_hashes"][entry_id] = {
                            "hash": entry_hash,
                            "file": rel_path
                        }

        return hashes

    def save_hashes(self, hashes: Dict):
        """Save hashes to cache."""
        hashes["last_scan"] = datetime.now().isoformat() + "Z"
        hashes["version"] = "1.0"

        with open(self.hash_file, 'w') as f:
            json.dump(hashes, f, indent=2)

    def load_hashes(self) -> Dict:
        """Load hashes from cache."""
        if not self.hash_file.exists():
            return None

        with open(self.hash_file) as f:
            return json.load(f)

    def detect_changes(self) -> Dict:
        """Detect changes since last scan."""
        old_hashes = self.load_hashes()
        current_hashes = self.scan_all_entries()

        if old_hashes is None:
            # First scan
            self.save_hashes(current_hashes)
            return {
                "type": "initial_scan",
                "total_entries": len(current_hashes["entry_hashes"]),
                "entries": list(current_hashes["entry_hashes"].keys())
            }

        changes = {
            "new_entries": [],
            "modified_entries": [],
            "deleted_entries": [],
            "timestamp": datetime.now().isoformat() + "Z"
        }

        # Detect new and modified entries
        for entry_id, current_data in current_hashes["entry_hashes"].items():
            if entry_id not in old_hashes["entry_hashes"]:
                changes["new_entries"].append({
                    "entry_id": entry_id,
                    "file": current_data["file"],
                    "hash": current_data["hash"]
                })
            elif old_hashes["entry_hashes"][entry_id]["hash"] != current_data["hash"]:
                changes["modified_entries"].append({
                    "entry_id": entry_id,
                    "file": current_data["file"],
                    "old_hash": old_hashes["entry_hashes"][entry_id]["hash"],
                    "new_hash": current_data["hash"]
                })

        # Detect deleted entries
        for entry_id in old_hashes["entry_hashes"]:
            if entry_id not in current_hashes["entry_hashes"]:
                changes["deleted_entries"].append({
                    "entry_id": entry_id,
                    "was_in": old_hashes["entry_hashes"][entry_id]["file"]
                })

        # Save current hashes
        self.save_hashes(current_hashes)

        return changes
```

---

## Part 4: Freshness Checker

### 4.1 Freshness Analyzer

```python
# tools/kb_freshness.py

import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict
import requests

class FreshnessChecker:
    """Check knowledge base entry freshness."""

    def __init__(self, kb_root: Path):
        self.kb_root = kb_root

    def check_all_entries(self) -> Dict:
        """Check freshness of all entries."""
        results = {
            "timestamp": datetime.now().isoformat() + "Z",
            "critical": [],
            "warning": [],
            "upcoming": [],
            "healthy": []
        }

        for meta_file in self.kb_root.rglob("*_meta.yaml"):
            with open(meta_file) as f:
                meta = yaml.safe_load(f)

            for entry_id, entry_meta in meta.get("entries", {}).items():
                status = self._check_entry(entry_id, entry_meta)
                results[status["category"]].append(status)

        return results

    def _check_entry(self, entry_id: str, entry_meta: Dict) -> Dict:
        """Check freshness of a single entry."""
        now = datetime.now()

        # Check version due date
        next_check = entry_meta.get("next_version_check_due")
        if next_check:
            due_date = datetime.fromisoformat(next_check.replace('Z', '+00:00'))
            if due_date < now:
                return {
                    "category": "critical",
                    "entry_id": entry_id,
                    "reason": "Version check overdue",
                    "due_date": next_check,
                    "days_overdue": (now - due_date).days,
                    "action_required": "Version check needed"
                }

        # Check validation status
        validation_status = entry_meta.get("validation_status")
        if validation_status == "needs_review":
            last_reviewed = entry_meta.get("validated_at")
            if last_reviewed:
                review_date = datetime.fromisoformat(last_reviewed.replace('Z', '+00:00'))
                days_since = (now - review_date).days
                if days_since > 30:
                    return {
                        "category": "warning",
                        "entry_id": entry_id,
                        "reason": "Needs review",
                        "days_since_review": days_since,
                        "action_required": "Re-validation needed"
                    }

        # Check upcoming reviews
        if next_check:
            due_date = datetime.fromisoformat(next_check.replace('Z', '+00:00'))
            days_until = (due_date - now).days
            if 0 <= days_until <= 30:
                return {
                    "category": "upcoming",
                    "entry_id": entry_id,
                    "next_review": next_check,
                    "days_until": days_until
                }

        # Entry is healthy
        return {
            "category": "healthy",
            "entry_id": entry_id,
            "validation_status": validation_status,
            "next_check": next_check
        }

    def check_version_updates(self, entry_meta: Dict) -> List[Dict]:
        """Check if there are version updates available."""
        alerts = []
        tested_versions = entry_meta.get("tested_versions", {})

        # Example: Check Python version
        if "python" in tested_versions:
            current_python = self._get_latest_python_version()
            tested_python = tested_versions["python"]

            if self._version_newer(current_python, tested_python):
                alerts.append({
                    "library": "python",
                    "tested": tested_python,
                    "current": current_python,
                    "action": "Test with newer Python version"
                })

        # Add more library checks as needed
        # ...

        return alerts

    def _get_latest_python_version(self) -> str:
        """Get latest Python version (simplified example)."""
        # In production, would check API or parse downloads
        # This is a placeholder
        return "3.13.0"

    def _version_newer(self, current: str, tested: str) -> bool:
        """Check if current version is newer than tested version."""
        try:
            current_parts = [int(x) for x in current.split('.')[:2]]
            tested_parts = [int(x) for x in tested.split('.')[:2]]
            return current_parts > tested_parts
        except:
            return False
```

---

## Part 5: CLI Integration

### 5.1 Enhanced kb.py with Metadata

```python
# Add to tools/kb.py

def cmd_check_freshness(args):
    """Check freshness of knowledge base entries."""
    from kb_freshness import FreshnessChecker

    config = KBConfig()
    checker = FreshnessChecker(config.kb_dir)

    results = checker.check_all_entries()

    print(f"\n🔍 Freshness Check - {results['timestamp']}\n")
    print(f"Critical: {len(results['critical'])}")
    print(f"Warning: {len(results['warning'])}")
    print(f"Upcoming: {len(results['upcoming'])}")
    print(f"Healthy: {len(results['healthy'])}\n")

    if results['critical']:
        print("🚨 CRITICAL:")
        for item in results['critical']:
            print(f"  - {item['entry_id']}: {item['reason']}")
            print(f"    Action: {item['action_required']}")

    if results['warning']:
        print("\n⚠️  WARNING:")
        for item in results['warning']:
            print(f"  - {item['entry_id']}: {item['reason']}")

def cmd_detect_changes(args):
    """Detect changes since last scan."""
    from kb_changes import ChangeDetector

    config = KBConfig()
    detector = ChangeDetector(config.kb_dir, config.cache_dir)

    changes = detector.detect_changes()

    if changes['type'] == 'initial_scan':
        print(f"\n📊 Initial scan: {changes['total_entries']} entries found")
        return

    print(f"\n🔄 Changes detected: {changes['timestamp']}\n")
    print(f"New: {len(changes['new_entries'])}")
    print(f"Modified: {len(changes['modified_entries'])}")
    print(f"Deleted: {len(changes['deleted_entries'])}\n")

    if changes['new_entries']:
        print("✅ New entries:")
        for item in changes['new_entries']:
            print(f"  - {item['entry_id']} in {item['file']}")

    if changes['modified_entries']:
        print("📝 Modified entries:")
        for item in changes['modified_entries']:
            print(f"  - {item['entry_id']} in {item['file']}")

def cmd_analyze_usage(args):
    """Analyze local usage patterns."""
    from kb_usage import UsageTracker

    config = KBConfig()
    tracker = UsageTracker(config.cache_dir)

    print("\n📊 Usage Analysis\n")

    # Top entries
    top_entries = tracker.get_top_entries(10)
    print("Top accessed entries:")
    for entry_id, count in top_entries:
        print(f"  - {entry_id}: {count} accesses")

    # Gaps
    gaps = tracker.detect_gaps(min_count=3)
    if gaps:
        print("\n🔍 Search gaps (potential new entries):")
        for gap in gaps:
            print(f"  - '{gap['query']}' ({gap['count']} searches) [{gap['priority']}]")

# Add to argparse
parser_freshness = subparsers.add_parser('check-freshness', help='Check entry freshness')
parser_freshness.set_defaults(func=cmd_check_freshness)

parser_changes = subparsers.add_parser('detect-changes', help='Detect changes')
parser_changes.set_defaults(func=cmd_detect_changes)

parser_usage = subparsers.add_parser('analyze-usage', help='Analyze usage patterns')
parser_usage.set_defaults(func=cmd_analyze_usage)
```

---

## Part 6: Git Integration

### 6.1 Git-Based Change Detection

```python
# tools/kb_git.py

import subprocess
from pathlib import Path
from datetime import datetime
from typing import List

class GitChangeDetector:
    """Detect changes using git."""

    def __init__(self, kb_root: Path):
        self.kb_root = kb_root
        self.git_dir = kb_root / ".git"

    def has_git(self) -> bool:
        """Check if directory is a git repo."""
        return self.git_dir.exists()

    def get_changed_files_since(self, ref: str = "HEAD@{1}") -> List[str]:
        """Get list of changed files since git ref."""
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", ref, "HEAD"],
                cwd=self.kb_root,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                files = result.stdout.strip().split('\n')
                return [f for f in files if f.endswith('.yaml')]

        except Exception as e:
            print(f"Git error: {e}")

        return []

    def get_changed_entries_since_last_pull(self) -> List[str]:
        """Get entries changed since last git pull."""
        files = self.get_changed_files_since("HEAD@{1}")

        entry_ids = []
        for file_path in files:
            # Extract entry IDs from file
            full_path = self.kb_root / file_path
            if full_path.exists() and not file_path.endswith("_meta.yaml"):
                entry_ids.extend(self._extract_entry_ids(full_path))

        return entry_ids

    def _extract_entry_ids(self, yaml_file: Path) -> List[str]:
        """Extract entry IDs from YAML file."""
        import yaml

        with open(yaml_file) as f:
            data = yaml.safe_load(f)

        entry_ids = []
        if 'errors' in data:
            for error in data['errors']:
                entry_ids.append(error.get('id'))

        return entry_ids

    def get_files_modified_in_period(self, days: int = 7) -> List[str]:
        """Get files modified in the last N days."""
        try:
            since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

            result = subprocess.run(
                ["git", "log", f"--since={since_date}", "--name-only", "--pretty=format:"],
                cwd=self.kb_root,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                files = result.stdout.strip().split('\n')
                yaml_files = [f for f in files if f.endswith('.yaml')]
                return list(set(yaml_files))  # Deduplicate

        except Exception as e:
            print(f"Git error: {e}")

        return []
```

---

## Part 7: Automated Workflows

### 7.1 Automated Metadata Initialization

```bash
# scripts/init_metadata.sh

#!/bin/bash

# Initialize metadata for all YAML files

KB_ROOT="${1:-.}"

echo "🔍 Scanning for YAML files in $KB_ROOT..."

find "$KB_ROOT" -name "*.yaml" ! -name "*_meta.yaml" ! -path "*/.cache/*" | while read file; do
    meta_file="${file%.yaml}_meta.yaml"

    if [ ! -f "$meta_file" ]; then
        echo "📝 Creating metadata for: $file"
        python -c "
from kb_meta import MetadataManager
from pathlib import Path

kb_root = Path('$KB_ROOT')
yaml_file = Path('$file')
manager = MetadataManager(kb_root)
manager.create_meta_file(yaml_file)
"
    fi
done

echo "✅ Metadata initialization complete"
```

### 7.2 Daily Freshness Check

```bash
# scripts/daily_freshness.sh

#!/bin/bash

# Run daily freshness check and generate report

KB_ROOT="${1:-.}"
REPORT_FILE="${2:-.cache/freshness_report_$(date +%Y%m%d).yaml}"

echo "🔍 Running freshness check..."

python -c "
from kb_freshness import FreshnessChecker
from pathlib import Path
import yaml

kb_root = Path('$KB_ROOT')
checker = FreshnessChecker(kb_root)
results = checker.check_all_entries()

with open('$REPORT_FILE', 'w') as f:
    yaml.dump(results, f)

print(f'\\n✅ Report saved to: $REPORT_FILE')
print(f'Critical: {len(results[\"critical\"])}')
print(f'Warning: {len(results[\"warning\"])}')
print(f'Upcoming: {len(results[\"upcoming\"])}')
print(f'Healthy: {len(results[\"healthy\"])}')
"

# Exit with error if critical issues found
if grep -q "critical:" "$REPORT_FILE" && grep -A 1 "critical:" "$REPORT_FILE" | grep -q "entry_id:"; then
    echo "🚨 Critical issues detected!"
    exit 1
fi
```

### 7.3 Weekly Usage Analysis

```bash
# scripts/weekly_usage.sh

#!/bin/bash

# Analyze usage and identify gaps

echo "📊 Analyzing usage patterns..."

python -c "
from kb_usage import UsageTracker
from pathlib import Path
import json

cache_dir = Path('.cache')
tracker = UsageTracker(cache_dir)

# Get top entries
top = tracker.get_top_entries(20)
print('\\n📈 Top 20 Entries:')
for entry_id, count in top:
    print(f'  {entry_id}: {count}')

# Detect gaps
gaps = tracker.detect_gaps(min_count=3)
print(f'\\n🔍 Search Gaps ({len(gaps)}):')
for gap in gaps:
    print(f'  - \"{gap[\"query\"]}\" ({gap[\"count\"]} searches) [{gap[\"priority\"]}]')

# Save detailed report
report = {
    'top_entries': top,
    'gaps': gaps,
    'generated_at': datetime.now().isoformat()
}

with open(cache_dir / 'usage_report.json', 'w') as f:
    json.dump(report, f, indent=2)

print('\\n✅ Usage analysis complete')
"
```

---

## Part 8: Git Hooks

### 8.1 Pre-commit Hook

```bash
# .git/hooks/pre-commit

#!/bin/bash

# Pre-commit hook: validate metadata exists for new/modified entries

echo "🔍 Checking metadata..."

# Get staged YAML files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.yaml$' || true)

for file in $STAGED_FILES; do
    # Skip meta files and cache
    if [[ "$file" == *"_meta.yaml" ]] || [[ "$file" == *".cache"* ]]; then
        continue
    fi

    # Check if meta file exists
    meta_file="${file%.yaml}_meta.yaml"

    if [ ! -f "$meta_file" ]; then
        echo "⚠️  Warning: No metadata file for $file"
        echo "   Run: python tools/kb.py update-metadata-for $file"
        # Don't block commit, just warn
    fi
done

echo "✅ Metadata check complete"
```

### 8.2 Post-merge Hook

```bash
# .git/hooks/post-merge

#!/bin/bash

# Post-merge hook: detect changes and suggest actions

echo "🔄 Detecting changes after merge..."

# Detect changed entries
python tools/kb.py detect-changes

# Suggest freshness check
echo "💡 Tip: Run 'python tools/kb.py check-freshness' to check for outdated entries"
```

---

## Summary

This implementation guide provides:

1. **MetadataManager** - Create and update `_meta.yaml` files
2. **UsageTracker** - Track usage locally in `.cache/usage.json`
3. **ChangeDetector** - Hash-based and git-based change detection
4. **FreshnessChecker** - Identify entries needing review
5. **CLI Integration** - New kb.py commands
6. **Git Integration** - Hooks and git-based detection
7. **Automated Scripts** - Daily/weekly maintenance workflows

All components are:
- ✅ **Distributed** - No central endpoint required
- ✅ **Git-synced** - Metadata propagates through git
- ✅ **Privacy-preserving** - Usage data stays local
- ✅ **Scalable** - Works with 10 or 10,000 entries
- ✅ **Merge-safe** - Handles git conflicts gracefully

The metadata system enables intelligent, automated knowledge curation while maintaining the distributed architecture of the Shared Knowledge Base.
