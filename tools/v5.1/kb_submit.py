#!/usr/bin/env python3
"""
kb_submit.py - Submit knowledge entries to Project KB or Shared KB

Usage:
    python tools/v5.1/kb_submit.py --target local --file solution.yaml
    python tools/v5.1/kb_submit.py --target shared --file solution.yaml --title "Issue title"

Version: 5.1.0
"""

import os
import sys
import argparse
import yaml
from datetime import datetime
from pathlib import Path

# Try to import PyGithub for GitHub Issues integration
try:
    from github import Github
except ImportError:
    Github = None

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROJECT_KB_DIR = PROJECT_ROOT / ".kb" / "project" / "knowledge"
CONTEXT_FILE = PROJECT_ROOT / ".kb" / "context" / "PROJECT.yaml"


def load_project_context():
    """Load project context from PROJECT.yaml"""
    if CONTEXT_FILE.exists():
        try:
            with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️  Warning: Could not load PROJECT.yaml: {e}")
    return {}


def ensure_github_token():
    """Ensure GITHUB_TOKEN is available in environment"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ Error: GITHUB_TOKEN not found in environment")
        print("   For submissions to Shared KB, a token is required.")
        print("   Add it to your .env file: GITHUB_TOKEN=ghp_your_token")
        sys.exit(1)
    return token


def validate_yaml_content(yaml_content):
    """
    Validate YAML content before submission.

    Returns:
        tuple: (is_valid, message, score)
    """
    try:
        data = yaml.safe_load(yaml_content)

        # Required fields check
        required_fields = ['version', 'category']
        missing = [f for f in required_fields if f not in data]

        if missing:
            return False, f"Missing required fields: {', '.join(missing)}", 0

        # Check for errors or patterns
        entries = data.get('errors', []) or data.get('patterns', [])
        if not entries:
            return False, "No 'errors' or 'patterns' entries found", 0

        entry = entries[0]

        # Quality score calculation
        score = 0

        # Basic structure (40 points)
        if 'version' in data:
            score += 10
        if 'category' in data:
            score += 10
        if 'last_updated' in data:
            score += 20

        # Entry quality (40 points)
        if entry.get('problem'):
            score += 10
        if entry.get('solution', {}).get('code'):
            score += 15
        if entry.get('solution', {}).get('explanation'):
            score += 15

        # Metadata (20 points)
        if entry.get('scope'):
            score += 10
        if entry.get('severity'):
            score += 10

        return True, f"Quality score: {score}/100", score

    except yaml.YAMLError as e:
        return False, f"YAML parsing error: {e}", 0
    except Exception as e:
        return False, f"Validation error: {e}", 0


def create_issue_body(meta, content, context):
    """
    Generate GitHub Issue body with metadata for curator.

    Args:
        meta: Metadata dictionary
        content: YAML content string
        context: Project context dictionary

    Returns:
        str: Formatted issue body
    """
    return f"""---
submission_meta:
  domain: {meta.get('domain', 'universal')}
  type: {meta.get('type', 'pattern')}
  project_source: {context.get('meta', {}).get('id', 'unknown')}
  agent_id: {os.getenv('CLAUDE_SESSION_ID', 'manual')}
  timestamp: {datetime.utcnow().isoformat()}Z
  verified: {meta.get('verified', 'true')}
---

### Problem Description
{meta.get('description', 'No description provided')}

### Proposed Entry
```yaml
{content}
```

