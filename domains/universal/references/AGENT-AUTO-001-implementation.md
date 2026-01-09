# Agent Auto-Configuration Pattern - Implementation Details

**Extracted from:** agent-auto-configuration.yaml
**Pattern ID:** AGENT-AUTO-001

## Knowledge Base Structure

```yaml
# Shared KB should contain:

universal/agent-instructions/
  ├── base-instructions.yaml          # Base instructions for all agents
  ├── context-detection.yaml           # How to detect context
  ├── templates/
  │   ├── issue-template.md
  │   ├── pr-template.md
  │   └── comment-template.md
  └── patterns/
      ├── github-attribution.yaml      # GITHUB-ATTRIB-001
      ├── agent-handoff.yaml           # AGENT-HANDOFF-001
      └── agent-accountability.yaml    # AGENT-ACCOUNTABILITY-001

tools/
  └── kb-agent-bootstrap.py            # Bootstrap script
```

## Bootstrap Script

```python
#!/usr/bin/env python3
"""
Agent Bootstrap Script
Run this when agent starts to auto-configure from Shared KB
"""

import os
import subprocess
import json
from pathlib import Path

def detect_project_name():
    """Auto-detect project name from git or config"""
    # Try git remote
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True
        )
        url = result.stdout.strip()
        # Extract: git@github.com:user/PARSER.git → PARSER
        if url.endswith(".git"):
            url = url[:-4]
        return url.split("/")[-1]
    except:
        pass

    # Try package.json
    package_json = Path("package.json")
    if package_json.exists():
        with open(package_json) as f:
            data = json.load(f)
            return data.get("name", "unknown")

    # Try pyproject.toml
    pyproject = Path("pyproject.toml")
    if pyproject.exists():
        # Parse TOML (simplified)
        with open(pyproject) as f:
            for line in f:
                if line.startswith("name = "):
                    return line.split("=")[1].strip().strip('"')

    # Try .agent-config
    config = Path(".agent-config")
    if config.exists():
        with open(config) as f:
            data = json.load(f)
            return data.get("project_name", "unknown")

    return "unknown"

def detect_agent_type():
    """Detect agent type from environment or config"""
    # Environment variable
    agent_type = os.getenv("AGENT_TYPE")
    if agent_type:
        return agent_type

    # From .agent-config
    config = Path(".agent-config")
    if config.exists():
        with open(config) as f:
            data = json.load(f)
            return data.get("agent_type", "claude-code")

    # Default
    return "claude-code"

def find_knowledge_base():
    """Find Shared KB in standard locations"""
    locations = [
        Path("docs/knowledge-base/shared"),
        Path(".shared-kb"),
        Path("knowledge-base"),
        Path(os.getenv("KB_PATH", "")),
    ]

    for location in locations:
        if location.exists() and (location / "universal").exists():
            return location

    return None

def load_instructions(kb_path):
    """Load agent instructions from KB"""
    instructions_file = kb_path / "universal/agent-instructions/base-instructions.yaml"

    if not instructions_file.exists():
        return {}

    # Parse YAML (simplified)
    import yaml
    with open(instructions_file) as f:
        return yaml.safe_load(f)

def apply_instructions(instructions, context):
    """Apply instructions to agent configuration"""
    if not instructions:
        return

    # Build configuration
    config = {
        "agent_type": context["agent_type"],
        "project_name": context["project_name"],
        "session_id": context.get("session_id", "unknown"),
        "capabilities": {}
    }

    # Process instruction groups
    for group, settings in instructions.get("instructions", {}).items():
        if settings.get("enabled", False):
            config["capabilities"][group] = {
                "pattern": settings.get("pattern"),
                "required_when": settings.get("required_when"),
                "steps": settings.get("steps", [])
            }

    # Save to .agent-config.local (auto-generated, don't commit)
    with open(".agent-config.local", "w") as f:
        json.dump(config, f, indent=2)

    return config

def main():
    """Bootstrap agent from Shared KB"""
    print("🤖 Agent Bootstrap: Starting...")

    # Detect context
    project_name = detect_project_name()
    agent_type = detect_agent_type()

    print(f"  → Project: {project_name}")
    print(f"  → Agent Type: {agent_type}")

    # Find KB
    kb_path = find_knowledge_base()
    if not kb_path:
        print("⚠️  Shared KB not found. Using default configuration.")
        return

    print(f"  → KB Path: {kb_path}")

    # Load instructions
    instructions = load_instructions(kb_path)
    if not instructions:
        print("⚠️  No instructions found in KB.")
        return

    print(f"  → Instructions version: {instructions.get('last_updated', 'unknown')}")

    # Apply instructions
    context = {
        "agent_type": agent_type,
        "project_name": project_name,
        "session_id": os.getenv("AGENT_SESSION", "auto-generated")
    }

    config = apply_instructions(instructions, context)

    print(f"✅ Bootstrap complete. Configuration saved to .agent-config.local")
    print(f"   Capabilities: {list(config.get('capabilities', {}).keys())}")

if __name__ == "__main__":
    main()
```

## Auto Update Hook

```python
# Add to agent's update cycle

def check_kb_updates():
    """Check if KB has new instructions"""
    kb_path = find_knowledge_base()
    if not kb_path:
        return

    # Get current KB version
    version_file = kb_path / ".kb-version"
    if version_file.exists():
        with open(version_file) as f:
            current_version = f.read().strip()
    else:
        current_version = "0"

    # Check for updates (git fetch)
    subprocess.run(["git", "-C", kb_path, "fetch"], check=False)

    # Get latest version
    try:
        latest_version = subprocess.run(
            ["git", "-C", kb_path, "rev-parse", "origin/main"],
            capture_output=True, text=True, check=True
        ).stdout.strip()
    except:
        return

    if latest_version != current_version:
        # Update KB
        subprocess.run(["git", "-C", kb_path, "pull"], check=True)

        # Reload instructions
        new_instructions = load_instructions(kb_path)

        # Re-configure if needed
        if new_instructions.get("requires_reconfigure", False):
            print("🔄 KB updated. Re-configuring...")
            apply_instructions(new_instructions, detect_context())

        # Save new version
        with open(version_file, "w") as f:
            f.write(latest_version)
```

## Configuration File

```json
// .agent-config (commit to repo, overrides)

{
  "project_name": "PARSER",
  "agent_type": "claude-code",
  "kb_path": "docs/knowledge-base/shared",
  "auto_update": true,
  "features": {
    "github_attribution": true,
    "kb_contribution": true
  }
}
```

## Integration Points

### Agent Startup

```bash
# Call this when agent initializes

python -c "
import sys
sys.path.insert(0, 'docs/knowledge-base/shared/tools')
from kb_agent_bootstrap import bootstrap_agent
bootstrap_agent()
"
```

### Agent Task Start

```python
# Before each task, check context

context = load_agent_config()
if task_type == "create_github_issue":
    if context["capabilities"]["github_attribution"]["enabled"]:
        apply_github_attribution(context)
```

### Agent Periodic

```python
# Check for KB updates every hour

while True:
    check_kb_updates()
    time.sleep(3600)
```
