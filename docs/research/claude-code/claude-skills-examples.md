# Claude Code SKILLS: Практические примеры и шаблоны
## Копируй-вставляй примеры для 5 основных типов Skills

---

## 1. TESTING SKILL (Полный пример)

### Файловая структура

```
.claude/skills/testing/
├── SKILL.md                    ← Основная инструкция
├── resources/
│   ├── patterns.md             ← Тестовые паттерны
│   ├── examples/
│   │   ├── simple-unit.test.ts
│   │   ├── async-api.test.ts
│   │   └── react-component.test.ts
│   ├── assertions.md           ← Все типы assertions
│   ├── template.test.ts        ← Шаблон нового теста
│   └── checklist.md            ← Pre-commit checklist
└── scripts/
    └── run-tests.sh            ← Optional: script helper
```

### SKILL.md

```markdown
---
name: testing-skill
description: |
  Generates unit tests with 80%+ code coverage.
  
  Triggers when:
  - User asks to "write tests", "generate tests", "test this"
  - Need Vitest + React Testing Library patterns
  - Part of code review or deployment process
  
  Outputs complete test files with edge cases,
  error handling, and assertions.
---

# Testing Skill

## What This Skill Does

1. **Analyze** the code you want to test
2. **Generate** tests following project patterns
3. **Validate** coverage is ≥80%
4. **Iterate** if needed

## When to Use

- Writing tests for new functions
- Adding tests to untested code  
- Code review requires test coverage
- Increasing overall code coverage

## Key Instructions

### Step 1: Read Target Code
Ask user to provide:
- The function/component to test
- Any relevant dependencies
- Known edge cases

Then read the file and understand:
- Function signature and return types
- External dependencies
- Error cases

### Step 2: Generate Test File

Follow this structure:
```typescript
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { functionUnderTest } from '../src/module';

describe('functionUnderTest', () => {
  describe('happy path', () => {
    it('should do X when given Y', () => {
      expect(functionUnderTest(input)).toBe(expected);
    });
  });

  describe('error handling', () => {
    it('should throw when input is invalid', () => {
      expect(() => functionUnderTest(null)).toThrow();
    });
  });

  describe('edge cases', () => {
    it('should handle empty input', () => {
      expect(functionUnderTest([])).toEqual([]);
    });
  });
});
```

### Step 3: Verify Coverage

Run tests and check coverage:
```bash
npx vitest --coverage src/module.test.ts
```

Requirements:
- ✅ Line coverage ≥80%
- ✅ Branch coverage ≥75%
- ✅ Function coverage ≥80%

If below target: identify uncovered lines and add tests.

### Step 4: Review with Checklist

Before submitting, verify:
- [ ] All describe/it blocks follow naming pattern
- [ ] Assertions use .toEqual() or .toBe() correctly
- [ ] Error cases are tested
- [ ] Edge cases covered (empty, null, undefined)
- [ ] No console.log() in tests
- [ ] No test.skip() or test.only()

## Important Patterns

### Pattern: Async Function Testing
See @resources/patterns.md - Async section

### Pattern: React Component Testing  
See @resources/examples/react-component.test.ts

### Pattern: Error Handling
See @resources/examples/error-handling.test.ts

## Tools Required
- **Read**: Read source files
- **Write**: Create test files
- **Execute**: Run `npx vitest --coverage` (optional)

## Full Examples
See @resources/examples/ for complete working examples.

## Template
Copy template: @resources/template.test.ts

## Common Issues

**Q: How many tests per function?**
A: Aim for 3-5 test cases:
  - 1 happy path test
  - 1-2 error case tests
  - 1-2 edge case tests

**Q: Should I test implementation details?**
A: No! Test behavior, not internals.
```

### resources/patterns.md (Excerpt)

```markdown
# Testing Patterns

## Happy Path Testing

Basic case: function works correctly with normal input.

```typescript
it('should return user when ID exists', () => {
  const user = getUserById(1);
  expect(user.name).toBe('Alice');
});
```

## Error Handling

Test that function fails correctly for bad input.

```typescript
it('throws when user ID is negative', () => {
  expect(() => getUserById(-1)).toThrow('Invalid ID');
});

