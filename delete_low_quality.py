#!/usr/bin/env python3
"""
Delete low-quality KB entries (quality score < 40).
These files have been identified as having minimal value and should be removed.
"""

import os
from pathlib import Path

os.chdir('T:/Code/shared-knowledge-base')

files_to_delete = [
    'domains/catalog/categories.yaml',
    'domains/catalog/index.yaml',
    'domains/docker/errors/best-practices_meta.yaml',
    'domains/docker/errors/common-errors_meta.yaml',
    'domains/docker/errors/docker-best-practices_meta.yaml',
    'domains/docker/errors/docker-network-errors_meta.yaml',
    'domains/docker/errors/docker-security_meta.yaml',
    'domains/docker/errors/docker-volume-mounts_meta.yaml',
    'domains/framework/fastapi/patterns/websocket.yaml',
    'domains/javascript/errors/async-errors_meta.yaml',
    'domains/javascript/patterns/bookmarklet-patterns.yaml',
    'domains/postgresql/errors/disk-space-issues_meta.yaml',
    'domains/postgresql/patterns/migration-upgrade.yaml',
    'domains/postgresql/patterns/performance-tuning.yaml',
    'domains/python/errors/csrf-auth_meta.yaml',
    'domains/python/errors/imports_meta.yaml',
    'domains/python/errors/testing_meta.yaml',
    'domains/python/errors/type-checking_meta.yaml',
    'domains/universal/agent-instructions/base-instructions.yaml',
    'domains/universal/errors/redis-errors_meta.yaml',
    'domains/universal/patterns/build-automation.yaml',
    'domains/universal/patterns/clean-architecture.yaml',
    'domains/universal/patterns/debugging-port-conflicts_meta.yaml',
    'domains/universal/patterns/filesystem-management_meta.yaml',
    'domains/universal/patterns/git-workflow.yaml',
    'domains/universal/patterns/git-workflow_meta.yaml',
    'domains/vps/errors/logs_meta.yaml',
    'domains/vps/errors/memory_meta.yaml',
    'domains/vps/errors/networking_meta.yaml',
    'domains/vps/patterns/backup-automation.yaml',
    'domains/vps/patterns/backup-automation_meta.yaml',
    'domains/vps/patterns/best-practices.yaml',
    'domains/vps/patterns/best-practices_meta.yaml',
    'domains/vps/patterns/nginx-analytics.yaml',
    'domains/vps/patterns/nginx-analytics_meta.yaml',
    'domains/vps/patterns/service-optimization.yaml',
    'domains/vps/patterns/service-optimization_meta.yaml',
    'domains/vps/patterns/tailscale-funnel.yaml',
    'domains/vps/patterns/tailscale-funnel_meta.yaml',
    'domains/vps/patterns/xray-management.yaml',
    'domains/vps/patterns/xray-management_meta.yaml',
]

deleted_count = 0
not_found = []

for filepath in files_to_delete:
    path = Path(filepath)
    if path.exists():
        path.unlink()
        print(f"✅ Deleted: {filepath}")
        deleted_count += 1
    else:
        not_found.append(filepath)
        print(f"⚠️  Not found: {filepath}")

print(f"\n{'='*60}")
print(f"Summary:")
print(f"  Deleted: {deleted_count} files")
print(f"  Not found: {len(not_found)} files")

if not_found:
    print(f"\nFiles not found:")
    for f in not_found:
        print(f"  - {f}")
