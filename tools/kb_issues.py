#!/usr/bin/env python3
"""
kb_issues.py - GitHub Issues Integration for Knowledge Base

Automatically create GitHub issues for:
- YAML validation errors
- Missing metadata
- Quality issues
- Deprecated entries
- Update recommendations

Usage:
    python tools/kb_issues.py create --type yaml-errors
    python tools/kb_issues.py create --type quality-issues
    python tools/kb_issues.py create --entry-id ERROR-ID --reason "reason"
    python tools/kb_issues.py batch-create --file issues.json

Author: Knowledge Base Curator
Version: 1.0.0
License: MIT
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import subprocess


@dataclass
class IssueTemplate:
    """GitHub Issue template."""
    title: str
    body: str
    labels: List[str]
    assignees: List[str]
    milestone: Optional[str] = None


class GitHubIssueCreator:
    """Create GitHub issues for Knowledge Base maintenance."""

    def __init__(self, kb_root: Optional[Path] = None, repo_owner: Optional[str] = None, repo_name: Optional[str] = None):
        """
        Initialize GitHubIssueCreator.

        Args:
            kb_root: Root directory of knowledge base
            repo_owner: GitHub repository owner (e.g., "ozand")
            repo_name: GitHub repository name (e.g., "shared-knowledge-base")
        """
        if kb_root is None:
            from kb_config import KBConfig
            config = KBConfig()
            kb_root = config.kb_root

        self.kb_root = Path(kb_root)
        self.repo_owner = repo_owner
        self.repo_name = repo_name

        # Load repository info from git remote
        if not self.repo_owner or not self.repo_name:
            self._detect_repo_info()

    def _detect_repo_info(self):
        """Detect repository owner and name from git remote."""
        try:
            result = subprocess.run(
                ["git", "remote", "-v"],
                capture_output=True,
                text=True,
                cwd=self.kb_root
            )

            for line in result.stdout.split('\n'):
                if 'origin' in line and 'fetch' in line:
                    # Parse: origin  https://github.com/owner/repo.git (fetch)
                    parts = line.split('/')
                    if 'github.com' in parts:
                        repo_index = parts.index('github.com')
                        if repo_index + 1 < len(parts):
                            repo_path = parts[repo_index + 1]
                            if repo_path.endswith('.git'):
                                repo_path = repo_path[:-4]
                            owner, name = repo_path.split('/')[:2]
                            self.repo_owner = owner
                            self.repo_name = name
                            break
        except Exception as e:
            print(f"⚠️  Could not detect repo info: {e}")
            self.repo_owner = "owner"
            self.repo_name = "repo"

    def create_issue(self, template: IssueTemplate) -> bool:
        """
        Create GitHub issue using gh CLI.

        Args:
            template: IssueTemplate with title, body, labels

        Returns:
            True if issue created successfully
        """
        # Build gh command
        cmd = [
            "gh", "issue", "create",
            "--title", template.title,
            "--body", template.body
        ]

        # Add labels
        if template.labels:
            labels_str = ",".join(template.labels)
            cmd.extend(["--label", labels_str])

        # Add assignees
        if template.assignees:
            assignees_str = ",".join(template.assignees)
            cmd.extend(["--assignee", assignees_str])

        # Add milestone
        if template.milestone:
            cmd.extend(["--milestone", template.milestone])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.kb_root
            )

            if result.returncode == 0:
                # Extract issue number from output
                output = result.stdout.strip()
                if output.isdigit():
                    issue_number = output
                    print(f"✓ Issue created: #{issue_number}")
                    return True
                else:
                    print(f"✓ Issue created (number unknown)")
                    return True
            else:
                print(f"✗ Failed to create issue: {result.stderr}")
                return False

        except Exception as e:
            print(f"✗ Error creating issue: {e}")
            return False

    def create_yaml_error_issue(self, file_path: str, errors: List[str]) -> bool:
        """
        Create issue for YAML validation errors.

        Args:
            file_path: Path to file with errors
            errors: List of error messages

        Returns:
            True if issue created
        """
        # Extract relative path and entry info
        try:
            full_path = Path(file_path)
            rel_path = full_path.relative_to(self.kb_root)
        except:
            rel_path = Path(file_path)

        title = f"YAML Validation Error: {rel_path}"

        body = f"""## YAML Validation Error

**File:** `{rel_path}`

**Errors Found:** {len(errors)}

### Error Details:

"""

        for i, error in enumerate(errors, 1):
            body += f"{i}. `{error}`\n"

        body += f"""

### Context

This file was detected during KB validation or migration.

### Steps to Fix

