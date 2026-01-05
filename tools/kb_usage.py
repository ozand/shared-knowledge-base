#!/usr/bin/env python3
"""
kb_usage.py - Knowledge Base Usage Tracker

Tracks knowledge base usage locally for analytics and gap detection.
Maintains usage data in .cache/usage.json (not synced to git).

Author: Knowledge Base Curator
Version: 1.0.0
License: MIT
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import uuid


class UsageTracker:
    """Track knowledge base usage locally."""

    def __init__(self, cache_dir: Optional[Path] = None, project_id: Optional[str] = None):
        """
        Initialize UsageTracker.

        Args:
            cache_dir: Cache directory path (defaults to kb_root/.cache)
            project_id: Optional project identifier
        """
        self.cache_dir = cache_dir or Path.cwd() / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.usage_file = self.cache_dir / "usage.json"
        self.max_sessions_per_entry = 100
        self.max_query_history = 50

        self._ensure_usage_file()

        # Set or generate project ID
        if project_id:
            self.project_id = project_id
        else:
            with open(self.usage_file) as f:
                data = json.load(f)
                self.project_id = data.get('project_id')

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

            with open(self.usage_file, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=2)

    def _generate_project_id(self) -> str:
        """Generate anonymous project ID."""
        return f"project-{uuid.uuid4().hex[:8]}"

    def track_access(
        self,
        entry_id: str,
        method: str = "search",
        query: Optional[str] = None,
        context: str = "unknown",
        resolved: bool = False,
        agent: str = "unknown"
    ) -> int:
        """
        Record access to an entry.

        Args:
            entry_id: Entry identifier (e.g., IMPORT-001)
            method: Access method (search, direct_id, category_browse)
            query: Search query if method is 'search'
            context: Access context (error_resolution, prevention, learning)
            resolved: Whether the access resolved the issue
            agent: Agent making the access

        Returns:
            Updated access count
        """
        with open(self.usage_file, 'r', encoding='utf-8') as f:
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
        now = datetime.now().isoformat() + "Z"

        entry["access_count"] += 1
        entry["last_accessed_at"] = now
        if entry["first_accessed_at"] is None:
            entry["first_accessed_at"] = now

        # Update method count
        if method not in entry["access_methods"]:
            entry["access_methods"][method] = 0
        entry["access_methods"][method] += 1

        # Update context count
        if context not in entry["access_context"]:
            entry["access_context"][context] = 0
        entry["access_context"][context] += 1

        # Add session record
        session = {
            "timestamp": now,
            "method": method,
            "query": query if method == "search" else None,
            "context": context,
            "resolved": resolved,
            "agent": agent
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

        usage_data["last_updated_at"] = now

        # Save
        with open(self.usage_file, 'w', encoding='utf-8') as f:
            json.dump(usage_data, f, indent=2)

        return entry["access_count"]

    def _update_query_tracking(self, analytics: Dict, query: str, resolved: bool):
        """
        Update query statistics.

        Args:
            analytics: Search analytics dictionary
            query: Search query string
            resolved: Whether query was resolved
        """
        target_list = analytics["top_search_queries"] if resolved else analytics["no_results_queries"]

        # Find existing or add new
        found = False
        for item in target_list:
            if item["query"].lower() == query.lower():
                item["count"] += 1
                found = True
                break

        if not found:
            target_list.append({"query": query, "count": 1})

        # Sort and keep top N
        target_list.sort(key=lambda x: x["count"], reverse=True)
        limit = self.max_query_history
        if len(target_list) > limit:
            target_list[:] = target_list[:limit]

    def get_entry_stats(self, entry_id: str) -> Optional[Dict]:
        """
        Get usage statistics for an entry.

        Args:
            entry_id: Entry identifier

        Returns:
            Entry statistics dictionary or None if not found
        """
        with open(self.usage_file, 'r', encoding='utf-8') as f:
            usage_data = json.load(f)

        return usage_data["entries"].get(entry_id)

    def get_top_entries(self, limit: int = 10) -> List[tuple]:
        """
        Get most accessed entries.

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of (entry_id, access_count) tuples
        """
        with open(self.usage_file, 'r', encoding='utf-8') as f:
            usage_data = json.load(f)

        entries_with_counts = [
            (entry_id, data["access_count"])
            for entry_id, data in usage_data["entries"].items()
        ]

        entries_with_counts.sort(key=lambda x: x[1], reverse=True)
        return entries_with_counts[:limit]

    def get_search_analytics(self) -> Dict:
        """
        Get search analytics summary.

        Returns:
            Search analytics dictionary
        """
        with open(self.usage_file, 'r', encoding='utf-8') as f:
            usage_data = json.load(f)

        return usage_data["search_analytics"]

    def detect_gaps(self, min_count: int = 3) -> List[Dict]:
        """
        Detect search gaps from failed searches.

        Args:
            min_count: Minimum search count to consider as gap

        Returns:
            List of gap dictionaries with query, count, priority
        """
        with open(self.usage_file, 'r', encoding='utf-8') as f:
            usage_data = json.load(f)

        gaps = []
        for item in usage_data["search_analytics"]["no_results_queries"]:
            if item["count"] >= min_count:
                priority = "critical" if item["count"] >= 5 else "high" if item["count"] >= 4 else "medium"
                gaps.append({
                    "query": item["query"],
                    "count": item["count"],
                    "priority": priority
                })

        # Sort by count descending
        gaps.sort(key=lambda x: x["count"], reverse=True)
        return gaps

    def get_low_quality_high_usage(self, quality_lookup: Dict[str, int]) -> List[Dict]:
        """
        Find entries with high usage but low quality scores.

        Args:
            quality_lookup: Dictionary mapping entry_id to quality_score

        Returns:
            List of entries needing improvement
        """
        with open(self.usage_file, 'r', encoding='utf-8') as f:
            usage_data = json.load(f)

        opportunities = []
        quality_threshold = 75
        min_access_count = 10

        for entry_id, usage in usage_data["entries"].items():
            if usage["access_count"] < min_access_count:
                continue

            quality_score = quality_lookup.get(entry_id)
            if quality_score is None or quality_score < quality_threshold:
                opportunities.append({
                    "entry_id": entry_id,
                    "access_count": usage["access_count"],
                    "quality_score": quality_score,
                    "gap": quality_threshold - (quality_score or 0),
                    "last_accessed": usage["last_accessed_at"]
                })

        # Sort by access count descending
        opportunities.sort(key=lambda x: x["access_count"], reverse=True)
        return opportunities

    def get_usage_summary(self, days: int = 30) -> Dict:
        """
        Get usage summary for recent period.

        Args:
            days: Number of days to look back

        Returns:
            Usage summary dictionary
        """
        with open(self.usage_file, 'r', encoding='utf-8') as f:
            usage_data = json.load(f)

        cutoff_date = datetime.now() - timedelta(days=days)

        recent_entries = {}
        total_accesses = 0

        for entry_id, entry_data in usage_data["entries"].items():
            recent_sessions = []

            for session in entry_data.get("sessions", []):
                session_time = datetime.fromisoformat(session["timestamp"].replace('Z', '+00:00'))
                if session_time > cutoff_date:
                    recent_sessions.append(session)
                    total_accesses += 1

            if recent_sessions:
                recent_entries[entry_id] = {
                    "access_count": len(recent_sessions),
                    "last_accessed": entry_data["last_accessed_at"],
                    "methods": {}
                }

                for session in recent_sessions:
                    method = session["method"]
                    recent_entries[entry_id]["methods"][method] = \
                        recent_entries[entry_id]["methods"].get(method, 0) + 1

        return {
            "period_days": days,
            "total_accesses": total_accesses,
            "entries_accessed": len(recent_entries),
            "top_entries": sorted(
                [(eid, data["access_count"]) for eid, data in recent_entries.items()],
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }

    def export_analytics(self, period: str = "all") -> Dict:
        """
        Export anonymized analytics for community sharing.

        Args:
            period: Period to export (all, or YYYY-MM format)

        Returns:
            Anonymized analytics dictionary
        """
        with open(self.usage_file, 'r', encoding='utf-8') as f:
            usage_data = json.load(f)

        # Create anonymized export
        export = {
            "version": "1.0",
            "period": period,
            "anonymized": True,
            "usage_summary": {
                "total_searches": usage_data["search_analytics"]["total_searches"],
                "successful_searches": usage_data["search_analytics"]["successful_searches"],
                "unique_entries_accessed": len(usage_data["entries"]),
                "success_rate": usage_data["search_analytics"]["successful_searches"] /
                               max(usage_data["search_analytics"]["total_searches"], 1)
            },
            "top_accessed_entries": [
                {"entry_id": eid, "access_count": count}
                for eid, count in self.get_top_entries(20)
            ],
            "search_gaps": [
                {"query": gap["query"], "count": gap["count"]}
                for gap in self.detect_gaps(min_count=2)
            ]
        }

        return export

    def reset_tracking(self):
        """Reset all tracking data (use with caution)."""
        self.usage_file.unlink()
        self._ensure_usage_file()
        print("✓ Usage tracking reset")


def main():
    """CLI interface for usage tracking."""
    import argparse

    parser = argparse.ArgumentParser(description="Knowledge Base Usage Tracker")
    parser.add_argument('action', choices=['track', 'stats', 'top', 'gaps', 'export', 'reset'],
                       help='Action to perform')
    parser.add_argument('--cache-dir', type=Path,
                       help='Cache directory path')
    parser.add_argument('--entry-id',
                       help='Entry ID to track')
    parser.add_argument('--method', choices=['search', 'direct_id', 'category_browse'],
                       default='search', help='Access method')
    parser.add_argument('--query',
                       help='Search query')
    parser.add_argument('--context', choices=['error_resolution', 'prevention', 'learning'],
                       default='unknown', help='Access context')
    parser.add_argument('--resolved', action='store_true',
                       help='Whether the access resolved the issue')
    parser.add_argument('--limit', type=int, default=10,
                       help='Limit for results')
    parser.add_argument('--output', type=Path,
                       help='Output file for export')

    args = parser.parse_args()
    tracker = UsageTracker(args.cache_dir)

    if args.action == 'track':
        if not args.entry_id:
            print("--entry-id required for track action")
            return

        count = tracker.track_access(
            args.entry_id,
            method=args.method,
            query=args.query,
            context=args.context,
            resolved=args.resolved
        )
        print(f"✓ Tracked access to {args.entry_id} (total: {count})")

    elif args.action == 'stats':
        summary = tracker.get_usage_summary(days=30)
        print(f"\n📊 Usage Summary ({summary['period_days']} days)\n")
        print(f"Total accesses: {summary['total_accesses']}")
        print(f"Unique entries: {summary['entries_accessed']}")

        if summary['top_entries']:
            print(f"\nTop entries:")
            for entry_id, count in summary['top_entries'][:5]:
                print(f"  - {entry_id}: {count}")

    elif args.action == 'top':
        top_entries = tracker.get_top_entries(args.limit)
        print(f"\n🔝 Top {len(top_entries)} Entries\n")
        for entry_id, count in top_entries:
            print(f"  {entry_id}: {count} accesses")

    elif args.action == 'gaps':
        gaps = tracker.detect_gaps(min_count=2)
        print(f"\n🔍 Search Gaps ({len(gaps)} found)\n")
        for gap in gaps:
            print(f"  - \"{gap['query']}\" ({gap['count']} searches) [{gap['priority']}]")

    elif args.action == 'export':
        export = tracker.export_analytics()

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(export, f, indent=2)
            print(f"✓ Exported to {args.output}")
        else:
            print(json.dumps(export, indent=2))

    elif args.action == 'reset':
        tracker.reset_tracking()


if __name__ == '__main__':
    main()
