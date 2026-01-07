# KB Create

Create new knowledge base entries from scratch following Shared KB standards.

## Usage
```
/kb-create [options]
```

## Examples

### Interactive Creation
```
/kb-create
```
Prompts for all required fields interactively

### Create with Pre-filled Template
```
/kb-create --scope python --category testing
```
Generates template with Python testing defaults

### Create from Error Message
```
/kb-create --error "TypeError: 'NoneType' object is not subscriptable"
```
Creates entry from error message

## What happens

### Step 1: Check for Duplicates
```bash
python tools/kb.py search "<keywords from title>"
```
Ensures entry doesn't already exist

### Step 2: Generate Template
```yaml
version: "1.0"
category: "<category>"
last_updated: "2026-01-07"

errors:
  - id: "CATEGORY-NNN"  # Auto-generated
    title: "<Title>"
    severity: "high"
    scope: "python"

    problem: |
      <Describe the issue>

    symptoms:
      - "<Error message or symptom>"

    root_cause: |
      <Explain why this happens>

    solution:
      code: |
        # Working solution
        pass

      explanation: |
        <How the solution works>

    prevention:
      - "<How to avoid this error>"

    tags: ["<tag1>", "<tag2>"]
```

### Step 3: Validate Entry
```bash
python tools/kb.py validate <new-entry>.yaml
```
Ensures quality score ≥75/100

### Step 4: Initialize Metadata
```bash
python tools/kb.py init-metadata <new-entry>.yaml
```
Creates _meta.yaml file

### Step 5: Update Index
```bash
python tools/kb.py index
```
Rebuilds search index

## Options

- `--scope <scope>` - Set scope (universal, python, javascript, docker, postgresql, framework)
- `--category <name>` - Set category name
- `--error <message>` - Create entry from error message
- `--template` - Generate template only
- `--next-id` - Show next available ID for scope

## Creation Checklist

### Before Creating
- [ ] Search for duplicates
- [ ] Determine correct scope
- [ ] Verify solution is unique
- [ ] Check it's not project-specific only

### While Creating
- [ ] Use YAML format exactly
- [ ] Include all required fields
- [ ] Provide working code examples
- [ ] Add prevention strategies
- [ ] Include relevant tags

### After Creating
- [ ] Validate (score ≥75/100)
- [ ] Initialize metadata
- [ ] Rebuild index
- [ ] Add cross-references
- [ ] Commit to git

## Scope Decision Tree

```
Is this error/pattern...
├─ Universal across languages? → universal/
├─ Specific to one language? → <language>/
├─ Framework-specific? → framework/<name>/
├─ Domain/business logic? → domain/
└─ Project-specific only? → project/ (DON'T push to shared KB)
```

## What NOT to Add

❌ Project-specific errors (use local KB)
❌ One-time occurrences
❌ Incomplete solutions
❌ Theoretical problems (never occurred)
❌ Proprietary information

## Tips

- **Search first** - Always check for duplicates
- **Be specific** - Clear problem descriptions
- **Test solutions** - Verify code works
- **Add context** - Real-world scenarios help
- **Think prevention** - How to avoid this error?

## Output Format
```
📝 Creating new KB entry...

Step 1: Checking for duplicates...
  ✓ No duplicates found for "async timeout"

Step 2: Determining scope...
  ✓ Scope: python (language-specific)

Step 3: Generating ID...
  ✓ Next ID: PYTHON-046

Step 4: Creating template...
  ✓ Created: python/errors/async-timeout.yaml

Step 5: Validating...
  ⚠️  Score: 72/100 (below 75)
  💡 Add prevention strategies to improve

Step 6: Next steps...
  1. Edit: python/errors/async-timeout.yaml
  2. Improve content (target: 75+ score)
  3. Validate: /kb-validate python/errors/async-timeout.yaml
  4. Metadata: python tools/kb.py init-metadata python/errors/async-timeout.yaml
  5. Index: /kb-index
```

## Related Commands
- `/kb-search` - Find duplicates before creating
- `/kb-validate` - Validate entry quality
- `/kb-index` - Update index after creation

## Troubleshooting

**Duplicate found?**
- Review existing entry
- Consider merging instead
- Or add cross-reference

**Wrong scope?**
- Use scope decision tree
- When in doubt, choose more specific
- Can promote to universal later

**Score < 75?**
- Add missing fields
- Improve documentation
- Add more examples
- Include prevention strategies

## See Also
- Skill: `kb-create` - Full creation documentation
- Entry Format: `@universal/patterns/shared-kb-yaml-format.yaml`
- Quality Standards: `@curator/QUALITY_STANDARDS.md`
