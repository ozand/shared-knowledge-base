#!/usr/bin/env python3
"""
kb_curate.py - Curator tool for processing KB submission Issues

Usage:
    python tools/v5.1/kb_curate.py --mode list
    python tools/v5.1/kb_curate.py --mode validate --issue 123
    python tools/v5.1/kb_curate.py --mode approve --issue 123
    python tools/v5.1/kb_curate.py --mode reject --issue 123 --reason "Duplicate"

Version: 5.1.0
"""

import os
import sys
import argparse
import yaml
import re
import subprocess
import logging
from pathlib import Path
from typing import Optional, Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Try to import PyGithub
try:
    from github import Github
except ImportError:
    Github = None
    logger.error("PyGithub library not installed")
    print("❌ Error: PyGithub library not installed")
    print("   Install it: pip install PyGithub")
    sys.exit(1)


# --- Configuration ---
DEFAULT_REPO = os.getenv("SHARED_KB_REPO", "ozand/shared-knowledge-base")
SUBMISSION_LABEL = "kb-submission"
NEEDS_REVIEW_LABEL = "needs-review"


def get_github_client() -> 'Github':
    """Initialize and return GitHub client"""
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        logger.error("GITHUB_TOKEN not found in environment")
        print("❌ Error: GITHUB_TOKEN not found in environment")
        print("   Set it: export GITHUB_TOKEN=ghp_your_token")
        sys.exit(1)

    return Github(token)


def extract_yaml_frontmatter(issue_body: str) -> Tuple[Optional[Dict], Optional[str]]:
    """
    Extract YAML frontmatter from GitHub Issue body.

    Args:
        issue_body: Issue body text

    Returns:
        Tuple of (metadata_dict, yaml_content) or (None, None) if not found
    """
    # Check for YAML frontmatter (between --- markers)
    if '---' not in issue_body:
        return None, None

    parts = issue_body.split('---')

    if len(parts) < 3:
        return None, None

    try:
        # Parse metadata (first YAML block)
        metadata = yaml.safe_load(parts[1])

        # Extract YAML content (between ```yaml and ```)
        content_match = re.search(r'```yaml\n(.*?)\n```', issue_body, re.DOTALL)

        yaml_content = content_match.group(1) if content_match else None

        return metadata, yaml_content

    except Exception as e:
        logger.error(f"Error parsing YAML: {e}")
        return None, None


def calculate_quality_score(entry: Dict) -> int:
    """
    Calculate quality score for KB entry.

    Args:
        entry: Parsed YAML entry dictionary

    Returns:
        Quality score (0-100)
    """
    score = 0

    # Basic structure (40 points)
    if 'version' in entry:
        score += 10
    if 'category' in entry:
        score += 10
    if 'last_updated' in entry:
        score += 20

    # Check for errors or patterns
    entries = entry.get('errors', []) or entry.get('patterns', [])
    if not entries:
        return score  # Return early if no entries

    item = entries[0]

    # Entry quality (40 points)
    if item.get('problem'):
        score += 10
    if item.get('solution', {}).get('code'):
        score += 15
    if item.get('solution', {}).get('explanation'):
        score += 15

    # Metadata (20 points)
    if item.get('scope'):
        score += 10
    if item.get('severity'):
        score += 10

    return score


