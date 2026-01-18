#!/usr/bin/env python3
"""
Context Archive Dispatcher

Routes /context-condense requests to a background analysis agent.
The agent uses Claude's native capabilities to analyze files.

Usage:
    python condense_with_agent.py <file_path> [--type chat|document]
"""

import sys
from pathlib import Path
from datetime import datetime


def check_file_and_prepare(file_path: str) -> dict | None:
    """Validate file and prepare metadata for agent."""
    path_obj = Path(file_path)

    if not path_obj.exists():
        print(f"✗ Error: File not found: {file_path}")
        return None

    if not path_obj.is_file():
        print(f"✗ Error: Not a file: {file_path}")
        return None

    try:
        with open(path_obj, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return None

    size_bytes = len(content.encode('utf-8'))
    size_kb = size_bytes / 1024

    # Estimate chunks (12KB per chunk)
    estimated_chunks = max(1, int(size_kb / 12) + 1)

    return {
        "file_path": str(path_obj.absolute()),
        "filename": path_obj.name,
        "size_bytes": size_bytes,
        "size_kb": size_kb,
        "content": content,
        "estimated_chunks": estimated_chunks,
        "processed_at": datetime.now().isoformat()
    }


def get_agent_prompt(file_info: dict, file_type: str, archive_root: str) -> str:
    """Generate the prompt for the background analysis agent."""

    prompt = f"""You are the Context Archive Agent. Your task is to analyze and condense a file.

## File Information
- **Path**: {file_info['file_path']}
- **Name**: {file_info['filename']}
- **Size**: {file_info['size_kb']:.1f} KB
- **Type**: {file_type}
- **Estimated chunks**: {file_info['estimated_chunks']}
- **Archive root**: {archive_root}

## Your Task

1. **Analyze the content** below to extract:
   - Key decisions and discussions
   - Technical details and architecture
   - Issues and their solutions
   - Action items (completed ✓, pending ⏳, unclear ❓)
   - Code references (files, line numbers)
   - Auto-extractable tags (use `backtick format`)

2. **Create a structured summary** with markdown headers:
   ```
   ## Key Decisions
   - [decisions]

   ## Technical Details
   - [details]

   ## Issues & Solutions
   - Problem → Solution

   ## Action Items
   - ✓ Done
   - ⏳ Pending
   - ❓ Unclear

   ## Code References
   - [files and references]

   ## Tags
   `tag1` `tag2` `tag3`
   ```

3. **Save the condensed file** to:
   `.context-archive/condensed/{file_type}s/{file_info['filename']}.condensed.md`

4. **Include YAML frontmatter** with metadata:
   - source_file
   - source_size
   - processed_at
   - chunks_processed (estimate based on analysis depth)
   - confidence_score (0.0-1.0)
   - file_hash
   - source_type
   - tags (list)

5. **Update the index** at `.context-archive/index/archive-index.yaml`

6. **Log the processing** to `.context-archive/metadata/processing-log.yaml`

## File Content to Analyze

---FILE START---
{file_info['content']}
---FILE END---

## Important

- Be thorough but concise in analysis
- Use actual backticks around tags: `tag1` `tag2`
- Estimate chunks_processed based on content depth
- Calculate confidence 0-1 (complexity factor: lower for very long/complex)
- Create .context-archive directories if needed
- Format YAML properly (use yaml.dump for index)
- Report success with file location when complete

Start now and report progress as you work."""

    return prompt


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python condense_with_agent.py <file_path> [--type chat|document]")
        print("\nExample:")
        print("  python condense_with_agent.py chat.txt")
        print("  python condense_with_agent.py doc.md --type document")
        sys.exit(1)

    file_path = sys.argv[1]
    file_type = "chat"

    if "--type" in sys.argv:
        idx = sys.argv.index("--type")
        if idx + 1 < len(sys.argv):
            file_type = sys.argv[idx + 1]

    archive_root = ".context-archive"

    # Validate file
    print(f"📁 Preparing to condense: {file_path}")
    file_info = check_file_and_prepare(file_path)

    if not file_info:
        sys.exit(1)

    print(f"✓ File loaded: {file_info['size_kb']:.1f} KB")
    print(f"✓ Estimated chunks: {file_info['estimated_chunks']}")
    print()

    # Generate agent prompt
    prompt = get_agent_prompt(file_info, file_type, archive_root)

    # Now would dispatch to background agent
    # For now, print the prompt so it can be used by Claude Code
    print("="*60)
    print("AGENT PROMPT (copy below to background task)")
    print("="*60)
    print(prompt)
    print("="*60)

    # Return success
    return 0


if __name__ == "__main__":
    sys.exit(main())
