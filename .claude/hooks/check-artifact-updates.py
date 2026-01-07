#!/usr/bin/env python
"""
SessionStart Hook: Check for SKU Artifact Updates
Runs when Claude Code session starts to notify about available artifact updates
"""

import os
import sys
import yaml
import subprocess
from pathlib import Path
from datetime import datetime, timedelta


def main():
    """Main hook logic"""

    # Configuration
    SKU_CHECK_INTERVAL_HOURS = int(os.environ.get('SKU_CHECK_INTERVAL_HOURS', '24'))
    STATE_FILE = Path.home() / '.sku' / 'update_check_state.yaml'

    # Check if sku is available
    try:
        result = subprocess.run(
            ['uvx', '--help'],
            capture_output=True,
            timeout=5,
            text=True
        )
        if result.returncode != 0:
            return  # uvx not available
    except:
        return  # uvx not available

    # Check if we should run (throttled)
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            state = yaml.safe_load(f)

        if state:
            last_check = datetime.fromisoformat(state.get('last_check', '2020-01-01'))
            if datetime.now() - last_check < timedelta(hours=SKU_CHECK_INTERVAL_HOURS):
                return  # Too soon, skip check

    # Check for updates in background (non-blocking)
    try:
        result = subprocess.run(
            ['uvx', 'sku', 'check-updates'],
            capture_output=True,
            timeout=30,
            text=True,
            env={**os.environ, 'SKU_NO_COLOR': '1'}
        )

        # Parse output
        output = result.stdout + result.stderr

        # Check if there are updates
        if 'update(s) available' in output.lower() or 'updates available' in output.lower():
            # Print notification
            print("\n" + "="*70)
            print("📦 SKU ARTIFACT UPDATES AVAILABLE")
            print("="*70)
            print("\nThe following shared artifacts have updates:")
            print(output)

            # Show quick action
            print("\nQuick commands:")
            print("  uvx sku update --all    - Update all (patches auto)")
            print("  uvx sku check-updates   - See all available updates")
            print("="*70 + "\n")

        # Update state
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            yaml.dump({
                'last_check': datetime.now().isoformat(),
                'session_start': True
            }, f)

    except subprocess.TimeoutExpired:
        # Don't block session start on slow checks
        pass
    except Exception as e:
        # Silently fail - don't interrupt session start
        pass


if __name__ == '__main__':
    main()
