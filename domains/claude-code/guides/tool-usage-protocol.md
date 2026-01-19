---
title: "RooCode Tool Usage Protocol"
version: "2.1.0"
last_updated: "2026-01-19"
category: "roocode_specific"
priority: critical
applies_to: ["roocode_users"]
agent_usage: "MUST read before ANY file operation in RooCode environment"
keywords: ["roocode", "tools", "file_operations", "execute_command", "read_file", "write_to_file"]
related_docs: ["roocode/agent-capabilities.md"]
---

# RooCode Tool Usage Protocol

> **MANDATE:** Always prefer specialized RooCode/MCP tools over execute_command

---

## 1. The Golden Rule (2026 Standard)

**You MUST always prefer specialized RooCode tools** (`read_file`, `list_files`, `write_to_file`, etc.) and **MCP (Model Context Protocol)** connected tools over the general-purpose `execute_command`.

**Use `execute_command` ONLY for:**
- Running scripts and processes
- Git operations
- Package installation
- Tasks with no specialized tool equivalent

---

## 2. Tool Equivalency Table

| ❌ Instead of this command | ✅ Use this RooCode tool | Why |
|---------------------------|------------------------|-----|
| `cat`, `head`, `tail`, `less` | `read_file` | Returns content with line numbers, supports partial reads, safer |
| `ls`, `find`, `tree` | `list_files` | Recursive, respects `.gitignore`/`.rooignore`, better formatting |
| `echo "..." >`, `>>` | `write_to_file` | **Interactive diff approval** prevents accidents |
| `touch`, `mkdir` | `write_to_file` | Auto-creates files and directories |
| `sed`, `awk` | `search_and_replace` or `apply_diff` | Powerful regex support + interactive approval |
| `grep`, `rg` | `search_files` or `codebase_search` | Fast, provides context, semantic search |
| `curl`, `wget` | `browser_action` / `fetch` | **MCP Standard**: Safer, renders JS, handles auth better |
| `mv`, `cp`, `rm` | `execute_command` + confirmation | **Exception:** No specialized tools yet. MUST request user confirmation via `ask_followup_question` before executing |

---

## 3. Detailed Tool Usage

### Web Research (MCP)

```python
# ✅ Correct
<use_mcp_tool>
  <server_name>brave-search</server_name>
  <tool_name>search</tool_name>
  <arguments>
    {"query": "latest react 19 features"}
  </arguments>
</use_mcp_tool>

# ❌ Wrong
<execute_command>
  <command>curl https://google.com/search?q=...</command>
</execute_command>
```

**Benefits:**
- Structured results (JSON)
- No parsing of raw HTML required
- Respects robots.txt and usage policies

---

### Reading Files

```python
# ✅ Correct
<read_file>
  <path>src/project_name/payments/processor.py</path>
</read_file>

# ❌ Wrong
<execute_command>
  <command>cat src/project_name/payments/processor.py</command>
</execute_command>
```

**Benefits:**
- Line numbers for easy reference
- Partial reading of large files
- Consistent formatting

---

### Listing Files

```python
# ✅ Correct
<list_files>
  <path>src/project_name</path>
  <recursive>true</recursive>
</list_files>

# ❌ Wrong
<execute_command>
  <command>ls -R src/project_name</command>
</execute_command>
```

**Benefits:**
- Respects `.gitignore` and `.rooignore`
- Tree-style visualization
- Filters out irrelevant files

---

### Writing Files

```python
# ✅ Correct
<write_to_file>
  <path>src/project_name/api/routes.py</path>
  <content>
def health_check():
    return {"status": "healthy"}
  </content>
</write_to_file>

# ❌ Wrong
<execute_command>
  <command>echo 'def health_check():' > src/project_name/api/routes.py</command>
</execute_command>
```

**Benefits:**
- **Interactive diff view** - user approves changes
- Auto-creates parent directories
- Prevents accidental overwrites

---

### Searching Code

```python
# ✅ Correct - keyword search
<search_files>
  <query>process_payment</query>
  <path>src/project_name</path>
</search_files>

# ✅ Correct - semantic search
<codebase_search>
  <query>how do we handle failed payments?</query>
</codebase_search>

# ❌ Wrong
<execute_command>
  <command>grep -r "process_payment" src/</command>
</execute_command>
```

**Benefits:**
- `search_files`: Fast ripgrep, provides context
- `codebase_search`: Understands meaning, not just keywords

---

### Search and Replace

