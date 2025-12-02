#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  Tool,
} from "@modelcontextprotocol/sdk/types.js";
import { exec } from "child_process";
import { promisify } from "util";
import * as fs from "fs/promises";
import * as path from "path";
import { fileURLToPath } from "url";

const execAsync = promisify(exec);

// Get the project root directory (parent of mcp-server)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, "../..");
const SCRIPTS_DIR = path.join(PROJECT_ROOT, "scripts");
const FRAMEWORKS_DIR = path.join(PROJECT_ROOT, "frameworks");
const TEMPLATES_DIR = path.join(PROJECT_ROOT, "templates");
const CONTEXT_DIR = path.join(PROJECT_ROOT, "context");

// Helper function to execute Python scripts
async function executePythonScript(
  scriptPath: string,
  args: string[]
): Promise<string> {
  const command = `python "${scriptPath}" ${args.join(" ")}`;
  try {
    const { stdout, stderr } = await execAsync(command, {
      maxBuffer: 10 * 1024 * 1024, // 10MB buffer for large outputs
    });
    if (stderr && !stderr.includes("Loading")) {
      // Ignore verbose loading messages
      console.error("Script stderr:", stderr);
    }
    return stdout;
  } catch (error: any) {
    throw new Error(`Script execution failed: ${error.message}`);
  }
}

// Helper function to recursively find files
async function findFiles(
  dir: string,
  extension: string
): Promise<{ name: string; path: string; relativePath: string }[]> {
  const results: { name: string; path: string; relativePath: string }[] = [];

  async function scan(currentDir: string) {
    try {
      const entries = await fs.readdir(currentDir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(currentDir, entry.name);

        if (entry.isDirectory()) {
          await scan(fullPath);
        } else if (entry.name.endsWith(extension)) {
          const relativePath = path.relative(dir, fullPath);
          const name = relativePath.replace(/\\/g, "/").replace(extension, "");
          results.push({
            name,
            path: fullPath,
            relativePath: relativePath.replace(/\\/g, "/"),
          });
        }
      }
    } catch (error) {
      // Ignore directories that can't be read
    }
  }

  await scan(dir);
  return results;
}

// Helper function to read file content
async function readFileContent(filePath: string): Promise<string> {
  try {
    return await fs.readFile(filePath, "utf-8");
  } catch (error: any) {
    throw new Error(`Failed to read file ${filePath}: ${error.message}`);
  }
}

// Helper function to extract description from markdown file
async function getFileDescription(filePath: string): Promise<string> {
  try {
    const content = await readFileContent(filePath);
    // Try to extract first paragraph or first non-empty line after title
    const lines = content.split("\n");
    let description = "";

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      // Skip title lines and empty lines
      if (line.startsWith("#") || line === "") continue;
      // Take first non-empty, non-title line
      description = line;
      break;
    }

    return description || "No description available";
  } catch (error) {
    return "No description available";
  }
}

