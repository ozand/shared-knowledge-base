#!/usr/bin/env python3
"""
kb_predictive.py - Predictive Analytics and ML-Based Suggestions

Predicts:
- Which entries will need updates soon
- New entries to create based on search trends
- Quality scores for new content
- Entries at risk of becoming stale
- Optimal review schedule

Uses lightweight statistical analysis (no heavy ML dependencies).

Usage:
    python tools/kb_predictive.py predict-updates
    python tools/kb_predictive.py suggest-entries
    python tools/kb_predictive.py estimate-quality [entry_file]
    python tools/kb_predictive.py risk-assessment

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
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import re


@dataclass
class UpdatePrediction:
    """Prediction for entry update."""
    entry_id: str
    probability: float  # 0-1
    reason: str
    suggested_action: str
    timeframe: str  # 'immediate', 'week', 'month', 'quarter'


@dataclass
class EntrySuggestion:
    """Suggestion for new entry creation."""
    title: str
    priority: str  # 'critical', 'high', 'medium', 'low'
    confidence: float  # 0-1
    search_count: int
    related_queries: List[str]
    suggested_scope: str


@dataclass
class QualityEstimate:
    """Estimated quality for entry content."""
    entry_id: str
    estimated_score: int  # 0-100
    confidence: float  # 0-1
    strengths: List[str]
    weaknesses: List[str]
    improvements: List[str]


@dataclass
class RiskAssessment:
    """Risk assessment for entry staleness."""
    entry_id: str
    risk_level: str  # 'critical', 'high', 'medium', 'low'
    factors: List[str]
    probability: float
    mitigation: str


class PredictiveAnalytics:
    """Predictive analytics for knowledge base management."""

    def __init__(self, kb_root: Optional[Path] = None):
        """
        Initialize PredictiveAnalytics.

        Args:
            kb_root: Root directory of knowledge base
        """
        if kb_root is None:
            from kb_config import KBConfig
            config = KBConfig()
            kb_root = config.kb_root

        self.kb_root = Path(kb_root)
        self.cache_dir = self.kb_root / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Prediction cache
        self.predictions_file = self.cache_dir / "predictions.json"

    def predict_updates_needed(self, days_ahead: int = 30) -> List[UpdatePrediction]:
        """
        Predict which entries will need updates soon.

        Args:
            days_ahead: Days to predict ahead

        Returns:
            List of UpdatePrediction objects
        """
        from kb_meta import MetadataManager
        from kb_freshness import FreshnessChecker

        manager = MetadataManager(self.kb_root)
        checker = FreshnessChecker(self.kb_root)

        all_metadata = manager.get_all_entries_metadata()
        predictions = []

        for entry_id, data in all_metadata.items():
            meta = data['metadata']

            # Factor 1: Version checks due
            next_check = meta.get('next_version_check_due')
            if next_check:
                try:
                    check_date = datetime.fromisoformat(next_check)
                    if check_date < datetime.now() + timedelta(days=days_ahead):
                        predictions.append(UpdatePrediction(
                            entry_id=entry_id,
                            probability=0.9,
                            reason=f"Version check due on {next_check}",
                            suggested_action="Run version check and update tested versions",
                            timeframe='immediate' if check_date < datetime.now() + timedelta(days=7) else 'week'
                        ))
                        continue
                except:
                    pass

            # Factor 2: Last analyzed age
            last_analyzed = meta.get('last_analyzed_at')
            if last_analyzed:
                try:
                    analyzed_date = datetime.fromisoformat(last_analyzed)
                    days_since = (datetime.now() - analyzed_date).days

                    # Higher probability if not analyzed recently
                    if days_since > 180:  # 6 months
                        probability = min(0.8, days_since / 365)
                        predictions.append(UpdatePrediction(
                            entry_id=entry_id,
                            probability=probability,
                            reason=f"Not analyzed for {days_since} days",
                            suggested_action="Review content for accuracy and completeness",
                            timeframe='month' if days_since < 365 else 'quarter'
                        ))
                except:
                    pass

            # Factor 3: Quality score
            quality = meta.get('quality_score')
            if quality is not None and quality < 75:
                predictions.append(UpdatePrediction(
                    entry_id=entry_id,
                    probability=0.7,
                    reason=f"Quality score below threshold ({quality}/100)",
                    suggested_action="Enhance content to improve quality score",
                    timeframe='month'
                ))

            # Factor 4: Library version mismatch
            tested_versions = meta.get('tested_versions', {})
            if tested_versions:
                # Check if any version is outdated
                version_status = checker._check_version_updates(tested_versions)
                if version_status:
                    for status in version_status:
                        if status.get('outdated'):
                            predictions.append(UpdatePrediction(
                                entry_id=entry_id,
                                probability=0.85,
                                reason=f"Outdated library version: {status['library']}",
                                suggested_action=f"Test with {status['current']} and update",
                                timeframe='week'
                            ))
                            break

        # Sort by probability
        predictions.sort(key=lambda p: p.probability, reverse=True)

        return predictions

    def suggest_new_entries(self, min_gap_count: int = 3) -> List[EntrySuggestion]:
        """
        Suggest new entries based on search gap trends.

        Args:
            min_gap_count: Minimum search gap count to suggest

        Returns:
            List of EntrySuggestion objects
        """
        from kb_usage import UsageTracker

        tracker = UsageTracker(self.cache_dir)
        gaps = tracker.detect_gaps(min_count=min_gap_count)

        suggestions = []

        for gap in gaps[:20]:  # Top 20 gaps
            query = gap['query']
            count = gap['count']

            # Determine priority based on count and frequency
            if count >= 10:
                priority = 'critical'
                confidence = 0.9
            elif count >= 5:
                priority = 'high'
                confidence = 0.8
            elif count >= 3:
                priority = 'medium'
                confidence = 0.7
            else:
                priority = 'low'
                confidence = 0.6

            # Suggest scope based on query keywords
            suggested_scope = self._infer_scope_from_query(query)

            # Find related queries
            related = [g['query'] for g in gaps
                      if g != gap and self._queries_related(query, g['query'])]

            suggestions.append(EntrySuggestion(
                title=query,
                priority=priority,
                confidence=confidence,
                search_count=count,
                related_queries=related[:5],
                suggested_scope=suggested_scope
            ))

        return suggestions

    def _infer_scope_from_query(self, query: str) -> str:
        """Infer scope from search query."""
        query_lower = query.lower()

        # Framework indicators
        frameworks = {
            'fastapi': 'framework/fastapi',
            'django': 'framework/django',
            'flask': 'framework/flask',
            'react': 'framework/react',
            'vue': 'framework/vue',
            'angular': 'framework/angular'
        }

        for framework, scope in frameworks.items():
            if framework in query_lower:
                return scope

        # Language indicators
        languages = {
            'python': 'language/python',
            'javascript': 'language/javascript',
            'typescript': 'language/typescript',
            'java': 'language/java',
            'go': 'language/go'
        }

        for language, scope in languages.items():
            if language in query_lower:
                return scope

        # Database indicators
        databases = {
            'postgresql': 'database/postgresql',
            'mysql': 'database/mysql',
            'mongodb': 'database/mongodb',
            'redis': 'database/redis'
        }

        for database, scope in databases.items():
            if database in query_lower:
                return scope

        # Default to universal
        return 'universal'

    def _queries_related(self, query1: str, query2: str) -> bool:
        """Check if two queries are related."""
        # Simple word overlap check
        words1 = set(query1.lower().split())
        words2 = set(query2.lower().split())

        overlap = words1 & words2
        return len(overlap) >= 2

    def estimate_quality(self, entry_id: str, content: Optional[Dict] = None) -> QualityEstimate:
        """
        Estimate quality score for entry.

        Args:
            entry_id: Entry identifier
            content: Entry content (if None, will load from KB)

        Returns:
            QualityEstimate object
        """
        from kb_meta import MetadataManager

        manager = MetadataManager(self.kb_root)

        # Load content if not provided
        if content is None:
            # Find file with this entry
            all_meta = manager.get_all_entries_metadata()
            if entry_id not in all_meta:
                return QualityEstimate(
                    entry_id=entry_id,
                    estimated_score=0,
                    confidence=0.0,
                    strengths=[],
                    weaknesses=['Entry not found'],
                    improvements=[]
                )

            file_path = Path(all_meta[entry_id]['file'])
            import yaml
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)

            # Find entry in data
            content = None
            for key in ['errors', 'patterns']:
                if key in data:
                    for item in data[key]:
                        if item.get('id') == entry_id:
                            content = item
                            break
        else:
            data = content

        if not content:
            return QualityEstimate(
                entry_id=entry_id,
                estimated_score=0,
                confidence=0.0,
                strengths=[],
                weaknesses=['No content available'],
                improvements=[]
            )

        # Quality factors (simple heuristic)
        scores = {
            'title': 0,  # Has clear title
            'description': 0,  # Has description
            'examples': 0,  # Has code examples
            'context': 0,  # Has context/when to use
            'references': 0,  # Has references
        }

        strengths = []
        weaknesses = []
        improvements = []

        # Check for title
        if content.get('title'):
            scores['title'] = 20
            strengths.append("Has clear title")
        else:
            weaknesses.append("Missing title")

        # Check for description
        desc = content.get('description', '')
        if desc and len(desc) > 50:
            scores['description'] = 20
            strengths.append("Comprehensive description")
        elif desc:
            scores['description'] = 10
            improvements.append("Expand description")
        else:
            weaknesses.append("Missing description")

        # Check for examples
        examples = content.get('examples', [])
        if examples and len(examples) >= 2:
            scores['examples'] = 25
            strengths.append(f"Multiple examples ({len(examples)})")
        elif examples:
            scores['examples'] = 15
            improvements.append("Add more examples")
        else:
            weaknesses.append("No code examples")

        # Check for context
        if content.get('context') or content.get('when_to_use'):
            scores['context'] = 20
            strengths.append("Includes usage context")
        else:
            improvements.append("Add context/when to use")

        # Check for references
        if content.get('references') or content.get('links'):
            scores['references'] = 15
            strengths.append("Has references/links")
        else:
            improvements.append("Add references")

        # Calculate total score
        estimated_score = sum(scores.values())
        confidence = 0.7  # Moderate confidence for heuristic approach

        # Generate improvements
        if not weaknesses and not improvements:
            strengths.append("Well-structured entry")

        return QualityEstimate(
            entry_id=entry_id,
            estimated_score=estimated_score,
            confidence=confidence,
            strengths=strengths,
            weaknesses=weaknesses,
            improvements=improvements
        )

    def assess_risk(self, entry_id: str) -> RiskAssessment:
        """
        Assess risk of entry becoming stale.

        Args:
            entry_id: Entry identifier

        Returns:
            RiskAssessment object
        """
        from kb_meta import MetadataManager

        manager = MetadataManager(self.kb_root)
        all_meta = manager.get_all_entries_metadata()

        if entry_id not in all_meta:
            return RiskAssessment(
                entry_id=entry_id,
                risk_level='unknown',
                factors=['Entry not found in metadata'],
                probability=0.0,
                mitigation='Create metadata for entry'
            )

        meta = all_meta[entry_id]['metadata']

        factors = []
        risk_score = 0.0

        # Factor 1: Age
        created_at = meta.get('created_at')
        if created_at:
            try:
                created = datetime.fromisoformat(created_at)
                age_days = (datetime.now() - created).days

                if age_days > 365:
                    factors.append(f"Entry is {age_days // 30} months old")
                    risk_score += 0.3
                elif age_days > 180:
                    factors.append(f"Entry is {age_days // 30} months old")
                    risk_score += 0.2
            except:
                pass

        # Factor 2: Last analyzed
        last_analyzed = meta.get('last_analyzed_at')
        if last_analyzed:
            try:
                analyzed = datetime.fromisoformat(last_analyzed)
                days_since = (datetime.now() - analyzed).days

                if days_since > 180:
                    factors.append(f"Not analyzed for {days_since} days")
                    risk_score += 0.4
                elif days_since > 90:
                    factors.append(f"Not analyzed for {days_since} days")
                    risk_score += 0.2
            except:
                pass

        # Factor 3: Library dependencies
        tested_versions = meta.get('tested_versions', {})
        if tested_versions:
            factors.append(f"Depends on {len(tested_versions)} external libraries")
            risk_score += 0.1 * len(tested_versions)

        # Factor 4: Quality score
        quality = meta.get('quality_score')
        if quality is not None and quality < 75:
            factors.append(f"Quality score below threshold ({quality})")
            risk_score += 0.2

        # Determine risk level
        probability = min(risk_score, 1.0)

        if probability >= 0.7:
            risk_level = 'critical'
            mitigation = 'Immediate review and update required'
        elif probability >= 0.5:
            risk_level = 'high'
            mitigation = 'Schedule review within 1 week'
        elif probability >= 0.3:
            risk_level = 'medium'
            mitigation = 'Schedule review within 1 month'
        else:
            risk_level = 'low'
            mitigation = 'Regular monitoring sufficient'

        return RiskAssessment(
            entry_id=entry_id,
            risk_level=risk_level,
            factors=factors,
            probability=probability,
            mitigation=mitigation
        )

    def generate_predictions_report(self) -> str:
        """
        Generate comprehensive predictions report.

        Returns:
            Formatted report string
        """
        report = f"""
