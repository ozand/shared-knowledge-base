# Agent Orchestration Pattern - Implementation & Examples

**Extracted from:** agent-orchestration.yaml
**Pattern ID:** AGENT-ORCHESTRATION-001

## Implementation Details

### Orchestrator Design

**Role:** Strategic brain, not executor

**Responsibilities:**
- Understand requirements and identify dependencies
- Plan execution phases
- Delegate to specialists
- Monitor progress and handle blockers
- Aggregate and validate results
- Handle errors and recovery

**Model Choice:** Claude Opus 4 (best reasoning)
**Tools:** Minimal (read, route, write)

**State Management:**
```
{
  "request_id": "feature-name-001",
  "status": "in_progress",
  "phase": 2,
  "agents": {
    "security": {"status": "completed", "output": "security-design.md"},
    "architecture": {"status": "completed", "output": "schema.sql"},
    "implementation": {"status": "in_progress", "progress": "75%"},
    "testing": {"status": "queued", "prerequisites": ["implementation"]}
  },
  "decisions": ["Use JWT", "PostgreSQL for production"],
  "next_action": "Wait for implementation to finish"
}
```

### Subagent Design

**Principles:**
- Specialization: Each agent expert in one domain
- Isolation: Each agent has own context
- Clear boundaries: No overlap between agents
- Focused tools: Only what's needed for domain
- Right model: Match model to task complexity

**Agent Types:**

#### Architect Agent
- **Model:** Claude Sonnet 4
- **Tools:** [read, write, grep]
- **Scope:** System design, data models, APIs
- **Output:** ADR (Architecture Decision Record) + schema

#### Security Agent
- **Model:** Claude Sonnet 4
- **Tools:** [read, grep, report]
- **Scope:** Security patterns, compliance, threat modeling
- **Output:** Security review + patterns

#### Implementation Agent
- **Model:** Claude Sonnet 4
- **Tools:** [read, write, execute]
- **Scope:** Code generation, API implementation
- **Output:** Production-ready code

#### Testing Agent
- **Model:** Claude Sonnet 4
- **Tools:** [read, write, execute]
- **Scope:** Test generation, coverage validation
- **Output:** Comprehensive test suite

#### Documentation Agent
- **Model:** Claude Haiku 4
- **Tools:** [read, write]
- **Scope:** Documentation, examples
- **Output:** README + API docs

### Orchestration Workflow

#### Phase 1: Request Handling
1. Receive user request: "Implement OAuth2 login"
2. Analyze requirements
3. Identify dependencies
4. Plan execution phases
5. Estimate effort & risks

#### Phase 2: Delegation

Create task breakdown:

**Phase 1: Security Design (Parallel)**
- Security Agent: Review OAuth2 flows (2h)
- Architecture Agent: Design user schema (2h)

**Phase 2: Implementation (After Phase 1)**
- Implementation Agent: Code endpoints (4h)
  - Depends on: security-design.md + user-schema.sql

**Phase 3: Testing (After Phase 2)**
- Testing Agent: Write tests (3h)
  - Depends on: auth-api.ts
  - Success criteria: coverage ≥80%

**Phase 4: Documentation (Parallel with Phase 3)**
- Documentation Agent: Create docs (2h)

#### Phase 3: Parallel Execution

Spawn agents with:
- Clear task description
- Input files/context
- Expected output format
- Deadline
- Success criteria

Agents run in parallel when possible:
- Security Agent ✓ (2h)
- Architecture Agent ✓ (2h)
- [Wait for both]
- Implementation Agent → (4h)
- [Wait]
- Testing Agent + Documentation Agent (parallel) (2-3h)

#### Phase 4: Aggregation

When all agents complete:
1. Collect all outputs
2. Validate quality:
   - Security design complete?
   - Schema matches requirements?
   - API follows security patterns?
   - Tests passing with ≥80% coverage?
   - Documentation accurate?
3. Check for conflicts
4. Verify dependencies satisfied
5. Aggregate into final deliverable

#### Phase 5: Validation

If validation fails:
- **Option 1:** Re-run agent with feedback
  - Provide failure reason
  - Add additional context
  - Allow 1 retry

- **Option 2:** Use different agent/model
  - Try with better model (Claude Opus)
  - Escalate to human review
  - Create issue for follow-up

If validation passes:
- Mark request as complete
- Update global state
- Return final result

## Real World Examples

### Example 1: OAuth2 Implementation

**Scenario:** Implement OAuth2 login feature

**Team:**
- Orchestrator Agent (Opus 4): Planning & coordination
- Security Agent (Sonnet 4): OAuth2 flow design
- Architecture Agent (Sonnet 4): User schema design
- Implementation Agent (Sonnet 4): API coding
- Testing Agent (Sonnet 4): Test generation
- Documentation Agent (Haiku 4): Docs & examples

**Workflow:**

**Phase 1: Parallel Design (2h)**
- Security Agent (2h): OAuth2 flow review
- Architecture Agent (2h): User schema design
- **Total:** 2h (parallel)

**Phase 2: Implementation (4h)**
- Implementation Agent (4h): Code auth endpoints
- **Depends on:** security-design.md + user-schema.sql
- **Total:** 4h