// Define available tools
const TOOLS: Tool[] = [
  {
    name: "assemble_context",
    description:
      "Assemble context for a task based on mode (planning/technical/analysis/communication/minimal/full). Returns a complete context-enriched prompt ready to use with Claude.",
    inputSchema: {
      type: "object",
      properties: {
        task: {
          type: "string",
          description: "The task or question to assemble context for",
        },
        mode: {
          type: "string",
          enum: [
            "planning",
            "technical",
            "analysis",
            "communication",
            "minimal",
            "full",
          ],
          description:
            "Context assembly mode: planning (strategic decisions), technical (coding/infrastructure), analysis (deep thinking), communication (writing), minimal (task only), full (comprehensive context)",
          default: "full",
        },
        framework: {
          type: "string",
          description:
            "Optional: Specific thinking framework to include (e.g., 'first-principles', 'pre-mortem', 'steelman-critique')",
        },
        project: {
          type: "string",
          description:
            "Optional: Project name to include project-specific context from context/projects/active/",
        },
      },
      required: ["task"],
    },
  },
  {
    name: "search_knowledge",
    description:
      "Search the knowledge base using semantic search. Searches across all context files, frameworks, and learnings to find relevant information.",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Search query to find relevant knowledge",
        },
        limit: {
          type: "number",
          description: "Maximum number of results to return",
          default: 5,
          minimum: 1,
          maximum: 20,
        },
      },
      required: ["query"],
    },
  },
  {
    name: "list_frameworks",
    description:
      "List all available thinking frameworks organized by category (planning, analysis, decision, technical, communication, creation)",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "list_templates",
    description:
      "List all available production templates organized by category (voice-ai, development, outreach, client, analysis)",
    inputSchema: {
      type: "object",
      properties: {},
    },
  },
  {
    name: "get_framework",
    description:
      "Get the full content of a specific thinking framework by name (e.g., 'planning/first-principles' or 'analysis/steelman-critique')",
    inputSchema: {
      type: "object",
      properties: {
        name: {
          type: "string",
          description:
            "Framework name (can include category prefix like 'planning/first-principles' or just 'first-principles')",
        },
      },
      required: ["name"],
    },
  },
  {
    name: "get_template",
    description:
      "Get the full content of a specific template by name (e.g., 'development/claude-code-handoff' or 'voice-ai/receptionist-base')",
    inputSchema: {
      type: "object",
      properties: {
        name: {
          type: "string",
          description:
            "Template name (can include category prefix like 'development/claude-code-handoff' or just 'claude-code-handoff')",
        },
      },
      required: ["name"],
    },
  },
  {
    name: "capture_output",
    description:
      "Save successful output for future learning. Stores content with metadata for later retrieval and learning.",
    inputSchema: {
      type: "object",
      properties: {
        content: {
          type: "string",
          description: "The content to save",
        },
        tags: {
          type: "array",
          items: { type: "string" },
          description: "Tags for categorization (e.g., ['technical', 'n8n'])",
        },
        category: {
          type: "string",
          description:
            "Category (e.g., 'framework', 'template', 'learning', 'example')",
        },
      },
      required: ["content", "category"],
    },
  },
  {
    name: "improve_prompt",
    description:
      "Improve a prompt using AI-powered analysis and optimization. Returns an improved version with explanation of changes made.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: {
          type: "string",
          description: "The prompt to improve",
        },
        auto_fix: {
          type: "boolean",
          description: "Automatically apply fixes (default: true)",
          default: true,
        },
      },
      required: ["prompt"],
    },
  },
  {
    name: "diagnose_prompt",
    description:
      "Diagnose a prompt for issues and weaknesses. Returns detailed analysis with quality scores, identified issues, and suggestions for improvement.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: {
          type: "string",
          description: "The prompt to diagnose",
        },
      },
      required: ["prompt"],
    },
  },
  {
    name: "optimize_prompt",
    description:
      "Generate multiple optimized variations of a prompt and return the best one. Uses different optimization techniques and scores each variation.",
    inputSchema: {
      type: "object",
      properties: {
        prompt: {
          type: "string",
          description: "The prompt to optimize",
        },
        num_variations: {
          type: "number",
          description: "Number of variations to generate (default: 3)",
          default: 3,
          minimum: 1,
          maximum: 10,
        },
      },
      required: ["prompt"],
    },
  },
  {
    name: "get_prompting_best_practices",
    description:
      "Get prompting best practices and guidelines. Optionally filter by topic to get relevant sections.",
    inputSchema: {
      type: "object",
      properties: {
        topic: {
          type: "string",
          description:
            "Optional topic to filter best practices (e.g., 'examples', 'temperature', 'chain-of-thought', 'xml', 'formatting')",
        },
      },
    },
  },
  {
    name: "route_prompt",
    description:
      "Analyze a task and recommend the optimal prompting framework and techniques to use. Returns framework path, recommended techniques, and model suggestion.",
    inputSchema: {
      type: "object",
      properties: {
        task: {
          type: "string",
          description: "The task description to analyze for routing",
        },
      },
      required: ["task"],
    },
  },
];

