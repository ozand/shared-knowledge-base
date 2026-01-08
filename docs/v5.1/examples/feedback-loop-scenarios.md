# Feedback Loop Examples

**Version:** 5.1.0
**Last Updated:** 2026-01-08

---

## Example 1: Docker Compose Healthcheck Failure

### Scenario
Agent tries to start services with `docker-compose up` but gets healthcheck errors.

### Stage 1: Detection
```bash
$ docker-compose up
ERROR: for db  Healthcheck failed: timeout
```

### Stage 2: Analysis
```
Context: Starting PostgreSQL container
Problem: Healthcheck timeout after 30 seconds
Root Cause: PostgreSQL needs more time to initialize on first start
Solution: Increase healthcheck interval and timeout
```

### Stage 3: YAML Entry
```yaml
version: "1.0"
category: "docker"
last_updated: "2026-01-08"

errors:
  - id: "DOCKER-001"
    title: "Docker Compose Healthcheck Timeout"
    severity: "medium"
    scope: "docker"
    problem: |
      Docker Compose healthcheck fails with timeout for PostgreSQL
      on first container start.
    solution:
      code: |
        version: '3.8'
        services:
          db:
            image: postgres:15
            healthcheck:
              test: ["CMD-SHELL", "pg_isready -U postgres"]
              interval: 10s
              timeout: 5s
              retries: 5
              start_period: 30s  # Critical: allow startup time
      explanation: |
        PostgreSQL needs time to initialize on first start. The
        start_period parameter gives the container 30 seconds before
        healthcheck failures count toward the retry limit.
```

### Stage 4: Routing
- Security: No secrets ✅
- Business Logic: No ✅
- Universal: Helps all Docker Compose + PostgreSQL users ✅
- **Decision: Shared KB**

### Stage 5: Submission
```bash
python .kb/shared/tools/kb_submit.py \
  --target shared \
  --file docker-healthcheck.yaml \
  --title "Fix: Docker Compose PostgreSQL healthcheck timeout" \
  --domain docker
```

---

## Example 2: Pydantic Validation Error (Project-Specific)

### Scenario
Agent fixing discount calculation bug in e-commerce application.

### Stage 1: Detection
```python
ValidationError: discount_amount must be <= price
```

### Stage 2: Analysis
```
Context: Applying discount to product
Problem: Validation error when discount > price
Root Cause: Business rule: discount cannot exceed item price
Solution: Add validation before applying discount
```

### Stage 3: YAML Entry
```yaml
version: "1.0"
category: "validation"
last_updated: "2026-01-08"

errors:
  - id: "SHOP-DISCOUNT-001"
    title: "Discount Validation Error"
    severity: "high"
    scope: "project"
    problem: |
      Pydantic validation error when discount_amount > price.
      Business rule violation.
    solution:
      code: |
        class DiscountApply(BaseModel):
            product_id: int
            discount_amount: Decimal

            @model_validator(mode='after')
            def validate_discount(self):
                if self.discount_amount > self.product.price:
                    raise ValueError(
                        f"Discount ({self.discount_amount}) cannot exceed "
                        f"price ({self.product.price})"
                    )
                return self
      explanation: |
        Business rule: discounts cannot be greater than item price.
        This validation prevents negative final prices.
```

### Stage 4: Routing
- Security: No secrets ✅
- Business Logic: YES - e-commerce discount rules ✅
- Universal: NO - specific to this business ✅
- **Decision: Project KB**

### Stage 5: Submission
```bash
python .kb/shared/tools/kb_submit.py \
  --target local \
  --file discount-validation.yaml
```

---

## Example 3: Stripe Webhook Signature Verification

### Scenario
Agent implementing Stripe payment integration.

### Stage 1: Detection
```python
InvalidSignatureError: Signature verification failed
```

### Stage 2: Analysis
```
Context: Processing Stripe webhook
Problem: Webhook signature verification failing
Root Cause: Stripe sends timestamp in header; need to include in verification
Solution: Use Stripe's verified signature library with timestamp tolerance
Attempts: 4 tries to get this right
```

### Stage 3: YAML Entry
```yaml
version: "1.0"
category: "integration"
last_updated: "2026-01-08"

errors:
  - id: "STRIPE-001"
    title: "Stripe Webhook Signature Verification"
    severity: "critical"
    scope: "python"
    framework: "fastapi"
    problem: |
      Stripe webhook signature verification fails with
      InvalidSignatureError.
    solution:
      code: |
        import stripe
        from fastapi import Request, HTTPException

        @app.post("/webhook/stripe")
        async def stripe_webhook(request: Request):
            payload = await request.body()
            sig_header = request.headers.get('stripe-signature')

            try:
                event = stripe.Webhook.construct_event(
                    payload,
                    sig_header,
                    stripe_webhook_secret,
                    tolerance=200  # Critical: allow timestamp drift
                )
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid payload")
            except stripe.error.SignatureVerificationError:
                raise HTTPException(status_code=400, detail="Invalid signature")

            # Process event
            return {"status": "success"}
      explanation: |
        Stripe webhook signatures include a timestamp. Without tolerance
        parameter, verification fails due to minor clock differences between
        Stripe's servers and yours. Tolerance of 200 seconds is recommended.
    attempts: 4
    related_docs:
      - "https://stripe.com/docs/webhooks/signatures"
```

### Stage 4: Routing
- Security: No actual secrets (uses env var for webhook secret) ✅
- Business Logic: No ✅
- Universal: YES - helps all Stripe integrations ✅
- **Decision: Shared KB**