```python
# ✅ Correct
<search_and_replace>
  <path>src/project_name/payments/processor.py</path>
  <search>old_function_name</search>
  <replace>new_function_name</replace>
</search_and_replace>

# ❌ Wrong
<execute_command>
  <command>sed -i 's/old_function_name/new_function_name/g' src/project_name/payments/processor.py</command>
</execute_command>
```

**Benefits:**
- Regex support
- Interactive approval
- Shows context of changes

---

## 4. When execute_command IS Justified

### ✅ Appropriate Uses

#### Package Management
```bash
uv add requests
npm install lodash
pip install --upgrade pip
```

#### Running Scripts
```bash
uv run pytest
npm run dev
python scripts/development/migrate_db.py
```

#### Git Operations
```bash
git status
git commit -m "feat: add payment processing"
git push origin main
```

#### Build Tools
```bash
npm run build
uv run mypy src/
ruff check . --fix
```

---

### ❌ Inappropriate Uses (Use Specialized Tools)

```bash
# ❌ Don't use execute_command for these:
cat src/main.py              # Use read_file
ls src/                      # Use list_files
echo "code" > file.py        # Use write_to_file
grep "pattern" src/          # Use search_files
sed 's/old/new/' file.py     # Use search_and_replace
```

---

## 5. File System Operations (Special Case)

**For `mv`, `cp`, `rm` operations:**

1. **Always request confirmation first:**

```python
<ask_followup_question>
  <question>
I need to delete the file `old_config.json`. This action is permanent. 
Should I proceed?
  </question>
</ask_followup_question>
```

2. **Only after confirmation, execute:**

```python
<execute_command>
  <command>rm old_config.json</command>
</execute_command>
```

**Why:** No specialized tools exist yet, but these are destructive operations.

---

## 6. Decision Tree

```
Need to perform file operation?
│
├─ Reading file content?
│  └─ Use read_file
│
├─ Listing directory?
│  └─ Use list_files
│
├─ Writing/creating file?
│  └─ Use write_to_file
│
├─ Searching code?
│  ├─ Keyword search? → Use search_files
│  └─ Semantic search? → Use codebase_search
│
├─ Modifying file content?
│  └─ Use search_and_replace or apply_diff
│
├─ Moving/copying/deleting files?
│  ├─ Ask confirmation via ask_followup_question
│  └─ Then use execute_command
│
└─ Running scripts, installing packages, git operations?
   └─ Use execute_command
```

---

## 7. Rationale

### Why This Protocol Exists

1. **Reliability:** Specialized tools have structured output
2. **Safety:** Interactive diff approval prevents accidents
3. **Integration:** Better integrated with RooCode environment
4. **User Experience:** Clearer intent, better error messages
5. **Auditability:** Tool usage is tracked and logged

### Performance Comparison

| Operation | execute_command | Specialized Tool | Winner |
|-----------|----------------|------------------|--------|
| Read file | ~50ms | ~30ms | Specialized |
| List files (recursive) | ~200ms | ~100ms | Specialized |
| Search code | ~150ms | ~80ms | Specialized |
| Write file | ~40ms | ~60ms + approval | execute_command (but less safe) |

**Conclusion:** Specialized tools are faster AND safer in most cases.

---

## 8. Common Mistakes

### Mistake 1: Using cat for file reading

```python
# ❌ Wrong
<execute_command>
  <command>cat src/main.py</command>
</execute_command>

# ✅ Correct
<read_file>
  <path>src/main.py</path>
</read_file>
```

### Mistake 2: Using echo for file writing

```python
# ❌ Wrong
<execute_command>
  <command>echo "print('hello')" > test.py</command>
</execute_command>

# ✅ Correct
<write_to_file>
  <path>test.py</path>
  <content>print('hello')</content>
</write_to_file>
```

### Mistake 3: Using grep for code search

```python
# ❌ Wrong
<execute_command>
  <command>grep -r "payment" src/</command>
</execute_command>

# ✅ Correct
<search_files>
  <query>payment</query>
  <path>src</path>
</search_files>
```

---

## 9. Quick Reference

**Always use specialized tools for:**
- 📖 Reading files
- 📝 Writing files
- 📂 Listing directories
- 🔍 Searching code
- ✏️  Modifying files

**Use execute_command only for:**
- 📦 Package management
- 🏃 Running scripts
- 🔄 Git operations
- 🔧 Build tools
- 🗑️  File system operations (with confirmation)

---

**Remember:** When in doubt, check this protocol. Using the wrong tool will reduce efficiency and may cause errors.