// Create the server
const server = new Server(
  {
    name: "prompt-engineering-system",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Handle list tools request
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return { tools: TOOLS };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "assemble_context": {
        const { task, mode = "full", framework, project } = args as {
          task: string;
          mode?: string;
          framework?: string;
          project?: string;
        };

        const scriptPath = path.join(SCRIPTS_DIR, "context-loader.py");
        const scriptArgs = [
          "--task",
          `"${task.replace(/"/g, '\\"')}"`,
          "--mode",
          mode,
        ];

        if (framework) {
          scriptArgs.push("--framework", framework);
        }
        if (project) {
          scriptArgs.push("--project", project);
        }

        const result = await executePythonScript(scriptPath, scriptArgs);

        return {
          content: [
            {
              type: "text",
              text: result,
            },
          ],
        };
      }

      case "search_knowledge": {
        const { query, limit = 5 } = args as { query: string; limit?: number };

        // Simple file-based search implementation
        // In a production system, this would use Qdrant vector search
        const searchResults: Array<{
          file: string;
          content: string;
          relevance: string;
        }> = [];

        // Search in context files
        const contextFiles = await findFiles(CONTEXT_DIR, ".md");
        for (const file of contextFiles.slice(0, limit)) {
          const content = await readFileContent(file.path);
          // Simple keyword matching (in production, use embeddings)
          if (
            content.toLowerCase().includes(query.toLowerCase()) ||
            file.name.toLowerCase().includes(query.toLowerCase())
          ) {
            searchResults.push({
              file: file.relativePath,
              content: content.substring(0, 500) + "...",
              relevance: "Found in context",
            });
          }
          if (searchResults.length >= limit) break;
        }

        if (searchResults.length === 0) {
          searchResults.push({
            file: "No results",
            content:
              "No matching knowledge found. Vector search requires Qdrant to be configured and running.",
            relevance: "N/A",
          });
        }

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(searchResults, null, 2),
            },
          ],
        };
      }

      case "list_frameworks": {
        const frameworks = await findFiles(FRAMEWORKS_DIR, ".md");
        const frameworkList = await Promise.all(
          frameworks.map(async (fw) => ({
            name: fw.name,
            path: fw.relativePath,
            description: await getFileDescription(fw.path),
          }))
        );

        // Group by category
        const grouped: Record<string, typeof frameworkList> = {};
        frameworkList.forEach((fw) => {
          const category = fw.name.split("/")[0];
          if (!grouped[category]) grouped[category] = [];
          grouped[category].push(fw);
        });

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(grouped, null, 2),
            },
          ],
        };
      }

      case "list_templates": {
        const templates = await findFiles(TEMPLATES_DIR, ".md");
        const templateList = await Promise.all(
          templates.map(async (tmpl) => ({
            name: tmpl.name,
            path: tmpl.relativePath,
            description: await getFileDescription(tmpl.path),
          }))
        );

        // Group by category
        const grouped: Record<string, typeof templateList> = {};
        templateList.forEach((tmpl) => {
          const category = tmpl.name.split("/")[0];
          if (!grouped[category]) grouped[category] = [];
          grouped[category].push(tmpl);
        });

        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(grouped, null, 2),
            },
          ],
        };
      }

      case "get_framework": {
        const { name: frameworkName } = args as { name: string };

        // Try to find the framework
        let frameworkPath = path.join(
          FRAMEWORKS_DIR,
          frameworkName.endsWith(".md") ? frameworkName : `${frameworkName}.md`
        );

        // If not found with full path, search for it
        if (!(await fs.access(frameworkPath).then(() => true).catch(() => false))) {
          const frameworks = await findFiles(FRAMEWORKS_DIR, ".md");
          const found = frameworks.find(
            (fw) =>
              fw.name === frameworkName ||
              fw.name.endsWith(`/${frameworkName}`) ||
              fw.name.endsWith(`/${frameworkName}`)
          );

          if (found) {
            frameworkPath = found.path;
          } else {
            return {
              content: [
                {
                  type: "text",
                  text: `Framework '${frameworkName}' not found. Use list_frameworks to see available frameworks.`,
                },
              ],
              isError: true,
            };
          }
        }

        const content = await readFileContent(frameworkPath);

        return {
          content: [
            {
              type: "text",
              text: content,
            },
          ],
        };
      }

      case "get_template": {
        const { name: templateName } = args as { name: string };

        // Try to find the template
        let templatePath = path.join(
          TEMPLATES_DIR,
          templateName.endsWith(".md") ? templateName : `${templateName}.md`
        );

        // If not found with full path, search for it
        if (!(await fs.access(templatePath).then(() => true).catch(() => false))) {
          const templates = await findFiles(TEMPLATES_DIR, ".md");
          const found = templates.find(
            (tmpl) =>
              tmpl.name === templateName ||
              tmpl.name.endsWith(`/${templateName}`) ||
              tmpl.name.endsWith(`/${templateName}`)
          );

          if (found) {
            templatePath = found.path;
          } else {
            return {
              content: [
                {
                  type: "text",
                  text: `Template '${templateName}' not found. Use list_templates to see available templates.`,
                },
              ],
              isError: true,
            };
          }
        }

        const content = await readFileContent(templatePath);

        return {
          content: [
            {
              type: "text",
              text: content,
            },
          ],
        };
      }

      case "capture_output": {
        const { content, tags = [], category } = args as {
          content: string;
          tags?: string[];
          category: string;
        };

        // Save to learnings directory
        const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
        const filename = `capture-${timestamp}.md`;
        const outputDir = path.join(CONTEXT_DIR, "learnings", "captures");

        // Create directory if it doesn't exist
        await fs.mkdir(outputDir, { recursive: true });

        const outputPath = path.join(outputDir, filename);
        const metadata = `---
category: ${category}
tags: ${JSON.stringify(tags)}
captured: ${new Date().toISOString()}
---

`;

        await fs.writeFile(outputPath, metadata + content, "utf-8");

        return {
          content: [
            {
              type: "text",
              text: `Content captured successfully to ${filename}\n\nCategory: ${category}\nTags: ${tags.join(", ")}\n\nThis output has been saved for future reference and learning.`,
            },
          ],
        };
      }

      case "improve_prompt": {
        const { prompt, auto_fix = true } = args as {
          prompt: string;
          auto_fix?: boolean;
        };

        // First diagnose the prompt
        const doctorScript = path.join(SCRIPTS_DIR, "prompt_doctor.py");
        const diagArgs = ["--diagnose", "-", "--json"];

        if (auto_fix) {
          diagArgs.push("--fix");
        }

        // Write prompt to temp file
        const tmpDir = path.join(PROJECT_ROOT, ".tmp");
        await fs.mkdir(tmpDir, { recursive: true });
        const tmpFile = path.join(tmpDir, `prompt-${Date.now()}.txt`);
        await fs.writeFile(tmpFile, prompt, "utf-8");

        try {
          // Run doctor with file input
          const command = `python "${doctorScript}" --diagnose "${tmpFile}" --json${
            auto_fix ? " --fix" : ""
          }`;
          const { stdout } = await execAsync(command, {
            maxBuffer: 10 * 1024 * 1024,
          });

          // Parse diagnosis result
          const diagnosis = JSON.parse(stdout);

          // If auto_fix is true and there's an improved prompt, get it
          let improvedPrompt = prompt;
          let explanation = "";

          if (auto_fix) {
            // Run again to get the fixed prompt
            const fixCommand = `python "${doctorScript}" --diagnose "${tmpFile}" --fix`;
            const { stdout: fixedOutput } = await execAsync(fixCommand, {
              maxBuffer: 10 * 1024 * 1024,
            });

            // Extract the fixed prompt from output
            const fixedMatch = fixedOutput.match(
              /FIXED PROMPT:\s*={50,}\s*([\s\S]+?)$/m
            );
            if (fixedMatch) {
              improvedPrompt = fixedMatch[1].trim();
            }

            // Generate explanation based on issues found
            const issues = diagnosis.issues || [];
            if (issues.length > 0) {
              explanation = `\n\nImprovements made:\n${issues
                .map(
                  (issue: any) =>
                    `- Fixed ${issue.type}: ${issue.suggestion}`
                )
                .join("\n")}`;
            }
          }

          const result = {
            original: prompt,
            improved: improvedPrompt,
            quality_score: diagnosis.quality_score,
            improvements: explanation,
            issues_found: diagnosis.issues?.length || 0,
          };

          return {
            content: [
              {
                type: "text",
                text: JSON.stringify(result, null, 2),
              },
            ],
          };
        } finally {
          // Clean up temp file
          try {
            await fs.unlink(tmpFile);
          } catch {}
        }
      }

      case "diagnose_prompt": {
        const { prompt } = args as { prompt: string };

        const scriptPath = path.join(SCRIPTS_DIR, "prompt_doctor.py");

        // Write prompt to temp file
        const tmpDir = path.join(PROJECT_ROOT, ".tmp");
        await fs.mkdir(tmpDir, { recursive: true });
        const tmpFile = path.join(tmpDir, `prompt-${Date.now()}.txt`);
        await fs.writeFile(tmpFile, prompt, "utf-8");

        try {
          const command = `python "${scriptPath}" --diagnose "${tmpFile}" --json`;
          const { stdout } = await execAsync(command, {
            maxBuffer: 10 * 1024 * 1024,
          });

          return {
            content: [
              {
                type: "text",
                text: stdout,
              },
            ],
          };
        } finally {
          // Clean up temp file
          try {
            await fs.unlink(tmpFile);
          } catch {}
        }
      }

      case "optimize_prompt": {
        const { prompt, num_variations = 3 } = args as {
          prompt: string;
          num_variations?: number;
        };

        const scriptPath = path.join(SCRIPTS_DIR, "prompt_optimizer.py");

        // Write prompt to temp file
        const tmpDir = path.join(PROJECT_ROOT, ".tmp");
        await fs.mkdir(tmpDir, { recursive: true });
        const tmpFile = path.join(tmpDir, `prompt-${Date.now()}.txt`);
        await fs.writeFile(tmpFile, prompt, "utf-8");

        try {
          const command = `python "${scriptPath}" -p "${tmpFile}" -n ${num_variations}`;
          const { stdout } = await execAsync(command, {
            maxBuffer: 10 * 1024 * 1024,
            timeout: 120000, // 2 minutes timeout for optimization
          });

          return {
            content: [
              {
                type: "text",
                text: stdout,
              },
            ],
          };
        } finally {
          // Clean up temp file
          try {
            await fs.unlink(tmpFile);
          } catch {}
        }
      }

      case "get_prompting_best_practices": {
        const { topic } = args as { topic?: string };

        const bestPracticesPath = path.join(
          CONTEXT_DIR,
          "technical",
          "prompting-best-practices.md"
        );

        let content = await readFileContent(bestPracticesPath);

        // Filter by topic if provided
        if (topic) {
          const topicLower = topic.toLowerCase();
          const lines = content.split("\n");
          const filtered: string[] = [];
          let inRelevantSection = false;
          let sectionLevel = 0;

          filtered.push("# Prompting Best Practices - Filtered Results\n");
          filtered.push(`**Topic:** ${topic}\n\n`);

          for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const trimmed = line.trim().toLowerCase();

            // Check for headers
            const headerMatch = line.match(/^(#{1,6})\s+(.+)$/);

            if (headerMatch) {
              const level = headerMatch[1].length;
              const headerText = headerMatch[2].toLowerCase();

              if (headerText.includes(topicLower)) {
                inRelevantSection = true;
                sectionLevel = level;
                filtered.push(line);
              } else if (inRelevantSection && level <= sectionLevel) {
                inRelevantSection = false;
              } else if (inRelevantSection) {
                filtered.push(line);
              }
            } else if (inRelevantSection || trimmed.includes(topicLower)) {
              if (!inRelevantSection && trimmed.includes(topicLower)) {
                inRelevantSection = true;
                sectionLevel = 2;
              }
              filtered.push(line);
            }
          }

          if (filtered.length > 3) {
            content = filtered.join("\n");
          } else {
            content = `# Prompting Best Practices\n\nNo specific section found for "${topic}". Showing complete guide:\n\n${content}`;
          }
        }

        return {
          content: [
            {
              type: "text",
              text: content,
            },
          ],
        };
      }

      case "route_prompt": {
        const { task } = args as { task: string };

        const scriptPath = path.join(SCRIPTS_DIR, "prompt_router.py");
        const command = `python "${scriptPath}" "${task.replace(/"/g, '\\"')}"`;

        const { stdout } = await execAsync(command, {
          maxBuffer: 10 * 1024 * 1024,
        });

        return {
          content: [
            {
              type: "text",
              text: stdout,
            },
          ],
        };
      }
      default:
        return {
          content: [
            {
              type: "text",
              text: `Unknown tool: ${name}`,
            },
          ],
          isError: true,
        };
    }
  } catch (error: any) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Prompt Engineering MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
