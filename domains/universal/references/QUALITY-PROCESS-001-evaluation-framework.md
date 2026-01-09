# Quality Assurance Pattern - Evaluation Framework

**Extracted from:** quality-assurance.yaml
**Pattern ID:** QUALITY-PROCESS-001

## Evaluation Framework

### Quality Assessment

**Criteria:**

1. **Technical correctness** (Weight: High)
   - Code works as intended
   - No bugs or errors
   - Follows best practices

2. **Completeness** (Weight: High)
   - Addresses full problem
   - Includes examples
   - Has documentation

3. **Testing** (Weight: Medium)
   - Tested in real environment
   - Includes test cases
   - Verification provided

4. **Documentation** (Weight: Medium)
   - Clear problem statement
   - Solution explained
   - Examples provided

**Scoring:**
- Excellent: ⭐⭐⭐⭐⭐ (5/5) - All criteria met, production-ready
- Good: ⭐⭐⭐⭐ (4/5) - Most criteria met, minor improvements needed
- Medium: ⭐⭐⭐ (3/5) - Some criteria met, needs work
- Low: ⭐⭐ (2/5) - Few criteria met, significant issues
- Poor: ⭐ (1/5) - Does not meet standards

### Process Assessment

**Criteria:**

1. **GitHub issue created** (Weight: Critical)
   - Correct: Agent creates GitHub issue first
   - Incorrect: Agent creates PR directly

2. **Attribution format** (Weight: High)
   - Correct: Follows GITHUB-ATTRIB-001 format
   - Incorrect: Missing attribution or incomplete

3. **Labels applied** (Weight: Medium)
   - Correct: Proper labels (agent:*, project:*, etc.)
   - Incorrect: No labels or incorrect labels

4. **Role compliance** (Weight: Critical)
   - Correct: Project agent does not modify KB directly
   - Incorrect: Project agent commits to KB or creates PR

**Decision Rules:**
- Rule 1: ANY critical criterion failed → Process = Incorrect (❌)
- Rule 2: High/High/Medium criteria passed → Process = Correct (✅)
- Rule 3: When in doubt, lean toward correcting process
