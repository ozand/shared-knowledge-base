# Context Archive Setup & Usage Guide

## What is Context Archive?

A system for **condensing large files and chat logs into searchable summaries** so you can preserve important context without bloating your context window.

**Problem it solves:**
- You have a 500KB chat log about an architecture decision
- Claude can't fit it all in the context window
- You need to reference it later
- **Solution:** Context Archive condenses it to a ~8KB summary with tags and references

---

## Quick Start (5 minutes)

### Step 1: Already Done! ✅
The archive is pre-initialized at `.kb/project/context-archive/`

### Step 2: Prepare Your File
Export or prepare a text file you want to condense:
- Chat logs (copy-paste chat history into .txt)
- Markdown documents
- Any large text file

### Step 3: Condense It
```bash
# Using Claude Code (in conversation) - uses Haiku by default (cost-efficient):
/context-condense path/to/your/file.txt

# Or from command line:
python tools/condense_background_agent.py path/to/your/file.txt --type chat

# For complex files, use Opus (slower but higher quality):
/context-condense path/to/your/file.txt --model claude-opus-4-5-20251101
python tools/condense_background_agent.py path/to/file.txt --model claude-opus-4-5-20251101
```

### Step 4: Search Your Archive
```bash
python tools/archive_search.py "keyword you're looking for"
```

Done! The file is now indexed and searchable.

---

## Directory Structure

```
.kb/project/context-archive/       # Your private archive
├── sources/                        # Original files live here
│   ├── chats/                      # Chat logs (.txt files)
│   └── documents/                  # Technical docs (.md files)
├── condensed/                      # AI-generated summaries (markdown)
│   ├── chats/
│   └── documents/
├── index/                          # Fast lookup index
│   └── archive-index.yaml
├── metadata/                       # Stats and logs
│   └── processing-log.yaml
├── archive-config.yaml             # Settings
└── README.md                       # User guide
```

---

## Common Workflows

### Workflow 1: Save a Chat for Later Reference

```bash
# 1. Export this chat (or copy-paste into file)
# Save as: my-project/2026-01-18-authentication-discussion.txt

# 2. Condense it
/context-condense my-project/2026-01-18-authentication-discussion.txt --type chat

# 3. Later, search for it
python tools/archive_search.py "jwt"
# Returns: "2026-01-18-authentication-discussion.txt (0.88 confidence)"

# 4. Read the condensed version
cat .kb/project/context-archive/condensed/chats/2026-01-18-authentication-discussion.condensed.md
```

### Workflow 2: Archive External Documentation

```bash
# 1. Save documentation to a file
# Save as: docs-backup/api-specification.md

# 2. Condense it
/context-condense docs-backup/api-specification.md --type document

# 3. Search by topic
python tools/archive_search.py "" --tag api

# 4. Find related docs
python tools/archive_search.py "authentication" --tag api
```

### Workflow 3: Find Context on Specific Topic

```bash
# Search for anything about JWT
python tools/archive_search.py "jwt"

# Search only chats (not documents)
python tools/archive_search.py "jwt" --type chat

# Search with multiple tags
python tools/archive_search.py "" --tag security,authentication

# View archive statistics
python tools/archive_index.py
```

---

## What Gets Extracted

When you condense a file, Context Archive automatically extracts:

### 1. **Key Decisions**
```
- Decided to use JWT instead of sessions
- Chose PostgreSQL for primary database
```

### 2. **Technical Details**
```
- Token format: RS256 JWT
- Expiry: 24 hours
- Refresh token storage: httpOnly cookies
```

### 3. **Issues & Solutions**
```
- Issue: Slow token validation
  Solution: Cache scopes in Redis
- Issue: CORS blocked auth headers
  Solution: Add credentials: 'include'
```

### 4. **Action Items**
```
✅ Implement JWT provider
⏳ Add connection pooling (IN PROGRESS)
❓ Should we support OAuth? (UNCLEAR)
```

### 5. **Code References**
```
- src/auth/jwt.ts lines 45-120
- db/migrations/001-auth.sql
- tests/auth.test.ts
```