1. Review the file: `{rel_path}`
2. Fix YAML syntax errors (see details above)
3. Validate: `python tools/kb.py validate {rel_path}`
4. Rebuild metadata: `python tools/kb.py init-metadata`

### Common YAML Issues

- **Indentation**: Use spaces, not tabs
- **Multi-line strings**: Use `|` or `>` correctly
- **Special characters**: Escape properly
- **Trailing whitespace**: Remove empty lines with spaces

### References

- [YAML Syntax Guide](https://yaml.org/spec/1.2/spec.html)
- [KB Validation Guide](FOR_CLAUDE_CODE.md)

---

**Automatically created by:** kb_issues.py
**Severity:** Medium (blocks metadata creation)
"""

        template = IssueTemplate(
            title=title,
            body=body,
            labels=["bug", "yaml", "validation", "kb-migration"],
            assignees=[]
        )

        return self.create_issue(template)

    def create_missing_metadata_issue(self, files_without_metadata: List[str]) -> bool:
        """
        Create issue for files missing metadata.

        Args:
            files_without_metadata: List of file paths

        Returns:
            True if issue created
        """
        title = f"Missing Metadata: {len(files_without_metadata)} files"

        body = f"""## Missing Metadata Detected

**Number of files:** {len(files_without_metadata)}

### Files Without Metadata:

"""

        for file_path in files_without_metadata[:20]:  # Limit to 20
            try:
                rel_path = Path(file_path).relative_to(self.kb_root)
                body += f"- `{rel_path}`\n"
            except:
                body += f"- `{file_path}`\n"

        if len(files_without_metadata) > 20:
            body += f"\n... and {len(files_without_metadata) - 20} more\n"

        body += """
### Impact

Files without metadata:
- ❌ Cannot be quality-assessed
- ❌ Don't appear in quality reports
- ❌ Not tracked in freshness checks
- ❌ Missing validation status

### Steps to Fix

For each file, run:
```bash
python tools/kb.py init-metadata --file <file_path>
```

Or fix all at once:
```bash
python tools/kb.py init-metadata
```

### References

- [Metadata System](METADATA_ARCHITECTURE.md)
- [FOR_CLAUDE_CODE.md](FOR_CLAUDE_CODE.md)

---

**Automatically created by:** kb_issues.py
**Severity:** Low (metadata is optional)
"""

        template = IssueTemplate(
            title=title,
            body=body,
            labels=["enhancement", "metadata", "kb-migration"],
            assignees=[]
        )

        return self.create_issue(template)

    def create_quality_issue(self, entry_id: str, quality_score: int, gaps: List[str]) -> bool:
        """
        Create issue for low-quality entries.

        Args:
            entry_id: Entry identifier
            quality_score: Current quality score (0-100)
            gaps: List of improvement areas

        Returns:
            True if issue created
        """
        title = f"Quality Issue: {entry_id} (Score: {quality_score}/100)"

        body = f"""## Low Quality Entry Detected

**Entry ID:** `{entry_id}`
**Quality Score:** {quality_score}/100
**Status:** {"❌ Needs Improvement" if quality_score < 75 else "⚠️  Could be better"}

### Quality Gaps

"""

        for gap in gaps:
            body += f"- **{gap}**\n"

        body += f"""

### Quality Standards

Entries should score ≥ 75/100 before being widely shared.
See [QUALITY_STANDARDS.md](QUALITY_STANDARDS.md) for rubric.

### Recommended Actions

1. **Expand content**: Add more details, examples, context
2. **Add examples**: Include code examples with explanations
3. **Review clarity**: Ensure clear title, structure, language
4. **Add references**: Link to related entries, documentation
5. **Testing**: Verify examples work as described

### After Improvements

1. Re-assess quality: `python -m tools.kb_predictive estimate-quality --entry-id {entry_id}`
2. Update metadata: `python tools/kb.py update-metadata --entry-id {entry_id} --quality-score <new_score>`
3. Mark as validated: Update `validation_status: validated`

### References

- [Quality Standards](QUALITY_STANDARDS.md)
- [Quality Assessment](SKILLS.md#audit-quality)

---

**Automatically created by:** kb_issues.py
**Priority:** Medium
"""

        labels = ["enhancement", "quality", "kb-improvement"]
        if quality_score < 60:
            labels.append("high-priority")
        elif quality_score >= 75:
            labels.append("low-priority")
        else:
            labels.append("medium-priority")

        template = IssueTemplate(
            title=title,
            body=body,
            labels=labels,
            assignees=[]
        )

        return self.create_issue(template)

    def create_deprecation_issue(self, entry_id: str, reason: str) -> bool:
        """
        Create issue for deprecated entries.

        Args:
            entry_id: Entry identifier
            reason: Reason for deprecation

        Returns:
            True if issue created
        """
        title = f"Deprecation Review: {entry_id}"

        body = f"""## Entry Requires Deprecation Review

**Entry ID:** `{entry_id}`

### Reason

{reason}

### Review Questions

1. **Is this entry still relevant?**
   - Yes → Keep it, update if needed
   - No → Deprecate it

2. **Is there a newer entry that supersedes this?**
   - Yes → Link to newer version, mark this as deprecated
   - No → Keep active

3. **Should this be merged with another entry?**
   - Yes → Merge and remove duplicate
   - No → Keep separate

### Actions

**Option 1: Keep Active**
```yaml
# Update entry metadata
validation_status: validated
deprecation_status: active
last_reviewed_at: 2026-01-06
```

**Option 2: Deprecate**
```yaml
deprecation_status: deprecated
deprecated_at: 2026-01-06
deprecated_reason: "{reason}"
superseded_by: "NEW-ENTRY-ID"
```

**Option 3: Merge**
1. Identify target entry
2. Merge content
3. Remove this entry
4. Update references

### References

- [Entry Lifecycle](WORKFLOWS.md#lifecycle-management)
- [Deprecation Policy](AGENT.md#deprecation)

---

**Automatically created by:** kb_issues.py
**Priority:** Low (review when convenient)
"""

        template = IssueTemplate(
            title=title,
            body=body,
            labels=["question", "deprecation", "kb-review"],
            assignees=[]
        )

        return self.create_issue(template)

    def scan_and_create_issues(self, issue_type: str = "all") -> Dict[str, int]:
        """
        Scan KB for issues and create GitHub issues.

        Args:
            issue_type: Type of issues to create ("yaml-errors", "quality", "deprecation", "all")

        Returns:
            Dictionary with issue creation statistics
        """
        from kb_meta import MetadataManager

        manager = MetadataManager(self.kb_root)
        stats = {
            "yaml_errors": 0,
            "quality_issues": 0,
            "deprecation": 0,
            "missing_metadata": 0,
            "total": 0
        }

        print(f"🔍 Scanning Knowledge Base for issues...")

        # 1. Check YAML errors
        if issue_type in ["yaml-errors", "all"]:
            print("\n📝 Checking for YAML errors...")
            yaml_errors = self._find_yaml_errors()
            stats["yaml_errors"] = len(yaml_errors)

            if yaml_errors:
                # Group by file
                errors_by_file = {}
                for error in yaml_errors:
                    file_path = error['file']
                    if file_path not in errors_by_file:
                        errors_by_file[file_path] = []
                    errors_by_file[file_path].append(error['message'])

                for file_path, errors in errors_by_file.items():
                    print(f"  Found {len(errors)} errors in {file_path}")
                    if self.create_yaml_error_issue(file_path, errors):
                        stats["total"] += 1

        # 2. Check quality issues
        if issue_type in ["quality", "all"]:
            print("\n⭐ Checking quality scores...")
            all_metadata = manager.get_all_entries_metadata()

            for entry_id, data in all_metadata.items():
                quality = data['metadata'].get('quality_score')

                if quality is not None and quality < 75:
                    print(f"  {entry_id}: {quality}/100 - Needs improvement")

                    # Determine gaps
                    gaps = self._determine_quality_gaps(entry_id, quality)

                    if self.create_quality_issue(entry_id, quality, gaps):
                        stats["quality_issues"] += 1
                        stats["total"] += 1

        # 3. Check for missing metadata
        if issue_type in ["missing-metadata", "all"]:
            print("\n📋 Checking for missing metadata...")
            yaml_files = []
            for ext in ['*.yaml', '*.yml']:
                yaml_files.extend(self.kb_root.rglob(ext))

            yaml_files = [f for f in yaml_files
                          if '_meta.yaml' not in str(f)
                          and '.cache' not in str(f)]

            files_without_metadata = []
            for yaml_file in yaml_files:
                meta_file = yaml_file.parent / f"{yaml_file.stem}_meta.yaml"
                if not meta_file.exists():
                    files_without_metadata.append(str(yaml_file))

            stats["missing_metadata"] = len(files_without_metadata)

            if files_without_metadata:
                print(f"  Found {len(files_without_metadata)} files without metadata")
                if self.create_missing_metadata_issue(files_without_metadata):
                    stats["total"] += 1

        # Print summary
        print(f"\n📊 Issue Creation Summary:")
        print(f"  YAML error issues: {stats['yaml_errors']}")
        print(f"  Quality issues: {stats['quality_issues']}")
        print(f"  Deprecation issues: {stats['deprecation']}")
        print(f"  Missing metadata: {stats['missing_metadata']}")
        print(f"  Total issues created: {stats['total']}")

        return stats

    def _find_yaml_errors(self) -> List[Dict]:
        """Find all YAML validation errors in KB."""
        from kb_config import KBConfig

        config = KBConfig(self.kb_root)

        # Get all YAML files
        yaml_files = []
        for ext in ['*.yaml', '*.yml']:
            yaml_files.extend(self.kb_root.rglob(ext))

        yaml_files = [f for f in yaml_files
                      if '_meta.yaml' not in str(f)
                      and '.cache' not in str(f)]

        errors = []

        for yaml_file in yaml_files:
            try:
                # Validate with kb.py
                result = subprocess.run(
                    ["python", "tools/kb.py", "validate", str(yaml_file)],
                    capture_output=True,
                    text=True,
                    cwd=self.kb_root
                )

                if result.returncode != 0:
                    errors.append({
                        'file': str(yaml_file),
                        'message': result.stdout.strip() or result.stderr.strip()
                    })
            except Exception as e:
                errors.append({
                    'file': str(yaml_file),
                    'message': str(e)
                })

        return errors

    def _determine_quality_gaps(self, entry_id: str, quality_score: int) -> List[str]:
        """Determine quality improvement areas."""
        gaps = []

        # Basic assessment based on score
        if quality_score < 60:
            gaps.append("Quality score is below acceptable threshold")
            gaps.append("Major improvements needed in all areas")

        if quality_score < 75:
            gaps.append("Quality score below recommended threshold (75)")
            gaps.append("Review and enhance content")

        # Could use kb_predictive to get detailed gaps
        # For now, provide general guidance
        if quality_score >= 60 and quality_score < 75:
            gaps.append("Consider adding more examples or context")

        return gaps


def main():
    """CLI interface for GitHub issues integration."""
    import argparse

    parser = argparse.ArgumentParser(description="GitHub Issues Integration for KB")
    parser.add_argument('action', choices=['create', 'scan', 'batch-create'],
                       help='Action to perform')
    parser.add_argument('--kb-root', type=Path,
                       help='Knowledge base root directory')
    parser.add_argument('--repo-owner',
                       help='GitHub repository owner (e.g., "ozand")')
    parser.add_argument('--repo-name',
                       help='GitHub repository name (e.g., "shared-knowledge-base")')
    parser.add_argument('--type',
                       choices=['yaml-errors', 'quality', 'deprecation', 'missing-metadata', 'all'],
                       help='Type of issues to create')
    parser.add_argument('--entry-id',
                       help='Entry ID (for single entry actions)')
    parser.add_argument('--file',
                       help='File path (for YAML error issues)')
    parser.add_argument('--reason',
                       help='Reason for issue (for deprecation etc.)')
    parser.add_argument('--quality-score', type=int,
                       help='Quality score (for quality issues)')
    parser.add_argument('--batch-file',
                       help='JSON file with batch issue definitions')

    args = parser.parse_args()

    creator = GitHubIssueCreator(args.kb_root, args.repo_owner, args.repo_name)

    if args.action == 'create':
        if args.type == 'yaml-errors' and args.file:
            # Create issue for specific file
            errors = [args.reason]  # Single error from --reason
            creator.create_yaml_error_issue(args.file, errors)

        elif args.type == 'quality' and args.entry_id:
            quality_score = args.quality_score or 0
            gaps = [args.reason] if args.reason else []
            creator.create_quality_issue(args.entry_id, quality_score, gaps)

        elif args.type == 'deprecation' and args.entry_id:
            creator.create_deprecation_issue(args.entry_id, args.reason or "Manual review needed")

        else:
            print("✗ Invalid combination of arguments for 'create' action")
            print("  Use --type with --entry-id or --file")
            return 1

    elif args.action == 'scan':
        stats = creator.scan_and_create_issues(args.type)

        if stats['total'] == 0:
            print("\n✅ No issues found!")
            return 0

    elif args.action == 'batch-create':
        if not args.batch_file:
            print("✗ --batch-file required for batch-create")
            return 1

        # Load batch file
        with open(args.batch_file, 'r') as f:
            issues = json.load(f)

        print(f"📋 Creating {len(issues)} issues from batch file...")

        created = 0
        for issue_def in issues:
            template = IssueTemplate(**issue_def)
            if creator.create_issue(template):
                created += 1

        print(f"\n✓ Created {created}/{len(issues)} issues")

    return 0


if __name__ == '__main__':
    sys.exit(main())
