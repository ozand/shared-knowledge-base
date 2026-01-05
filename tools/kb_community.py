#!/usr/bin/env python3
"""
kb_community.py - Community Analytics Aggregation

Aggregates anonymized analytics from multiple projects to identify:
- Universal patterns (entries used across multiple projects)
- Community gaps (common search failures)
- Quality trends across projects
- Popular entries by project type

Privacy-First:
- Only aggregated statistics are shared
- No identifying information
- Opt-in per project
- Anonymization of project names (hash-based)

Usage:
    python tools/kb_community.py aggregate [input_dir]
    python tools/kb_community.py report [output_file]
    python tools/kb_community.py export-analytics [--output export.json]

Author: Knowledge Base Curator
Version: 1.0.0
License: MIT
"""

import sys
from pathlib import Path

# Add tools directory to path for imports
tools_dir = Path(__file__).parent
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter


@dataclass
class ProjectStats:
    """Anonymized statistics from a single project."""
    project_hash: str  # SHA256 of project name (for privacy)
    project_type: str  # 'web', 'ml', 'mobile', 'desktop', 'api', 'other'
    total_entries: int
    period_days: int
    export_date: str
    total_accesses: int
    unique_entries_accessed: int
    top_entries: List[tuple]  # [(entry_id, count), ...]
    search_gaps: List[dict]  # [{query, count, priority}, ...]
    quality_scores: List[tuple]  # [(entry_id, score), ...]
    scope_breakdown: Dict[str, int]  # {scope: count}


