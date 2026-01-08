# Skill: Research Enhance

## What this Skill does
Enhance knowledge base entries with deep research from external sources. Incorporates latest best practices, community consensus, and version-specific information.

## Trigger
- User mentions "enhance", "research", "update entry", "add best practices"
- Entry score is low (75-84) and needs improvement
- After library/framework version updates
- During entry creation (to ensure completeness)
- Part of curator workflow

## What Claude can do with this Skill

### 1. Research Sources
```bash
# Official Documentation
- Language/framework docs (Python.org, FastAPI.io, etc.)
- API references and changelogs
- Release notes and migration guides

# Community Knowledge
- Stack Overflow (high-vote answers)
- GitHub issues and discussions
- Reddit (r/Python, r/javascript, etc.)
- Dev.to and Medium articles

# Best Practices
- Official style guides (PEP, Airbnb, etc.)
- Security advisories
- Performance optimization guides
- Testing best practices
```

### 2. Enhancement Workflow

#### Step 1: Analyze Entry Gaps
```yaml
# Current entry analysis
python/errors/async-errors.yaml:
  ✅ Problem: Clear
  ✅ Solution: Working code
  ⚠️  Root cause: Could be deeper
  ❌ Prevention: Missing
  ❌ Best practices: Not included
  ⚠️  Version info: Outdated (Python 3.9, now 3.13)

  Current score: 72/100
  Target score: 85+
```

#### Step 2: Research Plan
```
Research questions for async/await errors:
1. What's new in Python 3.11+ for async?
2. Common async pitfalls (official docs)
3. Community best practices (Stack Overflow)
4. Performance considerations
5. Security implications
6. Testing strategies for async code
```

#### Step 3: Conduct Research
```bash
# Official Python docs
https://docs.python.org/3/library/asyncio.html
→ Latest asyncio best practices
→ New Task Groups (Python 3.11+)
→ Error handling patterns

# Stack Overflow
Search: "python async await common mistakes"
→ Top 5 most common async errors
→ Community-voted solutions
→ Edge cases and pitfalls

# GitHub Discussions
python/cpython repository
→ Real-world async issues
→ Maintainer recommendations
→ Performance tips
```

#### Step 4: Enhance Entry
```yaml
# Enhanced entry
version: "1.1"  # Updated version
category: "async-errors"
last_updated: "2026-01-07"

errors:
  - id: "PYTHON-018"
    title: "Async/Await Error Handling"
    severity: "high"
    scope: "python"

    problem: |
      Improper error handling in async/await code leads to
      silent failures and uncaught exceptions.

      Common scenarios:
      - Missing await on coroutine calls
      - Not catching exceptions in tasks
      - Forgetting to gather tasks
      - Mixed sync/async code

    symptoms:
      - "RuntimeWarning: coroutine never awaited"
      - "Task was destroyed but it is pending"
      - Silent failures in async code
      - Unhandled exceptions in event loop

    root_cause: |
      Async errors occur because:
      1. Coroutines must be awaited or scheduled
      2. Exceptions in tasks aren't propagated automatically
      3. Event loop doesn't catch all exceptions by default
      4. Task groups (Python 3.11+) improve error handling

      Technical details:
      - Coroutines are lazy, don't run until awaited
      - create_task() detaches task from caller
      - Exceptions in detached tasks go to event loop
      - asyncio.run() catches exceptions, but task.create() doesn't

    solution:
      code: |
        import asyncio
        import logging

        # Python 3.11+: Use TaskGroup for error handling
        async def main():
            try:
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(task1())
                    tg.create_task(task2())
                    # All exceptions automatically gathered
            except* Exception as e:  # ExceptionGroup
                logging.error(f"Tasks failed: {e}")

        # Python 3.9-3.10: Manual error handling
        async def main_legacy():
            tasks = [
                asyncio.create_task(task1()),
                asyncio.create_task(task2())
            ]

            results = await asyncio.gather(
                *tasks,
                return_exceptions=True  # Catch exceptions
            )

            for result in results:
                if isinstance(result, Exception):
                    logging.error(f"Task failed: {result}")

        # Always use asyncio.run() at entry point
        if __name__ == "__main__":
            asyncio.run(main())

      explanation: |
        **Python 3.11+ TaskGroup (Recommended):**
        - Automatically awaits all tasks
        - Groups exceptions into ExceptionGroup
        - Cancels remaining tasks on error
        - Prevents task leaks

        **Legacy approach (Python 3.9-3.10):**
        - Use asyncio.gather(return_exceptions=True)
        - Manually check for exceptions in results
        - Remember to await all tasks

        **Key principles:**
        1. Always use asyncio.run() at entry point
        2. Prefer TaskGroup over create_task() (3.11+)
        3. Use return_exceptions=True with gather()
        4. Add logging for async errors

    prevention:
      - "Always use TaskGroup (Python 3.11+) for multiple tasks"
      - "Enable asyncio debug mode in development: PYTHONASYNCIODDEBUG=1"
      - "Use static type checker (mypy) with async support"
      - "Write unit tests for async code with pytest-asyncio"
      - "Review async code for missing awaits"
      - "Use linters: flake8-async, pylint (async checks)"

    best_practices: |
      **Error Handling:**
      - Use try/except blocks in coroutines
      - Log exceptions at appropriate error level
      - Provide context in error messages
      - Use structured logging for async operations

      **Testing:**
      - Test both success and failure paths
      - Use pytest-asyncio for async tests
      - Mock async dependencies properly
      - Test concurrent execution

      **Performance:**
      - Avoid creating too many tasks (throttle if needed)
      - Use asyncio.gather() for independent tasks
      - Use TaskGroup for dependent tasks (3.11+)
      - Profile async code with asyncio debug

      **Security:**
      - Validate inputs before async operations
      - Sanitize error messages (don't leak sensitive data)
      - Use timeouts for network operations
      - Limit concurrent operations

    version_notes: |
      **Python 3.13 (Latest):**
      - Improved TaskGroup error messages
      - Better performance for task cancellation
      - New asyncio.PickledObjectWarning

      **Python 3.11:**
      - Introduced TaskGroup (recommended)
      - ExceptionGroup for multiple exceptions
      - except* syntax for exception groups

      **Python 3.9-3.10:**
      - Use asyncio.gather(return_exceptions=True)
      - Manual exception handling required

    references:
      - "https://docs.python.org/3/library/asyncio-task.html#task-groups"
      - "https://docs.python.org/3/whatsnew/3.11.html#asyncio"
      - "https://stackoverflow.com/questions/37278647/how-to-properly-async-await"
      - "https://realpython.com/async-io-python/"

    tags: ["async", "await", "error-handling", "python-3.11", "taskgroup", "best-practices"]
```

