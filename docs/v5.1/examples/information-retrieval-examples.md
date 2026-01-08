# Information Retrieval Examples

**Version:** 5.1.0
**Last Updated:** 2026-01-08

---

## Example 1: Redis Connection Setup (Cascading Search)

### Scenario
Agent needs to configure Redis connection for a FastAPI application.

### Step 1: Initial Search

```bash
python .kb/shared/tools/v5.1/kb_search.py --scope all "redis connection"
```

### Step 2: Results (Prioritized)

```text
🔍 Search: 'redis connection' | Found: 2

--- PROJECT KB (1 entries) [HIGHEST PRIORITY - Overrides Shared KB] ---

⭐ .kb/project/integrations/redis-config.yaml
   Title: Production Redis Configuration
   Severity: high | Category: integration | Scope: project
   Summary: We use Redis Sentinel for high availability.
   Hosts: redis-sentinel-1, redis-sentinel-2, redis-sentinel-3
   Port: 26379
   Master name: myapp-master

--- SHARED KB (1 entries) ---

📚 .kb/shared/domains/python/redis-pool.yaml
   Title: Redis Connection Pool Best Practices
   Severity: medium | Category: database | Scope: python
   Summary: How to properly create connection pool in Python.
   Use redis.ConnectionPool with max_connections=50.

⚠️  NOTE: Project KB entries take precedence over Shared KB
   Always follow project-specific patterns over general standards
```

### Step 3: Agent Synthesis

```python
# Agent combines both sources:

from redis import Sentinel
import os

# From Shared KB: Proper pooling pattern
pool = redis.ConnectionPool(
    max_connections=50,  # Shared KB best practice
    socket_timeout=5,
    socket_connect_timeout=5,
)

# From Project KB: Sentinel configuration (overrides direct connection)
sentinel = Sentinel(
    [
        ('redis-sentinel-1', 26379),  # Project KB hosts
        ('redis-sentinel-2', 26379),
        ('redis-sentinel-3', 26379),
    ],
    master_name='myapp-master',  # Project KB master name
    connection_pool=pool,  # Shared KB pattern
)

master = sentinel.master_for('myapp-master')
```

**Result:** Best practices from Shared KB + project-specific config from Project KB

---

## Example 2: CORS Configuration (Conflict Resolution)

### Scenario
Agent needs to configure CORS for FastAPI.

### Step 1: Search

```bash
python .kb/shared/tools/v5.1/kb_search.py --scope all "fastapi cors"
```

### Step 2: Results

```text
🔍 Search: 'fastapi cors' | Found: 2

--- PROJECT KB (1 entries) [HIGHEST PRIORITY - Overrides Shared KB] ---

⭐ .kb/project/knowledge/decisions/cors-policy.yaml
   Title: Strict CORS for Production
   Severity: critical | Category: security | Scope: project
   Summary: Allow only specific origins from ENV.
   Do NOT use wildcard ["*"] in production.

--- SHARED KB (1 entries) ---

📚 .kb/shared/domains/python/fastapi-cors.yaml
   Title: FastAPI CORS Middleware Setup
   Severity: medium | Category: web-framework | Scope: python
   Summary: How to properly configure CORSMiddleware in FastAPI.
   Use allow_origins=["*"] for development.

⚠️  NOTE: Project KB entries take precedence over Shared KB
```

### Step 3: Conflict Resolution

**Agent's thought process:**

```
Shared KB suggests: allow_origins=["*"] (wildcard)
Project KB requires: Specific domains from ENV (no wildcard)

Decision: Follow Project KB (security policy)
Reason: Project KB override takes precedence
```

### Step 4: Implementation

```python
from fastapi.middleware.cors import CORSMiddleware
import os

# Agent follows PROJECT KB (overrides Shared KB)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(","),  # Project KB: specific domains
    allow_credentials=True,  # Shared KB pattern
    allow_methods=["*"],  # Shared KB pattern
    allow_headers=["*"],  # Shared KB pattern
)
```

**Result:** Project security policy (Project KB) + proper middleware setup (Shared KB)

---

## Example 3: Database Migration (Project-Specific)

### Scenario
Agent needs to create database migration.

