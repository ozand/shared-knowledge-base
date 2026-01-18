#!/usr/bin/env python3
"""
Context Utilities - Helper functions for file processing and results storage.
Used by the background agent to chunk files and save results.
"""

from pathlib import Path
from typing import List
import hashlib
import yaml


def chunk_text(text: str, chunk_size: int = 12000) -> List[str]:
    """Split text into manageable chunks.

    Args:
        text: Text to chunk
        chunk_size: Max characters per chunk

    Returns:
        List of text chunks
    """
    chunks = []
    current_pos = 0

    while current_pos < len(text):
        chunk_end = min(current_pos + chunk_size, len(text))

        # Try to end at sentence boundary if possible
        if chunk_end < len(text):
            last_period = text.rfind('.', current_pos, chunk_end)
            if last_period > current_pos + chunk_size // 2:
                chunk_end = last_period + 1

        chunks.append(text[current_pos:chunk_end])
        current_pos = chunk_end

    return chunks


def calculate_file_hash(text: str) -> str:
    """Calculate SHA256 hash of text (first 16 chars)."""
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def extract_tags_from_text(text: str) -> List[str]:
    """Extract tags from text (backtick-quoted words)."""
    import re
    tags = re.findall(r'`([a-z0-9-]+)`', text.lower())
    return list(set(tags))  # Deduplicate


def calculate_confidence(chunks_count: int, content_length: int) -> float:
    """Estimate confidence score (0-1).

    Args:
        chunks_count: Number of chunks processed
        content_length: Length of final condensed content

    Returns:
        Confidence score 0.0-1.0
    """
    # More chunks = more complex, lower confidence
    chunk_factor = max(0.7, 1.0 - (chunks_count * 0.05))
    # Longer output = more comprehensive
    length_factor = min(1.0, content_length / 5000)  # 5000 chars = 1.0
    return round((chunk_factor + length_factor) / 2, 2)


def save_condensed_file(
    output_path: Path,
    source_file: str,
    source_size_bytes: int,
    processed_at: str,
    chunks_processed: int,
    confidence_score: float,
    tags: List[str],
    condensed_content: str,
    file_hash: str,
    source_type: str
) -> bool:
    """Save condensed file with metadata.

    Args:
        output_path: Where to save the file
        source_file: Original file path
        source_size_bytes: Size of original file
        processed_at: ISO datetime
        chunks_processed: Number of chunks
        confidence_score: 0-1 confidence
        tags: List of extracted tags
        condensed_content: The condensed summary
        file_hash: Source file hash
        source_type: 'chat' or 'document'

    Returns:
        True if successful
    """
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        frontmatter = {
            "source_file": source_file,
            "source_size": f"{source_size_bytes / 1024:.1f} KB",
            "processed_at": processed_at,
            "chunks_processed": chunks_processed,
            "confidence_score": confidence_score,
            "file_hash": file_hash,
            "source_type": source_type,
            "tags": tags
        }

        frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False)

        markdown = f"""---
{frontmatter_yaml}---

# Context Summary

{condensed_content}

---

**Source**: `{source_file}`
**Archived**: {processed_at}
**Hash**: `{file_hash}`
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)

        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False


def format_chunk_analysis_prompt(chunk_text: str, chunk_number: int, total_chunks: int) -> str:
    """Format prompt for analyzing a chunk."""
    return f"""Analyze chunk {chunk_number}/{total_chunks} of a document.

Extract and organize:
1. **Key Decisions & Discussions**: Important decisions and their reasoning
2. **Technical Details**: Architecture, components, constraints
3. **Issues & Solutions**: Problems identified and how they were solved
4. **Action Items**: What was done (✓), pending (⏳), or unclear (❓)
5. **Code References**: Specific files, functions, or line numbers
6. **Tags**: Use `backtick-quoted tags` for automatic categorization

Format your response with markdown headers as shown above.

---CHUNK START---
{chunk_text}
---CHUNK END---

Provide a focused, dense summary without padding."""


def format_synthesis_prompt(chunk_summaries: List[str]) -> str:
    """Format prompt for merging chunk summaries."""
    summaries_text = "\n\n---CHUNK SEPARATOR---\n\n".join(chunk_summaries)

    return f"""Merge these {len(chunk_summaries)} chunk summaries into one unified document.

Rules:
1. Deduplicate information (keep only once)
2. Merge related decisions and technical details
3. Create timeline of issues and solutions
4. Consolidate all code references
5. Combine and categorize all tags
6. Use same format as input (markdown headers)

---CHUNK SUMMARIES START---

{summaries_text}

---CHUNK SUMMARIES END---

Produce a comprehensive, unified summary maintaining the structured format."""


if __name__ == "__main__":
    # Example usage
    test_text = "This is a test. " * 1000
    chunks = chunk_text(test_text, chunk_size=500)
    print(f"Split into {len(chunks)} chunks")
    print(f"Hash: {calculate_file_hash(test_text)}")