def validate_entry(entry: Dict) -> Tuple[bool, List[str]]:
    """
    Validate KB entry.

    Args:
        entry: Parsed YAML entry dictionary

    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []

    # Check required fields
    required_fields = ['version', 'category']
    for field in required_fields:
        if field not in entry:
            issues.append(f"Missing required field: {field}")

    # Check for errors or patterns
    entries = entry.get('errors', []) or entry.get('patterns', [])
    if not entries:
        issues.append("No 'errors' or 'patterns' found")
    else:
        item = entries[0]

        # Check entry fields
        if not item.get('problem'):
            issues.append("Missing 'problem' field in entry")

        if not item.get('solution'):
            issues.append("Missing 'solution' field in entry")
        else:
            if not item['solution'].get('code'):
                issues.append("Missing 'solution.code' field")
            if not item['solution'].get('explanation'):
                issues.append("Missing 'solution.explanation' field")

    return len(issues) == 0, issues


def list_submissions(g: 'Github', repo_name: str) -> None:
    """
    List all open kb-submission Issues.

    Args:
        g: GitHub client
        repo_name: Repository name (org/repo)
    """
    try:
        repo = g.get_repo(repo_name)

        # Get issues with submission label
        issues = repo.get_issues(
            labels=[SUBMISSION_LABEL],
            state='open'
        )

        issue_list = list(issues)

        if not issue_list:
            logger.info(f"No pending submissions found in {repo_name}")
            print(f"✅ No pending submissions found in {repo_name}")
            return

        print(f"📋 Pending Submissions ({len(issue_list)})\n")

        for issue in issue_list:
            # Extract metadata
            metadata, _ = extract_yaml_frontmatter(issue.body)

            if metadata:
                print(f"Issue #{issue.number}: {issue.title}")
                print(f"  Domain: {metadata.get('domain', 'unknown')}")
                print(f"  Type: {metadata.get('type', 'unknown')}")
                print(f"  Project: {metadata.get('project_source', 'unknown')}")
                print(f"  URL: {issue.html_url}")
            else:
                print(f"Issue #{issue.number}: {issue.title}")
                print(f"  ⚠️  Warning: Could not parse metadata")

            print()

    except Exception as e:
        logger.error(f"Error fetching submissions: {e}")
        print(f"❌ Error fetching submissions: {e}")


def validate_submission(g: 'Github', repo_name: str, issue_number: int) -> None:
    """
    Validate a specific submission Issue.

    Args:
        g: GitHub client
        repo_name: Repository name
        issue_number: Issue number
    """
    try:
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(issue_number)

        logger.info(f"Validating Issue #{issue_number}: {issue.title}")
        print(f"🔍 Validating Issue #{issue_number}: {issue.title}\n")

        # Extract metadata and content
        metadata, yaml_content = extract_yaml_frontmatter(issue.body)

        if not metadata or not yaml_content:
            logger.error("Could not extract YAML content from issue")
            print("❌ Validation failed: Could not extract YAML content")
            print("   Issue body may be malformed")
            return

        print("✅ Metadata extracted successfully")
        print(f"   Domain: {metadata.get('domain', 'unknown')}")
        print(f"   Type: {metadata.get('type', 'unknown')}")
        print(f"   Project: {metadata.get('project_source', 'unknown')}")

        # Parse YAML entry
        try:
            entry = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {e}")
            print(f"\n❌ YAML parsing error: {e}")
            return

        logger.info("YAML syntax validated successfully")
        print("\n✅ YAML syntax is valid")

        # Validate entry
        is_valid, issues = validate_entry(entry)

        if not is_valid:
            logger.warning(f"Validation failed: {len(issues)} issues")
            print("\n❌ Validation failed:")
            for issue_text in issues:
                print(f"   - {issue_text}")
        else:
            logger.info("All required fields present")
            print("\n✅ All required fields present")

        # Calculate quality score
        score = calculate_quality_score(entry)
        logger.info(f"Quality score: {score}/100")
        print(f"\n📊 Quality Score: {score}/100")

        if score >= 75:
            logger.info("Meets quality threshold")
            print("   ✅ Meets quality threshold (>= 75)")
        else:
            logger.warning(f"Below quality threshold: {score}/100")
            print("   ⚠️  Below quality threshold (>= 75)")

        # Check for duplicates (basic check)
        print("\n🔍 Duplicate check:")
        print("   ⚠️  Manual review required")
        print("   Run: kb_search.py \"<keywords>\" to check for duplicates")

    except Exception as e:
        logger.error(f"Error validating submission: {e}")
        print(f"❌ Error validating submission: {e}")


def approve_submission(g: 'Github', repo_name: str, issue_number: int) -> None:
    """
    Approve and commit submission to Shared KB.

    Args:
        g: GitHub client
        repo_name: Repository name
        issue_number: Issue number
    """
    try:
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(issue_number)

        logger.info(f"Approving Issue #{issue_number}: {issue.title}")
        print(f"✅ Approving Issue #{issue_number}: {issue.title}\n")

        # Extract metadata and content
        metadata, yaml_content = extract_yaml_frontmatter(issue.body)

        if not yaml_content:
            logger.error("Could not extract YAML content")
            print("❌ Error: Could not extract YAML content")
            return

        # Parse YAML to determine domain
        try:
            entry = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {e}")
            print(f"❌ YAML parsing error: {e}")
            return

        # Determine domain from entry
        entries = entry.get('errors', []) or entry.get('patterns', [])
        if not entries:
            logger.error("No entries found in YAML")
            print("❌ Error: No entries found in YAML")
            return

        item = entries[0]
        scope = item.get('scope', 'universal')

        # Map scope to domain directory
        domain_dirs = {
            'docker': 'docker',
            'python': 'python',
            'javascript': 'javascript',
            'postgresql': 'postgresql',
            'universal': 'universal',
            'catalog': 'catalog',
            'claude-code': 'claude-code'
        }

        domain = metadata.get('domain', domain_dirs.get(scope, 'universal'))

        # Get entry ID for filename
        entry_id = item.get('id', 'UNKNOWN')
        category = entry.get('category', 'general')

        # Create filename: CATEGORY-ID.yaml
        filename = f"{category}-{entry_id}.yaml"

        # Full path to domain directory
        domain_path = Path.cwd() / "domains" / domain

        # Create directory if it doesn't exist
        domain_path.mkdir(parents=True, exist_ok=True)

        # Full file path
        file_path = domain_path / filename

        # Write YAML content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)

        logger.info(f"Created file: {file_path} in domain: {domain}")
        print(f"📁 Domain: {domain}")
        print(f"📝 Created file: {file_path}")

        # Add to git
        import subprocess
        try:
            subprocess.run(['git', 'add', str(file_path)], check=True, capture_output=True)
            logger.info(f"Added to git: {filename}")
            print(f"✅ Added to git: {filename}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Could not add to git: {e}")
            print(f"⚠️  Warning: Could not add to git: {e}")

        # Add success comment and close issue
        issue.create_comment(
            "✅ **Approved**\n\n"
            "This submission has been validated and added to the Shared KB.\n\n"
            f"**Domain:** {domain}\n"
            f"**File:** {filename}\n"
            f"**Issue:** #{issue_number}\n\n"
            "The changes have been staged in git and will be committed after review.\n\n"
            "Thank you for your contribution!"
        )

        # Remove 'needs-review' label, add 'approved' label
        issue.remove_from_labels(NEEDS_REVIEW_LABEL)
        issue.add_to_labels('approved')

        # Close issue
        issue.edit(state='closed')

        logger.info(f"Issue #{issue_number} closed successfully")
        print(f"\n✅ Issue #{issue_number} closed")
        print(f"   Comment added, labels updated")
        print(f"\n📝 Next steps:")
        print(f"   1. Review the staged file: git status")
        print(f"   2. Commit changes: git commit -m 'Add {filename}'")
        print(f"   3. Push to main: git push origin main")

    except Exception as e:
        logger.error(f"Error approving submission: {e}")
        print(f"❌ Error approving submission: {e}")


def reject_submission(g: 'Github', repo_name: str, issue_number: int, reason: str) -> None:
    """
    Reject submission with feedback.

    Args:
        g: GitHub client
        repo_name: Repository name
        issue_number: Issue number
        reason: Rejection reason
    """
    try:
        repo = g.get_repo(repo_name)
        issue = repo.get_issue(issue_number)

        logger.info(f"Rejecting Issue #{issue_number}: {issue.title} - Reason: {reason}")
        print(f"❌ Rejecting Issue #{issue_number}: {issue.title}\n")

        # Add rejection comment
        comment = (
            "❌ **Changes Requested**\n\n"
            f"**Reason:** {reason}\n\n"
            "Please address the feedback and resubmit if applicable.\n\n"
            "Thank you for your contribution!"
        )

        issue.create_comment(comment)

        # Update labels
        issue.remove_from_labels(NEEDS_REVIEW_LABEL)
        issue.add_to_labels('rejected')

        # Close issue
        issue.edit(state='closed')

        logger.info(f"Issue #{issue_number} rejected and closed")
        print(f"✅ Issue #{issue_number} rejected and closed")
        print(f"   Reason: {reason}")

    except Exception as e:
        logger.error(f"Error rejecting submission: {e}")
        print(f"❌ Error rejecting submission: {e}")


def main() -> None:
    """CLI interface"""
    parser = argparse.ArgumentParser(
        description="Knowledge Base Curator Tool v5.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List pending submissions
  python tools/v5.1/kb_curate.py --mode list

  # Validate specific submission
  python tools/v5.1/kb_curate.py --mode validate --issue 123

  # Approve submission
  python tools/v5.1/kb_curate.py --mode approve --issue 123

  # Reject submission
  python tools/v5.1/kb_curate.py --mode reject --issue 123 \\
      --reason "Duplicate of existing entry"
        """
    )

    parser.add_argument(
        "--mode",
        choices=["list", "validate", "approve", "reject"],
        required=True,
        help="Operation mode"
    )

    parser.add_argument(
        "--issue",
        type=int,
        help="Issue number (required for validate, approve, reject)"
    )

    parser.add_argument(
        "--reason",
        help="Rejection reason (required for --mode reject)"
    )

    args = parser.parse_args()

    # Validate arguments
    if args.mode in ["validate", "approve", "reject"]:
        if not args.issue:
            logger.error(f"--issue is required for --mode {args.mode}")
            print(f"❌ Error: --issue is required for --mode {args.mode}")
            return 1

    if args.mode == "reject" and not args.reason:
        logger.error("--reason is required for --mode reject")
        print("❌ Error: --reason is required for --mode reject")
        return 1

    # Get GitHub client
    g = get_github_client()

    # Execute command
    if args.mode == "list":
        list_submissions(g, DEFAULT_REPO)

    elif args.mode == "validate":
        validate_submission(g, DEFAULT_REPO, args.issue)

    elif args.mode == "approve":
        approve_submission(g, DEFAULT_REPO, args.issue)

    elif args.mode == "reject":
        reject_submission(g, DEFAULT_REPO, args.issue, args.reason)

    return 0


if __name__ == "__main__":
    sys.exit(main())