### Step 1: Search

```bash
python .kb/shared/tools/v5.1/kb_search.py --scope all "alembic migration"
```

### Step 2: Results

```text
🔍 Search: 'alembic migration' | Found: 1

--- PROJECT KB (1 entries) [HIGHEST PRIORITY - Overrides Shared KB] ---

⭐ .kb/project/knowledge/lessons/alembic-lesson.yaml
   Title: Alembic with Multi-Database Setup
   Severity: high | Category: database | Scope: project
   Summary:
   We use separate databases for each tenant.
   Migration must run for each database dynamically.
   Don't use default alembic.ini pattern.

   Code: Use get_engine() to get tenant DB list
```

### Step 3: Only Project KB Found

**Agent's thought process:**

```
No results in Shared KB
Found only in Project KB
This is project-specific pattern

Decision: Follow Project KB instructions
```

---

## Example 4: Docker Healthcheck (Shared KB)

### Scenario
Agent needs to add healthcheck to Docker Compose.

### Step 1: Search

```bash
python .kb/shared/tools/v5.1/kb_search.py --scope all "docker compose healthcheck"
```

### Step 2: Results

```text
🔍 Search: 'docker compose healthcheck' | Found: 1

--- SHARED KB (1 entries) ---

📚 .kb/shared/domains/docker/healthcheck-timeout.yaml
   Title: Docker Compose Healthcheck Timeout
   Severity: medium | Category: deployment | Scope: docker
   Summary:
   Healthcheck fails with timeout for PostgreSQL on first start.
   Add start_period to allow initialization time.
```

### Step 3: Only Shared KB Found

**Agent's thought process:**

```
No project-specific guidance
Found standard pattern in Shared KB
This is general best practice

Decision: Follow Shared KB pattern
```

### Step 4: Implementation

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s  # From Shared KB
```

**Result:** Follows organizational standard from Shared KB

---

## Example 5: Pydantic Validation (Both Sources)

### Scenario
Agent fixing Pydantic validation error.

### Step 1: Search

```bash
python .kb/shared/tools/v5.1/kb_search.py --scope all "pydantic validation"
```

### Step 2: Results

```text
🔍 Search: 'pydantic validation' | Found: 2

--- PROJECT KB (1 entries) [HIGHEST PRIORITY] ---

⭐ .kb/project/knowledge/lessons/pydantic-discount.yaml
   Title: Discount Validation Rule
   Severity: high | Category: validation | Scope: project
   Summary: Business rule: discount cannot exceed item price.
   Custom validator needed.

--- SHARED KB (1 entries) ---

📚 .kb/shared/domains/python/pydantic-v2.yaml
   Title: Pydantic v2 Model Validation
   Severity: medium | Category: validation | Scope: python
   Summary: How to use @model_validator decorator in Pydantic v2.
   Use mode='after' for cross-field validation.

⚠️  NOTE: Project KB entries take precedence
```

### Step 3: Agent Synthesis

```python
from pydantic import BaseModel, model_validator

class DiscountApply(BaseModel):
    product_id: int
    discount_amount: Decimal
    price: Decimal

    @model_validator(mode='after')  # From Shared KB: Pydantic v2 pattern
    def validate_discount(self):
        # From Project KB: Business rule
        if self.discount_amount > self.price:
            raise ValueError(
                f"Discount ({self.discount_amount}) cannot exceed "
                f"price ({self.price})"
            )
        return self
```

**Result:** Shared KB technical pattern + Project KB business rule

---

## Query Formulation Examples

### Bad Queries → Good Queries

| Bad Query | Good Query | Why Better |
|-----------|------------|-------------|
| "error" | "fastapi websocket connection error" | Framework + specific error |
| "docker" | "docker compose healthcheck timeout" | Specific problem |
| "database" | "sqlalchemy connection pool exhausted" | Technology + issue |
| "test" | "pytest fixture not found" | Tool + error |
| "help" | "redis sentinel configuration python" | Technology + config |

### Search Strategy

**1. Start Specific:**
```bash
python kb_search.py "fastapi 0.104 websocket"
```

**2. If No Results, Broaden:**
```bash
python kb_search.py "fastapi websocket"
```

**3. If Still No Results, Try Different Terms:**
```bash
python kb_search.py "websocket connection"
```

**4. Finally, Consider Web Search:**
```bash
# (Then submit solution to Feedback Loop!)
```

---

## Performance Examples

### Speed Comparison

```bash
# Local search (milliseconds)
$ time python kb_search.py "docker compose"
🔍 Search: 'docker compose' | Found: 5
real    0m0.045s  # 45ms