it('throws when user not found', () => {
  expect(() => getUserById(999)).toThrow('User not found');
});
```

## Edge Cases

Boundary values and special cases:

```typescript
it('handles empty array', () => {
  expect(filterUsers([])).toEqual([]);
});

it('handles null input', () => {
  expect(filterUsers(null)).toEqual([]);
});

it('handles undefined properties', () => {
  const users = [{ name: 'Alice', age: undefined }];
  expect(filterUsers(users)).toEqual(users);
});
```

## Async Testing

For promises and async/await:

```typescript
it('resolves with user data', async () => {
  const user = await fetchUser(1);
  expect(user.id).toBe(1);
});

it('rejects with error message', async () => {
  await expect(fetchUser(-1)).rejects.toThrow();
});
```

## React Component Testing

See examples/react-component.test.ts
```

---

## 2. CODE REVIEW SKILL

### SKILL.md

```markdown
---
name: code-review-skill
description: |
  Reviews code for architecture, performance, security,
  and readability issues. Provides specific feedback
  with references to team standards.
---

# Code Review Skill

## What This Does

Automated code review checking:
1. Architecture compliance
2. Performance anti-patterns
3. Security vulnerabilities
4. Code clarity and maintainability

## Quick Review Process

### Step 1: Architecture Check
Review against patterns in @resources/architecture.md

Look for:
- Proper separation of concerns
- Correct use of design patterns
- Valid dependency directions

### Step 2: Performance Review
Check for common anti-patterns:
- N+1 database queries
- Unnecessary re-renders (React)
- Inefficient loops or algorithms

### Step 3: Security Audit
Search for vulnerabilities:
```bash
grep -rn "eval\|exec\|innerHTML\|dangerouslySetInnerHTML" \
  "$CHANGED_FILES"
```

### Step 4: Readability Check
Verify:
- Variable names are descriptive
- Functions are focused (single responsibility)
- Complex logic has comments
- No dead code

## Generating Review

Create report with:

```markdown
# Code Review: PR #1234

## Summary
- Architecture: ✅ PASS
- Performance: ⚠️ 1 concern
- Security: ✅ PASS  
- Readability: ✅ PASS

## Issues Found

### Issue 1: N+1 Query Pattern (Performance)
**File**: src/user.service.ts:45
**Severity**: HIGH
**Code**:
\`\`\`typescript
const users = await getAllUsers();
for (const user of users) {
  user.posts = await getPostsByUser(user.id); // ❌ Query per iteration!
}
\`\`\`

**Fix**:
\`\`\`typescript
const users = await getAllUsers();
const postsByUser = await getPostsByUserId(users.map(u => u.id));
// Map results to users
\`\`\`

[Continue with other issues...]

## Recommendation
**APPROVE** with suggestions to address HIGH priority issues.
```

## Tools
- **Grep**: Find vulnerable patterns
- **Read**: Analyze code context
- **Write**: Generate review report
```

---

## 3. DOCUMENTATION SKILL

### SKILL.md

```markdown
---
name: documentation-skill
description: |
  Generates README files, API documentation, and
  architecture guides. Follows company style and
  includes examples and setup instructions.
---

# Documentation Skill

## What This Does

Creates comprehensive documentation:
- README.md with quick start
- API documentation
- Architecture guides
- Contributing guidelines

## Process

### Step 1: Gather Information
Understand the project:
- What does it do?
- Who uses it?
- How do you set it up?
- What's the API/functionality?

### Step 2: Generate README

Use template @resources/templates/README.md

Structure:
```markdown
# Project Name

## What It Does
[One-paragraph summary]

## Installation
```bash
npm install
```

## Quick Start
[Minimal example]

## Features
- Feature 1
- Feature 2

## API Reference
[Endpoint/function details]

## Contributing
[How to contribute]

## License
[License info]
```

### Step 3: Generate API Docs

