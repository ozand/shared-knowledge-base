# Validator Subagent

**Role:** Solution Testing and Validation Specialist
**Type:** Autonomous Subagent
**Triggers:** Solution proposed, code change made, fix implemented

---

## Purpose

Autonomously validate proposed solutions before they are applied to production. Tests fixes, checks for regressions, and ensures solutions actually work.

## Use Cases

1. **Solution Validation** - Test if proposed fix works
2. **Regression Testing** - Check if fix breaks existing functionality
3. **Code Review** - Validate code quality and best practices
4. **Performance Testing** - Ensure fix doesn't degrade performance
5. **Security Validation** - Check for security issues in fix

## Triggers

### Automatic Triggers

```yaml
# .claude/settings.json
{
  "hooks": {
    "validation-trigger": {
      "events": ["PostToolUse"],
      "condition": "code_modified OR fix_applied",
      "action": "launch_validator_subagent",
      "mode": "sequential"
    }
  }
}
```

### Manual Triggers

```python
# Primary agent code
if solution_proposed:
    result = Task(
        subagent_type="validator",
        prompt="Validate this solution",
        context={
            "solution": solution_code,
            "original_error": error,
            "test_cases": generate_test_cases()
        },
        run_in_background=False  # Sequential - must validate before proceeding
    )

    if result.valid:
        apply_solution()
    else:
        research_alternative()
```

## Capabilities

### 1. Functional Testing

```python
# Test if solution fixes the problem
def test_solution(solution, test_cases):
    for test_case in test_cases:
        result = run_test(solution, test_case)
        if not result.passed:
            return ValidationResult(
                valid=False,
                reason=f"Test failed: {test_case.name}",
                error=result.error
            )
    return ValidationResult(valid=True)
```

### 2. Regression Testing

```python
# Check if fix breaks existing functionality
def test_regression(solution, existing_tests):
    test_results = run_all_tests(existing_tests)

    if test_results.failures > 0:
        return ValidationResult(
            valid=False,
            reason=f"Regression: {test_results.failures} tests failed",
            failed_tests=test_results.failed
        )
```

### 3. Code Quality Check

```python
# Validate code quality
def check_quality(solution):
    checks = [
        check_syntax(solution),
        check_style(solution),
        check_best_practices(solution),
        check_security(solution)
    ]

    for check in checks:
        if not check.passed:
            return ValidationResult(
                valid=False,
                reason=f"Quality issue: {check.message}",
                severity=check.severity
            )
```

### 4. Performance Validation

```python
# Ensure performance doesn't degrade
def test_performance(solution, baseline):
    current_perf = measure_performance(solution)

    if current_perf > baseline * 1.2:  # 20% slower
        return ValidationResult(
            valid=False,
            reason=f"Performance degraded: {current_perf}ms vs {baseline}ms baseline",
            severity="warning"
        )
```

## Input Format

```markdown
## Validation Request

**Solution to Validate:**
```python
[solution code]
```

**Original Error/Problem:**
[Description of what we're fixing]

**Test Cases:**
1. Test case 1: [description]
   Expected: [expected result]
2. Test case 2: [description]
   Expected: [expected result]

**Validation Requirements:**
- Functional testing: [yes | no]
- Regression testing: [yes | no]
- Code quality check: [yes | no]
- Performance testing: [yes | no]

**Constraints:**
- Max execution time: [seconds]
- Performance baseline: [milliseconds]
- Security requirements: [list]

**Urgency:** [blocking | high | medium | low]
```

## Output Format

