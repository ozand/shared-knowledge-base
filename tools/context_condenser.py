#!/usr/bin/env python3
"""
Context Condenser - Semantic compression and condensing for large text files.
Converts large chats/documents into dense, agent-friendly summaries.
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Tuple
from dataclasses import dataclass
import hashlib

try:
    from anthropic import Anthropic
except ImportError:
    print("ERROR: anthropic package required. Install: pip install anthropic")
    sys.exit(1)


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
    """Main context condensing engine."""

    CHUNK_SIZE = 12000  # characters per chunk
    DEFAULT_MODEL = "claude-haiku-4-5-20251001"  # Default: Haiku for cost-efficiency

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize with Anthropic client.

        Args:
            api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)
            model: Model to use (default: claude-haiku-4-5-20251001)
                   For better quality on complex docs, use claude-opus-4-5-20251101
        """
        api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable required")
        self.client = Anthropic(api_key=api_key)
        self.model = model or os.environ.get("CONDENSE_MODEL", self.DEFAULT_MODEL)

    CONDENSING_PROMPT = """You are a Context Condenser - an expert at extracting knowledge from large texts.
Your task is to analyze the provided text chunk and extract:

1. **Key Decisions & Discussions**: What important decisions were made and why
2. **Technical Details**: Architecture, components, constraints
3. **Issues & Solutions**: Problems identified and how they were solved
4. **Action Items**: What was done, what's pending, what's unclear
5. **Code References**: Specific files, functions, or line numbers mentioned
6. **Important Tags**: Categories/topics (authentication, database, performance, etc.)

Format your response as:

## Key Decisions
- [decision 1]
- [decision 2]

## Technical Details
- [detail 1]
- [detail 2]

## Issues & Solutions
- [problem] → [solution]

## Action Items
- ✓ [completed]
- ⏳ [pending]
- ❓ [unclear]

## Code References
- [file]: [description]

## Tags
`tag1` `tag2` `tag3`

Be concise but comprehensive. Preserve all critical information."""

    SYNTHESIS_PROMPT = """You are merging condensed summaries from multiple chunks into one cohesive document.

Provided summaries from {chunk_count} chunks of the same source:

{chunk_summaries}

---

Create a unified summary that:
1. Deduplicates information (keep only once if repeated)
2. Merges related decisions and technical details
3. Creates a complete timeline of issues and solutions
4. Consolidates all code references
5. Combines and categorizes all tags

Output in the same format as the chunk summaries but comprehensive and deduplicated."""

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

    def _condense_chunk(self, chunk: str) -> Tuple[str, int]:
        """Condense a single chunk using Claude."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": f"{self.CONDENSING_PROMPT}\n\n---CHUNK START---\n{chunk}\n---CHUNK END---"
                }
            ]
        )
        content = response.content[0].text
        tokens = response.usage.output_tokens + response.usage.input_tokens
        return content, tokens

    def _synthesize_chunks(self, chunk_summaries: List[str]) -> Tuple[str, int]:
        """Merge chunk summaries into unified document."""
        if len(chunk_summaries) == 1:
            return chunk_summaries[0], 0

        summaries_text = "\n\n---CHUNK SEPARATOR---\n\n".join(chunk_summaries)
        prompt = self.SYNTHESIS_PROMPT.format(
            chunk_count=len(chunk_summaries),
            chunk_summaries=summaries_text
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text
        tokens = response.usage.output_tokens + response.usage.input_tokens
        return content, tokens

    def _extract_tags(self, content: str) -> List[str]:
        """Extract tags from condensed content."""
        import re
        # Find tags in backticks
        tags = re.findall(r'`([a-z0-9-]+)`', content.lower())
        return list(set(tags))  # Deduplicate

    def _calculate_confidence(self, chunks_count: int, content_length: int) -> float:
        """Estimate confidence score (0-1)."""
        # More chunks = more complex, lower confidence
        # Longer output = more comprehensive
        chunk_factor = max(0.7, 1.0 - (chunks_count * 0.05))
        length_factor = min(1.0, content_length / 5000)  # 5000 chars = 1.0
        return round((chunk_factor + length_factor) / 2, 2)

    def condense_file(self, file_path: str, source_type: str = "chat") -> CondensingResult:
        """Main method to condense a file."""
        path_obj = Path(file_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        file_size = len(text.encode('utf-8'))

        # Calculate hash for change detection
        file_hash = hashlib.sha256(text.encode()).hexdigest()[:16]

        # Split into chunks
        chunks = self._chunk_text(text)
        print(f"Processing {len(chunks)} chunks...")

        # Condense each chunk
        chunk_summaries = []
        total_tokens = 0
        for i, chunk in enumerate(chunks, 1):
            print(f"  Chunk {i}/{len(chunks)}...", end=" ", flush=True)
            summary, tokens = self._condense_chunk(chunk)
            chunk_summaries.append(summary)
            total_tokens += tokens
            print(f"({tokens} tokens)")

        # Synthesize all chunks
        if len(chunks) > 1:
            print(f"Synthesizing {len(chunks)} chunk summaries...")
            final_content, synthesis_tokens = self._synthesize_chunks(chunk_summaries)
            total_tokens += synthesis_tokens
        else:
            final_content = chunk_summaries[0]

        # Extract tags
        tags = self._extract_tags(final_content)

        # Create result
        result = CondensingResult(
            source_file=str(file_path),
            source_size_bytes=file_size,
            processed_at=datetime.now().isoformat(),
            chunks_processed=len(chunks),
            total_tokens_processed=total_tokens,
            confidence_score=self._calculate_confidence(len(chunks), len(final_content)),
            tags=tags,
            condensed_content=final_content,
            file_hash=file_hash,
            source_type=source_type
        )

        return result


def create_markdown_output(result: CondensingResult) -> str:
    """Create final markdown output with metadata."""
    frontmatter = {
        "source_file": result.source_file,
        "source_size": f"{result.source_size_bytes / 1024:.1f} KB",
        "processed_at": result.processed_at,
        "chunks_processed": result.chunks_processed,
        "tokens_used": result.total_tokens_processed,
        "confidence_score": result.confidence_score,
        "file_hash": result.file_hash,
        "tags": result.tags
    }

    frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False)

    markdown = f"""---
{frontmatter_yaml}---

# Context Summary

{result.condensed_content}

---

**Source**: `{result.source_file}`
**Archived**: {result.processed_at}
**Hash**: `{result.file_hash}`
"""
    return markdown


if __name__ == "__main__":
    # Example usage
    if len(sys.argv) < 2:
        print("Usage: python context_condenser.py <file_path> [--type {chat|document}]")
        sys.exit(1)

    file_path = sys.argv[1]
    source_type = "chat"
    if "--type" in sys.argv:
        source_type = sys.argv[sys.argv.index("--type") + 1]

    condenser = ContextCondenser()
    result = condenser.condense_file(file_path, source_type)

    print("\n" + "="*60)
    print(f"✓ Condensed: {Path(file_path).name}")
    print(f"  Chunks: {result.chunks_processed}")
    print(f"  Tokens: {result.total_tokens_processed}")
    print(f"  Confidence: {result.confidence_score}")
    print(f"  Tags: {', '.join(result.tags)}")
    print("="*60)
