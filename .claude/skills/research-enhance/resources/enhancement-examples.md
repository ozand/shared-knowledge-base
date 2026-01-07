# Enhancement Examples - Real-World Scenarios

**Comprehensive examples of KB entry enhancements through research**

---

## Example 1: Python Async Timeout Enhancement

### Before Enhancement

**Entry:** `python/errors/async-timeout.yaml`

**Content:**
```yaml
problem: "Async operation hangs indefinitely"
solution:
  code: |
    await asyncio.wait_for(coro(), timeout=5.0)
```

**Quality Score:** 68/100

**Issues:**
- ❌ No root cause explanation
- ❌ No prevention strategies
- ❌ No best practices
- ⚠️ Limited to basic timeout
- ❌ Version info outdated

---

### Research Process

**Research Questions:**
1. What's new in Python 3.11+ for async?
2. Common async timeout pitfalls?
3. Best practices for production?

**Sources Consulted:**
- Python asyncio documentation (official)
- PEP 563 (TaskGroup)
- Stack Overflow: "async timeout best practices" (top answer: 127 upvotes)
- Real Python blog: "Async IO in Python"

**Findings:**
- Python 3.11+: TaskGroup for better structured concurrency
- Common pitfall: Not handling TimeoutError properly
- Best practice: Use asyncio.timeout() context manager (3.11+)
- Performance: TaskGroup faster than gather() for multiple tasks

---

### After Enhancement

**Entry:** `python/errors/async-timeout.yaml`

**Enhanced Content:**
```yaml
problem: |
  Async operation hangs indefinitely when external service
  doesn't respond within expected time

root_cause: |
  No timeout set on awaitable operation. Network issues, slow
  services, or deadlocks can cause indefinite hanging.

solution:
  code: |
    # Python 3.11+: Use asyncio.timeout (preferred)
    async with asyncio.timeout(5.0):
        result = await slow_operation()

    # Python 3.7-3.10: Use wait_for
    result = await asyncio.wait_for(slow_operation(), timeout=5.0)

  explanation: |
    asyncio.timeout() (3.11+) is a context manager that automatically
    cancels the operation on timeout. wait_for() is the legacy approach.

prevention:
  - "Always set timeouts on external I/O operations"
  - "Use TaskGroup (3.11+) for multiple concurrent operations"
  - "Log timeout events for monitoring and alerting"
  - "Implement circuit breakers for repeated timeouts"

examples:
  - scenario: "Multiple API calls with timeout"
    code: |
      # Python 3.11+: TaskGroup with timeout
      async with asyncio.timeout(10.0):
          async with asyncio.TaskGroup() as tg:
              tg.create_task(fetch_user(user_id))
              tg.create_task(fetch_orders(user_id))
              tg.create_task(fetch_recommendations(user_id))

    explanation: "TaskGroup cancels all tasks on timeout or error"

best_practices:
  - "Prefer asyncio.timeout() over wait_for() for Python 3.11+"
  - "Use specific timeout values based on operation SLA"
  - "Always handle TimeoutError explicitly"
  - "Log timeout with context (operation, duration)"
  - "Consider retries with exponential backoff"

tested_versions:
  - library: "python"
    version: "3.11+"
  notes: "asyncio.timeout() requires Python 3.11+"

performance:
  consideration: "TaskGroup (3.11+) 20-30% faster than gather() for 5+ tasks"
```

**Quality Score:** 92/100 (+24 points)

**Improvements:**
- ✅ Root cause explained
- ✅ Modern Python 3.11+ examples
- ✅ Prevention strategies (4 items)
- ✅ Best practices (5 items)
- ✅ Performance considerations
- ✅ Tested versions specified
- ✅ Real-world examples

---

## Example 2: Docker Volume Permissions Enhancement

### Before Enhancement

**Entry:** `docker/errors/volume-permission.yaml`

**Content:**
```yaml
problem: "Permission denied accessing mounted volume"
solution:
  code: |
    chmod 777 /data
```

