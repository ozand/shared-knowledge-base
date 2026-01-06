#!/bin/bash
# PostToolUse Hook: Auto-format YAML files
# Ensures consistent YAML formatting across KB

set -e

INPUT=$(cat)
FILE=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only format YAML files
if [[ ! "$FILE" == *.yaml && ! "$FILE" == *.yml ]]; then
  exit 0
fi

# Skip _meta.yaml files (different format)
if [[ "$FILE" == *_meta.yaml ]]; then
  exit 0
fi

echo "📝 Auto-formatting $FILE..."

# Check if Python is available
if ! command -v python &> /dev/null; then
  echo "⚠️  Python not found, skipping auto-format"
  exit 0
fi

# Use Python to format YAML consistently
python << 'PYTHON'
import sys
import yaml
import re

file_path = sys.argv[1]

try:
  with open(file_path, 'r') as f:
    data = yaml.safe_load(f)

  # Write back with consistent formatting
  with open(file_path, 'w') as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2)

  print(f"  ✅ Formatted: {file_path}")
except Exception as e:
  print(f"  ⚠️  Could not format {file_path}: {e}")
  sys.exit(0)  # Don't block on formatting errors
PYTHON "$FILE"

exit 0