**Phase 3: Parallel Testing & Docs (3h)**
- Testing Agent (3h): Test suite (85% coverage)
- Documentation Agent (2h): README + API docs
- **Total:** 3h (parallel)

**Results:**
- Total time: **9 hours** (2 + 4 + 3)
- vs single agent: ~40 hours (sequential)
- Speed improvement: **4.4x faster**
- Cost: $37 (mixed models) vs $4000 (40h @ $100/h)
- Cost savings: **100x cheaper**

### Example 2: Parallel Code Review

**Scenario:** Automated PR review system

**Agents:**
- PR Watcher: Detects new PRs, triggers workflow
- Style Reviewer: Linting, naming, patterns
- Security Reviewer: SQLi, XSS, auth issues
- Performance Reviewer: N+1, bundles, loops
- Architecture Reviewer: Design patterns, separation
- Aggregator: Combines all reviews, posts comment

**Workflow:**
- Trigger: GitHub webhook → PR created
- Parallel review: 4 reviewers work simultaneously (5 min)
- Aggregation: Aggregator combines feedback (1 min)
- Posting: Posts comprehensive review as single comment

**Results:**
- Review time: **6 minutes total**
- vs human: ~2 hours (human reviewer)
- Coverage: All domains checked, nothing missed
- Consistency: Same standards every time

### Example 3: Security Audit Parallel

**Scenario:** Comprehensive security audit of codebase

**Agents:**
- SQL Injection Agent: Grep for SQL patterns
- XSS Agent: Grep for innerHTML, eval
- Secrets Agent: Grep for passwords, API keys
- Dependencies Agent: Check outdated packages
- Config Agent: Check insecure configurations
- Report Aggregator: Compile findings

**Workflow:**
- Parallel search: 5 agents search simultaneously (2 min)
- Analysis: Each agent analyzes their findings (3 min)
- Aggregation: Aggregator compiles security report (2 min)

**Results:**
- Total time: **7 minutes**
- vs manual: ~4 hours (manual audit)
- Coverage: 5 agents = 5x coverage
- Consistency: No human fatigue, thorough every time

## Best Practices

1. **Use parallel execution when possible**
   - Guideline: Identify independent tasks that can run simultaneously
   - Example: Security + Architecture agents in Phase 1
   - Benefit: 3-5x faster completion

2. **Match model to task complexity**
   - Guideline:
     - Opus 4: Planning, orchestration, complex reasoning
     - Sonnet 4: Coding, analysis, specialized work
     - Haiku 4: Routine tasks, documentation
   - Benefit: 70% cost savings while maintaining quality

3. **Maintain clear agent boundaries**
   - Guideline: Each agent has one clear domain. No overlap.
   - Example: Security Agent: Only security. Architecture Agent: Only design.
   - Benefit: No duplicated work, clear responsibilities

4. **Use hooks for deterministic validation**
   - Guideline: Don't trust agent self-check. Use hooks for automatic validation.
   - Example: pre-commit hook: Run tests, check coverage, lint
   - Benefit: Quality gates, no false positives

5. **Implement proper error recovery**
   - Guideline: Don't fail entire workflow on single agent failure
   - Example: Re-run agent with feedback, or escalate to human
   - Benefit: Resilient system, graceful degradation

## Anti-Patterns

### Anti-Pattern 1: Too Much Autonomy

**Wrong:** "Here's the codebase. Build the whole system."
**Consequence:** Agent gets lost, makes conflicting decisions, low quality

**Correct:**
```
Build authentication system with constraints:
1. Use JWT tokens
2. Passwords hashed with bcrypt
3. Tests must pass before commit
4. Get approval before merging
```

### Anti-Pattern 2: Wrong Model for Task

**Wrong:** Use Haiku 4 for complex architectural planning
**Consequence:** Fails to understand nuances, poor decisions

**Correct:**
- Opus 4: Planning, orchestration
- Sonnet 4: Coding, specialized work
- Haiku 4: Routine tasks

### Anti-Pattern 3: Context Overflow in Orchestrator

**Wrong:** Orchestrator maintains ALL details of all subagents
**Consequence:** Context overflow, quality degrades

**Correct:**
```
Orchestrator maintains ONLY:
- Completed: Phase 1 (spec.md)
- In Progress: Phase 2 (implementation)
- Pending: Phase 3 (testing)
Each subagent manages their own context
```

### Anti-Pattern 4: No Validation Gates

**Wrong:** Trust agent self-check: "Does this look correct?"
**Consequence:** Agent says yes but it's wrong. No external validation.

**Correct:** Use hooks for automatic validation:
- Run tests (must pass)
- Check coverage (≥80%)
- Run linter (0 errors)
- Security scan (0 critical issues)

### Anti-Pattern 5: Unclear Agent Boundaries

**Wrong:** "Do whatever you think is best"
**Consequence:** Overlap, duplicated work, conflicting implementations

**Correct:**
- Security Agent: Only security decisions
- Architecture Agent: Only design decisions
- Implementation Agent: Only coding
- Clear boundaries, clear handoffs
