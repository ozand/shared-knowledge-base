#!/usr/bin/env python3
"""
Shared Knowledge Base - Installation Script

Installs Claude Code KB integration into your project.
This script copies templates from shared-knowledge-base/for-projects/
to your project's .claude/ directory.

Usage:
    python install.py [--full] [--minimal] [--agents] [--skills] [--commands]

Options:
    --full       Install everything (default)
    --minimal    Install core components only
    --agents     Install agent templates
    --skills     Install skill templates
    --commands   Install command templates
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def print_header(message):
    print(f"\n{Colors.BOLD}{message}{Colors.END}")

def get_paths():
    """Get paths for installation."""
    # Script location: shared-knowledge-base/for-projects/scripts/install.py
    script_path = Path(__file__).resolve()

    # shared-knowledge-base root
    shared_kb_root = script_path.parent.parent.parent

    # Templates directory
    templates_dir = shared_kb_root / "for-projects"

    # Project root (current working directory)
    project_root = Path.cwd()

    return {
        "shared_kb_root": shared_kb_root,
        "templates_dir": templates_dir,
        "project_root": project_root,
        "claude_dir": project_root / ".claude",
        "local_kb": project_root / "docs/knowledge-base"
    }

def create_directory_structure(paths):
    """Create .claude directory structure."""
    print_header("Creating Directory Structure")

    claude_dir = paths["claude_dir"]
    claude_dir.mkdir(exist_ok=True)

    subdirs = [
        "agents/subagents",
        "skills",
        "commands",
        "hooks"
    ]

    for subdir in subdirs:
        (claude_dir / subdir).mkdir(parents=True, exist_ok=True)

    print_success("Directory structure created")

def install_agents(paths, full=True):
    """Install agent templates."""
    print_header("Installing Agents")

    agents_src = paths["templates_dir"] / "agent-templates"
    agents_dst = paths["claude_dir"] / "agents"

    if not agents_src.exists():
        print_warning("Agent templates not found")
        return

    # Copy subagents
    subagents_src = agents_src / "subagents"
    subagents_dst = agents_dst / "subagents"

    if subagents_src.exists():
        shutil.copytree(subagents_src, subagents_dst, dirs_exist_ok=True)
        print_success(f"Subagents installed ({len(list(subagents_dst.glob('*.md')))} files)")

    # Copy kb-agent if exists
    kb_agent_src = agents_src / "kb-agent.md"
    if kb_agent_src.exists():
        shutil.copy(kb_agent_src, agents_dst / "kb-agent.md")
        print_success("KB agent installed")

def install_skills(paths, skills=None, full=True):
    """Install skill templates."""
    print_header("Installing Skills")

    skills_src = paths["templates_dir"] / "skill-templates"
    skills_dst = paths["claude_dir"] / "skills"

    if not skills_src.exists():
        print_warning("Skill templates not found")
        return

    if skills:
        # Install specific skills
        for skill_name in skills:
            skill_src = skills_src / skill_name
            skill_dst = skills_dst / skill_name
            if skill_src.exists():
                shutil.copytree(skill_src, skill_dst, dirs_exist_ok=True)
                print_success(f"Skill '{skill_name}' installed")
            else:
                print_warning(f"Skill '{skill_name}' not found")
    else:
        # Install all skills
        core_skills = ["kb-search", "kb-validate", "kb-index", "kb-create"]
        all_skills = [d.name for d in skills_src.iterdir() if d.is_dir()]

        if full:
            # Install all skills
            for skill_dir in skills_src.iterdir():
                if skill_dir.is_dir():
                    skill_dst = skills_dst / skill_dir.name
                    shutil.copytree(skill_dir, skill_dst, dirs_exist_ok=True)
            print_success(f"All skills installed ({len(all_skills)} skills)")
        else:
            # Install core skills only
            for skill_name in core_skills:
                skill_src = skills_src / skill_name
                skill_dst = skills_dst / skill_name
                if skill_src.exists():
                    shutil.copytree(skill_src, skill_dst, dirs_exist_ok=True)
            print_success(f"Core skills installed ({len(core_skills)} skills)")

def install_commands(paths, full=True):
    """Install command templates."""
    print_header("Installing Commands")

    commands_src = paths["templates_dir"] / "command-templates"
    commands_dst = paths["claude_dir"] / "commands"

    if not commands_src.exists():
        print_warning("Command templates not found")
        return

    if full:
        # Install all commands
        for cmd_file in commands_src.glob("*.md"):
            shutil.copy(cmd_file, commands_dst / cmd_file.name)
        print_success(f"All commands installed ({len(list(commands_dst.glob('*.md')))} commands)")
    else:
        # Install core commands only
        core_commands = ["kb-search.md", "kb-validate.md", "kb-create.md"]
        for cmd_name in core_commands:
            cmd_src = commands_src / cmd_name
            if cmd_src.exists():
                shutil.copy(cmd_src, commands_dst / cmd_name)
        print_success(f"Core commands installed ({len(core_commands)} commands)")

def install_config(paths):
    """Install configuration templates."""
    print_header("Installing Configuration")

    config_src = paths["templates_dir"] / "config-templates"
    project_root = paths["project_root"]

    if not config_src.exists():
        print_warning("Configuration templates not found")
        return

    # Copy settings.json if not exists
    settings_src = config_src / "settings.json"
    settings_dst = paths["claude_dir"] / "settings.json"
    if settings_src.exists() and not settings_dst.exists():
        shutil.copy(settings_src, settings_dst)
        print_success("settings.json created")
    elif settings_dst.exists():
        print_warning("settings.json already exists (skipped)")

    # Copy kb-config.yaml if not exists
    kb_config_src = config_src / "kb-config.yaml"
    kb_config_dst = project_root / ".kb-config.yaml"
    if kb_config_src.exists() and not kb_config_dst.exists():
        shutil.copy(kb_config_src, kb_config_dst)
        print_success(".kb-config.yaml created")
    elif kb_config_dst.exists():
        print_warning(".kb-config.yaml already exists (skipped)")

    # Copy hooks.json if not exists
    hooks_src = config_src / "hooks.json"
    hooks_dst = paths["claude_dir"] / "hooks.json"
    if hooks_src.exists() and not hooks_dst.exists():
        shutil.copy(hooks_src, hooks_dst)
        print_success("hooks.json created")
    elif hooks_dst.exists():
        print_warning("hooks.json already exists (skipped)")

def create_local_kb(paths):
    """Create local KB directories."""
    print_header("Creating Local KB")

    local_kb = paths["local_kb"]
    local_kb.mkdir(parents=True, exist_ok=True)

    # Create project-specific KB directories
    project_dirs = [
        "project/errors",
        "project/patterns"
    ]

    for dir_path in project_dirs:
        (local_kb / dir_path).mkdir(parents=True, exist_ok=True)

    print_success("Local KB directories created")

def show_next_steps(paths):
    """Show next steps."""
    print_header("Next Steps")

    shared_kb_path = paths["shared_kb_root"]
    project_root = paths["project_root"]

    print(f"""
