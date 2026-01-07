# 500-Line Rule

Guide to the modular skill pattern for token efficiency and maintainability.

---

## Overview

**Rule:** SKILL.md files should be <500 lines

**Purpose:**
1. **Token efficiency** - Load metadata first, content on-demand
2. **Maintainability** - Smaller files easier to maintain
3. **Focus** - Forces prioritization of important content
4. **Organization** - Better structure with resources/

**Result:** 70%+ token savings at session start

---

## Problem Statement

### Before 500-Line Rule

```
python-development/SKILL.md: 1200 lines

├── Quick Start (50 lines)
├── Core Concepts (200 lines)
├── Async Patterns (400 lines) ⚠️
├── Testing (350 lines) ⚠️
└── Error Handling (200 lines) ⚠️
```

**Problems:**
- ❌ Always loaded at session start (~9,000 tokens)
- ❌ Hard to maintain (large file)
- ❌ Difficult to navigate
- ❌ Mixed content (essential + details)
- ❌ Can't scale to large projects

### After 500-Line Rule

```
python-development/SKILL.md: 325 lines

├── Quick Start (50 lines)
├── Core Concepts (100 lines)
├── Async Patterns (50 lines)
│   └── **📘 Detailed:** @resources/async-patterns.md
├── Testing (50 lines)
│   └── **📘 Complete Guide:** @resources/testing.md
└── Error Handling (75 lines)
    └── **📘 Reference:** @resources/error-handling.md

resources/ (1,150 lines, on-demand)
├── async-patterns.md (400 lines)
├── testing.md (350 lines)
└── error-handling.md (400 lines)
```

**Benefits:**
- ✅ Session start: ~50 tokens (metadata) + ~2,400 tokens (SKILL.md)
- ✅ On-demand: Resources loaded when needed (~3,000 tokens each)
- ✅ Easy to maintain (small, focused files)
- ✅ Clear navigation (links to details)
- ✅ Scales to large projects

**Token savings: 98% at session start** (50 vs 9,000 tokens)

---

## Implementation

### Step 1: Measure Current Size

```bash
# Count lines in SKILL.md
wc -l .claude/skills/my-skill/SKILL.md

# Or on Windows
find /c /v "" .claude\skills\my-skill\SKILL.md
```

**If >500 lines:** Apply 500-line rule

---

### Step 2: Identify Large Sections

**Look for sections >100 lines:**

```bash
# Find section sizes (manual review)
# Look for:
- ## Async Patterns (400 lines) ⚠️ Too large
- ## Testing (350 lines) ⚠️ Too large
- ## Error Handling (200 lines) ⚠️ Too large
```

**Criteria for moving to resources/:**
- Section >100 lines
- Detailed explanation not needed for 80% of use cases
- Reference documentation
- Edge cases and advanced topics
- Multiple examples

---

### Step 3: Create resources/ Directory

```bash
# Create resources directory
mkdir -p .claude/skills/my-skill/resources
```

---

### Step 4: Move Large Sections to Resources

**Example transformation:**

**Before (SKILL.md - 400 lines):**
```markdown
## Async Patterns

### Basic Async/Await

Async/await is the primary way to write asynchronous code in Python:

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return "data"

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())
```

**Key points:**
- Use `async def` to define coroutines
- Use `await` to call coroutines
- Use `asyncio.run()` to execute

### Coroutine Chaining

Chain multiple coroutines together:

```python
async def fetch_user(user_id):
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": "John"}

async def fetch_posts(user_id):
    await asyncio.sleep(0.5)
    return [{"title": "Post 1"}, {"title": "Post 2"}]

async def main():
    user = await fetch_user(1)
    posts = await fetch_posts(user["id"])
    print(f"User: {user}")
    print(f"Posts: {posts}")

asyncio.run(main())
```

### Concurrent Execution

Run multiple coroutines concurrently:

```python
async def main():
    user, posts = await asyncio.gather(
        fetch_user(1),
        fetch_posts(1)
    )
    print(f"User: {user}")
    print(f"Posts: {posts}")

asyncio.run(main())
```

### Error Handling

Handle errors in async code:

```python
async def fetch_data():
    await asyncio.sleep(1)
    raise ValueError("Data not found")

async def main():
    try:
        result = await fetch_data()
    except ValueError as e:
        print(f"Error: {e}")

asyncio.run(main())
```

### Timeouts

Add timeouts to async operations:

```python
async def fetch_data():
    await asyncio.sleep(2)

async def main():
    try:
        result = await asyncio.wait_for(
            fetch_data(),
            timeout=1.0
        )
    except asyncio.TimeoutError:
        print("Operation timed out")

asyncio.run(main())
```

