#!/usr/bin/env python3
"""
monthly_community.py - Monthly Community Aggregation Script

Aggregates anonymized analytics from multiple projects.
Generates community reports and identifies universal patterns.

Usage:
    python scripts/monthly_community.py [--report report.txt]
    Can be run via cron/scheduler:
        0 0 1 * * python /path/to/kb/scripts/monthly_community.py

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
    from kb_community import CommunityAnalytics
except ImportError as e:
    print(f"❌ Cannot import required modules: {e}")
    sys.exit(1)


def main():
    """Run monthly community aggregation."""
    import argparse

    parser = argparse.ArgumentParser(description="Monthly Community Aggregation")
    parser.add_argument('--kb-root', type=Path, default=Path.cwd(),
                       help='Knowledge base root directory')
    parser.add_argument('--cache-dir', type=Path,
                       help='Cache directory (defaults to kb_root/.cache)')
    parser.add_argument('--output', type=Path,
                       help='Output file for report')
    parser.add_argument('--min-projects', type=int, default=3,
                       help='Minimum projects for universal pattern (default: 3)')
    parser.add_argument('--export', action='store_true',
                       help='Also export local analytics')
    parser.add_argument('--project-name', default='unknown',
                       help='Project name for export')
    parser.add_argument('--project-type', default='other',
                       choices=['web', 'ml', 'mobile', 'desktop', 'api', 'other'],
                       help='Project type for export')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    print("🌐 Monthly Community Aggregation")
    print(f"   Timestamp: {datetime.now().isoformat()}")
    print(f"   KB Root: {args.kb_root}")
    print()

    cache_dir = args.cache_dir
    if cache_dir is None:
        cache_dir = args.kb_root / ".cache" / "community"

    analytics = CommunityAnalytics(cache_dir)

    # Export local analytics if requested
    if args.export:
        print("📤 Exporting local analytics...")
        success = analytics.export_local_analytics(
            kb_root=args.kb_root,
            project_name=args.project_name,
            project_type=args.project_type
        )
        if not success:
            print("✗ Failed to export local analytics")
            return 1
        print()

    # Check if we have data
    if not analytics.projects_file.exists():
        print("ℹ️  No project exports found")
        print("\nTo participate in community analytics:")
        print("  1. Export your analytics: python -m kb_community export-analytics")
        print("  2. Share the export file (optional, opt-in)")
        print("  3. Add exports to: {cache_dir}/")
        return 0

    # Aggregate
    print("📊 Aggregating community data...")
    aggregated = analytics.aggregate_analytics()

    if not aggregated:
        print("✗ No data to aggregate")
        return 1

    print(f"   Projects: {aggregated['total_projects']}")
    print(f"   Entries: {aggregated['total_entries']}")
    print(f"   Accesses: {aggregated['total_accesses']:,}")
    print()

    # Identify universal patterns
    print("🌟 Identifying universal patterns...")
    universal = analytics.identify_universal_patterns(min_projects=args.min_projects)

    print(f"   Found {len(universal)} universal patterns")
    if universal:
        print(f"   Top 5:")
        for i, (entry_id, data) in enumerate(list(universal.items())[:5], 1):
            print(f"     {i}. {entry_id} ({data['project_count']} projects)")
    print()

    # Generate report
    print("📋 Generating community report...")
    report = analytics.generate_community_report()

    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"✓ Report saved to: {args.output}")
    else:
        if args.verbose:
            print()
            print(report)

    # Recommendations
    print()
    print("💡 Monthly Recommendations:")

    universal_patterns = aggregated.get('universal_patterns', {})
    if universal_patterns:
        print("\n  Universal Patterns:")
        print("  • Review top 10 universal patterns for quality")
        print("  • Consider expanding with more examples")

    gaps = aggregated.get('top_gaps', [])
    critical_gaps = [g for g in gaps if g['priority'] == 'critical']

    if critical_gaps:
        print("\n  Critical Gaps:")
        for gap in critical_gaps[:3]:
            print(f"  • Create entry: \"{gap['query']}\"")

    quality = aggregated.get('quality_metrics', {})
    if quality and quality['average_score'] < 75:
        print("\n  Quality Improvement:")
        print("  • Community average below 75")
        print("  • Review quality rubric with contributors")

    print()
    print("✅ Monthly community aggregation complete")

    return 0


if __name__ == '__main__':
    sys.exit(main())
