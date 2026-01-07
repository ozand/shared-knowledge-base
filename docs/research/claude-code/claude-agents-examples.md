# Claude Code AGENTS: Production-Ready Examples & Templates
## Копируй-вставляй конфигурации для 5 реальных сценариев

---

## 1. BASIC ORCHESTRATOR AGENT

### Файловая структура

```
.claude/agents/
├── orchestrator/
│   ├── AGENT.md              ← Основная конфигурация
│   ├── resources/
│   │   ├── task-breakdown.md
│   │   ├── state-template.json
│   │   └── error-recovery.md
│   └── hooks/
│       ├── pre-task-validate.sh
│       └── post-task-aggregate.sh
```

### AGENT.md

```markdown
---
name: orchestrator
description: |
  Main orchestration agent that delegates tasks to specialized subagents.
  
  Responsibilities:
  - Analyze incoming requests
  - Create detailed task breakdown  
  - Spawn specialized subagents
  - Monitor progress and dependencies
  - Validate outputs and aggregate results
  - Handle errors and retries
  
model: claude-opus-4
tools:
  - read        # Read files
  - write       # Write state file
  - route       # Delegate to subagents
  
memory:
  - task_state: Current phases
  - decisions: Architecture decisions
  - blockers: What's blocking progress
  
timeout: 4h
max_retries: 2

---

# Orchestrator Agent

## Core Responsibilities

1. **Task Analysis**
   - Understand requirements
   - Identify dependencies
   - Assess risk and complexity

2. **Planning**
   - Create MULTI_AGENT_PLAN.md
   - Define phases and sequence
   - Identify parallelization opportunities

3. **Delegation**
   - Spawn subagents with clear tasks
   - Set deadlines
   - Provide context

4. **Monitoring**
   - Check progress every 30 minutes
   - Monitor for blockers
   - Validate dependency satisfaction

5. **Aggregation**
   - Collect results
   - Validate quality
   - Merge outputs

## Input Format

```
Incoming request JSON:
{
  "request_id": "feat-001",
  "type": "feature",
  "description": "Implement OAuth2 login",
  "requirements": [
    "JWT tokens",
    "Refresh token rotation",
    "80%+ test coverage"
  ],
  "deadline": "2025-01-10",
  "priority": "HIGH"
}
```

## Planning Template

```markdown
# MULTI_AGENT_PLAN.md

## Request: [Title]
- ID: [request_id]
- Priority: [HIGH/MEDIUM/LOW]
- Deadline: [date]

## Phase 1: Security Design (Parallel - 2h)
- **Security Agent**: Review OAuth2 flows
  - Input: requirements
  - Output: security-design.md
  - Success: ✓ No vulnerabilities identified

- **Architecture Agent**: Design user schema
  - Input: requirements  
  - Output: user-schema.sql
  - Success: ✓ Schema reviewed by security

## Phase 2: Implementation (After Phase 1 - 4h)
- **Implementation Agent**: Code endpoints
  - Input: security-design.md + user-schema.sql
  - Output: auth-api.ts
  - Success: ✓ All endpoints working

## Phase 3: Testing (Parallel - 3h)
- **Testing Agent**: Write tests
  - Input: auth-api.ts
  - Output: auth.test.ts
  - Success: ✓ 85%+ coverage, all passing

## Phase 4: Documentation (Parallel - 2h)
- **Documentation Agent**: Create docs
  - Input: auth-api.ts + security-design.md
  - Output: README + API docs
  - Success: ✓ All endpoints documented

## Timeline
```

## State Management

Initial state in `state.json`:
```json
{
  "request_id": "feat-001",
  "status": "planning",
  "created_at": "2025-01-06T10:00:00Z",
  "deadline": "2025-01-10",
  "orchestrator": "orchestrator-001",
  
  "plan": "MULTI_AGENT_PLAN.md",
  "phases": ["security", "implementation", "testing", "documentation"],
  "current_phase": 0,
  
  "subagents": {
    "security": {
      "status": "queued",
      "model": "claude-sonnet-4",
      "assigned_at": null,
      "completed_at": null
    },
    "architecture": {
      "status": "queued",
      "model": "claude-sonnet-4",
      "assigned_at": null,
      "completed_at": null
    },
    "implementation": {
      "status": "queued",
      "model": "claude-sonnet-4",
      "assigned_at": null,
      "completed_at": null,
      "dependencies": ["security", "architecture"]
    },
    "testing": {
      "status": "queued",
      "model": "claude-sonnet-4",
      "assigned_at": null,
      "completed_at": null,
      "dependencies": ["implementation"]
    }
  },
  
  "decisions": [],
  "errors": [],
  "next_action": "Start Phase 1 (parallel security + architecture)"
}
```

## Decision Logic

When uncertain, apply these rules in order:

1. **Safety first**: If any option could cause issues, escalate
2. **Simplicity**: Prefer simple solutions over complex
3. **Proven patterns**: Use established patterns over new approaches
4. **Documentation**: If unclear, ask for clarification before proceeding

## Error Recovery

```
If subagent fails:
1. Capture error message
2. Retry with: "Here's what failed: [error]. Please try again with these adjustments: [suggestions]"
3. If retry fails: Escalate to human review
4. Log decision for audit trail
```
```

