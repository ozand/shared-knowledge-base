# Hook Performance Guide

Optimization strategies and performance targets for Claude Code hooks.

---

## Performance Targets

| Hook Event | Max Duration | Rationale |
|------------|--------------|-----------|
| **SessionStart** | 2 seconds | Session startup latency |
| **UserPromptSubmit** | 1 second | Don't block user input |
| **PreToolUse** | 500ms | Tool call latency |
| **PostToolUse** | 1 second | Can be async |
| **Stop** | Non-blocking | Session ending anyway |

---

## Optimization Strategies

### 1. Use Shell Hooks

**Shell hooks are fast (<100ms typical):**
```bash
#!/bin/bash
# Fast validation
if [[ "$FILE" == *.yaml ]]; then
    python tools/kb.py validate "$FILE" > /dev/null 2>&1
fi
```

**vs LLM hooks (1-3 seconds):**
```typescript
// Slower but more flexible
export async function validateYaml(file: string) {
  const result = await analyzeFile(file);
  return result;
}
```

**When to use:**
- Shell: Validation, formatting, simple tracking
- LLM: Skill activation, prompt enhancement, complex analysis

---

### 2. Cache Expensive Operations

**Problem:** Loading skill rules every call is slow

**Solution:** Cache in memory

```typescript
// ❌ BAD: Loads every time
async function loadSkillRules() {
  const content = await fs.readFile('.claude/skill-rules.json');
  return JSON.parse(content);
}

// ✅ GOOD: Cache result
let skillRulesCache = null;

async function loadSkillRules() {
  if (skillRulesCache) {
    return skillRulesCache;
  }

  const content = await fs.readFile('.claude/skill-rules.json');
  skillRulesCache = JSON.parse(content);
  return skillRulesCache;
}
```

---

### 3. Limit File Scanning

**Problem:** Scanning entire codebase is slow

**Solution:** Only scan open files

```bash
# ❌ BAD: Scans entire codebase
find . -name "*.py" -exec grep "TODO" {} \;

# ✅ GOOD: Only scans open files
for file in $OPEN_FILES; do
    grep "TODO" "$file"
done
```

---

### 4. Use Compiled Regex

**Problem:** Compiling regex every call is slow

**Solution:** Pre-compile regex patterns

```typescript
// ❌ BAD: Compiles every time
for (const pattern of patterns) {
  const regex = new RegExp(pattern, 'i');
  if (regex.test(prompt)) {
    // Match
  }
}

// ✅ GOOD: Pre-compiled
const compiledPatterns = patterns.map(p => new RegExp(p, 'i'));

for (const regex of compiledPatterns) {
  if (regex.test(prompt)) {
    // Match
  }
}
```

---

### 5. Break Early

**Problem:** Checking all keywords even after match

**Solution:** Return early when found

```typescript
// ❌ BAD: Checks all keywords
for (const keyword of keywords) {
  if (prompt.includes(keyword)) {
    score += 10;
  }
}

// ✅ GOOD: Returns early
for (const keyword of keywords) {
  if (prompt.includes(keyword)) {
    return true;  // Found match, return immediately
  }
}
```

---

## Profiling Hooks

### Measure Execution Time

**Bash:**
```bash
#!/bin/bash

START=$(date +%s%N)

# Hook logic
...

END=$(date +%s%N)
ELAPSED=$((($END - $START) / 1000000))
echo "Hook took ${ELAPSED}ms"
```

**TypeScript:**
```typescript
export async function myHook(args: any) {
  const start = Date.now();

  // Hook logic
  ...

  const elapsed = Date.now() - start;
  console.log(`Hook took ${elapsed}ms`);
}
```

**Python:**
```python
import time

def my_hook(args):
    start = time.time()

    # Hook logic
    ...

    elapsed = (time.time() - start) * 1000
    print(f"Hook took {elapsed:.0f}ms")
```

---

## Common Bottlenecks

### 1. File I/O

**Problem:** Reading many files is slow

**Solution:** Read only necessary files

```bash
# ❌ BAD: Reads all .py files
for file in $(find . -name "*.py"); do
    cat "$file"
done

# ✅ GOOD: Reads only open files
for file in $OPEN_FILES; do
    cat "$file"
done
```

---

### 2. Network Calls

**Problem:** Network calls add latency

**Solution:** Cache results, use timeouts

```typescript
// ✅ GOOD: Cache with timeout
const cache = new Map();
const CACHE_TTL = 60000; // 1 minute

async function fetchWithCache(url: string) {
  const cached = cache.get(url);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);

  try {
    const response = await fetch(url, {
      signal: controller.signal
    });
    const data = await response.json();

    cache.set(url, { data, timestamp: Date.now() });
    return data;
  } finally {
    clearTimeout(timeout);
  }
}
```

---

### 3. Expensive Computations

**Problem:** Complex calculations take time

**Solution:** Pre-compute, use lookup tables

```typescript
// ❌ BAD: Calculates every time
function isLeapYear(year: number) {
  return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
}

// ✅ GOOD: Pre-computed lookup
const leapYears = new Set([2000, 2004, 2008, 2012, 2016, 2020, 2024]);

function isLeapYearFast(year: number) {
  return leapYears.has(year);
}
```

---

## Performance Testing

### Load Testing

**Test hook performance under load:**

```python
# test_hook_performance.py

import time
import subprocess

def test_hook_performance():
  """Test hook execution time"""
  iterations = 100
  times = []

  for i in range(iterations):
    start = time.time()

    # Execute hook
    result = subprocess.run(
      ["bash", ".claude/hooks/PreToolUse/validate.sh", "Write", "test.yaml"],
      capture_output=True
    )

    elapsed = (time.time() - start) * 1000
    times.append(elapsed)

  avg = sum(times) / len(times)
  p95 = sorted(times)[int(len(times) * 0.95)]

  print(f"Average: {avg:.0f}ms")
  print(f"P95: {p95:.0f}ms")

  if avg > 500:
    print("⚠️  Average exceeds 500ms target")
  else:
    print("✅ Performance OK")

if __name__ == "__main__":
  test_hook_performance()
```

---

## Performance Checklist

Before releasing hooks:

- [ ] Tested execution time
- [ ] Within performance targets
- [ ] No unnecessary file I/O
- [ ] Cached expensive operations
- [ ] Limited file scanning
- [ ] Compiled regex patterns
- [ ] Early returns where possible
- [ ] Error handling doesn't impact performance
- [ ] Tested under load
- [ ] No memory leaks

---

**Version:** 1.0
**Last Updated:** 2026-01-07