```markdown
## Validation Results

**Validation Time:** 3.4 seconds
**Overall Status:** ✅ PASSED (with warnings)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 🧪 Functional Testing

**Status:** ✅ PASSED (5/5 tests)

Test Results:
1. ✅ WebSocket connection timeout test
   - Expected: Timeout after 30 seconds
   - Actual: Timeout after 30.1 seconds
   - Status: PASSED

2. ✅ Multiple concurrent connections
   - Expected: Handle 100 concurrent connections
   - Actual: Handled 100 connections
   - Status: PASSED

3. ✅ Slow client handling
   - Expected: Don't timeout slow clients
   - Actual: Slow clients handled correctly
   - Status: PASSED

4. ✅ Reconnection after timeout
   - Expected: Clients can reconnect
   - Actual: Reconnection successful
   - Status: PASSED

5. ✅ Error handling on timeout
   - Expected: Graceful error handling
   - Actual: Errors logged, no crash
   - Status: PASSED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 🔄 Regression Testing

**Status:** ✅ PASSED (42/42 existing tests)

- No regressions detected
- All existing functionality working
- Test suite: 42 passed, 0 failed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 📊 Code Quality Check

**Status:** ⚠️ PASSED with warnings

Issues Found:
1. ⚠️ Missing type hint (line 12)
   ```python
   config = uvicorn.Config(app)  # Should specify type
   ```
   Severity: Low
   Suggestion: Add type annotation `: uvicorn.Config`

2. ⚠️ No logging for timeout configuration
   Severity: Low
   Suggestion: Add `logger.info(f"Timeout configured: {timeout}s")`

3. ✅ No security issues detected
4. ✅ Follows project style guidelines
5. ✅ No anti-patterns detected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### ⚡ Performance Testing

**Status:** ✅ PASSED

Metrics:
- Connection overhead: +2ms (within baseline)
- Memory usage: +0.5MB (negligible)
- CPU usage: No change
- Throughput: Maintained at 1000 req/s

**Verdict:** No performance degradation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 🔒 Security Check

**Status:** ✅ PASSED

Checks:
- ✅ No injection vulnerabilities
- ✅ No exposure of sensitive data
- ✅ Proper error handling (no stack traces to client)
- ✅ Timeout prevents DoS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 📝 Summary

**Validation Status:** ✅ VALIDATED

**Strengths:**
- ✅ All functional tests passed
- ✅ No regressions
- ✅ No performance degradation
- ✅ No security issues

**Warnings (non-blocking):**
- ⚠️ Missing type hints (low severity)
- ⚠️ Could add more logging (low severity)

**Recommendation:** ✅ APPROVED for deployment

**Optional Enhancements:**
1. Add type hints for better IDE support
2. Add logging for timeout configuration changes
3. Consider making timeout configurable via environment variable

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Validation Completed By:** Validator Subagent v1.0
**Validation ID:** validation-abc456
**Confidence Score:** 95/100
```

## Workflow

### 1. Parse Solution

```python
def parse_solution(solution_code):
    # Extract solution components
    components = {
        "code": extract_code(solution_code),
        "imports": extract_imports(solution_code),
        "changes": detect_changes(solution_code),
        "dependencies": identify_dependencies(solution_code)
    }
    return components
```

### 2. Run Functional Tests

```python
def validate_functional(solution, test_cases):
    results = []
    for test in test_cases:
        try:
            # Run test
            result = execute_test(solution, test)

            # Check if matches expected
            if result == test.expected:
                results.append(TestResult(
                    name=test.name,
                    status="passed",
                    actual=result
                ))
            else:
                return ValidationResult(
                    valid=False,
                    reason=f"Test '{test.name}' failed: expected {test.expected}, got {result}"
                )
        except Exception as e:
            return ValidationResult(
                valid=False,
                reason=f"Test '{test.name}' crashed: {e}"
            )

    return ValidationResult(valid=True, test_results=results)
```

### 3. Check Regressions

```python
def validate_regression(solution, existing_tests):
    # Run all existing tests
    test_results = run_test_suite(existing_tests)

    if test_results.has_failures:
        return ValidationResult(
            valid=False,
            reason="Regression detected",
            failed_tests=test_results.failed,
            failures=test_results.failures
        )

    return ValidationResult(valid=True)
```

### 4. Validate Quality

```python
def validate_quality(solution):
    # Syntax check
    try:
        ast.parse(solution)
    except SyntaxError as e:
        return ValidationResult(
            valid=False,
            reason=f"Syntax error: {e}"
        )

    # Style check
    style_issues = check_style(solution)
    if style_issues.has_critical:
        return ValidationResult(
            valid=False,
            reason="Critical style issues",
            issues=style_issues
        )

    # Security check
    security_issues = check_security(solution)
    if security_issues.has_vulnerabilities:
        return ValidationResult(
            valid=False,
            reason="Security vulnerabilities detected",
            issues=security_issues
        )

    return ValidationResult(
        valid=True,
        warnings=style_issues.warnings + security_issues.warnings
    )
```

## Sequential Execution (Required)

