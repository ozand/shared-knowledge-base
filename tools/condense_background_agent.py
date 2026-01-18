#!/usr/bin/env python3
"""
Background Agent for Context Condensing
Processes large files and generates condensed summaries.
Integrates with Claude Code for /context-condense command.
"""

import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))

from context_condenser import ContextCondenser, create_markdown_output
from archive_index import ArchiveIndex, ProcessingLog


def condense_and_archive(file_path: str, archive_root: Path | None = None, source_type: str = "chat", model: str | None = None) -> bool:
    """
    Main condensing workflow:
    1. Condense file
    2. Save to archive
    3. Update index
    4. Log processing
    """
    if archive_root is None:
        archive_root = Path(".kb/project/context-archive")

    file_path_obj = Path(file_path)

    if not file_path_obj.exists():
        print(f"✗ File not found: {file_path}")
        return False

    archive_root = Path(archive_root)
    archive_root.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"📦 Context Condensing")
    print(f"{'='*60}")
    print(f"Source: {file_path_obj.name} ({file_path_obj.stat().st_size / 1024:.1f} KB)")

    try:
        # Step 1: Condense file
        print(f"\n1️⃣  Condensing file...")
        condenser = ContextCondenser(model=model)
        result = condenser.condense_file(str(file_path_obj), source_type)

        # Step 2: Determine output path
        condensed_dir = archive_root / "condensed"
        if source_type == "chat":
            condensed_dir = condensed_dir / "chats"
        else:
            condensed_dir = condensed_dir / "documents"

        condensed_dir.mkdir(parents=True, exist_ok=True)

        # Use original filename with .condensed.md extension
        output_name = f"{file_path_obj.stem}.condensed.md"
        output_path = condensed_dir / output_name

        # Step 3: Create markdown output
        print(f"2️⃣  Creating markdown output...")
        markdown_content = create_markdown_output(result)

        # Step 4: Save to archive
        print(f"3️⃣  Saving to archive...")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # Step 5: Update index
        print(f"4️⃣  Updating index...")
        index = ArchiveIndex(archive_root)

        # Determine relative path for storage
        try:
            rel_path = output_path.relative_to(archive_root)
        except ValueError:
            rel_path = output_path

        index.add_entry(
            source_file=str(file_path),
            condensed_file=str(rel_path),
            metadata={
                "source_size_bytes": result.source_size_bytes,
                "processed_at": result.processed_at,
                "chunks_processed": result.chunks_processed,
                "confidence_score": result.confidence_score,
                "tags": result.tags,
                "file_hash": result.file_hash,
                "source_type": result.source_type
            }
        )

        # Step 6: Log processing
        print(f"5️⃣  Logging to processing log...")
        log = ProcessingLog(archive_root / "metadata" / "processing-log.yaml")
        log.log_processing(
            source_file=str(file_path),
            result={
                "chunks_processed": result.chunks_processed,
                "tokens_used": result.total_tokens_processed,
                "confidence_score": result.confidence_score,
                "file_hash": result.file_hash
            }
        )

        # Success summary
        print(f"\n{'='*60}")
        print(f"✅ Success!")
        print(f"{'='*60}")
        print(f"Source: {file_path_obj.name}")
        print(f"Chunks: {result.chunks_processed}")
        print(f"Tokens: {result.total_tokens_processed}")
        print(f"Confidence: {result.confidence_score}")
        print(f"Tags: {', '.join(result.tags) or 'none'}")
        print(f"\nArchived to: {output_path}")
        print(f"\nYou can now search this archive with:")
        print(f"  python tools/archive_search.py 'query'")
        print(f"{'='*60}\n")

        return True

    except Exception as e:
        print(f"\n✗ Error: {e}")
        # Log error
        try:
            log = ProcessingLog(archive_root / "metadata" / "processing-log.yaml")
            log.log_error(str(file_path), str(e))
        except Exception:
            pass
        return False


def main():
    """Main entry point for background agent."""
    if len(sys.argv) < 2:
        print("Usage: python condense_background_agent.py <file> [OPTIONS]")
        print("\nOptions:")
        print("  --type {chat|document}     File type (default: chat)")
        print("  --archive PATH             Archive root (default: .kb/project/context-archive)")
        print("  --model MODEL              Model to use (default: claude-haiku-4-5-20251001)")
        print("\nExamples:")
        print("  python condense_background_agent.py chat-2026-01-18.txt")
        print("  python condense_background_agent.py large-doc.md --type document")
        print("  python condense_background_agent.py file.txt --model claude-opus-4-5-20251101")
        sys.exit(1)

    file_path = sys.argv[1]
    source_type = "chat"
    archive_root = Path(".kb/project/context-archive")
    model = None

    # Parse arguments
    if "--type" in sys.argv:
        idx = sys.argv.index("--type")
        if idx + 1 < len(sys.argv):
            source_type = sys.argv[idx + 1]

    if "--archive" in sys.argv:
        idx = sys.argv.index("--archive")
        if idx + 1 < len(sys.argv):
            archive_root = Path(sys.argv[idx + 1])

    if "--model" in sys.argv:
        idx = sys.argv.index("--model")
        if idx + 1 < len(sys.argv):
            model = sys.argv[idx + 1]

    # Run condensing
    success = condense_and_archive(file_path, archive_root, source_type, model)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
