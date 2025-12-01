# Quick Start Guide

Get the Prompt Engineering MCP Server running in 5 minutes.

## Prerequisites

- Node.js 18+ installed
- Python 3.x installed
- Claude Desktop installed

## Installation (3 steps)

### Step 1: Install & Build

**Option A: Automatic (Windows)**
```bash
cd C:/Users/JRiel/prompt-engineering-system/mcp-server
setup.bat
```

**Option B: Manual (All platforms)**
```bash
cd C:/Users/JRiel/prompt-engineering-system/mcp-server
npm install
npm run build
npm test
```

The test command verifies everything is set up correctly.

### Step 2: Configure Claude Desktop

**Windows:**
1. Open: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add this configuration:

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

**macOS:**
1. Open: `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Add the configuration above (adjust path)

**Linux:**
1. Open: `~/.config/Claude/claude_desktop_config.json`
2. Add the configuration above (adjust path)

**Important:** Use the absolute path to YOUR installation.

### Step 3: Restart Claude Desktop

1. Completely quit Claude Desktop (not just close window)
2. Restart Claude Desktop
3. MCP server will start automatically

## Verify It Works

In Claude Desktop, try these commands:

```
List all available frameworks
```

Expected: You should see frameworks organized by category.

```
Assemble context for planning mode with task "What should I focus on this quarter?"
```

Expected: You should get a comprehensive context-enriched prompt.

## First Commands to Try

### 1. Discover Resources
```
List all frameworks
List all templates
```

### 2. Try Context Assembly
```
Assemble context for technical mode with task "Build a webhook handler"
```

### 3. Get a Specific Resource
```
Get the first-principles framework
Get the claude-code-handoff template
```

### 4. Search Knowledge
```
Search knowledge for "n8n workflows"
```

## Troubleshooting

### "Tools not appearing"

1. Check config file location is correct
2. Verify absolute path in config points to dist/index.js
3. Completely restart Claude Desktop (quit and reopen)
4. Check Claude Desktop logs for errors

### "Python not found"

Run this to verify:
```bash
python --version
```

Should show Python 3.x.x

If not found, install Python and ensure it's in your PATH.

### "Module not found"

Run these:
```bash
cd C:/Users/JRiel/prompt-engineering-system/mcp-server
npm install
npm run build
```

### Build Errors

Delete and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Server Not Starting

Check that these exist:
- `C:/Users/JRiel/prompt-engineering-system/mcp-server/dist/index.js`
- `C:/Users/JRiel/prompt-engineering-system/scripts/context-loader.py`

Run verification:
```bash
npm test
```

## What Next?

### Learn the Tools
Read [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for detailed examples of every tool.

### Customize Context
Edit files in:
- `context/` - Your personal knowledge
- `frameworks/` - Your thinking frameworks
- `templates/` - Your production templates

### Build Workflows
Combine tools for powerful workflows:

**Example: Strategic Planning**
```
# 1. Get planning frameworks
List frameworks

# 2. Get specific framework
Get the pre-mortem framework

# 3. Assemble full context
Assemble context for planning mode with task "Should we expand to HVAC?"

# 4. Save the decision
Capture [your decision rationale] with category "learning" and tags ["strategy", "hvac"]
```

**Example: Technical Implementation**
```
# 1. Search for patterns
Search knowledge for "webhook" with limit 5

# 2. Get template
Get the n8n-workflow-spec template

# 3. Assemble context
Assemble context for technical mode with task "Build lead capture webhook"

# 4. Save the implementation
Capture [the workflow] with category "example" and tags ["n8n", "webhook"]
```

## Common Use Cases

### Daily Work
```
Assemble context for technical mode with task "Debug OAuth flow"
```

### Strategic Decisions
```
Assemble context for planning mode with task "Q1 priorities" and framework "first-principles"
```

### Client Communication
```
Get the proposal-generation template
Assemble context for communication mode with task "Write HVAC automation proposal"
```

### Learning & Growth
```
# After any successful task
Capture [what worked] with category "learning" and tags ["relevant", "tags"]
```

## Tips

1. **Start with list commands** to discover what's available
2. **Use minimal mode** for quick questions that don't need context
3. **Use full mode** when you're unsure what context you need
4. **Capture outputs** to build your knowledge base over time
5. **Search first** before creating new frameworks/templates

## Getting Help

- **Tool Reference**: [README.md](README.md)
- **Usage Examples**: [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

## Advanced

### Watch Mode (Development)
```bash
npm run watch
```

Automatically recompiles when you edit src/index.ts.

### Custom Python Path
If Python isn't in PATH, edit `src/index.ts`:
```typescript
const command = `C:/Path/To/python.exe "${scriptPath}" ${args.join(" ")}`;
```

Then rebuild:
```bash
npm run build
```

### Vector Search
To enable semantic search, configure Qdrant:
```bash
cd ../infrastructure
docker-compose up -d qdrant
```

## Success Indicators

You're ready when:
- ✅ `npm test` passes all checks
- ✅ Tools appear in Claude Desktop
- ✅ You can list frameworks/templates
- ✅ Context assembly works
- ✅ Knowledge search returns results

## Quick Command Reference

```bash
# Setup
npm install          # Install dependencies
npm run build        # Compile TypeScript
npm test            # Verify setup

# Development
npm run watch       # Auto-compile on changes

# Verification
python --version    # Check Python
node --version      # Check Node.js
```

---

**Ready to go?** Try: `List all frameworks` in Claude Desktop!
