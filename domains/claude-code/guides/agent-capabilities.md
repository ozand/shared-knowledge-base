---
title: "RooCode Agent Capabilities"
version: "1.0.0"
last_updated: "2025-01-01"
category: "roocode_specific"
priority: reference
applies_to: ["roocode_users"]
agent_usage: "Reference when delegating tasks or choosing which agent to invoke"
keywords: ["agents", "delegation", "orchestrator", "architect", "code", "debug"]
related_docs: ["roocode/tool-usage-protocol.md"]
---

# RooCode Agent Capabilities Handbook

> Single source of truth for agent roles, capabilities, and delegation decisions

---

## 1. Philosophy

This document defines:
- What each AI agent specializes in
- When to use each agent
- How agents should collaborate

**Source:** Derived from RooCode system prompts (`roo_code_mode.md`)

---

## 2. Agent Directory

### 🪃 Orchestrator

**Role:** Strategic coordinator for complex multi-step projects

**Specializes in:**
- Breaking down large tasks into subtasks
- Coordinating work between specialized agents
- Managing workflow and dependencies
- High-level project planning

**Use when:**
- Task requires multiple specialists
- Complex, multi-phase project
- Need to coordinate dependencies between subtasks
- Managing a feature that touches multiple systems

**Does NOT:**
- Write code directly (delegates to Code agent)
- Debug issues (delegates to Debug agent)
- Research codebase alone (delegates to Project Research)

**Example tasks:**
- "Build a complete payment processing system"
- "Migrate authentication from JWT to OAuth"
- "Refactor the entire API layer"

---

### 🗿️ Architect

**Role:** Technical leader focused on planning and design

**Specializes in:**
- Information gathering and analysis
- Creating detailed implementation plans
- Technical specifications and design documents
- Breaking down complex problems

**Use when:**
- Need to design before implementing
- Planning system architecture
- Creating technical specifications
- Analyzing trade-offs between approaches

**Output:** Detailed `implementation-plan` document

**Does NOT:**
- Implement code (delegates to Code agent)
- Make code changes during planning phase

**Example tasks:**
- "Design a caching layer for the API"
- "Create an implementation plan for real-time notifications"
- "Analyze and propose solution for performance bottleneck"

---

### 💻 Code

**Role:** Highly skilled software engineer

**Specializes in:**
- Writing new code
- Modifying existing code
- Refactoring and optimization
- Implementing features from specifications
- Code reviews and improvements

**Use when:**
- Need to write code
- Implementing features
- Refactoring existing code
- Making any code changes

**Does NOT:**
- Plan architecture (Architect does this)
- Debug complex issues (Debug agent better suited)
- Research codebase structure (Project Research better)

**Example tasks:**
- "Implement the payment processor class"
- "Add validation to the user registration endpoint"
- "Refactor the database query for better performance"

---

### 🪲 Debug

**Role:** Expert in systematic problem diagnosis

**Specializes in:**
- Investigating errors and exceptions
- Diagnosing performance issues
- Troubleshooting bugs
- Root cause analysis
- Creating reproduction steps

**Use when:**
- Something is broken
- Errors or exceptions occurring
- Unexpected behavior
- Performance problems
- Need to understand why code fails

**Does NOT:**
- Implement new features (Code agent does this)
- Write initial code (Code agent better)

**Example tasks:**
- "Why is the payment endpoint returning 500 errors?"
- "Investigate why tests are failing in CI"
- "Find the cause of memory leak in the background worker"

---

### ❓ Ask

**Role:** Knowledgeable technical assistant

**Specializes in:**
- Answering technical questions
- Providing explanations
- Clarifying concepts
- Documentation lookup
- Knowledge sharing

**Use when:**
- Need information or explanation
- Understanding how something works
- Learning about technologies or patterns
- Clarifying documentation

**Does NOT:**
- Make code changes (read-only)
- Implement features
- Debug issues

**Example tasks:**
- "Explain how dependency injection works"
- "What's the difference between async/await and promises?"
- "How should I structure my test fixtures?"

---

### 🔬 Project Research

**Role:** Detail-oriented codebase analyst

**Specializes in:**
- Examining project structure
- Analyzing file dependencies
- Understanding existing implementations
- Mapping architecture
- Finding patterns in code

**Use when:**
- Need to understand codebase structure
- Analyzing existing architecture
- Finding how features are currently implemented
- Mapping dependencies
- Before making large changes

**Does NOT:**
- Make code changes
- Implement features

**Example tasks:**
- "Map out how authentication currently works"
- "Find all places where the User model is used"
- "Analyze the project structure and dependencies"

---

### 📝 User Story Creator

**Role:** Agile requirements specialist

**Specializes in:**
- Creating user stories
- Defining acceptance criteria
- Breaking down requirements
- Clarifying feature scope
- Writing clear specifications

**Use when:**
- Need to create user stories
- Breaking down large features
- Defining acceptance criteria
- Clarifying requirements

**Output:** Well-formed user stories with acceptance criteria

**Does NOT:**
- Implement features
- Write technical specifications (Architect does this)

**Example tasks:**
- "Create user stories for the checkout flow"
- "Break down the 'user profile' epic into stories"
- "Define acceptance criteria for payment processing"

---

### ✍️ Documentation Writer

**Role:** Technical documentation expert

**Specializes in:**
- Creating technical documentation
- Writing API documentation
- Creating user guides
- Updating README files
- Documenting architecture

**Use when:**
- Need to create documentation
- Update existing docs
- Write API specifications
- Create user guides
- Document architecture decisions

**Does NOT:**
- Write code
- Implement features

**Example tasks:**
- "Create API documentation for the payment endpoints"
- "Update the README with new setup instructions"
- "Document the authentication flow"

---

## 3. Agent Selection Decision Tree

```
What type of task?
│
├─ Complex multi-step project?
│  └─ Use Orchestrator (will delegate to others)
│
├─ Need to plan/design before building?
│  └─ Use Architect → then Code for implementation
│
├─ Need to write/modify code?
│  └─ Use Code
│
├─ Something is broken?
│  └─ Use Debug
│
├─ Need to understand the codebase?
│  └─ Use Project Research
│
├─ Need information or explanation?
│  └─ Use Ask
│
├─ Need to define requirements?
│  └─ Use User Story Creator
│
└─ Need to write documentation?
   └─ Use Documentation Writer
```
