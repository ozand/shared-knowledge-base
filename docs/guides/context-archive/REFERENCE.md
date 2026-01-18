# Context Archive System

**Version:** 1.0
**Status:** Production Ready
**Last Updated:** 2026-01-18

---

## Overview

The **Context Archive** system is a distributed knowledge management solution for capturing, condensing, and retrieving context from large files and chat logs.

It solves the problem: *"I have a large chat log or document, but Claude can't fit it in the context window. How do I preserve the important knowledge for future reference?"*

**Key Features:**
- ✅ Automatic chunking of large files (no manual splitting)
- ✅ AI-powered semantic condensing (extracts key decisions, issues, code refs)
- ✅ Tag-based discovery (automatic tag extraction)
- ✅ Full-text search across condensed archive
- ✅ Confidence scoring (0-1 reliability metric)
- ✅ Index-based fast lookups
- ✅ Processing metrics and logs
- ✅ Integration with Knowledge Base and project files

---

## Architecture

### Components

```
┌─────────────────────────────────────────────────────┐
│  User: /context-condense file.txt                   │
└──────────────────┬──────────────────────────────────┘
                   │
         ┌─────────▼──────────┐
         │ condense_background │
         │      _agent.py      │
         └─────────┬───────────┘
                   │
     ┌─────────────┼──────────────┐
     │             │              │
┌────▼────┐   ┌────▼────┐   ┌────▼────┐
│ Context │   │ Archive │   │ Archive │
│Condenser│──▶│ Index   │   │ Search  │
│  .py    │   │  .py    │   │  .py    │
└─────────┘   └─────────┘   └─────────┘
     │             │
     └─────┬───────┘
           │
      ┌────▼──────────────────────────┐
      │  .kb/project/context-archive/ │
      │  ├── sources/                 │
      │  ├── condensed/               │
      │  ├── index/                   │
      │  └── metadata/                │
      └───────────────────────────────┘
```

### Data Flow

1. **Input**: Large file (chat log, document)
2. **Chunking**: Split into 12KB chunks
3. **Condensing**: Each chunk analyzed by Claude
4. **Synthesis**: Chunks merged into unified summary
5. **Indexing**: Summary added to archive catalog
6. **Output**: Searchable, tagged knowledge entry

### File Organization

```
.kb/project/context-archive/
│
├── sources/                          # Original files
│   ├── chats/
│   │   ├── 2026-01-18-session.txt   # Raw chat export
│   │   └── links.yaml                # References to external files
│   └── documents/
│       └── architecture-v2.md
│
├── condensed/                        # AI-generated summaries
│   ├── chats/
│   │   └── 2026-01-18-session.condensed.md
│   └── documents/
│       └── architecture-v2.condensed.md
│
├── index/                            # Discovery system
│   ├── archive-index.yaml            # Catalog of all entries
│   └── search-cache.json             # Precomputed indexes
│
├── metadata/                         # Operations & logs
│   ├── archive-config.yaml           # System configuration
│   ├── processing-log.yaml           # What was processed, when, how
│   └── statistics.yaml               # Archive metrics
│
├── README.md                         # User guide
├── .gitignore                        # Keep sources local
└── archive-config.yaml               # Settings
```

---

## Quick Start

### 1. Initialize Archive

```bash
python tools/init_context_archive.py

# Or specify custom location:
python tools/init_context_archive.py /path/to/archive
```

Creates directory structure and configuration.

### 2. Condense a File

```bash
# From Claude Code (uses Haiku by default - cost-efficient):
/context-condense path/to/large-file.txt

# From command line:
python tools/condense_background_agent.py path/to/file.txt --type chat

# For documents:
python tools/condense_background_agent.py architecture.md --type document

# For complex files requiring better quality (Opus model):
/context-condense path/to/large-file.txt --model claude-opus-4-5-20251101
python tools/condense_background_agent.py path/to/file.txt --model claude-opus-4-5-20251101
```

**What happens:**
- File is chunked into 12KB pieces
- Each chunk analyzed using specified model (Haiku by default)
  - **Haiku** (default): Faster, cost-efficient (~$0.50/500KB)
  - **Opus** (optional): Higher quality, slower (~$2/500KB)
- Summaries merged and deduplicated
- Tags automatically extracted
- Archive index updated
- Metadata logged

### 3. Search Archive

```bash
# By keyword
python tools/archive_search.py "authentication"

# By tag
python tools/archive_search.py "" --tag security,authentication

# Advanced search with filters
python tools/archive_search.py "database" --tag performance --type document
```