For each function/endpoint, document:
- **What it does** (one sentence)
- **Parameters** (types, descriptions)
- **Returns** (type, description)
- **Example** (minimal working example)
- **Errors** (what can go wrong)

```markdown
### getUserById(id: number): Promise<User>

Gets a user by their ID.

**Parameters:**
- `id: number` - The user ID to fetch

**Returns:**
Promise resolving to User object

**Example:**
\`\`\`javascript
const user = await getUserById(123);
console.log(user.name); // "Alice"
\`\`\`

**Throws:**
- Throws if ID is negative
- Throws if user not found
```

### Step 4: Review Completeness

Checklist:
- [ ] Project purpose is clear
- [ ] Setup instructions are complete
- [ ] At least one working example
- [ ] All public functions documented
- [ ] Error cases documented

## Tools
- **Read**: Read source code and comments
- **Write**: Create documentation files
```

---

## 4. REFACTORING SKILL

### SKILL.md

```markdown
---
name: refactoring-skill
description: |
  Safely refactors code following established patterns.
  Handles type updates, test modifications, and maintains
  backward compatibility where needed.
---

# Refactoring Skill

## When to Use

- Extract repeated code into functions
- Rename variables for clarity
- Simplify complex logic
- Apply design patterns
- Update outdated patterns

## Important Rules

1. **Make small, focused changes**
   - One refactoring at a time
   - Easy to review

2. **Keep tests passing**
   - Refactor code, not tests
   - Update only if test logic changes

3. **Maintain backward compatibility**
   - Don't break public APIs
   - Deprecate before removing

4. **Document changes**
   - Explain why (not just what)
   - Reference any patterns used

## Process

### Step 1: Plan Refactoring
Before coding, explain:
- Current code and its issues
- Desired end state
- Why this improves things
- Any breaking changes (if unavoidable)

```markdown
## Refactoring Plan

**Issue**: getUserPosts() function is 150 lines
- Multiple concerns (fetching, filtering, sorting)
- Hard to test in isolation
- Violates Single Responsibility Principle

**Solution**: Split into 3 functions
- fetchUserPosts(userId) - Get from DB
- filterActivePosts(posts) - Filter
- sortByDate(posts) - Sort

**Benefits**:
- Each function is testable
- Easy to reuse pieces
- Clear intent
```

### Step 2: Execute in Small Steps

Don't refactor everything at once:
1. Extract first concern
2. Test → verify working
3. Extract second concern
4. Test → verify working
5. Extract third concern
6. Test → verify working

### Step 3: Verify Tests Still Pass

```bash
npm test
```

All tests should pass without modification.
If test breaks → refactoring went too far.

## Tools
- **Read**: Analyze existing code
- **Write**: Updated code
- **Execute**: Run tests to verify
```

---

## 5. DEPLOYMENT SKILL

### SKILL.md

```markdown
---
name: deployment-skill
description: |
  Automates deployment process: builds, tests,
  validates, deploys to staging/production,
  monitors for issues.
---

# Deployment Skill

## Deployment Pipeline

```
1. Validate
   ├─ Tests pass
   ├─ Build succeeds
   └─ No security issues

2. Build
   ├─ Compile/bundle code
   ├─ Optimize assets
   └─ Generate artifacts

3. Deploy Staging
   ├─ Deploy to staging environment
   ├─ Run smoke tests
   └─ Verify basic functionality

4. Deploy Production
   ├─ Zero-downtime deployment
   ├─ Gradual rollout (10%, 50%, 100%)
   └─ Monitor for errors

5. Post-Deployment
   ├─ Health checks
   ├─ Performance monitoring
   └─ Team notification
```

## Step-by-Step

### Step 1: Pre-Deployment Checks

```bash
# Run tests
npm test

# Check coverage
npm run coverage

# Build
npm run build

# Security scan
npm run security-audit
```

All must pass.

### Step 2: Deploy to Staging

```bash
npm run deploy:staging
```

Then verify:
- [ ] Application loads
- [ ] Key endpoints respond
- [ ] No errors in logs
- [ ] Performance acceptable

### Step 3: Deploy to Production

```bash
npm run deploy:production
```

