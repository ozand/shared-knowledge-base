#!/usr/bin/env python3
"""
weekly_usage.py - Weekly Usage Analysis Script

Analyzes local usage patterns to identify gaps and improvement opportunities.
Generates reports and recommendations.

Usage:
    python scripts/weekly_usage.py [--days 7] [--output report.json]
    Can be run via cron/scheduler:
        0 10 * * 1 python /path/to/kb/scripts/weekly_usage.py --days 7

Author: Knowledge Base Curator
Version: 1.0.0
License: MIT
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add tools directory to path
tools_dir = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(tools_dir))

try:
    from kb_usage import UsageTracker
    from kb_meta import MetadataManager
except ImportError as e:
    print(f"❌ Cannot import required modules: {e}")
    sys.exit(1)


def main():
    """Run weekly usage analysis."""
    import argparse

    parser = argparse.ArgumentParser(description="Weekly Usage Analysis")
    parser.add_argument('--kb-root', type=Path, default=Path.cwd(),
                       help='Knowledge base root directory')
    parser.add_argument('--cache-dir', type=Path,
                       help='Cache directory (defaults to kb_root/.cache)')
    parser.add_argument('--days', type=int, default=7,
                       help='Days to analyze (default: 7)')
    parser.add_argument('--output', type=Path,
                       help='Output file for report (JSON format)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    kb_root = args.kb_root
    if args.cache_dir:
        cache_dir = args.cache_dir
    else:
        cache_dir = kb_root / ".cache"

    print("📊 Weekly Usage Analysis")
    print(f"   Timestamp: {datetime.now().isoformat()}")
    print(f"   KB Root: {kb_root}")
    print(f"   Period: Last {args.days} days")
    print()

    # Initialize tracker
    tracker = UsageTracker(cache_dir)

    # Get usage summary
    summary = tracker.get_usage_summary(days=args.days)

    print(f"📈 Usage Summary ({args.days} days)")
    print(f"   Total accesses: {summary['total_accesses']}")
    print(f"   Unique entries: {summary['entries_accessed']}")
    print()

    # Top entries
    if summary['top_entries']:
        print(f"🔝 Top {len(summary['top_entries'])} Entries:")
        for entry_id, count in summary['top_entries'][:10]:
            print(f"   {count:3d} - {entry_id}")
    else:
        print("No usage data yet")

    # Search gaps
    print()
    gaps = tracker.detect_gaps(min_count=2)

    if gaps:
        print(f"🔍 Search Gaps ({len(gaps)} found)")
        print("   Consider creating entries for:")

        for i, gap in enumerate(gaps[:10], 1):
            print(f"   {i}. \"{gap['query']}\" ({gap['count']} searches) [{gap['priority']}]")
    else:
        print("✓ No search gaps detected")

    # High access, low quality entries
    print()
    if MetadataManager:
        meta_manager = MetadataManager(kb_root)
        all_entries = meta_manager.get_all_entries_metadata()

        quality_lookup = {}
        for entry_id, data in all_entries.items():
            quality = data['metadata'].get('quality_score')
            if quality is not None:
                quality_lookup[entry_id] = quality

        opportunities = tracker.get_low_quality_high_usage(quality_lookup)

        if opportunities:
            print(f"⚠️  High Access, Low Quality ({len(opportunities)} entries)")
            print("   Consider enhancing:")

            for opp in opportunities[:5]:
                quality = opp['quality_score'] or 'Unknown'
                gap = opp['gap']
                print(f"   • {opp['entry_id']}: {opp['access_count']} accesses, "
                      f"quality: {quality} (gap: {gap} points)")
        else:
            print("✓ No low-quality, high-access entries")

    # Export report
    report = {
        "timestamp": datetime.now().isoformat(),
        "period_days": args.days,
        "summary": summary,
        "gaps": gaps,
        "opportunities": opportunities if MetadataManager else []
    }

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n✓ Report saved to: {args.output}")

    # Recommendations
    print()
    print("💡 Recommendations:")

    critical_gaps = [g for g in gaps if g['priority'] == 'critical']
    if critical_gaps:
        print("   Priority: IMMEDIATE")
        for gap in critical_gaps[:3]:
            print(f"   - Create entry for: \"{gap['query']}\"")

    if opportunities:
        print()
        print("   Priority: THIS WEEK")
        for opp in opportunities[:2]:
            print(f"   - Enhance {opp['entry_id']} (quality: {opp['quality_score']})")

    print()
    print("✅ Weekly usage analysis complete")

    return 0


if __name__ == '__main__':
    sys.exit(main())
