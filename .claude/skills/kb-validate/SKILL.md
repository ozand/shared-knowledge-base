# Skill: KB Validate

## What this Skill does
Validate knowledge base entries for quality, completeness, and compliance with KB standards. Ensures entries meet minimum quality score of 75/100.

## Trigger
- User mentions "validate", "check quality", "verify entry"
- Before creating new entries
- After editing existing entries
- During PR review process
- Called by quality-gate hook

## What Claude can do with this Skill

### 1. Validate Single Entry
```bash
python tools/kb.py validate python/errors/imports.yaml
```

### 2. Validate Directory
```bash
# Validate all entries in directory
python tools/kb.py validate python/errors/

# Validate entire KB
python tools/kb.py validate .
```

### 3. Quality Checks Performed

#### Required Fields Check
- ✅ `version` - Must be present
- ✅ `category` - Must be present
- ✅ `last_updated` - Must be present (YYYY-MM-DD format)
- ✅ `errors:` or `patterns:` section - Must have one

#### Entry-Level Checks (for errors:)
- ✅ `id` - Must follow CATEGORY-NNN format
- ✅ `title` - Must be descriptive
- ✅ `severity` - Must be: critical, high, medium, low
- ✅ `scope` - Must be: universal, python, javascript, docker, postgresql, framework, domain, project
- ✅ `problem` - Must describe the issue
- ✅ `solution` - Must have code and explanation
- ✅ `tags` - Must be array of relevant tags

#### Quality Score Calculation
- **Completeness (0-30)**: All required fields present
- **Technical Accuracy (0-30)**: Code works, solution valid
- **Documentation (0-20)**: Clear problem, good explanation
- **Best Practices (0-20)**: Follows standards, has prevention

**Minimum required: 75/100**

### 4. Validation Output
```
🔍 Validating python/errors/imports.yaml...

✅ Required Fields: PASS
   - version: "1.0" ✓
   - category: "import-errors" ✓
   - last_updated: 2026-01-07 ✓

✅ Entry Structure: PASS
   - id format: PYTHON-001 ✓
   - severity: high ✓
   - scope: python ✓

✅ Completeness: PASS
   - problem: Present ✓
   - solution: Complete ✓
   - prevention: Present ✓

⚠️  Quality Score: 78/100
   - Completeness: 28/30
   - Technical Accuracy: 25/30
   - Documentation: 15/20
   - Best Practices: 10/20

💡 Suggestions:
   - Add real-world example to prevention
   - Include edge case handling
   - Add performance considerations

✅ VALIDATION PASSED (Quality: 78/100)
```

## Key files to reference
- Validation tool: `@tools/validate-kb.py`
- Quality standards: `@curator/QUALITY_STANDARDS.md`
- YAML format: `@universal/patterns/shared-kb-yaml-format.yaml`

## Implementation rules
1. **Always validate** before committing new entries
2. **Fix issues** immediately if score < 75
3. **Re-validate** after fixes
4. **Document** quality score in _meta.yaml
5. **Block commit** if quality below threshold

## Common commands
```bash
# Validate specific file
python tools/kb.py validate python/errors/testing.yaml

# Validate using validate-kb.py (recommended for directories)
python tools/validate-kb.py --path python/errors/

# Validate and show quality score
python tools/validate-kb.py --path python/errors/async-errors.yaml

# Windows users: Use validate-kb.py for directory validation
python tools/validate-kb.py --path "python/errors/"
```

## Validation Workflow

### Before Creating New Entry
1. Check for duplicates: `python tools/kb.py search "keywords"`
2. Create entry with all fields
3. Validate: `python tools/kb.py validate <file>`
4. Fix any issues
5. Re-validate until score ≥ 75

### During PR Review
1. Validate all changed files
2. Check for duplicates in scope
3. Verify technical accuracy
4. Test code examples if possible
5. Ensure cross-references added

### Quality Improvement
1. Identify low-scoring entries
2. Review against quality rubric
3. Add missing content
4. Enhance documentation
5. Re-validate to confirm improvement

## Quality Categories

### Critical (Must Fix)
- Missing required fields
- Invalid YAML syntax
- Score < 75
- Duplicate entry
- Broken code examples

### Important (Should Fix)
- Score 75-85
- Missing prevention
- No cross-references
- Incomplete documentation

### Nice to Have
- Score 85-95
- Could use more examples
- Performance notes missing
- Edge cases not covered

### Excellent (95-100)
- Comprehensive coverage
- Multiple examples
- Performance analysis
- Security considerations
- Real-world scenarios

## Related Skills
- `kb-search` - Find duplicates before creating
- `kb-create` - Create new entries
- `audit-quality` - Comprehensive quality audit
- `find-duplicates` - Check for similar entries

## Automated Validation
This skill is automatically triggered by:
- **PreToolUse hook** - Before editing YAML files
- **PostToolUse hook** - After creating YAML files (quality-gate.sh)
- **Stop hook** - Before session ends (check-index.sh)

## Troubleshooting
- **Validation fails**: Check required fields list
- **Low score**: Review quality rubric, add missing content
- **YAML errors**: Fix indentation, quote strings
- **Duplicate found**: Merge or mark as related

---
**Version:** 1.0
**Last Updated:** 2026-01-07
**Skill Type:** Quality Assurance
**Minimum Score:** 75/100
