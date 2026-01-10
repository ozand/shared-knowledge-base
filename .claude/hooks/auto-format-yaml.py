#!/usr/bin/env python
"""
PostToolUse Hook: Auto-format YAML files
Ensures consistent YAML formatting across KB
"""

import sys
import json
import yaml

def main():
    # Read JSON input from stdin
    try:
        input_data = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        # No valid JSON input, exit gracefully
        sys.exit(0)

    # Extract file path
    file_path = input_data.get('tool_input', {}).get('file_path')

    # Only format YAML files
    if not file_path or not (file_path.endswith('.yaml') or file_path.endswith('.yml')):
        sys.exit(0)

    # Skip _meta.yaml files (different format)
    if file_path.endswith('_meta.yaml'):
        sys.exit(0)

    print(f"📝 Auto-formatting {file_path}...")

    # Format YAML
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if data is None:
            print(f"  ⚠️  Empty file, skipping: {file_path}")
            sys.exit(0)

        # Write back with consistent formatting
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2, allow_unicode=True)

        print(f"  ✅ Formatted: {file_path}")
    except Exception as e:
        print(f"  ⚠️  Could not format {file_path}: {e}")

    sys.exit(0)

if __name__ == "__main__":
    main()
