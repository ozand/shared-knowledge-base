# Testing Guide

Complete guide to testing Claude Code skills.

---

## Overview

**Purpose:** Ensure skills work correctly before releasing

**Testing levels:**
1. **Unit tests** - Individual components
2. **Integration tests** - Skill activation
3. **Manual tests** - Real-world usage
4. **User acceptance** - User feedback

---

## Pre-Testing Checklist

### Before Testing

**Files ready:**
- [ ] SKILL.md created (<500 lines)
- [ ] YAML frontmatter complete
- [ ] skill-rules.json entry added
- [ ] Resources/ created (if needed)
- [ ] Links verified
- [ ] No syntax errors

**Documentation:**
- [ ] Purpose clear
- [ ] Examples provided
- [ ] Links work
- [ ] Format consistent

---

## Manual Testing

### Test 1: Keyword Activation

**Purpose:** Verify keywords trigger skill suggestion

**Steps:**
1. Open Claude Code
2. Submit prompt with keyword
3. Verify skill suggested

**Test cases:**
```python
# Test each keyword
keywords = ["python", "async", "await", "coroutine"]

for keyword in keywords:
    prompt = f"Help me with {keyword} code"
    # Expected: Skill suggested
    # Check: Skill name in suggestions
```

**Example:**
```
Prompt: "Help with async code"
Expected Output:
Based on your request, consider using:
• async-programming: Async/await patterns, coroutines, and event loops
```

**Pass criteria:**
- ✅ Skill suggested
- ✅ Correct description shown
- ✅ Skill name matches

---

### Test 2: Intent Pattern Activation

**Purpose:** Verify intent patterns trigger skill suggestion

**Steps:**
1. Open Claude Code
2. Submit prompt matching intent pattern
3. Verify skill suggested

**Test cases:**
```python
# Test each intent pattern
patterns = [
    "Create async function",
    "Make async method",
    "Implement coroutine"
]

for pattern in patterns:
    # Expected: Skill suggested
    # Check: Skill name in suggestions
```

**Example:**
```
Prompt: "Create async function for API calls"
Expected Output:
Based on your request, consider using:
• async-programming: Async/await patterns, coroutines, and event loops
```

**Pass criteria:**
- ✅ Skill suggested
- ✅ Pattern matched correctly
- ✅ No false positives

---

### Test 3: File Trigger Activation

**Purpose:** Verify file triggers work correctly

**Steps:**
1. Create/open file matching pathPattern
2. Add content matching contentPattern
3. Submit prompt
4. Verify skill suggested

**Test cases:**
```python
# Test path patterns
files = ["api.py", "main.py", "utils.py"]

for file in files:
    # Create file with content
    content = "import asyncio\nfrom fastapi import FastAPI"

    # Expected: Skill suggested
```

**Example:**
```
File: api.py
Content: import asyncio
from fastapi import FastAPI

Prompt: "Add error handling"
Expected Output:
Based on your request, consider using:
• async-programming: Async/await patterns, coroutines, and event loops
```

**Pass criteria:**
- ✅ Skill suggested when file open
- ✅ Skill suggested when content matches
- ✅ Correct files matched

---

### Test 4: Resource Loading

**Purpose:** Verify resource files load correctly

**Steps:**
1. Click @ reference link
2. Verify resource file loads
3. Verify content displays correctly

**Test cases:**
```python
# Test each resource link
resources = [
    "resources/async-patterns.md",
    "resources/testing.md",
    "resources/error-handling.md"
]

for resource in resources:
    # Click link: @resources/async-patterns.md
    # Expected: Resource file loads
    # Check: Content displays
```

**Pass criteria:**
- ✅ All links work
- ✅ Files load correctly
- ✅ Content displays properly
- ✅ No 404 errors

---

### Test 5: Skill Content

**Purpose:** Verify skill content is useful and accurate

**Steps:**
1. Activate skill
2. Read SKILL.md
3. Try examples
4. Follow workflows

**Test cases:**
```python
# Test skill usefulness
tests = [
    "Quick start clear?",
    "Examples accurate?",
    "Workflows complete?",
    "Links work?",
    "Format consistent?"
]
```

**Pass criteria:**
- ✅ Quick start is clear
- ✅ Examples work correctly
- ✅ Workflows are complete
- ✅ All links work
- ✅ Format is consistent

---

## Automated Testing

### Test Script

**File:** `test_skill_activation.py`