### Async Context Managers

Use async context managers:

```python
class AsyncConnection:
    async def __aenter__(self):
        print("Connecting...")
        await asyncio.sleep(0.5)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection...")
        await asyncio.sleep(0.5)

async def main():
    async with AsyncConnection() as conn:
        print("Connected!")

asyncio.run(main())
```

### Async Iterators

Iterate asynchronously:

```python
class AsyncIterator:
    def __init__(self, items):
        self.items = items
        self.index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        await asyncio.sleep(0.5)
        if self.index >= len(self.items):
            raise StopAsyncIteration
        item = self.items[self.index]
        self.index += 1
        return item

async def main():
    async for item in AsyncIterator([1, 2, 3]):
        print(item)

asyncio.run(main())
```

[... 200+ more lines of detailed content ...]
```

**After (SKILL.md - 50 lines):**
```markdown
## Async Patterns

Async/await is the primary way to write asynchronous code in Python.

### Quick Example

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return "data"

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())
```

### Key Concepts

- **async def** - Define coroutines
- **await** - Call coroutines
- **asyncio.run()** - Execute coroutines
- **asyncio.gather()** - Run concurrently

### Common Patterns

**Sequential execution:**
```python
result = await fetch_data()
```

**Concurrent execution:**
```python
results = await asyncio.gather(
    fetch_data_1(),
    fetch_data_2()
)
```

**Error handling:**
```python
try:
    result = await fetch_data()
except Exception as e:
    print(f"Error: {e}")
```

**📘 Complete Async Guide:** `@resources/async-patterns.md`
```

**resources/async-patterns.md (400 lines) - NEW:**
```markdown
# Async Patterns

Complete guide to async/await patterns in Python.

[All the detailed content from before...]
```

---

### Step 5: Update YAML Frontmatter

**Add resource entries:**

```yaml
---
name: "python-development"
description: "Python development patterns and best practices"
version: "1.0"
tags: ["python", "development"]
resources:  # ← Add this section
  - "resources/async-patterns.md"
  - "resources/testing.md"
  - "resources/error-handling.md"
---
```

---

### Step 6: Test Links

**Verify all links work:**

1. Click each @ reference
2. Verify resource file loads
3. Check back links work
4. Test with Claude Code

---

## Content Strategy

### What Goes in SKILL.md (80/20 Rule)

**Include in SKILL.md:**
- Quick start (what users need most)
- Core concepts (overview, not deep dive)
- Common tasks (frequently used)
- Quick examples (minimal, clear)
- Links to detailed content

**Exclude from SKILL.md:**
- Detailed explanations (>100 lines)
- Edge cases and advanced topics
- Comprehensive reference
- Multiple examples for same concept
- Historical context

### What Goes in resources/

**Create resource files for:**
- Detailed explanations (200-400 lines)
- Edge cases and advanced topics
- Comprehensive reference (100-150 lines)
- Multiple examples
- Patterns and best practices
- Troubleshooting guides

---

## Examples from Production

### Example 1: research-enhance Skill

**Before:**
```
research-enhance/SKILL.md: 419 lines
- Enhancement workflow
- What Claude can do (detailed)
- Implementation rules
- Quality checklist
- Research sources (detailed)
- Enhancement examples (detailed)
```

**After:**
```
research-enhance/SKILL.md: 259 lines (-38%)
- Enhancement workflow (condensed)
- What Claude can do (examples)
- Implementation rules
- Quality checklist
- **📘 Research Sources:** @resources/research-sources.md
- **📘 Examples:** @resources/enhancement-examples.md

resources/ (752 lines - on-demand)
├── research-sources.md (339 lines)
└── enhancement-examples.md (413 lines)
```

**Token efficiency:**
- Before: 419 lines ≈ 3,140 tokens (always loaded)
- After: 50 tokens (metadata) + 1,940 tokens (SKILL.md) + 5,640 tokens (resources)
- **Session start savings: 98%** (50 vs 3,140 tokens)

---

### Example 2: python-async Skill

**Before:**
```
python-async/SKILL.md: 680 lines
- Quick start
- Core concepts
- Async patterns (300 lines) ⚠️
- Error handling (200 lines) ⚠️
- Testing (180 lines) ⚠️
```

**After:**
```
python-async/SKILL.md: 280 lines (-59%)
- Quick start
- Core concepts (condensed)
- Async patterns overview
- **📘 Complete Patterns:** @resources/async-patterns.md
- Error handling overview
- **📘 Complete Guide:** @resources/error-handling.md
- Testing overview
- **📘 Testing Guide:** @resources/testing.md

resources/ (1,100 lines - on-demand)
├── async-patterns.md (400 lines)
├── error-handling.md (350 lines)
└── testing.md (350 lines)
```

