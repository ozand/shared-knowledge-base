#!/usr/bin/env python3
"""
Unified Shared KB Installation Script

Cross-platform installation and update script for Shared Knowledge Base.
Works on Linux, macOS, and Windows without encoding issues.

Usage:
    python unified-install.py --full        # Full installation (new project)
    python unified-install.py --minimal     # Minimal installation
    python unified-install.py --update      # Update existing project
    python unified-install.py --interactive # Interactive mode
    python unified-install.py --check       # Check for updates

This script harmonizes all installation approaches:
- Replaces setup-shared-kb-sparse.sh/ps1
- Replaces install-sku.sh/ps1
- Replaces for-projects/scripts/install.py
- Provides unified cross-platform solution
"""

import os
import sys
import shutil
import argparse
import subprocess
import json
from pathlib import Path
from typing import List, Tuple, Optional
import urllib.request

# ANSI colors for cross-platform terminal output
class Colors:
    """Cross-platform color codes"""
    if sys.platform == "win32":
        # Windows: use ANSI escape sequences (Windows 10+)
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BLUE = '\033[94m'
        BOLD = '\033[1m'
        END = '\033[0m'
    else:
        # Unix-like: standard ANSI codes
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BLUE = '\033[94m'
        BOLD = '\033[1m'
        END = '\033[0m'

# ASCII replacements for emoji (avoid encoding issues)
ASCII = {
    'OK': '[OK]',
    'X': '[X]',
    '!': '[!]',
    '->': '->',
    'INFO': '[INFO]',
    'SUCCESS': '[SUCCESS]',
    'ERROR': '[ERROR]',
    'WARNING': '[WARNING]',
}

def print_success(msg: str):
    print(f"{Colors.GREEN}{ASCII['OK']} {msg}{Colors.END}")

def print_error(msg: str):
    print(f"{Colors.RED}{ASCII['ERROR']} {msg}{Colors.END}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}{ASCII['!']} {msg}{Colors.END}")

def print_info(msg: str):
    print(f"{Colors.BLUE}{ASCII['INFO']} {msg}{Colors.END}")

def print_header(msg: str):
    print(f"\n{Colors.BOLD}{msg}{Colors.END}")

def get_paths() -> dict:
    """Get all relevant paths for installation."""
    project_root = Path.cwd()
    shared_kb_path = project_root / "docs/knowledge-base/shared"

    return {
        "project_root": project_root,
        "shared_kb": shared_kb_path,
        "claude_dir": project_root / ".claude",
        "local_kb": project_root / "docs/knowledge-base",
        "agents_dir": project_root / ".claude/agents",
        "skills_dir": project_root / ".claude/skills",
        "commands_dir": project_root / ".claude/commands",
    }

def check_python_version() -> bool:
    """Check if Python version is 3.8+"""
    print_header("Checking Python Version")

    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python 3.8+ required, found {version.major}.{version.minor}.{version.micro}")
        return False

def check_existing_installation(paths: dict) -> dict:
    """Check if Shared KB is already installed."""
    print_header("Checking Existing Installation")

    status = {
        "submodule_exists": False,
        "sparse_configured": False,
        "agents_installed": False,
        "skills_installed": False,
        "commands_installed": False,
        "index_built": False,
    }

    # Check submodule
    if paths["shared_kb"].exists():
        status["submodule_exists"] = True
        print_info(f"Submodule exists: {paths['shared_kb']}")

        # Check sparse checkout
        git_dir = paths["project_root"] / ".git" / "modules" / "docs" / "knowledge-base" / "shared"
        if git_dir.exists():
            sparse_file = git_dir / "info" / "sparse-checkout"
            if sparse_file.exists():
                status["sparse_configured"] = True
                print_success("Sparse checkout configured")

    # Check agents
    if paths["agents_dir"].exists():
        agent_files = list(paths["agents_dir"].rglob("*.md"))
        if agent_files:
            status["agents_installed"] = True
            print_success(f"Agents: {len(agent_files)} files")

    # Check skills
    if paths["skills_dir"].exists():
        skill_dirs = [d for d in paths["skills_dir"].iterdir() if d.is_dir() and not d.name.startswith('.')]
        if skill_dirs:
            status["skills_installed"] = True
            print_success(f"Skills: {len(skill_dirs)} skills")

    # Check commands
    if paths["commands_dir"].exists():
        command_files = list(paths["commands_dir"].glob("*.md"))
        if command_files:
            status["commands_installed"] = True
            print_success(f"Commands: {len(command_files)} commands")

    # Check index
    index_file = paths["shared_kb"] / "_index.yaml"
    if index_file.exists():
        status["index_built"] = True
        print_success("Index built")

    return status

