#!/usr/bin/env python3
"""
Knowledge Base Search Tool

Search through YAML knowledge base files for errors, patterns, and solutions.

Usage:
    python search-kb.py "circular import"
    python search-kb.py --id IMPORT-001
    python search-kb.py --tag async --scope python
    python search-kb.py --severity high
"""

import argparse
import sys
import yaml
from pathlib import Path
from typing import List, Dict, Any


class KnowledgeBaseSearch:
    """Search knowledge base YAML files."""

    def __init__(self, kb_path: Path):
        self.kb_path = kb_path

    def search_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Search by keyword in any field."""
        results = []
        keyword_lower = keyword.lower()

        for yaml_file in self.kb_path.rglob("*.yaml"):
            with yaml_file.open(encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f)
                except yaml.YAMLError:
                    continue

            if "errors" in data:
                for error in data["errors"]:
                    if keyword_lower in str(error).lower():
                        results.append({
                            "file": yaml_file.relative_to(self.kb_path),
                            "type": "error",
                            **error
                        })

            if "patterns" in data:
                for pattern in data["patterns"]:
                    if keyword_lower in str(pattern).lower():
                        results.append({
                            "file": yaml_file.relative_to(self.kb_path),
                            "type": "pattern",
                            **pattern
                        })

        return results

    def search_by_id(self, error_id: str) -> Dict[str, Any] | None:
        """Search by error ID."""
        for yaml_file in self.kb_path.rglob("*.yaml"):
            with yaml_file.open(encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f)
                except yaml.YAMLError:
                    continue

            if "errors" in data:
                for error in data["errors"]:
                    if error.get("id") == error_id:
                        return {
                            "file": yaml_file.relative_to(self.kb_path),
                            "type": "error",
                            **error
                        }

        return None

    def search_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """Search by tag."""
        results = []

        for yaml_file in self.kb_path.rglob("*.yaml"):
            with yaml_file.open(encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f)
                except yaml.YAMLError:
                    continue

            if "errors" in data:
                for error in data["errors"]:
                    if tag in error.get("tags", []):
                        results.append({
                            "file": yaml_file.relative_to(self.kb_path),
                            "type": "error",
                            **error
                        })

        return results

    def search_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """Search by severity level."""
        results = []

        for yaml_file in self.kb_path.rglob("*.yaml"):
            with yaml_file.open(encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f)
                except yaml.YAMLError:
                    continue

            if "errors" in data:
                for error in data["errors"]:
                    if error.get("severity") == severity:
                        results.append({
                            "file": yaml_file.relative_to(self.kb_path),
                            "type": "error",
                            **error
                        })

        return results

    def search_by_scope(self, scope: str) -> List[Dict[str, Any]]:
        """Search by scope (universal, python, project, etc.)."""
        results = []

        for yaml_file in self.kb_path.rglob("*.yaml"):
            with yaml_file.open(encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f)
                except yaml.YAMLError:
                    continue

            if "errors" in data:
                for error in data["errors"]:
                    if error.get("scope") == scope:
                        results.append({
                            "file": yaml_file.relative_to(self.kb_path),
                            "type": "error",
                            **error
                        })

        return results


def format_result(result: Dict[str, Any], verbose: bool = False):
    """Format search result for display."""
    result_type = result.get("type", "unknown")

    if result_type == "error":
        print(f"\n{'='*70}")
        print(f"ID: {result.get('id', 'N/A')}")
        print(f"Title: {result.get('title', 'N/A')}")
        print(f"Severity: {result.get('severity', 'N/A')}")
        print(f"File: {result.get('file', 'N/A')}")

        if scope := result.get("scope"):
            print(f"Scope: {scope}")

        if tags := result.get("tags"):
            print(f"Tags: {', '.join(tags)}")

        if verbose:
            if problem := result.get("problem"):
                print(f"\nProblem:\n{problem}")

            if symptoms := result.get("symptoms"):
                print(f"\nSymptoms:")
                for symptom in symptoms:
                    print(f"  - {symptom}")

            if solution := result.get("solution", {}).get("code"):
                print(f"\nSolution:")
                print(solution)

    elif result_type == "pattern":
        print(f"\n{'='*70}")
        print(f"Pattern: {result.get('pattern_name', 'N/A')}")
        print(f"Use Case: {result.get('use_case', 'N/A')}")
        print(f"File: {result.get('file', 'N/A')}")

        if verbose:
            if solution := result.get("solution", {}).get("code"):
                print(f"\nImplementation:")
                print(solution)


def main():
    parser = argparse.ArgumentParser(
        description="Search knowledge base for errors and patterns"
    )
    parser.add_argument("keyword", nargs="?", help="Keyword to search for")
    parser.add_argument("--id", help="Search by error ID")
    parser.add_argument("--tag", help="Search by tag")
    parser.add_argument("--severity", choices=["critical", "high", "medium", "low"],
                       help="Search by severity")
    parser.add_argument("--scope", help="Search by scope (universal, python, etc.)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Show detailed information")
    parser.add_argument("--kb-path", default="docs/knowledge-base",
                       help="Path to knowledge base directory")

    args = parser.parse_args()

    # Find knowledge base path
    kb_path = Path(args.kb_path)
    if not kb_path.exists():
        # Try relative to script location
        script_dir = Path(__file__).parent.parent
        kb_path = script_dir
        if not kb_path.exists():
            print(f"Error: Knowledge base not found at {kb_path}")
            sys.exit(1)

    searcher = KnowledgeBaseSearch(kb_path)
    results = []

    # Search based on arguments
    if args.id:
        result = searcher.search_by_id(args.id)
        if result:
            results = [result]
    elif args.tag:
        results = searcher.search_by_tag(args.tag)
    elif args.severity:
        results = searcher.search_by_severity(args.severity)
    elif args.scope:
        results = searcher.search_by_scope(args.scope)
    elif args.keyword:
        results = searcher.search_by_keyword(args.keyword)
    else:
        parser.print_help()
        sys.exit(1)

    # Display results
    if not results:
        print("No results found.")
        sys.exit(0)

    print(f"\nFound {len(results)} result(s):\n")
    for result in results:
        format_result(result, verbose=args.verbose)

    print(f"\n{'='*70}\n")
    print(f"Total: {len(results)} result(s)")


if __name__ == "__main__":
    main()