**Quality Score:** 45/100

**Critical Issues:**
- ❌ **SECURITY RISK:** chmod 777 is dangerous
- ❌ No explanation of root cause
- ❌ No best practices
- ❌ No alternative solutions

---

### Research Process

**Research Questions:**
1. Why do Docker permission issues occur?
2. What are security implications of chmod 777?
3. What's the production-ready solution?

**Sources Consulted:**
- Docker documentation (official)
- Docker Security Best Practices
- Stack Overflow: "docker volume permissions" (top answer: 234 upvotes)
- SELinux documentation (for RHEL/CentOS)

**Findings:**
- Root cause: Container runs as different user than host
- **Security risk:** chmod 777 exposes data to all users
- Best practice: Match UID/GID between host and container
- SELinux: Requires `:z` or `:Z` flags on volumes

---

### After Enhancement

**Enhanced Content:**
```yaml
problem: |
  Permission denied when container tries to write to mounted volume

root_cause: |
  Container runs as root (default) but host directory owned by
  different user. UID/GID mismatch causes permission denied.

solution:
  code: |
    # ✅ GOOD: Match user ID
    docker run -u $(id -u):$(id -g) -v $(pwd)/data:/data app

    # ✅ GOOD: Create user in Dockerfile matching host
    Dockerfile:
      RUN useradd -m -u 1000 appuser
      USER appuser

  explanation: |
    Container and host must use same UID/GID. Three approaches:
    1. Pass user ID with -u flag
    2. Create user in Dockerfile with known UID
    3. Use entrypoint script to chown dynamically

security_warning: |
  ❌ NEVER use chmod 777 - exposes data to all users on host
  ⚠️ Avoid running container as root - security risk

prevention:
  - "Run containers as non-root user (security best practice)"
  - "Match UID/GID between host and container"
  - "Use read-only volumes where possible"
  - "Implement proper SELinux contexts on RHEL/CentOS"

alternatives:
  - title: "Use named volumes (Docker-managed)"
    code: |
      docker run -v app-data:/data app
    reason: "Docker manages permissions automatically"

  - title: "Use tmpfs for temporary data"
    code: |
      docker run --tmpfs /tmp:rw,size=100m app
    reason: "No permission issues, faster I/O"

best_practices:
  - "ALWAYS run as non-root in production"
  - "Use specific UID/GID, not root"
  - "Document user setup in Dockerfile"
  - "Test with different host user IDs"
  - "Consider SELinux contexts for production"

selinux:
  # For RHEL/CentOS/Fedora
  code: |
    docker run -v $(pwd)/data:/data:z app
  explanation: ":z flag relabels volume for SELinux"

examples:
  - scenario: "Docker Compose setup"
    code: |
      services:
        app:
          user: "${UID:-1000}:${GID:-1000}"
          volumes:
            - ./data:/app/data:z
    explanation: "Env variables for user ID, SELinux flag"
```

**Quality Score:** 95/100 (+50 points)

**Critical Improvements:**
- ✅ **SECURITY FIX:** Removed dangerous chmod 777
- ✅ Root cause explained (UID/GID mismatch)
- ✅ Security warning included
- ✅ Three production-ready solutions
- ✅ SELinux context handling
- ✅ Docker Compose example
- ✅ Best practices (5 items)

---

## Example 3: PostgreSQL Query Optimization Enhancement

### Before Enhancement

**Entry:** `postgresql/errors/slow-query.yaml`

**Content:**
```yaml
problem: "Query is slow"
solution:
  code: |
    CREATE INDEX idx_column ON table(column);
```

**Quality Score:** 52/100

**Issues:**
- ⚠️ Generic solution (may not apply)
- ❌ No query analysis
- ❌ No EXPLAIN ANALYZE guidance
- ❌ No indexing strategy

---

### Research Process

**Research Questions:**
1. How to analyze slow queries in PostgreSQL?
2. What are common indexing pitfalls?
3. When to use different index types?

