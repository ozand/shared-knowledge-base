#!/usr/bin/env python3
"""
init_metadata.py - Initialize metadata for all knowledge base entries

This script creates _meta.yaml files for all knowledge entries in the repository.
Run this after cloning the knowledge base or after adding new entries.

Usage:
    python scripts/init_metadata.py
    python scripts/init_metadata.py --verbose
"""

import sys
from pathlib import Path

# Add tools directory to path
tools_dir = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(tools_dir))

try:
    from kb_meta import MetadataManager
except ImportError:
    print("❌ Cannot import MetadataManager")
    print("   Make sure kb_meta.py is in the tools directory")
    sys.exit(1)


def main():
    """Initialize metadata for all YAML files."""
    import argparse

    parser = argparse.ArgumentParser(description="Initialize metadata for knowledge base")
    parser.add_argument('--kb-root', type=Path, default=Path.cwd(),
                       help='Knowledge base root directory')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    print("🔍 Knowledge Base Metadata Initialization")
    print(f"   KB Root: {args.kb_root}")
    print()

    manager = MetadataManager(args.kb_root)

    # Find all YAML files
    yaml_files = []
    for ext in ['*.yaml', '*.yml']:
        yaml_files.extend(args.kb_root.rglob(ext))

    # Skip meta files and cache
    yaml_files = [
        f for f in yaml_files
        if '_meta.yaml' not in str(f)
        and '.cache' not in str(f)
        and '__pycache__' not in str(f)
    ]

    if not yaml_files:
        print("⚠️  No YAML files found")
        return

    print(f"📝 Found {len(yaml_files)} YAML files\n")

    # Process each file
    created = 0
    skipped = 0
    errors = 0

    for i, yaml_file in enumerate(yaml_files, 1):
        rel_path = yaml_file.relative_to(args.kb_root)

        # Check if metadata already exists
        meta_file = yaml_file.parent / f"{yaml_file.stem}_meta.yaml"
        if meta_file.exists():
            if args.verbose:
                print(f"[{i}/{len(yaml_files)}] ✓ Skipped (exists): {rel_path}")
            skipped += 1
            continue

        # Create metadata
        try:
            result = manager.create_meta_file(yaml_file)
            if result:
                created += 1
                if args.verbose:
                    print(f"[{i}/{len(yaml_files)}] ✓ Created: {rel_path}")
            else:
                errors += 1
                if args.verbose:
                    print(f"[{i}/{len(yaml_files)}] ✗ Failed: {rel_path}")

        except Exception as e:
            errors += 1
            print(f"✗ Error processing {rel_path}: {e}")

    # Summary
    print()
    print("📊 Summary:")
    print(f"   Created: {created}")
    print(f"   Skipped (already exist): {skipped}")
    print(f"   Errors: {errors}")
    print(f"   Total: {len(yaml_files)}")
    print()

    if created > 0:
        print("✅ Metadata initialization complete")
        print()
        print("Next steps:")
        print("  1. Review the generated _meta.yaml files")
        print("  2. Run: kb.py check-freshness")
        print("  3. Run: kb.py reindex-metadata")
    else:
        print("ℹ️  All metadata files already exist")

    return 0 if errors == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
