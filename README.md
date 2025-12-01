# Universal Prompt Engineering System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive infrastructure for making every AI interaction better. Not a prompt library—a complete system that stores structured knowledge, provides thinking frameworks, assembles context dynamically, and routes to appropriate models.

## Features

| Feature | Description |
|---------|-------------|
| **Context Repository** | Structured knowledge about you, your business, and work patterns |
| **Thinking Frameworks** | 20+ frameworks for different types of cognitive work |
| **Production Templates** | Battle-tested prompts for recurring tasks |
| **Vector Search** | Semantic search across all your knowledge using Qdrant |
| **CLI Tools** | Bash and Python scripts for context assembly |
| **MCP Server** | Claude Desktop integration for automatic context loading |
| **Knowledge Scrapers** | Pull insights from Reddit and GitHub |
| **Cost Tracking** | Monitor API usage and costs |
| **Prompt Versioning** | Semantic versioning for your prompts |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/prompt-engineering-system.git
cd prompt-engineering-system

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Setup CLI
chmod +x scripts/prompt.sh
alias prompt='./scripts/prompt.sh'

# Test it
prompt status
prompt list-frameworks
prompt plan "What should my Q1 priorities be?"
```

## Directory Structure

```
prompt-engineering-system/
├── context/                    # Personal knowledge repository
│   ├── identity/               # Who you are, how you think
│   ├── business/               # Company, services, markets
│   ├── technical/              # Infrastructure, tools, patterns
│   ├── projects/               # Active and archived projects
│   └── learnings/              # What works, what doesn't
├── frameworks/                 # Thinking frameworks
│   ├── planning/               # first-principles, pre-mortem, constraints
│   ├── analysis/               # steelman, assumptions, root-cause
│   ├── decision/               # reversibility, regret-minimization
│   ├── technical/              # architecture, debugging
│   ├── prompting/              # chain-of-thought, few-shot, structured
│   └── communication/          # audience-adaptation
├── templates/                  # Production templates
│   ├── voice-ai/               # Receptionist, emergency handling
│   ├── development/            # Claude Code handoffs, n8n specs
│   ├── outreach/               # Cold emails, follow-ups
│   ├── client/                 # Proposals, SOPs
│   └── prompting/              # System prompt templates
├── scripts/                    # CLI and automation
│   ├── prompt.sh               # Main CLI tool
│   ├── context-loader.py       # Context assembly
│   ├── embed_context.py        # Vector embedding
│   ├── search_knowledge.py     # Semantic search
│   └── scrapers/               # Reddit/GitHub scrapers
├── chains/                     # Multi-stage prompt chains
├── workflows/                  # n8n workflow exports
├── outputs/                    # Generated outputs
├── tests/                      # Prompt testing (promptfoo)
├── docs/                       # Documentation
├── infrastructure/             # Docker configs (Qdrant, LiteLLM)
└── .claude/commands/           # Claude Code slash commands
```

## CLI Usage

### Basic Commands

```bash
# Full context planning (includes identity + business + technical)
prompt plan "Should I expand into HVAC market?"

# Quick question with minimal context
prompt quick "Best Docker network setup?"

# Use specific framework
prompt framework first-principles "Build vs buy decision"
prompt framework pre-mortem "Launch new product line"
prompt framework chain-of-thought "Debug authentication flow"

# Generate Claude Code handoff
prompt handoff "Build lead scoring workflow"

# List available resources
prompt list-frameworks
prompt list-templates
prompt status
```

### Advanced Commands

```bash
# Vector search across all context
prompt search "voice AI best practices"

# Assemble context for specific mode
prompt context full      # All context files
prompt context business  # Business context only
prompt context technical # Technical context only

# Run scrapers
python scripts/scrapers/scrape_and_ingest.py

# Embed new context files
python scripts/embed_context.py
```

## Frameworks

### Planning
- **first-principles.md** - Break down to fundamental truths
- **pre-mortem.md** - Imagine failure, work backwards
- **constraints-first.md** - Define boundaries before solutions

### Analysis
- **steelman.md** - Strongest version of opposing view
- **assumption-surfacing.md** - Find hidden assumptions
- **root-cause.md** - 5 Whys and fishbone analysis

### Prompting
- **chain-of-thought.md** - Step-by-step reasoning (+40-85% on complex tasks)
- **few-shot.md** - Example-based prompting
- **structured-prompting.md** - CARE, RTF, XML patterns

## Vector Search

```bash
# Start Qdrant
cd infrastructure && docker-compose up -d qdrant

# Embed all context files
python scripts/embed_context.py

# Search your knowledge base
python scripts/search_knowledge.py "voice AI error handling"
```

## Scrapers

Pull knowledge from Reddit and GitHub engineering communities:

```bash
# Configure in .env
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
GITHUB_TOKEN=your_token

# Run scrapers
python scripts/scrapers/scrape_and_ingest.py
```

**Sources:** r/PromptEngineering, r/ClaudeAI, r/LocalLLaMA, GitHub prompt-engineering repos

## Claude Code Integration

Place slash commands in `.claude/commands/`:

```bash
# Use frameworks directly
/plan "Should I pivot the product?"
/review "Check this architecture"
/handoff "Build the notification system"
```

## Infrastructure (Optional)

```bash
cd infrastructure
docker-compose up -d
```

- **LiteLLM** (port 4000): Unified API for all LLMs with fallbacks
- **Qdrant** (port 6333): Vector database for semantic search

## Customization

1. `context/identity/core-values.md` - Your principles
2. `context/business/corereceptionai-overview.md` - Your business
3. `context/technical/infrastructure-inventory.md` - Your setup
4. `frameworks/` - Add your own thinking frameworks
5. `templates/` - Add your recurring task templates

## Testing

```bash
npm install -g promptfoo
cd tests && promptfoo eval
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - See [LICENSE](LICENSE) for details.
