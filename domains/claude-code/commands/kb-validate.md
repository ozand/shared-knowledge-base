# KB Validate

Validate knowledge base entries for quality, completeness, and compliance with KB standards.

## Usage
```
/kb-validate <file-or-directory> [options]
```

## Examples

### Validate Single Entry
```
/kb-validate python/errors/imports.yaml
```
Validates one file, shows quality score

### Validate Directory
```
/kb-validate python/errors/
```
Validates all entries in Python errors directory

### Validate Entire KB
```
/kb-validate .
```
Validates all entries in knowledge base

### With Score Display
```
/kb-validate python/errors/async.yaml --score
```
Shows detailed quality score breakdown

## What happens

1. **Validation Checks**
   - Required fields present
   - YAML syntax valid
   - ID format correct (CATEGORY-NNN)
   - Severity and scope valid
   - Problem and solution complete
   - Tags present and relevant

2. **Quality Scoring**
   - Completeness (0-30 points)
   - Technical Accuracy (0-30 points)
   - Documentation (0-20 points)
   - Best Practices (0-20 points)
   - **Minimum required: 75/100**

3. **Output**
   - Pass/fail status
   - Quality score
   - Missing fields (if any)
   - Suggestions for improvement

## Output Format
```
🔍 Validating python/errors/async.yaml...

✅ Required Fields: PASS
   - version: "1.0" ✓
   - category: "async-errors" ✓
   - last_updated: 2026-01-07 ✓

✅ Entry Structure: PASS
   - id format: PYTHON-018 ✓
   - severity: high ✓
   - scope: python ✓

⚠️  Quality Score: 78/100
   - Completeness: 28/30
   - Technical Accuracy: 25/30
   - Documentation: 15/20
   - Best Practices: 10/20

💡 Suggestions:
   - Add real-world example to prevention
   - Include edge case handling

✅ VALIDATION PASSED (Quality: 78/100)
```

## Options

- `--score` - Show detailed quality score breakdown
- `--verbose` - Show all validation checks
- `--fix` - Auto-fix common issues (if possible)

## Quality Categories

### ⭐⭐⭐⭐⭐ Excellent (95-100)
Comprehensive coverage with examples, best practices, performance notes

### ⭐⭐⭐⭐ Good (85-94)
Complete and well-documented, could use more examples

### ⭐⭐⭐ Acceptable (75-84)
Meets minimum standards, needs minor enhancements

### ⭐⭐ Needs Work (65-74)
Below minimum, requires improvements

### ⭐ Poor (<65)
Significant issues, needs major revision

## Validation Checklist

- ✅ All required fields present
- ✅ YAML syntax valid
- ✅ ID follows CATEGORY-NNN format
- ✅ Severity is critical/high/medium/low
- ✅ Scope is valid (universal, python, javascript, docker, postgresql, framework, domain, project)
- ✅ Problem clearly described
- ✅ Solution has code and explanation
- ✅ Prevention strategies included
- ✅ Tags are relevant
- ✅ Quality score ≥75/100

## Tips

- **Validate before committing** - Always check new entries
- **Fix issues immediately** - Don't commit low-scoring entries
- **Re-validate after fixes** - Ensure improvements worked
- **Use --verbose** - See all checks for debugging

## Related Commands
- `/kb-search` - Find duplicates before creating
- `/kb-create` - Create new entries
- `/kb-index` - Rebuild index after changes

## Troubleshooting

**Validation fails?**
- Check required fields list
- Fix YAML syntax (indentation, quotes)
- Verify ID format (CATEGORY-NNN)

**Low score?**
- Add missing sections
- Improve documentation
- Add more examples
- Include prevention strategies

**YAML errors?**
- Check indentation (use spaces, not tabs)
- Quote strings with special characters
- Validate with online YAML parser

## See Also
- Skill: `kb-validate` - Full validation documentation
- Quality Standards: `@curator/QUALITY_STANDARDS.md`
- Entry Format: `@universal/patterns/shared-kb-yaml-format.yaml`