```python
#!/usr/bin/env python3
"""
Test skill activation and configuration
"""

import json
import re
import sys
from pathlib import Path


def test_skill_rules():
    """Test skill-rules.json syntax and structure"""
    print("Testing skill-rules.json...")

    # Load file
    skill_rules_path = Path(".claude/skill-rules.json")
    if not skill_rules_path.exists():
        print("❌ skill-rules.json not found")
        return False

    with open(skill_rules_path) as f:
        try:
            rules = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON: {e}")
            return False

    # Check required fields
    for skill_name, rule in rules.items():
        required_fields = ["type", "priority", "description", "promptTriggers"]
        for field in required_fields:
            if field not in rule:
                print(f"❌ {skill_name}: Missing required field '{field}'")
                return False

        # Check promptTriggers
        if "keywords" not in rule["promptTriggers"]:
            print(f"❌ {skill_name}: No keywords defined")
            return False

    print(f"✅ skill-rules.json valid ({len(rules)} skills)")
    return True


def test_yaml_frontmatter():
    """Test YAML frontmatter in SKILL.md files"""
    print("\nTesting YAML frontmatter...")

    skills_dir = Path(".claude/skills")
    if not skills_dir.exists():
        print("❌ .claude/skills/ not found")
        return False

    issues = []
    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            issues.append(f"{skill_dir.name}: SKILL.md not found")
            continue

        with open(skill_file) as f:
            content = f.read()

        # Check for YAML frontmatter
        if not content.startswith("---"):
            issues.append(f"{skill_dir.name}: Missing YAML frontmatter start")
            continue

        # Find end of YAML
        yaml_end = content.find("\n---", 4)
        if yaml_end == -1:
            issues.append(f"{skill_dir.name}: Missing YAML frontmatter end")
            continue

        # Extract YAML
        yaml_content = content[4:yaml_end]
        try:
            import yaml
            frontmatter = yaml.safe_load(yaml_content)

            # Check required fields
            required = ["name", "description", "version"]
            for field in required:
                if field not in frontmatter:
                    issues.append(f"{skill_dir.name}: Missing required field '{field}'")

            # Check name matches directory
            if frontmatter.get("name") != skill_dir.name:
                issues.append(
                    f"{skill_dir.name}: Name mismatch "
                    f"(YAML: {frontmatter.get('name')}, Dir: {skill_dir.name})"
                )

        except ImportError:
            print("⚠️  PyYAML not installed, skipping YAML validation")
        except yaml.YAMLError as e:
            issues.append(f"{skill_dir.name}: Invalid YAML: {e}")

    if issues:
        for issue in issues:
            print(f"❌ {issue}")
        return False

    print("✅ YAML frontmatter valid")
    return True


def test_skill_activation():
    """Test skill activation logic"""
    print("\nTesting skill activation...")

    with open(".claude/skill-rules.json") as f:
        rules = json.load(f)

    test_cases = [
        {
            "prompt": "Create async function in python",
            "file": "api.py",
            "file_content": "import asyncio",
            "expected_skills": ["python-async"]
        },
        {
            "prompt": "Build Docker image",
            "file": None,
            "file_content": None,
            "expected_skills": ["docker-development"]
        }
    ]

    all_passed = True
    for test in test_cases:
        matched = match_skills(test["prompt"], rules)
        expected = test["expected_skills"]

        if not any(skill in matched for skill in expected):
            print(f"❌ Test failed: '{test['prompt']}'")
            print(f"   Expected one of: {expected}")
            print(f"   Got: {matched}")
            all_passed = False
        else:
            print(f"✅ Test passed: '{test['prompt']}'")

    return all_passed


def match_skills(prompt, rules):
    """Match skills based on prompt"""
    matched = []

    for skill_name, rule in rules.items():
        score = 0

        # Base priority
        priority_scores = {
            "critical": 100,
            "high": 75,
            "medium": 50,
            "low": 25
        }
        score += priority_scores.get(rule.get("priority"), 50)

        # Keywords
        for keyword in rule["promptTriggers"].get("keywords", []):
            if keyword.lower() in prompt.lower():
                score += 10

        # Intent patterns
        for pattern in rule["promptTriggers"].get("intentPatterns", []):
            try:
                if re.search(pattern, prompt, re.IGNORECASE):
                    score += 20
                    break
            except re.error:
                pass

        if score > 50:  # Threshold
            matched.append(skill_name)

    return matched


def test_file_sizes():
    """Test SKILL.md file sizes"""
    print("\nTesting file sizes...")

    skills_dir = Path(".claude/skills")
    issues = []

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        lines = len(skill_file.read_text().splitlines())

        if lines > 500:
            issues.append(f"{skill_dir.name}: {lines} lines (max: 500)")

    if issues:
        for issue in issues:
            print(f"⚠️  {issue}")
        return False

    print("✅ All SKILL.md files within size limit")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Claude Code Skill Testing Suite")
    print("=" * 60)

    tests = [
        ("skill-rules.json", test_skill_rules),
        ("YAML frontmatter", test_yaml_frontmatter),
        ("Skill activation", test_skill_activation),
        ("File sizes", test_file_sizes)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} test failed with error: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

**Usage:**
```bash
python test_skill_activation.py
```

**Expected output:**
```
============================================================
Claude Code Skill Testing Suite
============================================================
Testing skill-rules.json...
✅ skill-rules.json valid (3 skills)

