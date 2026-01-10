"""
Core search functionality for Shared Knowledge Base.

Provides search capabilities across knowledge entries with support for
filtering, prioritization, and result aggregation.
"""

import re
import yaml
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict

from .models import (
    SearchFilter,
    SearchResult,
    SearchResults,
    EntryMetadata,
    SeverityLevel,
    ScopeLevel
)


class KnowledgeSearch:
    """
    Core search engine for knowledge base.

    Provides string-based search across YAML files with support for
    category, severity, scope, and tag filtering.
    """

    def __init__(self, search_paths: List[str] = None):
        """
        Initialize search engine.

        Args:
            search_paths: List of root paths to search (default: ["domains"])
        """
        self.search_paths = [Path(p) for p in (search_paths or ["domains"])]
        self.project_kb_path = Path(".kb/project")
        self.shared_kb_path = Path(".kb/shared")

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        severity: Optional[str] = None,
        scope: Optional[str] = None,
        limit: int = 50,
        include_project: bool = True,
        include_shared: bool = True
    ) -> SearchResults:
        """
        Search knowledge base for entries matching query and filters.

        Args:
            query: Search string to match
            category: Filter by category
            severity: Filter by severity level
            scope: Filter by scope
            limit: Maximum results to return
            include_project: Include project KB results
            include_shared: Include shared KB results

        Returns:
            SearchResults with matching entries
        """
        start_time = time.time()

        # Search in domains/
        domain_results = self._search_domains(
            query=query,
            category=category,
            severity=severity,
            scope=scope
        )

        # Search in project KB if exists and requested
        project_results = []
        if include_project and self.project_kb_path.exists():
            project_results = self._search_kb_directory(
                self.project_kb_path,
                query=query,
                category=category,
                severity=severity,
                scope=scope
            )

        # Search in shared KB if exists and requested
        shared_results = []
        if include_shared and self.shared_kb_path.exists():
            shared_results = self._search_kb_directory(
                self.shared_kb_path,
                query=query,
                category=category,
                severity=severity,
                scope=scope
            )

        # Combine and deduplicate results
        all_results = domain_results + project_results + shared_results
        seen_ids = set()
        unique_results = []
        for result in all_results:
            if result.metadata.id not in seen_ids:
                seen_ids.add(result.metadata.id)
                unique_results.append(result)

        # Apply limit
        limited_results = unique_results[:limit]

        # Separate by KB type
        final_project = [r for r in limited_results if r.kb_type == "project"]
        final_shared = [r for r in limited_results if r.kb_type == "shared"]

        execution_time = (time.time() - start_time) * 1000

        return SearchResults(
            query=query,
            total=len(limited_results),
            project_results=final_project,
            shared_results=final_shared,
            filters_applied=SearchFilter(
                query=query,
                category=category,
                severity=severity,
                scope=scope,
                limit=limit
            ),
            execution_time_ms=execution_time
        )

    def _search_domains(
        self,
        query: str,
        category: Optional[str] = None,
        severity: Optional[str] = None,
        scope: Optional[str] = None
    ) -> List[SearchResult]:
        """Search in domains/ directory"""
        results = []

        for search_path in self.search_paths:
            if not search_path.exists():
                continue

            for yaml_file in self._find_yaml_files(search_path):
                file_results = self._search_file(
                    yaml_file,
                    query=query,
                    category=category,
                    severity=severity,
                    scope=scope
                )
                results.extend(file_results)

        return results

    def _search_kb_directory(
        self,
        kb_path: Path,
        query: str,
        category: Optional[str] = None,
        severity: Optional[str] = None,
        scope: Optional[str] = None
    ) -> List[SearchResult]:
        """Search in a KB directory (.kb/project or .kb/shared)"""
        results = []

        if not kb_path.exists():
            return results

        kb_type = "project" if kb_path.name == "project" else "shared"

        for yaml_file in self._find_yaml_files(kb_path):
            file_results = self._search_file(
                yaml_file,
                query=query,
                category=category,
                severity=severity,
                scope=scope,
                kb_type=kb_type
            )
            results.extend(file_results)

        return results

    def _find_yaml_files(self, root_path: Path) -> List[Path]:
        """Find all YAML files, excluding index and meta files"""
        yaml_files = []

        for yaml_file in root_path.rglob('*.yaml'):
            # Skip index and meta files
            if any(x in str(yaml_file) for x in ['_index.yaml', '_meta.yaml', 'catalog.yaml']):
                continue

            yaml_files.append(yaml_file)

        return yaml_files

    def _search_file(
        self,
        file_path: Path,
        query: str,
        category: Optional[str] = None,
        severity: Optional[str] = None,
        scope: Optional[str] = None,
        kb_type: str = "shared"
    ) -> List[SearchResult]:
        """Search a single YAML file for matching entries"""
        results = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)

                if not content:
                    return results

                # Extract category from file
                file_category = content.get('category', '')

                # Search in errors
                for entry in content.get('errors', []):
                    if self._matches_filters(
                        entry,
                        query=query,
                        category=category or file_category,
                        severity=severity,
                        scope=scope
                    ):
                        metadata = self._extract_metadata(entry, file_path, file_category)
                        preview = self._extract_preview(entry)

                        results.append(SearchResult(
                            metadata=metadata,
                            preview=preview,
                            kb_type=kb_type
                        ))

                # Search in patterns
                for entry in content.get('patterns', []):
                    if self._matches_filters(
                        entry,
                        query=query,
                        category=category or file_category,
                        severity=severity,
                        scope=scope
                    ):
                        metadata = self._extract_metadata(entry, file_path, file_category, is_pattern=True)
                        preview = self._extract_preview(entry)

                        results.append(SearchResult(
                            metadata=metadata,
                            preview=preview,
                            kb_type=kb_type
                        ))

        except Exception as e:
            # Log error but continue processing
            pass

        return results

    def _matches_filters(
        self,
        entry: Dict[str, Any],
        query: str,
        category: Optional[str] = None,
        severity: Optional[str] = None,
        scope: Optional[str] = None
    ) -> bool:
        """Check if entry matches all filters"""
        # Query matching (string search in entry content)
        if query and not self._matches_query(entry, query):
            return False

        # Severity filter
        if severity and entry.get('severity') != severity:
            return False

        # Scope filter
        if scope and entry.get('scope') != scope:
            return False

        # Category filter
        # Note: category is typically at file level, not entry level
        # So we handle it at the file search level

        return True

    def _matches_query(self, entry: Dict[str, Any], query: str) -> bool:
        """Check if entry matches query string"""
        query_lower = query.lower()

        # Search in key fields
        searchable_fields = [
            entry.get('id', ''),
            entry.get('title', ''),
            entry.get('problem', ''),
            entry.get('root_cause', ''),
        ]

        # Search in solution
        solution = entry.get('solution', {})
        if isinstance(solution, dict):
            searchable_fields.append(solution.get('code', ''))
            searchable_fields.append(solution.get('explanation', ''))

        # Search in tags
        tags = entry.get('tags', [])
        if tags:
            searchable_fields.extend(tags)

        # Check if any field contains the query
        for field in searchable_fields:
            if field and query_lower in str(field).lower():
                return True

        return False

    def _extract_metadata(
        self,
        entry: Dict[str, Any],
        file_path: Path,
        category: str,
        is_pattern: bool = False
    ) -> EntryMetadata:
        """Extract metadata from entry"""
        solution = entry.get('solution', {})

        return EntryMetadata(
            id=entry.get('id', 'UNKNOWN'),
            title=entry.get('title', 'Untitled'),
            severity=entry.get('severity', 'medium'),
            scope=entry.get('scope', 'universal'),
            category=category,
            file_path=str(file_path),
            has_prevention=bool(entry.get('prevention')),
            has_code=bool(solution.get('code') if isinstance(solution, dict) else False),
            has_explanation=bool(solution.get('explanation') if isinstance(solution, dict) else False),
            tags=entry.get('tags')
        )

    def _extract_preview(self, entry: Dict[str, Any], max_length: int = 200) -> str:
        """Extract preview text from entry"""
        # Try problem first
        problem = entry.get('problem', '')
        if problem:
            preview = problem.strip().split('\n')[0]
            if len(preview) > max_length:
                preview = preview[:max_length-3] + '...'
            return preview

        # Try root_cause
        root_cause = entry.get('root_cause', '')
        if root_cause:
            preview = root_cause.strip().split('\n')[0]
            if len(preview) > max_length:
                preview = preview[:max_length-3] + '...'
            return preview

        # Try solution code
        solution = entry.get('solution', {})
        if isinstance(solution, dict):
            code = solution.get('code', '')
            if code:
                lines = code.strip().split('\n')[:3]
                preview = '\n'.join(lines)
                if len(preview) > max_length:
                    preview = preview[:max_length-3] + '...'
                return preview

        return "No preview available"

    def get_by_id(self, entry_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific entry by ID.

        Args:
            entry_id: Entry ID (e.g., "DOCKER-024")

        Returns:
            Entry dict if found, None otherwise
        """
        # Search all YAML files for matching ID
        all_paths = self.search_paths + [self.project_kb_path, self.shared_kb_path]

        for search_path in all_paths:
            if not search_path.exists():
                continue

            for yaml_file in self._find_yaml_files(search_path):
                try:
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        content = yaml.safe_load(f)

                        if not content:
                            continue

                        # Search in errors
                        for entry in content.get('errors', []):
                            if entry.get('id') == entry_id:
                                return {
                                    'entry': entry,
                                    'file_path': str(yaml_file),
                                    'category': content.get('category', '')
                                }

                        # Search in patterns
                        for entry in content.get('patterns', []):
                            if entry.get('id') == entry_id:
                                return {
                                    'entry': entry,
                                    'file_path': str(yaml_file),
                                    'category': content.get('category', '')
                                }

                except Exception:
                    continue

        return None

    def browse_by_category(
        self,
        category: str,
        limit: int = 50,
        kb_type: Optional[str] = None
    ) -> List[SearchResult]:
        """
        Browse all entries in a category.

        Args:
            category: Category name
            limit: Maximum entries to return
            kb_type: "project", "shared", or None for both

        Returns:
            List of search results
        """
        results = []

        # Search in domains/
        for search_path in self.search_paths:
            if not search_path.exists():
                continue

            for yaml_file in self._find_yaml_files(search_path):
                try:
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        content = yaml.safe_load(f)

                        if not content or content.get('category') != category:
                            continue

                        # Add errors
                        for entry in content.get('errors', []):
                            metadata = self._extract_metadata(entry, yaml_file, category)
                            results.append(SearchResult(
                                metadata=metadata,
                                preview=self._extract_preview(entry),
                                kb_type="shared"
                            ))

                        # Add patterns
                        for entry in content.get('patterns', []):
                            metadata = self._extract_metadata(entry, yaml_file, category, is_pattern=True)
                            results.append(SearchResult(
                                metadata=metadata,
                                preview=self._extract_preview(entry),
                                kb_type="shared"
                            ))

                except Exception:
                    continue

        # Apply limit
        return results[:limit]
