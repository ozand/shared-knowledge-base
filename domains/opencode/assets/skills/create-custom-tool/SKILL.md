---
name: create-custom-tool
description: Guide for creating custom Opencode tools (JS/TS or Python)
---

# Creating Custom Tools for Opencode

This skill provides templates and rules for creating custom tools in `.opencode/tools/`.

## 1. JavaScript/TypeScript Tool (Recommended)
Opencode uses `zod` for schema definition.

**Template:**
```typescript
import { tool } from "opencode";

export const myTool = tool({
  description: "Description of what the tool does",
  parameters: tool.schema.object({
    argName: tool.schema.string().describe("Description of the argument"),
    optionalArg: tool.schema.number().optional()
  }),
  execute: async ({ argName, optionalArg }) => {
    // Tool logic here
    console.log(`Executing with ${argName}`);
    return "Result string";
  }
});
```

## 2. Python Tool Wrapper (via Bun)
You can wrap Python scripts.

**Template:**
```typescript
import { tool } from "opencode";

export const pythonWrapper = tool({
  description: "Wraps a python script",
  parameters: tool.schema.object({
    input: tool.schema.string()
  }),
  execute: async ({ input }) => {
    // Assumes the script is in .opencode/scripts/
    const result = await Bun.$`python3 .opencode/scripts/myscript.py ${input}`.text();
    return result;
  }
});
```

## Rules
1.  **Location**: Save files in `.opencode/tools/`.
2.  **Naming**: Export names become tool names (e.g., `export const search` -> `tool_search` or just `search` depending on loading).
3.  **Dependencies**: If using external npm packages, ensure a `package.json` exists in `.opencode/tools/` or `.opencode/plugins/` and run `bun install`.
