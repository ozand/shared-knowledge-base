#!/usr/bin/env python
"""
PreToolUse Hook: Validate YAML before writing
Prevents invalid YAML from being created
"""

import sys
import json
import subprocess

def main():
    try:
        input_data = json.load(sys.stdin)
    except:
        sys.exit(0)

    file_path = input_data.get('tool_input', {}).get('file_path', '')

    # Only check YAML files
    if not (file_path.endswith('.yaml') or file_path.endswith('.yml')):
        sys.exit(0)

    # Skip _meta.yaml files (they're validated separately)
    if file_path.endswith('_meta.yaml'):
        sys.exit(0)

    print(f"🔍 Validating YAML syntax for {file_path}...")

    # Check if kb.py validate is available
    try:
        result = subprocess.run(
            ['python', 'tools/kb.py', 'validate', file_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        if '✓' not in result.stdout and result.returncode != 0:
            print(f"❌ YAML validation failed for {file_path}")
            print(f"Run 'python tools/kb.py validate {file_path}' for details")
            sys.exit(2)
    except Exception as e:
        # Fallback: basic YAML syntax check
        try:
            import yaml
            with open(file_path, 'r') as f:
                yaml.safe_load(f)
        except Exception as yaml_error:
            print(f"❌ Invalid YAML syntax in {file_path}")
            print(f"Error: {yaml_error}")
            sys.exit(2)

    print("✅ YAML validation passed")
    sys.exit(0)

if __name__ == "__main__":
    main()
