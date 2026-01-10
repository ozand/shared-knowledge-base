#!/usr/bin/env python
"""
PreToolUse Hook: Validate YAML before editing
Ensures existing YAML stays valid
"""

import sys
import json
import os

def main():
    try:
        input_data = json.load(sys.stdin)
    except:
        sys.exit(0)

    file_path = input_data.get('tool_input', {}).get('file_path', '')

    # Only check YAML files
    if not (file_path.endswith('.yaml') or file_path.endswith('.yml')):
        sys.exit(0)

    # Skip _meta.yaml files
    if file_path.endswith('_meta.yaml'):
        sys.exit(0)

    # Check if file exists
    if not os.path.exists(file_path):
        sys.exit(0)

    print(f"🔍 Checking existing YAML: {file_path}...")

    # Basic syntax check
    try:
        import yaml
        with open(file_path, 'r') as f:
            yaml.safe_load(f)
    except Exception as e:
        print(f"⚠️  Warning: {file_path} has existing YAML syntax issues")
        print(f"Error: {e}")
        print("Consider fixing before editing")
        sys.exit(0)  # Don't block, just warn

    sys.exit(0)

if __name__ == "__main__":
    main()
