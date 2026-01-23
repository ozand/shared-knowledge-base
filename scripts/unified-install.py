#!/usr/bin/env python3
"""
Unified Installer for Shared Knowledge Base (v5.1+)
Installs or updates the knowledge base and sets up the environment.
"""

import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path

REPO_URL = "https://github.com/ozand/shared-knowledge-base.git"
KB_DIR = Path(".kb")
SHARED_DIR = KB_DIR / "shared"
PROJECT_DIR = KB_DIR / "project"

def print_step(msg):
    print(f"🔹 {msg}")

def print_success(msg):
    print(f"✅ {msg}")

def run_cmd(cmd, cwd=None, check=True):
    try:
        subprocess.run(cmd, cwd=cwd, check=check, shell=True)
    except subprocess.CalledProcessError:
        print(f"❌ Command failed: {cmd}")
        sys.exit(1)

def ensure_structure():
    """Create the Two-Tier structure."""
    print_step("Checking directory structure...")

    if not KB_DIR.exists():
        KB_DIR.mkdir()

    if not PROJECT_DIR.exists():
        PROJECT_DIR.mkdir(parents=True)
        print_success("Created .kb/project/")

    # Create project capability structure
    for cap in ["agents", "skills", "hooks"]:
        (PROJECT_DIR / "domains" / "claude-code" / cap).mkdir(parents=True, exist_ok=True)

def install_shared(method="clone"):
    """Install shared KB as submodule or clone."""
    if SHARED_DIR.exists():
        print_step("Shared KB exists. Updating...")
        run_cmd("git pull origin main", cwd=SHARED_DIR)
        print_success("Updated Shared KB")
        return

    print_step(f"Installing Shared KB via {method}...")

    if method == "submodule":
        if not Path(".git").exists():
            print("⚠️  Not a git repository. Initializing git...")
            run_cmd("git init")

        run_cmd(f"git submodule add {REPO_URL} .kb/shared")
        run_cmd("git submodule update --init --recursive")
    else:
        run_cmd(f"git clone {REPO_URL} .kb/shared")

    print_success("Installed Shared KB")

def cleanup_artifacts():
    """Remove installation artifacts from shared KB.

    The shared-knowledge-base repository contains its own .kb/ directory
    which is only needed for development of SKB itself, not in consumer projects.
    This function removes those artifacts after installation.
    """
    print_step("Cleaning up installation artifacts...")

    # Remove .kb/shared/.kb/ if it exists (this is SKB's local KB, not needed in consumer projects)
    artifact = SHARED_DIR / ".kb"
    if artifact.exists():
        try:
            shutil.rmtree(artifact)
            print_success("Removed .kb/shared/.kb/ artifact")
        except Exception as e:
            print(f"⚠️  Could not remove artifact: {e}")

    # Also remove stray files that shouldn't be in consumer projects
    stray_files = [
        SHARED_DIR / "files_to_delete.txt",
        SHARED_DIR / "long_files.txt",
    ]

    # Remove session files matching the pattern
    import glob as _glob
    session_pattern = str(SHARED_DIR / "*this-session-is-being-continued*.txt")
    stray_files.extend(Path(p) for p in _glob.glob(session_pattern))

    removed_count = 0
    for f in stray_files:
        if f.exists():
            try:
                f.unlink()
                removed_count += 1
            except Exception:
                pass

    if removed_count > 0:
        print_success(f"Removed {removed_count} stray file(s)")

def setup_profile():
    """Initialize the active profile."""
    kb_py = SHARED_DIR / "tools" / "kb.py"
    if kb_py.exists():
        print_step("Initializing Knowledge Profile...")
        # Run kb.py profile init from project root
        # We need to set PYTHONPATH to include .kb/shared
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SHARED_DIR)

        subprocess.run([sys.executable, str(kb_py), "profile", "init"], env=env)
        print_success("Profile initialized")

def configure_gitignore():
    """Update .gitignore with KB entries."""
    print_step("Configuring .gitignore...")

    ignore_entries = [
        "\n# --- Shared Knowledge Base ---",
        ".kb/shared/",
        ".kb/cache/",
        ".kb/project/context-archive/sources/",
        "tmp/",
        "# -----------------------------"
    ]

    gitignore_path = Path(".gitignore")

    if not gitignore_path.exists():
        with open(gitignore_path, "w") as f:
            f.write("\n".join(ignore_entries) + "\n")
        print_success("Created .gitignore")
        return

    with open(gitignore_path, "r") as f:
        content = f.read()

    to_append = []
    for entry in ignore_entries:
        if entry.strip() and entry not in content:
            to_append.append(entry)

    if to_append:
        with open(gitignore_path, "a") as f:
            f.write("\n".join(to_append) + "\n")
        print_success("Updated .gitignore with protection rules")
    else:
        print_success(".gitignore already configured")

def main():
    parser = argparse.ArgumentParser(description="Shared KB Installer")
    parser.add_argument("--method", choices=["submodule", "clone"], default="submodule", help="Installation method")
    parser.add_argument("--full", action="store_true", help="Perform full setup (structure + install + profile)")

    args = parser.parse_args()

    print("🚀 Starting Shared KB Installation...")

    ensure_structure()
    configure_gitignore()
    install_shared(args.method)
    cleanup_artifacts()  # NEW: Clean up artifacts after installation

    if args.full:
        setup_profile()

    print("\n🎉 Installation Complete!")
    print("👉 Next step: python .kb/shared/tools/kb.py search 'help'")

if __name__ == "__main__":
    main()