---

## Benefits

### 1. Token Efficiency

**Session start:**
- Before: 680 lines ≈ 5,100 tokens
- After: 50 tokens (metadata) + 2,100 tokens (SKILL.md)
- **Savings: 58%**

**On-demand:**
- Resources loaded only when needed
- ~3,000 tokens per resource
- User controls when to load

**Overall:**
- 80% of sessions: User doesn't need details
- 20% of sessions: User loads one resource
- **Average savings: 70%+**

---

### 2. Maintainability

**Smaller files:**
- Easier to navigate
- Faster to load
- Simpler to edit
- Clearer structure

**Better organization:**
- One topic per file
- Clear purpose
- Easy to find content
- Logical structure

---

### 3. User Experience

**Progressive disclosure:**
- Essentials first
- Details on-demand
- User controls depth
- Less overwhelming

**Better navigation:**
- Clear links
- Descriptive titles
- Logical flow
- Easy to jump to details

---

## Best Practices

### 1. Content Distribution

**SKILL.md (300-500 lines):**
- Quick start: 50 lines
- Core concepts: 100 lines
- Common tasks: 100 lines
- Examples: 100 lines
- Links: 50 lines

**resources/ (300-500 lines each):**
- In-depth explanation: 200-300 lines
- Examples: 100-150 lines
- Reference: 50-100 lines

---

### 2. Section Sizing

**Target sizes:**
- Quick start: 30-50 lines
- Concept overview: 50-80 lines
- Task guide: 40-60 lines
- Example: 20-40 lines

**Move to resources/ if:**
- Section >100 lines
- Detailed explanation needed
- Multiple examples for same concept
- Reference documentation
- Edge cases

---

### 3. Linking

**DO:**
- Link to detailed content
- Use descriptive link text
- Group related links
- Provide context

**DON'T:**
- Duplicate content
- Put details in SKILL.md
- Forget to update links
- Use vague link text

---

### 4. File Naming

**DO:**
- Use lowercase with hyphens
- Descriptive names
- Consistent naming
- Related content grouped

**Examples:**
- `async-patterns.md` ✅
- `error-handling.md` ✅
- `testing-guide.md` ✅

**DON'T:**
- Use uppercase: `Async-Patterns.md` ❌
- Use underscores: `async_patterns.md` ❌
- Vague names: `details.md` ❌
- Numbers: `topic1.md` ❌

---

## Quality Metrics

### Token Efficiency

**Excellent:**
- SKILL.md <400 lines
- Resources 300-500 lines
- Metadata complete
- Session start <500 tokens

**Good:**
- SKILL.md <500 lines
- Resources organized
- Metadata present
- Session start <1,000 tokens

**Needs Improvement:**
- SKILL.md >500 lines
- No resources/
- Missing metadata
- Session start >2,000 tokens

---

### Organization Quality

**Excellent:**
- Clear SKILL.md structure
- Resources for detailed content
- Links to all details
- YAML frontmatter complete

**Good:**
- SKILL.md manageable size
- Some resources/
- Most content linked
- YAML frontmatter present

**Needs Improvement:**
- SKILL.md >500 lines
- No resources/
- Content duplication
- No YAML frontmatter

---

## Troubleshooting

### Issue: SKILL.md Still Too Large

**Symptoms:** SKILL.md >500 lines after optimization

**Solutions:**
1. Identify remaining large sections
2. Move to resources/
3. Condense examples
4. Remove edge cases
5. Link to external docs

### Issue: Too Many Resource Files

**Symptoms:** 10+ resource files

**Solutions:**
1. Combine related resources
2. Group by topic
3. Prioritize essential content
4. Consider external docs

### Issue: Content Duplication

**Symptoms:** Same content in SKILL.md and resources/

**Solutions:**
1. Keep overview in SKILL.md
2. Move details to resources/
3. Add links only
4. Remove duplication

---

## Related Resources

**Internal:**
- `@resources/yaml-frontmatter.md` - YAML frontmatter format
- `@resources/testing-guide.md` - Testing skills
- `@resources/troubleshooting.md` - Troubleshooting skills

**Related Skills:**
- `@skills/claude-code-architecture/SKILL.md` - System overview
- `@claude-code-architecture/resources/progressive-disclosure.md` - Progressive disclosure

**Shared KB:**
- `universal/patterns/PROGRESSIVE-DISCLOSURE-001` - Progressive disclosure pattern

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Based on:** Production testing with shared-knowledge-base
