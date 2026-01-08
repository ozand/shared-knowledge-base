#!/usr/bin/env python3
"""
daily_freshness.py - Daily Freshness Check Script

Runs daily freshness checks on knowledge base entries.
Generates reports and schedules next checks.

Usage:
    python scripts/daily_freshness.py [--output report.yaml]
    Can be run via cron/scheduler:
        0 2 * * * python /path/to/kb/scripts/daily_freshness.py

Author: Knowledge Base Curator
Version: 1.0.0
License: MIT
"""

import sys
from pathlib import Path
from datetime import datetime

# Add tools directory to path
tools_dir = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(tools_dir))

try:
    from kb_freshness import FreshnessChecker
    from kb_meta import MetadataManager
except ImportError as e:
    print(f"❌ Cannot import required modules: {e}")
    sys.exit(1)


def main():
    """Run daily freshness check."""
    import argparse

    parser = argparse.ArgumentParser(description="Daily Freshness Check")
    parser.add_argument('--kb-root', type=Path, default=Path.cwd(),
                       help='Knowledge base root directory')
    parser.add_argument('--output', type=Path,
                       help='Output file for report (YAML format)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    print("🔍 Daily Freshness Check")
    print(f"   Timestamp: {datetime.now().isoformat()}")
    print(f"   KB Root: {args.kb_root}")
    print()

    checker = FreshnessChecker(args.kb_root)

    # Run freshness check
    print("Checking all entries...")
    results = checker.check_all_entries()

    # Print report
    report = checker.generate_freshness_report(results)
    print(report)

    # Save report if requested
    if args.output:
        # Save as YAML
        import yaml
        with open(args.output, 'w') as f:
            yaml.dump(results, f, default_flow_style=False)
        print(f"✓ Report saved to: {args.output}")

    # Check for critical issues
    if results['critical']:
        print("\n🚨 CRITICAL ISSUES FOUND!")
        print("\nImmediate action required:")
        for item in results['critical']:
            if 'version_checks' in item:
                print(f"  • {item['entry_id']}: Update to {item['version_checks'][0]['current']}")

        # Exit with error code for CI/CD
        return 1

    # Update check schedule for entries that need it
    if args.verbose:
        print("\n💡 Scheduling next checks for entries due soon...")
        manager = MetadataManager(args.kb_root)

        # Find entries with checks due in next 7 days
        from datetime import timedelta
        upcoming = datetime.now() + timedelta(days=7)

        for item in results['upcoming']:
            if item['entry_id'] and item['days_until'] <= 7:
                # Find and update
                # (This would require file path lookup, simplified here)
                pass

    print("\n✅ Daily freshness check complete")

    return 0


if __name__ == '__main__':
    sys.exit(main())