class CommunityAnalytics:
    """Aggregate and analyze community-wide knowledge base usage."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize CommunityAnalytics.

        Args:
            cache_dir: Directory for community data (defaults to .cache/community)
        """
        if cache_dir is None:
            from kb_config import KBConfig
            config = KBConfig()
            cache_dir = config.cache_root / "community"

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Storage files
        self.projects_file = self.cache_dir / "projects.json"
        self.aggregated_file = self.cache_dir / "aggregated.json"
        self.patterns_file = self.cache_dir / "universal_patterns.json"

    def anonymize_project_name(self, project_name: str) -> str:
        """
        Anonymize project name using SHA256 hash.

        Args:
            project_name: Real project name

        Returns:
            Anonymized hash (first 16 chars)
        """
        return hashlib.sha256(project_name.encode()).hexdigest()[:16]

    def validate_export(self, export_data: Dict) -> tuple[bool, str]:
        """
        Validate analytics export data.

        Args:
            export_data: Export data to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        required_fields = [
            'project_hash', 'project_type', 'total_entries',
            'period_days', 'export_date', 'total_accesses',
            'unique_entries_accessed'
        ]

        for field in required_fields:
            if field not in export_data:
                return False, f"Missing required field: {field}"

        # Validate project type
        valid_types = ['web', 'ml', 'mobile', 'desktop', 'api', 'other']
        if export_data['project_type'] not in valid_types:
            return False, f"Invalid project_type: {export_data['project_type']}"

        # Validate dates
        try:
            datetime.fromisoformat(export_data['export_date'])
        except ValueError:
            return False, "Invalid export_date format"

        # Validate numeric fields
        if export_data['total_entries'] < 0:
            return False, "total_entries cannot be negative"

        if export_data['period_days'] <= 0:
            return False, "period_days must be positive"

        return True, ""

    def add_project_export(self, export_data: Dict) -> bool:
        """
        Add anonymized project export to community database.

        Args:
            export_data: Project stats export (JSON or dict)

        Returns:
            True if added successfully
        """
        # Load from file if needed
        if isinstance(export_data, (str, Path)):
            export_file = Path(export_data)
            if not export_file.exists():
                print(f"✗ Export file not found: {export_file}")
                return False

            with open(export_file, 'r') as f:
                export_data = json.load(f)

        # Validate
        is_valid, error = self.validate_export(export_data)
        if not is_valid:
            print(f"✗ Invalid export: {error}")
            return False

        # Load existing projects
        projects = []
        if self.projects_file.exists():
            with open(self.projects_file, 'r') as f:
                projects = json.load(f)

        # Check for duplicate (same project_hash + export_date)
        for proj in projects:
            if (proj['project_hash'] == export_data['project_hash'] and
                proj['export_date'] == export_data['export_date']):
                print(f"ℹ️  Export already exists for this project/date")
                return True

        # Add new export
        projects.append(export_data)

        # Save
        with open(self.projects_file, 'w') as f:
            json.dump(projects, f, indent=2)

        print(f"✓ Added export for project {export_data['project_hash']} ({export_data['project_type']})")
        return True

    def aggregate_analytics(self) -> Dict:
        """
        Aggregate analytics across all projects.

        Returns:
            Aggregated statistics dictionary
        """
        if not self.projects_file.exists():
            print("ℹ️  No project exports found")
            return {}

        with open(self.projects_file, 'r') as f:
            projects = json.load(f)

        if not projects:
            return {}

        # Initialize aggregations
        total_projects = len(projects)
        total_accesses = sum(p['total_accesses'] for p in projects)
        total_entries = sum(p['total_entries'] for p in projects)

        # Project type breakdown
        type_counts = Counter(p['project_type'] for p in projects)

        # Entry popularity across projects
        entry_projects = defaultdict(set)  # entry_id -> set of project_hashes
        entry_accesses = defaultdict(int)  # entry_id -> total accesses

        for proj in projects:
            proj_hash = proj['project_hash']
            for entry_id, count in proj.get('top_entries', []):
                entry_projects[entry_id].add(proj_hash)
                entry_accesses[entry_id] += count

        # Universal patterns (used in >= 3 projects)
        universal_patterns = {
            entry_id: {
                'project_count': len(proj_set),
                'total_accesses': entry_accesses[entry_id],
                'projects': list(proj_set)
            }
            for entry_id, proj_set in entry_projects.items()
            if len(proj_set) >= 3
        }

        # Sort by project count
        universal_patterns = dict(
            sorted(universal_patterns.items(),
                  key=lambda x: x[1]['project_count'],
                  reverse=True)
        )

        # Community search gaps
        gap_queries = defaultdict(int)
        gap_priorities = defaultdict(list)

        for proj in projects:
            for gap in proj.get('search_gaps', []):
                query = gap['query']
                gap_queries[query] += gap['count']
                gap_priorities[query].append(gap.get('priority', 'medium'))

        # Top gaps (most common search failures)
        top_gaps = [
            {
                'query': query,
                'count': count,
                'projects': len(gap_priorities[query]),
                'priority': max(set(gap_priorities[query]), key=gap_priorities[query].count)
            }
            for query, count in gap_queries.most_common(50)
        ]

        # Quality trends
        all_quality_scores = []
        for proj in projects:
            for entry_id, score in proj.get('quality_scores', []):
                all_quality_scores.append(score)

        avg_quality = sum(all_quality_scores) / len(all_quality_scores) if all_quality_scores else 0

        # Build aggregation
        aggregated = {
            'generated_at': datetime.now().isoformat(),
            'total_projects': total_projects,
            'total_accesses': total_accesses,
            'total_entries': total_entries,
            'avg_accesses_per_project': total_accesses / total_projects if total_projects > 0 else 0,
            'project_type_breakdown': dict(type_counts),
            'universal_patterns': universal_patterns,
            'top_gaps': top_gaps,
            'quality_metrics': {
                'average_score': round(avg_quality, 2),
                'total_scores': len(all_quality_scores),
                'score_distribution': {
                    'excellent': len([s for s in all_quality_scores if s >= 90]),
                    'good': len([s for s in all_quality_scores if 75 <= s < 90]),
                    'acceptable': len([s for s in all_quality_scores if 60 <= s < 75]),
                    'needs_improvement': len([s for s in all_quality_scores if s < 60])
                }
            }
        }

        # Save aggregated data
        with open(self.aggregated_file, 'w') as f:
            json.dump(aggregated, f, indent=2)

        return aggregated

    def identify_universal_patterns(self, min_projects: int = 3) -> Dict:
        """
        Identify universal patterns used across multiple projects.

        Args:
            min_projects: Minimum number of projects to consider "universal"

        Returns:
            Dictionary of universal patterns
        """
        if not self.aggregated_file.exists():
            self.aggregate_analytics()

        with open(self.aggregated_file, 'r') as f:
            aggregated = json.load(f)

        universal = aggregated.get('universal_patterns', {})

        # Filter by min_projects
        filtered = {
            entry_id: data
            for entry_id, data in universal.items()
            if data['project_count'] >= min_projects
        }

        # Save patterns
        with open(self.patterns_file, 'w') as f:
            json.dump(filtered, f, indent=2)

        return filtered

    def generate_community_report(self) -> str:
        """
        Generate comprehensive community analytics report.

        Returns:
            Formatted report string
        """
        aggregated = self.aggregate_analytics()

        if not aggregated:
            return "ℹ️  No community data available"

        report = f"""
