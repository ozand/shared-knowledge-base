"""
Core validation functionality for Shared Knowledge Base.

Provides YAML validation, schema checking, and quality gates.
"""

import re
import yaml
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from .models import ValidationError, ValidationResult, SeverityLevel, ScopeLevel


class KnowledgeValidator:
    """
    Core validator for knowledge base entries.

    Validates YAML syntax, schema compliance, and quality requirements.
    """

    # Valid severity levels
    VALID_SEVERITIES = ['critical', 'high', 'medium', 'low']

    # Valid scopes
    VALID_SCOPES = ['universal', 'python', 'javascript', 'docker', 'postgresql', 'vps', 'framework', 'project']

    # Required fields for error entries
    REQUIRED_ERROR_FIELDS = ['id', 'title', 'severity', 'scope', 'problem', 'solution']

    # Required fields for pattern entries
    REQUIRED_PATTERN_FIELDS = ['id', 'title', 'scope', 'pattern', 'implementation']

    def __init__(self, repo_path: str = None):
        """
        Initialize validator.

        Args:
            repo_path: Path to repository root (default: current directory)
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()

    def validate_file(self, file_path: Path) -> ValidationResult:
        """
        Validate a single YAML file.

        Args:
            file_path: Path to YAML file

        Returns:
            ValidationResult with any errors or warnings found
        """
        start_time = time.time()
        errors = []
        warnings = []

        try:
            # Check file exists
            if not file_path.exists():
                return ValidationResult(
                    is_valid=False,
                    files_checked=0,
                    errors=[ValidationError(
                        file_path=str(file_path),
                        error_type="file_not_found",
                        message=f"File not found: {file_path}",
                        severity="error"
                    )],
                    execution_time_ms=(time.time() - start_time) * 1000
                )

            # Check YAML syntax
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    content = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    return ValidationResult(
                        is_valid=False,
                        files_checked=1,
                        errors=[ValidationError(
                            file_path=str(file_path),
                            error_type="syntax",
                            message=f"YAML syntax error: {str(e)}",
                            severity="error"
                        )],
                        execution_time_ms=(time.time() - start_time) * 1000
                    )

            if not content:
                warnings.append(ValidationError(
                    file_path=str(file_path),
                    error_type="empty_file",
                    message="File is empty",
                    severity="warning"
                ))
                return ValidationResult(
                    is_valid=True,
                    files_checked=1,
                    warnings=warnings,
                    execution_time_ms=(time.time() - start_time) * 1000
                )

            # Validate schema
            schema_errors, schema_warnings = self._validate_schema(content, file_path)
            errors.extend(schema_errors)
            warnings.extend(schema_warnings)

            # Validate entries
            entry_errors, entry_warnings = self._validate_entries(content, file_path)
            errors.extend(entry_errors)
            warnings.extend(entry_warnings)

        except Exception as e:
            errors.append(ValidationError(
                file_path=str(file_path),
                error_type="validation_error",
                message=f"Validation failed: {str(e)}",
                severity="error"
            ))

        execution_time = (time.time() - start_time) * 1000

        return ValidationResult(
            is_valid=len(errors) == 0,
            files_checked=1,
            errors=errors,
            warnings=warnings,
            execution_time_ms=execution_time
        )

    def validate_directory(self, dir_path: Path, recursive: bool = True) -> ValidationResult:
        """
        Validate all YAML files in a directory.

        Args:
            dir_path: Path to directory
            recursive: Whether to search recursively

        Returns:
            ValidationResult with aggregated results
        """
        start_time = time.time()
        all_errors = []
        all_warnings = []
        files_checked = 0

        # Find all YAML files
        if recursive:
            yaml_files = list(dir_path.rglob('*.yaml'))
        else:
            yaml_files = list(dir_path.glob('*.yaml'))

        # Skip index and meta files
        yaml_files = [
            f for f in yaml_files
            if '_index.yaml' not in str(f) and '_meta.yaml' not in str(f) and 'catalog.yaml' not in str(f)
        ]

        # Validate each file
        for yaml_file in yaml_files:
            result = self.validate_file(yaml_file)
            files_checked += 1
            all_errors.extend(result.errors)
            all_warnings.extend(result.warnings)

        execution_time = (time.time() - start_time) * 1000

        return ValidationResult(
            is_valid=len(all_errors) == 0,
            files_checked=files_checked,
            errors=all_errors,
            warnings=all_warnings,
            execution_time_ms=execution_time
        )

    def _validate_schema(self, content: Dict[str, Any], file_path: Path) -> Tuple[List[ValidationError], List[ValidationError]]:
        """Validate file-level schema"""
        errors = []
        warnings = []

        # Check for required top-level fields
        if 'version' not in content:
            errors.append(ValidationError(
                file_path=str(file_path),
                error_type="required_field",
                message="Missing required field: version",
                severity="error",
                field_path="version"
            ))

        if 'category' not in content:
            errors.append(ValidationError(
                file_path=str(file_path),
                error_type="required_field",
                message="Missing required field: category",
                severity="error",
                field_path="category"
            ))

        # Check for errors or patterns
        has_errors = 'errors' in content and content['errors']
        has_patterns = 'patterns' in content and content['patterns']

        if not has_errors and not has_patterns:
            warnings.append(ValidationError(
                file_path=str(file_path),
                error_type="empty_content",
                message="File has no errors or patterns",
                severity="warning",
                field_path="errors"
            ))

        return errors, warnings

    def _validate_entries(self, content: Dict[str, Any], file_path: Path) -> Tuple[List[ValidationError], List[ValidationError]]:
        """Validate individual entries"""
        errors = []
        warnings = []

        # Validate error entries
        for idx, entry in enumerate(content.get('errors', [])):
            entry_errors, entry_warnings = self._validate_entry(entry, file_path, idx, 'error')
            errors.extend(entry_errors)
            warnings.extend(entry_warnings)

        # Validate pattern entries
        for idx, entry in enumerate(content.get('patterns', [])):
            entry_errors, entry_warnings = self._validate_entry(entry, file_path, idx, 'pattern')
            errors.extend(entry_errors)
            warnings.extend(entry_warnings)

        return errors, warnings

    def _validate_entry(
        self,
        entry: Dict[str, Any],
        file_path: Path,
        index: int,
        entry_type: str
    ) -> Tuple[List[ValidationError], List[ValidationError]]:
        """Validate a single entry"""
        errors = []
        warnings = []

        field_prefix = f"errors[{index}]" if entry_type == 'error' else f"patterns[{index}]"

        # Determine required fields based on entry type
        required_fields = self.REQUIRED_ERROR_FIELDS if entry_type == 'error' else self.REQUIRED_PATTERN_FIELDS

        # Check required fields
        for field in required_fields:
            if field not in entry:
                errors.append(ValidationError(
                    file_path=str(file_path),
                    error_type="required_field",
                    message=f"Missing required field: {field}",
                    severity="error",
                    field_path=f"{field_prefix}.{field}"
                ))

        # Validate ID format
        if 'id' in entry:
            id_errors, id_warnings = self._validate_id(entry['id'], file_path, field_prefix)
            errors.extend(id_errors)
            warnings.extend(id_warnings)

        # Validate severity
        if 'severity' in entry:
            if entry['severity'] not in self.VALID_SEVERITIES:
                errors.append(ValidationError(
                    file_path=str(file_path),
                    error_type="format",
                    message=f"Invalid severity: {entry['severity']}. Must be one of {self.VALID_SEVERITIES}",
                    severity="error",
                    field_path=f"{field_prefix}.severity"
                ))

        # Validate scope
        if 'scope' in entry:
            if entry['scope'] not in self.VALID_SCOPES:
                errors.append(ValidationError(
                    file_path=str(file_path),
                    error_type="format",
                    message=f"Invalid scope: {entry['scope']}. Must be one of {self.VALID_SCOPES}",
                    severity="error",
                    field_path=f"{field_prefix}.scope"
                ))

        # Validate solution structure
        if 'solution' in entry and isinstance(entry['solution'], dict):
            if not entry['solution'].get('code') and not entry['solution'].get('explanation'):
                warnings.append(ValidationError(
                    file_path=str(file_path),
                    error_type="incomplete_solution",
                    message="Solution should have code or explanation",
                    severity="warning",
                    field_path=f"{field_prefix}.solution"
                ))

        return errors, warnings

    def _validate_id(self, entry_id: str, file_path: Path, field_prefix: str) -> Tuple[List[ValidationError], List[ValidationError]]:
        """Validate entry ID format"""
        errors = []
        warnings = []

        # ID should match pattern: CATEGORY-NNN
        # Example: DOCKER-024, PYTHON-001
        if not re.match(r'^[A-Z_]+-\d{3,}$', str(entry_id)):
            warnings.append(ValidationError(
                file_path=str(file_path),
                error_type="format",
                message=f"ID format should be CATEGORY-NNN (e.g., DOCKER-024), got: {entry_id}",
                severity="warning",
                field_path=f"{field_prefix}.id"
            ))

        return errors, warnings

    def validate_yaml_content(self, yaml_content: str) -> ValidationResult:
        """
        Validate YAML content string.

        Args:
            yaml_content: YAML content as string

        Returns:
            ValidationResult with any errors found
        """
        import io

        start_time = time.time()
        errors = []

        try:
            content = yaml.safe_load(io.StringIO(yaml_content))

            if not content:
                return ValidationResult(
                    is_valid=True,
                    files_checked=1,
                    warnings=[ValidationError(
                        file_path="<string>",
                        error_type="empty_content",
                        message="YAML content is empty",
                        severity="warning"
                    )],
                    execution_time_ms=(time.time() - start_time) * 1000
                )

            # Validate schema
            schema_errors, schema_warnings = self._validate_schema(content, Path("<string>"))
            errors.extend(schema_errors)

            # Validate entries
            entry_errors, entry_warnings = self._validate_entries(content, Path("<string>"))
            errors.extend(entry_errors)

        except yaml.YAMLError as e:
            errors.append(ValidationError(
                file_path="<string>",
                error_type="syntax",
                message=f"YAML syntax error: {str(e)}",
                severity="error"
            ))

        execution_time = (time.time() - start_time) * 1000

        return ValidationResult(
            is_valid=len(errors) == 0,
            files_checked=1,
            errors=errors,
            execution_time_ms=execution_time
        )

    def calculate_quality_score(self, entry: Dict[str, Any]) -> int:
        """
        Calculate quality score for an entry (0-100).

        Args:
            entry: Entry dictionary

        Returns:
            Quality score from 0-100
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