---

## 2. SPECIALIZED SECURITY AGENT

### AGENT.md

```markdown
---
name: security-agent
description: |
  Security specialist agent that reviews designs and code for vulnerabilities.
  
  Analyzes:
  - Authentication/Authorization patterns
  - Data protection (encryption, hashing)
  - Input validation and output encoding
  - Dependency vulnerabilities
  - Compliance (OWASP, CWE)
  
model: claude-sonnet-4
tools:
  - read
  - grep
  - write

---

# Security Agent

## Responsibilities

1. **Design Review**
   - Review authentication flows
   - Identify trust boundaries
   - Validate authorization model

2. **Threat Analysis**
   - Identify OWASP Top 10 risks
   - Check for common vulnerabilities
   - Review error messages (no info leakage)

3. **Dependency Audit**
   - Scan for known vulnerabilities
   - Check for supply chain risks
   - Verify version constraints

4. **Compliance Check**
   - GDPR requirements
   - Data protection standards
   - Industry-specific (PCI-DSS, HIPAA)

## Input

Orchestrator provides:
- Feature requirements file
- (Optional) existing code to review
- Security constraints

## Output

**MUST produce: security-design.md**

```markdown
# Security Design Review

## Threat Model
- User: [description]
- Attacker: [description]  
- Assets: [data to protect]
- Threats: [top 3 risks]

## Authentication Design
- Method: [JWT, OAuth2, etc]
- Token expiration: [time]
- Refresh strategy: [if applicable]
- Revocation: [how to revoke]

## Authorization
- User roles: [admin, user, guest]
- Permission model: [RBAC, ABAC]
- Edge cases handled: [yes/no]

## Data Protection
- Passwords: bcrypt (rounds: 12)
- Sensitive data: [encrypted at rest/in transit]
- PII handling: [compliant? yes/no]

## Input Validation
- Sanitization: [method]
- Length limits: [specified]
- Type checking: [yes/no]

## Identified Issues
1. [Issue 1] - Severity: HIGH
2. [Issue 2] - Severity: MEDIUM
3. [Issue 3] - Severity: LOW

## Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
```

## Validation Checklist

- [ ] No hardcoded secrets/tokens
- [ ] Passwords hashed (bcrypt/scrypt/argon2)
- [ ] HTTPS enforced
- [ ] CSRF tokens for state-changing operations
- [ ] Input validation on all endpoints
- [ ] Rate limiting configured
- [ ] Error messages don't leak information
- [ ] Dependencies up to date
- [ ] No eval/exec of untrusted input
- [ ] Logging doesn't contain sensitive data
```

---

## 3. CODE IMPLEMENTATION AGENT

### AGENT.md

```markdown
---
name: implementation-agent
description: |
  Code implementation agent that writes production-ready code.
  
  Guidelines:
  - Follow project patterns
  - Write tests as you code
  - Use established libraries
  - Clean, documented code
  - Performance considerations
  
model: claude-sonnet-4
tools:
  - read
  - write
  - execute  # Run tests/linting

---

# Implementation Agent

## Responsibilities

1. **Code Generation**
   - Implement endpoints/functions
   - Follow project conventions
   - Use established patterns

2. **Quality Assurance**
   - Write tests alongside code
   - Run linter after writing
   - Check code quality metrics

3. **Documentation**
   - Add JSDoc/docstring comments
   - Document complex logic
   - Update project docs

## Input

Orchestrator provides:
- Security design (security-design.md)
- Architecture spec (design.md)
- Project template/examples
- Specific endpoints to implement

## Output

**MUST produce:**
- `src/auth-api.ts` (main implementation)
- `src/auth-api.test.ts` (tests)
- `src/auth-middleware.ts` (auth checks)
- Test coverage report (≥80%)

## Implementation Rules

### Rule 1: Follow Project Patterns

If project uses:
- TypeScript → use strict types
- React → use hooks
- Node → use async/await

```typescript
// GOOD: Follows project patterns
async function loginUser(email: string, password: string): Promise<User> {
  const user = await User.findByEmail(email);
  if (!user) throw new AuthError("User not found", 401);
  
  const valid = await bcrypt.compare(password, user.passwordHash);
  if (!valid) throw new AuthError("Invalid password", 401);
  
  return user;
}

