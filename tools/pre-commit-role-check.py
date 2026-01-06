#!/usr/bin/env python3
"""
Pre-commit hook: Block non-curators from modifying Shared KB

This hook enforces AGENT-ROLE-SEPARATION-001 by preventing
project agents from directly committing to shared-knowledge-base.

Installation:
    cp tools/pre-commit-role-check.py .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit

Usage:
    Automatically runs before each commit

To bypass (Curator only):
    touch .curator
    git commit
    rm .curator
"""

import os
import sys
import subprocess
from pathlib import Path


# Curator-only files and directories
CURATOR_PATHS = [
    "universal/",
    "python/",
    "postgresql/",
    "javascript/",
    "docker/",
    "framework/",
    "tools/",
    "curator/",
    "universal/agent-instructions/",
    "README.md",
    "VERSION",
    ".gitignore",
]


def is_curator():
    """Check if committer is Curator Agent"""
    # Method 1: Environment variable
    if os.getenv("AGENT_ROLE") == "curator":
        return True

    # Method 2: .curator flag file (in repo root)
    if Path(".curator").exists():
        return True

    # Method 3: Check if we're in shared-knowledge-base repo
    # If yes, require explicit .curator file
    cwd = Path.cwd()
    if (cwd / "universal").exists() and (cwd / "universal" / "patterns").exists():
        # We're in shared-knowledge-base repository
        return Path(".curator").exists()

    return False


def get_staged_files():
    """Get list of staged files"""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.strip().split("\n")
        return [f for f in files if f]  # Filter empty strings
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def check_curator_only_files(staged_files):
    """Check if staged files are curator-only"""
    violations = []

    for file in staged_files:
        for curator_path in CURATOR_PATHS:
            if file.startswith(curator_path):
                violations.append(file)
                break

    return violations


def print_error_message(violations):
    """Print detailed error message"""
    print("\n" + "=" * 70)
    print("❌ COMMIT BLOCKED: Curator-Only Files Modified")
    print("=" * 70)

    print("\n🚫 You are trying to modify Shared Knowledge Base files directly.")
    print("   This violates AGENT-ROLE-SEPARATION-001 pattern.")

    print("\n📋 Role Violation:")
    print("   • Your role: Project Agent")
    print("   • These files: Curator ONLY")

    print("\n❌ Forbidden Files:")
    for file in violations:
        print(f"   • {file}")

    print("\n✅ Correct Action (AGENT-HANDOFF-001):")
    print("   1. Create YAML entry with your pattern")
    print("   2. Validate locally:")
    print("      python tools/kb.py validate your-entry.yaml")
    print("   3. Create GitHub issue with attribution:")
    print("      gh issue create \\")
    print("        --label 'agent:claude-code' \\")
    print("        --label 'project:YOUR_PROJECT' \\")
    print("        --label 'agent-type:code-generation' \\")
    print("        --label 'kb-improvement' \\")
    print("        --title 'Add CATEGORY-NNN: Pattern Name' \\")
    print("        --body-file issue-template.md")

    print("\n📚 Documentation:")
    print("   • AGENT-ROLE-SEPARATION-001: Role separation pattern")
    print("   • AGENT-HANDOFF-001: Cross-repository collaboration")
    print("   • GITHUB-ATTRIB-001: GitHub attribution")

    print("\n💡 Why This Restriction?")
    print("   • Curator maintains quality control")
    print("   • Prevents validation errors")
    print("   • Ensures consistent KB structure")
    print("   • Curator reviews ALL contributions")

    print("\n🤖 If You Are Curator:")
    print("   touch .curator")
    print("   git commit")
    print("   rm .curator")

    print("\n" + "=" * 70 + "\n")


def main():
    """Main pre-commit check"""
    # Only check in shared-knowledge-base repository
    # Check for universal/patterns directory as indicator
    if not Path("universal/patterns").exists():
        return 0  # Not in shared-knowledge-base, allow commit

    # Allow Curator
    if is_curator():
        return 0  # Curator can commit anything

    # Check staged files
    staged_files = get_staged_files()

    if not staged_files:
        return 0  # No files staged

    # Check for curator-only files
    violations = check_curator_only_files(staged_files)

    if violations:
        print_error_message(violations)
        return 1  # Block commit

    # No violations, allow commit
    return 0


if __name__ == "__main__":
    sys.exit(main())
