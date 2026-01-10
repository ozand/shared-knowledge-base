#!/usr/bin/env python
"""
Stop Hook: Check if KB index needs rebuilding
Reminds to rebuild index after YAML changes
"""

import sys
import json
import subprocess

def main():
    # Check if there are uncommitted YAML changes
    try:
        # Get staged YAML files
        result = subprocess.run(
            ['git', 'diff', '--name-only', '--cached'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            modified_files = [
                f for f in result.stdout.strip().split('\n')
                if f and (f.endswith('.yaml') or f.endswith('.yml'))
            ]

            if modified_files:
                print("### ⚠️  YAML Files Modified")
                for f in modified_files:
                    print(f"  - {f}")
                print("")
                print("📌 Don't forget to rebuild the index:")
                print("   python tools/kb.py index --force -v")
    except:
        pass

    sys.exit(0)

if __name__ == "__main__":
    main()
