#!/usr/bin/env python3
"""
Knowledge Base Validation Tool

Validate YAML knowledge base files for correctness and completeness.

Usage:
    python validate-kb.py
    python validate-kb.py --path docs/knowledge-base
    python validate-kb.py --fix
"""

import argparse
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class KnowledgeBaseValidator:
    """Validate knowledge base YAML files."""

    REQUIRED_ERROR_FIELDS = ["id", "title", "severity", "problem", "tags"]
    REQUIRED_PATTERN_FIELDS = ["pattern_name", "use_case", "solution"]
    VALID_SEVERITIES = ["critical", "high", "medium", "low"]
    VALID_SCOPES = ["universal", "python", "framework", "domain", "project"]

    def __init__(self, kb_path: Path):
        self.kb_path = kb_path
        self.errors = []
        self.warnings = []

    def validate_file(self, yaml_file: Path) -> bool:
        """Validate single YAML file."""
        file_valid = True

        # Check if file can be parsed
        try:
            with yaml_file.open(encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.errors.append(f"{yaml_file}: Invalid YAML syntax - {e}")
            return False

        # Check version
        if "version" not in data:
            self.warnings.append(f"{yaml_file}: Missing 'version' field")

        # Check category
        if "category" not in data:
            self.warnings.append(f"{yaml_file}: Missing 'category' field")

        # Check last_updated
        if "last_updated" not in data:
            self.warnings.append(f"{yaml_file}: Missing 'last_updated' field")
        else:
            try:
                datetime.fromisoformat(data["last_updated"])
            except ValueError:
                self.errors.append(
                    f"{yaml_file}: Invalid 'last_updated' format. "
                    "Use YYYY-MM-DD"
                )
                file_valid = False

        # Validate errors
        if "errors" in data:
            for i, error in enumerate(data["errors"]):
                if not self.validate_error(yaml_file, i, error):
                    file_valid = False

        # Validate patterns
        if "patterns" in data:
            for i, pattern in enumerate(data["patterns"]):
                if not self.validate_pattern(yaml_file, i, pattern):
                    file_valid = False

        return file_valid

    def validate_error(self, file_path: Path, index: int, error: Dict) -> bool:
        """Validate single error entry."""
        valid = True

        # Check required fields
        for field in self.REQUIRED_ERROR_FIELDS:
            if field not in error:
                self.errors.append(
                    f"{file_path}: Error #{index} missing required field '{field}'"
                )
                valid = False

        # Check error ID format
        if "id" in error:
            error_id = error["id"]
            if not error_id or "-" not in error_id:
                self.errors.append(
                    f"{file_path}: Error #{index} has invalid ID format. "
                    "Use 'CATEGORY-NNN'"
                )
                valid = False

        # Check severity
        if "severity" in error:
            if error["severity"] not in self.VALID_SEVERITIES:
                self.errors.append(
                    f"{file_path}: Error #{index} has invalid severity "
                    f"'{error['severity']}'. "
                    f"Valid: {', '.join(self.VALID_SEVERITIES)}"
                )
                valid = False

        # Check scope if present
        if "scope" in error:
            if error["scope"] not in self.VALID_SCOPES:
                self.warnings.append(
                    f"{file_path}: Error #{index} has non-standard scope "
                    f"'{error['scope']}'. "
                    f"Recommended: {', '.join(self.VALID_SCOPES)}"
                )

        # Check for solution
        if "solution" not in error:
            self.warnings.append(
                f"{file_path}: Error #{index} missing 'solution'"
            )
        elif not isinstance(error["solution"], dict):
            self.errors.append(
                f"{file_path}: Error #{index} 'solution' must be a dict"
            )
            valid = False

        # Check for prevention strategies
        if "prevention" not in error:
            self.warnings.append(
                f"{file_path}: Error #{index} missing 'prevention' strategies"
            )

        # Check tags
        if "tags" in error:
            if not isinstance(error["tags"], list):
                self.errors.append(
                    f"{file_path}: Error #{index} 'tags' must be a list"
                )
                valid = False
            elif len(error["tags"]) == 0:
                self.warnings.append(
                    f"{file_path}: Error #{index} has no tags"
                )

        return valid

    def validate_pattern(self, file_path: Path, index: int, pattern: Dict) -> bool:
        """Validate single pattern entry."""
        valid = True

        # Check required fields
        for field in self.REQUIRED_PATTERN_FIELDS:
            if field not in pattern:
                self.errors.append(
                    f"{file_path}: Pattern #{index} missing required field '{field}'"
                )
                valid = False

        # Check solution structure
        if "solution" in pattern:
            if not isinstance(pattern["solution"], dict):
                self.errors.append(
                    f"{file_path}: Pattern #{index} 'solution' must be a dict"
                )
                valid = False

        return valid

    def validate_all(self) -> bool:
        """Validate all YAML files in knowledge base."""
        all_valid = True

        for yaml_file in self.kb_path.rglob("*.yaml"):
            # Skip shared directory
            if "shared" in yaml_file.parts:
                continue

            # Skip tools directory
            if "tools" in yaml_file.parts:
                continue

            if not self.validate_file(yaml_file):
                all_valid = False

        return all_valid

    def check_duplicate_ids(self):
        """Check for duplicate error IDs across all files."""
        error_ids = {}

        for yaml_file in self.kb_path.rglob("*.yaml"):
            if "shared" in yaml_file.parts or "tools" in yaml_file.parts:
                continue

            with yaml_file.open(encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f)
                except yaml.YAMLError:
                    continue

            if "errors" in data:
                for error in data["errors"]:
                    error_id = error.get("id")
                    if error_id:
                        if error_id in error_ids:
                            self.errors.append(
                                f"Duplicate error ID '{error_id}' in "
                                f"{yaml_file} and {error_ids[error_id]}"
                            )
                        else:
                            error_ids[error_id] = yaml_file

    def print_summary(self):
        """Print validation summary."""
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ All knowledge base files are valid!")

        print(f"\n{'='*70}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate knowledge base YAML files"
    )
    parser.add_argument("--path", type=Path,
                       default="docs/knowledge-base",
                       help="Path to knowledge base directory")
    parser.add_argument("--check-duplicates", action="store_true",
                       help="Check for duplicate error IDs")
    parser.add_argument("--strict", action="store_true",
                       help="Treat warnings as errors")

    args = parser.parse_args()

    # Find knowledge base
    kb_path = args.path
    if not kb_path.exists():
        # Try relative to script location
        script_dir = Path(__file__).parent.parent
        kb_path = script_dir
        if not kb_path.exists():
            print(f"Error: Knowledge base not found at {kb_path}")
            sys.exit(1)

    # Validate
    validator = KnowledgeBaseValidator(kb_path)
    valid = validator.validate_all()

    # Check for duplicates if requested
    if args.check_duplicates:
        validator.check_duplicate_ids()

    # Print summary
    validator.print_summary()

    # Exit code
    if validator.errors:
        sys.exit(1)
    elif args.strict and validator.warnings:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
