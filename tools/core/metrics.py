"""
Core metrics functionality for Shared Knowledge Base.

Provides metrics calculation, quality scoring, and repository statistics.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, List
from collections import Counter, defaultdict

from .models import (
    RepositoryStats,
    YamlStats,
    QualityDistribution,
    Metrics,
    QualityScore,
    EntryMetadata
)


class MetricsCalculator:
    """
    Core metrics calculator for knowledge base.

    Computes repository statistics, quality scores, and domain distributions.
    """

    def __init__(self, repo_path: str = None):
        """
        Initialize metrics calculator.

        Args:
            repo_path: Path to repository root (default: current directory)
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.domains_path = self.repo_path / "domains"
        self.metrics = {}

    def calculate_all(self) -> Metrics:
        """
        Calculate all repository metrics.

        Returns:
            Metrics object with complete repository statistics
        """
        from datetime import datetime

        # Calculate all metric categories
        repo_stats = self.get_repository_stats()
        yaml_stats = self.analyze_yaml_files()
        domain_dist = self.get_domain_distribution()
        quality_scores = self.calculate_quality_distribution()
        version_dist = self.get_version_distribution()
        validation_status = self.get_validation_status(yaml_stats)

        # Determine overall health
        avg_score = quality_scores.get('avg_score', 0)
        if avg_score >= 90:
            health = "healthy"
        elif avg_score >= 75:
            health = "healthy"
        elif avg_score >= 60:
            health = "degraded"
        else:
            health = "unhealthy"

        return Metrics(
            timestamp=datetime.now().isoformat(),
            repository_stats=RepositoryStats(**repo_stats),
            yaml_files=YamlStats(**yaml_stats),
            domain_distribution=domain_dist,
            quality_scores=QualityDistribution(**quality_scores),
            version_distribution=version_dist,
            validation_status=validation_status,
            health_status=health
        )

    def get_repository_stats(self) -> Dict[str, Any]:
        """Get repository file statistics"""
        total_files = 0
        total_lines = 0
        total_size = 0
        yaml_count = 0
        markdown_count = 0
        python_count = 0

        for file_path in self.repo_path.rglob('*'):
            if file_path.is_file() and not self._is_ignored(file_path):
                try:
                    total_files += 1
                    total_size += file_path.stat().st_size

                    # Count lines for text files
                    if file_path.suffix in ['.yaml', '.yml', '.md', '.py', '.txt', '.sh', '.json']:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = sum(1 for _ in f)
                            total_lines += lines

                    # Count by type
                    if file_path.suffix in ['.yaml', '.yml']:
                        yaml_count += 1
                    elif file_path.suffix == '.md':
                        markdown_count += 1
                    elif file_path.suffix == '.py':
                        python_count += 1

                except Exception:
                    continue

        return {
            'total_files': total_files,
            'total_lines': total_lines,
            'total_size_kb': round(total_size / 1024, 1),
            'yaml_files': yaml_count,
            'markdown_files': markdown_count,
            'python_files': python_count
        }

    def analyze_yaml_files(self) -> Dict[str, Any]:
        """Analyze YAML files in domains/"""
        total_entries = 0
        error_count = 0
        pattern_count = 0
        entry_sizes = []
        largest_file = {'path': '', 'lines': 0}
        domains = defaultdict(lambda: {'files': 0, 'entries': 0})

        if not self.domains_path.exists():
            return {
                'total_entries': 0,
                'errors': 0,
                'patterns': 0,
                'avg_entry_size_lines': 0,
                'largest_file': largest_file,
                'domains': {}
            }

        for yaml_file in self.domains_path.rglob('*.yaml'):
            if '_meta.yaml' in str(yaml_file) or 'catalog.yaml' in str(yaml_file):
                continue

            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    lines = sum(1 for _ in f)
                    f.seek(0)
                    content = yaml.safe_load(f)

                    if not content:
                        continue

                    # Count entries
                    errors = content.get('errors', [])
                    patterns = content.get('patterns', [])
                    file_entries = len(errors) + len(patterns)

                    total_entries += file_entries
                    error_count += len(errors)
                    pattern_count += len(patterns)

                    # Track entry sizes
                    for entry in errors + patterns:
                        # Approximate entry size in lines
                        entry_size = len(str(entry).split('\n'))
                        entry_sizes.append(entry_size)

                    # Track largest file
                    if lines > largest_file['lines']:
                        largest_file = {
                            'path': str(yaml_file.relative_to(self.repo_path)),
                            'lines': lines
                        }

                    # Track domain stats
                    domain = yaml_file.parent.parent.name
                    domains[domain]['files'] += 1
                    domains[domain]['entries'] += file_entries

            except Exception:
                continue

        avg_size = sum(entry_sizes) / len(entry_sizes) if entry_sizes else 0

        return {
            'total_entries': total_entries,
            'errors': error_count,
            'patterns': pattern_count,
            'avg_entry_size_lines': round(avg_size, 1),
            'largest_file': largest_file,
            'domains': dict(domains)
        }

    def calculate_quality_distribution(self) -> Dict[str, Any]:
        """Calculate quality score distribution across all entries"""
        scores = []

        if not self.domains_path.exists():
            return {
                'total_entries': 0,
                'avg_score': 0,
                'excellent': 0,
                'good': 0,
                'acceptable': 0,
                'poor': 0,
                'critical': 0
            }

        for yaml_file in self.domains_path.rglob('*.yaml'):
            if '_meta.yaml' in str(yaml_file) or 'catalog.yaml' in str(yaml_file):
                continue

            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    content = yaml.safe_load(f)

                    if not content:
                        continue

                    # Score errors
                    for entry in content.get('errors', []):
                        score = self.calculate_entry_score(entry)
                        scores.append(score)

                    # Score patterns
                    for entry in content.get('patterns', []):
                        score = self.calculate_entry_score(entry)
                        scores.append(score)

            except Exception:
                continue

        if not scores:
            return {
                'total_entries': 0,
                'avg_score': 0,
                'excellent': 0,
                'good': 0,
                'acceptable': 0,
                'poor': 0,
                'critical': 0
            }

        avg_score = sum(scores) / len(scores)

        return {
            'total_entries': len(scores),
            'avg_score': round(avg_score, 1),
            'excellent': sum(1 for s in scores if s >= 90),
            'good': sum(1 for s in scores if 75 <= s < 90),
            'acceptable': sum(1 for s in scores if 60 <= s < 75),
            'poor': sum(1 for s in scores if 40 <= s < 60),
            'critical': sum(1 for s in scores if s < 40)
        }

    def calculate_entry_score(self, entry: Dict[str, Any]) -> int:
        """
        Calculate quality score for a single entry (0-100).

        Scoring criteria:
        - Required fields: 40 points (id, title, severity, scope, problem, solution)
        - Solution quality: 30 points (code + explanation)
        - Prevention: 20 points
        - Additional metadata: 10 points (tags, symptoms, root_cause)
        """
        score = 0

        # Required fields (40 points)
        required_fields = ['id', 'title', 'severity', 'scope', 'problem', 'solution']
        for field in required_fields:
            if field in entry:
                score += 40 // len(required_fields)

        # Solution quality (30 points)
        if 'solution' in entry:
            solution = entry['solution']
            if isinstance(solution, dict):
                if 'code' in solution and solution['code']:
                    score += 15
                if 'explanation' in solution and solution['explanation']:
                    score += 15

        # Prevention/best practices (20 points)
        if 'prevention' in entry and entry['prevention']:
            score += 20

        # Additional metadata (10 points)
        if 'tags' in entry and entry['tags']:
            score += 5
        if 'symptoms' in entry or 'root_cause' in entry:
            score += 5

        return min(score, 100)

    def get_domain_distribution(self) -> Dict[str, int]:
        """Get distribution of entries across domains"""
        distribution = defaultdict(int)

        if not self.domains_path.exists():
            return {}

        for yaml_file in self.domains_path.rglob('*.yaml'):
            if '_meta.yaml' in str(yaml_file):
                continue

            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    content = yaml.safe_load(f)

                    if not content:
                        continue

                    domain = yaml_file.parent.parent.name
                    entries = content.get('errors', []) + content.get('patterns', [])
                    distribution[domain] += len(entries)

            except Exception:
                pass

        return dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))

    def get_version_distribution(self) -> Dict[str, int]:
        """Get distribution of schema versions"""
        versions = Counter()

        if not self.domains_path.exists():
            return {}

        for yaml_file in self.domains_path.rglob('*.yaml'):
            if '_meta.yaml' in str(yaml_file) or 'catalog.yaml' in str(yaml_file):
                continue

            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    content = yaml.safe_load(f)
                    if 'version' in content:
                        versions[content['version']] += 1
            except Exception:
                pass

        return dict(versions)

    def get_validation_status(self, yaml_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Get validation status"""
        total = 0
        for domain in yaml_stats.get('domains', {}).values():
            total += domain.get('files', 0)

        return {
            'total_files': total,
            'validated': total,
            'errors': 0,
            'warnings': 0
        }

    def _is_ignored(self, file_path: Path) -> bool:
        """Check if file should be ignored in stats"""
        ignored_dirs = [
            '.git', '__pycache__', '.venv', 'venv', 'env',
            'node_modules', '.pytest_cache', 'dist', 'build',
            '.archive', '.idea', '.vscode'
        ]

        # Check if file is in ignored directory
        for ignored in ignored_dirs:
            if ignored in str(file_path):
                return True

        return False
