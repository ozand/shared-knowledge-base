#!/usr/bin/env python3
"""
kb_patterns.py - Cross-Project Pattern Recognition

Identifies universal patterns across projects and scopes:
- Finds similar patterns in different contexts
- Suggests when to promote patterns to universal scope
- Extracts reusable patterns from specific implementations
- Links related patterns across domains

Usage:
    python tools/kb_patterns.py find-universal
    python tools/kb_patterns.py analyze-pattern [entry_id]
    python tools/kb_patterns.py suggest-promotions
    python tools/kb_patterns.py link-related

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

import yaml
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict
import re


@dataclass
class PatternSimilarity:
    """Similarity between two patterns."""
    entry_id_1: str
    entry_id_2: str
    similarity_score: float  # 0-1
    shared_keywords: Set[str]
    shared_examples: int
    relationship_type: str  # 'duplicate', 'variant', 'related'


@dataclass
class UniversalPatternCandidate:
    """Candidate for promotion to universal scope."""
    entry_id: str
    current_scope: str
    universality_score: float  # 0-1
    found_in_scopes: List[str]
    similar_patterns: List[str]
    recommendation: str  # 'promote', 'keep-as-is', 'merge'


@dataclass
class PatternAnalysis:
    """Analysis of a single pattern."""
    entry_id: str
    scope: str
    keywords: Set[str]
    category: str
    has_examples: bool
    example_count: int
    complexity_score: float  # 0-1
    reusability_score: float  # 0-1


class PatternRecognizer:
    """Recognize and analyze patterns across projects and scopes."""

    def __init__(self, kb_root: Optional[Path] = None):
        """
        Initialize PatternRecognizer.

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

        # Pattern cache
        self.patterns_file = self.cache_dir / "patterns.json"
        self.similarities_file = self.cache_dir / "pattern_similarities.json"

    def extract_keywords(self, text: str) -> Set[str]:
        """
        Extract keywords from text.

        Args:
            text: Text to extract from

        Returns:
            Set of keywords
        """
        # Common technical terms to look for
        technical_terms = {
            'api', 'rest', 'graphql', 'database', 'sql', 'nosql',
            'cache', 'redis', 'async', 'await', 'promise', 'callback',
            'authentication', 'authorization', 'oauth', 'jwt', 'session',
            'deployment', 'docker', 'kubernetes', 'container', 'microservice',
            'testing', 'unit', 'integration', 'e2e', 'mock', 'stub',
            'frontend', 'backend', 'fullstack', 'middleware', 'proxy',
            'error', 'exception', 'handling', 'validation', 'sanitization',
            'security', 'encryption', 'hashing', 'salting', 'csrf', 'xss',
            'performance', 'optimization', 'latency', 'throughput', 'scalability',
            'architecture', 'pattern', 'design', 'structure', 'layer', 'component'
        }

        # Extract words
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())

        # Filter to technical terms and common words
        keywords = set()
        for word in words:
            if word in technical_terms or len(word) > 6:
                keywords.add(word)

        return keywords

    def analyze_pattern(self, entry_id: str, content: Optional[Dict] = None) -> PatternAnalysis:
        """
        Analyze a single pattern.

        Args:
            entry_id: Entry identifier
            content: Entry content (optional)

        Returns:
            PatternAnalysis object
        """
        from kb_meta import MetadataManager

        manager = MetadataManager(self.kb_root)

        # Load content if not provided
        if content is None:
            all_meta = manager.get_all_entries_metadata()
            if entry_id not in all_meta:
                return None

            file_path = Path(all_meta[entry_id]['file'])
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
            return None

        # Get metadata
        all_meta = manager.get_all_entries_metadata()
        meta = all_meta.get(entry_id, {}).get('metadata', {})
        scope = meta.get('scope', 'unknown')

        # Extract keywords from title, description, and content
        text_parts = [
            content.get('title', ''),
            content.get('description', ''),
            content.get('context', ''),
            str(content.get('examples', []))
        ]

        all_text = ' '.join(text_parts)
        keywords = self.extract_keywords(all_text)

        # Determine category
        category = self._determine_category(content)

        # Check for examples
        examples = content.get('examples', [])
        has_examples = len(examples) > 0
        example_count = len(examples)

        # Calculate complexity score
        complexity_score = self._calculate_complexity(content)

        # Calculate reusability score
        reusability_score = self._calculate_reusability(content, keywords, examples)

        return PatternAnalysis(
            entry_id=entry_id,
            scope=scope,
            keywords=keywords,
            category=category,
            has_examples=has_examples,
            example_count=example_count,
            complexity_score=complexity_score,
            reusability_score=reusability_score
        )

    def _determine_category(self, content: Dict) -> str:
        """Determine category of pattern."""
        title = content.get('title', '').lower()
        description = content.get('description', '').lower()

        # Check for error/pattern indicators
        if 'error' in title or 'exception' in title or 'failure' in title:
            return 'error'
        elif 'pattern' in title or 'design' in title:
            return 'design'
        elif 'architecture' in title or 'structure' in title:
            return 'architecture'
        elif 'security' in title or 'auth' in title:
            return 'security'
        elif 'performance' in title or 'optimization' in title:
            return 'performance'
        elif 'testing' in title or 'test' in title:
            return 'testing'
        else:
            return 'general'

    def _calculate_complexity(self, content: Dict) -> float:
        """Calculate complexity score (0-1)."""
        factors = 0
        max_factors = 10

        # Length of description
        desc = content.get('description', '')
        if len(desc) > 500:
            factors += 2
        elif len(desc) > 200:
            factors += 1

        # Number of examples
        examples = content.get('examples', [])
        if len(examples) >= 3:
            factors += 3
        elif len(examples) >= 1:
            factors += 1

        # Has context or references
        if content.get('context'):
            factors += 2
        if content.get('references') or content.get('links'):
            factors += 2

        # Code blocks in examples
        code_blocks = 0
        for example in examples:
            if isinstance(example, dict):
                if 'code' in example:
                    code_blocks += 1
            elif isinstance(example, str):
                if '```' in example or 'def ' in example or 'function' in example:
                    code_blocks += 1

        if code_blocks >= 3:
            factors += 3
        elif code_blocks >= 1:
            factors += 1

        return factors / max_factors

    def _calculate_reusability(self, content: Dict, keywords: Set[str], examples: List) -> float:
        """Calculate reusability score (0-1)."""
        factors = 0
        max_factors = 8

        # Has clear title and description
        if content.get('title'):
            factors += 1
        if content.get('description') and len(content.get('description', '')) > 100:
            factors += 1

        # Has examples
        if len(examples) > 0:
            factors += 2

        # Has context
        if content.get('context') or content.get('when_to_use'):
            factors += 2

        # Generic keywords (not specific to one technology)
        generic_keywords = {'pattern', 'design', 'architecture', 'structure',
                          'error', 'handling', 'testing', 'validation'}
        if any(kw in keywords for kw in generic_keywords):
            factors += 2

        return factors / max_factors

    def find_similar_patterns(self, min_similarity: float = 0.3) -> List[PatternSimilarity]:
        """
        Find similar patterns across the knowledge base.

        Args:
            min_similarity: Minimum similarity score (0-1)

        Returns:
            List of PatternSimilarity objects
        """
        from kb_meta import MetadataManager

        manager = MetadataManager(self.kb_root)
        all_meta = manager.get_all_entries_metadata()

        # Analyze all patterns
        analyses = {}
        for entry_id in list(all_meta.keys())[:50]:  # Limit to 50 for performance
            analysis = self.analyze_pattern(entry_id)
            if analysis:
                analyses[entry_id] = analysis

        # Compare all pairs
        similarities = []
        entry_ids = list(analyses.keys())

        for i in range(len(entry_ids)):
            for j in range(i + 1, len(entry_ids)):
                id1, id2 = entry_ids[i], entry_ids[j]
                analysis1 = analyses[id1]
                analysis2 = analyses[id2]

                # Calculate similarity
                similarity = self._calculate_similarity(analysis1, analysis2)

                if similarity >= min_similarity:
                    shared_keywords = analysis1.keywords & analysis2.keywords
                    shared_examples = min(analysis1.example_count, analysis2.example_count)

                    # Determine relationship type
                    if similarity > 0.8:
                        relationship = 'duplicate'
                    elif similarity > 0.5:
                        relationship = 'variant'
                    else:
                        relationship = 'related'

                    similarities.append(PatternSimilarity(
                        entry_id_1=id1,
                        entry_id_2=id2,
                        similarity_score=similarity,
                        shared_keywords=shared_keywords,
                        shared_examples=shared_examples,
                        relationship_type=relationship
                    ))

        # Sort by similarity
        similarities.sort(key=lambda s: s.similarity_score, reverse=True)

        return similarities

    def _calculate_similarity(self, analysis1: PatternAnalysis, analysis2: PatternAnalysis) -> float:
        """Calculate similarity score between two patterns."""
        score = 0.0

        # Keyword overlap (40% weight)
        if analysis1.keywords and analysis2.keywords:
            keyword_overlap = len(analysis1.keywords & analysis2.keywords)
            keyword_union = len(analysis1.keywords | analysis2.keywords)
            if keyword_union > 0:
                score += (keyword_overlap / keyword_union) * 0.4

        # Category match (20% weight)
        if analysis1.category == analysis2.category:
            score += 0.2

        # Same scope? (10% weight)
        if analysis1.scope == analysis2.scope:
            score += 0.1

        # Complexity similarity (15% weight)
        complexity_diff = abs(analysis1.complexity_score - analysis2.complexity_score)
        score += (1 - complexity_diff) * 0.15

        # Reusability similarity (15% weight)
        reusability_diff = abs(analysis1.reusability_score - analysis2.reusability_score)
        score += (1 - reusability_diff) * 0.15

        return min(score, 1.0)

    def find_universal_candidates(self) -> List[UniversalPatternCandidate]:
        """
        Find patterns that should be promoted to universal scope.

        Returns:
            List of UniversalPatternCandidate objects
        """
        from kb_meta import MetadataManager

        manager = MetadataManager(self.kb_root)
        all_meta = manager.get_all_entries_metadata()

        # Group by scope
        scope_entries = defaultdict(list)
        for entry_id, data in all_meta.items():
            scope = data['metadata'].get('scope', 'unknown')
            if scope != 'universal':
                scope_entries[scope].append(entry_id)

        candidates = []

        # For each non-universal entry, check if similar patterns exist in other scopes
        for scope, entry_ids in scope_entries.items():
            for entry_id in entry_ids:
                analysis = self.analyze_pattern(entry_id)
                if not analysis:
                    continue

                # Find similar patterns in other scopes
                found_in_scopes = [scope]
                similar_patterns = []

                for other_scope, other_ids in scope_entries.items():
                    if other_scope == scope:
                        continue

                    for other_id in other_ids:
                        other_analysis = self.analyze_pattern(other_id)
                        if not other_analysis:
                            continue

                        similarity = self._calculate_similarity(analysis, other_analysis)

                        if similarity > 0.5:
                            found_in_scopes.append(other_scope)
                            similar_patterns.append(other_id)

                # Calculate universality score
                universality_score = len(set(found_in_scopes)) / len(scope_entries)

                # Generate recommendation
                if universality_score > 0.5 and analysis.reusability_score > 0.7:
                    recommendation = 'promote'
                elif universality_score > 0.3 and len(similar_patterns) > 2:
                    recommendation = 'merge'
                else:
                    recommendation = 'keep-as-is'

                if recommendation != 'keep-as-is':
                    candidates.append(UniversalPatternCandidate(
                        entry_id=entry_id,
                        current_scope=scope,
                        universality_score=universality_score,
                        found_in_scopes=list(set(found_in_scopes)),
                        similar_patterns=similar_patterns,
                        recommendation=recommendation
                    ))

        # Sort by universality score
        candidates.sort(key=lambda c: c.universality_score, reverse=True)

        return candidates

    def generate_patterns_report(self) -> str:
        """
        Generate comprehensive patterns report.

        Returns:
            Formatted report string
        """
        report = f"""
╔═══════════════════════════════════════════════════════════════╗
║            CROSS-PROJECT PATTERN RECOGNITION REPORT             ║
╚═══════════════════════════════════════════════════════════════╝

Generated: {datetime.now().isoformat()}

"""

        # Find similar patterns
        print("🔍 Finding similar patterns...")
        similarities = self.find_similar_patterns(min_similarity=0.4)

        if similarities:
            report += "🔗 SIMILAR PATTERNS\n"
            report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

            # Group by relationship type
            duplicates = [s for s in similarities if s.relationship_type == 'duplicate']
            variants = [s for s in similarities if s.relationship_type == 'variant']
            related = [s for s in similarities if s.relationship_type == 'related']

            if duplicates:
                report += f"\n  Potential Duplicates ({len(duplicates)}):\n"
                for sim in duplicates[:10]:
                    report += f"    • {sim.entry_id_1} ↔ {sim.entry_id_2}\n"
                    report += f"      Similarity: {sim.similarity_score:.1%}\n"
                    report += f"      Shared keywords: {', '.join(list(sim.shared_keywords)[:5])}\n"
                    if len(duplicates) > 10:
                        report += f"    ... and {len(duplicates) - 10} more\n"
                        break

            if variants:
                report += f"\n  Pattern Variants ({len(variants)}):\n"
                for sim in variants[:10]:
                    report += f"    • {sim.entry_id_1} ↔ {sim.entry_id_2}\n"
                    report += f"      Similarity: {sim.similarity_score:.1%}\n"
                    if len(variants) > 10:
                        report += f"    ... and {len(variants) - 10} more\n"
                        break

            if related:
                report += f"\n  Related Patterns ({len(related)}):\n"
                for sim in related[:5]:
                    report += f"    • {sim.entry_id_1} → {sim.entry_id_2}\n"
                    report += f"      Similarity: {sim.similarity_score:.1%}\n"
                if len(related) > 5:
                    report += f"    ... and {len(related) - 5} more\n"

            report += "\n"

        # Find universal candidates
        print("🌟 Finding universal pattern candidates...")
        candidates = self.find_universal_candidates()

        if candidates:
            report += "🌟 UNIVERSAL PATTERN CANDIDATES\n"
            report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

            # Group by recommendation
            to_promote = [c for c in candidates if c.recommendation == 'promote']
            to_merge = [c for c in candidates if c.recommendation == 'merge']

            if to_promote:
                report += f"\n  Recommended for Promotion ({len(to_promote)}):\n"
                for cand in to_promote[:10]:
                    report += f"    • {cand.entry_id}\n"
                    report += f"      Current: {cand.current_scope}\n"
                    report += f"      Found in: {', '.join(cand.found_in_scopes)}\n"
                    report += f"      Universality: {cand.universality_score:.1%}\n"
                    report += f"      Similar patterns: {len(cand.similar_patterns)}\n"
                if len(to_promote) > 10:
                    report += f"    ... and {len(to_promote) - 10} more\n"

            if to_merge:
                report += f"\n  Candidates for Merging ({len(to_merge)}):\n"
                for cand in to_merge[:10]:
                    report += f"    • {cand.entry_id}\n"
                    report += f"      Current: {cand.current_scope}\n"
                    report += f"      Similar patterns: {', '.join(cand.similar_patterns[:5])}\n"
                    report += f"      Found in: {', '.join(cand.found_in_scopes)}\n"
                if len(to_merge) > 10:
                    report += f"    ... and {len(to_merge) - 10} more\n"

            report += "\n"

        # Recommendations
        report += "💡 RECOMMENDATIONS\n"
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

        if similarities:
            duplicates = [s for s in similarities if s.relationship_type == 'duplicate']
            if duplicates:
                report += "\n  1. Review Potential Duplicates:\n"
                report += "     The following patterns may be duplicates:\n"
                for sim in duplicates[:3]:
                    report += f"     • {sim.entry_id_1} and {sim.entry_id_2}\n"
                    report += f"       Consider merging or clarifying differences\n"

        if candidates:
            to_promote = [c for c in candidates if c.recommendation == 'promote']
            if to_promote:
                report += "\n  2. Promote Universal Patterns:\n"
                report += "     The following patterns are used across multiple scopes:\n"
                for cand in to_promote[:3]:
                    report += f"     • {cand.entry_id}\n"
                    report += f"       Move from {cand.current_scope} to universal\n"

            to_merge = [c for c in candidates if c.recommendation == 'merge']
            if to_merge:
                report += "\n  3. Merge Similar Patterns:\n"
                report += "     The following patterns could be consolidated:\n"
                for cand in to_merge[:2]:
                    report += f"     • {cand.entry_id}\n"
                    report += f"       Similar to: {', '.join(cand.similar_patterns[:3])}\n"

        report += "\n✅ End of Pattern Recognition Report\n"

        return report