Testing YAML frontmatter...
✅ YAML frontmatter valid

Testing skill activation...
✅ Test passed: 'Create async function in python'
✅ Test passed: 'Build Docker image'

Testing file sizes...
✅ All SKILL.md files within size limit

============================================================
Test Summary
============================================================
✅ PASS: skill-rules.json
✅ PASS: YAML frontmatter
✅ PASS: Skill activation
✅ PASS: File sizes

Total: 4/4 tests passed

🎉 All tests passed!
```

---

## Integration Testing

### Test with Real Prompts

**Scenario 1: New user**
```
User: "I'm new to async programming in Python"
Expected: async-programming skill suggested
Skill loads successfully
User can follow quick start
```

**Scenario 2: Specific problem**
```
User: "How do I handle errors in async code?"
Expected: async-programming skill suggested
Skill loads successfully
User finds error handling section
```

**Scenario 3: File-based trigger**
```
File: api.py with "import asyncio"
User: "Add type hints to this code"
Expected: async-programming skill suggested
Skill loads successfully
Type hints examples available
```

---

## Quality Metrics

### Activation Quality

**Excellent:**
- ✅ Activates on relevant prompts (>90%)
- ✅ No false positives (<5%)
- ✅ Suggestion text clear
- ✅ Priority ranking correct

**Good:**
- ✅ Activates on relevant prompts (>75%)
- ✅ Few false positives (<10%)
- ✅ Suggestion text understandable
- ✅ Priority ranking mostly correct

**Needs Improvement:**
- ❌ Low activation rate (<75%)
- ❌ Many false positives (>10%)
- ❌ Suggestion text unclear
- ❌ Wrong priority ranking

---

### Content Quality

**Excellent:**
- ✅ Quick start gets user started
- ✅ Examples accurate and tested
- ✅ Workflows complete
- ✅ All links work
- ✅ Format consistent

**Good:**
- ✅ Quick start helpful
- ✅ Most examples work
- ✅ Workflows mostly complete
- ✅ Most links work
- ✅ Format mostly consistent

**Needs Improvement:**
- ❌ Quick start unclear
- ❌ Examples don't work
- ❌ Workflows incomplete
- ❌ Broken links
- ❌ Inconsistent format

---

## Troubleshooting Testing Issues

### Issue: Skill Not Activating

**Symptoms:** Skill doesn't suggest itself

**Debug:**
1. Check skill-rules.json exists
2. Verify JSON syntax
3. Check skill name matches
4. Test keywords in prompt
5. Verify hook registered

**Fix:**
```bash
# Validate JSON
jq . .claude/skill-rules.json

# Check hook registered
cat .claude/settings.json | grep UserPromptSubmit
```

---

### Issue: Test Script Fails

**Symptoms:** Automated tests fail

**Debug:**
1. Check error message
2. Verify file paths
3. Check dependencies (PyYAML, jq)
4. Review test expectations

**Fix:**
```bash
# Install dependencies
pip install pyyaml

# Or skip YAML validation
# Comment out import yaml section
```

---

## Best Practices

### 1. Test Early, Test Often

- Test as you develop
- Don't wait until end
- Iterate quickly

### 2. Test Real Scenarios

- Use actual prompts from users
- Test with real files
- Simulate real workflows

### 3. Automate When Possible

- Use test scripts
- Automate repetitive tests
- Continuous integration

### 4. Document Tests

- Keep test cases documented
- Update tests as skill evolves
- Share test results

---

## Related Resources

**Internal:**
- `@resources/troubleshooting.md` - Troubleshooting skills
- `@resources/skill-rules-schema.md` - skill-rules.json schema
- `@resources/500-line-rule.md` - Modular skill pattern

**External:**
- [Python unittest](https://docs.python.org/3/library/unittest.html)
- [pytest](https://docs.pytest.org/)

---

**Version:** 1.0
**Last Updated:** 2026-01-07
