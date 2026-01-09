# Agent Auto-Configuration Pattern - Examples

**Extracted from:** agent-auto-configuration.yaml
**Pattern ID:** AGENT-AUTO-001

## Example 1: New Project Setup

**Scenario:** Create new project with Shared KB

**Steps:**
1. Create project: my-new-project
2. Add Shared KB as submodule:
   ```bash
   git init
   git submodule add git@github.com:user/shared-knowledge-base.git docs/knowledge-base/shared
   ```
3. Create .agent-config (optional):
   ```json
   {"project_name": "my-new-project"}
   ```
4. Start agent - it auto-bootstraps from KB
5. Agent knows:
   - GitHub attribution (GITHUB-ATTRIB-001)
   - KB contribution workflow (AGENT-HANDOFF-001)
   - Quality standards (YAML-001, ISOLATED-TEST-001)
6. Zero manual system prompt changes needed

**Result:** Agent fully configured in 5 minutes

## Example 2: KB Update

**Scenario:** Add new pattern to Shared KB

**Steps:**
1. Update Shared KB:
   - Add new pattern: universal/patterns/NEW-PATTERN.yaml
   - Update base-instructions.yaml
   - Commit and push
2. Projects pull KB updates:
   ```bash
   cd docs/knowledge-base/shared && git pull
   ```
3. Agents detect new instructions:
   - check_kb_updates() finds new version
   - Load new instructions
   - Apply new capabilities
4. Agents start using new pattern immediately

**Result:** All agents get new pattern automatically

## Example 3: Auto Context Detection

**Scenario:** Agent determines project name automatically

**Detection Methods:**

### Method 1: Git Remote
```bash
git remote get-url origin
# Example: git@github.com:user/PARSER.git → PARSER
```

### Method 2: package.json
```json
{
  "name": "my-app"
}
# Example: "my-app" → my-app
```

### Method 3: pyproject.toml
```toml
name = 'my-project'
# Example: 'my-project' → my-project
```

### Method 4: .agent-config
```json
{
  "project_name": "explicit-name"
}
# Example: Explicit override
```

**Fallback:** "unknown"
