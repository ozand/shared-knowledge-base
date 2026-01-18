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
    except subprocess.CalledProcessError as e:
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

def main():
    parser = argparse.ArgumentParser(description="Shared KB Installer")
    parser.add_argument("--method", choices=["submodule", "clone"], default="submodule", help="Installation method")
    parser.add_argument("--full", action="store_true", help="Perform full setup (structure + install + profile)")
    
    args = parser.parse_args()
    
    print("🚀 Starting Shared KB Installation...")
    
    ensure_structure()
    install_shared(args.method)
    
    if args.full:
        setup_profile()
        
    print("\n🎉 Installation Complete!")
    print("👉 Next step: python .kb/shared/tools/kb.py search 'help'")

if __name__ == "__main__":
    main()
