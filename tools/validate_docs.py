#!/usr/bin/env python3
"""
Documentation Validation Script for Shared Knowledge Base

Validates documentation files against best practices:
- PROGRESSIVE-DISCLOSURE-001: Progressive disclosure structure
- DOCUMENTATION-TRANSLATION-001: Bilingual documentation strategy
- DOCUMENTATION-HIERARCHY-001: Multi-dimensional indexing

Usage:
    python tools/validate_docs.py [directory]
    python tools/validate_docs.py docs/research/claude-code/
    python tools/validate_docs.py --fix  # Auto-fix issues
"""

import os
import sys
import re
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import yaml


class DocumentationValidator:
    """Validates documentation files against best practices."""

    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir)
        self.issues = []
        self.fixes = []

    def validate_all(self) -> bool:
        """Validate all documentation files."""
        print(f"🔍 Validating documentation in: {self.root_dir}")
        print("=" * 60)

        # Find all markdown files
        md_files = list(self.root_dir.rglob("*.md"))
        print(f"📄 Found {len(md_files)} markdown files\n")

        # Validate each file
        for md_file in md_files:
            self.validate_file(md_file)

        # Print results
        self.print_results()

        return len(self.issues) == 0

    def validate_file(self, file_path: Path):
        """Validate a single documentation file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Run validations
            self.check_progressive_disclosure(file_path, content, lines)
            self.check_bilingual_docs(file_path, content, lines)
            self.check_language_metadata(file_path, content, lines)
            self.check_related_guides(file_path, content, lines)
            self.check_frontmatter(file_path, content)

        except Exception as e:
            self.issues.append({
                'file': str(file_path),
                'type': 'error',
                'message': f"Failed to read file: {e}"
            })

    def check_progressive_disclosure(self, file_path: Path, content: str, lines: List[str]):
        """
        Check PROGRESSIVE-DISCLOSURE-001 compliance.

        For large files (>500 lines):
        - Should have clear sections
        - Should use "Related Guides" section
        - Should not be monolithic
        """
        line_count = len(lines)

        if line_count > 500:
            # Check for "Related Guides" section
            if not re.search(r'##\s*Related\s+Guides', content, re.IGNORECASE):
                self.issues.append({
                    'file': str(file_path),
                    'type': 'progressive-disclosure',
                    'severity': 'medium',
                    'message': f"Missing 'Related Guides' section (file has {line_count} lines)",
                    'recommendation': "Add 'Related Guides' section at end with cross-references"
                })

            # Check for clear section structure
            section_count = len(re.findall(r'^#+\s+', content, re.MULTILINE))
            if section_count < 5:
                self.issues.append({
                    'file': str(file_path),
                    'type': 'progressive-disclosure',
                    'severity': 'low',
                    'message': f"Poor section structure (only {section_count} sections in {line_count} lines)",
                    'recommendation': "Add more section headers to break up content"
                })

    def check_bilingual_docs(self, file_path: Path, content: str, lines: List[str]):
        """
        Check DOCUMENTATION-TRANSLATION-001 compliance.

        For non-English files:
        - Should have English summary
        - Should have language metadata
        - Should link to English equivalent
        """
        # Detect if content is non-English (heuristic: Cyrillic characters)
        has_cyrillic = bool(re.search(r'[а-яА-Я]', content))
        has_english_summary = bool(re.search(r'##\s*English\s+Summary', content, re.IGNORECASE))

        if has_cyrillic and not has_english_summary:
            # Check if it's a translation (already in English)
            if not re.search(r'language:\s*english', content, re.IGNORECASE):
                self.issues.append({
                    'file': str(file_path),
                    'type': 'bilingual',
                    'severity': 'high',
                    'message': "Non-English document missing English summary",
                    'recommendation': "Add '## English Summary' section with key topics and related English docs"
                })

    def check_language_metadata(self, file_path: Path, content: str, lines: List[str]):
        """
        Check if file has proper language metadata.
        """
        # Check for language metadata in frontmatter or summary
        has_language_metadata = bool(re.search(
            r'(language|язык):\s*(English|Russian|Русский)',
            content,
            re.IGNORECASE
        ))

        # Check file size
        line_count = len(lines)
        if line_count > 300 and not has_language_metadata:
            self.issues.append({
                'file': str(file_path),
                'type': 'metadata',
                'severity': 'low',
                'message': f"Large file ({line_count} lines) missing language metadata",
                'recommendation': "Add language metadata in summary or frontmatter"
            })

    def check_related_guides(self, file_path: Path, content: str, lines: List[str]):
        """
        Check if documentation has "Related Guides" section.
        """
        line_count = len(lines)

        # Only check documentation files (not small files)
        if line_count < 200:
            return

        # Check for Related Guides section
        has_related_guides = bool(re.search(
            r'##\s*Related\s+Guides',
            content,
            re.IGNORECASE
        ))

        if not has_related_guides:
            self.issues.append({
                'file': str(file_path),
                'type': 'cross-references',
                'severity': 'low',
                'message': f"Missing 'Related Guides' section",
                'recommendation': "Add 'Related Guides' section at end with links to related documentation"
            })

    def check_frontmatter(self, file_path: Path, content: str):
        """
        Check if file has proper YAML frontmatter (for guides that need it).
        """
        # Check for YAML frontmatter
        has_frontmatter = content.startswith('---')

        # Only certain files require frontmatter
        filename = file_path.name

        # Files that should have frontmatter
        requires_frontmatter = [
            'INDEX.md',
            'README.md'
        ]

        if filename in requires_frontmatter and not has_frontmatter:
            self.issues.append({
                'file': str(file_path),
                'type': 'frontmatter',
                'severity': 'medium',
                'message': f"Missing YAML frontmatter ({filename} should have metadata)",
                'recommendation': "Add YAML frontmatter with version, last_updated, description"
            })

    def print_results(self):
        """Print validation results."""
        print("\n" + "=" * 60)
        print("📊 VALIDATION RESULTS")
        print("=" * 60)

        if not self.issues:
            print("✅ All validations passed!")
            return

        # Group issues by type
        by_type = {}
        for issue in self.issues:
            issue_type = issue['type']
            if issue_type not in by_type:
                by_type[issue_type] = []
            by_type[issue_type].append(issue)

        # Print issues by type
        for issue_type, issues in sorted(by_type.items()):
            print(f"\n⚠️  {issue_type.upper()} ({len(issues)} issues)")
            print("-" * 60)

            for issue in issues[:5]:  # Show first 5
                severity = issue.get('severity', 'unknown').upper()
                print(f"\n  [{severity}] {issue['file']}")
                print(f"  📌 {issue['message']}")
                if 'recommendation' in issue:
                    print(f"  💡 {issue['recommendation']}")

            if len(issues) > 5:
                print(f"\n  ... and {len(issues) - 5} more")

        # Summary
        print("\n" + "=" * 60)
        print(f"Total Issues: {len(self.issues)}")
        print(f"Files Checked: {len(list(self.root_dir.rglob('*.md')))}")
        print("=" * 60)

    def fix_issues(self):
        """Auto-fix common issues."""
        print("\n🔧 Auto-fixing issues...")

        fixed_count = 0

        for issue in self.issues:
            if issue['type'] == 'cross-references':
                # Can't auto-fix cross-references (need manual review)
                continue

            file_path = Path(issue['file'])

            if not file_path.exists():
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Apply fixes
                original_content = content

                if issue['type'] == 'metadata':
                    # Add language metadata if missing
                    if 'language:' not in content:
                        # Detect language
                        has_cyrillic = bool(re.search(r'[а-яА-Я]', content))
                        if has_cyrillic:
                            lang = "Russian"
                        else:
                            lang = "English"

                        # Add after first heading or at start
                        lines = content.split('\n')
                        insert_pos = 0

                        # Find first heading
                        for i, line in enumerate(lines):
                            if line.startswith('#'):
                                insert_pos = i + 1
                                break

                        # Insert metadata
                        lines.insert(insert_pos, "")
                        lines.insert(insert_pos + 1, f"**Language:** {lang}")
                        lines.insert(insert_pos + 2, f"**Lines:** {len(lines)}")

                        content = '\n'.join(lines)

                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    fixed_count += 1
                    print(f"  ✅ Fixed: {file_path.name}")

            except Exception as e:
                print(f"  ❌ Failed to fix {file_path.name}: {e}")

        print(f"\n✅ Fixed {fixed_count} issues")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate documentation files against best practices"
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='docs/research/claude-code/',
        help='Directory to validate (default: docs/research/claude-code/)'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Auto-fix common issues'
    )

    args = parser.parse_args()

    # Convert to absolute path
    directory = Path(args.directory).resolve()

    if not directory.exists():
        print(f"❌ Error: Directory not found: {directory}")
        sys.exit(1)

    # Run validation
    validator = DocumentationValidator(str(directory))
    passed = validator.validate_all()

    # Auto-fix if requested
    if args.fix:
        validator.fix_issues()

    # Exit with appropriate code
    sys.exit(0 if passed else 1)


if __name__ == '__main__':
    main()