1. Configure KB paths:

   Edit {project_root / ".kb-config.yaml"}:

   ```yaml
   shared_kb: "{shared_kb_path}"
   local_kb: "{paths["local_kb"]}"
   ```

2. Configure Claude Code:

   Edit {paths["claude_dir"] / "settings.json"}:

   ```json
   {{
     "agents": {{
       "enabled": ["kb-agent"]
     }},
     "skills": {{
       "enabled": ["kb-search", "kb-validate", "kb-create"]
     }}
   }}
   ```

3. Add project context:

   Edit {paths["claude_dir"] / "CLAUDE.md"}:

   ```markdown
   # Project: Your Project Name

   ## Context
   - Framework: [FastAPI, React, etc.]
   - Language: [Python, JavaScript, etc.]
   - Purpose: [What this project does]
   ```

4. Build KB index:

   ```bash
   python {shared_kb_path / "tools/kb.py"} index
   ```

5. Test integration:

   ```bash
   /kb-search "docker"
   /retrospective
   ```

For detailed instructions, see:
{paths["templates_dir"] / "PROJECT-INTEGRATION.md"}
""")

def main():
    """Main installation function."""
    parser = argparse.ArgumentParser(description="Install Shared KB integration")
    parser.add_argument("--full", action="store_true", help="Install everything (default)")
    parser.add_argument("--minimal", action="store_true", help="Install core components only")
    parser.add_argument("--agents", action="store_true", help="Install agents")
    parser.add_argument("--skills", type=str, help="Install specific skills (comma-separated)")
    parser.add_argument("--commands", action="store_true", help="Install commands")

    args = parser.parse_args()

    # Determine installation mode
    full_install = not args.minimal
    install_agents_flag = args.agents or args.full or (not args.minimal and not args.skills)
    install_skills_flag = args.skills or args.full or (not args.minimal and not args.agents)
    install_commands_flag = args.commands or args.full or (not args.minimal and not args.skills)

    # Parse skills if specified
    skills_list = None
    if args.skills:
        skills_list = [s.strip() for s in args.skills.split(",")]

    # Get paths
    paths = get_paths()

    # Print header
    print_header("🚀 Shared Knowledge Base Installation")
    print()
    print_info(f"Project root: {paths['project_root']}")
    print_info(f"Shared KB root: {paths['shared_kb_root']}")
    print()

    # Install components
    create_directory_structure(paths)

    if install_agents_flag:
        install_agents(paths, full=full_install)

    if install_skills_flag:
        install_skills(paths, skills=skills_list, full=full_install)

    if install_commands_flag:
        install_commands(paths, full=full_install)

    install_config(paths)
    create_local_kb(paths)

    # Show success
    print_header("🎉 Installation Complete!")
    print()

    # Show next steps
    show_next_steps(paths)

if __name__ == "__main__":
    main()
