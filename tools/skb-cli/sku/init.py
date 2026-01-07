"""
Project initialization for SKU
Handles setting up new projects with Enterprise Knowledge Graph
"""

import os
import yaml
import requests
from pathlib import Path
from typing import Optional, Dict, List
from .utils import console, error, success, info, warn


class InitManager:
    """Manages project initialization"""

    def __init__(self):
        """Initialize init manager"""
        self.repo_url = os.environ.get('SKU_REPO', 'ozand/shared-knowledge-base')
        self.raw_base = f"https://raw.githubusercontent.com/{self.repo_url}/main"

    def init(self, project_path: Optional[Path] = None,
             project_type: Optional[str] = None,
             team: Optional[str] = None,
             install_hooks: bool = True,
             install_artifacts: Optional[List[str]] = None) -> bool:
        """Initialize new project with Enterprise Knowledge Graph

        Args:
            project_path: Project directory (default: current directory)
            project_type: Project type (typescript, python, go, etc.)
            team: Team name for access control
            install_hooks: Install Claude Code hooks
            install_artifacts: List of artifacts to install

        Returns:
            True if initialization successful
        """
        if project_path is None:
            project_path = Path.cwd()

        project_path = Path(project_path)

        if not project_path.exists():
            error(f"Project path does not exist: {project_path}")
            return False

        console.print(f"\n[bold cyan]Initializing Enterprise Knowledge Graph[/bold cyan]")
        console.print(f"[dim]Project: {project_path}[/dim]\n")

        # Check if already initialized
        if (project_path / ".claude").exists():
            warn("⚠️  .claude/ already exists")
            response = input("Re-initialize? [y/N] ")
            if response.lower() != 'y':
                info("Initialization cancelled")
                return False

        # Step 1: Create .claude directory
        info("Step 1: Creating .claude/ directory...")
        self._create_claude_dir(project_path)

        # Step 2: Detect project type
        if project_type is None:
            project_type = self._detect_project_type(project_path)
            info(f"Detected project type: {project_type}")

        # Step 3: Create CLAUDE.md
        info("Step 2: Creating CLAUDE.md...")
        self._create_claude_md(project_path, project_type, team)

        # Step 4: Create settings.json with hooks
        if install_hooks:
            info("Step 3: Installing Claude Code hooks...")
            self._create_settings_json(project_path, project_type)
            self._install_hooks(project_path)

        # Step 5: Create .sku/config.yaml
        info("Step 4: Creating SKU configuration...")
        self._create_sku_config(project_path, team)

        # Step 6: Create .skuignore
        info("Step 5: Creating .skuignore...")
        self._create_sku_ignore(project_path)

        # Step 7: Install artifacts
        if install_artifacts:
            info("Step 6: Installing artifacts...")
            for artifact in install_artifacts:
                info(f"  Installing: {artifact}")
                # TODO: Install artifact

        console.print("\n[bold green]✓ Initialization complete![/bold green]\n")

        # Show next steps
        self._show_next_steps(project_path, project_type)

        return True

    def _create_claude_dir(self, project_path: Path):
        """Create .claude directory structure"""
        claude_dir = project_path / ".claude"
        claude_dir.mkdir(exist_ok=True)

        # Create subdirectories
        (claude_dir / "hooks").mkdir(exist_ok=True)
        (claude_dir / "skills").mkdir(exist_ok=True)
        (claude_dir / "agents").mkdir(exist_ok=True)

        success(f"✓ Created .claude/")

    def _detect_project_type(self, project_path: Path) -> str:
        """Detect project type from files

        Args:
            project_path: Project directory

        Returns:
            Project type string
        """
        # Check for package.json
        if (project_path / "package.json").exists():
            return "typescript"

        # Check for pyproject.toml or requirements.txt
        if (project_path / "pyproject.toml").exists() or \
           (project_path / "requirements.txt").exists():
            return "python"

        # Check for go.mod
        if (project_path / "go.mod").exists():
            return "go"

        # Check for pom.xml
        if (project_path / "pom.xml").exists():
            return "java"

        # Default
        return "generic"

    def _create_claude_md(self, project_path: Path, project_type: str, team: Optional[str]):
        """Create CLAUDE.md file

        Args:
            project_path: Project directory
            project_type: Project type
            team: Team name
        """
        claude_md = project_path / ".claude" / "CLAUDE.md"

        # Get project name from directory
        project_name = project_path.name

        content = f"""# {project_name} - Claude Code Instructions

**Project Type:** {project_type}
**Team:** {team or 'default'}
**Initialized:** {self._get_timestamp()}

---

## Quick Start

```bash
# Sync Enterprise Knowledge Graph catalog
uvx sku sync --index-only

# Search for artifacts
uvx sku search --tag {project_type}

# Install artifact
uvx sku install skill testing
```

---

## Project Context

This is a **{project_type}** project using the Enterprise Knowledge Graph for:

- **Shared Artifacts** - Reusable agents, skills, hooks
- **Project Knowledge** - Cross-project documentation and configs
- **Auto-Updates** - Stay informed about artifact changes

---

## Installed Artifacts

<!-- Artifacts installed via 'sku init' will be listed here -->

---

## Workflows

### Finding Information

```
User: How do I test async code?
→ Claude searches shared-knowledge-base
→ Returns testing skill with async examples
```

### Using Artifacts

```
User: Generate tests for UserService
→ Claude uses installed testing skill
→ Follows project conventions
```

---

## Configuration

- **SKU Config:** `.sku/config.yaml`
- **Claude Settings:** `.claude/settings.json`
- **Hooks:** `.claude/hooks/`

---

## Team Knowledge

This project has access to:
- **{team or 'All'}** team artifacts
- **Public** shared artifacts
- **Project-specific** documentation

---

**For help:** See [Enterprise Knowledge Graph Guide](https://raw.githubusercontent.com/{self.repo_url}/main/ENTERPRISE-KNOWLEDGE-GRAPH.md)
"""

        claude_md.write_text(content)
        success(f"✓ Created CLAUDE.md")

    def _create_settings_json(self, project_path: Path, project_type: str):
        """Create settings.json with hooks

        Args:
            project_path: Project directory
            project_type: Project type
        """
        settings_file = project_path / ".claude" / "settings.json"

        settings = {
            "hooks": {
                "SessionStart": [
                    {
                        "hooks": [
                            {
                                "type": "command",
                                "command": "python $CLAUDE_PROJECT_DIR/.claude/hooks/check-artifact-updates.py",
                                "timeout": 30
                            }
                        ]
                    }
                ]
            },
            "skills": {
                "enabled": ["kb-search"]
            },
            "mcpServers": {}
        }

        with open(settings_file, 'w') as f:
            import json
            json.dump(settings, f, indent=2)

        success(f"✓ Created settings.json")

    def _install_hooks(self, project_path: Path):
        """Install Claude Code hooks

        Args:
            project_path: Project directory
        """
        hooks_dir = project_path / ".claude" / "hooks"

        # Download update check hook
        try:
            response = requests.get(
                f"{self.raw_base}/.claude/hooks/check-artifact-updates.py",
                timeout=10
            )
            response.raise_for_status()

            (hooks_dir / "check-artifact-updates.py").write_text(response.text)
            success(f"✓ Installed check-artifact-updates.py hook")

        except Exception as e:
            warn(f"⚠️  Could not install hooks: {e}")

    def _create_sku_config(self, project_path: Path, team: Optional[str]):
        """Create .sku/config.yaml

        Args:
            project_path: Project directory
            team: Team name
        """
        sku_dir = project_path / ".sku"
        sku_dir.mkdir(exist_ok=True)

        config_file = sku_dir / "config.yaml"

        config = {
            "github": {
                "repository": self.repo_url,
                "branch": "main"
            },
            "auto_update": {
                "policy": "smart",
                "check_interval": "daily"
            },
            "project": {
                "id": project_path.name,
                "type": self._detect_project_type(project_path),
                "team": team or "default"
            }
        }

        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

        success(f"✓ Created .sku/config.yaml")

    def _create_sku_ignore(self, project_path: Path):
        """Create .skuignore file

        Args:
            project_path: Project directory
        """
        skuignore_file = project_path / ".skuignore"

        content = """# SKU ignore patterns
# Files/directories to exclude from artifact publication

# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/

# Build artifacts
dist/
build/
*.log

# IDE
.vscode/
.idea/
*.swp

# Local config
.env.local
*.local

# Generated
.generated/
"""

        skuignore_file.write_text(content)
        success(f"✓ Created .skuignore")

    def _show_next_steps(self, project_path: Path, project_type: str):
        """Show next steps after initialization

        Args:
            project_path: Project directory
            project_type: Project type
        """
        console.print("[bold cyan]Next Steps:[/bold cyan]\n")

        console.print("1. [cyan]Install artifacts:[/cyan]")
        console.print(f"   uvx sku search --tag {project_type}")
        console.print(f"   uvx sku install skill testing\n")

        console.print("2. [cyan]Publish project knowledge:[/cyan]")
        console.print(f"   uvx sku publish docs/ --type docs --version 1.0.0\n")

        console.print("3. [cyan]Commit to git:[/cyan]")
        console.print(f"   git add .claude/ .sku/ .skuignore")
        console.print(f"   git commit -m 'Initialize Enterprise Knowledge Graph'\n")

        console.print("4. [cyan]Learn more:[/cyan]")
        console.print(f"   https://github.com/{self.repo_url}/blob/main/ENTERPRISE-KNOWLEDGE-GRAPH.md\n")

    def _get_timestamp(self) -> str:
        """Get current timestamp

        Returns:
            ISO format timestamp
        """
        from datetime import datetime
        return datetime.now().isoformat()
