#!/usr/bin/env python3
"""
kb_config - Knowledge Base Configuration

Provides KBConfig class for configuration management.
Extracted from kb.py for v3.0 modularity.

Author: Knowledge Base Curator
Version: 1.0.0
License: MIT
"""

import yaml
from pathlib import Path
from typing import Optional


class KBConfig:
    """Knowledge base configuration."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()

        # Smart detection: check if we're in shared-knowledge-base repository
        # (has entries in root directory vs docs/knowledge-base structure)
        self.kb_dir = self._detect_kb_dir()
        self.kb_root = self.kb_dir  # Alias for compatibility
        self.cache_root = self.kb_dir / ".cache"  # Alias for compatibility
        self.shared_dir = self.kb_dir / "shared"
        self.cache_dir = self.kb_dir / ".cache"
        self.index_db = self.cache_dir / "kb_index.db"

        # Create cache directory if needed
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _detect_kb_dir(self) -> Path:
        """Detect KB directory - handles both standard and shared-kb-repo layouts."""
        cwd = self.project_root

        # Check for shared-knowledge-base repository layout (entries in root)
        # Look for errors/ or patterns/ directories anywhere in the tree
        has_kb_structure = any(
            d.is_dir() and d.name in ['errors', 'patterns']
            for d in cwd.rglob('*')
            if '.git' not in str(d) and '__pycache__' not in str(d) and '.cache' not in str(d)
        )

        if has_kb_structure:
            # This is the shared-knowledge-base repository itself
            return cwd

        # Standard project layout: docs/knowledge-base
        standard_kb = cwd / "docs" / "knowledge-base"
        if standard_kb.exists():
            return standard_kb

        # Fallback to docs/knowledge-base
        return cwd / "docs" / "knowledge-base"

    @classmethod
    def from_file(cls, config_path: Path) -> 'KBConfig':
        """Load configuration from YAML file."""
        with config_path.open() as f:
            config_data = yaml.safe_load(f)

        instance = cls()
        # Override defaults with config file values
        for key, value in config_data.items():
            if hasattr(instance, key):
                setattr(instance, key, Path(value) if 'dir' in key else value)

        return instance
