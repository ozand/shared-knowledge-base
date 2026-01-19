# Research Protocol: Updating Stale Guidelines

This protocol defines how to update documentation using the Research Agent workflow.

## The Trigger Prompt

Copy and paste this into an agent session to start the update process for a specific file.

```markdown
@sys_instruction
# Research Mission: Update Documentation

You are acting as the **Technical Researcher** (ref: `domains/universal/roles/researcher.md`).
Your target: Update `{TARGET_FILE}`.

**Step 1: Setup Workspace**
Run: `python tools/kb_research.py start "{TOPIC_SLUG}"`

**Step 2: Gap Analysis**
Read `{TARGET_FILE}`. Identify technologies, versions, or patterns that might be outdated (currently set to 2025).
Formulate 3-5 search queries to verify the current "State of the Art" for late 2025/early 2026.

**Step 3: Execute Research**
For each query:
1. Search the web.
2. Fetch the most relevant page.
3. Save the findings: `python tools/kb_research.py save "{TOPIC_SLUG}" "{URL}" "{CONTENT_SNIPPET}" --title "{TITLE}"`

**Step 4: Synthesis & Update**
Using *only* your gathered research:
1. Update `{TARGET_FILE}`.
2. Change `last_updated` to today's date.
3. Add a "Version History" entry.

**Step 5: Cleanup**
Run `git status` to verify changes.
```

## Example Scenario

**Target:** `domains/python/guides/02-code-quality.md`
**Topic Slug:** `python-code-quality-2026`

**Gap Analysis:**
- "Is `ruff` still the standard? Has it added new rules?"
- "Is `uv` still the recommended package manager?"
- "Are there new pre-commit hooks?"

**Research:**
- Search: "Ruff python linter best practices 2026"
- Search: "Python packaging uv vs poetry 2026"

**Synthesis:**
- Update the Ruff configuration section with v0.5+ syntax.
- Confirm `uv` dominance or switch if replaced.
