# Context Condense

**Command:** `/context-condense <file_path> [--type chat|document]`

**Description:** Condense a large file or chat into a searchable summary using Claude's analysis capabilities.

## How It Works

1. **Validate** the file (size, format, readability)
2. **Launch** a background analysis task
3. **Claude analyzes** the file, extracting:
   - Key decisions and discussions
   - Technical details and architecture
   - Issues and solutions
   - Action items (completed/pending/unclear)
   - Code references
   - Auto-extractable tags
4. **Save** condensed summary to `.context-archive/condensed/`
5. **Update** archive index automatically

## Usage

```bash
# Basic (chat type)
/context-condense path/to/chat-2026-01-18.txt

# Specify document type
/context-condense large-document.md --type document

# Chat type explicitly
/context-condense notes.txt --type chat
```

## Parameters

- **file_path** (required): Path to file to condense
  - Can be relative or absolute
  - Chat logs, markdown docs, or any text file
  - Size: tested up to 1MB (larger files still work but take longer)

- **--type** (optional): File type classification
  - `chat` (default): Chat logs, conversation exports, session notes
  - `document`: Technical docs, specifications, architecture, research

## Output

Creates condensed summary in `.context-archive/condensed/` structure:

```
.context-archive/
├── condensed/
│   ├── chats/
│   │   └── 2026-01-18-session.condensed.md
│   └── documents/
│       └── architecture.condensed.md
└── index/
    └── archive-index.yaml (auto-updated)
```

## Example Summary Output

```yaml
---
source_file: "sources/chats/2026-01-18-discussion.txt"
source_size: "175.3 KB"
processed_at: "2026-01-18T14:30:00Z"
chunks_processed: 14
confidence_score: 0.88
file_hash: "a1b2c3d4e5f6"
source_type: chat
tags:
  - authentication
  - jwt
  - security
  - database
  - performance
---

# Context Summary

## Key Decisions
- Decided to use JWT instead of sessions
- Chose PostgreSQL for auth data

## Technical Details
- Token format: RS256 JWT
- Expiry: 24 hours
- Refresh storage: httpOnly cookies

## Issues & Solutions
- Issue: Token validation slow
  Solution: Cache scopes in Redis (15min TTL)
  Result: 90% latency reduction

## Action Items
- ✓ JWT implementation complete
- ⏳ Redis caching in progress
- ❓ Should we support OAuth?

## Code References
- src/auth/jwt.ts lines 45-120
- db/migrations/001-auth.sql

## Tags
`authentication` `jwt` `security` `database` `performance`
```

## Search Archive

After condensing, search for related content:

```bash
# Search by keyword
python tools/archive_search.py "authentication"

# Search by tag
python tools/archive_search.py "" --tag jwt,security

# Search specific type
python tools/archive_search.py "database" --type chat

# View archive stats
python tools/archive_index.py
```

## Processing Details

- **Speed**: ~1-2 minutes for typical files (depends on length and complexity)
- **Quality**: Comprehensive analysis using Claude's understanding
- **Tags**: Automatically extracted from analysis (backtick-quoted words)
- **Confidence**: Scored 0.0-1.0 based on content clarity and completeness
- **Index**: Updated automatically for fast future searches

## What Gets Extracted

### Key Decisions
Important choices made during discussions/design, with reasoning

### Technical Details
Architecture, components, constraints, implementations, standards

### Issues & Solutions
Problems identified, how they were solved, results achieved

### Action Items
- **✓ Done**: Completed tasks
- **⏳ Pending**: Work in progress
- **❓ Unclear**: Decisions still pending or unclear direction

### Code References
Specific files, functions, classes, line numbers mentioned

### Tags
Auto-extracted categories for organization and discovery

## Tips for Best Results

1. **For chat logs:**
   - Export the full conversation
   - Include context about what was being solved
   - Longer chats are fine (will be split into chunks)

2. **For documents:**
   - Include table of contents or section headers
   - Clear structure helps tag extraction
   - Can be specifications, architecture docs, research notes

3. **After condensing:**
   - Use tags to find related discussions
   - Search keywords to reference specific information
   - Review confidence scores (0.85+ = high quality)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| File not found | Use absolute path or verify relative path from project root |
| YAML format error in output | Check tags don't use special characters |
| Low confidence score | File may be very complex; still usable but review content |
| Archive index not updated | Check `.context-archive/` directory exists |

## Integration

Works with:
- **Knowledge Base**: Reference KB entries from condensed files
- **Search**: Full-text and tag-based search across all condensed files
- **Project Files**: Archive can reference code and documentation

## Architecture

```
/context-condense file.txt
    ↓
Validate & prepare file
    ↓
Launch background analysis agent
    ↓
Agent analyzes file chunks
    ↓
Claude extracts key information
    ↓
Agent merges analyses
    ↓
Save to .context-archive/
    ↓
Update index & metadata
    ↓
Ready to search!
```

## See Also

- `python tools/archive_search.py` - Search condensed files
- `python tools/archive_index.py` - View archive statistics
- `.context-archive/README.md` - Archive system documentation
- `docs/CONTEXT-ARCHIVE.md` - Complete reference guide

---

**Version:** 2.0
**Uses:** Claude analysis (no separate API calls)
**Default Type:** chat
**Status:** Ready to use