def add_submodule(paths: dict) -> bool:
    """Add shared-knowledge-base as git submodule."""
    print_header("Adding Git Submodule")

    # Check if already exists
    if paths["shared_kb"].exists():
        print_warning("Submodule already exists")
        return True

    try:
        # Create parent directory
        paths["shared_kb"].parent.mkdir(parents=True, exist_ok=True)

        # Add submodule
        print_info("Adding submodule...")
        subprocess.run([
            "git", "submodule", "add",
            "https://github.com/ozand/shared-knowledge-base.git",
            str(paths["shared_kb"])
        ], check=True, capture_output=True)

        print_success("Submodule added")
        return True

    except subprocess.CalledProcessError as e:
        print_error(f"Failed to add submodule: {e}")
        return False

def setup_sparse_checkout(paths: dict) -> bool:
    """Configure sparse checkout to exclude curator files."""
    print_header("Configuring Sparse Checkout")

    try:
        # Enable sparse checkout
        print_info("Enabling sparse checkout...")
        subprocess.run([
            "git", "config", "core.sparseCheckout", "true"
        ], cwd=paths["shared_kb"], check=True, capture_output=True)

        # Create sparse-checkout configuration
        git_dir = paths["project_root"] / ".git" / "modules" / "docs" / "knowledge-base" / "shared"
        if not git_dir.exists():
            # Git submodule stores .git in parent repo
            git_dir = paths["project_root"] / ".git" / "modules" / "docs" / "knowledge-base" / "shared"

        info_dir = git_dir / "info"
        info_dir.mkdir(parents=True, exist_ok=True)

        sparse_file = info_dir / "sparse-checkout"

        sparse_config = """# Core documentation
README.md
GUIDE.md
QUICKSTART.md
README_INTEGRATION.md

# Agent guides
AGENT_INTEGRATION_GUIDE.md
AGENT_AUTOCONFIG_GUIDE.md
ROLE_SEPARATION_GUIDE.md

# Patterns (MAIN CONTENT - what agents need)
universal/
python/
postgresql/
docker/
javascript/
vps/

# Tools
tools/
scripts/

# Integration templates
for-projects/

# Base configuration
.kb-config.yaml
.gitignore.agents
.kb-version
"""

        with open(sparse_file, 'w') as f:
            f.write(sparse_config)

        print_success("Sparse checkout configured")

        # Pull only specified content
        print_info("Pulling specified content...")
        subprocess.run(["git", "pull", "origin", "main"],
                       cwd=paths["shared_kb"], check=True, capture_output=True)

        print_success("Content pulled (curator excluded)")
        return True

    except Exception as e:
        print_error(f"Failed to configure sparse checkout: {e}")
        return False