╔═══════════════════════════════════════════════════════════════╗
║          COMMUNITY KNOWLEDGE BASE ANALYTICS REPORT             ║
╚═══════════════════════════════════════════════════════════════╝

Generated: {aggregated['generated_at']}

📊 OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Projects:        {aggregated['total_projects']}
  Total Entries:         {aggregated['total_entries']}
  Total Accesses:        {aggregated['total_accesses']:,}
  Avg Accesses/Project:  {aggregated['avg_accesses_per_project']:,.1f}

"""

        # Project types
        type_breakdown = aggregated.get('project_type_breakdown', {})
        if type_breakdown:
            report += "📁 Project Types\n"
            report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            for proj_type, count in sorted(type_breakdown.items(), key=lambda x: x[1], reverse=True):
                pct = (count / aggregated['total_projects']) * 100
                report += f"  {proj_type:12s} {count:3d} projects ({pct:5.1f}%)\n"
            report += "\n"

        # Universal patterns
        universal = aggregated.get('universal_patterns', {})
        if universal:
            top_universal = list(universal.items())[:20]

            report += f"🌟 UNIVERSAL PATTERNS (Used in ≥3 projects)\n"
            report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            report += f"  {'Entry ID':40s} {'Projects':>8s} {'Accesses':>10s}\n"
            report += "  " + "-" * 62 + "\n"

            for entry_id, data in top_universal:
                report += f"  {entry_id:40s} {data['project_count']:>8d} {data['total_accesses']:>10,}\n"

            if len(universal) > 20:
                report += f"  ... and {len(universal) - 20} more\n"
            report += "\n"

        # Community gaps
        gaps = aggregated.get('top_gaps', [])
        if gaps:
            top_gaps = gaps[:15]

            report += f"🔍 COMMUNITY GAPS (Common search failures)\n"
            report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            report += f"  {'Query':40s} {'Count':>6s} {'Projects':>8s} {'Priority':>10s}\n"
            report += "  " + "-" * 68 + "\n"

            for gap in top_gaps:
                query = gap['query'][:40]
                report += f"  {query:40s} {gap['count']:>6d} {gap['projects']:>8d} {gap['priority']:>10s}\n"

            if len(gaps) > 15:
                report += f"  ... and {len(gaps) - 15} more\n"
            report += "\n"

        # Quality metrics
        quality = aggregated.get('quality_metrics', {})
        if quality:
            dist = quality.get('score_distribution', {})

            report += f"⭐ QUALITY METRICS\n"
            report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            report += f"  Average Score:     {quality['average_score']:.1f} / 100\n"
            report += f"  Total Scores:      {quality['total_scores']:,}\n"
            report += "\n"
            report += "  Distribution:\n"
            report += f"    Excellent (90-100):      {dist['excellent']:>6d} ({dist['excellent']/quality['total_scores']*100 if quality['total_scores'] > 0 else 0:.1f}%)\n"
            report += f"    Good (75-89):            {dist['good']:>6d} ({dist['good']/quality['total_scores']*100 if quality['total_scores'] > 0 else 0:.1f}%)\n"
            report += f"    Acceptable (60-74):      {dist['acceptable']:>6d} ({dist['acceptable']/quality['total_scores']*100 if quality['total_scores'] > 0 else 0:.1f}%)\n"
            report += f"    Needs Improvement (<60):  {dist['needs_improvement']:>6d} ({dist['needs_improvement']/quality['total_scores']*100 if quality['total_scores'] > 0 else 0:.1f}%)\n"
            report += "\n"

        # Recommendations
        report += "💡 RECOMMENDATIONS\n"
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        if universal:
            report += "  1. Universal Patterns:\n"
            report += "     These entries are highly valued across projects.\n"
            report += "     • Ensure they maintain high quality (≥90)\n"
            report += "     • Consider expanding with more examples\n"
            report += "     • Use as templates for new entries\n"
            report += "\n"

        if gaps:
            critical_gaps = [g for g in gaps if g['priority'] == 'critical']
            if critical_gaps:
                report += "  2. Critical Gaps:\n"
                report += "     Priority actions for community:\n"
                for gap in critical_gaps[:3]:
                    report += f"     • Create entry: \"{gap['query']}\"\n"
                report += "\n"

        if quality:
            if quality['average_score'] < 75:
                report += "  3. Quality Improvement:\n"
                report += "     Community average is below target (75).\n"
                report += "     • Review and enhance low-scoring entries\n"
                report += "     • Share quality rubric with contributors\n"
                report += "\n"

        report += "\n✅ End of Report\n"

        return report

    def export_local_analytics(self, kb_root: Optional[Path] = None,
                              output_file: Optional[Path] = None,
                              project_name: str = "unknown",
                              project_type: str = "other") -> bool:
        """
        Export local analytics for community aggregation.

        Args:
            kb_root: Knowledge base root directory
            output_file: Output file path (defaults to .cache/community/export.json)
            project_name: Project name (will be anonymized)
            project_type: Project type (web, ml, mobile, desktop, api, other)

        Returns:
            True if export successful
        """
        from kb_usage import UsageTracker
        from kb_meta import MetadataManager

        if kb_root is None:
            from kb_config import KBConfig
            config = KBConfig()
            kb_root = config.kb_root

        if output_file is None:
            output_file = self.cache_dir / "export.json"

        # Initialize tools
        tracker = UsageTracker(kb_root / ".cache")
        manager = MetadataManager(kb_root)

        # Get usage summary
        summary = tracker.get_usage_summary(days=30)  # Last 30 days

        # Get all metadata
        all_metadata = manager.get_all_entries_metadata()

        # Extract quality scores
        quality_scores = []
        for entry_id, data in all_metadata.items():
            score = data['metadata'].get('quality_score')
            if score is not None:
                quality_scores.append((entry_id, score))

        # Build export
        export_data = {
            'project_hash': self.anonymize_project_name(project_name),
            'project_type': project_type,
            'total_entries': len(all_metadata),
            'period_days': 30,
            'export_date': datetime.now().isoformat(),
            'total_accesses': summary['total_accesses'],
            'unique_entries_accessed': summary['entries_accessed'],
            'top_entries': summary['top_entries'][:50],  # Top 50
            'search_gaps': tracker.detect_gaps(min_count=2)[:50],  # Top 50 gaps
            'quality_scores': quality_scores,
            'scope_breakdown': self._calculate_scope_breakdown(all_metadata)
        }

        # Save export
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"✓ Exported analytics to: {output_file}")
        print(f"  Project: {export_data['project_hash']} ({project_type})")
        print(f"  Entries: {export_data['total_entries']}")
        print(f"  Accesses: {export_data['total_accesses']}")

        return True

    def _calculate_scope_breakdown(self, all_metadata: Dict) -> Dict[str, int]:
        """Calculate entry count by scope."""
        scope_counts = defaultdict(int)

        for entry_id, data in all_metadata.items():
            scope = data['metadata'].get('scope', 'unknown')
            scope_counts[scope] += 1

        return dict(scope_counts)


def main():
    """CLI interface for community analytics."""
    import argparse

    parser = argparse.ArgumentParser(description="Community Analytics Aggregation")
    parser.add_argument('action', choices=['aggregate', 'report', 'export-analytics'],
                       help='Action to perform')
    parser.add_argument('--kb-root', type=Path,
                       help='Knowledge base root directory')
    parser.add_argument('--input',
                       help='Input export file (for aggregate action)')
    parser.add_argument('--output', type=Path,
                       help='Output file path')
    parser.add_argument('--project-name', default='unknown',
                       help='Project name for export (will be anonymized)')
    parser.add_argument('--project-type', default='other',
                       choices=['web', 'ml', 'mobile', 'desktop', 'api', 'other'],
                       help='Project type for export')
    parser.add_argument('--cache-dir', type=Path,
                       help='Cache directory (defaults to kb_root/.cache/community)')
    parser.add_argument('--min-projects', type=int, default=3,
                       help='Minimum projects for universal pattern (default: 3)')

    args = parser.parse_args()

    # Initialize
    cache_dir = args.cache_dir
    if cache_dir is None and args.kb_root:
        cache_dir = args.kb_root / ".cache" / "community"

    analytics = CommunityAnalytics(cache_dir)

    if args.action == 'aggregate':
        if args.input:
            success = analytics.add_project_export(args.input)
            if not success:
                return 1

            # Regenerate aggregation
            aggregated = analytics.aggregate_analytics()
            print(f"\n✓ Aggregated {aggregated['total_projects']} projects")
        else:
            print("✗ --input required for aggregate action")
            return 1

    elif args.action == 'report':
        report = analytics.generate_community_report()

        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"✓ Report saved to: {args.output}")
        else:
            print(report)

    elif args.action == 'export-analytics':
        success = analytics.export_local_analytics(
            kb_root=args.kb_root,
            output_file=args.output,
            project_name=args.project_name,
            project_type=args.project_type
        )
        if not success:
            return 1

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