### 4. View Statistics

```bash
python tools/archive_index.py

# Shows:
# - Total files processed
# - Available tags
# - Recent entries
# - Archive size
# - Processing statistics
```

---

## Condensed File Format

Each condensed file includes YAML frontmatter and structured content.

### Example Output

```yaml
---
source_file: "sources/chats/2026-01-18-auth-discussion.txt"
source_size: "542.3 KB"
processed_at: "2026-01-18T14:30:00Z"
chunks_processed: 8
tokens_used: 24567
confidence_score: 0.88
file_hash: "a1b2c3d4e5f6g7h8"
tags:
  - authentication
  - jwt
  - security
  - database
  - performance
---

# Context Summary

## Key Decisions & Discussions
- **Decision**: Use JWT tokens instead of session cookies
  - Reasoning: Microservices architecture requires stateless auth
  - Considered: OAuth2 (too complex for MVP)
  - Considered: Sessions with Redis (doesn't scale to distributed)

- **Decision**: PostgreSQL for auth data (not NoSQL)
  - Reasoning: ACID guarantees needed for user transactions
  - Considered: MongoDB (team prefers SQL)

## Technical Details

### Authentication Architecture
- JWT tokens with 24-hour expiry
- Refresh tokens stored in secure httpOnly cookies
- Token signing: RS256 (RSA keys)
- Scope system: basic, admin, api

### Database Schema
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  password_hash VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tokens (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  type VARCHAR(20), -- 'access' | 'refresh'
  expires_at TIMESTAMP
);
```

### Key Components
- src/auth/jwt.ts - Token creation/validation
- src/auth/session.ts - Session middleware
- src/auth/passwords.ts - Hashing (bcrypt with 12 rounds)
- db/migrations/001-auth.sql - Database setup

## Issues & Solutions

### Issue 1: Token Validation Performance
**Problem**: Validating JWT on every request was slow
**Root Cause**: Fetching scopes from database
**Solution**: Cache token scopes in Redis (15min TTL)
**Result**: 90% reduction in auth latency
**Code**: src/auth/jwt-cache.ts lines 34-67

### Issue 2: Password Reset Security
**Problem**: Reset links didn't expire properly
**Root Cause**: Used string tokens (no expiry logic)
**Solution**: Use ULID + timestamp, verify within 1 hour
**Status**: ✅ Implemented (db migration 002)

### Issue 3: CORS with Auth Headers
**Problem**: Auth headers blocked by browser
**Root Cause**: CORS middleware didn't allow Authorization
**Solution**: Add to CORS config: `credentials: 'include'`
**Reference**: src/middleware/cors.ts:45-50

## Action Items Status

- ✅ **DONE**: JWT token generation & validation
- ✅ **DONE**: Database user schema
- ⏳ **IN PROGRESS**: Redis caching for scopes
- ⏳ **IN PROGRESS**: Password reset flow
- ❓ **UNCLEAR**: Should we support OAuth2 providers?
- ❌ **BLOCKED**: Need security review before production

## Code References

### Authentication
- `src/auth/jwt.ts` lines 1-120 - Token creation
- `src/auth/jwt.ts` lines 121-200 - Token validation
- `src/auth/middleware.ts` - Express middleware

### Database
- `db/migrations/001-auth.sql` - User & token tables
- `db/migrations/002-password-reset.sql` - Reset tokens

### Tests
- `tests/auth.test.ts` - Auth unit tests
- `tests/integration/auth-flow.test.ts` - End-to-end flows

## Related Files & Context

- **Architecture Doc**: `docs/architecture.md` (parent: overall system design)
- **Security Policy**: `.policy/auth-security.md` (related: security considerations)
- **Performance**: Previous session discussed caching (see 2026-01-16 log)

---

## Tags & Metadata

### Extracted Tags
`authentication` `jwt` `security` `database` `performance` `caching` `api` `typescript`

### Search Keywords
JWT, token validation, session management, password hashing, scopes, CORS, security

### Confidence Metrics
- **Semantic Completeness**: 0.92 (high - clear decisions documented)
- **Technical Accuracy**: 0.88 (good - code references provided)
- **Actionability**: 0.85 (good - clear next steps)
- **Overall Confidence**: 0.88

### Processing Metadata
- **Processed By**: claude-opus-4-5-20251101
- **Processed At**: 2026-01-18T14:30:00Z
- **Chunks Analyzed**: 8
- **Tokens Used**: 24,567
- **File Hash**: a1b2c3d4e5f6g7h8 (detect if source changed)

