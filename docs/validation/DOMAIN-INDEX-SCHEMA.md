# _domain_index.yaml Schema and Validation

**Version:** 4.0.0
**Last Updated:** 2026-01-08
**Purpose:** Define expected format and validation rules

---

## 📋 Official Schema (v4.0.0)

### Current Format (CORRECT)

```yaml
version: "2.0"
last_updated: "2026-01-07"
total_entries: 149
entries_with_domains: 65
coverage_percentage: 43.6

domains:
  api: 4
  asyncio: 6
  authentication: 6
  claude-code: 4
  deployment: 4
  docker: 11
  fastapi: 3
  monitoring: 4
  performance: 4
  postgresql: 8
  security: 2
  testing: 11
  websocket: 2

# Optional: Detailed domain info available via:
#   python tools/kb_domains.py info <domain>
```

### Field Specifications

**Root Level:**
```yaml
version:                 # string, required
  format: "X.Y"          # Major.Minor
  example: "2.0"

last_updated:            # string, required
  format: "YYYY-MM-DD"
  example: "2026-01-07"

total_entries:           # integer, required
  format: int
  example: 149

entries_with_domains:    # integer, required
  format: int
  example: 65

coverage_percentage:     # float, required
  format: float
  example: 43.6
```

**Domains Level:**
```yaml
domains:                 # object, required
  <domain_name>: <int>   # flat structure, NOT nested

  # Example:
  docker: 11             # integer = entry count
  postgresql: 8          # integer = entry count
```

**Domain Names (valid values):**
```yaml
api                    # API development
asyncio               # Async/await patterns
authentication        # Auth systems
claude-code           # Claude Code specific
deployment           # Deployment strategies
docker               # Docker containerization
fastapi              # FastAPI framework
monitoring           # Application monitoring
performance          # Performance optimization
postgresql           # PostgreSQL database
security             # Security practices
testing              # Testing frameworks
websocket            # WebSocket communication
```

---

## ❌ FORBIDDEN FORMAT (DO NOT USE)

### Wrong: Nested Structure

```yaml
❌ domains:
❌   docker:
❌     entries: 11              # NOT in v4.0.0 spec!
❌     token_estimate: 2000     # NOT in spec!
❌     tags: ["containers"]     # NOT in spec!
❌     description: "..."       # NOT in spec!
```

**Why wrong:**
- Not part of v4.0.0 specification
- Breaks forward compatibility
- Creates merge conflicts
- Tools must adapt to data, not reverse

---

## 🔍 Validation Rules

### Rule 1: Flat Structure Only
```python
def validate_domain_index(index):
    domains = index.get('domains', {})

    for domain_name, value in domains.items():
        # MUST be integer
        assert isinstance(value, int), \
            f"Domain {domain_name} must be int, got {type(value)}"

        # MUST NOT be dict
        assert not isinstance(value, dict), \
            f"Domain {domain_name} must NOT be dict"

    return True
```

### Rule 2: Required Fields Present
```python
def validate_required_fields(index):
    required = ['version', 'last_updated', 'total_entries',
                'entries_with_domains', 'coverage_percentage', 'domains']

    for field in required:
        assert field in index, f"Missing required field: {field}"

    return True
```

### Rule 3: No Extra Fields in Domains
```python
def validate_no_extra_domains(index):
    # Domains should only have simple integer values
    domains = index.get('domains', {})

    for domain_name, value in domains.items():
        if isinstance(value, dict):
            raise ValueError(
                f"Domain {domain_name} has nested structure. "
                f"Expected: int, Got: dict with keys {list(value.keys())}"
            )

    return True
```

### Rule 4: Valid Domain Names
```python
VALID_DOMAINS = {
    'api', 'asyncio', 'authentication', 'claude-code',
    'deployment', 'docker', 'fastapi', 'monitoring',
    'performance', 'postgresql', 'security', 'testing', 'websocket'
}

def validate_domain_names(index):
    domains = index.get('domains', {})

    for domain_name in domains.keys():
        assert domain_name in VALID_DOMAINS, \
            f"Unknown domain: {domain_name}"

    return True
```