### Context
- **Project:** {context.get('meta', {}).get('name', 'Unknown')}
- **Problem encountered:** {meta.get('description', 'N/A')}
- **Solution verified:** {meta.get('verified', 'true')}
"""


def submit_local(file_path):
    """
    Save knowledge entry to local Project KB.

    Args:
        file_path: Path to YAML file to save
    """
    target_path = PROJECT_KB_DIR / file_path.name

    # Create directory if it doesn't exist
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # Copy file content
    with open(file_path, 'r', encoding='utf-8') as src:
        content = src.read()

    with open(target_path, 'w', encoding='utf-8') as dst:
        dst.write(content)

    print(f"✅ [Local] File saved: .kb/project/knowledge/{file_path.name}")
    print("   Don't forget to commit to your project repository:")
    print("   git add .kb/project/knowledge/{} && git commit -m 'Add KB entry'".format(file_path.name))


def submit_shared(file_path, title, description, domain):
    """
    Submit knowledge entry to Shared KB via GitHub Issue.

    Args:
        file_path: Path to YAML file
        title: Issue title
        description: Problem description
        domain: Knowledge domain (docker, python, etc.)
    """
    if not Github:
        print("❌ Error: PyGithub library not installed")
        print("   Install it: pip install PyGithub")
        sys.exit(1)

    # Validate content first
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    is_valid, message, score = validate_yaml_content(content)

    if not is_valid:
        print(f"❌ Validation failed: {message}")
        print("   Please fix the YAML content before submitting.")
        sys.exit(1)

    print(f"✅ Validation passed: {message}")

    if score < 75:
        print(f"⚠️  Warning: Quality score ({score}) is below 75")
        response = input("   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("   Submission cancelled.")
            sys.exit(0)

    # Get GitHub token
    token = ensure_github_token()

    # Initialize GitHub client
    g = Github(token)

    # Get repository from environment or use default
    repo_name = os.getenv("SHARED_KB_REPO", "ozand/shared-knowledge-base")

    try:
        repo = g.get_repo(repo_name)
    except Exception as e:
        print(f"❌ Error accessing repository {repo_name}: {e}")
        print("   Check SHARED_KB_REPO environment variable")
        sys.exit(1)

    # Load project context
    context = load_project_context()

    # Build metadata
    meta = {
        "domain": domain,
        "type": "error-solution",
        "description": description,
        "verified": "true"
    }

    # Create issue body
    body = create_issue_body(meta, content, context)

    # Create labels
    labels = ["kb-submission", "needs-review", domain]

    try:
        # Create issue
        issue = repo.create_issue(
            title=f"[KB Submission] {title}",
            body=body,
            labels=labels
        )

        print(f"✅ [Shared] Issue created: #{issue.number}")
        print(f"   URL: {issue.html_url}")
        print("   The curator will review your submission soon.")

    except Exception as e:
        print(f"❌ Error creating issue: {e}")
        sys.exit(1)


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(
        description="Knowledge Base Submission Tool v5.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Save to local Project KB
  python tools/v5.1/kb_submit.py --target local --file solution.yaml

  # Submit to Shared KB via GitHub Issue
  python tools/v5.1/kb_submit.py --target shared \\
      --file solution.yaml \\
      --title "Docker compose healthcheck" \\
      --desc "Container becomes healthy before DB is ready" \\
      --domain docker
        """
    )

    parser.add_argument(
        "--target",
        choices=["local", "shared"],
        required=True,
        help="Where to save: 'local' for Project KB, 'shared' for Shared KB"
    )

    parser.add_argument(
        "--file",
        type=Path,
        required=True,
        help="Path to YAML file with knowledge entry"
    )

    # Arguments for shared submissions
    parser.add_argument(
        "--title",
        help="Issue title (required for --target shared)"
    )

    parser.add_argument(
        "--desc",
        default="",
        help="Problem description (for --target shared)"
    )

    parser.add_argument(
        "--domain",
        default="universal",
        help="Knowledge domain: docker, python, postgresql, etc. (default: universal)"
    )

    parser.add_argument(
        "--verified",
        action="store_true",
        help="Mark solution as verified (default: true)"
    )

    args = parser.parse_args()

    # Check if file exists
    if not args.file.exists():
        print(f"❌ File not found: {args.file}")
        sys.exit(1)

    # Route to appropriate function
    if args.target == "local":
        submit_local(args.file)

    elif args.target == "shared":
        if not args.title:
            print("❌ Error: --title is required for --target shared")
            print("   Example: --title 'Docker compose healthcheck fix'")
            sys.exit(1)
        submit_shared(args.file, args.title, args.desc, args.domain)


if __name__ == "__main__":
    main()
