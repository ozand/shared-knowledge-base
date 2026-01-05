#!/usr/bin/env python3
"""
kb_freshness.py - Knowledge Base Freshness Checker

Checks knowledge base entry freshness by:
- Comparing tested versions with current library versions
- Identifying entries with overdue version checks
- Flagging entries that need updates
- Scheduling version checks

Author: Knowledge Base Curator
Version: 1.0.0
License: MIT
"""

import yaml
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import re


class FreshnessChecker:
    """Check knowledge base entry freshness and version currency."""

    def __init__(self, kb_root: Optional[Path] = None):
        """
        Initialize FreshnessChecker.

        Args:
            kb_root: Root directory of knowledge base
        """
        self.kb_root = kb_root or Path.cwd()

        # Version check schedule (in days)
        self.check_intervals = {
            'critical': 30,    # Check critical entries monthly
            'high': 60,        # Check high entries every 2 months
            'medium': 90,      # Check medium entries quarterly
            'low': 180         # Check low entries semi-annually
        }

        # Common library version APIs
        self.version_apis = {
            'python': 'https://pypi.org/pypi/python/json',
            'fastapi': 'https://pypi.org/pypi/fastapi/json',
            'docker': None,  # Docker version checked differently
            'postgresql': 'https://api.github.com/repos/postgres/postgres/releases',
            'node': 'https://nodejs.org/dist/index.json',
            'npm': 'https://registry.npmjs.org/{package}/latest'
        }

    def check_all_entries(self) -> Dict:
        """
        Check freshness of all entries in the knowledge base.

        Returns:
            Dictionary with critical, warning, upcoming, healthy entries
        """
        results = {
            "timestamp": datetime.now().isoformat() + "Z",
            "critical": [],
            "warning": [],
            "upcoming": [],
            "healthy": []
        }

        # Find all metadata files
        meta_files = list(self.kb_root.rglob("*_meta.yaml"))

        for meta_file in meta_files:
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    meta = yaml.safe_load(f)

                for entry_id, entry_meta in meta.get('entries', {}).items():
                    status = self._check_entry(entry_id, entry_meta)
                    results[status["category"]].append(status)

            except Exception as e:
                print(f"✗ Error processing {meta_file}: {e}")

        return results

    def _check_entry(self, entry_id: str, entry_meta: Dict) -> Dict:
        """
        Check freshness of a single entry.

        Args:
            entry_id: Entry identifier
            entry_meta: Entry metadata

        Returns:
            Status dictionary with category and details
        """
        now = datetime.now()

        # Check version due date
        next_check = entry_meta.get('next_version_check_due')
        if next_check:
            try:
                due_date = datetime.fromisoformat(next_check.replace('Z', '+00:00'))
                if due_date < now:
                    severity = entry_meta.get('severity', 'medium')
                    return {
                        "category": "critical",
                        "entry_id": entry_id,
                        "reason": "Version check overdue",
                        "due_date": next_check,
                        "days_overdue": (now - due_date).days,
                        "severity": severity,
                        "action_required": "Version check needed",
                        "priority": self._get_priority_from_severity(severity)
                    }
            except:
                pass

        # Check validation status
        validation_status = entry_meta.get('validation_status')
        if validation_status == 'needs_review':
            last_reviewed = entry_meta.get('validated_at')
            if last_reviewed:
                try:
                    review_date = datetime.fromisoformat(last_reviewed.replace('Z', '+00:00'))
                    days_since = (now - review_date).days
                    if days_since > 30:
                        return {
                            "category": "warning",
                            "entry_id": entry_id,
                            "reason": "Needs review",
                            "days_since_review": days_since,
                            "validation_status": validation_status,
                            "action_required": "Re-validation needed"
                        }
                except:
                    pass

        # Check for version updates available
        tested_versions = entry_meta.get('tested_versions', {})
        version_checks = self._check_version_updates(tested_versions)
        if version_checks:
            severity = entry_meta.get('severity', 'medium')
            return {
                "category": "critical",
                "entry_id": entry_id,
                "reason": "New version available",
                "version_checks": version_checks,
                "severity": severity,
                "action_required": "Test with new version and update",
                "priority": "high"
            }

        # Check upcoming reviews
        if next_check:
            try:
                due_date = datetime.fromisoformat(next_check.replace('Z', '+00:00'))
                days_until = (due_date - now).days
                if 0 <= days_until <= 30:
                    return {
                        "category": "upcoming",
                        "entry_id": entry_id,
                        "next_review": next_check,
                        "days_until": days_until
                    }
            except:
                pass

        # Entry is healthy
        return {
            "category": "healthy",
            "entry_id": entry_id,
            "validation_status": validation_status,
            "next_check": next_check
        }

    def _get_priority_from_severity(self, severity: str) -> str:
        """Convert severity to priority level."""
        mapping = {
            'critical': 'critical',
            'high': 'high',
            'medium': 'medium',
            'low': 'low'
        }
        return mapping.get(severity, 'medium')

    def _check_version_updates(self, tested_versions: Dict) -> List[Dict]:
        """
        Check if there are newer versions available.

        Args:
            tested_versions: Dictionary of library -> version

        Returns:
            List of version update checks
        """
        updates = []

        for library, tested_version in tested_versions.items():
            current_version = self._get_latest_version(library)

            if current_version and self._version_newer(current_version, tested_version):
                updates.append({
                    "library": library,
                    "tested": tested_version,
                    "current": current_version,
                    "action": f"Test with {library} {current_version}"
                })

        return updates

    def _get_latest_version(self, library: str) -> Optional[str]:
        """
        Get latest version of a library.

        Args:
            library: Library name (python, fastapi, postgresql, etc.)

        Returns:
            Latest version string or None
        """
        try:
            if library in ['python', 'fastapi']:
                return self._get_pypi_version(library)
            elif library == 'postgresql':
                return self._get_postgres_version()
            elif library == 'node':
                return self._get_node_version()
            elif library == 'docker':
                return self._get_docker_version()
            else:
                return None
        except Exception as e:
            print(f"✗ Error getting version for {library}: {e}")
            return None

    def _get_pypi_version(self, package: str) -> Optional[str]:
        """Get latest version from PyPI."""
        try:
            url = f"https://pypi.org/pypi/{package}/json"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data['info']['version']
        except:
            return None

    def _get_postgres_version(self) -> Optional[str]:
        """Get latest PostgreSQL version from GitHub releases."""
        try:
            url = "https://api.github.com/repos/postgres/postgres/releases/latest"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            tag = data.get('tag_name', '')
            # Extract version from tag (e.g., "REL_15_2" -> "15.2")
            version = re.sub(r'^REL_', '', tag).replace('_', '.')
            return version
        except:
            return None

    def _get_node_version(self) -> Optional[str]:
        """Get latest Node.js version."""
        try:
            url = "https://nodejs.org/dist/index.json"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get('version')
        except:
            return None

    def _get_docker_version(self) -> Optional[str]:
        """Get latest Docker version (simplified)."""
        # Docker version checking is complex, return a known recent version
        # In production, would use Docker Hub API
        return "25.0"  # Example current version

    def _version_newer(self, current: str, tested: str) -> bool:
        """
        Check if current version is newer than tested version.

        Args:
            current: Current version string
            tested: Tested version string

        Returns:
            True if current is newer
        """
        try:
            current_parts = [int(x) for x in current.split('.')[:2]]
            tested_parts = [int(x) for x in tested.split('.')[:2]]
            return current_parts > tested_parts
        except:
            return False

    def generate_freshness_report(self, results: Dict) -> str:
        """
        Generate human-readable freshness report.

        Args:
            results: Results from check_all_entries

        Returns:
            Formatted report string
        """
        report = f"""
🔍 Freshness Report - {results['timestamp']}

📊 Summary:
   Critical: {len(results['critical'])}
   Warning: {len(results['warning'])}
   Upcoming: {len(results['upcoming'])}
   Healthy: {len(results['healthy'])}
"""

        if results['critical']:
            report += "\n🚨 CRITICAL (Immediate Action Required):\n"
            for item in results['critical']:
                if 'version_checks' in item:
                    report += f"\n  {item['entry_id']}: {item['reason']}\n"
                    for check in item['version_checks']:
                        report += f"    - {check['library']}: {check['tested']} → {check['current']}\n"
                    report += f"    Priority: {item['priority']}\n"
                    report += f"    Action: {item['action_required']}\n"
                else:
                    report += f"\n  {item['entry_id']}: {item['reason']}\n"
                    report += f"    Due: {item['due_date']} ({item['days_overdue']} days overdue)\n"
                    report += f"    Severity: {item.get('severity', 'unknown')}\n"
                    report += f"    Priority: {item['priority']}\n"

        if results['warning']:
            report += "\n⚠️  WARNING (Review Soon):\n"
            for item in results['warning']:
                report += f"  - {item['entry_id']}: {item['reason']} ({item['days_since_review']} days)\n"

        if results['upcoming']:
            report += f"\n📅 UPCOMING REVIEWS ({len(results['upcoming'])}):\n"
            for item in results['upcoming'][:10]:
                report += f"  - {item['entry_id']}: {item['days_until']} days\n"

        report += f"\n✅ Healthy: {len(results['healthy'])} entries\n"

        # Recommendations
        if results['critical']:
            report += "\n💡 Recommendations:\n"
            report += "   Priority: IMMEDIATE\n"

            # Group by action type
            version_updates = [i for i in results['critical'] if 'version_checks' in i]
            overdue_checks = [i for i in results['critical'] if 'days_overdue' in i]

            if version_updates:
                report += f"   - Test with new library versions ({len(version_updates)} entries)\n"

            if overdue_checks:
                report += f"   - Schedule version checks ({len(overdue_checks)} entries)\n"

        return report

    def schedule_next_check(self, entry_meta: Dict, severity: str) -> str:
        """
        Calculate next version check date based on severity.

        Args:
            entry_meta: Entry metadata
            severity: Entry severity level

        Returns:
            ISO format timestamp for next check
        """
        interval_days = self.check_intervals.get(severity, 90)
        next_check = datetime.now() + timedelta(days=interval_days)
        return next_check.isoformat() + "Z"

    def update_check_schedule(self, yaml_file: Path, entry_id: str) -> Optional[str]:
        """
        Update version check schedule for an entry.

        Args:
            yaml_file: Path to YAML file
            entry_id: Entry ID

        Returns:
            New next check date or None
        """
        from kb_meta import MetadataManager

        manager = MetadataManager(self.kb_root)
        entry_data = manager.get_entry_metadata(yaml_file, entry_id)

        if not entry_data:
            return None

        # Get severity from entry (need to read actual YAML)
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)

            if 'errors' in data:
                for error in data['errors']:
                    if error.get('id') == entry_id:
                        severity = error.get('severity', 'medium')
                        next_check = self.schedule_next_check(entry_data, severity)

                        # Update metadata
                        manager.update_entry_metadata(
                            yaml_file,
                            entry_id,
                            {'next_version_check_due': next_check},
                            agent='freshness-checker',
                            reason='Scheduled next version check'
                        )

                        return next_check

        except Exception as e:
            print(f"✗ Error updating check schedule: {e}")
            return None