# Web search (seconds)
$ time google "docker compose healthcheck"
real    0m2.345s  # 2.3 seconds
```

**Result:** Local search is ~50x faster!

### Scale Testing

```bash
# 1000 YAML files in Shared KB
$ time python kb_search.py "python"
🔍 Search: 'python' | Found: 342
real    0m0.120s  # Still only 120ms
```

**Result:** Scales efficiently!

---

## Conflict Resolution Examples

### Example 1: PostgreSQL Version

```
Shared KB: "Use PostgreSQL 16"
Project KB: "This project uses PostgreSQL 12 (legacy)"
→ Agent uses PostgreSQL 12 (Project KB wins)
```

### Example 2: API Authentication

```
Shared KB: "Use JWT tokens"
Project KB: "We use custom API keys with rotation"
→ Agent uses custom API keys (Project KB wins)
```

### Example 3: Logging Format

```
Shared KB: "Use JSON structured logging"
Project KB: No specific guidance
→ Agent uses JSON logging (Shared KB applies)
```

---

## Complete Workflow Example

### Task: Setup PostgreSQL connection

**1. Search First:**
```bash
python kb_search.py "postgresql connection pool"
```

**2. Review Results:**
- Project KB: Connection details (host, port, database name)
- Shared KB: Pool configuration best practices

**3. Combine Sources:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
import os

# From Shared KB: Pool best practices
engine = create_engine(
    "postgresql://user:pass@host/db",  # From Project KB
    poolclass=QueuePool,  # From Shared KB
    pool_size=20,  # From Shared KB
    max_overflow=30,  # From Shared KB
)
```

**4. Apply Context Injection:**
```python
# Actually use environment variables
DATABASE_URL = os.getenv("DATABASE_URL")  # Project KB pattern
engine = create_engine(DATABASE_URL, poolclass=QueuePool, ...)
```

---

## Search Frequency Scenarios

### When to Search (MANDATORY)

✅ **Before implementing feature:**
```bash
python kb_search.py "fastapi dependency injection"
```

✅ **When encountering error:**
```bash
python kb_search.py "module not found pytest"
```

✅ **Before choosing library:**
```bash
python kb_search.py "python async web framework"
```

✅ **When configuring infrastructure:**
```bash
python kb_search.py "nginx reverse proxy configuration"
```

### When NOT to Search

❌ During exploratory coding (optional)
❌ When learning for curiosity (optional)
❌ When prototyping rapidly (can search later)

---

## Tips for Effective Search

### 1. Use Framework Names

```bash
# Good
python kb_search.py "django user model"

# Better (with version)
python kb_search.py "django 5.0 user model"
```

### 2. Include Error Types

```bash
# Good
python kb_search.py "timeout error"

# Better (specific)
python kb_search.py "connection timeout sqlalchemy"
```

### 3. Add Context

```bash
# Good
python kb_search.py "docker"

# Better (with use case)
python kb_search.py "docker multi-stage build python"
```

### 4. Use --preview Flag

```bash
# See content before opening file
python kb_search.py "fastapi" --preview
```

---

## Summary

**Cascading Search** ensures:

1. ✅ **Project KB first** - Follow project-specific patterns
2. ✅ **Shared KB second** - Use organizational standards
3. ✅ **Web search last** - Find novelty when needed
4. ✅ **Priority resolution** - Project overrides Shared
5. ✅ **Context injection** - Combine best from multiple sources

**Key Benefits:**
- ⚡ **Fast:** Milliseconds, not seconds
- 🎯 **Relevant:** Prioritized by project context
- 🔒 **Private:** No external queries
- 📈 **Scalable:** Works with thousands of entries

**Result:** Agents that find, don't fabricate!
