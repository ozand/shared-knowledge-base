# Claude Code Shared Model - Setup Script & Troubleshooting

**Extracted from:** claude-code-shared-model.yaml
**Pattern ID:** CLAUDE-CODE-SHARED-MODEL-001

## Quick Setup Script

```bash
#!/bin/bash
# Setup Shared Claude Code Configuration

# Step 1: Create directory structure
mkdir -p .claude/{standards,skills,agents,team}

# Step 2: Create CLAUDE.md
cat > .claude/CLAUDE.md <<'EOF'
# Project Knowledge

## Quick Start
This repo uses shared Claude Code configuration.

## Architecture
See @standards/architecture.md

## Coding Standards
See @standards/coding-standards.md

## Testing
See @standards/testing-guidelines.md
Use /testing skill to generate tests

## Deployment
See @standards/deployment.md
EOF

# Step 3: Create standards template
cat > .claude/standards/architecture.md <<'EOF'
# Architecture Standards

## Principles
1. Separation of concerns
2. DRY (Don't Repeat Yourself)
3. SOLID principles

## Project Structure
[Your project structure here]
EOF

# Step 4: Create settings.json
cat > .claude/settings.json <<'EOF'
{
  "skills.enabled": ["testing", "refactoring"],
  "agents.enabled": ["code-review"]
}
EOF

# Step 5: Create testing skill
mkdir -p .claude/skills/testing
cat > .claude/skills/testing/SKILL.md <<'EOF'
# Testing Skill

Generates tests following team standards.

## Usage
/testing generate <file>

## Patterns
- Arrange-Act-Assert structure
- Descriptive test names
- Mock external dependencies
- 80%+ coverage target
EOF

# Step 6: Commit to git
git add .claude/
git commit -m "Add shared Claude Code configuration"

echo "✅ Shared Claude Code configuration created!"
echo "📖 Next: Edit .claude/standards/ with your team standards"
```

## Verification Checklist

### Check 1: Root CLAUDE.md Size

**Command:**
```bash
wc -l .claude/CLAUDE.md
```

**Expected:** Less than 400 lines (ideally ~300)

### Check 2: .claude/ is Committed

**Command:**
```bash
git ls-files .claude/ | grep -c .
```

**Expected:** Multiple files tracked

### Check 3: .local Files are Gitignored

**Command:**
```bash
cat .gitignore | grep '.claude/.*local'
```

**Expected:** Patterns present

### Check 4: No Rule Duplication

**Verification:** Search for same rule in multiple files

**Expected:** Each rule has single source of truth

### Check 5: Skills are Discoverable

**Test:** List all /skills in Claude Code

**Expected:** Skills appear in autocomplete

### Check 6: New Developer Can Onboard Quickly

**Test:** Time new dev from zero to first commit

**Expected:** Less than 1 day

## Troubleshooting

### Issue 1: Claude Not Seeing Standards

**Symptom:** Claude Code doesn't use team standards

**Checks:**

1. **Is .claude/ in git?**
   ```bash
   git ls-files .claude/ | wc -l
   ```
   Expected: Non-zero

2. **Is CLAUDE.md in .claude/?**
   ```bash
   ls -la .claude/CLAUDE.md
   ```
   Expected: File exists

3. **Are you in Claude Code project?**
   Verification: Check project settings in Claude Code

**Solutions:**

**Solution 1:** Rebuild Claude Code index
```bash
Restart Claude Code, reload project
```

**Solution 2:** Check file references
```bash
Test: Verify @standards/ references are correct paths
```

### Issue 2: Skill Not Discoverable

**Symptom:** /testing skill not found

**Checks:**

1. **Is skill enabled in settings.json?**
   ```bash
   cat .claude/settings.json | grep testing
   ```
   Expected: testing in skills.enabled

2. **Does SKILL.md exist?**
   ```bash
   ls -la .claude/skills/testing/SKILL.md
   ```
   Expected: File exists

**Solutions:**

**Solution 1:** Enable skill in settings.json
```json
{
  "skills.enabled": ["testing"]
}
```

**Solution 2:** Restart Claude Code
```bash
Action: Reload project to pick up new skills
```

### Issue 3: Team Ignoring Standards

**Symptom:** Developers not following shared standards

**Root Causes:**
- Standards not communicated
- Too strict/complex
- Not easily discoverable
- Outdated patterns

**Solutions:**

**Solution 1:** Improve discoverability
- Link CLAUDE.md in README.md
- Add to onboarding checklist
- Reference in code review template

**Solution 2:** Simplify standards
- Remove nice-to-have rules
- Focus on critical standards
- Provide examples for each rule

**Solution 3:** Gather feedback
- Monthly team review
- "What doesn't work?"
- Iterate based on feedback

## Success Metrics

### For Developers
- Skills trigger when needed (clear descriptions)
- Faster responses (lean SKILL.md)
- Easier maintenance (progressive disclosure)
- Better quality (evaluation-driven development)

### For Teams
- Shareable skills (clear structure)
- Consistent patterns (consolidated skills)
- Version tracking (semantic versioning)
- Onboarding easier (documented examples)

### For Claude
- Better matching (specific descriptions)
- Less context (progressive loading)
- Clearer instructions (well-structured)
- Fewer errors (error handling in scripts)