def main():
    """CLI interface for freshness checking."""
    import argparse

    parser = argparse.ArgumentParser(description="Knowledge Base Freshness Checker")
    parser.add_argument('action', choices=['check', 'schedule', 'report'],
                       help='Action to perform')
    parser.add_argument('--kb-root', type=Path, default=Path.cwd(),
                       help='Knowledge base root directory')
    parser.add_argument('--entry-id',
                       help='Specific entry ID to check')
    parser.add_argument('--file', type=Path,
                       help='YAML file for entry')
    parser.add_argument('--severity', choices=['critical', 'high', 'medium', 'low'],
                       help='Severity level for scheduling')
    parser.add_argument('--output', type=Path,
                       help='Output file for report')

    args = parser.parse_args()
    checker = FreshnessChecker(args.kb_root)

    if args.action == 'check':
        if args.entry_id and args.file:
            # Check specific entry
            from kb_meta import MetadataManager
            manager = MetadataManager(args.kb_root)
            entry_meta = manager.get_entry_metadata(args.file, args.entry_id)

            if entry_meta:
                status = checker._check_entry(args.entry_id, entry_meta)
                print(f"\n{args.entry_id}:")
                print(f"  Category: {status['category']}")
                print(f"  Validation status: {entry_meta.get('validation_status')}")
                print(f"  Next check: {entry_meta.get('next_version_check_due')}")

                if status['category'] == 'critical':
                    print(f"  Reason: {status['reason']}")
        else:
            # Check all entries
            results = checker.check_all_entries()
            print(checker.generate_freshness_report(results))

            if args.output:
                with open(args.output, 'w') as f:
                    f.write(checker.generate_freshness_report(results))
                print(f"\n✓ Report saved to {args.output}")

    elif args.action == 'schedule':
        if not args.file or not args.entry_id or not args.severity:
            print("--file, --entry-id, and --severity required for schedule action")
            return

        next_check = checker.update_check_schedule(args.file, args.entry_id)
        if next_check:
            print(f"✓ Scheduled next check for {args.entry_id}: {next_check}")
        else:
            print(f"✗ Failed to schedule check")

    elif args.action == 'report':
        results = checker.check_all_entries()
        report = checker.generate_freshness_report(results)
        print(report)


if __name__ == '__main__':
    main()
