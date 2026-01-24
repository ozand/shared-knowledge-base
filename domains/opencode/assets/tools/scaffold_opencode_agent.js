/**
 * Opencode Agent Scaffolder
 * Usage: bun scaffold_opencode_agent.js <agent-name> <description>
 */

const fs = require('fs');
const path = require('path');

const agentName = process.argv[2];
const description = process.argv[3] || "Custom agent";

if (!agentName) {
  console.error("Usage: bun scaffold_opencode_agent.js <agent-name> [description]");
  process.exit(1);
}

const agentsDir = path.join('.opencode', 'agents');
const agentPath = path.join(agentsDir, `${agentName}.md`);

// Ensure directory exists
if (!fs.existsSync(agentsDir)) {
  fs.mkdirSync(agentsDir, { recursive: true });
}

const content = `---
description: ${description}
temperature: 0.1
model: anthropic/claude-3-5-sonnet-20241022
---

You are the **${agentName}**.

# Role
${description}

# Instructions
- [Add specific instructions here]

# Tools
- [List specific tools here]
`;

fs.writeFileSync(agentPath, content);
console.log(`✅ Agent scaffolded at ${agentPath}`);
