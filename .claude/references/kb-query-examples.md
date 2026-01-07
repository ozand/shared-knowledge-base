# KB Query Examples - Advanced Patterns

**Comprehensive examples for using /kb-query command effectively**

---

## Basic Query Patterns

### Simple Query

**Command:**
```
/kb-query docker volume permissions
```

**What it does:**
- Searches KB for "docker volume permissions"
- Returns most relevant entry
- Provides solution with code examples

**Expected output:**
```
✅ Found: DOCKER-001 - Docker Volume Permission Denied

Problem: Container cannot access mounted volume...
Solution: Add user to docker group...
```

---

### Query with Context

**Command:**
```
/kb-query "async error" --context "FastAPI, Python 3.11+"
```

**What it does:**
- Searches for "async error"
- Filters results for FastAPI context
- Prioritizes Python 3.11+ compatible solutions

**When to use:**
- Framework-specific issues
- Version-specific problems
- Context-dependent solutions

---

### Query with Code Snippet

**Command:**
```
/kb-query "TypeError" --code "print(user['name'])"
```

**What it does:**
- Analyzes provided code snippet
- Identifies potential TypeError causes
- Searches KB for similar patterns

**Common TypeError patterns:**
- `KeyError: 'name'` - Key doesn't exist
- `TypeError: 'NoneType' object is not subscriptable` - user is None
- `TypeError: string indices must be integers` - user is string, not dict

---

## Advanced Query Patterns

### Query by Scope

**Universal patterns only:**
```
/kb-query "memory leak" --scope universal
```

Returns cross-language memory management patterns.

**Language-specific:**
```
/kb-query "memory leak" --scope python
```

Returns Python-specific memory leak solutions.

**Framework-specific:**
```
/kb-query "authentication" --scope framework
```

Returns framework auth patterns (Django, FastAPI, etc.)

---

### Query by Severity

**Critical issues only:**
```
/kb-query "security" --severity critical
```

Returns only critical severity security entries.

**High severity issues:**
```
/kb-query "database" --severity high
```

Returns high-severity database issues.

---

### Query by Category

**Python async errors:**
```
/kb-query "await" --category python
```

Returns Python async-related entries.

**Docker errors:**
```
/kb-query "permission" --category docker
```

Returns Docker permission issues.

---

## Complex Query Scenarios

### Scenario 1: Debugging Async Issues

**Problem:** "My async function hangs indefinitely"

**Query:**
```
/kb-query "async hang" --context "FastAPI, asyncio, Python 3.11"
```

**Expected workflow:**
1. KB returns ASYNC-001: "Missing await on coroutine"
2. Suggests checking for missing `await` keywords
3. Provides code examples
4. Links to related patterns: event loop, coroutine handling

**Follow-up queries:**
```
/kb-query "event loop" --scope python
/kb-query "coroutine" --category python
```

---

### Scenario 2: Docker Permission Issues

**Problem:** "Permission denied when accessing mounted volume"

**Query:**
```
/kb-query "volume permission" --category docker
```

**Expected workflow:**
1. KB returns DOCKER-001: "Volume Permission Denied"
2. Solution: Fix user permissions, use correct user ID
3. Prevention: Always set USER in Dockerfile
4. Related: SELinux contexts, volume drivers

---

### Scenario 3: Database Connection Errors

**Problem:** "PostgreSQL connection pool exhausted"

**Query:**
```
/kb-query "pool exhausted" --context "PostgreSQL, asyncpg"
```

**Expected workflow:**
1. KB returns POSTGRES-001: "Connection Pool Exhausted"
2. Solution: Increase pool size, fix connection leaks
3. Prevention: Always close connections, use context managers
4. Related: Connection timeout, pool configuration

---

## Query Optimization Tips

### Tip 1: Use Specific Keywords

**❌ Too broad:**
```
/kb-query "error"
```
Returns too many results.

**✅ Specific:**
```
/kb-query "KeyError access dict"
```
Returns targeted solutions.

---

### Tip 2: Provide Context When Needed

**❌ Without context:**
```
/kb-query "import error"
```
May return irrelevant solutions.

**✅ With context:**
```
/kb-query "import error" --context "pytest, Python 3.11"
```
Returns pytest-specific import solutions.

---

### Tip 3: Use Code Snippets for Debugging

**❌ Vague description:**
```
/kb-query "code doesn't work"
```

**✅ With code snippet:**
```
/kb-query "syntax error" --code "def my_func(:"
```
Returns targeted syntax error solutions.

---

### Tip 4: Iterate and Refine

**First query:**
```
/kb-query "timeout"
```
Too many results.

**Refined query:**
```
/kb-query "connection timeout" --scope python
```
Better results.

**Final refinement:**
```
/kb-query "asyncpg timeout" --context "Python 3.11"
```
Perfect match.

---

## Common Query Patterns by Task

### Debugging Errors
```
/kb-query "<error message>" --code "<problematic code>"
```

### Finding Best Practices
```
/kb-query "<practice>" --scope universal
```

### Framework-Specific Issues
```
/kb-query "<issue>" --context "<framework>, <version>"
```

### Security Issues
```
/kb-query "<security concern>" --severity critical
```

### Performance Issues
```
/kb-query "<performance problem>" --category <language>
```

---

## Troubleshooting Queries

### Issue: No Results Found

**Possible causes:**
1. Query too specific
2. KB doesn't have entry yet
3. Different terminology used

**Solutions:**
```
# Try broader query
/kb-query "<general term>"

# Try different keywords
/kb-query "<synonym>"

# Check if entry exists
python tools/kb.py search "<keyword>"
```

---

### Issue: Too Many Results

**Solution: Add filters**
```
/kb-query "<term>" --scope <scope>
/kb-query "<term>" --severity <severity>
/kb-query "<term>" --category <category>
```

---

### Issue: Results Not Relevant

**Solution: Add context**
```
/kb-query "<term>" --context "<framework>, <version>"
/kb-query "<term>" --code "<example>"
```

---

## Query Examples by Language

### Python Queries
```
# Async errors
/kb-query "asyncio error" --category python

# Type hints
/kb-query "type annotation" --scope python

# Testing
/kb-query "pytest fixture" --context "pytest 7.0+"
```

### JavaScript Queries
```
# Async/await
/kb-query "promise rejection" --category javascript

# Node.js
/kb-query "event loop" --context "Node.js 20+"
```

### Docker Queries
```
# Permissions
/kb-query "permission denied" --category docker

# Networking
/kb-query "container network" --scope docker
```

### PostgreSQL Queries
```
# Performance
/kb-query "slow query" --category postgresql

# Connections
/kb-query "connection pool" --context "asyncpg"
```

---

**Version:** 1.0
**Last Updated:** 2026-01-07
**Related:**
- `@references/cli-reference.md` - Complete CLI reference
- `@commands/kb-query.md` - Command implementation
