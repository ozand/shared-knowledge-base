# Troubleshooting

Common issues and solutions when creating Claude Code skills.

---

## Overview

**Purpose:** Debug and fix common skill development problems

**Common issues:**
1. Skill not activating
2. YAML parsing errors
3. Link not working
4. SKILL.md too large
5. Resources not loading

---

## Issue 1: Skill Not Activating

### Symptoms

- Skill doesn't suggest itself
- No auto-activation
- Skill not in suggestions

### Checklist

**1. skill-rules.json exists?**
```bash
# Check file exists
ls -la .claude/skill-rules.json

# Or Windows
dir .claude\skill-rules.json
```

**If missing:** Create skill-rules.json

---

**2. JSON syntax valid?**
```bash
# Validate JSON
jq . .claude/skill-rules.json

# Or Python
python -m json.tool .claude/skill-rules.json
```

**Common errors:**
- Missing comma: `{"a": 1 "b": 2}` ❌
- Trailing comma: `{"a": 1,}` ❌
- Missing quotes: `{name: "skill"}` ❌

**Fix:** Correct JSON syntax

---

**3. Skill name matches exactly?**
```bash
# Check skill name in YAML frontmatter
grep "name:" .claude/skills/my-skill/SKILL.md

# Check skill name in skill-rules.json
grep '"my-skill"' .claude/skill-rules.json

# Check directory name
ls -la .claude/skills/
```

**All three must match exactly:**
- YAML frontmatter: `name: "my-skill"`
- skill-rules.json: `"my-skill": {...}`
- Directory: `.claude/skills/my-skill/`

**Fix:** Ensure names match

---

**4. Keywords in user prompt?**
```bash
# Test with keyword
echo "Help with async code"
# Should trigger if "async" is a keyword
```

**If no match:**
- Add more keywords
- Check keyword spelling
- Verify case-insensitive matching

---

**5. Intent patterns work?**
```bash
# Test intent pattern
echo "Create async function"
# Should trigger if pattern matches
```

**Test regex:**
- Use regex101.com
- Check pattern syntax
- Verify case-insensitive flag

**Common pattern errors:**
- Unescaped dot: `"async.function"` ❌
- Greedy match: `".*"` ❌
- Missing group: `create|add` ❌

**Fix:**
- Escape special characters: `"async\.function"`
- Use non-greedy: `".*?"`
- Add groups: `"(create|add)"`

---

**6. Hook registered?**
```bash
# Check settings.json
cat .claude/settings.json | grep UserPromptSubmit
```

**Expected:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "type": "llm",
        "path": ".claude/hooks/UserPromptSubmit/skill-activation.ts"
      }
    ]
  }
}
```

**If missing:** Add hook configuration

---

**7. Claude Code restarted?**

**After changes:**
- skill-rules.json
- settings.json
- New skills

**Restart Claude Code** to reload configuration

---

## Issue 2: YAML Parsing Error

### Symptoms

- Frontmatter not recognized
- Parse errors
- Metadata not loaded

### Checklist

**1. Starts with `---`?**
```yaml
---
name: "skill-name"
---
```

**If missing:** Add `---` at start

---

**2. Ends with `---`?**
```yaml
---
name: "skill-name"
description: "Description"
version: "1.0"
---
```

**If missing:** Add `---` at end

---

**3. Valid YAML syntax?**
```yaml
# ❌ Wrong: Missing quotes
name: python-development

# ✅ Correct: With quotes
name: "python-development"

# ❌ Wrong: Extra spaces
name:  "python-development"

# ❌ Wrong: Missing colon
name "python-development"
```

**Common errors:**
- Missing quotes on strings
- Extra spaces after colon
- Missing colons
- Invalid characters in strings

---

**4. No tabs (use spaces)?**

YAML doesn't allow tabs

**❌ Wrong:**
```yaml
---
name: "skill"
	description: "Uses tab"
---
```

**✅ Correct:**
```yaml
---
name: "skill"
description: "Uses spaces"
---
```

---

**5. Valid data types?**

**Strings:** Must be quoted
```yaml
name: "skill-name"  # ✅
```

**Arrays:** Use `-` prefix
```yaml
tags:
  - "python"
  - "async"  # ✅
```

**Not:**
```yaml
tags: ["python", "async"]  # ❌ Not valid in flow style
```

---

## Issue 3: Links Not Working

### Symptoms

- Clicking @ reference doesn't work
- 404 error
- File not found

### Checklist

**1. Using @ syntax?**
```markdown
✅ @resources/async-patterns.md
❌ [async patterns](resources/async-patterns.md)
❌ async patterns (see resources/async-patterns.md)
```

**Fix:** Use @ references

---

**2. File path correct?**
```bash
# Check file exists
ls -la .claude/skills/my-skill/resources/async-patterns.md