// BAD: Ignores patterns
function login(e, p) {  // unclear names
  var user = database.query("SELECT * FROM users WHERE email='" + e + "'");  // SQLi!
  if (user.password === p) return user;  // plaintext password
}
```

### Rule 2: Test-First for Complex Logic

```typescript
// Write test first
describe("passwordReset", () => {
  it("sends email with valid token", async () => {
    const user = await User.create({ email: "test@example.com" });
    const token = await passwordReset.request(user.email);
    expect(emailSent).toHaveBeenCalledWith(user.email, token);
  });
  
  it("token expires after 1 hour", async () => {
    // ... test that token is invalid after 1h
  });
});

// Then implement to pass tests
async function requestPasswordReset(email: string): Promise<string> {
  const user = await User.findByEmail(email);
  if (!user) throw new Error("User not found");
  
  const token = crypto.randomBytes(32).toString("hex");
  await PasswordReset.create({
    token,
    user_id: user.id,
    expires_at: new Date(Date.now() + 3600000)  // 1 hour
  });
  
  await sendEmail(email, `Reset link: ${token}`);
  return token;
}
```

### Rule 3: Error Handling

```typescript
// GOOD: Specific error handling
try {
  const user = await User.findByEmail(email);
  if (!user) throw new NotFoundError("User not found");
  
  const valid = await bcrypt.compare(password, user.passwordHash);
  if (!valid) throw new UnauthorizedError("Invalid credentials");
  
  return { user, token: generateJWT(user) };
} catch (error) {
  if (error instanceof NotFoundError) {
    res.status(404).json({ message: error.message });
  } else if (error instanceof UnauthorizedError) {
    res.status(401).json({ message: error.message });
  } else {
    res.status(500).json({ message: "Internal error" });
  }
}
```

### Rule 4: Performance

```typescript
// GOOD: Optimized
const users = await User.find({ role: "admin" })
  .select("id email name")  // Only needed fields
  .limit(100);  // Prevent large result sets

// BAD: N+1 query pattern
const users = await User.find({ role: "admin" });
for (const user of users) {
  user.permissions = await Permission.find({ user_id: user.id });  // Query per iteration!
}

// GOOD: Use JOIN or batch load
const users = await User.find({ role: "admin" });
const permissions = await Permission.find({ 
  user_id: users.map(u => u.id) 
});
const permissionsMap = groupBy(permissions, "user_id");
for (const user of users) {
  user.permissions = permissionsMap[user.id] || [];
}
```

## Success Criteria

- [ ] All functions implemented
- [ ] Tests passing (≥80% coverage)
- [ ] Linter passing (0 errors)
- [ ] No security issues (grep scan)
- [ ] Code is readable and documented
- [ ] Performance acceptable
- [ ] Ready for code review
```

---

## 4. TESTING & VALIDATION AGENT

### AGENT.md

```markdown
---
name: testing-agent
description: |
  Testing specialist that writes comprehensive test suites.
  
  Ensures:
  - Happy path works
  - Error cases handled
  - Edge cases covered
  - Performance acceptable
  - Coverage ≥80%
  
model: claude-sonnet-4
tools:
  - read
  - write
  - execute

---

# Testing Agent

## Test Strategy

### Test Types

**1. Unit Tests** (Happy Path)
- Function works with valid input
- Returns expected output

```typescript
describe("generateJWT", () => {
  it("returns valid token with user claims", () => {
    const user = { id: "123", email: "user@example.com" };
    const token = generateJWT(user);
    
    expect(token).toBeDefined();
    expect(typeof token).toBe("string");
    
    const decoded = jwt.decode(token);
    expect(decoded.user_id).toBe("123");
  });
});
```

**2. Error Cases**
- Invalid input handling
- Proper error messages
- Correct status codes

```typescript
it("throws when user not found", async () => {
  await expect(loginUser("nonexistent@example.com", "password"))
    .rejects
    .toThrow(NotFoundError);
});