### 6. **Tags** (Auto-extracted)
`authentication` `jwt` `security` `database` `performance`

---

## Files in the System

### Core Tools

| File | Purpose |
|------|---------|
| `tools/context_condenser.py` | Main condensing engine (reads file → creates summary) |
| `tools/archive_index.py` | Index management (tracks what's been condensed) |
| `tools/archive_search.py` | Search engine (find by keyword or tag) |
| `tools/condense_background_agent.py` | CLI wrapper (what /context-condense uses) |
| `tools/init_context_archive.py` | Initialize archive structure |

### Configuration & Docs

| File | Purpose |
|------|---------|
| `.kb/project/context-archive/archive-config.yaml` | Settings (model, chunk size, etc.) |
| `.kb/project/context-archive/README.md` | User guide |
| `.kb/project/context-archive/index/archive-index.yaml` | Catalog of condensed files |
| `.kb/project/context-archive/metadata/processing-log.yaml` | What was processed and when |
| `docs/guides/context-archive/REFERENCE.md` | Complete reference documentation |
| `.claude/skills/context-condense.md` | Claude Code skill documentation |

### Data

| Location | Purpose |
|----------|---------|
| `.kb/project/context-archive/sources/chats/` | Where you put chat logs |
| `.kb/project/context-archive/sources/documents/` | Where you put documents |
| `.kb/project/context-archive/condensed/chats/` | Generated summaries of chats |
| `.kb/project/context-archive/condensed/documents/` | Generated summaries of documents |

---

## Command Reference

### Condense a File

**Default behavior:** Uses Haiku model (fast, cost-efficient)

```bash
# Using Claude Code
/context-condense path/to/file.txt
/context-condense path/to/file.txt --type document

# Using CLI directly
python tools/condense_background_agent.py path/to/file.txt
python tools/condense_background_agent.py path/to/file.txt --type chat
python tools/condense_background_agent.py path/to/file.txt --type document --archive /custom/path
```

**With specific model:**

```bash
# For higher quality on complex files (uses Opus - slower & more expensive):
/context-condense path/to/file.txt --model claude-opus-4-5-20251101
python tools/condense_background_agent.py path/to/file.txt --model claude-opus-4-5-20251101

# Explicitly use Haiku:
python tools/condense_background_agent.py path/to/file.txt --model claude-haiku-4-5-20251001
```

**Cost comparison (for 500KB file):**
- Haiku: ~$0.50-0.70
- Opus: ~$2-3

### Search Archive
```bash
# Full-text search
python tools/archive_search.py "authentication"

# By tag
python tools/archive_search.py "" --tag security
python tools/archive_search.py "" --tag security,authentication

# By type
python tools/archive_search.py "jwt" --type chat
python tools/archive_search.py "jwt" --type document

# View archive stats
python tools/archive_index.py
```

### View & Manage Index
```bash
# List all condensed files
python -c "from tools.archive_index import ArchiveIndex; from pathlib import Path; idx = ArchiveIndex(Path('.context-archive')); print(idx.get_index_summary())"

# Get all tags
python -c "from tools.archive_index import ArchiveIndex; from pathlib import Path; print(ArchiveIndex(Path('.context-archive')).get_all_tags())"

# View processing log
cat .context-archive/metadata/processing-log.yaml
```

---

## How It Works (Technical)

### Processing Pipeline

```
Input File (500KB)
        ↓
    [Chunker]      → Split into 12KB chunks (42 chunks)
        ↓
  [Condenser]      → Claude analyzes each chunk
        ↓
  [Synthesizer]    → Merges chunk summaries
        ↓
  [Tag Extractor]  → Finds topics automatically
        ↓
  [Index Updater]  → Adds to searchable catalog
        ↓
Output: 8KB markdown with metadata + indexed in archive
```

### Chunking Strategy
- Default chunk size: 12,000 characters (~2,400 words)
- Tries to break at sentence boundaries for context
- Configurable in `archive-config.yaml`

### Condensing Model
- Uses Claude Opus 4.5 (best semantic understanding)
- Each chunk condensed independently
- Then merged and deduplicated
- Typical costs: ~$0.50-0.70 per 500KB file

### Tag Extraction
- Automatically extracts backtick-quoted tags from summaries
- Example: `` `authentication` `` → tag "authentication"
- Enables fast categorization without manual tagging

---

## Integration with Knowledge Base

Context Archive complements the Knowledge Base:

| System | Storage | Scope | Use Case |
|--------|---------|-------|----------|
| **Shared KB** | `.kb/shared/` | Universal patterns | Industry standards, frameworks |
| **Project KB** | `.kb/project/` | Local/business | Company-specific patterns |
| **Context Archive** | `.kb/project/context-archive/` | Session/project | Chat logs, discussions, external docs |

**Integration Example:**
```
Found pattern in archive chat → Looks useful → Move to Project KB
Project KB entry says "see Shared KB" → Found universal pattern
Archive lets you find when/where pattern was discussed
```

---

## Performance & Costs

### Processing Time
- **Small file (50KB)**: 1-2 minutes
- **Medium file (500KB)**: 3-5 minutes
- **Large file (5MB)**: 15-30 minutes (needs chunking)

### Token Usage
- Typical: 15,000-20,000 tokens per 500KB
- Cost (Opus): ~$0.50-0.70
- Benefit: Weeks of searchability

### Storage
- Compressed ratio: ~20:1 (500KB → 8KB)
- Archive size for 100 condensed files: ~80MB total
- Index size: negligible (<1MB)

---

## Troubleshooting

### "File not found"
```bash
# Use absolute path:
/context-condense /absolute/path/to/file.txt

# Or check relative path (from project root):
ls path/to/file.txt
```

### "API key not found"
```bash
# Set environment variable:
export ANTHROPIC_API_KEY="sk-..."

# Then retry:
python tools/condense_background_agent.py file.txt
```

### "No tags extracted"
**Cause:** File lacks clear structure
**Solution:** Add section headers or topic markers

### "Low confidence score"
**Cause:** File too complex or ambiguous
**Solution:** Check preview with: `python tools/archive_search.py "query"`

### "Search returns nothing"
**Cause:** File not condensed yet
**Solution:** Check index: `cat .kb/project/context-archive/index/archive-index.yaml`

---

## Best Practices

### ✅ DO
- Condense long chats after solving complex problems
- Archive external documentation you reference often
- Use descriptive filenames: `2026-01-18-jwt-implementation.txt`
- Review archive monthly, remove outdated entries
- Search archive before asking in new conversation

### ❌ DON'T
- Condense small files (<50KB) - not worth it
- Edit condensed files directly (regenerate instead)
- Use for frequently-updated files (becomes stale)
- Store sensitive credentials (archive is local but indexed)

---

## Next Steps

1. **Test It:**
   ```bash
   # Create a sample file
   echo "Test content about authentication..." > test.txt

   # Condense it
   /context-condense test.txt

   # Search it
   python tools/archive_search.py "authentication"
   ```

2. **Set Up Regular Usage:**
   - Export chat at end of complex sessions
   - Save to `.kb/project/context-archive/sources/chats/`
   - Run `/context-condense` to archive

3. **Explore Advanced Features:**
   - View `docs/guides/context-archive/REFERENCE.md` for complete API
   - Check `.claude/skills/context-condense.md` for skill details
   - Run `python tools/archive_index.py` to see statistics

---

## Get Help

- **Command help:** `/context-condense --help`
- **Search help:** `python tools/archive_search.py --help`
- **Full docs:** `docs/guides/context-archive/REFERENCE.md`
- **Config:** `.kb/project/context-archive/archive-config.yaml`
- **Logs:** `.kb/project/context-archive/metadata/processing-log.yaml`

---

**Created:** 2026-01-18
**Status:** Ready to use
**Questions?** Check `docs/guides/context-archive/REFERENCE.md` for detailed reference