---

## Search & Discovery

### Search Methods

#### 1. Full-Text Search
```bash
python tools/archive_search.py "jwt"
# Returns: All condensed files mentioning JWT
```

**Uses**: Keyword matching with context extraction (200 chars around match)

#### 2. Tag-Based Search
```bash
python tools/archive_search.py "" --tag authentication

# Multiple tags (OR logic):
python tools/archive_search.py "" --tag authentication,security

# From API:
search.search_by_tags(['authentication', 'security'], match_all=False)
```

**Returns**: All files with any specified tag

#### 3. Metadata Filters
```bash
python tools/archive_search.py "query" --min-confidence 0.85
# Only files with high confidence summaries

# By type:
python tools/archive_search.py "auth" --type chat
# Only condensed chat logs
```

#### 4. Advanced Search (Combine All)
```python
from tools.archive_search import ArchiveSearch

search = ArchiveSearch(Path(".context-archive"))
results = search.advanced_search(
    query="token validation",
    tags=["authentication", "performance"],
    file_type="chat",
    min_confidence=0.80
)
```

### Search Results Format

```python
[
  {
    "source_file": "sources/chats/2026-01-18-auth.txt",
    "condensed_file": "condensed/chats/2026-01-18-auth.condensed.md",
    "type": "chat",
    "confidence": 0.88,
    "tags": ["authentication", "jwt", "security"],
    "matches": 3,
    "preview": "...JWT tokens instead of session cookies for microservices..."
  },
  ...
]
```

### Recommendations

Get related files based on shared tags:

```python
search = ArchiveSearch(Path(".context-archive"))
recommendations = search.get_recommendations("sources/chats/2026-01-18-auth.txt")
# Returns: [{"source_file": "...", "shared_tags": ["authentication"], ...}]
```

---

## Integration with Other Systems

### Knowledge Base Integration

| System | Purpose | Interaction |
|--------|---------|-------------|
| **Shared KB** | Verified, universal solutions | Reference from archive |
| **Project KB** | Local, business-specific | Can contain archive references |
| **Context Archive** | Session/project notes | Complements both KB tiers |

**Usage:**
- Found pattern in archive → Move to Project KB if it's local knowledge
- Archive references universal pattern → Link to Shared KB entry

### Claude Code Workflow

```
User asks question
    ↓
Claude searches context archive first
    ↓
If found: Use condensed summary for context
    ↓
If not found: Search knowledge bases
    ↓
Solve the problem + offer to /context-condense for future
```

---

## Configuration

### archive-config.yaml

```yaml
version: "1.0"
archive_root: ".kb/project/context-archive"

settings:
  # Default model for condensing (can be overridden via --model flag)
  # Options:
  #   - claude-haiku-4-5-20251001 (default): Fast, cost-efficient (~$0.50/500KB)
  #   - claude-opus-4-5-20251101: Higher quality (~$2/500KB)
  condensing_model: "claude-haiku-4-5-20251001"

  # Size of each chunk (chars)
  chunk_size: 12000

  # Minimum confidence to include in search
  confidence_threshold: 0.6

  # Auto-extract tags from condensed content
  auto_tagging: true

retention:
  # Keep original source files
  keep_source_files: true

  # Keep processing logs
  keep_processing_logs: true

  # Archive condensed files older than N days
  archive_old_condensed_after_days: 365
```

### Environment Variables

```bash
# Required for condensing
export ANTHROPIC_API_KEY="sk-..."

# Optional: specify archive location (default: .kb/project/context-archive)
export CONTEXT_ARCHIVE_ROOT="/path/to/archive"
```

---

## Performance & Optimization

### Processing Metrics

**Example: 500KB chat log**
- Chunks: 42 (@ 12KB each)
- Time: 3-5 minutes
- Tokens: 15,000-20,000
- Output: ~8KB condensed (20:1 compression)

**Factors affecting speed:**
- File size (obviously)
- Complexity (code + discussion = slower)
- API latency (usually 1-2s per chunk)

### Cost Estimation

Using Claude Opus (as of 2026-01):
- Input: $15/1M tokens
- Output: $45/1M tokens
- Example: 500KB file
  - Tokens: ~18,000
  - Cost: ~$0.50-0.70
  - Archive value: Weeks of searchability

### Optimization Tips