it("throws when password invalid", async () => {
  const user = await User.create({ email: "test@example.com", password: "123456" });
  
  await expect(loginUser(user.email, "wrongpassword"))
    .rejects
    .toThrow(UnauthorizedError);
});
```

**3. Edge Cases**
- Empty input
- Very large input
- Special characters
- Concurrent requests

```typescript
it("handles empty email", () => {
  expect(() => validateEmail("")).toThrow();
});

it("handles email with +", () => {
  expect(validateEmail("user+tag@example.com")).toBe(true);
});

it("handles concurrent login attempts", async () => {
  const results = await Promise.all([
    loginUser("user@example.com", "password"),
    loginUser("user@example.com", "password"),
    loginUser("user@example.com", "password")
  ]);
  
  // All succeed without conflicts
  expect(results.length).toBe(3);
});
```

### Coverage Target

```
Minimum Coverage: 80%
- Line coverage: ≥80%
- Branch coverage: ≥75%
- Function coverage: ≥80%
```

## Success Criteria

- [ ] All endpoints/functions tested
- [ ] Happy path tests (✓)
- [ ] Error cases covered (✓)
- [ ] Edge cases included (✓)
- [ ] Coverage ≥80%
- [ ] All tests passing
- [ ] No flaky tests
- [ ] Test names descriptive
- [ ] Setup/teardown clean
- [ ] Ready for CI/CD
```

---

## 5. MULTI-AGENT ORCHESTRATION SETUP

### settings.json

```json
{
  "agents": {
    "orchestrator": {
      "model": "claude-opus-4",
      "timeout_minutes": 240,
      "max_retries": 2,
      "parallel_subagents": 4
    },
    
    "subagents": {
      "default_model": "claude-sonnet-4",
      "timeout_minutes": 120,
      "contexts": {
        "security": {
          "description": "Security analysis and design review",
          "tools": ["read", "grep", "write"]
        },
        "architecture": {
          "description": "System design and schema creation",
          "tools": ["read", "write"]
        },
        "implementation": {
          "description": "Code implementation",
          "tools": ["read", "write", "execute"]
        },
        "testing": {
          "description": "Test generation and validation",
          "tools": ["read", "write", "execute"]
        },
        "documentation": {
          "description": "Documentation generation",
          "tools": ["read", "write"]
        }
      }
    }
  },
  
  "monitoring": {
    "track_tokens": true,
    "track_time": true,
    "track_errors": true,
    "alert_thresholds": {
      "error_rate_percent": 5,
      "cost_variance_percent": 200,
      "timeout_minutes": 180
    }
  },
  
  "git": {
    "auto_commit_enabled": false,
    "require_approval": true,
    "approval_required_from": ["architect", "lead"]
  }
}
```

### Hook: Pre-Agent-Run Validation

```bash
#!/bin/bash
# .claude/hooks/pre-agent-run.sh
# Validates before agent runs

set -e

echo "🔍 Pre-agent validation..."

# Check 1: Is MULTI_AGENT_PLAN.md valid?
if [ ! -f "MULTI_AGENT_PLAN.md" ]; then
  echo "❌ MULTI_AGENT_PLAN.md not found"
  exit 2  # BLOCK
fi

# Check 2: Are all required files present?
required_files=("src/" "tests/" ".claude/")
for file in "${required_files[@]}"; do
  if [ ! -e "$file" ]; then
    echo "❌ Required file missing: $file"
    exit 2  # BLOCK
  fi
done

# Check 3: Is state.json valid?
if ! jq empty state.json 2>/dev/null; then
  echo "❌ state.json is invalid JSON"
  exit 2  # BLOCK
fi

echo "✅ All validations passed"
exit 0  # ALLOW
```

### Hook: Post-Agent-Complete Validation