Deployment strategy:
- **Canary**: 10% traffic → 50% → 100%
- **Monitoring**: Check error rate, latency
- **Rollback**: If errors spike → rollback

### Step 4: Post-Deployment

Monitor:
- Error rate (target: <0.1%)
- Response time (target: <200ms p99)
- CPU usage (target: <70%)
- Memory usage (target: <80%)

### Step 5: Notify Team

Announce:
```slack
✅ Deployment complete!
- Version: 1.2.3
- Changes: [summary]
- Deployed at: 14:30 UTC
- Status: All healthy
- Rollback plan: Available if needed
```

## Tools
- **Execute**: Run deployment scripts
- **Read**: Check logs and metrics
- **Write**: Generate deployment report
```

---

## ШАБЛОНЫ для быстрого старта

### Шаблон 1: Минимальный SKILL.md

```markdown
---
name: my-skill
description: |
  Brief description of what this skill does.
  
  Triggers when user asks for [specific thing].
  Outputs [what you get].
---

# [Skill Name]

## When to Use
- User asks to "[action]"
- Part of [workflow]

## What This Does
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Key Instructions

### Step 1: [Action]
[Description]

### Step 2: [Action]
[Description]

## Tools Required
- **[Tool]**: For [purpose]

## Important Notes
- [Rule 1]
- [Rule 2]

## Examples
See @resources/examples/
```

### Шаблон 2: settings.json для Skills

```json
{
  "skills": {
    "paths": [
      "./.claude/skills",
      "./packages/*/claude/skills"
    ],
    "enabled": [
      "testing-skill",
      "code-review-skill",
      "documentation-skill",
      "refactoring-skill",
      "deployment-skill"
    ],
    "auto_discover": true,
    "version_check": true
  }
}
```

### Шаблон 3: Evaluation Scenarios

```markdown
# Skill Evaluation

## Evaluation 1: Basic Case

**Request**: "Generate tests for the login function"

**Expected Behavior**:
- [ ] Reads login function
- [ ] Generates Vitest tests
- [ ] Covers error cases (invalid email, wrong password)
- [ ] Achieves ≥80% coverage
- [ ] Matches project patterns

**Score**: 0-5 points
- 5: All tests perfect
- 4: 1-2 small issues
- 3: 3-4 issues
- 2: Missing key coverage
- 1: Doesn't work

---

## Evaluation 2: Medium Case

**Request**: "Add tests for API endpoint that fetches user posts with pagination"

**Expected Behavior**:
- [ ] Tests happy path (returns posts)
- [ ] Tests error path (user not found)
- [ ] Tests pagination (limit, offset)
- [ ] Tests async/await correctly
- [ ] Tests error handling

**Score**: 0-5 points

---

## Evaluation 3: Complex Case

**Request**: "Generate tests for React component with form, validation, and API call"

**Expected Behavior**:
- [ ] Uses React Testing Library
- [ ] Tests user interactions (typing, clicking)
- [ ] Tests validation messages
- [ ] Tests API call (success and error)
- [ ] Tests loading state
- [ ] Tests accessibility

**Score**: 0-5 points

---

## Baseline (Without Skill)
- Eval 1: 2/5
- Eval 2: 1/5
- Eval 3: 1/5
- **Total**: 4/15 (27%)

## After Skill Implementation
- Target: 13+/15 (87%+)
```

---

## BEST PRACTICES SUMMARY

```
✅ DO:
1. Keep SKILL.md ≤500 lines
2. Write specific descriptions
3. Test with fresh Claude instances
4. Use evaluation-driven development
5. Consolidate related skills
6. Document in CLAUDE.md
7. Version with semantic versioning
8. Get team feedback

❌ DON'T:
1. Create micro-skills (too many)
2. Write vague descriptions
3. Nest references deeply
4. Hard-code paths
5. Skip error handling in scripts
6. Forget to test edge cases
7. Deploy without team review
8. Ignore user feedback
```

---

**Дата**: 2025-01-06  
**Версия**: 1.0  
**Статус**: Ready to copy-paste

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

