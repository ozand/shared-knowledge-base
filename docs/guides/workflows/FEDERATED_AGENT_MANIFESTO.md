# The Federated Agent Manifesto
## Operating Manual for the Company OS Ecosystem (v5.2)

This document is the **Single Source of Truth** for AI Agents operating within the Company OS.
It consolidates protocols for initialization, synchronization, and collaboration.

---

## 1. The Prime Directive
**"We are not isolated scripts. We are nodes in a Federated Network."**

- **Shared Knowledge Base (`.kb/shared`)**: Our collective memory and tooling.
- **Company OS (`company-os`)**: Our central registry and command center.
- **Project (`.kb/project`)**: Your local domain of responsibility.

---

## 2. Lifecycle Protocols

### 🟢 Phase 1: Activation (New Project)
*When entering a project for the first time.*

**Command:**
`python .kb/shared/scripts/unified-install.py --full`

**Agent Actions:**
1.  **Install:** Download Shared KB.
2.  **Profile:** Run `python .kb/shared/tools/kb.py profile init` to auto-detect stack (Python/JS/Docker).
3.  **Identity:** Run `python .kb/shared/tools/kb.py sync init-passport` to create `PROJECT.yaml`.
4.  **Register:** Run `python .kb/shared/tools/kb.py sync push` to announce existence to Company OS.

### 🔵 Phase 2: Daily Operation (The Loop)
*Routine tasks during a session.*

**1. Stay Fresh:**
Always start by updating your tools to get the latest fixes.
`python .kb/shared/scripts/unified-install.py`

**2. Check Dependencies:**
See if other projects you rely on have released updates.
`python .kb/shared/tools/kb_sync.py check-updates`

**3. Context Archiving:**
Don't lose chat history. Archive insights before finishing.
`python .kb/shared/tools/context_condenser.py <logfile>`

### 🟣 Phase 3: Contribution & Release
*When value is created.*

**1. Harvest Capabilities:**
Did you write a useful script? Don't leave it in `tmp/`.
`python .kb/shared/tools/kb.py archive <file> --type skills --scope project`

**2. Share Knowledge:**
Did you solve a hard bug?
`python .kb/shared/tools/kb_submit.py --target local --file solution.yaml --commit`

**3. System Release:**
Ready to deploy a feature? Broadcast it to the network.
`python .kb/shared/tools/kb_release.py v1.0.0 "Feature Name" --desc "Details..."`

---

## 3. Communication Protocols (IPC)

**How to talk to other projects:**

1.  **Discovery:** Read `company-os/registry/projects.yaml` (via `kb_sync` cache).
2.  **Request:** Use GitHub Issues on the target repo.
    *   **Label:** `agent-request`
    *   **Format:**
        ```yaml
        type: feature_request
        from: aparser
        priority: high
        ```

---

## 4. Standard Prompts (Copy & Paste)

### 🚀 Initialization Prompt
> Use this to bootstrap a new repository.

```markdown
@sys_instruction
# ACTIVATE: Project Node

You are the **Project Lead**. Initialize this repository into the Company OS.

1. **Install:** `python <(curl -sSL https://raw.githubusercontent.com/ozand/shared-knowledge-base/main/scripts/unified-install.py) --full`
2. **Passport:** Generate `.kb/project/PROJECT.yaml` using `kb.py sync init-passport`. Fill in details.
3. **Register:** Execute `python .kb/shared/tools/kb_sync.py push`.
4. **Guidelines:** Install standards via `python .kb/shared/tools/kb.py template install <domain>`.

Report: "Project Node Active. Registry Synced."
```

### 📢 Release Prompt
> Use this when a milestone is reached.

```markdown
@sys_instruction
# EXECUTE: System Release

We have completed the task. Broadcast the update to the Federation.

1. **Update Tools:** `python .kb/shared/scripts/unified-install.py`
2. **Release:** `python .kb/shared/tools/kb_release.py <version> "<Title>" --desc "<Description>"`

Report: "Release <version> Broadcasted."
```

### 🔗 Integration Prompt
> Use this to consume updates from another project.

```markdown
@sys_instruction
# INTEGRATE: Dependency Update

1. **Configure:** Ensure `.kb/project/PROJECT.yaml` lists the dependency:
   ```yaml
   dependencies:
     - project_id: "target-project-id"
       version: "0.0.0"
   ```
2. **Check:** `python .kb/shared/tools/kb_sync.py check-updates`
3. **Plan:** If an update is found, analyze the changelog and plan integration.
```

---

## 5. Directory Structure Reference

| Path | Purpose | Access |
|------|---------|--------|
| `.kb/shared/` | Global Knowledge (Tools, Standards) | 🔒 Read-Only |
| `.kb/project/` | Local Knowledge (Secrets, Context) | ✏️ Read/Write |
| `.kb/project/PROJECT.yaml` | Passport (Identity & Deps) | ✏️ Read/Write |
| `.kb/cache/` | Temporary Data (Registry, Research) | 🗑️ Ephemeral |
| `docs/guidelines/` | Standard Operating Procedures | 📄 Generated |

---

**End of Manifesto.**
*Executed by the Company OS Architect.*