### 3. Quality Improvement
```
Before enhancement:
  Score: 72/100
  - Completeness: 20/30
  - Technical Accuracy: 25/30
  - Documentation: 12/20
  - Best Practices: 15/20

After enhancement:
  Score: 91/100  ⭐⭐⭐⭐⭐
  - Completeness: 29/30  (+9)
  - Technical Accuracy: 28/30  (+3)
  - Documentation: 19/20  (+7)
  - Best Practices: 15/20  (no change, already good)
```

## Key files to reference
- Research sources: Official docs, Stack Overflow, GitHub
- Quality standards: `@curator/QUALITY_STANDARDS.md`
- Entry format: `@universal/patterns/shared-kb-yaml-format.yaml`
- Version tracking: `@tools/kb_versions.py`

## Implementation rules
1. **Cite sources** - Add references section
2. **Verify currency** - Check latest versions
3. **Test solutions** - Ensure code works
4. **Update metadata** - Increment version, update date
5. **Validate** - Ensure score ≥85 after enhancement

## Common commands
```bash
# Enhance single entry
python tools/kb.py enhance python/errors/async-errors.yaml

# Research and enhance
python tools/kb.py enhance --research python/errors/async-errors.yaml

# Check for updates
python tools/kb_versions check --library python

# Batch enhance category
python tools/kb.py enhance python/errors --auto-research
```

## Research Checklist

### For Python Entries
- [ ] Check latest Python version (3.13 as of 2025)
- [ ] Review PEPs relevant to topic
- [ ] Search Stack Overflow (top answers)
- [ ] Check Python docs for updated examples
- [ ] Verify code against current best practices

### For Framework Entries (FastAPI, Django, etc.)
- [ ] Check latest framework version
- [ ] Review framework changelogs
- [ ] Search framework-specific resources
- [ ] Check official examples
- [ ] Verify against current docs

### For Technology Entries (Docker, PostgreSQL, etc.)
- [ ] Check latest stable version
- [ ] Review official documentation
- [ ] Search community forums
- [ ] Check for breaking changes
- [ ] Verify security advisories

## Enhancement Categories

### 1. Add Missing Prevention
```yaml
prevention:
  - "Specific actionable step"
  - "Tool or technique to avoid error"
  - "Best practice to follow"
```

### 2. Include Best Practices
```yaml
best_practices: |
  **Category 1:**
  - Best practice 1
  - Best practice 2

  **Category 2:**
  - Best practice 3
```

### 3. Add Version Information
```yaml
version_notes: |
  **Version X.Y (Latest):**
  - New feature or change

  **Version A.B:**
  - When feature was introduced
```

### 4. Include References
```yaml
references:
  - "https://official-docs.com"
  - "https://stack-overflow.com/q/123456"
  - "https://github.com/repo/discussions/123"
```

### 5. Add Performance Notes
```yaml
performance: |
  - Consideration 1
  - Benchmark if relevant
  - Optimization tips
```

### 6. Include Security Considerations
```yaml
security: |
  - Security risk if applicable
  - Mitigation strategies
  - Best practices for security
```

## Related Skills
- `kb-validate` - Validate after enhancement
- `audit-quality` - Quality audit identifies gaps
- `update-versions` - Update to latest versions
- `identify-gaps` - Find what's missing

## Research Tools

### Official Documentation
```bash
# Python
https://docs.python.org/3/

# FastAPI
https://fastapi.tiangolo.com/

# Docker
https://docs.docker.com/

# PostgreSQL
https://www.postgresql.org/docs/
```

### Community Resources
```bash
# Stack Overflow
https://stackoverflow.com/questions/tagged/<topic>

# GitHub Discussions
https://github.com/<org>/<repo>/discussions

# Reddit
https://www.reddit.com/r/<subreddit>/

# Dev.to
https://dev.to/t/<topic>
```

## Automation
Schedule periodic enhancement:
```bash
# Monthly: Check for updates
python tools/kb_versions check --all

# Quarterly: Enhance outdated entries
python tools/kb.py enhance --outdated --since "3 months ago"
```

---
**Version:** 1.0
**Last Updated:** 2026-01-07
**Skill Type:** Research & Enhancement
**Target Score:** 85+/100 after enhancement