# Verify path from SKILL.md
# SKILL.md is at: .claude/skills/my-skill/SKILL.md
# Resource is at: .claude/skills/my-skill/resources/async-patterns.md
# Link: @resources/async-patterns.md
```

**Path is relative from SKILL.md directory**

---

**3. File extension correct?**
```markdown
@resources/async-patterns  # ❌ Missing .md
@resources/async-patterns.md  # ✅ Correct
```

---

**4. Case matches?**
```bash
# Linux is case-sensitive
@resources/Async-Patterns.md  # ❌
@resources/async-patterns.md  # ✅
```

---

**5. No spaces in filename?**
```bash
@resources/async patterns.md  # ❌
@resources/async-patterns.md  # ✅
```

---

## Issue 4: SKILL.md Too Large

### Symptoms

- SKILL.md >500 lines
- Session start slow
- Hard to navigate

### Solutions

**1. Measure current size**
```bash
# Count lines
wc -l .claude/skills/my-skill/SKILL.md

# Or Windows
find /c /v "" .claude\skills\my-skill\SKILL.md
```

---

**2. Identify large sections**

Look for sections >100 lines:
- `## Async Patterns (400 lines)`
- `## Testing (350 lines)`
- `## Error Handling (200 lines)`

---

**3. Move to resources/**

**Step 1:** Create resource file
```bash
# Create resources directory
mkdir -p .claude/skills/my-skill/resources

# Create resource file
touch .claude/skills/my-skill/resources/async-patterns.md
```

**Step 2:** Move content
```markdown
# SKILL.md - Before (400 lines)

## Async Patterns

[400 lines of detailed content...]
```

```markdown
# SKILL.md - After (50 lines)

## Async Patterns

Quick overview...

**📘 Complete Patterns:** @resources/async-patterns.md
```

```markdown
# resources/async-patterns.md - NEW (400 lines)

# Async Patterns

[All the detailed content...]
```

**Step 3:** Update YAML frontmatter
```yaml
---
resources:
  - "resources/async-patterns.md"
---
```

---

**4. Condense examples**

**Before:** 5 examples (100 lines)
```markdown
## Examples

### Example 1
[20 lines]

### Example 2
[20 lines]

### Example 3
[20 lines]

### Example 4
[20 lines]

### Example 5
[20 lines]
```

**After:** 2 examples + link to more (40 lines)
```markdown
## Examples

### Example 1
[20 lines]

### Example 2
[20 lines]

**📘 More examples:** @resources/examples.md
```

---

**5. Remove edge cases**

Move edge cases to resources/:
- Rare scenarios
- Advanced topics
- Troubleshooting
- FAQ

---

## Issue 5: Resources Not Loading

### Symptoms

- Resource file doesn't load
- 404 error
- Content not displayed

### Checklist

**1. Resource file exists?**
```bash
ls -la .claude/skills/my-skill/resources/async-patterns.md
```

**If missing:** Create resource file

---

**2. Listed in YAML frontmatter?**
```yaml
---
resources:
  - "resources/async-patterns.md"  # ← Must be listed
---
```

**If missing:** Add to resources list

---

**3. Path correct?**

**From SKILL.md:**
```markdown
@resources/async-patterns.md
```

**File location:**
```
.claude/skills/my-skill/
├── SKILL.md
└── resources/
    └── async-patterns.md  # ← Must exist here
```

---

**4. Filename matches?**
```yaml
---
resources:
  - "resources/async-patterns.md"  # YAML
---
```

```markdown
@resources/async-patterns.md  # Link
```

```bash
async-patterns.md  # Actual filename
```

**All three must match exactly**

---

## Issue 6: skill-rules.json Not Found

### Symptoms

- Auto-activation doesn't work
- Hook errors
- Skill suggestions missing

### Solutions

**1. Create skill-rules.json**

**Location:** `.claude/skill-rules.json`

**Content:**
```json
{
  "my-skill": {
    "type": "domain",
    "priority": "high",
    "description": "My skill description",
    "promptTriggers": {
      "keywords": ["keyword1", "keyword2"],
      "intentPatterns": ["(create|add).*?pattern"],
      "fileTriggers": {
        "pathPatterns": ["**/*.py"],
        "contentPatterns": ["import asyncio"]
      }
    }
  }
}
```

---

**2. Validate JSON**
```bash
jq . .claude/skill-rules.json
```

---

**3. Register hook**

**In .claude/settings.json:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "type": "llm",
        "path": ".claude/hooks/UserPromptSubmit/skill-activation.ts"
      }
    ]
  }
}
```

