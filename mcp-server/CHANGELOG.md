# Changelog

All notable changes to the Prompt Engineering MCP Server will be documented in this file.

## [1.0.0] - 2024-11-27

### Added

#### Core Tools
- **assemble_context** - Dynamic context assembly with 6 modes (planning, technical, analysis, communication, minimal, full)
- **search_knowledge** - Knowledge base search with configurable limits
- **list_frameworks** - Browse all thinking frameworks by category
- **list_templates** - Browse all production templates by category
- **get_framework** - Retrieve specific framework content
- **get_template** - Retrieve specific template content
- **capture_output** - Save successful outputs for learning

#### Infrastructure
- TypeScript implementation with MCP SDK 0.6.0
- Automatic compilation from TypeScript to JavaScript
- Integration with existing Python context-loader.py script
- File-based knowledge search (keyword matching)
- Recursive framework and template discovery

#### Developer Experience
- Comprehensive README with installation instructions
- Usage examples documentation
- Windows setup script (setup.bat)
- Claude Desktop configuration example
- TypeScript watch mode for development
- Detailed error messages and validation

#### Documentation
- Installation guide
- Tool reference
- Usage examples for all tools
- Troubleshooting section
- Integration patterns
- Common workflows

### Technical Details

#### Dependencies
- @modelcontextprotocol/sdk ^0.6.0
- TypeScript ^5.6.0
- Node.js 22.x

#### Supported Modes
- `planning` - Strategic decisions with planning frameworks
- `technical` - Technical implementation with code patterns
- `analysis` - Deep thinking with analysis frameworks
- `communication` - Writing and client communication
- `minimal` - Task only, no additional context
- `full` - Comprehensive context (default)

#### Directory Structure
```
mcp-server/
├── src/
│   └── index.ts                          # Main server implementation
├── dist/                                 # Compiled output (generated)
├── package.json                          # Dependencies
├── tsconfig.json                         # TypeScript config
├── README.md                             # Installation guide
├── USAGE_EXAMPLES.md                     # Usage documentation
├── CHANGELOG.md                          # This file
├── setup.bat                             # Windows setup script
└── claude_desktop_config.example.json   # Config example
```

### Known Limitations

1. **Vector Search**: Currently uses keyword matching. Full semantic search requires Qdrant configuration.
2. **Platform**: Primarily tested on Windows. macOS/Linux paths may need adjustment.
3. **Python Dependency**: Requires Python 3.x in PATH for context assembly.

### Future Enhancements

Planned for future releases:

- [ ] Qdrant vector search integration
- [ ] Caching for frequently accessed frameworks/templates
- [ ] Support for custom context directories
- [ ] Advanced search filters (by category, tags, date)
- [ ] Workflow history tracking
- [ ] Export capabilities (PDF, HTML)
- [ ] Integration with Langfuse for tracking
- [ ] Multi-language support
- [ ] Real-time context suggestions

### Security

- Server runs locally only (stdio transport)
- No external network calls
- File access restricted to project directory
- No credential storage in code

### Performance

- Lazy loading of frameworks and templates
- Efficient file discovery with caching potential
- Minimal memory footprint (~10MB)
- Fast startup time (<1 second)

## Release Notes

### What's New in 1.0.0

This is the initial release of the Prompt Engineering MCP Server, making the entire prompt engineering system accessible directly from Claude Desktop.

**Key Features:**
- Zero-configuration context assembly for 6 different work modes
- Instant access to all frameworks and templates
- Knowledge base search
- Learning capture system

**Getting Started:**
1. Run `npm install && npm run build`
2. Add to Claude Desktop config
3. Restart Claude Desktop
4. Start using tools immediately

**Example First Steps:**
```
# Discover what's available
List all frameworks

# Try context assembly
Assemble context for planning mode with task "What should I prioritize this quarter?"

# Get a specific resource
Get the first-principles framework
```

### Upgrade Path

This is the initial release. Future versions will maintain backward compatibility with:
- Tool names and parameters
- File structure
- Configuration format

### Credits

Built with:
- Model Context Protocol by Anthropic
- Universal Prompt Engineering System architecture
- TypeScript and Node.js ecosystem

---

For detailed usage instructions, see [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md)
For installation help, see [README.md](README.md)