def install_agents(paths: dict, full: bool = True) -> bool:
    """Install agent templates."""
    print_header("Installing Agents")

    agents_src = paths["shared_kb"] / "for-projects" / "agent-templates"

    if not agents_src.exists():
        print_warning("Agent templates not found (skipping)")
        return True

    try:
        # Create agents directory
        paths["agents_dir"].mkdir(parents=True, exist_ok=True)

        # Copy subagents
        subagents_src = agents_src / "subagents"
        subagents_dst = paths["agents_dir"] / "subagents"

        if subagents_src.exists():
            shutil.copytree(subagents_src, subagents_dst, dirs_exist_ok=True)
            subagent_count = len(list(subagents_dst.glob("*.md")))
            print_success(f"Subagents: {subagent_count} files")

        # Copy kb-agent if exists
        kb_agent_src = agents_src / "kb-agent.md"
        if kb_agent_src.exists():
            shutil.copy(kb_agent_src, paths["agents_dir"] / "kb-agent.md")
            print_success("KB agent installed")

        return True

    except Exception as e:
        print_error(f"Failed to install agents: {e}")
        return False

def install_skills(paths: dict, full: bool = True) -> bool:
    """Install skill templates."""
    print_header("Installing Skills")

    skills_src = paths["shared_kb"] / "for-projects" / "skill-templates"

    if not skills_src.exists():
        print_warning("Skill templates not found (skipping)")
        return True

    try:
        paths["skills_dir"].mkdir(parents=True, exist_ok=True)

        if full:
            # Install all skills
            for skill_dir in skills_src.iterdir():
                if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                    skill_dst = paths["skills_dir"] / skill_dir.name
                    shutil.copytree(skill_dir, skill_dst, dirs_exist_ok=True)

            skill_count = len([d for d in paths["skills_dir"].iterdir() if d.is_dir()])
            print_success(f"All skills: {skill_count} skills")
        else:
            # Install core skills only
            core_skills = ["kb-search", "kb-validate", "kb-index", "kb-create"]
            for skill_name in core_skills:
                skill_src = skills_src / skill_name
                skill_dst = paths["skills_dir"] / skill_name
                if skill_src.exists():
                    shutil.copytree(skill_src, skill_dst, dirs_exist_ok=True)

            print_success(f"Core skills: {len(core_skills)} skills")

        return True

    except Exception as e:
        print_error(f"Failed to install skills: {e}")
        return False

def install_commands(paths: dict, full: bool = True) -> bool:
    """Install command templates."""
    print_header("Installing Commands")

    commands_src = paths["shared_kb"] / "for-projects" / "command-templates"

    if not commands_src.exists():
        print_warning("Command templates not found (skipping)")
        return True

    try:
        paths["commands_dir"].mkdir(parents=True, exist_ok=True)

        if full:
            # Install all commands
            for cmd_file in commands_src.glob("*.md"):
                shutil.copy(cmd_file, paths["commands_dir"] / cmd_file.name)

            cmd_count = len(list(paths["commands_dir"].glob("*.md")))
            print_success(f"All commands: {cmd_count} commands")
        else:
            # Install core commands only
            core_commands = ["kb-search.md", "kb-validate.md", "kb-create.md"]
            for cmd_name in core_commands:
                cmd_src = commands_src / cmd_name
                if cmd_src.exists():
                    shutil.copy(cmd_src, paths["commands_dir"] / cmd_name)

            print_success(f"Core commands: {len(core_commands)} commands")

        return True

    except Exception as e:
        print_error(f"Failed to install commands: {e}")
        return False

def create_config(paths: dict) -> bool:
    """Create configuration files."""
    print_header("Creating Configuration")

    try:
        # Copy settings.json if not exists
        settings_src = paths["shared_kb"] / "for-projects" / "config-templates" / "settings.json"
        settings_dst = paths["claude_dir"] / "settings.json"

        if settings_src.exists() and not settings_dst.exists():
            paths["claude_dir"].mkdir(parents=True, exist_ok=True)
            shutil.copy(settings_src, settings_dst)
            print_success("settings.json created")
        elif settings_dst.exists():
            print_info("settings.json already exists (skipping)")

        # Copy kb-config.yaml if not exists
        kb_config_src = paths["shared_kb"] / "for-projects" / "config-templates" / "kb-config.yaml"
        kb_config_dst = paths["project_root"] / ".kb-config.yaml"

        if kb_config_src.exists() and not kb_config_dst.exists():
            shutil.copy(kb_config_src, kb_config_dst)
            print_success(".kb-config.yaml created")
        elif kb_config_dst.exists():
            print_info(".kb-config.yaml already exists (skipping)")

        return True

    except Exception as e:
        print_error(f"Failed to create configuration: {e}")
        return False