def main():
    """CLI interface for pattern recognition."""
    import argparse

    parser = argparse.ArgumentParser(description="Cross-Project Pattern Recognition")
    parser.add_argument('action', choices=['find-universal', 'analyze-pattern',
                                          'suggest-promotions', 'link-related', 'report'],
                       help='Action to perform')
    parser.add_argument('--kb-root', type=Path,
                       help='Knowledge base root directory')
    parser.add_argument('--entry-id',
                       help='Entry ID (for specific actions)')
    parser.add_argument('--min-similarity', type=float, default=0.4,
                       help='Minimum similarity score (default: 0.4)')
    parser.add_argument('--output', type=Path,
                       help='Output file for report')

    args = parser.parse_args()

    recognizer = PatternRecognizer(args.kb_root)

    if args.action == 'find-universal':
        candidates = recognizer.find_universal_candidates()

        print(f"\n🌟 Universal Pattern Candidates\n")
        for cand in candidates:
            print(f"  {cand.entry_id}")
            print(f"    Current Scope: {cand.current_scope}")
            print(f"    Universality Score: {cand.universality_score:.1%}")
            print(f"    Found In: {', '.join(cand.found_in_scopes)}")
            print(f"    Recommendation: {cand.recommendation}")
            if cand.similar_patterns:
                print(f"    Similar Patterns: {', '.join(cand.similar_patterns[:5])}")
            print()

    elif args.action == 'analyze-pattern':
        if not args.entry_id:
            print("✗ --entry-id required for analyze-pattern")
            return 1

        analysis = recognizer.analyze_pattern(args.entry_id)

        if not analysis:
            print(f"✗ Pattern {args.entry_id} not found")
            return 1

        print(f"\n📊 Pattern Analysis: {args.entry_id}\n")
        print(f"  Scope: {analysis.scope}")
        print(f"  Category: {analysis.category}")
        print(f"  Has Examples: {analysis.has_examples} ({analysis.example_count})")
        print(f"  Complexity Score: {analysis.complexity_score:.2f}/1.0")
        print(f"  Reusability Score: {analysis.reusability_score:.2f}/1.0")
        print()
        print(f"  Keywords ({len(analysis.keywords)}):")
        print(f"    {', '.join(sorted(analysis.keywords))}")
        print()

    elif args.action == 'suggest-promotions':
        candidates = recognizer.find_universal_candidates()
        to_promote = [c for c in candidates if c.recommendation == 'promote']

        print(f"\n🌟 Patterns to Promote to Universal ({len(to_promote)})\n")
        for cand in to_promote:
            print(f"  {cand.entry_id}")
            print(f"    From: {cand.current_scope}")
            print(f"    Universality: {cand.universality_score:.1%}")
            print(f"    Found in: {', '.join(cand.found_in_scopes)}")
            print()

    elif args.action == 'link-related':
        similarities = recognizer.find_similar_patterns(min_similarity=args.min_similarity)

        print(f"\n🔗 Related Patterns (similarity ≥ {args.min_similarity})\n")
        for sim in similarities[:20]:
            print(f"  {sim.entry_id_1} ↔ {sim.entry_id_2}")
            print(f"    Similarity: {sim.similarity_score:.1%}")
            print(f"    Type: {sim.relationship_type}")
            if sim.shared_keywords:
                print(f"    Shared: {', '.join(list(sim.shared_keywords)[:5])}")
            print()

    elif args.action == 'report':
        report = recognizer.generate_patterns_report()

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
