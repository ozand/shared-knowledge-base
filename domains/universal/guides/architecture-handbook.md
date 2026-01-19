---
title: "Architecture Handbook: The 2026 Agent Ecosystem"
version: "1.0.0"
last_updated: "2026-01-19"
author: "Antigravity Agent"
status: "stable"
category: "guide"
---

# Architecture Handbook: The 2026 Agent Ecosystem

## Executive Summary

In 2026, software development has evolved from a human-centric process to a **multi-agent ecosystem**. The architecture defined in this handbook moves beyond simple "coding assistants" to a structured **Company OS** where autonomous agents collaborate, discover services, and maintain their own knowledge.

The core philosophy is **"Decoupled Autonomy, Strong Contracts"**:
1.  **Agents are specialized** (Security, Architecture, Implementation).
2.  **Knowledge is tiered** (Universal truths vs. Project specifics).
3.  **Communication is structured** (Protocol-driven IPC vs. chatting).

---

## 1. The Two-Tier Knowledge Architecture

We solve the "Context Window" problem not by making windows larger, but by making knowledge **modular**.

### 1.1 Shared Knowledge Base (The "Universal Truth")
The **Shared KB** contains patterns, guides, and standards that apply to *all* projects.
*   **Location:** Central repository (e.g., `shared-knowledge-base`).
*   **Content:** Language patterns (`python/`), Universal rules (`universal/`), Architecture patterns (`patterns/`).
*   **Governance:** Strictly managed by the **Curator Agent**. Project Agents *cannot* commit directly.

### 1.2 Project Knowledge Base (The "Local Truth")
Each project maintains its own `.kb/` directory (The **Project KB**). This is the agent's "working memory" for that specific codebase.
*   **Location:** `.kb/` inside the project root.
*   **Content:**
    *   `project/PROJECT.yaml`: The Project Passport (Identity).
    *   `architecture/`: Project-specific design docs.
    *   `active-domains/`: Symlinks or copies of relevant Shared KB modules.

### 1.3 Modular Loading
Instead of loading the entire Shared KB, agents use a **Modular Knowledge Manager** to load only what they need.
*   **Mechanism:** `kb_manager.scan()` detects tech stacks (e.g., `go.mod` found).
*   **Action:** `kb_manager.install("go")` pulls the Go domain from Shared KB into the Project KB.
*   **Result:** Context windows remain lean and relevant.

---

## 2. Company OS: The Central Nervous System

As the number of projects grows, agents need a way to find each other. **Company OS** is the service discovery layer.

### 2.1 The Registry
A centralized, machine-readable catalog of all active projects.
*   **Source of Truth:** `company-os/registry/projects.yaml`
*   **Synchronization:** Each project's agent maintains a `PROJECT.yaml` passport. When this changes, a sync tool pushes updates to the central registry.

### 2.2 Inter-Project Communication (IPC)
Agents do not "chat" informally to request changes across projects. They use the **IPCP (Inter-Project Communication Protocol)**.
*   **Medium:** GitHub Issues (structured).
*   **Schema:** Frontmatter in issue bodies defines the request.
    ```yaml
    ---
    ipc_version: "1.0"
    type: "feature_request"
    from_project: "company/frontend"
    to_component: "auth-service"
    priority: "high"
    ---
    ```
*   **Workflow:**
    1.  Agent A checks Registry to find Agent B's repo.
    2.  Agent A creates a structured Issue in Agent B's repo.
    3.  Agent B's "Watcher" detects the request and executes the work.

---

## 3. Agent Roles & Orchestration

Specialization requires strict role definitions to prevent chaos.

### 3.1 The Orchestrator-Worker Pattern
Complex tasks are never executed by a single agent.
*   **Orchestrator (e.g., Opus 4):**
    *   Plans the workflow.
    *   Maintains global state (`state.json`).
    *   Delegates tasks to workers.
    *   *Does not write code.*
*   **Workers (e.g., Sonnet 4):**
    *   **Specialists:** Security, Testing, Documentation, Implementation.
    *   Execute specific, bounded tasks.
    *   Return results to the Orchestrator.

### 3.2 Role Separation: Project vs. Curator
To protect the integrity of the Shared KB, we enforce **Strict Role Separation**.

| Role | Domain | Permissions | Responsibilities |
| :--- | :--- | :--- | :--- |
| **Project Agent** | Project Repo | **Read-Only** on Shared KB | • Consumes Shared KB patterns.<br>• Discovers new patterns.<br>• Submits patterns via **GitHub Issues** (Handoff). |
| **Curator Agent** | Shared KB Repo | **Write** on Shared KB | • Reviews submitted Issues.<br>• Validates & Refines YAML.<br>• **Commits** to Shared KB.<br>• Maintains quality and consistency. |

### 3.3 The Contribution Handoff
When a Project Agent solves a novel problem, it must "upload" that knowledge to the collective:
1.  **Extract:** Agent identifies a reusable pattern.
2.  **Format:** Agent creates a local YAML definition.
3.  **Submit:** Agent creates a **GitHub Issue** in the Shared KB repo (Pattern: `AGENT-HANDOFF-001`).
4.  **Integration:** The Curator Agent reviews and merges it into the Universal Truth.

---

## Summary of Key Patterns

*   **COMPANY-OS-ARCHITECTURE-001:** Central Registry & IPC.
*   **MODULAR-KNOWLEDGE-SYSTEM-001:** Dynamic loading of knowledge domains.
*   **AGENT-ORCHESTRATION-001:** Orchestrator-Worker coordination.
*   **AGENT-ROLE-SEPARATION-001:** Curator vs. Project Agent permissions.
*   **PROJECT-PASSPORT-001:** Self-describing project metadata.
