#!/usr/bin/env python3
"""
Context Condenser - Helper script for context archiving.
Note: This script DOES NOT perform condensation itself.
It prepares files for the Agent to condense manually.
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Tuple
from dataclasses import dataclass
import hashlib

@dataclass
class CondensingResult:
    """Result of context condensing operation."""
    source_file: str
    source_size_bytes: int
    processed_at: str
    chunks_processed: int
    total_tokens_processed: int
    confidence_score: float
    tags: List[str]
    condensed_content: str
    file_hash: str
    source_type: str  # 'chat' or 'document'


class ContextCondenser:
    """Helper for context condensation (Agent-driven)."""

    CHUNK_SIZE = 12000  # characters per chunk

    def __init__(self):
        """Initialize without API key."""
        pass

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into manageable chunks."""
        chunks = []
        current_pos = 0
        while current_pos < len(text):
            chunk_end = min(current_pos + self.CHUNK_SIZE, len(text))
            # Try to end at sentence boundary if possible
            if chunk_end < len(text):
                last_period = text.rfind('.', current_pos, chunk_end)
                if last_period > current_pos + self.CHUNK_SIZE // 2:
                    chunk_end = last_period + 1
            chunks.append(text[current_pos:chunk_end])
            current_pos = chunk_end
        return chunks

    def prepare_condensation(self, file_path: str, source_type: str = "chat") -> dict:
        """Prepare chunks for Agent to condense."""
        path_obj = Path(file_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        file_size = len(text.encode('utf-8'))
        file_hash = hashlib.sha256(text.encode()).hexdigest()[:16]

        # Split into chunks
        chunks = self._chunk_text(text)
        
        return {
            "source_file": str(file_path),
            "chunks": chunks,
            "metadata": {
                "source_size_bytes": file_size,
                "file_hash": file_hash,
                "source_type": source_type,
                "processed_at": datetime.now().isoformat()
            }
        }

def create_markdown_output(metadata: dict, condensed_content: str, tags: List[str]) -> str:
    """Create final markdown output with metadata."""
    frontmatter = {
        "source_file": metadata.get("source_file"),
        "source_size": f"{metadata.get('source_size_bytes', 0) / 1024:.1f} KB",
        "processed_at": metadata.get("processed_at"),
        "file_hash": metadata.get("file_hash"),
        "tags": tags
    }

    frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False)

    markdown = f"""---
{frontmatter_yaml}---

# Context Summary

{condensed_content}

---

**Source**: `{metadata.get("source_file")}`
**Archived**: {metadata.get("processed_at")}
**Hash**: `{metadata.get("file_hash")}`
"""
    return markdown


if __name__ == "__main__":
    # Example usage for CLI
    if len(sys.argv) < 2:
        print("Usage: python context_condenser.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    condenser = ContextCondenser()
    data = condenser.prepare_condensation(file_path)
    
    print(f"Prepared {len(data['chunks'])} chunks from {file_path}")
    print("INSTRUCTIONS FOR AGENT:")
    print("1. Read the file content in chunks.")
    print("2. Summarize each chunk.")
    print("3. Merge summaries into a final document.")
    print("4. Save to .kb/project/context-archive/condensed/...")
