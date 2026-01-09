# Testing & Validation Framework

**See:** @patterns/claude-code-files-organization-001.yaml

---

## Evaluation-Driven Development for Skills

### Process

**BEFORE writing skill:**

1. **Identify GAP**
   "Where does Claude fail without this skill?"

2. **Create 3 evaluation scenarios**
   - Eval 1: Basic case
   - Eval 2: Medium case
   - Eval 3: Complex case

3. **Run baseline (without skill)**
   ```python
   baseline_score = score(tests without skill)
   ```

4. **Write MINIMAL skill**
   Only enough to close the gap

5. **Test with Claude B (fresh instance)**
   ```python
   new_score = score(tests with skill)
   ```

6. **Compare:**
   ```python
   improvement = new_score - baseline
   ```

7. **Iterate based on failures**

### Example

```
Eval 1: "Generate tests for login function"
├─ Metrics: Vitest syntax? Y/N, Error cases? Y/N, Coverage? Y/N
├─ Baseline (without skill): 1/4 ✗
└─ Target: 4/4 ✓

Write minimal skill → Test → Improve → Retest
```

---

## Skill Testing Checklist

| Item | Importance | Reason |
|------|------------|--------|
| Created 3 evaluation scenarios | Critical | Measure effectiveness |
| Ran baseline (without skill) | Critical | Know starting point |
| SKILL.md ≤ 500 lines | High | Token efficiency |
| Description is specific | Critical | Skill discovery depends on it |
| Tested with fresh Claude instance | High | Unbiased evaluation |
| Team tested (2+ developers) | Medium | Diverse perspectives |

---

## Agent Testing Checklist

| Item | Importance |
|------|------------|
| Unit tests: Individual agent behaviors | High |
| Integration tests: Agent coordination | High |
| E2E tests: Full workflow | Medium |
| Load testing: Expected volume | Medium |
| Error rates: <1% target | Critical |
| Cost tracking: Per execution | High |
