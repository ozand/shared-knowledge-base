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
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Tuple, Dict

import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Try to import PyGithub for GitHub Issues integration
try:
    from github import Github
except ImportError:
    Github = None

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
# Use knowledge/ subdirectory for entries, but also create other standard dirs
PROJECT_KB_DIR = PROJECT_ROOT / ".kb" / "project" / "knowledge"
CONTEXT_FILE = PROJECT_ROOT / ".kb" / "context" / "PROJECT.yaml"


def ensure_project_kb_structure() -> None:
    """
    Ensure .kb/project/ directory structure exists.
    Creates standard subdirectories if missing.
    """
    project_kb_base = PROJECT_ROOT / ".kb" / "project"

    # Standard subdirectories
    subdirs = [
        project_kb_base / "knowledge",      # Main KB entries
        project_kb_base / "integrations",   # Integration configs
        project_kb_base / "endpoints",      # API endpoints
        project_kb_base / "decisions",      # Architectural decisions
        project_kb_base / "lessons",        # Lessons learned
        project_kb_base / "pending",        # Pending submissions
    ]

    for subdir in subdirs:
        subdir.mkdir(parents=True, exist_ok=True)

    # Create README if not exists
    readme_path = project_kb_base / "README.md"
    if not readme_path.exists():
        readme_content = """# Project Knowledge Base

This directory contains project-specific knowledge that should NOT be shared with the Shared KB.

## Directory Structure

### `knowledge/`
Knowledge entries submitted with `--target local`

### `integrations/`
Integration configurations and documentation

### `endpoints/`
API endpoints documentation

### `decisions/`
Architectural decisions (ADR)

### `lessons/`
Lessons learned from bugs and fixes

### `pending/`
Temporary storage for draft entries

## Important

⚠️ **Never commit secrets!** Use templates instead.
⚠️ **Never share business logic!** Keep project-specific knowledge here.
"""
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)


def load_project_context() -> Dict[str, Any]:
    """Load project context from PROJECT.yaml"""
    if CONTEXT_FILE.exists():
        try:
            with open(CONTEXT_FILE, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Could not load PROJECT.yaml: {e}")
    return {}


def ensure_github_token() -> str:
    """Ensure GITHUB_TOKEN is available in environment"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logger.error("GITHUB_TOKEN not found in environment")
        print("❌ Error: GITHUB_TOKEN not found in environment")
        print("   For submissions to Shared KB, a token is required.")
        print("   Add it to your .env file: GITHUB_TOKEN=ghp_your_token")
        sys.exit(1)
    return token


def validate_yaml_content(yaml_content: str) -> Tuple[bool, str, int]:
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


def create_issue_body(meta: Dict[str, Any], content: str, context: Dict[str, Any]) -> str:
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


def submit_local(file_path: Path, auto_commit: bool = False) -> None:
    """
    Save knowledge entry to local Project KB.

    Args:
        file_path: Path to YAML file to save
        auto_commit: Whether to automatically commit to git
    """
    # Ensure structure exists first
    ensure_project_kb_structure()

    # Determine target path based on category or default to knowledge/
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        data = yaml.safe_load(content) if content else {}

    # Extract category to determine subdirectory
    category = data.get('category', 'general')

    # Map categories to subdirectories
    category_map = {
        'integration': 'integrations',
        'integrations': 'integrations',
        'endpoint': 'endpoints',
        'api': 'endpoints',
        'decision': 'decisions',
        'adr': 'decisions',
        'lesson': 'lessons',
        'lesson-learned': 'lessons',
    }

    subdir = category_map.get(category.lower(), 'knowledge')
    target_dir = PROJECT_ROOT / ".kb" / "project" / subdir
    target_path = target_dir / file_path.name

    # Create directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)

    # Write file
    with open(target_path, 'w', encoding='utf-8') as dst:
        dst.write(content)

    rel_path = target_path.relative_to(PROJECT_ROOT)
    logger.info(f"Local KB entry saved: {rel_path}")
    print(f"✅ [Local] File saved: {rel_path}")

    if auto_commit:
        try:
            print("⏳ Auto-committing to git...")
            subprocess.run(["git", "add", str(target_path)], check=True, cwd=PROJECT_ROOT)
            subprocess.run(
                ["git", "commit", "-m", f"chore(kb): Add entry {file_path.name}"],
                check=True,
                cwd=PROJECT_ROOT
            )
            print(f"✅ [Git] Committed: {file_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Git commit failed: {e}")
            print("   Please commit manually.")
    else:
        print("   Don't forget to commit to your project repository:")
        print(f"   git add {rel_path} && git commit -m 'Add KB entry: {file_path.name}'")



def submit_shared(file_path: Path, title: str, description: str, domain: str) -> None:
    """
    Submit knowledge entry to Shared KB via GitHub Issue.

    Args:
        file_path: Path to YAML file
        title: Issue title
        description: Problem description
        domain: Knowledge domain (docker, python, etc.)
    """
    if not Github:
        logger.error("PyGithub library not installed")
        print("❌ Error: PyGithub library not installed")
        print("   Install it: pip install PyGithub")
        sys.exit(1)

    # Validate content first
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    is_valid, message, score = validate_yaml_content(content)

    if not is_valid:
        logger.error(f"Validation failed: {message}")
        print(f"❌ Validation failed: {message}")
        print("   Please fix the YAML content before submitting.")
        sys.exit(1)

    logger.info(f"Validation passed: {message}")
    print(f"✅ Validation passed: {message}")

    if score < 75:
        logger.warning(f"Quality score ({score}) is below 75")
        print(f"⚠️  Warning: Quality score ({score}) is below 75")
        response = input("   Continue anyway? (y/N): ")
        if response.lower() != 'y':
            logger.info("Submission cancelled by user due to low quality score")
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
        logger.error(f"Error accessing repository {repo_name}: {e}")
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

        logger.info(f"GitHub issue created: #{issue.number} - {issue.html_url}")
        print(f"✅ [Shared] Issue created: #{issue.number}")
        print(f"   URL: {issue.html_url}")
        print("   The curator will review your submission soon.")

    except Exception as e:
        logger.error(f"Error creating GitHub issue: {e}")
        print(f"❌ Error creating issue: {e}")
        sys.exit(1)


def main() -> None:
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

    parser.add_argument(
        "--commit",
        action="store_true",
        help="Automatically commit to git (for --target local)"
    )

    args = parser.parse_args()

    # Check if file exists
    if not args.file.exists():
        logger.error(f"File not found: {args.file}")
        print(f"❌ File not found: {args.file}")
        sys.exit(1)

    # Route to appropriate function
    if args.target == "local":
        submit_local(args.file, args.commit)

    elif args.target == "shared":

        if not args.title:
            logger.error("--title is required for --target shared")
            print("❌ Error: --title is required for --target shared")
            print("   Example: --title 'Docker compose healthcheck fix'")
            sys.exit(1)
        submit_shared(args.file, args.title, args.desc, args.domain)


if __name__ == "__main__":
    main()