### Stage 5: Submission
```bash
python .kb/shared/tools/kb_submit.py \
  --target shared \
  --file stripe-webhook.yaml \
  --title "Fix: Stripe webhook signature verification" \
  --domain python
```

---

## Example 4: Database Connection Pool Exhaustion

### Scenario
Application under load runs out of database connections.

### Stage 1: Detection
```
sqlalchemy.exc.TimeoutError: QueuePool limit exceeded
```

### Stage 2: Analysis
```
Context: Application under load testing
Problem: Database connection pool exhausted
Root Cause: Pool size too small for concurrent requests
Solution: Increase pool_size and max_overflow
```

### Stage 3: YAML Entry
```yaml
version: "1.0"
category: "database"
last_updated: "2026-01-08"

errors:
  - id: "SQLALCHEMY-001"
    title: "SQLAlchemy Connection Pool Exhaustion"
    severity: "high"
    scope: "python"
    framework: "sqlalchemy"
    problem: |
      SQLAlchemy raises QueuePool limit timeout under high load.
      Connections not being released or pool too small.
    solution:
      code: |
        from sqlalchemy import create_engine
        from sqlalchemy.pool import QueuePool

        engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=20,        # Increase from default 5
            max_overflow=30,     # Allow 30 additional connections
            pool_timeout=30,     # Wait 30s for connection
            pool_recycle=3600,   # Recycle connections after 1 hour
            pool_pre_ping=True,  # Test connections before using
        )
      explanation: |
        Default pool_size of 5 is too small for production. Increase
        pool_size based on expected concurrent requests. max_overflow
        allows temporary spikes. pool_recycle prevents stale connections.
        pool_pre_ping tests connections before use to avoid errors.
```

### Stage 4: Routing
- Security: No secrets (DATABASE_URL from env) ✅
- Business Logic: No ✅
- Universal: YES - common SQLAlchemy issue ✅
- **Decision: Shared KB**

### Stage 5: Submission
```bash
python .kb/shared/tools/kb_submit.py \
  --target shared \
  --file sqlalchemy-pool.yaml \
  --title "Fix: SQLAlchemy connection pool exhaustion" \
  --domain python
```

---

## Example 5: Environment-Specific Debug Flag

### Scenario
Agent discovers that debug mode is accidentally enabled in production.

### Stage 1: Detection
```
WARNING: Debug mode is enabled in production!
```

### Stage 2: Analysis
```
Context: Reviewing production logs
Problem: DEBUG=True in production environment
Root Cause: Environment variable not set, defaults to True
Solution: Explicit DEBUG=False in production settings
```

### Stage 3: YAML Entry
```yaml
version: "1.0"
category: "configuration"
last_updated: "2026-01-08"

errors:
  - id: "PROD-DEBUG-001"
    title: "Debug Mode Enabled in Production"
    severity: "critical"
    scope: "project"
    problem: |
      Django/FastAPI running with DEBUG=True in production environment.
      Exposes detailed error pages and configuration.
    solution:
      code: |
        # .env.production
        DEBUG=False
        ALLOWED_HOSTS=example.com,www.example.com
        SECURE_SSL_REDIRECT=True
        SESSION_COOKIE_SECURE=True
      explanation: |
        Project uses environment-specific .env files. Always explicitly
        set DEBUG=False in production environments. Never default to True.
```

### Stage 4: Routing
- Security: No actual secrets ✅
- Business Logic: NO ✅
- Universal: NO - project-specific configuration pattern ✅
- **Decision: Project KB**

### Stage 5: Submission
```bash
python .kb/shared/tools/kb_submit.py \
  --target local \
  --file debug-mode.yaml
```

---

## Routing Decision Matrix

### Quick Reference

| Category | Has Secrets? | Business Logic? | Universal Pattern? | Destination |
|----------|--------------|-----------------|-------------------|-------------|
| **Docker healthcheck** | No | No | Yes | Shared KB |
| **Discount validation** | No | Yes (e-commerce) | No | Project KB |
| **Stripe webhooks** | No | No | Yes | Shared KB |
| **SQLAlchemy pool** | No | No | Yes | Shared KB |
| **Debug mode config** | No | No | No (project-specific) | Project KB |

### Decision Tree

```
Start: Does YAML contain secrets?
├─ YES → Project KB (NEVER share)
└─ NO → Continue

Is it business logic (discounts, workflows, rules)?
├─ YES → Project KB
└─ NO → Continue

Would another project benefit from this?
├─ YES → Shared KB
└─ NO → Project KB
```

---

## Tips for Writing Good Entries

### DO:
- ✅ Be specific about error messages
- ✅ Include complete, runnable code
- ✅ Explain the "why", not just the "how"
- ✅ Add related documentation links
- ✅ Specify framework/library versions
- ✅ Note number of attempts (shows complexity)

### DON'T:
- ❌ Include actual passwords/tokens (use placeholders)
- ❌ Be vague about the problem
- ❌ Skip the explanation
- ❌ Submit incomplete code snippets
- ❌ Forget to categorize correctly

---

## Summary

These examples show the Feedback Loop in action:

1. ✅ **Detect** errors during execution
2. ✅ **Analyze** root causes systematically
3. ✅ **Extract** structured YAML knowledge
4. ✅ **Route** appropriately (Project vs Shared)
5. ✅ **Submit** using kb_submit.py

**Key Pattern:** Universal patterns → Shared KB, project-specific issues → Project KB

**Result:** Agent never makes the same mistake twice, knowledge compounds over time.