**Sources:**
- PostgreSQL documentation (official)
- PostgreSQL Performance Tips (official)
- DBA Stack Exchange (top answers)
- PostgreSQL conference talks

**Findings:**
- **Step 1:** Always run EXPLAIN ANALYZE first
- **Common mistake:** Indexing without analyzing query plan
- **Best practice:** Consider column order in composite indexes
- **Index types:** B-tree (default), BRIN (large tables), GIN (jsonb)

---

### After Enhancement

**Enhanced Content:**
```yaml
problem: |
  Query execution time exceeds acceptable threshold

root_cause: |
  Missing index, full table scan, inefficient join order,
  or lack of statistics. Use EXPLAIN ANALYZE to diagnose.

solution:
  code: |
    # Step 1: Analyze query plan
    EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 123;

    # Step 2: Create index if full table scan detected
    CREATE INDEX idx_orders_user_id ON orders(user_id);

    # Step 3: Re-analyze to verify improvement
    EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 123;

  explanation: |
    EXPLAIN ANALYZE shows actual execution time and row counts.
    Look for "Seq Scan" (full table scan) → Create index.
    Look for "Index Scan" → Index is being used ✅

diagnosis_workflow:
  - "Run EXPLAIN ANALYZE on slow query"
  - "Check for Seq Scan on large tables"
  - "Verify index is being used (Index Scan)"
  - "Check actual vs estimated rows (statistics issue)"

prevention:
  - "Run ANALYZE regularly after data changes"
  - "Create indexes on foreign keys and JOIN columns"
  - "Use appropriate index types (B-tree, BRIN, GIN, etc.)"
  - "Monitor query performance with pg_stat_statements"

index_types:
  - type: "B-tree (default)"
    use_case: "Equality and range queries"
    example: "WHERE user_id = 123"

  - type: "BRIN"
    use_case: "Very large tables with natural ordering"
    example: "WHERE created_at > NOW() - INTERVAL '1 day'"

  - type: "GIN"
    use_case: "jsonb, array columns"
    example: "WHERE data @> '{"key": "value"}'"

common_mistakes:
  - "Creating indexes without EXPLAIN ANALYZE first"
  - "Indexing low-cardinality columns (e.g., boolean)"
  - "Too many indexes (slow down INSERT/UPDATE)"
  - "Not updating statistics (ANALYZE)"

best_practices:
  - "Always EXPLAIN ANALYZE before optimizing"
  - "Index foreign key columns"
  - "Use partial indexes for filtered queries"
  - "Monitor index usage with pg_stat_user_indexes"
  - "Remove unused indexes (slow down writes)"

monitoring:
  query: |
    -- Find unused indexes
    SELECT schemaname, tablename, indexname, idx_scan
    FROM pg_stat_user_indexes
    WHERE idx_scan = 0
    AND indisunique = false;

  action: "DROP INDEX if not used (except unique constraints)"
```

**Quality Score:** 94/100 (+42 points)

**Key Improvements:**
- ✅ Systematic diagnosis workflow
- ✅ EXPLAIN ANALYZE guidance
- ✅ Different index types explained
- ✅ Common mistakes documented
- ✅ Monitoring query included
- ✅ Best practices (6 items)

---

## Enhancement Patterns Summary

### Common Improvements

| Area | Typical Improvement | Score Impact |
|------|-------------------|--------------|
| Add root cause | Explain why problem occurs | +5-10 |
| Add prevention | How to avoid issue | +8-15 |
| Add best practices | Community standards | +10-15 |
| Add examples | Real-world scenarios | +5-10 |
| Update versions | Current library versions | +3-8 |
| Add alternatives | Multiple solutions | +5-10 |
| Add security | Security implications | +10-20 |

### Research ROI

**Time spent:** 30-60 minutes per entry
**Typical score improvement:** +15-25 points
**Impact:** Entry becomes authoritative, production-ready

---

**Version:** 1.0
**Last Updated:** 2026-01-07
