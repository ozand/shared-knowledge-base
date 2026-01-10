#!/usr/bin/env python
"""
PostToolUse Hook: Validate metadata YAML files
Ensures _meta.yaml files follow correct structure
"""

import sys
import json
import re

def main():
    try:
        input_data = json.load(sys.stdin)
    except:
        sys.exit(0)

    file_path = input_data.get('tool_input', {}).get('file_path', '')

    # Only check _meta.yaml files
    if not file_path.endswith('_meta.yaml'):
        sys.exit(0)

    print(f"🔍 Validating metadata: {file_path}...")

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except:
        sys.exit(0)

    # Check 1: Must have created_at
    if not re.search(r"^created_at:", content, re.MULTILINE):
        print("  ❌ Missing 'created_at' field")
        print("  Metadata must have: created_at, last_analyzed_at, quality_score")
        sys.exit(2)

    # Check 2: Must have last_analyzed_at
    if not re.search(r"^last_analyzed_at:", content, re.MULTILINE):
        print("  ❌ Missing 'last_analyzed_at' field")
        sys.exit(2)

    # Check 3: Must have quality_score
    match = re.search(r"^quality_score:\s*(\d+)", content, re.MULTILINE)
    if not match:
        print("  ❌ Missing 'quality_score' field")
        sys.exit(2)

    # Check 4: quality_score must be 0-100
    score = int(match.group(1))
    if score < 0 or score > 100:
        print(f"  ❌ quality_score must be between 0 and 100, got: {score}")
        sys.exit(2)

    print("  ✅ Metadata validation passed")
    sys.exit(0)

if __name__ == "__main__":
    main()
