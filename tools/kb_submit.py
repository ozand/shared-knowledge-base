#!/usr/bin/env python3
"""
kb-submit - Submit knowledge entries to Shared Knowledge Base via GitHub Issues

Usage:
    python tools/kb_submit.py submit --entry path/to/entry.yaml
    python tools/kb_submit.py status --issue 123

Author: Claude Code
Version: 3.1
"""

import argparse
import yaml
import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import os


class KBSubmitter:
    """Submit KB entries to Shared Knowledge Base."""

    SHARED_KB_REPO = "ozand/shared-knowledge-base"

    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
        if not self.github_token:
            print("⚠ Warning: GITHUB_TOKEN not set. Using 'gh' CLI instead.")
            self.use_gh_cli = True
        else:
            self.use_gh_cli = False

    def submit_entry(self, entry_path: Path, dry_run: bool = False) -> bool:
        """
        Submit knowledge entry to Shared KB via GitHub Issue.

        Args:
            entry_path: Path to YAML entry file
            dry_run: If True, print issue content without creating

        Returns:
            True if submission successful
        """
        print(f"📤 Submitting entry: {entry_path}")

        # Load YAML entry
        try:
            with open(entry_path, 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f)
        except Exception as e:
            print(f"❌ Error loading YAML: {e}")
            return False

        # Extract entry data
        entries = content.get('errors', []) or content.get('patterns', [])
        if not entries:
            print("❌ No entries found in YAML file")
            return False

        entry = entries[0]
        entry_id = entry.get('id', 'UNKNOWN')
        title = entry.get('title', 'No title')
        severity = entry.get('severity', 'unknown')
        scope = entry.get('scope', 'unknown')

        # Get repository info
        repo_url = self._get_git_remote_url()
        project_name = self._extract_project_name(repo_url)

        # Build issue title
        issue_title = f"[{project_name}] {entry_id}: {title}"

        # Build issue body from template
        issue_body = self._build_issue_body(entry, content, repo_url, entry_path)

        # Show preview
        print(f"\n{'='*60}")
        print(f"Issue Title: {issue_title}")
        print(f"{'='*60}")
        print(f"\n{issue_body}\n")
        print(f"{'='*60}\n")

        if dry_run:
            print("⚠ Dry run: Issue not created")
            return True

        # Create issue
        issue_number = self._create_github_issue(issue_title, issue_body)

        if issue_number:
            # Update local YAML with github metadata
            self._update_local_yaml(entry_path, issue_number, entry, repo_url)
            return True
        else:
            return False

    def _build_issue_body(self, entry: Dict, full_content: Dict, repo_url: str, entry_path: Path) -> str:
        """Build issue body from entry data."""
        entry_id = entry.get('id', 'UNKNOWN')
        title = entry.get('title', '')
        severity = entry.get('severity', 'unknown')
        scope = entry.get('scope', 'unknown')
        problem = entry.get('problem', '')[:500] + ('...' if len(entry.get('problem', '')) > 500 else '')
        solution = entry.get('solution', {})
        solution_code = solution.get('code', '')[:300] + ('...' if len(solution.get('code', '')) > 300 else '')
        solution_expl = solution.get('explanation', '')[:300] + ('...' if len(solution.get('explanation', '')) > 300 else '')

        # Get domain info if available
        domains = entry.get('domains', {})
        domain_str = domains.get('primary', 'none')
        if domains.get('secondary'):
            domain_str += f" + {', '.join(domains['secondary'])}"

        # Get repository info
        project_name = self._extract_project_name(repo_url)

        # Build issue body
        body = f"""## Knowledge Base Contribution

### Entry Information

**Entry ID:** {entry_id}
**Title:** {title}
**Severity:** {severity}
**Scope:** {scope}
**Domain:** {domain_str}

### Problem Description

{problem}

### Solution Summary

**Code:**
```python
{solution_code}
```

**Explanation:**
{solution_expl}
```

### Full Entry YAML

<details>
<summary>Click to expand full YAML entry</summary>

```yaml
{yaml.dump(full_content, allow_unicode=True, sort_keys=False)}
```

</details>

---

### Agent Attribution

**Agent Type:** claude-code
**Agent Version:** 4.5
**Source Repository:** {repo_url}
**Local KB Path:** {entry_path}
**Project:** {project_name}

---

### Curator Review

- [ ] Verify YAML syntax
- [ ] Check for duplicates
- [ ] Validate scope appropriateness
- [ ] Test solution (if applicable)
- [ ] Verify metadata completeness
- [ ] Assign appropriate labels

### Review Decision

Please review this contribution and add one of the following labels:

- **`approved`** - Ready to merge to Shared KB
- **`needs-revision`** - Changes needed before approval
- **`rejected`** - Not appropriate for Shared KB

Use `/approve`, `/request-changes`, or `/reject` commands to add labels.
"""
        return body

    def _create_github_issue(self, title: str, body: str) -> Optional[int]:
        """Create GitHub issue using gh CLI or API."""
        labels = ["contribution", "triage-needed", f"scope:python", "agent:claude-code"]

        if self.use_gh_cli:
            # Use gh CLI
            cmd = [
                'gh', 'issue', 'create',
                '--repo', self.SHARED_KB_REPO,
                '--title', title,
                '--body', body,
                '--label', ','.join(labels)
            ]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                # Extract issue number from output
                # Output format: https://github.com/ozand/shared-knowledge-base/issues/123
                output = result.stdout.strip()
                issue_number = int(output.split('/')[-1])

                print(f"✅ Issue created: {output}")
                return issue_number

            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to create issue: {e.stderr}")
                return None
        else:
            # TODO: Implement GitHub API call
            print("❌ GitHub API submission not yet implemented. Use GITHUB_TOKEN or install gh CLI")
            return None

    def _update_local_yaml(self, entry_path: Path, issue_number: int, entry: Dict, repo_url: str):
        """Update local YAML with GitHub metadata."""
        # Add github section if not exists
        if 'github' not in entry:
            entry['github'] = {}

        entry['github'].update({
            'issue_number': issue_number,
            'issue_url': f"https://github.com/{self.SHARED_KB_REPO}/issues/{issue_number}",
            'issue_status': 'pending',
            'contribution_date': subprocess.check_output(['date', '-I', 'minutes'], text=True).strip()
        })

        # Add agent attribution
        if 'agent_attribution' not in entry['github']:
            entry['github']['agent_attribution'] = {
                'agent_type': 'claude-code',
                'agent_version': '4.5',
                'source_repository': repo_url,
                'local_kb_path': str(entry_path)
            }

        # Load full YAML
        with open(entry_path, 'r') as f:
            content = yaml.safe_load(f)

        # Update entry
        entries = content.get('errors', []) or content.get('patterns', [])
        if entries:
            entries[0].update(entry)

        # Write back
        with open(entry_path, 'w') as f:
            yaml.safe_dump(content, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

        print(f"✅ Updated {entry_path} with GitHub metadata")

    def _get_git_remote_url(self) -> str:
        """Get git remote URL."""
        try:
            result = subprocess.run(
                ['git', 'config', '--get', 'remote.origin.url'],
                capture_output=True,
                text=True,
                check=True
            )
            url = result.stdout.strip()

            # Convert SSH to HTTPS URL
            if url.startswith('git@github.com:'):
                url = url.replace('git@github.com:', 'https://github.com/')
                url = url.replace('.git', '')

            return url
        except subprocess.CalledProcessError:
            return "unknown/unknown"

    def _extract_project_name(self, repo_url: str) -> str:
        """Extract project name from repo URL."""
        parts = repo_url.split('/')
        if len(parts) >= 2:
            return parts[-1].replace('.git', '')
        return "unknown-project"

    def check_status(self, issue_number: int) -> bool:
        """Check status of submitted issue."""
        print(f"🔍 Checking issue #{issue_number}...")

        cmd = ['gh', 'issue', 'view', str(issue_number), '--repo', self.SHARED_KB_REPO]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to get issue status: {e.stderr}")
            return False


def main():
    """CLI interface."""
    parser = argparse.ArgumentParser(
        description='Submit KB entries to Shared Knowledge Base',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Submit entry
  python tools/kb_submit.py submit --entry path/to/entry.yaml

  # Dry run (preview)
  python tools/kb_submit.py submit --entry path/to/entry.yaml --dry-run

  # Check issue status
  python tools/kb_submit.py status --issue 123
        """
    )

    parser.add_argument('--token', help='GitHub personal access token (or set GITHUB_TOKEN env var)')

    subparsers = parser.add_subparsers(dest='command', help='Command')

    # Submit command
    parser_submit = subparsers.add_parser('submit', help='Submit entry to Shared KB')
    parser_submit.add_argument('--entry', type=Path, required=True, help='Path to YAML entry')
    parser_submit.add_argument('--dry-run', action='store_true', help='Preview without creating issue')

    # Status command
    parser_status = subparsers.add_parser('status', help='Check issue status')
    parser_status.add_argument('--issue', type=int, required=True, help='Issue number')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    submitter = KBSubmitter(github_token=args.token)

    if args.command == 'submit':
        success = submitter.submit_entry(args.entry, dry_run=args.dry_run)
        return 0 if success else 1

    elif args.command == 'status':
        success = submitter.check_status(args.issue)
        return 0 if success else 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
