import { tool } from "opencode";

// Tool to search the knowledge base
export const kb_search = tool({
  name: "kb_search",
  description: "Search the knowledge base for existing patterns or errors",
  parameters: tool.schema.object({
    query: tool.schema.string().describe("Search query term"),
    scope: tool.schema.enum(["project", "shared", "all"]).optional().describe("Search scope"),
    category: tool.schema.string().optional().describe("Filter by category (e.g. python, docker)")
  }),
  execute: async ({ query, scope = "all", category }) => {
    let cmd = `python tools/kb.py search "${query}" --scope ${scope}`;
    if (category) cmd += ` --category ${category}`;
    
    try {
      const result = await Bun.$`${{ raw: cmd }}`.text();
      return result;
    } catch (err) {
      return `Error executing search: ${err.message}`;
    }
  }
});

// Tool to validate YAML files
export const kb_validate = tool({
  name: "kb_validate",
  description: "Validate YAML files against the schema",
  parameters: tool.schema.object({
    path: tool.schema.string().describe("Path to file or directory to validate")
  }),
  execute: async ({ path }) => {
    try {
      const result = await Bun.$`python tools/kb.py validate ${path}`.text();
      return result;
    } catch (err) {
      // kb.py returns exit code 1 on validation failure, which throws in Bun
      // We want to return the output (errors) anyway
      return err.stdout ? err.stdout.toString() : err.message;
    }
  }
});

// Tool to check KB statistics
export const kb_stats = tool({
  name: "kb_stats",
  description: "Show statistics about the knowledge base",
  parameters: tool.schema.object({}),
  execute: async () => {
    const result = await Bun.$`python tools/kb.py stats`.text();
    return result;
  }
});

// Tool to rebuild the index
export const kb_index = tool({
  name: "kb_index",
  description: "Rebuild the search index (run after adding files)",
  parameters: tool.schema.object({
    force: tool.schema.boolean().optional().describe("Force full rebuild")
  }),
  execute: async ({ force }) => {
    const flag = force ? "--force" : "";
    const result = await Bun.$`python tools/kb.py index ${flag}`.text();
    return result;
  }
});