╔═══════════════════════════════════════════════════════════════╗
║              PREDICTIVE ANALYTICS REPORT                        ║
╚═══════════════════════════════════════════════════════════════╝

Generated: {datetime.now().isoformat()}

"""

        # Predict updates needed
        print("🔮 Predicting updates needed...")
        updates = self.predict_updates_needed()

        if updates:
            report += "🔄 PREDICTED UPDATES\n"
            report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            report += f"  {'Entry ID':40s} {'Prob.':>6s} {'Timeframe':>10s}\n"
            report += "  " + "-" * 60 + "\n"

            for pred in updates[:20]:
                report += f"  {pred.entry_id:40s} {pred.probability:>6.1%} {pred.timeframe:>10s}\n"
                if pred.reason:
                    report += f"    ↳ {pred.reason}\n"

            if len(updates) > 20:
                report += f"  ... and {len(updates) - 20} more\n"
            report += "\n"
        else:
            report += "✅ No updates predicted in near term\n\n"

        # Suggest new entries
        print("💡 Suggesting new entries...")
        suggestions = self.suggest_new_entries()

        if suggestions:
            report += "📝 SUGGESTED NEW ENTRIES\n"
            report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            report += f"  {'Title':40s} {'Priority':>10s} {'Searches':>8s} {'Conf.':>6s}\n"
            report += "  " + "-" * 70 + "\n"

            for sug in suggestions[:15]:
                report += f"  {sug.title:40s} {sug.priority:>10s} {sug.search_count:>8d} {sug.confidence:>6.1%}\n"

            if len(suggestions) > 15:
                report += f"  ... and {len(suggestions) - 15} more\n"
            report += "\n"

            # Priority breakdown
            priority_counts = {}
            for sug in suggestions:
                priority_counts[sug.priority] = priority_counts.get(sug.priority, 0) + 1

            report += "  Priority Breakdown:\n"
            for priority in ['critical', 'high', 'medium', 'low']:
                if priority in priority_counts:
                    report += f"    {priority:10s}: {priority_counts[priority]:>3d} entries\n"
            report += "\n"

        # Risk assessment
        print("⚠️  Assessing risks...")
        report += "⚠️  RISK ASSESSMENT\n"
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        from kb_meta import MetadataManager
        manager = MetadataManager(self.kb_root)
        all_meta = manager.get_all_entries_metadata()

        risk_levels = {'critical': [], 'high': [], 'medium': [], 'low': []}

        for entry_id in list(all_meta.keys())[:30]:  # Sample 30 entries
            risk = self.assess_risk(entry_id)
            risk_levels[risk.risk_level].append(risk)

        for level in ['critical', 'high', 'medium', 'low']:
            risks = risk_levels[level]
            if risks:
                report += f"\n  {level.upper()} ({len(risks)} entries):\n"
                for risk in risks[:5]:
                    report += f"    • {risk.entry_id}\n"
                    for factor in risk.factors[:2]:
                        report += f"      - {factor}\n"
                    report += f"      → {risk.mitigation}\n"

                if len(risks) > 5:
                    report += f"    ... and {len(risks) - 5} more\n"

        # Recommendations
        report += "\n💡 RECOMMENDATIONS\n"
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        critical_updates = [u for u in updates if u.timeframe == 'immediate']
        if critical_updates:
            report += "\n  IMMEDIATE ACTIONS:\n"
            for update in critical_updates[:3]:
                report += f"  • {update.entry_id}\n"
                report += f"    {update.suggested_action}\n"

        critical_gaps = [s for s in suggestions if s.priority == 'critical']
        if critical_gaps:
            report += "\n  NEW CONTENT TO CREATE:\n"
            for gap in critical_gaps[:3]:
                report += f"  • \"{gap.title}\"\n"
                report += f"    Priority: {gap.priority}, Confidence: {gap.confidence:.0%}\n"

        critical_risks = risk_levels['critical']
        if critical_risks:
            report += "\n  HIGH-RISK ENTRIES:\n"
            for risk in critical_risks[:3]:
                report += f"  • {risk.entry_id}\n"
                report += f"    {risk.mitigation}\n"

        report += "\n✅ End of Predictive Report\n"

        return report


def main():
    """CLI interface for predictive analytics."""
    import argparse

    parser = argparse.ArgumentParser(description="Predictive Analytics")
    parser.add_argument('action', choices=['predict-updates', 'suggest-entries',
                                          'estimate-quality', 'risk-assessment', 'report'],
                       help='Action to perform')
    parser.add_argument('--kb-root', type=Path,
                       help='Knowledge base root directory')
    parser.add_argument('--entry-id',
                       help='Entry ID (for specific actions)')
    parser.add_argument('--days', type=int, default=30,
                       help='Days to predict ahead (default: 30)')
    parser.add_argument('--min-gap-count', type=int, default=3,
                       help='Minimum gap count for suggestions (default: 3)')
    parser.add_argument('--output', type=Path,
                       help='Output file for report')

    args = parser.parse_args()

    analytics = PredictiveAnalytics(args.kb_root)

    if args.action == 'predict-updates':
        updates = analytics.predict_updates_needed(days_ahead=args.days)

        print(f"\n🔮 Predicted Updates (next {args.days} days)\n")
        for pred in updates:
            print(f"  {pred.entry_id}")
            print(f"    Probability: {pred.probability:.1%}")
            print(f"    Timeframe: {pred.timeframe}")
            print(f"    Reason: {pred.reason}")
            print(f"    Action: {pred.suggested_action}")
            print()

    elif args.action == 'suggest-entries':
        suggestions = analytics.suggest_new_entries(min_gap_count=args.min_gap_count)

        print(f"\n💡 Suggested New Entries\n")
        for sug in suggestions:
            print(f"  {sug.title}")
            print(f"    Priority: {sug.priority}")
            print(f"    Confidence: {sug.confidence:.1%}")
            print(f"    Search Count: {sug.search_count}")
            print(f"    Suggested Scope: {sug.suggested_scope}")
            if sug.related_queries:
                print(f"    Related: {', '.join(sug.related_queries)}")
            print()

    elif args.action == 'estimate-quality':
        if not args.entry_id:
            print("✗ --entry-id required for estimate-quality")
            return 1

        estimate = analytics.estimate_quality(args.entry_id)

        print(f"\n⭐ Quality Estimate for {args.entry_id}\n")
        print(f"  Estimated Score: {estimate.estimated_score}/100")
        print(f"  Confidence: {estimate.confidence:.1%}")
        print()
        print("  Strengths:")
        for strength in estimate.strengths:
            print(f"    ✓ {strength}")
        print()
        print("  Weaknesses:")
        for weakness in estimate.weaknesses:
            print(f"    ✗ {weakness}")
        print()
        print("  Suggested Improvements:")
        for improvement in estimate.improvements:
            print(f"    → {improvement}")
        print()

    elif args.action == 'risk-assessment':
        if not args.entry_id:
            # Assess all entries
            from kb_meta import MetadataManager
            manager = MetadataManager(args.kb_root)
            all_meta = manager.get_all_entries_metadata()

            print(f"\n⚠️  Risk Assessment\n")
            for entry_id in list(all_meta.keys())[:20]:  # First 20
                risk = analytics.assess_risk(entry_id)
                print(f"  {entry_id}")
                print(f"    Risk Level: {risk.risk_level.upper()} ({risk.probability:.1%})")
                if risk.factors:
                    print(f"    Factors: {', '.join(risk.factors[:2])}")
                print(f"    Mitigation: {risk.mitigation}")
                print()
        else:
            risk = analytics.assess_risk(args.entry_id)

            print(f"\n⚠️  Risk Assessment for {args.entry_id}\n")
            print(f"  Risk Level: {risk.risk_level.upper()}")
            print(f"  Probability: {risk.probability:.1%}")
            print()
            print("  Factors:")
            for factor in risk.factors:
                print(f"    • {factor}")
            print()
            print(f"  Mitigation: {risk.mitigation}")
            print()

    elif args.action == 'report':
        report = analytics.generate_predictions_report()

        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"✓ Report saved to: {args.output}")
        else:
            print(report)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
