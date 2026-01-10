#!/usr/bin/env python
"""
PostToolUse Hook: Quality gate for KB entries
Ensures KB entries meet minimum quality standards
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

    # Only check YAML files
    if not (file_path.endswith('.yaml') or file_path.endswith('.yml')):
        sys.exit(0)

    # Skip _meta.yaml files
    if file_path.endswith('_meta.yaml'):
        sys.exit(0)

    print(f"🔍 Quality gate for {file_path}...")

    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except:
        sys.exit(0)

    # Check 1: Must have required fields
    required_fields = ["version", "category", "last_updated"]
    missing_fields = []

    for field in required_fields:
        if not re.search(rf"^{field}:", content, re.MULTILINE):
            missing_fields.append(field)

    if missing_fields:
        print(f"  ❌ Missing required fields: {', '.join(missing_fields)}")
        print("  KB entries must have: version, category, last_updated")
        sys.exit(2)

    # Check 2: Must have errors: or patterns: section
    if not re.search(r"^errors:", content, re.MULTILINE) and not re.search(r"^^patterns:", content, re.MULTILINE):
        print("  ❌ Missing 'errors:' or 'patterns:' section")
        print("  KB entries must define errors or patterns")
        sys.exit(2)

    # Check 3: If errors:, must have at least one entry with id
    if re.search(r"^errors:", content, re.MULTILINE):
        if not re.search(r'^\s*id:\s*"', content, re.MULTILINE):
            print("  ❌ Error entries must have 'id:' field")
            print("  Format: id: \"CATEGORY-NNN\"")
            sys.exit(2)

    # Check 4: ID format validation (CATEGORY-NNN)
    if re.search(r'^\s*id:\s*"[A-Z]+-[0-9]{3}"', content, re.MULTILINE):
        print("  ✅ ID format is valid (CATEGORY-NNN)")
    else:
        print("  ⚠️  ID may not follow CATEGORY-NNN format")
        print("  Recommended: ERROR-001, PATTERN-001, etc.")
        # Don't block, just warn

    # Check 5: Must have scope field
    if re.search(r"^errors:", content, re.MULTILINE):
        if not re.search(r'^\s*scope:\s*', content, re.MULTILINE):
            print("  ❌ Error entries must have 'scope:' field")
            print("  Valid scopes: universal, python, javascript, docker, postgresql, framework, domain, project")
            sys.exit(2)

    # Check 6: Must have severity field
    if re.search(r"^errors:", content, re.MULTILINE):
        if not re.search(r'^\s*severity:\s*', content, re.MULTILINE):
            print("  ❌ Error entries must have 'severity:' field")
            print("  Valid severities: critical, high, medium, low")
            sys.exit(2)

    print("✅ Quality gate passed")
    sys.exit(0)

if __name__ == "__main__":
    main()
