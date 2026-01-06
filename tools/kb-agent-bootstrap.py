#!/usr/bin/env python3
"""
Agent Bootstrap Script

Automatically configures agents from Shared Knowledge Base.

When an agent starts, it runs this script to:
1. Detect project context (project name, agent type)
2. Load base instructions from Shared KB
3. Apply instructions to agent configuration
4. Register capabilities

Usage:
    python tools/kb-agent-bootstrap.py

Environment Variables:
    AGENT_TYPE - Override agent type (claude-code, cursor-ai, etc.)
    AGENT_SESSION - Override session ID
    KB_PATH - Override Shared KB path
    PROJECT_NAME - Override project name

Output:
    Creates .agent-config.local with auto-generated configuration
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


def detect_project_name() -> str:
    """Auto-detect project name from git or config files."""
    # Method 1: Environment override
    if env_project := os.getenv("PROJECT_NAME"):
        return env_project

    # Method 2: Git remote
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True
        )
        url = result.stdout.strip()
        # Extract project name from URL
        # git@github.com:user/PROJECT.git → PROJECT
        # https://github.com/user/PROJECT.git → PROJECT
        if url.endswith(".git"):
            url = url[:-4]
        project_name = url.split("/")[-1]
        if project_name:
            return project_name
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Method 3: package.json
    package_json = Path("package.json")
    if package_json.exists():
        try:
            with open(package_json) as f:
                data = json.load(f)
                if name := data.get("name"):
                    return name
        except (json.JSONDecodeError, IOError):
            pass

    # Method 4: pyproject.toml
    pyproject = Path("pyproject.toml")
    if pyproject.exists():
        try:
            with open(pyproject) as f:
                for line in f:
                    if line.strip().startswith("name = "):
                        # Extract name: name = "project" or name = 'project'
                        name_line = line.split("=", 1)[1].strip()
                        return name_line.strip('"').strip("'")
        except IOError:
            pass

    # Method 5: Cargo.toml
    cargo_toml = Path("Cargo.toml")
    if cargo_toml.exists():
        try:
            with open(cargo_toml) as f:
                for line in f:
                    if line.strip().startswith("name = "):
                        name_line = line.split("=", 1)[1].strip()
                        return name_line.strip('"').strip("'")
        except IOError:
            pass

    # Method 6: .agent-config
    agent_config = Path(".agent-config")
    if agent_config.exists():
        try:
            with open(agent_config) as f:
                data = json.load(f)
                if name := data.get("project_name"):
                    return name
        except (json.JSONDecodeError, IOError):
            pass

    # Default
    return "unknown"


def detect_agent_type() -> str:
    """Detect agent type from environment or config."""
    # Method 1: Environment variable
    if agent_type := os.getenv("AGENT_TYPE"):
        return agent_type

    # Method 2: .agent-config
    agent_config = Path(".agent-config")
    if agent_config.exists():
        try:
            with open(agent_config) as f:
                data = json.load(f)
                if agent_type := data.get("agent_type"):
                    return agent_type
        except (json.JSONDecodeError, IOError):
            pass

    # Default
    return "claude-code"


def generate_session_id() -> str:
    """Generate or load session ID."""
    # Method 1: Environment variable
    if session := os.getenv("AGENT_SESSION"):
        return session

    # Method 2: Generate timestamp-based session
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"session-{timestamp}"


def find_knowledge_base() -> Optional[Path]:
    """Find Shared KB in standard locations."""
    # Method 1: Environment override
    if kb_path := os.getenv("KB_PATH"):
        path = Path(kb_path)
        if path.exists() and (path / "universal").exists():
            return path

    # Method 2: Standard locations
    locations = [
        Path("docs/knowledge-base/shared"),
        Path(".shared-kb"),
        Path("knowledge-base"),
        Path("../shared-knowledge-base"),
        Path("../../shared-knowledge-base"),
    ]

    for location in locations:
        if location.exists() and (location / "universal").exists():
            return location

    # Method 3: .agent-config
    agent_config = Path(".agent-config")
    if agent_config.exists():
        try:
            with open(agent_config) as f:
                data = json.load(f)
                if kb_path := data.get("kb_path"):
                    path = Path(kb_path)
                    if path.exists():
                        return path
        except (json.JSONDecodeError, IOError):
            pass

    return None


def load_yaml_file(file_path: Path) -> Dict[str, Any]:
    """Load YAML file (with basic parsing if PyYAML not available)."""
    try:
        import yaml
        with open(file_path) as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        # Basic YAML parsing for simple cases
        print("⚠️  PyYAML not installed. Using basic parser.", file=sys.stderr)
        return parse_basic_yaml(file_path)


def parse_basic_yaml(file_path: Path) -> Dict[str, Any]:
    """Very basic YAML parser for simple key-value pairs."""
    result = {}
    current_section = None

    with open(file_path) as f:
        for line in f:
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue

            if line.endswith(":"):
                # Section
                current_section = line[:-1]
                result[current_section] = {}
            elif ":" in line:
                # Key-value
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if value:
                    result[key] = value

    return result


def check_kb_updates(kb_path: Path, quiet: bool = False) -> bool:
    """
    Check if Shared KB has updates available.

    Non-blocking: Doesn't fail if check fails (network, auth, etc.)
    """
    # Check if KB is a git repository
    git_dir = kb_path / ".git"
    if not git_dir.exists():
        return False

    try:
        # Fetch latest changes (don't merge)
        fetch_result = subprocess.run(
            ["git", "-C", str(kb_path), "fetch", "origin"],
            capture_output=True,
            text=True,
            timeout=10  # 10 second timeout
        )

        if fetch_result.returncode != 0:
            # Network or auth issue - silently skip
            return False

        # Check for new commits
        log_result = subprocess.run(
            ["git", "-C", str(kb_path), "log", "HEAD..origin/main",
             "--oneline", "--since", "1 month ago"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if log_result.returncode != 0:
            return False

        if not log_result.stdout.strip():
            # No updates
            return False

        # New commits available
        commits = log_result.stdout.strip().split('\n')
        num_commits = len(commits)

        if not quiet:
            print(f"\n{'=' * 60}")
            print(f"🆕 Shared KB Updates Available")
            print(f"{'=' * 60}")
            print(f"\n{num_commits} new update(s) available:")
            for i, commit in enumerate(commits[:5], 1):
                parts = commit.split(' ', 1)
                commit_hash = parts[0][:7]
                commit_msg = parts[1] if len(parts) > 1 else "No message"
                print(f"  {i}. {commit_hash} - {commit_msg}")

            if num_commits > 5:
                print(f"\n  ... and {num_commits - 5} more")

            # Detect if submodule or clone
            is_submodule = (kb_path / ".git").is_dir()

            print(f"\n💡 To update:")
            if is_submodule:
                print(f"   git submodule update --remote --merge {kb_path}")
            else:
                parent = kb_path.parent
                print(f"   cd {kb_path} && git pull origin main")

            print(f"\n⏰ Recommended: Update before starting major work")
            print(f"{'=' * 60}\n")

        return True

    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        # Silently fail - update check is non-blocking
        return False


def load_instructions(kb_path: Path) -> Dict[str, Any]:
    """Load agent instructions from KB."""
    instructions_file = kb_path / "universal/agent-instructions/base-instructions.yaml"

    if not instructions_file.exists():
        print(f"⚠️  Instructions file not found: {instructions_file}")
        return {}

    try:
        return load_yaml_file(instructions_file)
    except Exception as e:
        print(f"⚠️  Error loading instructions: {e}", file=sys.stderr)
        return {}


def apply_instructions(
    instructions: Dict[str, Any],
    context: Dict[str, str]
) -> Dict[str, Any]:
    """Apply instructions to create agent configuration."""
    config = {
        "agent_type": context["agent_type"],
        "project_name": context["project_name"],
        "session_id": context.get("session_id", "unknown"),
        "kb_path": str(context.get("kb_path", "")),
        "kb_version": instructions.get("version", "unknown"),
        "kb_last_updated": instructions.get("last_updated", "unknown"),
        "capabilities": {},
        "enabled_features": [],
    }

    # Process instruction groups
    instructions_data = instructions.get("instructions", {})
    if not instructions_data:
        print("⚠️  No instructions found in KB")
        return config

    for group_name, group_settings in instructions_data.items():
        if isinstance(group_settings, dict) and group_settings.get("enabled", False):
            config["capabilities"][group_name] = {
                "pattern": group_settings.get("pattern"),
                "priority": group_settings.get("priority", "MEDIUM"),
                "required_when": group_settings.get("required_when"),
                "steps": group_settings.get("steps", []),
            }
            config["enabled_features"].append(group_name)

    # Add capabilities registry
    if capabilities := instructions.get("capabilities"):
        config["available_capabilities"] = capabilities

    return config


def save_config(config: Dict[str, Any], output_path: Path = None) -> Path:
    """Save configuration to .agent-config.local file."""
    if output_path is None:
        output_path = Path(".agent-config.local")

    with open(output_path, "w") as f:
        json.dump(config, f, indent=2)

    return output_path


def print_summary(config: Dict[str, Any], kb_path: Optional[Path]):
    """Print bootstrap summary."""
    print("\n" + "=" * 60)
    print("🤖 Agent Bootstrap Complete")
    print("=" * 60)

    print(f"\n📋 Agent Context:")
    print(f"  • Agent Type: {config['agent_type']}")
    print(f"  • Project Name: {config['project_name']}")
    print(f"  • Session ID: {config['session_id']}")

    if kb_path:
        print(f"\n📚 Knowledge Base:")
        print(f"  • Path: {kb_path}")
        print(f"  • Version: {config['kb_version']}")
        print(f"  • Last Updated: {config['kb_last_updated']}")

    if config["enabled_features"]:
        print(f"\n✅ Enabled Features:")
        for feature in config["enabled_features"]:
            print(f"  • {feature}")

    if config.get("capabilities"):
        print(f"\n🔧 Capabilities:")
        for cap_name, cap_data in config["capabilities"].items():
            pattern = cap_data.get("pattern", "N/A")
            priority = cap_data.get("priority", "MEDIUM")
            print(f"  • {cap_name}: {pattern} [{priority}]")

    print(f"\n💾 Configuration saved to: .agent-config.local")
    print("=" * 60 + "\n")


def main():
    """Main bootstrap process."""
    parser = argparse.ArgumentParser(
        description="Bootstrap agent configuration from Shared Knowledge Base"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Detect context but don't save configuration"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output configuration as JSON"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress output (except errors)"
    )

    args = parser.parse_args()

    if not args.quiet:
        print("🤖 Agent Bootstrap: Starting...")

    # Step 1: Detect context
    project_name = detect_project_name()
    agent_type = detect_agent_type()
    session_id = generate_session_id()

    if not args.quiet:
        print(f"  → Project: {project_name}")
        print(f"  → Agent Type: {agent_type}")
        print(f"  → Session: {session_id}")

    # Step 2: Find KB
    kb_path = find_knowledge_base()
    if not kb_path:
        if not args.quiet:
            print("⚠️  Shared KB not found. Using minimal configuration.")
        config = {
            "agent_type": agent_type,
            "project_name": project_name,
            "session_id": session_id,
            "kb_path": "",
            "capabilities": {},
            "enabled_features": [],
        }
    else:
        if not args.quiet:
            print(f"  → KB Path: {kb_path}")

        # Step 3: Load instructions
        instructions = load_instructions(kb_path)

        if not instructions:
            if not args.quiet:
                print("⚠️  No instructions loaded from KB")
            config = {
                "agent_type": agent_type,
                "project_name": project_name,
                "session_id": session_id,
                "kb_path": str(kb_path),
                "capabilities": {},
                "enabled_features": [],
            }
        else:
            if not args.quiet:
                print(f"  → KB Version: {instructions.get('version', 'unknown')}")

            # Step 4: Apply instructions
            context = {
                "agent_type": agent_type,
                "project_name": project_name,
                "session_id": session_id,
                "kb_path": kb_path,
            }
            config = apply_instructions(instructions, context)

        # Step 4.5: Check for KB updates (non-blocking)
        if kb_path:
            check_kb_updates(kb_path, quiet=args.quiet)

    # Step 5: Save configuration
    if not args.dry_run:
        output_path = save_config(config)
    else:
        output_path = None
        if not args.quiet:
            print("⚠️  Dry run mode - configuration not saved")

    # Step 6: Output
    if args.json:
        print(json.dumps(config, indent=2))
    elif not args.quiet:
        print_summary(config, kb_path)

    # Set environment variables for subsequent commands
    if not args.dry_run:
        os.environ["AGENT_TYPE"] = agent_type
        os.environ["PROJECT_NAME"] = project_name
        os.environ["AGENT_SESSION"] = session_id
        if kb_path:
            os.environ["KB_PATH"] = str(kb_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
