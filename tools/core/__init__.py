"""
Shared Knowledge Base - Core Module

This module provides core functionality for knowledge base operations,
including search, validation, and metrics calculation. It is designed to be
used by CLI tools, MCP server, and future API interfaces.

Classes:
    KnowledgeSearch: Search knowledge entries with filters
    MetricsCalculator: Calculate repository metrics and quality scores
    KnowledgeValidator: Validate YAML files and entries

Example:
    >>> from tools.core import KnowledgeSearch, MetricsCalculator
    >>>
    >>> # Search for entries
    >>> search = KnowledgeSearch()
    >>> results = search.search("docker compose", scope="docker")
    >>> print(f"Found {results.total} entries")
    >>>
    >>> # Calculate metrics
    >>> metrics = MetricsCalculator()
    >>> repo_metrics = metrics.calculate_all()
    >>> print(f"Average quality: {repo_metrics.quality_scores.avg_score}/100")
"""

from .search import KnowledgeSearch
from .metrics import MetricsCalculator
from .validation import KnowledgeValidator
from .models import (
    # Search models
    SearchFilter,
    SearchResult,
    SearchResults,
    EntryMetadata,
    # Metrics models
    QualityScore,
    RepositoryStats,
    YamlStats,
    QualityDistribution,
    Metrics,
    # Validation models
    ValidationError,
    ValidationResult,
    # Health models
    HealthStatus
)

__all__ = [
    # Main classes
    'KnowledgeSearch',
    'MetricsCalculator',
    'KnowledgeValidator',
    # Search models
    'SearchFilter',
    'SearchResult',
    'SearchResults',
    'EntryMetadata',
    # Metrics models
    'QualityScore',
    'RepositoryStats',
    'YamlStats',
    'QualityDistribution',
    'Metrics',
    # Validation models
    'ValidationError',
    'ValidationResult',
    # Health models
    'HealthStatus'
]

__version__ = '1.0.0'