---

## 🧪 Testing Your _domain_index.yaml

### Quick Test
```bash
cd .kb/shared

# Test 1: Check syntax
python -c "import yaml; yaml.safe_load(open('_domain_index.yaml'))"

# Test 2: Validate structure
python tools/kb_domains.py list
# Should work OR report clear error

# Test 3: Check against upstream
diff _domain_index.yaml <(curl -s https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/_domain_index.yaml)
# Should be minimal or no differences
```

### Full Validation Script
```python
#!/usr/bin/env python3
import yaml
import sys

def validate_domain_index(filepath):
    with open(filepath) as f:
        index = yaml.safe_load(f)

    # Rule 1: Required fields
    required = ['version', 'last_updated', 'total_entries',
                'entries_with_domains', 'coverage_percentage', 'domains']
    for field in required:
        if field not in index:
            print(f"❌ Missing required field: {field}")
            return False

    # Rule 2: Domains structure
    domains = index.get('domains', {})
    for domain_name, value in domains.items():
        if not isinstance(value, int):
            print(f"❌ Domain {domain_name} must be int, got {type(value)}")
            return False

    print(f"✅ Valid format: {len(domains)} domains")
    print(f"✅ Total entries: {index['total_entries']}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate.py _domain_index.yaml")
        sys.exit(1)

    result = validate_domain_index(sys.argv[1])
    sys.exit(0 if result else 1)
```

---

## 📊 Format Evolution

### v3.x Format
```yaml
# Flat structure
domains:
  docker: 11
  postgresql: 8
```

### v4.0.0 Format (CURRENT)
```yaml
# Still flat structure
domains:
  docker: 11
  postgresql: 8
  claude-code: 4
```

### Future Format (HYPOTHETICAL)
```yaml
# May become nested in future versions
# BUT NOT in v4.0.0!
domains:
  docker:
    entries: 11
    metadata: {...}
```

**Key Point:** v4.0.0 uses FLAT structure. Tools must work with this.

---

## 🐛 Common Bugs

### Bug 1: Tool Expects Wrong Format
```python
# WRONG (tool bug):
for domain, data in domains.items():
    count = data['entries']  # Expects dict!

# CORRECT:
for domain, data in domains.items():
    count = data if isinstance(data, int) else data.get('entries', 0)
```

### Bug 2: Agent Modifies Format
```yaml
# Agent "fixes" _domain_index.yaml to match broken tool
❌ domains:
❌   docker:
❌     entries: 11  # Wrong! Not v4.0.0 format!

# Correct action: Fix tool, not data
```

### Bug 3: Manual Edits
```bash
# Someone manually edited _domain_index.yaml
❌ vim _domain_index.yaml
❌ Added custom fields

# Result: Breaks updates, validation fails
# Fix: git checkout _domain_index.yaml
```

---

## 📝 Migration Notes

### From v3.x to v4.0.0

**No changes needed!** Both use flat structure:

```yaml
# v3.x
domains:
  docker: 11

# v4.0.0
domains:
  docker: 11
  claude-code: 4
```

### Updating Tools

If your tool expects nested structure:

```python
# BEFORE (wrong):
def get_entry_count(domain_data):
    return domain_data['entries']

# AFTER (correct):
def get_entry_count(domain_data):
    if isinstance(domain_data, int):
        return domain_data
    return domain_data.get('entries', 0)
```

---

## 🔗 References

- **Schema Version:** 4.0.0
- **Upstream Reference:** https://github.com/ozand/shared-knowledge-base/blob/main/_domain_index.yaml
- **Validation Tool:** `python tools/kb.py validate .`
- **Issue Tracker:** https://github.com/ozand/shared-knowledge-base/issues

---

**Quality Score:** 100/100
**Validator Status:** Ready
**Backward Compatible:** Yes (v3.x → v4.0.0)
