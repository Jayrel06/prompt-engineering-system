# Prompt Engineering System - MCP Server

Model Context Protocol (MCP) server that exposes your prompt engineering system to Claude Desktop and other MCP clients.

## Features

This MCP server provides Claude Desktop with direct access to your prompt engineering system:

- **assemble_context** - Dynamically assemble context-enriched prompts based on task type
- **search_knowledge** - Semantic search across your knowledge base
- **list_frameworks** - Browse available thinking frameworks
- **list_templates** - Browse available production templates
- **get_framework** - Retrieve specific framework content
- **get_template** - Retrieve specific template content
- **capture_output** - Save successful outputs for future learning

## Installation

### 1. Install Dependencies

```bash
cd C:/Users/JRiel/prompt-engineering-system/mcp-server
npm install
```

### 2. Build the TypeScript Code

```bash
npm run build
```

This compiles the TypeScript to JavaScript in the `dist/` directory.

### 3. Configure Claude Desktop

Edit your Claude Desktop configuration file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

Add the MCP server configuration:

```json
{
  "mcpServers": {
    "prompt-engineering": {
      "command": "node",
      "args": [
        "C:/Users/JRiel/prompt-engineering-system/mcp-server/dist/index.js"
      ]
    }
  }
}
```

**Note**: Use absolute paths. Adjust the path if your project is in a different location.

### 4. Restart Claude Desktop

After saving the configuration, completely quit and restart Claude Desktop. The MCP server will start automatically when Claude Desktop launches.

### 5. Verify Installation

In Claude Desktop, you should see the tools available in the interface. You can test by asking:

> "Can you list the available thinking frameworks?"

Or:

> "Assemble context for planning mode with the task: What should my Q1 priorities be?"

## Available Tools

### assemble_context

Assembles a complete context-enriched prompt ready for Claude.

**Parameters:**
- `task` (string, required): The task or question
- `mode` (enum, optional): Context mode - planning/technical/analysis/communication/minimal/full (default: full)
- `framework` (string, optional): Specific thinking framework to include
- `project` (string, optional): Project name for project-specific context

**Example:**
```
Assemble context for task "Design a lead scoring system" in technical mode
```

### search_knowledge

Search across all context files, frameworks, and learnings.

**Parameters:**
- `query` (string, required): Search query
- `limit` (number, optional): Max results (default: 5, max: 20)

**Example:**
```
Search knowledge for "n8n workflow patterns" with limit 10
```

**Note**: Currently uses simple keyword matching. For semantic search, configure Qdrant vector database.

### list_frameworks

Lists all available thinking frameworks organized by category.

**Example:**
```
List all available frameworks
```

### list_templates

Lists all available production templates organized by category.

**Example:**
```
Show me the available templates
```

### get_framework

Retrieves the full content of a specific framework.

**Parameters:**
- `name` (string, required): Framework name (e.g., "first-principles" or "planning/first-principles")

**Example:**
```
Get the first-principles framework
```

### get_template

Retrieves the full content of a specific template.

**Parameters:**
- `name` (string, required): Template name (e.g., "claude-code-handoff" or "development/claude-code-handoff")

**Example:**
```
Get the claude-code-handoff template
```

### capture_output

Saves successful outputs for future learning and reference.

**Parameters:**
- `content` (string, required): The content to save
- `category` (string, required): Category (e.g., "framework", "template", "learning", "example")
- `tags` (array, optional): Tags for categorization (e.g., ["technical", "n8n"])

**Example:**
```
Capture this output with category "learning" and tags ["workflow", "automation"]
```

Saved to: `context/learnings/captures/`

## Development

### Watch Mode

For development, run TypeScript in watch mode:

```bash
npm run watch
```

This automatically recompiles when you make changes to `src/index.ts`.

### Debugging

The MCP server logs to stderr. To see logs:

1. Check Claude Desktop's developer console (if available)
2. Or run the server manually to see output:

```bash
node dist/index.js
```

Note: When running manually, the server expects JSON-RPC messages on stdin.

### Project Structure

```
mcp-server/
├── src/
│   └── index.ts          # Main MCP server implementation
├── dist/                 # Compiled JavaScript (generated)
├── package.json          # Node.js dependencies
├── tsconfig.json         # TypeScript configuration
└── README.md            # This file
```

## Troubleshooting

### Tools Not Appearing in Claude Desktop

1. Verify the config file path is correct
2. Check that the absolute path in `claude_desktop_config.json` is correct
3. Completely quit and restart Claude Desktop (not just close the window)
4. Check Claude Desktop logs for errors

### "Python not found" Error

The server calls Python scripts. Ensure Python 3 is installed and available in your PATH:

```bash
python --version
```

Should show Python 3.x.x

### Build Errors

If `npm run build` fails:

1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Run `npm run build`

### Context Files Not Loading

Verify your project structure:
- `scripts/context-loader.py` exists and is executable
- `context/`, `frameworks/`, `templates/` directories exist
- Files are in the expected locations

## Upgrading

To update dependencies:

```bash
npm update
npm run build
```

Restart Claude Desktop after rebuilding.

## Advanced Configuration

### Vector Search with Qdrant

To enable semantic search instead of keyword matching:

1. Start Qdrant (if using Docker):
   ```bash
   cd ../infrastructure
   docker-compose up -d qdrant
   ```

2. The search_knowledge tool will automatically use Qdrant when available at `localhost:6333`

### Custom Python Path

If Python is not in your PATH, modify `src/index.ts`:

```typescript
const command = `C:/Path/To/Python/python.exe "${scriptPath}" ${args.join(" ")}`;
```

## How It Works

1. **Claude Desktop** starts the MCP server as a subprocess
2. **MCP Server** communicates via JSON-RPC over stdio
3. **Tool Calls** execute Python scripts or read files directly
4. **Results** are returned to Claude as formatted text

The server acts as a bridge between Claude Desktop and your prompt engineering system's Python scripts and markdown files.

## Integration Examples

### Planning Session

> "Assemble context for planning mode with task: Should I expand into HVAC market?"

Returns a complete prompt with:
- Core values and decision frameworks
- Business overview
- Planning frameworks (first principles, pre-mortem)
- Relevant learnings

### Technical Task

> "Assemble context for technical mode with task: Design a webhook handler for lead capture"

Returns:
- Infrastructure inventory
- Coding standards
- Technical frameworks
- n8n patterns

### Learning Capture

> "Capture this workflow design with category 'example' and tags 'n8n', 'lead-capture'"

Saves the content to `context/learnings/captures/` for future reference.

## License

MIT - Part of the Universal Prompt Engineering System