---

**4. Restart Claude Code**

After creating skill-rules.json, restart Claude Code

---

## Issue 7: Hook Not Executing

### Symptoms

- Hook doesn't run
- No skill suggestions
- No automation

### Checklist

**1. Hook file exists?**
```bash
ls -la .claude/hooks/UserPromptSubmit/skill-activation.ts
```

**If missing:** Create hook file

---

**2. Hook registered?**
```bash
cat .claude/settings.json | grep UserPromptSubmit -A 5
```

**Expected:**
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "type": "llm",
        "path": ".claude/hooks/UserPromptSubmit/skill-activation.ts"
      }
    ]
  }
}
```

**If missing:** Add to settings.json

---

**3. Hook executable?** (shell hooks only)
```bash
chmod +x .claude/hooks/UserPromptSubmit/hook.sh
```

**If not executable:** Make executable

---

**4. Hook syntax valid?**

**TypeScript:**
```typescript
export async function skillActivationPrompt(prompt: string): Promise<string> {
  // ...
}
```

**Shell:**
```bash
#!/bin/bash
# Hook logic
```

**Test hook manually:**
```bash
# Shell hook
bash .claude/hooks/UserPromptSubmit/hook.sh "test prompt"

# TypeScript hook (if ts-node available)
ts-node .claude/hooks/UserPromptSubmit/hook.ts "test prompt"
```

---

**5. Claude Code restarted?**

After hook changes, restart Claude Code

---

## Debugging Tools

### Validate JSON

```bash
# jq (preferred)
jq . .claude/skill-rules.json

# Python
python -m json.tool .claude/skill-rules.json

# Node.js
jq '.' .claude/skill-rules.json
```

---

### Validate YAML

```python
# Python with PyYAML
import yaml

with open('.claude/skills/my-skill/SKILL.md') as f:
    content = f.read()
    # Extract YAML frontmatter
    yaml_start = content.find('---') + 3
    yaml_end = content.find('\n---', yaml_start)
    yaml_content = content[yaml_start:yaml_end]

    # Parse YAML
    frontmatter = yaml.safe_load(yaml_content)
    print(frontmatter)
```

---

### Test Regex

**Online tool:** https://regex101.com/

**Test patterns:**
```regex
(create|add|implement).*?python.*?(async|coroutine)
```

**Test string:**
```
Create async function in python
```

---

### Count Lines

```bash
# wc (Linux/Mac)
wc -l .claude/skills/my-skill/SKILL.md

# find (Windows)
find /c /v "" .claude\skills\my-skill\SKILL.md
```

---

## Prevention

### Best Practices

**1. Test as you develop**
- Don't wait until end
- Test each component
- Iterate quickly

**2. Use version control**
- Commit working state
- Easy to revert
- Track changes

**3. Document decisions**
- Why certain keywords
- Why certain patterns
- Trade-offs considered

**4. Get feedback early**
- Test with real users
- Collect feedback
- Iterate

---

## Common Mistakes

### 1. Forgetting YAML Frontmatter

**Symptom:** Skill not discoverable

**Fix:** Always add YAML frontmatter

---

### 2. Name Mismatches

**Symptom:** Skill not activating

**Fix:** Ensure name matches in all 3 places
- YAML frontmatter
- skill-rules.json
- Directory name

---

### 3. Invalid JSON

**Symptom:** skill-rules.json not loading

**Fix:** Validate JSON with `jq .`

---

### 4. Not Restarting Claude Code

**Symptom:** Changes not taking effect

**Fix:** Restart after changes to:
- skill-rules.json
- settings.json
- New skills

---

### 5. SKILL.md Too Large

**Symptom:** Slow session start

**Fix:** Apply 500-line rule, move to resources/

---

## Related Resources

**Internal:**
- `@resources/skill-rules-schema.md` - Complete JSON schema
- `@resources/500-line-rule.md` - Modular skill pattern
- `@resources/yaml-frontmatter.md` - YAML frontmatter guide
- `@resources/testing-guide.md` - Testing skills

**Related Skills:**
- `@skills/claude-code-architecture/SKILL.md` - System overview
- `@claude-code-architecture/resources/skill-activation.md` - Auto-activation

**External:**
- [jq JSON processor](https://stedolan.github.io/jq/)
- [regex101](https://regex101.com/)
- [PyYAML](https://pyyaml.org/)

---

**Version:** 1.0
**Last Updated:** 2026-01-07