```bash
#!/bin/bash
# .claude/hooks/post-agent-complete.sh
# Validates after agent completes

set -e

echo "🔍 Post-agent validation..."

# Check 1: Output file exists
if [ ! -f "$OUTPUT_FILE" ]; then
  echo "❌ Expected output file not generated: $OUTPUT_FILE"
  echo "{"
  echo "  \"decision\": \"block\","
  echo "  \"reason\": \"Expected output file $OUTPUT_FILE was not generated\""
  echo "}"
  exit 2
fi

# Check 2: Tests pass (if applicable)
if [[ "$OUTPUT_FILE" == *.test.ts ]]; then
  if ! npm test "$OUTPUT_FILE"; then
    echo "{"
    echo "  \"decision\": \"block\","
    echo "  \"reason\": \"Tests in $OUTPUT_FILE failed. Fix before continuing.\""
    echo "}"
    exit 2
  fi
fi

# Check 3: Linting passes (if applicable)
if [[ "$OUTPUT_FILE" == *.ts ]]; then
  if ! npm run lint -- "$OUTPUT_FILE"; then
    echo "{"
    echo "  \"decision\": \"block\","
    echo "  \"reason\": \"Linting errors in $OUTPUT_FILE. Fix before continuing.\""
    echo "}"
    exit 2
  fi
fi

echo "{"
echo "  \"decision\": \"allow\","
echo "  \"reason\": \"All validations passed\""
echo "}"
exit 0
```

---

## DEPLOYMENT CONFIGURATION

### Docker Setup

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Install Claude Agent SDK
RUN npm install @anthropic-ai/agent-sdk

# Copy project
COPY . .

# Install dependencies
RUN npm install

# Start agents
CMD ["npm", "run", "start:agents"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  orchestrator:
    build: .
    environment:
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      AGENT_NAME: orchestrator
      LOG_LEVEL: debug
    ports:
      - "3000:3000"
    volumes:
      - ./data:/app/data
      - ./.claude:/app/.claude
    networks:
      - agent-network

  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: agents_db
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - agent-network

  redis:
    image: redis:7
    ports:
      - "6379:6379"
    networks:
      - agent-network

networks:
  agent-network:

volumes:
  postgres_data:
```

---

## MONITORING & OBSERVABILITY

### Metrics Collection

```typescript
// logger.ts
interface AgentMetrics {
  agent_id: string;
  task_id: string;
  status: "started" | "completed" | "failed";
  tokens_used: number;
  duration_seconds: number;
  cost_usd: number;
  success: boolean;
  error?: string;
}

async function logMetrics(metrics: AgentMetrics) {
  await postgres.query(
    `INSERT INTO agent_metrics 
     (agent_id, task_id, status, tokens, duration, cost, success, error)
     VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
    [
      metrics.agent_id,
      metrics.task_id,
      metrics.status,
      metrics.tokens_used,
      metrics.duration_seconds,
      metrics.cost_usd,
      metrics.success,
      metrics.error
    ]
  );
}
```

### Dashboard SQL Queries

```sql
-- Success rate by agent (last 7 days)
SELECT 
  agent_id,
  COUNT(*) as total_tasks,
  SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful,
  ROUND(100 * SUM(CASE WHEN success THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate
FROM agent_metrics
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY agent_id
ORDER BY success_rate DESC;

-- Cost per agent (last 30 days)
SELECT 
  agent_id,
  SUM(cost_usd) as total_cost,
  AVG(cost_usd) as avg_cost_per_task,
  COUNT(*) as tasks
FROM agent_metrics
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY agent_id
ORDER BY total_cost DESC;

-- Performance metrics
SELECT 
  agent_id,
  MIN(duration_seconds) as min_duration,
  AVG(duration_seconds) as avg_duration,
  MAX(duration_seconds) as max_duration,
  PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY duration_seconds) as p95_duration
FROM agent_metrics
WHERE status = 'completed'
GROUP BY agent_id;
```

---

**Версия**: 1.0  
**Дата**: 2025-01-06  
**Статус**: Production-ready  
**Используй как template для собственных agents**

---

## Related Guides

### Getting Started
- [INDEX.md](INDEX.md) - Master documentation index
- [Complete Practices](CLAUDE-COMPLETE-PRACTICES.md) - Overview of all features (Russian)

### Core Features
- [Shared Architecture](claude-shared-architecture.md) - System overview
- [CLAUDE.md Guide](CLAUDE-CLAUDE-MD-GUIDE.md) - Project memory (English)

### Automation
- [Hooks Guide](claude-hooks-guide.md) - Workflow automation
- [Hooks Examples](claude-hooks-examples.md) - Production examples
- [Hooks Advanced](claude-hooks-advanced.md) - Advanced patterns

### Custom Capabilities
- [Skills Guide](claude-skills-guide.md) - Custom skills
- [Agents Guide](claude-agents-guide.md) - Agent system
- [Templates](claude-templates.md) - Template system

### Reference
- [Troubleshooting](claude-troubleshooting.md) - Common issues