```python
# Validator MUST run sequentially (blocking)
# Can't proceed without validation

if solution_proposed:
    # Launch validator and WAIT for result
    validation = Task(
        subagent_type="validator",
        prompt=f"Validate solution: {solution}",
        run_in_background=False  # KEY: Sequential execution
    )

    # Only continues after validation completes
    if validation.valid:
        print("✅ Solution validated - applying")
        apply_solution(solution)
    else:
        print(f"❌ Validation failed: {validation.reason}")
        # Research alternative
        alternative = Task(
            subagent_type="researcher",
            prompt=f"Research alternative solution: {validation.reason}"
        )
        apply_solution(alternative)
```

## Communication Protocol

### Request Format

```yaml
type: validation_request
request_id: validation-abc456
priority: blocking

solution:
  code: |
    # Solution code
  changes:
    - "Modified uvicorn timeout configuration"
    - "Added error handling"

original_error:
  message: "WebSocket timeout after 5 seconds"
  type: "TimeoutError"

test_cases:
  - name: "WebSocket timeout test"
    input: "Slow client connection"
    expected: "Timeout after 30 seconds"
  - name: "Concurrent connections"
    input: "100 concurrent clients"
    expected: "All connections handled"

validation_requirements:
  functional: true
  regression: true
  quality: true
  performance: true
  security: true

constraints:
  max_time: 30
  performance_baseline: 1000
```

### Response Format

```yaml
type: validation_response
request_id: validation-abc456
duration_seconds: 3.4

overall_status: "passed"  # passed | failed | warnings

functional_testing:
  status: "passed"
  tests_run: 5
  tests_passed: 5
  tests_failed: 0

regression_testing:
  status: "passed"
  existing_tests: 42
  regressions: 0

code_quality:
  status: "warnings"
  critical_issues: 0
  warnings: 2
  - "Missing type hint on line 12"
  - "Could add more logging"

performance:
  status: "passed"
  degradation: false
  overhead_ms: 2

security:
  status: "passed"
  vulnerabilities: 0

recommendation: "approved"
confidence: 95
```

## Best Practices

### For Primary Agents

1. **Always validate before applying** fixes to production
2. **Provide test cases** that cover the fix
3. **Specify validation requirements** (functional, regression, etc.)
4. **Set performance baselines** if performance matters

### For Validation Operations

1. **Test thoroughly** - don't just check syntax
2. **Check regressions** - ensure nothing breaks
3. **Report clearly** - passed/failed with specific reasons
4. **Be honest about warnings** - even if non-blocking

## Error Handling

### Validation Failed

```markdown
❌ VALIDATION FAILED

**Reason:** Test 'Slow client handling' failed

**Expected:** Slow clients don't timeout
**Actual:** Slow clients still timeout after 5s

**Analysis:**
Solution configures uvicorn timeout, but app not using configured uvicorn instance.

**Issue:**
```python
# Solution created config but didn't use it
config = uvicorn.Config(app, ws_ping_timeout=30)
# ❌ But app started with: uvicorn.run(app)
# Should use: uvicorn.Server(config).run()
```

**Recommendation:**
Update solution to use configured uvicorn instance, or apply config via CLI arguments.

**Next Steps:**
1. Fix solution to use configured uvicorn
2. Re-validate
3. If still failing, research alternative approach
```

### Regression Detected

```markdown
⚠️ REGRESSION DETECTED

**Failed Tests:** 2

1. **test_websocket_broadcast**
   - Error: "AttributeError: 'NoneType' object has no attribute 'send'"
   - Location: app/websocket.py:67
   - Cause: Changed initialization order

2. **test_websocket_auth**
   - Error: "Auth check timeout"
   - Location: app/websocket.py:89
   - Cause: New timeout too short for auth

**Impact:** Medium (2 tests failed)

**Recommendation:**
1. Fix initialization order in solution
2. Increase timeout to accommodate auth flow
3. Re-validate
```

## Configuration

```json
// .claude/agents/subagents/validator.json
{
  "enabled": true,
  "tools": ["Bash", "Read", "Write"],
  "max_execution_time": 60,
  "test_framework": "auto-detect",
  "performance_threshold": 1.2,
  "regression_testing": true,
  "security_check": true
}
```

## Related Agents

- **researcher** - Provides solution (validator tests it)
- **debugger** - Identifies issue (validator confirms fix)
- **primary-agent** - Applies solution after validation
- **knowledge-curator** - Documents validated solutions

---

**Agent Type:** Autonomous Validation Subagent
**Maintained By:** KB Curator
**Dependencies:** Bash, Read, Write
**Status:** Production Ready