def build_index(paths: dict) -> bool:
    """Build KB search index."""
    print_header("Building Search Index")

    try:
        kb_py = paths["shared_kb"] / "tools" / "kb.py"

        if not kb_py.exists():
            print_error("kb.py not found")
            return False

        # Build index
        print_info("Building index...")
        result = subprocess.run(
            [sys.executable, str(kb_py), "index"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print_success("Index built")
            return True
        else:
            print_error(f"Failed to build index: {result.stderr}")
            return False

    except Exception as e:
        print_error(f"Failed to build index: {e}")
        return False

def verify_installation(paths: dict) -> bool:
    """Verify installation."""
    print_header("Verifying Installation")

    all_passed = True

    # 1. Check submodule
    if paths["shared_kb"].exists():
        print_success("[1/5] Submodule exists")
    else:
        print_error("[1/5] Submodule missing")
        all_passed = False

    # 2. Check sparse checkout
    curator_dir = paths["shared_kb"] / "curator"
    if not curator_dir.exists() or not list(curator_dir.iterdir()):
        print_success("[2/5] Curator excluded (sparse checkout)")
    else:
        print_warning("[2/5] Curator not excluded")

    # 3. Check agents
    if paths["agents_dir"].exists():
        agent_count = len(list(paths["agents_dir"].rglob("*.md")))
        print_success(f"[3/5] Agents: {agent_count} files")
    else:
        print_error("[3/5] Agents missing")
        all_passed = False

    # 4. Check skills
    if paths["skills_dir"].exists():
        skill_count = len([d for d in paths["skills_dir"].iterdir() if d.is_dir()])
        print_success(f"[4/5] Skills: {skill_count} skills")
    else:
        print_error("[4/5] Skills missing")
        all_passed = False

    # 5. Check index
    index_file = paths["shared_kb"] / "_index.yaml"
    if index_file.exists():
        print_success("[5/5] Index built")
    else:
        print_error("[5/5] Index missing")
        all_passed = False

    return all_passed

def install_full(paths: dict) -> bool:
    """Full installation (new project)."""
    print_header("Starting Full Installation")

    steps = [
        ("Add submodule", lambda: add_submodule(paths)),
        ("Setup sparse checkout", lambda: setup_sparse_checkout(paths)),
        ("Install agents", lambda: install_agents(paths, full=True)),
        ("Install skills", lambda: install_skills(paths, full=True)),
        ("Install commands", lambda: install_commands(paths, full=True)),
        ("Create config", lambda: create_config(paths)),
        ("Build index", lambda: build_index(paths)),
    ]

    for name, step in steps:
        try:
            if not step():
                print_error(f"Failed at: {name}")
                return False
        except Exception as e:
            print_error(f"Error at {name}: {e}")
            return False

    return True

def install_minimal(paths: dict) -> bool:
    """Minimal installation (core components only)."""
    print_header("Starting Minimal Installation")

    steps = [
        ("Add submodule", lambda: add_submodule(paths)),
        ("Setup sparse checkout", lambda: setup_sparse_checkout(paths)),
        ("Install agents", lambda: install_agents(paths, full=False)),
        ("Install skills", lambda: install_skills(paths, full=False)),
        ("Install commands", lambda: install_commands(paths, full=False)),
        ("Create config", lambda: create_config(paths)),
        ("Build index", lambda: build_index(paths)),
    ]

    for name, step in steps:
        try:
            if not step():
                print_error(f"Failed at: {name}")
                return False
        except Exception as e:
            print_error(f"Error at {name}: {e}")
            return False

    return True

def check_updates(paths: dict) -> bool:
    """Check for available updates."""
    print_header("Checking for Updates")

    try:
        # Check if submodule exists
        if not paths["shared_kb"].exists():
            print_warning("Shared KB not installed")
            return False

        # Get current commit
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=paths["shared_kb"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print_error("Failed to get current version")
            return False

        current_commit = result.stdout.strip()

        # Fetch remote
        print_info("Fetching remote...")
        subprocess.run(
            ["git", "fetch", "origin"],
            cwd=paths["shared_kb"],
            capture_output=True
        )

        # Get latest commit
        result = subprocess.run(
            ["git", "rev-parse", "origin/main"],
            cwd=paths["shared_kb"],
            capture_output=True,
            text=True
        )

        latest_commit = result.stdout.strip()

        if current_commit != latest_commit:
            print_warning("Updates available")
            print_info(f"Current: {current_commit[:8]}")
            print_info(f"Latest:  {latest_commit[:8]}")

            # Show what's new
            result = subprocess.run(
                ["git", "log", f"{current_commit}..{latest_commit}", "--oneline"],
                cwd=paths["shared_kb"],
                capture_output=True,
                text=True
            )

            if result.stdout.strip():
                print_header("Recent Changes")
                print(result.stdout)

            return True
        else:
            print_success("Already up to date")
            return False

    except Exception as e:
        print_error(f"Failed to check updates: {e}")
        return False

def update(paths: dict) -> bool:
    """Update Shared KB and templates."""
    print_header("Updating Shared KB")

    # Check for updates first
    has_updates = check_updates(paths)

    if not has_updates:
        print_info("Nothing to update")
        return True

    # Update submodule
    try:
        print_info("Updating submodule...")
        subprocess.run(
            ["git", "pull", "origin", "main"],
            cwd=paths["shared_kb"],
            check=True
        )
        print_success("Submodule updated")
    except Exception as e:
        print_error(f"Failed to update submodule: {e}")
        return False

    # Update templates
    print_header("Updating Templates")

    # Reinstall from templates
    install_agents(paths, full=True)
    install_skills(paths, full=True)
    install_commands(paths, full=True)

    # Rebuild index
    build_index(paths)

    # Verify
    verify_installation(paths)

    print_success("Update complete")
    return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Unified Shared KB Installation Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python unified-install.py --full         # Full installation (new project)
  python unified-install.py --minimal      # Minimal installation
  python unified-install.py --update       # Update existing project
  python unified-install.py --check        # Check for updates
        """
    )

    parser.add_argument("--full", action="store_true", help="Full installation")
    parser.add_argument("--minimal", action="store_true", help="Minimal installation")
    parser.add_argument("--update", action="store_true", help="Update existing installation")
    parser.add_argument("--check", action="store_true", help="Check for updates")
    parser.add_argument("--verify", action="store_true", help="Verify installation")

    args = parser.parse_args()

    # Print header
    print("=" * 60)
    print("Unified Shared KB Installation")
    print("=" * 60)
    print()

    # Get paths
    paths = get_paths()

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Run appropriate action
    if args.verify:
        status = check_existing_installation(paths)
        verify_installation(paths)
    elif args.check:
        check_updates(paths)
    elif args.update:
        update(paths)
    elif args.full:
        if install_full(paths):
            verify_installation(paths)
            print_header("Installation Complete")
            print_success("Shared KB ready to use")
        else:
            print_error("Installation failed")
            sys.exit(1)
    elif args.minimal:
        if install_minimal(paths):
            verify_installation(paths)
            print_header("Installation Complete")
            print_success("Shared KB ready to use")
        else:
            print_error("Installation failed")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