1. **Chunk Large Files Externally**: Pre-split very large files (>10MB)
2. **Batch Similar Files**: Process similar topics together for tag consolidation
3. **Cleanup Old Entries**: Archive entries older than 6 months (low reference value)
4. **Cache Search Results**: Archive index is YAML, caching queries is efficient

---

## Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| "File not found" | Use absolute path or check relative path from project root |
| No tags extracted | Add headers/sections to file; Claude needs structure |
| Low confidence (<0.6) | File may be too complex; try splitting manually |
| "API key not found" | Export ANTHROPIC_API_KEY before running |
| Search returns nothing | Check file was actually condensed (see archive-index.yaml) |
| Import errors | Install requirements: `pip install -r tools/requirements.txt` |

### Debug Commands

```bash
# Verify archive structure
ls -la .kb/project/context-archive/

# Check index
cat .kb/project/context-archive/index/archive-index.yaml

# View processing log
cat .kb/project/context-archive/metadata/processing-log.yaml

# Test search directly
python -c "from tools.archive_search import ArchiveSearch; print(ArchiveSearch(Path('.kb/project/context-archive')).index.get_all_tags())"
```

---

## Best Practices

### When to Use Context Archive

✅ **Good Use Cases:**
- Large chat logs from complex problem-solving sessions
- External documentation you need to reference later
- Project architecture discussions
- Meeting notes or design decisions
- Long troubleshooting sessions

❌ **Not Ideal For:**
- Frequently-updated files (re-condense each time)
- Real-time data (archive becomes stale)
- Sensitive data (archive stored locally but indexed)
- Simple notes (just save as markdown)

### Organization Strategy

```
.kb/project/context-archive/
├── sources/chats/
│   ├── 2026-01-15-project-kickoff.txt
│   ├── 2026-01-18-authentication-design.txt
│   └── 2026-01-19-deployment-planning.txt
│
├── sources/documents/
│   ├── api-specification.md
│   ├── deployment-guide.md
│   └── architecture-diagrams.md
```

**Naming Convention:**
- Chats: `YYYY-MM-DD-topic.txt`
- Documents: `descriptive-name.md`

### Maintenance

1. **Weekly**: Review recent files, remove duplicates
2. **Monthly**: Check archive size, archive old files
3. **Quarterly**: Review tags, consolidate similar entries
4. **Annually**: Export statistics, archive to cold storage if needed

---

## API Reference

### ContextCondenser

```python
from tools.context_condenser import ContextCondenser

condenser = ContextCondenser()
result = condenser.condense_file("path/to/file.txt", source_type="chat")

# result contains:
# - source_file: str
# - source_size_bytes: int
# - processed_at: str (ISO datetime)
# - chunks_processed: int
# - total_tokens_processed: int
# - confidence_score: float (0-1)
# - tags: List[str]
# - condensed_content: str (the summary)
# - file_hash: str
# - source_type: str ("chat" or "document")
```

### ArchiveIndex

```python
from tools.archive_index import ArchiveIndex

index = ArchiveIndex(Path(".kb/project/context-archive"))

# Add entry
index.add_entry(source_file, condensed_file, metadata_dict)

# Query
entries = index.get_entries_by_tag("authentication")
entries = index.get_entries_by_type("chat")
all_tags = index.get_all_tags()
stats = index.get_stats()
```

### ArchiveSearch

```python
from tools.archive_search import ArchiveSearch

search = ArchiveSearch(Path(".kb/project/context-archive"))

# Full-text
results = search.search_full_text("authentication")

# By tags
results = search.search_by_tags(["auth", "security"])

# Advanced
results = search.advanced_search(
    query="JWT",
    tags=["security"],
    file_type="chat",
    min_confidence=0.85
)

# Recommendations
related = search.get_recommendations("sources/chats/2026-01-18-auth.txt")
```

---

## Contributing

To improve the Context Archive system:

1. **Report Issues**: Use GitHub issues with tag `context-archive`
2. **Feature Requests**: Document use cases that require new functionality
3. **Improvements**: Suggest optimizations or UI enhancements

---

## See Also

- `.claude/skills/context-condense.md` - Skill documentation
- `.kb/project/context-archive/README.md` - User guide
- `docs/SHARED-KNOWLEDGE-BASE.md` - Main KB documentation
- `tools/archive_search.py` - Search implementation
- `tools/context_condenser.py` - Condensing implementation

---

**Version:** 1.0
**Last Updated:** 2026-01-18
**Status:** Production Ready
**Maintained By:** Claude Code Agent
